import logging

from ttapi import aenums, cppclient
from ttapi.cppclient import TT_INVALID_PRICE

from basis_validation import *
from basis_validation.order.conditions import *
from captain.lib.controlled_types import OrderRes

log = logging.getLogger(__name__)

__all__ = ['does_exchange_send_timestamp',
           'request_sent_to_exch',
           'is_unsolicited_delete',
           'was_triggered_in_last_action',
           'handling_is_native',
           'handling_is_synthetic',
           'order_in_gw_order_book',
           'is_order_sent_to_exchange',
           'is_gateway_reject',
           'is_exchange_reject',
           'order_status_was_hold',
           'is_replace_instead_of_change']

TFX_MAX_VOLUME = 9999998
def is_gateway_reject(action, before, after):
    if before.pending.order_restrict in [aenums.TT_ICEBERG_ORDER_RES]:
        return True

    if before.pending.order_restrict == aenums.TT_MINVOL_ORDER_RES:
        if before.pending.min_qty <= 0:
            return True

    if before.pending.order_type not in [aenums.TT_LIMIT_ORDER, aenums.TT_MARKET_ORDER, aenums.TT_CROSS_ORDER]:
        return True

    if before.pending.order_type == aenums.TT_CROSS_ORDER:
        if before.pending.order_restrict != OrderRes.NONE:
            return True

    if before.pending.buy_sell not in [aenums.TT_BUY, aenums.TT_SELL]:
        return True

    if before.pending.open_close not in [aenums.TT_OPEN, aenums.TT_CLOSE]:
        return True

    if before.pending.order_type != aenums.TT_MARKET_ORDER and (before.pending.limit_prc == 0 and (before.pending.srs.prod.prod_type == aenums.TT_PROD_FUTURE)):
        return True

    if before.pending.order_qty < 0 or before.pending.order_qty > TFX_MAX_VOLUME:
        return True

    #TODO: exch_trader doesn't match with logged in trader,then order rejected by exchange,
    #if before.pending.order_action == aenums.TT_ORDER_ACTION_ADD:
    #    if before.pending.exch_trader not in traders:
    #        return True
    if before.pending.order_status != aenums.TT_ORDER_STATUS_NEW:
        if after.pending.buy_sell != before.pending.buy_sell:
            return True

    if before.pending.order_action == aenums.TT_ORDER_ACTION_INQUIRE:
        return True

    if before.pending.order_action == aenums.TT_ORDER_ACTION_CHANGE:
        for field in [ 'order_type', 'order_restrict', 'order_flags', 'order_exp_date']:
            after_val = getattr(after.pending, field)
            before_val = getattr(before.pending, field)
            if before_val != after_val:
                log.info('after.pending.%s is %s and before.pending.%s is %s' % (field, after_val, field, before_val))
                return True
        if before.pending.chg_qty == 0 and before.pending.limit_prc == before.book.limit_prc and \
        after.pending.order_type != aenums.TT_MARKET_ORDER:
                log.info('before.pending.chg_qty is %d and before.pending.limit_prc is %d and after.pending.limit_prc is %d' % 
                            (before.pending.chg_qty, before.pending.limit_prc, after.pending.limit_prc))
                return True
        if before.pending.chg_qty + after.pending.wrk_qty < 0:
            log.info('after.pending.wrk_qty %d before.pending.chg_qty %d' % (after.pending.wrk_qty, before.pending.chg_qty))
            return True

    if before.pending.order_action == aenums.TT_ORDER_ACTION_REPLACE:
        if before.pending.chg_qty == 0 and before.pending.limit_prc == before.book.limit_prc and \
        after.pending.order_type != aenums.TT_MARKET_ORDER:
                log.info('before.pending.chg_qty is %d and before.pending.limit_prc is %d and after.pending.limit_prc is %d' % 
                            (before.pending.chg_qty, before.pending.limit_prc, after.pending.limit_prc))
                return True
        if before.pending.chg_qty + after.pending.wrk_qty < 0:
            log.info('after.pending.wrk_qty %d before.pending.chg_qty %d' % (after.pending.wrk_qty, before.pending.chg_qty))
            return True

    if before.pending.order_action == aenums.TT_ORDER_ACTION_DELALL:
        if isProxyLogin(before.pending):
            return True

    if before.pending.order_flags == aenums.TT_MARKET_TO_LIMIT_MOD_CODE:
        return True

    if before.pending.order_action == aenums.TT_ORDER_ACTION_DELETE \
     and before.book.order_action == aenums.TT_ORDER_ACTION_DELETE:
        return True

    if before.pending.order_action != aenums.TT_ORDER_ACTION_ADD \
     and before.pending.order_no == 0:
        return True

    if before.pending.order_action != aenums.TT_ORDER_ACTION_ADD \
     and before.pending.order_no == 0 or after.pending.order_no < 999999:
        return True

    if before.pending.limit_prc == cppclient.TT_INVALID_PRICE \
     and before.pending.order_type == aenums.TT_LIMIT_ORDER:
        return True

    if before.pending.order_status_modifier == aenums.TT_ORDER_STATUS_MODIFIER_PENDING_TRIGGER \
     and before.pending.buy_sell == aenums.TT_BUY \
     and before.pending.limit_prc < before.pending.stop_prc:
        return True

    if before.pending.order_status_modifier == aenums.TT_ORDER_STATUS_MODIFIER_PENDING_TRIGGER \
     and before.pending.buy_sell == aenums.TT_SELL \
     and before.pending.limit_prc > before.pending.stop_prc:
        return True

    if hasattr(action, 'order_status'):
        if action.order_status == 'Risk Reject':
            return True

    return False

def is_exchange_reject(action, before, after):
    return( basis_order_conditions.is_order_status_reject(action, before, after) and
            not is_gateway_reject(action, before, after) )

def is_order_sent_to_exchange(action, before, after):
    if is_risk_reject(action, before, after):
        return False
    if ((after.pending.order_action == aenums.TT_ORDER_ACTION_ADD or
         after.pending.order_action == aenums.TT_ORDER_ACTION_INQUIRE or
         (after.pending.order_action == aenums.TT_ORDER_ACTION_CHANGE and not
          (after.pending.order_status == aenums.TT_ORDER_STATUS_REJECTED and
           is_gateway_reject(action, before, after))) or
         after.pending.order_action == aenums.TT_ORDER_ACTION_RESUBMIT ) and
          ( after.pending.order_status == aenums.TT_ORDER_STATUS_OK or
            (after.pending.order_status == aenums.TT_ORDER_STATUS_REJECTED and
             is_exchange_reject(action, before, after)) ) or
           ( after.pending.order_action == aenums.TT_ORDER_ACTION_HOLD and
             after.pending.order_status == aenums.TT_ORDER_STATUS_HOLD ) or
             ( after.pending.order_action == aenums.TT_ORDER_ACTION_DELETE and
               after.pending.order_status == aenums.TT_ORDER_STATUS_OK and not
               is_book_order_status_hold(action, before, after) ) or
                (after.pending.order_action == aenums.TT_ORDER_ACTION_HOLD and
                 after.pending.order_status == aenums.TT_ORDER_STATUS_DELETED and
                 is_exchange_reject(action, before, after))
                ):

        return True
    return False

def does_exchange_send_timestamp(action, before, after):
      return is_order_sent_to_exchange(action, before, after)

def request_sent_to_exch(action, before, after):
    return not(is_gateway_reject(action, before, after) \
        or (before.pending.order_status == aenums.TT_ORDER_STATUS_HOLD \
            and before.pending.order_action != aenums.TT_ORDER_ACTION_RESUBMIT))

def is_unsolicited_delete(action, before, after):
    return after.pending.order_action == aenums.TT_ORDER_ACTION_DELETE \
        and after.pending.order_action_orig not in(aenums.TT_ORDER_ACTION_DELETE,
                                                   aenums.TT_ORDER_ACTION_REPLACE)

def was_triggered_in_last_action(action, before, after):
    #NEED THIS ACTION DUE TO A BUG IN THE GW MOST LIKELY
    return before.book \
      and before.book.status_history == aenums.TT_STATUS_HISTORY_TRIGGERED \
      and before.book.order_action == aenums.TT_ORDER_ACTION_CHANGE \
      and before.book.order_status == aenums.TT_ORDER_STATUS_OK \
      and before.book.order_no == before.book.order_no_old

def handling_is_native(action, before, after):
    return (before.pending.handling == aenums.TT_NATIVE)

def handling_is_synthetic(action, before, after):
    return (before.pending.handling == aenums.TT_SYNTHETIC)

def order_in_gw_order_book(action, before, after):
    from pyrate.ttapi.manager import TTAPIManager
    os = TTAPIManager().getOrderSession()
    try:
        os.getOrderFromNumber(before.pending.order_no)
        return True
    except:
        return False

#def batchPolicies_is_seven(action, before, after):
#    return before.pending.batch_policies == 7

def order_status_was_hold(action, before, after):
    try:
        return before.book.order_status == aenums.TT_ORDER_STATUS_HOLD
    except AttributeError:
        return False

def is_replace_instead_of_change(action, before, after):
    if (before.pending.order_action == aenums.TT_ORDER_ACTION_CHANGE and
        before.pending.order_status == aenums.TT_ORDER_ACTION_HOLD and
        before.pending.chg_qty > 0):
        return True
    return False
    
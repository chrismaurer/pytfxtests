from captain.plugins.validator import not_

from basis_validation import basis_order_conditions, basis_order_roundtrip
from basis_validation.order.order_validator import srvr_vrmf
from basis_validation.order import roundtrip

import roundtrip_rules as tfx_order_roundtrip
import conditions as tfx_order_conditions
#from tfx.validation.order.conditions import *

__all__ = ['setup_order']

def setup_order(order_table):
    
    '''
    Steps to view available validation options:
    Start a python intrepreter (python -i) with your PYTHONPATH set as if you're running automation.
    type:  from basis_validation import order
    type:  from pprint import pprint
    
    To see all available rules:
    pprint( dir( order.roundtrip ) )
    
    To see all available conditions:
    pprint( dir( order.conditions ) )
    '''

    core_enums_table = order_table.get_rule('roundtrip').get_rule('core_enums')
    date_and_time_table = order_table.get_rule('roundtrip').get_rule('date_and_time')
    ids_table = order_table.get_rule('roundtrip').get_rule('ids')
    misc_table = order_table.get_rule('roundtrip').get_rule('misc')
    prices_table = order_table.get_rule('roundtrip').get_rule('prices')
    trader_info_table = order_table.get_rule('roundtrip').get_rule('trader_info')

    ##################
    # ## Conditions ##
    ##################
    # replaces
    order_table.replace_condition('is_gateway_reject', tfx_order_conditions.is_gateway_reject)
    order_table.replace_condition('is_exchange_reject', tfx_order_conditions.is_exchange_reject)
    order_table.replace_condition('is_order_sent_to_exchange', tfx_order_conditions.is_order_sent_to_exchange)
    order_table.replace_condition('does_exchange_send_timestamp', tfx_order_conditions.does_exchange_send_timestamp)

    # from Basis
    order_table.add_condition(basis_order_conditions.is_order_status_delete)
    # from TFX
    order_table.add_condition(tfx_order_conditions.handling_is_native)
    order_table.add_condition(tfx_order_conditions.handling_is_synthetic)
    order_table.add_condition(tfx_order_conditions.order_status_was_hold)

    ##################
    # ## Core Enums ##
    ##################

    # order_restrict
    core_enums_table.add_rule(basis_order_roundtrip.order_restrict_is_ioc, cond='False')
    core_enums_table.add_rule(tfx_order_conditions.handling_is_native, cond='handling_is_native')
    core_enums_table.add_rule(tfx_order_conditions.handling_is_synthetic, cond='handling_is_synthetic')

    #####################
    # ## Date and Time ##
    #####################
    if srvr_vrmf.version == 7 and srvr_vrmf.release == 17 and srvr_vrmf.modification < 7:
        date_and_time_table.add_rule(time_exch_is_tfx_exchange_time, cond='False')
        date_and_time_table.optout_rule('time_exch_is_exchange_time','is_order_sent_to_exchange and does_exchange_send_timestamp', 'time_exch_is_tfx_exchange_time','exch does not send it ')

    ##################
    # ##    Ids     ##
    ##################
    # exchange_order_id
    ids_table.add_rule(basis_order_roundtrip.exchange_order_id_is_not_empty,
                       cond='not (is_order_status_hold or is_order_action_hold\
                            or is_book_order_status_hold or is_order_status_reject)')
    ids_table.append_condition('exchange_order_id_is_not_empty', cond='is_order_action_resubmit and is_order_status_ok')
    ids_table.add_rule(basis_order_roundtrip.exchange_order_id_is_exchange_order_id_book,
                       cond='(order_status_was_hold and not is_order_action_resubmit)\
                            or (is_order_action_delete and not is_order_status_reject)')
    ids_table.append_condition('exchange_order_id_is_exchange_order_id_book',
                               cond='(order_status_was_hold and not is_order_action_resubmit)\
                                    or (is_order_action_delete and not is_order_status_reject)')

    # order_no
    ids_table.add_rule(basis_order_roundtrip.order_no_is_not_zero, cond='not is_order_status_reject')
    ids_table.add_rule(basis_order_roundtrip.order_no_is_order_no_sent, cond='is_order_status_reject and not (is_order_action_add and (is_exchange_reject or is_gateway_reject))')
    ids_table.add_rule(basis_order_roundtrip.order_no_is_zero, cond='False')
    
    # order_key
    ids_table.add_rule(basis_order_roundtrip.order_key_is_not_order_key_sent, cond='False')

    # order_no_old
    ids_table.add_rule(basis_order_roundtrip.order_no_old_is_zero, cond='False')
    ids_table.add_rule(basis_order_roundtrip.order_no_old_is_order_no_old_book, cond='False')
    ids_table.add_rule(not_(basis_order_roundtrip.order_no_old_is_order_no_received), 'order_no_old_is_not_order_no_received', 'False')

#    ids_table.add_rule(basis_order_roundtrip.order_no_old_is_order_no_old_book, cond='False')
#    ids_table.append_condition('order_no_old_is_order_no_sent', cond='is_order_status_reject and not (is_order_action_add and (is_exchange_reject or is_gateway_reject))')
#    ids_table.append_condition('order_no_old_is_order_no_sent', cond='is_order_action_orig_void')
    ids_table.optout_rule('order_no_old_is_order_no_sent', cond='is_order_action_update', new_rule='order_no_old_is_order_no_old_book')

    ##################
    # ##    Misc    ##
    ##################
    # exchange_credentials
    misc_table.replace_rule('exchange_credentials_is_populated', tfx_order_roundtrip.exchange_credentials_is_populated)
    misc_table.override_rule('exchange_credentials_is_empty',
                             'not is_order_sent_to_exchange and not (is_order_action_update and not (is_order_status_reject))',\
							 654321, note='The Order Session\'s ITM is sent as exchange credentials. Is this right?')

    

    ##################
    # ##   Prices   ##
    ##################
    # limit_prc
    prices_table.append_condition('limit_prc_is_limit_prc_sent', 'not is_order_action_delete or (is_order_action_delete and (is_order_status_reject or is_order_status_delete))')

    ###################
    # ## Trader Info ##
    ###################
    # origin
    trader_info_table.add_rule(basis_order_roundtrip.origin_is_empty, cond='not is_order_status_reject')

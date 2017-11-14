#Python Imports
import time

# Captain Imports
from ttapi import aenums
from captain.lib import Override, WaitForLastPricesOnTradeDataUpdateNoDuplicateCallbackCheck, ChangeAsCancelReplace
from captain.lib.price.actions import SetCurrentLastPrices
from captain.core import implements, Action

TFXOverrides = []

@implements(SetCurrentLastPrices)
class TFXSetCurrentLastPrices(Action):
    def run(self, ctx):

        prices = ctx.price_session.getPrices(ctx.contract)
        for price_id, price_value in prices.items():
            ctx.price_dict[price_id] = price_value.value
        #GetTradeData is only needed for contracts in PFX mode
        #because TTQ is correct from getPrices and
        #contracts in TTAPI mode do not have updates for
        #TradeDirection
        prc_tbl_rec_handle = ctx.price_session.getStrike(ctx.contract)
        if ctx.price_session.consumer.IsPFX_Series(prc_tbl_rec_handle):
            # sleeping here for new EMDI behavior (we can do a wait for non-trade data update instead)
            time.sleep(10)
            if ctx.price_session.consumer.GetTradeData(ctx.contract) is not None:
                last_prices = \
                ctx.price_session.consumer.GetTradeData(ctx.contract).LastPrices()
                ctx.price_dict['TradeDirection'] = last_prices.GetLastTradeDirection()
                ctx.price_dict[aenums.TT_LAST_TRD_PRC] = last_prices.GetLastTradedPrice()
                ctx.price_dict[aenums.TT_LAST_TRD_QTY] = last_prices.GetLastTradedQty()
                ctx.price_dict[aenums.TT_TRADE_STATE] = last_prices.GetTradeState()
                ctx.price_dict[aenums.TT_TOTL_TRD_QTY] = last_prices.GetTotalTradedQty()

         #removing recursion for new EMDI behavior -- left in commented out old code per Shailesh's request
#        for idx, contract_ctx in enumerate(ctx.leg_contexts):
#            ctx.leg_contexts[idx] = self.run(contract_ctx)

        return ctx

class TFXChangeIncreaseQty(object):
    def __call__(self, action_type, arg_spec, test):
        check = True
        name = None
        merge_ctx_name = None
        # Walk up the list of actions from our current location looking for
        # SetOrderAttrs modifying the current context.
        for action in reversed(test.actions):
            at = type(action)
            if at.base_id == 'LoadCtx':
                name = action._key
                check = False
                continue
            elif at.base_id == 'StoreCtx' and (action._key == name or action._key == merge_ctx_name):
                check = True
                name = None
                continue
            elif at.base_id == 'MergeCtx':
                merge_ctx_name = action.other_ctx
                continue

            if check:
                if at.base_id == 'SetOrderAttr' and \
                     action.args['chg_qty'] > 0:
                        return True
        return False

    def __hash__(self):
        return hash(hash_value(self.__class__.__name__).hexdigest())

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.__class__.__name__

    __repr__ = __str__

    @property
    def signature(self):
        return str(self)

#TFXOverrides.append(Override(TFXSetCurrentLastPrices))
#TFXOverrides.append(Override(ChangeAsCancelReplace, TFXChangeIncreaseQty()))
TFXOverrides.append(Override(WaitForLastPricesOnTradeDataUpdateNoDuplicateCallbackCheck))
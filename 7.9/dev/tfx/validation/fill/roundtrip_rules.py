import operator

from ttapi import aenums, cppclient
from basis_validation.fill.utils import *
#from basis_validation.utils import compare
#from basis_validation.fill.roundtrip import merge_callbacks, iter_fills
#from basis_validation.fill.roundtrip import iter_fills

###################
# Core Enum Rules
###################
def fill_cmb_code_is_spread(action, before, after):
    actual = "rgetattr(fill, 'fill_cmb_code')"
    expected = "aenums.TT_FUTURE_SPREAD_COMB_ID"
    iter_fills(action, before, after, get_all_fill_callbacks(after), actual, expected)
    #iter_fills(action, before, after, actual, expected)

###################
# Date & Time Rules
###################

###################
# ID Rules
###################
#def non_legs_source_id_is_exch_member_plus_exch_trader_book_order(action, before, after):
def source_id_is_exch_member_plus_exch_trader_book_order_on_order_feed(action, before, after):
    actual = "rgetattr(fill, 'source_id')"
    expected = "'{0}.{1}'.format(rgetattr(after.book, 'exch_member'), rgetattr(after.book, 'exch_trader'))"
#    fills=[]
#    for cbk in after.callbacks:
#        if cbk.consumer == 'OrderConsumer':
#            fills.append(cbk.fill)
#        else:
#            fills.append(cbk.cpFill)
#    iter_fills(action, before, after, fills, actual, expected)
    iter_fills(action, before, after,get_all_fill_callbacks_on_order_feed(after), actual, expected)
               # get_all_non_leg_fill_callbacks(after)

###################
# Misc Field Rules
###################
def confirm_rec_record_no_is_default(action, before, after):
    actual = "rgetattr(fill, 'confirm_rec.record_no')"
    iter_fills(action, before, after,get_all_fill_callbacks(after) , actual, '-1')

def exchange_credentials_is_populated(action, before, after):
    iter_fills(action, before, after, get_all_leg_fill_callbacks(after),
               'fill.exchange_credentials', "''", operator.ne)
    
###################
# Quantity Rules
###################

###################
# Price Rules
###################

###################
# Series Info Rules
###################

###################
# Trader Info Rules
###################

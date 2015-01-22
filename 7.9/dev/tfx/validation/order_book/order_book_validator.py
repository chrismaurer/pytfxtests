#Pyrate Imports
from captain.plugins.validator import LockedDecisionTable, DTResultsException

#Commontests Imports
from basis_validation import *
## OrderBook Imports
from basis_validation import order_book
from basis_validation.validator import FullValidator
from .roundtrip_rules import *

from .conditions import *
from .roundtrip_rules import *


from tfx.validation.order.conditions import *
__all__ = ['setup_order_book']

def setup_order_book(order_book_table):
    
##    ##################
##    ## Order Action ##
##    ##################
##     
    # order_actions
    order_book_table.override_rule('exec_qty_is_exec_qty_book_all_orders','is_book_order_working or is_book_order_onhold',None)  
    # date_exch
    order_book_table.optout_rule('date_exch_is_date_exch_book_all_orders','is_book_order_working or is_book_order_onhold ',None)
    # time_exch
    order_book_table.optout_rule('time_exch_is_time_exch_book_all_orders','is_book_order_working or is_book_order_onhold',None)
    # exch_trans_no
    order_book_table.optout_rule('exch_trans_no_is_exch_trans_no_book_all_orders','is_book_order_working or is_book_order_onhold',None)

    ###################
    # Misc
    ###################
    # exchange_credentials
    order_book_table.replace_rule('exchange_credentials_is_populated_non_held_orders', exchange_credentials_is_populated_non_held_orders) 
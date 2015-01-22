# Pyrate Imports
from ttapi import aenums, cppclient

# Commontests Imports
from basis_validation.utils import compare

def get_all_add_held_orders(before):
    held_orders = {}
    for sok, order in before.book.items():
        if (before.book[sok].order_status == aenums.TT_ORDER_STATUS_HOLD and
           before.book[sok].order_action == aenums.TT_ORDER_ACTION_ADD):
            held_orders[sok] = order
    return held_orders   

def get_all_change_held_orders(before):
    held_orders = {}
    for sok, order in before.book.items():
        if (before.book[sok].order_status == aenums.TT_ORDER_STATUS_HOLD and
           before.book[sok].order_action == aenums.TT_ORDER_ACTION_CHANGE):
            held_orders[sok] = order
    return held_orders   
     
def get_all_hold_held_orders(before):
    held_orders = {}
    for sok, order in before.book.items():
        if (before.book[sok].order_status == aenums.TT_ORDER_STATUS_HOLD and
           before.book[sok].order_action == aenums.TT_ORDER_ACTION_HOLD):
            held_orders[sok] = order
    return held_orders 
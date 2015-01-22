import logging, operator

from ttapi import aenums, cppclient

from basis_validation.utils import compare, get_core_vrmf

vlog = logging.getLogger('validator')

# Helper function to validate the agile data


###########################################
# Order Action Rules
###########################################

def order_action_is_add_held_orders(action, before, after):
    iter_orders(action, before, after, get_all_add_held_orders(before),
                'after.book[sok].order_action', 'aenums.TT_ORDER_ACTION_ADD')
    
def order_action_is_change_held_orders(action, before, after):
    iter_orders(action, before, after, get_all_change_held_orders(before),
                'after.book[sok].order_action', 'aenums.TT_ORDER_ACTION_CHANGE')

def order_action_is_hold_to_held_orders(action, before, after):
    iter_orders(action, before, after, get_all_hold_held_orders(before),
                'after.book[sok].order_action', 'aenums.TT_ORDER_ACTION_HOLD')

def exchange_credentials_is_populated_non_held_orders(action, before, after):
    iter_orders(action, before, after, get_all_non_held_orders(before),
                'after.book[sok].exchange_credentials', "''", op=operator.ne) 

import logging

from tfx.validation.order_book.utils import *

log = logging.getLogger(__name__)


###########################################
# Order OnHold Conditions
###########################################
def is_book_order_addonhold(action, before, after):
    if get_all_add_held_orders(before):
        return True
    return False

def is_book_order_changeonhold(action, before, after):
    if get_all_change_held_orders(before):
        return True
    return False

def is_book_order_holdonhold(action, before, after):
    if get_all_hold_held_orders(before):
        return True
    return False


   
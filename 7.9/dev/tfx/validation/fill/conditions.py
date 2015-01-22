import logging

from ttapi import aenums, cppclient

# commontests imports
from basis_validation import basis_order_conditions

log = logging.getLogger(__name__)

__all__ = ['srs_prod_type_is_spread']

# CommonTests Imports
from basis_validation import *

################################
##### SUPER CONDITIONS #########
################################

###################################
# Reject distinguishing conditions
###################################

###########################################
########## TTAPI CONDITIONS ###############
###########################################
def srs_prod_type_is_spread(action, before, after):
    return before.pending.srs.prod.prod_type == aenums.TT_PROD_FSPREAD

###########################################
######## PROTOCOL CONDITIONS ##############
###########################################

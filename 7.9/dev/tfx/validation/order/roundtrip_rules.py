import operator, sys
from ConfigParser import SafeConfigParser

# commontests imports
from basis_validation.order.roundtrip import time_exch_is_exchange_time
from basis_validation.utils import compare

__all__ = []  # populated at the bottom of this module

###################
# Core Enum Rules
###################

###################
# ID Rules
###################

###################
# Quantity Rules
###################

###################
# Price Rules
###################

###################
# Date & Time Rules
###################
def time_exch_is_tfx_exchange_time(action, before, after, tzone_offset=9, time_threshold=300):
    time_exch_is_exchange_time(action, before, after, tzone_offset, time_threshold)
    
###################
# Trader Info Rules
###################

###################
# Series Info Rules
###################

###################
# Misc
###################

_exchange_credentials = None
def get_exchange_credentials():
    global _exchange_credentials
    if not _exchange_credentials:
        from pyrate import Manager
        filename = "{0}\{1}hostinfo.cfg".format(Manager.getOrderServer().mappedConfigDir,
                                                Manager.getGateway().name)
        parser = SafeConfigParser()
        parser.read([filename])

        for section in parser.sections():
            if section.startswith('OrderServerSession_1'):
                _exchange_credentials = "{0}".format(parser.get(section, 'ITC')) + '-' + "{0}".format(parser.get(section, 'SenderCompID')) + '-TIF' 
    return _exchange_credentials

###################
# Misc
###################
def exchange_credentials_is_populated(action, before, after):
    compare(after.pending.exchange_credentials, get_exchange_credentials(), operator.eq)

#############################################
## Populate __all__ module level attribute ##
#############################################
this_mod = sys.modules[__name__]
for attr in dir(this_mod):
    attr_val = getattr(this_mod, attr)
    if not attr.startswith('_') and \
      (hasattr(attr_val, '__module__') and attr_val.__module__ == __name__):
        __all__.append(attr)
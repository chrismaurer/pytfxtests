import logging

from captain import *

from commontests import *
from commontests.test_fill_server_template import BaseTestFillModification

from tfx.tests.utils import mf_config, futures_filter

log = logging.getLogger(__name__)

class TestFillModification(BaseTestFillModification):
    def __init__(self, scenario=rollover_down_with_auto_sod_true, mf_config=mf_config,
                 prod_types=futures_filter, timeout=200):
        super(TestFillModification, self).__init__(scenario, mf_config, prod_types,
                                                              timeout=200)
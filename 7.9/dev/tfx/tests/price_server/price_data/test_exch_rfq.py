from captain.lib.controlled_types import Worker

from commontests.price_server.templates.test_exch_rfq_template import BaseTestRFQ
from commontests.utils import register_crews

from tfx.tests.utils import *

class TestRFQAllProducts(BaseTestRFQ):

    def __init__(self):

        super(TestRFQAllProducts, self).__init__()
        register_crews(Worker.DIRECT)

        self.market_config_and_filters = [(mf_config, [futures_filter, fspread_filter, option_filter])]

        self.Aconfig_settings = [{PFX_enabled : 'true'}]

        self.rfq_qtys = [1,
                         10,
                         99999,
                         999999
                         ]

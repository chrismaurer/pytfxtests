from captain.lib.controlled_types import Worker

from commontests.price_server.templates.test_exch_ntd_time_sales_template import BaseTestNTDTimeAndSales
from commontests.utils import register_crews

from tfx.tests.utils import *

# Overrides
from tfx.tests.overrides import TFXOverrides

class TestNTDTimeAndSalesAllProducts(BaseTestNTDTimeAndSales):

    def __init__(self):

        super(TestNTDTimeAndSalesAllProducts, self).__init__()
        register_crews(Worker.DIRECT)

        self.market_config_and_filters = [(mf_config, [futures_filter, fspread_filter, option_filter])]

        self.accumulate_ltq_and_Aconfig_settings = [(False, {PFX_enabled : 'true', accumulate_ltq : '1', EchoCount : '0'}),
                                                    (True, {PFX_enabled : 'true', accumulate_ltq : '0', EchoCount : '0'})]

        self.overrides=TFXOverrides

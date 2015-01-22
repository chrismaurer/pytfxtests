from captain.lib import SetSessions
from captain.lib.controlled_types import Worker

# GW and Commontests Imports
from commontests.utils import register_crews
from commontests.price_server.templates.test_exch_smoke_test_template import (BaseTestAggregateDepthSmoke,
                                                                              BaseInsideMarketDepthSmoke,
                                                                              BaseTestNTDTimeAndSalesSmoke,
                                                                              BaseTestVapSmoke)

from tfx.tests.utils import (mf_config, futures_filter, bounds_1_20, bounds_6_10, bounds_1_10)

# Overrides
from tfx.tests.overrides import TFXOverrides

__all__ = ['TestAggMarketSmoke', 'TestInsideMarketSmoke',
           'TestNTDTimeAndSalesFuturesSmoke', 'TestVAPSmoke']

class TestAggMarketSmoke(BaseTestAggregateDepthSmoke):

    def __init__(self):
        register_crews(Worker.DIRECT)

        super(TestAggMarketSmoke, self).__init__()

        self.tradable_price_tick_bounds = bounds_1_20
        self.orders_per_price_level_bounds = bounds_6_10
        self.order_round_lot_multiplier_bounds = bounds_1_10

        self.market_config_and_filters = [(mf_config, [futures_filter])]

        self.visible_levels = 10

class TestInsideMarketSmoke(BaseInsideMarketDepthSmoke):

    def __init__(self):
        register_crews(Worker.DIRECT)

        super(TestInsideMarketSmoke, self).__init__()

        self.tradable_price_tick_bounds = bounds_1_20
        self.orders_per_price_level_bounds = bounds_6_10
        self.order_round_lot_multiplier_bounds = bounds_1_10

        self.market_config_and_filters = [(mf_config, [futures_filter])]

        self.if_proxy = False

class TestNTDTimeAndSalesFuturesSmoke(BaseTestNTDTimeAndSalesSmoke):

    def __init__(self):
        register_crews(Worker.DIRECT)

        super(TestNTDTimeAndSalesFuturesSmoke, self).__init__()

        self.market_config_and_filters = [(mf_config, [futures_filter])]

        self.accumulate_ltq = False
        self.restart_timeout = 300
        self.overrides=TFXOverrides

class TestVAPSmoke(BaseTestVapSmoke):

    def __init__(self):
        register_crews(Worker.DIRECT)

        super(TestVAPSmoke, self).__init__()

        self.market_config_and_filters = [(mf_config, [futures_filter])]

        self.accumulate_ltq = False
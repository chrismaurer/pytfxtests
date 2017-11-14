from captain.lib.controlled_types import Worker

from commontests.price_server.templates.test_exch_aggregate_depth_template import BaseTestAggregateDepth
from commontests.utils import register_crews

from tfx.tests.utils import (mf_config, mf_option_config, option_filter,
                             bounds_1_35, bounds_5_10, bounds_1_10,
                             PFX_enabled, NumDepthLevels, EchoCount)

__all__ = ['TestAggregateDepthOptions']

class TestAggregateDepthOptions(BaseTestAggregateDepth):

    def __init__(self):

        super(TestAggregateDepthOptions, self).__init__()
        register_crews(Worker.DIRECT)

        self.market_config_and_filters = [(mf_option_config, [option_filter])]

        self.visible_levels_and_Aconfig_settings = [(20, {PFX_enabled : 'true', NumDepthLevels : '20', EchoCount : '0'})]

        self.tradable_price_tick_bounds = bounds_1_35
        self.orders_per_price_level_bounds = bounds_5_10
        self.order_round_lot_multiplier_bounds = bounds_1_10

        self.supports_chg_to_same_value = False
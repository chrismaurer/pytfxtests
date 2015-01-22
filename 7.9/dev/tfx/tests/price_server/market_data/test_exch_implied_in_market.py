from captain.lib.controlled_types import Worker

from commontests.price_server.templates.test_exch_implied_in_market_template import BaseTestImpliedInPrices
from commontests.utils import register_crews

from tfx.tests.utils import  (mf_config, spread_prod_type_implied_two_legged,
                             bounds_1_5, bounds_5_7, bounds_1_10)
from ttutil import PositiveIntegerBounds

__all__ = ['TestImpliedInPricesTwoLegged']

class TestImpliedInPricesTwoLegged(BaseTestImpliedInPrices):

    def __init__(self):

        super(TestImpliedInPricesTwoLegged, self).__init__()
        register_crews(Worker.DIRECT)

        self.market_config_and_filters = [(mf_config, spread_prod_type_implied_two_legged)]

        self.visible_levels_and_Aconfig_settings = [(1, {PFX_enabled : 'true', NumDepthLevels : '5', EchoCount : '0'})]

        self.tradable_price_tick_bounds = bounds_1_5
        self.orders_per_price_level_bounds = bounds_5_7
        self.order_round_lot_multiplier_bounds = bounds_1_10

        self.supports_chg_to_same_value = False
from commontests.price_server.templates.test_exch_implied_out_market_template import BaseTestImpliedOutPrices
from tfx.tests.utils import *
from ttutil import PositiveIntegerBounds

__all__ = ['TestImpliedOutPricesTwoLegged']

class TestImpliedOutPricesTwoLegged(BaseTestImpliedOutPrices):

    def __init__(self):

        super(TestImpliedOutPricesTwoLegged, self).__init__()
        register_crews(Worker.DIRECT)

        self.market_config_and_filters = [(mf_config, spread_prod_type_implied_two_legged)]

        self.visible_levels_and_Aconfig_settings = [(1, {PFX_enabled : 'true', NumDepthLevels : '5', EchoCount : '0'})]

        self.tradable_price_tick_bounds = PositiveIntegerBounds(1, 5)
        self.orders_per_price_level_bounds = PositiveIntegerBounds(5, 7)
        self.order_round_lot_multiplier_bounds = PositiveIntegerBounds(1, 10)

        self.supports_chg_to_same_value = False
        self.legs_for_implied_out = [0, 1]
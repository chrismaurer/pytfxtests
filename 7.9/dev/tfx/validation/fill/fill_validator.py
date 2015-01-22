# Pyrate Imports
#from captain.plugins.ninja import prune_table
# Pyrate Imports
from captain.plugins.validator import prune_table, not_
# CommonTests Imports
from basis_validation import *
from basis_validation import conditions as base_conditions
from basis_validation.fill import roundtrip as base_rules


# TFX Imports
from .conditions import *
from .roundtrip_rules import *

__all__ = ['setup_fill']

def setup_fill(fill_table):

    ##################
    # ## Conditions ##
    ##################
    # replaces

    # from Basis

    # from TFX
    fill_table.add_condition(srs_prod_type_is_spread)

    ##################
    # ## Core Enums ##
    ##################
    core_enums_table = fill_table.get_rule('roundtrip').get_rule('core_enums')


    # from Basis
    fill_table.add_condition(base_conditions.is_action_WaitForFillOnOrderFeed)
    # fill_cmb_code
#    core_enums_table.add_rule(basis_fill_roundtrip.fill_cmb_code_is_calendar, cond='False')
    core_enums_table.override_rule('fill_cmb_code_is_calendar', 'True', -137078, None, 'Returns TT_FUTURE_SPREAD_COMB_ID for Calendar spread')
#    core_enums_table.override_rule('fill_cmb_code_is_srs_comb_code_book_order', 'contract_has_legs and srs_prod_type_is_spread', -1,
#                                   'fill_cmb_code_is_spread', 'summary and leg fills have a fill_cmb_code of TT_FUTURE_SPREAD_COMB_ID when the series is a spread')

    #####################
    ### Date and Time ###
    #####################

    date_and_time_table = fill_table.get_rule('roundtrip').get_rule('date_and_time')
    date_and_time_table.add_rule(base_rules.order_time_is_time_sent_book_order_on_order_feed , cond='False')
    date_and_time_table.optout_rule('order_time_is_time_sent_book_order', 'is_action_WaitForFillOnOrderFeed',
                                    'order_time_is_time_sent_book_order_on_order_feed')


    ###########
    # ## IDs ##
    ###########
    ids_table = fill_table.get_rule('roundtrip').get_rule('ids')

    # exchange_order_id
    ids_table.add_rule(basis_fill_roundtrip.exchange_order_id_is_empty, cond='False')
    ids_table.add_rule(base_rules.exchange_order_id_is_exchange_order_id_book_order_on_order_feed , cond='False')
    ids_table.optout_rule('exchange_order_id_is_exchange_order_id_book_order', 'is_action_WaitForFillOnOrderFeed',
                          'exchange_order_id_is_exchange_order_id_book_order_on_order_feed')


    # isession
    ids_table.add_rule(not_(basis_fill_roundtrip.legs_isession_is_isession_book_order),
                       'legs_isession_is_not_isession_book_order', cond='does_contract_have_legs')
    ids_table.add_rule(basis_fill_roundtrip.non_legs_isession_is_isession_book_order, cond='False')
    #ids_table.override_rule('isession_is_isession_book_order', 'contract_has_legs', -1,
                            #'non_legs_isession_is_isession_book_order')

    # source_id

    ids_table.add_rule(source_id_is_exch_member_plus_exch_trader_book_order_on_order_feed, cond='False')
    #ids_table.add_rule(basis_fill_roundtrip.record_no_is_zero_on_order_feed, cond='False')
    #ids_table.override_rule('source_id_is_empty_on_order_feed','True', -1, None,
    #                        'source_id is a combination of exch_member and exch_trader')
    ids_table.override_rule('source_id_is_exch_member_plus_exch_trader_book_order_on_order_feed', 'True', -1, None,
                            'source_id is a combination of exch_member and exch_trader')
    #ids_table.override_rule('record_no_is_not_zero_on_order_feed','True', -1, None,'record_no is set to trans id from tradeid given by exch')

    ##############
    # ## Misc ##
    ##############
    misc_table = fill_table.get_rule('roundtrip').get_rule('misc')

    # exchange_credentials
    misc_table.replace_rule('exchange_credentials_is_populated', exchange_credentials_is_populated) 

    ##############
    # ## Prices ##
    ##############
    prices_table = fill_table.get_rule('roundtrip').get_rule('price')

#    prices_table.add_rule(basis_fill_roundtrip.cash_prc_is_zero, cond='False')
#    prices_table.override_rule('cash_prc_is_invalid_price', 'True', -1,
#                               'cash_prc_is_zero', 'cash_prc is set to 0 always for TFX')

    ##################
    # ## Quantities ##
    ##################
    quantities_table = fill_table.get_rule('roundtrip').get_rule('quantities')

    ###################
    # ## Series Info ##
    ###################
    series_info_table = fill_table.get_rule('roundtrip').get_rule('series_info')

    ###################
    # ## Trader Info ##
    ###################
    trader_info_table = fill_table.get_rule('roundtrip').get_rule('trader_info')

    # cntr_clg
    #trader_info_table.add_rule(basis_fill_roundtrip.cntr_clg_is_empty)
    #trader_info_table.override_rule('cntr_clg_is_not_empty', 'True', -1, 'cntr_clg_is_empty', 'cntr_clg is always empty for TFX')

    # cntr_party
    #trader_info_table.add_rule(basis_fill_roundtrip.cntr_party_is_empty, cond='False')
    #trader_info_table.override_rule('cntr_party_is_not_empty', 'True', -1, 'cntr_party_is_empty', 'cntr_party is always empty for TFX')
   # order_no
    ids_table.add_rule(base_rules.order_no_is_order_no_book_order_on_order_feed , cond='False')
    ids_table.optout_rule('order_no_is_order_no_book_order', 'is_action_WaitForFillOnOrderFeed',
                          'order_no_is_order_no_book_order_on_order_feed')


    # site_order_key
    ids_table.add_rule(base_rules.site_order_key_is_site_order_key_book_order_on_order_feed , cond='False')
    ids_table.optout_rule('site_order_key_is_site_order_key_book_order', 'is_action_WaitForFillOnOrderFeed',
                          'site_order_key_is_site_order_key_book_order_on_order_feed')

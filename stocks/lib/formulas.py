"""
This module contains functions to be used in order to calculate stock related formulas.
"""

from __future__ import division

import time

from functools import reduce


def calculate_dividend_yield(d, price):
    """
    :param d: dictionary with relevant stocks details
    :param price: float price
    :return: float
    """
    return _dividend_yield(d['last_dividend'], price)


def calculate_pe_ratio(d, price):
    """
    :param d: dictionary with relevant stocks details
    :param price: float price
    :return: float
    """
    return _pe_ratio(d['fixed_dividend'], price)


def calculate_volum_weighted_stock_price(records):
    """
    :param records: trade records per stock
    :return: float
    """
    last_trades = _get_last_trades(records)
    traded_prices = [l[3] for l in last_trades]
    quantities = [l[1] for l in last_trades]
    return _volum_weighted_stock_price(traded_prices, quantities)


def calculate_gbce_all_share_index(db):
    """
    :param db: entire db populated with stocks trades relevant data
    :return: float
    """
    prices = []
    for d in db:
        prices.extend([l[3] for l in db[d].get('records', [])])
    return _gbce_all_share_index(prices)


def _dividend_yield(last_dividend, price):
    try:
        result = last_dividend / price
    except ZeroDivisionError:
        return 'Given price is 0. Dividend Yield cannot be calculated'
    return result


def _pe_ratio(dividend, price):
    try:
        result = price / dividend
    except ZeroDivisionError:
        return 'Given dividend is 0. P/E Ratio cannot be calculated.'
    except TypeError:
        return 'Given dividend is None. P/E Ratio cannot be calculated'
    return result


def _volum_weighted_stock_price(traded_prices, quantities):
    quantities_sum = sum(quantities)
    sum_tradedp_quantities = sum([x*y for x, y in zip(traded_prices, quantities)])
    try:
        result = sum_tradedp_quantities / quantities_sum
    except ZeroDivisionError:
        return 'Given qantities add to 0. Volume wighted stock price cannot be calculated.'
    return result


def _gbce_all_share_index(prices):
    try:
        order = len(prices)
        multiplication = reduce((lambda x, y: x * y), prices)
        result = multiplication * (1 / float(order))
    except ZeroDivisionError:
        return 'Given prices argument empty.'
    except TypeError:
        return 'Given prices argument empty'
    return result


def _get_last_trades(trades):
    given_time = 900
    now = time.time()
    last_trades = filter(lambda l: now - l[0] <= given_time, trades)
    return last_trades

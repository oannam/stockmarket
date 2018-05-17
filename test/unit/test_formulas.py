"""
Module to unit test formulas module.
"""

from __future__ import print_function

import time
import unittest
import yaml

from stocks.lib import formulas


class TestFormulas(unittest.TestCase):

    def setUp(self):
        curr_test_case = self.id().split('.')[-1]

        last_trades = [
                [1526575101.733513, 2, 'buy', 200.0],
                [1526575109.240374, 1, 'buy', 300.0],
                [1526575117.03415, 5, 'sell', 100.0],
        ]
        if 'test_calculate_volum_weighted_stock_price' == curr_test_case:
            self.keep_address = formulas._get_last_trades
            formulas._get_last_trades = lambda x: last_trades
        if 'test_get_last_trades' == curr_test_case:
            self.keep_address = time.time
            time.time = lambda: 1526575117.03416

        with open('test/unit/sample_data.yml', 'r') as stream:
            self.simulated_db = yaml.load(stream)

        self.simulated_db['ALE']['records'] = []
        self.simulated_db['GIN']['records'] = []
        self.simulated_db['ALE']['records'].extend(
            [
                [1526575101.733513, 2, 'buy', 200.0],
                [1526575109.240374, 1, 'buy', 300.0],
                [1526575117.03415, 5, 'sell', 100.0],
            ]
        )
        self.simulated_db['GIN']['records'].extend(
            [
                [1526575101.733513, 2, 'buy', 200.0],
                [1526575109.240374, 3, 'sell', 300.0],
                [1526575117.03415, 4, 'buy', 100.0],
            ]
        )

    def tearDown(self):
        curr_test_case = self.id().split('.')[-1]

        if 'test_calculate_volum_weighted_stock_price' == curr_test_case:
            formulas._get_last_trades = self.keep_address
        if 'test_get_last_trades' == curr_test_case:
            time.time = self.keep_address

    def test_calculate_dividend_yield(self):
        self.assertEqual(formulas.calculate_dividend_yield(self.simulated_db['ALE'], 50), 0.46)

    def test_calculate_pe_ratio(self):
        self.assertEqual(
            formulas.calculate_pe_ratio(self.simulated_db['ALE'], 50),
            1666.6666666666667
        )

    def test_calculate_volum_weighted_stock_price(self):
        self.assertEqual(
            formulas.calculate_volum_weighted_stock_price(self.simulated_db['ALE']['records']),
            150.0
        )

    def test_calculate_gbce_all_share_index(self):
        self.assertEqual(
            formulas.calculate_gbce_all_share_index(self.simulated_db),
            6000000000000.0
        )

    def test_pe_ratio(self):
        self.assertEqual(formulas._pe_ratio(0.05, 120), 2400.0)
        self.assertEqual(
            formulas._pe_ratio(0, 120),
            'Given dividend is 0. P/E Ratio cannot be calculated.'
        )
        self.assertEqual(
            formulas._pe_ratio(None, 80),
            'Given dividend is None. P/E Ratio cannot be calculated'
        )

    def test_dividend_yield(self):
        self.assertEqual(formulas._dividend_yield(8, 60), 0.13333333333333333)
        self.assertEqual(
            formulas._dividend_yield(9, 0), 'Given price is 0. Dividend Yield cannot be calculated'
        )

    def test_volum_weighted_stock_price(self):
        self.assertEqual(
            formulas._volum_weighted_stock_price([50, 78, 90, 100], [1, 2, 3, 4]),
            87.6
        )
        self.assertEqual(
            formulas._volum_weighted_stock_price([50, 78, 90, 100], [0, 0, 0, 0]),
            'Given qantities add to 0. Volume wighted stock price cannot be calculated.'
        )

    def test_gbce_all_share_index(self):
        self.assertEqual(
            formulas._gbce_all_share_index([56, 89, 90, 100]),
            11214000.0
        )
        self.assertEqual(
            formulas._gbce_all_share_index([]),
            'Given prices argument empty'
        )
        self.assertEqual(
            formulas._gbce_all_share_index(None),
            'Given prices argument empty'
        )

    def test_get_last_trades(self):
        self.assertEqual(
            formulas._get_last_trades(self.simulated_db['GIN']['records']),
            [
                [1526575101.733513, 2, 'buy', 200.0],
                [1526575109.240374, 3, 'sell', 300.0],
                [1526575117.03415, 4, 'buy', 100.0],
            ]
        )

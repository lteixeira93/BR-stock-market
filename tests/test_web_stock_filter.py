# AAA - Arrange, Act, Assert - https://docs.pytest.org/en/7.1.x/explanation/anatomy.html#test-anatomy
# python -m coverage run -m pytest .\test_web_stock_filter.py ; python -m coverage html
import unittest

import pandas as pd

import settings
from web_stock_filter import WebStockFilter
from utils.config_parser import get_indicators_url


class TestWebStockFilter(unittest.TestCase):
    def setUp(self):
        self.empty_stocks_list = []
        self.stocks_filtered_dataframe = pd.read_pickle(settings.PICKLE_UT_FILTERED_FILEPATH)
        self.companies_stock_name_list = list(self.stocks_filtered_dataframe['Stock'])
        self.companies_stock_link_list = [
            get_indicators_url()
            + stock_check_link
            for stock_check_link in self.companies_stock_name_list
        ]
        self.companies_stock_invalid_link_list = [
            get_indicators_url()
            + stock_check_link + 'INVALID'
            for stock_check_link in self.companies_stock_name_list
        ]

    def test_request_invalid_thread_nums_link(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            WebStockFilter().check_bankruptcy(
                self.companies_stock_link_list,
                self.empty_stocks_list,
                -1,
                -1
            )
        self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()

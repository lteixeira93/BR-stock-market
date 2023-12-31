# AAA - Arrange, Act, Assert - https://docs.pytest.org/en/7.1.x/explanation/anatomy.html#test-anatomy
# python -m coverage run -m pytest .\test_local_stock_filter.py ; python -m coverage html
import itertools
import unittest
from collections import Counter
from unittest.mock import patch, PropertyMock

import pandas as pd

import settings
from dataframe_parser import DataframeParser
from local_stock_filter import LocalStockFilter
from web_driver import WebDriver


class TestLocalStockFilter(unittest.TestCase):
    def setUp(self):
        self.empty_stocks_list = []
        self.empty_dataframe = pd.DataFrame()

        # List after get_stocks_table()
        self.stocks_list = pd.read_pickle(settings.PICKLE_UT_FULL_LIST_FILEPATH)

        # Full dataframe after get_stocks_table()
        self.stocks_full_dataframe = pd.read_pickle(settings.PICKLE_UT_FULL_FILEPATH)

        # Full dataframe after prepare_dataframe()
        self.stocks_prepared_dataframe = pd.read_pickle(settings.PICKLE_UT_PREPARED_FILEPATH)

        # Dataframe after apply_financial_filters()
        self.stocks_filtered_dataframe_list = pd.read_pickle(settings.PICKLE_UT_FILTERED_FILEPATH)

        self.web_driver = WebDriver()
        self.dataframe_parser = DataframeParser(self.web_driver)
        self.stock_data_frame_renamed_drop = self.dataframe_parser.drop_and_rename_cols(self.stocks_full_dataframe)

    def tearDown(self):
        pass

    def test_extract_dataframe(self):
        """
        Ensures that extract_dataframe returns an instance of pd dataframe
        (Note: Not necessary to test built-in methods)
        """

        self.assertTrue(isinstance(self.dataframe_parser.extract_dataframe(self.stocks_list), pd.DataFrame))

    def test_extract_dataframe_from_empty_list(self):
        """Ensures that extract_dataframe raises SystemExit exception when empty list is received"""

        with self.assertRaises(SystemExit) as cm:
            self.dataframe_parser.extract_dataframe(self.empty_stocks_list)
        self.assertEqual(cm.exception.code, 1)

    def test_drop_unused_cols(self):
        """Ensures that dataframe not contains items to be dropped"""

        expected_drop_columns_list = self.dataframe_parser.drop_columns_list
        assert all([col not in self.stock_data_frame_renamed_drop.columns for col in expected_drop_columns_list])

    def test_rename_cols(self):
        """Ensures that columns in dataframe were renamed"""
        expected_renamed_columns_list = [
            'Stock', 'Price', 'EBIT_Margin_(%)', 'EV_EBIT', 'Dividend_Yield_(%)', 'Financial_Volume_(%)'
        ]
        assert all(col in self.stock_data_frame_renamed_drop.columns for col in expected_renamed_columns_list)

    def test_drop_rename_cols_empty_dataframe(self):
        """Ensures that drop_and_rename_cols raises SystemExit if an empty df is received"""
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            self.dataframe_parser.drop_and_rename_cols(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_drop_and_fill_nans_empty_dataframe(self):
        """Ensures that drop_and_fill_nans raises SystemExit if an empty df is received"""
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            self.dataframe_parser.drop_and_fill_nans(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_remove_invalid_chars(self):
        stock_merged_list = []
        has_invalid_chars = False
        stock_data_frame = self.dataframe_parser.drop_and_fill_nans(self.stock_data_frame_renamed_drop)
        stock_data_frame = self.dataframe_parser.remove_invalid_chars(stock_data_frame)
        stock_merged_list.append(stock_data_frame['EBIT_Margin_(%)'].tolist())
        stock_merged_list.append(stock_data_frame['Dividend_Yield_(%)'].tolist())
        stock_merged_list = list(itertools.chain.from_iterable(stock_merged_list))

        for ch in stock_merged_list:
            if ch == 0:
                pass
            elif '%' in ch or '.' in ch:
                has_invalid_chars = True

        self.assertFalse(has_invalid_chars)

    def test_remove_invalid_chars_empty_dataframe(self):
        """Ensures that remove_invalid_chars raises SystemExit if an empty df is received"""

        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            self.dataframe_parser.remove_invalid_chars(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_convert_data_type(self):
        """Ensures that convert_data_type convert data properly"""
        expected_types_list = ['object', 'float64', 'float64', 'float64', 'float64', 'int32']
        stock_data_frame = self.dataframe_parser.drop_and_fill_nans(self.stock_data_frame_renamed_drop)
        stock_data_frame = self.dataframe_parser.remove_invalid_chars(stock_data_frame)
        stock_data_frame = self.dataframe_parser.convert_data_type(stock_data_frame)

        stock_data_frame_types_list = []
        dtypes_list = stock_data_frame.dtypes.tolist()

        for idx, _ in enumerate(dtypes_list):
            stock_data_frame_types_list.append(str(dtypes_list[idx]))

        self.assertCountEqual(expected_types_list, stock_data_frame_types_list)

    def test_convert_data_type_empty_dataframe(self):
        """Ensures that convert_data_type raises SystemExit if an empty df is received"""

        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            self.dataframe_parser.convert_data_type(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_replace_nans_by_zero_empty_dataframe(self):
        """Ensures that replace_nans_by_zero raises SystemExit if an empty df is received"""

        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            self.dataframe_parser.replace_nans_by_zero(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    @patch("web_driver.WebDriver.get_stocks_table")
    @patch("dataframe_parser.DataframeParser.prepare_dataframe")
    def test_drop_low_financial_volume(self, mocked_prepare_dataframe, mocked_get_stocks_table):
        """Ensures that Financial_Volume_(%) less than 1_000_000 is dropped"""

        has_negative_financial_volumes = False
        mocked_get_stocks_table.return_value = self.stocks_list
        mocked_prepare_dataframe.return_value = self.stocks_prepared_dataframe

        stock_data_frame = LocalStockFilter().drop_low_financial_volume(mocked_prepare_dataframe.return_value)
        stock_financial_volume_list = stock_data_frame['Financial_Volume_(%)'].tolist()

        for fv in stock_financial_volume_list:
            if fv < 1_000_000:
                has_negative_financial_volumes = True

        self.assertFalse(has_negative_financial_volumes)

    def test_drop_low_financial_volume_negative_value(self):
        """Ensures that drop_low_financial_volume raises SystemExit if negative financial volume is received"""

        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().drop_low_financial_volume(self.empty_dataframe, financial_volume=-1)
        self.assertEqual(cm.exception.code, 1)

    def test_drop_negative_profit_stocks(self):
        has_negative_profit_stocks = False
        stock_data_frame = self.dataframe_parser.prepare_dataframe(self.stocks_list)
        stock_data_frame = LocalStockFilter().drop_low_financial_volume(stock_data_frame)
        stock_data_frame = LocalStockFilter().drop_negative_profit_stocks(stock_data_frame)
        stock_financial_volume_list = stock_data_frame['EBIT_Margin_(%)'].tolist()

        for fv in stock_financial_volume_list:
            if fv < 0:
                has_negative_profit_stocks = True

        self.assertFalse(has_negative_profit_stocks)

    def test_drop_duplicated_stocks_by_financial_volume(self):
        has_duplicated_stocks_by_financial_volume = False
        stock_data_frame = self.dataframe_parser.prepare_dataframe(self.stocks_list)
        stock_data_frame = LocalStockFilter().drop_low_financial_volume(stock_data_frame)
        stock_data_frame = LocalStockFilter().drop_negative_profit_stocks(stock_data_frame)
        stock_data_frame = LocalStockFilter().drop_negative_profit_stocks(stock_data_frame)
        stock_data_frame = LocalStockFilter().drop_duplicated_stocks_by_financial_volume(stock_data_frame)

        # Gets stock names and financial volumes to map each other
        companies_stock_name_list = list(stock_data_frame['Stock'])
        companies_stock_fv_list = list(stock_data_frame['Financial_Volume_(%)'])
        companies_stock_name_largest_fv_dict = dict(map(
            lambda i, j: (i, j), companies_stock_name_list, companies_stock_fv_list))

        # Counter same companies (Same four letters in stock name) to compare the financial volume
        companies_similar_stock_counter_dict = dict(Counter(k[:4] for k in companies_stock_name_largest_fv_dict))

        for value in companies_similar_stock_counter_dict.values():
            if value > 1:
                has_duplicated_stocks_by_financial_volume = True
        self.assertFalse(has_duplicated_stocks_by_financial_volume)

    def test_drop_stocks_in_bankruptcy(self):
        # Mocking attribute within the class
        with (patch.object(LocalStockFilter, 'companies_in_bankruptcy_list', new_callable=PropertyMock)
              as attr_mock):
            settings.UNIT_TEST = True
            attr_mock.return_value = ['ALSO3']
            stock_data_frame = LocalStockFilter().drop_stocks_in_bankruptcy(self.stocks_filtered_dataframe_list)
            print(stock_data_frame['Stock'].tolist())

            self.assertFalse('ALSO3' in stock_data_frame['Stock'].tolist())

    def test_prepared_dataframe_empty_list(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            self.dataframe_parser.prepare_dataframe(self.empty_stocks_list)
        self.assertEqual(cm.exception.code, 1)

    @patch("web_driver.WebDriver.get_stocks_table")
    @patch('dataframe_parser.DataframeParser.prepare_dataframe')
    def test_applied_financial_filters_empty_dataframe(self, mocked_prepare_dataframe, mocked_get_stocks_table):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            mocked_get_stocks_table.return_value = self.stocks_list
            mocked_prepare_dataframe.return_value = pd.DataFrame()
            LocalStockFilter().apply_financial_filters(self.dataframe_parser)
        self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()

# AAA - Arrange, Act, Assert - https://docs.pytest.org/en/7.1.x/explanation/anatomy.html#test-anatomy
# python -m coverage run -m pytest .\test_dataframe_parser.py ; python -m coverage html
import itertools
import unittest

import pandas as pd

import settings
from dataframe_parser import DataframeParser
from web_driver import WebDriver


class TestDataFrameParser(unittest.TestCase):
    def setUp(self):
        self.empty_stocks_list = []
        self.empty_dataframe = pd.DataFrame()

        # List after WebDriver().get_stocks_table()
        self.stocks_list = pd.read_pickle(settings.PICKLE_UT_FULL_LIST_FILEPATH)

        # Full dataframe after WebDriver().get_stocks_table()
        self.stocks_full_dataframe = pd.read_pickle(settings.PICKLE_UT_FULL_FILEPATH)

        # Full dataframe after prepare_dataframe(stocks_list)
        self.stocks_prepared_dataframe = pd.read_pickle(settings.PICKLE_UT_PREPARED_FILEPATH)

        # Dataframe after apply_financial_filters(stocks_list)
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
        """Ensures that dataframe not contains items dropped"""

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

import itertools
import os.path
import tempfile
import unittest
from collections import Counter
from datetime import date
from unittest.mock import patch, PropertyMock

import pandas as pd

import settings
from FileManagerSheet import FileManagerXLSX
from LocalStockFilter import LocalStockFilter
from WebDriver import WebDriver
from WebStockFilter import WebStockFilter


class TestWebDriver(unittest.TestCase):

    def setUp(self):
        self.stock_web_driver = WebDriver()
        self.all_df_columns = ['Ação', 'Empresa', 'Preço', 'Data Preço', 'Data Dem.Financ.', 'Consolidação', 'ROTanC',
                               'ROInvC', 'RPL', 'ROA', 'Margem Líquida', 'Margem Bruta', 'Margem EBIT', 'Giro Ativo',
                               'Alav.Financ.', 'Passivo/PL', 'Preço/Lucro', 'Preço/VPA', 'Preço/Rec.Líq.', 'Preço/FCO',
                               'Preço/FCF', 'Preço/EBIT', 'Preço/NCAV', 'Preço/Ativo Total', 'Preço/Cap.Giro',
                               'EV/EBIT', 'EV/EBITDA', 'EV/Rec.Líq.', 'EV/FCO', 'EV/FCF', 'EV/Ativo Total',
                               'Div.Yield', 'Volume Financ.(R$)', 'Market Cap(R$)', '# Ações Total', '# Ações Ord.',
                               '# Ações Pref.']

    def test_stocks_table_has_all_columns(self):
        stocks_list = self.stock_web_driver.get_stocks_table()
        stocks_data_frame = pd.DataFrame(stocks_list[1])

        # Assertions for modified DataFrame
        self.assertEqual(stocks_data_frame.columns.tolist(), self.all_df_columns)

    def test_request_exception(self):
        # Mocking attribute within the class
        with patch.object(WebDriver, 'url', new_callable=PropertyMock) as attr_mock:
            with self.assertRaises(SystemExit) as cm:
                attr_mock.return_value = 'https://invalidwebdriverlink.com'
                WebDriver().get_stocks_table()
            self.assertEqual(cm.exception.code, 1)


class TestLocalStockFilter(unittest.TestCase):
    def setUp(self):
        self.empty_stocks_list = []
        self.empty_dataframe = pd.DataFrame()
        self.stocks_list = pd.read_pickle(settings.PICKLE_UT_FULL_LIST_FILEPATH)
        self.stocks_full_dataframe = pd.read_pickle(settings.PICKLE_UT_FULL_FILEPATH)
        self.stocks_prepared_dataframe = pd.read_pickle(settings.PICKLE_UT_PREPARED_FILEPATH)
        self.stocks_filtered_dataframe_list = pd.read_pickle(settings.PICKLE_UT_FILTERED_FILEPATH)
        self.drop_columns_list = LocalStockFilter().drop_columns_list
        self.renamed_columns_list = [
            'Stock', 'Price', 'EBIT_Margin_(%)', 'EV_EBIT', 'Dividend_Yield_(%)', 'Financial_Volume_(%)'
        ]

    def test_extract_dataframe(self):
        self.assertTrue(isinstance(LocalStockFilter().extract_dataframe(self.stocks_list), pd.DataFrame))

    def test_extract_dataframe_from_empty_list(self):
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().extract_dataframe(self.empty_stocks_list)
        self.assertEqual(cm.exception.code, 1)

    def test_drop_unused_cols(self):
        stock_data_frame = LocalStockFilter().drop_and_rename_cols(self.stocks_full_dataframe)
        assert all([col not in stock_data_frame.columns for col in self.drop_columns_list])

    def test_rename_cols(self):
        stock_data_frame = LocalStockFilter().drop_and_rename_cols(self.stocks_full_dataframe)
        assert all(col in stock_data_frame.columns for col in self.renamed_columns_list)

    def test_drop_rename_cols_empty_dataframe(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().drop_and_rename_cols(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_drop_and_fill_nans_empty_dataframe(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().drop_and_fill_nans(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_remove_invalid_chars(self):
        stock_merged_list = []
        has_invalid_chars = False
        stock_data_frame = LocalStockFilter().drop_and_rename_cols(self.stocks_full_dataframe)
        stock_data_frame = LocalStockFilter().drop_and_fill_nans(stock_data_frame)
        stock_data_frame = LocalStockFilter().remove_invalid_chars(stock_data_frame)
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
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().remove_invalid_chars(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_convert_data_type(self):
        expected_types_list = ['object', 'float64', 'float64', 'float64', 'float64', 'int32']
        stock_data_frame = LocalStockFilter().drop_and_rename_cols(self.stocks_full_dataframe)
        stock_data_frame = LocalStockFilter().drop_and_fill_nans(stock_data_frame)
        stock_data_frame = LocalStockFilter().remove_invalid_chars(stock_data_frame)
        stock_data_frame = LocalStockFilter().convert_data_type(stock_data_frame)

        stock_data_frame_types_list = []
        dtypes_list = stock_data_frame.dtypes.tolist()

        for idx, _ in enumerate(dtypes_list):
            stock_data_frame_types_list.append(str(dtypes_list[idx]))

        self.assertCountEqual(expected_types_list, stock_data_frame_types_list)

    def test_convert_data_type_empty_dataframe(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().convert_data_type(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_replace_nans_by_zero_empty_dataframe(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().replace_nans_by_zero(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_drop_low_financial_volume(self):
        has_negative_financial_volumes = False
        stock_data_frame = LocalStockFilter().prepare_dataframe(self.stocks_list)
        stock_data_frame = LocalStockFilter().drop_low_financial_volume(stock_data_frame)
        stock_financial_volume_list = stock_data_frame['Financial_Volume_(%)'].tolist()

        for fv in stock_financial_volume_list:
            if fv < 1_000_000:
                has_negative_financial_volumes = True

        self.assertFalse(has_negative_financial_volumes)

    def test_drop_low_financial_volume_negative_value(self):
        with self.assertRaises(SystemExit) as cm:
            stock_data_frame = LocalStockFilter().prepare_dataframe(self.stocks_list)
            LocalStockFilter().drop_low_financial_volume(stock_data_frame, financial_volume=-1)
        self.assertEqual(cm.exception.code, 1)

    def test_drop_negative_profit_stocks(self):
        has_negative_profit_stocks = False
        stock_data_frame = LocalStockFilter().prepare_dataframe(self.stocks_list)
        stock_data_frame = LocalStockFilter().drop_low_financial_volume(stock_data_frame)
        stock_data_frame = LocalStockFilter().drop_negative_profit_stocks(stock_data_frame)
        stock_financial_volume_list = stock_data_frame['EBIT_Margin_(%)'].tolist()

        for fv in stock_financial_volume_list:
            if fv < 0:
                has_negative_profit_stocks = True

        self.assertFalse(has_negative_profit_stocks)

    def test_drop_duplicated_stocks_by_financial_volume(self):
        has_duplicated_stocks_by_financial_volume = False
        stock_data_frame = LocalStockFilter().prepare_dataframe(self.stocks_list)
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
            LocalStockFilter().prepare_dataframe(self.empty_stocks_list)
        self.assertEqual(cm.exception.code, 1)

    def test_applied_financial_filters_empty_dataframe(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().apply_financial_filters(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)


class TestFileManagerSheet(unittest.TestCase):
    def setUp(self):
        self.empty_dataframe = pd.DataFrame()
        self.stocks_filtered_dataframe = pd.read_pickle(settings.PICKLE_UT_FILTERED_FILEPATH)

    def test_file_write(self):
        # Mocking attribute within the class
        with (patch.object(FileManagerXLSX, 'filename', new_callable=PropertyMock) as attr_mock):
            with tempfile.TemporaryDirectory() as temp_dir:
                print(temp_dir)
                attr_mock.return_value = temp_dir + "\\" + str(date.today()) + settings.XLSX_FILENAME
                print(attr_mock.return_value)
                FileManagerXLSX().store_on_disk(self.stocks_filtered_dataframe)

                self.assertTrue(os.path.exists(attr_mock.return_value))

    def test_file_write_empty_dataframe(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().apply_financial_filters(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)


class TestWebStockFilter(unittest.TestCase):
    def setUp(self):
        self.empty_stocks_list = []
        self.stocks_filtered_dataframe = pd.read_pickle(settings.PICKLE_UT_FILTERED_FILEPATH)
        self.companies_stock_name_list = list(self.stocks_filtered_dataframe['Stock'])
        self.companies_stock_link_list = [
            LocalStockFilter().indicators_partial_url
            + stock_check_link
            for stock_check_link in self.companies_stock_name_list
        ]
        self.companies_stock_invalid_link_list = [
            LocalStockFilter().indicators_partial_url
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

import itertools
import unittest
from unittest.mock import patch, PropertyMock

import pandas as pd

import settings
from LocalStockFilter import LocalStockFilter
from WebDriver import WebDriver


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

    def test_drop_and_fill_nans(self):
        stock_data_frame = LocalStockFilter().drop_and_rename_cols(self.stocks_full_dataframe)
        pass

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
        print(stock_merged_list)

        for ch in stock_merged_list:
            if ch == 0:
                continue
            elif '%' in ch or '.' in ch:
                has_invalid_chars = True
        self.assertFalse(has_invalid_chars)

    def test_remove_invalid_chars_empty_dataframe(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().remove_invalid_chars(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_convert_data_type(self):
        pass

    def test_convert_data_type_empty_dataframe(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().convert_data_type(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_replace_nans_by_zero(self):
        pass

    def test_replace_nans_by_zero_empty_dataframe(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().replace_nans_by_zero(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_drop_low_financial_volume(self):
        pass

    def test_drop_low_financial_volume_empty_dataframe(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().drop_and_rename_cols(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_drop_negative_profit_stocks(self):
        pass

    def test_drop_negative_profit_stocks_empty_dataframe(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().drop_and_rename_cols(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_sort_by_ev_ebit(self):
        pass

    def test_sort_by_ev_ebit_empty_dataframe(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().drop_and_rename_cols(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_drop_duplicated_stocks_by_financial_volume(self):
        pass

    def test_drop_duplicated_stocks_by_financial_volume_empty_dataframe(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().drop_and_rename_cols(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_drop_stocks_in_bankruptcy(self):
        pass

    def test_drop_stocks_in_bankruptcy_empty_dataframe(self):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            LocalStockFilter().drop_and_rename_cols(self.empty_dataframe)
        self.assertEqual(cm.exception.code, 1)

    def test_prepared_dataframe(self):
        pass


class TestFileManagerSheet(unittest.TestCase):
    def test_file_write(self):
        pass

    def test_file_exists(self):
        pass

    def test_file_write_empty_dataframe(self):
        pass


class TestWebStockFilter(unittest.TestCase):
    def test_request_exception_valid_link(self):
        pass

    def test_request_exception_non_valid_link(self):
        pass

    def test_request_exception_blank_link(self):
        pass


if __name__ == "__main__":
    unittest.main()

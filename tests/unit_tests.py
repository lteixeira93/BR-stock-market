import pandas as pd
import pytest

from WebDriver import WebDriver


class TestWebDriver(pytest.TestCase):

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
        pass


class TestLocalStockFilter(pytest.TestCase):
    def test_extract_dataframe(self):
        pass

    def test_extract_empty_dataframe(self):
        pass

    def test_drop_and_rename(self):
        pass

    def test_drop_and_rename_empty_dataframe(self):
        pass

    def test_drop_and_fill_nans(self):
        pass

    def test_drop_and_fill_nans_empty_dataframe(self):
        pass

    def test_remove_invalid_chars(self):
        pass

    def test_remove_invalid_chars_empty_dataframe(self):
        pass

    def test_convert_data_type(self):
        pass

    def test_convert_data_type_empty_dataframe(self):
        pass

    def test_replace_nans_by_zero(self):
        pass

    def test_replace_nans_by_zero_empty_dataframe(self):
        pass

    def test_drop_low_financial_volume(self):
        pass

    def test_drop_low_financial_volume_empty_dataframe(self):
        pass

    def test_drop_negative_profit_stocks(self):
        pass

    def test_drop_negative_profit_stocks_empty_dataframe(self):
        pass

    def test_sort_by_ev_ebit(self):
        pass

    def test_sort_by_ev_ebit_empty_dataframe(self):
        pass

    def test_drop_duplicated_stocks_by_financial_volume(self):
        pass

    def test_drop_duplicated_stocks_by_financial_volume_empty_dataframe(self):
        pass

    def test_drop_stocks_in_bankruptcy(self):
        pass

    def test_drop_stocks_in_bankruptcy_empty_dataframe(self):
        pass


class TestFileManagerSheet(pytest.TestCase):
    def test_file_write(self):
        pass

    def test_file_exists(self):
        pass

    def test_file_write_empty_dataframe(self):
        pass


class TestWebStockFilter(pytest.TestCase):
    def test_request_exception_valid_link(self):
        pass

    def test_request_exception_non_valid_link(self):
        pass

    def test_request_exception_blank_link(self):
        pass


if __name__ == "__main__":
    pytest.main()

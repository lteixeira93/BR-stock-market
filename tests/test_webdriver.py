# AAA - Arrange, Act, Assert - https://docs.pytest.org/en/7.1.x/explanation/anatomy.html#test-anatomy
import unittest
from unittest.mock import patch, PropertyMock

import pandas as pd

from web_driver import WebDriver


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


if __name__ == "__main__":
    unittest.main()

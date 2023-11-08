# AAA - Arrange, Act, Assert - https://docs.pytest.org/en/7.1.x/explanation/anatomy.html#test-anatomy
# python -m coverage run -m pytest .\test_webdriver.py ; python -m coverage html
import unittest
from datetime import datetime
from unittest.mock import patch, PropertyMock

import pandas as pd
import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache

from web_driver import WebDriver


class TestWebDriver(unittest.TestCase):

    def setUp(self):
        self.web_driver_obj = WebDriver()
        self.all_df_columns = ['Ação', 'Empresa', 'Preço', 'Data Preço', 'Data Dem.Financ.', 'Consolidação', 'ROTanC',
                               'ROInvC', 'RPL', 'ROA', 'Margem Líquida', 'Margem Bruta', 'Margem EBIT', 'Giro Ativo',
                               'Alav.Financ.', 'Passivo/PL', 'Preço/Lucro', 'Preço/VPA', 'Preço/Rec.Líq.', 'Preço/FCO',
                               'Preço/FCF', 'Preço/EBIT', 'Preço/NCAV', 'Preço/Ativo Total', 'Preço/Cap.Giro',
                               'EV/EBIT', 'EV/EBITDA', 'EV/Rec.Líq.', 'EV/FCO', 'EV/FCF', 'EV/Ativo Total',
                               'Div.Yield', 'Volume Financ.(R$)', 'Market Cap(R$)', '# Ações Total', '# Ações Ord.',
                               '# Ações Pref.']
        # Reducing number of requests, using keep-alive and improving performance by using Cache
        self.session = CacheControl(requests.Session(), cache=FileCache('.web_cache'))

    def test_stocks_table_has_all_columns(self):
        stocks_list = self.web_driver_obj.get_stocks_table()
        stocks_data_frame = pd.DataFrame(stocks_list[1])

        # Assertions for modified DataFrame
        self.assertEqual(stocks_data_frame.columns.tolist(), self.all_df_columns)

    def test_request_exception(self):
        # Mocking attribute within the class
        with patch.object(WebDriver, 'indicators_url', new_callable=PropertyMock) as attr_mock:
            with self.assertRaises(SystemExit) as cm:
                attr_mock.return_value = 'https://invalidwebdriverlink.com'
                WebDriver().get_stocks_table()
            self.assertEqual(cm.exception.code, 1)

    def test_update_indicators_reference_first_day_of_current_month(self):
        # Mocking attribute within the class
        with patch.object(WebDriver, attribute='current_date', new_callable=PropertyMock) as attr_mock:
            attr_mock.return_value = datetime.today().date().replace(day=1)
            self.web_driver_obj.update_indicators_url()
            print(self.web_driver_obj.updated_date)
        self.assertTrue(self.web_driver_obj.updated_date in self.web_driver_obj.indicators_url)

    def test_update_indicators_reference_not_first_day_of_current_month(self):
        # Mocking attribute within the class
        with patch.object(WebDriver, attribute='current_date', new_callable=PropertyMock) as attr_mock:
            attr_mock.return_value = datetime.today().date()
            self.web_driver_obj.update_indicators_url()
            print(self.web_driver_obj.updated_date)
        self.assertTrue(self.web_driver_obj.updated_date in self.web_driver_obj.indicators_url)

    def test_update_indicators_reference_first_day_of_current_month_valid_link(self):
        # Mocking attribute within the class
        with patch.object(WebDriver, attribute='current_date', new_callable=PropertyMock) as attr_mock:
            attr_mock.return_value = datetime.today().date().replace(day=1)
            self.web_driver_obj.update_indicators_url()

        print(self.web_driver_obj.indicators_url)
        response = self.session.get(self.web_driver_obj.indicators_url, headers=self.web_driver_obj.header)
        self.assertTrue(response.ok)

    def test_update_indicators_reference_not_first_day_of_current_month_valid_link(self):
        # Mocking attribute within the class
        with patch.object(WebDriver, attribute='current_date', new_callable=PropertyMock) as attr_mock:
            attr_mock.return_value = datetime.today().date()
            self.web_driver_obj.update_indicators_url()

        print(self.web_driver_obj.indicators_url)
        response = self.session.get(self.web_driver_obj.indicators_url, headers=self.web_driver_obj.header)

        self.assertTrue(response.ok)


if __name__ == "__main__":
    unittest.main()

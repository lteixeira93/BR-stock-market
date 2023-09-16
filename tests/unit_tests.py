import unittest

from WebDriver import WebDriver


class TestStockWebDriver(unittest.TestCase):

    def setUp(self):
        self.stock_web_driver = WebDriver()

    # def test_get_dummy_stocks_table(self):
    #     # Mock the apply_stocks_filter method
    #     with patch.object(self.stock_web_driver, 'apply_stocks_filter') as mock_apply_stocks_filter:
    #         self.stock_web_driver.get_dummy_stocks_table()
    #         mock_apply_stocks_filter.assert_called_once()

    # def test_apply_stocks_filter(self):
    #     # Create a sample DataFrame for testing
    #     sample_data = {'Ação': ['RRRP3', 'TTEN3', 'QVQP3B'],
    #                    'Preço': ['3213', '5454', '543'],
    #                    'Margem EBIT': ['1,83%', '43,83%', ''],
    #                    'EV/EBIT': ['13289', '1328', ''],
    #                    'Div.Yield': ['43,00%', '', '']}
    #     sample_df = pd.DataFrame(sample_data)
    #
    #     # Call the method and check if the DataFrame is correctly modified
    #     self.stock_web_driver.apply_stocks_filter(sample_df)
    #
    #     # Assertions for modified DataFrame
    #     self.assertEqual(sample_df.columns.tolist(), ['Stock', 'Price', 'EBIT_Margin', 'EV_EBIT', 'Dividend_Yield'])
    #     self.assertEqual(sample_df['EBIT_Margin'].tolist(), [1, 43, 0])
    #     self.assertEqual(sample_df['EV_EBIT'].tolist(), [13289, 1328, 0])
    #     self.assertEqual(sample_df['Dividend_Yield'].tolist(), [43, 0, 0])
    #
    # def test_get_stocks_table(self):


if __name__ == "__main__":
    unittest.main()

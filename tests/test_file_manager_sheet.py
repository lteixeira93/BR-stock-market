# AAA - Arrange, Act, Assert - https://docs.pytest.org/en/7.1.x/explanation/anatomy.html#test-anatomy
# python -m coverage run -m pytest .\test_file_manager.py ; python -m coverage html
import os.path
import tempfile
import unittest
from datetime import date
from unittest.mock import patch, PropertyMock

import pandas as pd

import settings
from dataframe_parser import DataframeParser
from file_manager_sheet import FileManagerXLSX
from local_stock_filter import LocalStockFilter
from web_driver import WebDriver


class TestFileManagerSheet(unittest.TestCase):
    def setUp(self):
        self.empty_dataframe = pd.DataFrame()

        # Dataframe after apply_financial_filters()
        self.stocks_filtered_dataframe = pd.read_pickle(settings.PICKLE_UT_FILTERED_FILEPATH)

        # Full dataframe after get_stocks_table()
        self.stocks_full_dataframe = pd.read_pickle(settings.PICKLE_UT_FULL_FILEPATH)

        # List after get_stocks_table()
        self.stocks_list = pd.read_pickle(settings.PICKLE_UT_FULL_LIST_FILEPATH)

        self.web_driver = WebDriver()
        self.dataframe_parser = DataframeParser(self.web_driver)
        self.stock_data_frame_renamed_drop = self.dataframe_parser.drop_and_rename_cols(self.stocks_full_dataframe)

    def test_file_write(self):
        # Mocking attribute within the class
        with (patch.object(FileManagerXLSX, 'filename', new_callable=PropertyMock) as attr_mock):
            with tempfile.TemporaryDirectory() as temp_dir:
                print(temp_dir)
                attr_mock.return_value = temp_dir + "\\" + str(date.today()) + settings.XLSX_FILENAME
                print(attr_mock.return_value)
                FileManagerXLSX().store_on_disk(self.stocks_filtered_dataframe)

                self.assertTrue(os.path.exists(attr_mock.return_value))

    @patch("web_driver.WebDriver.get_stocks_table")
    @patch('dataframe_parser.DataframeParser.prepare_dataframe')
    def test_file_write_empty_dataframe(self, mocked_prepare_dataframe, mocked_get_stocks_table):
        # The test will automatically fail if no exception / exception other than SystemExit is raised.
        with self.assertRaises(SystemExit) as cm:
            mocked_get_stocks_table.return_value = self.stocks_list
            mocked_prepare_dataframe.return_value = pd.DataFrame()
            LocalStockFilter().apply_financial_filters(self.dataframe_parser)
        self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()

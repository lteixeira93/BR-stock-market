# AAA - Arrange, Act, Assert - https://docs.pytest.org/en/7.1.x/explanation/anatomy.html#test-anatomy
import os.path
import tempfile
import unittest
from datetime import date
from unittest.mock import patch, PropertyMock

import pandas as pd

import settings
from file_manager_sheet import FileManagerXLSX
from local_stock_filter import LocalStockFilter


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


if __name__ == "__main__":
    unittest.main()

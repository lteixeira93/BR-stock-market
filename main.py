import warnings

import pandas as pd

import settings
from FileManagerCSV import FileManagerXLSX
from LocalStockFilter import LocalStockFilter
from WebDriver import WebDriver

warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    # TODO: Add try catch, multithreading, UT
    # Initialize globals
    # with CodeTimer("main program"):
    if not settings.PICKLE_DATAFRAME:
        stock_list = WebDriver().get_stocks_table()
        stocks_data_frame = LocalStockFilter().prepare_dataframe(stock_list)
        stocks_data_frame = LocalStockFilter().apply_financial_filters(stocks_data_frame)
        FileManagerXLSX().store_on_disk(stocks_data_frame)
    else:
        fake_stocks_data_frame = pd.DataFrame()
        LocalStockFilter().apply_financial_filters(fake_stocks_data_frame)
# end def


if __name__ == "__main__":
    main()

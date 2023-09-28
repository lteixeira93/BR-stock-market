import time
import warnings

import pandas as pd
from linetimer import CodeTimer

import settings
from FileManagerSheet import FileManagerXLSX
from LocalStockFilter import LocalStockFilter
from WebDriver import WebDriver

warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    with CodeTimer("main program"):
        if not settings.PICKLE_DATAFRAME:
            stocks_list = WebDriver().get_stocks_table()
            stocks_data_frame = LocalStockFilter().prepare_dataframe(stocks_list)
            stocks_data_frame = LocalStockFilter().apply_financial_filters(stocks_data_frame)
            FileManagerXLSX().store_on_disk(stocks_data_frame)
            time.sleep(5)
        else:
            empty_stocks_data_frame = pd.DataFrame()
            LocalStockFilter().apply_financial_filters(empty_stocks_data_frame)
# end def


if __name__ == "__main__":
    main()

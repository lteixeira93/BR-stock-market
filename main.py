import time
import warnings

import pandas as pd
from linetimer import CodeTimer

import settings
from dataframe_parser import DataframeParser
from file_manager_sheet import FileManagerXLSX
from local_stock_filter import LocalStockFilter
from web_driver import WebDriver

warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    with CodeTimer("main program"):
        if not settings.PICKLE_DATAFRAME:
            web_driver = WebDriver()
            dataframe_parser = DataframeParser(web_driver)
            local_stock_filter = LocalStockFilter()
            stocks_data_frame = local_stock_filter.apply_financial_filters(dataframe_parser)

            FileManagerXLSX().store_on_disk(stocks_data_frame)
            time.sleep(2)
        else:
            web_driver = WebDriver()
            dataframe_parser = DataframeParser(web_driver)
            local_stock_filter = LocalStockFilter()
            local_stock_filter.apply_financial_filters(dataframe_parser)


# end def


if __name__ == "__main__":
    main()

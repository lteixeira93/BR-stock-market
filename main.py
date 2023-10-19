import time
import warnings

from linetimer import CodeTimer

import settings
from dataframe_parser import DataframeParser
from file_manager_sheet import FileManagerXLSX
from local_stock_filter import LocalStockFilter
from web_driver import WebDriver

warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    with CodeTimer("main program"):
        web_driver = WebDriver()
        dataframe_parser = DataframeParser(web_driver)
        local_stock_filter = LocalStockFilter()
        stocks_data_frame = local_stock_filter.apply_financial_filters(dataframe_parser)

        if not settings.USE_PICKLE_DATAFRAME:
            FileManagerXLSX().store_on_disk(stocks_data_frame)
            time.sleep(2)
# end def


if __name__ == "__main__":
    main()

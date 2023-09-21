import warnings

from linetimer import CodeTimer

from FileManagerCSV import FileManagerXLSX
from LocalStockFilter import LocalStockFilter
from WebDriver import WebDriver

warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    # TODO: Add try catch, multithreading, UT
    with CodeTimer("main program"):
        stock_list = WebDriver().get_stocks_table()
        stocks_data_frame = LocalStockFilter().prepare_dataframe(stock_list)
        stocks_data_frame = LocalStockFilter().apply_financial_filters(stocks_data_frame)
        FileManagerXLSX().store_on_disk(stocks_data_frame)
# end def

if __name__ == "__main__":
    main()

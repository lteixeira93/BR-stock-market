import warnings

from FileManagerCSV import FileManagerXLSX
from LocalStockFilter import LocalStockFilter
from WebDriver import WebDriver

warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    # TODO: Add try catch, multithreading, UT
    stocks_data_frame = LocalStockFilter().prepare_dataframe(WebDriver().get_stocks_table())
    stocks_data_frame = LocalStockFilter().apply_financial_filters(stocks_data_frame)

    FileManagerXLSX().store_on_disk(stocks_data_frame)


if __name__ == "__main__":
    main()

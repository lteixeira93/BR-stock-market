import warnings

from LocalStockFilter import LocalStockFilter
from WebDriver import WebDriver
from utils.helper import print_full_dataframe

warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    # TODO: Add try catch, multithreading, UT
    stocks_list = WebDriver().get_stocks_table()
    stocks_data_frame = LocalStockFilter().prepare_dataframe(stocks_list)
    stocks_data_frame = LocalStockFilter().apply_financial_filters(stocks_data_frame)

    print_full_dataframe(stocks_data_frame)


if __name__ == "__main__":
    main()

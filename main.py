import warnings

import pandas as pd

from StockFilter import StockFilter
from WebDriver import WebDriver
from utils.helper import print_full_dataframe

warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    # TODO: Add try catch, multithreading, UT
    stock_web_driver = WebDriver()
    stocks_list = stock_web_driver.get_stocks_table()

    stocks_data_frame = pd.DataFrame(stocks_list[1])

    stocks_data_frame = StockFilter().prepare_dataframe(stocks_list)
    stocks_data_frame = StockFilter().apply_financial_filters(stocks_data_frame)

    print_full_dataframe(stocks_data_frame)


if __name__ == "__main__":
    main()

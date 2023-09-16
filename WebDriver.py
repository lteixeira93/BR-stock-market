import pandas as pd
import requests

from StockFilter import StockFilter
from utils.helper import print_full_dataframe


class WebDriver:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(WebDriver, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.__url: str = 'https://shorturl.at/hrGHQ'
        self.__user_agent: str = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/50.0.2661.75 Safari/537.36')
        self.__url_request_type: str = 'XMLHttpRequest'
        self.__header = {
            "User-Agent": self.__user_agent,
            "X-Requested-With": self.__url_request_type
        }

    def get_stocks_table(self) -> None:
        r"""
        Get HTML stock tables into a DataFrame object.

        Returns
        -------
        None.
        """
        response = requests.get(self.__url, headers=self.__header)
        stock_list = pd.read_html(response.text, decimal=',', thousands='.')
        stocks_data_frame = pd.DataFrame(stock_list[1])
        self.apply_stocks_filter(stocks_data_frame)

    @staticmethod
    def apply_stocks_filter(stocks_data_frame) -> None:
        r"""
        Filter stock tables list of DataFrame objects based on:
        Stock                    object
        Price                   float64
        EBIT_Margin_(%)         float64
        EV_EBIT                   int32
        Dividend_Yield_(%)      float64
        Financial_Volume_(%)      int32

        Returns
        -------
        None.
        """
        stocks_data_frame = StockFilter().filter_dataframe(stocks_data_frame)

        # First filter: Drop all Financial_Volume_(%) less than 1_000_000 R$ - Filter Ok
        stocks_data_frame.sort_values(by=['Financial_Volume_(%)'], inplace=True)
        stocks_data_frame.drop(stocks_data_frame[stocks_data_frame['Financial_Volume_(%)'] < 1_000_000].index,
                               inplace=True)

        # Second filter: Drop companies with negative or zero profit EBIT_Margin_(%)
        stocks_data_frame.sort_values(by=['EBIT_Margin_(%)'], inplace=True)
        stocks_data_frame.drop(stocks_data_frame[stocks_data_frame['EBIT_Margin_(%)'] < 0].index, inplace=True)

        # Third filter: Sort from the cheapest to expensive stocks EV_EBIT
        stocks_data_frame.sort_values(by=['EV_EBIT'], inplace=True)
        print_full_dataframe(stocks_data_frame)

from typing import List

import pandas as pd
import requests


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

    def get_stocks_table(self) -> List:
        r"""
        Get and convert stocks table from HTML into a `DataFrame` object.

        Return
        -------
        `List` of DataFrames
        """
        response = requests.get(self.__url, headers=self.__header)
        stocks_list = pd.read_html(response.text, decimal=',', thousands='.')

        return stocks_list

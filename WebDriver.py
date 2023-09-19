from typing import List

import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebDriver:
    def __init__(self) -> None:
        self.indicators_partial_url: str = 'https://www.investsite.com.br/principais_indicadores.php?cod_negociacao='
        self.__url: str = 'https://shorturl.at/hrGHQ'
        self.__user_agent: str = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/50.0.2661.75 Safari/537.36')
        self.__url_request_type: str = 'XMLHttpRequest'
        self.header = {
            "User-Agent": self.__user_agent,
            "X-Requested-With": self.__url_request_type
        }
        self.__chrome_options = Options()
        self.__chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.__chrome_options)

    def get_stocks_table(self) -> List:
        r"""
        Get and convert stocks table from HTML into a `List`.

        Return
        -------
        `List` of DataFrames
        """
        try:
            response = requests.get(self.__url, headers=self.header)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        else:
            stocks_list = pd.read_html(response.text, decimal=',', thousands='.')

        return stocks_list

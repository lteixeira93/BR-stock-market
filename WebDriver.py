import time
from typing import List

import pandas as pd
import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from rich.progress import Progress
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebDriver:
    def __init__(
            self
    ) -> None:
        self.__url: str = 'https://shorturl.at/hrGHQ'
        self.__user_agent: str = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/50.0.2661.75 Safari/537.36')
        self.__url_request_type: str = 'XMLHttpRequest'
        self.header = {
            'User-Agent': self.__user_agent,
            'X-Requested-With': self.__url_request_type,
            'Accept-Encoding': 'gzip'
        }
        self.__chrome_options = Options()
        self.__chrome_options.add_argument("--headless")
        self.__chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.__chrome_options)
    # end def

    def get_stocks_table(
            self
    ) -> List:
        r"""
        Get and convert stocks table from HTML into a `List`.

        Return
        -------
        `List` of `DataFrames`
        """
        with Progress() as progress:
            task1 = progress.add_task("[green]Getting indicators:        ", total=100)

            # Reducing number of requests, using keep-alive and improving performance by using Cache
            session = CacheControl(requests.Session(), cache=FileCache('.web_cache'))

            while not progress.finished:
                progress.update(task1, advance=20)
                try:
                    response = session.get(self.__url, headers=self.header)
                    progress.update(task1, advance=50)
                    time.sleep(0.25)
                except requests.exceptions.RequestException as e:
                    raise SystemExit(e)
                else:
                    stocks_list = pd.read_html(response.text, decimal=',', thousands='.')
                    progress.update(task1, advance=30)

        return stocks_list
    # end def

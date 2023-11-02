import time
from datetime import datetime, timedelta
from typing import List

import pandas as pd
import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from rich.progress import Progress
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebDriver:
    indicators_url: str = (
        'https://www.investsite.com.br/selecao_acoes.php?dt_arr=%255B%252220230907%2522%252C%2522atual%2522'
        '%255D&ROTanC_min=&ROTanC_max=&ROInvC_min=&ROInvC_max=&chk_lst%5B%5D=itm8&ROE_min=&ROE_max=&ROA_min'
        '=&ROA_max=&margem_liquida_min=&margem_liquida_max=&margem_bruta_min=&margem_bruta_max'
        '=&margem_EBIT_min=&margem_EBIT_max=&chk_lst%5B%5D=itm13&giro_ativo_min=&giro_ativo_max'
        '=&fin_leverage_min=&fin_leverage_max=&debt_equity_min=&debt_equity_max=&p_e_min=&p_e_max=&p_bv_min'
        '=&p_bv_max=&p_receita_liquida_min=&p_receita_liquida_max=&p_FCO_min=&p_FCO_max=&p_FCF1_min'
        '=&p_FCF1_max=&p_EBIT_min=&p_EBIT_max=&p_ncav_min=&p_ncav_max=&p_ativo_total_min=&p_ativo_total_max'
        '=&p_capital_giro_min=&p_capital_giro_max=&EV_EBIT_min=&EV_EBIT_max=&chk_lst%5B%5D=itm26'
        '&EV_EBITDA_min=&EV_EBITDA_max=&EV_receita_liquida_min=&EV_receita_liquida_max=&EV_FCO_min'
        '=&EV_FCO_max=&EV_FCF1_min=&EV_FCF1_max=&EV_ativo_total_min=&EV_ativo_total_max=&div_yield_min'
        '=&div_yield_max=&chk_lst%5B%5D=itm32&vol_financ_min=&vol_financ_max=&chk_lst%5B%5D=itm33'
        '&market_cap_min=&market_cap_max=&setor='
    )
    link_date_lower_bound: int = 65
    link_date_higher_bound: int = 73
    old_date_str: str = indicators_url[link_date_lower_bound:link_date_higher_bound]
    current_date = datetime.today().date()
    updated_date: str = ''

    def __init__(
            self
    ) -> None:
        self.user_agent: str = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/50.0.2661.75 Safari/537.36')
        self.url_request_type: str = 'XMLHttpRequest'
        self.header = {
            'User-Agent': self.user_agent,
            'X-Requested-With': self.url_request_type,
            'Accept-Encoding': 'gzip'
        }
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.chrome_options)

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
        self.update_indicators_reference()

        with Progress() as progress:
            task1 = progress.add_task("[green]Getting indicators:        ", total=100)

            # Reducing number of requests, using keep-alive and improving performance by using Cache
            session = CacheControl(requests.Session(), cache=FileCache('.web_cache'))

            while not progress.finished:
                progress.update(task1, advance=20)
                try:
                    response = session.get(self.indicators_url, headers=self.header)
                    progress.update(task1, advance=50)
                    time.sleep(0.25)
                except requests.exceptions.RequestException as e:
                    print(f'Error accessing www.investsite.com.br\nError message: {e}')
                    raise SystemExit(1)
                else:
                    stocks_list = pd.read_html(response.text, decimal=',', thousands='.')
                    progress.update(task1, advance=30)

        return stocks_list

    # end def
    def update_indicators_reference(self) -> None:
        r"""
        Get indicators URL and reformat it to updated link date.
        """
        first_day_of_current_month = datetime.today().replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)

        # Day must be one day before actual date in order to have a valid and updated url.
        # If current day is the first day of the current month, then the last day of last month is used.
        if self.current_date.day == first_day_of_current_month.day:
            self.updated_date = (str(datetime.today().date().replace(
                day=last_day_of_previous_month.day,
                month=last_day_of_previous_month.month)).replace('-', ''))
        else:
            self.updated_date = str(datetime.today().date().replace(day=self.current_date.day - 1)).replace('-', '')

        self.indicators_url = self.indicators_url.replace(self.old_date_str, self.updated_date)
    # end def

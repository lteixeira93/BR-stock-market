import threading
from typing import List

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from WebDriver import WebDriver

# Creating lock to avoid race condition on shared resource
lock = threading.RLock()


class WebStockFilter(WebDriver):
    def __init__(
            self
    ) -> None:
        super().__init__()
        self.stock_bankruptcy_status: str = 'FASE OPERACIONAL'
        self.bankruptcy_text_xpath: str = '//*[@id="tabela_resumo_empresa"]/tbody/tr[4]/td[2]'

    def check_bankruptcy(
            self,
            companies_stock_link_list: List,
            companies_in_bankruptcy_list: List,
            first_half_per_thread: int,
            second_half_per_thread: int
    ) -> List:
        r"""
        Gets `List` of local-filtered stocks and do `multiprocessing` web analysis using bankruptcy indicators
        for each stock.

        Return
        -------
        `List` of stocks in bankruptcy
        """
        for company_stock_link in companies_stock_link_list[first_half_per_thread:second_half_per_thread]:
            try:
                self.driver.get(company_stock_link)
                bankruptcy_situation = self.driver.find_element(By.XPATH, self.bankruptcy_text_xpath)
            except NoSuchElementException:
                raise NoSuchElementException
            else:
                if self.stock_bankruptcy_status not in bankruptcy_situation.text:
                    # print(f"Found {company_stock_link[-5:]} in bankruptcy to be removed "
                    #       f"from selected stocks.")
                    with lock:
                        companies_in_bankruptcy_list.append(company_stock_link[-5:])

        return companies_in_bankruptcy_list

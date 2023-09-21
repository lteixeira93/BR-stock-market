from typing import List

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from WebDriver import WebDriver


class WebStockFilter(WebDriver):
    def __init__(
            self
    ) -> None:
        super().__init__()
        self.__stock_bankruptcy_status: str = 'FASE OPERACIONAL'
        self.__bankruptcy_text_xpath: str = '//*[@id="tabela_resumo_empresa"]/tbody/tr[4]/td[2]'

    def check_bankruptcy(
            self,
            companies_stock_link_list: List,
            first_half_per_core: int,
            second_half_per_core: int
    ):# -> List:
        r"""
        Gets `List` of local-filtered stocks and do `multiprocessing` web analysis using bankruptcy indicators
        for each stock.

        Return
        -------
        `List` of stocks in bankruptcy
        """
        companies_in_bankruptcy_list = []

        for company_stock_link in companies_stock_link_list[first_half_per_core:second_half_per_core]:
            try:
                self.driver.get(company_stock_link)
                bankruptcy_situation = self.driver.find_element(By.XPATH, self.__bankruptcy_text_xpath)
            except NoSuchElementException:
                raise NoSuchElementException
            else:
                if self.__stock_bankruptcy_status not in bankruptcy_situation.text:
                    print(f"Found {company_stock_link[-4:]} in bankruptcy to be removed "
                          f"from selected stocks.")
                    companies_in_bankruptcy_list.append(company_stock_link[-4:])

        print(companies_in_bankruptcy_list)
        # return companies_in_bankruptcy_list

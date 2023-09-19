from typing import List

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from WebDriver import WebDriver


class WebStockFilter(WebDriver):
    def __init__(self) -> None:
        super().__init__()
        self.__stock_bankruptcy_status: str = 'FASE OPERACIONAL' #'EM RECUPERAÇÃO JUDICIAL OU EQUIVALENTE'
        self.__bankruptcy_text_xpath: str = '//*[@id="tabela_resumo_empresa"]/tbody/tr[4]/td[2]'
        self.__companies_stock_link_list_dummy = [self.indicators_partial_url + 'GOAU4', self.indicators_partial_url + 'ETER3']

    def check_bankruptcy(self, companies_stock_name_list: List) -> List:
        r"""
        Gets list of local-filtered stocks and do web analysis using bankruptcy indicators for each stock.

        Return
        -------
        `List` of stocks in bankruptcy
        """
        # TODO: Can be multi processes
        companies_in_bankruptcy_list = []
        companies_stock_link_list = [self.indicators_partial_url + stock_check_link
                                     for stock_check_link in companies_stock_name_list]

        print(f'Running bankruptcy analysis on:\n{companies_stock_name_list}')
        for company_stock_name in self.__companies_stock_link_list_dummy:
            try:
                print(company_stock_name)
                self.driver.get(company_stock_name)
                bankruptcy_situation = self.driver.find_element(By.XPATH, self.__bankruptcy_text_xpath)
            except NoSuchElementException:
                raise NoSuchElementException
            else:
                if self.__stock_bankruptcy_status not in bankruptcy_situation.text:
                    print(f"Found {company_stock_name[len(self.indicators_partial_url):]} in bankruptcy to be removed "
                          "from selected stocks.")
                    companies_in_bankruptcy_list.append(company_stock_name[len(self.indicators_partial_url):])

        return companies_in_bankruptcy_list

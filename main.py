import pandas as pd
import requests


class StockWebDriver:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(StockWebDriver, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.__stock_data_frame = None
        self.__drop_columns_list = [
            'Empresa', 'Data Preço', 'Data Dem.Financ.', 'Consolidação', 'ROTanC', 'ROInvC', 'RPL',	'ROA', 'Margem Líquida', 'Margem Bruta',
            'Giro Ativo', 'Alav.Financ.', 'Passivo/PL', 'Preço/Lucro', 'Preço/VPA', 'Preço/Rec.Líq.', 'Preço/FCO' ,'Preço/FCF', 'Preço/EBIT',
            'Preço/NCAV', 'Preço/Ativo Total', 'Preço/Cap.Giro', 'EV/EBITDA', 'EV/Rec.Líq.', 'EV/FCF', 'EV/FCO', 'EV/Ativo Total',
            'Market Cap(R$)', '# Ações Total', '# Ações Ord.', '# Ações Pref.'
        ]

        self.__url: str = 'https://shorturl.at/hrGHQ'
        self.__user_agent: str = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/50.0.2661.75 Safari/537.36')
        self.__url_request_type: str = 'XMLHttpRequest'
        self.__header = {
          "User-Agent": self.__user_agent,
          "X-Requested-With": self.__url_request_type
        }
        self.__request = requests.get(self.__url, headers=self.__header)

    def get_stocks_table(self) -> None:
        r"""
        Get HTML stock tables into a list of DataFrame objects.

        Returns
        -------
        A list of DataFrames.
        """
        self.__stock_data_frame = pd.concat(pd.read_html(self.__request.text))
        print(self.__stock_data_frame)
        self.filter_stocks_table()

    def filter_stocks_table(self) -> None:
        r"""
        Filter stock tables list of DataFrame objects based on:
        EBIT Margin (%)
        EV/EBIT
        Dividend Yield (%)
        Financial Volume (%)

        Returns
        -------
        A list of DataFrames filtered.
        """
        self.__stock_data_frame.drop(columns=self.__drop_columns_list, inplace=True)
        self.__stock_data_frame = self.__stock_data_frame.drop(self.__stock_data_frame['Volume Financ.(R$)'] < '1_000_000') # TODO: Remove Financial volumes
        print(self.__stock_data_frame)


def main():
    stock_web_driver = StockWebDriver()
    stock_web_driver.get_stocks_table()


if __name__ == "__main__":
    main()

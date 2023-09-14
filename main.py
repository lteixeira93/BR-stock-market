import numpy as np
import pandas as pd
import requests


class StockWebDriver:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(StockWebDriver, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.__drop_columns_list = [
            'Empresa', 'Data Preço', 'Data Dem.Financ.', 'Consolidação', 'ROTanC', 'ROInvC', 'RPL', 'ROA',
            'Margem Líquida', 'Margem Bruta',
            'Giro Ativo', 'Alav.Financ.', 'Passivo/PL', 'Preço/Lucro', 'Preço/VPA', 'Preço/Rec.Líq.', 'Preço/FCO',
            'Preço/FCF', 'Preço/EBIT',
            'Preço/NCAV', 'Preço/Ativo Total', 'Preço/Cap.Giro', 'EV/EBITDA', 'EV/Rec.Líq.', 'EV/FCF', 'EV/FCO',
            'EV/Ativo Total',
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

    def get_dummy_stocks_table(self) -> None:
        r"""
        Get HTML stock tables into a list of DataFrame objects.

        Returns
        -------
        A list of DataFrames.
        """
        # create dataset
        dummy_data_frame = pd.DataFrame(
            {'Ação': ['RRRP3', 'TTEN3', 'QVQP3B', 'EALT3', 'EALT4', 'YBRA4'],
             'Preço': ['3213', '5454', '543', '0', np.nan, '2245'],
             'Margem EBIT': ['1,83%', '43,83%', np.nan, '0,00%', '66,83%', '23,83%'],
             'EV/EBIT': ['13289', '1328', np.nan, '443', '0', '434'],
             'Div.Yield': ['43,00%', np.nan, '66,00%', '12,00%', '1,00%', '0,01%'],
             'Volume Financ.(R$)': ['3.988', '167.033.988', '1.000.000', '0', '167.033', np.nan]}
        )
        self.apply_stocks_filter(dummy_data_frame)

    def get_stocks_table(self) -> None:
        r"""
        Get HTML stock tables into a list of DataFrame objects.

        Returns
        -------
        A list of DataFrames.
        """
        response = requests.get(self.__url, headers=self.__header)
        stock_list = pd.read_html(response.text)
        stock_data_frame = pd.DataFrame(stock_list[1])
        self.apply_stocks_filter(stock_data_frame)

    def apply_stocks_filter(self, stock_data_frame) -> None:
        r"""
        Filter stock tables list of DataFrame objects based on:
        EBIT_Margin (%)
        EV_EBIT
        Dividend_Yield (%)
        Financial_Volume (%)

        Returns
        -------
        A list of DataFrames filtered.
        """
        # stock_data_frame.drop(columns=self.__drop_columns_list, inplace=True)

        # Rename columns
        stock_data_frame.rename(columns={'Ação': 'Stock', 'Preço': 'Price', 'Margem EBIT': 'EBIT_Margin',
                                         'EV/EBIT': 'EV_EBIT', 'Div.Yield': 'Dividend_Yield',
                                         'Volume Financ.(R$)': 'Financial_Volume'},
                                inplace=True)

        # Wipe out invalid characters to manipulate the data #
        print(stock_data_frame)
        stock_data_frame['EBIT_Margin'] = stock_data_frame['EBIT_Margin'].str.rstrip('%')
        stock_data_frame['Dividend_Yield'] = stock_data_frame['Dividend_Yield'].str.rstrip('%')

        # Replaces NaN with 0, retain int part and convert it to integer
        stock_data_frame.fillna(0, inplace=True)
        print(stock_data_frame)
        stock_data_frame['Price'] = stock_data_frame['Price'].astype(str).str.split(',').str[0].astype(int)
        stock_data_frame['EBIT_Margin'] = stock_data_frame['EBIT_Margin'].astype(str).str.split(',').str[0].astype(int)
        stock_data_frame['Dividend_Yield'] = (stock_data_frame['Dividend_Yield'].astype(str).str.split(',').str[0]
                                              .astype(int))
        stock_data_frame['EV_EBIT'] = stock_data_frame['EV_EBIT'].astype(str).astype(int)
        stock_data_frame['Financial_Volume'] = (stock_data_frame['Financial_Volume'].astype(str).str.replace('.', '')
                                                .astype(int))

        print(stock_data_frame)
        print(stock_data_frame.dtypes)

        stock_data_frame.drop(stock_data_frame[stock_data_frame['Financial_Volume'] < 1000000].index,
                              inplace=True)  # TODO: Check reliability
        print(stock_data_frame)


def main():
    stock_web_driver = StockWebDriver()
    stock_web_driver.get_dummy_stocks_table()


if __name__ == "__main__":
    main()

from typing import List

import pandas as pd


class StockFilter:
    @staticmethod
    def apply_financial_filters(stocks_data_frame) -> pd.DataFrame:
        r"""
        Filter stock tables `List` of `DataFrame` objects based on:
        `Stock`, `Price`, `EBIT_Margin_(%)`, `EV_EBIT`, `Dividend_Yield_(%)`, `Financial_Volume_(%)`

        Return
        -------
        Pandas `DataFrame`
        """
        # First filter: Drop all Financial_Volume_(%) less than 1_000_000 R$ - Filter Ok
        stocks_data_frame.sort_values(by=['Financial_Volume_(%)'], inplace=True)
        stocks_data_frame.drop(stocks_data_frame[stocks_data_frame['Financial_Volume_(%)'] < 1_000_000].index,
                               inplace=True)

        # Second filter: Drop companies with negative or zero profit EBIT_Margin_(%)
        stocks_data_frame.sort_values(by=['EBIT_Margin_(%)'], inplace=True)
        stocks_data_frame.drop(stocks_data_frame[stocks_data_frame['EBIT_Margin_(%)'] < 0].index, inplace=True)

        # Third filter: Sort from the cheapest to expensive stocks EV_EBIT
        stocks_data_frame.sort_values(by=['EV_EBIT'], inplace=True)

        return stocks_data_frame

    @staticmethod
    def prepare_dataframe(stocks_list: List) -> pd.DataFrame:
        r"""
        Get `List` of `DataFrame`, convert to `DataFrame`, remove unused fields, wipe out data to be processed.

        Return
        -------
        Pandas `DataFrame`
        """
        stocks_data_frame = pd.DataFrame(stocks_list[1])

        drop_columns_list = [
            'Empresa', 'Data Preço', 'Data Dem.Financ.', 'Consolidação', 'ROTanC', 'ROInvC', 'RPL', 'ROA',
            'Margem Líquida', 'Margem Bruta',
            'Giro Ativo', 'Alav.Financ.', 'Passivo/PL', 'Preço/Lucro', 'Preço/VPA', 'Preço/Rec.Líq.', 'Preço/FCO',
            'Preço/FCF', 'Preço/EBIT',
            'Preço/NCAV', 'Preço/Ativo Total', 'Preço/Cap.Giro', 'EV/EBITDA', 'EV/Rec.Líq.', 'EV/FCF', 'EV/FCO',
            'EV/Ativo Total',
            'Market Cap(R$)', '# Ações Total', '# Ações Ord.', '# Ações Pref.'
        ]

        # Drop unused columns, rename remaining columns
        stocks_data_frame.drop(columns=drop_columns_list, inplace=True)
        stocks_data_frame.rename(columns={'Ação': 'Stock', 'Preço': 'Price', 'Margem EBIT': 'EBIT_Margin_(%)',
                                          'EV/EBIT': 'EV_EBIT', 'Div.Yield': 'Dividend_Yield_(%)',
                                          'Volume Financ.(R$)': 'Financial_Volume_(%)'},
                                 inplace=True)

        # Drop NaNs on EBIT_Margin_(%)
        stocks_data_frame.dropna(subset=['EBIT_Margin_(%)', 'EV_EBIT'], inplace=True)

        # Replaces NaN with 0, retain int part and convert it to integer
        stocks_data_frame.fillna(0, inplace=True)

        # Wipe out invalid characters to manipulate the data
        stocks_data_frame['Price'] = stocks_data_frame['Price'].astype(str).astype(float)
        stocks_data_frame['EBIT_Margin_(%)'] = stocks_data_frame['EBIT_Margin_(%)'].str.rstrip('%')
        stocks_data_frame['EBIT_Margin_(%)'] = stocks_data_frame['EBIT_Margin_(%)'].astype(str).str.replace('.', '')

        stocks_data_frame['EV_EBIT'] = stocks_data_frame['EV_EBIT'].astype(str).str.replace(',', '')

        stocks_data_frame['Dividend_Yield_(%)'] = stocks_data_frame['Dividend_Yield_(%)'].str.rstrip('%')
        stocks_data_frame['Dividend_Yield_(%)'] = stocks_data_frame['Dividend_Yield_(%)'].astype(str).str.replace('.',
                                                                                                                  '')

        # Removing characters (,.) and convert string numbers to int and float properly
        stocks_data_frame['EBIT_Margin_(%)'] = (stocks_data_frame['EBIT_Margin_(%)'].astype(str).str.replace(',', '.')
                                                .astype(float))

        stocks_data_frame['Dividend_Yield_(%)'] = (
            stocks_data_frame['Dividend_Yield_(%)'].astype(str).str.replace(',', '.')
            .astype(float))

        stocks_data_frame['EV_EBIT'] = stocks_data_frame['EV_EBIT'].astype(str).astype(float)

        stocks_data_frame['Financial_Volume_(%)'] = (stocks_data_frame['Financial_Volume_(%)'].astype(str).str
                                                     .replace('.', '').astype(float).astype(int))

        # Replaces NaN with 0, retain int part and convert it to integer
        stocks_data_frame.fillna(0, inplace=True)

        return stocks_data_frame

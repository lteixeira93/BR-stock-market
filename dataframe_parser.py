import time
from typing import List
import pandas as pd
from rich.progress import Progress

from web_driver import WebDriver


class DataframeParser:
    companies_in_bankruptcy_list = []

    def __init__(self, web_driver: WebDriver()):
        self.drop_columns_list = [
            'Empresa', 'Data Preço', 'Data Dem.Financ.', 'Consolidação', 'ROTanC', 'ROInvC', 'RPL', 'ROA',
            'Margem Líquida', 'Margem Bruta', 'Giro Ativo', 'Alav.Financ.', 'Passivo/PL', 'Preço/Lucro', 'Preço/VPA',
            'Preço/Rec.Líq.', 'Preço/FCO', 'Preço/FCF', 'Preço/EBIT', 'Preço/NCAV', 'Preço/Ativo Total',
            'Preço/Cap.Giro', 'EV/EBITDA', 'EV/Rec.Líq.', 'EV/FCF', 'EV/FCO', 'EV/Ativo Total', 'Market Cap(R$)',
            '# Ações Total', '# Ações Ord.', '# Ações Pref.'
        ]
        self.web_driver = web_driver
    # end def

    def prepare_dataframe(
            self,
            stocks_list: List
    ) -> pd.DataFrame:
        r"""
        Get `List` of `DataFrame`, convert to `DataFrame`, remove unused fields, wipe out data to be processed.

        Return
        -------
        Pandas `DataFrame`
        """
        if stocks_list:
            with Progress() as progress:
                task1 = progress.add_task("[green]Preparing fetched data:    ", total=100)

                while not progress.finished:
                    stocks_data_frame = self.extract_dataframe(stocks_list)
                    stocks_data_frame = self.drop_and_rename_cols(stocks_data_frame)
                    time.sleep(0.25)
                    progress.update(task1, advance=40)

                    stocks_data_frame = self.drop_and_fill_nans(stocks_data_frame)
                    stocks_data_frame = self.remove_invalid_chars(stocks_data_frame)
                    time.sleep(0.25)
                    progress.update(task1, advance=40)

                    stocks_data_frame = self.convert_data_type(stocks_data_frame)
                    stocks_data_frame = self.replace_nans_by_zero(stocks_data_frame)
                    time.sleep(0.25)
                    progress.update(task1, advance=20)
                return stocks_data_frame
        else:
            print('Cannot parse data, list is empty or corrupted.')
            raise SystemExit(1)

    @staticmethod
    def extract_dataframe(stocks_list: List) -> pd.DataFrame:
        r"""
        Get `List` of `DataFrames`, convert to `DataFrame`.

        Return
        -------
        Pandas `DataFrame`
        """
        try:
            return pd.DataFrame(stocks_list[1])
        except IndexError as e:
            print(f'Error parsing list of dataframes, list is empty or corrupted\nError message: {e}')
            raise SystemExit(1)

    # end def

    def drop_and_rename_cols(self, stocks_data_frame: pd.DataFrame) -> pd.DataFrame:
        r"""
        Get `DataFrame`, drop unused columns, rename remaining columns.

        Return
        -------
        Pandas `DataFrame`
        """
        if not stocks_data_frame.empty:
            stocks_data_frame.drop(columns=self.drop_columns_list, inplace=True)
            stocks_data_frame.rename(columns={'Ação': 'Stock', 'Preço': 'Price', 'Margem EBIT': 'EBIT_Margin_(%)',
                                              'EV/EBIT': 'EV_EBIT', 'Div.Yield': 'Dividend_Yield_(%)',
                                              'Volume Financ.(R$)': 'Financial_Volume_(%)'},
                                     inplace=True)
        else:
            print('Cannot drop nor rename, dataframe is empty or corrupted.')
            raise SystemExit(1)

        return stocks_data_frame

    # end def

    @staticmethod
    def drop_and_fill_nans(stocks_data_frame: pd.DataFrame) -> pd.DataFrame:
        r"""
        Get `DataFrame`, drop NaNs on EBIT_Margin_(%) and replaces NaN with 0.
        Return
        -------
        Pandas `DataFrame`
        """
        if not stocks_data_frame.empty:
            stocks_data_frame.dropna(subset=['EBIT_Margin_(%)', 'EV_EBIT'], inplace=True)
            stocks_data_frame.fillna(value=0, inplace=True)
        else:
            print('Cannot drop nor fill, dataframe is empty or corrupted.')
            raise SystemExit(1)

        return stocks_data_frame

    # end def

    @staticmethod
    def remove_invalid_chars(stocks_data_frame: pd.DataFrame) -> pd.DataFrame:
        r"""
        Get `DataFrame`, wipe out invalid characters to manipulate the data.

        Return
        -------
        Pandas `DataFrame`
        """
        if not stocks_data_frame.empty:
            stocks_data_frame['EV_EBIT'] = stocks_data_frame['EV_EBIT'].astype(str).str.replace(',', '')
            stocks_data_frame['EBIT_Margin_(%)'] = stocks_data_frame['EBIT_Margin_(%)'].str.rstrip('%')
            stocks_data_frame['EBIT_Margin_(%)'] = stocks_data_frame['EBIT_Margin_(%)'].astype(str).str.replace('.', '')
            stocks_data_frame['Dividend_Yield_(%)'] = stocks_data_frame['Dividend_Yield_(%)'].str.rstrip('%')
            stocks_data_frame['Dividend_Yield_(%)'] = (stocks_data_frame['Dividend_Yield_(%)'].astype(str).str
                                                       .replace('.', ''))
        else:
            print('Cannot remove invalid characters, dataframe is empty or corrupted.')
            raise SystemExit(1)

        return stocks_data_frame

    # end def

    @staticmethod
    def convert_data_type(stocks_data_frame: pd.DataFrame) -> pd.DataFrame:
        r"""
        Get `DataFrame`, removes characters (,.) and convert string numbers to int and float properly.

        Return
        -------
        Pandas `DataFrame`
        """
        if not stocks_data_frame.empty:
            stocks_data_frame['Price'] = stocks_data_frame['Price'].astype(str).astype(float)
            stocks_data_frame['EBIT_Margin_(%)'] = (
                stocks_data_frame['EBIT_Margin_(%)'].astype(str).str.replace(',', '.')
                .astype(float))

            stocks_data_frame['Dividend_Yield_(%)'] = (stocks_data_frame['Dividend_Yield_(%)'].astype(str).str
                                                       .replace(',', '.').astype(float))

            stocks_data_frame['EV_EBIT'] = stocks_data_frame['EV_EBIT'].astype(str).astype(float)

            stocks_data_frame['Financial_Volume_(%)'] = (stocks_data_frame['Financial_Volume_(%)'].astype(str).str
                                                         .replace('.', '').astype(float).astype(int))
        else:
            print('Cannot convert data, dataframe is empty or corrupted.')
            raise SystemExit(1)

        return stocks_data_frame

    # end def

    @staticmethod
    def replace_nans_by_zero(stocks_data_frame: pd.DataFrame) -> pd.DataFrame:
        r"""
        Get `DataFrame`, wipe out invalid characters to manipulate the data

        Return
        -------
        Pandas `DataFrame`
        """
        # Replaces NaN with 0, retain int part and convert it to integer
        if not stocks_data_frame.empty:
            stocks_data_frame.fillna(value=0, inplace=True)
        else:
            print('Cannot replace data, dataframe is empty or corrupted.')
            raise SystemExit(1)
        return stocks_data_frame
    # end def

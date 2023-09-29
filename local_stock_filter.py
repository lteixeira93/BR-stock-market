import os
import threading
import time
from collections import Counter
from typing import List

import numpy as np
import pandas as pd
import rich
from rich.progress import Progress

import settings
from local_filter import LocalFilter
from web_stock_filter import WebStockFilter


class LocalStockFilter(LocalFilter):
    companies_in_bankruptcy_list = []

    def __init__(self):
        self.indicators_partial_url: str = 'https://www.investsite.com.br/principais_indicadores.php?cod_negociacao='
        self.drop_columns_list = [
            'Empresa', 'Data Preço', 'Data Dem.Financ.', 'Consolidação', 'ROTanC', 'ROInvC', 'RPL', 'ROA',
            'Margem Líquida', 'Margem Bruta', 'Giro Ativo', 'Alav.Financ.', 'Passivo/PL', 'Preço/Lucro', 'Preço/VPA',
            'Preço/Rec.Líq.', 'Preço/FCO', 'Preço/FCF', 'Preço/EBIT', 'Preço/NCAV', 'Preço/Ativo Total',
            'Preço/Cap.Giro', 'EV/EBITDA', 'EV/Rec.Líq.', 'EV/FCF', 'EV/FCO', 'EV/Ativo Total', 'Market Cap(R$)',
            '# Ações Total', '# Ações Ord.', '# Ações Pref.'
        ]
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

    def apply_financial_filters(
            self,
            stocks_data_frame: pd.DataFrame
    ) -> pd.DataFrame:
        r"""
        Filter stock tables `List` of `DataFrame` objects based on:
        `Stock`, `Price`, `EBIT_Margin_(%)`, `EV_EBIT`, `Dividend_Yield_(%)`, `Financial_Volume_(%)`

        Return
        -------
        Pandas `DataFrame`
        """
        if not stocks_data_frame.empty or settings.PICKLE_DATAFRAME:
            with Progress() as progress:
                task1 = progress.add_task("[green]Applying financial filters:", total=100)

                while not progress.finished:
                    if not settings.PICKLE_DATAFRAME:
                        # First filter: Drop all Financial_Volume_(%) less than 1_000_000 R$
                        stocks_data_frame = self.drop_low_financial_volume(stocks_data_frame)

                        # Second filter: Drop companies with negative or zero profit EBIT_Margin_(%)
                        stocks_data_frame = self.drop_negative_profit_stocks(stocks_data_frame)
                        time.sleep(0.5)
                        progress.update(task1, advance=40)

                        # Third filter: Sort from the cheapest to expensive stocks EV_EBIT
                        stocks_data_frame = self.sort_by_ev_ebit(stocks_data_frame)

                        # Fourth filter: Remove stocks from the same company with less Financial_Volume_(%)
                        stocks_data_frame = self.drop_duplicated_stocks_by_financial_volume(stocks_data_frame)
                        time.sleep(0.5)
                        progress.update(task1, advance=40)

                    # Fifth filter: Remove stocks in bankruptcy
                    stocks_data_frame = self.drop_stocks_in_bankruptcy(stocks_data_frame)
                    time.sleep(0.5)
                    progress.update(task1, advance=20)
                    break
        else:
            print('Cannot apply filters, dataframe is empty or corrupted.')
            raise SystemExit(1)

        rich.print('[blue]Finished')
        return stocks_data_frame.head(20)

    @staticmethod
    def drop_low_financial_volume(
            stocks_data_frame: pd.DataFrame,
            financial_volume=1_000_000
    ) -> pd.DataFrame:
        r"""
        Gets `stocks_data_frame` and drop all Financial_Volume_(%) less than financial_volume.

        Return
        -------
        Pandas `DataFrame`
        """
        if financial_volume > 0:
            stocks_data_frame.sort_values(by=['Financial_Volume_(%)'], inplace=True)
            stocks_data_frame.drop(
                stocks_data_frame[stocks_data_frame['Financial_Volume_(%)'] < financial_volume].index,
                inplace=True)
        else:
            print('Cannot drop negative financial volume.')
            raise SystemExit(1)

        return stocks_data_frame

    @staticmethod
    def drop_negative_profit_stocks(
            stocks_data_frame: pd.DataFrame
    ) -> pd.DataFrame:
        r"""
        Gets `stocks_data_frame` and drop companies with negative or zero profit EBIT_Margin_(%).

        Return
        -------
        Pandas `DataFrame`
        """
        stocks_data_frame.sort_values(by=['EBIT_Margin_(%)'], inplace=True)
        stocks_data_frame.drop(stocks_data_frame[stocks_data_frame['EBIT_Margin_(%)'] < 0].index, inplace=True)

        return stocks_data_frame

    @staticmethod
    def sort_by_ev_ebit(
            stocks_data_frame: pd.DataFrame,
            by='EV_EBIT'
    ) -> pd.DataFrame:
        r"""
        Gets `stocks_data_frame` and sort from the cheapest to expensive stocks EV_EBIT.

        Return
        -------
        Pandas `DataFrame`
        """
        stocks_data_frame.sort_values(by=by, inplace=True)

        return stocks_data_frame

    @staticmethod
    def drop_duplicated_stocks_by_financial_volume(
            stocks_data_frame: pd.DataFrame
    ) -> pd.DataFrame:
        r"""
        Gets `stocks_data_frame` and remove stocks from the same company with less Financial_Volume_(%).

        Return
        -------
        Pandas `DataFrame`
        """
        # Maintain only first 40 most valuable stocks
        stocks_data_frame.drop(stocks_data_frame.index[41:], inplace=True)
        stocks_data_frame.reset_index(drop=True, inplace=True)

        # Gets stock names and financial volumes to map each other
        companies_stock_name_list = list(stocks_data_frame['Stock'])
        companies_stock_fv_list = list(stocks_data_frame['Financial_Volume_(%)'])
        companies_stock_name_largest_fv_dict = dict(map(
            lambda i, j: (i, j), companies_stock_name_list, companies_stock_fv_list))

        # Counter same companies (Same four letters in stock name) to compare the financial volume
        companies_similar_stock_counter_dict = dict(Counter(k[:4] for k in companies_stock_name_largest_fv_dict))

        # Pop stocks which are unique
        for key, value in companies_similar_stock_counter_dict.copy().items():
            if value == 1:
                companies_similar_stock_counter_dict.pop(key)

        # Creates dict with non-unique stocks with value as zero to be filled with financial volume
        largest_fv_dict = {key: 0 for key in companies_similar_stock_counter_dict}
        to_remove_keys_set = set()

        # Order by financial volume from the largest to smallest
        companies_stock_name_largest_fv_dict = dict(sorted(companies_stock_name_largest_fv_dict.items(),
                                                           key=lambda x: x[1], reverse=False))

        # Process non-unique stocks and fills with the greatest financial volume
        for key_i, value_i in companies_similar_stock_counter_dict.items():
            counter = value_i
            for key_j, value_j in companies_stock_name_largest_fv_dict.items():
                if counter == 0:
                    del largest_fv_dict[key_i]
                    break
                if key_i == key_j[:4]:
                    counter -= 1
                    if value_j > largest_fv_dict[key_i]:
                        largest_fv_dict[key_i] = value_j
                        largest_fv_dict[key_j] = largest_fv_dict[key_i]
                        if counter > 0:
                            to_remove_keys_set.add(key_j)
        # Removes the smallest financial volumes repeated stocks
        stocks_data_frame.drop(pd.Index(np.where(stocks_data_frame['Stock'].isin(list(to_remove_keys_set)))[0]),
                               inplace=True)
        stocks_data_frame.reset_index(drop=True, inplace=True)
        return stocks_data_frame

    def drop_stocks_in_bankruptcy(
            self,
            stocks_data_frame: pd.DataFrame
    ) -> pd.DataFrame:
        r"""
        Gets `stocks_data_frame` and drop stocks in bankruptcy.

        Return
        -------
        Pandas `DataFrame`
        """
        if settings.STORE_PICLE:
            # Stores dataframe on disk and exits.
            stocks_data_frame.to_pickle(settings.PICKLE_FILEPATH)
            exit()

        if settings.PICKLE_DATAFRAME:
            # Reads from picle to speed up tests loading dataframe.
            if os.path.exists(settings.PICKLE_FILEPATH):
                stocks_data_frame = pd.read_pickle(settings.PICKLE_FILEPATH)
            else:
                print("Pickle file not found, set STORE_PICLE as True")
                exit()

        companies_stock_name_list = list(stocks_data_frame['Stock'])
        companies_stock_link_list = [self.indicators_partial_url + stock_check_link
                                     for stock_check_link in companies_stock_name_list]

        # Creating list of links in format:
        # <INDICATORS_LINK> + <STOCK_NAME>
        number_of_threads = 4

        if settings.DEBUG_THREADS:
            print(f"Initializing analysis with {number_of_threads} cores, each core with "
                  f"{int(len(companies_stock_link_list) / number_of_threads)} tasks")
        threads = []
        next_first_half_chunk = 0

        if not settings.UNIT_TEST:
            # Sharing data between processes that can be serialized.
            for current_thread in range(1, number_of_threads + 1):
                # Dividing companies_stock_link_list for each current_thread to optimize requests
                first_half_per_thread = next_first_half_chunk
                second_half_per_thread = int(len(companies_stock_link_list) * current_thread / number_of_threads)
                next_first_half_chunk = second_half_per_thread + 1

                if settings.DEBUG_THREADS:
                    print(f"Core {current_thread} processing from {first_half_per_thread} to {second_half_per_thread}")

                threads.append(
                    threading.Thread(
                        target=WebStockFilter().check_bankruptcy,
                        kwargs={
                            'companies_stock_link_list': companies_stock_link_list,
                            'companies_in_bankruptcy_list': self.companies_in_bankruptcy_list,
                            'first_half_per_thread': first_half_per_thread,
                            'second_half_per_thread': second_half_per_thread
                        },
                        daemon=True
                    ),
                )

            [th.start() for th in threads]
            [th.join() for th in threads]

        stocks_data_frame = stocks_data_frame[~stocks_data_frame.Stock.isin(self.companies_in_bankruptcy_list)]

        return stocks_data_frame

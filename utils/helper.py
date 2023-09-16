import pandas as pd


def print_full_dataframe(dataframe) -> None:
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(dataframe)

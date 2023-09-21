from abc import ABC, abstractmethod
from typing import List

import pandas as pd


class LocalFilter(ABC):
    @staticmethod
    @abstractmethod
    def prepare_dataframe(
            stocks_list: List
    ) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def apply_financial_filters(
            self,
            stocks_data_frame: pd.DataFrame
    ) -> pd.DataFrame:
        raise NotImplementedError

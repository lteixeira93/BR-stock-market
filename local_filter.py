from abc import ABC, abstractmethod

import pandas as pd

from dataframe_parser import DataframeParser


class LocalFilter(ABC):
    @abstractmethod
    def apply_financial_filters(
            self,
            dataframe_parser: DataframeParser
    ) -> pd.DataFrame:
        raise NotImplementedError

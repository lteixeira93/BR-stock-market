from abc import ABC, abstractmethod


class LocalFilter(ABC):
    @abstractmethod
    def prepare_dataframe(self):
        raise NotImplementedError

    @abstractmethod
    def apply_financial_filters(self):
        raise NotImplementedError

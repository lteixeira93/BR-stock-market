from abc import ABC, abstractmethod
class FileManager(ABC):
    @abstractmethod
    def store_on_disk(self, stocks_data_frame):
        raise NotImplementedError

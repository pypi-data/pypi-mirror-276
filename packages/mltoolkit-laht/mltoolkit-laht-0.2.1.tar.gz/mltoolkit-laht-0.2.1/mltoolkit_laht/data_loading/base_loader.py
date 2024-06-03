from abc import ABC, abstractmethod
from ..utils.logger import Logger


class BaseLoader(ABC):

    def __init__(self, file_path):
        self.file_path = file_path
        self.logger = Logger.setup_logger(self.__class__.__name__)

    @abstractmethod
    def load_data(self):
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def get_schema(self):
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def update_schema(self):
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def show_info(self):
        raise NotImplementedError("Subclasses should implement this method.")

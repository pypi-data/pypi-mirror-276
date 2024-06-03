from abc import ABC, abstractmethod


class BaseFeatureEngineer(ABC):

    @abstractmethod
    def create_features(self, data):
        pass

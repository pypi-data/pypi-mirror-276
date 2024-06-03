from abc import ABC, abstractmethod


class BaseTrainer(ABC):

    @abstractmethod
    def train(self, X, y):
        pass

    @abstractmethod
    def predict(self, X):
        pass

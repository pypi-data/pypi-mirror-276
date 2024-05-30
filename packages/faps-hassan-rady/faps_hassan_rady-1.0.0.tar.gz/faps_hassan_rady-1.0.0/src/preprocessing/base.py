from abc import ABC, abstractmethod


class PreProcessor(ABC):
    name = None

    @abstractmethod
    def process(self, x, y):
        pass

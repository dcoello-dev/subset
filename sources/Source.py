from abc import ABC, abstractmethod


class Source(ABC):
    @staticmethod
    @abstractmethod
    def get() -> str:
        pass

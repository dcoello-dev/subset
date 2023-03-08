from abc import ABC, abstractmethod


class Sink(ABC):
    @staticmethod
    @abstractmethod
    def send(data: dict) -> None:
        pass

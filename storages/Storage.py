from abc import ABC, abstractmethod


class Storage(ABC):
    def __init__(self, config: dict):
        self._config = config

    @abstractmethod
    def store_changes(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def create_storage(config: dict, domains: list) -> None:
        pass

    @abstractmethod
    def get_domain(self, domain: str) -> dict:
        pass

    @abstractmethod
    def get_domains(self) -> list:
        pass

    @abstractmethod
    def get_list(self, domain: str) -> list:
        pass

    @abstractmethod
    def reset_domain(self, domain: str):
        pass

    @abstractmethod
    def add_elem_to_domain(self, domain: str, index: int, value: str) -> None:
        pass

    @abstractmethod
    def remove_elem_from_domain(self, domain: str, index: int) -> None:
        pass

    @abstractmethod
    def select_elem_from_domain(self, domain: str, index: int) -> None:
        pass

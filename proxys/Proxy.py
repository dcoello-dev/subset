from abc import ABC, abstractmethod


class Proxy(ABC):

    def __init__(self, config: dict):
        self._config = config

    @abstractmethod
    def update_shared_domain(
            self, user: str, domain: str, storage: dict) -> None:
        pass

    @abstractmethod
    def update_shared_domain_elem(
            self, user: str, domain: str, index: int, data: dict) -> None:
        pass

    @abstractmethod
    def list_shared_domains(self) -> dict:
        pass

    @abstractmethod
    def get_shared_domain(self, user, domain) -> dict:
        pass

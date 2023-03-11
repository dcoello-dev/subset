import sys

from abc import ABC, abstractmethod
from schema import SchemaError


class Sink(ABC):
    def __init__(self, supported_interfaces: list):
        self._supported_schemas = supported_interfaces

    def send(self, data: dict) -> None:
        for sch in self._supported_schemas:
            found = False
            try:
                sch().validate(data)
                found = True
            except SchemaError as e:
                pass

            if not found:
                print(
                    data.keys() +
                    " schema not supported on " +
                    self.__class__.__name__)
                sys.exit(1)

            self.send_sink(data)

    @abstractmethod
    def send_sink(self, data: dict) -> None:
        pass

from schema import Schema

from abc import ABC, abstractmethod


class Source(ABC):
    def __init__(self, sch: Schema):
        self._schema = sch

    @abstractmethod
    def get_source(self) -> dict:
        pass

    def get_schema(self):
        return self._schema

    def get(self) -> dict:
        data = self.get_source()
        self._schema().validate(data)
        return (data, self._schema)

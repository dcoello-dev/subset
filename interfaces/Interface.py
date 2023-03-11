from schema import Schema, SchemaError

from abc import ABC, abstractmethod


class Interface(ABC):
    def __init__(self, sch: Schema):
        self._schema = sch

    def validate(self, data: dict) -> bool:
        try:
            self._schema.validate(data)
            return True
        except SchemaError:
            return False

    @abstractmethod
    def to_string(data: dict) -> str:
        pass

    @abstractmethod
    def serialize(data: dict) -> str:
        pass

    @abstractmethod
    def deserialize(data: str) -> dict:
        pass

from interfaces.Interface import Interface

from schema import Schema, Use


class SimpleString(Interface):
    def __init__(self):
        super().__init__(Schema({
            "str": Use(str)
        }))

    def to_string(self, data: dict) -> str:
        return data["str"]

    def serialize(self, data: dict) -> str:
        pass

    def deserialize(self, data: str) -> dict:
        pass

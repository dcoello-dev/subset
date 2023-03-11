from interfaces.Interface import Interface

from core.Register import Type, Register

from schema import Schema, Use, Optional


@Register(Type.IFACE, "simple_string", "Simple string interface")
class SimpleString(Interface):
    def __init__(self):
        super().__init__(Schema({
            "str": Use(str)
        }))

    def to_string(data: dict) -> str:
        return data["str"]

    def serialize(data: dict) -> str:
        pass

    def deserialize(data: str) -> dict:
        pass

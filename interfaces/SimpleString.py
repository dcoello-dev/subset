from interfaces.Interface import Interface

from schema import Schema, Use


class SimpleString(Interface):
    def __init__(self):
        super().__init__(Schema({
            "str": Use(str)
        }))

    def to_string(self, data: dict) -> str:
        lines = data["str"].split("\n")
        msg = lines[0]
        if len(lines) > 1:
            msg += " /" + str(len(lines))
        return msg

    def to_tim(self, data: dict) -> str:
        lines = data["str"].split("\n")
        msg = lines[0][:40]
        if len(lines[0]) > 40:
            msg += " [bold fuchsia]/" + str(len(lines[0])) + "[/]"
        if len(lines) > 1:
            msg += " [bold orangered]/" + str(len(lines)) + "[/]"
        return msg

    def serialize(self, data: dict) -> str:
        pass

    def deserialize(self, data: str) -> dict:
        pass

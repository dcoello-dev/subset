import pyperclip

from core.Register import Type, Register

from sinks.Sink import Sink


@Register(Type.SINK, "clip", "Copy Data on clipboard")
class Clip(Sink):
    def __init__(self):
        pass

    @staticmethod
    def send(data: dict) -> None:
        pyperclip.copy(data["str"])

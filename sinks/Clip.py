import pyperclip

from core.Register import Type, Register

from sinks.Sink import Sink
from interfaces.SimpleString import SimpleString


@Register(Type.SINK, "clip", "Copy Data on clipboard")
class Clip(Sink):
    def __init__(self):
        super().__init__(SimpleString)

    def send_sink(data: dict) -> None:
        pyperclip.copy(data["str"])

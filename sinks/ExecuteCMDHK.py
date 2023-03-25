from pynput.keyboard import Controller, Key

from core.Register import Type, Register

from sinks.Sink import Sink
from interfaces.SimpleString import SimpleString


@Register(Type.SINK, "execute_cmd_hk", "Execute bash CMD")
class ExecuteCMDHK(Sink):
    def __init__(self):
        super().__init__([SimpleString])

    def send_sink(self, data: dict) -> None:
        keyboard = Controller()
        keyboard.type(data["str"])
        keyboard.tap(Key.enter)
        keyboard.tap(Key.enter)

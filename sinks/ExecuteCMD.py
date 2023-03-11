import pyperclip

from core.Register import Type, Register
from core.CLIFormat import CLIFormat

from sinks.Sink import Sink
from interfaces.SimpleString import SimpleString


@Register(Type.SINK, "execute_cmd", "Execute bash CMD")
class ExecuteCMD(Sink):
    def __init__(self):
        super().__init__([SimpleString])

    def send_sink(self, data: dict) -> None:
        CLIFormat.write_on_parent_shell(data["str"])

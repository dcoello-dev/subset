import os

from core.Register import Type, Register
from core.CMD import _ex_subprocess

from sources.Source import Source

from interfaces.SimpleString import SimpleString


@Register(Type.SOURCE, "last_history_elem", "Get last executed command")
class LastHistoryElem(Source):
    def __init__(self):
        super().__init__(SimpleString)

    def get_source(self) -> dict:
        with open(os.path.expanduser('~') + "/.bash_history", 'r') as f:
            lines = f.readlines()
            last_cmd = lines[-2].strip()
            return dict(str=last_cmd)

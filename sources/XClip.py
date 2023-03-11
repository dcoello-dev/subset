from core.Register import Type, Register
from core.CMD import _ex_subprocess

from sources.Source import Source

from interfaces.SimpleString import SimpleString


@Register(Type.SOURCE, "xclip", "Get xclip -o as source")
class XClip(Source):
    def __init__(self):
        super().__init__(SimpleString)

    def get_source(self) -> dict:
        _, output, _ = _ex_subprocess("xclip -o")
        return dict(str=output)

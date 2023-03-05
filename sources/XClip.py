from core.Register import Type, Register
from core.CMD import _ex_subprocess

from sources.Source import Source


@Register(Type.SOURCE, "xclip", "Get xclip -o as source")
class XClip(Source):
    def __init__(self):
        pass

    @staticmethod
    def get() -> str:
        _, output, _ = _ex_subprocess("xclip -o")
        return output

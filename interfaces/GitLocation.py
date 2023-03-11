from interfaces.Interface import Interface

from core.CLIFormat import *
from core.Register import Type, Register

from schema import Schema, Use


@Register(Type.IFACE, "git_location", "Stores directory and branch")
class GitLocation(Interface):
    def __init__(self):
        super().__init__(Schema({
            "dir": Use(str),
            "branch": Use(str)
        }))

    def to_string(data: dict) -> str:
        msg = CLIFormat.colored("dir",
                                CLIFormat.WARNING + CLIFormat.BOLD) + ": "
        msg += CLIFormat.colored(data["dir"] + " ", CLIFormat.OKBLUE)
        msg += CLIFormat.colored(" branch",
                                 CLIFormat.WARNING + CLIFormat.BOLD) + ": "
        msg += CLIFormat.colored(data["branch"] + " ", CLIFormat.OKBLUE)
        return msg

    def serialize(data: dict) -> str:
        pass

    def deserialize(data: str) -> dict:
        pass

import pytermgui

from interfaces.Interface import Interface

from core.CLIFormat import *

from schema import Schema, Use


class GitLocation(Interface):
    def __init__(self):
        super().__init__(Schema({
            "dir": Use(str),
            "branch": Use(str)
        }))

    def to_string(self, data: dict) -> str:
        msg = CLIFormat.colored("dir",
                                CLIFormat.WARNING + CLIFormat.BOLD) + ": "
        msg += CLIFormat.colored(data["dir"] + " ", CLIFormat.OKBLUE)
        msg += CLIFormat.colored(" branch",
                                 CLIFormat.WARNING + CLIFormat.BOLD) + ": "
        msg += CLIFormat.colored(data["branch"] + " ", CLIFormat.OKBLUE)
        return msg

    def to_tim(self, data: dict) -> str:
        return "[magenta]" + \
            data["dir"].split("/")[-1] + "[cyan]@[lime]" + \
            data["branch"] + "[/]"

    def serialize(self, data: dict) -> str:
        pass

    def deserialize(self, data: str) -> dict:
        pass

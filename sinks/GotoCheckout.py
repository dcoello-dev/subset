import git

from core.Register import Type, Register
from core.CLIFormat import CLIFormat

from sinks.Sink import Sink


@Register(Type.SINK, "goto_checkout",
          "Go to directory and checkout to branch")
class GotoCheckout(Sink):
    def __init__(self):
        pass

    @staticmethod
    def send(data: dict) -> None:
        CLIFormat.write_on_parent_shell("cd " + data["dir"])
        repo = git.Repo.init(data["dir"])
        cmd = repo.git
        cmd.checkout(data["branch"])

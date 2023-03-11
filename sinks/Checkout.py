import os
import git

from core.Register import Type, Register

from sinks.Sink import Sink
from interfaces.SimpleString import SimpleString


@Register(Type.SINK, "checkout", "Checkout to branch")
class Checkout(Sink):
    def __init__(self):
        super().__init__(SimpleString)

    def send_sink(data: dict) -> None:
        repo_dir = os.getcwd()
        repo = git.Repo.init(repo_dir)
        cmd = repo.git
        cmd.checkout(data["str"])

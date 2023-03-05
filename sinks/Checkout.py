import os
import git

from core.Register import Type, Register

from sinks.Sink import Sink


@Register(Type.SINK, "checkout", "Checkout to branch")
class Checkout(Sink):
    def __init__(self):
        pass

    @staticmethod
    def send(data: str) -> None:
        repo_dir = os.getcwd()
        repo = git.Repo.init(repo_dir)
        cmd = repo.git
        cmd.checkout(data)

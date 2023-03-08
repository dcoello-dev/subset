import os
import git

from core.Register import Type, Register

from sources.Source import Source


@Register(Type.SOURCE, "git_dir", "Get actual dir and branch as source")
class GitDir(Source):
    def __init__(self):
        pass

    @staticmethod
    def get() -> dict:
        repo_dir = os.getcwd()
        repo = git.Repo.init(repo_dir)
        return dict(dir=repo_dir, branch=repo.active_branch.name)

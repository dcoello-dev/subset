import os
import git

from core.Register import Type, Register

from sources.Source import Source

from interfaces.GitLocation import GitLocation


@Register(Type.SOURCE, "git_dir", "Get actual dir and branch as source")
class GitDir(Source):
    def __init__(self):
        super().__init__(GitLocation)

    def get_source(self) -> dict:
        repo_dir = os.getcwd()
        repo = git.Repo.init(repo_dir)
        return dict(dir=repo_dir, branch=repo.active_branch.name)

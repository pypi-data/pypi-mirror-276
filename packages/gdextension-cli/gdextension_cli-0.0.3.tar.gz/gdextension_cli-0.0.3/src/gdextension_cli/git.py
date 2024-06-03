"""
Abstractions for using git as an external tool.
"""

import logging
import subprocess
from pathlib import Path


class Repository:
    """A git repository."""

    root_path: Path

    def __init__(self, root_path: Path | str):
        self.root_path = Path(root_path)

    def clone(self, url: str, branch: str) -> "Repository":
        """
        Clones a git repository.
        :param url: The url of the repository.
        :param branch: The branch of the repository.
        :return: The repository itself.
        """
        self._run_git("clone", "-b", branch, url, str(self.root_path))
        return self

    def init(self) -> "Repository":
        """
        Initializes the repository with 'git init'.
        :return: The repository itself.
        """
        self._run_git("init")
        return self

    def add_submodule(self, url: str, branch: str):
        """
        Adds a submodule to the repository.
        :param url: The url of the submodule.
        :param branch: The branch of the submodule to be checked out.
        """
        self._run_git("submodule", "add", "-b", branch, url)

    def _run_git(self, *args: str):
        """
        Runs a git command with the given arguments and waits for it to complete.
        :param args: The arguments for the git command.
        """
        command = ["git"] + list(args)
        logging.debug("Running command: %s", " ".join(command))

        with subprocess.Popen(
            command,
            cwd=self.root_path,
            shell=True,
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ) as process:
            process.wait()

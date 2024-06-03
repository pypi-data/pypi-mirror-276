"""
Command to create a new project from a git template directory.
"""

import tempfile
import logging
from argparse import Namespace
from pathlib import Path

from gdextension_cli.commands.new_project_from_local import NewProjectFromLocalCommand
from gdextension_cli.git import Repository


class NewProjectFromGitCommand:
    """Command that creates a new project from a git repository."""

    def __init__(
        self,
        project_name: str,
        project_path: Path,
        godot_version: str,
    ):
        """
        Initializes the command.
        :param project_name: Name of the project.
        :param project_path: Path to the project.
        :param godot_version: Version of godot.
        """
        self.project_name = project_name
        self.project_path = project_path
        self.godot_version = godot_version
        self.template_repository_url = None
        self.template_version = None

    @staticmethod
    def from_arguments(args: Namespace) -> "NewProjectFromGitCommand":
        """
        Initializes the command from command line arguments.
        :param args: Command line arguments.
        :return: The created NewProjectFromGitCommand.
        """
        command = NewProjectFromGitCommand(
            args.name,
            args.output_path if args.output_path else Path.cwd() / args.name,
            args.godot_version,
        )
        command.template_repository_url = args.from_git
        command.template_version = args.template_version
        return command

    def run(self):
        """Runs the command to create a new project from a git repository."""
        logging.info("Creating new project '%s'", self.project_name)
        logging.info("Project path: %s", self.project_path)
        logging.info("Godot version: %s", self.godot_version)
        logging.info("Template repository: %s", self.template_repository_url)
        logging.info("Template version: %s", self.template_version)
        logging.info("########################################")

        with tempfile.TemporaryDirectory() as temp_dir:
            logging.info("Cloning template repository to %s", temp_dir)
            Repository(temp_dir).clone(
                self.template_repository_url, self.template_version
            )

            NewProjectFromLocalCommand(
                self.project_name,
                self.project_path,
                self.godot_version,
                temp_dir,
            ).run_processes()

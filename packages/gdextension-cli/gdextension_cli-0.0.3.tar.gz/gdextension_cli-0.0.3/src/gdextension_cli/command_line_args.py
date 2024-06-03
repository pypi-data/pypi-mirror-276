"""
Parser for command line arguments
"""

import argparse
import pathlib

from .__version__ import __version__


class CommandLineArgs:
    """
    Contains definitions and parses command line arguments.
    """

    HELP_OUTPUT_PATH = (
        "Output path of the project. "
        "Default: folder in current directory with name of the project"
    )

    HELP_REPOSITORY_URL = (
        "URL of a project template repository. "
        "Default is https://github.com/3LK3/gdextension-template.git"
    )

    HELP_TEMPLATE_VERSION = (
        "Branch name in template repository. "
        "ONLY valid in combination with --from-git. Default: 4.2"
    )

    HELP_GODOT_VERSION = (
        "Godot version (branch name in godot-cpp repository)."
        "Use master for latest version. Default: 4.2"
    )

    def __init__(self):
        self._parser = argparse.ArgumentParser(prog="gdextension-cli")
        self._subcommands = self._parser.add_subparsers(dest="subcommand")
        self._parser.add_argument(
            "-v", "--version", action="version", version=__version__
        )

    def create(self):
        """Created all subcommands and arguments"""
        self._create_command_new()
        # self._create_command_build()
        self._subcommands.add_parser("help", help="Shows this help")
        return self

    def _create_command_new(self):
        """Creates the parser for the new project command"""
        new_parser = self._subcommands.add_parser("new", help="Create a new project")
        new_parser.add_argument(
            "-v", "--verbose", action="store_true", help="More output!"
        )
        new_parser.add_argument("name", type=str, help="Name of the new project")
        new_parser.add_argument(
            "-o",
            "--output-path",
            type=pathlib.Path,
            required=False,
            help=self.HELP_OUTPUT_PATH,
        )
        new_parser.add_argument(
            "-g",
            "--godot-version",
            type=str,
            default="4.2",
            help=self.HELP_GODOT_VERSION,
        )
        new_parser.add_argument(
            "-t",
            "--template-version",
            type=str,
            default="4.2",
            help=self.HELP_TEMPLATE_VERSION,
        )

        from_group = new_parser.add_mutually_exclusive_group(required=False)
        from_group.add_argument(
            "--from-git",
            metavar="GIT_URL",
            type=str,
            required=False,
            default="https://github.com/3LK3/gdextension-template.git",
            help=self.HELP_REPOSITORY_URL,
        )
        from_group.add_argument(
            "--from-local",
            metavar="PATH",
            type=pathlib.Path,
            required=False,
            help="Path to a local folder containing a project template",
        )

    def parse(self) -> argparse.Namespace:
        """
        Parses command line arguments.
        :return: The namespace containing parsed arguments.
        """
        return self._parser.parse_args()

    def print_help(self):
        """Prints the help content."""
        self._parser.print_help()

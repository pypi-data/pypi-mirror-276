"""
gdextension_cli entry point with callable function main_cli()
"""

import logging

from .command_line_args import CommandLineArgs
from .commands.new_project_from_local import NewProjectFromLocalCommand
from .commands.new_project_from_git import NewProjectFromGitCommand


def main_cli():
    """gdextension-cli main entry point used in pyproject.toml"""
    command_line = CommandLineArgs()
    args = command_line.create().parse()

    initialize_logging(args.verbose if hasattr(args, "verbose") else logging.INFO)

    match args.subcommand:
        case "new":
            if args.from_local:
                NewProjectFromLocalCommand.from_arguments(args).run()
            elif args.from_git:
                NewProjectFromGitCommand.from_arguments(args).run()
            else:
                raise AssertionError(
                    "Expected arguments '--from-local' or '--from-git'"
                )
        case _:
            command_line.print_help()


def initialize_logging(verbose: bool):
    """
    Initializes the logging module with a log level based on the given verbose argument.
    :param verbose: DEBUG if True, otherwise INFO
    """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(levelname)s - %(message)s",
    )

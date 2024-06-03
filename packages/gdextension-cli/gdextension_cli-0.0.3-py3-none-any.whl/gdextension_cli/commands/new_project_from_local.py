"""
Command to create a new project from a local template directory.
"""

import glob
import logging
import shutil
from argparse import Namespace
from pathlib import Path

from gdextension_cli.git import Repository
from gdextension_cli.template_renderer import TemplateRenderer


class NewProjectFromLocalCommand:
    """Command that creates a new project from a local directory."""

    TEMPLATE_FILE_EXTENSION = ".tmpl"
    GODOT_CPP_URL = "https://github.com/godotengine/godot-cpp"
    IGNORED_DIRECTORIES = ["godot-cpp", "godot_cpp"]

    def __init__(
        self,
        project_name: str,
        project_path: Path,
        godot_version: str,
        template_path: Path | str,
    ):
        """
        Initializes the command.
        :param project_name: Name of the project.
        :param project_path: Path to the project.
        :param godot_version: Version of godot.
        :param template_path: Path to the template directory.
        """
        self.project_name = project_name
        self.project_path = project_path
        self.godot_version = godot_version
        self.template_path = Path(template_path)

    @staticmethod
    def from_arguments(args: Namespace) -> "NewProjectFromLocalCommand":
        """
        Initializes the command from command line arguments.
        :param args: Command line arguments.
        :return: The created NewProjectFromLocalCommand.
        """
        return NewProjectFromLocalCommand(
            args.name,
            args.output_path if args.output_path else Path.cwd() / args.name,
            args.godot_version,
            args.from_local,
        )

    def run(self):
        """
        Runs the command to create a new project from a local template directory.
        """
        logging.info("Creating new project '%s'", self.project_name)
        logging.info("Project path: %s", self.project_path)
        logging.info("Godot version: %s", self.godot_version)
        logging.info("Template path: %s", self.template_path)

        self.run_processes()

    def run_processes(self):
        """
        Runs the main logic of creating a new project.
         - checks for template and project directories
         - creates a git repository in the project directory
         - copies files and renders templates to the project directory
         - adds godot-cpp as a submodule the projects git repository
        """
        self._check_directories()

        project_repo = Repository(self.project_path)
        project_repo.init()

        self._copy_non_template_files()
        self._render_template_files()

        logging.info("Adding submodule godot-cpp from %s", self.GODOT_CPP_URL)
        project_repo.add_submodule(self.GODOT_CPP_URL, self.godot_version)

    def get_template_data(self) -> dict[str, str]:
        """
        Returns a dictionary containing the data used for templating.
        :return: Dictionary containing the data
        """
        return {
            "name": self.project_name,
            "lib_name": self.project_name.lower().replace("_", ""),
            "class_name": self._get_class_name(),
        }

    def _check_directories(self):
        """
        Checks for project and template directories.
        Creates project directory if it doesn't exist.
        """
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template path not found: {self.template_path}")
        if not self.project_path.exists():
            logging.debug("Creating project directory at %s", self.project_path)
            self.project_path.mkdir(parents=True)

    def _copy_file(self, file: Path | str):
        """
        Copies the given relative file from template path to the corresponding new project.
        :param file: The relative file path.
        """
        source_file = self.template_path / file
        if source_file.is_dir():
            return

        target_file = self.project_path / file
        if not target_file.parent.exists():
            logging.debug("Creating directory at %s", target_file.parent)
            target_file.parent.mkdir(parents=True)

        logging.info("Copy file %s to %s", file, target_file)
        shutil.copy(source_file, target_file)

    def _copy_non_template_files(self):
        """
        Copies all non template files from template_path to project_path.
        Non template files are all file without the extension '.tmpl'.
        """
        logging.info("Copying non template files ...")
        non_template_files = self._get_non_template_files()

        for file in non_template_files:
            if self._should_ignore(file):
                continue
            self._copy_file(file)

        self._copy_file(".gitignore")

    def _get_class_name(self) -> str:
        class_name = ""
        for part in self.project_name.lower().split("_"):
            class_name += part.capitalize()
        return class_name

    def _get_non_template_files(self) -> list[str]:
        """
        Returns a list of all non-template files.
        :return: All non-template files.
        """
        files = glob.glob(
            "**/*",
            root_dir=self.template_path,
            recursive=True,
        )
        return [file for file in files if not file.endswith(self.TEMPLATE_FILE_EXTENSION)]

    def _render_template_files(self):
        """
        Renders all template files from template_path to project_path.
        Template files are all files with the extension '.tmpl'.
        """
        logging.info("Copying template files ...")
        template_files = glob.glob(
            f"**/*{self.TEMPLATE_FILE_EXTENSION}",
            root_dir=self.template_path,
            recursive=True,
        )
        template_renderer = TemplateRenderer(
            self.template_path, self.get_template_data()
        )

        for file in template_files:
            source_file = self.template_path / file
            if source_file.is_dir():
                continue

            # Supports templated file names
            target_file = template_renderer.render_path(
                self.project_path / file, self.TEMPLATE_FILE_EXTENSION
            )
            if not target_file.parent.exists():
                logging.debug("Creating directory at %s", target_file.parent)
                target_file.parent.mkdir(parents=True)

            logging.info("Render template %s to %s", file, target_file)
            template_renderer.render_file(str(file), target_file)

    def _should_ignore(self, file_path) -> bool:
        """
        Whether to ignore the given file or not.
        :param file_path: The file path to be checked.
        :return: True if the file should be ignored. False otherwise.
        """
        for ignored in self.IGNORED_DIRECTORIES:
            if file_path.startswith(ignored):
                logging.debug("Ignoring %s", file_path)
                return True
        return False

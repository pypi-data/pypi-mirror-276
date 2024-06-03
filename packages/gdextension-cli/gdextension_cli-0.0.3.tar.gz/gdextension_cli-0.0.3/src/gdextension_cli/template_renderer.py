"""
Contains anything for rendering templates.
"""

import logging
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class TemplateRenderer:
    """Template renderer does what its name says."""

    environment: Environment
    data: dict[str, str]

    def __init__(self, template_path, data: dict[str, str]):
        logging.debug("Initializing template renderer ...")
        self.environment = Environment(loader=FileSystemLoader(template_path))
        self.data = data
        logging.debug("Using template data: %s", self.data)

    def render_path(self, path: Path, remove_extension: str | None = None) -> Path:
        """
        Renders the given path and removes the file extension if any given.
        :param path: Path to be rendered
        :param remove_extension: The file extension to be removed. Example: '.tmpl'
        :return: The rendered path
        """
        result = self.environment.from_string(str(path)).render(self.data)
        if remove_extension is not None:
            result = result[: -len(remove_extension)]
        return Path(result)

    def render_file(self, file: str, output_file: Path):
        """
        Renders the given file and writes it to the given output file.
        :param file: The file to be rendered
        :param output_file: The output file path
        """
        self.environment.get_template(file.replace("\\", "/")).stream(self.data).dump(
            str(output_file)
        )

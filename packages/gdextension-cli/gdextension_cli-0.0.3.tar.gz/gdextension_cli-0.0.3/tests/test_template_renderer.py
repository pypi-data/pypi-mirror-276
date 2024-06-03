from pathlib import Path

import pytest

from gdextension_cli.template_renderer import TemplateRenderer


@pytest.fixture
def simple_data():
    return {"name": "simple"}


def test_render_simple_path_correct(simple_data):
    renderer = TemplateRenderer("it/doesnt/matter", simple_data)
    actual = renderer.render_path(Path("/i/want/to/say/{{name}}.txt"))
    assert actual == Path(f"/i/want/to/say/{simple_data["name"]}.txt")

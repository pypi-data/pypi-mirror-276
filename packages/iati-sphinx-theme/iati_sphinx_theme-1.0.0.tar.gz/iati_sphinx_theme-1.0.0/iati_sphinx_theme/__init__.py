"""A sphinx theme for IATI documentation sites."""

from os import path

import sphinx.application


def setup(app: sphinx.application.Sphinx) -> None:
    app.add_html_theme("iati_sphinx_theme", path.abspath(path.dirname(__file__)))

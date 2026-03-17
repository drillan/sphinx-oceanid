"""sphinx-oceanid: High-quality Mermaid diagrams in Sphinx."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.application import Sphinx

__version__ = "0.1.0"

_STATIC_DIR = str(Path(__file__).parent / "_static")


def setup(app: Sphinx) -> dict[str, bool | str]:
    """Sphinx extension entry point.

    Registers nodes, directives, config values, and event handlers.
    """
    from .assets import install_assets
    from .config import register_config_values, validate_config
    from .directives import Mermaid
    from .nodes import mermaid_node
    from .visitors import html_depart_mermaid, html_visit_mermaid

    register_config_values(app)
    app.add_node(mermaid_node, html=(html_visit_mermaid, html_depart_mermaid))
    app.add_directive("mermaid", Mermaid)
    app.connect("config-inited", validate_config)
    app.connect("html-page-context", install_assets)
    app.connect("builder-inited", _register_static_path)

    return {"version": __version__, "parallel_read_safe": True}


def _register_static_path(app: Sphinx) -> None:
    """Register the extension's _static directory for file copying."""
    app.config.html_static_path.append(_STATIC_DIR)

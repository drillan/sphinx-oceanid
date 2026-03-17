"""sphinx-oceanid: High-quality Mermaid diagrams in Sphinx."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.application import Sphinx

__version__ = "0.1.0"


def setup(app: Sphinx) -> dict[str, bool | str]:
    """Sphinx extension entry point.

    Registers nodes, directives, config values, and event handlers.
    """
    from .assets import install_assets
    from .config import register_config_values
    from .directives import Mermaid
    from .nodes import mermaid_node
    from .visitors import html_depart_mermaid, html_visit_mermaid

    register_config_values(app)
    app.add_node(mermaid_node, html=(html_visit_mermaid, html_depart_mermaid))
    app.add_directive("mermaid", Mermaid)
    app.connect("html-page-context", install_assets)

    return {"version": __version__, "parallel_read_safe": True}

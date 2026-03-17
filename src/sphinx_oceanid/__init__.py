"""sphinx-oceanid: High-quality Mermaid diagrams in Sphinx."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.application import Sphinx

__version__ = "0.1.0"


def setup(app: Sphinx) -> dict[str, bool | str]:
    """Sphinx extension entry point.

    Registers config values. Directives, visitors, and event
    handlers will be added in subsequent implementation phases.
    """
    from .config import register_config_values

    register_config_values(app)
    return {"version": __version__, "parallel_read_safe": True}

"""HTML visitor functions for mermaid_node."""

from __future__ import annotations

import html
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.writers.html5 import HTML5Translator

    from .nodes import mermaid_node


def html_visit_mermaid(self: HTML5Translator, node: mermaid_node) -> None:
    """Generate opening HTML for a Mermaid diagram.

    Outputs ``<div class="oceanid-diagram" data-oceanid-code="...">``
    with ``<noscript>`` for accessibility (FR-011, FR-020).
    """
    code: str = node["code"]

    classes = ["oceanid-diagram"]
    align: str = node.get("align", "")
    if align:
        classes.append(f"align-{align}")

    attrs: list[str] = [f'class="{" ".join(classes)}"']

    ids: list[str] = node.get("ids", [])
    if ids:
        attrs.append(f'id="{html.escape(ids[0], quote=True)}"')

    # FR-020: XSS-safe data attribute
    attrs.append(f'data-oceanid-code="{html.escape(code, quote=True)}"')

    if node.get("zoom", False):
        attrs.append("data-oceanid-zoom")

    self.body.append(f"<div {' '.join(attrs)}>\n")

    # FR-011: noscript for accessibility
    self.body.append(f"<noscript><pre>{html.escape(code)}</pre></noscript>\n")


def html_depart_mermaid(self: HTML5Translator, node: mermaid_node) -> None:
    """Generate closing HTML for a Mermaid diagram."""
    self.body.append("</div>\n")

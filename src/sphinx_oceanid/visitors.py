"""HTML visitor functions for mermaid_node."""

from __future__ import annotations

import html
import json
from typing import TYPE_CHECKING

from docutils.nodes import SkipNode
from sphinx.util import logging

from .diagram_types import unsupported_diagram_message

if TYPE_CHECKING:
    from sphinx.writers.html5 import HTML5Translator

    from .nodes import mermaid_node

logger = logging.getLogger(__name__)


def _render_unsupported(self: HTML5Translator, node: mermaid_node) -> None:
    """Render HTML for an unsupported diagram type and raise SkipNode.

    Outputs ``<div class="oceanid-unsupported">`` with a message listing
    supported types and the original Mermaid source code.
    """
    code: str = node["code"]
    diagram_type: str | None = node.get("diagram_type")
    message = unsupported_diagram_message(diagram_type)

    logger.warning("%s", message, location=node)

    self.body.append('<div class="oceanid-unsupported">\n')
    self.body.append(f'<p class="oceanid-unsupported-message">{html.escape(message)}</p>\n')
    self.body.append(f'<pre class="oceanid-unsupported-code">{html.escape(code)}</pre>\n')
    self.body.append("</div>\n")

    raise SkipNode


def html_visit_mermaid(self: HTML5Translator, node: mermaid_node) -> None:
    """Generate opening HTML for a Mermaid diagram.

    Outputs ``<div class="oceanid-diagram" ...>`` with:

    - ``aria-label`` from ``:alt:`` for accessibility (FR-014)
    - ``data-oceanid-code`` with XSS-safe escaped Mermaid source (FR-020)
    - ``data-oceanid-zoom`` when ``:zoom:`` is enabled
    - ``id`` from ``:name:`` or auto-generated ``zoom_id``
    - ``<noscript>`` plain-text source display (FR-011)

    For unsupported diagram types, delegates to ``_render_unsupported``.
    """
    if not node["is_supported"]:
        _render_unsupported(self, node)
        return  # _render_unsupported raises SkipNode; return as safety net

    code: str = node["code"]

    classes = ["oceanid-diagram"]
    align: str = node.get("align", "")
    if align:
        classes.append(f"align-{align}")

    attrs: list[str] = [f'class="{" ".join(classes)}"']

    ids: list[str] = node.get("ids", [])
    if ids:
        attrs.append(f'id="{html.escape(ids[0], quote=True)}"')

    # FR-014: alt → aria-label for accessibility
    alt: str = node.get("alt", "")
    if alt:
        attrs.append(f'aria-label="{html.escape(alt, quote=True)}"')

    # FR-020: XSS-safe data attribute
    attrs.append(f'data-oceanid-code="{html.escape(code, quote=True)}"')

    mermaid_config: dict[str, object] = node.get("mermaid_config", {})
    if mermaid_config:
        config_json = json.dumps(mermaid_config, ensure_ascii=False)
        attrs.append(f'data-oceanid-config="{html.escape(config_json, quote=True)}"')

    mermaid_title: str = node.get("mermaid_title", "")
    if mermaid_title:
        attrs.append(f'data-oceanid-title="{html.escape(mermaid_title, quote=True)}"')

    zoom_globally = bool(self.config.oceanid_zoom)
    if node.get("zoom", False) or zoom_globally:
        attrs.append("data-oceanid-zoom")

    zoom_id: str = node.get("zoom_id", "")
    if zoom_id and not ids:
        attrs.insert(1, f'id="{html.escape(zoom_id, quote=True)}"')

    # Apply width/height as CSS custom properties when non-default
    style_parts: list[str] = []
    width: str = self.config.oceanid_width
    height: str = self.config.oceanid_height
    if width != "100%":
        style_parts.append(f"--oceanid-width: {html.escape(width, quote=True)}")
    if height != "auto":
        style_parts.append(f"--oceanid-height: {html.escape(height, quote=True)}")
    if style_parts:
        attrs.append(f'style="{"; ".join(style_parts)}"')

    self.body.append(f"<div {' '.join(attrs)}>\n")

    # FR-011: noscript for accessibility
    self.body.append(f"<noscript><pre>{html.escape(code)}</pre></noscript>\n")


def html_depart_mermaid(self: HTML5Translator, node: mermaid_node) -> None:
    """Generate closing HTML for a Mermaid diagram."""
    self.body.append("</div>\n")

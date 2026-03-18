"""HTML visitor functions for mermaid_node."""

from __future__ import annotations

import html
import json
from typing import TYPE_CHECKING

from docutils.nodes import SkipNode
from sphinx.util import logging

from .config import SUPPORTED_DIAGRAM_TYPES

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
    diagram_type: str = node.get("diagram_type") or "unknown"
    supported_list = ", ".join(sorted(SUPPORTED_DIAGRAM_TYPES))

    logger.warning(
        'Diagram type "%s" is not supported by sphinx-oceanid. Supported types: %s',
        diagram_type,
        supported_list,
        location=node,
    )

    self.body.append('<div class="oceanid-unsupported">\n')
    self.body.append(
        f'<p class="oceanid-unsupported-message">'
        f"Diagram type &quot;{html.escape(diagram_type)}&quot; "
        f"is not supported by sphinx-oceanid. "
        f"Supported types: {html.escape(supported_list)}."
        f"</p>\n"
    )
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

    self.body.append(f"<div {' '.join(attrs)}>\n")

    # FR-011: noscript for accessibility
    self.body.append(f"<noscript><pre>{html.escape(code)}</pre></noscript>\n")


def html_depart_mermaid(self: HTML5Translator, node: mermaid_node) -> None:
    """Generate closing HTML for a Mermaid diagram."""
    self.body.append("</div>\n")

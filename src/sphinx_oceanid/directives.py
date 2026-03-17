"""Mermaid directive for RST (SphinxDirective-based)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils.parsers.rst import directives
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

from .diagram_types import extract_diagram_type, is_supported_diagram
from .nodes import mermaid_node

if TYPE_CHECKING:
    from docutils import nodes

logger = logging.getLogger(__name__)


class Mermaid(SphinxDirective):
    """Sphinx directive for embedding Mermaid diagrams."""

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {  # noqa: RUF012
        "name": directives.unchanged,
        "align": lambda arg: directives.choice(arg, ("left", "center", "right")),
        "zoom": directives.flag,
    }

    def run(self) -> list[nodes.Node]:
        """Parse directive content and create mermaid_node."""
        code = self._get_code()
        if not code.strip():
            logger.warning(
                "mermaid directive has empty content",
                location=(self.env.docname, self.lineno),
            )
            return []

        diagram_type = extract_diagram_type(code)
        is_supported = is_supported_diagram(diagram_type)

        node = mermaid_node()
        node["code"] = code
        node["diagram_type"] = diagram_type
        node["is_supported"] = is_supported
        node["align"] = self.options.get("align", "")
        node["alt"] = ""
        node["zoom"] = "zoom" in self.options
        node["zoom_id"] = ""

        self.add_name(node)

        return [node]

    def _get_code(self) -> str:
        """Get Mermaid code from directive content."""
        return "\n".join(self.content)

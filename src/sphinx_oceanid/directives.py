"""Mermaid directive for RST (SphinxDirective-based)."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import yaml
from docutils import nodes as docutils_nodes
from docutils.parsers.rst import directives
from sphinx.errors import ExtensionError
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

from .config import SUPPORTED_DIAGRAM_TYPES
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
        "alt": directives.unchanged,
        "caption": directives.unchanged,
        "config": directives.unchanged,
        "title": directives.unchanged,
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

        code = self._apply_mermaid_frontmatter(code)

        diagram_type = extract_diagram_type(code)
        is_supported = is_supported_diagram(diagram_type)

        if not is_supported and self.config.oceanid_unsupported_action == "error":
            supported_list = ", ".join(sorted(SUPPORTED_DIAGRAM_TYPES))
            raise ExtensionError(
                f'Diagram type "{diagram_type or "unknown"}" '
                f"is not supported by sphinx-oceanid. "
                f"Supported types: {supported_list}."
            )

        zoom_enabled = "zoom" in self.options
        zoom_id = ""
        if zoom_enabled:
            serial = self.env.new_serialno("oceanid-zoom")
            zoom_id = f"oceanid-zoom-{serial}"

        node = mermaid_node()
        node["code"] = code
        node["diagram_type"] = diagram_type
        node["is_supported"] = is_supported
        node["align"] = self.options.get("align", "")
        node["alt"] = self.options.get("alt", "")
        node["zoom"] = zoom_enabled
        node["zoom_id"] = zoom_id

        self.add_name(node)

        if "caption" in self.options:
            return self._figure_wrapper(node)

        return [node]

    def _get_code(self) -> str:
        """Get Mermaid code from directive content."""
        return "\n".join(self.content)

    def _apply_mermaid_frontmatter(self, code: str) -> str:
        """Inject :config: and :title: options into Mermaid frontmatter."""
        config_dict: dict[str, object] = {}

        if "config" in self.options:
            try:
                parsed = json.loads(self.options["config"])
            except json.JSONDecodeError as exc:
                logger.warning(
                    "Invalid JSON in :config: option: %s",
                    exc,
                    location=(self.env.docname, self.lineno),
                )
                parsed = {}
            if isinstance(parsed, dict):
                config_dict.update(parsed)

        frontmatter: dict[str, object] = {}
        if config_dict:
            frontmatter["config"] = config_dict
        if "title" in self.options:
            frontmatter["title"] = self.options["title"]

        if not frontmatter:
            return code

        frontmatter_yaml = yaml.dump(
            frontmatter,
            default_flow_style=False,
            allow_unicode=True,
        ).rstrip("\n")

        return f"---\n{frontmatter_yaml}\n---\n{code}"

    def _figure_wrapper(self, node: mermaid_node) -> list[nodes.Node]:
        """Wrap mermaid_node in a figure with figcaption."""
        caption_text = self.options["caption"]
        caption_nodes = self.parse_text_to_nodes(caption_text)

        figure_node = docutils_nodes.figure()
        figure_node.append(node)

        caption_node = docutils_nodes.caption(caption_text, "", *caption_nodes)
        figure_node.append(caption_node)

        return [figure_node]

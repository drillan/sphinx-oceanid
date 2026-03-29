"""Mermaid directive for RST (SphinxDirective-based)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from docutils import nodes as docutils_nodes
from docutils.parsers.rst import directives
from sphinx.errors import ExtensionError
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

from .autoclassdiag import class_diagram
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
    optional_arguments = 1
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
                self._empty_content_warning(),
                location=(self.env.docname, self.lineno),
            )
            return []

        mermaid_config = self._parse_mermaid_config()
        mermaid_title = self.options.get("title", "")

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
        node["mermaid_config"] = mermaid_config
        node["mermaid_title"] = mermaid_title

        self.add_name(node)

        if "caption" in self.options:
            return self._figure_wrapper(node)

        return [node]

    def _empty_content_warning(self) -> str:
        """Return warning message for empty directive content."""
        return "mermaid directive has empty content"

    def _get_code(self) -> str:
        """Get Mermaid code from directive argument (external file) or inline content."""
        if self.arguments:
            return self._load_external_code(self.arguments[0])
        return "\n".join(self.content)

    def _load_external_code(self, filepath: str) -> str:
        """Load Mermaid code from an external file.

        Args:
            filepath: Path relative to the Sphinx source directory.

        Returns:
            File content as a string.

        Raises:
            ExtensionError: If the file is not found.
        """
        source_dir = Path(self.env.srcdir)
        target = source_dir / filepath
        try:
            return target.read_text(encoding="utf-8")
        except FileNotFoundError:
            raise ExtensionError(
                f"External Mermaid file not found: {filepath}",
                modname="sphinx_oceanid",
            ) from None

    def _parse_mermaid_config(self) -> dict[str, object]:
        """Parse :config: option into a dict.

        Returns:
            Parsed config dict, or empty dict if no config or invalid JSON.
        """
        if "config" not in self.options:
            return {}

        try:
            parsed = json.loads(self.options["config"])
        except json.JSONDecodeError as exc:
            logger.warning(
                "Invalid JSON in :config: option: %s",
                exc,
                location=(self.env.docname, self.lineno),
            )
            return {}

        if isinstance(parsed, dict):
            return parsed
        logger.warning(
            ":config: option must be a JSON object, got %s",
            type(parsed).__name__,
            location=(self.env.docname, self.lineno),
        )
        return {}

    def _figure_wrapper(self, node: mermaid_node) -> list[nodes.Node]:
        """Wrap mermaid_node in a figure with figcaption."""
        caption_text = self.options["caption"]
        caption_nodes = self.parse_text_to_nodes(caption_text)

        figure_node = docutils_nodes.figure()
        figure_node.append(node)

        caption_node = docutils_nodes.caption(caption_text, "", *caption_nodes)
        figure_node.append(caption_node)

        return [figure_node]


class MermaidClassDiagram(Mermaid):
    """Directive for auto-generating Mermaid class diagrams from Python class hierarchies.

    Usage::

        .. autoclasstree:: mypackage.MyClass
           :full:

    Overrides ``_get_code()`` to generate classDiagram from the given class arguments.
    All other behavior (frontmatter, options, node creation) is inherited from ``Mermaid``.
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 100
    option_spec = {  # noqa: RUF012
        **Mermaid.option_spec,
        "full": directives.flag,
        "strict": directives.flag,
        "namespace": directives.unchanged,
    }

    def _empty_content_warning(self) -> str:
        """Return warning message when no inheritance relationships are found."""
        return f"autoclasstree: no inheritance relationships found for {', '.join(self.arguments)}"

    def _get_code(self) -> str:
        """Generate Mermaid classDiagram code from Python class hierarchies."""
        return class_diagram(
            *self.arguments,
            full="full" in self.options,
            strict="strict" in self.options,
            namespace=self.options.get("namespace"),
        )

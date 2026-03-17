"""Tests for mermaid directive (Layer 2: Sphinx integration)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from sphinx.errors import ExtensionError

from sphinx_oceanid.nodes import mermaid_node

if TYPE_CHECKING:
    from sphinx.application import Sphinx


class TestMermaidDirective:
    """Tests for the mermaid directive."""

    @pytest.mark.sphinx("html", testroot="basic")
    def test_directive_creates_node(self, app: Sphinx) -> None:
        """mermaid directive creates mermaid_node in doctree."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        assert len(nodes) >= 1

    @pytest.mark.sphinx("html", testroot="basic")
    def test_directive_extracts_diagram_type(self, app: Sphinx) -> None:
        """Diagram type is correctly parsed from directive content."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        diagram_types = {n["diagram_type"] for n in nodes}
        assert "sequenceDiagram" in diagram_types
        assert "flowchart" in diagram_types

    @pytest.mark.sphinx("html", testroot="empty-content")
    def test_directive_empty_content_warns(self, app: Sphinx) -> None:
        """Empty mermaid content produces a Sphinx warning about empty content."""
        app.build()
        warnings = app._warning.getvalue()  # type: ignore[attr-defined]
        # After implementation, the mermaid directive should warn about empty content.
        # "empty content" (with space) avoids matching the path "empty-content" (with hyphen).
        assert "empty content" in warnings.lower()


class TestUnsupportedActionError:
    """Tests for oceanid_unsupported_action='error' (US4)."""

    @pytest.mark.sphinx(
        "html",
        testroot="unsupported-diagram",
        confoverrides={"oceanid_unsupported_action": "error"},
    )
    def test_unsupported_action_error(self, app: Sphinx) -> None:
        """oceanid_unsupported_action='error' causes build failure."""
        with pytest.raises(ExtensionError, match="not supported"):
            app.build()

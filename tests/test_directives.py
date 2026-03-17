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


class TestDirectiveOptions:
    """Tests for directive options: caption, zoom, alt, config, title (T037)."""

    @pytest.mark.sphinx("html", testroot="basic")
    def test_directive_with_caption_creates_figure(self, app: Sphinx) -> None:
        """caption option wraps mermaid_node in a figure node."""
        from docutils.nodes import figure

        app.build()
        doctree = app.env.get_doctree("index")
        figures = list(doctree.findall(figure))
        # At least one figure should exist (the captioned diagram)
        assert len(figures) >= 1
        # The figure should contain a mermaid_node
        mermaid_in_figure = list(figures[0].findall(mermaid_node))
        assert len(mermaid_in_figure) >= 1

    @pytest.mark.sphinx("html", testroot="basic")
    def test_directive_with_zoom_sets_zoom_id(self, app: Sphinx) -> None:
        """zoom option generates a zoom_id on the mermaid_node."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        zoom_nodes = [n for n in nodes if n.get("zoom")]
        assert len(zoom_nodes) >= 1
        for n in zoom_nodes:
            assert n["zoom_id"], "zoom_id must be non-empty when zoom is enabled"

    @pytest.mark.sphinx("html", testroot="basic")
    def test_directive_with_alt(self, app: Sphinx) -> None:
        """alt option stores alt text on the mermaid_node."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        alt_nodes = [n for n in nodes if n.get("alt")]
        assert len(alt_nodes) >= 1
        assert alt_nodes[0]["alt"] == "Sequence diagram of greeting"

    @pytest.mark.sphinx("html", testroot="basic")
    def test_directive_with_config_frontmatter(self, app: Sphinx) -> None:
        """config option injects frontmatter into mermaid code."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        config_nodes = [n for n in nodes if "---" in n["code"]]
        assert len(config_nodes) >= 1
        assert "theme: forest" in config_nodes[0]["code"]

    @pytest.mark.sphinx("html", testroot="basic")
    def test_directive_with_title_frontmatter(self, app: Sphinx) -> None:
        """title option injects title into mermaid frontmatter."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        title_nodes = [n for n in nodes if "My Diagram Title" in n["code"]]
        assert len(title_nodes) >= 1
        assert "---" in title_nodes[0]["code"]


class TestInvalidConfig:
    """Tests for invalid :config: option handling."""

    @pytest.mark.sphinx("html", testroot="invalid-config")
    def test_invalid_json_config_warns(self, app: Sphinx) -> None:
        """Invalid JSON in :config: option emits a Sphinx warning."""
        app.build()
        warnings: str = app._warning.getvalue()  # type: ignore[attr-defined]
        assert "Invalid JSON" in warnings

    @pytest.mark.sphinx("html", testroot="invalid-config")
    def test_invalid_json_config_builds_without_frontmatter(self, app: Sphinx, index: str) -> None:
        """Build succeeds without frontmatter when :config: has invalid JSON."""
        assert "data-oceanid-code=" in index
        # No frontmatter markers should appear in the code
        assert "---" not in index.split("data-oceanid-code=")[1].split('"')[1]


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


class TestAutoclasstreeDirectiveErrors:
    """Tests for autoclasstree error handling."""

    @pytest.mark.sphinx("html", testroot="autoclasstree-invalid")
    def test_autoclasstree_invalid_class_raises(self, app: Sphinx) -> None:
        """autoclasstree with invalid class name raises ExtensionError."""
        with pytest.raises(ExtensionError):
            app.build()


class TestAutoclasstreeDirective:
    """Tests for autoclasstree directive (US9, T054)."""

    @pytest.mark.sphinx("html", testroot="autoclasstree")
    def test_autoclasstree_creates_node(self, app: Sphinx) -> None:
        """autoclasstree directive creates mermaid_node in doctree."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        assert len(nodes) >= 1

    @pytest.mark.sphinx("html", testroot="autoclasstree")
    def test_autoclasstree_generates_classdiagram(self, app: Sphinx) -> None:
        """autoclasstree directive generates classDiagram code."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        assert len(nodes) >= 1
        assert nodes[0]["code"].startswith("classDiagram\n")

    @pytest.mark.sphinx("html", testroot="autoclasstree")
    def test_autoclasstree_diagram_type_is_classdiagram(self, app: Sphinx) -> None:
        """autoclasstree directive sets diagram_type to classDiagram."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        assert nodes[0]["diagram_type"] == "classDiagram"

    @pytest.mark.sphinx("html", testroot="autoclasstree")
    def test_autoclasstree_is_supported(self, app: Sphinx) -> None:
        """autoclasstree generates a supported diagram type."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        assert nodes[0]["is_supported"] is True


class TestExternalFile:
    """Tests for external .mmd file support (US7, T043)."""

    @pytest.mark.sphinx("html", testroot="external-file")
    def test_directive_external_file(self, app: Sphinx) -> None:
        """External file reference loads mermaid code correctly."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        assert len(nodes) == 1
        assert "Alice" in nodes[0]["code"]
        assert nodes[0]["diagram_type"] == "sequenceDiagram"

    @pytest.mark.sphinx("html", testroot="external-file-not-found")
    def test_directive_external_file_not_found(self, app: Sphinx) -> None:
        """Non-existent external file raises ExtensionError."""
        with pytest.raises(ExtensionError, match="not found"):
            app.build()

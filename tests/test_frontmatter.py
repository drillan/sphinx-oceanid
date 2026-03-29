"""Tests for Mermaid YAML frontmatter parsing and rendering (Issue #57)."""

from __future__ import annotations

import html
from typing import TYPE_CHECKING

import pytest

from sphinx_oceanid.frontmatter import parse_frontmatter
from sphinx_oceanid.nodes import mermaid_node

if TYPE_CHECKING:
    from sphinx.application import Sphinx


# ---------------------------------------------------------------------------
# Layer 1: Unit tests — parse_frontmatter (no Sphinx)
# ---------------------------------------------------------------------------


class TestParseFrontmatter:
    """Tests for parse_frontmatter pure function."""

    def test_extract_title(self) -> None:
        """Title is extracted from YAML frontmatter."""
        code = "---\ntitle: Auth Flow\n---\nflowchart TD\n  A --> B"
        result = parse_frontmatter(code)
        assert result.title == "Auth Flow"

    def test_extract_config(self) -> None:
        """Config dict is extracted from YAML frontmatter."""
        code = "---\nconfig:\n  theme: dark\n  look: handDrawn\n---\nflowchart TD\n  A --> B"
        result = parse_frontmatter(code)
        assert result.config == {"theme": "dark", "look": "handDrawn"}

    def test_extract_title_and_config(self) -> None:
        """Both title and config are extracted from frontmatter."""
        code = "---\ntitle: My Diagram\nconfig:\n  theme: dark\n---\nflowchart TD\n  A --> B"
        result = parse_frontmatter(code)
        assert result.title == "My Diagram"
        assert result.config == {"theme": "dark"}

    def test_strip_frontmatter_from_code(self) -> None:
        """Frontmatter is stripped from returned code."""
        code = "---\ntitle: My Title\n---\nflowchart TD\n  A --> B"
        result = parse_frontmatter(code)
        assert result.code == "flowchart TD\n  A --> B"
        assert "---" not in result.code

    def test_no_frontmatter(self) -> None:
        """Code without frontmatter returns unchanged."""
        code = "flowchart TD\n  A --> B"
        result = parse_frontmatter(code)
        assert result.code == code
        assert result.title == ""
        assert result.config == {}

    def test_empty_frontmatter(self) -> None:
        """Empty frontmatter block is handled."""
        code = "---\n---\nflowchart TD\n  A --> B"
        result = parse_frontmatter(code)
        assert result.code == "flowchart TD\n  A --> B"
        assert result.title == ""
        assert result.config == {}

    def test_frontmatter_with_extra_keys_ignored(self) -> None:
        """Unknown frontmatter keys are silently ignored."""
        code = "---\ntitle: Hello\nunknownKey: value\n---\nflowchart TD\n  A --> B"
        result = parse_frontmatter(code)
        assert result.title == "Hello"
        assert result.config == {}

    def test_non_dict_config_raises(self) -> None:
        """Non-dict config value raises ValueError."""
        code = "---\nconfig: not-a-dict\n---\nflowchart TD\n  A --> B"
        with pytest.raises(ValueError, match="config"):
            parse_frontmatter(code)

    def test_non_string_title_raises(self) -> None:
        """Non-string title value raises ValueError."""
        code = "---\ntitle:\n  nested: value\n---\nflowchart TD\n  A --> B"
        with pytest.raises(ValueError, match="title"):
            parse_frontmatter(code)


# ---------------------------------------------------------------------------
# Layer 2: Sphinx integration — directive + frontmatter
# ---------------------------------------------------------------------------


class TestFrontmatterDirective:
    """Tests for RST inline content with YAML frontmatter."""

    @pytest.mark.sphinx("html", testroot="frontmatter")
    def test_frontmatter_title_stored_on_node(self, app: Sphinx) -> None:
        """Frontmatter title is stored as mermaid_title on node."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        assert len(nodes) >= 1
        assert nodes[0]["mermaid_title"] == "Auth Flow"

    @pytest.mark.sphinx("html", testroot="frontmatter")
    def test_frontmatter_config_stored_on_node(self, app: Sphinx) -> None:
        """Frontmatter config is stored as mermaid_config on node."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        assert len(nodes) >= 1
        assert nodes[0]["mermaid_config"] == {"theme": "dark", "look": "handDrawn"}

    @pytest.mark.sphinx("html", testroot="frontmatter")
    def test_frontmatter_stripped_from_code(self, app: Sphinx) -> None:
        """Frontmatter is stripped from node code."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        assert "---" not in nodes[0]["code"]
        assert nodes[0]["code"].startswith("flowchart")


class TestExternalFileFrontmatter:
    """Tests for external .mmd file with YAML frontmatter."""

    @pytest.mark.sphinx("html", testroot="external-frontmatter")
    def test_external_frontmatter_title(self, app: Sphinx) -> None:
        """Frontmatter title from external file is stored on node."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        assert len(nodes) >= 1
        assert nodes[0]["mermaid_title"] == "User Authentication Flow"

    @pytest.mark.sphinx("html", testroot="external-frontmatter")
    def test_external_frontmatter_config(self, app: Sphinx) -> None:
        """Frontmatter config from external file is stored on node."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        assert nodes[0]["mermaid_config"] == {"theme": "dark", "look": "handDrawn"}

    @pytest.mark.sphinx("html", testroot="external-frontmatter")
    def test_external_frontmatter_stripped_from_code(self, app: Sphinx) -> None:
        """Frontmatter is stripped from code in external file."""
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        assert "---" not in nodes[0]["code"]
        assert "flowchart" in nodes[0]["code"]


class TestDirectiveOptionOverridesFrontmatter:
    """Directive options take precedence over frontmatter values."""

    @pytest.mark.sphinx("html", testroot="basic")
    def test_option_title_not_overridden_by_frontmatter(self, app: Sphinx) -> None:
        """When :title: option is set, frontmatter title does not override it.

        test-basic has :title: My Diagram Title on a diagram without frontmatter.
        """
        app.build()
        doctree = app.env.get_doctree("index")
        nodes = list(doctree.findall(mermaid_node))
        title_nodes = [n for n in nodes if n.get("mermaid_title")]
        assert title_nodes[0]["mermaid_title"] == "My Diagram Title"


# ---------------------------------------------------------------------------
# Layer 3: HTML output — data attributes in rendered HTML
# ---------------------------------------------------------------------------


class TestFrontmatterHtmlOutput:
    """Tests for frontmatter values in HTML output."""

    @pytest.mark.sphinx("html", testroot="frontmatter")
    def test_html_contains_data_oceanid_title(self, app: Sphinx, index: str) -> None:
        """HTML output includes data-oceanid-title from frontmatter."""
        assert f'data-oceanid-title="{html.escape("Auth Flow", quote=True)}"' in index

    @pytest.mark.sphinx("html", testroot="frontmatter")
    def test_html_contains_data_oceanid_config(self, app: Sphinx, index: str) -> None:
        """HTML output includes data-oceanid-config from frontmatter."""
        assert "data-oceanid-config=" in index

    @pytest.mark.sphinx("html", testroot="external-frontmatter")
    def test_external_html_contains_data_oceanid_title(self, app: Sphinx, index: str) -> None:
        """External file frontmatter title appears in HTML."""
        assert "data-oceanid-title=" in index
        assert "User Authentication Flow" in index

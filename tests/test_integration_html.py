"""Full HTML build integration tests (Layer 3)."""

from __future__ import annotations

import html
import json
import re
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.application import Sphinx


class TestHtmlIntegration:
    """Full HTML build integration tests for US1."""

    @pytest.mark.sphinx("html", testroot="basic")
    def test_full_html_build_succeeds(self, app: Sphinx, build_all: None) -> None:
        """HTML build completes and mermaid directives are processed."""
        assert (app.outdir / "index.html").exists()
        content = (app.outdir / "index.html").read_text()
        # After implementation, mermaid directives should produce oceanid content
        # (without setup, directives are silently dropped by Sphinx 9.x)
        assert "oceanid-diagram" in content

    @pytest.mark.sphinx("html", testroot="basic")
    def test_html_contains_oceanid_diagram(self, app: Sphinx, index: str) -> None:
        """Output HTML contains oceanid-diagram elements."""
        assert "oceanid-diagram" in index

    @pytest.mark.sphinx("html", testroot="basic")
    def test_html_contains_renderer_js(self, app: Sphinx, index: str) -> None:
        """Output HTML references oceanid-renderer.js."""
        assert "oceanid-renderer.js" in index

    @pytest.mark.sphinx("html", testroot="basic")
    def test_html_contains_css(self, app: Sphinx, index: str) -> None:
        """Output HTML references oceanid.css."""
        assert "oceanid.css" in index


def _extract_oceanid_divs(html_content: str) -> list[str]:
    """Extract all oceanid-diagram div opening tags from HTML content."""
    return re.findall(r'<div [^>]*class="[^"]*oceanid-diagram[^"]*"[^>]*>', html_content)


class TestUnsupportedDiagramIntegration:
    """Integration tests for unsupported diagram display (US4)."""

    @pytest.mark.sphinx("html", testroot="unsupported-diagram")
    def test_unsupported_diagram_display(self, app: Sphinx, index: str) -> None:
        """Unsupported diagram produces styled error message in full HTML build."""
        assert "oceanid-unsupported" in index
        assert "gantt" in index
        # Should NOT have the normal diagram container
        assert "oceanid-diagram" not in index

    @pytest.mark.sphinx("html", testroot="unsupported-diagram")
    def test_unsupported_diagram_shows_source_code(self, app: Sphinx, index: str) -> None:
        """Unsupported diagram shows the original Mermaid source code."""
        assert "oceanid-unsupported-code" in index
        # The gantt source code should be visible
        assert "A Gantt Chart" in index


class TestMarkdownIntegration:
    """Integration tests for MyST Markdown input (US2).

    Verifies that MyST fenced mermaid blocks produce functionally
    equivalent HTML to RST directives via myst_fence_as_directive.
    """

    @pytest.mark.sphinx("html", testroot="markdown")
    def test_markdown_build_succeeds(self, app: Sphinx, build_all: None) -> None:
        """MyST Markdown build completes with mermaid fenced blocks."""
        assert (app.outdir / "index.html").exists()

    @pytest.mark.sphinx("html", testroot="markdown")
    def test_markdown_contains_oceanid_diagram(self, app: Sphinx, index: str) -> None:
        """MyST fenced mermaid blocks produce oceanid-diagram elements."""
        assert "oceanid-diagram" in index

    @pytest.mark.sphinx("html", testroot="markdown")
    def test_markdown_diagram_has_align(self, app: Sphinx, index: str) -> None:
        """MyST fenced mermaid block with align option produces align class."""
        assert "align-center" in index

    @pytest.mark.sphinx("html", testroot="markdown")
    def test_markdown_diagram_has_name(self, app: Sphinx, index: str) -> None:
        """MyST fenced mermaid block with name option produces id attribute."""
        assert 'id="test-diagram"' in index

    @pytest.mark.sphinx("html", testroot="markdown")
    def test_markdown_diagram_has_data_code(self, app: Sphinx, index: str) -> None:
        """MyST fenced mermaid block content is in data-oceanid-code attribute."""
        escaped_code = html.escape("sequenceDiagram\n  Alice->>Bob: Hello", quote=True)
        assert f'data-oceanid-code="{escaped_code}"' in index

    @pytest.mark.sphinx("html", testroot="markdown")
    def test_markdown_contains_renderer_js(self, app: Sphinx, index: str) -> None:
        """MyST Markdown output references oceanid-renderer.js."""
        assert "oceanid-renderer.js" in index

    @pytest.mark.sphinx("html", testroot="markdown")
    def test_markdown_contains_css(self, app: Sphinx, index: str) -> None:
        """MyST Markdown output references oceanid.css."""
        assert "oceanid.css" in index

    @pytest.mark.sphinx("html", testroot="markdown")
    def test_markdown_equivalent_to_rst(self, app: Sphinx, index: str) -> None:
        """MyST output is functionally equivalent to RST output.

        Checks that the same structural elements are present:
        - oceanid-diagram class
        - align-center class
        - id from name option
        - data-oceanid-code with diagram content
        - noscript accessibility element
        """
        divs = _extract_oceanid_divs(index)
        assert len(divs) >= 1, "Expected at least one oceanid-diagram div"

        first_div = divs[0]
        assert "oceanid-diagram" in first_div
        assert "align-center" in first_div
        assert 'id="test-diagram"' in first_div
        assert "data-oceanid-code=" in first_div

        assert "<noscript>" in index


class TestAutoclasstreeIntegration:
    """Integration tests for autoclasstree directive (US9)."""

    @pytest.mark.sphinx("html", testroot="autoclasstree")
    def test_autoclasstree_build_succeeds(self, app: Sphinx, build_all: None) -> None:
        """HTML build with autoclasstree directive completes successfully."""
        assert (app.outdir / "index.html").exists()

    @pytest.mark.sphinx("html", testroot="autoclasstree")
    def test_autoclasstree_html_contains_diagram(self, app: Sphinx, index: str) -> None:
        """autoclasstree produces oceanid-diagram in HTML output."""
        assert "oceanid-diagram" in index

    @pytest.mark.sphinx("html", testroot="autoclasstree")
    def test_autoclasstree_html_contains_inheritance(self, app: Sphinx, index: str) -> None:
        """autoclasstree HTML contains class inheritance relationships."""
        # PurePosixPath inherits from PurePath
        assert "PurePath" in index


def _extract_config_json(html_content: str) -> dict[str, object]:
    """Extract the oceanid-config JSON from HTML content."""
    match = re.search(
        r'<script[^>]*id="oceanid-config"[^>]*>(.*?)</script>',
        html_content,
        re.DOTALL,
    )
    assert match, "oceanid-config script element not found"
    result: dict[str, object] = json.loads(match.group(1))
    return result


class TestFullscreenIntegration:
    """Integration tests for fullscreen modal (US8, FR-018)."""

    @pytest.mark.sphinx("html", testroot="fullscreen")
    def test_fullscreen_enabled_build_succeeds(self, app: Sphinx, build_all: None) -> None:
        """HTML build succeeds with fullscreen enabled."""
        assert (app.outdir / "index.html").exists()

    @pytest.mark.sphinx("html", testroot="fullscreen")
    def test_fullscreen_enabled_config_json(self, app: Sphinx, index: str) -> None:
        """Config JSON contains fullscreen: true when enabled."""
        config = _extract_config_json(index)
        assert config["fullscreen"] is True

    @pytest.mark.sphinx("html", testroot="fullscreen")
    def test_fullscreen_enabled_has_button_config(self, app: Sphinx, index: str) -> None:
        """Config JSON contains fullscreen button settings."""
        config = _extract_config_json(index)
        assert config["fullscreenButton"] == "\u26f6"
        assert config["fullscreenButtonOpacity"] == 50

    @pytest.mark.sphinx(
        "html",
        testroot="fullscreen",
        confoverrides={"oceanid_fullscreen_button": "F", "oceanid_fullscreen_button_opacity": 80},
    )
    def test_fullscreen_custom_button_config(self, app: Sphinx, index: str) -> None:
        """Config JSON reflects custom fullscreen button settings."""
        config = _extract_config_json(index)
        assert config["fullscreenButton"] == "F"
        assert config["fullscreenButtonOpacity"] == 80

    @pytest.mark.sphinx("html", testroot="basic", confoverrides={"oceanid_fullscreen": False})
    def test_fullscreen_disabled_config_json(self, app: Sphinx, index: str) -> None:
        """Config JSON contains fullscreen: false when disabled."""
        config = _extract_config_json(index)
        assert config["fullscreen"] is False

    @pytest.mark.sphinx("html", testroot="fullscreen")
    def test_fullscreen_js_referenced(self, app: Sphinx, index: str) -> None:
        """Fullscreen JS module file exists in built output."""
        assert (app.outdir / "_static" / "oceanid-fullscreen.js").exists()

    @pytest.mark.sphinx("html", testroot="fullscreen")
    def test_fullscreen_diagram_present(self, app: Sphinx, index: str) -> None:
        """Fullscreen-enabled page still contains oceanid-diagram elements."""
        assert "oceanid-diagram" in index


class TestZoomIntegration:
    """Integration tests for zoom feature (US8, FR-017)."""

    @pytest.mark.sphinx("html", testroot="zoom")
    def test_zoom_enabled_build_succeeds(self, app: Sphinx, build_all: None) -> None:
        """HTML build succeeds with zoom enabled."""
        assert (app.outdir / "index.html").exists()

    @pytest.mark.sphinx("html", testroot="zoom")
    def test_zoom_enabled_config_json(self, app: Sphinx, index: str) -> None:
        """Config JSON contains zoom: true when enabled globally."""
        config = _extract_config_json(index)
        assert config["zoom"] is True

    @pytest.mark.sphinx("html", testroot="basic", confoverrides={"oceanid_zoom": False})
    def test_zoom_disabled_config_json(self, app: Sphinx, index: str) -> None:
        """Config JSON contains zoom: false when disabled."""
        config = _extract_config_json(index)
        assert config["zoom"] is False

    @pytest.mark.sphinx("html", testroot="zoom")
    def test_zoom_js_referenced(self, app: Sphinx, index: str) -> None:
        """Zoom JS module file exists in built output."""
        assert (app.outdir / "_static" / "oceanid-zoom.js").exists()

    @pytest.mark.sphinx("html", testroot="zoom")
    def test_zoom_diagram_has_data_attribute(self, app: Sphinx, index: str) -> None:
        """With global zoom, diagrams get data-oceanid-zoom attribute."""
        assert "data-oceanid-zoom" in index

    @pytest.mark.sphinx("html", testroot="basic")
    def test_zoom_per_directive_selectors(self, app: Sphinx, index: str) -> None:
        """Per-directive :zoom: option populates zoomSelectors in config JSON."""
        config = _extract_config_json(index)
        zoom_selectors = config["zoomSelectors"]
        assert isinstance(zoom_selectors, list)
        assert len(zoom_selectors) >= 1

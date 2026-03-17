"""Full HTML build integration tests (Layer 3)."""

from __future__ import annotations

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

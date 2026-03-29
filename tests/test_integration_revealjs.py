"""sphinx-revealjs integration tests (Layer 3, US5).

Tests that sphinx-oceanid works correctly with the revealjs builder,
including config JSON flags and Reveal.js slidechanged event handling.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.application import Sphinx

pytest.importorskip("sphinx_revealjs")


class TestRevealjsIntegration:
    """Integration tests for sphinx-revealjs builder (US5)."""

    @pytest.mark.sphinx("revealjs", testroot="revealjs")
    def test_revealjs_build_succeeds(self, app: Sphinx, build_all: None) -> None:
        """Revealjs builder completes build without errors."""
        assert (app.outdir / "index.html").exists()

    @pytest.mark.sphinx("revealjs", testroot="revealjs")
    def test_revealjs_contains_oceanid_diagram(self, app: Sphinx, index: str) -> None:
        """Revealjs output contains oceanid-diagram elements."""
        assert "oceanid-diagram" in index

    @pytest.mark.sphinx("revealjs", testroot="revealjs")
    def test_revealjs_config_json_has_revealjs_flag(self, app: Sphinx, index: str) -> None:
        """Config JSON contains revealjs: true flag."""
        assert '"revealjs": true' in index

    @pytest.mark.sphinx("revealjs", testroot="revealjs")
    def test_revealjs_contains_multiple_diagrams(self, app: Sphinx, index: str) -> None:
        """Revealjs output contains diagrams from both slides."""
        assert "flowchart LR" in index
        assert "sequenceDiagram" in index

    @pytest.mark.sphinx("revealjs", testroot="revealjs")
    def test_revealjs_contains_renderer_js(self, app: Sphinx, index: str) -> None:
        """Revealjs output references oceanid-renderer.js."""
        assert "oceanid-renderer.js" in index

    @pytest.mark.sphinx("revealjs", testroot="revealjs")
    def test_revealjs_contains_css(self, app: Sphinx, index: str) -> None:
        """Revealjs output references oceanid.css."""
        assert "oceanid.css" in index


class TestRevealjsSlidechangedListener:
    """Tests for Reveal.js slidechanged event listener in renderer.js (T036)."""

    def test_renderer_js_contains_slidechanged_listener(self) -> None:
        """oceanid-renderer.js includes slidechanged event listener for Reveal.js."""
        from importlib.resources import files

        renderer_js = files("sphinx_oceanid") / "_static" / "oceanid-renderer.js"
        content = renderer_js.read_text(encoding="utf-8")
        assert "slidechanged" in content

    def test_renderer_js_checks_reveal_global(self) -> None:
        """oceanid-renderer.js uses typeof Reveal guard before attaching listener."""
        from importlib.resources import files

        renderer_js = files("sphinx_oceanid") / "_static" / "oceanid-renderer.js"
        content = renderer_js.read_text(encoding="utf-8")
        assert 'typeof Reveal !== "undefined"' in content

    @pytest.mark.sphinx("revealjs", testroot="revealjs")
    def test_revealjs_config_json_is_valid(self, app: Sphinx, index: str) -> None:
        """Config JSON embedded in revealjs output is valid JSON with expected keys."""
        start = index.find('id="oceanid-config">')
        assert start != -1, "oceanid-config element not found"
        json_start = index.find(">", start) + 1
        json_end = index.find("</script>", json_start)
        config = json.loads(index[json_start:json_end])
        assert config["revealjs"] is True
        assert "beautifulMermaidUrl" in config

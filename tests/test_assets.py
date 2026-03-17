"""Tests for per-page asset injection (Layer 2: Sphinx integration)."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from sphinx_oceanid.config import BEAUTIFUL_MERMAID_CDN_TEMPLATE, BEAUTIFUL_MERMAID_VERSION

if TYPE_CHECKING:
    from sphinx.application import Sphinx


class TestAssetInjection:
    """Tests for install_assets function."""

    @pytest.mark.sphinx("html", testroot="basic")
    def test_js_injected_on_mermaid_page(self, app: Sphinx, index: str) -> None:
        """JS is injected on pages with mermaid nodes."""
        assert "oceanid-renderer.js" in index

    @pytest.mark.sphinx("html", testroot="basic")
    def test_js_not_injected_on_empty_page(self, app: Sphinx, build_all: None) -> None:
        """JS is NOT injected on pages without mermaid nodes."""
        empty_html = (app.outdir / "empty.html").read_text()
        assert "oceanid-renderer.js" not in empty_html

    @pytest.mark.sphinx("html", testroot="basic")
    def test_config_json_content(self, app: Sphinx, index: str) -> None:
        """Config JSON script element contains correct values."""
        assert 'id="oceanid-config"' in index
        # Extract and parse the JSON content
        marker = 'id="oceanid-config">'
        start = index.index(marker) + len(marker)
        end = index.index("</script>", start)
        config = json.loads(index[start:end])
        assert "beautifulMermaidUrl" in config
        assert config["theme"] == "auto"

    @pytest.mark.sphinx("html", testroot="basic")
    def test_beautiful_mermaid_cdn_url(self, app: Sphinx, index: str) -> None:
        """beautiful-mermaid CDN URL is present in HTML."""
        expected_url = BEAUTIFUL_MERMAID_CDN_TEMPLATE.format(version=BEAUTIFUL_MERMAID_VERSION)
        assert expected_url in index

    @pytest.mark.sphinx("html", testroot="basic", confoverrides={"oceanid_local_js": "/local/path.js"})
    def test_local_js_path(self, app: Sphinx, index: str) -> None:
        """Local path is used instead of CDN URL when configured."""
        cdn_url = BEAUTIFUL_MERMAID_CDN_TEMPLATE.format(version=BEAUTIFUL_MERMAID_VERSION)
        assert cdn_url not in index
        assert "/local/path.js" in index

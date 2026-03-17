"""Tests for documentation build (docs/ directory)."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
BUILD_DIR = PROJECT_ROOT / "docs" / "_build" / "html"

SPHINX_BUILD_TIMEOUT_SECONDS = 120


@pytest.fixture(scope="module")
def docs_build() -> None:
    """Build the documentation and assert success."""
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    result = subprocess.run(
        ["uv", "--directory", str(PROJECT_ROOT), "run", "sphinx-build", "-W", str(DOCS_DIR), str(BUILD_DIR)],
        capture_output=True,
        text=True,
        timeout=SPHINX_BUILD_TIMEOUT_SECONDS,
    )
    assert result.returncode == 0, f"Docs build failed:\n{result.stderr}"


class TestDocsBuild:
    """Verify documentation builds correctly."""

    def test_index_html_exists(self, docs_build: None) -> None:
        """Index page is generated."""
        assert (BUILD_DIR / "index.html").exists()

    def test_supported_diagrams_page_exists(self, docs_build: None) -> None:
        """Supported diagrams page is generated."""
        assert (BUILD_DIR / "supported-diagrams.html").exists()

    def test_supported_diagrams_in_toctree(self, docs_build: None) -> None:
        """Supported diagrams page is linked from the index toctree."""
        index_html = (BUILD_DIR / "index.html").read_text()
        assert "supported-diagrams" in index_html

    def test_cross_reference_from_configuration(self, docs_build: None) -> None:
        """Configuration page links to supported-diagram-types target."""
        config_html = (BUILD_DIR / "configuration.html").read_text()
        assert "supported-diagram" in config_html

    def test_revealjs_page_exists(self, docs_build: None) -> None:
        """sphinx-revealjs integration guide page is generated."""
        assert (BUILD_DIR / "revealjs.html").exists()

    def test_revealjs_in_toctree(self, docs_build: None) -> None:
        """sphinx-revealjs page is linked from the index toctree."""
        index_html = (BUILD_DIR / "index.html").read_text()
        assert "revealjs" in index_html

    def test_revealjs_page_contains_expected_sections(self, docs_build: None) -> None:
        """sphinx-revealjs page contains key sections from the guide."""
        revealjs_html = (BUILD_DIR / "revealjs.html").read_text()
        assert "Prerequisites" in revealjs_html
        assert "slidechanged" in revealjs_html
        assert "IntersectionObserver" in revealjs_html
        assert "sphinx_revealjs" in revealjs_html

    def test_troubleshooting_page_exists(self, docs_build: None) -> None:
        """Troubleshooting page is generated."""
        assert (BUILD_DIR / "troubleshooting.html").exists()

    def test_troubleshooting_in_toctree(self, docs_build: None) -> None:
        """Troubleshooting page is linked from the index toctree."""
        index_html = (BUILD_DIR / "index.html").read_text()
        assert "troubleshooting" in index_html

    def test_troubleshooting_page_contains_common_issues(self, docs_build: None) -> None:
        """Troubleshooting page contains all expected common issue sections."""
        html = (BUILD_DIR / "troubleshooting.html").read_text()
        assert "CDN unreachable" in html
        assert "Rendering errors" in html
        assert "Theme mismatch" in html
        assert "Unsupported diagram types" in html
        assert "sphinx-revealjs" in html
        assert "Local JS bundle" in html
        assert "Migration from sphinxcontrib-mermaid" in html

    def test_troubleshooting_page_contains_faq(self, docs_build: None) -> None:
        """Troubleshooting page contains the FAQ section with expected questions."""
        html = (BUILD_DIR / "troubleshooting.html").read_text()
        assert "FAQ" in html
        assert "Which diagram types are supported" in html
        assert "standard Mermaid.js" in html
        assert "PDF" in html
        assert "theme auto-detection" in html

    def test_troubleshooting_cross_references(self, docs_build: None) -> None:
        """Troubleshooting page contains cross-references to other doc pages."""
        html = (BUILD_DIR / "troubleshooting.html").read_text()
        assert "configuration" in html
        assert "supported-diagram" in html
        assert "revealjs" in html

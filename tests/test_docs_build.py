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

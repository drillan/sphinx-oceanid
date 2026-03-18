"""Shared test configuration for sphinx-oceanid."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.application import Sphinx

pytest_plugins = "sphinx.testing.fixtures"

collect_ignore = ["roots"]

_PROJECT_ROOT = Path(__file__).parent.parent
_DOCS_DIR = _PROJECT_ROOT / "docs"
_DOCS_BUILD_DIR = _PROJECT_ROOT / "docs" / "_build" / "html"

_SPHINX_BUILD_TIMEOUT_SECONDS = 120


@pytest.fixture(scope="session")
def rootdir() -> Path:
    return Path(__file__).parent / "roots"


@pytest.fixture
def build_all(app: Sphinx) -> None:
    """Build the Sphinx project."""
    app.build()


@pytest.fixture
def index(app: Sphinx, build_all: None) -> str:
    """Read the index.html output after build."""
    return (app.outdir / "index.html").read_text()


@pytest.fixture(scope="session")
def docs_build() -> Path:
    """Build docs/ and return the HTML output directory.

    Shared across all test modules that need the docs build.
    """
    if _DOCS_BUILD_DIR.exists():
        shutil.rmtree(_DOCS_BUILD_DIR)
    result = subprocess.run(
        [
            "uv",
            "--directory",
            str(_PROJECT_ROOT),
            "run",
            "sphinx-build",
            "-W",
            str(_DOCS_DIR),
            str(_DOCS_BUILD_DIR),
        ],
        capture_output=True,
        text=True,
        timeout=_SPHINX_BUILD_TIMEOUT_SECONDS,
    )
    assert result.returncode == 0, f"Docs build failed:\n{result.stderr}"
    return _DOCS_BUILD_DIR

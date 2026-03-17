"""Shared test configuration for sphinx-oceanid."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.application import Sphinx

pytest_plugins = "sphinx.testing.fixtures"

collect_ignore = ["roots"]


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

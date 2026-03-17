"""Tests for project metadata (pyproject.toml) compliance with spec-python.md."""

import tomllib
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def project() -> dict[str, object]:
    """Load and return the [project] section from pyproject.toml."""
    path = Path(__file__).parent.parent / "pyproject.toml"
    with path.open("rb") as f:
        data = tomllib.load(f)
    proj = data["project"]
    assert isinstance(proj, dict)
    return proj


class TestProjectDependencies:
    """Verify runtime dependencies match spec-python.md requirements."""

    @pytest.mark.parametrize("dep", ["sphinx>=7.4", "pyyaml>=6.0"])
    def test_dependency_present(self, project: dict[str, object], dep: str) -> None:
        """Each required dependency with version constraint must be in dependencies."""
        deps = project["dependencies"]
        assert isinstance(deps, list)
        assert dep in deps, f"{dep} missing from [project].dependencies"


class TestProjectMetadata:
    """Verify project metadata matches spec-python.md."""

    def test_name(self, project: dict[str, object]) -> None:
        assert project["name"] == "sphinx-oceanid"

    def test_version(self, project: dict[str, object]) -> None:
        assert project["version"] == "0.1.0"

    def test_requires_python(self, project: dict[str, object]) -> None:
        assert project["requires-python"] == ">=3.13"

    def test_license(self, project: dict[str, object]) -> None:
        assert project["license"] == "BSD-3-Clause"

    def test_classifiers(self, project: dict[str, object]) -> None:
        classifiers = project["classifiers"]
        assert isinstance(classifiers, list)
        expected = [
            "Development Status :: 3 - Alpha",
            "Framework :: Sphinx :: Extension",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3.13",
            "Programming Language :: Python :: 3.14",
            "Topic :: Documentation",
        ]
        assert set(classifiers) == set(expected)

    def test_keywords(self, project: dict[str, object]) -> None:
        keywords = project["keywords"]
        assert isinstance(keywords, list)
        expected = {"sphinx", "mermaid", "diagrams", "documentation", "beautiful-mermaid"}
        assert set(keywords) == expected

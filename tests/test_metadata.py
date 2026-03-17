"""Tests for project metadata (pyproject.toml) compliance with spec-python.md."""

import tomllib
from pathlib import Path


def _load_pyproject() -> dict[str, object]:
    """Load pyproject.toml as a dictionary."""
    path = Path(__file__).parent.parent / "pyproject.toml"
    with path.open("rb") as f:
        return tomllib.load(f)


def _get_project() -> dict[str, object]:
    """Load and return the [project] section from pyproject.toml."""
    data = _load_pyproject()
    project = data["project"]
    assert isinstance(project, dict)
    return project


class TestProjectDependencies:
    """Verify runtime dependencies match spec-python.md requirements."""

    def test_sphinx_dependency(self) -> None:
        """sphinx>=7.4 must be in dependencies."""
        project = _get_project()
        deps = project["dependencies"]
        assert isinstance(deps, list)
        assert any("sphinx" in d for d in deps)

    def test_pyyaml_dependency(self) -> None:
        """pyyaml must be in dependencies (used by directives.py for YAML frontmatter)."""
        project = _get_project()
        deps = project["dependencies"]
        assert isinstance(deps, list)
        assert any("pyyaml" in str(d).lower() for d in deps), (
            "pyyaml is missing from [project].dependencies - "
            "directives.py imports yaml, so pyyaml must be a runtime dependency"
        )


class TestProjectMetadata:
    """Verify project metadata matches spec-python.md."""

    def test_name(self) -> None:
        project = _get_project()
        assert project["name"] == "sphinx-oceanid"

    def test_version(self) -> None:
        project = _get_project()
        assert project["version"] == "0.1.0"

    def test_requires_python(self) -> None:
        project = _get_project()
        assert project["requires-python"] == ">=3.13"

    def test_license(self) -> None:
        project = _get_project()
        assert project["license"] == "BSD-3-Clause"

    def test_classifiers_include_sphinx_extension(self) -> None:
        project = _get_project()
        classifiers = project["classifiers"]
        assert isinstance(classifiers, list)
        assert "Framework :: Sphinx :: Extension" in classifiers

    def test_keywords(self) -> None:
        project = _get_project()
        keywords = project["keywords"]
        assert isinstance(keywords, list)
        expected = {"sphinx", "mermaid", "diagrams", "documentation", "beautiful-mermaid"}
        assert set(keywords) == expected

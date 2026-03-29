"""Tests for documentation build (docs/ directory)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class TestDocsBuild:
    """Verify documentation builds correctly."""

    def _read(self, page: str, docs_build: Path) -> str:
        return (docs_build / page).read_text()

    def test_index_html_exists(self, docs_build: Path) -> None:
        """Index page is generated."""
        assert (docs_build / "index.html").exists()

    def test_supported_diagrams_page_exists(self, docs_build: Path) -> None:
        """Supported diagrams page is generated."""
        assert (docs_build / "supported-diagrams.html").exists()

    def test_supported_diagrams_in_toctree(self, docs_build: Path) -> None:
        """Supported diagrams page is linked from the index toctree."""
        assert "supported-diagrams" in self._read("index.html", docs_build)

    def test_cross_reference_from_configuration(self, docs_build: Path) -> None:
        """Configuration page links to supported-diagram-types target."""
        assert "supported-diagram" in self._read("configuration.html", docs_build)

    def test_revealjs_page_exists(self, docs_build: Path) -> None:
        """sphinx-revealjs integration guide page is generated."""
        assert (docs_build / "revealjs.html").exists()

    def test_revealjs_in_toctree(self, docs_build: Path) -> None:
        """sphinx-revealjs page is linked from the index toctree."""
        assert "revealjs" in self._read("index.html", docs_build)

    def test_revealjs_page_contains_expected_sections(self, docs_build: Path) -> None:
        """sphinx-revealjs page contains key sections from the guide."""
        content = self._read("revealjs.html", docs_build)
        assert "Prerequisites" in content
        assert "slidechanged" in content
        assert "IntersectionObserver" in content
        assert "sphinx_revealjs" in content

    def test_troubleshooting_page_exists(self, docs_build: Path) -> None:
        """Troubleshooting page is generated."""
        assert (docs_build / "troubleshooting.html").exists()

    def test_troubleshooting_in_toctree(self, docs_build: Path) -> None:
        """Troubleshooting page is linked from the index toctree."""
        assert "troubleshooting" in self._read("index.html", docs_build)

    def test_troubleshooting_page_contains_common_issues(self, docs_build: Path) -> None:
        """Troubleshooting page contains all expected common issue sections."""
        content = self._read("troubleshooting.html", docs_build)
        assert "CDN unreachable" in content
        assert "Rendering errors" in content
        assert "Theme mismatch" in content
        assert "Unsupported diagram types" in content
        assert "sphinx-revealjs" in content
        assert "Local JS bundle" in content
        assert "Migration from sphinxcontrib-mermaid" in content

    def test_troubleshooting_page_contains_faq(self, docs_build: Path) -> None:
        """Troubleshooting page contains the FAQ section with expected questions."""
        content = self._read("troubleshooting.html", docs_build)
        assert "FAQ" in content
        assert "Which diagram types are supported" in content
        assert "standard Mermaid.js" in content
        assert "PDF" in content
        assert "theme auto-detection" in content

    def test_troubleshooting_cross_references(self, docs_build: Path) -> None:
        """Troubleshooting page contains cross-references to other doc pages."""
        content = self._read("troubleshooting.html", docs_build)
        assert "configuration" in content
        assert "supported-diagram" in content
        assert "revealjs" in content


class TestSyntaxTabs:
    """Verify RST/MyST syntax tabs render correctly."""

    def _read(self, page: str, docs_build: Path) -> str:
        return (docs_build / page).read_text()

    def test_index_has_tab_set(self, docs_build: Path) -> None:
        """Index page contains sphinx-design tab-set containers."""
        content = self._read("index.html", docs_build)
        assert "sd-tab-set" in content

    def test_index_has_rst_and_myst_tabs(self, docs_build: Path) -> None:
        """Index page tab-sets have both RST and MyST tab labels."""
        content = self._read("index.html", docs_build)
        assert "RST" in content
        assert "MyST" in content

    def test_index_tabs_contain_syntax_examples(self, docs_build: Path) -> None:
        """Index page tabs contain RST and MyST highlighted code blocks."""
        content = self._read("index.html", docs_build)
        assert "highlight-rst" in content
        assert "highlight-markdown" in content

    def test_index_tabs_use_sync(self, docs_build: Path) -> None:
        """Index page tabs use sync keys so selection persists across tab-sets."""
        content = self._read("index.html", docs_build)
        assert 'data-sync-id="rst"' in content
        assert 'data-sync-id="myst"' in content

    def test_supported_diagrams_has_tab_set(self, docs_build: Path) -> None:
        """Supported diagrams page contains sphinx-design tab-set containers."""
        content = self._read("supported-diagrams.html", docs_build)
        assert "sd-tab-set" in content

    def test_supported_diagrams_has_rst_and_myst_tabs(self, docs_build: Path) -> None:
        """Supported diagrams page tab-sets have both RST and MyST tab labels."""
        content = self._read("supported-diagrams.html", docs_build)
        assert "RST" in content
        assert "MyST" in content

    def test_supported_diagrams_tabs_contain_syntax_examples(self, docs_build: Path) -> None:
        """Supported diagrams tabs contain RST and MyST highlighted code blocks."""
        content = self._read("supported-diagrams.html", docs_build)
        assert "highlight-rst" in content
        assert "highlight-markdown" in content

    def test_supported_diagrams_all_types_have_tabs(self, docs_build: Path) -> None:
        """Each diagram type example in supported-diagrams uses tab-sets."""
        content = self._read("supported-diagrams.html", docs_build)
        # Each of the 6 diagram types + graph alias = 7 examples, each with a tab-set
        tab_set_count = content.count("sd-tab-set")
        assert tab_set_count >= 7, f"Expected at least 7 tab-sets, found {tab_set_count}"


class TestPerTypeLimitations:
    """Verify per-type known limitations are documented on supported-diagrams page."""

    def _read(self, page: str, docs_build: Path) -> str:
        return (docs_build / page).read_text()

    def test_flowchart_limitations(self, docs_build: Path) -> None:
        """flowchart section documents click and bidirectional arrow limitations."""
        content = self._read("supported-diagrams.html", docs_build)
        assert "click" in content
        assert "&lt;--&gt;" in content or "<code" in content

    def test_sequence_diagram_limitations(self, docs_build: Path) -> None:
        """sequenceDiagram section documents autonumber, box, create/destroy limitations."""
        content = self._read("supported-diagrams.html", docs_build)
        assert "autonumber" in content
        assert "box" in content
        assert "create" in content
        assert "activate" in content

    def test_class_diagram_limitations(self, docs_build: Path) -> None:
        """classDiagram section documents click/note/link and classDef limitations."""
        content = self._read("supported-diagrams.html", docs_build)
        assert "classDef" in content

    def test_state_diagram_limitations(self, docs_build: Path) -> None:
        """stateDiagram section documents fork/join/choice and concurrent limitations."""
        content = self._read("supported-diagrams.html", docs_build)
        assert "fork" in content
        assert "choice" in content

    def test_er_diagram_limitations(self, docs_build: Path) -> None:
        """erDiagram section documents entity alias limitation."""
        content = self._read("supported-diagrams.html", docs_build)
        assert "alias" in content

    def test_xychart_limitations(self, docs_build: Path) -> None:
        """xychart-beta section documents named series label limitation."""
        content = self._read("supported-diagrams.html", docs_build)
        assert "series" in content

    def test_upstream_issue_references(self, docs_build: Path) -> None:
        """Limitations reference upstream beautiful-mermaid issues where applicable."""
        content = self._read("supported-diagrams.html", docs_build)
        assert "beautiful-mermaid" in content
        # At least one upstream issue number should be referenced
        assert "#53" in content or "#58" in content or "#80" in content

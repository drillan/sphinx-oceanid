"""Tests for HTML visitor output (Layer 2: Sphinx integration)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.application import Sphinx


class TestHtmlVisitor:
    """Tests for html_visit_mermaid / html_depart_mermaid."""

    @pytest.mark.sphinx("html", testroot="basic")
    def test_supported_diagram_html_output(self, app: Sphinx, index: str) -> None:
        """Supported diagram produces <div class="oceanid-diagram">."""
        assert 'class="oceanid-diagram' in index

    @pytest.mark.sphinx("html", testroot="basic")
    def test_data_oceanid_code_attribute(self, app: Sphinx, index: str) -> None:
        """data-oceanid-code attribute contains the Mermaid code."""
        assert "data-oceanid-code=" in index

    @pytest.mark.sphinx("html", testroot="basic")
    def test_noscript_content(self, app: Sphinx, index: str) -> None:
        """noscript element contains plain-text Mermaid code."""
        assert "<noscript>" in index

    @pytest.mark.sphinx("html", testroot="basic")
    def test_align_class(self, app: Sphinx, index: str) -> None:
        """align option is reflected as CSS class on the diagram div."""
        # The test root has :align: center on the first mermaid directive
        assert "oceanid-diagram" in index
        assert "align-center" in index


class TestDirectiveOptionHtml:
    """Tests for directive option HTML output (T038)."""

    @pytest.mark.sphinx("html", testroot="basic")
    def test_zoom_data_attribute(self, app: Sphinx, index: str) -> None:
        """zoom option produces data-oceanid-zoom attribute in HTML."""
        assert "data-oceanid-zoom" in index

    @pytest.mark.sphinx("html", testroot="basic")
    def test_zoom_id_as_html_id(self, app: Sphinx, index: str) -> None:
        """zoom-enabled diagram without :name: gets id from zoom_id."""
        assert 'id="oceanid-zoom-' in index

    @pytest.mark.sphinx("html", testroot="basic")
    def test_alt_aria_label(self, app: Sphinx, index: str) -> None:
        """alt option produces aria-label attribute in HTML."""
        assert 'aria-label="Sequence diagram of greeting"' in index

    @pytest.mark.sphinx("html", testroot="basic")
    def test_caption_produces_figure(self, app: Sphinx, index: str) -> None:
        """caption option wraps diagram in <figure> with <figcaption>."""
        assert "<figure" in index
        assert "<figcaption" in index
        assert "My caption text" in index

    @pytest.mark.sphinx("html", testroot="basic")
    def test_config_frontmatter_in_code(self, app: Sphinx, index: str) -> None:
        """config option injects frontmatter into data-oceanid-code."""
        # The frontmatter with theme: forest should be in the escaped code attribute
        assert "theme: forest" in index

    @pytest.mark.sphinx("html", testroot="basic")
    def test_title_frontmatter_in_code(self, app: Sphinx, index: str) -> None:
        """title option injects title frontmatter into data-oceanid-code."""
        assert "My Diagram Title" in index


class TestUnsupportedDiagram:
    """Tests for unsupported diagram type handling (US4)."""

    @pytest.mark.sphinx("html", testroot="unsupported-diagram")
    def test_unsupported_diagram_warning(self, app: Sphinx) -> None:
        """Unsupported diagram type emits Sphinx warning with type and location."""
        app.build()
        warnings: str = app._warning.getvalue()  # type: ignore[attr-defined]
        assert "gantt" in warnings
        assert "not supported" in warnings

    @pytest.mark.sphinx("html", testroot="unsupported-diagram")
    def test_unsupported_diagram_html_output(self, app: Sphinx, index: str) -> None:
        """Unsupported diagram produces styled error div per contract."""
        assert 'class="oceanid-unsupported"' in index
        assert "oceanid-unsupported-message" in index
        assert "gantt" in index
        assert "oceanid-unsupported-code" in index

    @pytest.mark.sphinx("html", testroot="unsupported-diagram")
    def test_unsupported_diagram_no_oceanid_diagram_class(self, app: Sphinx, index: str) -> None:
        """Unsupported diagram does NOT produce oceanid-diagram div."""
        assert "oceanid-diagram" not in index

    @pytest.mark.sphinx("html", testroot="unsupported-diagram")
    def test_unsupported_diagram_shows_supported_types(self, app: Sphinx, index: str) -> None:
        """Unsupported diagram message lists supported types."""
        assert "flowchart" in index
        assert "sequenceDiagram" in index
        assert "erDiagram" in index

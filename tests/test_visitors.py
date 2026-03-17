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

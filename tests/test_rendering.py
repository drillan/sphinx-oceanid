"""SVG rendering verification tests.

Validates that Mermaid diagram codes embedded in built HTML can be
successfully rendered to SVG by beautiful-mermaid (via Node.js).

Covers both:
- docs/ pages (supported-diagrams.md, index.md, etc.)
- tests/roots/ test fixtures (test-basic, test-markdown, etc.)

Requires: Node.js with beautiful-mermaid installed (``npm install beautiful-mermaid``).
Skipped automatically when unavailable.
"""

from __future__ import annotations

import html
import json
import re
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.application import Sphinx

RENDER_CHECK_SCRIPT = Path(__file__).parent / "helpers" / "render_check.mjs"
NODE_TIMEOUT_SECONDS = 30


def _node_rendering_available() -> bool:
    """Check if Node.js and beautiful-mermaid are available."""
    try:
        result = subprocess.run(
            ["node", str(RENDER_CHECK_SCRIPT)],
            input="[]",
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


pytestmark = pytest.mark.skipif(
    not _node_rendering_available(),
    reason="Node.js with beautiful-mermaid is not available",
)


def _extract_oceanid_codes(html_content: str) -> list[str]:
    """Extract all data-oceanid-code attribute values from HTML content."""
    raw_values = re.findall(r'data-oceanid-code="([^"]*)"', html_content)
    return [html.unescape(v) for v in raw_values]


def _render_with_node(codes: list[str]) -> list[dict[str, object]]:
    """Render Mermaid codes via Node.js and return results."""
    result = subprocess.run(
        ["node", str(RENDER_CHECK_SCRIPT)],
        input=json.dumps(codes),
        capture_output=True,
        text=True,
        timeout=NODE_TIMEOUT_SECONDS,
    )
    if result.returncode != 0:
        raise RuntimeError(f"render_check.mjs failed:\n{result.stderr}")
    results: list[dict[str, object]] = json.loads(result.stdout)
    return results


def _assert_all_render_successfully(codes: list[str]) -> None:
    """Assert that all Mermaid codes render to valid SVGs."""
    assert len(codes) > 0, "No diagram codes found to render"
    results = _render_with_node(codes)
    failures = [r for r in results if not r["success"]]
    if failures:
        messages = [f"  Code: {f['code']!r}\n  Error: {f['error']}" for f in failures]
        raise AssertionError(f"{len(failures)} diagram(s) failed to render:\n" + "\n\n".join(messages))
    for r in results:
        assert r["hasValidSvg"], f"SVG output is invalid for: {r['code']!r}"


# ---------------------------------------------------------------------------
# docs/ rendering tests
# ---------------------------------------------------------------------------


class TestDocsRendering:
    """Verify that all diagrams in docs/ pages render to valid SVG."""

    def test_supported_diagrams_page_renders(self, docs_build: Path) -> None:
        """All diagrams on supported-diagrams.html render to SVG."""
        content = (docs_build / "supported-diagrams.html").read_text()
        codes = _extract_oceanid_codes(content)
        _assert_all_render_successfully(codes)

    def test_index_page_renders(self, docs_build: Path) -> None:
        """All diagrams on index.html render to SVG."""
        content = (docs_build / "index.html").read_text()
        codes = _extract_oceanid_codes(content)
        _assert_all_render_successfully(codes)


# ---------------------------------------------------------------------------
# tests/roots/ rendering tests
# ---------------------------------------------------------------------------


class TestTestRootRendering:
    """Verify that diagrams in test root fixtures render to valid SVG."""

    @pytest.mark.sphinx("html", testroot="basic")
    def test_basic_diagrams_render(self, app: Sphinx, index: str) -> None:
        """All diagrams in test-basic render to SVG."""
        codes = _extract_oceanid_codes(index)
        _assert_all_render_successfully(codes)

    @pytest.mark.sphinx("html", testroot="basic")
    def test_basic_zoom_page_renders(self, app: Sphinx, build_all: None) -> None:
        """Diagrams on test-basic/zoom.html render to SVG."""
        content = (app.outdir / "zoom.html").read_text()
        codes = _extract_oceanid_codes(content)
        _assert_all_render_successfully(codes)

    @pytest.mark.sphinx("html", testroot="markdown")
    def test_markdown_diagrams_render(self, app: Sphinx, index: str) -> None:
        """MyST Markdown diagrams render to SVG."""
        codes = _extract_oceanid_codes(index)
        _assert_all_render_successfully(codes)

    @pytest.mark.sphinx("html", testroot="external-file")
    def test_external_file_diagrams_render(self, app: Sphinx, index: str) -> None:
        """External .mmd file diagram renders to SVG."""
        codes = _extract_oceanid_codes(index)
        _assert_all_render_successfully(codes)

    @pytest.mark.sphinx("html", testroot="fullscreen")
    def test_fullscreen_diagrams_render(self, app: Sphinx, index: str) -> None:
        """Diagrams with fullscreen enabled render to SVG."""
        codes = _extract_oceanid_codes(index)
        _assert_all_render_successfully(codes)

    @pytest.mark.sphinx("html", testroot="zoom")
    def test_zoom_diagrams_render(self, app: Sphinx, index: str) -> None:
        """Diagrams with zoom enabled render to SVG."""
        codes = _extract_oceanid_codes(index)
        _assert_all_render_successfully(codes)

    @pytest.mark.sphinx("html", testroot="autoclasstree")
    def test_autoclasstree_diagrams_render(self, app: Sphinx, index: str) -> None:
        """Auto-generated class diagram renders to SVG."""
        codes = _extract_oceanid_codes(index)
        _assert_all_render_successfully(codes)


sphinx_revealjs = pytest.importorskip("sphinx_revealjs")


class TestRevealjsRendering:
    """Verify that diagrams in revealjs output render to valid SVG."""

    @pytest.mark.sphinx("revealjs", testroot="revealjs")
    def test_revealjs_diagrams_render(self, app: Sphinx, index: str) -> None:
        """Diagrams in revealjs output render to SVG."""
        codes = _extract_oceanid_codes(index)
        _assert_all_render_successfully(codes)

"""Tests for static JS/CSS files (T019, T020, T021)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.application import Sphinx


class TestStaticFilesCopied:
    """Verify static files are copied to build output."""

    @pytest.mark.sphinx("html", testroot="basic")
    def test_renderer_js_in_output(self, app: Sphinx, build_all: None) -> None:
        """oceanid-renderer.js is copied to _static in build output."""
        renderer_js = app.outdir / "_static" / "oceanid-renderer.js"
        assert renderer_js.exists()

    @pytest.mark.sphinx("html", testroot="basic")
    def test_observer_js_in_output(self, app: Sphinx, build_all: None) -> None:
        """oceanid-observer.js is copied to _static in build output."""
        observer_js = app.outdir / "_static" / "oceanid-observer.js"
        assert observer_js.exists()

    @pytest.mark.sphinx("html", testroot="basic")
    def test_css_in_output(self, app: Sphinx, build_all: None) -> None:
        """oceanid.css is copied to _static in build output."""
        css = app.outdir / "_static" / "oceanid.css"
        assert css.exists()


class TestOceanidCssContent:
    """Verify CSS contains expected selectors (T021)."""

    @pytest.mark.sphinx("html", testroot="basic")
    def test_diagram_base_class(self, app: Sphinx, build_all: None) -> None:
        """CSS defines .oceanid-diagram base styles."""
        css = (app.outdir / "_static" / "oceanid.css").read_text()
        assert ".oceanid-diagram" in css

    @pytest.mark.sphinx("html", testroot="basic")
    def test_svg_container_class(self, app: Sphinx, build_all: None) -> None:
        """CSS defines .oceanid-svg-container styles."""
        css = (app.outdir / "_static" / "oceanid.css").read_text()
        assert ".oceanid-svg-container" in css

    @pytest.mark.sphinx("html", testroot="basic")
    def test_align_classes(self, app: Sphinx, build_all: None) -> None:
        """CSS defines alignment classes."""
        css = (app.outdir / "_static" / "oceanid.css").read_text()
        assert ".align-center" in css
        assert ".align-left" in css
        assert ".align-right" in css

    @pytest.mark.sphinx("html", testroot="basic")
    def test_render_error_classes(self, app: Sphinx, build_all: None) -> None:
        """CSS defines render error styles (FR-023)."""
        css = (app.outdir / "_static" / "oceanid.css").read_text()
        assert ".oceanid-render-error" in css
        assert ".oceanid-render-error-source" in css

    @pytest.mark.sphinx("html", testroot="basic")
    def test_source_display_class(self, app: Sphinx, build_all: None) -> None:
        """CSS defines source display styles (FR-024)."""
        css = (app.outdir / "_static" / "oceanid.css").read_text()
        assert ".oceanid-source-display" in css

    @pytest.mark.sphinx("html", testroot="basic")
    def test_unsupported_classes(self, app: Sphinx, build_all: None) -> None:
        """CSS defines unsupported diagram styles."""
        css = (app.outdir / "_static" / "oceanid.css").read_text()
        assert ".oceanid-unsupported" in css

    @pytest.mark.sphinx("html", testroot="basic")
    def test_noscript_hiding(self, app: Sphinx, build_all: None) -> None:
        """CSS hides noscript when rendered."""
        css = (app.outdir / "_static" / "oceanid.css").read_text()
        assert "data-oceanid-rendered" in css
        assert "noscript" in css


class TestRendererJsContent:
    """Verify renderer.js contains expected structure (T019)."""

    @pytest.mark.sphinx("html", testroot="basic")
    def test_load_config_function(self, app: Sphinx, build_all: None) -> None:
        """renderer.js defines loadConfig function."""
        js = (app.outdir / "_static" / "oceanid-renderer.js").read_text()
        assert "loadConfig" in js

    @pytest.mark.sphinx("html", testroot="basic")
    def test_partition_by_visibility(self, app: Sphinx, build_all: None) -> None:
        """renderer.js defines partitionByVisibility function."""
        js = (app.outdir / "_static" / "oceanid-renderer.js").read_text()
        assert "partitionByVisibility" in js

    @pytest.mark.sphinx("html", testroot="basic")
    def test_imports_observer(self, app: Sphinx, build_all: None) -> None:
        """renderer.js imports from oceanid-observer.js."""
        js = (app.outdir / "_static" / "oceanid-renderer.js").read_text()
        assert "oceanid-observer.js" in js

    @pytest.mark.sphinx("html", testroot="basic")
    def test_oceanid_config_element(self, app: Sphinx, build_all: None) -> None:
        """renderer.js reads from #oceanid-config element."""
        js = (app.outdir / "_static" / "oceanid-renderer.js").read_text()
        assert "oceanid-config" in js

    @pytest.mark.sphinx("html", testroot="basic")
    def test_window_load_listener(self, app: Sphinx, build_all: None) -> None:
        """renderer.js attaches to window load event."""
        js = (app.outdir / "_static" / "oceanid-renderer.js").read_text()
        assert "load" in js

    @pytest.mark.sphinx("html", testroot="basic")
    def test_es_module_format(self, app: Sphinx, build_all: None) -> None:
        """renderer.js uses ES module import syntax."""
        js = (app.outdir / "_static" / "oceanid-renderer.js").read_text()
        assert "import" in js


class TestObserverJsContent:
    """Verify observer.js contains expected structure (T020)."""

    @pytest.mark.sphinx("html", testroot="basic")
    def test_render_visible_diagrams_export(self, app: Sphinx, build_all: None) -> None:
        """observer.js exports renderVisibleDiagrams."""
        js = (app.outdir / "_static" / "oceanid-observer.js").read_text()
        assert "renderVisibleDiagrams" in js
        assert "export" in js

    @pytest.mark.sphinx("html", testroot="basic")
    def test_setup_lazy_rendering_export(self, app: Sphinx, build_all: None) -> None:
        """observer.js exports setupLazyRendering."""
        js = (app.outdir / "_static" / "oceanid-observer.js").read_text()
        assert "setupLazyRendering" in js

    @pytest.mark.sphinx("html", testroot="basic")
    def test_intersection_observer_usage(self, app: Sphinx, build_all: None) -> None:
        """observer.js uses IntersectionObserver for lazy rendering."""
        js = (app.outdir / "_static" / "oceanid-observer.js").read_text()
        assert "IntersectionObserver" in js

    @pytest.mark.sphinx("html", testroot="basic")
    def test_render_error_handling(self, app: Sphinx, build_all: None) -> None:
        """observer.js handles render errors (FR-023)."""
        js = (app.outdir / "_static" / "oceanid-observer.js").read_text()
        assert "data-oceanid-render-failed" in js
        assert "oceanid-render-error" in js

    @pytest.mark.sphinx("html", testroot="basic")
    def test_data_attribute_state_management(self, app: Sphinx, build_all: None) -> None:
        """observer.js manages data-oceanid-rendered attribute."""
        js = (app.outdir / "_static" / "oceanid-observer.js").read_text()
        assert "data-oceanid-rendered" in js

    @pytest.mark.sphinx("html", testroot="basic")
    def test_data_deferred_attribute(self, app: Sphinx, build_all: None) -> None:
        """observer.js sets data-oceanid-deferred attribute."""
        js = (app.outdir / "_static" / "oceanid-observer.js").read_text()
        assert "data-oceanid-deferred" in js

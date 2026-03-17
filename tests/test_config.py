"""Tests for sphinx_oceanid.config module."""

from types import SimpleNamespace

from sphinx_oceanid.config import (
    BEAUTIFUL_MERMAID_CDN_TEMPLATE,
    BEAUTIFUL_MERMAID_VERSION,
    CONFIG_SPECS,
    ConfigSpec,
    resolve_js_url,
)


class TestConfigSpec:
    """Tests for ConfigSpec dataclass."""

    def test_config_spec_is_frozen(self) -> None:
        spec = ConfigSpec("test", "default", "html", str, "desc")
        assert spec.name == "test"
        assert spec.default == "default"

    def test_config_specs_all_have_unique_names(self) -> None:
        """All config spec names must be unique."""
        names = [spec.name for spec in CONFIG_SPECS]
        assert len(names) == len(set(names))

    def test_config_specs_all_have_oceanid_prefix(self) -> None:
        """All config spec names must start with 'oceanid_'."""
        for spec in CONFIG_SPECS:
            assert spec.name.startswith("oceanid_"), f"{spec.name} missing oceanid_ prefix"

    def test_config_specs_count(self) -> None:
        """CONFIG_SPECS should contain exactly 13 settings."""
        assert len(CONFIG_SPECS) == 13

    def test_config_specs_all_rebuild_html(self) -> None:
        """All config specs should trigger HTML rebuild."""
        for spec in CONFIG_SPECS:
            assert spec.rebuild == "html", f"{spec.name} rebuild is {spec.rebuild}, expected 'html'"


class TestResolveJsUrl:
    """Tests for resolve_js_url function."""

    def test_resolve_js_url_default(self) -> None:
        """Default config produces CDN URL with default version."""
        config = SimpleNamespace(oceanid_local_js="", oceanid_version=BEAUTIFUL_MERMAID_VERSION)
        url = resolve_js_url(config)
        expected = BEAUTIFUL_MERMAID_CDN_TEMPLATE.format(version=BEAUTIFUL_MERMAID_VERSION)
        assert url == expected

    def test_resolve_js_url_custom_version(self) -> None:
        """Custom version produces CDN URL with that version."""
        config = SimpleNamespace(oceanid_local_js="", oceanid_version="2.0.0")
        url = resolve_js_url(config)
        expected = BEAUTIFUL_MERMAID_CDN_TEMPLATE.format(version="2.0.0")
        assert url == expected

    def test_resolve_js_url_local_path(self) -> None:
        """Local path takes priority over CDN URL."""
        config = SimpleNamespace(
            oceanid_local_js="/static/beautiful-mermaid.js", oceanid_version=BEAUTIFUL_MERMAID_VERSION
        )
        url = resolve_js_url(config)
        assert url == "/static/beautiful-mermaid.js"


class TestConstants:
    """Tests for module-level constants."""

    def test_beautiful_mermaid_version(self) -> None:
        assert BEAUTIFUL_MERMAID_VERSION == "1.1.3"

    def test_cdn_template_contains_version_placeholder(self) -> None:
        assert "{version}" in BEAUTIFUL_MERMAID_CDN_TEMPLATE

    def test_cdn_template_produces_valid_url(self) -> None:
        url = BEAUTIFUL_MERMAID_CDN_TEMPLATE.format(version="1.0.0")
        assert url.startswith("https://")
        assert "1.0.0" in url

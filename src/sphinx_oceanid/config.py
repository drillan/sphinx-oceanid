"""Config definitions, validation, and CDN URL resolution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

_ConfigRebuild = Literal["", "env", "epub", "gettext", "html", "applehelp", "devhelp"]

if TYPE_CHECKING:
    from sphinx.application import Sphinx

BEAUTIFUL_MERMAID_VERSION = "1.1.3"
BEAUTIFUL_MERMAID_CDN_TEMPLATE = "https://esm.sh/beautiful-mermaid@{version}"

SUPPORTED_DIAGRAM_TYPES: frozenset[str] = frozenset(
    {
        "flowchart",
        "graph",  # flowchart alias
        "stateDiagram",
        "stateDiagram-v2",
        "sequenceDiagram",
        "classDiagram",
        "erDiagram",
        "xychart-beta",
    }
)


@dataclass(frozen=True)
class ConfigSpec:
    """Declarative specification for a single Sphinx config value."""

    name: str
    default: object
    rebuild: _ConfigRebuild
    types: type | tuple[type, ...]
    description: str


CONFIG_SPECS: tuple[ConfigSpec, ...] = (
    # Rendering
    ConfigSpec("oceanid_version", BEAUTIFUL_MERMAID_VERSION, "html", str, "beautiful-mermaid library version"),
    ConfigSpec("oceanid_local_js", "", "html", str, "Path to local beautiful-mermaid JS bundle"),
    ConfigSpec(
        "oceanid_unsupported_action",
        "warning",
        "html",
        str,
        "Action for unsupported diagram types: 'warning' or 'error'",
    ),
    # Theme
    ConfigSpec("oceanid_theme", "auto", "html", str, "Theme name or 'auto' for detection"),
    ConfigSpec("oceanid_theme_dark", "zinc-dark", "html", str, "Dark theme when oceanid_theme='auto'"),
    ConfigSpec("oceanid_theme_light", "zinc-light", "html", str, "Light theme when oceanid_theme='auto'"),
    # Layout
    ConfigSpec("oceanid_width", "100%", "html", str, "Diagram container width"),
    ConfigSpec("oceanid_height", "auto", "html", str, "Diagram container height"),
    # Feature flags
    ConfigSpec("oceanid_zoom", False, "html", bool, "Enable zoom on all diagrams"),
    ConfigSpec("oceanid_fullscreen", False, "html", bool, "Enable fullscreen modal"),
    ConfigSpec("oceanid_fullscreen_button", "\u26f6", "html", str, "Fullscreen button character"),
    ConfigSpec("oceanid_fullscreen_button_opacity", 50, "html", int, "Fullscreen button opacity (0-100)"),
    ConfigSpec("oceanid_js_priority", 500, "html", int, "JS load priority"),
)


def register_config_values(app: Sphinx) -> None:
    """Register all config values with Sphinx."""
    for spec in CONFIG_SPECS:
        app.add_config_value(
            spec.name,
            spec.default,
            spec.rebuild,
            types=spec.types,
            description=spec.description,
        )


VALID_UNSUPPORTED_ACTIONS: frozenset[str] = frozenset({"warning", "error"})


def validate_config(app: Sphinx, config: object) -> None:
    """Validate config values at config-inited event.

    Raises:
        ExtensionError: If ``oceanid_unsupported_action`` is not a valid value.
    """
    from sphinx.errors import ExtensionError

    action: str = config.oceanid_unsupported_action  # type: ignore[attr-defined]
    if action not in VALID_UNSUPPORTED_ACTIONS:
        valid_list = ", ".join(sorted(VALID_UNSUPPORTED_ACTIONS))
        raise ExtensionError(f'Invalid oceanid_unsupported_action: "{action}". Valid values: {valid_list}.')


def resolve_js_url(config: object) -> str:
    """Resolve beautiful-mermaid JS URL from Sphinx config.

    Args:
        config: Sphinx config object.

    Returns:
        URL string for the beautiful-mermaid JS bundle.
    """
    local_path: str = config.oceanid_local_js  # type: ignore[attr-defined]
    if local_path:
        return local_path
    version: str = config.oceanid_version  # type: ignore[attr-defined]
    return BEAUTIFUL_MERMAID_CDN_TEMPLATE.format(version=version)

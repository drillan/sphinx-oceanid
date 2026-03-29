"""Per-page JS/CSS asset injection for Mermaid diagrams."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, cast

from .config import resolve_js_url
from .nodes import mermaid_node

if TYPE_CHECKING:
    from collections.abc import Callable

    from docutils import nodes
    from sphinx.application import Sphinx


def install_assets(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, object],
    doctree: nodes.document | None,
) -> None:
    """Inject JS/CSS assets on pages containing mermaid_node.

    Connected to the ``html-page-context`` event. Only injects assets
    on pages that contain at least one mermaid diagram (FR-012).
    """
    if doctree is None:
        return

    mermaid_nodes = list(doctree.findall(mermaid_node))
    if not mermaid_nodes:
        return

    page_config = _build_page_config(app, mermaid_nodes)
    config_json = json.dumps(page_config, ensure_ascii=False).replace("</", r"<\/")
    beautiful_mermaid_url = cast("str", page_config["beautifulMermaidUrl"])

    pathto = cast("Callable[[str, bool], str]", context["pathto"])
    js_url = pathto("_static/oceanid-renderer.js", True)
    css_url = pathto("_static/oceanid.css", True)

    assets_html = (
        f'\n<link rel="stylesheet" href="{css_url}" />\n'
        f'<script type="application/json" id="oceanid-config">{config_json}</script>\n'
        f"{_build_bootstrap_script(beautiful_mermaid_url)}\n"
        f'<script type="module" src="{js_url}"></script>\n'
    )

    body = cast("str", context["body"])
    context["body"] = body + assets_html


def _build_page_config(
    app: Sphinx,
    mermaid_nodes: list[mermaid_node],
) -> dict[str, object]:
    """Build the per-page config JSON for JavaScript consumption."""
    config = app.config

    zoom_selectors: list[str] = []
    for node in mermaid_nodes:
        if node.get("zoom"):
            ids: list[str] = node.get("ids", [])
            element_id = ids[0] if ids else node.get("zoom_id", "")
            if element_id:
                zoom_selectors.append(f"#{element_id}")

    return {
        "beautifulMermaidUrl": resolve_js_url(config),
        "theme": config.oceanid_theme,
        "themeDark": config.oceanid_theme_dark,
        "themeLight": config.oceanid_theme_light,
        "width": config.oceanid_width,
        "height": config.oceanid_height,
        "zoom": config.oceanid_zoom,
        "zoomSelectors": zoom_selectors,
        "fullscreen": config.oceanid_fullscreen,
        "fullscreenButton": config.oceanid_fullscreen_button,
        "fullscreenButtonOpacity": config.oceanid_fullscreen_button_opacity,
        "revealjs": app.builder.name == "revealjs",
    }


def _build_bootstrap_script(beautiful_mermaid_url: str) -> str:
    """Build inline bootstrap script for FR-024 module load failure handling."""
    safe_url = json.dumps(beautiful_mermaid_url)
    return (
        "<script>(function() {"
        f"var url = {safe_url};"
        "import(url).catch(function(err) {"
        'document.querySelectorAll("[data-oceanid-code]").forEach(function(el) {'
        'if (!el.querySelector(".oceanid-source-display")) {'
        'var pre = document.createElement("pre");'
        'pre.className = "oceanid-source-display";'
        'pre.textContent = el.getAttribute("data-oceanid-code");'
        "el.appendChild(pre);"
        "}"
        "});"
        'console.error("sphinx-oceanid: Failed to load beautiful-mermaid:", err);'
        "});"
        "})();</script>"
    )

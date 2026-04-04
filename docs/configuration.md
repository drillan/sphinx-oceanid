# Configuration

All configuration options use the `oceanid_` prefix in your Sphinx `conf.py`.

## Rendering

### `oceanid_version`

| | |
|---|---|
| **Type** | `str` |
| **Default** | `"1.1.3"` |

The [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) library version loaded from CDN. Ignored when `oceanid_local_js` is set.

```python
oceanid_version = "1.1.3"
```

### `oceanid_local_js`

| | |
|---|---|
| **Type** | `str` |
| **Default** | `""` (empty — uses CDN) |

Path to a local beautiful-mermaid JS bundle. When set, the CDN URL is not used. The path is relative to the HTML output root (the value is used as-is as a script URL).

```python
oceanid_local_js = "_static/beautiful-mermaid.js"
```

(conf-oceanid-unsupported-action)=
### `oceanid_unsupported_action`

| | |
|---|---|
| **Type** | `str` |
| **Default** | `"warning"` |

Action taken when an unsupported diagram type is encountered. beautiful-mermaid supports 6 diagram types (flowchart, sequenceDiagram, classDiagram, stateDiagram, erDiagram, xychart-beta). For any other type, sphinx-oceanid produces a build warning or raises an error — never silent degradation.

Valid values: `"warning"`, `"error"`.

```python
# Fail the build on unsupported diagram types
oceanid_unsupported_action = "error"
```

## Theme

### `oceanid_theme`

| | |
|---|---|
| **Type** | `str` |
| **Default** | `"auto"` |

Theme name for diagram rendering. When set to `"auto"`, the theme is detected from the Sphinx HTML theme's dark/light mode at runtime using CSS variables. Set to a specific theme name to override auto-detection.

```python
oceanid_theme = "auto"
```

### `oceanid_theme_dark`

| | |
|---|---|
| **Type** | `str` |
| **Default** | `"zinc-dark"` |

Theme used when `oceanid_theme = "auto"` and the page is in dark mode.

```python
oceanid_theme_dark = "zinc-dark"
```

### `oceanid_theme_light`

| | |
|---|---|
| **Type** | `str` |
| **Default** | `"zinc-light"` |

Theme used when `oceanid_theme = "auto"` and the page is in light mode.

```python
oceanid_theme_light = "zinc-light"
```

## Layout

### `oceanid_width`

| | |
|---|---|
| **Type** | `str` |
| **Default** | `"100%"` |

CSS width for the diagram container. Accepts any valid CSS width value.

```python
oceanid_width = "80%"
```

### `oceanid_height`

| | |
|---|---|
| **Type** | `str` |
| **Default** | `"auto"` |

CSS height for the diagram container. Accepts any valid CSS height value.

```python
oceanid_height = "400px"
```

## Feature Flags

### `oceanid_zoom`

| | |
|---|---|
| **Type** | `bool` |
| **Default** | `False` |

Enable pan-and-zoom interaction on all diagrams globally. Uses native Pointer Events and SVG viewBox manipulation — no d3.js dependency. Mouse wheel to zoom, drag to pan, double-click to reset, pinch to zoom on touch devices.

To enable zoom on individual diagrams only, use the `:zoom:` directive option instead.

```python
oceanid_zoom = True
```

### `oceanid_fullscreen`

| | |
|---|---|
| **Type** | `bool` |
| **Default** | `False` |

Enable a fullscreen button on all diagrams. Clicking it opens the diagram in a viewport-sized modal overlay. Close with Escape key, clicking outside, or the close button.

```python
oceanid_fullscreen = True
```

### `oceanid_fullscreen_button`

| | |
|---|---|
| **Type** | `str` |
| **Default** | `"⛶"` (U+26F6) |

Character displayed on the fullscreen button.

```python
oceanid_fullscreen_button = "🔍"
```

### `oceanid_fullscreen_button_opacity`

| | |
|---|---|
| **Type** | `int` |
| **Default** | `50` |

Opacity of the fullscreen button, from 0 (fully transparent) to 100 (fully opaque).

```python
oceanid_fullscreen_button_opacity = 80
```

## Quick reference

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `oceanid_version` | `str` | `"1.1.3"` | beautiful-mermaid library version |
| `oceanid_local_js` | `str` | `""` | Path to local JS bundle |
| `oceanid_unsupported_action` | `str` | `"warning"` | Action for unsupported diagram types |
| `oceanid_theme` | `str` | `"auto"` | Theme name or auto-detection |
| `oceanid_theme_dark` | `str` | `"zinc-dark"` | Dark theme for auto mode |
| `oceanid_theme_light` | `str` | `"zinc-light"` | Light theme for auto mode |
| `oceanid_width` | `str` | `"100%"` | Diagram container width |
| `oceanid_height` | `str` | `"auto"` | Diagram container height |
| `oceanid_zoom` | `bool` | `False` | Enable zoom globally |
| `oceanid_fullscreen` | `bool` | `False` | Enable fullscreen modal |
| `oceanid_fullscreen_button` | `str` | `"⛶"` | Fullscreen button character |
| `oceanid_fullscreen_button_opacity` | `int` | `50` | Button opacity (0–100) |

## Migrating from sphinxcontrib-mermaid

sphinx-oceanid uses the `oceanid_` prefix to coexist with sphinxcontrib-mermaid during migration. The table below maps common sphinxcontrib-mermaid settings to their sphinx-oceanid equivalents:

| sphinxcontrib-mermaid | sphinx-oceanid | Notes |
|-----------------------|----------------|-------|
| `mermaid_version` | `oceanid_version` | beautiful-mermaid version, not standard Mermaid.js |
| `mermaid_init_js` | — | Not applicable; beautiful-mermaid handles initialization |
| `mermaid_output_format` | — | Always SVG (beautiful-mermaid renders SVG only) |
| — | `oceanid_theme` | New: automatic dark/light theme detection |
| — | `oceanid_zoom` | New: built-in pan & zoom |
| — | `oceanid_fullscreen` | New: fullscreen modal |

To migrate:

1. Replace `sphinxcontrib.mermaid` with `sphinx_oceanid` in the `extensions` list.
2. Replace `mermaid_` prefixed settings with the corresponding `oceanid_` settings.
3. Remove settings that have no equivalent (e.g., `mermaid_init_js`, `mermaid_output_format`).
4. Verify that all diagrams use {ref}`supported types <supported-diagram-types>`. Unsupported types produce warnings by default.

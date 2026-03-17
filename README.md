# sphinx-oceanid

High-quality Mermaid diagrams in Sphinx, powered by [beautiful-mermaid](https://github.com/niccolozy/beautiful-mermaid).

## Features

- **beautiful-mermaid rendering** — Uses ELK.js-based layout engine for high-quality SVG output
- **CSS variable theming** — Automatic dark/light theme detection with instant switching (no re-render)
- **Zero-config** — Works out of the box with CDN-hosted beautiful-mermaid
- **sphinx-revealjs support** — Lazy rendering for hidden slides via IntersectionObserver
- **Pan & zoom** — Native Pointer Events + SVG transform (no d3.js dependency)
- **Fullscreen modal** — View diagrams in a viewport-sized overlay
- **External file support** — Reference `.mmd` files instead of inline code
- **Auto class diagrams** — Generate class hierarchy diagrams from Python code

## Supported Diagram Types

| Type | Alias |
|------|-------|
| `flowchart` | `graph` |
| `sequenceDiagram` | |
| `classDiagram` | |
| `stateDiagram` | `stateDiagram-v2` |
| `erDiagram` | |
| `xychart-beta` | |

Unsupported diagram types produce explicit warnings (or errors), never silent degradation.

## Installation

sphinx-oceanid requires Python 3.13+.

From GitHub:

```bash
pip install git+https://github.com/drillan/sphinx-oceanid.git
```

Or clone and install locally:

```bash
git clone https://github.com/drillan/sphinx-oceanid.git
cd sphinx-oceanid
pip install .
```

## Quick Start

Add the extension to your `conf.py`:

```python
extensions = ["sphinx_oceanid"]
```

Then use the `mermaid` directive in your reStructuredText files:

```rst
.. mermaid::

   flowchart LR
     A[Start] --> B[Process] --> C[End]
```

Or in Markdown (MyST) files:

````markdown
```{mermaid}
sequenceDiagram
  Alice->>Bob: Hello
  Bob-->>Alice: Hi!
```
````

## Configuration

All configuration options use the `oceanid_` prefix in `conf.py`:

```python
# conf.py
extensions = ["sphinx_oceanid"]

# Theme (default: "auto" — detects dark/light from Sphinx theme)
oceanid_theme = "auto"
oceanid_theme_dark = "zinc-dark"
oceanid_theme_light = "zinc-light"

# Enable zoom on all diagrams (default: False)
oceanid_zoom = True

# Enable fullscreen modal (default: False)
oceanid_fullscreen = True

# Action for unsupported diagram types: "warning" or "error" (default: "warning")
oceanid_unsupported_action = "warning"
```

## Directive Options

```rst
.. mermaid::
   :name: my-diagram
   :alt: Description for accessibility
   :align: center
   :caption: Diagram caption (rendered as <figcaption>)
   :title: Mermaid native title (rendered inside the diagram)
   :zoom:
   :config: {"theme": "forest"}

   flowchart LR
     A --> B --> C
```

## Auto Class Diagrams

Generate class hierarchy diagrams from Python code:

```rst
.. autoclasstree:: mypackage.MyClass
   :full:
   :namespace: mypackage
   :caption: Class hierarchy
```

## Documentation

Full documentation is available in the [docs/](docs/) directory.

## License

BSD-3-Clause. See [LICENSE](LICENSE) for details.

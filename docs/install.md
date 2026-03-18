# Installation

## Requirements

- **Python**: 3.13 or later
- **Sphinx**: 7.4 or later

## Install from GitHub

```bash
pip install git+https://github.com/drillan/sphinx-oceanid.git
```

Or clone and install locally:

```bash
git clone https://github.com/drillan/sphinx-oceanid.git
cd sphinx-oceanid
pip install .
```

## Enable the extension

Add `sphinx_oceanid` to the `extensions` list in your Sphinx `conf.py`:

```python
extensions = ["sphinx_oceanid"]
```

No additional configuration is required. sphinx-oceanid works out of the box using the CDN-hosted [beautiful-mermaid](https://github.com/niccolozy/beautiful-mermaid) library.

## Local beautiful-mermaid bundle (optional)

By default, sphinx-oceanid loads beautiful-mermaid from the [esm.sh](https://esm.sh/) CDN. To use a local copy instead:

1. Download the beautiful-mermaid JS bundle.

2. Place it in your Sphinx `_static/` directory (e.g., `_static/beautiful-mermaid.js`).

3. Set the path in `conf.py` (the path is relative to the HTML output root):

   ```python
   oceanid_local_js = "_static/beautiful-mermaid.js"
   ```

When `oceanid_local_js` is set, the CDN URL is not used.

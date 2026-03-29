# Getting Started

## Install

```bash
pip install sphinx-oceanid
```

For other installation methods, see {doc}`install`.

## Enable the extension

Add `sphinx_oceanid` to the `extensions` list in your Sphinx `conf.py`:

```python
extensions = ["sphinx_oceanid"]
```

No additional configuration is required. sphinx-oceanid works out of the box using the CDN-hosted [beautiful-mermaid](https://github.com/niccolozy/beautiful-mermaid) library.

## Write your first diagram

Use the `mermaid` directive in your documentation:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::

   flowchart LR
     A[Start] --> B[Process] --> C[End]
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
flowchart LR
  A[Start] --> B[Process] --> C[End]
```
````
:::
::::

For the full list of directive options and usage examples, see {doc}`index`.

## Preview

Mermaid diagrams require HTTP serving — opening built HTML via `file://` will not render diagrams due to browser CORS restrictions.

```bash
# Quick static server (no extra dependencies)
make -C docs serve

# Live reload (requires sphinx-autobuild)
pip install sphinx-oceanid[preview]
make -C docs livehtml
```

For Makefile setup and local bundle configuration, see {doc}`install`.

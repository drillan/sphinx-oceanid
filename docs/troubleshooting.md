# Troubleshooting and FAQ

## Common Issues

### Diagrams not rendering when opening HTML files directly

**Symptom**: Diagrams show the raw Mermaid source code when opening built HTML via `file://` in the browser. The browser developer console shows a CORS error.

**Cause**: `oceanid-renderer.js` dynamically imports beautiful-mermaid from the CDN using `await import(...)`. Browsers block cross-origin ES module imports from `file://` to `https://` due to the Same-Origin Policy. This also applies when using `oceanid_local_js` with a local bundle — `file://` blocks ES module `import()` regardless of the source location.

This is a browser security restriction, not a sphinx-oceanid bug.

**Solution**: Serve the documentation via HTTP instead of opening files directly.

Using sphinx-autobuild (recommended for active editing):

```bash
make livehtml
```

Using Python's built-in HTTP server (no extra dependencies):

```bash
make serve
```

See {doc}`install` for setup instructions and Makefile snippets.

### CDN unreachable

**Symptom**: Diagrams show the raw Mermaid source code instead of rendered SVG.

**Cause**: The beautiful-mermaid library cannot be loaded from the CDN. This can happen in offline environments, restricted networks, or when the CDN is temporarily unavailable.

**Diagnosis**:
1. Open the browser developer console (F12)
2. Check for network errors related to `esm.sh` or `beautiful-mermaid`
3. Look for `data-oceanid-render-failed` attributes on diagram containers

**Solution**: Use a local JS bundle instead of the CDN:

1. Download the beautiful-mermaid JS file
2. Place it in your Sphinx project's `_static/` directory
3. Configure `conf.py`:

```python
oceanid_local_js = "_static/beautiful-mermaid.js"
```

See {doc}`configuration` for details on the `oceanid_local_js` setting.

### Rendering errors

**Symptom**: A diagram shows an error message box with the original Mermaid source code, and the container has the `data-oceanid-render-failed` attribute.

**Cause**: beautiful-mermaid failed to parse or render the Mermaid code. This is typically caused by syntax errors in the diagram definition.

**Diagnosis**:
1. Open the browser developer console (F12) to see the detailed error message
2. Check the error message displayed in the diagram area — it includes the specific rendering failure reason
3. Verify that the Mermaid syntax is valid using the [Mermaid Live Editor](https://mermaid.live/)

**Solution**:
- Fix syntax errors in the Mermaid code
- Ensure the diagram type is one of the {ref}`supported types <supported-diagram-types>`
- Note: beautiful-mermaid may silently produce incomplete diagrams for certain syntax errors without raising an error. Always verify your diagrams visually after building

### Theme mismatch

**Symptom**: Diagrams do not match the page's dark or light theme, or the colors look wrong after switching themes.

**Cause**: The theme settings in `conf.py` may not align with the Sphinx HTML theme's dark/light mode mechanism.

**Diagnosis**:
1. Check the current `oceanid_theme` setting — when set to `"auto"`, themes are detected at runtime via CSS variables
2. Inspect the `<script id="oceanid-config">` element in the page source to verify the theme configuration
3. Check if your Sphinx HTML theme supports CSS variable-based dark/light switching

**Solution**:

- For automatic detection (recommended):

  ```python
  oceanid_theme = "auto"
  oceanid_theme_dark = "zinc-dark"
  oceanid_theme_light = "zinc-light"
  ```

- If auto-detection does not work with your theme, set a fixed theme:

  ```python
  oceanid_theme = "zinc-light"  # or any specific theme name
  ```

- Theme changes apply instantly via CSS variable swapping — no page reload or re-render is needed

See {doc}`configuration` for all theme settings.

### Unsupported diagram types

**Symptom**: An error box appears in the HTML output showing "Diagram type X is not supported by sphinx-oceanid" with a list of supported types. The Sphinx build log contains a warning.

**Cause**: beautiful-mermaid supports 6 diagram types only. Diagram types outside this set (e.g., `gantt`, `pie`, `gitGraph`, `mindmap`) cannot be rendered.

**Diagnosis**:
1. Check the build output for warnings like: `Unsupported Mermaid diagram type: "gantt"`
2. The error box in the HTML output displays the unsupported type and the supported types list

**Solution**:
- Use only {ref}`supported diagram types <supported-diagram-types>`: `flowchart`/`graph`, `sequenceDiagram`, `classDiagram`, `stateDiagram`/`stateDiagram-v2`, `erDiagram`, `xychart-beta`
- To make unsupported types fail the build instead of producing warnings:

  ```python
  oceanid_unsupported_action = "error"
  ```

- sphinx-oceanid does not support switching to standard Mermaid.js for unsupported types. See {doc}`supported-diagrams` for the full list.

### sphinx-revealjs: diagrams not rendering on non-initial slides

**Symptom**: Diagrams on slides other than the first one do not appear, or appear blank.

**Cause**: Reveal.js hides non-active slides using CSS. Diagrams on hidden slides are deferred and rendered when the slide becomes visible.

**Diagnosis**:
1. Navigate to the slide containing the diagram — it should render upon becoming visible
2. If it still does not render, open the developer console and check for JavaScript errors
3. Verify that `"revealjs": true` appears in the `<script id="oceanid-config">` JSON on the page

**Solution**:
- sphinx-oceanid automatically detects the `revealjs` builder and enables lazy rendering via IntersectionObserver and the `slidechanged` event. No manual configuration is needed
- If diagrams still do not render, ensure both extensions are registered:

  ```python
  extensions = ["sphinx_oceanid", "sphinx_revealjs"]
  ```

- If a slide uses custom CSS that sets `display: none` (outside of Reveal.js's default mechanism), the IntersectionObserver may not trigger. The `slidechanged` event listener handles this case

See {doc}`revealjs` for details.

### Local JS bundle not loading

**Symptom**: Diagrams are not rendered and the browser console shows a 404 error for the JavaScript file.

**Cause**: The path specified in `oceanid_local_js` does not point to an existing file in the HTML output directory.

**Diagnosis**:
1. Open the browser developer console and check for 404 errors
2. Verify the file exists at the specified path relative to the HTML output root

**Solution**:
- Ensure the JS file is placed in the correct location (e.g., `docs/_static/beautiful-mermaid.js`)
- The `oceanid_local_js` value is used as-is as a script URL. For files in `_static/`:

  ```python
  oceanid_local_js = "_static/beautiful-mermaid.js"
  ```

- After building, verify the file exists in the output directory (e.g., `docs/_build/html/_static/beautiful-mermaid.js`)

### Migration from sphinxcontrib-mermaid

**Symptom**: After switching from sphinxcontrib-mermaid to sphinx-oceanid, some diagrams show warnings or errors.

**Cause**: sphinx-oceanid uses beautiful-mermaid (6 diagram types) instead of standard Mermaid.js (20+ types), and configuration prefixes differ.

**Solution**:

1. Replace the extension in `conf.py`:

   ```python
   # Before
   extensions = ["sphinxcontrib.mermaid"]

   # After
   extensions = ["sphinx_oceanid"]
   ```

2. Update configuration prefixes (`mermaid_` to `oceanid_`):

   ```python
   # Before
   mermaid_version = "10.6.1"

   # After
   oceanid_version = "1.1.3"
   ```

3. Remove settings that have no equivalent in sphinx-oceanid (e.g., `mermaid_init_js`, `mermaid_output_format`)

4. Verify all diagrams use {ref}`supported types <supported-diagram-types>`. Unsupported types produce warnings by default — set `oceanid_unsupported_action = "error"` to catch them during the build

See the migration table in {doc}`configuration` for a full mapping of settings.

## FAQ

### Which diagram types are supported?

sphinx-oceanid supports 6 diagram types via beautiful-mermaid: `flowchart`/`graph`, `sequenceDiagram`, `classDiagram`, `stateDiagram`/`stateDiagram-v2`, `erDiagram`, and `xychart-beta`.

See {doc}`supported-diagrams` for examples and the full list of unsupported types.

### Can I use standard Mermaid.js instead of beautiful-mermaid?

No. sphinx-oceanid is designed specifically around beautiful-mermaid's ELK.js-based rendering engine for high-quality diagram layout. There is no option to switch to standard Mermaid.js, and unsupported diagram types are never silently rendered with a different engine.

If you need diagram types that beautiful-mermaid does not support, consider using [sphinxcontrib-mermaid](https://github.com/mgaitan/sphinxcontrib-mermaid) for those specific diagrams. Both extensions can coexist in the same project thanks to the different configuration prefixes (`oceanid_` vs `mermaid_`).

### Does it work with PDF/LaTeX output?

No. sphinx-oceanid produces HTML output only. beautiful-mermaid is a client-side JavaScript library that requires a browser to render diagrams. LaTeX, PDF, epub, and other non-HTML Sphinx builders are not supported.

### How does theme auto-detection work?

When `oceanid_theme` is set to `"auto"` (the default), sphinx-oceanid detects the page's dark or light mode at runtime using CSS variables from the Sphinx HTML theme. The detection works as follows:

1. The browser checks CSS variables to determine whether the page is in dark or light mode
2. If dark mode is detected, the `oceanid_theme_dark` theme is applied (default: `"zinc-dark"`)
3. If light mode is detected, the `oceanid_theme_light` theme is applied (default: `"zinc-light"`)
4. When the user toggles the theme, the change is applied instantly via CSS variable swapping — no page reload or diagram re-render is needed

This works with Sphinx themes that support CSS variable-based dark/light switching (e.g., Shibuya, Furo, PyData). If your theme uses a different mechanism, set `oceanid_theme` to a specific theme name instead.

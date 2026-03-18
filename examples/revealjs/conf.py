project = "sphinx-oceanid slides"

extensions = ["myst_parser", "sphinx_oceanid", "sphinx_revealjs"]
exclude_patterns = ["_build"]

# Reveal.js theme
revealjs_style_theme = "white"

# Force light theme (Reveal.js does not expose data-theme attributes,
# so auto-detection falls back to OS prefers-color-scheme)
oceanid_theme = "zinc-light"

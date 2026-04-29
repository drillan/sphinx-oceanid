# Installation

## Requirements

- **Python**: 3.13 or later
- **Sphinx**: 7.4 or later

## Install from PyPI

```bash
pip install sphinx-oceanid
```

## Install from source

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

No additional configuration is required. sphinx-oceanid works out of the box using the CDN-hosted [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) library.

## Local beautiful-mermaid bundle (optional)

By default, sphinx-oceanid loads beautiful-mermaid from the [esm.sh](https://esm.sh/) CDN. To use a local copy instead:

1. Download the beautiful-mermaid JS bundle.

2. Place it in your Sphinx `_static/` directory (e.g., `_static/beautiful-mermaid.js`).

3. Set the path in `conf.py` (the path is relative to the HTML output root):

   ```python
   oceanid_local_js = "_static/beautiful-mermaid.js"
   ```

When `oceanid_local_js` is set, the CDN URL is not used.

## Previewing documentation locally

sphinx-oceanid uses ES module dynamic imports to load beautiful-mermaid. Browsers block these imports when HTML files are opened via the `file://` protocol (CORS restriction). **You must serve the documentation via HTTP to see rendered diagrams locally.**

### Quick start: `make serve`

Add these targets to your project's `docs/Makefile`:

````makefile
.PHONY: serve livehtml

PORT ?= 8000

serve: html
	@echo "Serving at http://localhost:$(PORT) — press Ctrl+C to stop"
	python3 -m http.server -d $(BUILDDIR)/html $(PORT)

livehtml:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
````

- **`make serve`** — Build HTML and start a static server. No extra dependencies. Requires manual rebuild after changes.
- **`make livehtml`** — Auto-rebuild on file changes with live browser reload. Requires [sphinx-autobuild](https://github.com/sphinx-doc/sphinx-autobuild).

### Installing sphinx-autobuild

```bash
pip install sphinx-oceanid[preview]
```

Or install sphinx-autobuild directly:

```bash
pip install sphinx-autobuild
```

### Changing the port

```bash
make serve PORT=9000
```

## Claude Code Skill

sphinx-oceanid ships a `mermaid-diagram` skill that gives AI coding agents (Claude Code, GitHub Copilot, Cursor, etc.) proactive Mermaid suggestions and syntax validation while editing Sphinx docs.

### Prerequisites

- [GitHub CLI](https://cli.github.com/) **2.91 or later** (the `gh skill` extension is bundled; preview)

### Install

```bash
gh skill install drillan/sphinx-oceanid mermaid-diagram --agent claude-code
```

Supported `--agent` values and install destinations:

| Agent | Project scope (default) | User scope (`--scope user`) |
|-------|--------------------------|------------------------------|
| `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| `github-copilot` | `.agents/skills/` | `~/.copilot/skills/` |
| `cursor` | `.agents/skills/` | `~/.cursor/skills/` |
| `codex`, `gemini`, `antigravity` | `.agents/skills/` | per-agent default |

### Pin to a specific version

```bash
gh skill install drillan/sphinx-oceanid mermaid-diagram \
    --agent claude-code --pin v0.1.2
```

### Update or remove

```bash
gh skill update --all              # update every installed skill
gh skill update mermaid-diagram    # update only this skill
```

To remove the skill, delete its directory (e.g., `rm -rf .claude/skills/mermaid-diagram`).

### Manual install (without gh CLI)

Clone the repository and copy the skill directory:

```bash
git clone https://github.com/drillan/sphinx-oceanid.git
cp -r sphinx-oceanid/skills/mermaid-diagram .claude/skills/
```

Manually placed skills are not tracked by `gh skill update`.

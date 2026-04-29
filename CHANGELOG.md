# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- `mermaid-diagram` skill installable via `gh skill install drillan/sphinx-oceanid mermaid-diagram` (preview)
- Claude Code skill installation guide in `README.md`, `README.ja.md`, and `docs/install.md`
- `license: BSD-3-Clause` field in `skills/mermaid-diagram/SKILL.md` frontmatter

### Changed

- Shortened `mermaid-diagram` skill description to satisfy `gh skill publish` recommended max (1024 chars)
- **Breaking**: `oceanid_zoom` default changed from `False` to `True` — pan-and-zoom is now enabled on all diagrams by default. Set `oceanid_zoom = False` in `conf.py` to restore previous behavior.
- **Breaking**: `oceanid_fullscreen` default changed from `False` to `True` — the fullscreen button is now shown on all diagrams by default. Set `oceanid_fullscreen = False` in `conf.py` to restore previous behavior.

## [0.1.2] - 2026-03-29

### Added

- YAML frontmatter support for `title` and `config` in `.mmd` files, RST inline content, and MyST directive options (#58, #57)
- Per-diagram rendering overrides via `data-oceanid-config` (beautiful-mermaid `RenderOptions` compatible keys)
- Diagram title display via `data-oceanid-title` rendered as heading above SVG
- Sample `.mmd` file with frontmatter in documentation
- YAML Frontmatter section in docs with examples for all three input patterns

### Changed

- `_parse_mermaid_config()` now accepts both JSON strings and pre-parsed dicts
- Added `pyyaml` to dependencies for YAML frontmatter parsing

## [0.1.1] - 2026-03-29

### Changed

- Enrich supported-diagrams examples with subgraphs and node shapes (#55)
- Add per-diagram-type known limitations on supported-diagrams page (#54)
- Consolidate getting-started content and add dedicated guide (#53)
- Add RST/MyST tab-set to revealjs code samples
- Add revealjs diagram height constraint guide
- Add PyPI install instruction to docs/install.md

### Fixed

- Address code review feedback (#52)
- Refactor based on code review findings

## [0.1.0] - 2026-03-18

### Added

- Mermaid directive for embedding diagrams in Sphinx documents
- Support for 6 diagram types: flowchart, sequenceDiagram, classDiagram, stateDiagram, erDiagram, xychart-beta
- CSS variable theming with automatic dark/light detection (no re-render)
- Zero-config CDN-hosted beautiful-mermaid integration
- IntersectionObserver-based lazy rendering for sphinx-revealjs
- Pan & zoom via native Pointer Events + SVG transform (no d3.js)
- Fullscreen modal overlay
- External `.mmd` file support
- `autoclasstree` directive for Python class hierarchy diagrams

[0.1.2]: https://github.com/drillan/sphinx-oceanid/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/drillan/sphinx-oceanid/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/drillan/sphinx-oceanid/releases/tag/v0.1.0

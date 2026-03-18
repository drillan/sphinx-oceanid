# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

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

[0.1.0]: https://github.com/drillan/sphinx-oceanid/releases/tag/v0.1.0

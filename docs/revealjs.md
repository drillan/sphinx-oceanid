# sphinx-revealjs Integration

sphinx-oceanid works with [sphinx-revealjs](https://github.com/attakei/sphinx-revealjs) to embed Mermaid diagrams in presentation slides. Diagrams on hidden slides are rendered lazily — they appear when you navigate to the slide.

## Prerequisites

Install both packages:

```bash
pip install sphinx-oceanid sphinx-revealjs
```

## Configuration

Add both extensions to your `conf.py`:

```python
extensions = ["sphinx_oceanid", "sphinx_revealjs"]
```

No additional configuration is needed. sphinx-oceanid automatically detects the `revealjs` builder and enables slide-aware rendering.

## How it works

sphinx-oceanid uses two mechanisms to handle diagrams on hidden slides:

### IntersectionObserver (primary)

When the page loads, sphinx-oceanid partitions all diagrams into **visible** and **hidden** groups. Visible diagrams render immediately. Hidden diagrams (those on non-active slides) are deferred and observed with an [IntersectionObserver](https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserver). When a slide becomes visible, the observer triggers rendering.

### Reveal.js slidechanged event (secondary)

As a complementary trigger, sphinx-oceanid listens to the Reveal.js [`slidechanged`](https://revealjs.com/events/) event. On each slide transition, any unrendered diagrams that are now visible get rendered. This covers edge cases where IntersectionObserver may not fire during certain Reveal.js transitions.

### Auto-detection

When Sphinx builds with the `revealjs` builder, sphinx-oceanid sets `"revealjs": true` in the page configuration JSON. This flag activates the `slidechanged` event listener. You do not need to set this manually — it is detected from the builder name.

## Example

A minimal presentation with diagrams on two slides:

```rst
Slide 1: Architecture
=====================

.. mermaid::

   flowchart LR
     Client --> API --> Database

Slide 2: Sequence
==================

.. mermaid::

   sequenceDiagram
     Client->>API: POST /data
     API->>Database: INSERT
     Database-->>API: OK
     API-->>Client: 201 Created
```

Build with the revealjs builder:

```bash
sphinx-build -b revealjs docs docs/_build/revealjs
```

The diagram on Slide 1 renders immediately. The diagram on Slide 2 renders when you navigate to it.

## Directive options

All standard `mermaid` directive options work in revealjs slides:

```rst
Slide with zoom
================

.. mermaid::
   :caption: Class hierarchy
   :zoom:

   classDiagram
     Animal <|-- Duck
     Animal <|-- Fish
```

See {doc}`the main documentation <index>` for the full list of directive options.

## Known considerations

### Slides with `display: none`

Reveal.js hides non-active slides using CSS. The IntersectionObserver detects visibility changes when slides transition. However, if a slide is set to `display: none` through custom CSS (not Reveal.js's default mechanism), the observer may not trigger. The `slidechanged` event listener handles this case.

### Animation timing

Diagrams render when a slide becomes visible, not during the transition animation. On fast slide transitions, there may be a brief moment before the diagram appears. This is generally imperceptible for standard transition speeds.

### Theme compatibility

sphinx-oceanid's automatic dark/light theme detection works with revealjs themes. The diagram theme follows the presentation theme. See {doc}`configuration` for theme options.

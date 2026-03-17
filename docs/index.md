# sphinx-oceanid documentation

## Directive Options

The `mermaid` directive supports the following options:

### `:alt:` — Alternative text

Provides accessibility text for the diagram. Rendered as an `aria-label` attribute on the diagram container.

````rst
.. mermaid::
   :alt: Sequence diagram showing Alice greeting Bob

   sequenceDiagram
     Alice->>Bob: Hello
````

### `:caption:` — Figure caption

Wraps the diagram in an HTML `<figure>` element with a `<figcaption>`. Supports inline markup and cross-references via `:name:`.

````rst
.. mermaid::
   :caption: System architecture overview
   :name: fig-architecture

   flowchart LR
     A --> B --> C
````

### `:zoom:` — Enable zoom

Enables pan-and-zoom interaction on a specific diagram. Uses native Pointer Events + SVG transform (no d3.js).

````rst
.. mermaid::
   :zoom:

   classDiagram
     Animal <|-- Duck
````

### `:config:` — Mermaid configuration

Injects a JSON configuration object into the Mermaid frontmatter. Allows per-diagram theme and rendering options.

````rst
.. mermaid::
   :config: {"theme": "forest"}

   flowchart LR
     A --> B
````

### `:title:` — Mermaid native title

Inserts a title into the Mermaid frontmatter. Unlike `:caption:` (which renders outside the diagram as `<figcaption>`), `:title:` is rendered inside the diagram by Mermaid itself.

````rst
.. mermaid::
   :title: Processing Flow

   flowchart LR
     A --> B --> C
````

### Combined example

All options can be used together:

````rst
.. mermaid::
   :name: my-diagram
   :alt: Flow showing data processing pipeline
   :align: center
   :caption: Data Processing Pipeline
   :zoom:
   :config: {"theme": "forest"}
   :title: Pipeline Overview

   flowchart LR
     Input --> Process --> Output
````

```{toctree}
:maxdepth: 2
:caption: Contents:
```

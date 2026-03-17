# sphinx-oceanid documentation

## Usage

### Inline diagrams

Write Mermaid code directly in the directive body:

````rst
.. mermaid::

   flowchart LR
     A --> B --> C
````

```{mermaid}
flowchart LR
  A --> B --> C
```

### External files

Reference an external `.mmd` file instead of inline code. The path is relative to the Sphinx source directory.

````rst
.. mermaid:: diagrams/flow.mmd
````

All directive options work with external files:

````rst
.. mermaid:: diagrams/flow.mmd
   :caption: System architecture
   :zoom:
````

If the file is not found, the build produces an error with the file path and source location.

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

```{mermaid}
:alt: Sequence diagram showing Alice greeting Bob

sequenceDiagram
  Alice->>Bob: Hello
```

### `:caption:` — Figure caption

Wraps the diagram in an HTML `<figure>` element with a `<figcaption>`. Supports inline markup and cross-references via `:name:`.

````rst
.. mermaid::
   :caption: System architecture overview
   :name: fig-architecture

   flowchart LR
     A --> B --> C
````

```{mermaid}
:caption: System architecture overview
:name: fig-architecture-demo

flowchart LR
  A --> B --> C
```

### `:zoom:` — Enable zoom

Enables pan-and-zoom interaction on a specific diagram. Uses native Pointer Events + SVG transform (no d3.js).

````rst
.. mermaid::
   :zoom:

   classDiagram
     Animal <|-- Duck
````

```{mermaid}
:zoom:

classDiagram
  Animal <|-- Duck
```

### `:config:` — Mermaid configuration

Injects a JSON configuration object into the Mermaid frontmatter. Allows per-diagram theme and rendering options.

````rst
.. mermaid::
   :config: {"theme": "forest"}

   flowchart LR
     A --> B
````

```{mermaid}
:config: {"theme": "forest"}

flowchart LR
  A --> B
```

### `:title:` — Mermaid native title

Inserts a title into the Mermaid frontmatter. Unlike `:caption:` (which renders outside the diagram as `<figcaption>`), `:title:` is rendered inside the diagram by Mermaid itself.

````rst
.. mermaid::
   :title: Processing Flow

   flowchart LR
     A --> B --> C
````

```{mermaid}
:title: Processing Flow

flowchart LR
  A --> B --> C
```

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

```{mermaid}
:name: my-diagram-demo
:alt: Flow showing data processing pipeline
:align: center
:caption: Data Processing Pipeline
:zoom:
:config: {"theme": "forest"}
:title: Pipeline Overview

flowchart LR
  Input --> Process --> Output
```

## Auto-generated Class Diagrams

The `autoclasstree` directive generates Mermaid class diagrams from Python class hierarchies automatically.

### Basic usage

Specify one or more fully qualified class or module names as arguments:

````rst
.. autoclasstree:: mypackage.MyClass
````

This generates a `classDiagram` showing the direct inheritance relationships of `MyClass`.

### Options

#### `:full:` — Full hierarchy

Traverse the full inheritance tree up to (but excluding) `object`:

````rst
.. autoclasstree:: mypackage.MyClass
   :full:
````

#### `:strict:` — Strict module filtering

Only include classes defined in the specified module (exclude re-exported classes):

````rst
.. autoclasstree:: mypackage.models
   :strict:
````

#### `:namespace:` — Namespace filtering

Only include base classes whose module starts with the given namespace:

````rst
.. autoclasstree:: mypackage.MyClass
   :full:
   :namespace: mypackage
````

All standard `mermaid` directive options (`:name:`, `:align:`, `:caption:`, `:zoom:`, `:alt:`, `:config:`, `:title:`) are also available:

````rst
.. autoclasstree:: mypackage.MyClass
   :full:
   :caption: Class hierarchy of MyClass
   :align: center
   :zoom:
````

```{toctree}
:maxdepth: 2
:caption: Contents:

install
supported-diagrams
configuration
revealjs
troubleshooting
```

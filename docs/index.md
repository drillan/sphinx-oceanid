# sphinx-oceanid documentation

## Usage

### Inline diagrams

Write Mermaid code directly in the directive body:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::

   flowchart LR
     A --> B --> C
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
flowchart LR
  A --> B --> C
```
````
:::
::::

```{mermaid}
flowchart LR
  A --> B --> C
```

### External files

Reference an external `.mmd` file instead of inline code. The path is relative to the Sphinx source directory.

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid:: diagrams/flow.mmd
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid} diagrams/flow.mmd
```
````
:::
::::

All directive options work with external files:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid:: diagrams/flow.mmd
   :caption: System architecture
   :zoom:
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid} diagrams/flow.mmd
:caption: System architecture
:zoom:
```
````
:::
::::

If the file is not found, the build produces an error with the file path and source location.

#### Sample `.mmd` file

External `.mmd` files can include [YAML frontmatter](#yaml-frontmatter) to set the title and per-diagram configuration:

```yaml
---
title: User Authentication Flow
config:
  bg: "#1a1b26"
  fg: "#a9b1d6"
---
flowchart TD
  A[Login Page] --> B{Valid credentials?}
  B -->|Yes| C[Generate Token]
  C --> D[Dashboard]
  B -->|No| E[Show Error]
  E --> A
```

Reference the file as usual:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid:: diagrams/auth-flow.mmd
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid} diagrams/auth-flow.mmd
```
````
:::
::::

```{mermaid} diagrams/auth-flow.mmd
```

(yaml-frontmatter)=
## YAML Frontmatter

sphinx-oceanid supports [Mermaid YAML frontmatter](https://mermaid.js.org/config/frontmatter.html) for setting `title` and `config` within diagram code. The frontmatter block is delimited by `---` markers at the start of the code.

### In external `.mmd` files

This is the recommended way to use frontmatter. Place the YAML block at the top of the file:

```yaml
---
title: My Diagram
config:
  bg: "#1a1b26"
  fg: "#a9b1d6"
---
flowchart TD
  A --> B
```

### In RST inline content

Frontmatter can also be written directly in the directive body:

````rst
.. mermaid::

   ---
   title: My Diagram
   config:
     bg: "#1a1b26"
   ---
   flowchart TD
     A --> B
````

### In MyST Markdown

In MyST, the `---` block inside `` ```{mermaid} `` is interpreted as [directive options](https://myst-parser.readthedocs.io/en/latest/syntax/directives.html), not as Mermaid frontmatter. Use `title` and `config` as directive options:

````markdown
```{mermaid}
---
title: My Diagram
config: {"bg": "#1a1b26", "fg": "#a9b1d6"}
---
flowchart TD
  A --> B
```
````

```{note}
In MyST, the `config` value must be a JSON string on a single line because MyST's option parser does not preserve nested YAML structure. This is the same limitation as [sphinxcontrib-mermaid](https://github.com/mgaitan/sphinxcontrib-mermaid).
```

### Precedence

Directive options (`:title:`, `:config:`) take precedence over frontmatter values. This allows overriding frontmatter in external files without editing the file itself.

```{note}
sphinx-oceanid uses [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) as its rendering engine, which has its own color system based on `RenderOptions`. The following `config` keys are applied as per-diagram rendering overrides:

`bg`, `fg`, `line`, `accent`, `muted`, `surface`, `border`, `font`, `padding`, `nodeSpacing`, `layerSpacing`, `componentSpacing`, `transparent`, `interactive`

Standard Mermaid.js configuration keys such as `theme`, `look`, and `themeVariables` are not supported by beautiful-mermaid and will be silently ignored.
```

## Directive Options

The `mermaid` directive supports the following options:

### `:alt:` — Alternative text

Provides accessibility text for the diagram. Rendered as an `aria-label` attribute on the diagram container.

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::
   :alt: Sequence diagram showing Alice greeting Bob

   sequenceDiagram
     Alice->>Bob: Hello
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
:alt: Sequence diagram showing Alice greeting Bob

sequenceDiagram
  Alice->>Bob: Hello
```
````
:::
::::

```{mermaid}
:alt: Sequence diagram showing Alice greeting Bob

sequenceDiagram
  Alice->>Bob: Hello
```

### `:caption:` — Figure caption

Wraps the diagram in an HTML `<figure>` element with a `<figcaption>`. Supports inline markup and cross-references via `:name:`.

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::
   :caption: System architecture overview
   :name: fig-architecture

   flowchart LR
     A --> B --> C
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
:caption: System architecture overview
:name: fig-architecture-demo

flowchart LR
  A --> B --> C
```
````
:::
::::

```{mermaid}
:caption: System architecture overview
:name: fig-architecture-demo

flowchart LR
  A --> B --> C
```

### `:zoom:` — Enable zoom

Enables pan-and-zoom interaction on a specific diagram. Uses native Pointer Events + SVG transform (no d3.js).

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::
   :zoom:

   classDiagram
     Animal <|-- Duck
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
:zoom:

classDiagram
  Animal <|-- Duck
```
````
:::
::::

```{mermaid}
:zoom:

classDiagram
  Animal <|-- Duck
```

### `:config:` — Mermaid configuration

Passes a JSON configuration object as per-diagram Mermaid settings. Stored as a `data-oceanid-config` attribute on the diagram container.

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::
   :config: {"theme": "forest"}

   flowchart LR
     A --> B
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
:config: {"theme": "forest"}

flowchart LR
  A --> B
```
````
:::
::::

```{mermaid}
:config: {"theme": "forest"}

flowchart LR
  A --> B
```

### `:title:` — Diagram title

Sets a title displayed above the rendered diagram. Stored as a `data-oceanid-title` attribute on the diagram container. Unlike `:caption:` (which wraps the diagram in a `<figure>` with `<figcaption>`), `:title:` renders as a heading directly above the SVG.

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::
   :title: Processing Flow

   flowchart LR
     A --> B --> C
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
:title: Processing Flow

flowchart LR
  A --> B --> C
```
````
:::
::::

```{mermaid}
:title: Processing Flow

flowchart LR
  A --> B --> C
```

### Combined example

All options can be used together:

::::{tab-set}
:::{tab-item} RST
:sync: rst
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
:::
:::{tab-item} MyST
:sync: myst
````markdown
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
````
:::
::::

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

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. autoclasstree:: mypackage.MyClass
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{autoclasstree} mypackage.MyClass
```
````
:::
::::

This generates a `classDiagram` showing the direct inheritance relationships of `MyClass`.

### Options

#### `:full:` — Full hierarchy

Traverse the full inheritance tree up to (but excluding) `object`:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. autoclasstree:: mypackage.MyClass
   :full:
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{autoclasstree} mypackage.MyClass
:full:
```
````
:::
::::

#### `:strict:` — Strict module filtering

Only include classes defined in the specified module (exclude re-exported classes):

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. autoclasstree:: mypackage.models
   :strict:
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{autoclasstree} mypackage.models
:strict:
```
````
:::
::::

#### `:namespace:` — Namespace filtering

Only include base classes whose module starts with the given namespace:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. autoclasstree:: mypackage.MyClass
   :full:
   :namespace: mypackage
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{autoclasstree} mypackage.MyClass
:full:
:namespace: mypackage
```
````
:::
::::

All standard `mermaid` directive options (`:name:`, `:align:`, `:caption:`, `:zoom:`, `:alt:`, `:config:`, `:title:`) are also available:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. autoclasstree:: mypackage.MyClass
   :full:
   :caption: Class hierarchy of MyClass
   :align: center
   :zoom:
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{autoclasstree} mypackage.MyClass
:full:
:caption: Class hierarchy of MyClass
:align: center
:zoom:
```
````
:::
::::

```{toctree}
:maxdepth: 2
:caption: Contents:

getting-started
install
supported-diagrams
configuration
revealjs
troubleshooting
```

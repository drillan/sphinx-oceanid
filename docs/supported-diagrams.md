(supported-diagram-types)=
# Supported Diagram Types

sphinx-oceanid uses [beautiful-mermaid](https://github.com/niccolozy/beautiful-mermaid) (an ELK.js-based rendering engine) instead of standard Mermaid.js. beautiful-mermaid supports 6 diagram types with high-quality layout. Standard Mermaid.js supports 20+ types, so diagrams outside these 6 types are not rendered.

## Supported types

| Type | Alias | Description |
|------|-------|-------------|
| `flowchart` | `graph` | Flow charts and directed graphs |
| `sequenceDiagram` | | Interaction between processes over time |
| `classDiagram` | | UML class diagrams |
| `stateDiagram` | `stateDiagram-v2` | State machine diagrams |
| `erDiagram` | | Entity-relationship diagrams |
| `xychart-beta` | | XY charts (bar, line) |

## Examples

### flowchart / graph

````rst
.. mermaid::

   flowchart LR
     A[Start] --> B{Decision}
     B -->|Yes| C[OK]
     B -->|No| D[Cancel]
````

```{mermaid}
flowchart LR
  A[Start] --> B{Decision}
  B -->|Yes| C[OK]
  B -->|No| D[Cancel]
```

The `graph` keyword is an alias for `flowchart`:

````rst
.. mermaid::

   graph TD
     A --> B
     B --> C
````

```{mermaid}
graph TD
  A --> B
  B --> C
```

### sequenceDiagram

````rst
.. mermaid::

   sequenceDiagram
     participant Alice
     participant Bob
     Alice->>Bob: Hello Bob
     Bob-->>Alice: Hi Alice
     Alice->>Bob: How are you?
     Bob-->>Alice: Fine, thanks!
````

```{mermaid}
sequenceDiagram
  participant Alice
  participant Bob
  Alice->>Bob: Hello Bob
  Bob-->>Alice: Hi Alice
  Alice->>Bob: How are you?
  Bob-->>Alice: Fine, thanks!
```

### classDiagram

````rst
.. mermaid::

   classDiagram
     Animal <|-- Duck
     Animal <|-- Fish
     Animal : +String name
     Animal : +move()
     Duck : +swim()
     Fish : +swim()
````

```{mermaid}
classDiagram
  Animal <|-- Duck
  Animal <|-- Fish
  Animal : +String name
  Animal : +move()
  Duck : +swim()
  Fish : +swim()
```

You can also auto-generate class diagrams from Python code using the `autoclasstree` directive. See {doc}`index` for details.

### stateDiagram / stateDiagram-v2

````rst
.. mermaid::

   stateDiagram-v2
     [*] --> Active
     Active --> Inactive : timeout
     Inactive --> Active : input
     Active --> [*] : quit
````

```{mermaid}
stateDiagram-v2
  [*] --> Active
  Active --> Inactive : timeout
  Inactive --> Active : input
  Active --> [*] : quit
```

Both `stateDiagram` and `stateDiagram-v2` keywords are supported.

### erDiagram

````rst
.. mermaid::

   erDiagram
     CUSTOMER ||--o{ ORDER : places
     ORDER ||--|{ LINE-ITEM : contains
     PRODUCT ||--o{ LINE-ITEM : "is in"
````

```{mermaid}
erDiagram
  CUSTOMER ||--o{ ORDER : places
  ORDER ||--|{ LINE-ITEM : contains
  PRODUCT ||--o{ LINE-ITEM : "is in"
```

### xychart-beta

````rst
.. mermaid::

   xychart-beta
     title "Monthly Sales"
     x-axis [Jan, Feb, Mar, Apr, May]
     y-axis "Revenue (USD)" 0 --> 5000
     bar [1200, 2400, 1800, 3600, 4200]
     line [1200, 2400, 1800, 3600, 4200]
````

```{mermaid}
xychart-beta
  title "Monthly Sales"
  x-axis [Jan, Feb, Mar, Apr, May]
  y-axis "Revenue (USD)" 0 --> 5000
  bar [1200, 2400, 1800, 3600, 4200]
  line [1200, 2400, 1800, 3600, 4200]
```

## Unsupported diagram types

The following Mermaid diagram types are **not supported** by beautiful-mermaid and cannot be rendered by sphinx-oceanid:

| Type | Description |
|------|-------------|
| `gantt` | Gantt charts |
| `pie` | Pie charts |
| `gitGraph` | Git branch/commit graphs |
| `journey` | User journey maps |
| `mindmap` | Mind maps |
| `timeline` | Timeline diagrams |
| `sankey-beta` | Sankey diagrams |
| `quadrantChart` | Quadrant charts |
| `requirementDiagram` | Requirement diagrams |
| `C4Context` | C4 context diagrams |
| `C4Container` | C4 container diagrams |
| `C4Component` | C4 component diagrams |
| `C4Deployment` | C4 deployment diagrams |
| `block-beta` | Block diagrams |
| `packet-beta` | Packet diagrams |
| `kanban` | Kanban boards |
| `architecture-beta` | Architecture diagrams |
| `zenuml` | ZenUML sequence diagrams |

## Behavior with unsupported types

When sphinx-oceanid encounters an unsupported diagram type, the behavior depends on the {ref}`oceanid_unsupported_action <conf-oceanid-unsupported-action>` configuration:

### `"warning"` (default)

- Sphinx outputs a **warning** message during the build, listing the unsupported type and the supported types
- The build **continues**
- In the output HTML, the diagram is replaced with an error message box showing:
  - The unsupported type name
  - The list of supported types
  - The original Mermaid source code

```html
<div class="oceanid-unsupported">
  <p class="oceanid-unsupported-message">
    Diagram type "gantt" is not supported by sphinx-oceanid.
    Supported types: flowchart, graph, sequenceDiagram, classDiagram,
    stateDiagram, stateDiagram-v2, erDiagram, xychart-beta.
  </p>
  <pre class="oceanid-unsupported-code">gantt
    title Project
    ...</pre>
</div>
```

### `"error"`

- Sphinx **raises an error** and the build fails immediately

```python
# conf.py
oceanid_unsupported_action = "error"
```

sphinx-oceanid **never** silently degrades or falls back to standard Mermaid.js. Unsupported diagrams always produce explicit feedback.

## Limitations

### beautiful-mermaid limitations

- **6 diagram types only**: beautiful-mermaid renders 6 types (listed above) vs 20+ types in standard Mermaid.js. This is a design choice for high-quality ELK.js-based layout
- **No server-side rendering**: beautiful-mermaid is a client-side JavaScript library. Diagrams require a browser to render. LaTeX/PDF output is not supported
- **Silent failure on some syntax errors**: beautiful-mermaid may render an incomplete diagram without raising an error if the Mermaid code contains certain syntax errors. Always verify your diagrams visually after building

### sphinx-oceanid limitations

- **HTML output only**: sphinx-oceanid produces HTML output. Other Sphinx builders (LaTeX, epub) are not supported
- **JavaScript required**: Diagrams are rendered client-side. The `<noscript>` element shows the raw Mermaid source code when JavaScript is disabled

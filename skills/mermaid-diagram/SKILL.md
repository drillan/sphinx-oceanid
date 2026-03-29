---
name: mermaid-diagram
description: >
  Write Mermaid diagrams in Sphinx documentation using sphinx-oceanid.
  Supports both MyST Markdown (.md) and reStructuredText (.rst) syntax.
  Prevents common mistakes like using unsupported diagram types.

  MUST trigger when:
  - Editing or creating .md or .rst files under docs/ in a project where
    docs/conf.py contains sphinx_oceanid in the extensions list
  - User asks to add a diagram, flowchart, sequence diagram, class diagram,
    state diagram, ER diagram, or chart to documentation
  - User mentions 'mermaid', 'diagram', or wants to visualize architecture,
    workflows, data flows, class hierarchies, or state machines in their docs

  SHOULD trigger proactively when:
  - Writing documentation that describes processes, workflows, or step-by-step
    flows (suggest flowchart)
  - Writing documentation that describes component interactions or API calls
    (suggest sequenceDiagram)
  - Writing documentation that describes class hierarchies or module
    relationships (suggest classDiagram)
  - Writing documentation that describes state transitions or lifecycles
    (suggest stateDiagram)
  - Writing documentation that describes data models or entity relationships
    (suggest erDiagram)
  - Writing documentation that describes numeric data, comparisons, or trends
    (suggest xychart-beta)
---

# Mermaid Diagrams with sphinx-oceanid

This project uses [sphinx-oceanid](https://github.com/drillan/sphinx-oceanid/) to render Mermaid diagrams in Sphinx documentation. sphinx-oceanid uses the beautiful-mermaid rendering engine (ELK.js layout), which produces high-quality SVG output but only supports a specific set of diagram types.

## Supported Diagram Types

Only these 6 types are supported. Using any other type causes a build warning or error:

| Type | Alias | Use Case |
|------|-------|----------|
| `flowchart` | `graph` | Workflows, decision trees, data pipelines |
| `sequenceDiagram` | — | API interactions, message flows between components |
| `classDiagram` | — | Class hierarchies, module relationships |
| `stateDiagram` | `stateDiagram-v2` | State machines, lifecycle transitions |
| `erDiagram` | — | Data models, entity relationships |
| `xychart-beta` | — | Bar charts, line charts with numeric axes |

**Not supported** (will produce errors): gantt, pie, gitGraph, journey, mindmap, timeline, sankey-beta, quadrantChart, block-beta, kanban, architecture-beta, and others. If a user needs one of these, explain the limitation and suggest an alternative from the supported types or a different approach (e.g., a table, an image).

## Syntax (MyST Markdown)

This project uses MyST (Markdown) for documentation. Use the `{mermaid}` directive:

````markdown
```{mermaid}
flowchart LR
  A[Input] --> B[Process] --> C[Output]
```
````

### With Options

````markdown
```{mermaid}
:caption: System Architecture
:alt: Architecture diagram showing data flow
:align: center
:zoom:

flowchart TD
  API[API Server] --> DB[(Database)]
  API --> Cache[Redis Cache]
```
````

### External .mmd File

````markdown
```{mermaid} diagrams/architecture.mmd
:caption: Full Architecture
:zoom:
```
````

The path is relative to the Sphinx source directory (`docs/`). The `.mmd` file contains only the Mermaid code (no directive syntax).

## Directive Options

| Option | Type | Description |
|--------|------|-------------|
| `:caption:` | text | Rendered as `<figcaption>` below the diagram |
| `:alt:` | text | Accessibility text (`aria-label`) |
| `:align:` | `left` / `center` / `right` | Horizontal alignment |
| `:zoom:` | flag (no value) | Enable mouse wheel zoom and drag pan |
| `:name:` | text | Unique ID for cross-references |
| `:title:` | text | Mermaid-native title (inside diagram) |
| `:config:` | JSON | Per-diagram Mermaid config override |

## Diagram Examples

### Flowchart — Data Pipeline

````markdown
```{mermaid}
:caption: Market Data Pipeline
:align: center

flowchart LR
  Fetch[Fetch OHLCV] --> Clean[Clean & Validate]
  Clean --> Store[(Parquet Store)]
  Store --> Analyze[Analysis Engine]
  Analyze --> Report[Generate Report]
```
````

### Sequence Diagram — API Call

````markdown
```{mermaid}
:caption: Quote Retrieval Flow
:align: center

sequenceDiagram
  participant C as Client
  participant A as API
  participant D as Database
  C->>A: Request quotes
  A->>D: Query Parquet
  D-->>A: Return data
  A-->>C: JSON response
```
````

### State Diagram — Order Lifecycle

````markdown
```{mermaid}
:caption: Order State Machine

stateDiagram-v2
  [*] --> Pending
  Pending --> Submitted: Place order
  Submitted --> Filled: Execution
  Submitted --> Cancelled: Cancel
  Filled --> [*]
  Cancelled --> [*]
```
````

### ER Diagram — Data Model

````markdown
```{mermaid}
:caption: Market Data Schema

erDiagram
  COMMODITY ||--o{ QUOTE : has
  COMMODITY {
    string code PK
    string name
    string exchange
  }
  QUOTE {
    date date PK
    float open
    float high
    float low
    float close
    int volume
  }
```
````

### XY Chart — Performance

````markdown
```{mermaid}
:caption: Monthly Returns

xychart-beta
  title "Strategy Monthly Returns (%)"
  x-axis [Jan, Feb, Mar, Apr, May, Jun]
  y-axis "Return (%)" -5 --> 10
  bar [2.1, -1.3, 4.5, 3.2, -0.8, 5.1]
  line [1.0, 0.5, 2.0, 2.5, 1.5, 3.0]
```
````

### Class Diagram — Module Structure

````markdown
```{mermaid}
:caption: Analysis Module Hierarchy

classDiagram
  class BaseAnalyzer {
    +load_data()
    +validate()
    +analyze()*
  }
  class QuotesAnalyzer {
    +analyze()
    +calc_ohlcv()
  }
  class TicksAnalyzer {
    +analyze()
    +calc_vwap()
  }
  BaseAnalyzer <|-- QuotesAnalyzer
  BaseAnalyzer <|-- TicksAnalyzer
```
````

## Auto Class Diagrams

Generate class hierarchy diagrams automatically from Python code:

````markdown
```{autoclasstree} market_analysis.QuotesAnalyzer
:full:
:namespace: market_analysis
:caption: QuotesAnalyzer class hierarchy
:zoom:
```
````

| Option | Description |
|--------|-------------|
| `:full:` | Traverse full inheritance tree (up to `object`) |
| `:strict:` | Only classes defined in the specified module |
| `:namespace:` | Filter base classes by this namespace prefix |

## conf.py Configuration

The current project has `sphinx_oceanid` in extensions. Additional settings can be added to `docs/conf.py`:

```python
# Theme auto-detects dark/light from Shibuya theme (default: "auto")
oceanid_theme = "auto"

# Enable zoom on all diagrams globally (default: False)
oceanid_zoom = True

# Enable fullscreen modal button (default: False)
oceanid_fullscreen = True

# Action for unsupported diagram types: "warning" or "error" (default: "warning")
oceanid_unsupported_action = "warning"
```

## Best Practices

- **Always verify the diagram type is supported** before writing. The 6 supported types cover most visualization needs.
- **Use `:caption:` and `:alt:`** for accessibility and context.
- **Use `:zoom:` for complex diagrams** — especially flowcharts with many nodes or detailed ER diagrams.
- **Prefer inline code over .mmd files** for small diagrams (under ~20 lines). Use external `.mmd` files for large, reusable diagrams.
- **Build and preview** after adding diagrams: `uv run make -C docs html` then serve with a local HTTP server (Mermaid requires HTTP, not `file://`).
- **Keep diagrams focused** — split large diagrams into smaller, focused ones rather than one monolithic diagram.

(supported-diagram-types)=
# Supported Diagram Types

sphinx-oceanid uses [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) (an ELK.js-based rendering engine) instead of standard Mermaid.js. beautiful-mermaid supports 6 diagram types with high-quality layout. Standard Mermaid.js supports 20+ types, so diagrams outside these 6 types are not rendered.

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

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::

   flowchart LR
     A[Start] --> B{Decision}
     B -->|Yes| C[OK]
     B -->|No| D[Cancel]
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
flowchart LR
  A[Start] --> B{Decision}
  B -->|Yes| C[OK]
  B -->|No| D[Cancel]
```
````
:::
::::

```{mermaid}
flowchart LR
  A[Start] --> B{Decision}
  B -->|Yes| C[OK]
  B -->|No| D[Cancel]
```

```{note}
**Known limitations**

- `click` events are not supported
- Bidirectional arrow (`<-->`) has an SVG rendering bug ([beautiful-mermaid#58](https://github.com/lukilabs/beautiful-mermaid/issues/58))
```

The `graph` keyword is an alias for `flowchart`:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::

   graph TD
     A --> B
     B --> C
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
graph TD
  A --> B
  B --> C
```
````
:::
::::

```{mermaid}
graph TD
  A --> B
  B --> C
```

#### Subgraphs

Nested subgraphs with `direction` override:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::

   flowchart TB
     subgraph Frontend
       direction LR
       A[Browser] --> B[React App]
     end
     subgraph Backend
       direction LR
       C[API Server] --> D[(Database)]
     end
     Frontend --> Backend
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
flowchart TB
  subgraph Frontend
    direction LR
    A[Browser] --> B[React App]
  end
  subgraph Backend
    direction LR
    C[API Server] --> D[(Database)]
  end
  Frontend --> Backend
```
````
:::
::::

```{mermaid}
flowchart TB
  subgraph Frontend
    direction LR
    A[Browser] --> B[React App]
  end
  subgraph Backend
    direction LR
    C[API Server] --> D[(Database)]
  end
  Frontend --> Backend
```

#### Node shapes, edge styles, and classDef

Various node shapes, edge styles (dotted `-.->`, thick `==>`), and `classDef` styling:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::

   flowchart LR
     classDef accent fill:#f9f,stroke:#333
     A([Terminal]) ==> B{Diamond}
     B -.->|Option 1| C[(Cylinder)]
     B -->|Option 2| D{{Hexagon}}
     A & B --> E((Circle))
     class A accent
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
flowchart LR
  classDef accent fill:#f9f,stroke:#333
  A([Terminal]) ==> B{Diamond}
  B -.->|Option 1| C[(Cylinder)]
  B -->|Option 2| D{{Hexagon}}
  A & B --> E((Circle))
  class A accent
```
````
:::
::::

```{mermaid}
flowchart LR
  classDef accent fill:#f9f,stroke:#333
  A([Terminal]) ==> B{Diamond}
  B -.->|Option 1| C[(Cylinder)]
  B -->|Option 2| D{{Hexagon}}
  A & B --> E((Circle))
  class A accent
```

### sequenceDiagram

::::{tab-set}
:::{tab-item} RST
:sync: rst
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
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
sequenceDiagram
  participant Alice
  participant Bob
  Alice->>Bob: Hello Bob
  Bob-->>Alice: Hi Alice
  Alice->>Bob: How are you?
  Bob-->>Alice: Fine, thanks!
```
````
:::
::::

```{mermaid}
sequenceDiagram
  participant Alice
  participant Bob
  Alice->>Bob: Hello Bob
  Bob-->>Alice: Hi Alice
  Alice->>Bob: How are you?
  Bob-->>Alice: Fine, thanks!
```

#### TCP handshake and connection lifecycle

`participant` aliases, activation via `+`/`-` shorthand, `Note`, `loop`, and `alt`/`else` blocks — modeled on TCP 3-way handshake, data transfer, and connection teardown:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::

   sequenceDiagram
     participant C as Client
     participant S as Server
     Note over C, S: 3-way handshake
     C ->>+ S: SYN
     S -->>- C: SYN-ACK
     C ->> S: ACK
     loop Data transfer
       C ->>+ S: Request
       alt Success
         S -->>- C: 200 OK
       else Error
         S -->> C: 500
       end
     end
     Note over C, S: Connection teardown
     C ->> S: FIN
     S -->> C: FIN-ACK
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
sequenceDiagram
  participant C as Client
  participant S as Server
  Note over C, S: 3-way handshake
  C ->>+ S: SYN
  S -->>- C: SYN-ACK
  C ->> S: ACK
  loop Data transfer
    C ->>+ S: Request
    alt Success
      S -->>- C: 200 OK
    else Error
      S -->> C: 500
    end
  end
  Note over C, S: Connection teardown
  C ->> S: FIN
  S -->> C: FIN-ACK
```
````
:::
::::

```{mermaid}
sequenceDiagram
  participant C as Client
  participant S as Server
  Note over C, S: 3-way handshake
  C ->>+ S: SYN
  S -->>- C: SYN-ACK
  C ->> S: ACK
  loop Data transfer
    C ->>+ S: Request
    alt Success
      S -->>- C: 200 OK
    else Error
      S -->> C: 500
    end
  end
  Note over C, S: Connection teardown
  C ->> S: FIN
  S -->> C: FIN-ACK
```

```{note}
**Known limitations**

- `autonumber` is not supported
- `box` groups are not supported
- `create` / `destroy` (dynamic actor lifecycle) are not supported
- Explicit `activate` / `deactivate` commands are not supported (`+`/`-` shorthand only)
- A note placed before the first message is silently dropped ([beautiful-mermaid#53](https://github.com/lukilabs/beautiful-mermaid/issues/53))
```

### classDiagram

::::{tab-set}
:::{tab-item} RST
:sync: rst
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
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
classDiagram
  Animal <|-- Duck
  Animal <|-- Fish
  Animal : +String name
  Animal : +move()
  Duck : +swim()
  Fish : +swim()
```
````
:::
::::

```{mermaid}
classDiagram
  Animal <|-- Duck
  Animal <|-- Fish
  Animal : +String name
  Animal : +move()
  Duck : +swim()
  Fish : +swim()
```

#### Class blocks, annotations, relationships, and generics

Class blocks with visibility markers, `<<abstract>>` annotation, generics (`~T~`), and multiple relationship types with cardinality:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::

   classDiagram
     class Animal {
       <<abstract>>
       +String name
       +move()* void
     }
     class List~T~ {
       +get(index int) T
     }
     Animal <|-- Duck
     Animal *-- "1" Heart
     Duck ..|> Swimmable
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
classDiagram
  class Animal {
    <<abstract>>
    +String name
    +move()* void
  }
  class List~T~ {
    +get(index int) T
  }
  Animal <|-- Duck
  Animal *-- "1" Heart
  Duck ..|> Swimmable
```
````
:::
::::

```{mermaid}
classDiagram
  class Animal {
    <<abstract>>
    +String name
    +move()* void
  }
  class List~T~ {
    +get(index int) T
  }
  Animal <|-- Duck
  Animal *-- "1" Heart
  Duck ..|> Swimmable
```

#### Auto-generated from Python code

The `autoclasstree` directive generates class diagrams from Python class hierarchies automatically. This example visualizes the Sphinx role class hierarchy:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. autoclasstree:: sphinx.roles
   :strict:
   :caption: Sphinx role class hierarchy
   :zoom:
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{autoclasstree} sphinx.roles
:strict:
:caption: Sphinx role class hierarchy
:zoom:
```
````
:::
::::

```{autoclasstree} sphinx.roles
:strict:
:caption: Sphinx role class hierarchy
:zoom:
```

See {doc}`index` for full `autoclasstree` options (`:full:`, `:strict:`, `:namespace:`).

```{note}
**Known limitations**

- `click` / `note` / `link` are not supported
- `classDef` assignments are not reflected in SVG output ([beautiful-mermaid#80](https://github.com/lukilabs/beautiful-mermaid/issues/80))
```

### stateDiagram / stateDiagram-v2

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::

   stateDiagram-v2
     [*] --> Active
     Active --> Inactive : timeout
     Inactive --> Active : input
     Active --> [*] : quit
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
stateDiagram-v2
  [*] --> Active
  Active --> Inactive : timeout
  Inactive --> Active : input
  Active --> [*] : quit
```
````
:::
::::

```{mermaid}
stateDiagram-v2
  [*] --> Active
  Active --> Inactive : timeout
  Inactive --> Active : input
  Active --> [*] : quit
```

#### Composite states and aliases

Composite (nested) states with `direction` override, and state aliases using `state "Description" as id`:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::

   stateDiagram-v2
     state "Waiting for input" as waiting
     state Active {
       direction LR
       [*] --> Running
       Running --> Paused : pause
       Paused --> Running : resume
     }
     [*] --> waiting
     waiting --> Active : start
     Active --> [*] : stop
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
stateDiagram-v2
  state "Waiting for input" as waiting
  state Active {
    direction LR
    [*] --> Running
    Running --> Paused : pause
    Paused --> Running : resume
  }
  [*] --> waiting
  waiting --> Active : start
  Active --> [*] : stop
```
````
:::
::::

```{mermaid}
stateDiagram-v2
  state "Waiting for input" as waiting
  state Active {
    direction LR
    [*] --> Running
    Running --> Paused : pause
    Paused --> Running : resume
  }
  [*] --> waiting
  waiting --> Active : start
  Active --> [*] : stop
```

Both `stateDiagram` and `stateDiagram-v2` keywords are supported.

```{note}
**Known limitations**

- `<<fork>>` / `<<join>>` / `<<choice>>` pseudo-states are not supported
- Concurrent states (`--` separator) are not supported
- `note` is not supported
```

### erDiagram

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::

   erDiagram
     CUSTOMER ||--o{ ORDER : places
     ORDER ||--|{ LINE-ITEM : contains
     PRODUCT ||--o{ LINE-ITEM : "is in"
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
erDiagram
  CUSTOMER ||--o{ ORDER : places
  ORDER ||--|{ LINE-ITEM : contains
  PRODUCT ||--o{ LINE-ITEM : "is in"
```
````
:::
::::

```{mermaid}
erDiagram
  CUSTOMER ||--o{ ORDER : places
  ORDER ||--|{ LINE-ITEM : contains
  PRODUCT ||--o{ LINE-ITEM : "is in"
```

#### Entity attributes and relationship styles

Entity blocks with typed attributes (`PK`, `FK`, `UK` markers), all four cardinality types, and identifying (`--`) vs non-identifying (`..`) relationships:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::

   erDiagram
     CUSTOMER {
       int id PK
       string name
       string email UK
     }
     ORDER {
       int id PK
       int customer_id FK
     }
     CUSTOMER ||--o{ ORDER : places
     CUSTOMER |o..o| ADDRESS : "lives at"
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
erDiagram
  CUSTOMER {
    int id PK
    string name
    string email UK
  }
  ORDER {
    int id PK
    int customer_id FK
  }
  CUSTOMER ||--o{ ORDER : places
  CUSTOMER |o..o| ADDRESS : "lives at"
```
````
:::
::::

```{mermaid}
erDiagram
  CUSTOMER {
    int id PK
    string name
    string email UK
  }
  ORDER {
    int id PK
    int customer_id FK
  }
  CUSTOMER ||--o{ ORDER : places
  CUSTOMER |o..o| ADDRESS : "lives at"
```

```{note}
**Known limitations**

- Entity aliases (`CUSTOMER["Customer"]`) are not supported
```

### xychart-beta

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::

   xychart-beta
     title "Monthly Sales"
     x-axis [Jan, Feb, Mar, Apr, May]
     y-axis "Revenue (USD)" 0 --> 5000
     bar [1200, 2400, 1800, 3600, 4200]
     line [1200, 2400, 1800, 3600, 4200]
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
xychart-beta
  title "Monthly Sales"
  x-axis [Jan, Feb, Mar, Apr, May]
  y-axis "Revenue (USD)" 0 --> 5000
  bar [1200, 2400, 1800, 3600, 4200]
  line [1200, 2400, 1800, 3600, 4200]
```
````
:::
::::

```{mermaid}
xychart-beta
  title "Monthly Sales"
  x-axis [Jan, Feb, Mar, Apr, May]
  y-axis "Revenue (USD)" 0 --> 5000
  bar [1200, 2400, 1800, 3600, 4200]
  line [1200, 2400, 1800, 3600, 4200]
```

#### Numeric x-axis and horizontal orientation

Numeric x-axis range, axis titles, and `horizontal` orientation with multiple series:

::::{tab-set}
:::{tab-item} RST
:sync: rst
````rst
.. mermaid::

   xychart-beta horizontal
     title "Score by Iteration"
     x-axis "Iteration" 1 --> 5
     y-axis "Score" 0 --> 100
     bar [45, 62, 78, 85, 92]
     line [40, 58, 73, 82, 90]
````
:::
:::{tab-item} MyST
:sync: myst
````markdown
```{mermaid}
xychart-beta horizontal
  title "Score by Iteration"
  x-axis "Iteration" 1 --> 5
  y-axis "Score" 0 --> 100
  bar [45, 62, 78, 85, 92]
  line [40, 58, 73, 82, 90]
```
````
:::
::::

```{mermaid}
xychart-beta horizontal
  title "Score by Iteration"
  x-axis "Iteration" 1 --> 5
  y-axis "Score" 0 --> 100
  bar [45, 62, 78, 85, 92]
  line [40, 58, 73, 82, 90]
```

```{note}
**Known limitations**

- Named series labels are not supported (minor)
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

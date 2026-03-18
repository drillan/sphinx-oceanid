# sphinx-oceanid

Mermaid diagrams powered by beautiful-mermaid

## Flowchart

```{mermaid}
flowchart LR
  A[Start] --> B{Decision}
  B -->|Yes| C[OK]
  B -->|No| D[Cancel]
```

## Sequence Diagram

```{mermaid}
sequenceDiagram
  participant Alice
  participant Bob
  Alice->>Bob: Hello Bob
  Bob-->>Alice: Hi Alice
  Alice->>Bob: How are you?
  Bob-->>Alice: Fine, thanks!
```

## Class Diagram

```{mermaid}
classDiagram
  Animal <|-- Duck
  Animal <|-- Fish
  Animal : +String name
  Animal : +move()
  Duck : +swim()
  Fish : +swim()
```

## State Diagram

```{mermaid}
stateDiagram-v2
  [*] --> Active
  Active --> Inactive : timeout
  Inactive --> Active : input
  Active --> [*] : quit
```

## ER Diagram

```{mermaid}
erDiagram
  CUSTOMER ||--o{ ORDER : places
  ORDER ||--|{ LINE-ITEM : contains
  PRODUCT ||--o{ LINE-ITEM : "is in"
```

## XY Chart

```{mermaid}
xychart-beta
  title "Monthly Sales"
  x-axis [Jan, Feb, Mar, Apr, May]
  y-axis "Revenue (USD)" 0 --> 5000
  bar [1200, 2400, 1800, 3600, 4200]
  line [1200, 2400, 1800, 3600, 4200]
```

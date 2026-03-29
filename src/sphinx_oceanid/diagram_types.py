"""Diagram type parsing and support detection (pure functions)."""

from __future__ import annotations

import re

SUPPORTED_DIAGRAM_TYPES: frozenset[str] = frozenset(
    {
        "flowchart",
        "graph",  # flowchart alias
        "stateDiagram",
        "stateDiagram-v2",
        "sequenceDiagram",
        "classDiagram",
        "erDiagram",
        "xychart-beta",
    }
)

_FRONTMATTER_RE = re.compile(r"^---.*?---\s*", re.DOTALL)

# All Mermaid diagram keywords (both supported and unsupported)
_DIAGRAM_TYPE_RE = re.compile(
    r"^\s*("
    r"flowchart|graph|sequenceDiagram|classDiagram|"
    r"stateDiagram(?:-v2)?|erDiagram|xychart-beta|"
    r"gantt|pie|gitGraph|journey|mindmap|timeline|"
    r"sankey-beta|quadrantChart|requirementDiagram|"
    r"C4Context|C4Container|C4Component|C4Deployment|"
    r"block-beta|packet-beta|kanban|architecture-beta|"
    r"zenuml"
    r")\b",
    re.MULTILINE,
)


def extract_diagram_type(code: str) -> str | None:
    """Extract diagram type from Mermaid code.

    Skips YAML frontmatter (---...---) if present before parsing.

    Args:
        code: Mermaid notation string.

    Returns:
        Diagram type string, or None if not recognized.
    """
    stripped = _FRONTMATTER_RE.sub("", code)
    match = _DIAGRAM_TYPE_RE.search(stripped)
    if match:
        return match.group(1)
    return None


def is_supported_diagram(diagram_type: str | None) -> bool:
    """Check whether a diagram type is supported by beautiful-mermaid.

    Args:
        diagram_type: Return value from extract_diagram_type().

    Returns:
        True if the diagram type is supported.
    """
    if diagram_type is None:
        return False
    return diagram_type in SUPPORTED_DIAGRAM_TYPES


def unsupported_diagram_message(diagram_type: str | None) -> str:
    """Build a human-readable message for an unsupported diagram type.

    Args:
        diagram_type: Diagram type string, or None if unrecognized.

    Returns:
        Formatted error message with the list of supported types.
    """
    label = diagram_type or "unknown"
    supported_list = ", ".join(sorted(SUPPORTED_DIAGRAM_TYPES))
    return f'Diagram type "{label}" is not supported by sphinx-oceanid. Supported types: {supported_list}.'

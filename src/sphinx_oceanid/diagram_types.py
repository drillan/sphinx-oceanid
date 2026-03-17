"""Diagram type parsing and support detection (pure functions)."""

from __future__ import annotations

import re

from .config import SUPPORTED_DIAGRAM_TYPES

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

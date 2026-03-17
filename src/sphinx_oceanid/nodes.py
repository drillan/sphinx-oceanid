"""Docutils node definition for Mermaid diagrams."""

from docutils import nodes


class mermaid_node(nodes.General, nodes.Element):
    """Docutils node representing a Mermaid diagram.

    Attributes:
        code: Mermaid notation string.
        diagram_type: Parsed diagram type (e.g. "flowchart", "sequenceDiagram").
        is_supported: Whether beautiful-mermaid supports this diagram type.
        align: "left" | "center" | "right".
        alt: Alternative text for accessibility.
        zoom: Whether zoom is enabled.
        zoom_id: Unique ID for the zoom element.
    """

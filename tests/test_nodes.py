"""Tests for sphinx_oceanid.nodes module."""

from docutils import nodes

from sphinx_oceanid.nodes import mermaid_node


class TestMermaidNode:
    """Tests for mermaid_node class."""

    def test_mermaid_node_creation(self) -> None:
        """mermaid_node can be instantiated with attributes."""
        node = mermaid_node(
            code="flowchart LR\n  A --> B",
            diagram_type="flowchart",
            is_supported=True,
        )
        assert node["code"] == "flowchart LR\n  A --> B"
        assert node["diagram_type"] == "flowchart"
        assert node["is_supported"] is True

    def test_mermaid_node_default_attributes(self) -> None:
        """mermaid_node has sensible defaults for optional attributes."""
        node = mermaid_node(
            code="sequenceDiagram\n  Alice->>Bob: Hello",
            diagram_type="sequenceDiagram",
            is_supported=True,
        )
        assert node.get("align") is None
        assert node.get("alt") is None
        assert node.get("zoom") is None
        assert node.get("zoom_id") is None

    def test_mermaid_node_with_all_attributes(self) -> None:
        """mermaid_node accepts all documented attributes."""
        node = mermaid_node(
            code="erDiagram\n  A ||--o{ B : has",
            diagram_type="erDiagram",
            is_supported=True,
            align="center",
            alt="ER diagram",
            zoom=True,
            zoom_id="zoom-1",
        )
        assert node["code"] == "erDiagram\n  A ||--o{ B : has"
        assert node["diagram_type"] == "erDiagram"
        assert node["is_supported"] is True
        assert node["align"] == "center"
        assert node["alt"] == "ER diagram"
        assert node["zoom"] is True
        assert node["zoom_id"] == "zoom-1"

    def test_mermaid_node_inherits_general(self) -> None:
        """mermaid_node inherits from nodes.General."""
        node = mermaid_node(code="", diagram_type=None, is_supported=False)
        assert isinstance(node, nodes.General)

    def test_mermaid_node_inherits_element(self) -> None:
        """mermaid_node inherits from nodes.Element."""
        node = mermaid_node(code="", diagram_type=None, is_supported=False)
        assert isinstance(node, nodes.Element)

"""Tests for sphinx_oceanid.diagram_types module."""

import pytest

from sphinx_oceanid.diagram_types import extract_diagram_type, is_supported_diagram


class TestExtractDiagramType:
    """Tests for extract_diagram_type function."""

    @pytest.mark.parametrize(
        ("code", "expected"),
        [
            ("flowchart LR\n  A --> B", "flowchart"),
            ("graph TD\n  A --> B", "graph"),
            ("sequenceDiagram\n  Alice->>Bob: Hello", "sequenceDiagram"),
            ("classDiagram\n  Animal <|-- Duck", "classDiagram"),
            ("stateDiagram-v2\n  [*] --> Still", "stateDiagram-v2"),
            ("stateDiagram\n  [*] --> Still", "stateDiagram"),
            ("erDiagram\n  CUSTOMER ||--o{ ORDER : places", "erDiagram"),
            ("xychart-beta\n  title My Chart", "xychart-beta"),
        ],
    )
    def test_extract_supported_diagram_types(self, code: str, expected: str) -> None:
        """Supported diagram types are correctly extracted."""
        assert extract_diagram_type(code) == expected

    @pytest.mark.parametrize(
        ("code", "expected"),
        [
            ("gantt\n  title A Gantt", "gantt"),
            ("pie\n  title Pets", "pie"),
            ("gitGraph\n  commit", "gitGraph"),
            ("mindmap\n  root((mindmap))", "mindmap"),
            ("timeline\n  title History", "timeline"),
        ],
    )
    def test_extract_unsupported_diagram_types(self, code: str, expected: str) -> None:
        """Unsupported diagram types are also correctly extracted."""
        assert extract_diagram_type(code) == expected

    def test_extract_with_frontmatter(self) -> None:
        """Diagram type is extracted after YAML frontmatter."""
        code = "---\ntitle: My Diagram\nconfig:\n  theme: dark\n---\nflowchart LR\n  A --> B"
        assert extract_diagram_type(code) == "flowchart"

    def test_extract_empty_string(self) -> None:
        """Empty string returns None."""
        assert extract_diagram_type("") is None

    def test_extract_no_diagram_type(self) -> None:
        """Unrecognized content returns None."""
        assert extract_diagram_type("not a diagram\njust some text") is None

    def test_extract_with_leading_whitespace(self) -> None:
        """Leading whitespace before diagram type is handled."""
        assert extract_diagram_type("  flowchart LR\n  A --> B") == "flowchart"

    def test_extract_with_comments(self) -> None:
        """Content that looks like a comment before diagram type."""
        code = "%% This is a comment\nsequenceDiagram\n  Alice->>Bob: Hello"
        # Comments are not diagram types, so the regex should find sequenceDiagram
        assert extract_diagram_type(code) == "sequenceDiagram"


class TestIsSupportedDiagram:
    """Tests for is_supported_diagram function."""

    @pytest.mark.parametrize(
        "diagram_type",
        [
            "flowchart",
            "graph",
            "sequenceDiagram",
            "classDiagram",
            "stateDiagram",
            "stateDiagram-v2",
            "erDiagram",
            "xychart-beta",
        ],
    )
    def test_supported_types(self, diagram_type: str) -> None:
        """All beautiful-mermaid supported types return True."""
        assert is_supported_diagram(diagram_type) is True

    def test_is_supported_none(self) -> None:
        """None input returns False."""
        assert is_supported_diagram(None) is False

    @pytest.mark.parametrize(
        "diagram_type",
        [
            "gantt",
            "pie",
            "gitGraph",
            "mindmap",
            "timeline",
            "journey",
            "sankey-beta",
        ],
    )
    def test_unsupported_types(self, diagram_type: str) -> None:
        """Unsupported diagram types return False."""
        assert is_supported_diagram(diagram_type) is False

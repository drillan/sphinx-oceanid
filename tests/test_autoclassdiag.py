"""Tests for autoclassdiag module (Layer 1: Unit tests, no Sphinx)."""

from __future__ import annotations

import pytest

from sphinx_oceanid.autoclassdiag import class_diagram, get_classes

# --- Test class hierarchies ---


class Animal:
    pass


class Mammal(Animal):
    pass


class Bird(Animal):
    pass


class Dog(Mammal):
    pass


class Cat(Mammal):
    pass


class FlyingFish(Bird, Animal):
    """Multiple inheritance test."""


class Platypus(Mammal, Bird):
    """Diamond inheritance test."""


class DeepChild(Dog):
    """Three levels deep: DeepChild -> Dog -> Mammal -> Animal."""


# --- Tests for get_classes ---


class TestGetClasses:
    """Tests for get_classes() function."""

    def test_get_classes_single_class(self) -> None:
        """Single fully qualified class name yields that class."""
        classes = list(get_classes(f"{__name__}.Animal"))
        assert classes == [Animal]

    def test_get_classes_module(self) -> None:
        """Module name yields all classes defined in that module."""
        classes = list(get_classes(__name__))
        class_names = {c.__name__ for c in classes}
        assert "Animal" in class_names
        assert "Dog" in class_names

    def test_get_classes_strict_module(self) -> None:
        """strict=True only yields classes defined in the module itself."""
        classes = list(get_classes(__name__, strict=True))
        class_names = {c.__name__ for c in classes}
        # All test classes are defined in this module
        assert "Animal" in class_names
        assert "Dog" in class_names

    def test_get_classes_not_found_raises(self) -> None:
        """Non-existent class/module raises OceanidError."""
        from sphinx_oceanid.exceptions import OceanidError

        with pytest.raises(OceanidError):
            list(get_classes("nonexistent.module.Class"))

    def test_get_classes_not_class_nor_module_raises(self) -> None:
        """Object that is neither class nor module raises OceanidError."""
        from sphinx_oceanid.exceptions import OceanidError

        # __name__ + ".SOME_CONSTANT" would be a string, not a class
        with pytest.raises(OceanidError):
            list(get_classes(f"{__name__}.SOME_CONSTANT"))


# A constant to trigger "not a class nor a module" error
SOME_CONSTANT = "I am not a class"


# --- Tests for class_diagram ---


class TestClassDiagramBasic:
    """Tests for basic class_diagram() behavior (T052)."""

    def test_class_diagram_basic(self) -> None:
        """Simple inheritance A -> B produces valid classDiagram."""
        result = class_diagram(f"{__name__}.Dog")
        assert result.startswith("classDiagram\n")
        assert "Mammal <|-- Dog" in result

    def test_class_diagram_no_inheritance(self) -> None:
        """Class with only object as parent produces empty string."""
        result = class_diagram(f"{__name__}.Animal")
        assert result == ""

    def test_class_diagram_multiple_classes(self) -> None:
        """Multiple class arguments generate combined diagram."""
        result = class_diagram(f"{__name__}.Dog", f"{__name__}.Cat")
        assert "Mammal <|-- Dog" in result
        assert "Mammal <|-- Cat" in result


class TestClassDiagramMultipleInheritance:
    """Tests for multiple inheritance (T052)."""

    def test_class_diagram_multiple_inheritance(self) -> None:
        """Class with multiple parents shows all direct parents."""
        result = class_diagram(f"{__name__}.Platypus")
        assert "Mammal <|-- Platypus" in result
        assert "Bird <|-- Platypus" in result

    def test_class_diagram_diamond_inheritance_full(self) -> None:
        """Full traversal of diamond inheritance shows all ancestors."""
        result = class_diagram(f"{__name__}.Platypus", full=True)
        assert "Mammal <|-- Platypus" in result
        assert "Bird <|-- Platypus" in result
        assert "Animal <|-- Mammal" in result
        assert "Animal <|-- Bird" in result


class TestClassDiagramUpToObject:
    """Tests for full hierarchy traversal up to object (T052)."""

    def test_class_diagram_up_to_object(self) -> None:
        """full=True traverses up to object (excluded) from deep hierarchy."""
        result = class_diagram(f"{__name__}.DeepChild", full=True)
        assert "Dog <|-- DeepChild" in result
        assert "Mammal <|-- Dog" in result
        assert "Animal <|-- Mammal" in result
        # object should NOT appear
        assert "object" not in result

    def test_class_diagram_shallow_by_default(self) -> None:
        """Default (full=False) only shows direct parents."""
        result = class_diagram(f"{__name__}.DeepChild")
        assert "Dog <|-- DeepChild" in result
        # Should NOT include grandparent
        assert "Mammal <|-- Dog" not in result


class TestClassDiagramNamespace:
    """Tests for namespace filtering."""

    def test_class_diagram_namespace_filter(self) -> None:
        """namespace parameter filters base classes by module prefix."""
        result = class_diagram(f"{__name__}.Dog", full=True, namespace=__name__)
        assert "Mammal <|-- Dog" in result
        assert "Animal <|-- Mammal" in result

    def test_class_diagram_namespace_excludes_foreign(self) -> None:
        """namespace parameter excludes classes from other modules."""
        # With a namespace that doesn't match, no inheritances should be found
        result = class_diagram(f"{__name__}.Dog", full=True, namespace="nonexistent")
        assert result == ""


class TestClassDiagramOutput:
    """Tests for output format correctness."""

    def test_output_starts_with_classDiagram(self) -> None:
        """Output begins with 'classDiagram' keyword."""
        result = class_diagram(f"{__name__}.Dog")
        assert result.startswith("classDiagram\n")

    def test_output_lines_are_sorted(self) -> None:
        """Inheritance lines are sorted for deterministic output."""
        result = class_diagram(f"{__name__}.Platypus", full=True)
        lines = result.strip().split("\n")[1:]  # Skip "classDiagram" header
        stripped_lines = [line.strip() for line in lines]
        assert stripped_lines == sorted(stripped_lines)

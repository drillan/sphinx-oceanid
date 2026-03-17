"""Auto-generation of Mermaid class diagrams from Python class hierarchies.

Ported from sphinxcontrib-mermaid with modernization (type annotations, pathlib).
"""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING

from sphinx.errors import ExtensionError
from sphinx.util import import_object

from .exceptions import OceanidError

if TYPE_CHECKING:
    from collections.abc import Iterator


def get_classes(*cls_or_modules: str, strict: bool = False) -> Iterator[type]:
    """Yield class objects from fully qualified names.

    Each argument can be a fully qualified class name (e.g. ``mypackage.MyClass``)
    or a module name (e.g. ``mypackage.models``). Modules yield all classes
    defined within them.

    Args:
        *cls_or_modules: Fully qualified class or module names.
        strict: If True, only yield classes whose ``__module__`` starts with
            the module's ``__name__`` (i.e. classes defined in that module,
            not re-exported ones).

    Yields:
        Class objects found from the given names.

    Raises:
        OceanidError: If a name cannot be imported or is neither a class nor a module.
    """
    for cls_or_module in cls_or_modules:
        try:
            obj = import_object(cls_or_module)
        except ExtensionError as exc:
            raise OceanidError(str(exc)) from exc

        if inspect.isclass(obj):
            yield obj
        elif inspect.ismodule(obj):
            for member in obj.__dict__.values():
                if inspect.isclass(member) and (not strict or member.__module__.startswith(obj.__name__)):
                    yield member
        else:
            raise OceanidError(f"{cls_or_module} is not a class nor a module")


def class_diagram(
    *cls_or_modules: str,
    full: bool = False,
    strict: bool = False,
    namespace: str | None = None,
) -> str:
    """Generate a Mermaid classDiagram from Python class hierarchies.

    Args:
        *cls_or_modules: Fully qualified class or module names.
        full: If True, traverse the full inheritance tree up to ``object``.
            If False (default), only show direct parents.
        strict: If True, only include classes defined in the specified module.
        namespace: If set, only include base classes whose ``__module__``
            starts with this prefix.

    Returns:
        Mermaid classDiagram notation string, or empty string if no
        inheritance relationships are found.
    """
    inheritances: set[tuple[type, type]] = set()

    def _get_tree(cls: type) -> None:
        for base in cls.__bases__:
            if base is object:
                continue
            if namespace and not base.__module__.startswith(namespace):
                continue
            inheritances.add((base, cls))
            if full:
                _get_tree(base)

    for cls in get_classes(*cls_or_modules, strict=strict):
        _get_tree(cls)

    if not inheritances:
        return ""

    # Collect all classes and detect short-name collisions
    all_classes: set[type] = set()
    for parent, child in inheritances:
        all_classes.add(parent)
        all_classes.add(child)

    name_groups: dict[str, list[type]] = {}
    for cls in all_classes:
        name_groups.setdefault(cls.__name__, []).append(cls)

    def _mermaid_name(cls: type) -> str:
        if len(name_groups[cls.__name__]) > 1:
            return f"`{cls.__module__}.{cls.__name__}`"
        return cls.__name__

    lines = sorted(f"  {_mermaid_name(parent)} <|-- {_mermaid_name(child)}" for parent, child in inheritances)
    return "classDiagram\n" + "\n".join(lines)

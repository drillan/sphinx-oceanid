"""Exception classes for sphinx-oceanid."""

from sphinx.errors import ExtensionError


class OceanidError(ExtensionError):
    """Base exception for all sphinx-oceanid errors."""

    category = "sphinx-oceanid error"

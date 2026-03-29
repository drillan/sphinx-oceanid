"""Mermaid YAML frontmatter parsing (pure functions)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import yaml

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)---\n?", re.DOTALL)


@dataclass(frozen=True)
class FrontmatterResult:
    """Result of parsing Mermaid YAML frontmatter."""

    code: str
    title: str = ""
    config: dict[str, object] = field(default_factory=dict)


def parse_frontmatter(code: str) -> FrontmatterResult:
    """Parse YAML frontmatter from Mermaid code.

    Extracts ``title`` and ``config`` from the ``---``-delimited YAML block
    at the start of the code. Unknown keys are silently ignored.

    Args:
        code: Mermaid notation string, possibly prefixed with YAML frontmatter.

    Returns:
        FrontmatterResult with extracted values and the remaining code.

    Raises:
        ValueError: If ``title`` is not a string or ``config`` is not a dict.
    """
    match = _FRONTMATTER_RE.match(code)
    if not match:
        return FrontmatterResult(code=code)

    yaml_block = match.group(1)
    remaining_code = code[match.end() :]

    parsed = yaml.safe_load(yaml_block)
    if not isinstance(parsed, dict):
        return FrontmatterResult(code=remaining_code)

    title = parsed.get("title", "")
    if title and not isinstance(title, str):
        raise ValueError(f"Frontmatter 'title' must be a string, got {type(title).__name__}")

    config = parsed.get("config", {})
    if config and not isinstance(config, dict):
        raise ValueError(f"Frontmatter 'config' must be a dict, got {type(config).__name__}")

    return FrontmatterResult(
        code=remaining_code,
        title=title if isinstance(title, str) else "",
        config=config if isinstance(config, dict) else {},
    )

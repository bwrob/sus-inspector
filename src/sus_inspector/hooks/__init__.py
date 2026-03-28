"""Hook registry for custom object renderers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

    from rich.console import RenderableType

# Type for hook registry: list of (type_checker_func, render_func)
VIEW_HOOKS: list[
    tuple[type | Callable[[Any], bool], Callable[[Any], RenderableType]]
] = []


def register_hook(
    type_checker: type | Callable[[Any], bool],
    render_func: Callable[[Any], RenderableType],
) -> None:
    """Register a custom view for a specific object type.

    Args:
        type_checker: A type or a function that returns True if the object matches.
        render_func: A function that takes the object and returns a Rich renderable.

    """
    VIEW_HOOKS.insert(0, (type_checker, render_func))

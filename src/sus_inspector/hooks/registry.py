"""Hook registry for custom object renderers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

    from rich.console import RenderableType

# Type for hook registry: list of (type_checker_func, render_func)
HookList = list[
    tuple[
        "type | Callable[[Any], bool]",
        "Callable[[Any], RenderableType]",
    ]
]

# Instance-level hooks (how to show the instance data)
INSTANCE_HOOKS: HookList = []

# Class-level hooks (how to show the class metadata/structure)
CLASS_HOOKS: HookList = []

# Type for hook registry: list of (type_checker_func, render_func)
VIEW_HOOKS: HookList = INSTANCE_HOOKS


def register_instance_hook(
    type_checker: type | Callable[[Any], bool],
    render_func: Callable[[Any], RenderableType],
) -> None:
    """Register a custom instance view for a specific object type.

    Args:
        type_checker: A type or a function that returns True if the object matches.
        render_func: A function that takes the object and returns a Rich renderable.

    """
    INSTANCE_HOOKS.insert(0, (type_checker, render_func))


def register_class_hook(
    type_checker: type | Callable[[Any], bool],
    render_func: Callable[[Any], RenderableType],
) -> None:
    """Register a custom class view for a specific object type.

    Args:
        type_checker: A type or a function that returns True if the object matches.
        render_func: A function that takes the object and returns a Rich renderable.

    """
    CLASS_HOOKS.insert(0, (type_checker, render_func))


def register_hook(
    type_checker: type | Callable[[Any], bool],
    render_func: Callable[[Any], RenderableType],
) -> None:
    """Register a custom instance view (alias for register_instance_hook).

    Args:
        type_checker: A type or a function that returns True if the object matches.
        render_func: A function that takes the object and returns a Rich renderable.

    """
    register_instance_hook(type_checker, render_func)


def get_renderer(obj: Any, hooks: HookList) -> Callable[[Any], RenderableType] | None:
    """Find the first matching renderer for an object.

    Args:
        obj: The object to render.
        hooks: The hook registry to search in.

    Returns:
        Callable[[Any], RenderableType] | None: The renderer if found, else None.

    """
    for type_checker, render_func in hooks:
        if isinstance(type_checker, type):
            if isinstance(obj, type_checker):
                return render_func
        elif type_checker(obj):  # type: ignore[operator]
            return render_func
    return None


def ensure_default_hooks() -> None:
    """Register default hooks if the registry is empty."""
    if INSTANCE_HOOKS:
        return

    # Register built-in hooks lazily
    from sus_inspector.hooks.builtins import list_view  # noqa: PLC0415

    register_hook(list, list_view)

    # Optional Pydantic support
    try:
        from pydantic import BaseModel  # noqa: PLC0415

        from sus_inspector.hooks.pydantic import pydantic_view  # noqa: PLC0415

        register_hook(BaseModel, pydantic_view)
    except ImportError:
        pass

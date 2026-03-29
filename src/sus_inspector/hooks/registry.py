"""Hook registry for custom object renderers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sus_inspector.hooks.inspector import CLASS_REGISTRY, INSTANCE_REGISTRY

if TYPE_CHECKING:
    from collections.abc import Callable

    from rich.console import RenderableType

# For backward compatibility with existing code
INSTANCE_HOOKS = INSTANCE_REGISTRY._inspectors  # noqa: SLF001
CLASS_HOOKS = CLASS_REGISTRY._inspectors  # noqa: SLF001
VIEW_HOOKS = INSTANCE_HOOKS


def register_instance_hook(
    type_checker: type | Callable[[Any], bool],
    render_func: Callable[[Any], RenderableType],
    *,
    append: bool = False,
) -> None:
    """Register a custom instance view for a specific object type.

    Args:
        type_checker: A type or a function that returns True if the object matches.
        render_func: A function that takes the object and returns a Rich renderable.
        append: If True, append to the end of the list (lower priority).

    """
    INSTANCE_REGISTRY.register(type_checker, render_func, append=append)


def register_class_hook(
    type_checker: type | Callable[[Any], bool],
    render_func: Callable[[Any], RenderableType],
    *,
    append: bool = False,
) -> None:
    """Register a custom class view for a specific object type.

    Args:
        type_checker: A type or a function that returns True if the object matches.
        render_func: A function that takes the object and returns a Rich renderable.
        append: If True, append to the end of the list (lower priority).

    """
    CLASS_REGISTRY.register(type_checker, render_func, append=append)


def register_hook(
    type_checker: type | Callable[[Any], bool],
    render_func: Callable[[Any], RenderableType],
    *,
    append: bool = False,
) -> None:
    """Register a custom instance view (alias for register_instance_hook).

    Args:
        type_checker: A type or a function that returns True if the object matches.
        render_func: A function that takes the object and returns a Rich renderable.
        append: If True, append to the end of the list (lower priority).

    """
    register_instance_hook(type_checker, render_func, append=append)


def get_renderer(
    obj: object,
    hooks: Any,  # noqa: ANN401
) -> Callable[[Any], RenderableType] | None:
    """Find the first matching renderer for an object.

    Args:
        obj: The object to render.
        hooks: The hook registry to search in (maintained for backward compatibility).

    Returns:
        Callable[[Any], RenderableType] | None: The renderer if found, else None.

    """
    # Determine which registry to use based on the provided hooks list
    if hooks is CLASS_HOOKS:
        return CLASS_REGISTRY.get_inspector(obj)
    return INSTANCE_REGISTRY.get_inspector(obj)


def ensure_default_hooks() -> None:
    """Register default hooks if the registry is empty."""
    if INSTANCE_REGISTRY._inspectors:  # noqa: SLF001
        return

    # Register built-in hooks lazily
    from sus_inspector.hooks.builtins import (  # noqa: PLC0415
        CallableInspector,
        CollectionInspector,
        ObjectInspector,
        PrimitiveInspector,
    )

    # Primitive types
    primitive_inspector = PrimitiveInspector()
    for t in (int, float, str, bool, type(None)):
        register_hook(t, primitive_inspector)

    # Collection types
    collection_inspector = CollectionInspector()
    for t in (list, tuple, dict, set):
        register_hook(t, collection_inspector)

    # Callables
    register_hook(callable, CallableInspector())

    # General Object fallback (registered last, so it's lower priority than above)
    register_hook(object, ObjectInspector(), append=True)

    # Optional Pydantic support
    try:
        from pydantic import BaseModel  # noqa: PLC0415

        from sus_inspector.hooks.pydantic import PydanticInspector  # noqa: PLC0415

        register_hook(BaseModel, PydanticInspector())
    except ImportError:
        pass

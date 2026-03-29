"""Inspector registry for object-specific rendering logic."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Callable

    from rich.console import RenderableType


@runtime_checkable
class Inspector(Protocol):
    """Protocol for custom object inspectors."""

    def __call__(self, obj: Any) -> RenderableType:  # noqa: ANN401
        """Inspect an object and return a Rich renderable.

        Args:
            obj: The object to inspect.

        Returns:
            RenderableType: A Rich renderable representing the object.

        """
        ...


class InspectorRegistry:
    """Registry for mapping types to inspectors."""

    def __init__(self) -> None:
        """Initialize the registry."""
        self._inspectors: list[
            tuple[
                type | Callable[[Any], bool],
                Inspector | Callable[[Any], RenderableType],
            ]
        ] = []

    @property
    def inspectors(
        self,
    ) -> list[
        tuple[
            type | Callable[[Any], bool],
            Inspector | Callable[[Any], RenderableType],
        ]
    ]:
        """Return the list of registered inspectors.

        Returns:
            The internal list of inspectors.

        """
        return self._inspectors

    def register(
        self,
        type_checker: type | Callable[[Any], bool],
        inspector: Inspector | Callable[[Any], RenderableType],
        *,
        append: bool = False,
    ) -> None:
        """Register an inspector for a specific type or condition.

        Args:
            type_checker: A type or a function that returns True if the object matches.
            inspector: An Inspector or a callable that returns a RenderableType.
            append: If True, append to the end of the list (lower priority).

        """
        if append:
            self._inspectors.append((type_checker, inspector))
        else:
            self._inspectors.insert(0, (type_checker, inspector))

    def get_inspector(
        self,
        obj: Any,  # noqa: ANN401
    ) -> Inspector | Callable[[Any], RenderableType] | None:
        """Find the first matching inspector for an object.

        Args:
            obj: The object to inspect.

        Returns:
            The inspector if found, else None.

        """
        for type_checker, inspector in self._inspectors:
            if isinstance(type_checker, type):
                if isinstance(obj, type_checker):
                    return inspector
            elif type_checker(obj):
                return inspector
        return None


# Global registries
INSTANCE_REGISTRY = InspectorRegistry()
CLASS_REGISTRY = InspectorRegistry()

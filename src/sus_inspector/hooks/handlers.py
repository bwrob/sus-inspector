"""Base class and registry for specialized object handlers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from rich.console import RenderableType

# Constants for complexity assessment
COMPLEXITY_FIELD_THRESHOLD = 10


class BaseObjectHandler(ABC):
    """Base class for all library-specific object handlers."""

    @abstractmethod
    def can_handle(self, obj: Any) -> bool:  # noqa: ANN401
        """Check if this handler can process the given object.

        Args:
            obj: The object to check.

        Returns:
            bool: True if this handler can process the object.

        """
        ...

    @abstractmethod
    def get_type_tag(self, obj: Any) -> str:  # noqa: ANN401
        """Return a string tag representing the library type.

        Args:
            obj: The object to get the tag for.

        Returns:
            str: The type tag (e.g., 'Pydantic', 'Dataclass').

        """
        ...

    @abstractmethod
    def get_fields(self, obj: Any) -> dict[str, Any]:  # noqa: ANN401
        """Extract fields and values from the object.

        Args:
            obj: The object to extract fields from.

        Returns:
            dict[str, Any]: A dictionary of field names and values.

        """
        ...

    def is_complex(self, obj: Any) -> bool:  # noqa: ANN401
        """Assess if the object is complex based on heuristics.

        Args:
            obj: The object to assess.

        Returns:
            bool: True if the object is considered complex.

        """
        # Default implementation (can be overridden by specialized handlers)
        fields = self.get_fields(obj)
        return len(fields) > COMPLEXITY_FIELD_THRESHOLD

    @abstractmethod
    def render(
        self,
        obj: Any,  # noqa: ANN401
        *,
        expanded: bool = False,
    ) -> RenderableType:
        """Render the object as a Rich renderable.

        Args:
            obj: The object to render.
            expanded: Whether to render the full view or a summary.

        Returns:
            RenderableType: The Rich renderable.

        """
        ...


class HandlerRegistry:
    """Registry for specialized object handlers."""

    def __init__(self) -> None:
        """Initialize the registry."""
        self._handlers: list[BaseObjectHandler] = []

    def register(self, handler: BaseObjectHandler) -> None:
        """Register a new object handler.

        Args:
            handler: The handler to register.

        """
        self._handlers.append(handler)

    def get_handler(self, obj: Any) -> BaseObjectHandler | None:  # noqa: ANN401
        """Find the first handler that can process the given object.

        Args:
            obj: The object to find a handler for.

        Returns:
            BaseObjectHandler | None: The matching handler, or None if no match.

        """
        for handler in self._handlers:
            if handler.can_handle(obj):
                return handler
        return None

    @property
    def has_handlers(self) -> bool:
        """Check if any handlers are registered.

        Returns:
            bool: True if the registry is not empty.

        """
        return bool(self._handlers)


# Global registry for specialized handlers
HANDLER_REGISTRY = HandlerRegistry()


def ensure_handlers() -> None:
    """Register all available specialized handlers."""
    if HANDLER_REGISTRY.has_handlers:
        return

    # Handlers will be registered here as they are implemented in subsequent tasks.

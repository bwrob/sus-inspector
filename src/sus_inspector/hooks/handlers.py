"""Registry for specialized object handlers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sus_inspector.hooks.base import BaseObjectHandler


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

    # Phase 1: dataclasses (always available in stdlib)
    from sus_inspector.hooks.dataclasses import DataclassHandler  # noqa: PLC0415

    HANDLER_REGISTRY.register(DataclassHandler())

    # Phase 2: Optional libraries
    try:
        from sus_inspector.hooks.pydantic import PydanticHandler  # noqa: PLC0415

        HANDLER_REGISTRY.register(PydanticHandler())
    except ImportError:
        pass

    try:
        from sus_inspector.hooks.attrs import AttrsHandler  # noqa: PLC0415

        HANDLER_REGISTRY.register(AttrsHandler())
    except ImportError:
        pass

    try:
        from sus_inspector.hooks.msgspec import MsgspecHandler  # noqa: PLC0415

        HANDLER_REGISTRY.register(MsgspecHandler())
    except ImportError:
        pass

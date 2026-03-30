"""Base class for specialized object handlers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from sus_inspector.hooks.complexity import is_complex_object

if TYPE_CHECKING:
    from rich.console import RenderableType


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

    def is_complex(self, obj: Any) -> bool:  # noqa: ANN401, PLR6301
        """Assess if the object is complex based on heuristics.

        Args:
            obj: The object to assess.

        Returns:
            bool: True if the object is considered complex.

        """
        return is_complex_object(obj)

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

"""Base class for specialized object handlers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from rich.console import Group
from rich.pretty import Pretty
from rich.table import Table
from rich.text import Text

from sus_inspector.hooks.complexity import is_complex_object

if TYPE_CHECKING:
    from rich.console import RenderableType


class BaseObjectHandler(ABC):
    """Base class for all library-specific object handlers."""

    @abstractmethod
    def can_handle(self, obj: Any) -> bool:  # noqa: ANN401
        """Check if this handler can process the given object.

        Returns:
            bool: True if this handler can process the object.

        """
        ...

    @abstractmethod
    def get_type_tag(self, obj: Any) -> str:  # noqa: ANN401
        """Return a string tag representing the library type.

        Returns:
            str: The type tag (e.g., 'Pydantic', 'Dataclass').

        """
        ...

    @abstractmethod
    def get_fields(self, obj: Any) -> dict[str, Any]:  # noqa: ANN401
        """Extract fields and values from the object.

        Returns:
            dict[str, Any]: A dictionary of field names and values.

        """
        ...

    def is_complex(self, obj: Any) -> bool:  # noqa: ANN401, PLR6301
        """Assess if the object is complex based on heuristics.

        Returns:
            bool: True if the object is considered complex.

        """
        return is_complex_object(obj)

    def render(
        self,
        obj: Any,  # noqa: ANN401
        *,
        expanded: bool = False,
    ) -> RenderableType:
        """Render the object as a Rich renderable.

        Returns:
            RenderableType: The Rich renderable.

        """
        model_name = type(obj).__name__
        tag = self.get_type_tag(obj)
        tag_style = self.get_tag_style()

        header = Text.assemble(
            ("[", "dim"),
            (tag, tag_style),
            ("] ", "dim"),
            (model_name, "bold"),
        )

        fields = self.get_fields(obj)

        if not expanded and self.is_complex(obj):
            summary = f"({len(fields)} fields) ..."
            return Group(header, Text(summary, style="italic dim"))

        table = Table(box=None, padding=(0, 1), show_header=False)
        table.add_column("Field", style="cyan")
        table.add_column("Value")

        for k, v in fields.items():
            table.add_row(f"{k}:", Pretty(v, max_length=3, max_string=50))

        return Group(header, table)

    def get_tag_style(self) -> str:  # noqa: PLR6301
        """Return the style for the type tag.

        Returns:
            str: Rich style string.

        """
        return "bold white"

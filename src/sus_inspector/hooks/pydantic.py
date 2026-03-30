"""Specialized handler for Pydantic models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rich.console import Group
from rich.pretty import Pretty
from rich.text import Text
from typing_extensions import override

from sus_inspector.hooks.base import BaseObjectHandler

if TYPE_CHECKING:
    from rich.console import RenderableType


class PydanticHandler(BaseObjectHandler):
    """Handler for Pydantic (v1 and v2) models."""

    @override
    def can_handle(self, obj: Any) -> bool:
        """Check if the object is a Pydantic model.

        Returns:
            bool: True if obj is a Pydantic model.

        """
        try:
            from pydantic import BaseModel  # noqa: PLC0415
        except ImportError:
            return False
        return isinstance(obj, BaseModel)

    @override
    def get_type_tag(self, obj: Any) -> str:
        """Return the 'Pydantic' tag.

        Returns:
            str: "Pydantic"

        """
        return "Pydantic"

    @override
    def get_fields(self, obj: Any) -> dict[str, Any]:
        """Extract fields using model_dump or dict.

        Returns:
            dict[str, Any]: Fields and values.

        """
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        if hasattr(obj, "dict"):
            return obj.dict()
        return {}

    @override
    def render(
        self,
        obj: Any,
        *,
        expanded: bool = False,
    ) -> RenderableType:
        """Render the Pydantic model.

        Returns:
            RenderableType: Rich group containing the tag and data.

        """
        model_name = type(obj).__name__
        tag = self.get_type_tag(obj)

        header = Text.assemble(
            ("[", "dim"),
            (tag, "bold yellow"),
            ("] ", "dim"),
            (model_name, "bold"),
        )

        if not expanded and self.is_complex(obj):
            fields = self.get_fields(obj)
            summary = f"({len(fields)} fields) ..."
            return Group(header, Text(summary, style="italic dim"))

        return Group(
            header,
            Pretty(obj, expand_all=True),
        )


class PydanticInspector(PydanticHandler):
    """Inspector for Pydantic models (legacy compatibility)."""

    def __call__(self, obj: Any) -> RenderableType:  # noqa: ANN401
        """Compatibility for old __call__ interface.

        Returns:
            RenderableType: Rich renderable.

        """
        return self.render(obj)


def pydantic_view(obj: Any) -> RenderableType:  # noqa: ANN401
    """Compatibility wrapper for Pydantic model rendering.

    Args:
        obj: The Pydantic model.

    Returns:
        RenderableType: Rich renderable.

    """
    return PydanticHandler().render(obj)

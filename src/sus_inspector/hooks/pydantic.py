"""Specialized handler for Pydantic models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

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
    def get_tag_style(self) -> str:
        """Return the style for the Pydantic tag.

        Returns:
            str: "bold yellow"

        """
        return "bold yellow"

    @override
    def get_fields(self, obj: Any) -> dict[str, Any]:
        """Extract fields without recursion to keep original objects.

        Returns:
            dict[str, Any]: Fields and values.

        """
        # We want the original objects, not a serialized dict
        fields = dict(obj.__dict__)
        # For Pydantic v2, we might also want model_extra
        if hasattr(obj, "model_extra") and obj.model_extra:
            fields.update(obj.model_extra)
        return fields


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

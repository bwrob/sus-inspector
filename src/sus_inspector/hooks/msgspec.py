"""Specialized handler for msgspec structs."""

from __future__ import annotations

from typing import Any

from typing_extensions import override

from sus_inspector.hooks.base import BaseObjectHandler


class MsgspecHandler(BaseObjectHandler):
    """Handler for msgspec structs."""

    @override
    def can_handle(self, obj: Any) -> bool:
        """Check if the object is a msgspec struct instance.

        Returns:
            bool: True if obj is a msgspec struct.

        """
        try:
            import msgspec  # noqa: PLC0415
        except ImportError:
            return False
        return isinstance(obj, msgspec.Struct)

    @override
    def get_type_tag(self, obj: Any) -> str:
        """Return the 'Msgspec' tag.

        Returns:
            str: "Msgspec"

        """
        return "Msgspec"

    @override
    def get_tag_style(self) -> str:
        """Return the style for the Msgspec tag.

        Returns:
            str: "bold green"

        """
        return "bold green"

    @override
    def get_fields(self, obj: Any) -> dict[str, Any]:
        """Extract fields to keep original objects.

        Returns:
            dict[str, Any]: Fields and values.

        """
        return {f: getattr(obj, f) for f in obj.__struct_fields__}

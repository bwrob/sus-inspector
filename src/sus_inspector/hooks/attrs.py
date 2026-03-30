"""Specialized handler for attrs objects."""

from __future__ import annotations

from typing import Any, cast

from typing_extensions import override

from sus_inspector.hooks.base import BaseObjectHandler


class AttrsHandler(BaseObjectHandler):
    """Handler for attrs (and attr) classes."""

    @override
    def can_handle(self, obj: Any) -> bool:
        """Check if the object is an attrs-decorated class instance.

        Returns:
            bool: True if obj is an attrs instance.

        """
        try:
            import attr  # noqa: PLC0415
        except ImportError:
            return False
        # cast type(obj) to Any to avoid basedpyright unknown type issue
        return attr.has(cast("Any", type(obj))) and not isinstance(obj, type)

    @override
    def get_type_tag(self, obj: Any) -> str:
        """Return the 'Attrs' tag.

        Returns:
            str: "Attrs"

        """
        return "Attrs"

    @override
    def get_tag_style(self) -> str:
        """Return the style for the Attrs tag.

        Returns:
            str: "bold magenta"

        """
        return "bold magenta"

    @override
    def get_fields(self, obj: Any) -> dict[str, Any]:
        """Extract fields using attr.asdict or manual extraction.

        Returns:
            dict[str, Any]: Fields and values.

        """
        import attr  # noqa: PLC0415

        return attr.asdict(obj, recurse=False)

"""Specialized handler for attrs objects."""

from __future__ import annotations

from typing import Any, cast

from rich.console import Group
from rich.pretty import Pretty
from rich.text import Text
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
    def get_fields(self, obj: Any) -> dict[str, Any]:
        """Extract fields using attr.asdict or manual extraction.

        Returns:
            dict[str, Any]: Fields and values.

        """
        import attr  # noqa: PLC0415

        return attr.asdict(obj, recurse=False)

    @override
    def render(
        self,
        obj: Any,
        *,
        expanded: bool = False,
    ) -> Any:
        """Render the attrs instance.

        Returns:
            Group: Rich group containing the tag and data.

        """
        model_name = type(obj).__name__
        tag = self.get_type_tag(obj)

        header = Text.assemble(
            ("[", "dim"),
            (tag, "bold magenta"),
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

"""Specialized handler for msgspec structs."""

from __future__ import annotations

from typing import Any

from rich.console import Group
from rich.pretty import Pretty
from rich.text import Text
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
    def get_fields(self, obj: Any) -> dict[str, Any]:
        """Extract fields using msgspec.structs.asdict or manual extraction.

        Returns:
            dict[str, Any]: Fields and values.

        """
        # msgspec.structs.asdict is fast and handles structs well
        return {f: getattr(obj, f) for f in obj.__struct_fields__}

    @override
    def render(
        self,
        obj: Any,
        *,
        expanded: bool = False,
    ) -> Any:
        """Render the msgspec struct.

        Returns:
            Group: Rich group containing the tag and data.

        """
        model_name = type(obj).__name__
        tag = self.get_type_tag(obj)

        header = Text.assemble(
            ("[", "dim"),
            (tag, "bold green"),
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

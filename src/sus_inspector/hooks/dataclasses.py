"""Specialized handler for Python dataclasses."""

from __future__ import annotations

import dataclasses
from typing import Any

from rich.console import Group
from rich.pretty import Pretty
from rich.text import Text
from typing_extensions import override

from sus_inspector.hooks.base import BaseObjectHandler


class DataclassHandler(BaseObjectHandler):
    """Handler for Python standard library dataclasses."""

    @override
    def can_handle(self, obj: Any) -> bool:
        """Check if the object is a dataclass instance.

        Returns:
            bool: True if obj is a dataclass.

        """
        return dataclasses.is_dataclass(obj) and not isinstance(obj, type)

    @override
    def get_type_tag(self, obj: Any) -> str:
        """Return the 'Dataclass' tag.

        Returns:
            str: "Dataclass"

        """
        return "Dataclass"

    @override
    def get_fields(self, obj: Any) -> dict[str, Any]:
        """Extract fields using dataclasses.asdict or manual extraction.

        Returns:
            dict[str, Any]: Fields and values.

        """
        # We don't use asdict to avoid recursive conversion of nested dataclasses
        return {f.name: getattr(obj, f.name) for f in dataclasses.fields(obj)}

    @override
    def render(
        self,
        obj: Any,
        *,
        expanded: bool = False,
    ) -> Group:
        """Render the dataclass instance.

        Returns:
            Group: Rich group containing the tag and data.

        """
        model_name = type(obj).__name__
        tag = self.get_type_tag(obj)

        header = Text.assemble(
            ("[", "dim"),
            (tag, "bold cyan"),
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

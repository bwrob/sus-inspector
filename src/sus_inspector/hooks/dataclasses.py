"""Specialized handler for Python dataclasses."""

from __future__ import annotations

import dataclasses
from typing import Any

from typing_extensions import override

from sus_inspector.hooks.base import BaseObjectHandler, FieldMetadata


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
    def get_tag_style(self) -> str:
        """Return the style for the Dataclass tag.

        Returns:
            str: "bold cyan"

        """
        return "bold cyan"

    @override
    def get_fields(self, obj: Any) -> dict[str, Any]:
        """Extract fields using manual extraction to keep original objects.

        Returns:
            dict[str, Any]: Fields and values.

        """
        return {f.name: getattr(obj, f.name) for f in dataclasses.fields(obj)}

    @override
    def get_field_metadata(self, obj: Any) -> list[FieldMetadata]:
        """Extract metadata for dataclass fields.

        Returns:
            list[FieldMetadata]: List of field metadata dictionaries.

        """
        cls = obj if isinstance(obj, type) else type(obj)
        fields = dataclasses.fields(cls)

        # Dataclasses don't natively support field-level docstrings easily
        # unless using some convention.
        metadata: list[FieldMetadata] = [
            {
                "name": f.name,
                "type_annotation": f.type,
                "description": None,
                "default_value": f.default
                if f.default is not dataclasses.MISSING
                else None,
            }
            for f in fields
        ]
        return metadata

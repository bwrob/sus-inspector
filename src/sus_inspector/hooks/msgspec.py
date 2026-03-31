"""Specialized handler for msgspec structs."""

from __future__ import annotations

from typing import Any, cast, get_type_hints

from typing_extensions import override

from sus_inspector.hooks.base import BaseObjectHandler, FieldMetadata


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

    @override
    def get_field_metadata(self, obj: Any) -> list[FieldMetadata]:
        """Extract metadata for msgspec fields.

        Returns:
            list[FieldMetadata]: List of field metadata dictionaries.

        """
        cls = obj if isinstance(obj, type) else type(obj)
        metadata: list[FieldMetadata] = []

        # msgspec doesn't store much metadata in the struct itself,
        # but we can get names and type hints.
        hints = get_type_hints(cls)
        # Cast to Any to avoid basedpyright issues with unknown members
        cls_any = cast("Any", cls)

        # To get default values correctly for msgspec.Struct
        # we can use inspect.signature on the class __init__
        import inspect  # noqa: PLC0415

        try:
            sig = inspect.signature(cls)
            params = sig.parameters
        except (ValueError, TypeError):
            params = cast("Any", {})

        for name in cls_any.__struct_fields__:
            default = None
            if name in params:
                param = cast("Any", params[name])
                if param.default is not inspect.Parameter.empty:
                    default = param.default

            metadata.append(
                {
                    "name": name,
                    "type_annotation": hints.get(name, Any),
                    "description": None,
                    "default_value": default,
                }
            )
        return metadata

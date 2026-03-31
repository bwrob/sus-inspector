"""Base class for specialized object handlers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, TypedDict

from rich.console import Group
from rich.pretty import Pretty
from rich.table import Table
from rich.text import Text

from sus_inspector.hooks.complexity import is_complex_object

if TYPE_CHECKING:
    from rich.console import RenderableType


class FieldMetadata(TypedDict):
    """Metadata for a single field in a class."""

    name: str
    type_annotation: Any
    description: str | None
    default_value: Any


class BaseObjectHandler(ABC):
    """Base class for all library-specific object handlers."""

    @abstractmethod
    def can_handle(self, obj: Any) -> bool:  # noqa: ANN401
        """Check if this handler can process the given object.

        Args:
            obj: The object to check.

        Returns:
            bool: True if this handler can process the object.

        """
        ...

    @abstractmethod
    def get_type_tag(self, obj: Any) -> str:  # noqa: ANN401
        """Return a string tag representing the library type.

        Args:
            obj: The object to get the tag for.

        Returns:
            str: The type tag (e.g., 'Pydantic', 'Dataclass').

        """
        ...

    @abstractmethod
    def get_fields(self, obj: Any) -> dict[str, Any]:  # noqa: ANN401
        """Extract fields and values from the object.

        Args:
            obj: The object to extract fields from.

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

    def get_field_metadata(self, obj: Any) -> list[FieldMetadata]:  # noqa: ANN401, PLR6301
        """Extract metadata for all fields in the class.

        Args:
            obj: The object or class.

        Returns:
            list[FieldMetadata]: List of field metadata dictionaries.

        """
        _ = obj
        return []

    def get_methods(self, obj: Any) -> dict[str, Any]:  # noqa: ANN401, PLR6301
        """Extract methods from the object.

        Args:
            obj: The object to extract methods from.

        Returns:
            dict[str, Any]: A dictionary of method names and callables.

        """
        import inspect  # noqa: PLC0415

        cls = obj if isinstance(obj, type) else type(obj)
        methods: dict[str, Any] = {}
        for name in dir(cls):
            if name.startswith("__"):
                continue
            try:
                value = getattr(cls, name)
                if inspect.isroutine(value):
                    methods[name] = value
            except (AttributeError, Exception):  # noqa: BLE001, S112
                continue
        return methods

    def render_class_view(self, obj: Any) -> RenderableType:  # noqa: ANN401
        """Render a rich view of the class structure.

        Args:
            obj: The object or class.

        Returns:
            RenderableType: Rich renderable showing class fields and metadata.

        """
        field_meta = self.get_field_metadata(obj)
        methods = self.get_methods(obj)

        if not field_meta and not methods:
            return Text("No field or method metadata available.")

        output: list[Any] = []

        if field_meta:
            output.append(self._render_field_table(field_meta))

        if methods:
            output.append(self._render_method_table(methods))

        return Group(*output)

    def _render_field_table(self, field_meta: list[FieldMetadata]) -> Table:  # noqa: PLR6301
        """Render the field metadata table.

        Returns:
            Table: Rich table showing field details.

        """
        table = Table(
            title="Field Schema", show_header=True, header_style="bold magenta"
        )
        table.add_column("Field", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Description", style="italic")
        table.add_column("Default", style="dim")

        for field in field_meta:
            type_str = str(field["type_annotation"])
            if "'" in type_str:
                type_str = type_str.split("'")[1]

            default_val = field.get("default_value")
            table.add_row(
                field["name"],
                type_str,
                field["description"] or "",
                str(default_val) if default_val is not None else "",
            )
        return table

    def _render_method_table(self, methods: dict[str, Any]) -> Table:  # noqa: PLR6301
        """Render the methods table.

        Returns:
            Table: Rich table showing method signatures.

        """
        method_table = Table(
            title="Methods", show_header=True, header_style="bold blue"
        )
        method_table.add_column("Method", style="cyan")
        method_table.add_column("Signature", style="green")

        import inspect  # noqa: PLC0415

        for name, func in sorted(methods.items()):
            try:
                sig = str(inspect.signature(func))
            except (ValueError, TypeError):
                sig = "(...)"
            method_table.add_row(name, sig)
        return method_table

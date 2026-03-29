"""Built-in view hooks for common Python types."""

from __future__ import annotations

import inspect
from typing import Any, cast

from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from rich.pretty import Pretty
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

PREVIEW_LENGTH = 50
MAX_ITEMS = 100
MAX_PREVIEW_LENGTH = 80


class PrimitiveInspector:
    """Inspector for primitive Python types (int, float, str, bool, None)."""

    def __call__(self, obj: Any) -> Panel:  # noqa: ANN401
        """Render a primitive object.

        Args:
            obj: The object to render.

        Returns:
            Panel: Rich panel representation.

        """
        return Panel(Pretty(obj), title=f"Primitive: {type(obj).__name__}")


class CallableInspector:
    """Inspector for functions, methods, and other callables."""

    def __call__(self, obj: Any) -> Group:  # noqa: ANN401
        """Render a callable preview with section-based layout.

        Args:
            obj: The callable object to render.

        Returns:
            Group: Rich renderable showing callable info.

        """
        sections = []

        # Header Info
        name = getattr(obj, "__name__", "unknown")
        type_name = type(obj).__name__
        sections.append(
            Panel(
                Text.assemble(
                    (f"{type_name}: ", "bold cyan"),
                    (name, "bold yellow"),
                ),
                subtitle="Header Info",
            )
        )

        # Signature
        try:
            sig = inspect.signature(obj)
            sig_text = Text(str(sig), style="green")
            sections.append(Panel(sig_text, title="Signature", border_style="green"))
        except (ValueError, TypeError):
            sections.append(
                Panel(Text("(not available)"), title="Signature", border_style="red")
            )

        # Docstring
        doc = inspect.getdoc(obj)
        if doc:
            sections.append(
                Panel(
                    Syntax(doc, "python", theme="monokai", background_color="default"),
                    title="Docstring",
                    border_style="blue",
                )
            )

        # Metadata (Closure, Module, etc.)
        metadata = []
        if hasattr(obj, "__module__"):
            metadata.append(Text(f"Module: {obj.__module__}"))
        if hasattr(obj, "__closure__") and obj.__closure__:
            metadata.append(Text(f"Closure Cells: {len(obj.__closure__)}"))

        if metadata:
            sections.append(
                Panel(
                    Columns(metadata, padding=(0, 2)),
                    title="Metadata",
                    border_style="magenta",
                )
            )

        return Group(*sections)


class ObjectInspector:
    """Inspector for general Python objects and instances."""

    def __call__(self, obj: Any) -> Table:  # noqa: ANN401
        """Render an object instance preview.

        Args:
            obj: The object to render.

        Returns:
            Table: Rich table representation.

        """
        table = self._init_table(obj)

        # Basic Info
        doc = inspect.getdoc(obj)
        if doc:
            first_line = doc.split("\n")[0]
            table.add_row("__doc__", "str", first_line)

        # Attributes and Methods (Public only)
        for name in dir(obj):
            if name.startswith("_"):
                continue
            self._add_member_row(table, obj, name)

        return table

    @staticmethod
    def _init_table(obj: Any) -> Table:  # noqa: ANN401
        """Initialize the result table.

        Args:
            obj: The object to inspect.

        Returns:
            Table: The initialized Rich table.

        """
        table = Table(
            title=f"Object: {type(obj).__name__}",
            title_justify="left",
            show_edge=False,
        )
        table.add_column("Member", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Value/Doc", style="green")
        return table

    def _add_member_row(self, table: Table, obj: Any, name: str) -> None:  # noqa: ANN401
        """Add a single member row to the table."""
        try:
            val = getattr(obj, name)
            if inspect.isroutine(val):
                table.add_row(name, type(val).__name__, "(method)")
            else:
                preview = self._get_value_preview(val)
                table.add_row(name, type(val).__name__, preview)
        except (AttributeError, TypeError):
            table.add_row(name, "error", "[red]Attribute Error[/red]")
        except Exception:  # noqa: BLE001
            table.add_row(name, "error", "[red]Unexpected Error[/red]")

    @staticmethod
    def _get_value_preview(val: Any) -> str:  # noqa: ANN401
        """Get a string preview of a value.

        Args:
            val: The value to preview.

        Returns:
            str: The string representation of the value.

        """
        val_str = str(val)
        if len(val_str) > PREVIEW_LENGTH:
            return val_str[:PREVIEW_LENGTH] + "..."
        return val_str


class CollectionInspector:
    """Inspector for collection types (list, tuple, dict, set)."""

    def __call__(self, obj: Any) -> Table:  # noqa: ANN401
        """Render a collection object.

        Args:
            obj: The object to render.

        Returns:
            Table: Rich table representation.

        """
        if isinstance(obj, (list, tuple, set)):
            return list_view(obj)
        if isinstance(obj, dict):
            return dict_view(obj)
        return Table(title=f"Not a collection: {type(obj).__name__}")


def dict_view(obj: dict[Any, Any]) -> Table:
    """Render a dictionary as a Rich Table.

    Args:
        obj: The dictionary object to render.

    Returns:
        Table: Rich table representation.

    """
    title = f"Dict (length: {len(obj)})"
    table = Table(title=title, title_justify="left", show_edge=False)
    table.add_column("Key", justify="right", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Value Preview")

    for k, v in list(obj.items())[:MAX_ITEMS]:
        val_str = str(v)
        preview = (
            val_str[:MAX_PREVIEW_LENGTH] + "..."
            if len(val_str) > MAX_PREVIEW_LENGTH
            else val_str
        )
        table.add_row(str(k), type(v).__name__, preview)

    if len(obj) > MAX_ITEMS:
        rem = len(obj) - MAX_ITEMS
        table.add_row("...", "...", f"...and {rem} more items")

    return table


def list_view(obj: object) -> Table:
    """Render a list as a Rich Table.

    Args:
        obj: The list object to render.

    Returns:
        Table: Rich table representation.

    """
    if not isinstance(obj, (list, tuple, set)):
        # This shouldn't happen if type checker is correct
        return Table(title="Not a supported collection")

    obj_list = list(cast("list[object]", obj))
    type_name = type(obj).__name__.capitalize()
    title = f"{type_name} (length: {len(obj_list)})"
    table = Table(title=title, title_justify="left", show_edge=False)
    table.add_column("Index", justify="right", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Preview")

    for i, item in enumerate(obj_list[:MAX_ITEMS]):
        item_str = str(item)
        preview = (
            item_str[:MAX_PREVIEW_LENGTH] + "..."
            if len(item_str) > MAX_PREVIEW_LENGTH
            else item_str
        )
        table.add_row(str(i), type(item).__name__, preview)

    if len(obj_list) > MAX_ITEMS:
        rem = len(obj_list) - MAX_ITEMS
        table.add_row("...", "...", f"...and {rem} more items")

    return table

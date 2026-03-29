"""Built-in view hooks for common Python types."""

from __future__ import annotations

from typing import Any, cast

from rich.panel import Panel
from rich.pretty import Pretty
from rich.table import Table
from rich.text import Text


class PrimitiveInspector:
    """Inspector for primitive Python types (int, float, str, bool, None)."""

    def __call__(self, obj: Any) -> Panel:
        """Render a primitive object.

        Args:
            obj: The object to render.

        Returns:
            Panel: Rich panel representation.

        """
        return Panel(Pretty(obj), title=f"Primitive: {type(obj).__name__}")


class CallableInspector:
    """Inspector for functions, methods, and other callables."""

    def __call__(self, obj: Any) -> Any:
        """Render a callable preview with section-based layout.

        Args:
            obj: The callable object to render.

        Returns:
            RenderableType: Rich renderable showing callable info.

        """
        import inspect  # noqa: PLC0415

        from rich.columns import Columns
        from rich.console import Group
        from rich.syntax import Syntax

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

    def __call__(self, obj: Any) -> Table:
        """Render an object instance preview.

        Args:
            obj: The object to render.

        Returns:
            Table: Rich table representation.

        """
        import inspect  # noqa: PLC0415

        table = Table(
            title=f"Object: {type(obj).__name__}",
            title_justify="left",
            show_edge=False,
        )
        table.add_column("Member", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Value/Doc", style="green")

        # Basic Info
        doc = inspect.getdoc(obj)
        if doc:
            first_line = doc.split("\n")[0]
            table.add_row("__doc__", "str", first_line)

        # Attributes and Methods (Public only)
        for name in dir(obj):
            if name.startswith("_"):
                continue
            try:
                val = getattr(obj, name)
                if inspect.isroutine(val):
                    table.add_row(name, type(val).__name__, "(method)")
                else:
                    val_str = str(val)
                    preview = val_str[:50] + "..." if len(val_str) > 50 else val_str
                    table.add_row(name, type(val).__name__, preview)
            except Exception:
                table.add_row(name, "error", "[red]Attribute Error[/red]")

        return table


class CollectionInspector:
    """Inspector for collection types (list, tuple, dict, set)."""

    def __call__(self, obj: Any) -> Table:
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
    max_preview_items = 100
    max_preview_length = 80
    title = f"Dict (length: {len(obj)})"
    table = Table(title=title, title_justify="left", show_edge=False)
    table.add_column("Key", justify="right", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Value Preview")

    for i, (k, v) in enumerate(list(obj.items())[:max_preview_items]):
        val_str = str(v)
        preview = (
            val_str[:max_preview_length] + "..."
            if len(val_str) > max_preview_length
            else val_str
        )
        table.add_row(str(k), type(v).__name__, preview)

    if len(obj) > max_preview_items:
        rem = len(obj) - max_preview_items
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
    max_preview_items = 100
    max_preview_length = 80
    type_name = type(obj).__name__.capitalize()
    title = f"{type_name} (length: {len(obj_list)})"
    table = Table(title=title, title_justify="left", show_edge=False)
    table.add_column("Index", justify="right", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Preview")

    for i, item in enumerate(obj_list[:max_preview_items]):
        item_str = str(item)
        preview = (
            item_str[:max_preview_length] + "..."
            if len(item_str) > max_preview_length
            else item_str
        )
        table.add_row(str(i), type(item).__name__, preview)

    if len(obj_list) > max_preview_items:
        rem = len(obj_list) - max_preview_items
        table.add_row("...", "...", f"...and {rem} more items")

    return table

"""Built-in view hooks for common Python types."""

from __future__ import annotations

import inspect
from inspect import cleandoc
from typing import Any, cast

from rich.columns import Columns
from rich.console import Group
from rich.highlighter import ReprHighlighter
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

    highlighter: ReprHighlighter

    def __init__(self) -> None:
        """Initialize the inspector."""
        self.highlighter = ReprHighlighter()

    def __call__(self, obj: Any) -> Group:  # noqa: ANN401
        """Render a callable preview with section-based layout.

        Args:
            obj: The callable object to render.

        Returns:
            Group: Rich renderable showing callable info.

        """
        sections = [
            self._render_header(obj),
            self._render_signature(obj),
        ]

        # Docstring
        doc_panel = self._render_docstring(obj)
        if doc_panel:
            sections.append(doc_panel)

        # Metadata (Closure, Module, etc.)
        meta_panel = self._render_metadata(obj)
        if meta_panel:
            sections.append(meta_panel)

        return Group(*sections)

    @staticmethod
    def _render_header(obj: Any) -> Panel:  # noqa: ANN401
        """Render header information.

        Args:
            obj: The callable object.

        Returns:
            Panel: The header panel.

        """
        name = getattr(obj, "__name__", "unknown")
        type_name = type(obj).__name__

        header_text = Text.assemble(
            (f"{type_name}: ", "bold cyan"),
            (name, "bold yellow"),
        )

        try:
            file_path = inspect.getfile(obj)
            header_text.append("\n")
            _ = header_text.append(f"File: {file_path}", style="dim italic")
        except (TypeError, OSError):
            pass

        return Panel(header_text, subtitle="Header Info")

    @staticmethod
    def _render_signature(obj: Any) -> Panel:  # noqa: ANN401
        """Render callable signature.

        Args:
            obj: The callable object.

        Returns:
            Panel: The signature panel.

        """
        try:
            sig = inspect.signature(obj)
            params = [f"    {param}," for param in sig.parameters.values()]
            params_str = "\n".join(params)
            sig_str = f"(\n{params_str}\n) -> {sig.return_annotation}"
            return Panel(
                Syntax(sig_str, "python", theme="monokai", background_color="default"),
                title="Signature",
                border_style="green",
            )
        except (ValueError, TypeError):
            return Panel(Text("(not available)"), title="Signature", border_style="red")

    @staticmethod
    def _render_docstring(obj: Any) -> Panel | None:  # noqa: ANN401
        """Render docstring if available.

        Args:
            obj: The object to get docstring from.

        Returns:
            Panel | None: The docstring panel if found, else None.

        """
        doc = inspect.getdoc(obj)
        if doc:
            clean_doc = cleandoc(doc)
            return Panel(
                Text(clean_doc, style="italic"),
                title="Docstring",
                border_style="blue",
            )
        return None

    @staticmethod
    def _render_metadata(obj: Any) -> Panel | None:  # noqa: ANN401
        """Render metadata like module and closure.

        Args:
            obj: The object to get metadata from.

        Returns:
            Panel | None: The metadata panel if found, else None.

        """
        metadata = []
        if hasattr(obj, "__module__"):
            metadata.append(Text(f"Module: {obj.__module__}"))
        if hasattr(obj, "__closure__") and obj.__closure__:
            metadata.append(Text(f"Closure Cells: {len(obj.__closure__)}"))

        if metadata:
            return Panel(
                Columns(metadata, padding=(0, 2)),
                title="Metadata",
                border_style="magenta",
            )
        return None


class ObjectInspector:
    """Inspector for general Python objects and instances."""

    highlighter: ReprHighlighter

    def __init__(self) -> None:
        """Initialize the inspector."""
        self.highlighter = ReprHighlighter()

    def __call__(self, obj: Any) -> Group:  # noqa: ANN401
        """Render an object instance preview.

        Args:
            obj: The object to render.

        Returns:
            Group: Rich renderable showing object info.

        """
        sections = []

        # Value preview (if not basic type)
        if self._should_show_value_preview(obj):
            sections.append(
                Panel(
                    Pretty(
                        obj,
                        indent_guides=True,
                        max_length=5,
                        max_string=PREVIEW_LENGTH,
                    ),
                    title="Value Preview",
                    border_style="dim",
                )
            )

        # Categorize members
        attrs, methods = self._categorize_members(obj)

        # Render Attributes
        if attrs:
            sections.append(self._render_member_table(attrs, "Attributes", "cyan"))

        # Render Methods
        if methods:
            sections.append(self._render_member_table(methods, "Methods", "magenta"))

        return Group(*sections)

    @staticmethod
    def _should_show_value_preview(obj: Any) -> bool:  # noqa: ANN401
        """Check if we should show a value preview for the object.

        Args:
            obj: The object.

        Returns:
            bool: True if we should show preview.

        """
        basic_types = (int, float, str, bool, type(None), list, dict, set, tuple)
        return not isinstance(obj, basic_types)

    @staticmethod
    def _categorize_members(
        obj: Any,  # noqa: ANN401
    ) -> tuple[list[tuple[str, Any]], list[tuple[str, Any]]]:
        """Categorize members into attributes and methods.

        Args:
            obj: The object.

        Returns:
            tuple: (attrs, methods)

        """
        attrs: list[tuple[str, Any]] = []
        methods: list[tuple[str, Any]] = []

        for name in dir(obj):
            if name.startswith("_"):
                continue
            try:
                # Use getattr for now, we want actual values
                val = getattr(obj, name)
                if inspect.isroutine(val):
                    methods.append((name, val))
                else:
                    attrs.append((name, val))
            except Exception:  # noqa: BLE001
                attrs.append((name, "[red]Error[/red]"))
        return attrs, methods

    def _render_member_table(
        self, members: list[tuple[str, Any]], title: str, name_style: str
    ) -> Table:
        """Render a table of members.

        Args:
            members: List of (name, value) tuples.
            title: Table title.
            name_style: Style for the name column.

        Returns:
            Table: The rendered table.

        """
        table = Table(
            title=title,
            title_justify="left",
            show_edge=False,
            header_style="bold",
        )
        table.add_column("Member", style=name_style)
        table.add_column("Type", style="dim")
        table.add_column("Value/Preview")

        for name, val in members:
            type_name = type(val).__name__ if not isinstance(val, str) else "error"
            if inspect.isroutine(val):
                preview = self._get_method_preview(val)
            else:
                preview = self.highlighter(self._get_value_preview(val))
            table.add_row(name, type_name, preview)

        return table

    @staticmethod
    def _get_method_preview(val: Any) -> Text:  # noqa: ANN401
        """Get a preview for a method.

        Args:
            val: The method.

        Returns:
            Text: The preview text.

        """
        try:
            sig = inspect.signature(val)
            return Text(f"def {sig}", style="green")
        except (ValueError, TypeError):
            return Text("def (...)", style="green")

    @staticmethod
    def _get_value_preview(val: Any) -> str:  # noqa: ANN401
        """Get a string preview of a value.

        Args:
            val: The value.

        Returns:
            str: The preview string.

        """
        if isinstance(val, str) and val.startswith("[red]"):
            return val
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

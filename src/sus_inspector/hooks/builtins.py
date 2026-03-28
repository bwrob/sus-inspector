"""Built-in view hooks for common Python types."""

from __future__ import annotations

from rich.table import Table


def list_view(obj: list[object]) -> Table:
    """Render a list as a Rich Table.

    Args:
        obj: The list object to render.

    Returns:
        Table: Rich table representation.

    """
    max_preview_items = 100
    max_preview_length = 80
    title = f"List (length: {len(obj)})"
    table = Table(title=title, title_justify="left", show_edge=False)
    table.add_column("Index", justify="right", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Preview")

    for i, item in enumerate(obj[:max_preview_items]):
        item_str = str(item)
        preview = (
            item_str[:max_preview_length] + "..."
            if len(item_str) > max_preview_length
            else item_str
        )
        table.add_row(str(i), type(item).__name__, preview)

    if len(obj) > max_preview_items:
        rem = len(obj) - max_preview_items
        table.add_row("...", "...", f"...and {rem} more items")

    return table

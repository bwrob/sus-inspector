"""Built-in view hooks for common Python types."""

from __future__ import annotations

from typing import cast

from rich.table import Table


def list_view(obj: object) -> Table:
    """Render a list as a Rich Table.

    Args:
        obj: The list object to render.

    Returns:
        Table: Rich table representation.

    """
    if not isinstance(obj, list):
        # This shouldn't happen if type checker is correct
        return Table(title="Not a list")

    obj_list = cast("list[object]", obj)
    max_preview_items = 100
    max_preview_length = 80
    title = f"List (length: {len(obj_list)})"
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

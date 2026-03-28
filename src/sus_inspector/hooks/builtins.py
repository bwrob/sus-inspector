"""Built-in view hooks for common Python types."""

from __future__ import annotations

from typing import Any

from rich.table import Table


def list_view(obj: list[Any]) -> Table:
    """Render a list as a Rich Table."""
    max_preview_items = 100
    table = Table(
        title=f"List (length: {len(obj)})", title_justify="left", show_edge=False
    )
    table.add_column("Index", justify="right", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Preview")

    for i, item in enumerate(obj[:max_preview_items]):
        preview = str(item)[:80] + "..." if len(str(item)) > 80 else str(item)
        table.add_row(str(i), type(item).__name__, preview)

    if len(obj) > max_preview_items:
        table.add_row("...", "...", f"...and {len(obj) - max_preview_items} more items")

    return table

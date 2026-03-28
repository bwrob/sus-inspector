"""Optional Pydantic view hooks."""

from __future__ import annotations

from typing import Any

from rich.console import Group
from rich.pretty import Pretty
from rich.text import Text


def pydantic_view(obj: Any) -> Group:
    """Render a Pydantic model by serializing its data."""
    data = obj.model_dump() if hasattr(obj, "model_dump") else obj.dict()
    return Group(
        Text(f"Pydantic Model: {type(obj).__name__}", style="bold yellow"),
        Text("Serialized Data:", style="italic dim"),
        Pretty(data, expand_all=True),
    )

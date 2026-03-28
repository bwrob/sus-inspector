"""Optional Pydantic view hooks."""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

from rich.console import Group
from rich.pretty import Pretty
from rich.text import Text

if TYPE_CHECKING:
    from pydantic import BaseModel
    from rich.console import RenderableType

with contextlib.suppress(ImportError):
    pass


def pydantic_view(obj: BaseModel) -> RenderableType:
    """Render a Pydantic model by serializing its data.

    Args:
        obj: The model to serialize.

    Returns:
        RenderableType: Rich renderable showing serialized data.

    """
    model_name = type(obj).__name__
    return Group(
        Text(f"Pydantic Model: {model_name}", style="bold yellow"),
        Text("Serialized Data:", style="italic dim"),
        Pretty(obj, expand_all=True),
    )

"""Tests for Pydantic view hooks."""

from __future__ import annotations

from pydantic import BaseModel
from rich.console import Console, Group

from sus_inspector.hooks.pydantic import pydantic_view


def test_pydantic_view() -> None:
    """pydantic_view should render a BaseModel."""

    class User(BaseModel):
        id: int
        name: str

    user = User(id=1, name="Alice")
    renderable = pydantic_view(user)
    assert isinstance(renderable, Group)

    # Use a console to render to string to check content
    console = Console(width=80, force_terminal=False)
    with console.capture() as capture:
        console.print(renderable)
    content = capture.get()

    assert "User" in content
    assert "Alice" in content

"""Tests for Pydantic specialized handler."""

from __future__ import annotations

from typing import Any, Final, cast

from pydantic import BaseModel
from rich.console import Group

from sus_inspector.hooks.pydantic import PydanticHandler, pydantic_view

F_COUNT_12: Final = 12


class User(BaseModel):
    """Pydantic model for testing."""

    id: int
    name: str


class LargeModel(BaseModel):
    """Large Pydantic model for testing."""

    f0: int = 0
    f1: int = 1
    f2: int = 2
    f3: int = 3
    f4: int = 4
    f5: int = 5
    f6: int = 6
    f7: int = 7
    f8: int = 8
    f9: int = 9
    f10: int = 10
    f11: int = 11


def test_pydantic_handler_can_handle() -> None:
    """Test can_handle method."""
    handler = PydanticHandler()
    user = User(id=1, name="Alice")

    assert handler.can_handle(user) is True
    assert handler.can_handle({"id": 1}) is False
    assert handler.can_handle(User) is False


def test_pydantic_handler_get_type_tag() -> None:
    """Test get_type_tag method."""
    handler = PydanticHandler()
    user = User(id=1, name="Alice")
    assert handler.get_type_tag(user) == "Pydantic"


def test_pydantic_handler_get_fields() -> None:
    """Test get_fields method."""
    handler = PydanticHandler()
    user = User(id=1, name="Alice")
    fields = handler.get_fields(user)
    assert fields == {"id": 1, "name": "Alice"}


def test_pydantic_handler_render() -> None:
    """Test render method."""
    handler = PydanticHandler()
    user = User(id=1, name="Alice")
    renderable = handler.render(user)
    assert isinstance(renderable, Group)

    # Complex object
    large = LargeModel()
    renderable_complex = handler.render(large, expanded=False)
    assert isinstance(renderable_complex, Group)
    group = cast("Any", renderable_complex)
    assert f"({F_COUNT_12} fields) ..." in str(group.renderables[1])


def test_pydantic_view_wrapper() -> None:
    """Test the compatibility wrapper."""
    user = User(id=1, name="Alice")
    renderable = pydantic_view(user)
    assert isinstance(renderable, Group)

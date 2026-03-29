from typing import Any
from rich.text import Text
from sus_inspector.hooks.registry import (
    INSTANCE_HOOKS,
    CLASS_HOOKS,
    register_instance_hook,
    register_class_hook,
    get_renderer,
)


def test_double_registry_lookup():
    """Test that instance and class registries can have different hooks."""

    class MyType:
        pass

    def instance_renderer(obj: Any):
        return Text("Instance")

    def class_renderer(obj: Any):
        return Text("Class")

    # Clear hooks for test
    INSTANCE_HOOKS.clear()
    CLASS_HOOKS.clear()

    register_instance_hook(MyType, instance_renderer)
    register_class_hook(MyType, class_renderer)

    obj = MyType()

    # Test instance lookup
    inst_render = get_renderer(obj, INSTANCE_HOOKS)
    assert inst_render == instance_renderer
    assert inst_render(obj).plain == "Instance"

    # Test class lookup
    class_render = get_renderer(obj, CLASS_HOOKS)
    assert class_render == class_renderer
    assert class_render(obj).plain == "Class"


def test_fallback_logic():
    """Test that fallback works correctly (returns None if no hook)."""

    class MyType:
        pass

    INSTANCE_HOOKS.clear()
    CLASS_HOOKS.clear()

    obj = MyType()
    assert get_renderer(obj, INSTANCE_HOOKS) is None
    assert get_renderer(obj, CLASS_HOOKS) is None

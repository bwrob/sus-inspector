"""Hook system for custom object renderers."""

from __future__ import annotations

from sus_inspector.hooks.registry import (
    CLASS_HOOKS,
    INSTANCE_HOOKS,
    VIEW_HOOKS,
    register_class_hook,
    register_hook,
    register_instance_hook,
)

__all__ = [
    "CLASS_HOOKS",
    "INSTANCE_HOOKS",
    "VIEW_HOOKS",
    "register_class_hook",
    "register_hook",
    "register_instance_hook",
]

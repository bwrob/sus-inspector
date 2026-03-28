"""Hook system for custom object renderers."""

from __future__ import annotations

from sus_inspector.hooks.registry import VIEW_HOOKS, register_hook

__all__ = ["VIEW_HOOKS", "register_hook"]

"""sus-inspector: The interactive, terminal-based object inspector.

This module provides the core TUI and operator-overloading logic for inspecting
suspicious Python objects during debugging.
"""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any

from rich._inspect import Inspect
from rich.console import Group, RenderableType
from rich.pretty import Pretty
from rich.table import Table
from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Footer, Header, Input, Static, Tree

if TYPE_CHECKING:
    from collections.abc import Callable

    from textual.widgets.tree import TreeNode

# --- Optional Pydantic Support ---
try:
    from pydantic import BaseModel

    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False


# --- 1. Define the Hook System ---
# Type for hook registry: list of (type_checker_func, render_func)
VIEW_HOOKS: list[
    tuple[type | Callable[[Any], bool], Callable[[Any], RenderableType]]
] = []


def register_hook(
    type_checker: type | Callable[[Any], bool],
    render_func: Callable[[Any], RenderableType],
) -> None:
    """Register a custom view for a specific object type.

    Args:
        type_checker: A type or a function that returns True if the object matches.
        render_func: A function that takes the object and returns a Rich renderable.

    """
    VIEW_HOOKS.insert(0, (type_checker, render_func))


# --- Custom View Functions ---
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


def pydantic_view(obj: Any) -> Group:
    """Render a Pydantic model by serializing its data."""
    data = obj.model_dump() if hasattr(obj, "model_dump") else obj.dict()
    return Group(
        Text(f"Pydantic Model: {type(obj).__name__}", style="bold yellow"),
        Text("Serialized Data:", style="italic dim"),
        Pretty(data, expand_all=True),
    )


# Register default hooks
register_hook(list, list_view)
if HAS_PYDANTIC:
    register_hook(BaseModel, pydantic_view)


# --- 2. The Textual App ---
class ObjectExplorerApp(App[None]):
    """Textual TUI for exploring Python objects."""

    CSS = """
    #tree-pane {
        width: 30%;
        border: solid $primary;
    }
    #detail-pane {
        width: 70%;
        border: solid $secondary;
    }
    #path-bar {
        dock: bottom;
        background: $accent;
    }
    #search-bar {
        dock: bottom;
        display: none;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "quit", "Quit"),
        ("/", "search", "Search Tree"),
    ]

    def __init__(self, obj: Any, obj_name: str = "root", **kwargs: Any) -> None:
        """Initialize the object explorer app.

        Args:
            obj: The object to inspect.
            obj_name: The name of the root object for the tree display.
            **kwargs: Additional arguments for the Textual App.

        """
        super().__init__(**kwargs)
        self.root_obj = obj
        self.root_name = obj_name

    def compose(self) -> ComposeResult:
        """Compose the UI layout."""
        yield Header(show_clock=True, icon="🔍")

        with Horizontal():
            tree: Tree[Any] = Tree(self.root_name, id="tree-pane")
            tree.border_title = "Object Tree"
            yield tree

            with VerticalScroll(id="detail-pane") as vs:
                vs.border_title = "Inspection View"
                vs.border_subtitle = "Select an item..."
                yield Static("Select a node to inspect...", id="detail-view")

        yield Static(f"Path: {self.root_name}", id="path-bar")
        yield Input(
            placeholder="Search keys (Press Enter to find next)...", id="search-bar"
        )
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the tree root."""
        tree = self.query_one(Tree)
        tree.root.data = self.root_obj
        self.add_children(tree.root, self.root_obj)
        tree.root.expand()
        tree.focus()

    def action_search(self) -> None:
        """Triggered by pressing '/' to show the search bar."""
        search_bar = self.query_one("#search-bar", Input)
        search_bar.display = True
        search_bar.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle search queries."""
        query = event.value.lower()
        tree = self.query_one(Tree)
        search_bar = self.query_one("#search-bar", Input)

        def find_node(node: TreeNode[Any], search_term: str) -> TreeNode[Any] | None:
            if search_term in str(node.label).lower() and node != tree.root:
                return node
            for child in node.children:
                found = find_node(child, search_term)
                if found:
                    return found
            return None

        found_node = find_node(tree.root, query)

        if found_node:
            curr = found_node.parent
            while curr:
                curr.expand()
                curr = curr.parent
            tree.select_node(found_node)
            tree.scroll_to_node(found_node)

        search_bar.display = False
        search_bar.value = ""
        tree.focus()

    def add_children(self, node: TreeNode[Any], obj: Any) -> None:
        """Recursively add children to a tree node based on object attributes/keys."""
        try:
            if isinstance(obj, dict):
                for k, v in obj.items():
                    node.add(str(k), data=v, allow_expand=self._is_expandable(v))
            elif isinstance(obj, (list, tuple, set)):
                for i, v in enumerate(obj):
                    node.add(f"[{i}]", data=v, allow_expand=self._is_expandable(v))
            else:
                for attr_name in dir(obj):
                    if not attr_name.startswith("_"):
                        try:
                            attr_value = getattr(obj, attr_name)
                            node.add(
                                attr_name,
                                data=attr_value,
                                allow_expand=self._is_expandable(attr_value),
                            )
                        except (AttributeError, Exception):
                            # Skip attributes that can't be accessed
                            continue
        except Exception:
            # General fallback if object exploration fails
            pass

    def _is_expandable(self, obj: Any) -> bool:
        """Check if an object can have children in the tree."""
        if isinstance(obj, (dict, list, tuple, set)):
            return len(obj) > 0
        return bool(hasattr(obj, "__dict__")) or bool(hasattr(obj, "__slots__"))

    def on_tree_node_expanded(self, event: Tree.NodeExpanded[Any]) -> None:
        """Lazy-load children when a node is expanded."""
        if event.node.data is not None and not event.node.children:
            self.add_children(event.node, event.node.data)

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted[Any]) -> None:
        """Update the detail view when a node is selected."""
        detail_view = self.query_one("#detail-view", Static)
        detail_pane = self.query_one("#detail-pane")
        path_bar = self.query_one("#path-bar", Static)
        obj = event.node.data

        # --- Update the Tree Path Bar ---
        path_segments = []
        curr = event.node
        while curr and curr.parent:
            path_segments.insert(0, str(curr.label))
            curr = curr.parent

        full_path = self.root_name
        for p in path_segments:
            if p.startswith("["):
                full_path += p
            else:
                full_path += f".{p}"

        path_bar.update(f"Path: {full_path}")

        # --- Handle the Data View ---
        if obj is None:
            detail_pane.border_subtitle = "NoneType"
            detail_view.update("No data.")
            return

        detail_pane.border_subtitle = f"Type: {type(obj).__name__}"

        for type_checker, render_func in VIEW_HOOKS:
            matches = (
                isinstance(obj, type_checker)
                if isinstance(type_checker, type)
                else type_checker(obj)
            )
            if matches:
                try:
                    detail_view.update(render_func(obj))
                    return
                except Exception:
                    continue

        # Fallback to rich.inspect
        detail_view.update(Inspect(obj, methods=True, help=True, value=True))


# --- 3. The Magic Syntax ---
class InteractiveExplorer:
    """The main 'sus' interface supporting both calls and operator overloading."""

    def __call__(self, obj: Any, name: str = "root") -> Any:
        """Standard call: sus(obj, name='my_obj')."""
        self._run(obj, name)
        return obj

    def __truediv__(self, obj: Any) -> Any:
        """Operator overloading: sus / obj."""
        if obj is Ellipsis:
            # Capture local variables from the caller's frame
            frame = inspect.currentframe().f_back
            if frame:
                local_vars = {
                    k: v for k, v in frame.f_locals.items() if not k.startswith("__")
                }
                self._run(local_vars, "locals")
            return None

        name = (
            str(type(obj).__name__)
            if not hasattr(obj, "__name__")
            else str(obj.__name__)
        )
        self._run(obj, name)
        return obj

    def _run(self, obj: Any, name: str) -> None:
        """Start the Textual App."""
        app = ObjectExplorerApp(obj, obj_name=name)
        app.run()


sus = InteractiveExplorer()

# --- Example Usage ---
if __name__ == "__main__":

    def simulate_buggy_api() -> None:
        """Example function to demonstrate usage."""
        response_payload = {
            "metadata": {"status": 200, "latency_ms": 42},
            "data": {
                "users": [
                    {"id": 1, "name": "Alice", "role": "admin"},
                    {
                        "id": 2,
                        "name": "Bob",
                        "role": "user",
                        "nested_secret": {"token": "xyz123"},
                    },
                ]
            },
        }

        # Inspect the object
        sus / response_payload

    simulate_buggy_api()

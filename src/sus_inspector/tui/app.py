"""The main Textual UI application for object exploration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rich._inspect import Inspect
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Footer, Header, Input, Static, Tree

from sus_inspector.hooks import VIEW_HOOKS

if TYPE_CHECKING:
    from textual.widgets.tree import TreeNode


class ObjectExplorerApp(App[None]):
    """Textual TUI for exploring Python objects."""

    CSS_PATH = "styles.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "quit", "Quit"),
        ("/", "search", "Search Tree"),
    ]

    def __init__(self, obj: Any, obj_name: str = "root", **kwargs: Any) -> None:
        """Initialize the object explorer app."""
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
                            continue
        except Exception:
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

        detail_view.update(Inspect(obj, methods=True, help=True, value=True))

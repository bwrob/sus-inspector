import inspect

from rich._inspect import Inspect
from rich.console import Group
from rich.pretty import Pretty
from rich.table import Table
from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Footer, Header, Input, Static, Tree

# --- Optional Pydantic Support ---
try:
    from pydantic import BaseModel

    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False


# --- 1. Define the Hook System ---
VIEW_HOOKS = []


def register_hook(type_checker, render_func) -> None:
    """Register a custom view for a specific object type."""
    VIEW_HOOKS.insert(0, (type_checker, render_func))


# --- Custom View Functions ---
def list_view(obj: list):
    table = Table(
        title=f"List (length: {len(obj)})", title_justify="left", show_edge=False
    )
    table.add_column("Index", justify="right", style="#66D9EF")  # Monokai Blue
    table.add_column("Type", style="#F92672")  # Monokai Pink
    table.add_column("Preview", style="#A6E22E")  # Monokai Green

    for i, item in enumerate(obj[:100]):
        preview = str(item)[:80] + "..." if len(str(item)) > 80 else str(item)
        table.add_row(str(i), type(item).__name__, preview)

    if len(obj) > 100:
        table.add_row("...", "...", f"...and {len(obj) - 100} more items")

    return table


def pydantic_view(obj):
    data = obj.model_dump() if hasattr(obj, "model_dump") else obj.dict()
    return Group(
        Text(
            f"Pydantic Model: {type(obj).__name__}", style="bold #E6DB74"
        ),  # Monokai Yellow
        Text("Serialized Data:", style="italic dim"),
        Pretty(data, expand_all=True),
    )


register_hook(list, list_view)
if HAS_PYDANTIC:
    register_hook(BaseModel, pydantic_view)


# --- 2. The Textual App ---
class ObjectExplorerApp(App):
    # Monokai Inspired Theme
    CSS = """
    Screen {
        background: #272822;
        color: #F8F8F2;
    }
    #tree-pane {
        width: 35%;
        border: round #A6E22E; /* Monokai Green */
        background: #272822;
        margin: 0 1 0 1;
    }
    #tree-pane:focus {
        border: round #F92672; /* Monokai Pink on focus */
    }
    #detail-pane {
        width: 65%;
        border: round #66D9EF; /* Monokai Blue */
        background: #272822;
        padding: 1 2;
        margin: 0 1 0 0;
    }
    #path-bar {
        dock: bottom;
        width: 100%;
        height: 1;
        background: #3E3D32; /* Monokai Dark Gray */
        color: #E6DB74;      /* Monokai Yellow */
        padding: 0 2;
        text-style: bold;
    }
    #search-bar {
        dock: bottom;
        width: 100%;
        display: none;
        border-top: solid #F92672;
        background: #272822;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "quit", "Quit"),
        ("/", "search", "Search Tree"),
    ]

    def __init__(self, obj, obj_name="root", **kwargs) -> None:
        super().__init__(**kwargs)
        self.root_obj = obj
        self.root_name = obj_name

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, icon="🔍")

        with Horizontal():
            tree = Tree(self.root_name, id="tree-pane")
            tree.border_title = "Object Tree"
            yield tree

            with VerticalScroll(id="detail-pane") as vs:
                vs.border_title = "Inspection View"
                vs.border_subtitle = "Select an item..."
                yield Static("Select a node to inspect...", id="detail-view")

        # New bottom UI elements
        yield Static(f"Path: {self.root_name}", id="path-bar")
        yield Input(
            placeholder="Search keys (Press Enter to find next)...", id="search-bar"
        )
        yield Footer()

    def on_mount(self) -> None:
        tree = self.query_one(Tree)
        tree.root.data = self.root_obj
        self.add_children(tree.root, self.root_obj)
        tree.root.expand()
        tree.focus()

    def action_search(self) -> None:
        """Triggered by pressing '/'."""
        search_bar = self.query_one("#search-bar", Input)
        search_bar.display = True
        search_bar.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handles hitting Enter in the search bar."""
        query = event.value.lower()
        tree = self.query_one(Tree)
        search_bar = self.query_one("#search-bar", Input)

        # Simple Recursive Search on loaded nodes
        def find_node(node, search_term):
            if search_term in str(node.label).lower() and node != tree.root:
                return node
            for child in node.children:
                found = find_node(child, search_term)
                if found:
                    return found
            return None

        found_node = find_node(tree.root, query)

        if found_node:
            # Expand parent nodes so it's visible
            curr = found_node.parent
            while curr:
                curr.expand()
                curr = curr.parent
            # Move cursor and focus
            tree.select_node(found_node)
            tree.scroll_to_node(found_node)

        # Hide search bar and return control to the tree
        search_bar.display = False
        search_bar.value = ""
        tree.focus()

    def add_children(self, node, obj) -> None:
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
                        except Exception:
                            pass
        except Exception:
            pass

    def _is_expandable(self, obj) -> bool:
        if isinstance(obj, (dict, list, tuple, set)):
            return len(obj) > 0
        return bool(hasattr(obj, "__dict__"))

    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        if event.node.data is not None and not event.node.children:
            self.add_children(event.node, event.node.data)

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
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
                full_path += p  # Array indices (e.g., [0]) don't get a dot
            else:
                full_path += f".{p}"  # Dicts and attributes get a dot

        path_bar.update(f"Path: {full_path}")

        # --- Handle the Data View ---
        if obj is None:
            detail_pane.border_subtitle = "NoneType"
            detail_view.update("No data.")
            return

        detail_pane.border_subtitle = f"Type: {type(obj).__name__}"

        for type_checker, render_func in VIEW_HOOKS:
            if isinstance(obj, type_checker):
                try:
                    detail_view.update(render_func(obj))
                    return
                except Exception:
                    pass

        detail_view.update(Inspect(obj, methods=True, help=True, value=True))


# --- 3. The Magic Syntax ---
class InteractiveExplorer:
    def __call__(self, obj, name="root"):
        self._run(obj, name)

    def __truediv__(self, obj):
        if obj is Ellipsis:
            frame = inspect.currentframe().f_back
            local_vars = {
                k: v for k, v in frame.f_locals.items() if not k.startswith("__")
            }
            self._run(local_vars, "locals")
            return None

        self._run(
            obj,
            str(type(obj).__name__) if not hasattr(obj, "__name__") else obj.__name__,
        )
        return obj

    def _run(self, obj, name) -> None:
        app = ObjectExplorerApp(obj, obj_name=name)
        app.run()


sus = InteractiveExplorer()

# --- Example Usage ---
if __name__ == "__main__":

    def simulate_buggy_api() -> None:
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

        # Give it a test drive!
        # 1. Use arrow keys to expand data -> users -> [1] -> nested_secret -> token
        # 2. Watch the yellow Path bar at the bottom update perfectly.
        # 3. Press `/`, type 'token', and press Enter to instantly find it.
        sus / response_payload

    simulate_buggy_api()

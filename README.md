# 🔍 sus-inspector

The interactive, terminal-based object inspector for suspicious Python objects.

`sus-inspector` bridges the gap between the instant gratification of `icecream` and the deep introspection of `wat`. When an object in your code is acting suspicious, you don't need a heavy IDE debugger—you just need to poke it, search it, and see what's inside.

Powered by **Textual** and **Rich**.

---

## 🧠 Philosophy

*   **Zero Friction**: Inspecting an object should take exactly one line of code and zero setup.
*   **Keyboard First**: Navigating deep API responses or nested classes should be as fast as playing a terminal game.
*   **Beautiful by Default**: Data is easier to read when it's formatted well. `sus` uses a high-contrast Monokai-inspired theme, rich tables, and syntax highlighting.
*   **Extensible**: You can teach the debugger how to render your custom data models.

---

## 📦 Installation

```bash
pip install sus-inspector
```

*(Note: Requires `textual` and `rich`. `pydantic` is natively supported if installed.)*

---

## 🪄 The Magic Syntax

Import the global `sus` instance and drop it anywhere in your code. It blocks execution, opens the TUI, and returns the object completely untouched when you exit.

### 1. The Quick Inspect (`/`)

Borrowed from the brilliant `wat` inspector, the division operator allows for lightning-fast typing.

```python
from sus_inspector import sus
import requests

response = requests.get("https://api.github.com")

# Inspect the suspicious response
sus / response
```

### 2. The Local Scope Sweep (`...`)

Want to know everything that is happening in the current function? Pass the Ellipsis (`...`) to instantly inspect all local variables in the caller's frame.

```python
def calculate_payout(user_id):
    base_score = 42
    multiplier = 1.5
    
    # Wait, something is wrong here... 
    sus / ...  
    
    return base_score * multiplier
```

### 3. Standard Call

If operator overloading isn't your style, it works like a normal function, too:

```python
sus(my_data, name="My API Payload")
```

---

## 🎮 UI Features

*   **Split-Pane Exploration**: Navigate the object tree on the left (Arrow Keys); view deep, rich details on the right.
*   **Smart Lazy-Loading**: Only parses nested dictionaries, lists, or class attributes when you expand them, preventing terminal freezes on massive objects.
*   **Breadcrumb Path Bar**: A live tracker at the bottom shows your exact traversal path (e.g., `dict.data.users[1].metadata.token`).
*   **Fuzzy Search (`/`)**: Press `/` to open the search bar. Type a key, press Enter, and the tree will automatically expand and jump to the first matching node.

---

## 🛠️ Extensibility (Custom View Hooks)

`sus` comes with a plugin system so you can define exactly how specific data types should be rendered in the Detail View.

By default, it uses `rich.inspect`, but it ships with native hooks for `list` (rendered as a truncated table) and `pydantic.BaseModel` (rendered as a serialized JSON tree).

You can easily register your own:

```python
from sus_inspector import sus, register_hook
from rich.panel import Panel
import pandas as pd

def pandas_view(df: pd.DataFrame):
    """Custom view to render Pandas DataFrames cleanly."""
    summary = f"Shape: {df.shape}\nColumns: {list(df.columns)}"
    return Panel(summary, title="Pandas DataFrame", border_style="cyan")

# Teach sus how to handle DataFrames!
register_hook(pd.DataFrame, pandas_view)

sus / my_messy_dataframe
```

---

## 🏗️ Architecture

To move from a single-file prototype to a maintainable package, the codebase will be split into the following structure:

```text
sus-inspector/
├── pyproject.toml
└── src/sus_inspector/
    ├── __init__.py       # Exports `sus`, `register_hook`
    ├── core.py           # Contains the `InteractiveExplorer` class and operator magic
    ├── tui/
    │   ├── app.py        # Textual UI application
    │   ├── styles.tcss   # External styles
    │   └── widgets.py    # Custom widgets
    ├── search.py         # Search logic
    └── hooks/
        ├── __init__.py   # Hook registry
        ├── builtins.py   # list, dict, set renderers
        └── pydantic.py   # Pydantic support
```

---

## 🗺️ Current Roadmap

- [x] Operator Overloading API (`sus / obj`)
- [x] Local Frame Inspection (`sus / ...`)
- [x] Basic Search functionality
- [ ] Refactor prototype into modular architecture
- [ ] Visual toggle (`d`) to show/hide private `__dunder__` methods
- [ ] Support for evaluating simple expressions in search bar

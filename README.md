# sus-inspector
Debugging inspector. Is this object sus?

## 🔍 sus-debug

The interactive, terminal-based object inspector for suspicious Python objects.

sus bridges the gap between the instant gratification of icecream and the deep introspection of wat. When an object in your code is acting suspicious, you don't need a heavy IDE debugger—you just need to poke it, search it, and see what's inside.

Powered by textual and rich.

## 🧠 Philosophy

Zero Friction: Inspecting an object should take exactly one line of code and zero setup.

Keyboard First: Navigating deep API responses or nested classes should be as fast as playing a terminal game.

Beautiful by Default: Data is easier to read when it's formatted well. sus uses a high-contrast Monokai theme, rich tables, and syntax highlighting.

Extensible: You should be able to teach the debugger how to render your company's custom data models.

## 📦 Installation

pip install sus-debug


(Note: Requires textual and rich. pydantic is natively supported if installed.)

## 🪄 The Magic Syntax

Import the global sus instance and drop it anywhere in your code. It blocks execution, opens the TUI, and returns the object completely untouched when you exit.

1. The Quick Inspect (/)

Borrowed from the brilliant wat inspector, the division operator allows for lightning-fast typing.

from sus import sus
import requests

response = requests.get("[https://api.github.com](https://api.github.com)")

Inspect the suspicious response
sus / response


2. The Local Scope Sweep (...)

Want to know everything that is happening in the current function? Pass the Ellipsis (...) to instantly inspect all local variables in the caller's frame.

def calculate_payout(user_id):
    base_score = 42
    multiplier = 1.5
    
    # Wait, something is wrong here... 
    sus / ...  
    
    return base_score * multiplier


3. Standard Call

If operator overloading isn't your style, it works like a normal function, too:

sus(my_data, name="My API Payload")


## 🎮 UI Features

Split-Pane Exploration: Navigate the object tree on the left (Arrow Keys); view deep, rich details on the right.

Smart Lazy-Loading: Only parses nested dictionaries, lists, or class attributes when you expand them, preventing terminal freezes on massive objects.

Breadcrumb Path Bar: A live tracker at the bottom shows your exact traversal path (e.g., dict.data.users[1].metadata.token).

Fuzzy Search (/): Press / to open the search bar. Type a key, press Enter, and the tree will automatically expand and jump to the first matching node.

## 🛠️ Extensibility (Custom View Hooks)

sus comes with a plugin system so you can define exactly how specific data types should be rendered in the Detail View.

By default, it uses rich.inspect, but it ships with native hooks for list (rendered as a truncated table) and pydantic.BaseModel (rendered as a serialized JSON tree).

You can easily register your own:

from sus import sus, register_hook
from rich.panel import Panel
import pandas as pd

def pandas_view(df: pd.DataFrame):
    """Custom view to render Pandas DataFrames cleanly."""
    summary = f"Shape: {df.shape}\nColumns: {list(df.columns)}"
    return Panel(summary, title="Pandas DataFrame", border_style="cyan")

Teach sus how to handle DataFrames!
register_hook(pd.DataFrame, pandas_view)

sus / my_messy_dataframe


# 🏗️ Development Context (For AI Prompting & Contributors)

(Note: This section is to guide the architecture as the project scales out of a single file).

Target Architecture

To move from sus.py to a maintainable package, the codebase should be split into the following structure:

sus-debug/
├── pyproject.toml
└── sus/
    ├── __init__.py       # Exports `sus`, `register_hook`
    ├── core.py           # Contains the `InteractiveExplorer` class and operator magic
    ├── tui.py            # Contains the `ObjectExplorerApp` Textual UI definitions
    ├── search.py         # Logic for the tree traversal/search algorithm
    └── hooks/
        ├── __init__.py   # Hook registry (`VIEW_HOOKS`)
        ├── builtins.py   # `list`, `dict`, `set` renderers
        └── pydantic.py   # Safe-imported Pydantic renderers


Current Roadmap

[x] Operator Overloading API (sus / obj)

[x] Local Frame Inspection (sus / ...)

[x] Basic Search functionality

[ ] Next: Refactor single-file sus.py into the modular architecture above.

[ ] Add a visual toggle (e.g., pressing d) to show/hide private __dunder__ methods in the tree.

[ ] Add support for evaluating simple expressions in the search bar.
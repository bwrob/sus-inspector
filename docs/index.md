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

## 📦 Quick Start

```python
from sus_inspector import sus
import requests

response = requests.get("https://api.github.com")

# Inspect the suspicious response
sus / response
```

---

## 🎮 UI Features

*   **Split-Pane Exploration**: Navigate the object tree on the left (Arrow Keys); view deep, rich details on the right.
*   **Smart Lazy-Loading**: Only parses nested dictionaries, lists, or class attributes when you expand them, preventing terminal freezes on massive objects.
*   **Breadcrumb Path Bar**: A live tracker at the bottom shows your exact traversal path (e.g., `dict.data.users[1].metadata.token`).
*   **Fuzzy Search (`/`)**: Press `/` to open the search bar. Type a key, press Enter, and the tree will automatically expand and jump to the first matching node.

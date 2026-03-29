# Getting Started

## 📦 Installation

Install `sus-inspector` using `pip`:

```bash
pip install sus-inspector
```

*(Note: Requires `textual` and `rich`. `pydantic` is natively supported if installed.)*

---

## 🪄 Usage

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

## 💉 Zero-Import Mode (Global Injection)

You can make `sus` available globally in your environment (no import needed) by running:

```bash
# Targets the active virtual environment (recommended)
sus --inject

# Targets the global user-site (available in all projects)
sus --inject --global
```

This will safely add `sus` to your `builtins`. To undo this, run:

```bash
sus --remove
# or
sus --remove --global
```

# Specification: Visual Toggle ('d') and Smart Tree Grouping

## Overview
Currently, the object inspector shows all attributes and methods in a flat list. This feature adds a toggle for private members and implements a "Smart Grouping" system to handle complex objects like Pydantic models or large classes.

## Functional Requirements
- **Key Binding ('d'):** Toggle visibility of members starting with `_`.
- **Smart Grouping (Threshold = 10):**
    - If total members < 10: Display in a flat list (Sorted: Fields then Methods).
    - If total members >= 10: Group into "📁 Fields (N)" and "📁 Methods (M)" virtual nodes.
- **Auto-Expand:** The "Fields" virtual node should be auto-expanded upon the first visit to the object.
- **Visual Cues:**
    - Fields: Prefixed with `• ` and styled in `cyan`.
    - Methods: Prefixed with `ƒ ` and styled in `magenta`.
- **Boilerplate Filtering:** When `show_private` is OFF, specifically hide common library noise (e.g., Pydantic internal dunders).

## Technical Details
- **Categorization:** Use `inspect.isroutine()` to identify behavior vs state.
- **Tree Refresh:** Toggling 'd' must clear and re-populate the current node's children to reflect the new filter/grouping.
- **State:** `show_private: bool` (default False), `grouping_threshold: int` (default 10).

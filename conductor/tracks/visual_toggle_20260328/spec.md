# Specification: Visual Toggle ('d') and Tree Grouping

## Overview
Currently, the object inspector shows all attributes and methods of an object in a single flat list within the selection tree. This can lead to a cluttered view, especially with many `__dunder__` methods and mixed member types. This feature will add:
1.  A toggle (mapped to the 'd' key) to show or hide private (prefixed with `_` or `__`) members.
2.  A structural separation of **Fields** (attributes) and **Methods** into distinct sub-nodes in the selection tree to improve scannability.

## User Story
As a developer, I want to toggle the visibility of private members and see fields separated from methods so that I can quickly navigate the public API and distinguish state from behavior.

## Functional Requirements
- **Key Binding (Private Toggle):** Pressing 'd' in the TUI will toggle the visibility of private and `__dunder__` members in the object tree.
- **Tree Grouping:** Members of an object should be grouped into "Fields" and "Methods" virtual folders in the tree.
- **Visual Feedback:** The TUI should indicate whether private members are currently hidden or shown (e.g., in the footer or a status bar).
- **Default State:**
    - Private members: **Hidden** by default.
    - Grouping: **Enabled** by default.
- **Persistence:** The toggle state should persist across different object inspections during the same session.

## Non-Functional Requirements
- **Performance:** Toggling and grouping should be fast, utilizing lazy-loading of tree nodes.
- **Consistency:** The grouping and filtering should apply recursively to all objects in the tree.

## Technical Details
- **TUI Framework:** Textual.
- **Tree Widget (`ObjectExplorerApp`):**
    - Update `add_children` to handle grouping logic.
    - Use `inspect.isroutine` to distinguish methods from fields.
    - Implement filtering logic based on the `show_private` flag.
- **State Management:** Add `show_private` (bool) and `group_members` (bool) flags to the `ObjectExplorerApp` class.

## Acceptance Criteria
- [ ] Pressing 'd' toggles visibility of members starting with `_`.
- [ ] Objects in the tree have "Fields" and "Methods" sub-nodes.
- [ ] Private methods/fields are hidden when the toggle is OFF.
- [ ] The tree correctly re-renders when the toggle is changed.

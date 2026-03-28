# Specification: Visual Toggle ('d') to Show/Hide Private Methods

## Overview
Currently, the object inspector shows all attributes and methods of an object. This can lead to a cluttered view, especially with Python's many `__dunder__` methods. This feature will add a toggle (mapped to the 'd' key) to show or hide private (prefixed with `_` or `__`) methods in the TUI.

## User Story
As a developer, I want to toggle the visibility of private methods so that I can focus on the public API of the object I am inspecting, but still see the internals when needed.

## Functional Requirements
- **Key Binding:** Pressing 'd' in the TUI will toggle the visibility of private and `__dunder__` methods in the object tree.
- **Visual Feedback:** The TUI should clearly indicate whether private methods are currently hidden or shown.
- **Persistence:** The toggle state should ideally persist across different object inspections during the same session (optional, but nice-to-have).
- **Default State:** By default, private methods should be hidden to ensure a "Zero Friction" and clean initial view.

## Non-Functional Requirements
- **Performance:** Toggling should be instantaneous and not require re-parsing the entire object tree.
- **Consistency:** The toggle should affect all levels of the tree consistently.

## Technical Details
- **TUI Framework:** Textual.
- **Tree Widget:** Update the existing tree widget to filter out attributes/methods starting with `_`.
- **State Management:** Add a boolean flag in the `InteractiveExplorer` or TUI `App` class to track the toggle state.

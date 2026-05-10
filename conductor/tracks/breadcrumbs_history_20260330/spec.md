# Specification: Smart Breadcrumbs & History

## Overview
Enhance navigation in the TUI by adding a visual breadcrumb trail of the current path and a session history of previously selected objects.

## Functional Requirements
- **Visual Breadcrumb Trail**: Display a clickable path (e.g., `root > data > [0]`) at the bottom of the screen.
- **Back/Forward Navigation**: Map `Alt+Left` and `Alt+Right` to navigate the selection history.
- **Session History List**: A searchable popup (`Ctrl+H`) showing all unique objects visited in the current session.
- **Jump to Path**: Clickable segments in the breadcrumb trail will jump back to that level in the tree.

## Technical Details
- Maintain a `history: list[TreeNode]` and `history_index: int` in the `App`.
- Use a `Horizontal` container with `Button` or `Label` for the breadcrumb trail.

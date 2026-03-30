# Specification: Integrated PyDoc/Help View

## Overview
Add a dedicated pane that renders the output of Python's built-in `pydoc.render_doc()` or `help()` functions for the currently selected object.

## Functional Requirements
- **Help View Pane**: A dedicated TUI pane that displays formatted documentation.
- **Built-in `help()` Integration**: Capture and render the output of `pydoc.render_doc(obj)` for a selected object.
- **Local Docstring View**: Integrate with the current docstring display, showing a more detailed or extended version in the help pane.
- **Syntax Highlighting**: Apply syntax highlighting to any code snippets found within the documentation.

## Technical Details
- Use `pydoc.render_doc(obj, renderer=pydoc.plaintext)` and wrap it in a Rich `Syntax` or `Text` block.
- Map the 'h' key to toggle the help pane.
- Integrate with `ClassInfoPane` to avoid duplicate information.

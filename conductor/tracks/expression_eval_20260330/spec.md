# Specification: Live Expression Evaluation

## Overview
Add a "Scratchpad" tray at the bottom of the TUI where users can evaluate arbitrary Python expressions.

## Functional Requirements
- **Bottom Tray UI**: An expandable/collapsible tray at the bottom of the screen.
- **Contextual Execution**: Evaluate expressions using the currently selected object as `self` or `obj`.
- **Simple Completion**: Basic auto-completion for keywords and common object attributes.
- **Execution History**: Keep a log of evaluated expressions and their results within the session.

## Technical Details
- Use a Textual `Input` and `Static` area for the tray.
- Use `eval()` or `compile()` with a custom namespace.

# Product Definition: sus-inspector

## Initial Concept
The interactive, terminal-based object inspector for suspicious Python objects. `sus-inspector` bridges the gap between the instant gratification of `icecream` and the deep introspection of `wat`.

## Vision & Goals
`sus-inspector` aims to be the go-to tool for Python developers and API consumers who need to quickly and deeply inspect complex objects without the overhead of a full debugger.

### Primary Objectives
- **Zero Friction:** Inspection should take exactly one line of code and zero setup.
- **Keyboard First:** Navigation should be as fast as a terminal game, prioritizing speed and efficiency.
- **Beautiful by Default:** Data should be richly formatted and easy to read using a consistent, high-contrast theme and modular inspectors.

## Target Audience
- **Python Developers:** Debugging complex nested objects, class instances, and functional logic in real-time.
- **API Consumers:** Exploring deeply nested JSON structures or class-based responses from external services.

## Core Features
- **Interactive Navigation:** Visual breadcrumb trail for instant context and clickable "jump-to-path" capability.
- **Session History:** Robust navigation history with back/forward support (Alt+Left/Right) and a searchable history popup (Ctrl+H).
- **Comprehensive Documentation Site:** A central resource for users and developers, including automated API reference and getting started guides.
- **Inspector Registry:** A modular system for custom object-specific rendering logic, allowing for highly tailored inspection views.
- **Side-by-side TUI layout:** Optimized dual-pane display for simultaneous instance and class metadata inspection.
- **Smart Grouping:** Automatically groups members into "Fields" and "Methods" for complex objects.
- **Visual Toggle ('d'):** Quickly show or hide private `_` members for cleaner inspection.
- **Expression Evaluation:** Allow users to evaluate simple Python expressions directly within the search bar or TUI.- **Interactive Class Views:** Dedicated views for inspecting class-level metadata, methods, and inheritance trees (Toggle with 'c').
- **Enhanced Custom Handlers:** Expand the plugin system with more robust, interactive handlers for common libraries and data structures.

## Technical & Design Constraints
- **Minimal Dependencies:** Core functionality must rely only on Textual and Rich to keep the package lightweight.
- **Performance First:** Utilize smart lazy-loading to ensure the TUI remains responsive even when inspecting massive objects.
- **Exhaustive Reliability:** Maintain 100% code coverage to ensure the tool is dependable for mission-critical debugging.
- **Cross-Terminal Support:** Ensure a consistent and high-quality experience across various terminal emulators and environments.

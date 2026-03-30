# Specification: Custom Plugin System

## Overview
Create a formalized API to allow users to extend `sus-inspector` with custom object renderers and themes without modifying the core codebase.

## Functional Requirements
- **CLI-only Load**: A `--plugin` CLI flag to load one or more `.py` files as plugins.
- **Runtime Registration API**: A simple Python API (e.g., `register_plugin()`) to register custom inspectors or themes from a script.
- **Hook Isolation**: Ensure plugins don't interfere with built-in hooks unless intended.
- **Theme Support**: Allow plugins to provide a `.tcss` file or a set of styles.

## Technical Details
- Use `importlib.util` to dynamically load Python modules from paths.
- Call a predefined `register_sus_plugin()` function in each loaded plugin file.

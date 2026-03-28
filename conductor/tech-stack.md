# Technology Stack: sus-inspector

## Core Technologies
### Programming Language
- **Python (>= 3.10):** The primary language for the project, chosen for its vast ecosystem and powerful reflection/introspection capabilities.

### Terminal User Interface (TUI)
- **Textual:** A modern, feature-rich TUI framework used to build the interactive explorer.
- **Rich:** A Python library for rich text and beautiful formatting in the terminal, used for rendering object details.

### Build & Package Management
- **uv_build:** A fast and efficient build-backend for Python packages.

## Developer Tools
### Linting & Formatting
- **Ruff:** A high-performance Python linter and formatter used to maintain code quality.
- **Pre-commit:** Used to automate linting and formatting checks before each commit.

### Type Checking
- **Basedpyright:** A powerful and extensible static type checker for Python.

### Task Management
- **Poethepoet:** A task runner for Python projects, used to automate common development workflows.

### Testing & Verification
- **Pytest:** The standard testing framework for Python projects.
- **Ty:** A lightweight tool for running common Python tasks.

## Optional Integrations
- **Pydantic:** Natively supported if installed, used for specialized rendering of `BaseModel` instances.

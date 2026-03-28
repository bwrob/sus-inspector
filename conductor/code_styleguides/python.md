# Python Style Guide (sus-inspector)

## Core Principles
- **Strict Typing:** All code must be fully typed and pass `basedpyright` in strict mode. Use the `typing` module for complex types.
- **Automated Formatting:** Code style is enforced by `ruff format` (Black-compatible, 88 char line limit).
- **Comprehensive Linting:** `ruff` is used with the `ALL` rule set (with minimal exceptions) to ensure high code quality.
- **Strict TDD:** Changes must be accompanied by comprehensive tests using `pytest`, targeting **95% test coverage**.
- **Minimal Dependencies:** Strive for minimal and light dependencies. Larger or specialized dependencies should be offered as optional extras.

## Tooling & Workflow
The project uses `uv` for dependency management and `poethepoet` for task automation.

### Standard Commands
- **Check All:** `uv run poe check-all` (Runs formatting, linting, and type checking)
- **Auto-Fix:** `uv run ruff check --fix`
- **Format:** `uv run ruff format`
- **Type Check:** `uv run basedpyright`
- **Test:** `uv run pytest` (or `uv run poe coverage` for reports)

## Code Structure & Naming
- **Modules:** Use `snake_case` for module names (e.g., `my_module.py`).
- **Classes:** Use `PascalCase` for class names (e.g., `MyClass`).
- **Functions/Variables:** Use `snake_case` (e.g., `my_function`, `my_variable`).
- **Constants:** Use `UPPER_CASE` for constants (e.g., `MAX_RETRIES`).
- **Private Members:** Use a single leading underscore for internal/private members (e.g., `_internal_helper`).

## Documentation
- **Docstrings:** Use Google-style docstrings for all public modules, classes, and functions.
- **Type Hints:** Are mandatory for all function arguments and return types.

## Git Conventions
We follow the **Conventional Commits** (Angular) standard:
- **Format:** `type(scope): subject`
- **Common Types:** `feat:`, `fix:`, `docs:`, `dev:`, `test:`, `refactor:`.

**Example:**
```text
feat(tui): implement visual toggle for private methods
test(core): add unit tests for object inspection logic
```

**BE CONSISTENT.** When editing code, always match the existing style and architectural patterns.

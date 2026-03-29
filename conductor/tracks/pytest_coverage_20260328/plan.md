# Implementation Plan: Comprehensive Testing & 100% Coverage

## Phase 1: Test Environment & Tooling Setup
- [x] Task: Configure `pytest` and coverage tools.
    - [x] Create a feature branch `feat/testing-infrastructure`.
    - [x] Add `pytest-cov` and `hypothesis` to the project's developer dependencies using `uv`.
    - [x] Update `pyproject.toml` or `pytest.ini` with coverage settings (e.g., `--cov=src/sus_inspector`, `--cov-fail-under=100`).
    - [x] Create a basic `conftest.py` if needed for shared fixtures or settings.
- [x] Task: Conductor - User Manual Verification 'Test Environment & Tooling Setup' (Protocol in workflow.md)

## Phase 2: Core Logic & Unit Testing
- [x] Task: Implement unit tests for `sus_inspector.core` and utilities.
    - [x] Create a feature branch `feat/unit-tests-core`.
    - [x] Write unit tests for object metadata extraction and property-based tests with `hypothesis`.
    - [x] Verify coverage for `core.py` and `instances.py`.
    - [x] Reach 100% for these core modules.
- [x] Task: Implement unit tests for hooks and registry system.
    - [x] Create a feature branch `feat/unit-tests-hooks`.
    - [x] Write tests for the hook registry and built-in handlers (Pydantic, etc.).
    - [x] Mock external dependencies if necessary.
    - [x] Reach 100% for all files in `sus_inspector/hooks/`.
- [x] Task: Conductor - User Manual Verification 'Core Logic & Unit Testing' (Protocol in workflow.md)

## Phase 3: TUI & Integration Testing
- [x] Task: Implement TUI tests using Textual's Pilot.
    - [x] Create a feature branch `feat/tui-integration-tests`.
    - [x] Use Textual's `Pilot` to verify application startup, key bindings (e.g., 'd', 'c' toggle logic), and UI state changes.
    - [x] Verify that UI actions result in the correct object state and rendered output.
    - [x] Reach 100% for `sus_inspector/tui/` and `sus_inspector/app.py`.
- [x] Task: Implement regression and CLI tests.
    - [x] Create a feature branch `feat/regression-cli-tests`.
    - [x] Write tests for the CLI interface (`cli.py`, `main.py`).
    - [x] Add regression tests for any known edge cases.
    - [x] Reach 100% for all remaining files.
- [x] Task: Conductor - User Manual Verification 'TUI & Integration Testing' (Protocol in workflow.md)

## Phase 4: Final Verification & Coverage Audit
- [x] Task: Perform a complete coverage audit.
    - [x] Run the full test suite with coverage reporting enabled.
    - [x] Identify and address any remaining coverage gaps.
    - [x] Ensure all code paths (including error handling) are exercised.
- [x] Task: Final Polish & Verification.
    - [x] Verify 100% test coverage globally.
    - [x] Run full linting and type-checking suite.
    - [x] Confirm all tests pass consistently across environments.
- [x] Task: Conductor - User Manual Verification 'Final Polish & Verification' (Protocol in workflow.md)

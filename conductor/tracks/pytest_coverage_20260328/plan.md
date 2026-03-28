# Implementation Plan: Comprehensive Testing & 100% Coverage

## Phase 1: Test Environment & Tooling Setup
- [ ] Task: Configure `pytest` and coverage tools.
    - [ ] Create a feature branch `feat/testing-infrastructure`.
    - [ ] Add `pytest-cov` and `hypothesis` to the project's developer dependencies using `uv`.
    - [ ] Update `pyproject.toml` or `pytest.ini` with coverage settings (e.g., `--cov=src/sus_inspector`, `--cov-fail-under=100`).
    - [ ] Create a basic `conftest.py` if needed for shared fixtures or settings.
- [ ] Task: Conductor - User Manual Verification 'Test Environment & Tooling Setup' (Protocol in workflow.md)

## Phase 2: Core Logic & Unit Testing
- [ ] Task: Implement unit tests for `sus_inspector.core` and utilities.
    - [ ] Create a feature branch `feat/unit-tests-core`.
    - [ ] Write unit tests for object metadata extraction and property-based tests with `hypothesis`.
    - [ ] Verify coverage for `core.py` and `instances.py`.
    - [ ] Reach 100% for these core modules.
- [ ] Task: Implement unit tests for hooks and registry system.
    - [ ] Create a feature branch `feat/unit-tests-hooks`.
    - [ ] Write tests for the hook registry and built-in handlers (Pydantic, etc.).
    - [ ] Mock external dependencies if necessary.
    - [ ] Reach 100% for all files in `sus_inspector/hooks/`.
- [ ] Task: Conductor - User Manual Verification 'Core Logic & Unit Testing' (Protocol in workflow.md)

## Phase 3: TUI & Integration Testing
- [ ] Task: Implement TUI tests using Textual's Pilot.
    - [ ] Create a feature branch `feat/tui-integration-tests`.
    - [ ] Use Textual's `Pilot` to verify application startup, key bindings (e.g., 'd', 'c' toggle logic), and UI state changes.
    - [ ] Verify that UI actions result in the correct object state and rendered output.
    - [ ] Reach 100% for `sus_inspector/tui/` and `sus_inspector/app.py`.
- [ ] Task: Implement regression and CLI tests.
    - [ ] Create a feature branch `feat/regression-cli-tests`.
    - [ ] Write tests for the CLI interface (`cli.py`, `main.py`).
    - [ ] Add regression tests for any known edge cases.
    - [ ] Reach 100% for all remaining files.
- [ ] Task: Conductor - User Manual Verification 'TUI & Integration Testing' (Protocol in workflow.md)

## Phase 4: Final Verification & Coverage Audit
- [ ] Task: Perform a complete coverage audit.
    - [ ] Run the full test suite with coverage reporting enabled.
    - [ ] Identify and address any remaining coverage gaps.
    - [ ] Ensure all code paths (including error handling) are exercised.
- [ ] Task: Final Polish & Verification.
    - [ ] Verify 100% test coverage globally.
    - [ ] Run full linting and type-checking suite.
    - [ ] Confirm all tests pass consistently across environments.
- [ ] Task: Conductor - User Manual Verification 'Final Polish & Verification' (Protocol in workflow.md)

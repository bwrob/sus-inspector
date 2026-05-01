# Implementation Plan: Comprehensive Test Suite Improvement

## Phase 1: Coverage Audit & Foundation
- [ ] Task: Run current test suite with coverage and identify specific gaps below 98%.
- [ ] Task: Set up `hypothesis` configuration and basic strategies in `tests/conftest.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Coverage Audit & Foundation' (Protocol in workflow.md)

## Phase 2: Core Logic & Property-Based Testing
- [ ] Task: Write behavioral tests for `sus_inspector/core.py` (focus on public API).
- [ ] Task: Implement property-based tests using `hypothesis` for object traversal logic.
- [ ] Task: Increase `core.py` and `metadata.py` coverage to 100%.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Core Logic & Property-Based Testing' (Protocol in workflow.md)

## Phase 3: TUI Behavioral Flows
- [ ] Task: Audit existing TUI tests for implementation-coupling and refactor to use `AppTest` flows.
- [ ] Task: Implement new behavioral tests for TUI navigation, visual toggles, and breadcrumb history.
- [ ] Task: Increase `tui/` module coverage to > 95%.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: TUI Behavioral Flows' (Protocol in workflow.md)

## Phase 4: Integration Exhaustion & Final Verification
- [ ] Task: Expand integration tests for `hooks/` (Pydantic, attrs, msgspec) covering complex/nested structures.
- [ ] Task: Verify overall project coverage reaches 98%.
- [ ] Task: Run `uv run poe code-quality` to ensure no linting/type regressions.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Integration Exhaustion & Final Verification' (Protocol in workflow.md)

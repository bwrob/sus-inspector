# Implementation Plan: Live Expression Evaluation

## Phase 1: Preparation & Evaluation Logic
- [ ] Task: Implement `evaluate_expression(obj: object, expr: str)` with a custom namespace.
- [ ] Task: Integrate `jedi` (if installed) or basic `rlcompleter` for simple completion.
- [ ] Task: Write tests to verify evaluation of arbitrary expressions.
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: UI Integration (Expression Tray)
- [ ] Task: Implement an expandable bottom tray UI with an `Input` field.
- [ ] Task: Map a key binding (e.g., `e`) to focus the expression tray.
- [ ] Task: Write TUI tests for expression input and basic output display.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Result Log & History
- [ ] Task: Add a scrollable result log to the expression tray.
- [ ] Task: Implement input history (up/down arrow navigation).
- [ ] Task: Write TUI tests for the result log and input history.
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Final Polish
- [ ] Task: Final code quality check.
- [ ] Task: Verify 95% coverage for the evaluation logic.
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

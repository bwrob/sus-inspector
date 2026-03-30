# Implementation Plan: Memory Profiling

## Phase 1: Core Logic & Calculator
- [ ] Task: Implement a recursive size calculator with circular reference detection.
- [ ] Task: Add a `depth_limit` parameter to the calculator.
- [ ] Task: Write tests for calculating sizes of nested objects (lists, dicts, complex classes).
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: UI Integration (Memory Breakdown)
- [ ] Task: Implement a new `MemoryPane` or specialized detail view section.
- [ ] Task: Show a table of top memory contributors (attribute names and sizes).
- [ ] Task: Integrate the `Progress` widget for deep calculations.
- [ ] Task: Write TUI tests for the memory view display.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Config & Performance
- [ ] Task: Add a UI setting or command to adjust the `depth_limit`.
- [ ] Task: Optimize the recursive calculator using memoization or other performance techniques.
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Final Polish
- [ ] Task: Final code quality check.
- [ ] Task: Verify 95% coverage for the memory calculator.
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

# Development Workflow: sus-inspector

## 1. Core Principles
- **Context First:** Always read `tech-stack.md` and related files in `src/` before writing code.
- **Strict TDD:** Tests are the specification. Write the test -> Watch it fail -> Write code -> Watch it pass.
- **Type-Safety First:** Use Pydantic or dataclasses and type hints before implementing logic.
- **Zero Tolerance:** No linting warnings (`ruff`), no type errors (`basedpyright`), and 95% test coverage.
- **Conventional Commits:** Use Angular-style messages (e.g., `feat:`, `fix:`, `test:`, `refactor:`).
- **Atomic Operations:** Keep changes small and focused on a single task.

## 2. Branching & Commits
- **Track Branches:** Every track must be developed on a dedicated branch (e.g., `track/shortname-YYYYMMDD`). This branch will persist for the duration of the track.
- **Merge Requests (MRs):** Upon completing a track, create a Merge Request (or Pull Request) to merge the track branch into the main development branch.
- **Per-Task Commits:** Commit changes after every completed task in `plan.md`.
- **Git Notes Summaries:** Store detailed task summaries in Git notes metadata to keep the commit history clean.

## 3. The Development Loop (Per Task)
For every item in `plan.md`, execute this exact cycle:

### Phase A: Design & Specification
1. **Branch Check:** Ensure you are on the correct track-specific branch.
2. **Interface Definition:** Write or update type definitions and function signatures.
3. **Write Test:** Create a `pytest` case in `tests/` that reproduces the requirement.
4. **Verify Failure:** Run `uv run pytest` and confirm the test fails (Red state).

### Phase B: Implementation
1. **Implement:** Write the minimum code necessary to pass the test.
2. **Verify Pass:** Run the test again and ensure it passes (Green state).
3. **Consistency Check:** Ensure the implementation follows the project's architectural patterns.

### Phase C: Polish & Verify
1. **Format & Lint:** Run `ruff check --fix` and `ruff format`.
2. **Type Check:** Run `basedpyright`.
3. **Coverage:** Ensure the new code maintains or exceeds the **95% test coverage** requirement.
4. **Refactor:** Clean up the code if necessary, re-running all tests afterward.

### Phase D: Commit & Document
1. **Update Plan:** Mark the task in `plan.md` as `[x]`.
2. **Git Commit:** Commit with a conventional message.
3. **Record Summary:** Use `git notes` to attach a summary of the changes to the commit.

## 4. Tooling Reference
- **Package Manager:** `uv`
- **Testing:** `pytest`
- **Linting & Formatting:** `ruff`
- **Type Checking:** `basedpyright`
- **Task Runner:** `poethepoet` (if configured)

## 5. Phase Completion & Checkpointing
When all tasks in a **Phase** are complete:
1. **Code Quality:** Run `uv run poe code-quality` and fix all reported issues (linting, formatting, type-checking, complexity).
2. **Full Suite:** Run the complete test suite.
3. **User Manual Verification:** Execute the meta-task: `- [ ] Task: Conductor - User Manual Verification '<Phase Name>' (Protocol in workflow.md)`.


## 6. Protocol: Conductor - User Manual Verification
This meta-task requires the Conductor agent to:
1.  **Self-Review:** Compare the implementation against the `spec.md` and `plan.md`.
2.  **Demonstrate:** Provide a summary or example of the feature in action (e.g., a code snippet or TUI screenshot description).
3.  **Confirm:** Ask the user to confirm the phase meets their expectations before proceeding to the next phase.

## 7. Protocol: Track Finalization & PR
After a track is successfully implemented and archived (moved to `conductor/archive/`):
1.  **PR Creation:** Open a Pull Request from the track branch to `main` using the GitHub CLI (`gh`).
2.  **PR Details:**
    - **Title:** Use the track description (e.g., `feat(conductor): <Track Description>`).
    - **Body:** Briefly summarize the changes and link to the archived track's `index.md`.
3.  **Command:** `rtk gh pr create --fill --label "track-complete"`.

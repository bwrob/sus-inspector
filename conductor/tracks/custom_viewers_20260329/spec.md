# Specification: Unified Custom Object Viewers (track/custom-viewers-20260329)

## Overview
Implement a unified, dynamic, and interactive system for inspecting common Python data objects (dataclasses, Pydantic models, attrs classes, and msgspec structs) within `sus-inspector`.

## Functional Requirements
- **Broad Library Support:** Provide specialized rendering for:
  - Python Standard Library `dataclasses`.
  - `pydantic` (v1 and v2) `BaseModel` instances.
  - `attrs` classes.
  - `msgspec` structs.
- **Library-Specific UI:** Clearly identify the library type for each object (e.g., a "Pydantic" or "Dataclass" tag/header).
- **Complexity Assessment:** Automatically determine if an object is "complex" based on a combination of:
  - **Nesting Depth:** > 2 levels.
  - **Field Count:** > 10 fields.
  - **Object Size:** Total number of leaf nodes.
  - **Smart Heuristic:** An extensible heuristic to balance detail and performance.
- **Dynamic Content:**
  - **Simple Objects:** Show all fields and values immediately.
  - **Complex Objects:** Show a summarized view with the option to expand.
- **Interactive Navigation:** Use a tree-based expansion system to allow users to navigate nested structures.

## Non-Functional Requirements
- **Lazy Loading:** Ensure the TUI remains responsive even when inspecting large, deeply nested objects.
- **Zero Configuration:** Automatically detect and handle these types without manual user setup.

## Acceptance Criteria
1. Objects from all four libraries are correctly identified and rendered.
2. The UI clearly labels the object type (e.g., `[Pydantic] User(id=1, ...)`).
3. The complexity assessment correctly triggers a summarized view for objects meeting the criteria.
4. Users can expand/collapse nested objects via keyboard/mouse interaction.
5. Inspecting a deeply nested object does not cause performance degradation.

## Out of Scope
- Editing or modifying object values.
- Supporting legacy (non-v1/v2) versions of libraries unless straightforward.
- Exporting or saving the tree state.

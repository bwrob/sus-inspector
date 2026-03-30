# Specification: Reference Tracking (GC Integration)

## Overview
Utilize Python's `gc` (garbage collector) module to allow users to inspect the reference graph of an object, seeing what points to it (referrers) and what it points to (referents).

## Functional Requirements
- **Referrers View**: Display a list of objects that hold a reference to the selected object.
- **Referents View**: Display a list of objects that the selected object points to.
- **Interactive Traversal**: Users can select a referrer or referent to jump to that object and inspect it in the main tree.
- **Filtering**: Hide internal references or specific known noise (like the `gc` module's internal tracking).

## Technical Details
- Use `gc.get_referrers()` and `gc.get_referents()`.
- Add a new section/pane or specialized tree nodes for "References".

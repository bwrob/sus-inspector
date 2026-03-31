"""Complexity assessment for Python objects."""

from __future__ import annotations

from typing import Any, cast


def _get_fields(o: Any) -> dict[str, Any]:  # noqa: ANN401
    """Get fields from common object types.

    Returns:
        dict[str, Any]: A dictionary of field names and values.

    """
    if isinstance(o, dict):
        return cast("dict[str, Any]", o)
    # Access __dict__ more safely
    obj_dict = getattr(o, "__dict__", None)
    if isinstance(obj_dict, dict):
        return cast("dict[str, Any]", obj_dict)
    if hasattr(o, "__slots__"):
        slots = cast("tuple[str, ...] | str", o.__slots__)
        if isinstance(slots, str):
            slots = (slots,)
        return {str(s): getattr(o, s) for s in slots if hasattr(o, s)}
    return {}


def _traverse_with_metrics(
    o: Any,  # noqa: ANN401
    current_depth: int,
    max_depth: int,
) -> tuple[int, int]:
    """Traverse object to calculate size and depth.

    Returns:
        tuple[int, int]: (total_size, max_reached_depth)

    """
    fields = _get_fields(o)
    if not fields or current_depth >= max_depth:
        return 1, current_depth

    total_size = 1
    max_reached_depth = current_depth
    for val in fields.values():
        size, depth = _traverse_with_metrics(val, current_depth + 1, max_depth)
        total_size += size
        max_reached_depth = max(max_reached_depth, depth)

    return total_size, max_reached_depth


def get_object_complexity(obj: Any, max_depth: int = 3) -> dict[str, int]:  # noqa: ANN401
    """Assess the complexity of an object.

    Args:
        obj: The object to assess.
        max_depth: Maximum depth to traverse for size calculation.

    Returns:
        dict[str, int]: A dictionary containing complexity metrics:
            - 'depth': Maximum nesting depth found.
            - 'field_count': Number of top-level fields/attributes.
            - 'total_size': Total number of nodes found within max_depth.

    """
    top_fields = _get_fields(obj)
    size, depth = _traverse_with_metrics(obj, 0, max_depth)

    return {
        "depth": depth,
        "field_count": len(top_fields),
        "total_size": size,
    }


def is_complex_object(
    obj: Any,  # noqa: ANN401
    *,
    depth_threshold: int = 2,
    field_threshold: int = 10,
    size_threshold: int = 50,
) -> bool:
    """Determine if an object is complex based on metrics.

    Args:
        obj: The object to check.
        depth_threshold: Depth above which object is complex.
        field_threshold: Field count above which object is complex.
        size_threshold: Total size above which object is complex.

    Returns:
        bool: True if any threshold is exceeded.

    """
    metrics = get_object_complexity(obj, max_depth=depth_threshold + 1)

    return (
        metrics["depth"] > depth_threshold
        or metrics["field_count"] > field_threshold
        or metrics["total_size"] > size_threshold
    )

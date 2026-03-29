"""Class metadata extraction and rendering."""

from __future__ import annotations

import inspect
from typing import Any, NamedTuple

from rich.text import Text
from rich.tree import Tree


class ClassMetadata(NamedTuple):
    """Container for class-level metadata.

    Attributes:
        name: Name of the class.
        doc: Docstring of the class.
        class_fields: Dictionary of class-level attributes.
        class_methods: List of names of class methods.
        mro: Method Resolution Order as a list of names.
        inheritance_tree: Rich Tree representing the hierarchy.

    """

    name: str
    doc: str | None
    class_fields: dict[str, Any]
    class_methods: list[str]
    mro: list[str]
    inheritance_tree: Tree


def get_class_metadata(obj: Any) -> ClassMetadata:
    """Extract metadata from an object's class.

    Args:
        obj: The object or class to extract metadata from.

    Returns:
        ClassMetadata: The extracted metadata.

    """
    cls = obj if inspect.isclass(obj) else type(obj)

    # Docstring
    doc = inspect.getdoc(cls)

    # Class Fields and Methods
    class_fields = {}
    class_methods = []

    for name, value in inspect.getmembers(cls):
        if name.startswith("__"):
            continue

        # Check if it's a class method (bound to the class)
        if inspect.ismethod(value) and getattr(value, "__self__", None) is cls:
            class_methods.append(name)
        elif not inspect.isroutine(value):
            class_fields[name] = value

    # MRO
    mro = [c.__name__ for c in inspect.getmro(cls)]

    # Inheritance Tree
    def build_tree(current_cls: type, branch: Tree) -> None:
        """Recursively build the inheritance tree."""
        for base in current_cls.__bases__:
            if base is object:
                continue
            sub_branch = branch.add(Text(base.__name__, style="blue"))
            build_tree(base, sub_branch)

    root_text = Text(cls.__name__, style="bold green")
    tree = Tree(root_text)
    build_tree(cls, tree)

    return ClassMetadata(
        name=cls.__name__,
        doc=doc,
        class_fields=class_fields,
        class_methods=class_methods,
        mro=mro,
        inheritance_tree=tree,
    )

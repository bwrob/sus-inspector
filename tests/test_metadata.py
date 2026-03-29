from sus_inspector.metadata import get_class_metadata


class Base:
    """Base class doc."""

    base_field = "base"


class Sub(Base):
    """Sub class doc."""

    sub_field = "sub"

    @classmethod
    def sub_method(cls):
        pass


def test_get_class_metadata():
    obj = Sub()
    meta = get_class_metadata(obj)

    assert meta.name == "Sub"
    assert meta.doc == "Sub class doc."
    assert "sub_field" in meta.class_fields
    assert "base_field" in meta.class_fields
    assert "sub_method" in meta.class_methods
    assert "Sub" in meta.mro
    assert "Base" in meta.mro
    assert "object" in meta.mro


def test_inheritance_tree_structure():
    obj = Sub()
    meta = get_class_metadata(obj)
    # Tree visualization is hard to assert exactly,
    # but we can check if it exists and has the right root.
    assert meta.inheritance_tree.label.plain == "Sub"

"""Tests for SPEC-001: DDR XML Object Type Registry."""

from fm_ddr_to_llm.object_types import OBJECT_TYPES, ObjectTypeDef


def test_registry_has_core_types():
    """All core FM object types are registered."""
    expected = {
        "base_table",
        "field",
        "table_occurrence",
        "relationship",
        "layout",
        "script",
        "script_step",
        "value_list",
        "custom_function",
        "custom_menu",
        "custom_menu_set",
        "account",
        "privilege_set",
        "extended_privilege",
        "external_data_source",
    }
    assert expected.issubset(set(OBJECT_TYPES.keys()))


def test_each_type_has_tag_and_id_attr():
    """Every registered type has the required fields."""
    for name, obj_def in OBJECT_TYPES.items():
        assert obj_def.tag, f"{name} missing tag"
        assert obj_def.id_attr, f"{name} missing id_attr"
        assert obj_def.name_attr, f"{name} missing name_attr"


def test_build_pattern_matches_base_table():
    """build_pattern produces a regex that matches BaseTable tags."""
    obj_def = OBJECT_TYPES["base_table"]
    pattern = obj_def.build_pattern()
    tag = '<BaseTable id="1065089" name="Contacts" records="150">'
    match = pattern.search(tag)
    assert match is not None
    assert match.group("id") == "1065089"
    assert match.group("name") == "Contacts"


def test_build_pattern_matches_attrs_any_order():
    """Pattern works regardless of attribute order."""
    obj_def = OBJECT_TYPES["field"]
    pattern = obj_def.build_pattern()
    # Reversed order from normal
    tag = '<Field name="Email" id="4" fieldType="Normal" dataType="Text"/>'
    match = pattern.search(tag)
    assert match is not None
    assert match.group("id") == "4"
    assert match.group("name") == "Email"

"""Tests for SPEC-002: Streaming Regex ID Extractor."""

from __future__ import annotations

from pathlib import Path

from fm_ddr_to_llm.extractor import extract_from_file


def test_extracts_base_tables(sample_ddr_xml: Path):
    """Extracts base tables with IDs."""
    objects = extract_from_file(sample_ddr_xml)
    tables = [o for o in objects if o.type_name == "base_table"]
    assert len(tables) == 2
    names = {o.name for o in tables}
    assert names == {"Contacts", "Invoices"}
    ids = {o.object_id for o in tables}
    assert "1065089" in ids
    assert "1065090" in ids


def test_extracts_fields_with_parent_context(sample_ddr_xml: Path):
    """Extracts fields and tracks which base table they belong to."""
    objects = extract_from_file(sample_ddr_xml)
    fields = [o for o in objects if o.type_name == "field"]
    # 5 in Contacts + 4 in Invoices = 9
    assert len(fields) == 9

    contacts_fields = [f for f in fields if f.parent_context == "Contacts"]
    assert len(contacts_fields) == 5

    invoices_fields = [f for f in fields if f.parent_context == "Invoices"]
    assert len(invoices_fields) == 4


def test_extracts_table_occurrences(sample_ddr_xml: Path):
    """Extracts table occurrences from RelationshipGraph."""
    objects = extract_from_file(sample_ddr_xml)
    tos = [o for o in objects if o.type_name == "table_occurrence"]
    assert len(tos) == 3
    names = {o.name for o in tos}
    assert "Invoices_by_Contact" in names


def test_extracts_relationships(sample_ddr_xml: Path):
    objects = extract_from_file(sample_ddr_xml)
    rels = [o for o in objects if o.type_name == "relationship"]
    assert len(rels) == 1
    assert rels[0].object_id == "300"


def test_extracts_layouts(sample_ddr_xml: Path):
    objects = extract_from_file(sample_ddr_xml)
    layouts = [o for o in objects if o.type_name == "layout"]
    assert len(layouts) == 2
    assert {o.name for o in layouts} == {"Contact Detail", "Invoice List"}


def test_extracts_scripts(sample_ddr_xml: Path):
    objects = extract_from_file(sample_ddr_xml)
    scripts = [o for o in objects if o.type_name == "script"]
    assert len(scripts) == 2
    assert {o.name for o in scripts} == {"Create Invoice", "Navigate to Invoices"}


def test_extracts_script_steps(sample_ddr_xml: Path):
    objects = extract_from_file(sample_ddr_xml)
    steps = [o for o in objects if o.type_name == "script_step"]
    # 3 steps in Create Invoice + 2 in Navigate to Invoices = 5
    assert len(steps) == 5


def test_extracts_value_lists(sample_ddr_xml: Path):
    objects = extract_from_file(sample_ddr_xml)
    vls = [o for o in objects if o.type_name == "value_list"]
    assert len(vls) == 1
    assert vls[0].name == "Contact Names"


def test_extracts_custom_functions(sample_ddr_xml: Path):
    objects = extract_from_file(sample_ddr_xml)
    cfs = [o for o in objects if o.type_name == "custom_function"]
    assert len(cfs) == 1
    assert cfs[0].name == "FormatName"
    assert cfs[0].extra.get("parameters") == "first;last"


def test_extracts_accounts(sample_ddr_xml: Path):
    objects = extract_from_file(sample_ddr_xml)
    accts = [o for o in objects if o.type_name == "account"]
    assert len(accts) == 1
    assert accts[0].name == "Admin"


def test_handles_malformed_xml(malformed_ddr_xml: Path):
    """Extractor doesn't crash on malformed XML — extracts what it can."""
    objects = extract_from_file(malformed_ddr_xml)
    tables = [o for o in objects if o.type_name == "base_table"]
    # Should get at least the good tables
    assert len(tables) >= 2
    fields = [o for o in objects if o.type_name == "field"]
    # Should get at least the non-broken fields
    assert len(fields) >= 2


def test_extracts_extra_attrs(sample_ddr_xml: Path):
    """Extra attributes (fieldType, dataType, etc.) are captured."""
    objects = extract_from_file(sample_ddr_xml)
    calc_field = [
        o
        for o in objects
        if o.type_name == "field" and o.name == "FullName"
    ]
    assert len(calc_field) == 1
    assert calc_field[0].extra.get("fieldType") == "Calculated"

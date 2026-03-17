"""Tests for SPEC-004 & SPEC-005: Cross-Reference Graph Builder."""

from __future__ import annotations

from pathlib import Path

from fm_ddr_to_llm.extractor import extract_from_file
from fm_ddr_to_llm.graph import build_graph_from_ddr_xml
from fm_ddr_to_llm.registry import build_registry


def test_table_occurrence_to_base_table_edges(sample_ddr_xml: Path):
    """TO → base table edges are created."""
    registry = build_registry(extract_from_file(sample_ddr_xml))
    graph = build_graph_from_ddr_xml(sample_ddr_xml, registry)
    based_on = [e for e in graph.edges if e.relationship == "based_on"]
    assert len(based_on) == 3  # 3 TOs, each based on a base table
    # Invoices_by_Contact (id=202) → Invoices (id=1065090)
    tos_inv = [e for e in based_on if e.source_id == "202"]
    assert len(tos_inv) == 1
    assert tos_inv[0].target_id == "1065090"


def test_relationship_to_table_edges(sample_ddr_xml: Path):
    """Relationship → left/right table edges are created."""
    registry = build_registry(extract_from_file(sample_ddr_xml))
    graph = build_graph_from_ddr_xml(sample_ddr_xml, registry)
    left = [e for e in graph.edges if e.relationship == "left_table"]
    right = [e for e in graph.edges if e.relationship == "right_table"]
    assert len(left) == 1
    assert left[0].source_id == "300"
    assert left[0].target_id == "200"
    assert len(right) == 1
    assert right[0].target_id == "201"


def test_script_references_field(sample_ddr_xml: Path):
    """Script → field reference edges are created."""
    registry = build_registry(extract_from_file(sample_ddr_xml))
    graph = build_graph_from_ddr_xml(sample_ddr_xml, registry)
    field_refs = [e for e in graph.edges if e.relationship == "references_field"]
    assert len(field_refs) >= 1
    # Script 500 references field ContactID
    s500_refs = [e for e in field_refs if e.source_id == "500"]
    assert len(s500_refs) >= 1


def test_script_goes_to_layout(sample_ddr_xml: Path):
    """Script → layout reference edges are created."""
    registry = build_registry(extract_from_file(sample_ddr_xml))
    graph = build_graph_from_ddr_xml(sample_ddr_xml, registry)
    layout_refs = [e for e in graph.edges if e.relationship == "goes_to_layout"]
    assert len(layout_refs) >= 2  # Both scripts go to layout 401


def test_script_calls_script(sample_ddr_xml: Path):
    """Script → script call edges are created."""
    registry = build_registry(extract_from_file(sample_ddr_xml))
    graph = build_graph_from_ddr_xml(sample_ddr_xml, registry)
    calls = [e for e in graph.edges if e.relationship == "calls_script"]
    assert len(calls) == 1
    assert calls[0].source_id == "501"
    assert calls[0].target_id == "500"


def test_layout_uses_table_occurrence(sample_ddr_xml: Path):
    """Layout → table occurrence edges are created."""
    registry = build_registry(extract_from_file(sample_ddr_xml))
    graph = build_graph_from_ddr_xml(sample_ddr_xml, registry)
    to_refs = [e for e in graph.edges if e.relationship == "uses_table_occurrence"]
    assert len(to_refs) == 2  # Two layouts, each referencing a TO


def test_layout_displays_field(sample_ddr_xml: Path):
    """Layout → field display edges are created."""
    registry = build_registry(extract_from_file(sample_ddr_xml))
    graph = build_graph_from_ddr_xml(sample_ddr_xml, registry)
    field_refs = [e for e in graph.edges if e.relationship == "displays_field"]
    # Contact Detail: 3 fields, Invoice List: 2 fields
    assert len(field_refs) == 5


def test_edges_from_and_to_queries(sample_ddr_xml: Path):
    """edges_from and edges_to return correct subsets."""
    registry = build_registry(extract_from_file(sample_ddr_xml))
    graph = build_graph_from_ddr_xml(sample_ddr_xml, registry)
    from_500 = graph.edges_from("script", "500")
    assert len(from_500) >= 2  # goes_to_layout + references_field
    to_401 = graph.edges_to("layout", "401")
    assert len(to_401) >= 2  # Both scripts go to layout 401


def test_graph_serializes_to_dict(sample_ddr_xml: Path):
    """Graph serializes to a list of dicts."""
    registry = build_registry(extract_from_file(sample_ddr_xml))
    graph = build_graph_from_ddr_xml(sample_ddr_xml, registry)
    data = graph.to_dict()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all("source_type" in e and "target_type" in e for e in data)

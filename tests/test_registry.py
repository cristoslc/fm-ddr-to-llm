"""Tests for SPEC-003: ID Registry Output Format."""

from __future__ import annotations

import json
from pathlib import Path

from fm_ddr_to_llm.extractor import extract_from_file
from fm_ddr_to_llm.registry import build_registry, load_registry, save_registry


def test_registry_indexes_by_type(sample_ddr_xml: Path):
    objects = extract_from_file(sample_ddr_xml)
    registry = build_registry(objects)
    assert "base_table" in registry["by_type"]
    assert len(registry["by_type"]["base_table"]) == 2


def test_registry_indexes_by_composite_key(sample_ddr_xml: Path):
    objects = extract_from_file(sample_ddr_xml)
    registry = build_registry(objects)
    assert "base_table:1065089" in registry["by_id"]
    entry = registry["by_id"]["base_table:1065089"]
    assert entry["name"] == "Contacts"


def test_registry_round_trips_through_json(sample_ddr_xml: Path, tmp_path: Path):
    objects = extract_from_file(sample_ddr_xml)
    registry = build_registry(objects)
    out = tmp_path / "registry.json"
    save_registry(registry, out)
    loaded = load_registry(out)
    assert loaded["by_id"] == registry["by_id"]
    assert len(loaded["objects"]) == len(registry["objects"])


def test_registry_preserves_parent_context(sample_ddr_xml: Path):
    objects = extract_from_file(sample_ddr_xml)
    registry = build_registry(objects)
    # Field id=1 in Contacts table
    contacts_pk = [
        o for o in registry["objects"]
        if o["type"] == "field" and o["name"] == "PrimaryKey" and o["parent_context"] == "Contacts"
    ]
    assert len(contacts_pk) == 1

"""Tests for SPEC-006 & SPEC-007: Pipeline and output format."""

from __future__ import annotations

import json
from pathlib import Path

from fm_ddr_to_llm.pipeline import run_pipeline, save_output


def test_pipeline_end_to_end(sample_ddr_xml: Path):
    """Full pipeline produces a valid result."""
    result = run_pipeline(sample_ddr_xml)
    assert result.registry["objects"]
    assert result.graph.edges
    assert result.ddr_xml_path == str(sample_ddr_xml)


def test_pipeline_output_format(sample_ddr_xml: Path):
    """Output dict has the expected structure."""
    result = run_pipeline(sample_ddr_xml)
    output = result.to_dict()
    assert "meta" in output
    assert "registry" in output
    assert "cross_references" in output
    assert "summary" in output
    assert output["meta"]["version"] == "0.1.0"


def test_pipeline_summary(sample_ddr_xml: Path):
    """Summary contains object and cross-ref counts."""
    result = run_pipeline(sample_ddr_xml)
    summary = result.to_dict()["summary"]
    assert summary["total_objects"] > 0
    assert summary["total_cross_references"] > 0
    assert "base_table" in summary["objects_by_type"]


def test_pipeline_output_is_valid_json(sample_ddr_xml: Path, tmp_path: Path):
    """Output file is valid JSON."""
    result = run_pipeline(sample_ddr_xml)
    out = tmp_path / "output.json"
    save_output(result, out)
    data = json.loads(out.read_text())
    assert data["summary"]["total_objects"] > 0


def test_pipeline_deterministic(sample_ddr_xml: Path):
    """Same input produces identical output."""
    r1 = run_pipeline(sample_ddr_xml)
    r2 = run_pipeline(sample_ddr_xml)
    assert r1.to_dict() == r2.to_dict()


def test_pipeline_handles_malformed_xml(malformed_ddr_xml: Path):
    """Pipeline doesn't crash on malformed XML."""
    result = run_pipeline(malformed_ddr_xml)
    assert result.registry["objects"]  # Should get at least some objects

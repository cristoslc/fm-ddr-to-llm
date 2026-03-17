"""SPEC-006 & SPEC-007: Pipeline orchestration and output format.

Orchestrates the full pipeline: DDR XML → extract IDs → build graph → structured output.
DDRParser integration is optional — the pipeline works with or without DDRParser output.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .extractor import extract_from_file
from .graph import CrossReferenceGraph, build_graph_from_ddr_xml
from .registry import build_registry


@dataclass
class PipelineResult:
    """The complete output of the pipeline."""

    registry: dict[str, Any]
    graph: CrossReferenceGraph
    ddr_xml_path: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize the full result to a dict."""
        return {
            "meta": {
                "source": self.ddr_xml_path,
                "version": "0.1.0",
            },
            "registry": self.registry,
            "cross_references": self.graph.to_dict(),
            "summary": self._build_summary(),
        }

    def _build_summary(self) -> dict[str, Any]:
        """Build a summary of what was extracted."""
        by_type = self.registry.get("by_type", {})
        return {
            "total_objects": len(self.registry.get("objects", [])),
            "total_cross_references": len(self.graph.edges),
            "objects_by_type": {
                type_name: len(objects)
                for type_name, objects in sorted(by_type.items())
            },
        }



def run_pipeline(ddr_xml_path: Path) -> PipelineResult:
    """Run the full extraction pipeline on a DDR XML file.

    Steps:
    1. Extract object IDs from DDR XML (streaming regex)
    2. Build the ID registry
    3. Build the cross-reference graph
    4. Return the combined result
    """
    # Step 1: Extract objects
    objects = extract_from_file(ddr_xml_path)

    # Step 2: Build registry
    registry = build_registry(objects)

    # Step 3: Build cross-reference graph
    graph = build_graph_from_ddr_xml(ddr_xml_path, registry)

    return PipelineResult(
        registry=registry,
        graph=graph,
        ddr_xml_path=str(ddr_xml_path),
    )


def save_output(result: PipelineResult, output_path: Path) -> None:
    """Save the pipeline result as JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output = result.to_dict()
    output_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

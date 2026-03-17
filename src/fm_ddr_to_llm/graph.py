"""SPEC-004 & SPEC-005: Cross-Reference Graph Builder.

SPEC-004: Correlates DDRParser text output with the ID registry.
SPEC-005: Builds cross-reference edges linking objects by FM IDs.

The graph answers questions like:
- Which scripts reference field X?
- Which layouts use table occurrence Y?
- What's the data flow from this layout to the underlying table?
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Edge:
    """A cross-reference edge between two FM objects."""

    source_type: str
    source_id: str
    target_type: str
    target_id: str
    relationship: str  # e.g., "references_field", "uses_table_occurrence"
    context: str = ""  # e.g., which script step, which layout object


@dataclass
class CrossReferenceGraph:
    """The complete cross-reference graph for a FileMaker solution."""

    edges: list[Edge] = field(default_factory=list)

    def add_edge(
        self,
        source_type: str,
        source_id: str,
        target_type: str,
        target_id: str,
        relationship: str,
        context: str = "",
    ) -> None:
        self.edges.append(
            Edge(
                source_type=source_type,
                source_id=source_id,
                target_type=target_type,
                target_id=target_id,
                relationship=relationship,
                context=context,
            )
        )

    def edges_from(self, type_name: str, object_id: str) -> list[Edge]:
        """Get all edges originating from a specific object."""
        return [
            e
            for e in self.edges
            if e.source_type == type_name and e.source_id == object_id
        ]

    def edges_to(self, type_name: str, object_id: str) -> list[Edge]:
        """Get all edges pointing to a specific object."""
        return [
            e
            for e in self.edges
            if e.target_type == type_name and e.target_id == object_id
        ]

    def to_dict(self) -> list[dict[str, str]]:
        """Serialize edges to a list of dicts."""
        return [
            {
                "source_type": e.source_type,
                "source_id": e.source_id,
                "target_type": e.target_type,
                "target_id": e.target_id,
                "relationship": e.relationship,
                "context": e.context,
            }
            for e in self.edges
        ]


def _build_name_to_id_map(
    registry: dict[str, Any],
) -> dict[str, dict[str, list[dict[str, Any]]]]:
    """Build a lookup: type_name -> name -> list of registry entries.

    Used for correlating DDRParser text references (which use names)
    back to IDs in the registry.
    """
    name_map: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for obj in registry.get("objects", []):
        t = obj["type"]
        n = obj["name"]
        if t not in name_map:
            name_map[t] = {}
        if n not in name_map[t]:
            name_map[t][n] = []
        name_map[t][n].append(obj)
    return name_map


def build_graph_from_ddr_xml(
    ddr_xml_path: Path,
    registry: dict[str, Any],
) -> CrossReferenceGraph:
    """Build cross-reference edges by scanning the DDR XML for reference patterns.

    This extracts structural relationships directly from the XML:
    - Table occurrences → base tables (via baseTableId attribute)
    - Relationships → table occurrences (via LeftTable/RightTable)
    - Layouts → table occurrences (via table assignment)
    - Script steps → fields, scripts, layouts (via references in step parameters)
    """
    graph = CrossReferenceGraph()
    by_id = registry.get("by_id", {})

    # Patterns for extracting references from DDR XML
    # Table occurrence → base table
    to_pattern = re.compile(
        r'<Table\s[^>]*\bid="(?P<to_id>[^"]*)"[^>]*\bbaseTableId="(?P<bt_id>[^"]*)"',
    )
    # Relationship → left/right tables
    rel_start_pattern = re.compile(r'<Relationship\s[^>]*\bid="(?P<rel_id>[^"]*)"')
    left_table_pattern = re.compile(r'<LeftTable\s[^>]*\bid="(?P<id>[^"]*)"')
    right_table_pattern = re.compile(r'<RightTable\s[^>]*\bid="(?P<id>[^"]*)"')
    # Field references in various contexts
    field_ref_pattern = re.compile(
        r'<FieldRef\s[^>]*\bid="(?P<field_id>[^"]*)"[^>]*\bname="(?P<field_name>[^"]*)"',
    )
    # Script references
    script_ref_pattern = re.compile(
        r'<ScriptRef\s[^>]*\bid="(?P<script_id>[^"]*)"',
    )
    # Layout references
    layout_ref_pattern = re.compile(
        r'<LayoutRef\s[^>]*\bid="(?P<layout_id>[^"]*)"',
    )
    # Table references (in layout context)
    table_ref_pattern = re.compile(
        r'<TableRef\s[^>]*\bid="(?P<table_id>[^"]*)"',
    )

    current_script_id = ""
    current_layout_id = ""
    current_rel_id = ""
    current_context = ""

    with open(ddr_xml_path, encoding="utf-8", errors="replace") as f:
        for line in f:
            # Track context: which script/layout/relationship we're inside
            script_match = re.search(r'<Script\s[^>]*\bid="(?P<id>[^"]*)"', line)
            if script_match:
                current_script_id = script_match.group("id")
                current_context = "script"

            layout_match = re.search(r'<Layout\s[^>]*\bid="(?P<id>[^"]*)"', line)
            if layout_match:
                current_layout_id = layout_match.group("id")
                current_context = "layout"

            # Table occurrence → base table edges
            for m in to_pattern.finditer(line):
                graph.add_edge(
                    source_type="table_occurrence",
                    source_id=m.group("to_id"),
                    target_type="base_table",
                    target_id=m.group("bt_id"),
                    relationship="based_on",
                )

            # Relationship tracking
            rel_match = rel_start_pattern.search(line)
            if rel_match:
                current_rel_id = rel_match.group("rel_id")

            for m in left_table_pattern.finditer(line):
                if current_rel_id:
                    graph.add_edge(
                        source_type="relationship",
                        source_id=current_rel_id,
                        target_type="table_occurrence",
                        target_id=m.group("id"),
                        relationship="left_table",
                    )

            for m in right_table_pattern.finditer(line):
                if current_rel_id:
                    graph.add_edge(
                        source_type="relationship",
                        source_id=current_rel_id,
                        target_type="table_occurrence",
                        target_id=m.group("id"),
                        relationship="right_table",
                    )

            # Field references
            for m in field_ref_pattern.finditer(line):
                if current_context == "script" and current_script_id:
                    graph.add_edge(
                        source_type="script",
                        source_id=current_script_id,
                        target_type="field",
                        target_id=m.group("field_id"),
                        relationship="references_field",
                        context=f"field: {m.group('field_name')}",
                    )
                elif current_context == "layout" and current_layout_id:
                    graph.add_edge(
                        source_type="layout",
                        source_id=current_layout_id,
                        target_type="field",
                        target_id=m.group("field_id"),
                        relationship="displays_field",
                        context=f"field: {m.group('field_name')}",
                    )

            # Script references (e.g., Perform Script steps)
            for m in script_ref_pattern.finditer(line):
                if current_context == "script" and current_script_id:
                    graph.add_edge(
                        source_type="script",
                        source_id=current_script_id,
                        target_type="script",
                        target_id=m.group("script_id"),
                        relationship="calls_script",
                    )

            # Layout references (e.g., Go to Layout steps)
            for m in layout_ref_pattern.finditer(line):
                if current_context == "script" and current_script_id:
                    graph.add_edge(
                        source_type="script",
                        source_id=current_script_id,
                        target_type="layout",
                        target_id=m.group("layout_id"),
                        relationship="goes_to_layout",
                    )

            # Table references in layouts
            for m in table_ref_pattern.finditer(line):
                if current_context == "layout" and current_layout_id:
                    graph.add_edge(
                        source_type="layout",
                        source_id=current_layout_id,
                        target_type="table_occurrence",
                        target_id=m.group("table_id"),
                        relationship="uses_table_occurrence",
                    )

            # Reset context on closing tags
            if "</Script>" in line:
                current_script_id = ""
                if current_context == "script":
                    current_context = ""
            if "</Layout>" in line:
                current_layout_id = ""
                if current_context == "layout":
                    current_context = ""
            if "</Relationship>" in line:
                current_rel_id = ""

    return graph

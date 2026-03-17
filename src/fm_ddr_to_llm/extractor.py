"""SPEC-002: Streaming Regex ID Extractor.

Crawls DDR XML files line-by-line with regex to extract FileMaker object IDs.
Does not use XML DOM parsing — handles large/malformed files gracefully.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TextIO

from .object_types import OBJECT_TYPES, ObjectTypeDef


@dataclass
class ExtractedObject:
    """A single FileMaker object extracted from DDR XML."""

    type_name: str
    object_id: str
    name: str
    extra: dict[str, str] = field(default_factory=dict)
    # Context: which base table or parent catalog this was found in
    parent_context: str = ""


def _extract_attr(tag_text: str, attr_name: str) -> str | None:
    """Extract a single attribute value from an XML tag string."""
    match = re.search(rf'\b{re.escape(attr_name)}="([^"]*)"', tag_text)
    return match.group(1) if match else None


def _extract_from_tag(tag_text: str, obj_def: ObjectTypeDef) -> ExtractedObject | None:
    """Try to extract an object from a matched XML tag string."""
    obj_id = _extract_attr(tag_text, obj_def.id_attr)
    if obj_id is None:
        return None

    name = _extract_attr(tag_text, obj_def.name_attr) or ""
    extra = {}
    for attr in obj_def.extra_attrs:
        val = _extract_attr(tag_text, attr)
        if val is not None:
            extra[attr] = val

    return ExtractedObject(
        type_name=obj_def.type_name,
        object_id=obj_id,
        name=name,
        extra=extra,
    )


def extract_from_stream(stream: TextIO) -> list[ExtractedObject]:
    """Extract all FM objects from a DDR XML stream.

    Reads line-by-line to handle arbitrarily large files without loading
    the entire DOM. Tolerates malformed XML — extraction is best-effort.
    """
    results: list[ExtractedObject] = []

    # Build compiled patterns for each object type.
    # We use a simpler approach: scan each line for opening tags of interest.
    tag_patterns: list[tuple[ObjectTypeDef, re.Pattern[str]]] = []
    for obj_def in OBJECT_TYPES.values():
        # Match opening tag with at least an id attribute
        pattern = re.compile(
            rf'<{re.escape(obj_def.tag)}\s[^>]*\b{re.escape(obj_def.id_attr)}="[^"]*"[^>]*>',
            re.DOTALL,
        )
        tag_patterns.append((obj_def, pattern))

    # Track current base table context for field extraction
    current_base_table: str = ""
    current_catalog: str = ""

    # Buffer for multi-line tags (tags split across lines)
    buffer = ""
    in_partial_tag = False

    for line in stream:
        # Handle multi-line tags: if a line has an unclosed '<', buffer it
        if in_partial_tag:
            buffer += line
            if ">" in line:
                in_partial_tag = False
                line = buffer
                buffer = ""
            else:
                continue
        elif "<" in line and ">" not in line.rsplit("<", 1)[-1]:
            buffer = line
            in_partial_tag = True
            continue

        # Track catalog context
        if "<BaseTable " in line:
            bt_name = _extract_attr(line, "name")
            if bt_name:
                current_base_table = bt_name

        if "<BaseTableCatalog" in line:
            current_catalog = "BaseTableCatalog"
        elif "<LayoutCatalog" in line:
            current_catalog = "LayoutCatalog"
        elif "<ScriptCatalog" in line:
            current_catalog = "ScriptCatalog"
        elif "<ValueListCatalog" in line:
            current_catalog = "ValueListCatalog"
        elif "<CustomFunctionCatalog" in line:
            current_catalog = "CustomFunctionCatalog"
        elif "<CustomMenuCatalog" in line:
            current_catalog = "CustomMenuCatalog"
        elif "<CustomMenuSetCatalog" in line:
            current_catalog = "CustomMenuSetCatalog"
        elif "<RelationshipGraph" in line:
            current_catalog = "RelationshipGraph"
        elif "<AccountCatalog" in line:
            current_catalog = "AccountCatalog"
        elif "<PrivilegeCatalog" in line:
            current_catalog = "PrivilegeCatalog"
        elif "<ExtendedPrivilegeCatalog" in line:
            current_catalog = "ExtendedPrivilegeCatalog"
        elif "<ExternalDataSourcesCatalog" in line:
            current_catalog = "ExternalDataSourcesCatalog"

        # Try each pattern against the line
        for obj_def, pattern in tag_patterns:
            # Skip Group tags unless we're in the right catalog
            if obj_def.tag == "Group":
                if obj_def.type_name == "layout_group" and current_catalog != "LayoutCatalog":
                    continue
                if obj_def.type_name == "script_group" and current_catalog != "ScriptCatalog":
                    continue

            # Skip Table tags that aren't in RelationshipGraph (vs BaseTable)
            if obj_def.type_name == "table_occurrence" and current_catalog != "RelationshipGraph":
                continue

            for match in pattern.finditer(line):
                obj = _extract_from_tag(match.group(0), obj_def)
                if obj is not None:
                    # Add parent context for fields
                    if obj.type_name == "field" and current_base_table:
                        obj.parent_context = current_base_table
                    results.append(obj)

    return results


def extract_from_file(path: Path) -> list[ExtractedObject]:
    """Extract all FM objects from a DDR XML file."""
    with open(path, encoding="utf-8", errors="replace") as f:
        return extract_from_stream(f)

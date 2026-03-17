"""SPEC-003: ID Registry Output Format.

Defines the structured output that maps extracted FM objects into a
JSON-serializable registry. This is the contract between the extractor
(SPEC-002) and the cross-reference graph builder (SPEC-004/005).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .extractor import ExtractedObject


def build_registry(objects: list[ExtractedObject]) -> dict[str, Any]:
    """Build a structured ID registry from extracted objects.

    Returns a dict with:
    - "objects": list of all objects with their type, id, name, extra, parent_context
    - "by_type": dict mapping type_name -> list of objects of that type
    - "by_id": dict mapping "type_name:object_id" -> object (for lookup)
    """
    registry: dict[str, Any] = {
        "objects": [],
        "by_type": {},
        "by_id": {},
    }

    for obj in objects:
        entry = {
            "type": obj.type_name,
            "id": obj.object_id,
            "name": obj.name,
            "extra": obj.extra,
            "parent_context": obj.parent_context,
        }
        registry["objects"].append(entry)

        # Index by type
        if obj.type_name not in registry["by_type"]:
            registry["by_type"][obj.type_name] = []
        registry["by_type"][obj.type_name].append(entry)

        # Index by composite key
        key = f"{obj.type_name}:{obj.object_id}"
        registry["by_id"][key] = entry

    return registry


def registry_to_json(registry: dict[str, Any], indent: int = 2) -> str:
    """Serialize the registry to a JSON string."""
    return json.dumps(registry, indent=indent, ensure_ascii=False)


def save_registry(registry: dict[str, Any], path: Path) -> None:
    """Write the registry to a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(registry_to_json(registry), encoding="utf-8")


def load_registry(path: Path) -> dict[str, Any]:
    """Load a registry from a JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))

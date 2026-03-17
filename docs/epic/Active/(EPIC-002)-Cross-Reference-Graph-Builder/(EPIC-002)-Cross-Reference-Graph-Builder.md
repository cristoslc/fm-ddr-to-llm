---
title: "Cross-Reference Graph Builder"
artifact: EPIC-002
track: container
status: Active
author: cristos
created: 2026-03-16
last-updated: 2026-03-16
parent-vision: VISION-001
parent-initiative: ""
priority-weight: medium
success-criteria:
  - Correlates DDRParser text output with the ID registry from EPIC-001
  - Builds a cross-reference graph linking objects by their FileMaker IDs (scripts to fields, layouts to table occurrences, etc.)
  - Resolves references across DDRParser's folder structure (e.g., a script in Scripts/ referencing a field defined in BaseTables/)
  - Produces a queryable graph structure suitable for downstream output formatting
depends-on-artifacts:
  - EPIC-001
addresses: []
evidence-pool: ""
---

# Cross-Reference Graph Builder

## Goal / Objective

Take the ID registry produced by EPIC-001 and DDRParser's text output, then build a cross-reference graph that links FileMaker objects by their internal IDs. The graph answers questions like: "which scripts reference field X?", "which layouts use table occurrence Y?", and "what's the data flow from this layout to the underlying table?"

This is the enrichment layer that transforms disconnected documentation into a navigable map.

## Scope Boundaries

**In scope:**
- Matching DDRParser output files to ID registry entries
- Building edges between objects (field references in scripts, TO usage in layouts, etc.)
- Graph data structure suitable for serialization
- Handling ambiguity (e.g., objects with identical names but different IDs)

**Out of scope:**
- ID extraction from raw XML (that's EPIC-001)
- CLI interface and final output format (that's EPIC-003)
- LLM prompt engineering or optimization

## Child Specs

_Updated as Agent Specs are created under this epic._

## Key Dependencies

- EPIC-001 (ID registry output)
- DDRParser output structure (stable — documented in README)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-16 | 6d50e36 | Initial creation |

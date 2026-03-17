---
title: "DDR XML ID Extractor"
artifact: EPIC-001
track: container
status: Active
author: cristos
created: 2026-03-16
last-updated: 2026-03-16
parent-vision: VISION-001
parent-initiative: ""
priority-weight: high
success-criteria:
  - Extracts internal FileMaker object IDs (tables, fields, scripts, layouts, table occurrences, value lists, custom functions, relationships) from raw DDR XML
  - Works via lightweight text/regex crawling — no full XML DOM parsing
  - Handles multi-gigabyte DDR files without loading them entirely into memory
  - Tolerates malformed XML without crashing
  - Produces a structured ID registry (mapping object type + ID to name and metadata)
  - Works for any FileMaker solution without per-solution configuration
depends-on-artifacts: []
addresses: []
evidence-pool: ""
---

# DDR XML ID Extractor

## Goal / Objective

Build a lightweight crawler that extracts internal FileMaker object IDs from raw DDR XML files using text/regex patterns rather than full XML parsing. The output is an ID registry — a structured mapping of every identifiable object in the solution (type, ID, name, and any immediately available metadata like parent table for fields).

This is the foundation the cross-reference graph (EPIC-002) builds on.

## Scope Boundaries

**In scope:**
- Regex/text-based extraction of object IDs from DDR XML
- Streaming/chunked file processing for large files
- ID registry output format (to be determined — JSON or similar)
- Object types: base tables, fields, scripts, script steps, layouts, layout objects, table occurrences, value lists, custom functions, relationships, custom menus
- Error resilience for malformed XML sections

**Out of scope:**
- Full XML DOM parsing
- Cross-referencing between objects (that's EPIC-002)
- DDRParser integration (that's EPIC-003)
- Output format for LLM consumption (that's EPIC-003)

## Child Specs

_Updated as Agent Specs are created under this epic._

## Key Dependencies

- Requires sample DDR XML files for development and testing. No dependency on other EPICs.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-16 | -- | Initial creation |

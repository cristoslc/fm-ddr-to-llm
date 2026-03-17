---
title: "FM DDR to LLM"
artifact: VISION-001
track: standing
status: Active
product-type: personal
author: cristos
created: 2026-03-16
last-updated: 2026-03-16
priority-weight: high
depends-on-artifacts: []
evidence-pool: ""
---

# FM DDR to LLM

## Target Audience

FileMaker developers who want LLMs to reason about their solutions. The tool assumes FM expertise — it doesn't explain what a DDR is or how FileMaker works. Primary user is the author; secondarily, any FileMaker developer with the same need.

## Value Proposition

FileMaker solutions are opaque to LLMs. The DDR contains everything — schema, scripts, layouts, relationships — but it's a monolithic XML blob that's too large, too noisy, and too flat for an LLM to reason about effectively. DDRParser gets halfway there by producing readable files, but strips the internal IDs that make cross-referencing possible.

fm-ddr-to-llm bridges that gap: a deterministic pipeline that produces a structured, cross-referenced representation of any FileMaker solution — one that an LLM can actually navigate. Feed it a DDR, get back a knowledge base where scripts, fields, layouts, and relationships are linked by their FileMaker IDs.

## Problem Statement

DDRParser converts DDR XML into organized text files, but discards FileMaker's internal object IDs during parsing. Without IDs, there's no reliable way to trace which scripts reference which fields, which layouts use which table occurrences, or how objects relate across the solution. Name-based matching is fragile (duplicates, renames, ambiguity). The tool is closed-source, so you can't patch it.

The result: LLMs can read individual files but can't follow the threads that connect them. You get a pile of documentation, not a navigable map.

## Existing Landscape

- **DDRParser** — Converts DDR XML to readable text files. Mature, fast, handles edge cases. Closed-source, strips IDs.
- **VSCode + Copilot indexing** — Free win by dropping DDRParser output into a workspace. Breaks down for cross-cutting context.
- **BaseElements** — Free FileMaker analysis tool. Imports DDR, provides cross-referencing, dependency tracking, broken code detection. Updated for FileMaker 2025 AI script steps. Output lives inside its own FileMaker file — not designed for arbitrary LLM export.
- **InspectorPro 9** — Now free. Built-in AI for script summarization, GitHub/GitLab integration for version tracking. AI is baked into InspectorPro's own UI — not exportable to arbitrary LLM workflows.
- **FMPerception** — Commercial developer intelligence tool. Updated for FileMaker 2025. Deep analysis capabilities but focused on its own analysis UI.
- **Claris MCP** — New in FileMaker 2025. Bridges FileMaker apps and AI assistants via Model Context Protocol. Connects to running FileMaker solutions, not static DDR analysis.
- **Gap:** No existing tool produces a structured, cross-referenced, LLM-agnostic representation from DDR XML.

## Build vs. Buy

1. **Existing solution?** No. All existing tools lock output inside their own UIs or strip critical metadata (IDs).
2. **Glue-code existing tools?** Yes — this is the tier. DDRParser handles the hard formatting work. A custom enrichment layer fills the gap by crawling raw DDR XML with lightweight text/regex extraction to recover IDs and build cross-references.
3. **Build from scratch?** Not needed. DDRParser is the foundation; custom enrichment supplements it.

**Landing: tier 2 — glue-code.**

## Maintenance Budget

Light tending. Two external dependencies that could drift:

- **DDRParser** — output format changes (infrequent).
- **FileMaker DDR XML schema** — changes roughly once per major FileMaker version.

Design minimizes maintenance surface: no running services, isolated extraction patterns, stable output format. Acceptable effort: fix things when they break after a FileMaker or DDRParser version bump.

## Success Metrics

1. **An LLM can answer cross-cutting questions** — "which scripts reference field X?", "what layouts use table occurrence Y?", "trace the data flow from this layout to the underlying table" — using only the pipeline output as context.
2. **Any FileMaker solution works** — drop in a DDR, get output. No per-solution configuration.
3. **Deterministic and reproducible** — same DDR in, same output out. No LLM ops in the pipeline.
4. **Runs in under a few minutes** — even for large multi-file solutions with big DDR XML files.

## Non-Goals

- **Replacing DDRParser** — we supplement it, not rebuild it.
- **Real-time analysis** — no connection to running FileMaker servers or live solutions.
- **LLM operations in the pipeline** — no summarization, embedding generation, or AI-assisted enrichment steps.
- **A UI** — this is a CLI pipeline, not an application with a front-end.
- **Full XML DOM parsing** — the enrichment layer uses lightweight text/regex crawling, not a full XML parser.
- **Competing with BaseElements/InspectorPro/FMPerception** — those are interactive analysis tools. This produces static output for LLM consumption.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-16 | -- | Initial creation from brainstorming session |

# Changelog

## [0.1.0-alpha] - 2026-03-17

First alpha release of fm-ddr-to-llm.

### New Features

- Implement full DDR-to-LLM pipeline (SPEC-001 through SPEC-007): streaming regex
  extractor, ID registry, cross-reference graph, and JSON output — 35 tests passing
- Add DDRParser prerequisite detection with automatic download and macOS installation;
  CLI gates on prereq and offers inline install without restarting

### Bug Fixes

- Detect UTF-16 BOM before opening DDR XML files — FileMaker DDR exports are UTF-16
  LE with BOM; hardcoded utf-8 produced silent mojibake and zero extracted objects

### Documentation

- Add README with full usage docs, architecture overview, and output schema reference
- Create RUNBOOK-001: DDR XML to LLM JSON processing procedure
- Build DDRParser research trove with license analysis, CLI reference, and comparison
  with fm-ddr-to-llm (docs/troves/ddrparser/)

### Other Changes

- Add product Vision (VISION-001) and pipeline Epics (EPIC-001 through EPIC-003)
- Add AGENTS.md and CLAUDE.md swain governance
- Configure .gitignore for Python, FileMaker, pipeline I/O, and local tooling
- Track .tickets/ execution history; exclude ephemeral .tickets/.locks/
- Remove uv.lock — zero runtime deps means fresh resolution is sufficient

# DDRparser Synthesis

## What DDRparser Does

DDRparser is a free command-line tool by HORNEKS ANS that converts FileMaker DDR XML exports into organized, human-readable plain-text files. It accepts two input formats: the traditional DDR (Tools > Database Design Report, available in all FileMaker Pro versions) and the newer Save as XML export (FileMaker Pro 19+). Output is one text file per object (scripts, tables, layouts, etc.) sorted into logical folders by type.

## Key Findings

- **Performance**: Handles multi-gigabyte DDR files in seconds. A 1GB DDR XML across four files parsed in 18 seconds -- fast enough for routine use.
- **Output structure**: Splits into folders: Scripts, Layouts, ValueLists, MenuSets, CustomFunctions, BaseTables, Relationships. Each object gets its own file.
- **Git integration**: Built-in optional auto-commit. Designed for version-control workflows with diff and change tracking.
- **Tool integration**: Works with BBEdit, VS Code, and Kaleidoscope for multi-file search and diff.
- **Platform support**: macOS (Intel + Apple Silicon) and Windows. Current version: 1.4.1.
- **Licensing**: Freeware -- free for personal and commercial use. **No redistribution permitted** ("not redistributed in modified or compiled form without permission"). Not open source. No OSI-approved license. See license analysis below.
- **Translation features**: Built-in multilingual workflow -- extracts translatable strings to POT files, compiles .po/.mo, optional OpenAI auto-translation (since v1.3.0).
- **GUI tool**: Optional FileMaker GUI frontend using ACF plugin (free license expired 2025-09-01; still works in 30-minute sessions).

## Relationship to fm-ddr-to-llm

DDRparser and fm-ddr-to-llm solve related but different problems:

| Dimension | DDRparser | fm-ddr-to-llm |
|-----------|-----------|----------------|
| **Goal** | Human-readable text files for developers | Structured JSON for LLM consumption |
| **Output** | Plain-text files in folders | Single JSON with registry + cross-reference graph |
| **IDs preserved** | No -- strips internal FileMaker object IDs | Yes -- recovers and indexes all object IDs |
| **Cross-references** | Implicit (text search) | Explicit (directed edges between objects) |
| **Primary consumer** | Developers with text editors | LLMs and programmatic tools |

DDRparser is mentioned in the fm-ddr-to-llm README as prior art. The two tools are complementary: DDRparser for human browsing/diffing, fm-ddr-to-llm for machine reasoning.

## Points of Agreement

Both sources confirm:
- FileMaker DDR XML is the canonical source of truth for solution structure
- The XML is too large and opaque for direct consumption
- Parsing needs to handle multi-gigabyte files efficiently
- Git integration is a primary use case for parsed output

## License Analysis

From `license.txt` in the DDRparser 1.4.1 Mac DMG (Copyright 2025 HORNEKS ANS):

1. **Free for personal and commercial use** -- no restrictions on use case.
2. **No redistribution** -- "The software is not redistributed in modified or compiled form without permission." Vendoring or bundling DDRparser in fm-ddr-to-llm is prohibited without explicit permission from HORNEKS ANS.
3. **No name use for promotion** -- cannot use "HORNEKS ANS" or "DDRparser" to promote derived tools.
4. **No warranty** -- AS-IS, user responsible for verifying results.

**Decision for fm-ddr-to-llm**: If DDRParser integration is implemented, it must be an **optional external dependency** that users download and install themselves from horneks.no. The README/RUNBOOK should document it as a prerequisite with a link, not ship or vendor the binary.

## CLI Reference

From `readme.txt` in the distribution:

| Flag | Description |
|------|-------------|
| `-i <file>` | Input DDR Summary XML file |
| `-f <folder>` | Output folder (optional) |
| `-v` | Verbose output |
| `--version` | Show version info |
| `-b` | Enable BaseTable Alt output (Exp and Num) |
| `--clean` | Remove obsolete files from target directories |
| `--git-auto-commit "msg"` | Auto-commit changes to Git |
| `-t` | Extract translatable strings to POT |
| `--create_mo` | Compile .po to .mo |
| `--update-pos` | Update .po/.mo with new strings |
| `--use-openAI-apikey <key>` | Auto-translate via OpenAI |
| `-h` | Show help |

System requirements: macOS 10.13+, Apple Silicon and Intel, terminal access.

## Gaps

- No documentation on DDRparser's internal parsing approach (regex vs DOM vs SAX)
- No API or programmatic output format -- text only
- No information on whether DDRparser could be used as an upstream preprocessor for fm-ddr-to-llm (the license permits use but not redistribution)
- Closed source -- cannot inspect, patch, or extend

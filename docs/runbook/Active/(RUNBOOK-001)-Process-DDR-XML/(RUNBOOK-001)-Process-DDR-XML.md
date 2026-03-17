---
title: "Process DDR XML"
artifact: RUNBOOK-001
track: standing
status: Active
mode: manual
trigger: on-demand
author: cristos
created: 2026-03-17
last-updated: 2026-03-17
validates:
  - VISION-001
  - EPIC-001
  - EPIC-002
  - EPIC-003
parent-epic: ""
depends-on-artifacts: []
---

# Process DDR XML

## Purpose

End-to-end procedure for generating a DDR XML from a FileMaker solution and converting it to structured JSON output using fm-ddr-to-llm. Validates the full pipeline from FileMaker export through to LLM-ready output.

## Prerequisites

- FileMaker Pro installed (any version that supports DDR XML export)
- A FileMaker solution file (.fmp12) to analyze
- Python 3.12+ installed
- fm-ddr-to-llm installed (`uv tool install .` from the project root) or available via `uv run`

## Steps

1. **Action:** Open the FileMaker solution in FileMaker Pro.
   **Expected:** Solution opens successfully with all files accessible.

2. **Action:** Generate the DDR XML export.
   - Go to **Tools > Database Design Report**
   - Select **all files** in the solution
   - Select **all elements** (Tables, Fields, Scripts, Layouts, Relationships, etc.)
   - Set output format to **XML**
   - Choose an output directory and save
   **Expected:** One or more `.xml` files are created in the output directory. For single-file solutions, there will be one XML file. For multi-file solutions, there will be one XML per file.

3. **Action:** Run the pipeline on the DDR XML.
   ```bash
   fm-ddr-to-llm path/to/SolutionName.xml -o output.json
   ```
   **Expected:** Console output shows:
   - `Processing: path/to/SolutionName.xml`
   - Object and cross-reference counts
   - Breakdown by object type
   - `Output saved to: output.json`

4. **Action:** Verify the output file is valid JSON and contains expected sections.
   ```bash
   python3 -c "import json; d=json.load(open('output.json')); print('objects:', d['summary']['total_objects']); print('xrefs:', d['summary']['total_cross_references']); print('types:', list(d['summary']['objects_by_type'].keys()))"
   ```
   **Expected:** Prints object count > 0, cross-reference count > 0, and a list of object types including at least `base_table`, `field`, `script`, `layout`.

5. **Action:** Spot-check a known cross-reference. Pick a script you know references a specific field, then verify:
   ```bash
   python3 -c "
   import json
   d = json.load(open('output.json'))
   script_name = 'YOUR_SCRIPT_NAME'
   scripts = [o for o in d['registry']['objects'] if o['type'] == 'script' and o['name'] == script_name]
   if scripts:
       sid = scripts[0]['id']
       refs = [x for x in d['cross_references'] if x['source_id'] == sid and x['source_type'] == 'script']
       for r in refs:
           print(f\"{r['relationship']} -> {r['target_type']}:{r['target_id']} ({r.get('context', '')})\")
   else:
       print(f'Script not found: {script_name}')
   "
   ```
   Replace `YOUR_SCRIPT_NAME` with an actual script name from the solution.
   **Expected:** Cross-references list includes the expected field references, layout navigations, and/or script calls for that script.

6. **Action:** Feed the output to an LLM. Load `output.json` into your LLM context (Claude Projects, VSCode Copilot workspace, RAG pipeline, etc.) and ask a cross-cutting question like: "Which scripts reference the Email field in the Contacts table?"
   **Expected:** The LLM can answer using the cross-reference data in the JSON, tracing from field ID through the `references_field` edges back to the source scripts.

## Teardown

No cleanup required. The output JSON and DDR XML files can be kept or deleted as needed.

## Run Log

| Date | Executor | Result | Duration | Notes |
|------|----------|--------|----------|-------|
| 2026-03-17 | cristos | - | - | Template created |

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-17 | -- | Initial creation |

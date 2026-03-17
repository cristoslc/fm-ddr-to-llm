# fm-ddr-to-llm

A deterministic pipeline that converts FileMaker Database Design Reports (DDR XML) into structured, cross-referenced JSON output for LLM consumption.

## Why

FileMaker solutions are opaque to LLMs. The DDR contains everything -- schema, scripts, layouts, relationships -- but it's a monolithic XML blob that's too large and flat for an LLM to reason about. Tools like [DDRParser](https://horneks.no/git-source-control-for-filemaker-meet-ddrparser) produce readable files but strip the internal object IDs that make cross-referencing possible.

fm-ddr-to-llm recovers those IDs directly from the DDR XML using streaming regex extraction (no DOM parsing), builds a cross-reference graph linking objects by their FileMaker IDs, and outputs structured JSON that an LLM can navigate.

## Installation

Requires Python 3.12+.

```bash
# Install with uv
uv tool install .

# Or run directly
uv run fm-ddr-to-llm --help
```

## Usage

```bash
# Basic: process a DDR XML file
fm-ddr-to-llm path/to/Solution.xml

# Specify output path
fm-ddr-to-llm path/to/Solution.xml -o output.json
```

The output file defaults to `<input-stem>-llm.json` in the same directory as the input.

### Generating a DDR XML

In FileMaker Pro:

1. Open your solution
2. Go to **Tools > Database Design Report**
3. Select all files and elements
4. Set output format to **XML**
5. Save the report

## Output format

The pipeline produces a single JSON file with four sections:

```json
{
  "meta": {
    "source": "path/to/Solution.xml",
    "version": "0.1.0"
  },
  "registry": {
    "objects": [ ... ],
    "by_type": { ... },
    "by_id": { ... }
  },
  "cross_references": [ ... ],
  "summary": {
    "total_objects": 142,
    "total_cross_references": 87,
    "objects_by_type": { ... }
  }
}
```

### Registry

Every FileMaker object extracted from the DDR, indexed three ways:

- **`objects`** -- flat list of all objects
- **`by_type`** -- grouped by object type (e.g., `base_table`, `field`, `script`)
- **`by_id`** -- keyed by `"type:id"` for direct lookup (e.g., `"field:42"`)

Each object entry:

```json
{
  "type": "field",
  "id": "42",
  "name": "Email",
  "extra": { "fieldType": "Normal", "dataType": "Text" },
  "parent_context": "Contacts"
}
```

### Extracted object types

| Type | DDR XML tag | Extra attributes |
|------|-------------|-----------------|
| `base_table` | `BaseTable` | records |
| `field` | `Field` | fieldType, dataType |
| `table_occurrence` | `Table` (in RelationshipGraph) | baseTable, baseTableId |
| `relationship` | `Relationship` | |
| `layout` | `Layout` | includeInMenu |
| `script` | `Script` | includeInMenu |
| `script_step` | `Step` | enable |
| `value_list` | `ValueList` | |
| `custom_function` | `CustomFunction` | parameters, visible |
| `custom_menu` | `CustomMenu` | |
| `custom_menu_set` | `CustomMenuSet` | |
| `account` | `Account` | status |
| `privilege_set` | `PrivilegeSet` | |
| `extended_privilege` | `ExtendedPrivilege` | |
| `external_data_source` | `ExternalDataSource` | |
| `layout_group` | `Group` (in LayoutCatalog) | |
| `script_group` | `Group` (in ScriptCatalog) | |

### Cross-references

Each cross-reference is a directed edge between two objects:

```json
{
  "source_type": "script",
  "source_id": "500",
  "target_type": "field",
  "target_id": "42",
  "relationship": "references_field",
  "context": "field: Email"
}
```

Relationship types:

| Relationship | Source | Target | Meaning |
|-------------|--------|--------|---------|
| `based_on` | table_occurrence | base_table | TO is based on this table |
| `left_table` | relationship | table_occurrence | Left side of a relationship |
| `right_table` | relationship | table_occurrence | Right side of a relationship |
| `references_field` | script | field | Script step uses this field |
| `displays_field` | layout | field | Layout displays this field |
| `calls_script` | script | script | Perform Script reference |
| `goes_to_layout` | script | layout | Go to Layout reference |
| `uses_table_occurrence` | layout | table_occurrence | Layout is assigned to this TO |

## How it works

```
DDR XML ──► Streaming Regex Extractor ──► ID Registry ──► Cross-Reference Graph ──► JSON Output
   \                                                            ^
    \──────────── (second pass for references) ────────────────/
```

1. **Extract** -- Scan the DDR XML line-by-line with regex patterns to extract object IDs, names, and metadata. No DOM parsing: handles multi-gigabyte and malformed XML files.
2. **Register** -- Build an indexed registry mapping every object by type and composite key.
3. **Cross-reference** -- Scan the XML again to extract structural relationships (field references, script calls, layout assignments, table occurrence mappings).
4. **Output** -- Serialize the registry and graph as JSON.

## Development

```bash
# Run tests
uv run pytest -v

# Run a single test file
uv run pytest tests/test_extractor.py -v
```

## Limitations

- Extraction is regex-based, not a full XML parser. Some edge cases in unusual DDR formatting may be missed.
- Cross-references are extracted from the XML structure (explicit `FieldRef`, `ScriptRef`, `LayoutRef`, `TableRef` elements). References embedded inside calculation text or custom function bodies are not yet extracted.
- DDRParser integration (human-readable text output) is not yet wired into the pipeline. The current pipeline works directly from DDR XML.

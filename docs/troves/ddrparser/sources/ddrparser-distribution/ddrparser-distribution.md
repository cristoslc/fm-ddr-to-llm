---
source-id: "ddrparser-distribution"
title: "DDRparser 1.4.1 Mac Distribution - License and README"
type: document
url: "https://horneks.no/?sdm_process_download=1&download_id=485"
fetched: 2026-03-17T00:00:00Z
hash: "a9b78a619823bf07862086e00c9402c907f66e675d1f4d00e9677df6834cab26"
---

# DDRparser 1.4.1 Mac Distribution

Contents of the DDRparser Mac DMG (DDRparser 1.4.1, dated 2025-08-27 to 2025-09-03):

- `license.txt` — permissive freeware license
- `readme.txt` — version history, usage instructions, CLI options
- `DDRparser_1.4.1.pkg` — macOS installer (signed and notarized by Apple)
- `DDR-GUI-Tool.fmp12` — optional FileMaker GUI frontend
- `XML/` — sample DDR and SaveAsXML exports with parsed output

---

## License (verbatim)

```
DDRparser — Version 1.0.0
Copyright © 2025 HORNEKS ANS

Permission is hereby granted, free of charge, to any person using this software
for personal or commercial use, provided that:

1. The software is not redistributed in modified or compiled form without permission.
2. The name "HORNEKS ANS" and the name "DDRparser" are not used to promote derived tools.
3. This software is provided "as is" without warranty of any kind.

By using this software you accept that you are responsible for verifying the results
produced by the tool in your own workflow or application.

For updates and support, visit: https://horneks.no
```

### License analysis

- **Free for personal and commercial use** — no restrictions on who can use it or for what purpose.
- **No redistribution** — "not redistributed in modified or compiled form without permission." This prohibits vendoring/bundling DDRparser in other distributions.
- **No name use for promotion** — cannot use "HORNEKS ANS" or "DDRparser" names to promote derived tools.
- **No warranty** — AS-IS, user responsible for verifying results.
- **Not open source** — this is a freeware license, not OSI-approved. No source code access, no modification rights.

**Implication for fm-ddr-to-llm**: DDRparser CANNOT be vendored or bundled. If integrated, it must be listed as an external prerequisite that users download and install themselves from horneks.no.

---

## README (verbatim)

### What is it?

DDRparser is a command-line tool that parses FileMaker Database Design Report (DDR) XML exports and splits them into structured, readable text files -- searchable and usable in any code editor. The application is code-signed and notarised by Apple.

### Input formats

1. **DDR format** — Tools > Database Design Report. Produces `Summary.xml` plus per-file XML. Available in all FileMaker Pro versions.
2. **SaveAsXML format** — Tools > Save a Copy as XML. Produces a single XML file. Available in FileMaker Pro 19+.

The tool auto-detects the format.

### CLI Usage

```
DDRparser -i Summary.xml
```

#### Options

| Flag | Description |
|------|-------------|
| `-i <file>` | Input DDR Summary XML file |
| `-f <folder>` | Output folder (optional) |
| `-v` | Verbose output |
| `--version` | Show version info |
| `-b` | Enable BaseTable Alt output (Exp and Num) |
| `--clean` | Remove obsolete files from target directories |
| `--git-auto-commit "msg"` | Automatically commit changes to Git repo |
| `-t` | Extract translatable strings to POT files |
| `--create_mo` | Compile .po files into .mo |
| `--update-pos` | Update .po/.mo files with new strings from .pot |
| `--use-openAI-apikey <key>` | Auto-translate new strings via OpenAI |
| `-h` | Show help |

### Output structure

```
Scripts/
Layouts/
ValueLists/
MenuSets/
CustomFunctions/
BaseTables/
Relationships/
FileInfo/
```

One text file per object, sorted into folders by type.

### System Requirements

- macOS 10.13 or later
- Apple Silicon and Intel supported
- Terminal access

---

## Version History

| Version | Key changes |
|---------|------------|
| 1.4.1 | Improved SaveAsXML parsing performance; added Tooltips and Grouped Button parsing for layouts |
| 1.4.0 | First Windows version (beta); cross-platform ACF scripts in GUI app; reduced memory footprint for translation parsing |
| 1.3.2 | Solution name from File tag; DDR group hierarchy for layouts/scripts; relationship graph CC/CD sync |
| 1.3.1 | Layout/script group hierarchy headings |
| 1.3.0 | Multilingual translation workflows; .po/.mo compilation; OpenAI auto-translation |
| 1.2.0 | Cascade Create/Delete markings in relationships; translatable string extraction |
| 1.1.1 | Theme Catalogue export for both formats; skip unchanged writes to reduce SSD wear |
| 1.1.0 | SaveAsXML format support (beta); bug fixes for relationship graph and Insert Text step |
| 1.0.2 | GUI tool improvements; value-list extraction fixes; relationship layout edits |
| 1.0.1 | Bug fixes for script parsing; XML node extraction tools |
| 1.0.0 | First release |

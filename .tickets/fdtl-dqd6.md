---
id: fdtl-dqd6
status: closed
deps: [fdtl-r3w1]
links: []
created: 2026-03-17T02:15:55Z
type: task
priority: 2
assignee: cristos
parent: fdtl-ayff
tags: [spec:SPEC-006]
---
# SPEC-006: Pipeline CLI Entrypoint

CLI that accepts DDR XML path, orchestrates DDRParser and enrichment stages, outputs structured result. No LLM operations — pure deterministic transformation.


## Notes

**2026-03-17T12:10:31Z**

Pipeline CLI: argparse entrypoint, orchestrates extract→registry→graph→output. Summary stats on stdout. 6 tests pass including determinism and malformed XML.

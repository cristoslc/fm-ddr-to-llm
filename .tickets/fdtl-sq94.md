---
id: fdtl-sq94
status: closed
deps: [fdtl-2t1d]
links: []
created: 2026-03-17T02:15:39Z
type: task
priority: 1
assignee: cristos
parent: fdtl-wygv
tags: [spec:SPEC-002]
---
# SPEC-002: Streaming Regex ID Extractor

Core extraction engine that crawls DDR XML line-by-line or chunk-by-chunk with regex, extracting object IDs without DOM parsing. Must handle multi-gigabyte files without loading into memory. Tolerates malformed XML sections.


## Notes

**2026-03-17T12:10:31Z**

Streaming regex extractor implemented: line-by-line crawl, multi-line tag buffering, catalog context tracking, parent table context for fields, malformed XML tolerance. 12 tests pass.

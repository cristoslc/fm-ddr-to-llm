---
id: fdtl-kycw
status: closed
deps: [fdtl-sq94]
links: []
created: 2026-03-17T02:15:39Z
type: task
priority: 1
assignee: cristos
parent: fdtl-wygv
tags: [spec:SPEC-003]
---
# SPEC-003: ID Registry Output Format

Define the structured JSON output that maps each extracted object (type + ID to name + metadata like parent table for fields). This is the contract between EPIC-001 and EPIC-002.


## Notes

**2026-03-17T12:10:31Z**

Registry output format: JSON with objects list, by_type index, by_id composite key index. Round-trip serialization. 4 tests pass.

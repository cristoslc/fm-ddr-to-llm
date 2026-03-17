---
id: fdtl-r3w1
status: closed
deps: [fdtl-cn5n]
links: []
created: 2026-03-17T02:15:55Z
type: task
priority: 2
assignee: cristos
parent: fdtl-qfq2
tags: [spec:SPEC-005]
---
# SPEC-005: Cross-Reference Edge Builder

Parse references within DDRParser output (field refs in scripts, TO usage in layouts) and link them via IDs from the registry. Produces the cross-reference graph edges.


## Notes

**2026-03-17T12:10:31Z**

Cross-reference edge builder: 7 relationship types (based_on, left_table, right_table, references_field, displays_field, calls_script, goes_to_layout, uses_table_occurrence). edges_from/edges_to queries. 9 tests pass.

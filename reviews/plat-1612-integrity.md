---
id: SR-007
title: "Integrity review — HIPAA Security Rule specification (PLAT-1612)"
type: SpecReview
analysis: integrity
scope: "PR #7: FR-005, FR-008, FR-009, spec/tests.md"
review_set: all
---
## Summary

The new functional requirements have verification criteria and corresponding planned test-case rows. However, FR-008-AC-2 checks the new clause set only against a table that itself misidentifies multiple § 164.308 standards, so passing that consistency check would preserve incorrect regulatory identifiers.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The table labels § 164.308(a)(1), (a)(3), (a)(4), (a)(5), (a)(6), and (a)(7) as standards instead of the actual standard paragraphs ending in `(i)`. | FR-008, FR-008-AC-2 |

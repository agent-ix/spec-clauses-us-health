---
id: SR-014
title: Gap analysis of PLAT-1595 implementation
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-clauses-us-health; FR-008, FR-010, spec/tests.md, spec_clauses_us_health/, tests/"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-clauses-us-health/FR-008", type: references}
  - {target: "ix://agent-ix/spec-clauses-us-health/FR-010", type: references}
---

## Summary

Plan completion: not assessed. Against `origin/main` at `d12dfd2`, this PR raises tagged criteria from 23 to 30 and reduces untagged criteria from 24 to 17. All FR-008-AC-1..5 and FR-010-AC-1..2 criteria are tagged. The implementation files and tests have owning requirements. The code review separately records defects in the legal source mapping and a CI regression.

## Verdict

**FAIL for repository-wide strict coverage** — 17 criteria remain untagged, all outside the newly implemented FR-008 and FR-010-AC-1/2 scope or explicitly planned for later work.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The computed matrix has 17 untagged criteria: FR-001-AC-1/3, FR-006-AC-2/3, FR-007-AC-1/2, FR-009-AC-1/2/3/4/6, FR-010-AC-4, FR-011-AC-2/3/4, NFR-001-AC-2, and NFR-001-M-1. These are outside PLAT-1595 or planned for PLAT-1596, PLAT-1549, PLAT-1559, and the later crosswalk work. All seven criteria covered by this PR are tagged. | spec/tests.md:42-90; tests/test_clause_sets.py |

## Coverage

Plan completion: not assessed. `quoin matrix --repo <PR worktree> --json` reports 53 criteria: 30 tagged, 17 untagged, and 6 method-without-symbol. Baseline `origin/main` reports 23 tagged, 24 untagged, and 6 method-without-symbol. Specifically, FR-008-AC-1..5 and FR-010-AC-1/2 are tagged by the new tests; FR-010-AC-3 is an inspection method and FR-010-AC-4 remains planned for PLAT-1596. No reverse-gap source behavior or stub was found among the changed files. The optional semantic review was not requested and was skipped.

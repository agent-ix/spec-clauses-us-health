---
id: SR-20261104139924
title: "Gap analysis — US health pack repository"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-clauses-us-health; spec/, spec_clauses_us_health/, tests/, reviews/2026-11-16-spec-clauses-us-health-gap-analysis.md"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-clauses-us-health/FR-001", type: references }
---

## Summary

Audited the current spec-to-matrix-to-test chain and the repository's executable test surface. The focused PR tests are substantive, but FR-001-AC-1 remains untagged and the copied gap-analysis record no longer matches the current matrix.

## Verdict

**FAIL** — the full matrix has one untagged criterion, FR-001-AC-1.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-001-AC-1 has no bound test after TC-001 was removed; `quire matrix --strict` exits 1 for this criterion. | spec/functional/FR-001-pack-module-and-home.md:27; tests/test_clause_sets.py; spec/tests.md:74-90 |
| FND-002 | medium | The copied dated gap-analysis artifact reports four untagged criteria, says all are outside this PR, and records stale dispositions for AC-3, NFR-001-AC-2, and NFR-001-M-1. The current matrix has only FR-001-AC-1 untagged; those other three are now tagged, and AC-1 is touched by this PR. Refresh the copied report against current main. | reviews/2026-11-16-spec-clauses-us-health-gap-analysis.md:20-46 |

## Coverage

- Reconciliation: `quire matrix --scope . --format json`; `quire matrix --scope . --strict` exits 1 with FR-001-AC-1 untagged.
- Other matrix states: nine criteria use non-test verification methods and are reported as `method-without-symbol`; these are not static `untagged` criteria.
- Changed coverage: FR-001-AC-2/3 and NFR-001-AC-2/NFR-001-M-1 have trace binders; TC-003, TC-027, and TC-028 are tagged and contain behavioral assertions.
- Reverse gap: no user-facing production surface exists in this repository; executable behavior is the test suite and packaging helpers. No new unowned behavior or source/test stubs were found in the changed code.
- Semantic review: not run.
- Plan completion: not assessed.

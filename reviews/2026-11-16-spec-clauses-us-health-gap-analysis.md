---
id: SR-20261104139922
title: "Gap analysis — spec-clauses-us-health repository audit"
type: SpecReview
analysis: gap-analysis
scope: "spec/, spec_clauses_us_health/, tests/"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-clauses-us-health/FR-006", type: references }
---

## Summary

This repository-driven audit checked the spec, computed Quoin Test Matrix, tagged tests, and code for `agent-ix/spec-clauses-us-health`. The current PR's touched criteria are tagged, but four unrelated repository criteria remain untagged; plan completion was not assessed.

## Verdict

**FAIL** — the full-repository matrix has four untagged acceptance criteria, all outside this PR's diff.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-001-AC-1 has no test bound to its criterion id. | FR-001-AC-1 |
| FND-002 | high | FR-001-AC-3 has no test bound to its criterion id. | FR-001-AC-3 |
| FND-003 | high | NFR-001-AC-2 has no test bound to its criterion id. | NFR-001-AC-2 |
| FND-004 | high | NFR-001-M-1 has no test bound to its criterion id. | NFR-001-M-1 |

## Coverage

- Reconciliation: quoin matrix (Quoin 0.35.0; Quire 0.45.0 / engine 0.60.0)
- Plan completion: not assessed
- Criteria: tagged 84 · untagged 4 · tagged-by-ignored-test 0 · method-without-symbol 9
- Evidence: bound 0 · stale 0 · suspect 0 · undischarged 0 · no run evidence 97
- Coverage totals: 97 criteria; Quire coverage reports 0 untracked symbols and 15 diagnostics (trace-id-outside-marker, criterion-tagged-outside-row, one unmatched trace-target archetype, and one universal-criterion diagnostic).
- Untraced user-facing behaviors: 0; source stubs: 0; test stubs: 0. This repository's executable surface is its test suite and small test helpers; no production application source is present.
- Semantic review: skipped.


## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | deferred | Planner ruling assigns the missing M1 manifest coverage to PLAT-1545, the US health-law module scaffold ticket. This criterion is outside PLAT-1621. |
| FND-002 | deferred | Planner ruling assigns the missing install/module-list coverage to PLAT-1545, the US health-law module scaffold ticket. This criterion is outside PLAT-1621. |
| FND-003 | deferred | Planner ruling assigns the remaining source-metadata coverage to PLAT-1549's publish-gate work. This criterion is outside PLAT-1621. |
| FND-004 | deferred | Planner ruling assigns the remaining rights-metadata publication-check coverage to PLAT-1549. This metric is outside PLAT-1621. |

## Re-audit at PR #33 head 28500bcd1dc02598a5bb05d2f2d81484d62350d0

### Current verdict

**PASS** — the current Quoin Test Matrix has no untagged criteria. The four earlier findings are resolved: FR-001-AC-1 was retired after its M1-only manifest scope became historical, and FR-001-AC-3, NFR-001-AC-2, and NFR-001-M-1 now have tagged tests.

### Current coverage

- Reconciliation: quoin matrix (Quoin 0.35.0; Quire 0.45.0 / engine 0.60.0)
- Plan completion: not assessed
- Criteria: tagged 87 · untagged 0 · tagged-by-ignored-test 0 · method-without-symbol 9
- Evidence: bound 0 · stale 0 · suspect 0 · undischarged 0 · no run evidence 96
- Quire coverage reports 0 untracked symbols and 20 diagnostics (16 trace IDs repeated in docstrings, 2 criterion tags outside a test matrix row, one unmatched trace-target archetype, and one universal-criterion diagnostic).
- Changed tests: 56 passed across `tests/test_clause_sets.py` and `tests/test_publish_gate.py`.
- Untraced user-facing behaviors: 0; source stubs: 0; test stubs: 0. The repository contains tests and test helpers, with no production application source.
- Semantic review: skipped.

## Dispositions — round 2

| FND | outcome | after_excerpt | reason |
| --- | --- | --- | --- |
| FND-001 | fixed | `M1 module initially contained only the Part 11 set. Later milestones added further US sets, superseding that initial manifest shape.` | - |
| FND-002 | fixed | `@pytest.mark.trace("TC-002", "FR-001-AC-2", "TC-003", "FR-001-AC-3")` | - |
| FND-003 | fixed | `@pytest.mark.trace("TC-028", "NFR-001-AC-2")` | - |
| FND-004 | fixed | `@pytest.mark.trace("TC-027", "NFR-001-M-1")` | - |

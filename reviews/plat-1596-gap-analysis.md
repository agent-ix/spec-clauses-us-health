---
id: SR-017
title: "Gap analysis — US health-law pack"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-clauses-us-health; repository-wide spec, tests, clause data, and module"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-001"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-us-health/FR-006"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-us-health/FR-007"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-us-health/FR-011"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-us-health/FR-012"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-us-health/FR-013"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-us-health/NFR-001"
    type: reviews
---

## Summary

Ran repository-wide Quoin matrix and Quire coverage analysis for PLAT-1596. The PR adds trace bindings for all six test-verifiable FR-009 criteria and FR-010-AC-4; FR-009-AC-5 and NFR-001-AC-4 are Analysis methods and correctly have no test symbol. Nineteen other criteria remain untagged, all of them also untagged on clean `origin/main` (25 untagged there versus 19 here); none is newly untagged by this PR.

## Verdict

**FAIL** — the whole-repository matrix still has untagged criteria, although this PR closes six existing gaps and adds no new untagged criterion.

## Coverage

- Reconciliation: `quoin matrix --repo . --json` (Quoin 0.34.0; Quire matrix engine from the installed tool chain).
- Current PR: 62 criteria — 36 tagged, 19 untagged, 7 method-without-symbol; all 62 have no run evidence bound in Quoin's evidence store.
- Clean `origin/main` baseline (`2fdd55c`): 62 criteria — 30 tagged, 25 untagged, 7 method-without-symbol. The six newly tagged criteria are FR-009-AC-1, AC-2, AC-3, AC-4, AC-6 and FR-010-AC-4.
- No untracked symbols. Existing coverage diagnostics include three docstring-only IDs in `tests/test_publish_gate.py` and a declared trace target for an absent StR archetype; they are present on the baseline.
- No plan was supplied. Plan completion: not assessed.
- Reverse-gap inventory: the PR adds one clause-set data file and test helpers only; each changed behavior maps to FR-009/FR-010 and no new CLI, public function, config, or runtime surface is introduced. No new source or test stubs were found.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | Criterion is untagged on this branch and clean main. | FR-001-AC-1 |
| FND-002 | high | Criterion is untagged on this branch and clean main. | FR-001-AC-3 |
| FND-003 | high | Criterion is untagged on this branch and clean main. | FR-006-AC-2 |
| FND-004 | high | Criterion is untagged on this branch and clean main. | FR-006-AC-3 |
| FND-005 | high | Criterion is untagged on this branch and clean main. | FR-007-AC-1 |
| FND-006 | high | Criterion is untagged on this branch and clean main. | FR-007-AC-2 |
| FND-007 | high | Criterion is untagged on this branch and clean main. | FR-011-AC-2 |
| FND-008 | high | Criterion is untagged on this branch and clean main. | FR-011-AC-3 |
| FND-009 | high | Criterion is untagged on this branch and clean main. | FR-011-AC-4 |
| FND-010 | high | Criterion is untagged on this branch and clean main. | FR-012-AC-1 |
| FND-011 | high | Criterion is untagged on this branch and clean main. | FR-012-AC-2 |
| FND-012 | high | Criterion is untagged on this branch and clean main. | FR-012-AC-3 |
| FND-013 | high | Criterion is untagged on this branch and clean main. | FR-012-AC-4 |
| FND-014 | high | Criterion is untagged on this branch and clean main. | FR-012-AC-5 |
| FND-015 | high | Criterion is untagged on this branch and clean main. | FR-013-AC-1 |
| FND-016 | high | Criterion is untagged on this branch and clean main. | FR-013-AC-2 |
| FND-017 | high | Criterion is untagged on this branch and clean main. | FR-013-AC-3 |
| FND-018 | high | Criterion is untagged on this branch and clean main. | NFR-001-AC-2 |
| FND-019 | high | Criterion is untagged on this branch and clean main. | NFR-001-M-1 |

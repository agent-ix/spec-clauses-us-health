---
id: SR-20261104139914
title: "Code review of PLAT-1621 PR #30"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; spec/tests.md, tests/test_m4_discharge.py, tests/corpus/approvals/hipaa-addressable-acceptance.json, tests/corpus/approvals/hipaa-procedure-acceptance.json, tests/corpus/hipaa/audit-event.json, tests/corpus/hipaa/control.json, tests/corpus/hipaa/customer-procedure-placeholder.txt, tests/corpus/hipaa/data-classification.json, tests/corpus/hipaa/role-permission.json"
review_set: subset
---

## Summary

Reviewed the frozen PR #30 diff against PLAT-1621 AC1–6, FR-021-AC1/2, FR-012-AC4/5, FR-006-AC2/3 and FR-019-AC4/5. The focused Quoin discharge test and Python style checks pass, but four assertions leave material parts of those criteria unverified. No applicable AssuranceProfile exists under `spec/`.

## Verdict

**CONDITIONAL** — the addressable, delegated-fact and open-output paths exercise real Quoin commands, but the test does not verify the index-to-matrix count contract, delegated approval output, all rejection conditions, or that evaluation generates no disposition.

## Review Scope

- PLAT-1621 AC1–6.
- FR-021-AC-1/2.
- FR-012-AC-4/5.
- FR-006-AC-2/3.
- FR-019-AC-4/5.
- TC-084 and its test-to-criterion bindings.

## Verification

- `locked-build.sh ... python -m pytest -q tests/test_m4_discharge.py`: passed (1 test).
- `locked-build.sh ... python -m black --check tests/test_m4_discharge.py`: passed.
- `locked-build.sh ... python -m ruff check tests/test_m4_discharge.py`: passed.
- `quire matrix --strict`: recognized all scoped criteria as tagged, but exited 1 for four unrelated existing untagged criteria: FR-001-AC-1, FR-001-AC-3, NFR-001-AC-2 and NFR-001-M-1. `quire coverage` reported no untracked symbols.
- `quire validate` for the spec corpus passed with the ISO and process modules; it reports the existing FR-009 vague-response warning.
- No gap-analysis method was run: the diff adds tests and synthetic fixtures but changes no production code.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | TC-084 compares `rowCount` with the source clause-list length instead of the emitted M4 matrix row count, so an index/matrix mismatch can pass. | tests/test_m4_discharge.py:270-275 |
| FND-002 | medium | Customer-owned rows are not asserted to preserve `delegated` and their `approvalRef` in the RMM tailoring description. | tests/test_m4_discharge.py:297-301 |
| FND-003 | medium | The negative addressable case empties only `rationale`; it does not verify rejection when `accepted_risk` or the named `approvalRef` is missing. | tests/test_m4_discharge.py:341-349 |
| FND-004 | medium | The evaluator binding is saved without checking that evaluation generated no disposition; the test supplies its own separate facts list. | tests/test_m4_discharge.py:82-127, 156-225 |

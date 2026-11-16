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

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-005 | high | TC-084 discharges addressable clause `164.308(a)(5)(ii)(A)` with `delegated`, although FR-012 requires any non-direct addressable discharge to use human `accepted_risk`; Quoin 0.35.0 accepts the nonconforming disposition. | tests/test_m4_discharge.py:220-229, 305-312; spec_clauses_us_health/clauses/us-hhs-45-cfr-164-subpart-c-2026-11-12.json:324-338 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Verified at 0a7419b; the index is now compared with the emitted matrix rows. After excerpt: `assert indexes[M4_KEY]["rowCount"] == len(m4_matrix["rows"])` |
| FND-002 | fixed | Verified at 0a7419b; delegated decision and approval reference are asserted in the RMM tailoring description. After excerpt: `f"delegated (approval {procedure_approval})"` |
| FND-003 | fixed | Verified at 0a7419b; missing decision and missing approvalRef facts are submitted to record-discharge and rejected. After excerpt: `assert rejected.returncode != 0, rejected.stdout` |
| FND-004 | fixed | Verified at 0a7419b; evaluator binding is asserted to contain no disposition or decision fields. After excerpt: `assert all("decision" not in clause and "disposition" not in clause for clause in binding["clauses"])` |
| FND-005 | still-open | Quoin 0.35.0 accepts and renders the test's `delegated` disposition for `164.308(a)(5)(ii)(A)`, whose clause style is addressable. FR-012 Behavior and AC4 require `accepted_risk` for any non-direct addressable discharge; FR-173-AC-13 only covers malformed or missing scope-exclusion fields and does not authorize this pack-level exception. Route the conformance gap to the Quoin engine owner; the test-only assertions do not address it. |


## New findings (disposition pass 2)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-006 | high | TC-084 assigns `accepted_risk` to `164.308(a)(5)(ii)(A)`, whose only expected output is `written-procedure` (kind `procedure`), although FR-006 classifies every all-procedure clause as customer-owned and requires each discharged customer-owned clause to use `delegated`. The accepted-risk example therefore violates FR-006-AC-1/2. | tests/test_m4_discharge.py:44, 220-230, 302-319; spec/spec.md:503-504, 536-549; spec/functional/FR-006-customer-owned-obligations.md:20-25, 34-36; spec_clauses_us_health/clauses/us-hhs-45-cfr-164-subpart-c-2026-11-12.json:324-337 |

## Dispositions — round 2

| FND | outcome | after_excerpt | reason |
| --- | --- | --- | --- |
| FND-005 | fixed | `"decision": "accepted_risk"` | - |
| FND-006 | still-open | - | The clause has only the `written-procedure` expected output; the pack output catalog classifies that as kind `procedure`. FR-006-AC-1 therefore makes it customer-owned and FR-006-AC-2 requires `delegated` for its discharged corpus fact. TC-084 currently sends it through the accepted-risk addressable loop, contrary to the requirement. |


## Dispositions — round 3

| FND | outcome | after_excerpt | reason |
| --- | --- | --- | --- |
| FND-006 | fixed | `if clause["styles"].get("implementation") != "addressable"` | - |

Verified at PR #30 head `7473d9aeb35e4ba3d7f77c3d8f3f3e115d137011`, rebased on merged #32. The merged FR-006-AC-1 now excludes addressable clauses from the customer-owned table even when all their outputs are procedures. TC-021 tests this boundary for both Part 11 and M4; TC-084 retains the accepted_risk disposition for addressable `164.308(a)(5)(ii)(A)` and delegated facts only for non-addressable customer-owned clauses. This resolves FND-006.

## Round 3 verification

- `locked-build.sh ... python -m pytest -q tests/test_m4_discharge.py`: passed (2 tests).
- `locked-build.sh ... python -m black --check tests/test_m4_discharge.py`: passed.
- `locked-build.sh ... python -m ruff check tests/test_m4_discharge.py`: passed.
- `FR-173-AC-13` in Quoin main is unchanged.
- Review of the current diff found no additional code findings.
- The refreshed `reviews/plat-1621-pr30-code-review.md` in the PR still ends with round 2 and `FND-006 still-open`; this scratch artifact contains the round 3 resolution and must replace the stale committed copy before merge.


## Round 4 scope and verification

Reviewed the new fix commit `f411413cc6a8d4006ee2666abb80bb068899b569` at current PR head. It changes only `tests/test_m3_discharge.py` by removing the exact installed-module ref assertion from `_security_module`; the behavior checks remain. No exact `v0.14.0` or `spec-objects-security@vN` pin remains in code or package configuration. The test still resolves the installed module by name, runs Quire validation and the `threat-has-control` relation query, and asserts the expected threat id, covered state, linked control id, and `mitigates` verb; the focused test passed.

All earlier code-review findings FND-001 through FND-006 retain their latest `fixed` outcome. No new code findings were introduced. The prior artifact freshness issue is resolved by the current dated artifact `reviews/2026-11-16-plat-1621-pr30-code-review.md`, which carries the round 3 FND-006 disposition; the nondated `reviews/plat-1621-pr30-code-review.md` remains as preserved history. The current artifact includes this round 4 delta review.

- `locked-build.sh ... python -m pytest -q tests/test_m3_discharge.py`: passed (1 test).
- `locked-build.sh ... python -m black --check tests/test_m3_discharge.py`: passed.
- `locked-build.sh ... python -m ruff check tests/test_m3_discharge.py`: passed.
- `FR-173-AC-13` remains unchanged in Quoin main.

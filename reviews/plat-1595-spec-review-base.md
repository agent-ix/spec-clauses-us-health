---
id: SR-015
title: Base review of PLAT-1595 TestMatrix updates
type: SpecReview
analysis: base
scope: "agent-ix/spec-clauses-us-health; spec/tests.md TC-032..TC-036, TC-043..TC-044; tests/test_clause_sets.py"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-clauses-us-health/FR-008", type: references}
  - {target: "ix://agent-ix/spec-clauses-us-health/FR-010", type: references}
---

## Summary

The TestMatrix rows for TC-032..TC-036 and TC-043..TC-044 now report implementation, and each has a corresponding criterion-tagged test. One changed test description does not match the criterion's stated behavior for unknown classification values.

## Verdict

**CONDITIONAL** — one medium finding remains.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | TC-036 now says an undeclared `cyber_device` value is “reported,” and its test expects exit 0 with `unresolved` plus an `unknown_value` reason; FR-008-AC-5 still says the set “rejects an undeclared value.” Clarify whether rejection means a nonzero refusal or an unresolved result with a diagnostic, then align the criterion, test, and matrix row. | spec/tests.md:96; spec/functional/FR-008-fdca-section-524b-clause-set.md:46; tests/test_clause_sets.py:386-410 |

## Scope

| Unit | Role | Result |
| --- | --- | --- |
| TC-032..TC-036 | examined | Each changed row maps to FR-008-AC-1..5 and is marked implemented; tests carry matching trace tags. TC-036's wording diverges from FR-008-AC-5. |
| TC-043..TC-044 | examined | Both rows map to FR-010-AC-1/2, are marked implemented, and have matching tags. |
| FR-008-AC-1..AC-5 | examined | The source/version, IDs, applicability, clause outputs, and undeclared-value requirement are stated. AC-5 needs a clearer expected result. |
| FR-010-AC-1..AC-4 | examined | AC-1/2 align with the new catalog tests; AC-3 and AC-4 remain planned for source-authoring and PLAT-1596. |

---
id: SR-005
title: "Code review — HIPAA Security Rule specification (PLAT-1612)"
type: SpecReview
analysis: code-review
scope: "PR #7: spec/spec.md, spec/functional/FR-005-pack-wide-output-catalog.md, spec/functional/FR-008-hipaa-security-rule-clause-set.md, spec/functional/FR-009-hipaa-nist-crosswalk-source-and-target.md, spec/tests.md"
review_set: all
---
## Summary

Reviewed the specification diff for soundness, test intent, internal consistency, source fidelity, and implementation handoff. Found one high-severity legal-clause identity error and one medium-severity missing owner reference for a planned output producer.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The normative table uses incorrect § 164.308 standard IDs: `(a)(1)`, `(a)(3)`, `(a)(4)`, `(a)(5)`, `(a)(6)`, and `(a)(7)` omit the actual `(i)` paragraph. | FR-008, FR-008-AC-2 |
| FND-002 | medium | The `health-data-flows` catalog row still says only that a separate Data-Flow Model issue owns the producer. It does not identify PLAT-1756, so the normatively specified output has no actionable owner link in the PR. | FR-005 |
## New findings (disposition pass 2)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | medium | FR-005-AC-1 now requires all 28 catalog rows, but the current test still asserts 25; GitHub CI fails with `assert 28 == 25`. | FR-005-AC-1 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Fixed; verified in PR head 3addbdf. |
| FND-002 | fixed | Fixed; verified in PR head 3addbdf. |
| FND-001 | fixed | Fixed; reverified on c2c440d748f35085a4addc8d596a061ec8cbb817. FR-008-AC-2 is now FR-012-AC-2 and still names the six corrected identifiers. |
| FND-002 | fixed | Fixed; reverified on c2c440d748f35085a4addc8d596a061ec8cbb817. The `health-data-flows` row still names PLAT-1756. |
| FND-003 | still-open | GitHub CI run 43704164941 fails because tests/test_clause_sets.py::test_us_clause_set_output_catalog_matches_the_spec asserts 25 while the current spec has 28 catalog entries. |
| FND-003 | fixed | Fixed and verified on a5afd94d7c74804d0abed851f8ef9bcd84ea2f9d. `tests/test_clause_sets.py` now asserts 28, matching FR-005-AC-1; the focused suite passed 27 tests. |

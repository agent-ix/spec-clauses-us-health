---
id: SR-004
title: "Code review of Part 11 output bindings (PLAT-1553)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; PR #5 at 77b986ce: tests/test_clause_sets.py, tests/test_part11_outputs.py, spec/spec.md, spec/tests.md, Part 11 clause data"
review_set: subset
---

## Summary

Reviewed the changed Python tests, output catalog changes, TestMatrix rows, and ticket ACs. The Part 11 output table comparison and customer-owned classification assertions align with the stated criteria. No NFR-001 package/corpus/string scan was added. Two high-severity duplication findings remain in the changed test code.

## Verdict

**FAIL** — FND-001 and FND-002 are high-severity duplication findings under the code-review policy. CI is green at 77b986ce; tests were not run during this review.

## Scope

| Unit | Role | Result |
| --- | --- | --- |
| PLAT-1553 ACs 1–6 | examined | The output definitions are tied to the existing capability names; tests compare Part 11 expected outputs with the normative spec table, exercise § 11.30 for closed/open cases, compare customer-owned rows with procedure-only outputs, and call the existing cross-set helper. |
| FR-003-AC-3, FR-004-AC-1/2, FR-005-AC-2, FR-006-AC-1 | examined | Changed tests carry matching FR criterion tags; quoin matrix reports each criterion tagged. |
| NFR-001 licensing boundary | examined | New tests parse the spec output tables and compare clause identifiers/output names; no package, corpus, or string scan was introduced. |
| spec/tests.md changed rows | examined | TC-010, TC-012/013, TC-019 and TC-021 are marked implemented and have tagged tests in the repository. |
| CI | examined | PR checks and CLA checks pass; tests were not run by this review. |

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | US_OUTPUT_CATALOG is a second manually maintained copy of the output catalog defined in spec/spec.md. This PR changes four entries in that duplicate and retains an equality test as a drift gate; the duplicated data can still drift and must be removed. Use the spec table as the single source and validate the clause-set catalog against it without a second catalog literal. | tests/test_clause_sets.py:31-65,233-250 |
| FND-002 | high | The new test_part11_outputs module repeats behavior already asserted in test_clause_sets.py: the open/closed § 11.30 outcomes are covered by the existing FR-004 tests, and the all-US-set consistency-helper invocation is already in test_all_declared_sets_load_and_match_one_catalog. These parallel tests create duplicate owners for the same assertions; extend/tag the existing tests and remove the duplicates. | tests/test_part11_outputs.py:71-81,108-115; tests/test_clause_sets.py:540-566,297-300 |

## Assurance Context

No active AssuranceProfile applies to output-catalog/test coverage changes. AP-201 governs finding measurement and report rendering; AP-202 governs live Jev lens evaluation.

---
id: SR-20261104139935
title: "Gap analysis of PLAT-1826 PR #36"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-clauses-us-health; FR-014, FR-015, FR-018, FR-019 and their tests"
review_set: subset
---

## Summary

Ticket: PLAT-1826. Planless audit; plan completion is not assessed. `quire matrix --scope . --format json` at 33ddd519 tags every AC of the touched requirements:

- FR-014-AC-1..5 and FR-015-AC-1..5 each have one or more tests.
- FR-018-AC-1 is tagged by TC-075.
- FR-018-AC-2 is tagged by four TC-076 tests: the exact-one-class partition, the producers that exist, the customer-provided outputs, and no owner ticket with a non-tool documentation-level decision.
- FR-018-AC-3 is tagged by TC-077.
- FR-019-AC-1..5 are tagged by the M2, M3 and M4 discharge tests.

The only production change is clause data. It equals the normative spec tables (TC-075 and the FR-015-AC-2/3 tests pass), and there are no stubs. The partition test makes the catalog keys equal the disjoint union of the produced, customer-document and customer-procedure classes, so a new unclassified output fails.

## Verdict

**PASS.** There are no untagged criteria, no reverse gaps and no stubs. The changed ACs fail on origin/main data and pass at HEAD (measured). Test strength is covered in the code-review artifact (one vacuous sub-assertion, SR-20261104139934 FND-001). Semantic review was not run.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No gaps found (placeholder) | - |

## Coverage

- Criteria examined: FR-014-AC-1..5, FR-015-AC-1..5, FR-018-AC-1..3 and FR-019-AC-1..5. All are tagged.
- Semantic review: skipped. It is not requested in this dispatch.
- Plan completion: not assessed

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-002 | high | The fix round adds FR-018-AC-4 (installed commands exist and dossier kinds are registered) and FR-018-AC-5 (no owner ticket; `documentation-level-decision` is a customer document). No test carries either trace tag: `quire matrix` at f76d2a43 reports both `untagged`. The TC-076 tests assert both, but are tagged `FR-018-AC-2` only; spec/tests.md maps TC-076 to all three ACs. Add `"FR-018-AC-4"` to `test_m2_record_outputs_name_producers_that_exist` and `"FR-018-AC-5"` to `test_m2_outputs_name_no_owner_ticket_and_no_tool_decision`. | tests/test_premarket_outputs.py:207,246 |
| FND-003 | low | FR-018-AC-2 says the customer record, document and procedure classes "state that no toolchain producer exists". The procedure branch is untested: the loop checks only `startswith("Customer-owned")`. The `written-procedure` catalog description ("Customer-owned written procedure.") does not say it, and it cannot change, because it is shared with the EU pack. Only the mapping row states it. Assert `"no toolchain producer" in rows[output]["producer_or_owner"]` for procedures, and word AC-2 so that the mapping row is what states it. | tests/test_premarket_outputs.py:241-243; spec/functional/FR-018-m2-output-producer-mapping.md:49 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-002 | fixed | Verified at bd81fb4c: `quire matrix` reports FR-018-AC-4 tagged by `test_m2_record_outputs_name_producers_that_exist` and FR-018-AC-5 tagged by `test_m2_outputs_name_no_owner_ticket_and_no_tool_decision`, and all FR-018 ACs are tagged. After excerpt: `@pytest.mark.trace("TC-076", "FR-018-AC-2", "FR-018-AC-4")` / `@pytest.mark.trace("TC-076", "FR-018-AC-2", "FR-018-AC-5")` |
| FND-003 | fixed | Verified at bd81fb4c by running it: deleting "; no toolchain producer" from the written-procedure mapping row now fails `test_m2_outputs_without_a_producer_are_customer_provided`. AC-2 now says the mapping row is what states it. After excerpt: `assert "no toolchain producer" in rows[output]["producer_or_owner"], output` / `the mapping row of each of the last three states that no toolchain producer exists` |

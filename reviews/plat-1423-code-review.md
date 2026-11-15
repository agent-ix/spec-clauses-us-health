---
id: SR-001
title: "Code review — Part 11 clause set (PLAT-1423)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; spec_clauses_us_health/clauses/us-fda-21-cfr-11-2026-11-12.json; tests/test_clause_sets.py; spec/tests.md"
review_set: subset
---

## Summary

Reviewed the Part 11 clause data and new Python tests against PLAT-1423 AC-1–8, the PLAT-1422 normative table, and the public eCFR Part 11 page. The reviewed test methods are trace-tagged; two source summaries miss material requirements, and the test oracle duplicates the normative clause ID list.

## Verdict

**FAIL** — FND-001 is a high P0 duplicate; FND-002 and FND-003 are material gaps in the authored clause summaries.

## Scope

| Unit | Role | Result |
| --- | --- | --- |
| FR-002-AC-1..3 | examined | Rights metadata, publish-check acceptance, and synthetic licensed-set refusal are asserted by TC-005..007. |
| FR-003-AC-1..5 | examined | Key/source, 25 IDs, mandatory text/output completeness, invalid-output rejection, and 11.100(c) catalog mapping are asserted by TC-008..011 and TC-031. |
| FR-004-AC-1..6 | examined | Closed/open outcomes, per-paragraph assessments, method gating, unresolved defaults, and invalid dimensions/values are asserted by TC-012..017. |
| FR-007-AC-3 | examined | TC-026 asserts one recorded fact renders compliant and another applicable clause remains undischarged. |
| NFR-001-AC-3 | examined | Manual wording review used only the cited public eCFR source; no package, corpus, or string scan was used. |
| `spec/tests.md` PLAT-1423 status rows | examined | Newly implemented rows correspond to the added trace-tagged tests; broader planned rows remain unchanged. |
| Changed CI/workflow files | examined | None changed in this PR. |

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | `PART_11_IDS` repeats the 25-ID normative table in `spec/spec.md`; TC-009 compares the evaluated set to that second list rather than to the normative table. This is duplicate requirement data and can drift while the test still passes against a stale oracle. Read the expected IDs from the normative table or establish one source of truth. | tests/test_clause_sets.py:35-52 |
| FND-002 | medium | The summary for 11.300(d) says to alert “promptly,” weakening the source’s requirement to report attempted misuse “in an immediate and urgent manner.” Preserve that urgency in the summary. | spec_clauses_us_health/clauses/us-fda-21-cfr-11-2026-11-12.json:919-922 |
| FND-003 | medium | The 11.10(e) summary omits that audit-trail documentation must be available for agency review and copying, and does not state that the trail independently records the date and time of operator entries/actions. These are required parts of the control. | spec_clauses_us_health/clauses/us-fda-21-cfr-11-2026-11-12.json:319-322 |
| FND-004 | medium | The new set’s 11 used `outputCatalog` entries are not compared to the canonical spec catalog. TC-018 compares a separate test constant to `spec/spec.md`, while the cross-set test with this single set can only detect conflicts between sets. The current 11 entries match the spec, but a drift in the clause JSON would pass. | tests/test_clause_sets.py:215-244, 285-289 |
| FND-005 | low | The new pytest functions lack the Description, Assumptions, and Criteria docstrings required by the Python test guidance; the trace markers are present. Add concise docstrings to the new tests. | tests/test_clause_sets.py:415-622 |

## Source Review

The set cites the official eCFR Part 11 page, and its version date matches the page's “up to date as of 11/12/2026” notice. The summaries are original, concise paraphrases of public law; they do not reproduce eCFR prose. No paywalled standard is named or used as a source. Rights metadata states `citation_only`, `original`, and the public-law basis. This review did not scan package or corpus contents for licensing.

## Assurance Context

No active AssuranceProfile applies to this clause-set authoring change.


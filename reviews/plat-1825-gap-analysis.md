---
id: SR-20261104139932
title: "Gap analysis of PLAT-1825 PR #35"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-clauses-us-health; FR-008, FR-010, FR-011, FR-020 and their tests"
review_set: subset
---

## Summary

Ticket: PLAT-1825. Planless; plan completion: not assessed. Touched requirements: FR-008-AC-3 (TC-034, two tests), FR-010-AC-3 (TC-045, four tests), FR-011 (crosswalk rows `524B(b)(1)`→`VI.B` and `VI.B`→`RA-5`/`SI-5`, covered by the existing crosswalk tests, which pass) and FR-020-AC-3 (M3 discharge test). Each changed AC has a tagged test that asserts behavior and fails on origin/main's data. There are no stubs and no production code outside the clause data.

## Verdict

**CHANGES REQUESTED.** One gap: the new V.A.1 producer mapping is not exercised by the corpus. The FR-008-AC-3 cross-term branch is untested; it is recorded as a spec defect in the spec-review artifact.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | V.A.1 maps `threat-model` to `quoin dossier generate --doc threat-model`, but the corpus has no `threat_model` record, so nothing proves the mapping and V.A.1 renders undischarged. Minimum corpus to add, plus one test: (1) THREATMODEL-M3-001 (`threat_model`), with `method` and `reviewed_by` frontmatter, `## Scope`, `## Assumptions` and `## Out of scope` sections, and relationships `scopes` → CONN-M3-001 and BOUNDARY-M3-001 and `considers` → THREAT-M3-001; (2) CONN-M3-001, a spec-objects-architecture `connection` with `crosses` → BOUNDARY-M3-001; (3) a `threatens` → CONN-M3-001 edge on THREAT-M3-001; (4) an `arises_from` → THREAT-M3-001 edge on RISK-M3-001. The test runs `quoin dossier generate --doc threat-model --scope <project>` and asserts that DOS-TM lists THREATMODEL-M3-001, a crossing row for CONN-M3-001 with THREAT-M3-001 (tampering) and CTRL-M3-001, `Open findings: none` and zero gaps. It then records a V.A.1 discharge fact citing the generated document and asserts V.A.1 `compliant`. | tests/test_m3_discharge.py:318-323 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-002 | low | The `### Open findings none` assertion only partly proves anything. The `crossing-without-threat` flow rule fires only for a scoped connection that `carries` a `data_classification`. CONN-M3-001 carries none, so that check can never fire. Measured: deleting THREAT-M3-001's `threatens` edge still renders `none` and status `complete`. (`threat-without-treatment` is live: deleting CTRL-M3-001 yields a gap.) Add a `carries` edge from CONN-M3-001 to a corpus `data_classification` record, so that `none` proves the threat closes the crossing. | tests/corpus/security/CONN-M3-001.md:6-8 |
| FND-003 | low | FR-020-AC-5 has no trace tag on the M3 test (it has FR-020-AC-1..4 only). The new tests.md row reads "Planned for PLAT-1608" although it is implemented by this PR. Add `@pytest.mark.trace("FR-020-AC-5")` and mark the row implemented. | tests/test_m3_discharge.py:118-124 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Verified at e8f7e3b1 by running it. `quoin dossier generate --doc threat-model --scope <corpus> --version 1 --json` exits 0 with DOS-TM status `complete` and gaps `[]`. The document lists THREATMODEL-M3-001 and the crossing row. Without THREATMODEL-M3-001 the status is `incomplete` with gap `no_threat_model`, so the test fails. The M3 test discharges V.A.1 from the generated document and asserts `compliant` (passes). After excerpt: `| CONN-M3-001 | none | BOUNDARY-M3-001 (semi_trusted) | THREAT-M3-001 (tampering) | CTRL-M3-001 (not stated) | RISK-M3-001: not_accepted, reviewer@example.invalid |` |

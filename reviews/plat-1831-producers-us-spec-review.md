---
id: SR-20261104139947
title: "Spec review of PLAT-1831 spec-clauses-us-health PR #42 (catalog producers)"
type: SpecReview
analysis: base
scope: "agent-ix/spec-clauses-us-health; spec/functional/FR-005-pack-wide-output-catalog.md, spec/spec.md (US Output Producers), spec/tests.md (PR #42 head fba28a1)"
review_set: subset
---

## Summary

Ticket: PLAT-1831. Reviewed the new FR-005 statements, FR-005-AC-5 and AC-6, and the "US Output Producers" section against quoin FR-211, quire-rs FR-073 and the PLAT-1853 decision (option (a): customer-supplied artifacts get a retained kind that packs list in `producers`). `quire validate` passes on both files.

## Verdict

**Changes requested.** The producers table is real contract, not ceremony. It follows the repository's existing rule that spec.md holds the canonical catalog entry that every set must equal, and `producers` is part of that entry. It pins no count. The defect is the closed "SHALL NOT" prohibition and the "every other output" classification, which contradict the PLAT-1853 direction and cannot be tested. AC-5 also bundles two obligations, and AC-6 is not an obligation of this module.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The SHALL NOT forbids `producers` on customer-supplied and tool-rendered outputs. That contradicts the PLAT-1853 decision to give customer artifacts a retained kind that packs list. The "every other output" classification also leaves out outputs that are neither kind (system-validation, audit-logging, audit-trail, signed-record), and no test can check it. Delete the bullet and the "Every other output omits... Omission means" paragraph, and keep the table as the contract. | spec/functional/FR-005-pack-wide-output-catalog.md:31-33; spec/spec.md:571-575 |
| FND-002 | low | FR-005-AC-5 is compound: it covers kind validity and conformance to the table. The FR-005 bullet also lists the four outputs again, which duplicates the table. Split the AC and refer to the table instead of listing names. | spec/functional/FR-005-pack-wide-output-catalog.md:23-30,43 |
| FND-003 | low | FR-005 allows "an experiment or operational record's `subject.kind`", but AC-5 says "from the quoin FR-211 set" and its test accepts only the five family kinds. State that this pack names only family kinds, or align the AC and the test. | spec/functional/FR-005-pack-wide-output-catalog.md:25-27 |
| FND-004 | low | FR-005-AC-6 ("installed quire validates and evaluates every set with producers") is quire-rs FR-073-AC-7/AC-9's contract. The existing publish-check criteria already cover it here, and its test is vacuous when no set carries producers. Delete it, along with its TC-086 row. | spec/functional/FR-005-pack-wide-output-catalog.md:44; spec/tests.md:108,282 |

## Dispositions

Round 1, checked against `git diff fba28a13..eb8b71d8` (head eb8b71d). `quire validate --scope .` passes on `spec/functional/FR-005-pack-wide-output-catalog.md`, `spec/spec.md`, `spec/tests.md` and the three `reviews/plat-1831-producers-us-*.md` files. `quoin matrix` shows FR-005-AC-5 and FR-005-AC-6 as `tagged`.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | The SHALL NOT bullet and the "Every other output omits... Omission means" paragraph are deleted. The table is now the contract. |
| FND-002 | fixed | The AC is split into AC-5 (kind vocabulary) and AC-6 (conformance to the table). The bullet refers to the table instead of listing names. |
| FND-003 | fixed | FR-005 now states that the module uses only the family kinds and names no experiment or operational `subject.kind`. AC-5 and the test agree. |
| FND-004 | fixed | The quire-acceptance AC and TC-086 are removed. AC-6 now means conformance to the table and is traced to TC-018. |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-005 | low | spec/tests.md:108 maps FR-005-AC-6 to TC-018, and the test carries the tag, but the TC-018 row lists only FR-005-AC-1 and still reads "Planned for PLAT-1545". Fix: add FR-005-AC-6 to that row's requirement cells. | spec/tests.md:108,214 |
| FND-006 | low | FR-005-AC-5 says each set's `producers` lists "distinct, unpadded" kinds, but TC-085 checks only that spec-table kinds belong to the family set; distinctness belongs to quire FR-073-AC-9. Fix: reword AC-5 to "Every kind in the US Output Producers table is one of run, scan, mock-inspection, analysis-report, scenario." | spec/functional/FR-005-pack-wide-output-catalog.md:38 |

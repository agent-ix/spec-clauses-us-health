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

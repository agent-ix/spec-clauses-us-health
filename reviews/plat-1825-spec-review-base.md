---
id: SR-20261104139933
title: "Spec review of PLAT-1825 PR #35"
type: SpecReview
analysis: base
scope: "agent-ix/spec-clauses-us-health; spec/functional/FR-008-fdca-section-524b-clause-set.md, spec/functional/FR-010-cybersecurity-output-catalog.md, spec/functional/FR-020-m3-cybersecurity-corpus-discharge.md, spec/spec.md, spec/tests.md"
review_set: subset
---

## Summary

Ticket: PLAT-1825. Spec review with integrity and EARS checks of the FR-008, FR-010 and FR-020 edits, the master 524B table, the crosswalk table and the output catalog. `quire validate` passes on all five files.

## Verdict

**CHANGES REQUESTED** (two medium findings).

Design judgements:

- **The `additional_cybersecurity_regulation` dimension is an honest use of applicability.** The ClauseSet schema has no static "never" op, only `all`, `any`, `not`, `eq`, `in` and `at_least`. The clause is a real statutory paragraph that FR-008-AC-2 must keep. The user states the fact, and the pack does not infer it. `issued` makes it bind to a customer-provided document, so the set still works if FDA issues a regulation before a new pack version. The cost is one more context value per user; without it, the row reads undetermined (see code-review FND-006).
- **The VI.B retarget from SR-2 to RA-5 and SI-5 is defensible.** VI.B of the guidance is the cybersecurity management plan: vulnerability monitoring, coordinated disclosure and patch timelines. That matches vulnerability monitoring (RA-5) and advisories (SI-5), not a supply-chain risk plan (SR-2). SI-2 (flaw remediation) would also fit; adding it is optional.
- **The new `524B(b)(1)`→`VI.B` crosswalk is correct.**

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | FR-008-AC-3 and the master prose say that with `cyber_device` absent every 524B clause is unresolved. Measured with quire 0.52.0: `cyber_device` absent plus `additional_cybersecurity_regulation=none_issued` makes `524B(b)(4)` `not_binding`, because `all` resolves false on the known term. The spec states an outcome the engine does not produce, and no test covers that combination. State this case in AC-3 and spec.md, and add it to the TC-034 test. | spec/functional/FR-008-fdca-section-524b-clause-set.md:51 |
| FND-002 | medium | FR-010-AC-3 allows two classes: a named installed producer command, or a customer-provided document. The 524B set's catalog also holds `security-risk-records` (person-authored spec-objects-security records) and `soup-list`, which fit neither class. Add a third class, records the customer authors in a named module, or name `quoin soup report` for `soup-list`. The test must then partition the whole catalog (code-review FND-001). | spec/functional/FR-010-cybersecurity-output-catalog.md:47 |
| FND-003 | low | New status cells read "Implemented in PLAT-1825": ticket narration in a public spec table. The convention predates this PR across tests.md; prefer a bare "Implemented" for the rows this PR writes. | spec/tests.md:128,236 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Verified at e8f7e3b1. Stating the engine's behaviour is the right call: if no regulation exists there is no (b)(4) obligation, whether or not the device is a cyber device. A test now covers the case. After excerpt: `With cyber_device absent, 524B(b)(4) is not binding for additional_cybersecurity_regulation=none_issued and the other clauses stay unresolved.` |
| FND-002 | fixed | Verified at e8f7e3b1. AC-3 now defines three exclusive classes, and soup-list names `quoin soup report` (the only US set using soup-list is 524B). After excerpt: `Every cybersecurity catalog row is in exactly one class: it names a producer command that exists in its installed CLI, it names the module whose records the customer authors, or it is a customer-provided document.` |
| FND-003 | fixed | Verified at e8f7e3b1. After excerpt: `| FR-010 | FR-010-AC-3 | TC-045 | ✅ Implemented |` |

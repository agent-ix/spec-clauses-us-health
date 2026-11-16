---
id: SR-20261104139926
title: "Specification integrity review — PLAT-1545/PLAT-1549 changes"
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-clauses-us-health; spec/functional/FR-001-pack-module-and-home.md, spec/functional/FR-002-rights-metadata-is-truthful-and-publishable.md, spec/non-functional/NFR-001-licensing-boundary.md, spec/tests.md"
review_set: subset
---

## Summary

Checked completeness, consistency, atomicity, and testability of the changed criterion and measurement language. The rights boundary now distinguishes pack-owned structured metadata checks from Quire's restricted-text publish check; the remaining inconsistency is the retired historical test paired with an active obsolete criterion.

## Verdict

**FAIL** — FR-001-AC-1 has no current observable test contract, and the test plan records a commit revision.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-001-AC-1 specifies an M1-only manifest invariant, but its test is retired after later sets were added. The criterion's present tense and `Test` method conflict with the historical-only rationale; redefine it as a current manifest obligation or remove the obsolete criterion. | spec/functional/FR-001-pack-module-and-home.md:27; spec/tests.md:74-90 |
| FND-002 | high | The historical rationale stores a Git commit hash in the test plan, creating a recorded-revision pin. Remove the hash and keep the explanation at the level of the M1-only history. | spec/tests.md:74-75 |

## Dispositions

| FND | outcome | after_excerpt | reason |
| --- | --- | --- | --- |
| FND-001 | fixed | `The M1 module initially contained only the Part 11 set. Later milestones added further US sets, superseding that initial manifest shape.` | - |
| FND-002 | fixed | `TC-001 is retired after M1: it covered the initial one-set manifest, whose shape was superseded as later US sets were added. Do not assert the historical M1 manifest shape against the expanded current module.` | - |

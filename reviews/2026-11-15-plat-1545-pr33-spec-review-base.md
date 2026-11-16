---
id: SR-20261104139925
title: "Base specification review — PLAT-1545/PLAT-1549 changes"
type: SpecReview
analysis: base
scope: "agent-ix/spec-clauses-us-health; spec/functional/FR-001-pack-module-and-home.md, spec/functional/FR-002-rights-metadata-is-truthful-and-publishable.md, spec/non-functional/NFR-001-licensing-boundary.md, spec/tests.md"
review_set: subset
---

## Summary

Reviewed the changed requirements and test-plan rows for ID integrity, verifiability, cross-references, coverage, and the required hash/pin check. FR-001-AC-1 is still active but has no test, and the historical note records a commit hash.

## Verdict

**FAIL** — the matrix has an untagged criterion and the changed test plan introduces a revision pin.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | `spec/tests.md` records commit `b678d5d` as the fixed historical revision for the old one-set manifest. The base checklist prohibits recorded/reviewed revisions in requirements and test plans; remove the hash reference. | spec/tests.md:74-75 |
| FND-002 | high | TC-001 is removed from the matrix while FR-001-AC-1 remains an active Test criterion describing the obsolete one-set M1 state; `quire matrix --strict` confirms no test is bound. Rewrite the criterion for the current manifest and bind a test, or retire the criterion. | spec/functional/FR-001-pack-module-and-home.md:27; spec/tests.md:74-90 |

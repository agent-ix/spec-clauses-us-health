---
id: SR-20261104139923
title: "Code review — US health pack coverage tests"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; spec/functional/FR-001-pack-module-and-home.md, spec/functional/FR-002-rights-metadata-is-truthful-and-publishable.md, spec/non-functional/NFR-001-licensing-boundary.md, spec/tests.md, tests/test_clause_sets.py, tests/test_publish_gate.py, reviews/2026-11-16-plat-1621-pr30-code-review.md, reviews/2026-11-16-spec-clauses-us-health-gap-analysis.md"
review_set: subset
---

## Summary

Reviewed PR #33's test and requirement changes for PLAT-1545/PLAT-1549, including actual Quoin installation behavior, the source metadata oracle, rights checks, and matrix bindings. Focused tests and style checks pass, but an active criterion is left untested, a commit hash is recorded in the test plan, and the missing licence-field case is not exercised.

## Verdict

**FAIL** — the PR leaves FR-001-AC-1 untagged and adds a prohibited revision pin to the test plan.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | TC-001 is retired while active FR-001-AC-1 still requires the loaded M1 manifest to contain exactly one set; the computed matrix reports it untagged. Reframe the criterion to the current manifest contract and bind its existing current-manifest test, or retire the criterion itself. | spec/functional/FR-001-pack-module-and-home.md:27; spec/tests.md:74-75; tests/test_clause_sets.py:108-121 |
| FND-002 | high | The test-plan note pins the historical manifest to commit `b678d5d`. The hash is unnecessary revision-tracking ceremony in a requirements/test artifact; remove it and describe the historical rationale without a recorded revision. | spec/tests.md:74-75 |
| FND-003 | medium | FR-002-AC-1 now promises rejection of a missing or blank `rights.licence`, but the negative test exercises only a whitespace value. Add a missing-key case or narrow the AC to the behavior actually tested. | spec/functional/FR-002-rights-metadata-is-truthful-and-publishable.md:26; tests/test_publish_gate.py:59-73 |

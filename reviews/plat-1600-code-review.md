---
id: SR-019
title: "Code review — PLAT-1600 cybersecurity crosswalks"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; PR #13 at 5c7a14336540c2152be2765650ca17898c59371d; 524B/FDA crosswalk data, tests, and CI"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-clauses-us-health/FR-011", type: references }
---

## Summary

The crosswalk data matches PLAT-1593's exact plan, including the scoped `524B(b)(4)` contextual pointers to FDA `VII.C.2` and NIST `SA-8`; neither asserts coverage. Tests cover exact tuples, target resolution, non-copying, and the unknown-target case. The initial CI run at `d1a1626` failed because Quoin's default `spec-objects-security@v0.11.0` did not declare NIST 5.2.0. The current head pins `v0.13.0`; its full CI suite passes.

## Verdict

**PASS** at `5c7a14336540c2152be2765650ca17898c59371d` after the dependency pin fix.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | The tests require NIST `sp800-53@5.2.0`, but the initial CI setup installed only Quoin's default `spec-objects-security@v0.11.0`, which did not declare that set; three tests failed. | tests/test_crosswalks.py:300-316; .github/workflows/ci.yml:25-26 |

## Review Coverage

- Compared the 524B and FDA guidance crosswalk source/target/relation tuples with the normative table in `spec/spec.md` and PLAT-1593. The exact-pair test passed locally.
- Confirmed `524B(b)(4)` maps only to FDA `VII.C.2` and NIST `SA-8`, with informative relations and rationales saying the pointers are context only. The spec expressly disclaims coverage, extra regulation, equivalence, and legal compliance.
- Confirmed the tests check every 524B-to-guidance mapping, exact table equality, all NIST resolutions, unknown `XX-99`, original rationales, and absence of copied NIST clause files.
- At initial head `d1a1626`, GitHub CI installed only default `spec-objects-security@v0.11.0`; the full suite failed 3 tests because that release did not declare `nist/sp800-53@5.2.0` (50 passed, 3 failed).
- At current head `5c7a143`, CI explicitly installs `spec-objects-security@v0.13.0`; the full suite passes (53 passed), and all required checks are green.
- No `spec/**` artifacts changed in this PR, so spec-review methods were not run. No production code changed, so Quoin gap-analysis was not applicable.

## Findings data

```yaml
findings:
  - fnd: FND-001
    severity: medium
    confidence: high
    method: code-review
    check: coverage
    artifact_id: FR-011-AC-3
    related_ids: [FR-011-AC-5]
    path: tests/test_crosswalks.py
    lines: "300-316"
    excerpt: "Every section 524B and FDA guidance clause has at least one target in the NIST set; every target resolves when `spec-objects-security` is installed."
    finding: "The tests require nist/sp800-53@5.2.0, but initial CI installed only Quoin's default spec-objects-security@v0.11.0, which did not declare that set; three tests failed."
bindings:
  - {test_id: TC-047, ac_id: FR-011-AC-1, trace: correct}
  - {test_id: TC-048, ac_id: FR-011-AC-2, trace: correct}
  - {test_id: TC-049, ac_id: FR-011-AC-3, trace: correct}
  - {test_id: TC-050, ac_id: FR-011-AC-4, trace: correct}
  - {test_id: TC-051, ac_id: FR-011-AC-5, trace: correct}
```

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | CI now installs the pinned spec-objects-security v0.13.0 before tests; current GitHub CI reports 53 passed. |

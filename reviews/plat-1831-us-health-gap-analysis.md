---
id: SR-20261104139938
title: "Gap analysis of PLAT-1831 spec-clauses-us-health PR #37"
type: SpecReview
analysis: gap-analysis
scope: "agent-ix/spec-clauses-us-health; tests/test_part11_discharge.py, tests/test_m2_discharge.py, tests/test_m3_discharge.py, tests/test_m4_discharge.py, spec/functional/FR-006, FR-007, FR-019, FR-020, FR-021"
review_set: subset
---

## Summary

Ticket: PLAT-1831. This is a PR-scoped gap check, not a full-repo audit. The diff contains no production code. It changes test bodies and toolchain manifests only, so the full matrix and reverse-gap sweep do not apply. Plan completion: not assessed.

The check looked at whether removing the version asserts weakens any acceptance criterion the touched tests trace to. Those criteria are FR-006-AC-1 and AC-2, FR-007-AC-1 to AC-3, FR-019-AC-1 to AC-4, FR-020-AC-1 to AC-4 and FR-021-AC-1 to AC-2.

## Verdict

**CLEAN.** No criterion in those FRs names a toolchain version. The `@pytest.mark.trace` tags are unchanged. The deleted lines asserted only `quoin --version == "0.35.0"`, which is not an observable behavior any criterion requires. Every traced test still exercises quoin and quire and asserts their exit codes. All five files pass on the new toolchain (8 passed).

Outside the diff, `.github/workflows/ci.yml` pins two install refs. `engineering-assurance` is pinned at v0.10.1, which is the current release. `spec-objects-security` is pinned at v0.14.0, while the latest release is v0.18.0. These are install-source refs, not assertions, and this PR does not touch them. The stale spec-objects-security ref is reported to the lead and is not a finding against this PR.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |

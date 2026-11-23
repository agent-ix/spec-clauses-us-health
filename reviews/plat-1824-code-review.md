---
id: SR-20261104139928
title: "Code review of PLAT-1824 PR #34"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; tests/test_clause_sets.py, tests/corpus/hipaa/role-permission.json, spec_clauses_us_health/clauses/us-hhs-45-cfr-164-subpart-c-2026-11-12.json"
review_set: subset
---

## Summary

Ticket: PLAT-1824. Reviewed `git diff origin/main...HEAD` at 8e804c81 (two commits). The clause JSON matches the normative table; HIPAA no longer maps any clause to the repository outputs `access-control` or `audit-trail`; the corpus role record now uses `security.role` like its sibling `security.control` and `security.audit_event` records. The new FR-012-AC-7 test fails on origin/main's mapping (measured) and passes on the branch. One count pin was bumped instead of removed.

## Verdict

**CHANGES REQUESTED** — fix the count pin (FND-001); FND-002 is a small test/trace cleanup. No paywalled text, no score or acceptability assignment, no vendored content in the changed files.

## Verification

- `python3 -m pytest -q tests/test_clause_sets.py -k "ephi_system or normative_table_exactly or output_catalog_matches_the_spec"`: 3 passed.
- Same new test copied onto an origin/main export: fails at the `access-control`/`audit-trail` assertion.
- `quire relations --help` (quire 0.52.0): `--health-data-flows` exists, so the new producer description names a real command.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | `assert len(catalog) == 39` pins the size of the spec's own catalog table, which the test itself parsed; it protects nothing and was bumped 38→39 by this PR. Delete it; the per-set equality loop is the functional check. | tests/test_clause_sets.py:638 |
| FND-002 | low | The FR-012-AC-7 test also asserts the `health-data-flows` description substring (an FR-021/FR-005 concern already pinned exactly by the normative-table test) and two negative mappings AC-7 does not state. Delete the substring assertion and name the two negative clauses in AC-7. | tests/test_clause_sets.py:357-361 |

---
id: SR-20261104139945
title: "Code review of PLAT-1831 spec-clauses-us-health PR #42 (catalog producers)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; spec_clauses_us_health/clauses/*.json, tests/test_clause_sets.py (PR #42 head fba28a130cff0841a2d06f037c8632e5bcd1ee4a)"
review_set: subset
---

## Summary

Ticket: PLAT-1831. Diff reviewed: `git diff origin/main...HEAD` at head fba28a1. The PR adds `producers` to the catalog entries of `verification-records` (run), `sbom` (run), `vulnerability-assessment` (scan) and `cybersecurity-test-results` (run, scan) in five US sets, and adds two tests plus a spec-table reader.

Mapping checked against agent-ix/quoin origin/main (f8637f1): `rust/crates/quoin-evidence/src/adapters/registry.rs` lists `junit` and `sbom` in `ADAPTERS` (run records, `runs/`) and `sarif`, `cargo-deny` and `osv-scanner` in `FINDING_ADAPTERS` (FindingRecord, `scans/`); FR-041-CON-2 says "An SBOM is a run record"; FR-034-AC-13/AC-24 put sarif and cargo-deny scans under `scans/`. FR-211 gives the retained kind as the family's singular name. All four mappings are correct. `system-validation` (producer-trust decisions live under `trust/`, which FR-211 makes non-citable), `audit-logging` (`security.audit_event` spec objects, not store records) and `fda-certification-record` (customer-supplied) do not resolve to run or scan records, so leaving them for PLAT-1853 is right.

Focused runs with quoin 0.36.10 / quire 0.52.1 under a throwaway HOME: `tests/test_clause_sets.py -k "producers or catalog"` 8 passed; `test_part11_discharge.py test_m2_discharge.py test_m4_discharge.py` 5 passed. With the old set data restored, `test_catalog_producers_name_only_fr_211_kinds_and_match_the_spec`, `test_us_clause_set_output_catalog_matches_the_spec` and `test_all_declared_sets_load_and_match_one_catalog` fail; `test_quire_accepts_sets_that_carry_producers` still passes.

## Verdict

**Changes requested (low only).** The data is correct and the main tests are real: they fail on the old data. Quoin 0.36.10 ignores `producers`, and the existing `record-discharge` test over `verification-records` (test_m2_discharge.py) passes with `producers` present, so discharge behaviour is unchanged. That is shown by existing tests, not asserted by a new one, which is adequate while quoin does not read the member. No invented kinds, no count pins, no ticket narration in code comments, and descriptions are unchanged.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | `test_quire_accepts_sets_that_carry_producers` passes on data with no `producers` (verified on origin/main data) and repeats the existing `publish-check` tests over PACKAGE_ROOT; delete it with FR-005-AC-6. | tests/test_clause_sets.py:1517-1539 |
| FND-002 | low | `test_catalog_producers_name_only_fr_211_kinds_and_match_the_spec` re-checks quire FR-073-AC-9 shape rules (non-empty, distinct, unpadded) and the per-set table equality that `_canonical_catalog` already gives TC-018/TC-043; keep only the FR-211 membership check of the spec table. | tests/test_clause_sets.py:1491-1514 |

## Dispositions

Round 1, checked against `git diff fba28a13..eb8b71d8` (head eb8b71d815e634497dd5461c6934acaa8c81bd40). With quoin 0.36.10 and quire 0.52.1, `tests/test_clause_sets.py -k "producers or catalog"` gives 7 passed and `test_m2_discharge.py` gives 1 passed. With the old set data restored, `test_us_clause_set_output_catalog_matches_the_spec` and `test_all_declared_sets_load_and_match_one_catalog` still fail.

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | `test_quire_accepts_sets_that_carry_producers`, its TC-086 trace and FR-005-AC-6 as written are removed. |
| FND-002 | fixed | The test is now `test_spec_producers_name_only_fr_211_kinds`; it checks only that the spec-table kinds belong to the FR-211 family set. Per-set equality stays with TC-018 and TC-043. |

---
id: SR-20261104139934
title: "Code review of PLAT-1826 PR #36"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; tests/test_premarket_outputs.py, tests/test_m2_discharge.py, spec_clauses_us_health/clauses/us-fda-21-cfr-820-2026-11-12.json, spec_clauses_us_health/clauses/us-fda-premarket-device-software-2023-06-14.json"
review_set: subset
---

## Summary

Ticket: PLAT-1826. Reviewed `git diff origin/main...HEAD` at 33ddd519 (three commits). The seven Part 820 "owner PLAT-1762" rows are now customer-provided documents with no toolchain producer, the owner-ticket test is deleted, and VI.A maps to a new customer `documentation-level-decision` document.

Every producer claim was checked against installed quoin 0.36.8 and quire 0.52.0 and against quoin origin/main 86313ad5. The registered dossier kinds are srs, architecture, trace-matrix, rmm, verification-report, soup, anomalies, risk-management, risk-management-plan, release-record, threat-model and records-of-processing (`quoin-dossier/src/registry.rs`). Each `--doc` kind the mapping names is registered, and its generator renders the stated records: `risk_management.rs` reads `quoin risk-summary` hazard rows, `srs.rs` reads FR, NFR and StR, `architecture.rs` reads parts, ports, connections, allocations and ADRs, `anomalies.rs` reads `quoin anomaly report`, `release_record.rs` reads the release snapshot, and `verification_report.rs` and `trace_matrix.rs` read the evidence matrix.

## Verdict

**CHANGES REQUESTED (minor).** One medium finding: the dossier-kind mapping check cannot fail for two of the six records (FND-001). One low finding covers test tidiness (FND-002).

The producer claims are true. The customer-provided outputs are honestly marked. The VI.A reading is correct, and no command assigns Basic or Enhanced. There is no paywalled text, no tool-assigned score, class, level or acceptability, and no vendoring. The new code comments carry no ticket ids.

**Kind probe robustness.** `_dossier_kinds` already exists on main (the M3 tests use it). It parses the prose of the `DOSSIER_UNKNOWN_KIND` error, because quoin offers no structured list of kinds. The JSON context carries only the unknown kind. If the wording changes, the test fails loudly with the quoin output (`_listed_names` asserts the marker), so it cannot pass silently. It checks the installed tool, which is the tool a customer runs, and it pins no count or version. This is acceptable.

**EU parity (FR-006-AC-3).** Checked against spec-clauses-eu-law origin/main 0bd17d4 (PR #22, fetched today). The EU and US packs share 12 output names: access-control, anomaly-list, audit-trail, release-record, risk-management-records, security-risk-records, software-architecture, software-requirements, soup-list, training-record, verification-records and written-procedure. Kind and description are identical for all 12, both on us-health origin/main and at the PR head. The PR changes no shared definition. None of the seven retyped outputs, and not `documentation-level-decision`, exist in the EU pack. The coder's claim that "EU descriptions already differ" is false against origin/main. The local EU checkout sits on stale branch `peter/plat-1424-spec-eu-law` (289f333, 2026-11-15), which is the likely source of the claim. The final commit (a6741f9) keeps the shared descriptions anyway, so nothing breaks.

## Verification

- `pytest tests/test_premarket_outputs.py tests/test_m2_discharge.py` in the worktree: 11 passed and 1 failed. The failure is the out-of-scope `== "0.35.0"` pin (installed 0.36.8). In a scratch clone with that one line neutralised, `test_m2_discharge` passes, including `VI.A undischarged` and `VI.C compliant`.
- New tests run against origin/main's `spec/spec.md` and clause JSON: all four TC-076 tests and the M2 discharge test fail, so each asserts the changed behavior.
- Mutation: removing `; rendered by quoin dossier generate --doc anomalies` and `--doc architecture` from spec.md leaves all 11 tests passing (FND-001).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | `assert f"--doc {kind}" in mapping or kind in mapping` cannot fail for `anomaly-list` or `software-architecture`. The bare kind is already a substring of the row text ("Unresolved anomalies reported by", "spec-objects-architecture"), so deleting the "rendered by `quoin dossier generate --doc ...`" clause still passes (measured). Assert `f"--doc {kind}" in mapping` only, and assert `"quoin dossier generate" in mapping` for every output in `M2_DOSSIER_KINDS`. That replaces the one-off risk-management assert. | tests/test_premarket_outputs.py:217-222 |
| FND-002 | low | The module docstring still says outputs connect to "producers or tracked owners", which this PR removes. `assert set(M2_DOSSIER_KINDS) <= set(MODULE_EVIDENCE) \| set(COMMAND_EVIDENCE)` compares two module constants and can never fail at runtime. Reword the docstring and delete the constant-to-constant assert. | tests/test_premarket_outputs.py:1,219 |

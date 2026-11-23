---
id: SR-20261104139931
title: "Code review of PLAT-1825 PR #35"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; tests/test_premarket_outputs.py, tests/test_m3_discharge.py, tests/test_clause_sets.py, tests/corpus/security/*.md, spec_clauses_us_health/clauses/us-congress-fdca-524b-2026-10-15.json, spec_clauses_us_health/clauses/us-fda-premarket-cybersecurity-2026-02-03.json"
review_set: subset
---

## Summary

Ticket: PLAT-1825. Reviewed `git diff origin/main...HEAD` at cfb14464 (four commits). The clause JSON matches the normative tables. Every named producer exists in the installed toolchain: quoin 0.36.8 (`dossier generate --doc threat-model` is a registered kind; `anomaly report`; `soup report`; the `sbom`, `sarif`, `osv-scanner`, `cargo-deny` and `junit` evidence adapters), quire 0.52.0 (`relations --flow`) and engineering-assurance 0.10.1 (`producer-execute`). The `vulnerability-management-plan`, `security-risk-assessment` and `additional-cybersecurity-requirement-records` outputs are honestly marked as customer-provided documents. `524B(b)(4)` is no longer discharged in the corpus.

## Verdict

**CHANGES REQUESTED.** Two medium findings: the FR-010-AC-3 test checks only a hand-picked subset of the catalog (FND-001), and the `--module` drop hides a module-loading defect that has no owner ticket (FND-002). The rest are low test-quality items.

The three corpus edits are required by the current spec-objects-security module, not masking anything. Without them, `quire validate` fails: `trust_level` and `decision` are required, and `stride_category` must be a lowercase enum value. The move from `threat-has-control` to `risk-has-treatment` follows that module's own removal of `threat-has-control` (its FR-027). The `resolvedPath` preference is harmless.

The new tests fail on origin/main's clause data and pass on the branch (measured; the only exception is `test_threat_model_dossier_kind_is_registered`, see FND-004). No paywalled text, no tool-assigned score, class or acceptability, no vendoring, and no ticket ids in the new code comments.

## Verification

- Scratch export of HEAD with the out-of-scope `== "0.35.0"` assert neutralised. `pytest tests/test_m3_discharge.py tests/test_premarket_outputs.py -k "m3 or cybersecurity or threat_model"`: 5 passed. `tests/test_clause_sets.py -k "524b or crosswalk"`: 6 passed. `tests/test_m4_discharge.py`: 2 passed.
- Same tests with origin/main's two clause JSON files and spec.md: 6 failed; only `test_threat_model_dossier_kind_is_registered` and unrelated tests pass.
- `quire relations --scope <corpus> --module <spec-objects-security v0.18.0> --relation risk-has-treatment --json`: exit 3, 65 UnknownEdgeType/UnknownRole diagnostics, then "no loaded module declares `traceability.required_relations`". Adding `--module` for spec-artifacts-process, spec-objects-architecture and spec-artifacts-iso gives exit 0 and the covered row. Ambient discovery (no `--module`) also gives exit 0.
- M4 RMM row for `524B(b)(4)`: `applicability: unresolved, compliance: undetermined, reason: context does not declare additional_cybersecurity_regulation`.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | TC-045 checks only the outputs listed in `CYBERSECURITY_PRODUCERS` and `CYBERSECURITY_CUSTOMER_DOCUMENTS`. The M3 catalog also holds `security-risk-records` and `soup-list` (524B set). Neither names a producer command nor is a customer-provided document, yet no test fails, so FR-010-AC-3 ("every cybersecurity catalog row") is not enforced. Assert that the catalog keys equal the union of the declared classes, so that a new or unclassified row fails. | tests/test_premarket_outputs.py:203-231,265-290 |
| FND-002 | medium | Dropping `--module` from `quire relations` hides a real defect. spec-objects-security (v0.18.0 and origin/main a989d73, `imports: {}`) uses edge types it does not register (`references`, `mitigates`, `threatens`, `affects`, `exposes`, ...). Loaded alone under `--module`, its `required_relations` are dropped, and quire exits 3 with a misleading "no loaded module declares traceability.required_relations". `quire validate --module` keeps going with exit 0. The test change itself is fine, because ambient discovery is the normal user path. The defect still needs an owner ticket: spec-objects-security should declare its edge-type dependencies, and quire-rs should report the real cause. | tests/test_m3_discharge.py:207-216 |
| FND-003 | low | Weak or redundant M3 assertions. `"524B(b)(4)" not in facts` is a tautology: `facts` is built from a literal list a few lines above. `compliance != "compliant"` is weaker than FR-020-AC-3; the engine emits `"not_applicable"`, so assert equality. The `"owner"` scan duplicates the TC-045 test. | tests/test_m3_discharge.py:386-389,404-405 |
| FND-004 | low | `test_threat_model_dossier_kind_is_registered` probes the installed quoin, not the pack, so it passes on origin/main data too. Fold it into `CYBERSECURITY_PRODUCERS` as a `threat-model` token checked in both the description and the dossier kind list, then delete it. In the same test file, the `or " ".join(command[:2])` fallback lets any `quoin evidence ...` text satisfy `quoin evidence record`. `_evidence_adapters` also raises a bare IndexError if the error text changes; give it an assertion message instead. | tests/test_premarket_outputs.py:260,274,311-326 |
| FND-005 | low | RISK-M3-001 now records `decision: undecided`, but the corpus cites it as evidence that discharges `524B(a)` as compliant. `not_accepted` (the risk was not accepted as-is and is treated by CTRL-M3-001) is coherent and is still selected by `risk-has-treatment`. | tests/corpus/security/RISK-M3-001.md:8 |
| FND-006 | low | `M4_CONTEXT` passes `cyber_device=yes` without `additional_cybersecurity_regulation`, so the M4 reference RMM now carries `524B(b)(4)` as unresolved/undetermined (measured). Add `additional_cybersecurity_regulation=none_issued`, as M3 does. | tests/test_m4_discharge.py:35 |
| FND-007 | low | Same antipattern this PR removes, still present for the M2 rows. `test_m2_record_outputs_name_a_producer_or_owner_ticket` asserts that `owner PLAT-1762` appears in catalog descriptions, and spec.md keeps the "owner PLAT-1762" text in seven catalog rows. These are ticket ids in a normative catalog, protected by a test. Reword the rows as customer-supplied with no toolchain producer, and delete the owner-ticket assertions. | tests/test_premarket_outputs.py:161-178 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Verified at e8f7e3b1. A new test asserts that the M3 catalog keys equal the disjoint union of the producer, authored-record and customer-document classes. After excerpt: `assert set(_m3_output_catalog()) == set().union(*classes)` |
| FND-002 | deferred | Moved by the lead to PLAT-1852 (https://linear.app/agent-ix/issue/PLAT-1852), which owns the spec-objects-security edge-type dependency and the misleading quire message. No change in this PR. |
| FND-003 | fixed | Verified at e8f7e3b1. The tautology and the duplicate owner scan are deleted, and the weak inequality is now equality. After excerpt: `assert rows["524B(b)(4)"]["compliance"] == "not_applicable"` |
| FND-004 | fixed | Verified at e8f7e3b1. The standalone probe is deleted and `threat-model` is a `dossier-kind` check tied to the description. The `command[:2]` fallback is gone, and `_listed_names` asserts with a message. After excerpt: `("dossier-kind", "threat-model")` |
| FND-005 | fixed | Verified at e8f7e3b1. After excerpt: `decision: not_accepted` / `decided_by: "reviewer@example.invalid"` |
| FND-006 | fixed | Verified at e8f7e3b1. After excerpt: `"additional_cybersecurity_regulation=none_issued",` |
| FND-007 | deferred | Moved by the lead to PLAT-1826 (https://linear.app/agent-ix/issue/PLAT-1826). That ticket's text still says the outputs should be "honest and owned (PLAT-1762)", so the lead should note on PLAT-1826 that the owner-ticket rows and the test asserting them are to be deleted. |

---
id: SR-037
title: "Code review — PLAT-1608 M3 discharge implementation"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; PR #28; tests/test_m3_discharge.py, tests/corpus/, .github/workflows/ci.yml; FR-020; FR-019"
review_set: subset
---

## Summary

Disposition pass at PR #28 head b7ed2da confirms all findings fixed. M2/M3 share one pack staging helper, VULN-M3-001 validates while PLAT-1619 outputs remain open without facts, and the original PR #27 review is preserved separately from SR-037.

## Verdict

**PASS** — all three findings are fixed, focused checks pass, hosted CI is green, and the historical PR #27 review is retained at its original path.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | `_stage_module` duplicates existing pack staging helpers in the same test suite. | tests/test_m3_discharge.py:51 |
| FND-002 | medium | The corpus adds no vulnerability document despite the ticket's explicit scope. | tests/corpus/security/ |

## Review coverage

Checked PLAT-1608 AC1–6 against the Linear issue, FR-020-AC1..4, FR-019-AC4/5, and TC-083. Confirmed the assertion for exact FDA set key `us-fda/premarket-cybersecurity@2026-02-03`; no-producer rows are derived from the master catalog and compared to the M3 open list; SBOM evidence is ingested through Quoin, SOUP is promoted/reported, frontmatter `mitigates` produces the `threat-has-control` covered result, warning posture is not suppressed, missing refs go through `resolve_fact_refs`, and deterministic Markdown is asserted. The CI change installs released `spec-objects-security@v0.14.0` using its supported GitHub source; no vendored files or checksum pins were added. The test is tagged for all FR-020 criteria and inherited FR-019-AC4/5. `quire matrix --strict` recognized these bindings; it also reported pre-existing unrelated untagged criteria. The focused test failed locally because the current environment's default security module is v0.13.0 while the PR asserts v0.14.0; hosted CI at the frozen head is green, so this is recorded as an environment mismatch, not a PR finding. No applicable AssuranceProfile was found under `spec/`.

+++ [reviewer data]

```yaml
clean: false
scope:
  - {id: PLAT-1608-AC-1, path: Linear PLAT-1608, role: examined, excerpt: "The pack RMM index lists us-congress/fdca-524b@… and the current us-fda/premarket-cybersecurity@2026-02-03 set alongside the earlier sets, and each rowCount equals its matrix."}
  - {id: PLAT-1608-AC-2, path: Linear PLAT-1608, role: examined, excerpt: "524B(b)(3) shows Compliant, with a fact citing ingested SBOM evidence."}
  - {id: PLAT-1608-AC-3, path: Linear PLAT-1608, role: examined, excerpt: "No-producer elements show Not compliant - undischarged; the open list equals PLAT-1593's no-producer mapping rows."}
  - {id: PLAT-1608-AC-4, path: Linear PLAT-1608, role: examined, excerpt: "With cyber_device=no, every 524B row shows Not applicable."}
  - {id: PLAT-1608-AC-5, path: Linear PLAT-1608, role: examined, excerpt: "A broken evidence ref fails resolution and names the clause."}
  - {id: PLAT-1608-AC-6, path: Linear PLAT-1608, role: examined, excerpt: "Two runs over the same inputs give byte-identical Markdown."}
  - {id: FR-020-AC-1, path: spec/functional/FR-020-m3-cybersecurity-corpus-discharge.md, role: examined, excerpt: "The M3 RMM lists the 524B and current FDA cybersecurity sets alongside earlier sets in byte order with matching row counts."}
  - {id: FR-020-AC-2, path: spec/functional/FR-020-m3-cybersecurity-corpus-discharge.md, role: examined, excerpt: "524B(b)(3) renders as Compliant with a discharge fact citing ingested SBOM evidence."}
  - {id: FR-020-AC-3, path: spec/functional/FR-020-m3-cybersecurity-corpus-discharge.md, role: examined, excerpt: "No-producer M3 clauses remain undischarged and equal the PLAT-1593 mapping."}
  - {id: FR-020-AC-4, path: spec/functional/FR-020-m3-cybersecurity-corpus-discharge.md, role: examined, excerpt: "cyber_device=no renders every 524B row Not applicable."}
  - {id: FR-019-AC-4, path: spec/functional/FR-019-m2-corpus-discharge.md, role: examined, excerpt: "A missing corpus ref is rejected by the pack-side resolver and identifies the affected clause."}
  - {id: FR-019-AC-5, path: spec/functional/FR-019-m2-corpus-discharge.md, role: examined, excerpt: "Two runs over the same corpus inputs and context produce byte-identical Markdown."}
  - {id: TC-083, path: spec/tests.md, role: examined, excerpt: "M3 corpus discharge integration test verifies evidence, mapping, applicability, missing refs and deterministic output."}
findings:
  - fnd: FND-001
    severity: high
    confidence: high
    method: code-review
    check: other
    artifact_id: PLAT-1608
    related_ids: [TC-083]
    path: tests/test_m3_discharge.py
    lines: "51-66"
    excerpt: "Corpus additions and a test that records facts for both M3 sets and renders the pack RMM under cyber_device=yes."
    finding: "The added _stage_module duplicates the same temporary pack staging behavior already implemented by _stage_module in tests/test_m2_discharge.py (lines 181-197); tests/conftest.py also has the shared stage_clause_sets helper. Search found both existing implementations. Consolidate staging into one helper that supports the selected pack name and full manifest."
  - fnd: FND-002
    severity: medium
    confidence: high
    method: code-review
    check: coverage
    artifact_id: PLAT-1608
    related_ids: []
    path: tests/corpus/security/
    lines: "-"
    excerpt: "Corpus additions include threat/trust_boundary/control/vulnerability documents with threat-has-control satisfied."
    finding: "The ticket's explicit corpus scope requires threat, trust_boundary, control, and vulnerability documents, but the PR adds only THREAT-M3-001, RISK-M3-001, CTRL-M3-001, and BOUNDARY-M3-001. No vulnerability document exists in the corpus, leaving that requested object unrepresented."
bindings:
  - {test_id: test_m3_discharge_renders_cybersecurity_sets_from_ingested_evidence, ac_id: FR-020-AC-1, trace: correct}
  - {test_id: test_m3_discharge_renders_cybersecurity_sets_from_ingested_evidence, ac_id: FR-020-AC-2, trace: correct}
  - {test_id: test_m3_discharge_renders_cybersecurity_sets_from_ingested_evidence, ac_id: FR-020-AC-3, trace: correct}
  - {test_id: test_m3_discharge_renders_cybersecurity_sets_from_ingested_evidence, ac_id: FR-020-AC-4, trace: correct}
  - {test_id: test_m3_discharge_renders_cybersecurity_sets_from_ingested_evidence, ac_id: FR-019-AC-4, trace: correct}
  - {test_id: test_m3_discharge_renders_cybersecurity_sets_from_ingested_evidence, ac_id: FR-019-AC-5, trace: correct}
```


## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-003 | medium | SR-037 replaces the existing PR #27 review artifact at the same path, removing that record. | reviews/plat-1608-code-review.md:1 |

At head b7ed2da, SR-20261104139908 remains at `reviews/plat-1608-code-review.md`, while SR-037 is stored at `reviews/plat-1608-code-review-pr28.md`.

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Both M2 and M3 now call the shared `tests/conftest.py::stage_clause_sets`; no test-local `_stage_module` remains. |
| FND-002 | fixed | `VULN-M3-001.md` is included and passes `quire validate` through the focused M3 test; `V.A.5` and `VII.C.1` are asserted open and no facts are recorded for those PLAT-1619-owned outputs. |
| FND-003 | still-open: preserve both reviews | At head 67373e6 the PR #27 artifact was overwritten; a later commit restored it and placed SR-037 at a separate path. |
| FND-003 | fixed | At head b7ed2da the PR #27 artifact remains intact at reviews/plat-1608-code-review.md and SR-037 exists at reviews/plat-1608-code-review-pr28.md. |

~~~yaml
dispositions:
  - fnd: FND-001
    outcome: fixed
    after_excerpt: "module = stage_clause_sets(\n            root,\n            *(PACKAGE_ROOT / relative for relative in pack_manifest[\"clause_sets\"]),\n            module_name=\"spec_clauses_us_health\",\n            module_version=\"0.1.0\",\n        )"
  - fnd: FND-002
    outcome: fixed
    after_excerpt: "type: vulnerability\nobject: vulnerability\nseverity: high"
  - fnd: FND-003
    outcome: still-open
    reason: "The PR #27 review artifact was overwritten at head 67373e6."
  - fnd: FND-003
    outcome: fixed
    after_excerpt: "id: SR-037\nscope: \"agent-ix/spec-clauses-us-health; PR #28; tests/test_m3_discharge.py, tests/corpus/, .github/workflows/ci.yml; FR-020; FR-019\""
    reason: "Head b7ed2da restores SR-20261104139908 to its original PR #27 path and adds SR-037 at reviews/plat-1608-code-review-pr28.md."
~~~

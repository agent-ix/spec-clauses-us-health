---
type: master-requirements
name: spec-clauses-us-health
org: agent-ix
component_type: clause-set-module
implementation_language: markdown
tags:
  - us-health-law
  - clause-sets
  - 21-cfr-part-11
security_critical: false
---
# Master Requirements Specification

## Purpose

This specification defines the shared module and content conventions for the US
Health-Law Compliance Pack. Its first set describes the obligations in 21 CFR
Part 11 as original, concise clause summaries linked to the public eCFR source.
The pack lets a project record evidence or a customer-owned disposition against
each applicable clause and produce a requirements mapping matrix (RMM). It does
not determine whether a customer is legally compliant.

## Scope

### In Scope

- Repository `agent-ix/spec-clauses-us-health`, Python package
  `spec_clauses_us_health`, and one quire module named by its package manifest.
- The Part 11 set identity, rights metadata, source, clause identifiers, force,
  classification dimensions, applicability expressions, and expected outputs.
- A stable output catalog for all US Health-Law sets in this repository; the
  EU pack may adopt the names in its own specification.
- Customer-owned obligations, the synthetic discharge corpus, and module
  packaging and CI boundaries.
- Public source attribution and the rule against reproducing paywalled standards.

### Out of Scope

- Authored clause JSON, module implementation, CI workflow, publication gate,
  output bindings, and executable reference-corpus tests; these are subsequent
  implementation tickets.
- Legal interpretation, legal advice, certification, or a claim that use of this
  pack establishes regulatory compliance.
- Other US authorities and regulations, including 21 CFR Part 820, FDA premarket
  guidance, 21 U.S.C. 350n, and HIPAA; these belong to later milestones.
- Licensed packs, text incorporated by reference, and any engine change.

## System Overview

The repository ships a clause-only quire module. Its manifest lists every pack
set using module-relative paths in `clause_sets`; it declares no object types,
archetypes, or edges. In M1 it contains the single `us-fda/21-cfr-11@2026-11-12`
set. The version is the eCFR Title 21 “up to date as of” date read for this
specification. A later eCFR snapshot is a new set version, compared with
`quire clauses diff`.

Each set carries `rights.structure: citation_only`, `rights.text: original`,
`rights.clearance_ref: null`, and informational `rights.licence: "Public
domain: US federal regulation (17 U.S.C. 105)"`. The source is titled “21 CFR
Part 11 Electronic Records; Electronic Signatures”, identified as “21 CFR Part
11”, and linked to the current eCFR URL in References. Clause titles and
summaries are original wording. Public law may be named and cited; no text from
a paywalled standard, including material incorporated by reference, is included
or paraphrased.

The pack uses `system_type` (`closed`, `open`),
`electronic_signatures` (`used`, `not_used`), `signature_basis`
(`non_biometric`, `biometric`), `signature_method`
(`identification_code_password`, `other`). For each § 11.10 paragraph, the pack
also declares an unordered
`open_system_11_10_<letter>_applicability` dimension with values `appropriate`
and `not_appropriate`. The signature method and each open-system applicability
value are supplied by the user; the pack does not infer them. Section 11.10
controls bind for closed systems. For open systems, each control remains
unresolved until the user classifies that control as appropriate or not
appropriate under § 11.30. Section 11.300 binds only for non-biometric
signatures that the user classifies as using an identification-code/password
method. Applicability uses the existing
`clause-set-v1` expression model. The clause table below is normative for
identifiers, applicability, and output names. The clause content ticket authors
original concise summaries from the listed citations.

### Part 11 Clause Table

All clauses have force `mandatory`. Each output name resolves to the shared
catalog below. `all[...]` denotes the engine's `all` expression and each
`eq` is an equality condition.

| Clause ID | Applicability | Expected outputs |
|---|---|---|
| `11.10(a)` | `any[eq system_type closed, all[eq system_type open, eq open_system_11_10_a_applicability appropriate]]` | `system-validation`, `verification-records` |
| `11.10(b)` | `any[eq system_type closed, all[eq system_type open, eq open_system_11_10_b_applicability appropriate]]` | `verification-records` |
| `11.10(c)` | `any[eq system_type closed, all[eq system_type open, eq open_system_11_10_c_applicability appropriate]]` | `audit-trail` |
| `11.10(d)` | `any[eq system_type closed, all[eq system_type open, eq open_system_11_10_d_applicability appropriate]]` | `access-control` |
| `11.10(e)` | `any[eq system_type closed, all[eq system_type open, eq open_system_11_10_e_applicability appropriate]]` | `audit-trail` |
| `11.10(f)` | `any[eq system_type closed, all[eq system_type open, eq open_system_11_10_f_applicability appropriate]]` | `system-validation`, `written-procedure` |
| `11.10(g)` | `any[eq system_type closed, all[eq system_type open, eq open_system_11_10_g_applicability appropriate]]` | `access-control` |
| `11.10(h)` | `any[eq system_type closed, all[eq system_type open, eq open_system_11_10_h_applicability appropriate]]` | `system-validation` |
| `11.10(i)` | `any[eq system_type closed, all[eq system_type open, eq open_system_11_10_i_applicability appropriate]]` | `training-record` |
| `11.10(j)` | `any[eq system_type closed, all[eq system_type open, eq open_system_11_10_j_applicability appropriate]]` | `written-procedure` |
| `11.10(k)` | `any[eq system_type closed, all[eq system_type open, eq open_system_11_10_k_applicability appropriate]]` | `access-control`, `audit-trail` |
| `11.30` | `eq system_type open` | `signed-record`, `access-control` |
| `11.50(a)` | `eq electronic_signatures used` | `signed-record`, `signer-registry`, `signature-meaning` |
| `11.50(b)` | `eq electronic_signatures used` | `signed-record`, `audit-trail` |
| `11.70` | `eq electronic_signatures used` | `signed-record` |
| `11.100(a)` | `eq electronic_signatures used` | `signer-registry` |
| `11.100(b)` | `eq electronic_signatures used` | `signer-registry`, `approval-trail` |
| `11.100(c)` | `eq electronic_signatures used` | `fda-certification-record` |
| `11.200(a)` | `all[eq electronic_signatures used, eq signature_basis non_biometric]` | `signer-registry`, `access-control`, `written-procedure` |
| `11.200(b)` | `all[eq electronic_signatures used, eq signature_basis biometric]` | `access-control`, `system-validation` |
| `11.300(a)` | `all[eq electronic_signatures used, eq signature_basis non_biometric, eq signature_method identification_code_password]` | `signer-registry`, `access-control` |
| `11.300(b)` | `all[eq electronic_signatures used, eq signature_basis non_biometric, eq signature_method identification_code_password]` | `written-procedure` |
| `11.300(c)` | `all[eq electronic_signatures used, eq signature_basis non_biometric, eq signature_method identification_code_password]` | `written-procedure` |
| `11.300(d)` | `all[eq electronic_signatures used, eq signature_basis non_biometric, eq signature_method identification_code_password]` | `access-control`, `written-procedure` |
| `11.300(e)` | `all[eq electronic_signatures used, eq signature_basis non_biometric, eq signature_method identification_code_password]` | `system-validation` |

Sections 11.1–11.3 establish scope, implementation, and definitions and are not
clauses in this set. Paragraph IDs retain the CFR designator, including
subparagraph letters. The list above contains 25 clause IDs.

### US Health-Law Output Catalog

Every US set in this repository declares only the outputs it uses. When an
output name is reused here, its kind and description remain identical across
the US sets. The cross-set test enforces this local convention; there is no
engine-level pack catalog. The EU pack may adopt these names, but this spec
does not claim cross-repository enforcement.

| Name | Kind | Description |
|---|---|---|
| `audit-trail` | `record` | Git history and signed-approval history produced by the `approval-trail` capability for the record. |
| `signed-record` | `record` | Signed commits and tags verified by the `signature-verify` capability. |
| `signer-registry` | `record` | Allowed-signers mapping from signing key to named person, read by the `approval-trail` capability. |
| `signature-meaning` | `record` | The `Signed-off-meaning:` trailer verified by the `approval-verify` capability. |
| `fda-certification-record` | `record` | Evidence that the electronic-signature certification was submitted to FDA. |
| `approval-trail` | `record` | Signed approval history for a record produced by the `approval-trail` capability. |
| `access-control` | `record` | Repository permission and branch-rule settings. |
| `system-validation` | `record` | Validation evidence for the toolchain's intended use. |
| `written-procedure` | `procedure` | Customer-owned written procedure. |
| `training-record` | `procedure` | Customer-owned training record. |
| `risk-management-records` | `record` | `spec-objects-safety` hazard, harm, risk-estimate, and residual-risk records. |
| `software-requirements` | `record` | Functional and non-functional requirements (FR/NFR). |
| `software-architecture` | `record` | `spec-objects-architecture` parts and connections. |
| `verification-records` | `record` | Test matrix and retained evidence. |
| `soup-list` | `record` | Software of unknown provenance (SOUP) report. |
| `security-risk-records` | `record` | `spec-objects-security` threat, risk, and control records. |
| `anomaly-list` | `record` | Unresolved-anomaly report. |
| `release-record` | `record` | Engineering-assurance release decision. |

### Customer-Owned Obligations

A clause is customer-owned when every expected output has kind `procedure`.
The customer discharges such a clause using a `disposition` fact whose decision
is `delegated`, rationale is non-empty, and `approvalRef` names the customer's
acceptance. A `direct` fact is not accepted for this case. The pack toolchain
does not claim or generate a procedure output. The M1 customer-owned clause
table is:

| Clause ID | Expected outputs |
|---|---|
| `11.10(i)` | `training-record` |
| `11.10(j)` | `written-procedure` |
| `11.300(b)` | `written-procedure` |
| `11.300(c)` | `written-procedure` |

This table contains exactly the clauses whose expected outputs are all kind
`procedure` in the Part 11 clause table above. No customer-owned flag or other
field is added to the clause-set schema.

### Reference Corpus and Delivery Architecture

`tests/corpus/` is a minimal synthetic project used by discharge tests. Any
synthetic identifiers and evidence references authored for it use the reserved
`example.invalid` domain. Tests generate a fixture SSH key and signed commits
and tag at runtime; each test writes discharge facts to a temporary evidence
store. The package includes a single-repository US catalog consistency test.
The module package contains its manifest and clause JSON; CI installs the
package/module and checks validation, publication rights, applicability,
catalog consistency, and corpus discharge. The module remains clause-only and
sets `pack: false` when installed.

## Requirements Architecture

The functional requirements define the module boundary, truthful rights,
Part 11 identifiers and outputs, applicability, shared output catalog,
customer-owned discharge, and the reference corpus. NFR-001 constrains the
licensing boundary for every published file. The module uses existing
`clause-set-v1`, `clause_sets`, clause evaluation, publication checking, and
discharge/RMM commands; no engine changes are in scope.

### Upstream Contracts

- `quire-rs` FR-073 and FR-083: clause-set model, validation, and publication
  checks.
- `quoin` FR-133, FR-135, and FR-140: discharge evidence and RMM.
- Existing implementations: `quire-rs/src/clauses.rs`,
  `quire-rs/src/loader/manifest.rs`, `quire-cli/src/commands/clauses.rs`,
  `quire-cli/src/commands/publish_check.rs`, and
  `quoin/rust/crates/quoin-cli/src/discharge.rs`.

## References

- Electronic Code of Federal Regulations, 21 CFR Part 11, Title 21 up to date
  as of 2026-11-12: <https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11>.
- FDA, *Part 11, Electronic Records; Electronic Signatures — Scope and
  Application* (2003). This public guidance may be cited for context, but is
  not an M1 set and no guidance text is incorporated here.

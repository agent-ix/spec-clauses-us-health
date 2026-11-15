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
each applicable clause and produce a requirements mapping matrix (RMM). M1
defines Part 11; later milestones add section 524B of the FD&C Act and current
FDA premarket cybersecurity guidance. The pack does not determine whether a
customer is legally compliant.

## Scope

### In Scope

- Repository `agent-ix/spec-clauses-us-health`, Python package
  `spec_clauses_us_health`, and one quire module named by its package manifest.
- The Part 11 set identity, rights metadata, source, clause identifiers, force,
  classification dimensions, applicability expressions, and expected outputs.
- The section 524B and current FDA cybersecurity guidance set identities,
  rights metadata, clause tables, applicability, expected outputs, and
  crosswalk conventions.
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
- Other US authorities and regulations, including 21 CFR Part 820, 21 U.S.C.
  350n, and HIPAA; these belong to later milestones.
- Licensed packs, text incorporated by reference, and any engine change.

## System Overview

The repository ships a clause-only quire module. Its manifest lists every pack
set using module-relative paths in `clause_sets`; it declares no object types,
archetypes, or edges. It contains the sets defined in this specification. The
M1 set is `us-fda/21-cfr-11@2026-11-12`; its version is the eCFR Title 21 “up
to date as of” date read for that snapshot. A later eCFR snapshot is a new set
version, compared with `quire clauses diff`.

Each set carries `rights.structure: citation_only`, `rights.text: original`,
`rights.clearance_ref: null`, plus an informational public-source
`rights.licence` basis. Each set's source metadata cites the public legal or
FDA source it describes. Clause titles and summaries are original wording.
Public law and FDA guidance may be named and cited; no text from a paywalled
standard, including material incorporated by reference, is included or
paraphrased.

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

### Section 524B Clause Table

The set identity is `us-congress/fdca-524b@2026-10-15`, matching the US Code
source text in effect through Public Law 119-124 (October 15, 2026). Clause
summaries use original wording. The user supplies `cyber_device` as `yes` or
`no`, recording an assessment of the definition in 21 U.S.C. § 360n-2(c); the
pack never derives this value. Every clause has force `mandatory` and applies
only when `cyber_device=yes`. With the value absent, applicability is
unresolved; with `no`, each clause is not binding. Section 524B(b)(4) is cited
as a reserved provision but is not a clause until a regulation establishes an
additional requirement.

| Clause ID | Applicability | Expected outputs |
|---|---|---|
| `524B(a)` | `eq cyber_device yes` | `security-risk-records`, `soup-list` |
| `524B(b)(1)` | `eq cyber_device yes` | `vulnerability-management-plan`, `vulnerability-assessment` |
| `524B(b)(2)` | `eq cyber_device yes` | `security-risk-records`, `vulnerability-management-plan` |
| `524B(b)(2)(A)` | `eq cyber_device yes` | `security-risk-records`, `vulnerability-management-plan` |
| `524B(b)(2)(B)` | `eq cyber_device yes` | `security-risk-records`, `vulnerability-management-plan` |
| `524B(b)(3)` | `eq cyber_device yes` | `soup-list` |

### FDA Premarket Cybersecurity Guidance Clause Table

The set identity is `us-fda/premarket-cybersecurity@2026-02-03`, matching the
date on the FDA's current final guidance PDF. Its general recommendation clauses
have force `recommended` and always apply. The section VII clauses are
recommended and apply only when `cyber_device=yes`. For guidance applicability,
the user supplies the same `cyber_device` value; the pack does not infer it.

| Clause ID | Applicability | Expected outputs |
|---|---|---|
| `V.A.1` | Always | `threat-model` |
| `V.A.2` | Always | `security-risk-assessment` |
| `V.A.4` | Always | `soup-list` |
| `V.A.5` | Always | `vulnerability-assessment` |
| `V.B.2` | Always | `security-architecture-views` |
| `V.C` | Always | `cybersecurity-test-results` |
| `VI.B` | Always | `vulnerability-management-plan` |
| `VII.C.1` | `eq cyber_device yes` | `vulnerability-management-plan`, `vulnerability-assessment` |
| `VII.C.2` | `eq cyber_device yes` | `security-risk-assessment`, `security-architecture-views`, `cybersecurity-test-results` |
| `VII.C.3` | `eq cyber_device yes` | `soup-list` |

### Cybersecurity Crosswalk Plan

The 524B set crosswalks its clauses to the guidance recommendations that
describe evidence relevant to each statutory obligation. The implementation
crosswalk also maps 524B and guidance clauses to `nist/sp800-53@5.2.0` when the
published `spec-objects-security` module is installed as a test dependency. The
NIST target identifiers are declared by that module; copied target catalogs are
out of scope. Each 524B clause has at least one guidance target. Each crosswalk
target in the NIST set must resolve. A missing NIST target fails validation and
identifies the unknown identifier. Crosswalks are informative mappings; they do
not claim that a device is compliant, that one clause is equivalent to another,
or that a control satisfies a legal obligation.

| Source clause | Target set key | Target ID | Relation |
|---|---|---|---|
| `524B(a)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.1` | `mapped_to` |
| `524B(a)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.2` | `mapped_to` |
| `524B(a)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.3` | `mapped_to` |
| `524B(b)(1)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.1` | `mapped_to` |
| `524B(b)(2)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.2` | `mapped_to` |
| `524B(b)(2)(A)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.2` | `mapped_to` |
| `524B(b)(2)(B)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.2` | `mapped_to` |
| `524B(b)(3)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.3` | `mapped_to` |
| `524B(a)` | `nist/sp800-53@5.2.0` | `RA-3` | `mapped_to` |
| `524B(b)(1)` | `nist/sp800-53@5.2.0` | `RA-5` | `mapped_to` |
| `524B(b)(1)` | `nist/sp800-53@5.2.0` | `SI-5` | `mapped_to` |
| `524B(b)(2)` | `nist/sp800-53@5.2.0` | `SA-3` | `mapped_to` |
| `524B(b)(2)` | `nist/sp800-53@5.2.0` | `SA-8` | `mapped_to` |
| `524B(b)(2)(A)` | `nist/sp800-53@5.2.0` | `SA-3` | `mapped_to` |
| `524B(b)(2)(A)` | `nist/sp800-53@5.2.0` | `SA-8` | `mapped_to` |
| `524B(b)(2)(B)` | `nist/sp800-53@5.2.0` | `SI-2` | `mapped_to` |
| `524B(b)(3)` | `nist/sp800-53@5.2.0` | `CM-8` | `mapped_to` |
| `524B(b)(3)` | `nist/sp800-53@5.2.0` | `SR-4` | `mapped_to` |
| `V.A.1` | `nist/sp800-53@5.2.0` | `RA-3` | `mapped_to` |
| `V.A.2` | `nist/sp800-53@5.2.0` | `RA-3` | `mapped_to` |
| `V.A.2` | `nist/sp800-53@5.2.0` | `RA-5` | `mapped_to` |
| `V.A.4` | `nist/sp800-53@5.2.0` | `CM-8` | `mapped_to` |
| `V.A.4` | `nist/sp800-53@5.2.0` | `SR-4` | `mapped_to` |
| `V.A.5` | `nist/sp800-53@5.2.0` | `RA-5` | `mapped_to` |
| `V.A.5` | `nist/sp800-53@5.2.0` | `SI-2` | `mapped_to` |
| `V.B.2` | `nist/sp800-53@5.2.0` | `SA-8` | `mapped_to` |
| `V.B.2` | `nist/sp800-53@5.2.0` | `SA-11` | `mapped_to` |
| `V.C` | `nist/sp800-53@5.2.0` | `CA-8` | `mapped_to` |
| `V.C` | `nist/sp800-53@5.2.0` | `SA-11` | `mapped_to` |
| `VI.B` | `nist/sp800-53@5.2.0` | `SR-2` | `mapped_to` |
| `VII.C.1` | `nist/sp800-53@5.2.0` | `RA-5` | `mapped_to` |
| `VII.C.1` | `nist/sp800-53@5.2.0` | `SI-5` | `mapped_to` |
| `VII.C.2` | `nist/sp800-53@5.2.0` | `SA-3` | `mapped_to` |
| `VII.C.2` | `nist/sp800-53@5.2.0` | `SA-8` | `mapped_to` |
| `VII.C.3` | `nist/sp800-53@5.2.0` | `CM-8` | `mapped_to` |
| `VII.C.3` | `nist/sp800-53@5.2.0` | `SR-4` | `mapped_to` |

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
| `threat-model` | `record` | Product threat model and trust-boundary analysis; owner: PLAT-1546. |
| `security-risk-assessment` | `record` | Assessment of cybersecurity risks to the device and related systems; owner: PLAT-1622. |
| `security-architecture-views` | `record` | Views describing security-relevant device architecture and data flows; owner: PLAT-1532. |
| `vulnerability-assessment` | `record` | Assessment of identified vulnerabilities and unresolved software anomalies; owner: PLAT-1619. |
| `cybersecurity-test-results` | `record` | Results of security-focused testing against the device and its controls; owner: PLAT-1638. |
| `vulnerability-management-plan` | `record` | Plan and procedures for monitoring, identifying, and addressing postmarket vulnerabilities; owner: PLAT-1656. |

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
Part 11 identifiers and outputs, section 524B and FDA guidance sets,
applicability, the shared output catalog and crosswalks, customer-owned
discharge, and the reference corpus. NFR-001 constrains the licensing boundary
for every published file. The module uses existing
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
- United States Code, 21 U.S.C. § 360n-2, text in effect through Public Law
  119-124 (October 15, 2026):
  <https://uscode.house.gov/us/usc/119-124/t21/s360n-2/>.
- FDA, *Cybersecurity in Medical Devices: Quality Management System
  Considerations and Content of Premarket Submissions*, issued February 3,
  2026: <https://www.fda.gov/media/119933/download>. This edition supersedes
  the June 27, 2025 final guidance.
- NIST SP 800-53 Rev. 5, set key `nist/sp800-53@5.2.0`, supplied by the
  `spec-objects-security` module for crosswalk target resolution.

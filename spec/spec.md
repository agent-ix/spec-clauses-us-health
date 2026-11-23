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
  - 45-cfr-part-164-subpart-c
security_critical: false
---
# Master Requirements Specification

## Purpose

This specification defines the shared module and content conventions for the US
Health-Law Compliance Pack. Its sets describe obligations in 21 CFR Parts 11
and 820, 45 CFR Part 164 Subpart C, section 524B of the FD&C Act, and FDA
premarket guidance as original, concise clause summaries linked to public
sources. The pack lets a project record evidence or a customer-owned disposition
against each applicable clause and produce a requirements mapping matrix (RMM).
It does not determine whether a customer is legally compliant.

## Scope

### In Scope

- Repository `agent-ix/spec-clauses-us-health`, Python package
  `spec_clauses_us_health`, and one quire module named by its package manifest.
- The Part 11, Part 820, and HIPAA Security Rule set identities, rights
  metadata, sources, clause identifiers, force, classification dimensions,
  applicability expressions, and expected outputs.
- The section 524B, FDA cybersecurity, and FDA device-software guidance set
  identities, rights metadata, clause tables, applicability, expected outputs,
  and crosswalk conventions.
- A stable output catalog for all US Health-Law sets in this repository; the
  EU pack may adopt the names in its own specification.
- Customer-owned obligations, the synthetic discharge corpus, and module
  packaging and CI boundaries.
- Public source attribution and the rule against reproducing paywalled standards.
- The Part 820 Quality Management System Regulation and FDA's June 2023
  premarket device-software guidance, with original clause summaries.

### Out of Scope

- Authored clause JSON, module implementation, CI workflow, publication gate,
  output bindings, and executable reference-corpus tests; these are subsequent
  implementation tickets.
- Legal interpretation, legal advice, certification, or a claim that use of this
  pack establishes regulatory compliance.
- Other US authorities and regulations not expressly named in the M1, M2, M3,
  M4, or cybersecurity milestones; these belong to later milestones.
- HIPAA Security Rule § 164.314(b), which applies specifically to group health
  plans and is outside the covered-entity/business-associate roles modeled here.
- Licensed packs, text incorporated by reference, and any engine change.

## System Overview

The repository ships a clause-only quire module. Its manifest lists every pack
set using module-relative paths in `clause_sets`; it declares no object types,
archetypes, or edges. It contains the sets defined in this specification. The
M1 set is `us-fda/21-cfr-11@2026-11-12`; the M4 set is
`us-hhs/45-cfr-164-subpart-c@2026-11-12`. Each version is the eCFR “up to date
as of” date read for that snapshot. A later eCFR snapshot is a new set version,
compared with `quire clauses diff`.

The M2 sets are `us-fda/21-cfr-820@2026-11-12` and
`us-fda/premarket-device-software@2023-06-14`. Their clause IDs and outputs
are defined in the M2 tables below. The pack does not determine regulatory
scope or infer product-specific applicability decisions.

Each set carries `rights.structure: citation_only`, `rights.text: original`,
`rights.clearance_ref: null`, plus an informational public-source
`rights.licence` basis. Each set's source metadata cites the public legal or
FDA source it describes. Clause titles and summaries are original wording.
Public law and FDA guidance may be named and cited; no text from a paywalled
standard, including material incorporated by reference, is included or
paraphrased.

The Part 11 set uses `system_type` (`closed`, `open`),
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
`clause-set-v1` expression model. The Part 11 clause table below is normative
for identifiers, applicability, and output names. The clause content ticket
authors original concise summaries from the listed citations.

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
unresolved; with `no`, each clause is not binding. Section 524B(b)(4) requires
compliance with additional cybersecurity requirements established by regulation.

| Clause ID | Applicability | Expected outputs |
|---|---|---|
| `524B(a)` | `eq cyber_device yes` | `security-risk-records`, `soup-list` |
| `524B(b)(1)` | `eq cyber_device yes` | `vulnerability-management-plan`, `vulnerability-assessment` |
| `524B(b)(2)` | `eq cyber_device yes` | `security-risk-records`, `vulnerability-management-plan` |
| `524B(b)(2)(A)` | `eq cyber_device yes` | `security-risk-records`, `vulnerability-management-plan` |
| `524B(b)(2)(B)` | `eq cyber_device yes` | `security-risk-records`, `vulnerability-management-plan` |
| `524B(b)(3)` | `eq cyber_device yes` | `sbom` |
| `524B(b)(4)` | `eq cyber_device yes` | `security-risk-records` |

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
| `V.A.4` | Always | `sbom` |
| `V.A.5` | Always | `vulnerability-assessment` |
| `V.B.2` | Always | `security-architecture-views` |
| `V.C` | Always | `cybersecurity-test-results` |
| `VI.B` | Always | `vulnerability-management-plan` |
| `VII.C.1` | `eq cyber_device yes` | `vulnerability-management-plan`, `vulnerability-assessment` |
| `VII.C.2` | `eq cyber_device yes` | `security-risk-assessment`, `security-architecture-views`, `cybersecurity-test-results` |
| `VII.C.3` | `eq cyber_device yes` | `sbom` |

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
or that a control satisfies a legal obligation. Each relation value uses the
`ClauseSet` enum: `equivalent`, `partial`, or `informative`. Every mapping in
this plan is `informative`: it points readers to related guidance or controls
and makes no equivalence or partial-coverage claim.

For `524B(b)(4)`, the statute authorizes FDA to require other cybersecurity
requirements through regulation. The current guidance's footnote 14 explains
that FDA is not required to issue a regulation elaborating the requirements
already specified in section 524B; it does not identify a specific additional
regulation under this paragraph. The `VII.C.2` pointer is included only as
context because that section discusses cybersecurity processes and procedures
for reasonable assurance under `524B(b)(2)`. The `SA-8` pointer is included
only because NIST describes it as a general security-engineering-principles
control. Neither pointer asserts coverage of `524B(b)(4)`, identifies an
additional FDA regulation, or establishes equivalence or legal compliance.

| Source clause | Target set key | Target ID | Relation |
|---|---|---|---|
| `524B(a)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.1` | `informative` |
| `524B(a)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.2` | `informative` |
| `524B(a)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.3` | `informative` |
| `524B(b)(1)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.1` | `informative` |
| `524B(b)(2)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.2` | `informative` |
| `524B(b)(2)(A)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.2` | `informative` |
| `524B(b)(2)(B)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.2` | `informative` |
| `524B(b)(3)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.3` | `informative` |
| `524B(b)(4)` | `us-fda/premarket-cybersecurity@2026-02-03` | `VII.C.2` | `informative` |
| `524B(a)` | `nist/sp800-53@5.2.0` | `RA-3` | `informative` |
| `524B(b)(1)` | `nist/sp800-53@5.2.0` | `RA-5` | `informative` |
| `524B(b)(1)` | `nist/sp800-53@5.2.0` | `SI-5` | `informative` |
| `524B(b)(2)` | `nist/sp800-53@5.2.0` | `SA-3` | `informative` |
| `524B(b)(2)` | `nist/sp800-53@5.2.0` | `SA-8` | `informative` |
| `524B(b)(2)(A)` | `nist/sp800-53@5.2.0` | `SA-3` | `informative` |
| `524B(b)(2)(A)` | `nist/sp800-53@5.2.0` | `SA-8` | `informative` |
| `524B(b)(2)(B)` | `nist/sp800-53@5.2.0` | `SI-2` | `informative` |
| `524B(b)(3)` | `nist/sp800-53@5.2.0` | `CM-8` | `informative` |
| `524B(b)(3)` | `nist/sp800-53@5.2.0` | `SR-4` | `informative` |
| `524B(b)(4)` | `nist/sp800-53@5.2.0` | `SA-8` | `informative` |
| `V.A.1` | `nist/sp800-53@5.2.0` | `RA-3` | `informative` |
| `V.A.2` | `nist/sp800-53@5.2.0` | `RA-3` | `informative` |
| `V.A.2` | `nist/sp800-53@5.2.0` | `RA-5` | `informative` |
| `V.A.4` | `nist/sp800-53@5.2.0` | `CM-8` | `informative` |
| `V.A.4` | `nist/sp800-53@5.2.0` | `SR-4` | `informative` |
| `V.A.5` | `nist/sp800-53@5.2.0` | `RA-5` | `informative` |
| `V.A.5` | `nist/sp800-53@5.2.0` | `SI-2` | `informative` |
| `V.B.2` | `nist/sp800-53@5.2.0` | `SA-8` | `informative` |
| `V.B.2` | `nist/sp800-53@5.2.0` | `SA-11` | `informative` |
| `V.C` | `nist/sp800-53@5.2.0` | `CA-8` | `informative` |
| `V.C` | `nist/sp800-53@5.2.0` | `SA-11` | `informative` |
| `VI.B` | `nist/sp800-53@5.2.0` | `SR-2` | `informative` |
| `VII.C.1` | `nist/sp800-53@5.2.0` | `RA-5` | `informative` |
| `VII.C.1` | `nist/sp800-53@5.2.0` | `SI-5` | `informative` |
| `VII.C.2` | `nist/sp800-53@5.2.0` | `SA-3` | `informative` |
| `VII.C.2` | `nist/sp800-53@5.2.0` | `SA-8` | `informative` |
| `VII.C.3` | `nist/sp800-53@5.2.0` | `CM-8` | `informative` |
| `VII.C.3` | `nist/sp800-53@5.2.0` | `SR-4` | `informative` |

### HIPAA Security Rule Clause Table

The M4 set identity is `us-hhs/45-cfr-164-subpart-c@2026-11-12`; its source is
45 CFR Part 164 Subpart C, Security Standards for the Protection of Electronic
Protected Health Information. The source is the official eCFR snapshot linked in
References. Each standard and each implementation specification listed below
is one `mandatory` clause. A standard without implementation specifications
has style `required`. `required` and `addressable` are styles, not force
values. For an addressable specification, `direct` means implemented as
written. Another disposition is not inferred from the style or from an
applicability result: only a human may record a disposition fact with decision
`accepted_risk`, non-empty rationale, and a named person in `approvalRef`.
That decision and its rationale and approver SHALL be visible in the RMM
tailoring columns. The module SHALL NOT choose or generate a disposition.

`hipaa_role` has unordered values `covered_entity` and
`business_associate`. Clauses not marked role-specific apply to both roles.
The role-specific clauses under § 164.314(a)(2) apply as shown; the dimension
does not make any legal determination. § 164.314(b) is excluded because it
addresses group health plans and their plan sponsors, a role outside this
covered-entity/business-associate set. It must not be silently treated as
covered by either value.

| Clause ID | Type | Style | Applicability | Expected outputs |
|---|---|---|---|---|
| `164.308(a)(1)(i)` | Standard | required | both roles | `security-controls`, `security-risk-records`, `written-procedure` |
| `164.308(a)(1)(ii)(A)` | Implementation specification | required | both roles | `security-risk-records` |
| `164.308(a)(1)(ii)(B)` | Implementation specification | required | both roles | `security-controls`, `security-risk-records` |
| `164.308(a)(1)(ii)(C)` | Implementation specification | required | both roles | `written-procedure` |
| `164.308(a)(1)(ii)(D)` | Implementation specification | required | both roles | `audit-logging` |
| `164.308(a)(2)` | Standard | required | both roles | `security-controls` |
| `164.308(a)(3)(i)` | Standard | required | both roles | `security-controls`, `written-procedure` |
| `164.308(a)(3)(ii)(A)` | Implementation specification | addressable | both roles | `security-controls`, `written-procedure` |
| `164.308(a)(3)(ii)(B)` | Implementation specification | addressable | both roles | `security-controls`, `written-procedure` |
| `164.308(a)(3)(ii)(C)` | Implementation specification | addressable | both roles | `ephi-access-control`, `security-controls`, `written-procedure` |
| `164.308(a)(4)(i)` | Standard | required | both roles | `ephi-access-control`, `security-controls` |
| `164.308(a)(4)(ii)(A)` | Implementation specification | required | both roles | `ephi-access-control` |
| `164.308(a)(4)(ii)(B)` | Implementation specification | addressable | both roles | `ephi-access-control`, `written-procedure` |
| `164.308(a)(4)(ii)(C)` | Implementation specification | addressable | both roles | `ephi-access-control`, `written-procedure` |
| `164.308(a)(5)(i)` | Standard | required | both roles | `security-controls`, `written-procedure` |
| `164.308(a)(5)(ii)(A)` | Implementation specification | addressable | both roles | `written-procedure` |
| `164.308(a)(5)(ii)(B)` | Implementation specification | addressable | both roles | `security-controls` |
| `164.308(a)(5)(ii)(C)` | Implementation specification | addressable | both roles | `audit-logging`, `security-controls` |
| `164.308(a)(5)(ii)(D)` | Implementation specification | addressable | both roles | `ephi-access-control`, `security-controls`, `written-procedure` |
| `164.308(a)(6)(i)` | Standard | required | both roles | `security-controls`, `written-procedure` |
| `164.308(a)(6)(ii)` | Implementation specification | required | both roles | `audit-logging`, `written-procedure` |
| `164.308(a)(7)(i)` | Standard | required | both roles | `security-controls`, `written-procedure` |
| `164.308(a)(7)(ii)(A)` | Implementation specification | required | both roles | `security-controls` |
| `164.308(a)(7)(ii)(B)` | Implementation specification | required | both roles | `security-controls` |
| `164.308(a)(7)(ii)(C)` | Implementation specification | required | both roles | `security-controls` |
| `164.308(a)(7)(ii)(D)` | Implementation specification | addressable | both roles | `security-controls`, `written-procedure` |
| `164.308(a)(7)(ii)(E)` | Implementation specification | addressable | both roles | `security-risk-records` |
| `164.308(a)(8)` | Standard | required | both roles | `security-controls`, `security-risk-records` |
| `164.308(b)` | Standard | required | both roles | `written-procedure` |
| `164.308(b)(3)` | Implementation specification | required | both roles | `written-procedure` |
| `164.310(a)(1)` | Standard | required | both roles | `security-controls` |
| `164.310(a)(2)(i)` | Implementation specification | addressable | both roles | `security-controls`, `written-procedure` |
| `164.310(a)(2)(ii)` | Implementation specification | addressable | both roles | `security-controls`, `written-procedure` |
| `164.310(a)(2)(iii)` | Implementation specification | addressable | both roles | `security-controls`, `written-procedure` |
| `164.310(a)(2)(iv)` | Implementation specification | addressable | both roles | `security-controls`, `written-procedure` |
| `164.310(b)` | Standard | required | both roles | `security-controls`, `written-procedure` |
| `164.310(c)` | Standard | required | both roles | `security-controls` |
| `164.310(d)(1)` | Standard | required | both roles | `security-controls` |
| `164.310(d)(2)(i)` | Implementation specification | required | both roles | `security-controls`, `written-procedure` |
| `164.310(d)(2)(ii)` | Implementation specification | required | both roles | `security-controls`, `written-procedure` |
| `164.310(d)(2)(iii)` | Implementation specification | addressable | both roles | `security-controls`, `written-procedure` |
| `164.310(d)(2)(iv)` | Implementation specification | addressable | both roles | `security-controls` |
| `164.312(a)(1)` | Standard | required | both roles | `ephi-access-control`, `security-controls` |
| `164.312(a)(2)(i)` | Implementation specification | required | both roles | `ephi-access-control` |
| `164.312(a)(2)(ii)` | Implementation specification | required | both roles | `ephi-access-control`, `written-procedure` |
| `164.312(a)(2)(iii)` | Implementation specification | addressable | both roles | `ephi-access-control`, `security-controls` |
| `164.312(a)(2)(iv)` | Implementation specification | addressable | both roles | `security-controls` |
| `164.312(b)` | Standard | required | both roles | `audit-logging` |
| `164.312(c)(1)` | Standard | required | both roles | `security-controls` |
| `164.312(c)(2)` | Implementation specification | addressable | both roles | `security-controls` |
| `164.312(d)` | Standard | required | both roles | `ephi-access-control`, `security-controls` |
| `164.312(e)(1)` | Standard | required | both roles | `health-data-flows`, `security-controls` |
| `164.312(e)(2)(i)` | Implementation specification | addressable | both roles | `health-data-flows`, `security-controls` |
| `164.312(e)(2)(ii)` | Implementation specification | addressable | both roles | `health-data-flows`, `security-controls` |
| `164.314(a)(1)` | Standard | required | both roles | `written-procedure` |
| `164.314(a)(2)(i)` | Implementation specification | required | both roles | `written-procedure` |
| `164.314(a)(2)(ii)` | Implementation specification | required | `hipaa_role=covered_entity` | `written-procedure` |
| `164.314(a)(2)(iii)` | Implementation specification | required | `hipaa_role=business_associate` | `written-procedure` |
| `164.316(a)` | Standard | required | both roles | `written-procedure` |
| `164.316(b)(1)` | Standard | required | both roles | `written-procedure` |
| `164.316(b)(2)(i)` | Implementation specification | required | both roles | `written-procedure` |
| `164.316(b)(2)(ii)` | Implementation specification | required | both roles | `written-procedure` |
| `164.316(b)(2)(iii)` | Implementation specification | required | both roles | `written-procedure` |

Each clause has at least one expected output. `access-control` and
`audit-trail` describe the development repository (repository permissions,
branch rules, git and signed-approval history) and are not used by this set:
the Security Rule safeguards concern the customer's ePHI system, so access
control uses `ephi-access-control` and audit controls use `audit-logging`.
Physical-access clause § 164.310(a)(2)(iii) uses `security-controls` and
`written-procedure`, and encryption clause § 164.312(a)(2)(iv) uses
`security-controls` only, rather than an access-control record. `security-controls` denotes
customer control records and has no producer specified by this clause set.
`health-data-flows` is produced by `quire relations --health-data-flows` from
the declared architecture model. The table specifies
the required clause and output design.

### NIST SP 800-66 Rev. 2 Crosswalk Plan

The crosswalk source is NIST CPRT's published SP 800-66 Rev. 2 to SP 800-53
Rev. 5.1.1 workbook, framework identifier `SP800-66R2-800-53R5.1.1`, version
`1.0.0`. The exact source-element-to-target pair table and one-based workbook
row locators are normative in [FR-013](./functional/FR-013-hipaa-nist-crosswalk-source-and-target.md). The workbook does not expose CPRT internal relationship IDs. Its row locator, source element, target, workbook identity, and retained focal-to-reference direction identify each published relationship without inventing an ID. PLAT-1616 SHALL verify target control identifiers in the
installed `nist/sp800-53@5.2.0` catalog and record any source-to-target
normalization. The crosswalk SHALL include at least one verified target for
each of §§ 164.308, 164.310, 164.312, 164.314(a), and 164.316, and SHALL mark
unmapped source clauses explicitly rather than infer a match from similar
wording.

| Security Rule standard | Source in the crosswalk | Target version | Minimum coverage |
|---|---|---|---|
| `164.308` Administrative safeguards | NIST CPRT published SP 800-66 Rev. 2 to SP 800-53 Rev. 5.1.1 workbook; exact pairs and row locators in FR-013 | `nist/sp800-53@5.2.0` | At least one source-backed target for each standard; retain worksheet/row provenance and source direction |
| `164.310` Physical safeguards | Same workbook and FR-013 pair table | `nist/sp800-53@5.2.0` | Same; list source elements with no relationship as unmapped |
| `164.312` Technical safeguards | Same workbook and FR-013 pair table | `nist/sp800-53@5.2.0` | Same; verify each target exists in the installed target catalog |
| `164.314(a)` Organizational requirements | Same workbook and FR-013 pair table | `nist/sp800-53@5.2.0` | Same; do not extend mapping to excluded § 164.314(b) |
| `164.316` Policies and procedures and documentation requirements | Same workbook and FR-013 pair table | `nist/sp800-53@5.2.0` | Same; retain exact workbook row provenance and source direction |

### M2 Part 820 Quality Management System Regulation Clause Table

The M2 Part 820 set is `us-fda/21-cfr-820@2026-11-12`, sourced from the eCFR
snapshot for Title 21 up to date as of 2026-11-12. Only sections imposing an
actionable manufacturer obligation are clauses. §§ 820.1, 820.3, and 820.7
provide scope, definitions, and incorporation-by-reference information; §
820.5 and §§ 820.20–820.30 are reserved. None is a clause. Clause summaries
use original concise wording and do not restate incorporated requirements.

All clauses have force `mandatory`. Applicability dimensions are human-supplied
facts. The evaluator does not infer whether a statutory condition applies to a
device or manufacturer. A missing dimension leaves that dependent clause
unresolved; `not_applicable` leaves it not binding.

| Clause ID | Applicability | Expected outputs | IBR relationship in source |
|---|---|---|---|
| `820.10(a)` | unconditional | `software-requirements`, `release-record` | yes |
| `820.10(b)(1)` | unconditional | `device-identification-record` | yes |
| `820.10(b)(2)` | `eq qmsr_traceability_applicability applies` | `written-procedure`, `traceability-records` | yes |
| `820.10(b)(3)` | unconditional | `complaint-records`, `regulatory-report-records` | yes |
| `820.10(b)(4)` | `eq qmsr_advisory_notice_applicability applies` | `written-procedure`, `advisory-notice-records` | yes |
| `820.10(c)` | `eq qmsr_design_development_applicability applies` | `software-requirements`, `software-architecture`, `verification-records`, `risk-management-records` | yes |
| `820.10(d)` | `eq qmsr_life_support_applicability applies` | `traceability-records` | yes |
| `820.35(a)` | unconditional | `complaint-records` | yes |
| `820.35(b)` | `eq qmsr_servicing_applicability applies` | `service-records` | yes |
| `820.35(c)` | unconditional | `device-identification-record` | yes |
| `820.45(a)` | unconditional | `written-procedure`, `labeling-inspection-records` | yes |
| `820.45(b)` | unconditional | `release-record` | yes |
| `820.45(c)` | unconditional | `written-procedure`, `labeling-inspection-records` | yes |

The dimension declarations are `qmsr_traceability_applicability`,
`qmsr_advisory_notice_applicability`,
`qmsr_design_development_applicability`, `qmsr_life_support_applicability`,
and `qmsr_servicing_applicability`; each has unordered values `applies` and
`not_applicable`. A person selects each value. In particular, the class and
device-category conditions in § 820.10(c) are not inferred from a `device_class`
value. The table records every clause identifier, applicability condition,
output, and incorporated-by-reference boundary required by PLAT-1569.

### M2 FDA Premarket Device-Software Guidance Clause Table

The M2 premarket set is `us-fda/premarket-device-software@2023-06-14`, sourced
from FDA's *Content of Premarket Submissions for Device Software Functions*
guidance issued June 14, 2023. The guidance is nonbinding and the set's clauses
have force `recommended`. IDs refer to Sections VI.A–VI.J. Clause content uses
original summaries; consensus standards are unnamed and are not represented as
clause sources.

`documentation_level` is an ordered dimension `[[basic], [enhanced]]` selected
by a person. `at_least documentation_level basic` binds a baseline row at either
level. `at_least documentation_level enhanced` binds only at the enhanced
level. A missing value leaves every row unresolved. No set logic selects or
infers a documentation level.

| Clause ID | Documentation level | Applicability | Expected outputs | Part 820 crosswalk target IDs |
|---|---|---|---|---|
| `VI.A` | basic and enhanced | `at_least documentation_level basic` | `risk-management-records` | `820.10(a)`, `820.10(c)` |
| `VI.B` | basic and enhanced | `at_least documentation_level basic` | `software-description` | `820.10(a)`, `820.10(c)` |
| `VI.C` | basic and enhanced | `at_least documentation_level basic` | `risk-management-records` | `820.10(a)`, `820.10(c)` |
| `VI.D` | basic and enhanced | `at_least documentation_level basic` | `software-requirements` | `820.10(a)`, `820.10(c)` |
| `VI.E` | basic and enhanced | `at_least documentation_level basic` | `software-architecture` | `820.10(c)` |
| `VI.F.enhanced` | enhanced | `at_least documentation_level enhanced` | `software-design` | `820.10(c)` |
| `VI.G` | basic and enhanced | `at_least documentation_level basic` | `written-procedure` | `820.10(a)`, `820.10(c)` |
| `VI.G.enhanced` | enhanced | `at_least documentation_level enhanced` | `configuration-management-plan` | `820.10(a)`, `820.10(c)` |
| `VI.H` | basic and enhanced | `at_least documentation_level basic` | `verification-records` | `820.10(a)`, `820.10(c)` |
| `VI.H.enhanced` | enhanced | `at_least documentation_level enhanced` | `verification-records` | `820.10(a)`, `820.10(c)` |
| `VI.I` | basic and enhanced | `at_least documentation_level basic` | `release-record` | `820.10(a)` |
| `VI.J` | basic and enhanced | `at_least documentation_level basic` | `anomaly-list` | `820.10(a)` |

These are the complete Section VI clause identifiers and exact Part 820 target
IDs for PLAT-1572 and PLAT-1582. The §
VI.F software-design specification is an enhanced-only submission clause; the
basic-level treatment is not a premarket-submission recommendation. Enhanced
§ VI.G and VI.H rows state only the added documentation beyond their baseline
rows. The table is the normative source for ids, force, level, and output names.

### M2 Guidance-to-Part-820 Crosswalk Rule

PLAT-1582 owns authored crosswalk rows. Each guidance clause in the M2
premarket table SHALL crosswalk to at least one Part 820 clause in the M2
Part 820 table. Each row records a relation and an original rationale. A
crosswalk is an informative mapping and SHALL NOT claim legal equivalence.
Targets not present in the Part 820 table are invalid. No mapping is inferred
from similar wording.

### M2 Output Producer Mapping

The M2 output map is normative for the premarket device-software and Part 820
sets. It connects each clause output to the capability or command that can
produce its artifact. A listed producer is a capability available on
`origin/main`; naming a capability does not assert that an instance exists in
a customer's repository. The owner ticket records planned work when a record
has no producer. Those records stay open until a customer supplies evidence.

Customer-owned documents and procedures are not generated by this toolchain.
Their output rows identify the customer as owner. The map never creates facts;
facts are recorded against artifact instances with a person's attestation.

| M2 clause IDs | Output name | Kind | Producer or owner |
|---|---|---|---|
| `VI.A`, `VI.C`, `820.10(c)` | `risk-management-records` | `record` | `spec-objects-safety` `hazard` and `failure_mode` artifacts; `quoin risk-summary` |
| `VI.B` | `software-description` | `document` | Customer-provided software function, input, output, and platform description; no toolchain producer |
| `VI.D`, `820.10(a)`, `820.10(c)` | `software-requirements` | `record` | `spec-artifacts-iso` StR, FR, and NFR archetypes |
| `VI.E`, `820.10(c)` | `software-architecture` | `record` | `spec-objects-architecture` `part`, `port`, `connection`, and `allocation` artifacts; ADR artifacts from `spec-artifacts-process` |
| `VI.F.enhanced` | `software-design` | `document` | Customer-provided software design specification; no toolchain producer |
| `VI.G`, `820.10(b)(2)`, `820.10(b)(4)`, `820.45(a)`, `820.45(c)` | `written-procedure` | `procedure` | Customer-owned written procedure; no toolchain producer |
| `VI.G.enhanced` | `configuration-management-plan` | `document` | Customer-provided configuration-management and maintenance plan; no toolchain producer |
| `VI.H`, `VI.H.enhanced`, `820.10(c)` | `verification-records` | `record` | `quire matrix` / `quoin matrix` results and `quoin evidence record` |
| `VI.I`, `820.10(a)`, `820.45(b)` | `release-record` | `record` | Release evidence snapshot produced by `quoin release snapshot`. |
| `VI.J` | `anomaly-list` | `record` | Unresolved anomalies reported by `quoin anomaly report`. |
| `820.10(b)(1)`, `820.35(c)` | `device-identification-record` | `record` | No producer on `origin/main`; customer-supplied device identity and UDI assignment records; owner PLAT-1762. |
| `820.10(b)(2)`, `820.10(d)` | `traceability-records` | `record` | No producer on `origin/main`; customer-supplied traceability procedures and device or batch records; owner PLAT-1762. |
| `820.10(b)(3)`, `820.35(a)` | `complaint-records` | `record` | No producer on `origin/main`; customer-supplied complaint intake, evaluation, investigation, and response records; owner PLAT-1762. |
| `820.10(b)(3)` | `regulatory-report-records` | `record` | No producer on `origin/main`; customer-supplied records of reports to regulatory authorities; owner PLAT-1762. |
| `820.10(b)(4)` | `advisory-notice-records` | `record` | No producer on `origin/main`; customer-supplied records of advisory notices and related actions; owner PLAT-1762. |
| `820.35(b)` | `service-records` | `record` | No producer on `origin/main`; customer-supplied device servicing records; owner PLAT-1762. |
| `820.45(a)`, `820.45(c)` | `labeling-inspection-records` | `record` | No producer on `origin/main`; customer-supplied labeling and packaging inspection records; owner PLAT-1762. |

PLAT-1762 owns producer definition for the seven Part 820 record outputs with
no current producer. Until that work produces an artifact capability, those
rows remain open; no clause fact is created from the catalog or this map.

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
| `risk-management-records` | `record` | `spec-objects-safety` `hazard` and `failure_mode` artifacts; `quoin risk-summary`. |
| `software-requirements` | `record` | Requirements authored with the `spec-artifacts-iso` StR, FR, and NFR archetypes. |
| `software-architecture` | `record` | `spec-objects-architecture` `part`, `port`, `connection`, and `allocation` artifacts; ADR artifacts from `spec-artifacts-process`. |
| `verification-records` | `record` | `quire matrix` / `quoin matrix` results and `quoin evidence record`. |
| `soup-list` | `record` | Software of unknown provenance (SOUP) report. |
| `security-risk-records` | `record` | `spec-objects-security` threat, risk, and control records. |
| `anomaly-list` | `record` | Unresolved anomalies reported by `quoin anomaly report`. |
| `release-record` | `record` | Release evidence snapshot produced by `quoin release snapshot`. |
| `audit-logging` | `record` | `security.audit_event` records and associated retention evidence. |
| `security-controls` | `record` | `security.control` records; the clause set does not define a producer. |
| `health-data-flows` | `record` | Health-data flow projection produced by `quire relations --health-data-flows` from the declared architecture model. |
| `ephi-access-control` | `record` | Access-control records for the ePHI system: `spec-objects-security` `security.role`, `security.permission`, `security.auth_flow`, `security.mfa_method`, `security.password_policy` and `security.session_config` records the customer authors, or customer-supplied evidence; the clause set defines no producer. |
| `threat-model` | `record` | Product threat model and trust-boundary analysis; owner: PLAT-1546. |
| `security-risk-assessment` | `record` | Assessment of cybersecurity risks to the device and related systems; owner: PLAT-1622. |
| `security-architecture-views` | `record` | Views describing security-relevant device architecture and data flows; owner: PLAT-1532. |
| `vulnerability-assessment` | `record` | Assessment of identified vulnerabilities and unresolved software anomalies; owner: PLAT-1619. |
| `cybersecurity-test-results` | `record` | Results of security-focused testing against the device and its controls; owner: PLAT-1638. |
| `vulnerability-management-plan` | `record` | Plan and procedures for monitoring, identifying, and addressing postmarket vulnerabilities; owner: PLAT-1656. |
| `sbom` | `record` | SBOM records with component support status and end-of-support dates, from `quoin evidence record --adapter sbom` and `quoin soup report` (PLAT-1517/PLAT-1518). |
| `device-identification-record` | `record` | No producer on `origin/main`; customer-supplied device identity and UDI assignment records; owner PLAT-1762. |
| `traceability-records` | `record` | No producer on `origin/main`; customer-supplied traceability procedures and device or batch records; owner PLAT-1762. |
| `complaint-records` | `record` | No producer on `origin/main`; customer-supplied complaint intake, evaluation, investigation, and response records; owner PLAT-1762. |
| `regulatory-report-records` | `record` | No producer on `origin/main`; customer-supplied records of reports to regulatory authorities; owner PLAT-1762. |
| `advisory-notice-records` | `record` | No producer on `origin/main`; customer-supplied records of advisory notices and related actions; owner PLAT-1762. |
| `service-records` | `record` | No producer on `origin/main`; customer-supplied device servicing records; owner PLAT-1762. |
| `labeling-inspection-records` | `record` | No producer on `origin/main`; customer-supplied labeling and packaging inspection records; owner PLAT-1762. |
| `software-description` | `document` | Customer-provided software function, input, output, and platform description; no toolchain producer. |
| `software-design` | `document` | Customer-provided software design specification; no toolchain producer. |
| `configuration-management-plan` | `document` | Customer-provided configuration-management and maintenance plan; no toolchain producer. |

### Customer-Owned Obligations

For the Part 11 M1 table, a non-addressable clause is customer-owned when every
expected output has kind `procedure`, as specified by
[FR-006](./functional/FR-006-customer-owned-obligations.md). Addressable
clauses are excluded even when all expected outputs have kind `procedure`.
The customer discharges a listed clause using a `disposition` fact whose
decision is `delegated`, rationale is non-empty, and `approvalRef` names the
customer's acceptance. A `direct` fact is not accepted for this case. The pack
toolchain does not claim or generate a procedure output. The M1
customer-owned clause table is:

| Clause ID | Expected outputs |
|---|---|
| `11.10(i)` | `training-record` |
| `11.10(j)` | `written-procedure` |
| `11.300(b)` | `written-procedure` |
| `11.300(c)` | `written-procedure` |

This table contains exactly the non-addressable Part 11 M1 clauses whose
expected outputs are all kind `procedure`. No customer-owned flag or other
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
Part 11, Part 820, FDA guidance, section 524B, and HIPAA Security Rule
identifiers and outputs, applicability, the shared output catalog and crosswalks,
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
- United States Code, 21 U.S.C. § 360n-2, text in effect through Public Law
  119-124 (October 15, 2026):
  <https://uscode.house.gov/us/usc/119-124/t21/s360n-2/>.
- FDA, *Cybersecurity in Medical Devices: Quality Management System
  Considerations and Content of Premarket Submissions*, issued February 3,
  2026: <https://www.fda.gov/media/119933/download>. This edition supersedes
  the June 27, 2025 final guidance.
- Electronic Code of Federal Regulations, 21 CFR Part 820, Title 21 up to date
  as of 2026-11-12: <https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-820>.
- FDA, *Content of Premarket Submissions for Device Software Functions*,
  issued June 14, 2023: <https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-premarket-submissions-device-software-functions>.
- Electronic Code of Federal Regulations, 45 CFR Part 164 Subpart C, Title 45
  up to date as of 2026-11-12:
  <https://www.ecfr.gov/on/2026-11-12/title-45/subtitle-A/subchapter-C/part-164/subpart-C>.
- NIST, *Implementing the Health Insurance Portability and Accountability Act
  (HIPAA) Security Rule: A Cybersecurity Resource Guide*, SP 800-66 Rev. 2
  (2024), CPRT dataset `SP800_66_2_0_0`:
  <https://csrc.nist.gov/pubs/sp/800/66/r2/final> and
  <https://csrc.nist.gov/projects/cprt/catalog>.
- NIST SP 800-53 Rev. 5, set key `nist/sp800-53@5.2.0`, supplied by the
  `spec-objects-security` module for crosswalk target resolution.

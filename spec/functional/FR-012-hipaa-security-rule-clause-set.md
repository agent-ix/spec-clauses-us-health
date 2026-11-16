---
id: FR-012
title: The M4 set describes the HIPAA Security Rule safeguards
type: FR
---
# FR-012: The M4 set describes the HIPAA Security Rule safeguards

## Description

The M4 clause set identifies 45 CFR Part 164 Subpart C using authority
`us-hhs`, ID `45-cfr-164-subpart-c`, and the eCFR snapshot version date
`2026-11-12`. The specification's clause table is normative for clause IDs,
standard/specification type, required/addressable style, role applicability,
and output names. The table includes each standard and each implementation
specification in §§ 164.308, 164.310, 164.312, 164.314(a), and 164.316. It
excludes § 164.314(b), which is specific to group health plans and is not
represented by the set's covered-entity and business-associate roles. Clause
titles and summaries use original concise wording from public eCFR citations.

## Behavior

- The M4 set SHALL use identity `us-hhs/45-cfr-164-subpart-c@2026-11-12` and
  source metadata SHALL cite the official eCFR snapshot linked in
  `spec/spec.md`.
- Every standard and implementation specification in the normative clause
  table SHALL have exactly one clause with force `mandatory` and at least one
  expected output declared in that set's output catalog.
- Every listed clause SHALL use the style in the normative table. A standard
  with no implementation specification SHALL use style `required`.
- Each clause SHALL encode the table's value in
  `styles.implementation` as `required` or `addressable`; standards without an
  implementation specification SHALL carry `styles.implementation: required`.
- For an `addressable` implementation specification, the pack's
  reference-corpus `direct` fact SHALL represent implementation as written.
  An alternate discharge in the pack's reference corpus SHALL use a
  human-authored `accepted_risk` disposition with non-empty rationale and a
  named person in `approvalRef`; the generated RMM SHALL preserve the decision,
  rationale, and approver in its tailoring columns. Customer-owned clauses are
  governed by [FR-006](./FR-006-customer-owned-obligations.md).
- Quoin's generic disposition contract is defined by
  [FR-046](ix://agent-ix/quoin/FR-046). This pack SHALL NOT require Quoin to
  reject a generic disposition solely because the clause key is classified as
  addressable in this pack's table.
- The set SHALL declare unordered `hipaa_role` values `covered_entity` and
  `business_associate`; each § 164.314(a)(2) clause SHALL use the applicability
  shown in the normative table.
- The set SHALL NOT derive, select, or generate an addressable disposition.
  Applicability and output evaluation SHALL NOT count as approval or
  acceptance of risk.
- Clause content SHALL use original concise summaries of the public eCFR
  source. It SHALL NOT reproduce or paraphrase licensed standards.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-012-AC-1 | The M4 set identity and source metadata match `us-hhs/45-cfr-164-subpart-c@2026-11-12` and the official eCFR snapshot; source rights metadata records public US federal regulation and original text. | Test |
| FR-012-AC-2 | The set clause ID list exactly matches every row in the normative HIPAA Security Rule table, including standards `164.308(a)(1)(i)`, `164.308(a)(3)(i)`, `164.308(a)(4)(i)`, `164.308(a)(5)(i)`, `164.308(a)(6)(i)`, and `164.308(a)(7)(i)`; every clause has force `mandatory`, an expected output in its output catalog, and the specified style. | Test |
| FR-012-AC-3 | The set declares exactly `covered_entity` and `business_associate` as `hipaa_role` values; § 164.314(a)(2)(ii) resolves only for covered entities, § 164.314(a)(2)(iii) only for business associates, and (a)(2)(i) plus both-role clauses apply to both roles. | Test |
| FR-012-AC-4 | The reference-corpus direct fact discharges an addressable clause as implemented as written; each alternate addressable fact in the corpus uses a human `accepted_risk` disposition, non-empty rationale, and named `approvalRef`. Quoin records this valid fact; this criterion does not require the generic parser to infer a pack-specific style from the clause key. | Test |
| FR-012-AC-5 | For an addressable clause with an `accepted_risk` disposition, the generated RMM preserves the decision and exposes its rationale and approver in tailoring columns; missing disposition remains unresolved, and no evaluation path generates a disposition. | Test |
| FR-012-AC-6 | No clause summary or packaged source reproduces or paraphrases text from a paywalled standard; the set declares `rights.text: original` and a public-law source basis. | Analysis |

## Dependencies

- The set extends the clause-set, rights, applicability, and RMM contracts
  specified for [FR-003](./FR-003-part-11-clause-set.md), [FR-002](./FR-002-rights-metadata-is-truthful-and-publishable.md), and [FR-004](./FR-004-applicability.md).
- The M4 clause content is authored in PLAT-1613; NIST crosswalk content is
  authored in PLAT-1616; disposition workflow is delivered in PLAT-1621.

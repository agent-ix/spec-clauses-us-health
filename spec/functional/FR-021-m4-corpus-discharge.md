---
id: FR-021
title: M4 discharge index and open outputs
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-006"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-012"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-019"
    type: extends
---
# FR-021: M4 discharge index and open outputs

## Description

The M4 reference-corpus discharge SHALL identify the HIPAA Security Rule set
in the pack RMM and leave clauses without a toolchain producer open. The
addressable disposition, customer-owned obligation, evidence-reference, and
deterministic-rendering contracts remain as specified in FR-012, FR-006, and
FR-019.

## Behavior

- The M4 discharge RMM SHALL list
  `us-hhs/45-cfr-164-subpart-c@2026-11-12` alongside the earlier declared sets,
  and its `rowCount` SHALL equal the set's clause matrix row count.
- While the reference corpus records no fact for `health-data-flows`, the M4
  RMM SHALL keep each clause requiring that output as
  `Not compliant - undischarged` and SHALL NOT claim toolchain-generated
  evidence for the output. The output's producer is
  `quire relations --health-data-flows`; the RMM does not run it.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-021-AC-1 | The M4 RMM index includes `us-hhs/45-cfr-164-subpart-c@2026-11-12` alongside the earlier declared sets, and its `rowCount` equals the M4 clause matrix row count. | Test |
| FR-021-AC-2 | While the reference corpus records no `health-data-flows` fact, each M4 clause requiring it is `Not compliant - undischarged`, and the RMM claims no toolchain-generated evidence for that output. | Test |

## Dependencies

- Extends the M4 clause and addressable-disposition requirements in
  [FR-012](./FR-012-hipaa-security-rule-clause-set.md), customer-owned
  dispositions in [FR-006](./FR-006-customer-owned-obligations.md), and shared
  evidence-reference and deterministic-rendering contracts in
  [FR-019](./FR-019-m2-corpus-discharge.md).

---
id: FR-008
title: The section 524B set records cyber-device submission obligations
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-003"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-004"
    type: extends
---
# FR-008: The section 524B set records cyber-device submission obligations

## Description

When a user classifies a product as a cyber device, the pack SHALL evaluate the
section 524B obligations against the user's classification without deriving
whether the statutory definition is met.

## Behavior

- The set SHALL use authority `us-congress`, ID `fdca-524b`, and version
  `2026-10-15`, matching the official US Code text in effect through Public Law
  119-124.
- The set SHALL contain exactly the clause IDs and outputs in the Section 524B
  table in [the master specification](../spec.md).
- Every listed clause SHALL have force `mandatory` and applicability
  `eq cyber_device yes`.
- Clause `524B(b)(2)` SHALL describe the required cybersecurity processes and
  procedures; `524B(b)(2)(A)` and `(B)` SHALL describe the regular-cycle and
  out-of-cycle patch obligations, respectively.
- The set SHALL declare the unordered `cyber_device` dimension with values
  `yes` and `no`.
- The user SHALL provide `cyber_device` as `yes` or `no`.
- The set SHALL NOT infer the value from other product facts.
- The set SHALL cite section 524B(b)(4) as reserved source material without
  creating a clause for requirements that no regulation has established.
- Clause summaries SHALL use original wording and identify their statutory
  paragraph in source metadata.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-008-AC-1 | The set identity and source metadata identify 21 U.S.C. § 360n-2, with version `2026-10-15` and the official US Code URL. | Test |
| FR-008-AC-2 | The set contains exactly `524B(a)`, `524B(b)(1)`, `524B(b)(2)`, `524B(b)(2)(A)`, `524B(b)(2)(B)`, and `524B(b)(3)`; it contains no clause for 524B(b)(4). | Test |
| FR-008-AC-3 | With `cyber_device=yes`, every listed clause is binding; with `no`, every listed clause is not binding; with no value, every listed clause is unresolved. | Test |
| FR-008-AC-4 | Every clause is mandatory, names at least one declared output, and conforms to the existing clause-set schema. | Test |
| FR-008-AC-5 | The set does not infer `cyber_device` from any other dimension and rejects an undeclared value. | Test |

## Dependencies

- Extends [FR-003](./FR-003-part-11-clause-set.md) set identity, rights, and source conventions.
- Extends [FR-004](./FR-004-applicability.md) user-supplied applicability dimensions.
- Uses the existing `clause-set-v1` model and `quire clauses evaluate` contract.

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
- Every listed clause SHALL have force `mandatory`. Every clause except
  `524B(b)(4)` SHALL have applicability `eq cyber_device yes`.
- Clause `524B(b)(2)` SHALL describe the required cybersecurity processes and
  procedures; `524B(b)(2)(A)` and `(B)` SHALL describe the regular-cycle and
  out-of-cycle patch obligations, respectively.
- The set SHALL declare the unordered `cyber_device` dimension with values
  `yes` and `no`.
- The user SHALL provide `cyber_device` as `yes` or `no`.
- The set SHALL NOT infer the value from other product facts.
- The set SHALL represent section 524B(b)(4) as an obligation to comply with
  additional cybersecurity requirements established through regulation. No such
  regulation has been issued, so the set SHALL declare the unordered
  `additional_cybersecurity_regulation` dimension with values `issued` and
  `none_issued`, and `524B(b)(4)` SHALL apply only when `cyber_device=yes` and
  `additional_cybersecurity_regulation=issued`. The user supplies the value; the
  set SHALL NOT infer it.
- Clause summaries SHALL use original wording and identify their statutory
  paragraph in source metadata.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-008-AC-1 | The set identity and source metadata identify 21 U.S.C. § 360n-2, with version `2026-10-15` and the official US Code URL. | Test |
| FR-008-AC-2 | The set contains exactly `524B(a)`, `524B(b)(1)`, `524B(b)(2)`, `524B(b)(2)(A)`, `524B(b)(2)(B)`, `524B(b)(3)`, and `524B(b)(4)`. | Test |
| FR-008-AC-3 | With `cyber_device=yes`, every listed clause except `524B(b)(4)` is binding; with `no`, every listed clause is not binding; with no value, every listed clause is unresolved. With `cyber_device=yes`, `524B(b)(4)` is not binding for `additional_cybersecurity_regulation=none_issued`, binding for `issued`, and unresolved when the value is absent. | Test |
| FR-008-AC-4 | Every clause is mandatory, names at least one declared output, and conforms to the existing clause-set schema. | Test |
| FR-008-AC-5 | The set does not infer `cyber_device` from any other dimension. An undeclared value produces an unresolved outcome with an `unknown_value` reason naming `cyber_device`. | Test |

## Dependencies

- Extends [FR-003](./FR-003-part-11-clause-set.md) set identity, rights, and source conventions.
- Extends [FR-004](./FR-004-applicability.md) user-supplied applicability dimensions.
- Uses the existing `clause-set-v1` model and `quire clauses evaluate` contract.

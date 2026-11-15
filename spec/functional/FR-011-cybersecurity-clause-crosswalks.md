---
id: FR-011
title: Cybersecurity clauses crosswalk to guidance and NIST controls
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-008"
    type: constrains
  - target: "ix://agent-ix/spec-clauses-us-health/FR-009"
    type: constrains
---
# FR-011: Cybersecurity clauses crosswalk to guidance and NIST controls

## Description

The pack SHALL expose the relationship between statutory obligations,
supporting FDA recommendations, and relevant public NIST controls.

## Behavior

- Every section 524B clause SHALL crosswalk to at least one clause in the FDA
  guidance set.
- Every section 524B and FDA guidance clause SHALL crosswalk to at least one
  target in `nist/sp800-53@5.2.0`.
- Each relation SHALL use the `ClauseSet` enum value `equivalent`, `partial`,
  or `informative`. These crosswalks SHALL use `informative` because they
  identify related guidance or controls without claiming equivalence or
  coverage.
- The integration test SHALL load the target set from the installed
  `spec-objects-security` module as a test dependency.
- The pack SHALL NOT copy the target set's clauses or identifier catalog.
- A target that does not exist in the installed NIST set SHALL fail the
  crosswalk check with the unknown identifier.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-011-AC-1 | The master specification contains a crosswalk table with source clause, target set key, target ID, and a supported relation (`equivalent`, `partial`, or `informative`); every relation in this plan is `informative`. | Inspection |
| FR-011-AC-2 | Every 524B clause crosswalks to at least one FDA guidance clause. | Test |
| FR-011-AC-3 | Every section 524B and FDA guidance clause has at least one target in the NIST set; every target resolves when `spec-objects-security` is installed. | Test |
| FR-011-AC-4 | A fixture containing an unknown NIST target fails and identifies that target ID. | Test |
| FR-011-AC-5 | Tests install the released module as a dependency and do not copy its clause data into this repository. | Inspection |

## Dependencies

- Depends on [FR-008](./FR-008-fdca-section-524b-clause-set.md) and
  [FR-009](./FR-009-fda-premarket-cybersecurity-guidance-clause-set.md).
- The target set is `nist/sp800-53@5.2.0`, declared by the public
  `spec-objects-security` module.

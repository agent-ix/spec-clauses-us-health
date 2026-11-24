---
id: FR-007
title: The reference corpus supports isolated discharge tests
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-003"
    type: references
  - target: "ix://agent-ix/engineering-assurance/FR-036"
    type: references
  - target: "ix://agent-ix/engineering-assurance/FR-041"
    type: references
  - target: "ix://agent-ix/engineering-assurance/FR-043"
    type: references
  - target: "ix://agent-ix/engineering-assurance/FR-084"
    type: references
  - target: "ix://agent-ix/engineering-assurance/FR-086"
    type: references
---
# FR-007: The reference corpus supports isolated discharge tests

## Description

The reference corpus gives pack tests a minimal synthetic project on which to
evaluate clauses and record discharges. Signing material and discharge facts
are created in isolated test execution resources rather than as corpus inputs.

## Behavior

- The corpus SHALL reside at `tests/corpus/`.
- A discharge integration test SHALL generate its fixture signing key in a
  temporary directory at runtime, use it to create signed commits and a signed
  tag, and remove the key when the test completes.
- The test SHALL write discharge facts to a temporary evidence store.
- When a discharge integration test evaluates the Part 11 set in
  [FR-003](./FR-003-part-11-clause-set.md), the test SHALL obtain evidence for
  catalog outputs that name an Engineering
  Assurance capability by invoking that capability and retaining its JSON
  result, rather than constructing a capability-shaped result itself; the
  capabilities are `signature-verify`, `approval-verify`, and `approval-trail`.
- The test SHALL compare each retained capability result with its result
  contract in the cited Engineering Assurance requirement.
- The test SHALL NOT treat a declared signing gesture as evidence of a human
  gesture.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-007-AC-1 | `tests/corpus/` validates with `quire validate`. | Test |
| FR-007-AC-2 | A discharge integration test creates a fixture signing key in a temporary directory, successfully verifies a signed commit and signed tag made with that key, and removes the key when the test completes. | Test |
| FR-007-AC-3 | A discharge integration test records its facts in a temporary evidence store and removes that store when the test completes. | Test |
| FR-007-AC-4 | The Part 11 discharge test retains the exact JSON emitted by `signature-verify` for a signed commit and tag and checks protocol `engineering-assurance.signature-verify-result/v1` and status `signed_valid`; it does not fabricate either result. | Test |
| FR-007-AC-5 | The Part 11 discharge test retains the exact `approval-verify` JSON for the fixture record id and digest and checks protocol `engineering-assurance.approval-verify-result/v1` and status `approved`; it does not fabricate the result. | Test |
| FR-007-AC-6 | The Part 11 discharge test retains the exact `approval-trail` JSON for the fixture record and checks protocol `engineering-assurance.approval-trail-result/v1` and a matching `approved` entry; when no `tag_receipts` input is supplied, it also checks `tag_receipts.checked` is false and `complete` is false. It does not fabricate the result. | Test |
| FR-007-AC-7 | For the software-key fixture, the Part 11 discharge test checks that the approval result's signature gesture evidence is `none` and does not use a declared signing gesture as evidence of a human gesture. | Test |

## Dependencies

- The corpus is shared with later US and EU pack tests. The Part 11 capability
  results follow Engineering Assurance [FR-036](ix://agent-ix/engineering-assurance/FR-036),
  [FR-041](ix://agent-ix/engineering-assurance/FR-041),
  [FR-043](ix://agent-ix/engineering-assurance/FR-043),
  [FR-084](ix://agent-ix/engineering-assurance/FR-084), and
  [FR-086](ix://agent-ix/engineering-assurance/FR-086).

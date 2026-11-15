---
id: FR-007
title: The reference corpus supports isolated discharge tests
type: FR
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

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-007-AC-1 | `tests/corpus/` validates with `quire validate`. | Test |
| FR-007-AC-2 | A discharge integration test creates a fixture signing key in a temporary directory, successfully verifies a signed commit and signed tag made with that key, and removes the key when the test completes. | Test |
| FR-007-AC-3 | A discharge integration test records its facts in a temporary evidence store and removes that store when the test completes. | Test |

## Dependencies

- The corpus is shared with later US and EU pack tests.

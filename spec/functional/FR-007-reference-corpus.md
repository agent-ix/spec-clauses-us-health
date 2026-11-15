---
id: FR-007
title: The discharge corpus is synthetic and contains no committed secrets
type: FR
---
# FR-007: The discharge corpus is synthetic and contains no committed secrets

## Description

The shared reference corpus gives pack tests a minimal project on which to
evaluate clauses and record discharges without embedding customer data or
credentials.

## Behavior

- The corpus SHALL reside at `tests/corpus/`.
- Tests SHALL generate fixture signing keys and signatures at runtime and write
  discharge facts to a temporary evidence store.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-007-AC-1 | `tests/corpus/` validates with `quire validate`. | Test |
| FR-007-AC-2 | The corpus contains no private key and every identifier and evidence reference uses `example.invalid`. | Test |
| FR-007-AC-3 | Signed commits, a signed tag, and discharge facts are generated at test time; private keys and discharge facts are absent from the repository. | Test |

## Dependencies

- The corpus is shared with later US and EU pack tests.

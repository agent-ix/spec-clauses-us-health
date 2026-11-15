---
id: FR-004
title: The Part 11 set evaluates system and signature applicability
type: FR
---
# FR-004: The Part 11 set evaluates system and signature applicability

## Description

The set classifies system type, electronic-signature use, and signature basis
with the finite values and expressions in the normative table. An unknown
dimension remains unresolved rather than being treated as not applicable.

## Behavior

- `system_type` SHALL have unordered values `closed`, `open`; 11.10 applies to
  both values and 11.30 only to `open`.
- `electronic_signatures` SHALL have unordered values `used`, `not_used`; the
  11.50–11.300 clauses require `used`.
- `signature_basis` SHALL have unordered values `non_biometric`, `biometric`;
  11.200(a) and 11.300 require non-biometric, while 11.200(b) requires
  biometric.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-004-AC-1 | With `system_type=closed,electronic_signatures=not_used`, all 11.10 clauses bind, 11.30 and all 11.50–11.300 clauses are not_binding. | Test |
| FR-004-AC-2 | With `system_type=open,electronic_signatures=used,signature_basis=non_biometric`, 11.30 and 11.300 bind, while 11.200(b) is not_binding. | Test |
| FR-004-AC-3 | With an empty context, every clause evaluates unresolved. | Test |
| FR-004-AC-4 | Every applicability expression conforms to `clause-set-v1`; no undeclared dimension or value is accepted. | Test |

## Dependencies

- Uses the existing `quire clauses evaluate` contract.

---
id: FR-004
title: The Part 11 set evaluates system and signature applicability
type: FR
---
# FR-004: The Part 11 set evaluates system and signature applicability

## Description

The set records system type, whether electronic signatures are used, the
signature basis, the method used for non-biometric signatures, and the user's
assessment of each § 11.10 control's applicability to an open system. A missing
input remains unresolved. The set does not infer the open-system assessment or
the signature method.

## Behavior

- `system_type` SHALL have unordered values `closed`, `open`; 11.10 applies to
  closed systems, and its controls apply to open systems only as appropriate.
  For each 11.10 paragraph, the set SHALL leave open-system applicability
  unresolved until a user supplies that paragraph's
  `open_system_11_10_<letter>_applicability` value as `appropriate` or
  `not_appropriate`.
- `electronic_signatures` SHALL have unordered values `used`, `not_used`; the
  11.50–11.300 clauses require `used`.
- `signature_basis` SHALL have unordered values `non_biometric`, `biometric`;
  11.200(a) and 11.300 require non-biometric, while 11.200(b) requires
  biometric.
- `signature_method` SHALL have unordered values `identification_code_password`,
  `other`; a user SHALL supply this dimension before the set resolves 11.300.
  11.300 applies only when the supplied method is
  `identification_code_password`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-004-AC-1 | With `system_type=closed,electronic_signatures=not_used`, all 11.10 clauses bind, 11.30 and all 11.50–11.300 clauses are not_binding. | Test |
| FR-004-AC-2 | With `system_type=open,electronic_signatures=used,signature_basis=non_biometric` and no per-paragraph open-system 11.10 applicability values, all 11.10 clauses remain unresolved; 11.30 binds; 11.200(a) binds; and every 11.300 clause remains unresolved. | Test |
| FR-004-AC-3 | With an open system, when the user supplies 11.10(a) as `appropriate`, 11.10(a) binds; when the user supplies 11.10(b) as `not_appropriate`, 11.10(b) is not_binding; and 11.10(c) remains unresolved when its value is omitted. | Test |
| FR-004-AC-4 | With `electronic_signatures=used,signature_basis=non_biometric,signature_method=identification_code_password`, 11.300 clauses bind; with `signature_method=other`, they are not_binding. | Test |
| FR-004-AC-5 | With an empty context, every clause evaluates unresolved. | Test |
| FR-004-AC-6 | Every applicability expression conforms to `clause-set-v1`; no undeclared dimension or value is accepted. | Test |

## Dependencies

- Uses the existing `quire clauses evaluate` contract.

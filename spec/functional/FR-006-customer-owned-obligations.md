---
id: FR-006
title: Customer-owned obligations require delegated customer disposition
type: FR
---
# FR-006: Customer-owned obligations require delegated customer disposition

## Description

A clause whose expected outputs are all `procedure` outputs belongs to the
customer. The pack records the customer's disposition without claiming to
create or verify a procedure on its behalf.

## Behavior

- Pack validation SHALL classify a clause as customer-owned when every expected
  output has kind `procedure`; it SHALL NOT add a clause-set schema field.
- The discharge tool SHALL accept a customer-owned obligation only with a
  `delegated` disposition, a non-empty rationale, and an `approvalRef` naming
  customer acceptance.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-006-AC-1 | Every clause whose expected outputs are all kind `procedure` appears in the customer-owned table; the M1 IDs are 11.10(i), 11.10(j), 11.300(b), and 11.300(c). | Test |
| FR-006-AC-2 | Corpus discharge accepts these clauses only with decision `delegated`, a non-empty rationale, and an `approvalRef` naming customer acceptance. | Test |
| FR-006-AC-3 | A `direct` fact for a customer-owned clause is rejected, and no procedure output is claimed by the toolchain. | Test |

## Dependencies

- Uses `quoin` FR-133, FR-135, and FR-140 discharge/RMM contracts.

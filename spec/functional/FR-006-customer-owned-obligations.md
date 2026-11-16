---
id: FR-006
title: Customer-owned obligations require delegated customer disposition
type: FR
---
# FR-006: Customer-owned obligations require delegated customer disposition

## Description

A non-addressable clause whose expected outputs are all `procedure` outputs
belongs to the customer. An addressable clause remains the manufacturer's
responsibility and is not customer-owned, even when all of its expected outputs
are `procedure`; its alternate outcomes follow
[FR-012](./FR-012-hipaa-security-rule-clause-set.md). The pack's
reference-corpus facts record the customer's disposition without claiming to
create or verify a procedure on its behalf. Quoin's
[FR-046](ix://agent-ix/quoin/FR-046) contract accepts the generic decisions
`delegated`, `accepted_risk`, and `temporary_exception`; this pack's corpus uses
`delegated` for non-addressable customer-owned clauses and does not redefine
which decisions the engine accepts for other callers.

## Behavior

- The pack's customer-owned table SHALL classify a clause as customer-owned
  only when the clause is not addressable and every expected output has kind
  `procedure`; an addressable clause SHALL NOT appear in the table even when
  every expected output has kind `procedure`. The table SHALL NOT require a
  clause-set schema field.
- The pack's reference-corpus facts SHALL record each discharged
  non-addressable customer-owned clause with a `delegated` disposition, a
  non-empty rationale, and an `approvalRef` naming the synthetic
  customer-acceptance record.
- The pack's reference-corpus facts SHALL NOT assign a `direct` fact to a
  non-addressable customer-owned clause or claim a procedure output was
  produced by the toolchain.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-006-AC-1 | Every non-addressable clause whose expected outputs are all kind `procedure` appears in the customer-owned table, and no addressable clause appears even if all outputs are `procedure`; the M1 IDs are 11.10(i), 11.10(j), 11.300(b), and 11.300(c). | Test |
| FR-006-AC-2 | For every discharged non-addressable customer-owned clause, the reference-corpus fact has decision `delegated`, a non-empty rationale, and an `approvalRef` that resolves to a synthetic customer-acceptance record naming a person. `quoin evidence record-discharge` records that fact, and the RMM preserves the delegated decision, rationale, and `approvalRef`. | Test |
| FR-006-AC-3 | The reference-corpus facts contain no `direct` fact or evidence reference claiming a procedure was produced by the toolchain for a non-addressable customer-owned clause. | Test |

## Dependencies

- Uses `quoin` FR-133, FR-135, and FR-140 discharge/RMM contracts, the generic
  decision values defined by [Quoin FR-046](ix://agent-ix/quoin/FR-046), and
  the addressable decision contract in [FR-012](./FR-012-hipaa-security-rule-clause-set.md).
  The pack does not require Quoin to reject a generic decision solely because
  a clause key belongs to a pack-specific customer-owned table.

---
id: FR-018
title: M2 expected outputs map to producers or an owner
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-009"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-014"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-015"
    type: extends
---
# FR-018: M2 expected outputs map to producers or an owner

## Description

The M2 premarket guidance and Part 820 sets SHALL identify what produces each
expected output or identify the owner of an output that has no toolchain
producer. An output name alone does not establish that an artifact exists or
that a clause is satisfied.

## Behavior

- The master specification SHALL contain an output mapping table covering each
  unique `(clause ID, output name)` pair in the M2 premarket and Part 820 clause
  tables.
- Every output of kind `record` in either M2 set SHALL name a producer that is
  available on `origin/main`, or name an owner ticket in the mapping table and
  state that no producer is available.
- A mapping row for a customer-supplied document or procedure SHALL identify
  it as customer-owned; it SHALL NOT imply that the toolchain creates it.
- The mapping table is descriptive. No test or script SHALL generate evidence
  facts from an `outputCatalog` entry. A fact cites an artifact instance and
  carries a person's attestation under the discharge requirements.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-018-AC-1 | The output mapping table contains each unique `(clause ID, output name)` pair in the normative M2 Part 820 and premarket tables exactly once, with no missing or extra pair. | Test |
| FR-018-AC-2 | Each M2 `record` output is mapped to a producer available on `origin/main`, or has an explicit no-producer row naming its owner ticket; document and procedure outputs are identified as customer-owned. | Test |
| FR-018-AC-3 | The output catalog definitions for names shared across the M2, Part 11, and other US sets have identical kind and description. | Test |

## Dependencies

- Extends [FR-009](./FR-009-fda-premarket-cybersecurity-guidance-clause-set.md),
  [FR-014](./FR-014-part-820-quality-management-system-clause-set.md), and
  [FR-015](./FR-015-fda-device-software-guidance-clause-set.md).
- Uses the output names and customer-owned rule in [the master specification](../spec.md).
- PLAT-1762 owns future producer definitions for the seven Part 820 record
  outputs that have no toolchain producer on `origin/main`.

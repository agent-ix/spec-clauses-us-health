---
id: FR-018
title: M2 expected outputs map to producers or are customer-provided
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-009"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-014"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-015"
    type: extends
---
# FR-018: M2 expected outputs map to producers or are customer-provided

## Description

The M2 premarket guidance and Part 820 sets SHALL identify what produces each
expected output or identify the output as customer-provided when the toolchain
has no producer for it. An output name alone does not establish that an artifact exists or
that a clause is satisfied.

## Behavior

- The master specification SHALL contain an output mapping table covering each
  unique `(clause ID, output name)` pair in the M2 premarket and Part 820 clause
  tables.
- Every output of kind `record` in either M2 set SHALL name the installed
  command or module artifact types that produce it. Each named command SHALL
  exist, and each named `quoin dossier generate` document kind SHALL be a kind
  the installed `quoin` registers.
- An output that has no producer SHALL be kind `document` or `procedure`, SHALL
  be identified as customer-provided or customer-owned, and SHALL NOT imply
  that the toolchain creates it. No mapping row names a ticket as owner.
- Documentation level is a person's decision. The `documentation-level-decision`
  output is a customer document; no command assigns or infers the level.
- The mapping table is descriptive. No test or script SHALL generate evidence
  facts from an `outputCatalog` entry. A fact cites an artifact instance and
  carries a person's attestation under the discharge requirements.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-018-AC-1 | The output mapping table contains each unique `(clause ID, output name)` pair in the normative M2 Part 820 and premarket tables exactly once, with no missing or extra pair. | Test |
| FR-018-AC-2 | Each M2 output is in exactly one class: a `record` produced by installed commands or module artifact types that exist, an authored `record` naming its module, or a customer-provided `document` or `procedure` with no producer; no M2 description names a ticket as owner. | Test |
| FR-018-AC-3 | The output catalog definitions for names shared across the M2, Part 11, and other US sets have identical kind and description. | Test |

## Dependencies

- Extends [FR-009](./FR-009-fda-premarket-cybersecurity-guidance-clause-set.md),
  [FR-014](./FR-014-part-820-quality-management-system-clause-set.md), and
  [FR-015](./FR-015-fda-device-software-guidance-clause-set.md).
- Uses the output names and customer-owned rule in [the master specification](../spec.md).

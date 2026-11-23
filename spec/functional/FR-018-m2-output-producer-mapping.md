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
- Every produced `record` output in either M2 set SHALL name the installed
  commands or module artifact types that produce it.
- Each command a mapping row names SHALL exist in the installed CLI, and each
  `quoin dossier generate` document kind it names SHALL be a kind the installed
  `quoin` registers.
- The mapping table SHALL identify an output with no producer as
  customer-provided or customer-owned and SHALL NOT imply that the toolchain
  creates it. Its kind
  describes what the output is (`record`, `document`, or `procedure`), not
  whether a tool produces it.
- No mapping row or output description SHALL name a ticket as owner.
- The `documentation-level-decision` output SHALL be a customer document, and
  no command SHALL assign or infer the documentation level.
- The mapping table is descriptive. No test or script SHALL generate evidence
  facts from an `outputCatalog` entry. A fact cites an artifact instance and
  carries a person's attestation under the discharge requirements.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-018-AC-1 | The output mapping table contains each unique `(clause ID, output name)` pair in the normative M2 Part 820 and premarket tables exactly once, with no missing or extra pair. | Test |
| FR-018-AC-2 | Each M2 output is in exactly one class: a produced `record`, a customer-provided `record`, a customer-provided `document`, or a customer-owned `procedure`; the last three state that no toolchain producer exists. | Test |
| FR-018-AC-4 | Each command a produced record's mapping row names exists in the installed CLI, and each named `quoin dossier generate` kind is registered by the installed `quoin`. | Test |
| FR-018-AC-5 | No M2 mapping row or output description names a ticket as owner, and `documentation-level-decision` is a customer document. | Test |
| FR-018-AC-3 | The output catalog definitions for names shared across the M2, Part 11, and other US sets have identical kind and description. | Test |

## Dependencies

- Extends [FR-009](./FR-009-fda-premarket-cybersecurity-guidance-clause-set.md),
  [FR-014](./FR-014-part-820-quality-management-system-clause-set.md), and
  [FR-015](./FR-015-fda-device-software-guidance-clause-set.md).
- Uses the output names and customer-owned rule in [the master specification](../spec.md).

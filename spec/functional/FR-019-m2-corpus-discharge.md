---
id: FR-019
title: M2 sets discharge from the reference corpus
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-007"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-014"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-015"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-016"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-018"
    type: extends
---
# FR-019: M2 sets discharge from the reference corpus

## Description

When the reference corpus contains recorded evidence for the M2 Part 820 and
premarket device-software sets, the pack SHALL render those outcomes together
with Part 11 in a requirements mapping matrix. The matrix SHALL preserve
unresolved work and reflect the declared applicability and output mappings.

## Behavior

- The M2 discharge RMM SHALL include the Part 11, Part 820, and premarket
  device-software set identities in byte order, with each set's row count equal
  to its clause matrix row count.
- A clause with a corresponding artifact and discharge fact in the reference
  corpus SHALL render as `Compliant`.
- A clause without a corresponding corpus artifact SHALL remain
  `Not compliant - undischarged`. The M2 discharge RMM SHALL report compliant
  and undischarged clause lists that match the M2 producer mapping table in the
  master specification.
- When `documentation_level=basic`, the enhanced-only premarket
  device-software clauses SHALL render as `Not applicable`.
- The pack-side evidence-reference resolver SHALL reject a discharge fact that
  references an evidence file absent from the corpus and identify the affected
  clause. The Quoin discharge CLI is not the component that rejects this
  missing reference.
- Repeated rendering with the same corpus inputs and context SHALL produce
  byte-identical Markdown.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-019-AC-1 | The M2 RMM lists the Part 11, Part 820, and premarket device-software set identities in byte order, and each `rowCount` equals its corresponding clause matrix row count. | Test |
| FR-019-AC-2 | Every clause with a corpus artifact is `Compliant`, every clause without one is `Not compliant - undischarged`, and both lists equal the M2 producer mapping table. | Test |
| FR-019-AC-3 | With `documentation_level=basic`, each enhanced-only premarket device-software clause renders as `Not applicable`. | Test |
| FR-019-AC-4 | Changing a discharge fact's evidence reference to a missing corpus file makes the pack-side evidence-reference resolver reject the fact and identify the affected clause. | Test |
| FR-019-AC-5 | Two runs over the same corpus inputs and context produce byte-identical Markdown. | Test |

## Dependencies

- Extends [FR-007](./FR-007-reference-corpus.md) and uses the set contracts in
  [FR-014](./FR-014-part-820-quality-management-system-clause-set.md),
  [FR-015](./FR-015-fda-device-software-guidance-clause-set.md), and
  [FR-016](./FR-016-m2-applicability.md), plus the producer mappings in
  [FR-018](./FR-018-m2-output-producer-mapping.md).

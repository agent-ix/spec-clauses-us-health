---
id: FR-020
title: M3 cybersecurity sets discharge from the reference corpus
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-007"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-008"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-009"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-010"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-011"
    type: extends
---
# FR-020: M3 cybersecurity sets discharge from the reference corpus

## Description

When the reference corpus contains cybersecurity evidence, the pack SHALL
render outcomes for the M3 section 524B and FDA cybersecurity guidance sets
alongside the earlier sets. The RMM SHALL reflect recorded evidence,
applicability, and the producer mapping defined in the master specification.

## Behavior

- The M3 discharge RMM SHALL include `us-congress/fdca-524b@2026-10-15` and
  `us-fda/premarket-cybersecurity@2026-02-03` with the earlier declared sets, in
  byte order, and each set's row count SHALL equal its clause matrix row count.
- The 524B(b)(3) clause SHALL render as `Compliant` only when its discharge
  fact cites evidence produced from the ingested SBOM.
- An M3 clause whose expected output has no producer on `origin/main` SHALL
  remain `Not compliant - undischarged`. The M3 open-clause list SHALL equal
  clauses whose expected outputs map to no-producer rows authored by PLAT-1593
  and recorded in the master specification. The toolchain SHALL NOT generate
  evidence for those rows.
- When `cyber_device=no`, every section 524B clause SHALL render as
  `Not applicable`.
- The pack-side evidence-reference resolver SHALL reject a discharge fact
  that references an evidence file absent from the corpus and identify the
  affected clause. The Quoin discharge CLI is not the component that rejects
  this missing reference.
- Repeated rendering with the same corpus inputs and context SHALL produce
  byte-identical Markdown.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-020-AC-1 | The M3 RMM lists `us-congress/fdca-524b@2026-10-15` and `us-fda/premarket-cybersecurity@2026-02-03` alongside the earlier sets in byte order, and each `rowCount` equals its corresponding clause matrix row count. | Test |
| FR-020-AC-2 | `524B(b)(3)` renders as `Compliant` with a discharge fact citing evidence produced from the ingested SBOM. | Test |
| FR-020-AC-3 | M3 clauses whose expected output has no producer on `origin/main` render as `Not compliant - undischarged`, and the open-clause list equals the no-producer rows authored by PLAT-1593 and recorded in the master specification. | Test |
| FR-020-AC-4 | With `cyber_device=no`, every section 524B clause renders as `Not applicable`. | Test |
| FR-020-AC-5 | Changing a discharge fact's evidence reference to a missing corpus file makes the pack-side evidence-reference resolver reject the fact and identify the affected clause. | Test |
| FR-020-AC-6 | Two runs over the same corpus inputs and context produce byte-identical Markdown. | Test |

## Dependencies

- Extends [FR-007](./FR-007-reference-corpus.md), [FR-008](./FR-008-fdca-section-524b-clause-set.md),
  [FR-009](./FR-009-fda-premarket-cybersecurity-guidance-clause-set.md),
  [FR-010](./FR-010-cybersecurity-output-catalog.md), and
  [FR-011](./FR-011-cybersecurity-clause-crosswalks.md).

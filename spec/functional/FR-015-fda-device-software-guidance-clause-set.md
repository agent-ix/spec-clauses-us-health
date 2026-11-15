---
id: FR-015
title: The M2 set records FDA device-software submission recommendations
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-001"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-002"
    type: extends
---
# FR-015: The M2 set records FDA device-software submission recommendations

## Description

The M2 set SHALL identify FDA's *Content of Premarket Submissions for Device
Software Functions* guidance using identity
`us-fda/premarket-device-software@2023-06-14` and the official FDA URL linked
from `spec.md`. The Section VI clause IDs, force, documentation level, and
output names SHALL match the normative table in `spec.md`. Clause text SHALL
be original concise summaries of the guidance.

## Behavior

- The set SHALL declare `documentation_level` with ordered values
  `[[basic], [enhanced]]`.
- Every clause in the Section VI table SHALL have force `recommended`, at least
  one output in the US Health-Law Output Catalog, and the table's applicability
  expression.
- The set SHALL NOT treat the guidance as binding law or infer documentation
  level from product information.
- The set SHALL declare the public FDA guidance URL as its source with original
  text rights metadata under FR-002.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-015-AC-1 | The set identity is exactly `us-fda/premarket-device-software@2023-06-14`, and its source metadata identifies the June 14, 2023 FDA guidance and official FDA guidance page. | Test |
| FR-015-AC-2 | The set contains exactly the clause identifiers in the M2 FDA Premarket Device-Software Guidance Clause Table, covering Sections VI.A through VI.J and the listed enhanced-level rows. | Test |
| FR-015-AC-3 | Every clause has force `recommended`, non-empty original text, at least one output in its declared catalog, and the level-specific applicability expression in the table. | Test |
| FR-015-AC-4 | The set declares exactly the ordered `documentation_level` values `basic` and `enhanced`, and no other value. | Test |
| FR-015-AC-5 | `quire validate --module <pkg>` and `quire publish-check --module <pkg>` exit 0 for the module containing the set. | Test |

## Dependencies

- Extends [FR-001](./FR-001-pack-module-and-home.md) module composition and
  [FR-002](./FR-002-rights-metadata-is-truthful-and-publishable.md) source
  rights.
- Uses [FR-005](./FR-005-pack-wide-output-catalog.md) output definitions and
  the existing clause-set model.
- Clause content is authored in PLAT-1572.

---
id: FR-014
title: The M2 set describes selected Part 820 manufacturer requirements
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-001"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-002"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-005"
    type: uses
---
# FR-014: The M2 set describes selected Part 820 manufacturer requirements

## Description

The M2 Part 820 set uses identity `us-fda/21-cfr-820@2026-11-12` and the eCFR
snapshot linked from `spec.md`. The normative table defines its clauses,
applicability, outputs, and incorporated-by-reference boundary.

## Behavior

- The Part 820 set SHALL use force `mandatory` for every listed clause.
- The Part 820 set SHALL include exactly the clause IDs listed in its normative
  table, with no additional or missing clause IDs.
- Each clause SHALL declare at least one expected output named in the US
  Health-Law Output Catalog in `spec.md`.
- Each conditional clause SHALL use the exact applicability expression in the
  normative table.
- Every other listed clause SHALL have no applicability expression.
- The set SHALL identify the official eCFR URL as its public source.
- Under FR-002, the set SHALL declare original text and a public US federal
  regulation basis.
- The set SHALL NOT include § 820.35(d) as a mandatory obligation, reserved
  provisions, enforcement consequences, or a restatement of incorporated text.
- Clause summaries SHALL use original concise wording.
- Clause summaries SHALL NOT restate incorporated requirements.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-014-AC-1 | The set identity is exactly `us-fda/21-cfr-820@2026-11-12`, and its source metadata identifies the official eCFR Part 820 URL and the public-law source basis. | Test |
| FR-014-AC-2 | The set contains exactly the clause IDs in the M2 Part 820 Clause Table, including the § 820.10 paragraphs, §§ 820.35(a)–(c), and §§ 820.45(a)–(c); it omits §§ 820.1, 820.3, 820.5, 820.7, 820.10(e), 820.35(d), and reserved provisions. | Test |
| FR-014-AC-3 | Every listed clause has force `mandatory`, at least one expected output in its declared output catalog, and the incorporated-by-reference treatment stated in the table. | Test |
| FR-014-AC-4 | Each listed clause's applicability expression exactly matches the table; a fixture with a changed, missing, or added expression fails and names the clause. | Test |
| FR-014-AC-5 | `quire validate --module <pkg>` and `quire publish-check --module <pkg>` exit 0 for the module containing the set. | Test |

## Dependencies

- Extends [FR-001](./FR-001-pack-module-and-home.md) module composition and
  [FR-002](./FR-002-rights-metadata-is-truthful-and-publishable.md) source
  rights.
- Uses [FR-005](./FR-005-pack-wide-output-catalog.md) output definitions and
  the existing clause-set model.
- Clause content is authored in PLAT-1569.

---
id: FR-003
title: The M1 set contains one mandatory clause per listed CFR paragraph
type: FR
---
# FR-003: The M1 set contains one mandatory clause per listed CFR paragraph

## Description

The Part 11 set uses authority `us-fda`, ID `21-cfr-11`, and version
`2026-11-12`, matching the eCFR Title 21 “up to date as of” date read for this
specification. Its source metadata names and cites 21 CFR Part 11. A later
snapshot is a new version; `quire clauses diff` compares versions.

## Behavior

- The set SHALL contain exactly the 25 clause IDs in the Part 11 clause table
  in `spec/spec.md`; sections 11.1–11.3 are excluded.
- Every clause SHALL have force `mandatory` and at least one expected output
  from the shared catalog.
- Clause summaries and titles SHALL be original wording.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-003-AC-1 | The set identity is exactly `us-fda/21-cfr-11@2026-11-12`, with the stated Part 11 source title, identifier, and official eCFR URL. | Test |
| FR-003-AC-2 | The clause ID list equals the 25 IDs in the normative clause table; no 11.1–11.3 entries appear. | Test |
| FR-003-AC-3 | Every listed clause is mandatory and names at least one catalog output; clause-set validation succeeds. | Test |
| FR-003-AC-4 | A clause naming an output absent from its output catalog fails validation and identifies the clause. | Test |

## Dependencies

- Uses `quire-rs` FR-073 and FR-083.

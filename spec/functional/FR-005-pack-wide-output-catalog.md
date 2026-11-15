---
id: FR-005
title: Reused output names preserve one pack-wide definition
type: FR
---
# FR-005: Reused output names preserve one pack-wide definition

## Description

The shared catalog in `spec/spec.md` is the convention for M1–M4 US sets and
the EU set. Because the engine stores an output catalog per set, each set
declares its used subset with the catalog's exact kind and description.

## Behavior

- The M1 set SHALL use only names in the shared catalog.
- A pack test SHALL compare each output's kind and description across all sets
  and fail on any conflict.
- The module SHALL NOT add a pack-level catalog field to the engine schema.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-005-AC-1 | The catalog defines all 17 names listed in `spec/spec.md`, with the stated kind and description; the first nine entries are exactly those required for M1. | Inspection |
| FR-005-AC-2 | A test over every set in the module fails when two declarations of one output name differ in kind or description. | Test |
| FR-005-AC-3 | M1, later US sets, and the EU pack can reuse the catalog names without adding a pack-level catalog field. | Inspection |

## Dependencies

- Defines the convention reused by PLAT-1424 and later US pack sets.

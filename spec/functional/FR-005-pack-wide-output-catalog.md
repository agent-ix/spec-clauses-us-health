---
id: FR-005
title: Reused output names preserve one US pack definition
type: FR
---
# FR-005: Reused output names preserve one US pack definition

## Description

The output catalog in `spec/spec.md` is the local convention for every US set
in this repository. M4 adds `audit-logging`, `security-controls`, and
`health-data-flows` to the existing 25 catalog entries. Because the engine
stores an output catalog per set, each US set declares its used subset with the
catalog's exact kind and description. The same names are offered to the EU pack
for reuse, but cross-repository consistency is outside this requirement's
enforceable scope.

## Behavior

- The M1 set SHALL use only names in the US catalog.
- A pack test SHALL compare each output's kind and description across all US
  sets in this repository and fail on any conflict.
- The module SHALL NOT add a pack-level catalog field to the engine schema.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-005-AC-1 | A catalog test finds exactly the 28 names listed in `spec/spec.md`, with the stated kind and description; it confirms that the first ten entries are the M1 catalog entries. | Test |
| FR-005-AC-2 | A test over every US set in this repository fails when two declarations of one output name differ in kind or description. | Test |
| FR-005-AC-3 | A fixture US set that reuses a catalog name with its declared kind and description passes the catalog test. | Test |
| FR-005-AC-4 | The module schema defines no pack-level output catalog field. | Test |

## Dependencies

- Defines the catalog for later US sets; the EU pack may adopt the same names in its own specification.

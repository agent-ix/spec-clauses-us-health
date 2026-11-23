---
id: FR-005
title: Reused output names preserve one US pack definition
type: FR
---
# FR-005: Reused output names preserve one US pack definition

## Description

The output catalog in `spec/spec.md` is the local convention for every US set
in this repository, including the M2 Part 820 and premarket device-software
sets. Because the engine stores an output catalog per set, each US set declares
its used subset with the catalog's exact kind and description. The same names
are offered to the EU pack for reuse, but cross-repository consistency is
outside this requirement's enforceable scope.

## Behavior

- The M1 set SHALL use only names in the US catalog.
- A pack test SHALL compare each output's kind and description across all US
  sets in this repository and fail on any conflict.
- The module SHALL NOT add a pack-level catalog field to the engine schema.
- An output whose evidence is a retained record in the quoin evidence store
  SHALL carry `producers` in each set's catalog entry: a non-empty list of
  distinct retained kinds as defined by quoin FR-211 (`run`, `scan`,
  `mock-inspection`, `analysis-report`, `scenario`, or an experiment or
  operational record's `subject.kind`). Quoin resolves an `evidenceRefs` entry
  against this list. `verification-records`, `sbom`, `vulnerability-assessment`
  and `cybersecurity-test-results` carry it, as the "US Output Producers"
  table in [the master specification](../spec.md) states.
- An output that a tool renders or reports (a generated document, snapshot or
  report) and an output the customer supplies SHALL NOT carry `producers`.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-005-AC-1 | A catalog test finds exactly the names listed in `spec/spec.md`, with the stated kind and description; it confirms that the first ten entries are the M1 catalog entries. | Test |
| FR-005-AC-2 | A test over every US set in this repository fails when two declarations of one output name differ in kind or description. | Test |
| FR-005-AC-3 | A fixture US set that reuses a catalog name with its declared kind and description passes the catalog test. | Test |
| FR-005-AC-4 | The module schema defines no pack-level output catalog field. | Test |
| FR-005-AC-5 | Each catalog entry that carries `producers` lists only distinct, unpadded kinds from the quoin FR-211 set, and exactly the outputs in the "US Output Producers" table carry it with the listed kinds in every set that declares them. | Test |
| FR-005-AC-6 | The installed `quire` validates and evaluates every set with `producers` present. | Test |

## Dependencies

- Defines the catalog for later US sets, including M2; the EU pack may adopt the same names in its own specification.

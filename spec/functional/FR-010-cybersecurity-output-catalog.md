---
id: FR-010
title: Cybersecurity sets reuse declared US output definitions
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-005"
    type: extends
---
# FR-010: Cybersecurity sets reuse declared US output definitions

## Description

The section 524B and FDA guidance sets SHALL use the cybersecurity output
definitions in the US pack catalog so a clause output has one meaning across
sets.

## Behavior

- The US catalog SHALL contain the cybersecurity output rows in
  [the master specification](../spec.md), each with a producer capability or
  owning project ticket.
- The two new sets SHALL declare the kind and description from the shared
  catalog for every output they use.
- The SBOM SHALL use a dedicated `sbom` output so lifecycle fields are explicit
  and do not change the meaning of the existing general-purpose `soup-list`.
- Each SBOM component SHALL include its support status and end-of-support date.
- The `sbom` producer SHALL use `quoin evidence record --adapter sbom` and
  `quoin soup report` for the component lifecycle fields (PLAT-1517/PLAT-1518).
- The catalog check SHALL compare names, kinds, and descriptions across every
  US set and fail on a conflicting declaration.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-010-AC-1 | Every cybersecurity output referenced by the 524B or FDA guidance tables has a row in the master catalog with its declared kind and description. | Test |
| FR-010-AC-2 | Every cybersecurity set output matches the catalog's kind and description; a conflict fails and names the output and set. | Test |
| FR-010-AC-3 | The catalog identifies a producer capability or owning ticket for every new row. | Inspection |
| FR-010-AC-4 | The guidance clauses V.A.4 and VII.C.3 use the dedicated `sbom` output, with support status and end-of-support date for every component; they do not use `soup-list` for the SBOM. | Test |

## Dependencies

- Extends [FR-005](./FR-005-pack-wide-output-catalog.md) local output catalog rules.
- Producer capabilities are named in the catalog; the requirements mapping
  work remains in the producer tickets.

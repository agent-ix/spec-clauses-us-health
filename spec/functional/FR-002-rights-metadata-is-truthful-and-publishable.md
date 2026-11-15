---
id: FR-002
title: Each clause set declares truthful and publishable rights metadata
type: FR
---
# FR-002: Each clause set declares truthful and publishable rights metadata

## Description

Every pack set states its structural and textual rights accurately. Part 11 is
public federal law, but this set's summaries are original text. Its rights
metadata records that basis without including the regulation's prose.

## Behavior

- Each set SHALL use `rights.structure: citation_only`, `rights.text: original`,
  and `rights.clearance_ref: null` for the M1 Part 11 set.
- Each set SHALL provide a non-blank informational `rights.licence`.
- No set SHALL claim licensed text or include material from a paywalled
  standard.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-002-AC-1 | The Part 11 set has `structure: citation_only`, `text: original`, `clearance_ref: null`, and a non-blank licence string identifying public-domain US federal regulation. | Test |
| FR-002-AC-2 | `quire publish-check --module <pkg>` exits 0. | Test |
| FR-002-AC-3 | A fixture copy changed to `rights.text: licensed` makes publish-check exit 2 and identify the set by authority, ID, and version. | Test |

## Dependencies

- Uses `quire-rs` FR-073 and FR-083 publication contracts.

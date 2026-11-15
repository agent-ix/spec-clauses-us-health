---
id: FR-001
title: The repository ships one clause-only US health-law module
type: FR
---
# FR-001: The repository ships one clause-only US health-law module

## Description

The pack shall be distributable as the `spec_clauses_us_health` Python package
from the private-until-reviewed `agent-ix/spec-clauses-us-health` repository.
Its quire manifest lists every US health-law set using module-relative paths.
The module contains no object types, archetypes, or edges and installs with
`pack: false`.

## Behavior

- The repository SHALL use `spec/` for requirements and the package directory
  for module resources.
- In M1, `clause_sets` SHALL list exactly `us-fda/21-cfr-11@2026-11-12`.
- The module SHALL remain clause-only and declare no engine extension.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-001-AC-1 | The loaded M1 manifest lists exactly one set, `us-fda/21-cfr-11@2026-11-12`, and later US sets can be added to the same list. | Test |
| FR-001-AC-2 | The module declares no object types, archetypes, or edges; quire module validation succeeds. | Test |
| FR-001-AC-3 | Installing the package with `quoin module install path:<pkg>` succeeds and `quoin module list` reports `pack: false`. | Test |
| FR-001-AC-4 | The repository's spec files validate with `quire validate --scope . --module <spec-artifacts-iso-module> "spec/**/*.md"`. | Test |

## Dependencies

- Uses `quire-rs` FR-083 and the existing clause-set module loader.

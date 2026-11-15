---
id: TM-001
title: "US Health-Law Compliance Pack Test Matrix"
type: TestMatrix
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-001"
    type: covers
  - target: "ix://agent-ix/spec-clauses-us-health/FR-002"
    type: covers
  - target: "ix://agent-ix/spec-clauses-us-health/FR-003"
    type: covers
  - target: "ix://agent-ix/spec-clauses-us-health/FR-004"
    type: covers
  - target: "ix://agent-ix/spec-clauses-us-health/FR-005"
    type: covers
  - target: "ix://agent-ix/spec-clauses-us-health/FR-006"
    type: covers
  - target: "ix://agent-ix/spec-clauses-us-health/FR-007"
    type: covers
  - target: "ix://agent-ix/spec-clauses-us-health/NFR-001"
    type: covers
---
# TM-001: US Health-Law Compliance Pack Test Matrix

## Overview

This matrix defines the planned verification cases for the Part 11 module and
its discharge corpus. Each acceptance criterion maps to a concrete test case.
All cases remain `🚧 Planned` until their implementation tickets add executable
tests and criterion trace tags. This document records the test plan; Quire's
computed matrix and source trace tags remain the evidence of implementation
coverage.

The module scaffold and catalog tests belong to PLAT-1545. Clause evaluation
tests are authored with PLAT-1423. Corpus discharge cases are implemented with
PLAT-1559. Licensing rights metadata is exercised by the PLAT-1549 publish gate;
source-rights analysis records only the public source and its rights basis.

## Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Status |
|---|---|---|---|
| FR-001 | FR-001-AC-1 | TC-001 | 🚧 Planned for PLAT-1545 |
| FR-001 | FR-001-AC-2 | TC-002 | 🚧 Planned for PLAT-1545 |
| FR-001 | FR-001-AC-3 | TC-003 | 🚧 Planned for PLAT-1545 |
| FR-001 | FR-001-AC-4 | TC-004 | 🚧 Planned for PLAT-1545 |
| FR-002 | FR-002-AC-1 | TC-005 | 🚧 Planned for PLAT-1545 |
| FR-002 | FR-002-AC-2 | TC-006 | 🚧 Planned for PLAT-1549 |
| FR-002 | FR-002-AC-3 | TC-007 | 🚧 Planned for PLAT-1549 |
| FR-003 | FR-003-AC-1 | TC-008 | 🚧 Planned for PLAT-1423 |
| FR-003 | FR-003-AC-2 | TC-009 | 🚧 Planned for PLAT-1423 |
| FR-003 | FR-003-AC-3 | TC-010 | 🚧 Planned for PLAT-1423 |
| FR-003 | FR-003-AC-4 | TC-011 | 🚧 Planned for PLAT-1423 |
| FR-003 | FR-003-AC-5 | TC-031 | 🚧 Planned for PLAT-1423 |
| FR-004 | FR-004-AC-1 | TC-012 | 🚧 Planned for PLAT-1423 |
| FR-004 | FR-004-AC-2 | TC-013 | 🚧 Planned for PLAT-1423 |
| FR-004 | FR-004-AC-3 | TC-014 | 🚧 Planned for PLAT-1423 |
| FR-004 | FR-004-AC-4 | TC-015 | 🚧 Planned for PLAT-1423 |
| FR-004 | FR-004-AC-5 | TC-016 | 🚧 Planned for PLAT-1423 |
| FR-004 | FR-004-AC-6 | TC-017 | 🚧 Planned for PLAT-1423 |
| FR-005 | FR-005-AC-1 | TC-018 | 🚧 Planned for PLAT-1545 |
| FR-005 | FR-005-AC-2 | TC-019 | 🚧 Planned for PLAT-1545 |
| FR-005 | FR-005-AC-3 | TC-020 | 🚧 Planned for PLAT-1545 |
| FR-005 | FR-005-AC-4 | TC-030 | 🚧 Planned for PLAT-1545 |
| FR-006 | FR-006-AC-1 | TC-021 | 🚧 Planned for PLAT-1559 |
| FR-006 | FR-006-AC-2 | TC-022 | 🚧 Planned for PLAT-1559 |
| FR-006 | FR-006-AC-3 | TC-023 | 🚧 Planned for PLAT-1559 |
| FR-007 | FR-007-AC-1 | TC-024 | 🚧 Planned for PLAT-1559 |
| FR-007 | FR-007-AC-2 | TC-025 | 🚧 Planned for PLAT-1559 |
| FR-007 | FR-007-AC-3 | TC-026 | 🚧 Planned for PLAT-1559 |

## Non-Functional Requirement Coverage

| Non-Functional Req | Verification Method | Evidence/Test Cases | Status |
|---|---|---|---|
| NFR-001 | Test | TC-027, TC-028 | 🚧 Planned for PLAT-1549 |
| NFR-001 | Analysis | TC-029 | 🚧 Planned with source authoring |

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---|---|---|---|---|---|
| TC-001 | The M1 manifest lists only the Part 11 set at the selected version | Unit | P0 | FR-001-AC-1 | 🚧 Planned for PLAT-1545 |
| TC-002 | The installed module contains only clause-set contributions | Unit | P0 | FR-001-AC-2 | 🚧 Planned for PLAT-1545 |
| TC-003 | Local installation succeeds and reports `pack: false` | Integration | P0 | FR-001-AC-3 | 🚧 Planned for PLAT-1545 |
| TC-004 | The specification corpus validates with the declared artifact module | Integration | P1 | FR-001-AC-4 | 🚧 Planned for PLAT-1545 |
| TC-005 | The Part 11 set carries its exact rights values and a non-blank public-source basis | Unit | P0 | FR-002-AC-1 | 🚧 Planned for PLAT-1545 |
| TC-006 | Publish-check accepts the Part 11 module with original-text rights | Integration | P0 | FR-002-AC-2 | 🚧 Planned for PLAT-1549 |
| TC-007 | Publish-check rejects a set declared with licensed text | Integration | P1 | FR-002-AC-3 | 🚧 Planned for PLAT-1549 |
| TC-008 | The set identity and source metadata match the Part 11 specification | Unit | P0 | FR-003-AC-1 | 🚧 Planned for PLAT-1423 |
| TC-009 | The set contains exactly the 25 specified CFR paragraph identifiers | Unit | P0 | FR-003-AC-2 | 🚧 Planned for PLAT-1423 |
| TC-010 | Each clause is mandatory and references at least one catalog output | Unit | P0 | FR-003-AC-3 | 🚧 Planned for PLAT-1423 |
| TC-011 | A clause that references an undeclared output fails validation with its clause ID | Unit | P1 | FR-003-AC-4 | 🚧 Planned for PLAT-1423 |
| TC-012 | Closed-system controls bind and signature controls do not bind when signatures are unused | Unit | P0 | FR-004-AC-1 | 🚧 Planned for PLAT-1423 |
| TC-013 | Open-system controls remain unresolved without a supplied appropriateness assessment | Unit | P0 | FR-004-AC-2 | 🚧 Planned for PLAT-1423 |
| TC-014 | Per-paragraph open-system appropriateness values resolve only their matching 11.10 controls | Unit | P0 | FR-004-AC-3 | 🚧 Planned for PLAT-1423 |
| TC-015 | Section 11.300 binds only for a supplied identification-code/password method | Unit | P0 | FR-004-AC-4 | 🚧 Planned for PLAT-1423 |
| TC-016 | An empty applicability context leaves every clause unresolved | Unit | P1 | FR-004-AC-5 | 🚧 Planned for PLAT-1423 |
| TC-017 | Undeclared applicability dimensions or values are rejected | Unit | P1 | FR-004-AC-6 | 🚧 Planned for PLAT-1423 |
| TC-018 | The US catalog contains its exact 18 output definitions and M1 entries | Unit | P0 | FR-005-AC-1 | 🚧 Planned for PLAT-1545 |
| TC-019 | Conflicting kind or description for a reused output fails across US sets | Unit | P0 | FR-005-AC-2 | 🚧 Planned for PLAT-1545 |
| TC-020 | A later US set reuses an output only with the catalog definition | Unit | P1 | FR-005-AC-3 | 🚧 Planned for PLAT-1545 |
| TC-021 | Customer-owned clauses are exactly those whose outputs are all procedures | Unit | P0 | FR-006-AC-1 | 🚧 Planned for PLAT-1559 |
| TC-022 | Delegated discharge requires a rationale and customer acceptance reference | Integration | P0 | FR-006-AC-2 | 🚧 Planned for PLAT-1559 |
| TC-023 | Direct discharge is rejected and the toolchain claims no procedure output | Integration | P0 | FR-006-AC-3 | 🚧 Planned for PLAT-1559 |
| TC-024 | The synthetic corpus validates against the discharge input contract | Integration | P1 | FR-007-AC-1 | 🚧 Planned for PLAT-1559 |
| TC-025 | Test-time fixture signing creates and verifies a signed commit and tag, then removes the temporary key | Integration | P1 | FR-007-AC-2 | 🚧 Planned for PLAT-1559 |
| TC-026 | Test-time discharge facts use and clean up a temporary evidence store | Integration | P1 | FR-007-AC-3 | 🚧 Planned for PLAT-1559 |
| TC-027 | Rights metadata passes the publication check for every US set | Integration | P0 | NFR-001-AC-1, NFR-001-M-1 | 🚧 Planned for PLAT-1549 |
| TC-028 | The source metadata identifies only the cited public eCFR and public-law basis | Unit | P1 | NFR-001-AC-2 | 🚧 Planned for PLAT-1549 |
| TC-029 | Rights analysis confirms original summaries and excludes paywalled source text | Analysis | P1 | NFR-001-AC-3 | 🚧 Planned with source authoring |
| TC-030 | The module schema contains no pack-level output catalog field | Unit | P1 | FR-005-AC-4 | 🚧 Planned for PLAT-1545 |
| TC-031 | The certification-submission clause maps to the FDA certification record output | Unit | P1 | FR-003-AC-5 | 🚧 Planned for PLAT-1423 |

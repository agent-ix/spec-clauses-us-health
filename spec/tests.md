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
  - target: "ix://agent-ix/spec-clauses-us-health/FR-008"
    type: covers
  - target: "ix://agent-ix/spec-clauses-us-health/FR-009"
    type: covers
  - target: "ix://agent-ix/spec-clauses-us-health/FR-010"
    type: covers
  - target: "ix://agent-ix/spec-clauses-us-health/FR-011"
    type: covers
  - target: "ix://agent-ix/spec-clauses-us-health/FR-012"
    type: covers
  - target: "ix://agent-ix/spec-clauses-us-health/FR-013"
    type: covers
  - target: "ix://agent-ix/spec-clauses-us-health/FR-014"
    type: covers
  - target: "ix://agent-ix/spec-clauses-us-health/FR-018"
  - target: "ix://agent-ix/spec-clauses-us-health/FR-017"
    type: covers
  - target: "ix://agent-ix/spec-clauses-us-health/NFR-001"
    type: covers
---
# TM-001: US Health-Law Compliance Pack Test Matrix

## Overview

This matrix defines the planned verification cases for the US health-law
module and its discharge corpus. Each acceptance criterion maps to a concrete test case.
Cases move from planned to implemented when their implementation tickets add
executable tests and criterion trace tags. This document records the test plan;
Quire's computed matrix and source trace tags remain the evidence of
implementation coverage.

The module scaffold and catalog tests belong to PLAT-1545. Clause evaluation
tests are authored with PLAT-1423. PLAT-1553 binds Part 11 outputs to producing
capabilities and verifies the customer-owned table; corpus discharge cases
remain with PLAT-1559. Licensing rights metadata is exercised by the PLAT-1549
publish gate; source-rights analysis records only the public source and its
rights basis. PLAT-1613 authors HIPAA clause content, PLAT-1616 authors its
NIST crosswalk, and PLAT-1621 delivers the addressable-disposition workflow.
PLAT-1572 authors the M2 FDA device-software guidance set and its level-based
evaluation tests. PLAT-1569 authors the M2 Part 820 set and its clause-table
and applicability tests. PLAT-1575 maps each M2 clause output to an available
producer or an owner ticket for outputs without a producer; its mapping checks
do not generate evidence facts.
PLAT-1582 authors the exact M2 guidance-to-Part-820 crosswalks and their
resolution tests.

## Functional Requirement Coverage

| Functional Req | Acceptance Criteria | Test Cases | Status |
|---|---|---|---|
| FR-001 | FR-001-AC-1 | TC-001 | 🚧 Planned for PLAT-1545 |
| FR-001 | FR-001-AC-2 | TC-002 | 🚧 Planned for PLAT-1545 |
| FR-001 | FR-001-AC-3 | TC-003 | 🚧 Planned for PLAT-1545 |
| FR-001 | FR-001-AC-4 | TC-004 | 🚧 Planned for PLAT-1545 |
| FR-002 | FR-002-AC-1 | TC-005 | ✅ Implemented in PLAT-1423 |
| FR-002 | FR-002-AC-2 | TC-006 | ✅ Implemented in PLAT-1423 |
| FR-002 | FR-002-AC-3 | TC-007 | ✅ Implemented in PLAT-1423 |
| FR-003 | FR-003-AC-1 | TC-008 | ✅ Implemented in PLAT-1423 |
| FR-003 | FR-003-AC-2 | TC-009 | ✅ Implemented in PLAT-1423 |
| FR-003 | FR-003-AC-3 | TC-010 | ✅ Implemented in PLAT-1423 |
| FR-003 | FR-003-AC-4 | TC-011 | ✅ Implemented in PLAT-1423 |
| FR-003 | FR-003-AC-5 | TC-031 | ✅ Implemented in PLAT-1423 |
| FR-004 | FR-004-AC-1 | TC-012 | ✅ Implemented in PLAT-1423 |
| FR-004 | FR-004-AC-2 | TC-013 | ✅ Implemented in PLAT-1423 |
| FR-004 | FR-004-AC-3 | TC-014 | ✅ Implemented in PLAT-1423 |
| FR-004 | FR-004-AC-4 | TC-015 | ✅ Implemented in PLAT-1423 |
| FR-004 | FR-004-AC-5 | TC-016 | ✅ Implemented in PLAT-1423 |
| FR-004 | FR-004-AC-6 | TC-017 | ✅ Implemented in PLAT-1423 |
| FR-005 | FR-005-AC-1 | TC-018 | 🚧 Planned for PLAT-1545 |
| FR-005 | FR-005-AC-2 | TC-019 | ✅ Implemented in PLAT-1553 |
| FR-005 | FR-005-AC-3 | TC-020 | 🚧 Planned for PLAT-1545 |
| FR-005 | FR-005-AC-4 | TC-030 | 🚧 Planned for PLAT-1545 |
| FR-006 | FR-006-AC-1 | TC-021 | ✅ Implemented in PLAT-1553 |
| FR-006 | FR-006-AC-2 | TC-022 | 🚧 Planned for PLAT-1559 |
| FR-006 | FR-006-AC-3 | TC-023 | 🚧 Planned for PLAT-1559 |
| FR-007 | FR-007-AC-1 | TC-024 | 🚧 Planned for PLAT-1559 |
| FR-007 | FR-007-AC-2 | TC-025 | 🚧 Planned for PLAT-1559 |
| FR-007 | FR-007-AC-3 | TC-026 | ✅ Single-set path in PLAT-1423; corpus extension in PLAT-1559 |
| FR-008 | FR-008-AC-1 | TC-032 | ✅ Implemented in PLAT-1595 |
| FR-008 | FR-008-AC-2 | TC-033 | ✅ Implemented in PLAT-1595 |
| FR-008 | FR-008-AC-3 | TC-034 | ✅ Implemented in PLAT-1595 |
| FR-008 | FR-008-AC-4 | TC-035 | ✅ Implemented in PLAT-1595 |
| FR-008 | FR-008-AC-5 | TC-036 | ✅ Implemented in PLAT-1595 |
| FR-009 | FR-009-AC-1 | TC-037 | ✅ Implemented in PLAT-1596 |
| FR-009 | FR-009-AC-2 | TC-038 | ✅ Implemented in PLAT-1596 |
| FR-009 | FR-009-AC-3 | TC-039 | ✅ Implemented in PLAT-1596 |
| FR-009 | FR-009-AC-4 | TC-040 | ✅ Implemented in PLAT-1596 |
| FR-009 | FR-009-AC-5 | TC-041 | ✅ Implemented in PLAT-1596 |
| FR-009 | FR-009-AC-6 | TC-042 | ✅ Implemented in PLAT-1596 |
| FR-010 | FR-010-AC-1 | TC-043 | ✅ Implemented in PLAT-1595 |
| FR-010 | FR-010-AC-2 | TC-044 | ✅ Implemented in PLAT-1595; includes future declared sets |
| FR-010 | FR-010-AC-3 | TC-045 | 🚧 Planned with source authoring |
| FR-010 | FR-010-AC-4 | TC-046 | ✅ Implemented in PLAT-1596 |
| FR-011 | FR-011-AC-1 | TC-047 | 🚧 Planned for PLAT-1600 |
| FR-011 | FR-011-AC-2 | TC-048 | 🚧 Planned for PLAT-1600 |
| FR-011 | FR-011-AC-3 | TC-049 | 🚧 Planned for PLAT-1600 |
| FR-011 | FR-011-AC-4 | TC-050 | 🚧 Planned for PLAT-1600 |
| FR-011 | FR-011-AC-5 | TC-051 | 🚧 Planned for PLAT-1600 |
| FR-012 | FR-012-AC-1 | TC-052 | 🚧 Planned for PLAT-1613 |
| FR-012 | FR-012-AC-2 | TC-053 | 🚧 Planned for PLAT-1613 |
| FR-012 | FR-012-AC-3 | TC-054 | 🚧 Planned for PLAT-1613 |
| FR-012 | FR-012-AC-4 | TC-055 | 🚧 Planned for PLAT-1621 |
| FR-012 | FR-012-AC-5 | TC-056 | 🚧 Planned for PLAT-1621 |
| FR-012 | FR-012-AC-6 | TC-068 | 🚧 Planned for PLAT-1613 |
| FR-013 | FR-013-AC-1 | TC-057 | 🚧 Planned for PLAT-1616 |
| FR-013 | FR-013-AC-2 | TC-058 | 🚧 Planned for PLAT-1616 |
| FR-013 | FR-013-AC-3 | TC-059 | 🚧 Planned for PLAT-1616 |
| FR-014 | FR-014-AC-1 | TC-069 | ✅ Implemented in PLAT-1569 |
| FR-014 | FR-014-AC-2 | TC-070 | ✅ Implemented in PLAT-1569 |
| FR-014 | FR-014-AC-3 | TC-071 | ✅ Implemented in PLAT-1569 |
| FR-014 | FR-014-AC-4 | TC-072 | ✅ Implemented in PLAT-1569 |
| FR-014 | FR-014-AC-5 | TC-073 | ✅ Implemented in PLAT-1569 |
| FR-015 | FR-015-AC-1 | TC-060 | ✅ Implemented in PLAT-1572 |
| FR-015 | FR-015-AC-2 | TC-061 | ✅ Implemented in PLAT-1572 |
| FR-015 | FR-015-AC-3 | TC-062 | ✅ Implemented in PLAT-1572 |
| FR-015 | FR-015-AC-4 | TC-063 | ✅ Implemented in PLAT-1572 |
| FR-015 | FR-015-AC-5 | TC-064 | ✅ Implemented in PLAT-1572 |
| FR-016 | FR-016-AC-1 | TC-074 | ✅ Implemented in PLAT-1569 |
| FR-016 | FR-016-AC-2 | TC-074 | ✅ Implemented in PLAT-1569 |
| FR-017 | FR-017-AC-1 | TC-078 | 🚧 Planned for PLAT-1582 |
| FR-017 | FR-017-AC-2 | TC-079 | 🚧 Planned for PLAT-1582 |
| FR-017 | FR-017-AC-3 | TC-080 | 🚧 Planned for PLAT-1582 |
| FR-017 | FR-017-AC-4 | TC-081 | 🚧 Planned for PLAT-1582 |
| FR-016 | FR-016-AC-3 | TC-065, TC-067 | ✅ Implemented in PLAT-1572 |
| FR-016 | FR-016-AC-4 | TC-065 | ✅ Implemented in PLAT-1572 |
| FR-016 | FR-016-AC-5 | TC-066 | ✅ Implemented in PLAT-1572 |
| FR-018 | FR-018-AC-1 | TC-075 | ✅ Implemented in PLAT-1575 |
| FR-018 | FR-018-AC-2 | TC-076 | ✅ Implemented in PLAT-1575 |
| FR-018 | FR-018-AC-3 | TC-077 | ✅ Implemented in PLAT-1575 |

## Non-Functional Requirement Coverage

| Non-Functional Req | Verification Method | Evidence/Test Cases | Status |
|---|---|---|---|
| NFR-001 | Test | TC-027, TC-028 | 🚧 Planned for PLAT-1549 |
| NFR-001 | Analysis | TC-029 (`reviews/plat-1572-source-rights-analysis.md`) | ✅ Recorded in PLAT-1572 |

## Test Case Summary

| Test ID | Title | Type | Priority | Traces To | Status |
|---|---|---|---|---|---|
| TC-001 | The M1 manifest lists only the Part 11 set at the selected version | Unit | P0 | FR-001-AC-1 | 🚧 Planned for PLAT-1545 |
| TC-002 | The installed module contains only clause-set contributions | Unit | P0 | FR-001-AC-2 | 🚧 Planned for PLAT-1545 |
| TC-003 | Local installation succeeds and reports `pack: false` | Integration | P0 | FR-001-AC-3 | 🚧 Planned for PLAT-1545 |
| TC-004 | The specification corpus validates with the declared artifact module | Integration | P1 | FR-001-AC-4 | 🚧 Planned for PLAT-1545 |
| TC-005 | The Part 11 set carries its exact rights values and a non-blank public-source basis | Unit | P0 | FR-002-AC-1 | ✅ Implemented in PLAT-1423 |
| TC-006 | Publish-check accepts the Part 11 module with original-text rights | Integration | P0 | FR-002-AC-2 | ✅ Implemented in PLAT-1423 |
| TC-007 | Publish-check rejects a set declared with licensed text | Integration | P1 | FR-002-AC-3 | ✅ Implemented in PLAT-1423 |
| TC-008 | The set identity and source metadata match the Part 11 specification | Unit | P0 | FR-003-AC-1 | ✅ Implemented in PLAT-1423 |
| TC-009 | The set contains exactly the 25 specified CFR paragraph identifiers | Unit | P0 | FR-003-AC-2 | ✅ Implemented in PLAT-1423 |
| TC-010 | Each clause is mandatory and references at least one catalog output | Unit | P0 | FR-003-AC-3 | ✅ Implemented in PLAT-1423 |
| TC-011 | A clause that references an undeclared output fails validation with its clause ID | Unit | P1 | FR-003-AC-4 | ✅ Implemented in PLAT-1423 |
| TC-012 | Closed-system controls bind and signature controls do not bind when signatures are unused | Unit | P0 | FR-004-AC-1 | ✅ Implemented in PLAT-1423 |
| TC-013 | Open-system controls remain unresolved without a supplied appropriateness assessment | Unit | P0 | FR-004-AC-2 | ✅ Implemented in PLAT-1423 |
| TC-014 | Per-paragraph open-system appropriateness values resolve only their matching 11.10 controls | Unit | P0 | FR-004-AC-3 | ✅ Implemented in PLAT-1423 |
| TC-015 | Section 11.300 binds only for a supplied identification-code/password method | Unit | P0 | FR-004-AC-4 | ✅ Implemented in PLAT-1423 |
| TC-016 | An empty applicability context leaves every clause unresolved | Unit | P1 | FR-004-AC-5 | ✅ Implemented in PLAT-1423 |
| TC-017 | Undeclared applicability dimensions or values are rejected | Unit | P1 | FR-004-AC-6 | ✅ Implemented in PLAT-1423 |
| TC-018 | The US catalog contains its exact 28 output definitions and M1 entries | Unit | P0 | FR-005-AC-1 | 🚧 Planned for PLAT-1545 |
| TC-019 | Conflicting kind or description for a reused output fails across US sets | Unit | P0 | FR-005-AC-2 | ✅ Helper and Part 11 catalog checked in PLAT-1553 |
| TC-020 | A later US set reuses an output only with the catalog definition | Unit | P1 | FR-005-AC-3 | 🚧 Planned for PLAT-1545 |
| TC-021 | Customer-owned clauses are exactly those whose outputs are all procedures | Unit | P0 | FR-006-AC-1 | ✅ Implemented in PLAT-1553 |
| TC-022 | Delegated discharge requires a rationale and customer acceptance reference | Integration | P0 | FR-006-AC-2 | 🚧 Planned for PLAT-1559 |
| TC-023 | Direct discharge is rejected and the toolchain claims no procedure output | Integration | P0 | FR-006-AC-3 | 🚧 Planned for PLAT-1559 |
| TC-024 | The synthetic corpus validates against the discharge input contract | Integration | P1 | FR-007-AC-1 | 🚧 Planned for PLAT-1559 |
| TC-025 | Test-time fixture signing creates and verifies a signed commit and tag, then removes the temporary key | Integration | P1 | FR-007-AC-2 | 🚧 Planned for PLAT-1559 |
| TC-026 | Test-time discharge facts use and clean up a temporary evidence store | Integration | P1 | FR-007-AC-3 | 🚧 Planned for PLAT-1559 |
| TC-027 | Rights metadata passes the publication check for every US set | Integration | P0 | NFR-001-AC-1, NFR-001-M-1 | 🚧 Planned for PLAT-1549 |
| TC-028 | The source metadata identifies only the cited public eCFR and public-law basis | Unit | P1 | NFR-001-AC-2 | 🚧 Planned for PLAT-1549 |
| TC-029 | June 2023 FDA software guidance analysis confirms original summaries and the public-source rights basis | Analysis | P1 | NFR-001-AC-3 | ✅ Recorded in PLAT-1572 |
| TC-030 | The module schema contains no pack-level output catalog field | Unit | P1 | FR-005-AC-4 | 🚧 Planned for PLAT-1545 |
| TC-031 | The certification-submission clause maps to the FDA certification record output | Unit | P1 | FR-003-AC-5 | ✅ Implemented in PLAT-1423 |
| TC-032 | The 524B set identity and source metadata match the current US Code source | Unit | P0 | FR-008-AC-1 | ✅ Implemented in PLAT-1595 |
| TC-033 | The 524B clause IDs exactly match the statutory table | Unit | P0 | FR-008-AC-2 | ✅ Implemented in PLAT-1595 |
| TC-034 | Cyber-device applicability binds, does not bind, or remains unresolved for the supplied value | Unit | P0 | FR-008-AC-3 | ✅ Implemented in PLAT-1595 |
| TC-035 | Every 524B clause is mandatory and references only declared outputs | Unit | P0 | FR-008-AC-4 | ✅ Implemented in PLAT-1595 |
| TC-036 | Cyber-device applicability reports undeclared values and is not inferred | Unit | P1 | FR-008-AC-5 | ✅ Implemented in PLAT-1595 |
| TC-037 | The FDA guidance set uses the current guidance identity, date, and official source | Unit | P0 | FR-009-AC-1 | ✅ Implemented in PLAT-1596 |
| TC-038 | The FDA guidance clause IDs exactly match the guidance table | Unit | P0 | FR-009-AC-2 | ✅ Implemented in PLAT-1596 |
| TC-039 | Every FDA guidance clause is recommended and names a declared output | Unit | P0 | FR-009-AC-3 | ✅ Implemented in PLAT-1596 |
| TC-040 | Section VII applicability follows the user-supplied cyber-device value | Unit | P0 | FR-009-AC-4 | ✅ Implemented in PLAT-1596 |
| TC-041 | Rights analysis finds no paywalled consensus-standard names or paraphrases | Analysis | P0 | FR-009-AC-5, NFR-001-AC-4 | ✅ Implemented in PLAT-1596 |
| TC-042 | The FDA clauses requiring an SBOM name the SBOM output with support status and end-of-support date | Unit | P0 | FR-009-AC-6 | ✅ Implemented in PLAT-1596 |
| TC-043 | Every cybersecurity clause output resolves to a row in the master catalog | Unit | P0 | FR-010-AC-1 | ✅ Implemented in PLAT-1595 |
| TC-044 | Cybersecurity set outputs match catalog kind and description across all sets | Unit | P0 | FR-010-AC-2 | ✅ Implemented in PLAT-1595; includes future declared sets |
| TC-045 | Each new cybersecurity catalog row names its producer or owning ticket | Inspection | P1 | FR-010-AC-3 | 🚧 Planned with source authoring |
| TC-046 | The guidance uses the dedicated SBOM output and declares no generic SOUP output for SBOM clauses | Unit | P1 | FR-010-AC-4 | ✅ Implemented in PLAT-1596 |
| TC-047 | The crosswalk table contains source, target key, target ID, and a supported relation value | Inspection | P1 | FR-011-AC-1 | 🚧 Planned for PLAT-1600 |
| TC-048 | Each 524B clause crosswalks to an FDA guidance clause | Unit | P0 | FR-011-AC-2 | 🚧 Planned for PLAT-1600 |
| TC-049 | Each cybersecurity clause resolves at least one NIST crosswalk target from the installed module | Integration | P0 | FR-011-AC-3 | 🚧 Planned for PLAT-1600 |
| TC-050 | An unknown NIST target fails with that identifier in the diagnostic | Unit | P1 | FR-011-AC-4 | 🚧 Planned for PLAT-1600 |
| TC-051 | Test dependencies install the published target module without copying its clause data | Inspection | P1 | FR-011-AC-5 | 🚧 Planned for PLAT-1600 |
| TC-052 | The M4 set identity, dated eCFR source, and original-text rights metadata match the specification | Unit | P0 | FR-012-AC-1 | 🚧 Planned for PLAT-1613 |
| TC-053 | Every table clause is present once with mandatory force, specified style, and catalog outputs | Unit | P0 | FR-012-AC-2 | 🚧 Planned for PLAT-1613 |
| TC-054 | `hipaa_role` values resolve only the applicable § 164.314(a)(2) clauses | Unit | P0 | FR-012-AC-3 | 🚧 Planned for PLAT-1613 |
| TC-055 | An alternate addressable discharge without accepted-risk rationale and named approver is rejected | Integration | P0 | FR-012-AC-4 | 🚧 Planned for PLAT-1621 |
| TC-056 | RMM shows the human addressable disposition rationale and approver and does not generate a decision | Integration | P0 | FR-012-AC-5 | 🚧 Planned for PLAT-1621 |
| TC-057 | The 274 source rows match the identifier-only workbook fixture with exact locators, direction, relation, and original rationale | Unit | P0 | FR-013-AC-1, FR-013-AC-3 | 🚧 Planned for PLAT-1616 |
| TC-058 | Every included standard has a target, § 164.314(b) is absent, all targets resolve, and AC-999 fails with its crosswalk named | Unit | P0 | FR-013-AC-2 | 🚧 Planned for PLAT-1616 |
| TC-059 | The 14 unmapped clauses remain explicit and every leading-zero normalization is recorded | Unit | P1 | FR-013-AC-3 | 🚧 Planned for PLAT-1616 |
| TC-060 | The M2 premarket device-software set identifies its official FDA source and public rights basis | Unit | P0 | FR-015-AC-1 | ✅ Implemented in PLAT-1572 |
| TC-061 | M2 premarket device-software clause IDs and outputs match the Section VI table | Unit | P0 | FR-015-AC-2 | ✅ Implemented in PLAT-1572 |
| TC-062 | Each M2 premarket software clause has recommended force, an output, and its table-defined level | Unit | P0 | FR-015-AC-3 | ✅ Implemented in PLAT-1572 |
| TC-063 | The M2 documentation level contains only ordered basic and enhanced values | Unit | P0 | FR-015-AC-4 | ✅ Implemented in PLAT-1572 |
| TC-064 | M2 specification validation and clause-set publish check both pass | Integration | P1 | FR-015-AC-5 | ✅ Implemented in PLAT-1572 |
| TC-065 | Basic and enhanced levels bind the specified Section VI rows; omitted level leaves all rows unresolved | Unit | P0 | FR-016-AC-3, FR-016-AC-4 | ✅ Implemented in PLAT-1572 |
| TC-066 | An undeclared documentation level leaves clauses unresolved with an explicit dimension diagnostic | Unit | P1 | FR-016-AC-5 | ✅ Implemented in PLAT-1572 |
| TC-067 | The basic-level RMM marks an enhanced-only recommendation not applicable | Integration | P1 | FR-016-AC-3 | ✅ Implemented in PLAT-1572 |
| TC-068 | HIPAA source-rights analysis confirms original summaries and excludes paywalled source text | Analysis | P1 | FR-012-AC-6 | 🚧 Planned for PLAT-1613 |
| TC-069 | `test_part820_identity_source_and_rights_match_the_dated_ecfr_snapshot`: wrong key, source URL, or rights basis fails the exact metadata assertion | Unit | P0 | FR-014-AC-1 | ✅ Implemented in PLAT-1569 |
| TC-070 | `test_part820_clause_ids_match_the_normative_table_and_exclusions`: an extra or missing ID fails the exact set comparison | Unit | P0 | FR-014-AC-2 | ✅ Implemented in PLAT-1569 |
| TC-071 | `test_part820_clauses_match_force_outputs_and_ibr_treatment`: wrong force, output list, or IBR text fails with the affected clause ID | Unit | P0 | FR-014-AC-3 | ✅ Implemented in PLAT-1569 |
| TC-072 | `test_part820_applicability_matches_the_normative_table_exactly` and mutation fixtures: changed, missing, or added expression raises an assertion naming the clause ID | Unit | P0 | FR-014-AC-4 | ✅ Implemented in PLAT-1569 |
| TC-073 | `test_part820_spec_validates_and_module_passes_publish_check`: a nonzero validation or publish-check exit fails acceptance | Integration | P1 | FR-014-AC-5 | ✅ Implemented in PLAT-1569 |
| TC-074 | `test_part820_human_dimensions_control_only_their_dependent_clauses`: each declared dimension binds, excludes, or remains unresolved as supplied; `device_class=class_II` does not resolve a missing Part 820 dimension | Unit | P0 | FR-016-AC-1, FR-016-AC-2 | ✅ Implemented in PLAT-1569 |
| TC-075 | Every unique M2 clause and expected-output pair appears once in the producer mapping table | Unit | P0 | FR-018-AC-1 | ✅ Implemented in PLAT-1575 |
| TC-076 | Every M2 record mapping names its owner or a producer whose module entries or CLI command resolve in installed sources | Unit | P0 | FR-018-AC-2 | ✅ Implemented in PLAT-1575 |
| TC-077 | Shared output names retain the same kind and description in every US set | Unit | P0 | FR-018-AC-3 | ✅ Implemented in PLAT-1575 |
| TC-078 | `test_premarket_crosswalk_pairs_match_the_m2_table_and_resolve`: source-target pairs equal the M2 table and all declared targets resolve | Unit | P0 | FR-017-AC-1 | 🚧 Planned for PLAT-1582 |
| TC-079 | `test_crosswalk_unknown_source_or_target_fails_with_identifier`: invalid source and target fixtures fail with their identifier | Unit | P0 | FR-017-AC-2 | 🚧 Planned for PLAT-1582 |
| TC-080 | `test_crosswalk_requires_relation_and_nonblank_rationale`: each mapping has supported relation and one-sentence original rationale without designators | Unit | P1 | FR-017-AC-3 | 🚧 Planned for PLAT-1582 |
| TC-081 | `test_crosswalk_is_informative_and_does_not_claim_equivalence`: all mappings remain informative | Unit | P1 | FR-017-AC-4 | 🚧 Planned for PLAT-1582 |

---
id: FR-017
title: FDA device-software recommendations crosswalk to Part 820 clauses
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-014"
    type: depends_on
  - target: "ix://agent-ix/spec-clauses-us-health/FR-015"
    type: depends_on
---
# FR-017: FDA device-software recommendations crosswalk to Part 820 clauses

## Description

The M2 pack represents relationships between FDA device-software guidance
clauses and applicable Part 820 clauses as an informative crosswalk. These
relationships do not create discharge facts, decide applicability, or claim
that Quoin or an RMM renders the crosswalk.

Each crosswalk row SHALL preserve a human-authored relation and rationale. A
row SHALL NOT state legal equivalence.

## Behavior

- Each guidance clause SHALL crosswalk to at least one clause declared in the
  M2 Part 820 table, with exactly the targets listed for that source in the
  `Part 820 crosswalk target IDs` column of the M2 FDA table.
- Each crosswalk row SHALL have a supported relation and a non-empty,
  one-sentence rationale in original words. A rationale SHALL NOT contain
  source or target designators.
- The crosswalk SHALL NOT infer a match from similar wording or include a
  target absent from the Part 820 table.
- Each crosswalk SHALL be informative. It does not assert equivalence, create
  discharge facts, or claim RMM rendering.
- An unknown source or target clause identifier SHALL fail validation with a
  diagnostic naming the crosswalk and invalid identifier.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-017-AC-1 | Every guidance clause has one or more target IDs exactly as listed in the M2 FDA table; the source-target pair set equals that table, every target resolves to a Part 820 ID, and every row has relation and rationale. | Test |
| FR-017-AC-2 | A crosswalk fixture with an unknown source or target clause fails and names the invalid identifier. | Test |
| FR-017-AC-3 | Every row has a supported relation and a non-empty, one-sentence rationale without source or target designators; missing values fail validation. | Test |
| FR-017-AC-4 | Every mapping is informative and asserts no equivalence; no discharge facts or RMM rendering are claimed. | Test |

## Trace Bindings

| Criterion | Test | Verification |
|---|---|---|
| FR-017-AC-1 | TC-078 `test_premarket_crosswalk_pairs_match_the_m2_table_and_resolve` | Unit |
| FR-017-AC-2 | TC-079 `test_crosswalk_unknown_source_or_target_fails_with_identifier` | Unit |
| FR-017-AC-3 | TC-080 `test_crosswalk_requires_relation_and_nonblank_rationale` | Unit |
| FR-017-AC-4 | TC-081 `test_crosswalk_is_informative_and_does_not_claim_equivalence` | Unit |

## Dependencies

- Crosswalk rows are authored in PLAT-1582.
- Uses the clause IDs in
  [FR-014](./FR-014-part-820-quality-management-system-clause-set.md) and
  [FR-015](./FR-015-fda-device-software-guidance-clause-set.md).

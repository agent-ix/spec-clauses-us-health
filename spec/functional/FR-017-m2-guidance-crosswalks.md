---
id: FR-017
title: FDA device-software recommendations crosswalk to Part 820 clauses
type: FR
---
# FR-017: FDA device-software recommendations crosswalk to Part 820 clauses

## Description

The M2 pack represents relationships between FDA device-software guidance
clauses and applicable Part 820 clauses as an informative crosswalk.

Each crosswalk row SHALL preserve a human-authored relation and rationale. A
row SHALL NOT state legal equivalence.

## Behavior

- Each guidance clause SHALL crosswalk to at least one clause declared in the
  M2 Part 820 table.
- Each crosswalk row SHALL have a supported relation and non-empty original
  rationale.
- The crosswalk SHALL NOT infer a match from similar wording or include a
  target absent from the Part 820 table.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-017-AC-1 | Every guidance clause in the M2 table has at least one crosswalk row whose target resolves to an ID in the Part 820 table and whose relation and rationale are present. | Test |
| FR-017-AC-2 | A crosswalk fixture with an unknown source or target clause fails and names the invalid identifier. | Test |
| FR-017-AC-3 | A crosswalk row with a missing relation or empty rationale fails validation. | Test |
| FR-017-AC-4 | The crosswalk identifies every mapping as informative and contains no relation `equivalent`. | Test |

## Dependencies

- Crosswalk rows are authored in PLAT-1582.
- Uses the clause IDs in
  [FR-014](./FR-014-part-820-quality-management-system-clause-set.md) and
  [FR-015](./FR-015-fda-device-software-guidance-clause-set.md).

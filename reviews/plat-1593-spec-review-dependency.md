---
id: SR-006
title: Integrity review of PLAT-1593 spec changes
type: SpecReview
analysis: integrity
scope: "agent-ix/spec-clauses-us-health; FR-008 through FR-011 and the master crosswalk table"
review_set: all
---

## Summary

The IDs are sequential and the new requirement relationships are acyclic. The master crosswalk table uses a relation value outside the engine contract, so the crosswalk rows cannot validate as written.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | Every crosswalk row uses mapped_to, but CrosswalkRelation accepts only equivalent, partial, or informative; choose a supported relation for each mapping and require supported values in the table. | spec/spec.md:183 | wrong-requirement |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | after_excerpt: Each relation value uses the `ClauseSet` enum: `equivalent`, `partial`, or `informative`. Every mapping in this plan is `informative`: it points readers to related guidance or controls and makes no equivalence or partial-coverage claim. |

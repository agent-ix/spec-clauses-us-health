---
id: FR-001
title: "Preserve synthetic record integrity"
type: FR
relationships: []
---
# FR-001: Preserve synthetic record integrity

## Description

The fictional `example.invalid` records service SHALL retain each synthetic
record together with its declared digest.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-001-AC-1 | A stored record retains its declared digest. | Test |

## Dependencies

- Upstream: the fictional `example.invalid` record submission service.

---
id: SR-008
title: Evidence review of PLAT-1593 spec changes
type: SpecReview
analysis: evidence
scope: "agent-ix/spec-clauses-us-health; FR-009-AC-3, FR-010-AC-1, NFR-001-AC-2 through AC-4, and guidance output definitions"
review_set: all
---

## Summary

Quoin advise's mismatches on Inspection and Analysis methods were reviewed and are justified for producer ownership and semantic rights review. The specification does not require the SBOM record to carry the support level and end-of-support date required by the current guidance and the ticket.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | medium | FR-009 and its catalog allow V.A.4 and VII.C.3 to emit a generic soup-list without requiring per-component support status and end-of-support dates; add those fields to the output definition and its acceptance criteria. | spec/functional/FR-009-fda-premarket-cybersecurity-guidance-clause-set.md:46 | missing-requirement |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | after_excerpt: Each SBOM component SHALL include its support status and end-of-support date. |

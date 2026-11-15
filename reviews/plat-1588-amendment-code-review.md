---
id: SR-034
title: "Code review — PLAT-1588 missing-reference contract clarification"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; PR #26 at bcefb9f0a870d85b8aff344e7a795bce7c9ae258; FR-019-AC-4, TC-082, prior SR-029 record"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-019"
    type: references
---

## Summary

The amendment makes the rejecting component explicit and aligns the matrix description with PLAT-1588 AC4. It does not claim that Quoin CLI rejects missing references. No defects were found.

## Review Coverage

- Examined `spec/functional/FR-019-m2-corpus-discharge.md`: the changed Behavior and FR-019-AC-4 require the pack-side evidence-reference resolver to reject the missing reference and identify its clause.
- Examined `spec/tests.md`: TC-082 now says pack-side missing-reference rejection naming the clause and remains Planned for PLAT-1588.
- Examined `reviews/plat-1588-spec-review-sr029.md`: it records the earlier still-open wording mismatch as historical review data; the current amendment addresses it.
- Compared the amended requirement with PLAT-1588 AC4: the acceptance criterion requires the ref-resolution check to fail and name the clause, without requiring Quoin CLI failure.
- Quire validation exits 0. The existing FR-009 vague-response warning and module-resolution notices are outside this amendment.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |

```yaml
clean: true
scope:
  - {id: FR-019, path: "spec/functional/FR-019-m2-corpus-discharge.md", role: examined, excerpt: "The pack-side evidence-reference resolver SHALL reject a discharge fact that references an evidence file absent from the corpus and identify the affected clause. The Quoin discharge CLI is not the component that rejects this missing reference."}
  - {id: FR-019-AC-4, path: "spec/functional/FR-019-m2-corpus-discharge.md", role: examined, excerpt: "Changing a discharge fact's evidence reference to a missing corpus file makes the pack-side evidence-reference resolver reject the fact and identify the affected clause."}
  - {id: TC-082, path: "spec/tests.md", role: examined, excerpt: "M2 RMM includes three ordered sets with matching row counts, mapped outcomes, basic-level applicability, pack-side missing-reference rejection naming the clause, and deterministic Markdown | Integration | P0 | FR-019-AC-1, FR-019-AC-2, FR-019-AC-3, FR-019-AC-4, FR-019-AC-5 | Planned for PLAT-1588"}
  - {id: PLAT-1588-AC-4, path: "Linear PLAT-1588", role: context_only, excerpt: "Changing one fact's evidence ref to a missing file fails the ref-resolution check, naming the clause."}
findings: []
```

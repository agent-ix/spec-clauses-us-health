---
id: SR-036
title: "EARS review — PLAT-1588 reference resolver requirement"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-clauses-us-health; PR #26; FR-019 behavior and AC-4"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-019"
    type: references
---

## Summary

The revised FR-019 behavior and AC-4 name a subject, a concrete rejection response, and a clause-specific diagnostic. Quire reports no EARS warning for FR-019; no defects were found.

## Review Coverage

- Examined the edited FR-019 Behavior statement and AC-4 for EARS grammar, singularity, subject, and verifiable outcome.
- Confirmed the ticket-specific test oracle is the pack-side resolver, not the Quoin discharge CLI.
- Quire validation reported only the existing FR-009 vague-response advisory; FR-019 has no EARS diagnostic.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |

```yaml
clean: true
scope:
  - {id: FR-019, path: "spec/functional/FR-019-m2-corpus-discharge.md", role: examined, excerpt: "The pack-side evidence-reference resolver SHALL reject a discharge fact that references an evidence file absent from the corpus and identify the affected clause. The Quoin discharge CLI is not the component that rejects this missing reference."}
  - {id: FR-019-AC-4, path: "spec/functional/FR-019-m2-corpus-discharge.md", role: examined, excerpt: "Changing a discharge fact's evidence reference to a missing corpus file makes the pack-side evidence-reference resolver reject the fact and identify the affected clause."}
findings: []
```

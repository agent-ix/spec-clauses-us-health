---
id: SR-012
title: Code review of PLAT-1593 PR checks
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; tests/test_clause_sets.py catalog assertion affected by FR-010-AC-1"
review_set: all
---

## Summary

The spec-only PR changes the normative catalog size, and the existing catalog test fails against that new source of truth. The failure prevents the PR checks from passing.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | CI fails because tests/test_clause_sets.py expects 18 catalog entries while the updated specification defines 24; update the test and expected catalog from the normative source so the check passes with the six added entries. | tests/test_clause_sets.py:220 | correct-requirement-no-evidence |

---
id: SR-004
title: "Base specification review — HIPAA Security Rule set (PLAT-1612)"
type: SpecReview
analysis: base
scope: "PR #7: spec/spec.md, spec/functional/FR-005-pack-wide-output-catalog.md, spec/functional/FR-008-hipaa-security-rule-clause-set.md, spec/functional/FR-009-hipaa-nist-crosswalk-source-and-target.md, spec/tests.md"
review_set: all
---
## Summary

The changed specification is organized and its acceptance criteria map to planned test cases. The normative HIPAA table contains multiple incorrect § 164.308 standard identifiers, so the clause set cannot be implemented to match the controlling regulation as written.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | The normative table substitutes parent paragraph IDs for standards in § 164.308(a),. This makes the promised exact clause set inaccurate. | FR-008, FR-008-AC-2 |

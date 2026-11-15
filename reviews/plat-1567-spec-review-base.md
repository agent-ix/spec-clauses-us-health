---
id: SR-026
title: Base review of PLAT-1567 validation-command amendment
type: SpecReview
analysis: base
scope: "agent-ix/spec-clauses-us-health; FR-014-AC-5 and FR-015-AC-5"
review_set: subset
---

## Summary

No active AssuranceProfile instance applies in this repository. The corrected validation commands still omit the process module root required to load the repository's `TestMatrix` artifact, so both criteria fail on the full spec glob.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | medium | The command supplies only the ISO module root, but `spec/tests.md` declares `type: TestMatrix` from `spec-artifacts-process`; Quire reports `unknown type 'TestMatrix'` and exits 1. Add the process module root as another repeatable `--module` argument. | FR-014-AC-5, FR-015-AC-5 | wrong-requirement |

+++ [reviewer data]

```yaml
clean: false
scope:
  - id: FR-014-AC-5
    path: spec/functional/FR-014-part-820-quality-management-system-clause-set.md
    role: examined
    excerpt: "`quire validate --scope . --module <spec-artifacts-iso-module-root> 'spec/**/*.md'` and `quire publish-check --module <pkg>` both exit 0."
  - id: FR-015-AC-5
    path: spec/functional/FR-015-fda-device-software-guidance-clause-set.md
    role: examined
    excerpt: "`quire validate --scope . --module <spec-artifacts-iso-module-root> 'spec/**/*.md'` and `quire publish-check --module <pkg>` both exit 0."
findings:
  - fnd: FND-001
    severity: medium
    confidence: high
    method: spec-review/base
    check: soundness
    artifact_id: FR-014-AC-5
    related_ids: [FR-015-AC-5]
    path: spec/functional/FR-014-part-820-quality-management-system-clause-set.md
    lines: "47"
    excerpt: "`quire validate --scope . --module <spec-artifacts-iso-module-root> 'spec/**/*.md'` and `quire publish-check --module <pkg>` both exit 0."
    finding: "The command omits the process module root that declares the TestMatrix archetype used by spec/tests.md. Running it against the full spec glob with only spec-artifacts-iso exits 1 with unknown type 'TestMatrix'; adding spec-artifacts-process as a second --module root exits 0."
```
+++

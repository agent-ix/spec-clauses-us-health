---
id: SR-029
title: "Specification review — PLAT-1588 test matrix"
type: SpecReview
analysis: base
scope: "agent-ix/spec-clauses-us-health; PR #24 at b76147b3dc534d867454a2a1598ee7202d4b4e4b; spec/tests.md M2 matrix entry"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-clauses-us-health/FR-007", type: references }
---

## Summary

The new test-matrix row records the M2 discharge behavior but binds it only to FR-007-AC-2 and FR-007-AC-3. Those criteria specify temporary signing material and evidence-store lifecycle; they do not specify the M2 RMM's clause ordering, open work, applicability, reference failure, or deterministic output. PLAT-1588's ticket ACs are not represented by functional acceptance criteria in the matrix.

## Verdict

**FAIL** at `b76147b3dc534d867454a2a1598ee7202d4b4e4b`; add requirement ownership for the M2 discharge behavior before marking the matrix case implemented.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | TC-082 marks M2 discharge outcomes implemented under FR-007 ACs that do not define those outcomes. | spec/tests.md:243; spec/functional/FR-007-reference-corpus.md:16-28 |

## Review Coverage

- Checked the changed matrix entry against FR-007-AC-2/3, which cover signed commit/tag verification and temporary evidence-store use.
- Checked that the M2 output behavior comes from PLAT-1588 AC1–5 and PLAT-1575 AC4, while no functional FR acceptance criterion specifies those discharge outcomes.
- This is a base traceability finding. No integrity sub-analysis was run because the PR changes no FR structure or requirement text.

## Findings data

```yaml
findings:
  - fnd: FND-001
    severity: medium
    confidence: high
    method: spec-review/base
    check: trace
    artifact_id: TC-082
    related_ids: [FR-007-AC-2, FR-007-AC-3]
    path: spec/tests.md
    lines: "243"
    excerpt: "| TC-082 | M2 RMM includes all three ordered sets, retains open work, and is deterministic | Integration | P0 | FR-007-AC-2, FR-007-AC-3 | ✅ Implemented in PLAT-1588 |"
    finding: "The test-matrix row claims M2 discharge behavior is implemented, but its only FR links cover creation and cleanup of fixture signing material and the evidence store. No functional requirement AC owns the ordered M2 index, open-work result, applicability output, missing-reference rejection, or deterministic Markdown that PLAT-1588 tests. The matrix therefore cannot trace the ticket's M2 discharge acceptance criteria to a normative requirement."
bindings:
  - {test_id: TC-082, ac_id: FR-007-AC-2, trace: correct}
  - {test_id: TC-082, ac_id: FR-007-AC-3, trace: correct}
```


## New findings (disposition pass 2)

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-002 | medium | FR-019-AC-4 requires the discharge operation to fail, but the test accepts a successful Quoin discharge and only the separate pack resolver raises. | spec/functional/FR-019-m2-corpus-discharge.md:51; tests/test_m2_discharge.py:496-507 |

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | FR-019 now owns all five M2 discharge outcomes, and TC-082 maps each FR-019 AC to the integration test. |
| FND-002 | still-open | The spec says the discharge operation fails, while the tested Quoin command returns success and the separate pack resolver raises; the requirement wording must match the intended pack resolver contract. |

```yaml
dispositions:
  - fnd: FND-001
    outcome: fixed
    after_excerpt: |-
      | FR-019 | FR-019-AC-1 | TC-082 | ✅ Implemented in PLAT-1588 |
      | FR-019 | FR-019-AC-2 | TC-082 | ✅ Implemented in PLAT-1588 |
      | FR-019 | FR-019-AC-3 | TC-082 | ✅ Implemented in PLAT-1588 |
      | FR-019 | FR-019-AC-4 | TC-082 | ✅ Implemented in PLAT-1588 |
      | FR-019 | FR-019-AC-5 | TC-082 | ✅ Implemented in PLAT-1588 |
  - fnd: FND-002
    outcome: still-open
    reason: "FR-019-AC-4 currently requires the discharge operation to fail; the test passes Quoin discharge and only the pack resolver fails. Clarify that the pack resolver, rather than the Quoin CLI, is the component that rejects the reference."
```

## Disposition pass 2 result

FND-001 is fixed. FND-002 remains open pending alignment of FR-019-AC-4 with PLAT-1588 AC4's pack reference-resolution contract.

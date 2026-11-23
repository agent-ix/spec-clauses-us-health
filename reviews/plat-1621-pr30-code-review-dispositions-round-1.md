---
id: RV-1621
title: "PLAT-1621 PR #30 code review dispositions, round 1"
type: Review
---

<!-- reviewer-dispositions repo=agent-ix/spec-clauses-us-health visibility=public quoin=0.35.0 module=spec-artifacts-process@v0.31.0 id=SR-20261104139914 round=1 model=gpt-6.1-sol run=89d407ca-049b-455c-a4b6-d64625b72b9b -->

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | `tests/test_m4_discharge.py:278-283` now compares the index count with the emitted M4 matrix rows. |
| FND-002 | fixed | `tests/test_m4_discharge.py:305-312` now asserts the delegated decision and procedure approvalRef in the RMM tailoring description. |
| FND-003 | fixed | `tests/test_m4_discharge.py:353-377` now rejects alternate facts missing the decision or approvalRef; the empty-rationale Quoin discharge refusal remains exercised. |
| FND-004 | fixed | `tests/test_m4_discharge.py:123-128` now asserts that evaluation emits no disposition/facts or per-clause decision fields. |
| FND-005 | still-open | The passing test still records `delegated` for addressable clause `164.308(a)(5)(ii)(A)` and asserts it is tailored. FR-012 requires `accepted_risk` for any non-direct addressable discharge; Quoin 0.35.0 accepts this contrary record. FR-173-AC-13 only concerns missing/invalid scope-exclusion fields and does not authorize this pack-level exception. Route the conformance gap to the Quoin engine owner; no scope expansion is needed. |

At updated head `0a7419bf4ba7d208bb8b5b7b1e7ab72ed8ddb90c`, FND-001 through FND-004 are fixed. FND-005 remains open: `164.308(a)(5)(ii)(A)` has `styles.implementation: addressable` and only the `written-procedure` output, yet TC-084 puts it in `CUSTOMER_OWNED`, records `decision: delegated`, and asserts a tailored row. FR-012 Behavior says any other addressable discharge must be a human `accepted_risk` disposition, and FR-012-AC-4 rejects an alternate without `accepted_risk`. A delegated disposition is a non-direct discharge on that addressable clause, so the accepted report violates the existing requirement. FR-173-AC-13 rejects missing or invalid `scope_exclusion` fields; it does not change the M4 pack-specific rule. The current focused test passes on Quoin 0.35.0 while preserving the invalid result. This needs a Quoin-side conformance fix or a requirement-consistent test input before merge.

Updated artifact: `/tmp/plat-1621-pr30-reviews/plat-1621-pr30-code-review.md`.

+++ [reviewer data]

```yaml
dispositions:
  - fnd: FND-001
    outcome: fixed
    path: tests/test_m4_discharge.py
    lines: "278-283"
    after_excerpt: |-
      m4_matrix = next(
          matrix
          for matrix in report["matrices"]
          if clause_set_key(matrix["clauseSet"]) == M4_KEY
      )
      assert indexes[M4_KEY]["rowCount"] == len(m4_matrix["rows"])
  - fnd: FND-002
    outcome: fixed
    path: tests/test_m4_discharge.py
    lines: "309-311"
    after_excerpt: |-
      assert rows[clause_id]["tailoringDescription"] == (
          f"delegated (approval {procedure_approval})"
      )
  - fnd: FND-003
    outcome: fixed
    path: tests/test_m4_discharge.py
    lines: "353-356"
    after_excerpt: |-
      rejected_facts = [
          {key: value for key, value in facts[4].items() if key != "decision"},
          {key: value for key, value in facts[4].items() if key != "approvalRef"},
      ]
  - fnd: FND-004
    outcome: fixed
    path: tests/test_m4_discharge.py
    lines: "123-128"
    after_excerpt: |-
      assert "dispositions" not in binding
      assert "facts" not in binding
      assert all(
          "decision" not in clause and "disposition" not in clause
          for clause in binding["clauses"]
      )
  - fnd: FND-005
    outcome: still-open
    reason: >-
      The test still records and asserts a delegated discharge on addressable
      clause 164.308(a)(5)(ii)(A), while FR-012 Behavior and FR-012-AC-4 require
      any non-direct addressable discharge to use accepted_risk. Quoin 0.35.0
      accepts it; the focused test passes. FR-173-AC-13 only concerns required
      scope-exclusion fields and does not authorize this pack-level exception.
new_findings:
  - fnd: FND-005
    severity: high
    confidence: high
    method: code-review
    check: code-bug
    artifact_id: FR-012-AC-4
    related_ids: [FR-006-AC-2, TC-084]
    path: tests/test_m4_discharge.py
    lines: "220-229, 305-312"
    related_paths:
      - spec/functional/FR-012-hipaa-security-rule-clause-set.md
      - spec/functional/FR-006-customer-owned-obligations.md
      - spec_clauses_us_health/clauses/us-hhs-45-cfr-164-subpart-c-2026-11-12.json
    excerpt: |-
      A direct fact can discharge an addressable clause as implemented as written; an alternate discharge without a human `accepted_risk`, non-empty rationale, and named `approvalRef` is rejected.
    finding: >-
      TC-084 records a delegated disposition for 164.308(a)(5)(ii)(A), whose
      clause entry declares styles.implementation addressable and expectedOutputs
      only written-procedure, then asserts that Quoin renders it as tailored
      with delegated (approval <procedure_approval>). That is a non-direct
      addressable discharge without accepted_risk. The focused Quoin 0.35.0
      test passes, so the existing addressable rule is not enforced for this
      record. FR-173-AC-13 concerns missing/invalid scope-exclusion fields and
      does not authorize this M4 behavior.
```

+++

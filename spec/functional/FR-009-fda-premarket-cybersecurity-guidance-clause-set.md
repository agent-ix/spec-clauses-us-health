---
id: FR-009
title: The FDA cybersecurity guidance set records current recommendations
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-003"
    type: extends
  - target: "ix://agent-ix/spec-clauses-us-health/FR-004"
    type: extends
---
# FR-009: The FDA cybersecurity guidance set records current recommendations

## Description

The pack SHALL record current FDA premarket cybersecurity recommendations as
recommended clauses, including the recommendations for cyber devices under
section 524B.

## Behavior

- The set SHALL use authority `us-fda`, ID `premarket-cybersecurity`, and
  version `2026-02-03`, matching the date on the current FDA final guidance.
- The set SHALL contain exactly the clause IDs and outputs in the FDA
  cybersecurity guidance table in [the master specification](../spec.md).
- Every clause SHALL have force `recommended` and original concise wording.
- The set SHALL leave the applicability of general recommendation clauses
  unconditional.
- When the user supplies `cyber_device=yes`, the set SHALL bind each section
  VII.C clause.
- If the user supplies `cyber_device=no`, the set SHALL leave each section
  VII.C clause not binding.
- If the user omits `cyber_device`, the set SHALL leave each section VII.C
  clause unresolved.
- The set SHALL declare `cyber_device` with the same unordered values as the
  section 524B set.
- The set SHALL NOT infer `cyber_device` from other product facts.
- The set SHALL cite only the current FDA guidance and other public sources.
- The set SHALL NOT name or paraphrase paywalled consensus standards.
- The `V.A.4` and `VII.C.3` clauses SHALL reference the `sbom` output, which
  records component support status and end-of-support dates.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-009-AC-1 | The set identity is exactly `us-fda/premarket-cybersecurity@2026-02-03`, and its source metadata identifies the current FDA guidance and official FDA URL. | Test |
| FR-009-AC-2 | The set contains exactly the guidance section IDs in the master specification's guidance table, including `VII.C.1`, `VII.C.2`, and `VII.C.3`. | Test |
| FR-009-AC-3 | Every clause is recommended and names at least one output declared with the catalog definition. | Test |
| FR-009-AC-4 | The section VII.C clauses bind for `cyber_device=yes`, are not binding for `no`, and remain unresolved when the value is absent; general recommendation clauses remain applicable. | Test |
| FR-009-AC-5 | No set text or metadata names or paraphrases a paywalled consensus standard; the source-rights analysis records only the public FDA citation and rights basis. | Analysis |
| FR-009-AC-6 | `V.A.4` and `VII.C.3` reference `sbom`, whose output definition includes per-component support status and end-of-support dates. | Test |

## Dependencies

- Extends [FR-003](./FR-003-part-11-clause-set.md) set identity, rights, and source conventions.
- Extends [FR-004](./FR-004-applicability.md) user-supplied applicability dimensions.
- Uses the existing `clause-set-v1` model and `quire clauses evaluate` contract.

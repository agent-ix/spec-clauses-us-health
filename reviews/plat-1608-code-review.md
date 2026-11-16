---
id: SR-20261104139908
title: Code review - PLAT-1608 M3 discharge specification
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; PR #27; FR-020 and spec/tests.md"
review_set: subset
---

## Summary

FR-020 and TC-083 cover the planned M3 behavior, but two generic RMM contracts are duplicated from FR-019 and the SBOM-only condition is not tested negatively. Verdict: FAIL.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | FR-020-AC-5 duplicates the shared resolver contract in FR-019-AC-4. | FR-020-AC-5, FR-019-AC-4 |
| FND-002 | high | FR-020-AC-6 repeats the shared deterministic-rendering contract in FR-019-AC-5. | FR-020-AC-6, FR-019-AC-5 |
| FND-003 | medium | The SBOM-only compliance statement lacks a negative criterion. | FR-020 |

## Review coverage

Reviewed the complete diff: new FR-020 and TC-083/coverage additions in spec/tests.md. Compared all six PLAT-1608 ACs with FR-020-AC-1..6. The corrected Linear AC1 uses the current FR-009 key, us-fda/premarket-cybersecurity@2026-02-03. Reviewed FR-007..FR-011, FR-019, the cybersecurity output catalog, producer table, and clause set identities. Quire matrix reports FR-020-AC-1..6 untagged, consistent with TC-083 marked Planned. No applicable AssuranceProfile is present under spec/. No hashes, digests, pins, local tool paths, or copied artifacts were introduced.

## Findings data

~~~yaml
clean: false
scope:
  - {id: FR-020, path: spec/functional/FR-020-m3-cybersecurity-corpus-discharge.md, role: examined, excerpt: "When the reference corpus contains cybersecurity evidence, the pack SHALL render outcomes for the M3 section 524B and FDA cybersecurity guidance sets alongside the earlier sets. The RMM SHALL reflect recorded evidence, applicability, and the producer mapping defined in the master specification."}
  - {id: FR-020-AC-1, path: spec/functional/FR-020-m3-cybersecurity-corpus-discharge.md, role: examined, excerpt: "The M3 RMM lists us-congress/fdca-524b@2026-10-15 and us-fda/premarket-cybersecurity@2026-02-03 alongside the earlier sets in byte order, and each rowCount equals its corresponding clause matrix row count."}
  - {id: FR-020-AC-2, path: spec/functional/FR-020-m3-cybersecurity-corpus-discharge.md, role: examined, excerpt: "524B(b)(3) renders as Compliant with a discharge fact citing evidence produced from the ingested SBOM."}
  - {id: FR-020-AC-3, path: spec/functional/FR-020-m3-cybersecurity-corpus-discharge.md, role: examined, excerpt: "M3 clauses whose expected output has no producer on origin/main render as Not compliant - undischarged, and the open-clause list equals the no-producer rows authored by PLAT-1593 and recorded in the master specification."}
  - {id: FR-020-AC-4, path: spec/functional/FR-020-m3-cybersecurity-corpus-discharge.md, role: examined, excerpt: "With cyber_device=no, every section 524B clause renders as Not applicable."}
  - {id: FR-020-AC-5, path: spec/functional/FR-020-m3-cybersecurity-corpus-discharge.md, role: examined, excerpt: "Changing a discharge fact's evidence reference to a missing corpus file makes the pack-side evidence-reference resolver reject the fact and identify the affected clause."}
  - {id: FR-020-AC-6, path: spec/functional/FR-020-m3-cybersecurity-corpus-discharge.md, role: examined, excerpt: "Two runs over the same corpus inputs and context produce byte-identical Markdown."}
  - {id: TC-083, path: spec/tests.md, role: examined, excerpt: "M3 RMM includes the cybersecurity sets, ingested SBOM evidence, mapped open work, cyber-device applicability, pack-side missing-reference rejection naming the clause, and deterministic Markdown"}
findings:
  - fnd: FND-001
    severity: high
    confidence: high
    method: code-review
    check: other
    artifact_id: FR-020-AC-5
    related_ids: [FR-019-AC-4]
    path: spec/functional/FR-020-m3-cybersecurity-corpus-discharge.md
    lines: "55"
    excerpt: "FR-020-AC-5: Changing a discharge fact's evidence reference to a missing corpus file makes the pack-side evidence-reference resolver reject the fact and identify the affected clause."
    finding: "FR-020-AC-5 restates the generic resolver contract already owned by FR-019-AC-4, creating two normative owners for one shared behavior."
  - fnd: FND-002
    severity: high
    confidence: high
    method: code-review
    check: other
    artifact_id: FR-020-AC-6
    related_ids: [FR-019-AC-5]
    path: spec/functional/FR-020-m3-cybersecurity-corpus-discharge.md
    lines: "56"
    excerpt: "FR-020-AC-6: Two runs over the same corpus inputs and context produce byte-identical Markdown."
    finding: "FR-020-AC-6 repeats the generic deterministic-rendering contract from FR-019-AC-5, creating two normative owners for one shared behavior."
  - fnd: FND-003
    severity: medium
    confidence: high
    method: code-review
    check: soundness
    artifact_id: FR-020
    related_ids: [FR-020-AC-2]
    path: spec/functional/FR-020-m3-cybersecurity-corpus-discharge.md
    lines: "31-32"
    excerpt: "The 524B(b)(3) clause SHALL render as Compliant only when its discharge fact cites evidence produced from the ingested SBOM."
    finding: "The behavior says SBOM evidence is necessary for compliance, but the criterion checks only the positive SBOM-backed case. There is no failing evidence for the exclusive condition."
bindings: []
~~~

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | FR-020 now extends FR-019 and TC-083 traces the M3 integration case to the shared FR-019-AC-4 contract; FR-020 no longer restates it. |
| FND-002 | fixed | FR-020 now extends FR-019 and TC-083 traces the M3 integration case to the shared FR-019-AC-5 contract; FR-020 no longer restates it. |
| FND-003 | fixed | The behavior now requires an SBOM-backed fact without asserting exclusivity. |

~~~yaml
dispositions:
  - fnd: FND-001
    outcome: fixed
    after_excerpt: "Dependencies extend the shared evidence-reference and deterministic-rendering contracts in FR-019."
  - fnd: FND-002
    outcome: fixed
    after_excerpt: "Dependencies extend the shared evidence-reference and deterministic-rendering contracts in FR-019."
  - fnd: FND-003
    outcome: fixed
    after_excerpt: "The 524B(b)(3) clause SHALL have a discharge fact that cites evidence produced from the ingested SBOM."
~~~

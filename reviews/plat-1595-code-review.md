---
id: SR-013
title: Code review of PLAT-1595 FD&C Act 524B clause set
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; spec/tests.md, spec_clauses_us_health/manifest.yaml, spec_clauses_us_health/clauses/us-congress-fdca-524b-2026-10-15.json, tests/test_clause_sets.py, tests/test_part11_outputs.py; PR #8 at e8d3e0c"
review_set: subset
relationships:
  - {target: "ix://agent-ix/spec-clauses-us-health/FR-008", type: references}
  - {target: "ix://agent-ix/spec-clauses-us-health/FR-010", type: references}
  - {target: "ix://agent-ix/spec-clauses-us-health/FR-003", type: references}
  - {target: "ix://agent-ix/spec-clauses-us-health/FR-006", type: references}
---

## Summary

Reviewed PR #8 at `e8d3e0c` against PLAT-1595, FR-008, and FR-010. The new criteria have trace tags and the output-catalog checks use the existing specification table. CI currently fails because two existing Part 11 tests assume the module has one clause set. Statutory source and SBOM output mappings also have correctness defects.

## Verdict

**FAIL** — three high-severity findings remain.

## Scope

| Unit | Role | Result |
| --- | --- | --- |
| FR-008-AC-1 through FR-008-AC-5 | examined | New tests are present and tagged. The current-source and exact-ID claims conflict with the official statute for subsection (b)(4). |
| FR-010 behavior and FR-010-AC-1 through FR-010-AC-4 | examined | The new catalog consistency tests are tagged. The 524B SBOM clause is wired to `soup-list` rather than the dedicated `sbom` output. |
| FR-003-AC-3 and FR-006-AC-1 | examined | Existing Part 11 tests still destructure the full module's loaded sets as a single element; current CI fails in both tests. |
| PR checks | examined | CI run 43704408713 fails with two `ValueError: too many values to unpack` failures in `tests/test_part11_outputs.py`; the new `test_clause_sets.py` cases pass in that run. |
| Clause JSON source and applicability | examined | Version and official URL match the current US Code release point; `cyber_device` is supplied by the caller and missing/unknown values remain unresolved. |
| Computed matrix | examined | Every FR-008-AC-1..5 and FR-010-AC-1..2 criterion is tagged. No new trace gap was found. |

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | Adding the second set makes `load_clause_sets()` return two values, but both Part 11 output tests still use `(clause_set,) = load_clause_sets()`. CI fails in both tests with `ValueError`; select the Part 11 set by its key, as the updated tests in `test_clause_sets.py` do. | tests/test_part11_outputs.py:36,62 |
| FND-002 | high | The set identifies 21 U.S.C. § 360n-2(b)(4) as “reserved” and omits it, but the official US Code text effective through Public Law 119-124 (2026-10-15) contains an active requirement to comply with additional requirements imposed by regulation. The source statement and exact clause set are therefore incomplete and incorrect. | spec_clauses_us_health/clauses/us-congress-fdca-524b-2026-10-15.json:15; tests/test_clause_sets.py:307-328 |
| FND-003 | high | Clause `524B(b)(3)` is the statutory software bill of materials obligation but its `expectedOutputs` names `soup-list`; the dedicated `sbom` output is instead assigned to `524B(b)(1)`. This contradicts FR-010's dedicated SBOM requirement and fails to bind the SBOM obligation to the output that carries component support status and end-of-support dates. | spec_clauses_us_health/clauses/us-congress-fdca-524b-2026-10-15.json:83-87,161-174 |

## Coverage

The official source checked was [21 U.S.C. § 360n-2](https://uscode.house.gov/us/usc/119-124/t21/s360n-2/), whose page states that the text is effective through Public Law 119-124 (October 15, 2026). `quire validate` passed with the ISO and process modules; it emitted one pre-existing vague-response advisory in FR-009.

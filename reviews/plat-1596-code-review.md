---
id: SR-016
title: "Code review — FDA premarket cybersecurity clause set"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; spec/functional/FR-009-fda-premarket-cybersecurity-guidance-clause-set.md, spec/functional/FR-010-cybersecurity-output-catalog.md, spec_clauses_us_health/clauses/us-fda-premarket-cybersecurity-2026-02-03.json, tests/test_clause_sets.py"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-009"
    type: reviews
  - target: "ix://agent-ix/spec-clauses-us-health/FR-010"
    type: reviews
---

## Summary

Reviewed PLAT-1596 PR #9 at `90b8028` for Python test quality, clause-data faithfulness, source accuracy, licensing, and acceptance-criterion coverage. Found three high-severity defects and one medium trace defect: the V.A.5 clause is misattributed against the current FDA guidance, a new test helper duplicates an existing generic helper, shared output definitions are repeated in the new set, and an automated test is tagged to Analysis-only criteria.

## Verdict

**FAIL** — the new clause set misstates the current FDA section V.A.5 and violates the repository review rule against duplicating existing behavior and definitions.

## Scope

- Examined FR-009-AC-1 through FR-009-AC-6, FR-010-AC-2 and FR-010-AC-4, and NFR-001-AC-4.
- Examined the current FDA guidance PDF issued 2026-02-03, including its table of contents and Sections V.A.4–V.A.5.
- Compared the new evaluator test helper with `tests/conftest.py::evaluate_clause_set`. Compared output-catalog entries with `spec/spec.md:375-381` and `spec_clauses_us_health/clauses/us-congress-fdca-524b-2026-10-15.json:39-53`.
- Compared output-catalog entries with the existing 524B clause set and the master output catalog.
- No applicable AssuranceProfile exists under `spec/`.
- The tests use the actual Quire engine CLI; the coder reported `38 passed`, Ruff and Black passed, `quire publish-check` passed, and spec validation exited 0. GitHub checks were still running at review time.

## Findings

| ID | Severity | Summary | Refs | Escape Cause |
| --- | --- | --- | --- | --- |
| FND-001 | high | V.A.5 is implemented as a known-vulnerability assessment, but the current [FDA guidance issued 2026-02-03](https://www.fda.gov/media/119933/download) assigns V.A.5 to assessment of unresolved anomalies; known vulnerabilities are covered under V.A.4. This misattributes the recommendation and leaves the anomaly assessment absent while the test derives its expected ID from the same incorrect local table. | spec_clauses_us_health/clauses/us-fda-premarket-cybersecurity-2026-02-03.json:91-99 | wrong-requirement |
| FND-002 | high | `_fda_guidance_evaluate` duplicates the existing generic `evaluate_clause_set` helper imported from `tests/conftest.py`; use the existing helper with `FDA_GUIDANCE_KEY`. | tests/test_clause_sets.py:97-112 | implementation-bug-despite-evidence |
| FND-003 | high | The new clause set repeats output-catalog definitions already owned by the master catalog and present in the 524B set, including `sbom`, `vulnerability-assessment`, and `vulnerability-management-plan`; these duplicate statements can drift. | spec_clauses_us_health/clauses/us-fda-premarket-cybersecurity-2026-02-03.json:26-55 | implementation-bug-despite-evidence |
| FND-004 | medium | TC-041 is tagged to FR-009-AC-5 and NFR-001-AC-4 even though both criteria specify Analysis verification; the matrix correctly classifies them as method-without-symbol, so the test tag does not verify either analysis. | tests/test_clause_sets.py:542-558 | correct-requirement-no-evidence |

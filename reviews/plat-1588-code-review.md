---
id: SR-028
title: "Code review — PLAT-1588 M2 discharge"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; PR #24 at b76147b3dc534d867454a2a1598ee7202d4b4e4b; M2 discharge test, CI release CLI setup, and test matrix"
review_set: subset
relationships:
  - { target: "ix://agent-ix/spec-clauses-us-health/FR-007", type: references }
  - { target: "ix://agent-ix/spec-clauses-us-health/FR-018", type: references }
---

## Summary

The focused test passes and the CI setup downloads the official Engineering Assurance v0.10.1 release asset without committing a binary or checksum pin. The PR does not fully verify PLAT-1588 AC2–4: the mapping comparison is hardcoded rather than read from PLAT-1575, only one of three enhanced-only clauses is checked, and the missing-reference assertion is a local Python check rather than a failed Quoin discharge.

## Verdict

**FAIL** at `b76147b3dc534d867454a2a1598ee7202d4b4e4b`; fix the three acceptance-test gaps before merge.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | AC2 does not compare either discharge list with PLAT-1575's mapping table. | tests/test_m2_discharge.py:377-398 |
| FND-002 | medium | AC3 checks only VI.F.enhanced, omitting the other enhanced-only rows. | tests/test_m2_discharge.py:418-425 |
| FND-003 | medium | AC4's missing-reference check raises a Python assertion without invoking the Quoin reference-resolution path. | tests/test_m2_discharge.py:427-436 |

## Review Coverage

- Inspected `.github/workflows/ci.yml`, `spec/tests.md`, and `tests/test_m2_discharge.py` against PLAT-1588 AC1–5, PLAT-1575 AC4, FR-007, FR-016, FR-018, and neighboring Part 11 discharge tests.
- Confirmed the release URL is the public Engineering Assurance v0.10.1 GitHub release asset. The CI workflow installs it directly in PATH; no executable is tracked and no checksum is pinned.
- Confirmed Quoin's computed matrix marks the test function as a binder for FR-007-AC-2 and FR-007-AC-3. Those tags match the generated signed commit/tag, temporary signing key, and temporary evidence store behavior.
- Re-ran the focused test through `/home/peter/dev/worktrees/locked-build.sh`: 1 passed.
- Ran the repository spec validation. It reports the pre-existing unknown `TestMatrix` type in `spec/tests.md` and the existing FR-009 vague-response advisory; the current Quire module does not register `TestMatrix`.
- No production code changed, so Quoin gap-analysis was not applicable. No requirement statements changed, so spec sub-analyses were not applicable.

## Findings data

```yaml
findings:
  - fnd: FND-001
    severity: medium
    confidence: high
    method: code-review
    check: coverage
    artifact_id: PLAT-1588-AC-2
    related_ids: [PLAT-1575-AC-4]
    path: tests/test_m2_discharge.py
    lines: "377-398"
    excerpt: "Every element with a corpus artifact shows `Compliant`. Every element without one shows `Not compliant - undischarged`. Both lists equal PLAT-1575's mapping table."
    finding: "The test hardcodes five compliant clause IDs and treats every other applicable row as undischarged, but it never reads or compares PLAT-1575's mapping table. A change to that mapping can therefore leave this AC passing while the RMM lists are wrong."
  - fnd: FND-002
    severity: medium
    confidence: high
    method: code-review
    check: coverage
    artifact_id: PLAT-1588-AC-3
    related_ids: [FR-016-AC-3]
    path: tests/test_m2_discharge.py
    lines: "418-425"
    excerpt: "With `documentation_level=basic`, the enhanced-only clauses show `Not applicable`."
    finding: "The basic-context run checks only `VI.F.enhanced`. FR-016-AC-3 and the clause table also identify `VI.G.enhanced` and `VI.H.enhanced`, so regressions in either row would not fail this test."
  - fnd: FND-003
    severity: medium
    confidence: high
    method: code-review
    check: test-intent
    artifact_id: PLAT-1588-AC-4
    related_ids: []
    path: tests/test_m2_discharge.py
    lines: "427-436"
    excerpt: "Changing one fact's evidence ref to a missing file fails the ref-resolution check, naming the clause."
    finding: "This block checks that a manually constructed project path is missing and raises a Python `AssertionError`; it does not mutate a fact and run `quoin discharge`. It therefore cannot establish that Quoin's ref-resolution check rejects the missing fact reference or names the clause."
bindings:
  - {test_id: TC-082, ac_id: FR-007-AC-2, trace: correct}
  - {test_id: TC-082, ac_id: FR-007-AC-3, trace: correct}
```

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-004 | high | `_m2_mapping_rows` duplicates the existing `_mapping_rows` parser. | tests/test_m2_discharge.py:198-217; tests/test_premarket_outputs.py:142-169 |
| FND-005 | high | `_resolve_fact_refs` duplicates the existing Part 11 reference resolver. | tests/test_m2_discharge.py:299-314; tests/test_part11_discharge.py:71-88 |

## Dispositions

| FND | outcome | reason |
|---|---|---|
| FND-001 | fixed | The test derives compliant and open clause lists from `_expected_m2_lists()`, which reads the PLAT-1575 mapping table. |
| FND-002 | fixed | The basic-context test now asserts `VI.F.enhanced`, `VI.G.enhanced`, and `VI.H.enhanced` are not applicable. |
| FND-003 | fixed | The test mutates the recorded `820.10(c)` fact, runs `quoin discharge`, and passes the modified facts to the established pack reference resolver, which raises an error naming `820.10(c)`. |
| FND-004 | still-open | `tests/test_premarket_outputs.py::_mapping_rows` already implements this table parser; reusing one shared implementation is required by the no-duplication review rule. |
| FND-005 | still-open | `tests/test_part11_discharge.py::_resolve_fact_refs` already implements this resolver; reusing one shared implementation is required by the no-duplication review rule. |
| FND-001 | fixed | The expected compliant/open lists are now derived from the shared PLAT-1575 mapping parser and asserted against the M2 RMM rows. |
| FND-002 | fixed | The basic-context test asserts `VI.F.enhanced`, `VI.G.enhanced`, and `VI.H.enhanced` are not applicable. |
| FND-003 | fixed | The test mutates `820.10(c)`, runs Quoin discharge, and checks the mutated fact with the shared pack reference resolver. |
| FND-004 | fixed | Both output tests now import the one `m2_mapping_rows` helper from `tests/conftest.py`. |
| FND-005 | fixed | Both discharge tests now import the one `resolve_fact_refs` helper from `tests/conftest.py`. |

```yaml
- fnd: FND-004
  outcome: still-open
  reason: "The new _m2_mapping_rows duplicates tests/test_premarket_outputs.py::_mapping_rows; the shared parser should have one home."
- fnd: FND-005
  outcome: still-open
  reason: "The new _resolve_fact_refs duplicates tests/test_part11_discharge.py::_resolve_fact_refs; the resolver should have one home."
- fnd: FND-001
  outcome: fixed
  after_excerpt: |-
    expected_compliant, expected_open = _expected_m2_lists()
    assert {clause_id for clause_id, row in m2_rows.items() if row["compliance"] == "compliant"} == expected_compliant
    assert {clause_id for clause_id, row in m2_rows.items() if row["compliance"] == "undischarged"} == expected_open
- fnd: FND-002
  outcome: fixed
  after_excerpt: |-
    for clause_id in ["VI.F.enhanced", "VI.G.enhanced", "VI.H.enhanced"]:
        assert basic_rows[clause_id]["applicability"] == "not_applicable"
- fnd: FND-003
  outcome: fixed
  after_excerpt: |-
    facts[0]["evidenceRefs"][-1] = "evidence://example.invalid/evidence/missing.json"
    facts_path.write_text(json.dumps(facts))
    changed_report = run(*args)
    with pytest.raises(AssertionError, match=r"820\.10\(c\): evidence ref does not resolve"):
        _resolve_fact_refs(project, facts)
```


```yaml
dispositions:
  - fnd: FND-001
    outcome: fixed
    after_excerpt: |-
      expected_compliant, expected_open = _expected_m2_lists()
      assert {clause_id for clause_id, row in m2_rows.items() if row["compliance"] == "compliant"} == expected_compliant
      assert {clause_id for clause_id, row in m2_rows.items() if row["compliance"] == "undischarged"} == expected_open
  - fnd: FND-002
    outcome: fixed
    after_excerpt: |-
      for clause_id in ["VI.F.enhanced", "VI.G.enhanced", "VI.H.enhanced"]:
          assert basic_rows[clause_id]["applicability"] == "not_applicable"
  - fnd: FND-003
    outcome: fixed
    after_excerpt: |-
      changed_report = run(*args)
      with pytest.raises(AssertionError, match=r"820\.10\(c\): evidence ref does not resolve"):
          resolve_fact_refs(project, facts)
  - fnd: FND-004
    outcome: fixed
    after_excerpt: |-
      from conftest import m2_mapping_rows
      rows = m2_mapping_rows()
  - fnd: FND-005
    outcome: fixed
    after_excerpt: |-
      from conftest import resolve_fact_refs
      resolve_fact_refs(project, facts)
```

## Disposition pass 2 result

**PASS** for SR-028 at `bf04ca0cc6e52e589fb1d05192eae383995d2db2`. All five findings are fixed. The focused related suites passed (6 tests).

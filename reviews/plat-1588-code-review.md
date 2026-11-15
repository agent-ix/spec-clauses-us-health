
| FND | Severity | Check | Summary |
| --- | --- | --- | --- |
| FND-001 | medium | coverage | AC2 does not compare either discharge list with PLAT-1575's mapping table. |
| FND-002 | medium | coverage | AC3 checks only VI.F.enhanced, omitting the other enhanced-only rows. |
| FND-003 | medium | test-intent | AC4's missing-reference check is a local Python assertion, not a failed Quoin discharge. |

+++ [reviewer data]

```yaml
clean: false
scope:
  - {id: PLAT-1588-AC-1, path: "Linear PLAT-1588; tests/test_m2_discharge.py", role: examined, excerpt: "Its index lists the three ordered sets, and each rowCount equals that matrix's row count."}
  - {id: PLAT-1588-AC-2, path: "Linear PLAT-1588; tests/test_m2_discharge.py", role: examined, excerpt: "Every element with a corpus artifact shows Compliant. Every element without one shows Not compliant - undischarged. Both lists equal PLAT-1575's mapping table."}
  - {id: PLAT-1588-AC-3, path: "Linear PLAT-1588; tests/test_m2_discharge.py", role: examined, excerpt: "With documentation_level=basic, the enhanced-only clauses show Not applicable."}
  - {id: PLAT-1588-AC-4, path: "Linear PLAT-1588; tests/test_m2_discharge.py", role: examined, excerpt: "Changing one fact's evidence ref to a missing file fails the ref-resolution check, naming the clause."}
  - {id: PLAT-1588-AC-5, path: "Linear PLAT-1588; tests/test_m2_discharge.py", role: examined, excerpt: "Two runs over the same inputs give byte-identical Markdown."}
  - {id: PLAT-1575-AC-4, path: "Linear PLAT-1575", role: context_only, excerpt: "On the corpus (PLAT-1588), each element whose producer exists has a direct fact citing a corpus artifact. Each element without one shows Not compliant - undischarged in the RMM. The test asserts both lists against the mapping table."}
  - {id: FR-007-AC-2, path: "spec/functional/FR-007-reference-corpus.md", role: examined, excerpt: "A discharge integration test creates a fixture signing key in a temporary directory, successfully verifies a signed commit and signed tag made with that key, and removes the key when the test completes."}
  - {id: FR-007-AC-3, path: "spec/functional/FR-007-reference-corpus.md", role: examined, excerpt: "A discharge integration test records its facts in a temporary evidence store and removes that store when the test completes."}
  - {id: FR-016-AC-3, path: "spec/functional/FR-016-m2-applicability.md", role: examined, excerpt: "With documentation_level=basic, every baseline Section VI clause is binding and VI.F.enhanced, VI.G.enhanced, and VI.H.enhanced are not_binding."}
  - {id: FR-018, path: "spec/functional/FR-018-m2-output-producer-mapping.md", role: context_only, excerpt: "The M2 premarket guidance and Part 820 sets SHALL identify what produces each expected output or identify the owner of an output that has no toolchain producer."}
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
    excerpt: "With documentation_level=basic, the enhanced-only clauses show Not applicable."
    finding: "The basic-context run checks only VI.F.enhanced. FR-016-AC-3 and the clause table also identify VI.G.enhanced and VI.H.enhanced, so regressions in either row would not fail this test."
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
    finding: "This block checks that a manually constructed project path is missing and raises a Python AssertionError; it does not mutate a fact and run quoin discharge. It therefore cannot establish that Quoin's ref-resolution check rejects the missing fact reference or names the clause."
bindings:
  - {test_id: TC-082, ac_id: FR-007-AC-2, trace: correct}
  - {test_id: TC-082, ac_id: FR-007-AC-3, trace: correct}
```

+++


---
id: SR-20261104139937
title: "Code review of PLAT-1831 spec-clauses-us-health PR #37"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; package.json, package-lock.json, tests/test_part11_discharge.py, tests/test_m2_discharge.py, tests/test_m3_discharge.py, tests/test_m4_discharge.py"
review_set: subset
---

## Summary

Ticket: PLAT-1831. Reviewed `git diff origin/main...HEAD` at 57ebf933 (spec-clauses-us-health PR #37). The PR deletes the four-line `quoin --version` / `== "0.35.0"` block from four discharge tests. It also moves devDependencies to `@agent-ix/quoin` 0.36.10 and `@agent-ix/quire-cli` 0.52.1, with a regenerated `package-lock.json`.

## Verdict

**APPROVE.** No defects.

- Versions: `npm view` against registry.npmjs.org reports quoin 0.36.10 and quire-cli 0.52.1 as the current releases.
- Lockfile: every `resolved` URL in the file is `https://registry.npmjs.org/`, with no npm.ix or other private host. The diff changes only the two packages, their four platform optionals each, versions, and integrity hashes. No other entries change.
- Removed block: it guarded only an exact version string, which is ceremony. Each test still calls `engine_tool("quoin")`, which runs `pytest.fail` when the CLI is missing. Each test also asserts `returncode == 0` on its first real quoin call (`module install`), so a missing or broken quoin still fails loudly. No spec FR or AC in FR-006, FR-007 or FR-019 to FR-021 requires a pinned toolchain version.
- Style: ruff and black pass on the four touched files.

## Verification

- A scratch clone at 57ebf933 ran `npm ci` with npmjs-only flags. It resolved quoin 0.36.10 and quire 0.52.1 (engine 0.62.2), with `node_modules/.bin` first on PATH and engineering-assurance 0.10.1. Running `pytest tests/test_part11_discharge.py tests/test_m2_discharge.py tests/test_m3_discharge.py tests/test_m4_discharge.py tests/test_part11_outputs.py` gave 8 passed.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |

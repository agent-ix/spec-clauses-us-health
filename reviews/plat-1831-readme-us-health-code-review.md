---
id: SR-20261104139942
title: "Code review of PLAT-1831 spec-clauses-us-health PR #40 (adopter README)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; README.md"
review_set: subset
---

## Summary

Ticket: PLAT-1831. Reviewed `git diff origin/main...HEAD` at 99b7d9ed (spec-clauses-us-health PR #40), in a scratch clone. The PR rewrites README.md only, for adopters: pack contents, install, a four-step workflow, an end-to-end example, one table per clause set ("Tool produces", "You supply", "Limits"), what the tool does not do, and known limits.

## Verdict

**REQUEST CHANGES.** Two medium accuracy defects in adopter-facing text and three low ones. All five are prose fixes.

What holds up:

- Accuracy of the per-set tables. I checked 22 rows and context lines against the clause JSON output catalogs on main. Every one matches: Part 11 (11.10, 11.30, 11.50/11.70, 11.100, 11.200/11.300, and the context line), Part 820 (820.10, 820.35, 820.45, context), 524B (row and context), premarket cybersecurity (V.A to V.C, VI.B, VII.C), device software (VI.A to VI.J, context), and HIPAA (164.308, 164.310, 164.312, 164.314/164.316, context).
- Commands. Every named command exists with the stated behaviour in quoin 0.36.10 / quire 0.52.1: `quoin release snapshot`, `quoin risk-summary`, `quoin soup report`, `quoin anomaly report`, `quoin evidence record` (`--adapter sbom`), `quoin dossier generate --doc threat-model`, `quoin matrix`, `quire matrix`, `quire relations --flow` and `--health-data-flows`, `quire clauses evaluate`, `quoin evidence record-discharge`, and `quoin discharge --rmm --pack`. `--adapter osv-scanner` is missing from the 0.36.10 `--help` enum, but the adapter registry on quoin v0.36.10 lists it (`rust/crates/quoin-evidence/src/adapters/registry.rs`), so the README claim stands. The stale help text is quoin's defect, not this PR's. The engineering-assurance names `approval-trail`, `signature-verify`, `approval-verify` and `producer-execute` all exist on its main.
- End-to-end example. I ran it with the repo's own toolchain (`npm ci` from npmjs only: quoin 0.36.10, quire 0.52.1, engine 0.62.2), in a throwaway HOME at an absolute scratch path and an empty git repo. The git install exits 0 and lands at `$HOME/.ix/filament/modules/spec_clauses_us_health`, as the example's `M=` says. Evaluate, record-discharge and discharge all exit 0. The rows shown match: 11.10(a) is `Compliant` with `evidence/matrix.json`, 11.10(b) is `Not compliant - undischarged: no discharge fact`, 11.30 is `Not applicable`, and all 524B rows are `Unresolved`.
- Known limit, **confirmed on 0.36.10**. The direct fact's `evidenceRefs: ["evidence/matrix.json"]` names a file that does not exist in the repo, and the RMM still reports 11.10(a) `Compliant`. The README's "evidence checks are shallow" limit is accurate.
- Hard rules. No paywalled text: all six sources are public US law or guidance, and the npm package is confirmed absent from npmjs (E404). The npm install form is marked "once the package is published". No tool-assigned scores, classes or acceptability. No roadmap or delivery order. No internal paths, SHAs or toolchain version pins in prose: `--version 2026-11-12` is the required clause-set version argument.
- Usefulness: clear, well scoped, not padded. The tables tell an adopter exactly what they must bring.

## Verification

- Scratch clone at 99b7d9ed; `npm ci --registry https://registry.npmjs.org/ --@agent-ix:registry=https://registry.npmjs.org/ --userconfig /dev/null`; `quoin --version` 0.36.10.
- Throwaway HOME: `quoin module install github:agent-ix/spec-clauses-us-health//spec_clauses_us_health`, then the README example verbatim. Extra probes: rendering with `--as-of 2028-01-01T00:00:00Z` gives `Not compliant - attestation not current: discharge fact is expired`. A disposition fact without `attestation` is rejected with `attestation must be an object`. A `delegated` disposition with an attestation renders `Tailored`.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The clause-state legend does not match what the RMM prints. "Compliant" also needs an attestation that is current at `--as-of`; an expired one prints `Not compliant - attestation not current`. "Undischarged" is printed as `Not compliant - undischarged: no discharge fact`. `Undetermined` (Unresolved) and `Not applicable` are missing. The tool literally prints "Not compliant", so name it and say it means "nothing current recorded", not a finding of non-compliance. | README.md:184-189 |
| FND-002 | medium | Step 3's disposition description would produce facts that `record-discharge` rejects. The field is `decision`; every disposition also needs an `attestation` (rejected without one: `attestation must be an object`), and `temporary_exception` also needs `decisionExpiresAt`, which must not be later than the attestation's `expiresAt`. Add these, ideally with a one-fact disposition example. | README.md:58-61 |
| FND-003 | low | The crosswalk sentence is incomplete. The device-software set carries 20 informative crosswalks to Part 820, and the HIPAA set carries 274 CPRT crosswalks to NIST SP 800-53. Neither is a cybersecurity-set-to-cybersecurity-set link. | README.md:31-33 |
| FND-004 | low | The "trimmed output" block drops the table's separator row and the two Tailoring columns, and unescapes the ids. The real output is `11.10\(a\)` under a pack index. An adopter grepping for `11.10(a)` finds nothing. Show the real header and separator rows, or say the columns and escapes were trimmed. | README.md:95-102 |
| FND-005 | low | The premarket-cybersecurity "Context: `cyber_device`" line reads as if the whole set is gated. Only VII.C.1 to VII.C.3 depend on it; V.A.1 to VI.B always apply. The same applies to HIPAA (line 168): `hipaa_role` gates only 164.314(a)(2)(ii) and (iii). | README.md:149 |

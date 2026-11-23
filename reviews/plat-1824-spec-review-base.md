---
id: SR-20261104139930
title: "Spec review of PLAT-1824 PR #34"
type: SpecReview
analysis: base
scope: "agent-ix/spec-clauses-us-health; spec/spec.md, spec/functional/FR-005-pack-wide-output-catalog.md, spec/functional/FR-012-hipaa-security-rule-clause-set.md, spec/functional/FR-021-m4-corpus-discharge.md"
review_set: subset
---

## Summary

Ticket: PLAT-1824. The split is honest: the repository outputs `access-control` and `audit-trail` stay in the pack catalog for Part 11, and HIPAA moves to the product-side `ephi-access-control` and `audit-logging`. `ephi-access-control` already names the spec-objects-security `role`, `permission`, `auth_flow`, `mfa_method` and `session_config` objects (all present on spec-objects-security origin/main) as its form, consistent with `audit-logging` naming `security.audit_event` and `security-controls` stating no producer; no repository output honestly applies to a Security Rule safeguard, so dropping it from HIPAA is correct. The stale PLAT-1756 note is gone and `quire relations --health-data-flows` exists. `quire validate` passes on the four changed spec files.

## Verdict

**CHANGES REQUESTED** — FND-001 is a normative contradiction introduced by this PR.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | Prose says § 164.312(a)(2)(iv) uses `security-controls` and `written-procedure`; the table and JSON give it `security-controls` only. Reword: § 164.310(a)(2)(iii) uses `security-controls` and `written-procedure`; § 164.312(a)(2)(iv) uses `security-controls`. | spec/spec.md:341-343 |
| FND-002 | medium | FR-005-AC-1 pins "exactly the 39 names"; a count in an AC is ceremony. Say "exactly the names listed in `spec/spec.md`". | spec/functional/FR-005-pack-wide-output-catalog.md:28 |
| FND-003 | low | FR-012 statement requires `ephi-access-control` for "access and authentication clauses" without saying which; § 164.312(a)(2)(iv) sits under the access-control standard yet does not get it, and AC-7 names only three of the eight clauses that do. Reference the table (or list the clauses) in the statement. | spec/functional/FR-012-hipaa-security-rule-clause-set.md:44-48 |
| FND-004 | low | The `ephi-access-control` description names objects as "`spec-objects-security` `role`, ..." while sibling outputs and the corpus use `security.role`-style names. Use `security.role`, `security.permission`, `security.auth_flow`, `security.mfa_method`, `security.session_config`. | spec/spec.md:523 |
| FND-005 | low | Ticket narration remains in public spec prose in the paragraph this PR rewrote ("authored in PLAT-1613 and PLAT-1616") and in FR-012 Dependencies (PLAT-1613/1616/1621). Delete those sentences. | spec/spec.md:347-348; spec/functional/FR-012-hipaa-security-rule-clause-set.md:74-75 |
| FND-006 | low | Audit gap: § 164.308(a)(3)(ii)(C) termination procedures and § 164.308(a)(5)(ii)(D) password management govern ePHI access but map to `security-controls`/`written-procedure` only; spec-objects-security has `password_policy`. Consider adding `ephi-access-control` (and `password_policy` to its description). | spec/spec.md:281, 290 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Verified at 7871610. After excerpt: "Physical-access clause § 164.310(a)(2)(iii) uses `security-controls` and `written-procedure`, and encryption clause § 164.312(a)(2)(iv) uses `security-controls` only" |
| FND-002 | fixed | Verified at 7871610. After excerpt: "A catalog test finds exactly the names listed in `spec/spec.md`" |
| FND-003 | fixed | Verified at 7871610; statement binds to the table and AC-7 lists all eleven clauses, asserted as an exact set. After excerpt: "SHALL list `ephi-access-control` for exactly the clauses in the normative table that show it" |
| FND-004 | fixed | Verified at 7871610 in spec, JSON and test. After excerpt: "`security.role`, `security.permission`, `security.auth_flow`, `security.mfa_method`, `security.password_policy` and `security.session_config`" |
| FND-005 | fixed | Verified at 7871610; PLAT-1613/1616/1621 sentences removed from spec.md and FR-012. After excerpt: "The table specifies the required clause and output design." |
| FND-006 | fixed | Verified at 7871610; both clauses now list `ephi-access-control` in table and JSON, and `security.password_policy` (present in spec-objects-security origin/main) is named. After excerpt: "| `164.308(a)(5)(ii)(D)` | ... | `ephi-access-control`, `security-controls`, `written-procedure` |" |

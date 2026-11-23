---
id: SR-20261104139944
title: "Code review of PLAT-1831 spec-clauses-us-health PR #41 (README follow-up)"
type: SpecReview
analysis: code-review
scope: "agent-ix/spec-clauses-us-health; README.md"
review_set: subset
---

## Summary

Ticket: PLAT-1831. Reviewed `git diff origin/main...HEAD` at fb8d90d2 (spec-clauses-us-health PR #41), in a scratch clone. The diff adds 15 lines to README.md. The first block explains that the engineering-assurance CLI is a native binary outside the npm toolchain and installs it with `cargo install --git ... --locked --features full --bin engineering-assurance`. The second is a paragraph saying authored records are schema-checked by `quire validate`, and that "Nothing" under "Tool produces" means no command writes a report for that clause.

## Verdict

**REQUEST CHANGES.** One medium and two low findings, all prose.

What holds up:

- `--features full` is required. The engineering-assurance `Cargo.toml` on main declares the `engineering-assurance` `[[bin]]` with `required-features = ["full"]`, and its own README says a build without it installs nothing. The cargo command matches the engineering-assurance README verbatim.
- The commands the README attributes to engineering-assurance exist as subcommands of the v0.10.1 release binary (`--help`): `approval-trail`, `approval-verify`, `signature-verify` and `producer-execute`.
- `quire validate` checks records against their record-type schema and does not judge their content. That sentence is accurate.
- Hard rules hold. The block pins no version, cites no internal path, and adds no roadmap or compliance verdict.

## Verification

- `gh release list -R agent-ix/engineering-assurance`: v0.10.1 is Latest (2026-11-15), and its one asset is named `engineering-assurance`. I downloaded it; `file` reports an x86-64 Linux ELF, and `--version` prints `engineering-assurance 0.10.1`. This repo's `.github/workflows/ci.yml` (lines 25-28) curls that same asset. The engineering-assurance repo is public.
- Compared with the EU pack's open README PR (spec-clauses-eu-law #27, which the PR says it aligns with). The EU paragraph has an extra sentence that ties "data-flow" to `quoin dossier generate` and "baseline" to `engineering-assurance release-verify`. This PR dropped that sentence and kept the list.
- Checked the five "Nothing" rows against the clause catalogs on main: 820.35, VI.B, 164.308, 164.310 and 164.314/164.316.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The README offers only `cargo install --git`. That is a full Rust build of unreleased `main`, not a release. engineering-assurance publishes a prebuilt Linux x86-64 binary on every release (v0.10.1 is Latest), and this repo's own CI installs that binary. Offer it first, without a version pin, for example `gh release download -R agent-ix/engineering-assurance -p engineering-assurance` (latest release), then `chmod +x`. Keep cargo as the route for other platforms. | README.md:53-60 |
| FND-002 | low | "It does not mean nothing checks your records" is wrong for three of the five "Nothing" rows. 820.35 (complaint, service and device-identification records), VI.B (vulnerability-management plan) and 164.314/164.316 (written procedures) have no shipped record type, so nothing checks them. Only the HIPAA `security.control` records under 164.308 and 164.310 are schema-checked. Say which rows have checked record types, and that documents and procedures are not checked by anything. | README.md:149-150 |
| FND-003 | low | The record-type list names "baseline records", which no US clause set uses and the README never mentions again. The EU sentence that explained it (Baseline read by `engineering-assurance release-verify`) was dropped. The list also omits record types the US tables rely on: `soup_record` for `quoin soup report`, Anomaly documents for `quoin anomaly report`, and the `security.control`, `audit_event` and access-control records for HIPAA. Drop "baseline", or restore its sentence, and name the record types the US rows use. | README.md:146-148 |

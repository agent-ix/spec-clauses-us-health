---
id: SR-20261104139936
title: "Spec review of PLAT-1826 PR #36"
type: SpecReview
analysis: base
scope: "agent-ix/spec-clauses-us-health; spec/functional/FR-018-m2-output-producer-mapping.md, spec/spec.md, spec/tests.md"
review_set: subset
---

## Summary

Ticket: PLAT-1826. Spec review, with integrity and EARS checks, of the FR-018 rewrite, the premarket VI table, the M2 output map, the US output catalog and TC-076. Context read: FR-014, FR-015 and FR-019, plus the review sources lane-E.md (FDA premarket coverage table) and the regulated-review "Dossier vs FDA premarket list" bullet. `quire validate` passes with one EARS warning (FND-002).

## Verdict

**CHANGES REQUESTED (minor).** The substance is right. The 2023 premarket guidance's § VI.A is the documentation-level evaluation: the sponsor states Basic or Enhanced and the rationale. Mapping VI.A to a customer `documentation-level-decision` document is the correct reading, and the old `risk-management-records` mapping duplicated VI.C. The text says the person decides, and no command assigns or infers the level, which matches the `documentation_level` dimension rule above the table. The seven no-producer Part 820 outputs are honestly customer-provided, and no owner-ticket row remains. All findings are low.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | The map preamble still says "A listed producer is a capability available on `origin/main`", while FR-018 and TC-076 now define producers as installed commands, modules and registered dossier kinds. The two bases differ, and the repo's origin/main is not the toolchain's. Reword to "available in the installed toolchain". | spec/spec.md:466-467 |
| FND-002 | low | The new FR-018 Behavior bullets stack several SHALLs ("SHALL name ... Each named command SHALL exist, and each ... kind SHALL be", "SHALL be kind ..., SHALL be identified ..., and SHALL NOT imply"). `quire validate` now reports `ears:non-singular` at line 31; origin/main's FR-018 had no EARS warning. Split them into one SHALL per bullet. | spec/functional/FR-018-m2-output-producer-mapping.md:27-33 |
| FND-003 | low | FR-018-AC-2 is compound and names a third class ("an authored `record` naming its module") that neither the map nor TC-076 separates from produced records. The Behavior rule that each named dossier kind is registered has no AC clause, although TC-076 tests it. Drop the authored-record class, or define it, and add the dossier-kind clause to the AC. | spec/functional/FR-018-m2-output-producer-mapping.md:45 |
| FND-004 | low | Ticket narration remains in normative M2 prose next to the edited text: "required by PLAT-1569", "IDs for PLAT-1572 and PLAT-1582", and "Clause content is authored in PLAT-1569/PLAT-1572". The PR removes the same pattern ("PLAT-1582 owns authored crosswalk rows", the PLAT-1762 dependency), but not these. Delete the ticket references. | spec/spec.md:414,447; spec/functional/FR-014-part-820-quality-management-system-clause-set.md:56; spec/functional/FR-015-fda-device-software-guidance-clause-set.md:53 |
| FND-005 | low | FR-018 ties the output `kind` to whether a producer exists ("An output that has no producer SHALL be kind `document` or `procedure`"). That rule retypes complaint, service, labeling-inspection, traceability, regulatory-report and advisory-notice records as `document`. Under the QMSR (ISO 13485 records versus documents) these are records. `kind` is descriptive only (quire checks only that it is non-empty), and the "no toolchain producer" text already carries the honesty. Consider letting a customer-provided output keep kind `record`. This is a judgment call; the M3 pack already types `additional-cybersecurity-requirement-records` as `document`. | spec/functional/FR-018-m2-output-producer-mapping.md:31-33; spec/spec.md:488-494 |

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-006 | low | After the lead's decision (seven Part 820 outputs are kind `record` again), the map preamble still says "An output with no producer is a customer-provided document." That is now false for the seven customer-provided records and the customer-owned procedure. Reword to "...is customer-provided or customer-owned". | spec/spec.md:468-469 |

## Dispositions

| FND | outcome | reason |
| --- | --- | --- |
| FND-001 | fixed | Verified at f76d2a43. The next sentence regressed (see FND-006). After excerpt: `A listed producer is a command or module artifact type in the installed toolchain; naming a capability does not assert that an instance exists in a customer's repository.` |
| FND-002 | fixed | Verified at f76d2a43: `quire validate` on FR-018 reports no EARS warning. After excerpt: `- Each command a mapping row names SHALL exist in the installed CLI, and each quoin dossier generate document kind it names SHALL be a kind the installed quoin registers.` |
| FND-003 | fixed | Verified at f76d2a43. AC-2 now has four named classes and no "authored record". The dossier-kind rule is its own FR-018-AC-4. Its missing trace tag is gap-analysis FND-002. After excerpt: `FR-018-AC-2 \| Each M2 output is in exactly one class: a produced record, a customer-provided record, a customer-provided document, or a customer-owned procedure; the last three state that no toolchain producer exists.` |
| FND-004 | fixed | Verified at f76d2a43. spec.md:414 and :447 are reworded, and the FR-014 and FR-015 ticket lines are deleted. After excerpt: `output, and incorporated-by-reference boundary required for the Part 820 set.` / `These are the complete Section VI clause identifiers and exact Part 820 target IDs.` |
| FND-005 | fixed | Lead decision applied and verified at f76d2a43. The seven Part 820 QMS outputs are kind `record` in the JSON, the map and the catalog. FR-018 says kind describes what the output is, not whether a tool produces it. The new `M2_CUSTOMER_RECORDS` class is tested, and it fails on the 33ddd519 data (measured). After excerpt: `"complaint-records": { "kind": "record", "description": "Customer-provided complaint intake, evaluation, investigation, and response records; no toolchain producer." }` |
| FND-006 | fixed | Verified at bd81fb4c. After excerpt: `An output with no producer is customer-provided or customer-owned. Its clause stays open until a customer supplies evidence.` |

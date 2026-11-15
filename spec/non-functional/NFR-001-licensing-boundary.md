---
id: NFR-001
title: Published pack content respects the licensing boundary
type: NFR
quality_attribute: compliance
---
# NFR-001: Published pack content respects the licensing boundary

## Statement

Every published file SHALL use original expression or identify only public
sources by title and citation. It SHALL NOT reproduce or paraphrase paywalled
standards, including any standard incorporated by reference in a regulation or
FDA guidance.

## Scope

Applies to source, spec, tests, examples, package resources, and generated
artifacts included in distributions or CI output.

## Rationale

Public law may be named and cited, but a regulation's incorporation by reference
does not grant distribution rights to the incorporated standard. The clause
text therefore remains original and concise.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|---|---|---|---|
| Prohibited standards-body designators in package source | 0 | Any hit fails | Deterministic scan |
| Rights scan fixture with an injected designator | Rejected with file and line | Any undetected fixture fails | Test |

## Verification

The publication-gate designator scan runs over the package and reports a
nonzero exit when a prohibited designator occurs. A fixture with an injected
designator must fail and identify its file and line.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-001-AC-1 | The package scan reports no prohibited standard-body designators in published files. | Test |
| NFR-001-AC-2 | An injected designator fixture fails and identifies the file and line. | Test |
| NFR-001-AC-3 | No authored file names or paraphrases a paywalled standard. | Inspection |

## Dependencies

- The publication-gate implementation is specified in PLAT-1549.

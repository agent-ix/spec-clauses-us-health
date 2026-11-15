---
id: NFR-001
title: Published pack content respects the licensing boundary
type: NFR
quality_attribute: compliance
---
# NFR-001: Published pack content respects the licensing boundary

## Statement

The pack SHALL publish original clause summaries backed by public sources only.

## Scope

Applies to source, spec, tests, examples, package resources, and generated
artifacts included in distributions or CI output.

## Rationale

Public law may be named and cited, but a regulation's incorporation by reference
does not grant distribution rights to the incorporated standard. The clause
text therefore remains original and concise. Analysis is used for
NFR-001-AC-3 because a property test would require scanning authored or
packaged prose and cannot determine semantic paraphrase reliably; the public
source's rights basis is recorded instead.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|---|---|---|---|
| Set rights metadata | Every published set declares original text and a public source basis | A set without both declarations fails publication check | Test |

## Verification

`quire publish-check` verifies the set's declared rights metadata. A source
analysis records the public citation and rights basis used for each authored
set. The metadata test checks structured rights fields only. We do not scan
package files or corpus fixtures. A string scan cannot determine whether prose
paraphrases protected expression and would inspect distribution files.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-001-AC-1 | Every published set declares `rights.text: original`, a non-blank public-source licence basis, and passes `quire publish-check`. | Test |
| NFR-001-AC-2 | The M1 source metadata names the eCFR Part 11 page, and each set's source metadata identifies a public legal or public FDA source. | Test |
| NFR-001-AC-3 | Clause summaries use original expression and do not reproduce or paraphrase a paywalled standard; the verification record cites only the public source and rights basis. | Analysis |

## Dependencies

- The publication-gate implementation is specified in PLAT-1549.

---
id: NFR-001
title: Published pack content respects the licensing boundary
type: NFR
quality_attribute: compliance
---
# NFR-001: Published pack content respects the licensing boundary

## Statement

The pack SHALL publish original clause summaries backed by public sources only,
and SHALL NOT reproduce or paraphrase paywalled consensus standards.

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
| Set rights metadata | Every published set declares original text and a non-blank public-source basis | The pack metadata test fails for a set without either declaration; Quire publish-check refuses restricted `rights.text` | Test |

## Verification

The pack metadata test checks structured rights fields only: each current set
declares `rights.text: original` and a non-blank `rights.licence` public-source
basis. `quire publish-check` independently refuses restricted `rights.text`.
A source analysis records the public citation and rights basis used for each
authored set. We do not scan package files or corpus fixtures. A string scan
cannot determine whether prose paraphrases protected expression and would
inspect distribution files.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-001-AC-1 | Every published set declares `rights.text: original`, a non-blank public-source licence basis, and passes `quire publish-check`. | Test |
| NFR-001-AC-2 | Every set's source metadata identifies its public legal or FDA source; Part 11 and the Part 820 set identify their eCFR pages, and each FDA guidance set identifies its official FDA guidance page. | Test |
| NFR-001-AC-3 | Clause summaries use original expression and do not reproduce or paraphrase a paywalled standard; the verification record cites only the public source and rights basis. | Analysis |
| NFR-001-AC-4 | The 524B and FDA cybersecurity guidance sets contain no name, number, or paraphrase of a paywalled consensus standard referenced by the guidance. | Analysis |
| NFR-001-AC-5 | The Part 820 set contains no paraphrase of an incorporated requirement; the clause table identifies each IBR boundary, and set text does not name or restate the incorporated standard. | Analysis |
| NFR-001-AC-6 | The June 2023 FDA device-software guidance set contains no name, number, or paraphrase of a consensus standard cited by the guidance; a declaration of conformity remains generic and names none. | Analysis |

## Dependencies

- The publication-gate implementation is specified in PLAT-1549.

---
id: FR-013
title: The M4 crosswalk preserves NIST CPRT provenance
type: FR
---
# FR-013: The M4 crosswalk preserves NIST CPRT provenance

## Description

The M4 crosswalk records the HIPAA Security Rule source elements mapped by
NIST CPRT to controls in `nist/sp800-53@5.2.0`. The source is NIST's published
SP 800-66 Rev. 2 to SP 800-53 Rev. 5.1.1 crosswalk workbook. The relationship
set and its direction come from the published workbook; the target IDs are
normalized to the installed 5.2.0 catalog.

## Behavior

- Each record SHALL preserve the workbook's HIPAA reference element, NIST
  focal control, worksheet, and one-based source row. The workbook does not
  expose CPRT relationship IDs; the worksheet-row locator identifies the
  source record without inventing an ID.
- The record set SHALL contain every workbook row whose reference element is
  within §§ 164.308, 164.310, 164.312, 164.314(a), or 164.316. It SHALL NOT
  contain a § 164.314(b) relationship. Implementations SHALL NOT infer an
  additional relation from wording or fan out a parent-level element to child
  clauses.
- Each normalized target SHALL resolve in the installed
  `nist/sp800-53@5.2.0` catalog. A 5.1.1-to-5.2.0 normalization SHALL remove
  only leading zeroes from control and enhancement numbers and SHALL record
  its source ID, target ID, method, reason, and workbook provenance.
- Because workbook reference elements can be parent-level identifiers rather
  than clause IDs in this clause set, the module SHALL store them in the
  pack-specific `cprtCrosswalks` field. It SHALL NOT add synthetic clauses or
  place these elements in native `ClauseSet.crosswalks` records. Quire
  evaluation and Quoin RMM do not consume `cprtCrosswalks`.
- A source clause with no exact workbook relationship SHALL be listed in
  `unmappedSourceClauses` rather than assigned an inferred control.
- Rows from control-family worksheets SHALL use relation `partial`; rows from
  the `Relationships-AC` worksheet, which lists related controls, SHALL use
  relation `informative`. Each row SHALL have a non-blank original rationale
  in our own words. A rationale SHALL describe only the workbook relationship
  and SHALL NOT claim equivalence, complete coverage, or discharge.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-013-AC-1 | The complete `(reference element, focal control)` pair set equals the in-scope workbook rows. Each record retains the exact worksheet and row locator and the workbook's focal-to-reference direction. | Test |
| FR-013-AC-2 | Each included standard has at least one relationship; § 164.314(b) is absent. Every target resolves in the pinned NIST catalog. A fixture target `AC-999` fails with a diagnostic naming its crosswalk. | Test |
| FR-013-AC-3 | Every relationship has the required `partial` or `informative` value and a non-blank original rationale; the designator scan finds none. The 14 source clauses with no exact relationship remain explicitly unmapped, and each changed target records the exact leading-zero normalization. | Test |

## Dependencies

- Target catalog: `nist/sp800-53@5.2.0`, from the installed
  `spec-objects-security` module.
- The source workbook is identified below. The test fixture contains only the
  selected public identifiers and source row locators as an independent test
  oracle; it contains no descriptions or workbook hash.

## Source and row selection

NIST CPRT, **SP-800-66-Rev-2-to-SP-800-53-Rev-5.1.1**, framework
`SP800-66R2-800-53R5.1.1`, version `1.0.0`, released 2024-03-20:
[official workbook](https://csrc.nist.gov/csrc/media/Projects/olir/documents/submissions/SP800-53_SecurityRule_Crosswalk_2024.xlsx).
NIST publications are generally public domain in the United States; see the
[NIST publication rights FAQ](https://www.nist.gov/nist-research-library/library-faqs).
Only identifiers and row locators are used. No descriptions or source text are
reproduced.

The in-scope rows are the non-header records on all workbook worksheets whose
`Reference Document Element` begins with `164.308`, `164.310`, `164.312`,
`164.314(a)`, or `164.316`. In the published workbook, `Focal Document Element`
is the NIST 5.1.1 control and `Reference Document Element` is the HIPAA source
element. The complete list of those rows is independently recorded in
`tests/fixtures/cprt-hipaa-nist-relationships.csv` for test comparison; that
fixture contains identifiers only.

## `cprtCrosswalks` record shape

Each record contains:

| Field | Meaning |
|---|---|
| `sourceElementId` | The workbook's HIPAA reference element ID, unchanged. |
| `target.set` and `target.clause` | `nist/sp800-53@5.2.0` and the canonical target ID in that catalog. |
| `relation` | `partial` for control-family worksheet rows; `informative` for `Relationships-AC` rows. |
| `rationale` | One original sentence describing the source relationship without an equivalence or discharge claim. |
| `provenance.workbook` | Workbook title, ID, version, release date, and official URL. |
| `provenance.worksheet` and `provenance.row` | Exact worksheet name and one-based source row. |
| `provenance.direction`, `focalElement`, and `referenceElement` | `focal-to-reference`, with the original NIST 5.1.1 and HIPAA identifiers. |
| `normalization` | Present only when IDs differ; records `leading-zero-removal`, the source ID, canonical target ID, and reason. |

The pack's tests validate the extension's shape, row set, relation labels,
rationales, unmapped identifiers, target membership, and normalization. It is
provenance metadata, not an engine crosswalk or an RMM input.

## Explicitly unmapped source clauses

The following clause IDs have no exact source relationship in the published
workbook and SHALL remain unmapped:

- `164.308(a)(1)(i)`
- `164.308(a)(3)(i)`
- `164.308(a)(4)(i)`
- `164.308(a)(5)(i)`
- `164.308(a)(6)(i)`
- `164.308(a)(7)(i)`
- `164.308(b)`
- `164.308(b)(3)`
- `164.310(a)(1)`
- `164.310(d)(1)`
- `164.312(a)(1)`
- `164.312(c)(1)`
- `164.314(a)(1)`
- `164.316(b)(1)`

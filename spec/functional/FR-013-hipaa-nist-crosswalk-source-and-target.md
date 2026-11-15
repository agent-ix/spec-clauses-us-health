---
id: FR-013
title: The M4 crosswalk preserves NIST CPRT provenance
type: FR
---
# FR-013: The M4 crosswalk preserves NIST CPRT provenance

## Description

The M4 crosswalk maps the HIPAA Security Rule source elements in the exact
pair table below to the target set `nist/sp800-53@5.2.0`. The source is NIST
CPRT's published SP 800-66 Rev. 2 to SP 800-53 Rev. 5.1.1 crosswalk workbook.
PLAT-1616 authors the mappings; this requirement fixes the source, target,
provenance fields, and coverage needed to make that implementation
well-defined.

## Behavior

- A crosswalk row SHALL identify the HIPAA source element, the corresponding
  NIST target control in `nist/sp800-53@5.2.0`, and the exact source workbook
  locator (worksheet name and one-based row number).
- Each row SHALL preserve the published workbook's direction: its focal
  element is the NIST target and its reference element is the HIPAA source.
  The source does not expose CPRT internal relationship IDs; the workbook
  locator SHALL identify the relationship record without inventing an ID.
- The (source element, target control) pair set SHALL equal the pair table
  below. Implementations SHALL NOT infer a relationship from similar wording
  or add a pair absent from the published source table.
- The crosswalk SHALL mark a source clause with no CPRT relationship to the
  target as unmapped rather than assign an inferred control.
- The crosswalk validator SHALL verify each target control against the pinned
  5.2.0 target catalog;
  any target normalization from CPRT's 5.1.1 control identifier SHALL be
  recorded with its reason and source evidence.
- Because some CPRT reference elements are parent-level identifiers rather
  than clause IDs in this clause set, the module SHALL store these source
  relationships as `cprtCrosswalks`; it SHALL NOT add synthetic clauses or map
  parent-level source elements to child clauses.
- `cprtCrosswalks` is pack-specific provenance metadata. Quire's native
  `ClauseSet.crosswalks` field requires `sourceClause` to identify a clause in
  the source set, so it cannot represent these exact parent-level source
  elements. Quire evaluation and Quoin RMM do not consume `cprtCrosswalks`;
  these records provide auditable source relationships only.
- The crosswalk SHALL include at least one CPRT-backed, verified target
  control for each included standard: §§ 164.308, 164.310, 164.312, 164.314(a),
  and 164.316. It SHALL NOT include § 164.314(b).

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-013-AC-1 | The crosswalk pair set equals the exact source-to-target table below; each row records the source element ID, the target ID found in `nist/sp800-53@5.2.0`, the source workbook worksheet and row locator, and the workbook's focal-to-reference direction. | Test |
| FR-013-AC-2 | Each of §§ 164.308, 164.310, 164.312, 164.314(a), and 164.316 has at least one verified CPRT-backed target mapping; § 164.314(b) has none. | Test |
| FR-013-AC-3 | A clause with no source relationship is explicitly unmapped, and a target absent from the pinned target catalog or an unrecorded 5.1.1-to-5.2.0 normalization fails validation. | Test |

## Dependencies

- The target catalog is `nist/sp800-53@5.2.0` and the source is NIST CPRT
  `SP800-66R2-800-53R5.1.1`, identified in the [crosswalk plan](../spec.md).
- PLAT-1616 authors crosswalk data; this requirement defines its contract.

## Exact source-to-target pair table

The complete pair set, official source identity and release, rights scope,
SHA-256 digest, source locators, target normalization, and pair counts are in
the table below. The published source contains identifiers and descriptions;
only identifiers are reproduced. It does not provide a CPRT internal
relationship ID, so the exact published worksheet-row locator is the
traceable relationship record reference.

## Exact CPRT source-to-target pair table

This table is the complete row-level pair set from NIST CPRT's published workbook **SP-800-66-Rev-2-to-SP-800-53-Rev-5.1.1**, framework identifier `SP800-66R2-800-53R5.1.1`, version `1.0.0`, released 2024-03-20. NIST publishes the file at [SP800-53_SecurityRule_Crosswalk_2024.xlsx](https://csrc.nist.gov/csrc/media/Projects/olir/documents/submissions/SP800-53_SecurityRule_Crosswalk_2024.xlsx). NIST states its publications are generally in the U.S. public domain ([NIST publication rights FAQ](https://www.nist.gov/nist-research-library/library-faqs)). This table reproduces only identifiers; it does not copy workbook descriptions or NIST publication text. SHA-256: `80ee1b51d5b48f394e35311a9a93006d2f9e530e35266c6f1f00eb212b776b95`. The workbook does not expose CPRT internal relationship IDs; `sheet:row` below is the stable row locator in the published source artifact. The workbook row direction is NIST target control (`Focal Document Element`) to HIPAA source element (`Reference Document Element`); the first and third columns provide a reverse-lookup view without changing or claiming a different source relationship direction. Only element identifiers are reproduced here; source descriptions and control text are not copied.

Each row is represented in the HIPAA set's `cprtCrosswalks` array with this
shape:

| Field | Meaning |
|---|---|
| `sourceElementId` | The workbook's HIPAA reference element ID; it is not rewritten as a clause ID. |
| `target.set` and `target.clause` | The installed target key `nist/sp800-53@5.2.0` and its canonical control ID. |
| `provenance.workbook` | Workbook ID, title, version, release date, official URL, and the source artifact SHA-256. |
| `provenance.worksheet` and `provenance.row` | The exact worksheet and one-based row locator in that workbook. |
| `provenance.direction`, `focalElement`, and `referenceElement` | The original NIST-focal to HIPAA-reference direction and IDs. |
| `normalization` | Present only when a source control ID changes; records the 5.1.1 ID, 5.2.0 ID, method, and reason. |

The repository test suite validates the record shape, exact pair set,
provenance, unmapped IDs, target catalog membership, and every normalization.
The `cprtCrosswalks` extension is not a native Quire `ClauseSet.crosswalks`
entry and does not affect profile evaluation or RMM rendering.

The fourth column is the exact NIST 5.1.1 element identifier. The fifth is its canonical ID in the installed `nist/sp800-53@5.2.0` catalog. Normalization removes leading zeroes from control and enhancement numbers only; it does not change the control family or number. Each normalized target was found in the pinned catalog. The pair table covers the five included Security Rule standards and contains no § 164.314(b) entry.

Some source elements in the workbook are parent-level identifiers that are not
clause IDs in the HIPAA clause set. Preserve those source identifiers exactly
as source provenance; do not fan their relationships out to child clauses.
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

| HIPAA source element ID | CPRT 5.1.1 target ID | 5.2.0 target ID | CPRT workbook row |
|---|---|---|---|
| `164.308(a)(3)` | `AC-01` | `AC-1` | `Relationships-AC:2` |
| `164.308(a)(3)(ii)(A)` | `AC-01` | `AC-1` | `Relationships-AC:3` |
| `164.308(a)(4)` | `AC-01` | `AC-1` | `Relationships-AC:4` |
| `164.308(a)(4)(ii)(B)` | `AC-01` | `AC-1` | `Relationships-AC:5` |
| `164.308(a)(4)(ii)(C)` | `AC-01` | `AC-1` | `Relationships-AC:6` |
| `164.312(a)` | `AC-01` | `AC-1` | `Relationships-AC:7` |
| `164.316(b)(2)(ii)` | `AC-01` | `AC-1` | `Relationships-AC:8` |
| `164.316(b)(2)(iii)` | `AC-01` | `AC-1` | `Relationships-AC:9` |
| `164.308(a)(3)` | `AC-02` | `AC-2` | `Relationships-AC:10` |
| `164.308(a)(3)(ii)(A)` | `AC-02` | `AC-2` | `Relationships-AC:11` |
| `164.308(a)(3)(ii)(B)` | `AC-02` | `AC-2` | `Relationships-AC:12` |
| `164.308(a)(4)` | `AC-02` | `AC-2` | `Relationships-AC:13` |
| `164.308(a)(4)(ii)(B)` | `AC-02` | `AC-2` | `Relationships-AC:14` |
| `164.308(a)(4)(ii)(C)` | `AC-02` | `AC-2` | `Relationships-AC:15` |
| `164.312(a)(2)(i)` | `AC-02` | `AC-2` | `Relationships-AC:16` |
| `164.312(a)(2)(ii)` | `AC-02` | `AC-2` | `Relationships-AC:17` |
| `164.308(a)(3)` | `AC-03` | `AC-3` | `Relationships-AC:31` |
| `164.308(a)(3)(ii)(A)` | `AC-03` | `AC-3` | `Relationships-AC:32` |
| `164.308(a)(4)(ii)(B)` | `AC-03` | `AC-3` | `Relationships-AC:33` |
| `164.310(b)` | `AC-03` | `AC-3` | `Relationships-AC:34` |
| `164.312(a)` | `AC-03` | `AC-3` | `Relationships-AC:35` |
| `164.312(a)(2)(i)` | `AC-03` | `AC-3` | `Relationships-AC:36` |
| `164.312(a)(2)(ii)` | `AC-03` | `AC-3` | `Relationships-AC:37` |
| `164.308(a)(3)(ii)(A)` | `AC-04` | `AC-4` | `Relationships-AC:53` |
| `164.308(a)(4)(ii)(B)` | `AC-04` | `AC-4` | `Relationships-AC:54` |
| `164.310(b)` | `AC-04` | `AC-4` | `Relationships-AC:55` |
| `164.308(a)(3)` | `AC-05` | `AC-5` | `Relationships-AC:88` |
| `164.308(a)(4)` | `AC-05` | `AC-5` | `Relationships-AC:89` |
| `164.308(a)(4)(ii)(A)` | `AC-05` | `AC-5` | `Relationships-AC:90` |
| `164.312(a)` | `AC-05` | `AC-5` | `Relationships-AC:91` |
| `164.308(a)(3)` | `AC-06` | `AC-6` | `Relationships-AC:92` |
| `164.308(a)(4)` | `AC-06` | `AC-6` | `Relationships-AC:93` |
| `164.308(a)(4)(ii)(A)` | `AC-06` | `AC-6` | `Relationships-AC:94` |
| `164.312(a)` | `AC-06` | `AC-6` | `Relationships-AC:95` |
| `164.310(b)` | `AC-11` | `AC-11` | `Relationships-AC:118` |
| `164.310(b)` | `AC-12` | `AC-12` | `Relationships-AC:120` |
| `164.312(a)(2)(iii)` | `AC-12` | `AC-12` | `Relationships-AC:121` |
| `164.310(b)` | `AC-16` | `AC-16` | `Relationships-AC:129` |
| `164.310(b)` | `AC-17` | `AC-17` | `Relationships-AC:140` |
| `164.310(b)` | `AC-19` | `AC-19` | `Relationships-AC:157` |
| `164.308(a)(5)` | `AT-01` | `AT-1` | `AT:2` |
| `164.316(b)(2)(ii)` | `AT-01` | `AT-1` | `AT:3` |
| `164.316(b)(2)(iii)` | `AT-01` | `AT-1` | `AT:4` |
| `164.308(a)(5)` | `AT-02` | `AT-2` | `AT:5` |
| `164.308(a)(5)(ii)(A)` | `AT-02` | `AT-2` | `AT:6` |
| `164.308(a)(5)(ii)(B)` | `AT-02` | `AT-2` | `AT:7` |
| `164.308(a)(5)(ii)(D)` | `AT-02` | `AT-2` | `AT:8` |
| `164.308(a)(5)` | `AT-03` | `AT-3` | `AT:15` |
| `164.308(a)(5)(ii)(A)` | `AT-03` | `AT-3` | `AT:16` |
| `164.308(a)(5)(ii)(B)` | `AT-03` | `AT-3` | `AT:17` |
| `164.308(a)(5)(ii)(C)` | `AT-03` | `AT-3` | `AT:18` |
| `164.308(a)(5)(ii)(D)` | `AT-03` | `AT-3` | `AT:19` |
| `164.308(a)(5)` | `AT-04` | `AT-4` | `AT:25` |
| `164.312(b)` | `AU-01` | `AU-1` | `AU:2` |
| `164.316(b)(2)(ii)` | `AU-01` | `AU-1` | `AU:3` |
| `164.316(b)(2)(iii)` | `AU-01` | `AU-1` | `AU:4` |
| `164.312(b)` | `AU-02` | `AU-2` | `AU:5` |
| `164.312(b)` | `AU-03` | `AU-3` | `AU:10` |
| `164.312(b)` | `AU-04` | `AU-4` | `AU:14` |
| `164.308(a)(1)(ii)(D)` | `AU-06` | `AU-6` | `AU:22` |
| `164.308(a)(5)(ii)(C)` | `AU-06` | `AU-6` | `AU:23` |
| `164.312(b)` | `AU-06` | `AU-6` | `AU:24` |
| `164.308(a)(1)(ii)(D)` | `AU-07` | `AU-7` | `AU:35` |
| `164.312(b)` | `AU-07` | `AU-7` | `AU:36` |
| `164.312(b)` | `AU-08` | `AU-8` | `AU:39` |
| `164.308(a)(8)` | `CA-01` | `CA-1` | `CA:2` |
| `164.316(b)(2)(ii)` | `CA-01` | `CA-1` | `CA:3` |
| `164.316(b)(2)(iii)` | `CA-01` | `CA-1` | `CA:4` |
| `164.308(a)(8)` | `CA-02` | `CA-2` | `CA:5` |
| `164.316(b)` | `CA-02` | `CA-2` | `CA:6` |
| `164.308(a)(4)(ii)(A)` | `CA-03` | `CA-3` | `CA:10` |
| `164.308(b)(1)` | `CA-03` | `CA-3` | `CA:11` |
| `164.308(b)(4)` | `CA-03` | `CA-3` | `CA:12` |
| `164.314(a)(2)(ii)` | `CA-03` | `CA-3` | `CA:13` |
| `164.308(a)(2)` | `CA-06` | `CA-6` | `CA:24` |
| `164.308(a)(8)` | `CA-06` | `CA-6` | `CA:25` |
| `164.308(a)(1)(ii)(D)` | `CA-07` | `CA-7` | `CA:28` |
| `164.308(a)(8)` | `CA-07` | `CA-7` | `CA:29` |
| `164.308(a)(8)` | `CA-08` | `CA-8` | `CA:36` |
| `164.316(b)(2)(ii)` | `CM-01` | `CM-1` | `CM:2` |
| `164.316(b)(2)(iii)` | `CM-01` | `CM-1` | `CM:3` |
| `164.310(d)` | `CM-08` | `CM-8` | `CM:47` |
| `164.310(d)(2)(iii)` | `CM-08` | `CM-8` | `CM:48` |
| `164.308(a)(7)` | `CP-01` | `CP-1` | `CP:2` |
| `164.316(b)(2)(ii)` | `CP-01` | `CP-1` | `CP:3` |
| `164.316(b)(2)(iii)` | `CP-01` | `CP-1` | `CP:4` |
| `164.308(a)(7)` | `CP-02` | `CP-2` | `CP:5` |
| `164.308(a)(7)(ii)(B)` | `CP-02` | `CP-2` | `CP:6` |
| `164.308(a)(7)(ii)(C)` | `CP-02` | `CP-2` | `CP:7` |
| `164.308(a)(7)(ii)(D)` | `CP-02` | `CP-2` | `CP:8` |
| `164.308(a)(7)(ii)(E)` | `CP-02` | `CP-2` | `CP:9` |
| `164.310(a)(2)(i)` | `CP-02` | `CP-2` | `CP:10` |
| `164.312(a)(2)(ii)` | `CP-02` | `CP-2` | `CP:11` |
| `164.308(a)(7)(ii)(E)` | `CP-02(08)` | `CP-2(8)` | `CP:19` |
| `164.308(a)(7)(ii)(D)` | `CP-03` | `CP-3` | `CP:20` |
| `164.308(a)(7)(ii)(D)` | `CP-04` | `CP-4` | `CP:23` |
| `164.308(a)(7)(ii)(A)` | `CP-06` | `CP-6` | `CP:30` |
| `164.308(a)(7)(ii)(B)` | `CP-06` | `CP-6` | `CP:31` |
| `164.310(a)(2)(i)` | `CP-06` | `CP-6` | `CP:32` |
| `164.308(a)(7)(ii)(B)` | `CP-07` | `CP-7` | `CP:36` |
| `164.310(a)(2)(i)` | `CP-07` | `CP-7` | `CP:37` |
| `164.308(a)(7)(ii)(B)` | `CP-08` | `CP-8` | `CP:44` |
| `164.308(a)(7)(ii)(A)` | `CP-09` | `CP-9` | `CP:50` |
| `164.308(a)(7)(ii)(B)` | `CP-09` | `CP-9` | `CP:51` |
| `164.310(d)(2)(iv)` | `CP-09` | `CP-9` | `CP:52` |
| `164.312(c)` | `CP-09` | `CP-9` | `CP:53` |
| `164.308(a)(7)(ii)(A)` | `CP-09(01)` | `CP-9(1)` | `CP:54` |
| `164.308(a)(7)(ii)(B)` | `CP-10` | `CP-10` | `CP:62` |
| `164.308(a)(7)(ii)(C)` | `CP-10` | `CP-10` | `CP:63` |
| `164.316(b)(2)(ii)` | `IA-01` | `IA-1` | `IA:2` |
| `164.316(b)(2)(iii)` | `IA-01` | `IA-1` | `IA:3` |
| `164.312(a)(2)(i)` | `IA-02` | `IA-2` | `IA:4` |
| `164.312(d)` | `IA-02` | `IA-2` | `IA:5` |
| `164.312(a)(2)(i)` | `IA-03` | `IA-3` | `IA:19` |
| `164.312(d)` | `IA-03` | `IA-3` | `IA:20` |
| `164.312(a)(2)(i)` | `IA-04` | `IA-4` | `IA:25` |
| `164.312(d)` | `IA-04` | `IA-4` | `IA:26` |
| `164.312(a)(2)(i)` | `IA-08` | `IA-8` | `IA:57` |
| `164.312(d)` | `IA-08` | `IA-8` | `IA:58` |
| `164.312(d)` | `IA-09` | `IA-9` | `IA:65` |
| `164.308(a)(6)` | `IR-01` | `IR-1` | `IR:2` |
| `164.316(b)(2)(ii)` | `IR-01` | `IR-1` | `IR:3` |
| `164.316(b)(2)(iii)` | `IR-01` | `IR-1` | `IR:4` |
| `164.308(a)(6)` | `IR-02` | `IR-2` | `IR:5` |
| `164.308(a)(6)` | `IR-03` | `IR-3` | `IR:9` |
| `164.308(a)(6)` | `IR-04` | `IR-4` | `IR:13` |
| `164.308(a)(6)(ii)` | `IR-04` | `IR-4` | `IR:14` |
| `164.308(a)(1)(ii)(D)` | `IR-05` | `IR-5` | `IR:30` |
| `164.308(a)(6)(ii)` | `IR-05` | `IR-5` | `IR:31` |
| `164.308(a)(1)(ii)(D)` | `IR-06` | `IR-6` | `IR:33` |
| `164.308(a)(6)(ii)` | `IR-06` | `IR-6` | `IR:34` |
| `164.314(a)(2)(i)` | `IR-06` | `IR-6` | `IR:35` |
| `164.314(a)(2)(iii)` | `IR-06` | `IR-6` | `IR:36` |
| `164.308(a)(6)(ii)` | `IR-07` | `IR-7` | `IR:41` |
| `164.308(a)(6)(ii)` | `IR-08` | `IR-8` | `IR:44` |
| `164.308(a)(6)(ii)` | `IR-09` | `IR-9` | `IR:46` |
| `164.310(a)(2)(iv)` | `MA-01` | `MA-1` | `MA:2` |
| `164.316(b)(2)(ii)` | `MA-01` | `MA-1` | `MA:3` |
| `164.316(b)(2)(iii)` | `MA-01` | `MA-1` | `MA:4` |
| `164.310(a)(2)(iv)` | `MA-02` | `MA-2` | `MA:5` |
| `164.308(a)(3)(ii)(A)` | `MA-05` | `MA-5` | `MA:23` |
| `164.310(a)(2)(iv)` | `MA-06` | `MA-6` | `MA:29` |
| `164.310(d)` | `MP-01` | `MP-1` | `MP:2` |
| `164.316(b)(2)(ii)` | `MP-01` | `MP-1` | `MP:3` |
| `164.316(b)(2)(iii)` | `MP-01` | `MP-1` | `MP:4` |
| `164.308(a)(3)(ii)(A)` | `MP-02` | `MP-2` | `MP:5` |
| `164.310(c)` | `MP-02` | `MP-2` | `MP:6` |
| `164.310(d)` | `MP-02` | `MP-2` | `MP:7` |
| `164.312(c)` | `MP-02` | `MP-2` | `MP:8` |
| `164.310(c)` | `MP-03` | `MP-3` | `MP:11` |
| `164.310(d)` | `MP-03` | `MP-3` | `MP:12` |
| `164.310(c)` | `MP-04` | `MP-4` | `MP:13` |
| `164.310(d)` | `MP-04` | `MP-4` | `MP:14` |
| `164.310(d)(2)(iv)` | `MP-04` | `MP-4` | `MP:15` |
| `164.310(d)` | `MP-05` | `MP-5` | `MP:18` |
| `164.310(d)(2)(iii)` | `MP-05` | `MP-5` | `MP:19` |
| `164.312(c)` | `MP-05` | `MP-5` | `MP:20` |
| `164.310(d)` | `MP-06` | `MP-6` | `MP:25` |
| `164.310(d)(2)(i)` | `MP-06` | `MP-6` | `MP:26` |
| `164.310(d)(2)(ii)` | `MP-06` | `MP-6` | `MP:27` |
| `164.310(a)` | `PE-01` | `PE-1` | `PE:2` |
| `164.310(a)(2)(ii)` | `PE-01` | `PE-1` | `PE:3` |
| `164.310(a)(2)(iii)` | `PE-01` | `PE-1` | `PE:4` |
| `164.316(b)(2)(ii)` | `PE-01` | `PE-1` | `PE:5` |
| `164.316(b)(2)(iii)` | `PE-01` | `PE-1` | `PE:6` |
| `164.310(a)` | `PE-02` | `PE-2` | `PE:7` |
| `164.310(a)(2)(i)` | `PE-02` | `PE-2` | `PE:8` |
| `164.310(a)(2)(iii)` | `PE-02` | `PE-2` | `PE:9` |
| `164.310(c)` | `PE-02` | `PE-2` | `PE:10` |
| `164.310(a)` | `PE-03` | `PE-3` | `PE:14` |
| `164.310(a)(2)(i)` | `PE-03` | `PE-3` | `PE:15` |
| `164.310(a)(2)(iii)` | `PE-03` | `PE-3` | `PE:16` |
| `164.310(b)` | `PE-03` | `PE-3` | `PE:17` |
| `164.310(c)` | `PE-03` | `PE-3` | `PE:18` |
| `164.310(a)` | `PE-03(01)` | `PE-3(1)` | `PE:19` |
| `164.310(a)(2)(iii)` | `PE-03(01)` | `PE-3(1)` | `PE:20` |
| `164.310(a)` | `PE-04` | `PE-4` | `PE:28` |
| `164.310(c)` | `PE-04` | `PE-4` | `PE:29` |
| `164.310(a)` | `PE-05` | `PE-5` | `PE:30` |
| `164.310(b)` | `PE-05` | `PE-5` | `PE:31` |
| `164.310(c)` | `PE-05` | `PE-5` | `PE:32` |
| `164.310(a)(2)(iii)` | `PE-06` | `PE-6` | `PE:36` |
| `164.310(a)(2)(iii)` | `PE-08` | `PE-8` | `PE:42` |
| `164.310(d)` | `PE-16` | `PE-16` | `PE:66` |
| `164.310(d)(2)(iii)` | `PE-16` | `PE-16` | `PE:67` |
| `164.310(a)(2)(i)` | `PE-17` | `PE-17` | `PE:68` |
| `164.310(c)` | `PE-18` | `PE-18` | `PE:69` |
| `164.310(d)` | `PE-20` | `PE-20` | `PE:73` |
| `164.310(d)(2)(iii)` | `PE-20` | `PE-20` | `PE:74` |
| `164.316(a)` | `PL-01` | `PL-1` | `PL:2` |
| `164.316(b)(2)(ii)` | `PL-01` | `PL-1` | `PL:3` |
| `164.316(b)(2)(iii)` | `PL-01` | `PL-1` | `PL:4` |
| `164.308(a)(1)(ii)(B)` | `PL-02` | `PL-2` | `PL:5` |
| `164.310(a)(2)(ii)` | `PL-02` | `PL-2` | `PL:6` |
| `164.316(a)` | `PL-02` | `PL-2` | `PL:10` |
| `164.316(b)` | `PL-02` | `PL-2` | `PL:11` |
| `164.316(b)(2)(iii)` | `PL-02` | `PL-2` | `PL:12` |
| `164.310(b)` | `PL-04` | `PL-4` | `PL:17` |
| `164.316(b)(2)(ii)` | `PM-01` | `PM-1` | `PM:2` |
| `164.316(b)(2)(iii)` | `PM-01` | `PM-1` | `PM:3` |
| `164.308(a)(2)` | `PM-02` | `PM-2` | `PM:4` |
| `164.308(a)(3)(ii)(A)` | `PS-01` | `PS-1` | `PS:2` |
| `164.308(a)(3)(ii)(B)` | `PS-01` | `PS-1` | `PS:3` |
| `164.308(a)(3)(ii)(C)` | `PS-01` | `PS-1` | `PS:4` |
| `164.316(b)(2)(ii)` | `PS-01` | `PS-1` | `PS:5` |
| `164.316(b)(2)(iii)` | `PS-01` | `PS-1` | `PS:6` |
| `164.308(a)(3)(ii)(B)` | `PS-02` | `PS-2` | `PS:7` |
| `164.308(a)(3)(ii)(B)` | `PS-03` | `PS-3` | `PS:8` |
| `164.308(a)(3)(ii)(C)` | `PS-04` | `PS-4` | `PS:13` |
| `164.308(a)(3)(ii)(B)` | `PS-05` | `PS-5` | `PS:16` |
| `164.308(a)(3)(ii)(C)` | `PS-05` | `PS-5` | `PS:17` |
| `164.308(a)(3)(ii)(A)` | `PS-06` | `PS-6` | `PS:18` |
| `164.308(a)(3)(ii)(B)` | `PS-06` | `PS-6` | `PS:19` |
| `164.308(a)(4)(ii)(B)` | `PS-06` | `PS-6` | `PS:20` |
| `164.310(b)` | `PS-06` | `PS-6` | `PS:21` |
| `164.310(d)(2)(iii)` | `PS-06` | `PS-6` | `PS:22` |
| `164.314(a)` | `PS-06` | `PS-6` | `PS:23` |
| `164.314(a)(2)(i)` | `PS-06` | `PS-6` | `PS:24` |
| `164.314(a)(2)(ii)` | `PS-06` | `PS-6` | `PS:25` |
| `164.314(a)(2)(iii)` | `PS-06` | `PS-6` | `PS:26` |
| `164.308(a)(3)(ii)(A)` | `PS-07` | `PS-7` | `PS:30` |
| `164.308(a)(3)(ii)(B)` | `PS-07` | `PS-7` | `PS:31` |
| `164.308(a)(4)(ii)(B)` | `PS-07` | `PS-7` | `PS:32` |
| `164.308(b)(1)` | `PS-07` | `PS-7` | `PS:33` |
| `164.314(a)` | `PS-07` | `PS-7` | `PS:34` |
| `164.314(a)(2)(i)` | `PS-07` | `PS-7` | `PS:35` |
| `164.314(a)(2)(ii)` | `PS-07` | `PS-7` | `PS:36` |
| `164.314(a)(2)(iii)` | `PS-07` | `PS-7` | `PS:37` |
| `164.308(a)(1)(ii)(C)` | `PS-08` | `PS-8` | `PS:38` |
| `164.316(b)(2)(ii)` | `PT-01` | `PT-1` | `PT:2` |
| `164.316(b)(2)(iii)` | `PT-01` | `PT-1` | `PT:3` |
| `164.308(a)(1)` | `RA-01` | `RA-1` | `RA:2` |
| `164.316(a)` | `RA-01` | `RA-1` | `RA:3` |
| `164.316(b)(2)(ii)` | `RA-01` | `RA-1` | `RA:4` |
| `164.316(b)(2)(iii)` | `RA-01` | `RA-1` | `RA:5` |
| `164.308(a)(1)(ii)(A)` | `RA-02` | `RA-2` | `RA:6` |
| `164.308(a)(1)(ii)(B)` | `RA-02` | `RA-2` | `RA:7` |
| `164.308(a)(7)(ii)(E)` | `RA-02` | `RA-2` | `RA:8` |
| `164.308(a)(7)(ii)(E)` | `RA-02(01)` | `RA-2(1)` | `RA:9` |
| `164.308(a)(1)(ii)(A)` | `RA-03` | `RA-3` | `RA:10` |
| `164.308(a)(1)(ii)(B)` | `RA-03` | `RA-3` | `RA:11` |
| `164.316(a)` | `RA-03` | `RA-3` | `RA:12` |
| `164.316(b)(2)(ii)` | `SA-01` | `SA-1` | `SA:2` |
| `164.316(b)(2)(iii)` | `SA-01` | `SA-1` | `SA:3` |
| `164.308(b)(4)` | `SA-04` | `SA-4` | `SA:9` |
| `164.314(a)` | `SA-04` | `SA-4` | `SA:10` |
| `164.314(a)(2)(i)` | `SA-04` | `SA-4` | `SA:11` |
| `164.314(a)(2)(iii)` | `SA-04` | `SA-4` | `SA:12` |
| `164.308(b)(1)` | `SA-09` | `SA-9` | `SA:67` |
| `164.308(b)(4)` | `SA-09` | `SA-9` | `SA:68` |
| `164.314(a)` | `SA-09` | `SA-9` | `SA:69` |
| `164.314(a)(2)(i)` | `SA-09` | `SA-9` | `SA:70` |
| `164.314(a)(2)(ii)` | `SA-09` | `SA-9` | `SA:71` |
| `164.314(a)(2)(iii)` | `SA-09` | `SA-9` | `SA:72` |
| `164.316(b)(2)(ii)` | `SC-01` | `SC-1` | `SC:2` |
| `164.316(b)(2)(iii)` | `SC-01` | `SC-1` | `SC:3` |
| `164.312(c)` | `SC-08` | `SC-8` | `SC:51` |
| `164.312(c)(2)` | `SC-08` | `SC-8` | `SC:52` |
| `164.312(e)(1)` | `SC-08` | `SC-8` | `SC:53` |
| `164.312(e)(2)(i)` | `SC-08` | `SC-8` | `SC:54` |
| `164.312(e)(2)(ii)` | `SC-08` | `SC-8` | `SC:55` |
| `164.312(e)(2)(ii)` | `SC-12` | `SC-12` | `SC:65` |
| `164.312(a)(2)(iv)` | `SC-13` | `SC-13` | `SC:72` |
| `164.312(e)(2)(ii)` | `SC-13` | `SC-13` | `SC:73` |
| `164.312(c)` | `SI-01` | `SI-1` | `SI:2` |
| `164.316(b)(2)(ii)` | `SI-01` | `SI-1` | `SI:3` |
| `164.316(b)(2)(iii)` | `SI-01` | `SI-1` | `SI:4` |
| `164.308(a)(1)(ii)(D)` | `SI-04` | `SI-4` | `SI:23` |
| `164.312(c)` | `SI-07` | `SI-7` | `SI:55` |
| `164.312(c)(2)` | `SI-07` | `SI-7` | `SI:56` |
| `164.312(e)(2)(i)` | `SI-07` | `SI-7` | `SI:57` |
| `164.316(b)(2)(i)` | `SI-12` | `SI-12` | `SI:88` |
| `164.316(b)(2)(ii)` | `SR-01` | `SR-1` | `SR:2` |
| `164.316(b)(2)(iii)` | `SR-01` | `SR-1` | `SR:3` |

Pair count: **274**. Source standards: `164.308` (107), `164.310` (60), `164.312` (41), `164.314(a)` (18), and `164.316` (48).

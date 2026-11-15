---
id: FR-016
title: M2 applicability uses only explicit human-supplied facts
type: FR
relationships:
  - target: "ix://agent-ix/spec-clauses-us-health/FR-004"
    type: extends
---
# FR-016: M2 applicability uses only explicit human-supplied facts

## Description

M2 applicability uses only the dimensions and expressions declared in the
master tables. Device-category and documentation-level decisions remain
human-supplied facts.

## Behavior

- The Part 820 set SHALL declare `qmsr_traceability_applicability`,
  `qmsr_advisory_notice_applicability`,
  `qmsr_design_development_applicability`, `qmsr_life_support_applicability`,
  and `qmsr_servicing_applicability`, each with unordered values `applies` and
  `not_applicable`.
- A person SHALL supply each dimension.
- The evaluator SHALL NOT infer a dimension from `device_class` or another
  product fact.
- When a conditional Part 820 dimension is `applies`, its clause SHALL be
  `binding`; when it is `not_applicable`, its clause SHALL be `not_binding`;
  when it is absent, its clause SHALL be `unresolved`.
- Clauses without a table-declared applicability expression SHALL remain
  applicable regardless of absent product context.
- A person SHALL supply `documentation_level`.
- The evaluator SHALL NOT infer `documentation_level` from device class,
  product type, risk, or other context.
- With `documentation_level=basic`, baseline guidance clauses SHALL be
  `binding`; the rows available only at `documentation_level=enhanced` SHALL
  be `not_binding`.
- With `documentation_level=enhanced`, baseline and enhanced-level guidance
  clauses SHALL be `binding`.
- With no `documentation_level`, every guidance clause SHALL be `unresolved`.

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-016-AC-1 | For each of the five Part 820 applicability dimensions, `applies` yields `binding`, `not_applicable` yields `not_binding`, and an omitted dimension yields `unresolved` for its dependent clause. | Test |
| FR-016-AC-2 | A Part 820 clause with no applicability expression remains applicable when all M2 context is absent; no evaluator derives a value for a declared dimension. | Test |
| FR-016-AC-3 | With `documentation_level=basic`, every baseline Section VI clause is `binding` and `VI.F.enhanced`, `VI.G.enhanced`, and `VI.H.enhanced` are `not_binding`. | Test |
| FR-016-AC-4 | With `documentation_level=enhanced`, all Section VI clauses are `binding`; with no value, all Section VI clauses are `unresolved`. | Test |
| FR-016-AC-5 | A profile or context containing an undeclared documentation-level or applicability value fails validation or clause evaluation with a diagnostic identifying the invalid dimension. | Test |

## Dependencies

- Extends user-supplied applicability rules in
  [FR-004](./FR-004-applicability.md).
- Defines applicability behavior for
  [FR-014](./FR-014-part-820-quality-management-system-clause-set.md) and
  [FR-015](./FR-015-fda-device-software-guidance-clause-set.md).

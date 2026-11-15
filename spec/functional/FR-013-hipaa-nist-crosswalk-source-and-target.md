---
id: FR-013
title: The M4 crosswalk preserves NIST CPRT provenance
type: FR
---
# FR-013: The M4 crosswalk preserves NIST CPRT provenance

## Description

The M4 crosswalk maps the Security Rule clauses to the target set
`nist/sp800-53@5.2.0` using the NIST CPRT dataset `SP800_66_2_0_0` as its
source. PLAT-1616 authors the mappings; this requirement fixes the source,
target, provenance fields, and coverage needed to make that implementation
well-defined.

## Behavior

- A crosswalk row SHALL identify a Security Rule clause, the corresponding
  CPRT source element and relationship, and a target control in
  `nist/sp800-53@5.2.0`.
- The crosswalk SHALL preserve the source relationship's direction and
  identifier and SHALL NOT infer a relationship solely from similar wording.
- The crosswalk SHALL mark a source clause with no CPRT relationship to the
  target as unmapped rather than assign an inferred control.
- The crosswalk validator SHALL verify each target control against the pinned
  5.2.0 target catalog;
  any target normalization from CPRT's 5.1.1 control identifier SHALL be
  recorded with its reason and source evidence.
- The crosswalk SHALL include at least one CPRT-backed, verified target
  control for each included standard: §§ 164.308, 164.310, 164.312, 164.314(a),
  and 164.316. It SHALL NOT include § 164.314(b).

## Acceptance Criteria

| ID | Criteria | Verification |
|---|---|---|
| FR-013-AC-1 | Each mapping row records the clause ID, CPRT source element ID, CPRT relationship ID and direction, and a target ID found in `nist/sp800-53@5.2.0`. | Test |
| FR-013-AC-2 | Each of §§ 164.308, 164.310, 164.312, 164.314(a), and 164.316 has at least one verified CPRT-backed target mapping; § 164.314(b) has none. | Test |
| FR-013-AC-3 | A clause with no source relationship is explicitly unmapped, and a target absent from the pinned target catalog or an unrecorded 5.1.1-to-5.2.0 normalization fails validation. | Test |

## Dependencies

- The target catalog is `nist/sp800-53@5.2.0` and the source is NIST CPRT
  `SP800_66_2_0_0`, identified in the [crosswalk plan](../spec.md).
- PLAT-1616 authors crosswalk data; this requirement defines its contract.

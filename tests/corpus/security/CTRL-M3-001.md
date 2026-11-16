---
id: CTRL-M3-001
title: Dependency inventory and remediation
type: control
object: control
relationships:
  - target: THREAT-M3-001
    type: mitigates
  - target: RISK-M3-001
    type: mitigates
---
# CTRL-M3-001 — Dependency inventory and remediation

The release process ingests the component inventory, records support status,
and blocks release of a device build with an unsupported component until the
component is upgraded or an approved risk treatment is recorded.

## Mappings

The control mitigates THREAT-M3-001 by identifying affected components and
requiring remediation. It treats RISK-M3-001 by tracking unsupported
dependencies through the release process.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| control_id | UUID | 1..1 | identity |
| effectiveness | String | 1..1 | minLength: 1 |
| owner | String | 1..1 | minLength: 1 |

## Invariants

### UnsupportedComponentsHaveDisposition

```ocl
context DependencyInventoryAndRemediation
inv UnsupportedComponentsHaveDisposition:
  self.effectiveness->notEmpty()
```

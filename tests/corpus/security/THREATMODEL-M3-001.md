---
id: THREATMODEL-M3-001
title: Device network threat model
type: threat_model
object: threat_model
method: stride_per_interaction
reviewed_by: "reviewer@example.invalid"
relationships:
  - target: CONN-M3-001
    type: scopes
  - target: BOUNDARY-M3-001
    type: scopes
  - target: THREAT-M3-001
    type: considers
---
# THREATMODEL-M3-001 — Device network threat model

## Scope

The connection between the remote client and the device service, analysed per
interaction with STRIDE across the device network trust boundary.

## Assumptions

The device service is reachable only through the authenticated network path.

## Out of scope

The remote client host and the device's physical interfaces.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| threat_model_id | UUID | 1..1 | identity |
| method | String | 1..1 | minLength: 1 |
| reviewed_by | String | 1..1 | minLength: 1 |

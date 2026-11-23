---
id: RISK-M3-001
title: Device compromise through an unsupported dependency
type: risk
object: risk
likelihood: possible
impact: major
decision: not_accepted
decided_by: "reviewer@example.invalid"
relationships:
  - target: THREAT-M3-001
    type: arises_from
---
# RISK-M3-001 — Unsupported dependency compromise

An unsupported dependency may expose the device to a compromise that disrupts
essential functions or exposes device data.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| risk_id | UUID | 1..1 | identity |
| likelihood | String | 1..1 | minLength: 1 |
| impact | String | 1..1 | minLength: 1 |
| assessed_at | Timestamp | 1..1 |  |

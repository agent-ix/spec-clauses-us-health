---
id: THREAT-M3-001
title: Unpatched third-party component permits remote compromise
type: threat
object: threat
stride_category: tampering
vector: A vulnerable library version can be reached through the device's network service.
relationships:
  - target: CONN-M3-001
    type: threatens
---
# THREAT-M3-001 — Third-party component compromise

An attacker can exploit a vulnerable library included in the device and alter
device behavior or execute unauthorized code.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| threat_id | UUID | 1..1 | identity |
| stride_category | String | 1..1 | minLength: 1 |
| vector | String | 1..1 | minLength: 1 |

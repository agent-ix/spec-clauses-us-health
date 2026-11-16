---
id: VULN-M3-001
title: Unsupported component version remains in the device build
type: vulnerability
object: vulnerability
severity: high
---
# VULN-M3-001 — Unsupported dependency version

The device build contains a third-party component whose support period has
ended. The component version may contain defects without an upstream security
fix, increasing exposure to the related component-compromise threat.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| vulnerability_id | UUID | 1..1 | identity |
| severity | String | 1..1 | minLength: 1 |
| affected_component | String | 1..1 | minLength: 1 |
| detected_at | Timestamp | 1..1 |  |

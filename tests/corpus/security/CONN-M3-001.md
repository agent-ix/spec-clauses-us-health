---
id: CONN-M3-001
title: Remote client to device service connection
type: connection
object: connection
relationships:
  - target: BOUNDARY-M3-001
    type: crosses
  - target: CLASS-M3-001
    type: carries
---
# [CONN-M3-001] Remote client to device service connection

## Connection

| Source | Source Multiplicity | Target | Target Multiplicity | Direction |
|---|---|---|---|---|
| client_out | 1..1 | service_in | 1..1 | source-to-target |

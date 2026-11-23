---
id: BOUNDARY-M3-001
title: Device network trust boundary
type: trust_boundary
object: trust_boundary
trust_level: semi_trusted
---
# BOUNDARY-M3-001 — Device network trust boundary

## Boundary

```mermaid
flowchart LR
  subgraph untrusted[External network]
    client[Remote client]
  end
  subgraph trusted[Device]
    api[Device service]
    store[(Device data)]
  end
  client -->|Authenticated TLS| api
  api --> store
```

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| boundary_id | UUID | 1..1 | identity |
| trust_level | String | 1..1 | minLength: 1 |
| ingress_protocol | String | 1..1 | minLength: 1 |

## Invariants

### ExternalTrafficIsAuthenticated

```ocl
context DeviceNetworkTrustBoundary
inv ExternalTrafficIsAuthenticated:
  self.ingress_protocol <> 'plaintext'
```

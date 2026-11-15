---
id: NFR-001
title: "Retain synthetic evidence references"
type: NFR
relationships: []
---
# NFR-001: Retain synthetic evidence references

## Statement

The fictional `example.invalid` records service SHALL preserve a resolvable
reference for each synthetic approval record.

## Scope

- Applies to: synthetic records and approvals in this test corpus.
- Operational context: isolated local test execution.

## Rationale

Resolvable references let a reviewer inspect the synthetic source records.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| Resolved evidence references | 100% | 100% | Test |

## Verification

The integration test opens every path named by a discharge fact.

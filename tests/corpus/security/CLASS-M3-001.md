---
id: CLASS-M3-001
title: Device operational data
type: data_classification
object: data_classification
regulated_categories: [personal]
---
# [CLASS-M3-001] Device operational data

## Handling

Device operational data is carried over the authenticated network path and is
retained only for the device support period.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| classification_id | UUID | 1..1 | identity |
| level | String | 1..1 | minLength: 1 |
| retention | Duration | 1..1 |  |
| logging_permitted | Boolean | 1..1 |  |

"""Part 11 output bindings and customer-owned clause mapping."""

from __future__ import annotations

import re

import pytest
from conftest import (
    PACKAGE_ROOT,
    REPO_ROOT,
    assert_output_catalog_consistent,
    evaluate_clause_set,
    load_clause_sets,
)

PART_11_KEY = "us-fda/21-cfr-11@2026-11-12"


def _section_rows(heading: str) -> list[list[str]]:
    spec = (REPO_ROOT / "spec" / "spec.md").read_text()
    section = spec.split(heading, 1)[1].split("### ", 1)[0]
    return [
        [cell.strip() for cell in line.strip().strip("|").split("|")]
        for line in section.splitlines()
        if line.strip().startswith("| `")
    ]


def _clause_outputs_table() -> dict[str, list[str]]:
    return {
        re.search(r"`([^`]+)`", cells[0]).group(1): re.findall(r"`([^`]+)`", cells[2])
        for cells in _section_rows("### Part 11 Clause Table")
        if len(cells) == 3
    }


def _outcome(binding: dict, clause_id: str) -> str:
    return next(
        clause["outcome"]
        for clause in binding["clauses"]
        if clause["clauseId"] == clause_id
    )


@pytest.mark.trace("TC-010", "FR-003-AC-3")
def test_every_part11_clause_has_declared_outputs_matching_the_spec():
    """Description: Verify nonempty Part 11 outputs against the normative table.

    Assumptions: The Part 11 clause table in spec.md defines expected outputs.
    Criteria: Each clause has outputs exactly matching the table and all are declared.
    """
    (clause_set,) = load_clause_sets()
    expected_outputs = _clause_outputs_table()
    declared_outputs = clause_set["outputCatalog"]

    assert {clause["id"] for clause in clause_set["clauses"]} == set(expected_outputs)
    for clause in clause_set["clauses"]:
        clause_id = clause["id"]
        outputs = clause["expectedOutputs"]
        assert outputs, f"{clause_id} has no expected outputs"
        assert outputs == expected_outputs[clause_id], (
            f"{clause_id} expected outputs {outputs!r} do not match the spec table "
            f"{expected_outputs[clause_id]!r}"
        )
        undeclared = [name for name in outputs if name not in declared_outputs]
        assert (
            not undeclared
        ), f"{clause_id} references undeclared outputs: {undeclared!r}"


@pytest.mark.trace("TC-012", "TC-013", "FR-004-AC-1", "FR-004-AC-2")
def test_part11_open_system_binds_11_30_and_closed_system_does_not():
    """Description: Check § 11.30 outcomes for both system classifications.

    Assumptions: Applicability follows the system_type dimension.
    Criteria: § 11.30 is not_binding for closed and binding for open systems.
    """
    closed = evaluate_clause_set(PACKAGE_ROOT, PART_11_KEY, "system_type=closed")
    opened = evaluate_clause_set(PACKAGE_ROOT, PART_11_KEY, "system_type=open")

    assert _outcome(closed, "11.30") == "not_binding"
    assert _outcome(opened, "11.30") == "binding"


@pytest.mark.trace("TC-021", "FR-006-AC-1")
def test_customer_owned_table_matches_all_procedure_output_clauses():
    """Description: Compare the customer-owned table with procedure-only clauses.

    Assumptions: A clause is customer-owned exactly when every output is a procedure.
    Criteria: The spec table lists exactly the clauses satisfying that definition.
    """
    (clause_set,) = load_clause_sets()
    output_kinds = {
        name: definition["kind"]
        for name, definition in clause_set["outputCatalog"].items()
    }
    expected = {
        clause["id"]
        for clause in clause_set["clauses"]
        if clause["expectedOutputs"]
        and all(output_kinds[name] == "procedure" for name in clause["expectedOutputs"])
    }
    rows = _section_rows("### Customer-Owned Obligations")
    listed = {re.search(r"`([^`]+)`", row[0]).group(1) for row in rows if len(row) == 2}
    assert listed == expected


@pytest.mark.trace("TC-019", "FR-005-AC-2")
def test_part11_outputs_pass_the_us_catalog_consistency_helper():
    """Description: Check the Part 11 output definitions with the shared helper.

    Assumptions: The repository helper compares reused output definitions.
    Criteria: All declared US clause sets pass catalog consistency validation.
    """
    assert_output_catalog_consistent(load_clause_sets())

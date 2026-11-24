"""Part 11 output bindings and customer-owned clause mapping."""

from __future__ import annotations

import re

import pytest
from conftest import REPO_ROOT, load_clause_sets


def _part11_clause_set() -> dict:
    return next(
        clause_set
        for clause_set in load_clause_sets()
        if clause_set["authority"] == "us-fda"
        and clause_set["id"] == "21-cfr-11"
        and clause_set["version"] == "2026-11-12"
    )


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


@pytest.mark.trace("FR-003-AC-3")
def test_every_part11_clause_has_declared_outputs_matching_the_spec():
    """Description: Verify nonempty Part 11 outputs against the normative table.

    Assumptions: The Part 11 clause table in spec.md defines expected outputs.
    Criteria: Each clause has outputs exactly matching the table and all are declared.
    """
    clause_set = _part11_clause_set()
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


@pytest.mark.trace("FR-006-AC-1")
def test_customer_owned_table_matches_all_procedure_output_clauses():
    """Description: Compare the customer-owned table with procedure-only clauses.

    Assumptions: A clause is customer-owned exactly when every output is a procedure.
    Criteria: The spec table lists exactly the clauses satisfying that definition.
    """
    clause_set = _part11_clause_set()
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

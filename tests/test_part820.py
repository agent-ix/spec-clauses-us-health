"""Part 820 clause-set conformance to the M2 specification."""

from __future__ import annotations

import copy
import pathlib
import re

import pytest
import yaml
from conftest import (
    MANIFEST_PATH,
    PACKAGE_ROOT,
    REPO_ROOT,
    assert_output_catalog_consistent,
    clause_set_key,
    engine_tool,
    evaluate_clause_set,
    load_clause_sets,
    run,
)

PART_820_FILE = "us-fda-21-cfr-820-2026-11-12.json"
PART_820_KEY = "us-fda/21-cfr-820@2026-11-12"
IBR_TEXT = (
    "This provision is part of a regulation that incorporates requirements by "
    "reference; consult the cited public source for the full requirements."
)


def _spec_rows() -> list[list[str]]:
    spec = (REPO_ROOT / "spec" / "spec.md").read_text()
    section = spec.split(
        "### M2 Part 820 Quality Management System Regulation Clause Table", 1
    )[1].split("### ", 1)[0]
    rows = []
    for line in section.splitlines():
        if line.strip().startswith("| `") and line.count("|") >= 4:
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            rows.append(
                [
                    cells[0].strip("`"),
                    *[cell.strip("`") for cell in cells[1:-1]],
                    cells[-1],
                ]
            )
    return rows


def _part820_set() -> dict:
    return next(
        clause_set
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) == PART_820_KEY
    )


def _outcomes(binding: dict) -> dict[str, str]:
    return {clause["clauseId"]: clause["outcome"] for clause in binding["clauses"]}


def _assert_applicability_matches_spec(clause_set: dict) -> None:
    clauses = {clause["id"]: clause for clause in clause_set["clauses"]}
    for clause_id, applicability, *_ in _spec_rows():
        if applicability == "unconditional":
            expected = None
        else:
            _, dimension, value = applicability.split()
            expected = {"op": "eq", "dimension": dimension, "value": value}
        actual = clauses[clause_id].get("applicability")
        assert (
            actual == expected
        ), f"{clause_id}: expected applicability {expected!r}; found {actual!r}"


@pytest.mark.trace("TC-069", "FR-014-AC-1")
def test_part820_identity_source_and_rights_match_the_dated_ecfr_snapshot():
    """The set identifies the specified public source and rights basis."""
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert f"clauses/{PART_820_FILE}" in manifest["clause_sets"]

    clause_set = _part820_set()
    assert clause_set["rights"] == {
        "structure": "citation_only",
        "text": "original",
        "clearance_ref": None,
        "licence": "Public domain: US federal regulation (17 U.S.C. 105)",
    }
    assert clause_set["source"] == {
        "title": "21 CFR Part 820 Quality Management System Regulation",
        "identifier": "21 CFR Part 820, Title 21 up to date as of 2026-11-12",
        "officialUrl": (
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-820"
        ),
    }
    assert clause_set_key(clause_set) == PART_820_KEY


@pytest.mark.trace("TC-070", "FR-014-AC-2")
def test_part820_clause_ids_match_the_normative_table_and_exclusions():
    """The selected clause IDs match the spec without reserved or excluded rows."""
    clause_set = _part820_set()
    expected_ids = {row[0] for row in _spec_rows()}
    actual_ids = [clause["id"] for clause in clause_set["clauses"]]

    assert len(actual_ids) == len(set(actual_ids)) == len(expected_ids)
    assert set(actual_ids) == expected_ids
    assert not {
        "820.1",
        "820.3",
        "820.5",
        "820.7",
        "820.10(e)",
        "820.35(d)",
    }.intersection(actual_ids)


@pytest.mark.trace("TC-071", "FR-014-AC-3")
def test_part820_clauses_match_force_outputs_and_ibr_treatment():
    """Each row is mandatory and declares the outputs and IBR boundary in the spec."""
    clause_set = _part820_set()
    expected = {
        row[0]: {
            "outputs": [value.strip("`") for value in row[2].split(", ")],
            "ibr": row[3],
        }
        for row in _spec_rows()
    }
    clauses = {clause["id"]: clause for clause in clause_set["clauses"]}
    titles = [clause["title"] for clause in clauses.values()]

    assert len(titles) == len(set(titles))
    for clause_id, clause in clauses.items():
        assert clause["force"] == "mandatory"
        assert clause["expectedOutputs"] == expected[clause_id]["outputs"]
        assert clause["expectedOutputs"]
        assert set(clause["expectedOutputs"]) <= set(clause_set["outputCatalog"])
        assert clause["title"].startswith(f"{clause_id} ")
        if expected[clause_id]["ibr"] == "yes":
            assert clause["text"] == IBR_TEXT
        else:
            assert clause["text"].strip()

    assert_output_catalog_consistent(load_clause_sets())


@pytest.mark.trace("TC-072", "FR-014-AC-4")
def test_part820_applicability_matches_the_normative_table_exactly():
    """Conditional expressions match the table and unconditional clauses have none."""
    _assert_applicability_matches_spec(_part820_set())


@pytest.mark.parametrize(
    ("clause_id", "mutation"),
    [
        ("820.10(b)(2)", "changed"),
        ("820.10(b)(2)", "missing"),
        ("820.10(a)", "added"),
    ],
)
@pytest.mark.trace("TC-072", "FR-014-AC-4")
def test_part820_applicability_fixture_errors_name_the_clause(clause_id, mutation):
    """Changed, missing, and unexpected expressions identify the affected clause."""
    clause_set = copy.deepcopy(_part820_set())
    clauses = {clause["id"]: clause for clause in clause_set["clauses"]}
    if mutation == "changed":
        clauses[clause_id]["applicability"]["value"] = "not_applicable"
    elif mutation == "missing":
        del clauses[clause_id]["applicability"]
    else:
        clauses[clause_id]["applicability"] = {
            "op": "eq",
            "dimension": "qmsr_traceability_applicability",
            "value": "applies",
        }

    with pytest.raises(AssertionError, match=re.escape(clause_id)):
        _assert_applicability_matches_spec(clause_set)


@pytest.mark.trace("TC-074", "FR-016-AC-1", "FR-016-AC-2")
def test_part820_human_dimensions_control_only_their_dependent_clauses():
    """Only supplied Part 820 dimensions resolve their dependent clauses."""
    dimensions = {
        "qmsr_traceability_applicability": "820.10(b)(2)",
        "qmsr_advisory_notice_applicability": "820.10(b)(4)",
        "qmsr_design_development_applicability": "820.10(c)",
        "qmsr_life_support_applicability": "820.10(d)",
        "qmsr_servicing_applicability": "820.35(b)",
    }
    all_applies = [f"{dimension}=applies" for dimension in dimensions]
    baseline = _outcomes(evaluate_clause_set(PACKAGE_ROOT, PART_820_KEY, *all_applies))
    assert set(baseline.values()) == {"binding"}

    missing_all = _outcomes(evaluate_clause_set(PACKAGE_ROOT, PART_820_KEY))
    unrelated_fact = _outcomes(
        evaluate_clause_set(PACKAGE_ROOT, PART_820_KEY, "device_class=class_II")
    )
    assert unrelated_fact == missing_all
    conditional_ids = set(dimensions.values())
    assert {key for key, value in missing_all.items() if value == "unresolved"} == (
        conditional_ids
    )
    assert {key for key, value in missing_all.items() if value == "binding"} == (
        set(baseline) - conditional_ids
    )

    for dimension, clause_id in dimensions.items():
        not_applicable = [
            f"{item}={'not_applicable' if item == dimension else 'applies'}"
            for item in dimensions
        ]
        excluded = _outcomes(
            evaluate_clause_set(PACKAGE_ROOT, PART_820_KEY, *not_applicable)
        )
        assert excluded[clause_id] == "not_binding"
        assert {key for key, value in excluded.items() if value == "binding"} == (
            set(baseline) - {clause_id}
        )

        omitted = [f"{item}=applies" for item in dimensions if item != dimension]
        unresolved = _outcomes(
            evaluate_clause_set(PACKAGE_ROOT, PART_820_KEY, *omitted)
        )
        assert unresolved[clause_id] == "unresolved"
        assert {key for key, value in unresolved.items() if value == "binding"} == (
            set(baseline) - {clause_id}
        )


@pytest.mark.trace("TC-073", "FR-014-AC-5")
def test_part820_spec_validates_and_module_passes_publish_check():
    """Quire validates the spec and the package publish check accepts the set."""
    artifact_module = pathlib.Path.home() / ".ix/filament/modules/spec-artifacts-iso"
    process_module = pathlib.Path.home() / ".ix/filament/modules/spec-artifacts-process"
    validation = run(
        engine_tool("quire"),
        "validate",
        "--scope",
        str(REPO_ROOT),
        "--module",
        str(artifact_module),
        "--module",
        str(process_module),
        "spec/**/*.md",
    )
    assert validation.returncode == 0, validation.stderr + validation.stdout
    publish = run(engine_tool("quire"), "publish-check", "--module", str(PACKAGE_ROOT))
    assert publish.returncode == 0, publish.stderr + publish.stdout

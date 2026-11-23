"""Packaging and shared behavior for the US health-law clause module."""

from __future__ import annotations

import json
import os
import pathlib
import re
import shutil
import subprocess
import tarfile
import tempfile
import zipfile
from urllib.parse import urlparse

import pytest
import yaml
from conftest import (
    CLAUSES_DIR,
    MANIFEST_PATH,
    PACKAGE_ROOT,
    REPO_ROOT,
    assert_output_catalog_consistent,
    clause_set_key,
    engine_tool,
    evaluate_clause_set,
    load_clause_sets,
    record_and_render_matrix,
    run,
    stage_clause_sets,
)

PART_11_FILE = "us-fda-21-cfr-11-2026-11-12.json"
PART_11_KEY = "us-fda/21-cfr-11@2026-11-12"
PART_820_FILE = "us-fda-21-cfr-820-2026-11-12.json"
PART_820_KEY = "us-fda/21-cfr-820@2026-11-12"
FDCA_524B_FILE = "us-congress-fdca-524b-2026-10-15.json"
FDCA_524B_KEY = "us-congress/fdca-524b@2026-10-15"
FDA_GUIDANCE_FILE = "us-fda-premarket-cybersecurity-2026-02-03.json"
FDA_GUIDANCE_KEY = "us-fda/premarket-cybersecurity@2026-02-03"
HIPAA_FILE = "us-hhs-45-cfr-164-subpart-c-2026-11-12.json"
HIPAA_KEY = "us-hhs/45-cfr-164-subpart-c@2026-11-12"
PREMARKET_SOFTWARE_FILE = "us-fda-premarket-device-software-2023-06-14.json"
PREMARKET_SOFTWARE_KEY = "us-fda/premarket-device-software@2023-06-14"


def _part_11_outcomes(binding: dict) -> dict[str, str]:
    return {clause["clauseId"]: clause["outcome"] for clause in binding["clauses"]}


def _spec_table(section_title: str) -> list[list[str]]:
    spec = (REPO_ROOT / "spec" / "spec.md").read_text()
    section = spec.split(f"### {section_title}", 1)[1].split("### ", 1)[0]
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


# Retained evidence-store kinds a catalog `producers` entry may name (quoin FR-211).
FR_211_FIXED_KINDS = {"run", "scan", "mock-inspection", "analysis-report", "scenario"}


def _spec_producers() -> dict[str, list[str]]:
    """Read the "US Output Producers" table: output name to its producer kinds."""
    return {
        name: [kind.strip("`") for kind in cell.split(", ")]
        for name, cell, _evidence in _spec_table("US Output Producers")
    }


def _canonical_catalog() -> dict[str, dict]:
    """The spec's catalog rows with their `producers` where the spec lists them."""
    producers = _spec_producers()
    catalog = {}
    for name, kind, description in _spec_table("US Health-Law Output Catalog"):
        entry = {"kind": kind, "description": description}
        if name in producers:
            entry["producers"] = producers[name]
        catalog[name] = entry
    return catalog


def _part_11_evaluate_error(module_root: pathlib.Path, *context: str):
    return run(
        engine_tool("quire"),
        "clauses",
        "evaluate",
        "--module",
        str(module_root),
        "--authority",
        "us-fda",
        "--set",
        "21-cfr-11",
        "--version",
        "2026-11-12",
        "--json",
        *[argument for entry in context for argument in ("--context", entry)],
    )


def _fdca_524b_evaluate_error(module_root: pathlib.Path, *context: str):
    return run(
        engine_tool("quire"),
        "clauses",
        "evaluate",
        "--module",
        str(module_root),
        "--authority",
        "us-congress",
        "--set",
        "fdca-524b",
        "--version",
        "2026-10-15",
        "--json",
        *[argument for entry in context for argument in ("--context", entry)],
    )


def _clause_outcomes(binding: dict) -> dict[str, str]:
    return {clause["clauseId"]: clause["outcome"] for clause in binding["clauses"]}


def _synthetic_set(key: str, output_catalog: dict) -> dict:
    authority, remainder = key.split("/")
    set_id, version = remainder.split("@")
    return {
        "authority": authority,
        "id": set_id,
        "version": version,
        "outputCatalog": output_catalog,
    }


@pytest.mark.trace("TC-002", "FR-001-AC-2")
def test_manifest_is_clause_only_and_lists_all_pack_sets():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert manifest["clause_sets"] == [
        f"clauses/{PART_11_FILE}",
        f"clauses/{PART_820_FILE}",
        f"clauses/{FDCA_524B_FILE}",
        f"clauses/{FDA_GUIDANCE_FILE}",
        f"clauses/{PREMARKET_SOFTWARE_FILE}",
        f"clauses/{HIPAA_FILE}",
    ]
    assert not {"object_types", "archetypes", "edges"}.intersection(manifest)


@pytest.mark.trace("TC-004", "FR-001-AC-4")
def test_quire_validates_the_module():
    artifact_module = pathlib.Path.home() / ".ix/filament/modules/spec-artifacts-iso"
    result = run(
        engine_tool("quire"),
        "validate",
        "--module",
        str(PACKAGE_ROOT),
        "--module",
        str(artifact_module),
        "spec/functional/*.md",
        "spec/non-functional/*.md",
        "spec/spec.md",
    )
    assert result.returncode == 0, result.stderr + result.stdout


@pytest.mark.trace("TC-002", "FR-001-AC-2", "TC-003", "FR-001-AC-3")
def test_local_quoin_install_has_no_object_or_artifact_contributions(tmp_path):
    """A local Quoin install reports the clause-only module shape.

    Assumptions:
        The module is installed into a fresh config root from this worktree.

    Criteria:
        The installed module is a path source with pack false and no object or
        artifact type contributions.

    Trace: FR-001-AC-2, FR-001-AC-3
    """
    home = tmp_path / "home"
    config_root = tmp_path / "config"
    home.mkdir()
    config_root.mkdir()
    env = {
        **os.environ,
        "HOME": str(home),
        "IX_CONFIG_ROOT": str(config_root),
    }
    installed = run(
        engine_tool("quoin"), "module", "install", f"path:{PACKAGE_ROOT}", env=env
    )
    assert installed.returncode == 0, installed.stderr + installed.stdout
    listed = run(engine_tool("quoin"), "module", "list", env=env)
    assert listed.returncode == 0, listed.stderr + listed.stdout
    modules = json.loads(listed.stdout)["plugins"]
    found = [
        module for module in modules if module.get("name") == "spec_clauses_us_health"
    ]
    assert len(found) == 1
    assert found[0]["source"]["type"] == "path"
    assert found[0]["pack"] is False
    catalog_after = run(engine_tool("quoin"), "catalog", "list", "--json", env=env)
    assert catalog_after.returncode == 0, catalog_after.stderr + catalog_after.stdout
    catalog_modules = json.loads(catalog_after.stdout)["modules"]
    (catalog_module,) = [
        module
        for module in catalog_modules
        if module.get("name") == "spec_clauses_us_health"
    ]
    assert catalog_module["objectTypes"] == []
    assert catalog_module["artifactTypes"] == []


@pytest.mark.trace("TC-028", "NFR-001-AC-2")
def test_every_declared_set_identifies_its_official_public_source():
    """Every manifest entry has source metadata for its official public source.

    Assumptions:
        The repository manifest selects all currently published US sets.

    Criteria:
        Every selected set maps to its expected official eCFR, US Code, or FDA URL.

    Trace: NFR-001-AC-2
    """
    expected_sources = {
        PART_11_KEY: (
            "eCFR",
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11",
        ),
        PART_820_KEY: (
            "eCFR",
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-820",
        ),
        FDCA_524B_KEY: (
            "US Code",
            "https://uscode.house.gov/us/usc/119-124/t21/s360n-2/",
        ),
        FDA_GUIDANCE_KEY: ("FDA guidance", "https://www.fda.gov/media/119933/download"),
        PREMARKET_SOFTWARE_KEY: (
            "FDA guidance",
            "https://www.fda.gov/regulatory-information/search-fda-guidance-"
            "documents/content-premarket-submissions-device-software-functions",
        ),
        HIPAA_KEY: (
            "eCFR",
            "https://www.ecfr.gov/on/2026-11-12/title-45/subtitle-A/"
            "subchapter-C/part-164/subpart-C",
        ),
    }
    actual_sources = {}
    for clause_set in load_clause_sets():
        key = clause_set_key(clause_set)
        source = clause_set.get("source")
        assert isinstance(source, dict), f"{key}: source metadata is missing"
        official_url = source.get("officialUrl")
        assert isinstance(official_url, str), f"{key}: official URL is missing"
        parsed_url = urlparse(official_url)
        assert parsed_url.scheme == "https", f"{key}: official URL is not HTTPS"
        if parsed_url.hostname == "www.ecfr.gov":
            source_kind = "eCFR"
        elif parsed_url.hostname == "uscode.house.gov":
            source_kind = "US Code"
        elif parsed_url.hostname == "www.fda.gov":
            source_kind = "FDA guidance"
        else:
            source_kind = f"unexpected host {parsed_url.hostname}"
        actual_sources[key] = (source_kind, official_url)

    assert actual_sources == expected_sources


@pytest.mark.trace("TC-052", "FR-012-AC-1")
def test_hipaa_set_identity_source_and_rights_match_the_dated_ecfr_snapshot():
    clause_set = next(
        item for item in load_clause_sets() if clause_set_key(item) == HIPAA_KEY
    )
    assert clause_set["schemaVersion"] == "clause-set-v1"
    assert clause_set["rights"] == {
        "structure": "citation_only",
        "text": "original",
        "clearance_ref": None,
        "licence": "Public domain: US federal regulation (17 U.S.C. 105)",
    }
    assert clause_set["source"] == {
        "title": (
            "45 CFR Part 164 Subpart C, Security Standards for the Protection of "
            "Electronic Protected Health Information"
        ),
        "identifier": "45 CFR Part 164 Subpart C",
        "officialUrl": "https://www.ecfr.gov/on/2026-11-12/title-45/subtitle-A/subchapter-C/part-164/subpart-C",
    }


@pytest.mark.trace("TC-053", "FR-012-AC-2")
def test_hipaa_clauses_match_the_normative_table_exactly():
    clause_set = next(
        item for item in load_clause_sets() if clause_set_key(item) == HIPAA_KEY
    )
    rows = _spec_table("HIPAA Security Rule Clause Table")
    expected = {
        row[0]: {
            "style": row[2],
            "outputs": [output.strip("`") for output in row[4].split(", ")],
        }
        for row in rows
    }
    clauses = {clause["id"]: clause for clause in clause_set["clauses"]}
    assert len(clauses) == len(clause_set["clauses"]) == len(expected)
    assert set(clauses) == set(expected)
    for clause_id, clause in clauses.items():
        assert clause["force"] == "mandatory"
        assert clause["styles"]["implementation"] == expected[clause_id]["style"]
        assert clause["expectedOutputs"] == expected[clause_id]["outputs"]
        assert set(clause["expectedOutputs"]) <= set(clause_set["outputCatalog"])
        assert clause["title"].strip() and clause["text"].strip()
    assert not any(clause_id.startswith("164.314(b)") for clause_id in clauses)
    assert clause_set["outputCatalog"] == {
        "security-controls": {
            "kind": "record",
            "description": (
                "`security.control` records; the clause set does not define a producer."
            ),
        },
        "security-risk-records": {
            "kind": "record",
            "description": "`spec-objects-security` threat, risk, and control records.",
        },
        "written-procedure": {
            "kind": "procedure",
            "description": "Customer-owned written procedure.",
        },
        "audit-logging": {
            "kind": "record",
            "description": (
                "`security.audit_event` records and associated retention evidence."
            ),
        },
        "health-data-flows": {
            "kind": "record",
            "description": (
                "Health-data flow projection produced by "
                "`quire relations --health-data-flows` from the declared "
                "architecture model."
            ),
        },
        "ephi-access-control": {
            "kind": "record",
            "description": (
                "Access-control records for the ePHI system: `spec-objects-security` "
                "`security.role`, `security.permission`, `security.auth_flow`, "
                "`security.mfa_method`, `security.password_policy` and "
                "`security.session_config` records the customer authors, or "
                "customer-supplied evidence; the clause set defines no producer."
            ),
        },
    }
    evaluated = evaluate_clause_set(PACKAGE_ROOT, HIPAA_KEY)
    assert set(_clause_outcomes(evaluated)) == set(expected)


@pytest.mark.trace("FR-012-AC-7")
def test_hipaa_access_and_audit_clauses_map_to_the_ephi_system_not_the_repository():
    clause_set = next(
        item for item in load_clause_sets() if clause_set_key(item) == HIPAA_KEY
    )
    outputs = {c["id"]: c["expectedOutputs"] for c in clause_set["clauses"]}
    assert not any(
        {"access-control", "audit-trail"} & set(names) for names in outputs.values()
    )
    assert not {"access-control", "audit-trail"} & set(clause_set["outputCatalog"])
    assert outputs["164.312(b)"] == ["audit-logging"]
    ephi = {
        "164.308(a)(3)(ii)(C)",
        "164.308(a)(4)(i)",
        "164.308(a)(4)(ii)(A)",
        "164.308(a)(4)(ii)(B)",
        "164.308(a)(4)(ii)(C)",
        "164.308(a)(5)(ii)(D)",
        "164.312(a)(1)",
        "164.312(a)(2)(i)",
        "164.312(a)(2)(ii)",
        "164.312(a)(2)(iii)",
        "164.312(d)",
    }
    assert {i for i, names in outputs.items() if "ephi-access-control" in names} == ephi
    assert "ephi-access-control" not in outputs["164.310(a)(2)(iii)"]
    assert outputs["164.312(a)(2)(iv)"] == ["security-controls"]


@pytest.mark.trace("TC-054", "FR-012-AC-3")
def test_hipaa_role_only_gates_business_associate_contract_clauses():
    clause_set = next(
        item for item in load_clause_sets() if clause_set_key(item) == HIPAA_KEY
    )
    assert clause_set["classificationDimensions"] == {
        "hipaa_role": {"values": ["covered_entity", "business_associate"]}
    }
    expected_ids = {row[0] for row in _spec_table("HIPAA Security Rule Clause Table")}
    covered_entity = _clause_outcomes(
        evaluate_clause_set(PACKAGE_ROOT, HIPAA_KEY, "hipaa_role=covered_entity")
    )
    business_associate = _clause_outcomes(
        evaluate_clause_set(PACKAGE_ROOT, HIPAA_KEY, "hipaa_role=business_associate")
    )
    missing = _clause_outcomes(evaluate_clause_set(PACKAGE_ROOT, HIPAA_KEY))
    ce_only = "164.314(a)(2)(ii)"
    ba_only = "164.314(a)(2)(iii)"
    both = expected_ids - {ce_only, ba_only}
    assert (
        set(covered_entity) == set(business_associate) == set(missing) == expected_ids
    )
    assert {
        key for key, value in covered_entity.items() if value == "binding"
    } == expected_ids - {ba_only}
    assert {
        key for key, value in business_associate.items() if value == "binding"
    } == expected_ids - {ce_only}
    assert {covered_entity[ba_only], business_associate[ce_only]} == {"not_binding"}
    assert all(
        covered_entity[key] == business_associate[key] == "binding" for key in both
    )
    assert missing[ce_only] == missing[ba_only] == "unresolved"
    assert all(missing[key] == "binding" for key in both)


@pytest.mark.trace("TC-060", "FR-015-AC-1")
def test_premarket_software_identity_source_and_rights_match_spec():
    """The clause set identifies only the dated public FDA guidance."""
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert f"clauses/{PREMARKET_SOFTWARE_FILE}" in manifest["clause_sets"]

    (clause_set,) = [
        item
        for item in load_clause_sets()
        if clause_set_key(item) == PREMARKET_SOFTWARE_KEY
    ]
    assert clause_set["rights"] == {
        "structure": "citation_only",
        "text": "original",
        "clearance_ref": None,
        "licence": "Public domain: U.S. Government guidance (17 U.S.C. 105)",
    }
    assert clause_set["source"] == {
        "title": "Content of Premarket Submissions for Device Software Functions",
        "identifier": "FDA Guidance for Industry and FDA Staff, issued 2023-06-14",
        "officialUrl": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-premarket-submissions-device-software-functions",
    }
    result = evaluate_clause_set(PACKAGE_ROOT, PREMARKET_SOFTWARE_KEY)
    assert result["clauseSet"] == {
        "authority": "us-fda",
        "id": "premarket-device-software",
        "version": "2023-06-14",
    }


@pytest.mark.trace("TC-061", "FR-015-AC-2")
def test_premarket_software_clause_ids_and_outputs_match_section_vi_table():
    """The complete Section VI clause and output set matches the specification."""
    clause_set = next(
        item
        for item in load_clause_sets()
        if clause_set_key(item) == PREMARKET_SOFTWARE_KEY
    )
    expected = {
        row[0]: {
            "outputs": [value.strip("`") for value in row[3].split(", ")],
            "applicability": row[2],
        }
        for row in _spec_table("M2 FDA Premarket Device-Software Guidance Clause Table")
    }
    clauses = {clause["id"]: clause for clause in clause_set["clauses"]}
    assert len(clauses) == len(clause_set["clauses"]) == len(expected)
    assert set(clauses) == set(expected)
    assert {
        clause_id: clause["expectedOutputs"] for clause_id, clause in clauses.items()
    } == {clause_id: row["outputs"] for clause_id, row in expected.items()}


@pytest.mark.trace("TC-062", "FR-015-AC-3")
def test_premarket_software_clauses_match_force_outputs_and_level_table():
    """Every recommendation has original text, catalog outputs, and declared gating."""
    clause_set = next(
        item
        for item in load_clause_sets()
        if clause_set_key(item) == PREMARKET_SOFTWARE_KEY
    )
    expected = {
        row[0]: {
            "outputs": [value.strip("`") for value in row[3].split(", ")],
            "applicability": row[2],
        }
        for row in _spec_table("M2 FDA Premarket Device-Software Guidance Clause Table")
    }
    clauses = {clause["id"]: clause for clause in clause_set["clauses"]}
    for clause_id, clause in clauses.items():
        assert clause["force"] == "recommended"
        assert clause["title"].strip() and clause["text"].strip()
        assert clause["expectedOutputs"] == expected[clause_id]["outputs"]
        assert clause["expectedOutputs"]
        assert set(clause["expectedOutputs"]) <= set(clause_set["outputCatalog"])
        assert clause["applicability"] == {
            "op": "at_least",
            "dimension": "documentation_level",
            "value": expected[clause_id]["applicability"]
            .split(" ")[-1]
            .strip("`")
            .strip(),
        }


@pytest.mark.trace("TC-063", "FR-015-AC-4")
def test_documentation_level_is_exactly_ordered_basic_then_enhanced():
    """The declared human-supplied levels have only the specified order."""
    clause_set = next(
        item
        for item in load_clause_sets()
        if clause_set_key(item) == PREMARKET_SOFTWARE_KEY
    )
    assert clause_set["classificationDimensions"] == {
        "documentation_level": {
            "values": ["basic", "enhanced"],
            "order": [["basic"], ["enhanced"]],
        }
    }


@pytest.mark.trace("TC-064", "FR-015-AC-5")
def test_premarket_software_module_validates_and_passes_publish_check():
    """The spec and publishability checks accept the completed module."""
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


@pytest.mark.trace("TC-065", "FR-016-AC-3", "FR-016-AC-4")
def test_premarket_software_level_evaluation_is_explicit_and_ordered():
    """Basic, enhanced, and missing levels produce the required outcomes."""
    expected_ids = {
        row[0]
        for row in _spec_table("M2 FDA Premarket Device-Software Guidance Clause Table")
    }
    enhanced_only = {"VI.F.enhanced", "VI.G.enhanced", "VI.H.enhanced"}
    for value, excluded in (("basic", enhanced_only), ("enhanced", set())):
        outcomes = _clause_outcomes(
            evaluate_clause_set(
                PACKAGE_ROOT, PREMARKET_SOFTWARE_KEY, f"documentation_level={value}"
            )
        )
        assert set(outcomes) == expected_ids
        assert {key for key, outcome in outcomes.items() if outcome == "binding"} == (
            expected_ids - excluded
        )
        if excluded:
            assert {outcomes[key] for key in excluded} == {"not_binding"}

    missing = _clause_outcomes(
        evaluate_clause_set(PACKAGE_ROOT, PREMARKET_SOFTWARE_KEY)
    )
    assert set(missing) == expected_ids
    assert set(missing.values()) == {"unresolved"}


@pytest.mark.trace("TC-066", "FR-016-AC-5")
def test_invalid_documentation_level_is_unresolved_with_dimension_diagnostic():
    """An undeclared level leaves clauses unresolved with a dimension diagnostic."""
    result = run(
        engine_tool("quire"),
        "clauses",
        "evaluate",
        "--module",
        str(PACKAGE_ROOT),
        "--authority",
        "us-fda",
        "--set",
        "premarket-device-software",
        "--version",
        "2023-06-14",
        "--context",
        "documentation_level=advanced",
        "--json",
    )
    assert result.returncode == 0, result.stderr + result.stdout
    binding = json.loads(result.stdout)
    assert set(_clause_outcomes(binding).values()) == {"unresolved"}
    assert all(
        any(
            reason["code"] == "unknown_value"
            and reason["dimension"] == "documentation_level"
            and '"advanced"' in reason["message"]
            for reason in clause["reasons"]
        )
        for clause in binding["clauses"]
    )


@pytest.mark.trace("TC-067", "FR-016-AC-3")
def test_basic_level_rmm_marks_enhanced_only_clause_not_applicable(tmp_path):
    """A basic-level report visibly excludes an enhanced-only recommendation."""
    result = record_and_render_matrix(
        tmp_path,
        PACKAGE_ROOT,
        PREMARKET_SOFTWARE_KEY,
        "documentation_level=basic",
        clause_id="VI.A",
    )
    assert result.returncode == 0, result.stderr + result.stdout
    assert r"VI.F.enhanced | Not applicable |" in result.stdout + result.stderr


def test_publish_check_accepts_all_declared_clause_sets():
    result = run(engine_tool("quire"), "publish-check", "--module", str(PACKAGE_ROOT))
    assert result.returncode == 0, result.stderr + result.stdout


def test_publish_check_rejects_a_licensed_synthetic_set(tmp_path):
    root = tmp_path / "module"
    clauses = root / "clauses"
    clauses.mkdir(parents=True)
    (root / "manifest.yaml").write_text(
        "manifest_version: 1.0.0\nname: rights-fixture\nversion: 0.0.1\n"
        "clause_sets:\n  - clauses/licensed.json\n"
    )
    fixture = {
        "schemaVersion": "clause-set-v1",
        "authority": "example.test",
        "id": "licensed-fixture",
        "title": "Synthetic rights fixture",
        "version": "1.0.0",
        "rights": {"structure": "citation_only", "text": "licensed"},
        "classificationDimensions": {},
        "outputCatalog": {},
        "clauses": [],
    }
    (clauses / "licensed.json").write_text(json.dumps(fixture))
    result = run(engine_tool("quire"), "publish-check", "--module", str(root))
    assert result.returncode == 2, result.stderr + result.stdout


@pytest.mark.trace("TC-018", "FR-005-AC-1", "FR-005-AC-6", "TC-043", "FR-010-AC-1")
def test_us_clause_set_output_catalog_matches_the_spec():
    names = [row[0] for row in _spec_table("US Health-Law Output Catalog")]
    assert len(names) == len(set(names)), "duplicate output catalog name in spec"
    catalog = _canonical_catalog()
    m1_names = {
        output.strip("`")
        for row in _spec_table("Part 11 Clause Table")
        for output in row[2].split(", ")
    }
    assert set(list(catalog)[:10]) <= m1_names

    for clause_set in load_clause_sets():
        used_names = {
            output
            for clause in clause_set["clauses"]
            for output in clause["expectedOutputs"]
        }
        undeclared = sorted(used_names - catalog.keys())
        assert not undeclared, (
            f"{clause_set_key(clause_set)} references outputs absent from the "
            f"normative catalog: {undeclared!r}"
        )
        assert clause_set["outputCatalog"] == {
            name: catalog[name] for name in sorted(used_names)
        }, f"{clause_set_key(clause_set)} output catalog differs from the spec"


@pytest.mark.trace("TC-019", "FR-005-AC-2", "TC-044", "FR-010-AC-2")
def test_catalog_consistency_error_names_both_conflicting_sets():
    sets = [
        _synthetic_set(
            "example.test/first@1.0.0",
            {
                "audit-trail": {"kind": "record", "description": "Git history."},
            },
        ),
        _synthetic_set(
            "example.test/second@1.0.0",
            {
                "audit-trail": {"kind": "procedure", "description": "Git history."},
            },
        ),
    ]
    with pytest.raises(
        AssertionError, match=r"example.test/first@1.0.0.*example.test/second@1.0.0"
    ):
        assert_output_catalog_consistent(sets)


@pytest.mark.trace("TC-020", "FR-005-AC-3")
def test_catalog_consistency_accepts_a_reused_definition():
    definition = {"kind": "record", "description": "Git history of the record."}
    assert_output_catalog_consistent(
        [
            _synthetic_set("example.test/first@1.0.0", {"audit-trail": definition}),
            _synthetic_set("example.test/second@1.0.0", {"audit-trail": definition}),
        ]
    )


@pytest.mark.trace("TC-030", "FR-005-AC-4")
def test_no_pack_level_output_catalog_is_declared():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert "output_catalog" not in manifest
    assert "outputCatalog" not in manifest


@pytest.mark.trace("TC-019", "FR-005-AC-2", "TC-044", "FR-010-AC-2")
def test_all_declared_sets_load_and_match_one_catalog():
    clause_sets = load_clause_sets()
    assert all(clause_set_key(item) for item in clause_sets)
    assert_output_catalog_consistent(clause_sets)
    catalog = _canonical_catalog()
    for clause_set in clause_sets:
        used_names = {
            name
            for clause in clause_set["clauses"]
            for name in clause["expectedOutputs"]
        }
        assert clause_set["outputCatalog"] == {
            name: catalog[name] for name in sorted(used_names)
        }, f"{clause_set_key(clause_set)} differs from the canonical output catalog"


@pytest.mark.trace("TC-032", "FR-008-AC-1")
def test_fdca_524b_identity_and_source_match_the_current_us_code():
    """Verify the 524B key, version, and official statute source.

    Assumptions: The source version is the US Code release point in force on
    2026-10-15.
    Criteria: The key and source metadata match the declared source.
    """
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert f"clauses/{FDCA_524B_FILE}" in manifest["clause_sets"]

    clause_set = next(
        item for item in load_clause_sets() if clause_set_key(item) == FDCA_524B_KEY
    )
    assert clause_set["source"] == {
        "title": "FD&C Act section 524B, Ensuring cybersecurity of devices",
        "identifier": "21 U.S.C. § 360n-2",
        "officialUrl": ("https://uscode.house.gov/us/usc/119-124/t21/s360n-2/"),
    }
    assert clause_set["version"] == "2026-10-15"
    result = _fdca_524b_evaluate_error(PACKAGE_ROOT)
    assert result.returncode == 0, result.stderr + result.stdout
    assert json.loads(result.stdout)["clauseSet"] == {
        "authority": "us-congress",
        "id": "fdca-524b",
        "version": "2026-10-15",
    }


@pytest.mark.trace("TC-033", "FR-008-AC-2")
def test_fdca_524b_contains_exactly_the_specified_clause_ids_and_outputs():
    """Compare the loaded 524B clause IDs and outputs with the spec table.

    Assumptions: The table in `spec.md` is the source of truth.
    Criteria: The set contains exactly the active clauses and output mappings
    listed in the specification, including paragraph (b)(4).
    """
    binding = _fdca_524b_evaluate_error(PACKAGE_ROOT)
    assert binding.returncode == 0, binding.stderr + binding.stdout

    expected = {
        row[0]: [output.strip("`") for output in row[2].split(", ")]
        for row in _spec_table("Section 524B Clause Table")
    }
    clauses = {
        entry["clauseId"]: entry for entry in json.loads(binding.stdout)["clauses"]
    }
    assert set(clauses) == set(expected)
    assert "524B(b)(4)" in clauses
    assert {
        clause_id: clause["expectedOutputs"] for clause_id, clause in clauses.items()
    } == expected


@pytest.mark.trace("TC-034", "FR-008-AC-3")
def test_fdca_524b_applicability_uses_only_the_user_supplied_classification():
    """Evaluate statutory clauses only from the supplied cyber-device value.

    Assumptions: The caller supplies `cyber_device` as yes or no.
    Criteria: Yes binds, no does not bind, and an absent value remains unresolved.
    """
    (clause_set,) = [
        item for item in load_clause_sets() if clause_set_key(item) == FDCA_524B_KEY
    ]
    assert clause_set["classificationDimensions"] == {
        "cyber_device": {"values": ["yes", "no"]},
        "additional_cybersecurity_regulation": {"values": ["issued", "none_issued"]},
    }

    expected_ids = {row[0] for row in _spec_table("Section 524B Clause Table")}
    statutory_ids = expected_ids - {"524B(b)(4)"}
    yes = _fdca_524b_evaluate_error(PACKAGE_ROOT, "cyber_device=yes")
    no = _fdca_524b_evaluate_error(PACKAGE_ROOT, "cyber_device=no")
    missing = _fdca_524b_evaluate_error(PACKAGE_ROOT)
    assert yes.returncode == 0, yes.stderr + yes.stdout
    assert no.returncode == 0, no.stderr + no.stdout
    assert missing.returncode == 0, missing.stderr + missing.stdout
    yes_outcomes = _clause_outcomes(json.loads(yes.stdout))
    assert {yes_outcomes[clause_id] for clause_id in statutory_ids} == {"binding"}
    assert yes_outcomes["524B(b)(4)"] == "unresolved"
    assert _clause_outcomes(json.loads(no.stdout)) == {
        clause_id: "not_binding" for clause_id in expected_ids
    }
    assert _clause_outcomes(json.loads(missing.stdout)) == {
        clause_id: "unresolved" for clause_id in expected_ids
    }


@pytest.mark.trace("TC-034", "FR-008-AC-3")
def test_fdca_524b_b4_applies_only_when_a_regulation_is_declared_issued():
    """524B(b)(4) is not binding until the user records an issued regulation.

    Assumptions: No regulation under paragraph (b)(4) has been issued; the user
    supplies `additional_cybersecurity_regulation`.
    Criteria: `none_issued` leaves the clause not binding, `issued` binds it,
    and neither value changes the other 524B clauses.
    """
    none_issued = json.loads(
        _fdca_524b_evaluate_error(
            PACKAGE_ROOT,
            "cyber_device=yes",
            "additional_cybersecurity_regulation=none_issued",
        ).stdout
    )
    issued = json.loads(
        _fdca_524b_evaluate_error(
            PACKAGE_ROOT,
            "cyber_device=yes",
            "additional_cybersecurity_regulation=issued",
        ).stdout
    )
    no_device_none_issued = json.loads(
        _fdca_524b_evaluate_error(
            PACKAGE_ROOT, "additional_cybersecurity_regulation=none_issued"
        ).stdout
    )
    no_device_outcomes = _clause_outcomes(no_device_none_issued)
    assert no_device_outcomes.pop("524B(b)(4)") == "not_binding"
    assert set(no_device_outcomes.values()) == {"unresolved"}
    assert _clause_outcomes(none_issued)["524B(b)(4)"] == "not_binding"
    assert _clause_outcomes(issued)["524B(b)(4)"] == "binding"
    for report in (none_issued, issued):
        others = {
            outcome
            for clause_id, outcome in _clause_outcomes(report).items()
            if clause_id != "524B(b)(4)"
        }
        assert others == {"binding"}


@pytest.mark.trace("TC-035", "FR-008-AC-4")
def test_fdca_524b_clauses_are_mandatory_and_use_declared_outputs():
    """Validate every 524B clause's required fields and output declarations.

    Assumptions: Quire validates the declared clause-set schema on evaluation.
    Criteria: Each clause is mandatory, has text and outputs, and loads.
    """
    clause_set = next(
        item for item in load_clause_sets() if clause_set_key(item) == FDCA_524B_KEY
    )
    assert all(clause["force"] == "mandatory" for clause in clause_set["clauses"])
    assert all(clause["expectedOutputs"] for clause in clause_set["clauses"])
    assert all(clause["text"].strip() for clause in clause_set["clauses"])
    assert all(clause["title"].strip() for clause in clause_set["clauses"])
    assert all(
        set(clause["expectedOutputs"]) <= set(clause_set["outputCatalog"])
        for clause in clause_set["clauses"]
    )
    evaluated = _fdca_524b_evaluate_error(PACKAGE_ROOT)
    assert evaluated.returncode == 0, evaluated.stderr + evaluated.stdout


@pytest.mark.trace("TC-036", "FR-008-AC-5")
def test_fdca_524b_does_not_infer_classification_and_reports_unknown_value(tmp_path):
    """Keep cyber-device classification caller-owned and reject unknown values.

    Assumptions: Unrelated context is not a declared classification dimension.
    Criteria: Unrelated facts do not resolve applicability, and an unknown
    cyber-device value produces an unresolved outcome with an unknown-value reason.
    """
    dimension_module = stage_clause_sets(
        tmp_path / "dimension", CLAUSES_DIR / FDCA_524B_FILE
    )
    extra_fact = _fdca_524b_evaluate_error(
        dimension_module, "unrelated_product_fact=yes"
    )
    assert extra_fact.returncode == 0, extra_fact.stderr + extra_fact.stdout
    assert set(_clause_outcomes(json.loads(extra_fact.stdout)).values()) == {
        "unresolved"
    }

    unknown_value = _fdca_524b_evaluate_error(PACKAGE_ROOT, "cyber_device=maybe")
    assert unknown_value.returncode == 0, unknown_value.stderr + unknown_value.stdout
    unknown_binding = json.loads(unknown_value.stdout)
    assert set(_clause_outcomes(unknown_binding).values()) == {"unresolved"}
    assert all(
        any(
            reason["code"] == "unknown_value" and reason["dimension"] == "cyber_device"
            for reason in clause["reasons"]
        )
        for clause in unknown_binding["clauses"]
    )


@pytest.mark.trace("TC-037", "FR-009-AC-1")
def test_fda_guidance_identity_and_source_match_the_current_guidance():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert f"clauses/{FDA_GUIDANCE_FILE}" in manifest["clause_sets"]

    (clause_set,) = [
        item for item in load_clause_sets() if clause_set_key(item) == FDA_GUIDANCE_KEY
    ]
    assert clause_set["rights"] == {
        "structure": "citation_only",
        "text": "original",
        "clearance_ref": None,
        "licence": "Public domain: U.S. Government guidance (17 U.S.C. 105)",
    }
    assert clause_set["source"] == {
        "title": (
            "Cybersecurity in Medical Devices: Quality Management System "
            "Considerations and Content of Premarket Submissions"
        ),
        "identifier": "FDA Guidance for Industry and FDA Staff, issued 2026-02-03",
        "officialUrl": "https://www.fda.gov/media/119933/download",
    }
    result = evaluate_clause_set(PACKAGE_ROOT, FDA_GUIDANCE_KEY)
    assert result["clauseSet"] == {
        "authority": "us-fda",
        "id": "premarket-cybersecurity",
        "version": "2026-02-03",
    }


@pytest.mark.trace("TC-038", "FR-009-AC-2")
def test_fda_guidance_clause_ids_and_outputs_match_the_specification():
    result = evaluate_clause_set(PACKAGE_ROOT, FDA_GUIDANCE_KEY)
    expected = {
        row[0]: [output.strip("`") for output in row[2].split(", ")]
        for row in _spec_table("FDA Premarket Cybersecurity Guidance Clause Table")
    }
    clauses = {entry["clauseId"]: entry for entry in result["clauses"]}
    assert set(clauses) == set(expected)
    assert {
        key: clause["expectedOutputs"] for key, clause in clauses.items()
    } == expected
    (clause_set,) = [
        item for item in load_clause_sets() if clause_set_key(item) == FDA_GUIDANCE_KEY
    ]
    section_v_a_5 = next(
        clause for clause in clause_set["clauses"] if clause["id"] == "V.A.5"
    )
    assert "anomal" in section_v_a_5["title"].lower()
    assert "anomal" in section_v_a_5["text"].lower()
    assert "known vulnerabilit" not in section_v_a_5["text"].lower()


@pytest.mark.trace("TC-039", "FR-009-AC-3")
def test_fda_guidance_clauses_are_recommended_and_use_declared_outputs():
    (clause_set,) = [
        item for item in load_clause_sets() if clause_set_key(item) == FDA_GUIDANCE_KEY
    ]
    assert all(clause["force"] == "recommended" for clause in clause_set["clauses"])
    assert all(
        clause["title"].strip() and clause["text"].strip()
        for clause in clause_set["clauses"]
    )
    assert all(clause["expectedOutputs"] for clause in clause_set["clauses"])
    assert all(
        set(clause["expectedOutputs"]) <= set(clause_set["outputCatalog"])
        for clause in clause_set["clauses"]
    )
    result = evaluate_clause_set(PACKAGE_ROOT, FDA_GUIDANCE_KEY)
    assert result["clauses"]


@pytest.mark.trace("TC-040", "FR-009-AC-4")
def test_fda_guidance_applicability_uses_only_the_supplied_cyber_device_value():
    (clause_set,) = [
        item for item in load_clause_sets() if clause_set_key(item) == FDA_GUIDANCE_KEY
    ]
    assert clause_set["classificationDimensions"] == {
        "cyber_device": {"values": ["yes", "no"]}
    }
    ids = {
        row[0]
        for row in _spec_table("FDA Premarket Cybersecurity Guidance Clause Table")
    }
    gated_ids = {"VII.C.1", "VII.C.2", "VII.C.3"}
    for value, expected in (("yes", "binding"), ("no", "not_binding")):
        result = evaluate_clause_set(
            PACKAGE_ROOT, FDA_GUIDANCE_KEY, f"cyber_device={value}"
        )
        outcomes = _clause_outcomes(result)
        assert set(outcomes) == ids
        assert {key for key, outcome in outcomes.items() if outcome == expected} == (
            ids if value == "yes" else gated_ids
        )
        assert all(outcomes[clause_id] == "binding" for clause_id in ids - gated_ids)

    missing = evaluate_clause_set(PACKAGE_ROOT, FDA_GUIDANCE_KEY)
    missing_outcomes = _clause_outcomes(missing)
    assert {missing_outcomes[key] for key in gated_ids} == {"unresolved"}
    assert all(missing_outcomes[key] == "binding" for key in ids - gated_ids)

    unrelated = evaluate_clause_set(
        PACKAGE_ROOT, FDA_GUIDANCE_KEY, "product_has_network=yes"
    )
    unrelated_outcomes = _clause_outcomes(unrelated)
    assert {unrelated_outcomes[key] for key in gated_ids} == {"unresolved"}
    assert all(unrelated_outcomes[key] == "binding" for key in ids - gated_ids)


def test_fda_guidance_rights_metadata_and_wording_are_citation_only():
    clause_path = CLAUSES_DIR / FDA_GUIDANCE_FILE
    raw = clause_path.read_text()
    clause_set = json.loads(raw)
    analysis = (
        REPO_ROOT / "reviews" / "plat-1596-source-rights-analysis.md"
    ).read_text()
    assert clause_set["rights"]["structure"] == "citation_only"
    assert clause_set["rights"]["text"] == "original"
    assert clause_set["rights"]["clearance_ref"] is None
    assert "https://www.fda.gov/media/119933/download" in analysis
    assert "17 U.S.C. 105" in analysis
    assert "no fda guidance text or paywalled standard text is reproduced" in " ".join(
        analysis.lower().split()
    )
    assert not re.search(r"\b(?:ISO|IEC|ANSI|AAMI|IEEE|NEMA|ASTM|UL)\s*[0-9]", raw)


@pytest.mark.trace("TC-042", "FR-009-AC-6")
@pytest.mark.trace("TC-046", "FR-010-AC-4")
def test_fda_guidance_sbom_clauses_use_the_catalogued_lifecycle_output():
    (clause_set,) = [
        item for item in load_clause_sets() if clause_set_key(item) == FDA_GUIDANCE_KEY
    ]
    clauses = {clause["id"]: clause for clause in clause_set["clauses"]}
    assert clauses["V.A.4"]["expectedOutputs"] == ["sbom"]
    assert clauses["VII.C.3"]["expectedOutputs"] == ["sbom"]
    description = clause_set["outputCatalog"]["sbom"]["description"]
    assert "support status" in description
    assert "end-of-support dates" in description
    assert "soup-list" not in clauses["V.A.4"]["expectedOutputs"]
    assert "soup-list" not in clauses["VII.C.3"]["expectedOutputs"]


def test_clause_files_ship_in_wheel_and_npm_tarball():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    shipped = [PACKAGE_ROOT / item for item in manifest["clause_sets"]]
    with tempfile.TemporaryDirectory() as tmp:
        built = subprocess.run(
            ["poetry", "build", "-f", "wheel", "-o", tmp],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        assert built.returncode == 0, built.stderr
        with zipfile.ZipFile(next(pathlib.Path(tmp).glob("*.whl"))) as archive:
            wheel_files = set(archive.namelist())
        packed = subprocess.run(
            ["npm", "pack", "--pack-destination", tmp],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            env={**os.environ, "npm_config_registry": "https://registry.npmjs.org/"},
        )
        assert packed.returncode == 0, packed.stderr
        with tarfile.open(next(pathlib.Path(tmp).glob("*.tgz"))) as archive:
            npm_files = set(archive.getnames())
    assert "spec_clauses_us_health/manifest.yaml" in wheel_files
    assert "package/manifest.yaml" in npm_files
    for path in shipped:
        relative = path.relative_to(PACKAGE_ROOT).as_posix()
        assert f"spec_clauses_us_health/{relative}" in wheel_files
        assert f"package/{relative}" in npm_files
    assert not (REPO_ROOT / "manifest.yaml").exists(), "postpack left staged files"
    assert not (REPO_ROOT / "clauses").exists(), "postpack left staged clauses"


def test_npm_pack_restores_preexisting_staging_paths(tmp_path):
    package = tmp_path / "package"
    package.mkdir()
    shutil.copy(REPO_ROOT / "package.json", package / "package.json")
    shutil.copy(REPO_ROOT / "README.md", package / "README.md")
    shutil.copy(REPO_ROOT / "LICENSE", package / "LICENSE")
    shutil.copytree(REPO_ROOT / "scripts", package / "scripts")
    shutil.copytree(PACKAGE_ROOT, package / PACKAGE_ROOT.name)

    original_manifest = b"previous module manifest\n\x00\xff"
    (package / "manifest.yaml").write_bytes(original_manifest)
    clauses = package / "clauses"
    (clauses / "nested").mkdir(parents=True)
    original_files = {
        "first.json": b"first clause bytes\x00",
        "nested/second.json": b"second clause bytes\xff",
    }
    for relative_path, contents in original_files.items():
        (clauses / relative_path).write_bytes(contents)

    packed = subprocess.run(
        ["npm", "pack", "--pack-destination", str(tmp_path)],
        cwd=package,
        capture_output=True,
        text=True,
        env={**os.environ, "npm_config_registry": "https://registry.npmjs.org/"},
    )
    assert packed.returncode == 0, packed.stderr
    assert (package / "manifest.yaml").read_bytes() == original_manifest
    restored = {
        path.relative_to(clauses).as_posix(): path.read_bytes()
        for path in clauses.rglob("*")
        if path.is_file()
    }
    assert restored == original_files
    assert (clauses / "nested").is_dir()
    assert not (package / ".npm-stage-backup").exists()


def test_markerless_backup_refuses_unowned_data_and_allows_retry(tmp_path):
    package = tmp_path / "package"
    scripts = package / "scripts"
    scripts.mkdir(parents=True)
    script = scripts / "stage-npm.mjs"
    shutil.copy(REPO_ROOT / "scripts" / "stage-npm.mjs", script)
    shutil.copytree(PACKAGE_ROOT, package / PACKAGE_ROOT.name)
    backup = package / ".npm-stage-backup"

    backup.mkdir()
    empty_cleanup = subprocess.run(
        ["node", str(script), "--clean"], capture_output=True, text=True
    )
    assert empty_cleanup.returncode == 0, empty_cleanup.stderr
    assert not backup.exists()

    backup.mkdir()
    unowned_file = backup / "keep.bin"
    unowned_bytes = b"unowned backup data\x00\xff"
    unowned_file.write_bytes(unowned_bytes)
    prepack = subprocess.run(["node", str(script)], capture_output=True, text=True)
    assert prepack.returncode != 0
    assert "inspect and remove the unowned data" in prepack.stderr
    assert "run --clean" not in prepack.stderr

    nonempty_cleanup = subprocess.run(
        ["node", str(script), "--clean"], capture_output=True, text=True
    )
    assert nonempty_cleanup.returncode != 0
    assert "inspect and remove the unowned data" in nonempty_cleanup.stderr
    assert unowned_file.read_bytes() == unowned_bytes

    unowned_file.unlink()
    retry_cleanup = subprocess.run(
        ["node", str(script), "--clean"], capture_output=True, text=True
    )
    assert retry_cleanup.returncode == 0, retry_cleanup.stderr
    assert not backup.exists()

    retry_prepack = subprocess.run(
        ["node", str(script)], capture_output=True, text=True
    )
    assert retry_prepack.returncode == 0, retry_prepack.stderr
    restored = subprocess.run(
        ["node", str(script), "--clean"], capture_output=True, text=True
    )
    assert restored.returncode == 0, restored.stderr
    assert not (package / "manifest.yaml").exists()
    assert not (package / "clauses").exists()


@pytest.mark.trace("TC-005", "TC-008", "FR-002-AC-1", "FR-003-AC-1")
def test_part_11_manifest_and_source_metadata_match_the_spec():
    """Description: Verify the Part 11 set identity, source, and rights metadata.

    Assumptions: The reviewed spec defines a public-law citation-only set.
    Criteria: Manifest, set key, source citation, and rights match that definition.
    """
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert manifest["clause_sets"] == [
        f"clauses/{PART_11_FILE}",
        f"clauses/{PART_820_FILE}",
        f"clauses/{FDCA_524B_FILE}",
        f"clauses/{FDA_GUIDANCE_FILE}",
        f"clauses/{PREMARKET_SOFTWARE_FILE}",
        f"clauses/{HIPAA_FILE}",
    ]

    clause_set = next(
        item for item in load_clause_sets() if clause_set_key(item) == PART_11_KEY
    )
    assert clause_set_key(clause_set) == PART_11_KEY
    assert clause_set["rights"] == {
        "structure": "citation_only",
        "text": "original",
        "clearance_ref": None,
        "licence": "Public domain: US federal regulation (17 U.S.C. 105)",
    }
    assert clause_set["source"] == {
        "title": "21 CFR Part 11 Electronic Records; Electronic Signatures",
        "identifier": "21 CFR Part 11",
        "officialUrl": (
            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11"
        ),
    }
    evaluated = _part_11_evaluate_error(PACKAGE_ROOT)
    assert evaluated.returncode == 0, evaluated.stderr
    assert json.loads(evaluated.stdout)["clauseSet"] == {
        "authority": "us-fda",
        "id": "21-cfr-11",
        "version": "2026-11-12",
    }


@pytest.mark.trace("TC-009", "FR-003-AC-2")
def test_part_11_contains_exactly_the_specified_clause_ids():
    """Description: Check clause IDs against the normative Part 11 table.

    Assumptions: The clause table in spec.md is the identifier source of truth.
    Criteria: Evaluated clause IDs equal the IDs listed in that table.
    """
    binding = evaluate_clause_set(PACKAGE_ROOT, PART_11_KEY)
    expected = {row[0] for row in _spec_table("Part 11 Clause Table")}
    assert {entry["clauseId"] for entry in binding["clauses"]} == expected


@pytest.mark.trace("TC-010", "FR-003-AC-3")
def test_part_11_clauses_are_mandatory_nonempty_and_loadable():
    """Description: Validate required clause fields and engine loadability.

    Assumptions: The Part 11 set contains the 25 normative table entries.
    Criteria: Every entry is mandatory, nonempty, has outputs, and evaluates.
    """
    clause_set = next(
        item for item in load_clause_sets() if clause_set_key(item) == PART_11_KEY
    )
    assert len(clause_set["clauses"]) == 25
    assert all(clause["force"] == "mandatory" for clause in clause_set["clauses"])
    assert all(clause["text"].strip() for clause in clause_set["clauses"])
    assert all(clause["expectedOutputs"] for clause in clause_set["clauses"])
    validated = _part_11_evaluate_error(PACKAGE_ROOT)
    assert validated.returncode == 0, validated.stderr + validated.stdout


@pytest.mark.trace("TC-011", "FR-003-AC-4")
def test_clause_with_undeclared_output_fails_and_names_the_clause(tmp_path):
    """Description: Reject a clause that references an undeclared output.

    Assumptions: Clause-set evaluation validates output references.
    Criteria: Evaluation fails and identifies the affected clause.
    """
    staged = stage_clause_sets(tmp_path, CLAUSES_DIR / PART_11_FILE)
    staged_path = staged / "clauses" / PART_11_FILE
    staged_set = json.loads(staged_path.read_text())
    next(clause for clause in staged_set["clauses"] if clause["id"] == "11.10(a)")[
        "expectedOutputs"
    ] = ["missing-output"]
    staged_path.write_text(json.dumps(staged_set))

    result = _part_11_evaluate_error(staged)
    assert result.returncode != 0
    assert "11.10(a)" in result.stderr + result.stdout


@pytest.mark.trace("TC-012", "FR-004-AC-1")
def test_closed_systems_bind_11_10_without_signatures_binding_elsewhere():
    """Description: Evaluate closed-system controls without electronic signatures.

    Assumptions: A closed system binds § 11.10 controls.
    Criteria: § 11.10 binds and clauses outside that section do not.
    """
    outcomes = _part_11_outcomes(
        evaluate_clause_set(
            PACKAGE_ROOT,
            PART_11_KEY,
            "system_type=closed",
            "electronic_signatures=not_used",
        )
    )
    assert all(outcomes[f"11.10({letter})"] == "binding" for letter in "abcdefghijk")
    assert all(
        outcome == "not_binding"
        for clause_id, outcome in outcomes.items()
        if not clause_id.startswith("11.10(")
    )


@pytest.mark.trace("TC-013", "FR-004-AC-2")
def test_open_system_controls_wait_for_per_paragraph_assessments():
    """Description: Keep open-system controls unresolved before assessment.

    Assumptions: Open-system applicability is supplied per § 11.10 paragraph.
    Criteria: § 11.10 and § 11.300 controls remain unresolved without those values.
    """
    outcomes = _part_11_outcomes(
        evaluate_clause_set(
            PACKAGE_ROOT,
            PART_11_KEY,
            "system_type=open",
            "electronic_signatures=used",
            "signature_basis=non_biometric",
        )
    )
    assert all(outcomes[f"11.10({letter})"] == "unresolved" for letter in "abcdefghijk")
    assert outcomes["11.30"] == "binding"
    assert outcomes["11.200(a)"] == "binding"
    assert all(outcomes[f"11.300({letter})"] == "unresolved" for letter in "abcde")


@pytest.mark.trace("TC-014", "FR-004-AC-3")
def test_open_system_assessments_resolve_only_the_named_control():
    """Description: Apply open-system assessments to their named controls only.

    Assumptions: Each assessment dimension maps to one § 11.10 paragraph.
    Criteria: Appropriate binds, not-appropriate does not bind, and others stay
    unresolved.
    """
    outcomes = _part_11_outcomes(
        evaluate_clause_set(
            PACKAGE_ROOT,
            PART_11_KEY,
            "system_type=open",
            "open_system_11_10_a_applicability=appropriate",
            "open_system_11_10_b_applicability=not_appropriate",
        )
    )
    assert outcomes["11.10(a)"] == "binding"
    assert outcomes["11.10(b)"] == "not_binding"
    assert outcomes["11.10(c)"] == "unresolved"


@pytest.mark.trace("TC-015", "FR-004-AC-4")
def test_nonbiometric_11_300_requires_identification_code_password():
    """Description: Gate § 11.300 on the selected non-biometric method.

    Assumptions: The user supplies signature basis and method.
    Criteria: Identification-code/password binds § 11.300; another method does not.
    """
    shared = (
        "electronic_signatures=used",
        "signature_basis=non_biometric",
    )
    identification = _part_11_outcomes(
        evaluate_clause_set(
            PACKAGE_ROOT,
            PART_11_KEY,
            *shared,
            "signature_method=identification_code_password",
        )
    )
    other = _part_11_outcomes(
        evaluate_clause_set(
            PACKAGE_ROOT,
            PART_11_KEY,
            *shared,
            "signature_method=other",
        )
    )
    assert all(identification[f"11.300({letter})"] == "binding" for letter in "abcde")
    assert all(other[f"11.300({letter})"] == "not_binding" for letter in "abcde")


@pytest.mark.trace("TC-016", "FR-004-AC-5")
def test_empty_context_leaves_every_part_11_clause_unresolved():
    """Description: Check default outcomes when applicability is unspecified.

    Assumptions: No context dimensions have inferred defaults.
    Criteria: All Part 11 clauses evaluate as unresolved.
    """
    outcomes = _part_11_outcomes(evaluate_clause_set(PACKAGE_ROOT, PART_11_KEY))
    assert set(outcomes.values()) == {"unresolved"}


@pytest.mark.trace("TC-017", "FR-004-AC-6")
def test_undeclared_applicability_dimensions_and_values_are_rejected(tmp_path):
    """Description: Reject undeclared applicability dimensions and values.

    Assumptions: The engine validates context against the set declaration.
    Criteria: Unknown dimension and unknown value each cause evaluation failure.
    """
    dimension_module = stage_clause_sets(
        tmp_path / "dimension", CLAUSES_DIR / PART_11_FILE
    )
    dimension_path = dimension_module / "clauses" / PART_11_FILE
    dimension_set = json.loads(dimension_path.read_text())
    dimension_set["clauses"][0]["applicability"]["terms"][1]["terms"][1][
        "dimension"
    ] = "not_declared"
    dimension_path.write_text(json.dumps(dimension_set))
    unknown_dimension = _part_11_evaluate_error(dimension_module)
    assert unknown_dimension.returncode != 0

    value_module = stage_clause_sets(tmp_path / "value", CLAUSES_DIR / PART_11_FILE)
    value_path = value_module / "clauses" / PART_11_FILE
    value_set = json.loads(value_path.read_text())
    value_set["clauses"][0]["applicability"]["terms"][1]["terms"][1]["value"] = "maybe"
    value_path.write_text(json.dumps(value_set))
    unknown_value = _part_11_evaluate_error(value_module)
    assert unknown_value.returncode != 0


@pytest.mark.trace("TC-031", "FR-003-AC-5")
def test_certification_clause_uses_the_fda_record_output():
    """Description: Check the § 11.100(c) output mapping.

    Assumptions: The output catalog identifies FDA certification evidence as a record.
    Criteria: § 11.100(c) declares the FDA certification record output.
    """
    clause_set = next(
        item for item in load_clause_sets() if clause_set_key(item) == PART_11_KEY
    )
    clause = next(
        entry for entry in clause_set["clauses"] if entry["id"] == "11.100(c)"
    )
    assert "fda-certification-record" in clause["expectedOutputs"]
    assert clause_set["outputCatalog"]["fda-certification-record"]["kind"] == "record"


@pytest.mark.trace("TC-006", "FR-002-AC-2")
def test_part_11_publish_check_accepts_the_original_text_module():
    """Description: Run publish-check on the original-text Part 11 module.

    Assumptions: Original summaries with public-law citations are publishable.
    Criteria: Publish-check exits successfully.
    """
    result = run(engine_tool("quire"), "publish-check", "--module", str(PACKAGE_ROOT))
    assert result.returncode == 0, result.stderr + result.stdout


@pytest.mark.trace("TC-007", "FR-002-AC-3")
def test_licensed_part_11_fixture_is_refused_with_its_set_key(tmp_path):
    """Description: Refuse a Part 11 fixture marked with licensed text.

    Assumptions: Publish-check enforces clause-set rights metadata.
    Criteria: The check fails and reports the affected set key.
    """
    staged = stage_clause_sets(tmp_path, CLAUSES_DIR / PART_11_FILE)
    staged_path = staged / "clauses" / PART_11_FILE
    staged_set = json.loads(staged_path.read_text())
    staged_set["rights"]["text"] = "licensed"
    staged_path.write_text(json.dumps(staged_set))

    result = run(engine_tool("quire"), "publish-check", "--module", str(staged))
    assert result.returncode == 2
    assert PART_11_KEY in result.stderr + result.stdout


@pytest.mark.trace("TC-026", "FR-007-AC-3")
def test_single_set_rmm_marks_one_direct_fact_compliant(tmp_path):
    """Description: Render one direct fact while retaining an undischarged control.

    Assumptions: A fact scoped to § 11.10(e) discharges only that clause.
    Criteria: § 11.10(e) is compliant and another applicable clause is not compliant.
    """
    result = record_and_render_matrix(
        tmp_path,
        PACKAGE_ROOT,
        PART_11_KEY,
        "system_type=closed",
        clause_id="11.10(e)",
    )
    assert result.returncode == 0, result.stderr + result.stdout
    output = result.stdout + result.stderr
    assert r"11.10\(e\) | Applicable | Compliant" in output
    assert r"11.10\(a\) | Applicable | Not compliant - undischarged" in output


@pytest.mark.trace("TC-085", "FR-005-AC-5")
def test_spec_producers_name_only_fr_211_kinds():
    """Every kind in the spec's producers table is an FR-211 family kind."""
    expected = _spec_producers()
    assert expected, "the spec lists no output with producers"
    for name, kinds in expected.items():
        assert kinds and set(kinds) <= FR_211_FIXED_KINDS, f"{name}: {kinds!r}"

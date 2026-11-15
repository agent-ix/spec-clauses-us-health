"""Packaging and shared behavior for the US health-law clause module."""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import tarfile
import tempfile
import zipfile

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


def _part_11_outcomes(binding: dict) -> dict[str, str]:
    return {clause["clauseId"]: clause["outcome"] for clause in binding["clauses"]}


def _spec_table(section_title: str) -> list[list[str]]:
    spec = (REPO_ROOT / "spec" / "spec.md").read_text()
    section = spec.split(f"### {section_title}", 1)[1].split("### ", 1)[0]
    rows = []
    for line in section.splitlines():
        if line.strip().startswith("| `") and line.count("|") == 4:
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            rows.append(
                [
                    cells[0].strip("`"),
                    *[cell.strip("`") for cell in cells[1:-1]],
                    cells[-1],
                ]
            )
    return rows


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
def test_manifest_is_clause_only_and_lists_the_part_11_set():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert manifest["clause_sets"] == [f"clauses/{PART_11_FILE}"]
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


@pytest.mark.trace("TC-002", "FR-001-AC-2")
def test_local_quoin_install_has_no_object_or_artifact_contributions(tmp_path):
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


def test_publish_check_accepts_the_empty_scaffold():
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


@pytest.mark.trace("TC-018", "FR-005-AC-1")
def test_us_clause_set_output_catalog_matches_the_spec():
    catalog = {
        name: {"kind": kind, "description": description}
        for name, kind, description in _spec_table("US Health-Law Output Catalog")
    }
    m1_names = list(
        dict.fromkeys(
            output.strip("`")
            for row in _spec_table("Part 11 Clause Table")
            for output in row[2].split(", ")
        )
    )
    assert len(catalog) == 18
    assert set(list(catalog)[: len(m1_names)]) == set(m1_names)

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


@pytest.mark.trace("TC-019", "FR-005-AC-2")
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


@pytest.mark.trace("TC-019", "FR-005-AC-2")
def test_all_declared_sets_load_and_match_one_catalog():
    clause_sets = load_clause_sets()
    assert all(clause_set_key(item) for item in clause_sets)
    assert_output_catalog_consistent(clause_sets)


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

    Assumptions: The reviewed spec defines one public-law citation-only set.
    Criteria: Manifest, set key, source citation, and rights match that definition.
    """
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert manifest["clause_sets"] == [f"clauses/{PART_11_FILE}"]

    (clause_set,) = load_clause_sets()
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
    (clause_set,) = load_clause_sets()
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
    (clause_set,) = load_clause_sets()
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

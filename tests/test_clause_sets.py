"""Packaging and shared behavior for the US health-law clause module."""

from __future__ import annotations

import json
import os
import pathlib
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
    load_clause_sets,
    run,
)

US_OUTPUT_CATALOG = {
    "audit-trail": ("record", "Git history of the record."),
    "signed-record": ("record", "Signed commit or tag verified by `git verify-commit` or `git verify-tag`."),
    "signer-registry": ("record", "Allowed-signers mapping from signing key to named person."),
    "signature-meaning": ("record", "The `Signed-off-meaning:` trailer."),
    "fda-certification-record": ("record", "Evidence that the electronic-signature certification was submitted to FDA."),
    "approval-trail": ("record", "Engineering-assurance approval-trail output."),
    "access-control": ("record", "Repository permission and branch-rule settings."),
    "system-validation": ("record", "Validation evidence for the toolchain's intended use."),
    "written-procedure": ("procedure", "Customer-owned written procedure."),
    "training-record": ("procedure", "Customer-owned training record."),
    "risk-management-records": ("record", "`spec-objects-safety` hazard, harm, risk-estimate, and residual-risk records."),
    "software-requirements": ("record", "Functional and non-functional requirements (FR/NFR)."),
    "software-architecture": ("record", "`spec-objects-architecture` parts and connections."),
    "verification-records": ("record", "Test matrix and retained evidence."),
    "soup-list": ("record", "Software of unknown provenance (SOUP) report."),
    "security-risk-records": ("record", "`spec-objects-security` threat, risk, and control records."),
    "anomaly-list": ("record", "Unresolved-anomaly report."),
    "release-record": ("record", "Engineering-assurance release decision."),
}


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
def test_manifest_is_clause_only_and_starts_with_no_clause_sets():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert manifest["clause_sets"] == []
    assert not {"object_types", "archetypes", "edges"}.intersection(manifest)


@pytest.mark.trace("TC-002", "FR-001-AC-2")
def test_quire_validates_the_module():
    result = run(engine_tool("quire"), "validate", "--module", str(PACKAGE_ROOT))
    assert result.returncode == 0, result.stderr + result.stdout


@pytest.mark.trace("TC-003", "FR-001-AC-3")
def test_local_quoin_install_reports_pack_false(tmp_path):
    env = {**os.environ, "HOME": str(tmp_path / "home")}
    pathlib.Path(env["HOME"]).mkdir()
    installed = run(
        engine_tool("quoin"), "module", "install", f"path:{PACKAGE_ROOT}", env=env
    )
    assert installed.returncode == 0, installed.stderr + installed.stdout
    listed = run(engine_tool("quoin"), "module", "list", "--json", env=env)
    assert listed.returncode == 0, listed.stderr + listed.stdout
    modules = json.loads(listed.stdout)
    found = [module for module in modules if module.get("name") == "spec_clauses_us_health"]
    assert len(found) == 1
    assert found[0]["pack"] is False


@pytest.mark.trace("TC-007", "NFR-001-AC-1")
def test_publish_check_accepts_the_empty_scaffold():
    result = run(engine_tool("quire"), "publish-check", "--module", str(PACKAGE_ROOT))
    assert result.returncode == 0, result.stderr + result.stdout


@pytest.mark.trace("TC-007", "NFR-001-AC-1")
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
def test_us_output_catalog_matches_the_spec_and_m1_prefix():
    assert len(US_OUTPUT_CATALOG) == 18
    assert list(US_OUTPUT_CATALOG)[:10] == [
        "audit-trail", "signed-record", "signer-registry", "signature-meaning",
        "fda-certification-record", "approval-trail", "access-control",
        "system-validation", "written-procedure", "training-record",
    ]
    spec = (REPO_ROOT / "spec" / "spec.md").read_text()
    rows = [
        line for line in spec.splitlines()
        if line.startswith("| `") and line.count("|") == 3
    ]
    actual = {}
    for row in rows:
        name, kind, description = (cell.strip() for cell in row.strip("|").split("|"))
        actual[name.strip("`")] = (kind.strip("`").strip(), description.strip())
    assert actual == US_OUTPUT_CATALOG


@pytest.mark.trace("TC-019", "FR-005-AC-2")
def test_catalog_consistency_error_names_both_conflicting_sets():
    sets = [
        _synthetic_set("example.test/first@1.0.0", {
            "audit-trail": {"kind": "record", "description": "Git history."},
        }),
        _synthetic_set("example.test/second@1.0.0", {
            "audit-trail": {"kind": "procedure", "description": "Git history."},
        }),
    ]
    with pytest.raises(AssertionError, match=r"example.test/first@1.0.0.*example.test/second@1.0.0"):
        assert_output_catalog_consistent(sets)


@pytest.mark.trace("TC-020", "FR-005-AC-3")
def test_catalog_consistency_accepts_a_reused_definition():
    definition = {"kind": "record", "description": "Git history of the record."}
    assert_output_catalog_consistent([
        _synthetic_set("example.test/first@1.0.0", {"audit-trail": definition}),
        _synthetic_set("example.test/second@1.0.0", {"audit-trail": definition}),
    ])


@pytest.mark.trace("TC-030", "FR-005-AC-4")
def test_no_pack_level_output_catalog_is_declared():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert "output_catalog" not in manifest
    assert "outputCatalog" not in manifest


def test_all_declared_sets_load_and_match_one_catalog():
    clause_sets = load_clause_sets()
    assert all(clause_set_key(item) for item in clause_sets)
    assert_output_catalog_consistent(clause_sets)


@pytest.mark.trace("TC-182")
def test_clause_files_ship_in_wheel_and_npm_tarball():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    shipped = [PACKAGE_ROOT / item for item in manifest["clause_sets"]]
    with tempfile.TemporaryDirectory() as tmp:
        built = subprocess.run(
            ["poetry", "build", "-f", "wheel", "-o", tmp], cwd=REPO_ROOT,
            capture_output=True, text=True,
        )
        assert built.returncode == 0, built.stderr
        with zipfile.ZipFile(next(pathlib.Path(tmp).glob("*.whl"))) as archive:
            wheel_files = set(archive.namelist())
        packed = subprocess.run(
            ["npm", "pack", "--pack-destination", tmp], cwd=REPO_ROOT,
            capture_output=True, text=True,
            env={**os.environ, "npm_config_registry": "https://registry.npmjs.org/"},
        )
        assert packed.returncode == 0, packed.stderr
        with tarfile.open(next(pathlib.Path(tmp).glob("*.tgz"))) as archive:
            npm_files = set(archive.getnames())
    for path in shipped:
        relative = path.relative_to(PACKAGE_ROOT).as_posix()
        assert f"spec_clauses_us_health/{relative}" in wheel_files
        assert f"package/{relative}" in npm_files
    assert not (REPO_ROOT / "manifest.yaml").exists(), "postpack left staged files"
    assert not (REPO_ROOT / "clauses").exists(), "postpack left staged clauses"

"""Publication rights and package lifecycle gates for the US health pack."""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess

import pytest
from conftest import (
    MANIFEST_PATH,
    PACKAGE_ROOT,
    REPO_ROOT,
    clause_set_key,
    engine_tool,
    load_clause_sets,
)


def _assert_pack_rights_metadata(clause_sets: list[dict]) -> None:
    """Require original text and a non-blank public-source basis per set."""
    for clause_set in clause_sets:
        key = clause_set_key(clause_set)
        rights = clause_set.get("rights")
        assert isinstance(rights, dict), f"{key}: rights metadata is missing"
        assert rights.get("text") == "original", f"{key}: rights.text is not original"
        licence = rights.get("licence")
        assert (
            isinstance(licence, str) and licence.strip()
        ), f"{key}: rights.licence public-source basis is missing or blank"


@pytest.mark.trace("TC-006", "FR-002-AC-2", "TC-027", "NFR-001-AC-1", "NFR-001-M-1")
def test_publish_check_accepts_the_real_module() -> None:
    """The real module publishes only when each declared set passes rights checks.

    Assumptions:
        The module manifest and clause files are the source selected for publish.

    Criteria:
        quire publish-check exits successfully on the complete module.

    Trace: FR-002-AC-2, NFR-001-AC-1, NFR-001-M-1
    """
    _assert_pack_rights_metadata(load_clause_sets())
    result = subprocess.run(
        [engine_tool("quire"), "publish-check", "--module", str(PACKAGE_ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout


@pytest.mark.trace("TC-027", "NFR-001-M-1")
def test_pack_rights_metadata_check_rejects_a_blank_public_source_basis() -> None:
    """The pack metadata check names a set whose public-source basis is blank.

    Assumptions:
        Clause-set rights fields are structured metadata, not authored prose.

    Criteria:
        The pack assertion rejects a blank rights.licence and identifies its set.
        Quire separately refuses sets whose rights.text is restricted.

    Trace: NFR-001-M-1
    """
    clause_sets = load_clause_sets()
    clause_sets[0]["rights"]["licence"] = "  "
    set_key = clause_set_key(clause_sets[0])

    with pytest.raises(AssertionError, match=set_key) as error:
        _assert_pack_rights_metadata(clause_sets)
    assert "rights.licence" in str(error.value)


@pytest.mark.trace("TC-007", "FR-002-AC-3")
def test_publish_check_rejects_licensed_fixture_and_names_the_set(
    tmp_path: pathlib.Path,
) -> None:
    """A licensed fixture is refused with its exact public set key.

    Assumptions:
        The fixture is synthetic and contains no source text.

    Criteria:
        Quire exits 2 and reports the authority, ID, and version.

    Trace: FR-002-AC-3
    """
    module = tmp_path / "module"
    clauses = module / "clauses"
    clauses.mkdir(parents=True)
    (module / "manifest.yaml").write_text(
        "manifest_version: 1.0.0\nname: rights-fixture\nversion: 0.0.1\n"
        "clause_sets:\n  - clauses/licensed.json\n"
    )
    fixture = {
        "schemaVersion": "clause-set-v1",
        "authority": "example.invalid",
        "id": "licensed-fixture",
        "title": "Synthetic rights fixture",
        "version": "0.1.0",
        "rights": {"structure": "citation_only", "text": "licensed"},
        "classificationDimensions": {},
        "outputCatalog": {},
        "clauses": [],
    }
    (clauses / "licensed.json").write_text(json.dumps(fixture))

    result = subprocess.run(
        [engine_tool("quire"), "publish-check", "--module", str(module)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2, result.stderr + result.stdout
    assert "example.invalid/licensed-fixture@0.1.0" in result.stderr + result.stdout


def test_npm_pack_dry_run_restores_staged_module_paths() -> None:
    """A dry-run package uses the stage lifecycle and restores its worktree.

    Assumptions:
        npm runs prepack and postpack for a dry-run package.

    Criteria:
        Packaging exits successfully and leaves no staged root module paths;
        package metadata keeps public access without overriding npm's registry.

    """
    package_metadata = json.loads((REPO_ROOT / "package.json").read_text())
    assert package_metadata["publishConfig"] == {"access": "public"}

    result = subprocess.run(
        ["npm", "pack", "--dry-run", "--json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    assert not (REPO_ROOT / "manifest.yaml").exists()
    assert not (REPO_ROOT / "clauses").exists()
    assert MANIFEST_PATH.is_file()


def test_npm_pack_dry_run_restores_preexisting_payload_bytes(
    tmp_path: pathlib.Path,
) -> None:
    """Dry-run staging restores pre-existing payload paths byte-for-byte.

    Assumptions:
        The isolated package copy contains the real package lifecycle and module.

    Criteria:
        npm pack succeeds and restores the original manifest and nested clauses.
    """
    package = tmp_path / "package"
    package.mkdir()
    for name in ("package.json", "README.md", "LICENSE"):
        shutil.copy2(REPO_ROOT / name, package / name)
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

    result = subprocess.run(
        ["npm", "pack", "--dry-run", "--json"],
        cwd=package,
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "npm_config_registry": "https://registry.npmjs.org/",
        },
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    assert (package / "manifest.yaml").read_bytes() == original_manifest
    restored_files = {
        path.relative_to(clauses).as_posix(): path.read_bytes()
        for path in clauses.rglob("*")
        if path.is_file()
    }
    assert restored_files == original_files
    assert (clauses / "nested").is_dir()
    assert not (package / ".npm-stage-backup").exists()

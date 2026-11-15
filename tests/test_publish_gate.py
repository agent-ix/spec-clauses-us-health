"""Publication rights and package lifecycle gates for the US health pack."""

from __future__ import annotations

import json
import pathlib
import subprocess

import pytest

from conftest import MANIFEST_PATH, PACKAGE_ROOT, REPO_ROOT, engine_tool


@pytest.mark.trace("TC-006", "FR-002-AC-2", "TC-027", "NFR-001-AC-1")
def test_publish_check_accepts_the_real_module() -> None:
    """The real module publishes only when each declared set passes rights checks.

    Assumptions:
        The module manifest and clause files are the source selected for publish.

    Criteria:
        quire publish-check exits successfully on the complete module.

    Trace: FR-002-AC-2, NFR-001-AC-1
    """
    result = subprocess.run(
        [engine_tool("quire"), "publish-check", "--module", str(PACKAGE_ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout


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
        Packaging exits successfully and leaves no staged root module paths.

    """
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

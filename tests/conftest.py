"""Shared test helpers for US health-law clause sets."""

from __future__ import annotations

import json
import pathlib
import re
import shutil
import subprocess

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKAGE_ROOT = REPO_ROOT / "spec_clauses_us_health"
MANIFEST_PATH = PACKAGE_ROOT / "manifest.yaml"
CLAUSES_DIR = PACKAGE_ROOT / "clauses"


def m2_mapping_rows(spec_root: pathlib.Path = REPO_ROOT) -> list[dict[str, object]]:
    """Read the normative M2 output mapping table from the master specification."""
    spec = (spec_root / "spec" / "spec.md").read_text()
    section = spec.split("### M2 Output Producer Mapping", 1)[1].split("### ", 1)[0]
    rows = []
    for line in section.splitlines():
        if not line.strip().startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        clause_ids = tuple(re.findall(r"`([^`]+)`", cells[0]))
        output_name = cells[1].strip("`")
        if not clause_ids or not output_name:
            continue
        rows.append(
            {
                "clause_ids": clause_ids,
                "output": output_name,
                "kind": cells[2].strip("`"),
                "producer_or_owner": cells[3],
            }
        )
    return rows


def resolve_fact_refs(repo: pathlib.Path, facts: list[dict]) -> None:
    """Require each fact reference to resolve inside the synthetic corpus."""
    for fact in facts:
        refs = fact.get("evidenceRefs", [])
        if fact.get("approvalRef"):
            refs = [*refs, fact["approvalRef"]]
        for reference in refs:
            relative = (
                reference.removeprefix("evidence://example.invalid/")
                if reference.startswith("evidence://example.invalid/")
                else reference
            )
            path = (repo / relative).resolve()
            assert path.is_relative_to(
                repo.resolve()
            ), f"{fact['clauseId']}: evidence ref escapes the corpus: {reference}"
            assert (
                path.is_file()
            ), f"{fact['clauseId']}: evidence ref does not resolve: {reference}"


def engine_tool(name: str) -> str:
    """Find one installed engine CLI, preferring a repository-local install."""
    local = REPO_ROOT / "node_modules" / ".bin" / name
    path = str(local) if local.exists() else shutil.which(name)
    if path is None:
        pytest.fail(f"the `{name}` CLI is not installed or available on PATH")
    return path


def load_clause_sets(manifest_path: pathlib.Path = MANIFEST_PATH) -> list[dict]:
    """Load all clause-set JSON files declared by a module manifest."""
    manifest = yaml.safe_load(manifest_path.read_text())
    package_root = manifest_path.parent
    return [
        json.loads((package_root / relative_path).read_text())
        for relative_path in manifest.get("clause_sets", [])
    ]


def clause_set_key(clause_set: dict) -> str:
    return f"{clause_set['authority']}/{clause_set['id']}@{clause_set['version']}"


def run(*args: str, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, **kwargs)


def evaluate_clause_set(module_root: pathlib.Path, key: str, *context: str) -> dict:
    authority, rest = key.split("/")
    set_id, version = rest.split("@")
    args = [
        engine_tool("quire"),
        "clauses",
        "evaluate",
        "--module",
        str(module_root),
        "--authority",
        authority,
        "--set",
        set_id,
        "--version",
        version,
        "--json",
    ]
    for entry in context:
        args.extend(["--context", entry])
    result = run(*args)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def stage_clause_sets(
    tmp_path: pathlib.Path,
    *files: pathlib.Path,
    module_name: str = "staged-clause-sets",
    module_version: str = "0.0.1",
) -> pathlib.Path:
    """Create an isolated clause module from supplied set files."""
    root = tmp_path / "staged-module"
    clauses_dir = root / "clauses"
    clauses_dir.mkdir(parents=True)
    for path in files:
        shutil.copy(path, clauses_dir / path.name)
    entries = "".join(f"  - clauses/{path.name}\n" for path in files)
    (root / "manifest.yaml").write_text(
        "manifest_version: 1.0.0\n"
        f"name: {module_name}\n"
        f"version: {module_version}\n"
        f"clause_sets:\n{entries}"
    )
    return root


def record_and_render_matrix(
    tmp_path: pathlib.Path,
    module_root: pathlib.Path,
    key: str,
    *context: str,
    clause_id: str,
) -> subprocess.CompletedProcess:
    """Record one synthetic discharge in a temporary store and render its RMM."""
    binding = evaluate_clause_set(module_root, key, *context)
    binding_path = tmp_path / "binding.json"
    binding_path.write_text(json.dumps(binding))
    facts_path = tmp_path / "facts.json"
    facts_path.write_text(
        json.dumps(
            [
                {
                    "kind": "direct",
                    "clauseId": clause_id,
                    "evidenceRefs": ["evidence://example.invalid/run/one"],
                    "attestation": {
                        "attestedBy": "reviewer",
                        "authority": "quality-lead",
                        "attestedAt": "2026-11-01T00:00:00Z",
                        "expiresAt": "2027-11-01T00:00:00Z",
                    },
                }
            ]
        )
    )
    repo = tmp_path / "evidence-store"
    repo.mkdir()
    recorded = run(
        engine_tool("quoin"),
        "evidence",
        "record-discharge",
        "--repo",
        str(repo),
        "--binding",
        str(binding_path),
        "--facts",
        str(facts_path),
    )
    assert recorded.returncode == 0, recorded.stderr
    return run(
        engine_tool("quoin"),
        "discharge",
        "--binding",
        str(binding_path),
        "--rmm",
        "--repo",
        str(repo),
        "--as-of",
        "2026-11-14T00:00:00Z",
    )


def assert_output_catalog_consistent(clause_sets: list[dict]) -> None:
    """Reject output kind/description drift across sets, naming both sets."""
    definitions: dict[str, tuple[dict, dict]] = {}
    for clause_set in clause_sets:
        current_key = clause_set_key(clause_set)
        for name, definition in clause_set.get("outputCatalog", {}).items():
            previous = definitions.get(name)
            if previous and previous[1] != definition:
                previous_key = clause_set_key(previous[0])
                raise AssertionError(
                    f"output {name!r} differs between {previous_key} and {current_key}"
                )
            definitions[name] = (clause_set, definition)

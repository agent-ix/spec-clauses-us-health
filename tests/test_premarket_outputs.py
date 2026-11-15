"""M2 clause outputs are connected to producers or tracked owners."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
import yaml
from conftest import (
    assert_output_catalog_consistent,
    clause_set_key,
    engine_tool,
    load_clause_sets,
    m2_mapping_rows,
)

PART_820_KEY = "us-fda/21-cfr-820@2026-11-12"
PREMARKET_KEY = "us-fda/premarket-device-software@2023-06-14"
M2_KEYS = {PART_820_KEY, PREMARKET_KEY}

MODULE_EVIDENCE = {
    "risk-management-records": {
        "spec-objects-safety": {"object_types": {"hazard", "failure_mode"}}
    },
    "software-requirements": {
        "spec-artifacts-iso": {"composition": {"StR", "FR", "NFR"}}
    },
    "software-architecture": {
        "spec-objects-architecture": {
            "object_types": {"part", "port", "connection", "allocation"}
        },
        "spec-artifacts-process": {"artifact_types": {"ADR"}},
    },
}

COMMAND_EVIDENCE = {
    "risk-management-records": (("quoin", "risk-summary"),),
    "verification-records": (
        ("quire", "matrix"),
        ("quoin", "matrix"),
        ("quoin", "evidence", "record"),
    ),
    "release-record": (("quoin", "release", "snapshot"),),
    "anomaly-list": (("quoin", "anomaly", "report"),),
}


def _installed_module_manifests() -> dict[str, tuple[Path, dict]]:
    """Load manifests from the modules that the installed Quoin resolves."""
    result = subprocess.run(
        [engine_tool("quoin"), "module", "list"],
        check=True,
        capture_output=True,
        text=True,
    )
    installed = json.loads(result.stdout)
    manifests = {}
    for module in installed["plugins"]:
        root = Path(module.get("resolvedPath") or module["targetPath"])
        manifest_path = root / "manifest.yaml"
        if manifest_path.is_file():
            manifests[module["name"]] = (
                manifest_path,
                yaml.safe_load(manifest_path.read_text()),
            )
    return manifests


def _declared_names(manifest: dict, key: str) -> set[str]:
    return {entry["name"] for entry in manifest.get(key, [])}


def _declared_composition(manifest: dict) -> set[str]:
    return {
        artifact
        for archetype in manifest.get("archetypes", [])
        for artifact in archetype.get("composition", {}).get("expected_artifacts", [])
    }


def _assert_command_exists(command: tuple[str, ...]) -> None:
    """Require each mapped producer command to appear in its installed CLI help."""
    result = subprocess.run(
        [engine_tool(command[0]), *command[1:], "--help"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert (
        command[-1] in result.stdout
    ), f"producer command {' '.join(command)} is absent from its CLI help"


def _assert_producer_source_evidence(output: str, mapping: str) -> None:
    """Resolve each mapped producer to an installed manifest or CLI entrypoint."""
    manifests = _installed_module_manifests()
    assert (
        output in MODULE_EVIDENCE or output in COMMAND_EVIDENCE
    ), f"{output}: producer has no source-evidence strategy"

    for module_name, declarations in MODULE_EVIDENCE.get(output, {}).items():
        assert module_name in mapping, f"{output}: mapping omits {module_name}"
        assert module_name in manifests, f"{output}: {module_name} is not installed"
        manifest_path, manifest = manifests[module_name]
        for declaration, expected in declarations.items():
            if declaration == "composition":
                actual = _declared_composition(manifest)
            else:
                actual = _declared_names(manifest, declaration)
            assert expected <= actual, (
                f"{output}: {manifest_path} lacks {declaration} "
                f"{sorted(expected - actual)}"
            )
            for entrypoint in expected:
                assert (
                    entrypoint.casefold() in mapping.casefold()
                ), f"{output}: mapping omits declared entrypoint {entrypoint!r}"

    for command in COMMAND_EVIDENCE.get(output, ()):
        assert (
            " ".join(command).casefold() in mapping.casefold()
        ), f"{output}: mapping omits producer command {' '.join(command)!r}"
        _assert_command_exists(command)


def _m2_sets() -> list[dict]:
    """Return the Part 820 and premarket sets declared by the module."""
    return [
        clause_set
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) in M2_KEYS
    ]


@pytest.mark.trace("TC-075", "FR-018-AC-1")
def test_m2_output_mapping_covers_every_clause_output_pair_once():
    """The mapping table equals the M2 clause tables without duplicate pairs."""
    expected_pairs = {
        (clause["id"], output)
        for clause_set in _m2_sets()
        for clause in clause_set["clauses"]
        for output in clause["expectedOutputs"]
    }
    rows = m2_mapping_rows()
    mapped_pairs = [
        (clause_id, row["output"]) for row in rows for clause_id in row["clause_ids"]
    ]

    assert len(mapped_pairs) == len(
        set(mapped_pairs)
    ), "the mapping repeats a clause/output pair"
    assert set(mapped_pairs) == expected_pairs, (
        f"missing {sorted(expected_pairs - set(mapped_pairs))}; "
        f"extra {sorted(set(mapped_pairs) - expected_pairs)}"
    )


@pytest.mark.trace("TC-076", "FR-018-AC-2")
def test_m2_record_outputs_name_a_producer_or_owner_ticket():
    """Each M2 record description matches its current producer or tracked owner."""
    rows = m2_mapping_rows()
    by_output = {row["output"]: row for row in rows}
    assert len(by_output) == len(rows), "each output must have one mapping row"

    for clause_set in _m2_sets():
        for output, definition in clause_set["outputCatalog"].items():
            row = by_output[output]
            assert row["kind"] == definition["kind"], output
            mapping = str(row["producer_or_owner"])
            description = definition["description"]

            if definition["kind"] == "record":
                if "No producer on `origin/main`" in mapping:
                    assert "owner PLAT-1762" in mapping, output
                    assert "PLAT-1762" in description, output
                else:
                    assert mapping in description or description in mapping, output
                    _assert_producer_source_evidence(output, mapping)
            elif definition["kind"] == "document":
                assert "Customer-provided" in mapping, output
                assert "no toolchain producer" in mapping, output
            else:
                assert definition["kind"] == "procedure", output
                assert "Customer-owned" in mapping, output
                assert "no toolchain producer" in mapping, output


@pytest.mark.trace("TC-077", "FR-018-AC-3")
def test_shared_output_catalog_definitions_are_identical_across_us_sets():
    """Reused outputs keep the same kind and description throughout the module."""
    assert_output_catalog_consistent(load_clause_sets())

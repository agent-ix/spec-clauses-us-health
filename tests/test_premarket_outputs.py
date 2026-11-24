"""M2 clause outputs are connected to producers or marked customer-provided."""

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


@pytest.mark.trace("FR-018-AC-1")
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


M2_DOSSIER_KINDS = {
    "software-requirements": ("srs",),
    "software-architecture": ("architecture",),
    "verification-records": ("verification-report", "trace-matrix"),
    "risk-management-records": ("risk-management",),
    "release-record": ("release-record",),
    "anomaly-list": ("anomalies",),
}
# Outputs the customer supplies; the toolchain has no producer for them.
M2_CUSTOMER_DOCUMENTS = {
    "documentation-level-decision",
    "software-description",
    "software-design",
    "configuration-management-plan",
}
M2_CUSTOMER_RECORDS = {
    "device-identification-record",
    "traceability-records",
    "complaint-records",
    "regulatory-report-records",
    "advisory-notice-records",
    "service-records",
    "labeling-inspection-records",
}
M2_CUSTOMER_PROCEDURES = {"written-procedure"}


def _m2_output_catalog() -> dict[str, dict]:
    catalog: dict[str, dict] = {}
    for clause_set in _m2_sets():
        catalog.update(clause_set["outputCatalog"])
    return catalog


@pytest.mark.trace("FR-018-AC-2")
def test_every_m2_output_is_in_exactly_one_class():
    """Each M2 output is a produced record or a customer document or procedure."""
    classes = [
        set(MODULE_EVIDENCE) | set(COMMAND_EVIDENCE),
        M2_CUSTOMER_RECORDS,
        M2_CUSTOMER_DOCUMENTS,
        M2_CUSTOMER_PROCEDURES,
    ]
    assert sum(len(names) for names in classes) == len(set().union(*classes))
    assert set(_m2_output_catalog()) == set().union(*classes)


@pytest.mark.trace("FR-018-AC-2", "FR-018-AC-4")
def test_m2_record_outputs_name_producers_that_exist(tmp_path):
    """Each produced record names installed commands, modules and dossier kinds."""
    rows = {row["output"]: row for row in m2_mapping_rows()}
    dossier_kinds = _dossier_kinds(tmp_path)
    for output, definition in _m2_output_catalog().items():
        if output not in set(MODULE_EVIDENCE) | set(COMMAND_EVIDENCE):
            continue
        mapping = str(rows[output]["producer_or_owner"])
        assert definition["kind"] == rows[output]["kind"] == "record", output
        assert definition["description"].rstrip(".") in mapping, output
        _assert_producer_source_evidence(output, mapping)
        for kind in M2_DOSSIER_KINDS.get(output, ()):
            assert f"--doc {kind}" in mapping, output
            assert kind in dossier_kinds, f"{output}: no {kind} dossier kind"
    for output in M2_DOSSIER_KINDS:
        assert "quoin dossier generate" in rows[output]["producer_or_owner"], output


@pytest.mark.trace("FR-018-AC-2")
def test_m2_outputs_without_a_producer_are_customer_provided():
    """Documents and procedures the toolchain cannot produce are customer-owned."""
    catalog = _m2_output_catalog()
    rows = {row["output"]: row for row in m2_mapping_rows()}
    for output in M2_CUSTOMER_DOCUMENTS:
        assert catalog[output]["kind"] == rows[output]["kind"] == "document", output
        assert catalog[output]["description"].startswith("Customer-provided"), output
        assert "no toolchain producer" in catalog[output]["description"], output
        assert "Customer-provided" in rows[output]["producer_or_owner"], output
        assert "no toolchain producer" in rows[output]["producer_or_owner"], output
    for output in M2_CUSTOMER_RECORDS:
        assert catalog[output]["kind"] == rows[output]["kind"] == "record", output
        assert catalog[output]["description"].startswith("Customer-provided"), output
        assert "no toolchain producer" in catalog[output]["description"], output
        assert "Customer-provided" in rows[output]["producer_or_owner"], output
        assert "no toolchain producer" in rows[output]["producer_or_owner"], output
    for output in M2_CUSTOMER_PROCEDURES:
        assert catalog[output]["kind"] == rows[output]["kind"] == "procedure", output
        assert catalog[output]["description"].startswith("Customer-owned"), output
        assert "Customer-owned" in rows[output]["producer_or_owner"], output
        assert "no toolchain producer" in rows[output]["producer_or_owner"], output


@pytest.mark.trace("FR-018-AC-2", "FR-018-AC-5")
def test_m2_outputs_name_no_owner_ticket_and_no_tool_decision():
    """No M2 output points at a ticket, and the level is never tool-assigned."""
    catalog = _m2_output_catalog()
    for output, definition in catalog.items():
        assert "PLAT-" not in definition["description"], output
        assert "owner" not in definition["description"].casefold(), output
    for row in m2_mapping_rows():
        assert "PLAT-" not in str(row["producer_or_owner"]), row["output"]
    assert "never assigns" in catalog["documentation-level-decision"]["description"]
    vi_a = next(
        clause
        for clause_set in _m2_sets()
        for clause in clause_set["clauses"]
        if clause["id"] == "VI.A"
    )
    assert vi_a["expectedOutputs"] == ["documentation-level-decision"]


@pytest.mark.trace("FR-018-AC-3")
def test_shared_output_catalog_definitions_are_identical_across_us_sets():
    """Reused outputs keep the same kind and description throughout the module."""
    assert_output_catalog_consistent(load_clause_sets())


M3_KEYS = {
    "us-congress/fdca-524b@2026-10-15",
    "us-fda/premarket-cybersecurity@2026-02-03",
}

# Producer commands each cybersecurity output names, with the checks its
# description relies on: a flag in the command's help ("help"), an accepted
# `quoin evidence record` adapter ("adapter"), or a registered `quoin dossier
# generate` document kind ("dossier-kind").
CYBERSECURITY_PRODUCERS = {
    "threat-model": [
        (
            ("quoin", "dossier", "generate"),
            [("help", "--doc"), ("dossier-kind", "threat-model")],
        )
    ],
    "vulnerability-assessment": [
        (("quoin", "anomaly", "report"), []),
        (("quoin", "evidence", "record"), [("adapter", "osv-scanner")]),
    ],
    "security-architecture-views": [(("quire", "relations"), [("help", "--flow")])],
    "cybersecurity-test-results": [
        (
            ("quoin", "evidence", "record"),
            [
                ("adapter", "sarif"),
                ("adapter", "osv-scanner"),
                ("adapter", "cargo-deny"),
                ("adapter", "junit"),
            ],
        )
    ],
    "sbom": [
        (("quoin", "evidence", "record"), [("adapter", "sbom")]),
        (("quoin", "soup", "report"), []),
    ],
    "soup-list": [(("quoin", "soup", "report"), [])],
}
# Records the customer authors in a named module.
CYBERSECURITY_AUTHORED_RECORDS = {"security-risk-records": "spec-objects-security"}
CYBERSECURITY_CUSTOMER_DOCUMENTS = {
    "security-risk-assessment",
    "vulnerability-management-plan",
    "additional-cybersecurity-requirement-records",
}


def _m3_output_catalog() -> dict[str, dict]:
    catalog: dict[str, dict] = {}
    for clause_set in load_clause_sets():
        if clause_set_key(clause_set) in M3_KEYS:
            catalog.update(clause_set["outputCatalog"])
    return catalog


def _evidence_adapters(tmp_path: Path) -> set[str]:
    """Read the adapter names the installed quoin accepts for `evidence record`."""
    (tmp_path / "spec").mkdir()
    results = tmp_path / "results.json"
    results.write_text("{}")
    result = subprocess.run(
        [
            engine_tool("quoin"),
            "evidence",
            "record",
            "--suite",
            "S",
            "--tool",
            "t",
            "--adapter",
            "no-such-adapter",
            "--results",
            str(results),
            "--repo",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    return _listed_names(result.stdout + result.stderr, "Available:")


def _dossier_kinds(tmp_path: Path) -> set[str]:
    """Read the document kinds the installed quoin registers for `dossier generate`."""
    result = subprocess.run(
        [
            engine_tool("quoin"),
            "dossier",
            "generate",
            "--doc",
            "no-such-kind",
            "--out",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    return _listed_names(result.stdout + result.stderr, "the kinds are")


def _listed_names(output: str, marker: str) -> set[str]:
    assert marker in output, f"expected {marker!r} in quoin output: {output}"
    listed = output.split(marker, 1)[1].lstrip().split("\n", 1)[0]
    listed = listed.split('"', 1)[0].rstrip(".")
    return {name.strip() for name in listed.split(",")}


@pytest.mark.trace("FR-010-AC-3")
def test_every_cybersecurity_output_is_in_exactly_one_class():
    """Each catalog output is a producer, authored records, or a customer document."""
    classes = [
        set(CYBERSECURITY_PRODUCERS),
        set(CYBERSECURITY_AUTHORED_RECORDS),
        CYBERSECURITY_CUSTOMER_DOCUMENTS,
    ]
    assert sum(len(names) for names in classes) == len(set().union(*classes))
    assert set(_m3_output_catalog()) == set().union(*classes)


@pytest.mark.trace("FR-010-AC-3")
def test_cybersecurity_record_outputs_name_commands_that_exist(tmp_path):
    """Each producer output names real, installed commands and what they accept."""
    catalog = _m3_output_catalog()
    adapters = _evidence_adapters(tmp_path)
    dossier_kinds = _dossier_kinds(tmp_path)
    for output, producers in CYBERSECURITY_PRODUCERS.items():
        description = catalog[output]["description"]
        assert catalog[output]["kind"] == "record", output
        for command, checks in producers:
            assert (
                " ".join(command) in description
            ), f"{output}: description omits {' '.join(command)!r}"
            _assert_command_exists(command)
            help_text = subprocess.run(
                [engine_tool(command[0]), *command[1:], "--help"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            for check, value in checks:
                assert value in description, f"{output}: description omits {value}"
                if check == "help":
                    assert value in help_text, f"{output}: {command} lacks {value}"
                elif check == "adapter":
                    assert value in adapters, f"{output}: no {value} adapter"
                else:
                    assert value in dossier_kinds, f"{output}: no {value} kind"


@pytest.mark.trace("FR-010-AC-3")
def test_authored_cybersecurity_records_name_their_module():
    """Records the customer authors name the module that defines them."""
    catalog = _m3_output_catalog()
    for output, module in CYBERSECURITY_AUTHORED_RECORDS.items():
        assert catalog[output]["kind"] == "record", output
        assert module in catalog[output]["description"], output


@pytest.mark.trace("FR-010-AC-3")
def test_cybersecurity_outputs_without_a_producer_are_customer_documents():
    """Plans and assessments the toolchain cannot produce are customer-provided."""
    catalog = _m3_output_catalog()
    assert CYBERSECURITY_CUSTOMER_DOCUMENTS <= set(catalog)
    for output in CYBERSECURITY_CUSTOMER_DOCUMENTS:
        assert catalog[output]["kind"] == "document", output
        assert catalog[output]["description"].startswith("Customer-provided"), output
        assert "no toolchain producer" in catalog[output]["description"], output


@pytest.mark.trace("FR-010-AC-3")
def test_cybersecurity_outputs_name_no_owner_ticket():
    """No cybersecurity output points at a ticket as its owner."""
    for output, definition in _m3_output_catalog().items():
        assert "PLAT-" not in definition["description"], output
        assert "owner" not in definition["description"].casefold(), output

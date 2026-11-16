"""Discharge the M3 cybersecurity sets from synthetic producer evidence."""

from __future__ import annotations

import json
import pathlib
import shutil

import pytest
import yaml
from conftest import (
    PACKAGE_ROOT,
    REPO_ROOT,
    clause_set_key,
    engine_tool,
    load_clause_sets,
    resolve_fact_refs,
    run,
)

AS_OF = "2026-11-14T00:00:00Z"
M2_CONTEXT = [
    "documentation_level=enhanced",
    "qmsr_traceability_applicability=applies",
    "qmsr_advisory_notice_applicability=applies",
    "qmsr_design_development_applicability=applies",
    "qmsr_life_support_applicability=applies",
    "qmsr_servicing_applicability=applies",
]
M3_CONTEXT = ["cyber_device=yes"]
M3_KEYS = {
    "us-congress/fdca-524b@2026-10-15",
    "us-fda/premarket-cybersecurity@2026-02-03",
}
PART_11_CONTEXT = [
    "system_type=closed",
    "electronic_signatures=used",
    "signature_basis=non_biometric",
    "signature_method=identification_code_password",
]


def _json(*args: str) -> dict:
    result = run(*args)
    assert result.returncode == 0, result.stderr + result.stdout
    return json.loads(result.stdout)


def _stage_module(destination: pathlib.Path) -> pathlib.Path:
    """Stage all in-repository sets so the test exercises the complete pack."""
    manifest = yaml.safe_load((PACKAGE_ROOT / "manifest.yaml").read_text())
    destination.mkdir()
    entries = []
    for relative in manifest["clause_sets"]:
        source = PACKAGE_ROOT / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        entries.append(f"  - {relative}")
    (destination / "manifest.yaml").write_text(
        "manifest_version: 1.0.0\nname: spec_clauses_us_health\nversion: 0.1.0\n"
        "clause_sets:\n" + "\n".join(entries) + "\n"
    )
    return destination


def _record_fact(
    repo: pathlib.Path,
    root: pathlib.Path,
    config: pathlib.Path,
    evidence_repo: pathlib.Path,
    binding: dict,
    clause_id: str,
    references: list[str],
) -> pathlib.Path:
    facts_path = root / f"facts-{clause_id.replace('.', '-')}.json"
    facts = [
        {
            "kind": "direct",
            "clauseId": clause_id,
            "evidenceRefs": references,
            "attestation": {
                "attestedBy": "reviewer@example.invalid",
                "authority": "synthetic-customer-reviewer",
                "attestedAt": AS_OF,
                "expiresAt": "2027-11-14T00:00:00Z",
            },
        }
    ]
    facts_path.write_text(json.dumps(facts))
    binding_path = root / f"binding-{clause_id.replace('.', '-')}.json"
    binding_path.write_text(json.dumps(binding))
    recorded = run(
        engine_tool("quoin"),
        "evidence",
        "record-discharge",
        "--repo",
        str(evidence_repo),
        "--binding",
        str(binding_path),
        "--facts",
        str(facts_path),
        "--config-root",
        str(config),
    )
    assert recorded.returncode == 0, recorded.stderr + recorded.stdout
    resolve_fact_refs(repo, facts)
    return facts_path


def _master_no_producer_outputs() -> set[str]:
    """Read no-producer ownership from the normative output catalog."""
    spec = (REPO_ROOT / "spec" / "spec.md").read_text()
    section = spec.split("### US Health-Law Output Catalog", 1)[1].split("### ", 1)[0]
    outputs = set()
    for line in section.splitlines():
        if not line.strip().startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        name = cells[0].strip("`")
        description = cells[2].casefold()
        if "no producer on `origin/main`" in description or "owner: plat-" in description:
            outputs.add(name)
    return outputs


def _security_module() -> pathlib.Path:
    installed = _json(engine_tool("quoin"), "module", "list")["plugins"]
    matches = [entry for entry in installed if entry.get("name") == "spec-objects-security"]
    assert len(matches) == 1, "expected one installed spec-objects-security module"
    path = pathlib.Path(matches[0]["targetPath"]).resolve()
    assert path.is_dir(), f"security module path does not exist: {path}"
    return path


@pytest.mark.trace("TC-083")
@pytest.mark.trace("FR-020-AC-1")
@pytest.mark.trace("FR-020-AC-2")
@pytest.mark.trace("FR-020-AC-3")
@pytest.mark.trace("FR-020-AC-4")
@pytest.mark.trace("FR-019-AC-4")
@pytest.mark.trace("FR-019-AC-5")
def test_m3_discharge_renders_cybersecurity_sets_from_ingested_evidence(
    tmp_path: pathlib.Path,
) -> None:
    """SBOM, SOUP, and linked security records discharge only backed clauses."""
    version = run(engine_tool("quoin"), "--version")
    assert version.returncode == 0, version.stderr
    assert version.stdout.strip() == "0.35.0"

    root = tmp_path / "m3-run"
    root.mkdir()
    project = root / "project"
    project.mkdir()
    shutil.copytree(REPO_ROOT / "tests/corpus", project, dirs_exist_ok=True)
    shutil.copytree(
        REPO_ROOT / "tests/corpus/security",
        project / "spec/security",
        dirs_exist_ok=True,
    )
    shutil.copytree(
        REPO_ROOT / "tests/corpus/evidence",
        project / "evidence/fixtures",
        dirs_exist_ok=True,
    )
    (project / "spec/evidence").mkdir(parents=True, exist_ok=True)
    (project / "spec/evidence/suites.md").write_text(
        "# Synthetic evidence suites\n\n"
        "| ID | Name | Tool | Kind | Obligations |\n"
        "|---|---|---|---|---|\n"
        "| M3-SBOM | Synthetic component inventory | synthetic-syft | Static | 524B(b)(3), V.A.4, VII.C.3 |\n"
    )

    module = _stage_module(root / "pack-module")
    config = root / "quoin-config"
    installed = run(
        engine_tool("quoin"),
        "module",
        "install",
        f"path:{module}",
        "--config-root",
        str(config),
    )
    assert installed.returncode == 0, installed.stderr + installed.stdout

    bindings: dict[str, dict] = {}
    for key in sorted(M3_KEYS):
        authority, rest = key.split("/")
        set_id, version = rest.split("@")
        args = [
            engine_tool("quire"),
            "clauses",
            "evaluate",
            "--module",
            str(module),
            "--authority",
            authority,
            "--set",
            set_id,
            "--version",
            version,
            "--json",
        ]
        for context in M3_CONTEXT:
            args.extend(["--context", context])
        bindings[set_id] = _json(*args)

    security_module = _security_module()
    relations = _json(
        engine_tool("quire"),
        "relations",
        "--scope",
        str(project),
        "--module",
        str(security_module),
        "--relation",
        "threat-has-control",
        "--json",
    )
    threat_rows = relations["relations"][0]["rows"]
    assert len(threat_rows) == 1
    assert threat_rows[0]["document"]["id"] == "THREAT-M3-001"
    assert threat_rows[0]["state"] == "covered"
    assert [edge["id"] for edge in threat_rows[0]["linked"]] == ["CTRL-M3-001"]
    assert threat_rows[0]["linked"][0]["verb"] == "mitigates"

    evidence_repo = project / "evidence-store"
    evidence_repo.mkdir()
    config.mkdir(parents=True, exist_ok=True)
    sbom = project / "evidence/fixtures/m3-sbom.cdx.json"
    sbom_recorded = _json(
        engine_tool("quoin"),
        "evidence",
        "record",
        "--suite",
        "M3-SBOM",
        "--tool",
        "synthetic-syft",
        "--adapter",
        "sbom",
        "--results",
        str(sbom),
        "--discharges",
        "524B(b)(3),V.A.4,VII.C.3",
        "--repo",
        str(project),
        "--timestamp",
        AS_OF,
        "--config-root",
        str(config),
        "--json",
    )
    sbom_run = sbom_recorded["run_path"]
    assert (project / sbom_run).is_file(), sbom_run

    soup_records = project / "spec/soup"
    promoted = run(
        engine_tool("quoin"),
        "soup",
        "promote",
        str(sbom),
        "--repo",
        str(project),
        "--out",
        str(soup_records),
        "--discharges",
        "524B(a)",
        "--config-root",
        str(config),
        "--module",
        str(security_module),
    )
    assert promoted.returncode == 0, promoted.stderr + promoted.stdout
    assert list(soup_records.glob("*.md")), "SBOM produced no SOUP records"

    binding_path = root / "binding-soup-report.json"
    binding_path.write_text(json.dumps(bindings["fdca-524b"]))
    soup_report = run(
        engine_tool("quoin"),
        "soup",
        "report",
        "--as-of",
        AS_OF,
        "--binding",
        str(binding_path),
        "--repo",
        str(project),
        "--records",
        str(soup_records),
        "--support",
        str(project / "evidence/fixtures/m3-soup-support.json"),
        "--json",
        "--config-root",
        str(config),
    )
    assert soup_report.returncode == 0, soup_report.stderr + soup_report.stdout
    report_ref = "evidence/soup-report.json"
    _write_report = project / report_ref
    _write_report.parent.mkdir(parents=True, exist_ok=True)
    _write_report.write_text(soup_report.stdout)
    parsed_soup = json.loads(soup_report.stdout)
    assert {row["purl"] for row in parsed_soup["rows"]} == {
        "pkg:npm/core-utils@1.2.3",
        "pkg:npm/tls-helper@4.5.6",
        "pkg:generic/device-agent@0.8.0",
    }
    assert next(
        row for row in parsed_soup["rows"] if row["purl"] == "pkg:npm/tls-helper@4.5.6"
    )["support_status"] == "unsupported"

    shared_security_refs = [
        "spec/security/THREAT-M3-001.md",
        "spec/security/RISK-M3-001.md",
        "spec/security/CTRL-M3-001.md",
        "spec/security/BOUNDARY-M3-001.md",
    ]
    facts = {}
    for clause_id, set_id, refs in [
        ("524B(a)", "fdca-524b", shared_security_refs + [report_ref]),
        ("524B(b)(3)", "fdca-524b", [sbom_run, report_ref]),
        ("524B(b)(4)", "fdca-524b", shared_security_refs),
        ("V.A.4", "premarket-cybersecurity", [sbom_run, report_ref]),
        ("VII.C.3", "premarket-cybersecurity", [sbom_run, report_ref]),
    ]:
        facts[clause_id] = _record_fact(
            project,
            root,
            config,
            evidence_repo,
            bindings[set_id],
            clause_id,
            refs,
        )

    args = [
        engine_tool("quoin"),
        "discharge",
        "--rmm",
        "--pack",
        "spec_clauses_us_health",
        "--repo",
        str(evidence_repo),
        "--as-of",
        AS_OF,
        "--json",
        "--config-root",
        str(config),
    ]
    for context in PART_11_CONTEXT + M2_CONTEXT + M3_CONTEXT:
        args.extend(["--context", context])
    first = run(*args)
    second = run(*args)
    assert first.returncode == 0, first.stderr + first.stdout
    assert second.returncode == 0, second.stderr + second.stdout
    assert first.stdout.encode() == second.stdout.encode()
    report = json.loads(first.stdout)
    expected_keys = sorted(clause_set_key(item) for item in load_clause_sets())
    index = {
        f"{entry['clauseSet']['authority']}/{entry['clauseSet']['id']}@"
        f"{entry['clauseSet']['version']}": entry
        for entry in report["index"]
    }
    assert sorted(index) == expected_keys
    for clause_set in load_clause_sets():
        key = clause_set_key(clause_set)
        assert index[key]["rowCount"] == len(clause_set["clauses"])

    rows = {
        row["clauseId"]: row
        for matrix in report["matrices"]
        for row in matrix["rows"]
    }
    output_catalog = {
        name: definition
        for key in M3_KEYS
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) == key
        for name, definition in clause_set["outputCatalog"].items()
    }
    master_unproduced = _master_no_producer_outputs()
    m3_unproduced = master_unproduced.intersection(output_catalog)
    assert m3_unproduced == {
        name
        for name, definition in output_catalog.items()
        if "owner: PLAT-" in definition["description"]
    }
    clauses = {
        clause["id"]: clause
        for key in M3_KEYS
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) == key
        for clause in clause_set["clauses"]
    }
    expected_open = {
        clause_id
        for clause_id, clause in clauses.items()
        if set(clause["expectedOutputs"]).intersection(m3_unproduced)
    }
    actual_open = {
        clause_id
        for clause_id in clauses
        if rows[clause_id]["compliance"] == "undischarged"
    }
    assert actual_open == expected_open
    assert rows["524B(b)(3)"]["compliance"] == "compliant"
    assert rows["524B(a)"]["compliance"] == "compliant"
    assert rows["524B(b)(4)"]["compliance"] == "compliant"
    assert rows["V.A.4"]["compliance"] == "compliant"
    assert rows["VII.C.3"]["compliance"] == "compliant"

    for clause_id, facts_path in facts.items():
        changed = json.loads(facts_path.read_text())
        changed[0]["evidenceRefs"][0] = "evidence://example.invalid/evidence/missing.json"
        with pytest.raises(
            AssertionError,
            match=rf"{clause_id}: evidence ref does not resolve",
        ):
            resolve_fact_refs(project, changed)

    markdown_args = [argument for argument in args if argument != "--json"]
    markdown = run(*markdown_args)
    markdown_repeat = run(*markdown_args)
    assert markdown.returncode == 0, markdown.stderr + markdown.stdout
    assert markdown_repeat.returncode == 0, markdown_repeat.stderr + markdown_repeat.stdout
    assert markdown.stdout.encode() == markdown_repeat.stdout.encode()
    assert "us-congress/fdca-524b@2026-10-15" in markdown.stdout
    assert "us-fda/premarket-cybersecurity@2026-02-03" in markdown.stdout
    assert "Not compliant - undischarged" in markdown.stdout

    no_device_args = []
    index_arg = 0
    while index_arg < len(args):
        if args[index_arg] == "--context" and args[index_arg + 1] == "cyber_device=yes":
            index_arg += 2
            continue
        no_device_args.append(args[index_arg])
        index_arg += 1
    no_device_args.extend(["--context", "cyber_device=no"])
    no_device = run(*no_device_args)
    assert no_device.returncode == 0, no_device.stderr + no_device.stdout
    no_device_rows = {
        row["clauseId"]: row
        for matrix in json.loads(no_device.stdout)["matrices"]
        for row in matrix["rows"]
    }
    fdca_ids = {
        clause["id"]
        for clause in next(
            clause_set
            for clause_set in load_clause_sets()
            if clause_set_key(clause_set) == "us-congress/fdca-524b@2026-10-15"
        )["clauses"]
    }
    assert all(
        no_device_rows[clause_id]["applicability"] == "not_applicable"
        for clause_id in fdca_ids
    )

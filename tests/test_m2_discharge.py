"""Discharge the M2 device-software sets on synthetic evidence."""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import tempfile

import pytest
from conftest import (
    PACKAGE_ROOT,
    REPO_ROOT,
    clause_set_key,
    engine_tool,
    load_clause_sets,
    m2_mapping_rows,
    resolve_fact_refs,
    run,
    stage_clause_sets,
)

AS_OF = "2026-11-14T00:00:00Z"
PART_11_CONTEXT = [
    "system_type=closed",
    "electronic_signatures=used",
    "signature_basis=non_biometric",
    "signature_method=identification_code_password",
]
M2_CONTEXT = [
    "documentation_level=enhanced",
    "qmsr_traceability_applicability=applies",
    "qmsr_advisory_notice_applicability=applies",
    "qmsr_design_development_applicability=applies",
    "qmsr_life_support_applicability=applies",
    "qmsr_servicing_applicability=applies",
]
SETS = [
    ("us-fda", "21-cfr-11", "2026-11-12"),
    ("us-fda", "21-cfr-820", "2026-11-12"),
    ("us-fda", "premarket-device-software", "2023-06-14"),
]
M2_SET_KEYS = {
    "us-fda/21-cfr-820@2026-11-12",
    "us-fda/premarket-device-software@2023-06-14",
}
CORPUS_OUTPUT_REFS = {
    "risk-management-records": ["risk/hazard.md"],
    "software-requirements": ["spec/FR-003-m2-requirements.md"],
    "software-architecture": ["architecture/device.md"],
    "verification-records": ["verification/matrix.json"],
    "release-record": ["evidence/release-verify.json"],
    "anomaly-list": ["spec/AN-001-synthetic.md"],
}


def _json(*args: str, cwd: pathlib.Path | None = None) -> dict:
    result = run(*args, cwd=cwd)
    assert result.returncode == 0, result.stderr + result.stdout
    return json.loads(result.stdout)


def _git(repo: pathlib.Path, *args: str) -> str:
    result = run(
        "git",
        "-C",
        str(repo),
        *args,
        cwd=repo,
        env=os.environ | {"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"},
    )
    assert result.returncode == 0, result.stderr + result.stdout
    return result.stdout.strip()


def _write(repo: pathlib.Path, name: str, data: str) -> str:
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data)
    return name


def _release_evidence(repo: pathlib.Path, root: pathlib.Path) -> str:
    """Verify a temporary signed release record with the published EA CLI."""
    key = root / "release_signing_key"
    generated = run(
        "ssh-keygen",
        "-q",
        "-t",
        "ed25519",
        "-N",
        "",
        "-C",
        "release@example.invalid",
        "-f",
        str(key),
    )
    assert generated.returncode == 0, generated.stderr
    public_key = pathlib.Path(f"{key}.pub").read_text().strip()
    allowed = root / "allowed_signers"
    allowed.write_text(f"release@example.invalid {public_key}\n")

    baseline = _write(
        repo,
        "baseline.md",
        "---\nid: BL-1\ntitle: Baseline\ntype: Baseline\nname: Synthetic baseline\n"
        "items:\n  - path: spec/FR-003-m2-requirements.md\n    kind: spec_artifact\n"
        "---\n\nSynthetic baseline.\n",
    )
    _git(repo, "init", "--quiet", "-b", "main")
    _git(repo, "config", "user.name", "Synthetic Release Owner")
    _git(repo, "config", "user.email", "release@example.invalid")
    _git(repo, "add", ".")
    _git(
        repo,
        "-c",
        "gpg.format=ssh",
        "-c",
        f"user.signingkey={key}",
        "commit",
        "-S",
        "-m",
        "Synthetic baseline",
    )
    baseline_commit = _git(repo, "rev-parse", "HEAD")

    record_path = "release/REL-1.md"
    snapshot_path = _write(repo, "release/snapshot.json", '{"synthetic":true}\n')
    record = (
        "---\nid: REL-1\ntitle: Release one\ntype: Release\nname: Synthetic release\n"
        f'baseline:\n  path: {baseline}\n  commit: "{baseline_commit}"\n'
        f"snapshot_path: {snapshot_path}\ndecision_owner: release@example.invalid\n"
        "accepted_anomalies:\n  - synthetic test anomaly\n---\n\nSynthetic release.\n"
    )
    _write(repo, record_path, record)
    _git(repo, "add", record_path, snapshot_path)
    _git(repo, "commit", "-m", "Synthetic release")
    release_commit = _git(repo, "rev-parse", "HEAD")
    blob = _git(repo, "rev-parse", f"{release_commit}:{record_path}")
    message = (
        "Synthetic release\n\nApproved-Record-Id: REL-1\n"
        f"Approved-Record-Digest: git-blob:{blob}\n"
        "Signed-off-meaning: synthetic release accepted"
    )
    _git(
        repo,
        "-c",
        "gpg.format=ssh",
        "-c",
        f"user.signingkey={key}",
        "tag",
        "-s",
        "-m",
        message,
        "m2-synthetic-release",
        release_commit,
    )
    request = {
        "protocol": "engineering-assurance.release-verify-request/v1",
        "repository": str(repo),
        "tag": "m2-synthetic-release",
        "record_path": record_path,
        "allowed_signers": str(allowed),
    }
    verified = run(
        engine_tool("engineering-assurance"),
        "release-verify",
        "--request",
        "-",
        cwd=repo,
        input=json.dumps(request),
    )
    assert verified.returncode == 0, verified.stderr + verified.stdout
    value = json.loads(verified.stdout)
    assert value["status"] == "released", value
    out = _write(repo, "evidence/release-verify.json", verified.stdout)
    assert pathlib.Path(f"{key}.pub").is_file()
    return out


def _expected_m2_lists() -> tuple[set[str], set[str]]:
    """Classify clause rows using the PLAT-1575 mapping and corpus artifacts."""
    mapping = m2_mapping_rows()
    mapping_by_pair = {
        (clause_id, row["output"]): row["producer_or_owner"]
        for row in mapping
        for clause_id in row["clause_ids"]
    }
    m2_sets = [
        clause_set
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) in M2_SET_KEYS
    ]
    all_clauses = {
        clause["id"]: clause
        for clause_set in m2_sets
        for clause in clause_set["clauses"]
    }
    compliant = set()
    for clause_id, clause in all_clauses.items():
        outputs = clause["expectedOutputs"]
        mapped_outputs = [mapping_by_pair[(clause_id, output)] for output in outputs]
        has_producer = all(
            "no producer" not in producer.casefold()
            and "customer-provided" not in producer.casefold()
            and "customer-owned" not in producer.casefold()
            and "owner plat-" not in producer.casefold()
            for producer in mapped_outputs
        )
        if has_producer and all(output in CORPUS_OUTPUT_REFS for output in outputs):
            compliant.add(clause_id)
    return compliant, set(all_clauses) - compliant


def _record_fact(
    evidence_repo: pathlib.Path,
    binding: dict,
    clause_id: str,
    evidence_refs: list[str],
    root: pathlib.Path,
    config: pathlib.Path,
) -> pathlib.Path:
    path = root / f"facts-{clause_id.replace('.', '-')}.json"
    path.write_text(
        json.dumps(
            [
                {
                    "kind": "direct",
                    "clauseId": clause_id,
                    "evidenceRefs": evidence_refs,
                    "attestation": {
                        "attestedBy": "reviewer@example.invalid",
                        "authority": "synthetic-customer-reviewer",
                        "attestedAt": AS_OF,
                        "expiresAt": "2027-11-14T00:00:00Z",
                    },
                }
            ]
        )
    )
    binding_path = root / f"binding-{clause_id.replace('.', '-')}.json"
    binding_path.write_text(json.dumps(binding))
    result = run(
        engine_tool("quoin"),
        "evidence",
        "record-discharge",
        "--repo",
        str(evidence_repo),
        "--binding",
        str(binding_path),
        "--facts",
        str(path),
        "--config-root",
        str(config),
    )
    assert result.returncode == 0, result.stderr + result.stdout
    return path


@pytest.mark.trace("TC-082")
@pytest.mark.trace("FR-019-AC-1")
@pytest.mark.trace("FR-019-AC-2")
@pytest.mark.trace("FR-019-AC-3")
@pytest.mark.trace("FR-019-AC-4")
@pytest.mark.trace("FR-019-AC-5")
def test_m2_discharge_renders_three_sets_with_producer_backed_facts(
    tmp_path: pathlib.Path,
):
    """Producer evidence discharges present artifacts and leaves gaps open."""
    version = run(engine_tool("quoin"), "--version")
    assert version.returncode == 0, version.stderr
    assert version.stdout.strip() == "0.35.0"

    with tempfile.TemporaryDirectory(dir=tmp_path, prefix="m2-corpus-") as temp:
        root = pathlib.Path(temp)
        project = root / "project"
        project.mkdir()
        shutil.copytree(REPO_ROOT / "tests/corpus", project, dirs_exist_ok=True)
        for name, content in {
            "spec/FR-003-m2-requirements.md": (
                "---\nid: FR-003\ntitle: Synthetic device requirement\ntype: FR\n"
                "---\n\n## Description\n\n"
                "The synthetic device retains its risk records.\n"
            ),
            "architecture/device.md": "Synthetic architecture part and connection.\n",
            "risk/hazard.md": "Hazard -> hazardous situation -> harm; estimate: low.\n",
            "verification/matrix.json": '{"synthetic":true}\n',
            "spec/soup/fixture.json": '{"components":[]}\n',
            "spec/AN-001-synthetic.md": (
                "---\nid: AN-001\ntype: Anomaly\ntitle: Synthetic anomaly\n"
                "status: assessed\nsafety_impact: none\n---\n\n"
                "## Description\n\nSynthetic.\n"
            ),
        }.items():
            _write(project, name, content)

        release_ref = _release_evidence(project, root)
        module = stage_clause_sets(
            root,
            *[
                PACKAGE_ROOT / "clauses" / name
                for name in [
                    "us-fda-21-cfr-11-2026-11-12.json",
                    "us-fda-21-cfr-820-2026-11-12.json",
                    "us-fda-premarket-device-software-2023-06-14.json",
                ]
            ],
            module_name="spec_clauses_us_health",
            module_version="0.1.0",
        )
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
        for authority, set_id, version in SETS:
            bindings[set_id] = _json(
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
                *sum(
                    (["--context", item] for item in PART_11_CONTEXT + M2_CONTEXT),
                    [],
                ),
            )

        evidence_repo = project / "evidence-store"
        evidence_repo.mkdir()
        req_ref = "spec/FR-003-m2-requirements.md"
        arch_ref = "architecture/device.md"
        risk_ref = "risk/hazard.md"
        matrix_ref = "verification/matrix.json"
        direct_facts = {
            ("21-cfr-11", "11.10(e)"): [req_ref],
            ("21-cfr-820", "820.10(a)"): [release_ref, req_ref],
            ("21-cfr-820", "820.10(c)"): [
                req_ref,
                arch_ref,
                risk_ref,
                matrix_ref,
            ],
            ("21-cfr-820", "820.45(b)"): [release_ref],
            ("premarket-device-software", "VI.C"): [risk_ref],
            ("premarket-device-software", "VI.D"): [req_ref],
            ("premarket-device-software", "VI.E"): [arch_ref],
            ("premarket-device-software", "VI.H"): [matrix_ref],
            ("premarket-device-software", "VI.H.enhanced"): [matrix_ref],
            ("premarket-device-software", "VI.I"): [release_ref],
            ("premarket-device-software", "VI.J"): ["spec/AN-001-synthetic.md"],
        }
        facts_paths = {}
        for (set_id, clause_id), refs in direct_facts.items():
            binding = bindings[set_id]
            clause_ids = {row["clauseId"] for row in binding["clauses"]}
            assert clause_id in clause_ids, clause_id
            facts_paths[clause_id] = _record_fact(
                evidence_repo, binding, clause_id, refs, root, config
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
        for item in PART_11_CONTEXT + M2_CONTEXT:
            args.extend(["--context", item])
        first = run(*args)
        second = run(*args)
        assert first.returncode == 0, first.stderr + first.stdout
        assert second.returncode == 0, second.stderr + second.stdout
        assert first.stdout.encode() == second.stdout.encode()
        report = json.loads(first.stdout)
        keys = [
            f"{entry['clauseSet']['authority']}/{entry['clauseSet']['id']}@"
            f"{entry['clauseSet']['version']}"
            for entry in report["index"]
        ]
        assert keys == sorted(
            [
                "us-fda/21-cfr-11@2026-11-12",
                "us-fda/21-cfr-820@2026-11-12",
                "us-fda/premarket-device-software@2023-06-14",
            ]
        )
        for entry in report["index"]:
            matching = next(
                binding
                for binding in bindings.values()
                if binding["clauseSet"] == entry["clauseSet"]
            )
            assert entry["rowCount"] == len(matching["clauses"])

        rows = {
            row["clauseId"]: row
            for matrix in report["matrices"]
            for row in matrix["rows"]
        }
        expected_compliant, expected_open = _expected_m2_lists()
        m2_rows = {
            clause_id: row
            for clause_id, row in rows.items()
            if clause_id in expected_compliant or clause_id in expected_open
        }
        assert {
            clause_id
            for clause_id, row in m2_rows.items()
            if row["compliance"] == "compliant"
        } == expected_compliant
        assert {
            clause_id
            for clause_id, row in m2_rows.items()
            if row["compliance"] == "undischarged"
        } == expected_open
        assert rows["820.10(c)"]["compliance"] == "compliant", rows["820.10(c)"]
        assert rows["820.10(a)"]["compliance"] == "compliant"
        assert rows["VI.A"]["compliance"] == "undischarged"
        assert rows["VI.C"]["compliance"] == "compliant"
        assert rows["VI.I"]["compliance"] == "compliant"
        assert rows["VI.B"]["compliance"] == "undischarged"
        assert rows["820.10(b)(1)"]["compliance"] == "undischarged"

        basic_args = []
        index = 0
        while index < len(args):
            if (
                args[index] == "--context"
                and args[index + 1] == "documentation_level=enhanced"
            ):
                index += 2
                continue
            basic_args.append(args[index])
            index += 1
        basic_args.extend(["--context", "documentation_level=basic"])
        basic = run(*basic_args)
        assert basic.returncode == 0, basic.stderr + basic.stdout
        basic_rows = {
            row["clauseId"]: row
            for matrix in json.loads(basic.stdout)["matrices"]
            for row in matrix["rows"]
        }
        for clause_id in ["VI.F.enhanced", "VI.G.enhanced", "VI.H.enhanced"]:
            assert basic_rows[clause_id]["applicability"] == "not_applicable"

        facts_path = facts_paths["820.10(c)"]
        facts = json.loads(facts_path.read_text())
        facts[0]["evidenceRefs"][
            -1
        ] = "evidence://example.invalid/evidence/missing.json"
        facts_path.write_text(json.dumps(facts))
        binding_path = root / "binding-820-10(c).json"
        invalid_record = run(
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
        assert invalid_record.returncode == 0, (
            invalid_record.stderr + invalid_record.stdout
        )
        changed_report = run(*args)
        assert changed_report.returncode == 0, (
            changed_report.stderr + changed_report.stdout
        )
        assert "evidence/missing.json" in changed_report.stdout
        with pytest.raises(
            AssertionError, match=r"820\.10\(c\): evidence ref does not resolve"
        ):
            resolve_fact_refs(project, facts)

        markdown = run(*[arg for arg in args if arg != "--json"])
        markdown_repeat = run(*[arg for arg in args if arg != "--json"])
        assert markdown.returncode == 0, markdown.stderr + markdown.stdout
        assert markdown_repeat.returncode == 0, (
            markdown_repeat.stderr + markdown_repeat.stdout
        )
        assert markdown.stdout.encode() == markdown_repeat.stdout.encode()
        assert "us-fda/21-cfr-820@2026-11-12" in markdown.stdout
        assert "Not compliant - undischarged" in markdown.stdout

    assert not pathlib.Path(temp).exists()

"""End-to-end discharge of the Part 11 set using only synthetic evidence."""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import tempfile

import pytest
from conftest import PACKAGE_ROOT, REPO_ROOT, engine_tool, run

PART_11_KEY = "us-fda/21-cfr-11@2026-11-12"
AS_OF = "2026-11-14T00:00:00Z"
CONTEXT = [
    "system_type=closed",
    "electronic_signatures=used",
    "signature_basis=non_biometric",
    "signature_method=identification_code_password",
]
CUSTOMER_OWNED = {"11.10(i)", "11.10(j)", "11.300(b)", "11.300(c)"}


def _run_json(*args: str, cwd: pathlib.Path | None = None, input: str | None = None):
    result = run(*args, cwd=cwd, input=input)
    assert result.returncode == 0, result.stderr + result.stdout
    return json.loads(result.stdout)


def _git(repo: pathlib.Path, *args: str):
    command = ["git", "-C", str(repo)]
    command.extend(args)
    env = os.environ | {"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"}
    result = run(*command, cwd=repo, env=env)
    assert result.returncode == 0, result.stderr + result.stdout
    return result.stdout.strip()


def _save_tool_output(repo: pathlib.Path, name: str, value: dict) -> str:
    relative = pathlib.PurePosixPath("evidence") / name
    destination = repo.joinpath(*relative.parts)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n"
    )
    return relative.as_posix()


def _resolve_fact_refs(repo: pathlib.Path, facts: list[dict]) -> None:
    for fact in facts:
        refs = fact.get("evidenceRefs", [])
        if fact.get("approvalRef"):
            refs = [*refs, fact["approvalRef"]]
        for reference in refs:
            if reference.startswith("evidence://example.invalid/"):
                relative = reference.removeprefix("evidence://example.invalid/")
            else:
                relative = reference
            path = (repo / relative).resolve()
            assert path.is_relative_to(
                repo.resolve()
            ), f"{fact['clauseId']}: evidence ref escapes the corpus: {reference}"
            assert (
                path.is_file()
            ), f"{fact['clauseId']}: evidence ref does not resolve: {reference}"


def _make_signed_corpus(repo: pathlib.Path, private_key: pathlib.Path) -> pathlib.Path:
    corpus = REPO_ROOT / "tests" / "corpus"
    shutil.copytree(corpus, repo, dirs_exist_ok=True)
    public_key = pathlib.Path(f"{private_key}.pub").read_text().strip()
    allowed_signers = repo / "allowed_signers"
    allowed_signers.write_text(f"reviewer@example.invalid {public_key}\n")

    _git(repo, "init", "--quiet")
    _git(repo, "config", "user.name", "Synthetic Reviewer")
    _git(repo, "config", "user.email", "reviewer@example.invalid")
    _git(repo, "add", ".")
    _git(
        repo,
        "-c",
        "gpg.format=ssh",
        "-c",
        f"user.signingkey={private_key}",
        "commit",
        "-S",
        "-m",
        "Synthetic Part 11 corpus",
    )
    _git(
        repo,
        "-c",
        "gpg.format=ssh",
        "-c",
        f"user.signingkey={private_key}",
        "-c",
        f"gpg.ssh.allowedSignersFile={allowed_signers}",
        "tag",
        "-s",
        "-m",
        "Synthetic Part 11 approval\n\n"
        "Approved-Record-Id: record://example.invalid/FR-001\n"
        "Approved-Record-Digest: sha256:0123456789abcdef\n"
        "Signed-off-meaning: reviewed",
        "part11-synthetic-approval",
    )
    return allowed_signers


def _stage_part11_module(destination: pathlib.Path) -> pathlib.Path:
    """Keep the runtime pack to one set so its report index is unambiguous."""
    clauses = destination / "clauses"
    clauses.mkdir(parents=True)
    clause_path = PACKAGE_ROOT / "clauses" / "us-fda-21-cfr-11-2026-11-12.json"
    shutil.copyfile(clause_path, clauses / clause_path.name)
    (destination / "manifest.yaml").write_text(
        "manifest_version: 1.0.0\n"
        "name: spec_clauses_us_health\n"
        "version: 0.1.0\n"
        "clause_sets:\n"
        "  - clauses/us-fda-21-cfr-11-2026-11-12.json\n"
    )
    return destination


def _run_producer(command: str, request: dict) -> dict:
    return _run_json(
        engine_tool("engineering-assurance"),
        command,
        "--request",
        "-",
        input=json.dumps(request),
    )


@pytest.mark.trace("TC-024", "FR-007-AC-1")
def test_synthetic_corpus_validates():
    """Description: Validate each Markdown artifact in the synthetic corpus.

    Assumptions: Quire's installed ISO module provides the FR and NFR schemas.
    Criteria: Corpus Markdown passes structural validation.
    """
    result = run(
        engine_tool("quire"), "validate", "tests/corpus/**/*.md", cwd=REPO_ROOT
    )
    assert result.returncode == 0, result.stderr + result.stdout


@pytest.mark.trace("TC-025", "FR-007-AC-2")
@pytest.mark.trace("TC-026", "FR-007-AC-3")
@pytest.mark.trace("TC-022", "FR-006-AC-2")
def test_part11_discharge_renders_deterministic_pack_rmm(tmp_path: pathlib.Path):
    """Description: Produce signed synthetic evidence and discharge the Part 11 pack.

    Assumptions: The published Quoin CLI accepts the publishable US module as a pack.
    Criteria: Direct and delegated facts render truthfully, open and non-applicable
        clauses remain visible, evidence refs resolve, and repeated output is stable.
    """
    version = run(engine_tool("quoin"), "--version")
    assert version.returncode == 0, version.stderr
    assert version.stdout.strip() == "0.35.0"

    with tempfile.TemporaryDirectory(
        dir=tmp_path, prefix="part11-corpus-"
    ) as temporary:
        root = pathlib.Path(temporary)
        repo = root / "project"
        repo.mkdir()
        private_key = root / "fixture_signing_key"
        keygen = run(
            "ssh-keygen",
            "-q",
            "-t",
            "ed25519",
            "-N",
            "",
            "-C",
            "signer@example.invalid",
            "-f",
            str(private_key),
        )
        assert keygen.returncode == 0, keygen.stderr
        allowed_signers = _make_signed_corpus(repo, private_key)
        clause_module = _stage_part11_module(root / "part11-module")
        config_root = root / "quoin-config"
        install = run(
            engine_tool("quoin"),
            "module",
            "install",
            f"path:{clause_module}",
            "--config-root",
            str(config_root),
        )
        assert install.returncode == 0, install.stderr + install.stdout

        commit = _git(repo, "rev-parse", "HEAD")
        signature_commit = _run_producer(
            "signature-verify",
            {
                "protocol": "engineering-assurance.signature-verify-request/v1",
                "repository": str(repo),
                "revision": commit,
                "kind": "commit",
                "allowed_signers": str(allowed_signers),
            },
        )
        signature_tag = _run_producer(
            "signature-verify",
            {
                "protocol": "engineering-assurance.signature-verify-request/v1",
                "repository": str(repo),
                "revision": "part11-synthetic-approval",
                "kind": "tag",
                "allowed_signers": str(allowed_signers),
            },
        )
        approval_request = {
            "protocol": "engineering-assurance.approval-verify-request/v1",
            "repository": str(repo),
            "tag": "part11-synthetic-approval",
            "record_id": "record://example.invalid/FR-001",
            "record_digest": "sha256:0123456789abcdef",
            "allowed_signers": str(allowed_signers),
        }
        approval = _run_producer("approval-verify", approval_request)
        trail = _run_producer(
            "approval-trail",
            {
                "protocol": "engineering-assurance.approval-trail-request/v1",
                "repository": str(repo),
                "record_id": approval_request["record_id"],
                "record_digest": approval_request["record_digest"],
                "allowed_signers": str(allowed_signers),
            },
        )
        assert signature_commit["status"] == "signed_valid", signature_commit
        assert signature_tag["status"] == "signed_valid"
        assert approval["status"] == "approved"
        assert trail["entries"]

        refs = {
            "commit": _save_tool_output(
                repo, "signature-commit.json", signature_commit
            ),
            "tag": _save_tool_output(repo, "signature-tag.json", signature_tag),
            "approval": _save_tool_output(repo, "approval-verify.json", approval),
            "trail": _save_tool_output(repo, "approval-trail.json", trail),
        }
        binding = _run_json(
            engine_tool("quire"),
            "clauses",
            "evaluate",
            "--module",
            str(clause_module),
            "--authority",
            "us-fda",
            "--set",
            "21-cfr-11",
            "--version",
            "2026-11-12",
            "--json",
            *sum((["--context", item] for item in CONTEXT), []),
        )
        binding_path = root / "binding.json"
        binding_path.write_text(json.dumps(binding))
        clause_ids = {clause["clauseId"] for clause in binding["clauses"]}
        assert CUSTOMER_OWNED <= clause_ids

        attestation = {
            "attestedBy": "reviewer@example.invalid",
            "authority": "quality-lead@example.invalid",
            "attestedAt": "2026-11-14T00:00:00Z",
            "expiresAt": "2027-11-14T00:00:00Z",
        }
        facts = [
            {
                "kind": "direct",
                "clauseId": "11.10(e)",
                "evidenceRefs": [
                    refs["commit"],
                    refs["tag"],
                    refs["approval"],
                    refs["trail"],
                ],
                "attestation": attestation,
            }
        ]
        for clause_id in sorted(CUSTOMER_OWNED):
            facts.append(
                {
                    "kind": "disposition",
                    "clauseId": clause_id,
                    "decision": "delegated",
                    "owner": "customer@example.invalid",
                    "rationale": "Customer owns this fictional procedure obligation.",
                    "approvalRef": f"evidence://example.invalid/{refs['approval']}",
                    "attestation": attestation,
                }
            )

        _resolve_fact_refs(repo, facts)
        facts_path = root / "facts.json"
        facts_path.write_text(json.dumps(facts))
        evidence_store = repo / "evidence-store"
        evidence_store.mkdir()
        record = run(
            engine_tool("quoin"),
            "evidence",
            "record-discharge",
            "--repo",
            str(evidence_store),
            "--binding",
            str(binding_path),
            "--facts",
            str(facts_path),
            "--config-root",
            str(config_root),
        )
        assert record.returncode == 0, record.stderr + record.stdout

        invalid_dispositions = [
            (
                {
                    "kind": "disposition",
                    "clauseId": "11.10(i)",
                    "decision": "delegated",
                    "owner": "customer@example.invalid",
                    "approvalRef": "evidence://example.invalid/evidence/approval-verify.json",
                    "attestation": attestation,
                },
                "rationale",
            ),
            (
                {
                    "kind": "disposition",
                    "clauseId": "11.10(i)",
                    "decision": "delegated",
                    "owner": "customer@example.invalid",
                    "rationale": "Customer owns this fictional procedure obligation.",
                    "attestation": attestation,
                },
                "approvalRef",
            ),
        ]
        for index, (invalid_fact, missing_field) in enumerate(invalid_dispositions):
            invalid_facts_path = root / f"invalid-facts-{index}.json"
            invalid_facts_path.write_text(json.dumps([invalid_fact]))
            invalid_store = root / f"invalid-store-{index}"
            invalid_store.mkdir()
            rejected = run(
                engine_tool("quoin"),
                "evidence",
                "record-discharge",
                "--repo",
                str(invalid_store),
                "--binding",
                str(binding_path),
                "--facts",
                str(invalid_facts_path),
                "--config-root",
                str(config_root),
            )
            assert rejected.returncode != 0, rejected.stdout
            assert missing_field in rejected.stderr + rejected.stdout

        args = [
            engine_tool("quoin"),
            "discharge",
            "--rmm",
            "--pack",
            "spec_clauses_us_health",
            "--repo",
            str(evidence_store),
            "--as-of",
            AS_OF,
            "--json",
            "--config-root",
            str(config_root),
        ]
        for item in CONTEXT:
            args.extend(["--context", item])
        first = run(*args)
        second = run(*args)
        assert first.returncode == 0, first.stderr + first.stdout
        assert second.returncode == 0, second.stderr + second.stdout
        assert first.stdout.encode() == second.stdout.encode()
        report = json.loads(first.stdout)
        assert report["context"] == dict(
            item.split("=", maxsplit=1) for item in CONTEXT
        )
        assert len(report["index"]) == 1
        assert report["index"][0]["clauseSet"] == {
            "authority": "us-fda",
            "id": "21-cfr-11",
            "version": "2026-11-12",
        }
        matrix = report["matrices"][0]
        rows = {row["clauseId"]: row for row in matrix["rows"]}
        assert rows["11.10(e)"]["compliance"] == "compliant"
        assert rows["11.10(a)"]["compliance"] == "undischarged"
        assert rows["11.30"]["applicability"] == "not_applicable"
        markdown_args = [arg for arg in args if arg != "--json"]
        markdown = run(*markdown_args)
        markdown_repeat = run(*markdown_args)
        assert markdown.returncode == 0, markdown.stderr + markdown.stdout
        assert markdown_repeat.returncode == 0, (
            markdown_repeat.stderr + markdown_repeat.stdout
        )
        assert markdown.stdout.encode() == markdown_repeat.stdout.encode()
        assert PART_11_KEY in markdown.stdout
        assert r"11.10\(a\)" in markdown.stdout
        assert "Not compliant - undischarged: no discharge fact" in markdown.stdout
        assert "11.30" in markdown.stdout
        assert "Not applicable" in markdown.stdout
        for clause_id in CUSTOMER_OWNED:
            assert clause_id not in {
                fact["clauseId"] for fact in facts if fact["kind"] == "direct"
            }
            assert rows[clause_id]["compliance"] == "tailored"
            tailoring = rows[clause_id]["tailoringDescription"]
            assert "delegated" in tailoring
            assert (
                f"approval evidence://example.invalid/{refs['approval']}" in tailoring
            )

        missing_ref = "evidence://example.invalid/evidence/missing.json"
        with pytest.raises(
            AssertionError, match=r"11\.10\(e\).*evidence ref does not resolve"
        ) as error:
            _resolve_fact_refs(repo, [{**facts[0], "evidenceRefs": [missing_ref]}])
        assert missing_ref in str(error.value)

    assert not pathlib.Path(temporary).exists()
    assert not private_key.exists()

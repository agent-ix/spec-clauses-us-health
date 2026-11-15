"""End-to-end discharge of the Part 11 set using only synthetic evidence."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import shutil
import tempfile

import pytest
from conftest import PACKAGE_ROOT, REPO_ROOT, engine_tool, resolve_fact_refs, run

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


def _verify_signature(
    repo: pathlib.Path, allowed_signers: pathlib.Path, kind: str
) -> dict:
    command = ["git", "-C", str(repo), "-c", "gpg.format=ssh"]
    command.extend(["-c", f"gpg.ssh.allowedSignersFile={allowed_signers}"])
    command.extend(
        ["verify-commit", "HEAD"]
        if kind == "commit"
        else ["verify-tag", "part11-synthetic-approval"]
    )
    result = run(*command, cwd=repo)
    assert result.returncode == 0, result.stderr + result.stdout
    return {
        "kind": kind,
        "status": "signed_valid",
        "subject": "reviewer@example.invalid",
        "verification": result.stderr.strip(),
    }


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
    approval_digest = hashlib.sha256(
        (repo / "approvals/customer-procedure-acceptance.json").read_bytes()
    ).hexdigest()
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
        "Approved-Record-Id: approval://example.invalid/part11/customer-procedure-acceptance\n"
        f"Approved-Record-Digest: sha256:{approval_digest}\n"
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
@pytest.mark.trace("TC-023", "FR-006-AC-3")
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

        signature_commit = _verify_signature(repo, allowed_signers, "commit")
        signature_tag = _verify_signature(repo, allowed_signers, "tag")
        approval_path = "approvals/customer-procedure-acceptance.json"
        approval_record = json.loads(
            (REPO_ROOT / "tests/corpus" / approval_path).read_text()
        )
        assert approval_record == {
            "recordId": "approval://example.invalid/part11/customer-procedure-acceptance",
            "recordType": "person-approval",
            "personId": "person://example.invalid/customer/quality-lead",
            "personName": "Synthetic Customer Quality Lead",
            "approvedClauseIds": sorted(CUSTOMER_OWNED),
            "approvedAt": AS_OF,
            "rationale": (
                "Synthetic customer acceptance for the Part 11 procedure "
                "obligations."
            ),
        }
        tag_message = _git(
            repo,
            "for-each-ref",
            "refs/tags/part11-synthetic-approval",
            "--format=%(contents)",
        )
        assert approval_record["recordId"] in tag_message
        assert (
            hashlib.sha256((repo / approval_path).read_bytes()).hexdigest()
            in tag_message
        )

        refs = {
            "commit": _save_tool_output(
                repo, "signature-commit.json", signature_commit
            ),
            "tag": _save_tool_output(repo, "signature-tag.json", signature_tag),
            "approval": approval_path,
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

        customer_owned_facts = {
            fact["clauseId"]: fact
            for fact in facts
            if fact["clauseId"] in CUSTOMER_OWNED
        }
        assert set(customer_owned_facts) == CUSTOMER_OWNED
        for clause_id, fact in customer_owned_facts.items():
            assert fact["kind"] == "disposition"
            assert fact["decision"] == "delegated"
            assert fact["rationale"].strip()
            assert fact["approvalRef"] == (
                f"evidence://example.invalid/{approval_path}"
            )
            assert clause_id in approval_record["approvedClauseIds"]
            assert "evidenceRefs" not in fact
        assert not any(
            fact["kind"] == "direct" and fact["clauseId"] in CUSTOMER_OWNED
            for fact in facts
        )
        resolve_fact_refs(repo, facts)
        resolved_approval = (repo / approval_path).resolve()
        assert resolved_approval.is_relative_to(repo.resolve())
        assert resolved_approval.is_file()
        assert json.loads(resolved_approval.read_text()) == approval_record
        assert approval_record["recordType"] == "person-approval"
        assert approval_record["personId"] == (
            "person://example.invalid/customer/quality-lead"
        )
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
        recorded_clauses = {
            line.split(maxsplit=1)[0] for line in record.stdout.splitlines()
        }
        assert recorded_clauses == {fact["clauseId"] for fact in facts}

        invalid_dispositions = [
            (
                {
                    "kind": "disposition",
                    "clauseId": "11.10(i)",
                    "decision": "delegated",
                    "owner": "customer@example.invalid",
                    "approvalRef": f"evidence://example.invalid/{approval_path}",
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
            assert rows[clause_id]["compliance"] == "tailored"
            assert rows[clause_id]["evidenceRefs"] == []
            fact = customer_owned_facts[clause_id]
            assert rows[clause_id]["tailoringDescription"] == (
                f"delegated (approval {fact['approvalRef']})"
            )
            assert rows[clause_id]["tailoringRationale"] == fact["rationale"]

        missing_ref = "evidence://example.invalid/evidence/missing.json"
        with pytest.raises(
            AssertionError, match=r"11\.10\(e\).*evidence ref does not resolve"
        ) as error:
            resolve_fact_refs(repo, [{**facts[0], "evidenceRefs": [missing_ref]}])
        assert missing_ref in str(error.value)

    assert not pathlib.Path(temporary).exists()
    assert not private_key.exists()

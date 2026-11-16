"""Discharge the HIPAA Security Rule set from a synthetic reference corpus."""

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
    stage_clause_sets,
)

AS_OF = "2026-11-14T00:00:00Z"
M4_KEY = "us-hhs/45-cfr-164-subpart-c@2026-11-12"
CONTEXT = [
    "system_type=closed",
    "electronic_signatures=used",
    "signature_basis=non_biometric",
    "signature_method=identification_code_password",
    "documentation_level=enhanced",
    "qmsr_traceability_applicability=applies",
    "qmsr_advisory_notice_applicability=applies",
    "qmsr_design_development_applicability=applies",
    "qmsr_life_support_applicability=applies",
    "qmsr_servicing_applicability=applies",
    "cyber_device=yes",
    "hipaa_role=covered_entity",
]
DIRECT = "164.308(a)(3)(ii)(A)"
AUDIT_LOGGING = "164.312(b)"
ACCESS_CONTROL = "164.308(a)(4)(ii)(A)"
CLASSIFICATION = "164.308(a)(1)(i)"
ALTERNATIVE = "164.308(a)(3)(ii)(B)"
NOT_REASONABLE = "164.308(a)(3)(ii)(C)"
TRAINING_ALTERNATIVE = "164.308(a)(5)(ii)(A)"
UNDECIDED = "164.308(a)(4)(ii)(B)"
CUSTOMER_OWNED = {
    "164.308(a)(1)(ii)(C)",
    "164.308(b)",
    "164.308(b)(3)",
    "164.314(a)(1)",
    "164.314(a)(2)(i)",
    "164.314(a)(2)(ii)",
    "164.316(a)",
    "164.316(b)(1)",
    "164.316(b)(2)(i)",
    "164.316(b)(2)(ii)",
    "164.316(b)(2)(iii)",
}


def _json(*args: str) -> dict:
    result = run(*args)
    assert result.returncode == 0, result.stderr + result.stdout
    return json.loads(result.stdout)


@pytest.mark.trace("TC-084")
@pytest.mark.trace("FR-021-AC-1")
@pytest.mark.trace("FR-021-AC-2")
@pytest.mark.trace("FR-012-AC-4")
@pytest.mark.trace("FR-012-AC-5")
@pytest.mark.trace("FR-006-AC-2")
@pytest.mark.trace("FR-006-AC-3")
@pytest.mark.trace("FR-019-AC-4")
@pytest.mark.trace("FR-019-AC-5")
def test_m4_discharge_preserves_human_dispositions_and_open_outputs(
    tmp_path: pathlib.Path,
) -> None:
    """Render M4 outcomes from customer facts and keep unproduced outputs open."""
    version = run(engine_tool("quoin"), "--version")
    assert version.returncode == 0, version.stderr
    assert version.stdout.strip() == "0.35.0"

    root = tmp_path / "m4-run"
    root.mkdir()
    project = root / "project"
    project.mkdir()
    shutil.copytree(REPO_ROOT / "tests/corpus", project, dirs_exist_ok=True)

    manifest = yaml.safe_load((PACKAGE_ROOT / "manifest.yaml").read_text())
    module = stage_clause_sets(
        root,
        *(PACKAGE_ROOT / relative for relative in manifest["clause_sets"]),
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

    binding = _json(
        engine_tool("quire"),
        "clauses",
        "evaluate",
        "--module",
        str(module),
        "--authority",
        "us-hhs",
        "--set",
        "45-cfr-164-subpart-c",
        "--version",
        "2026-11-12",
        "--json",
        *sum((["--context", item] for item in CONTEXT), []),
    )
    assert "dispositions" not in binding
    assert "facts" not in binding
    assert all(
        "decision" not in clause and "disposition" not in clause
        for clause in binding["clauses"]
    )
    binding_path = root / "binding.json"
    binding_path.write_text(json.dumps(binding))

    refs = {
        "event": "hipaa/audit-event.json",
        "control": "hipaa/control.json",
        "permissions": "hipaa/role-permission.json",
        "classification": "hipaa/data-classification.json",
        "procedure": "hipaa/customer-procedure-placeholder.txt",
        "addressable_approval": "approvals/hipaa-addressable-acceptance.json",
        "procedure_approval": "approvals/hipaa-procedure-acceptance.json",
    }
    attestation = {
        "attestedBy": "reviewer@example.invalid",
        "authority": "synthetic-customer-security-officer",
        "attestedAt": AS_OF,
        "expiresAt": "2027-11-14T00:00:00Z",
    }
    approval_ref = f"evidence://example.invalid/{refs['addressable_approval']}"
    addressable_approval = json.loads(
        (project / refs["addressable_approval"]).read_text()
    )
    procedure_approval_record = json.loads(
        (project / refs["procedure_approval"]).read_text()
    )
    assert addressable_approval["personName"] == "Synthetic Customer Security Officer"
    assert set(addressable_approval["approvedClauseIds"]) == {
        ALTERNATIVE,
        NOT_REASONABLE,
        TRAINING_ALTERNATIVE,
    }
    assert (
        procedure_approval_record["personName"] == "Synthetic Customer Privacy Officer"
    )
    facts = [
        {
            "kind": "direct",
            "clauseId": DIRECT,
            "evidenceRefs": [
                f"evidence://example.invalid/{refs['control']}",
                f"evidence://example.invalid/{refs['permissions']}",
                f"evidence://example.invalid/{refs['classification']}",
            ],
            "attestation": attestation,
        },
        {
            "kind": "direct",
            "clauseId": AUDIT_LOGGING,
            "evidenceRefs": [f"evidence://example.invalid/{refs['event']}"],
            "attestation": attestation,
        },
        {
            "kind": "direct",
            "clauseId": ACCESS_CONTROL,
            "evidenceRefs": [f"evidence://example.invalid/{refs['permissions']}"],
            "attestation": attestation,
        },
        {
            "kind": "direct",
            "clauseId": CLASSIFICATION,
            "evidenceRefs": [
                f"evidence://example.invalid/{refs['classification']}",
                f"evidence://example.invalid/{refs['control']}",
            ],
            "attestation": attestation,
        },
        {
            "kind": "disposition",
            "clauseId": ALTERNATIVE,
            "decision": "accepted_risk",
            "owner": "customer@example.invalid",
            "rationale": (
                "Alternative measure: synthetic compensating review is "
                "performed weekly."
            ),
            "approvalRef": approval_ref,
            "attestation": attestation,
        },
        {
            "kind": "disposition",
            "clauseId": NOT_REASONABLE,
            "decision": "accepted_risk",
            "owner": "customer@example.invalid",
            "rationale": (
                "Not reasonable and appropriate: the synthetic deployment has no "
                "removable media path."
            ),
            "approvalRef": approval_ref,
            "attestation": attestation,
        },
        {
            "kind": "disposition",
            "clauseId": TRAINING_ALTERNATIVE,
            "decision": "accepted_risk",
            "owner": "customer@example.invalid",
            "rationale": (
                "Alternative measure: synthetic security-awareness records are "
                "reviewed quarterly."
            ),
            "approvalRef": approval_ref,
            "attestation": attestation,
        },
    ]
    procedure_approval = f"evidence://example.invalid/{refs['procedure_approval']}"
    for clause_id in sorted(CUSTOMER_OWNED):
        facts.append(
            {
                "kind": "disposition",
                "clauseId": clause_id,
                "decision": "delegated",
                "owner": "customer@example.invalid",
                "rationale": "The customer owns and maintains the written procedure.",
                "approvalRef": procedure_approval,
                "attestation": attestation,
            }
        )

    resolve_fact_refs(project, facts)
    assert not any(fact["clauseId"] == UNDECIDED for fact in facts)
    facts_path = root / "facts.json"
    facts_path.write_text(json.dumps(facts))
    evidence_store = project / "evidence-store"
    evidence_store.mkdir()
    recorded = run(
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
        str(config),
    )
    assert recorded.returncode == 0, recorded.stderr + recorded.stdout

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
        str(config),
    ]
    for item in CONTEXT:
        args.extend(["--context", item])
    first = run(*args)
    second = run(*args)
    assert first.returncode == 0, first.stderr + first.stdout
    assert second.returncode == 0, second.stderr + second.stdout
    assert first.stdout.encode() == second.stdout.encode()
    report = json.loads(first.stdout)
    indexes = {clause_set_key(entry["clauseSet"]): entry for entry in report["index"]}
    assert M4_KEY in indexes
    m4_matrix = next(
        matrix
        for matrix in report["matrices"]
        if clause_set_key(matrix["clauseSet"]) == M4_KEY
    )
    assert indexes[M4_KEY]["rowCount"] == len(m4_matrix["rows"])
    rows = {
        row["clauseId"]: row for matrix in report["matrices"] for row in matrix["rows"]
    }
    for clause_id in [DIRECT, AUDIT_LOGGING, ACCESS_CONTROL, CLASSIFICATION]:
        assert rows[clause_id]["compliance"] == "compliant"
    for clause_id in [ALTERNATIVE, NOT_REASONABLE, TRAINING_ALTERNATIVE]:
        assert rows[clause_id]["compliance"] == "tailored"
        assert (
            rows[clause_id]["tailoringDescription"]
            == f"accepted_risk (approval {approval_ref})"
        )
        assert rows[clause_id]["tailoringRationale"] == next(
            fact["rationale"] for fact in facts if fact["clauseId"] == clause_id
        )
    assert next(fact for fact in facts if fact["clauseId"] == ALTERNATIVE)[
        "rationale"
    ].startswith("Alternative measure:")
    assert next(fact for fact in facts if fact["clauseId"] == NOT_REASONABLE)[
        "rationale"
    ].startswith("Not reasonable and appropriate:")
    assert next(fact for fact in facts if fact["clauseId"] == TRAINING_ALTERNATIVE)[
        "rationale"
    ].startswith("Alternative measure:")
    assert rows[UNDECIDED]["compliance"] == "undischarged"
    for clause_id in CUSTOMER_OWNED:
        fact = next(item for item in facts if item["clauseId"] == clause_id)
        assert rows[clause_id]["compliance"] == "tailored"
        assert rows[clause_id]["tailoringRationale"] == fact["rationale"]
        assert rows[clause_id]["tailoringDescription"] == (
            f"delegated (approval {procedure_approval})"
        )
        assert rows[clause_id]["evidenceRefs"] == []

    m4_clause_set = next(
        item for item in load_clause_sets() if clause_set_key(item) == M4_KEY
    )
    health_data_flow_clause_ids = {
        clause["id"]
        for clause in m4_clause_set["clauses"]
        if "health-data-flows" in clause["expectedOutputs"]
    }
    health_data_flow_rows = [
        rows[clause_id] for clause_id in health_data_flow_clause_ids
    ]
    assert health_data_flow_rows
    assert all(row["compliance"] == "undischarged" for row in health_data_flow_rows)
    assert all(row["evidenceRefs"] == [] for row in health_data_flow_rows)
    assert not any(
        "health-data-flows" in fact.get("evidenceRefs", []) for fact in facts
    )

    markdown_args = [arg for arg in args if arg != "--json"]
    markdown = run(*markdown_args)
    markdown_repeat = run(*markdown_args)
    assert markdown.returncode == 0, markdown.stderr + markdown.stdout
    assert markdown_repeat.returncode == 0, (
        markdown_repeat.stderr + markdown_repeat.stdout
    )
    assert markdown.stdout.encode() == markdown_repeat.stdout.encode()
    assert M4_KEY in markdown.stdout
    assert "Not compliant - undischarged" in markdown.stdout

    missing_ref = "evidence://example.invalid/evidence/hipaa/missing.json"
    with pytest.raises(
        AssertionError, match=r"164\.308\(a\)\(3\)\(ii\)\(A\).*does not resolve"
    ) as error:
        resolve_fact_refs(
            project,
            [{**facts[0], "evidenceRefs": [missing_ref]}],
        )
    assert missing_ref in str(error.value)

    rejected_facts = [
        {key: value for key, value in facts[4].items() if key != "decision"},
        {key: value for key, value in facts[4].items() if key != "approvalRef"},
    ]
    for index, invalid_fact in enumerate(rejected_facts):
        invalid_facts_path = root / f"invalid-addressable-facts-{index}.json"
        invalid_facts_path.write_text(json.dumps([invalid_fact]))
        invalid_store = root / f"invalid-addressable-store-{index}"
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
            str(config),
        )
        assert rejected.returncode != 0, rejected.stdout
        if index == 1:
            assert "approvalRef" in rejected.stderr + rejected.stdout

    stored_alternative = next(
        path
        for path in evidence_store.rglob("*.json")
        if json.loads(path.read_text()).get("fact", {}).get("clauseId") == ALTERNATIVE
    )
    stored_fact = json.loads(stored_alternative.read_text())
    stored_fact["fact"]["rationale"] = ""
    stored_alternative.write_text(json.dumps(stored_fact))
    refused_report = run(*args)
    assert refused_report.returncode != 0, refused_report.stdout
    assert "rationale" in refused_report.stderr + refused_report.stdout

"""M2 clause outputs are connected to producers or tracked owners."""

from __future__ import annotations

import re

import pytest
from conftest import assert_output_catalog_consistent, clause_set_key, load_clause_sets

PART_820_KEY = "us-fda/21-cfr-820@2026-11-12"
PREMARKET_KEY = "us-fda/premarket-device-software@2023-06-14"
M2_KEYS = {PART_820_KEY, PREMARKET_KEY}

PRODUCER_TOKENS = {
    "risk-management-records": ("spec-objects-safety", "quoin risk-summary"),
    "software-requirements": ("spec-artifacts-iso", "StR", "FR", "NFR"),
    "software-architecture": (
        "spec-objects-architecture",
        "spec-artifacts-process",
        "ADR",
    ),
    "verification-records": ("quire matrix", "quoin matrix", "quire-rs"),
    "release-record": ("release-decision", "release-verify", "quoin release snapshot"),
    "anomaly-list": ("quoin anomaly report",),
}


def _m2_sets() -> list[dict]:
    """Return the Part 820 and premarket sets declared by the module."""
    return [
        clause_set
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) in M2_KEYS
    ]


def _mapping_rows() -> list[dict[str, object]]:
    """Read the normative M2 output mapping table from the master specification."""
    from conftest import REPO_ROOT

    spec = (REPO_ROOT / "spec" / "spec.md").read_text()
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


@pytest.mark.trace("TC-075", "FR-018-AC-1")
def test_m2_output_mapping_covers_every_clause_output_pair_once():
    """The mapping table equals the M2 clause tables without duplicate pairs."""
    expected_pairs = {
        (clause["id"], output)
        for clause_set in _m2_sets()
        for clause in clause_set["clauses"]
        for output in clause["expectedOutputs"]
    }
    rows = _mapping_rows()
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
    rows = _mapping_rows()
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
                    assert (
                        output in PRODUCER_TOKENS
                    ), f"{output}: no verified producer is listed"
                    for token in PRODUCER_TOKENS[output]:
                        assert token in mapping, f"{output}: missing producer {token!r}"
                        assert (
                            token in description
                        ), f"{output}: description omits producer {token!r}"
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

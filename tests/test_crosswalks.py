"""Section 524B and FDA cybersecurity crosswalks to public guidance and NIST."""

from __future__ import annotations

import copy
import csv
import json
import pathlib
import re

import pytest
import yaml
from conftest import (
    REPO_ROOT,
    clause_set_key,
    engine_tool,
    load_clause_sets,
    run,
)

FDCA_KEY = "us-congress/fdca-524b@2026-10-15"
FDA_GUIDANCE_KEY = "us-fda/premarket-cybersecurity@2026-02-03"
HIPAA_KEY = "us-hhs/45-cfr-164-subpart-c@2026-11-12"
NIST_KEY = "nist/sp800-53@5.2.0"
SECURITY_MODULE_NAME = "spec-objects-security"
CPRT_WORKBOOK_URL = (
    "https://csrc.nist.gov/csrc/media/Projects/olir/documents/submissions/"
    "SP800-53_SecurityRule_Crosswalk_2024.xlsx"
)
NIST_DESIGNATOR = re.compile(r"\b(?:ISO|IEC|ANSI|AAMI|IEEE|NEMA|ASTM|UL)\s*[0-9]", re.I)
PREMARKET_DEVICE_SOFTWARE_KEY = "us-fda/premarket-device-software@2023-06-14"
PART_820_KEY = "us-fda/21-cfr-820@2026-11-12"
CLAUSE_DESIGNATOR = re.compile(
    r"\b(?:VI\.[A-J](?:\.enhanced)?|820\.\d+(?:\([a-z0-9]+\))?)", re.I
)


def _source_sets() -> dict[str, dict]:
    return {
        clause_set_key(clause_set): clause_set
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) in {FDCA_KEY, FDA_GUIDANCE_KEY}
    }


def _hipaa_clause_set() -> dict:
    matches = [
        clause_set
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) == HIPAA_KEY
    ]
    assert len(matches) == 1, f"expected exactly one HIPAA set, got {len(matches)}"
    return matches[0]


def _hipaa_expected_rows() -> list[tuple[str, str, str, int]]:
    fixture = REPO_ROOT / "tests" / "fixtures" / "cprt-hipaa-nist-relationships.csv"
    with fixture.open(newline="") as stream:
        return [
            (
                row["reference_element"],
                row["focal_element"],
                row["worksheet"],
                int(row["row"]),
            )
            for row in csv.DictReader(stream)
        ]


def _hipaa_unmapped_source_ids() -> set[str]:
    clause_ids = {clause["id"] for clause in _hipaa_clause_set()["clauses"]}
    source_ids = {row[0] for row in _hipaa_expected_rows()}
    return clause_ids - source_ids


def _normalized_nist_id(source_id: str) -> str:
    without_control_zeroes = re.sub(r"-(0+)(\d+)", r"-\2", source_id)
    return re.sub(r"\((0+)(\d+)\)", r"(\2)", without_control_zeroes)


def _hipaa_crosswalk_row(crosswalk: dict) -> tuple[str, str, str, int]:
    provenance = crosswalk["provenance"]
    return (
        crosswalk["sourceElementId"],
        provenance["focalElement"],
        provenance["worksheet"],
        provenance["row"],
    )


def _unresolved_cprt_targets(
    crosswalks: list[dict], target_clause_ids: set[str]
) -> list[str]:
    failures = []
    for crosswalk in crosswalks:
        target = crosswalk["target"]
        target_set = target["set"]
        target_key = (
            f"{target_set['authority']}/{target_set['id']}@{target_set['version']}"
        )
        if target_key != NIST_KEY or target["clause"] not in target_clause_ids:
            failures.append(
                f"crosswalk {crosswalk['sourceElementId']} -> {target_key}#"
                f"{target['clause']} references unknown target {target['clause']}"
            )
    return failures


def _m2_crosswalk_sets() -> dict[str, dict]:
    return {
        clause_set_key(clause_set): clause_set
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) in {PREMARKET_DEVICE_SOFTWARE_KEY, PART_820_KEY}
    }


def _m2_crosswalk_link_failures(
    crosswalks: list[dict], source_clause_ids: set[str], target_clause_ids: set[str]
) -> list[str]:
    failures = []
    for crosswalk in crosswalks:
        source = crosswalk.get("sourceClause", "")
        if source not in source_clause_ids:
            failures.append(
                f"crosswalk {source!r} has unknown source clause {source!r}"
            )
        target = crosswalk.get("target", {}).get("clause", "")
        if target not in target_clause_ids:
            failures.append(
                f"crosswalk {source!r} has unknown target clause {target!r}"
            )
    return failures


def _m2_crosswalk_metadata_failures(crosswalks: list[dict]) -> list[str]:
    failures = []
    for crosswalk in crosswalks:
        source = crosswalk.get("sourceClause", "")
        if crosswalk.get("relation") not in {"equivalent", "partial", "informative"}:
            failures.append(f"crosswalk {source!r} has an unsupported relation")
        rationale = crosswalk.get("rationale", "").strip()
        if not rationale:
            failures.append(f"crosswalk {source!r} has no rationale")
        elif not rationale.endswith(".") or re.search(
            r"[.!?](?:\s+\S|$).*[.!?]", rationale
        ):
            failures.append(f"crosswalk {source!r} rationale is not one sentence")
        if CLAUSE_DESIGNATOR.search(rationale):
            failures.append(f"crosswalk {source!r} rationale contains a designator")
    return failures


def _crosswalk_table_rows() -> list[tuple[str, str, str, str]]:
    spec = (REPO_ROOT / "spec" / "spec.md").read_text()
    section = spec.split("### Cybersecurity Crosswalk Plan", 1)[1].split(
        "### HIPAA Security Rule Clause Table", 1
    )[0]
    rows = []
    for line in section.splitlines():
        if not line.strip().startswith("| `"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0] != "Source clause":
            rows.append((cells[0], cells[1], cells[2], cells[3]))
    return rows


def _source_key(clause_id: str) -> str:
    return FDCA_KEY if clause_id.startswith("524B") else FDA_GUIDANCE_KEY


def _expected_rows() -> list[tuple[str, str, str, str, str]]:
    return [
        (_source_key(source), source, target, target_clause, relation)
        for source, target, target_clause, relation in _crosswalk_table_rows()
    ]


def _actual_rows() -> list[tuple[str, str, str, str, str]]:
    rows = []
    for source_key, clause_set in _source_sets().items():
        for crosswalk in clause_set.get("crosswalks", []):
            target = crosswalk["target"]
            target_key = (
                f"{target['set']['authority']}/{target['set']['id']}@"
                f"{target['set']['version']}"
            )
            rows.append(
                (
                    source_key,
                    crosswalk["sourceClause"],
                    target_key,
                    target["clause"],
                    crosswalk["relation"],
                )
            )
    return rows


def _installed_security_module() -> pathlib.Path:
    result = run(engine_tool("quoin"), "module", "list")
    assert result.returncode == 0, result.stderr + result.stdout
    modules = json.loads(result.stdout)["plugins"]
    matches = [
        module for module in modules if module.get("name") == SECURITY_MODULE_NAME
    ]
    assert len(matches) == 1, f"expected one installed {SECURITY_MODULE_NAME} module"
    module_path = pathlib.Path(matches[0]["targetPath"]).resolve()
    assert module_path.is_dir(), f"installed module path does not exist: {module_path}"
    assert not module_path.is_relative_to(
        REPO_ROOT.resolve()
    ), "NIST targets must come from the installed module, not a repository copy"
    return module_path


def _installed_nist_clause_ids() -> set[str]:
    module_path = _installed_security_module()
    manifest = yaml.safe_load((module_path / "manifest.yaml").read_text())
    for relative_path in manifest.get("clause_sets", []):
        path = module_path / relative_path
        clause_set = json.loads(path.read_text())
        if clause_set_key(clause_set) == NIST_KEY:
            return {clause["id"] for clause in clause_set["clauses"]}
    pytest.fail(f"installed {SECURITY_MODULE_NAME} does not declare {NIST_KEY}")


def _unresolved_nist_targets(
    crosswalks: list[dict], target_clause_ids: set[str]
) -> list[str]:
    failures = []
    for crosswalk in crosswalks:
        target = crosswalk["target"]
        target_set = target["set"]
        target_key = (
            f"{target_set['authority']}/{target_set['id']}@{target_set['version']}"
        )
        if target_key == NIST_KEY and target["clause"] not in target_clause_ids:
            failures.append(
                f"crosswalk {crosswalk['sourceClause']} -> {target_key}#"
                f"{target['clause']} refers to unknown target clause {target['clause']}"
            )
    return failures


@pytest.mark.trace("FR-011-AC-1")
def test_cybersecurity_crosswalks_match_the_normative_table_exactly() -> None:
    """Compare source, target, relation, and b(4) context to the spec.

    Assumptions:
        The cybersecurity crosswalk plan in spec/spec.md is normative.
    Criteria:
        Each table row appears exactly once, with b(4) targets explicitly contextual.
    Trace: FR-011-AC-1
    """
    expected = _expected_rows()
    actual = _actual_rows()
    assert len(actual) == len(set(actual)), "a cybersecurity crosswalk row is repeated"
    assert set(actual) == set(expected), (
        f"missing crosswalks: {sorted(set(expected) - set(actual))}; "
        f"unexpected crosswalks: {sorted(set(actual) - set(expected))}"
    )

    b4_crosswalks = [
        crosswalk
        for crosswalk in _source_sets()[FDCA_KEY]["crosswalks"]
        if crosswalk["sourceClause"] == "524B(b)(4)"
    ]
    assert {
        (crosswalk["target"]["set"]["id"], crosswalk["target"]["clause"])
        for crosswalk in b4_crosswalks
    } == {
        ("premarket-cybersecurity", "VII.C.2"),
        ("sp800-53", "SA-8"),
    }
    assert all(crosswalk["relation"] == "informative" for crosswalk in b4_crosswalks)
    assert all(
        "only as context" in crosswalk["rationale"] for crosswalk in b4_crosswalks
    )


@pytest.mark.trace("FR-011-AC-2")
def test_every_524b_clause_crosswalks_to_fda_guidance() -> None:
    """Require each statutory clause to reference at least one FDA guidance clause.

    Assumptions:
        The 524B and guidance clause IDs are declared in their clause-set files.
    Criteria:
        Every 524B source ID has a crosswalk to a clause in the FDA guidance set.
    Trace: FR-011-AC-2
    """
    sets = _source_sets()
    statutory_ids = {clause["id"] for clause in sets[FDCA_KEY]["clauses"]}
    guidance_ids = {clause["id"] for clause in sets[FDA_GUIDANCE_KEY]["clauses"]}
    targets_by_source: dict[str, set[str]] = {}
    for crosswalk in sets[FDCA_KEY].get("crosswalks", []):
        target = crosswalk["target"]
        target_key = (
            f"{target['set']['authority']}/{target['set']['id']}@"
            f"{target['set']['version']}"
        )
        if target_key == FDA_GUIDANCE_KEY:
            targets_by_source.setdefault(crosswalk["sourceClause"], set()).add(
                target["clause"]
            )

    assert set(targets_by_source) == statutory_ids, (
        f"524B clauses without guidance crosswalks: "
        f"{sorted(statutory_ids - set(targets_by_source))}"
    )
    for source_id, targets in targets_by_source.items():
        assert targets, f"524B clause {source_id} has no FDA guidance target"
        assert targets <= guidance_ids, (
            f"524B clause {source_id} references unknown FDA guidance clauses "
            f"{sorted(targets - guidance_ids)}"
        )


@pytest.mark.trace("FR-011-AC-3", "FR-011-AC-5")
def test_every_cybersecurity_clause_resolves_nist_targets_from_module() -> None:
    """Resolve every cybersecurity clause's NIST target through the installed module.

    Assumptions:
        CI installs default Quire modules before tests; NIST files are not copied.
    Criteria:
        Every 524B and FDA guidance clause has an existing NIST target.
    Trace: FR-011-AC-3, FR-011-AC-5
    """
    sets = _source_sets()
    source_ids = {
        (source_key, clause["id"])
        for source_key, clause_set in sets.items()
        for clause in clause_set["clauses"]
    }
    nist_crosswalks = []
    sources_with_nist_targets = set()
    for source_key, clause_set in sets.items():
        for crosswalk in clause_set.get("crosswalks", []):
            target = crosswalk["target"]
            target_set = target["set"]
            target_key = (
                f"{target_set['authority']}/{target_set['id']}@"
                f"{target_set['version']}"
            )
            if target_key == NIST_KEY:
                nist_crosswalks.append(crosswalk)
                sources_with_nist_targets.add((source_key, crosswalk["sourceClause"]))

    assert sources_with_nist_targets == source_ids, (
        f"cybersecurity clauses without NIST targets: "
        f"{sorted(source_ids - sources_with_nist_targets)}"
    )
    failures = _unresolved_nist_targets(nist_crosswalks, _installed_nist_clause_ids())
    assert failures == [], "\n".join(failures)


@pytest.mark.trace("FR-011-AC-4")
def test_unknown_nist_target_fails_with_the_source_and_target_ids() -> None:
    """A synthetic missing NIST target names its originating crosswalk.

    Assumptions:
        The validator uses the installed NIST clause IDs as its target catalog.
    Criteria:
        Injecting XX-99 yields a diagnostic naming the source, target, and crosswalk.
    Trace: FR-011-AC-4
    """
    targets = _installed_nist_clause_ids()
    crosswalk = next(
        item
        for item in _actual_crosswalks()
        if item["target"]["set"]["id"] == "sp800-53"
    )
    fixture = copy.deepcopy(crosswalk)
    fixture["target"]["clause"] = "XX-99"

    failures = _unresolved_nist_targets([fixture], targets)
    assert len(failures) == 1
    assert fixture["sourceClause"] in failures[0]
    assert "XX-99" in failures[0]
    assert "crosswalk" in failures[0]


def _actual_crosswalks() -> list[dict]:
    return [
        crosswalk
        for clause_set in _source_sets().values()
        for crosswalk in clause_set.get("crosswalks", [])
    ]


@pytest.mark.trace("FR-011-AC-3", "FR-011-AC-5")
def test_crosswalks_have_valid_relations_rationales_and_no_standard_designators() -> (
    None
):
    """Crosswalk metadata is authored, informative, and avoids paywalled standards.

    Assumptions:
        `informative` is the relation prescribed for every row in the spec plan.
    Criteria:
        Each row has a nonblank rationale, a supported relation, and no standards
        designator in its rationale.
    Trace: FR-011-AC-3, FR-011-AC-5
    """
    allowed_relations = {"equivalent", "partial", "informative"}
    crosswalks = _actual_crosswalks()
    assert crosswalks, "no cybersecurity crosswalks are present"
    for crosswalk in crosswalks:
        source = crosswalk["sourceClause"]
        assert (
            crosswalk["relation"] in allowed_relations
        ), f"crosswalk {source} has unsupported relation {crosswalk['relation']!r}"
        rationale = crosswalk.get("rationale", "")
        assert rationale.strip(), f"crosswalk {source} has no rationale"
        assert not NIST_DESIGNATOR.search(
            rationale
        ), f"crosswalk {source} names a standards designator"


@pytest.mark.trace("FR-011-AC-5")
def test_nist_target_catalog_is_read_from_the_installed_module_not_a_copy() -> None:
    """The resolver reads the declared NIST set only from the installed module.

    Assumptions:
        `quoin module ensure-defaults` installs spec-objects-security in CI.
    Criteria:
        The NIST file is declared by that installed module and is not tracked here.
    Trace: FR-011-AC-5
    """
    module_path = _installed_security_module()
    manifest = yaml.safe_load((module_path / "manifest.yaml").read_text())
    assert any(
        clause_set_key(json.loads((module_path / relative_path).read_text()))
        == NIST_KEY
        for relative_path in manifest.get("clause_sets", [])
    ), f"installed module does not declare {NIST_KEY}"

    tracked = run("git", "ls-files", "*nist-sp800-53*.json", cwd=REPO_ROOT)
    assert tracked.returncode == 0, tracked.stderr
    assert (
        tracked.stdout.strip() == ""
    ), "NIST clause data was copied into this repository"


@pytest.mark.trace("FR-013-AC-1", "FR-013-AC-3")
def test_hipaa_crosswalks_match_the_exact_public_cprt_workbook_rows() -> None:
    """Bind each HIPAA mapping to the workbook row and its original direction.

    Assumptions:
        The identifier-only fixture was extracted directly from the official
        workbook and records its focal/reference values and row locators.
    Criteria:
        The packaged crosswalk has exactly those rows and keeps the published
        NIST-focal to HIPAA-reference direction.
    """
    clause_set = _hipaa_clause_set()
    crosswalks = clause_set.get("cprtCrosswalks", [])
    expected = _hipaa_expected_rows()
    actual = [_hipaa_crosswalk_row(item) for item in crosswalks]

    assert len(actual) == len(set(actual)), "a HIPAA CPRT row is repeated"
    assert set(actual) == set(expected), (
        f"missing rows: {sorted(set(expected) - set(actual))}; "
        f"unexpected rows: {sorted(set(actual) - set(expected))}"
    )
    expected_pairs = {
        (source, _normalized_nist_id(focal)) for source, focal, _, _ in expected
    }
    actual_pairs = {
        (item["sourceElementId"], item["target"]["clause"]) for item in crosswalks
    }
    assert actual_pairs == expected_pairs
    for crosswalk in crosswalks:
        assert set(crosswalk) <= {
            "sourceElementId",
            "target",
            "provenance",
            "normalization",
            "relation",
            "rationale",
        }
        assert {
            "sourceElementId",
            "target",
            "provenance",
            "relation",
            "rationale",
        } <= set(crosswalk)
        assert set(crosswalk["target"]) == {"set", "clause"}
        assert crosswalk["target"]["set"] == {
            "authority": "nist",
            "id": "sp800-53",
            "version": "5.2.0",
        }
        provenance = crosswalk["provenance"]
        assert set(provenance) == {
            "workbook",
            "worksheet",
            "row",
            "direction",
            "focalElement",
            "referenceElement",
        }
        assert crosswalk["sourceElementId"] == provenance["referenceElement"]
        assert isinstance(provenance["row"], int) and provenance["row"] > 1
        assert provenance["worksheet"]
        workbook = provenance["workbook"]
        assert set(workbook) == {
            "id",
            "title",
            "version",
            "released",
            "url",
        }
        assert workbook["url"] == CPRT_WORKBOOK_URL
        assert workbook["id"] == "SP800-66R2-800-53R5.1.1"
        assert workbook["title"] == "SP-800-66-Rev-2-to-SP-800-53-Rev-5.1.1"
        assert workbook["version"] == "1.0.0"
        assert provenance["direction"] == "focal-to-reference"
        assert provenance["focalElement"] == crosswalk["target"]["clause"] or (
            crosswalk.get("normalization", {}).get("from") == provenance["focalElement"]
        )
        expected_relation = (
            "informative"
            if provenance["worksheet"] == "Relationships-AC"
            else "partial"
        )
        assert crosswalk["relation"] == expected_relation
        assert crosswalk["rationale"].strip()
        assert not NIST_DESIGNATOR.search(crosswalk["rationale"])
        if expected_relation == "informative":
            assert crosswalk["rationale"] == (
                "SP 800-66 Rev. 2 lists this control as related to the cited "
                "HIPAA element; this is an informative reference, not an "
                "implementation claim."
            )
        else:
            assert crosswalk["rationale"] == (
                "SP 800-66 Rev. 2 maps this control to the cited HIPAA element; "
                "this indicates partial correspondence, not full coverage or "
                "equivalence."
            )
    assert not clause_set.get(
        "crosswalks"
    ), "parent-level source elements must not be represented as native clause refs"


@pytest.mark.trace("FR-013-AC-2")
def test_hipaa_cprt_crosswalks_cover_only_the_included_security_standards() -> None:
    """Check source-standard coverage and the excluded business-associate clause."""
    crosswalks = _hipaa_clause_set().get("cprtCrosswalks", [])
    covered_standards = set()
    for crosswalk in crosswalks:
        source = crosswalk["sourceElementId"]
        for standard in ("164.308", "164.310", "164.312", "164.316"):
            if source.startswith(standard):
                covered_standards.add(standard)
        if source.startswith("164.314(a)"):
            covered_standards.add("164.314(a)")

    assert covered_standards == {
        "164.308",
        "164.310",
        "164.312",
        "164.314(a)",
        "164.316",
    }
    assert not any(
        crosswalk["sourceElementId"].startswith("164.314(b)")
        for crosswalk in crosswalks
    ), "§ 164.314(b) must not be included"

    installed_targets = _installed_nist_clause_ids()
    assert _unresolved_cprt_targets(crosswalks, installed_targets) == []

    invalid_fixture = json.loads(
        (
            REPO_ROOT / "tests" / "fixtures" / "cprt-invalid-target-ac-999.json"
        ).read_text()
    )
    failures = _unresolved_cprt_targets([invalid_fixture], installed_targets)
    assert len(failures) == 1
    assert invalid_fixture["sourceElementId"] in failures[0]
    assert "AC-999" in failures[0]
    assert "crosswalk" in failures[0]


@pytest.mark.trace("FR-013-AC-3")
def test_hipaa_unmapped_clauses_targets_and_normalizations_are_explicit() -> None:
    """Reject inferred mappings, absent targets, and unrecorded normalization."""
    clause_set = _hipaa_clause_set()
    crosswalks = clause_set.get("cprtCrosswalks", [])
    unmapped = clause_set.get("unmappedSourceClauses", [])
    expected_unmapped = _hipaa_unmapped_source_ids()
    hipaa_clause_ids = {clause["id"] for clause in clause_set["clauses"]}

    assert set(unmapped) == expected_unmapped
    assert set(unmapped) <= hipaa_clause_ids
    assert not set(unmapped) & {item["sourceElementId"] for item in crosswalks}

    installed_targets = _installed_nist_clause_ids()
    for crosswalk in crosswalks:
        target = crosswalk["target"]
        target_set = target["set"]
        target_key = (
            f"{target_set['authority']}/{target_set['id']}@{target_set['version']}"
        )
        assert target_key == NIST_KEY
        target_id = target["clause"]
        assert target_id in installed_targets, f"unknown NIST target {target_id}"

        provenance = crosswalk["provenance"]
        source_target_id = provenance["focalElement"]
        normalized_id = _normalized_nist_id(source_target_id)
        assert normalized_id == target_id
        normalization = crosswalk.get("normalization")
        if source_target_id == target_id:
            assert (
                normalization is None
            ), "unchanged targets must not claim normalization"
        else:
            assert normalization == {
                "method": "leading-zero-removal",
                "from": source_target_id,
                "to": target_id,
                "reason": (
                    "The installed 5.2.0 catalog uses the control and enhancement "
                    "numbers without leading zeroes."
                ),
            }, f"unrecorded or incorrect normalization for {source_target_id}"


@pytest.mark.trace("FR-017-AC-1")
def test_premarket_crosswalk_pairs_match_the_m2_table_and_resolve() -> None:
    """Every guidance clause has exactly its declared Part 820 targets.

    Assumptions:
        The M2 Section VI crosswalk target column is normative.
    Criteria:
        The complete source-target set matches the table and all IDs resolve.
    """
    expected_pairs = {
        ("VI.A", "820.10(a)"),
        ("VI.A", "820.10(c)"),
        ("VI.B", "820.10(a)"),
        ("VI.B", "820.10(c)"),
        ("VI.C", "820.10(a)"),
        ("VI.C", "820.10(c)"),
        ("VI.D", "820.10(a)"),
        ("VI.D", "820.10(c)"),
        ("VI.E", "820.10(c)"),
        ("VI.F.enhanced", "820.10(c)"),
        ("VI.G", "820.10(a)"),
        ("VI.G", "820.10(c)"),
        ("VI.G.enhanced", "820.10(a)"),
        ("VI.G.enhanced", "820.10(c)"),
        ("VI.H", "820.10(a)"),
        ("VI.H", "820.10(c)"),
        ("VI.H.enhanced", "820.10(a)"),
        ("VI.H.enhanced", "820.10(c)"),
        ("VI.I", "820.10(a)"),
        ("VI.J", "820.10(a)"),
    }
    sets = _m2_crosswalk_sets()
    assert set(sets) == {PREMARKET_DEVICE_SOFTWARE_KEY, PART_820_KEY}
    source_set = sets[PREMARKET_DEVICE_SOFTWARE_KEY]
    part_820_set = sets[PART_820_KEY]
    rows = source_set["crosswalks"]
    actual_pairs = {(row["sourceClause"], row["target"]["clause"]) for row in rows}
    source_ids = {clause["id"] for clause in source_set["clauses"]}
    target_ids = {clause["id"] for clause in part_820_set["clauses"]}

    assert len(actual_pairs) == len(rows), "an M2 crosswalk pair is duplicated"
    assert actual_pairs == expected_pairs, (
        f"missing pairs: {sorted(expected_pairs - actual_pairs)}; "
        f"unexpected pairs: {sorted(actual_pairs - expected_pairs)}"
    )
    assert {source for source, _ in actual_pairs} == source_ids
    assert not _m2_crosswalk_link_failures(rows, source_ids, target_ids)


@pytest.mark.trace("FR-017-AC-2")
def test_crosswalk_unknown_source_or_target_fails_with_identifier() -> None:
    """Cross-set link validation names the invalid identifier and its row.

    Assumptions:
        Crosswalk references are validated against declared clause IDs.
    Criteria:
        Unknown source and target fixtures each produce a crosswalk diagnostic.
    """
    sets = _m2_crosswalk_sets()
    source_set = sets[PREMARKET_DEVICE_SOFTWARE_KEY]
    part_820_set = sets[PART_820_KEY]
    source_ids = {clause["id"] for clause in source_set["clauses"]}
    target_ids = {clause["id"] for clause in part_820_set["clauses"]}
    valid_row = source_set["crosswalks"][0]

    unknown_source = copy.deepcopy(valid_row)
    unknown_source["sourceClause"] = "unknown-source"
    source_failures = _m2_crosswalk_link_failures(
        [unknown_source], source_ids, target_ids
    )
    assert len(source_failures) == 1
    assert "crosswalk" in source_failures[0] and "unknown-source" in source_failures[0]

    unknown_target = copy.deepcopy(valid_row)
    unknown_target["target"]["clause"] = "unknown-target"
    target_failures = _m2_crosswalk_link_failures(
        [unknown_target], source_ids, target_ids
    )
    assert len(target_failures) == 1
    assert "crosswalk" in target_failures[0] and "unknown-target" in target_failures[0]


@pytest.mark.trace("FR-017-AC-3")
def test_crosswalk_requires_relation_and_nonblank_rationale() -> None:
    """Each M2 row has authored relation and original single-sentence rationale.

    Assumptions:
        The supported native crosswalk relation values are closed.
    Criteria:
        Rows use a supported relation, have one sentence, and contain no clause IDs.
    """
    sets = _m2_crosswalk_sets()
    rows = sets[PREMARKET_DEVICE_SOFTWARE_KEY]["crosswalks"]
    assert rows
    assert not _m2_crosswalk_metadata_failures(rows)

    missing_relation = copy.deepcopy(rows[0])
    missing_relation.pop("relation")
    assert (
        "unsupported relation" in _m2_crosswalk_metadata_failures([missing_relation])[0]
    )
    blank_rationale = copy.deepcopy(rows[0])
    blank_rationale["rationale"] = "  "
    assert "no rationale" in _m2_crosswalk_metadata_failures([blank_rationale])[0]
    multiple_sentences = copy.deepcopy(rows[0])
    multiple_sentences["rationale"] = (
        "This provides context. It does not assert equivalence."
    )
    assert (
        "not one sentence" in _m2_crosswalk_metadata_failures([multiple_sentences])[0]
    )
    named_designator = copy.deepcopy(rows[0])
    named_designator["rationale"] = "This relates to 820.10(a)."
    assert "designator" in _m2_crosswalk_metadata_failures([named_designator])[0]


@pytest.mark.trace("FR-017-AC-4")
def test_crosswalk_is_informative_and_does_not_claim_equivalence() -> None:
    """M2 crosswalks remain descriptive relations without derived control facts.

    Assumptions:
        The clause-set crosswalk model stores references, relations, and rationale.
    Criteria:
        Every row is informative and the records contain no derived fact fields.
    """
    rows = _m2_crosswalk_sets()[PREMARKET_DEVICE_SOFTWARE_KEY]["crosswalks"]
    assert rows
    for row in rows:
        assert (
            row["relation"] == "informative"
        ), f"crosswalk {row['sourceClause']} asserts {row['relation']!r}"
        assert set(row) == {
            "sourceClause",
            "target",
            "relation",
            "rationale",
        }, (
            f"crosswalk {row['sourceClause']} contains fields beyond "
            "descriptive metadata"
        )

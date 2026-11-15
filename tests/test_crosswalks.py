"""Section 524B and FDA cybersecurity crosswalks to public guidance and NIST."""

from __future__ import annotations

import copy
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
NIST_KEY = "nist/sp800-53@5.2.0"
SECURITY_MODULE_NAME = "spec-objects-security"
NIST_DESIGNATOR = re.compile(r"\b(?:ISO|IEC|ANSI|AAMI|IEEE|NEMA|ASTM|UL)\s*[0-9]", re.I)


def _source_sets() -> dict[str, dict]:
    return {
        clause_set_key(clause_set): clause_set
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) in {FDCA_KEY, FDA_GUIDANCE_KEY}
    }


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


@pytest.mark.trace("TC-047", "FR-011-AC-1")
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


@pytest.mark.trace("TC-048", "FR-011-AC-2")
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


@pytest.mark.trace("TC-049", "FR-011-AC-3", "FR-011-AC-5")
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


@pytest.mark.trace("TC-050", "FR-011-AC-4")
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


@pytest.mark.trace("TC-051", "FR-011-AC-3", "FR-011-AC-5")
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


@pytest.mark.trace("TC-051", "FR-011-AC-5")
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

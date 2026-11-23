# US Health-Law Compliance Pack

A clause-set module for [Quoin](https://github.com/agent-ix/quoin) and Quire
that helps a team building medical-device or health software record, clause by
clause, the evidence it holds against US health-law obligations, and render
the result as a requirements mapping matrix (RMM).

The pack is for you if you build a device, software as a medical device, or
software that handles electronic protected health information, and you want a
repeatable, reviewable record of what evidence backs each obligation.

The pack records evidence. It does not decide whether you comply. See
[What the tool does not do](#what-the-tool-does-not-do).

## What is in the pack

Six clause sets. Every clause is a short summary in our own words with a
citation to the public source; no text from paywalled standards is included.
All six sources are US federal law or US Government guidance.

| Clause set | Source |
| --- | --- |
| `us-fda/21-cfr-11` | 21 CFR Part 11, electronic records and electronic signatures |
| `us-fda/21-cfr-820` | 21 CFR Part 820, Quality Management System Regulation |
| `us-congress/fdca-524b` | FD&C Act section 524B, cybersecurity of devices |
| `us-fda/premarket-cybersecurity` | FDA guidance: cybersecurity in medical devices, premarket submissions and QMS considerations |
| `us-fda/premarket-device-software` | FDA guidance: content of premarket submissions for device software functions |
| `us-hhs/45-cfr-164-subpart-c` | HIPAA Security Rule (45 CFR Part 164 Subpart C) |

Each clause carries an identifier, a force (mandatory or recommended), an
applicability rule over context you declare, and the named outputs that would
back it. Crosswalks are informative links to related clauses: 524B to the
FDA cybersecurity guidance and to NIST SP 800-53, the FDA cybersecurity
guidance to NIST SP 800-53, the device-software guidance to Part 820, and the
HIPAA Security Rule to NIST SP 800-53.

## Install

From npm, once the package is published:

```sh
quoin module install package:@agent-ix/spec-clauses-us-health
```

From git, which works today:

```sh
quoin module install github:agent-ix/spec-clauses-us-health//spec_clauses_us_health
```

Check it with `quoin module list`.

Several commands in the tables below are `engineering-assurance` commands.
That CLI is a native binary and is not part of the npm toolchain. Install it
with Cargo:

```sh
cargo install --git https://github.com/agent-ix/engineering-assurance \
  --locked --features full --bin engineering-assurance
```

## Use it

1. Declare your context, for example `system_type=closed`. Applicability is
   computed from context you supply. The pack never guesses it, and a clause
   whose context is missing shows as unresolved.
2. Evaluate a clause set to get a binding report with
   `quire clauses evaluate --module <installed module path> --authority <a> --set <s> --version <v> --json --context key=value`.
3. Record your discharge facts with `quoin evidence record-discharge`. A fact is
   either direct (evidence references plus an attestation) or a disposition.
   A disposition has a `decision` (`delegated`, `accepted_risk` or
   `temporary_exception`), an `owner`, a `rationale` and an `approvalRef`.
   Every fact, direct or disposition, needs an `attestation` object
   (`attestedBy`, `authority`, `attestedAt`, `expiresAt`). A
   `temporary_exception` also needs `decisionExpiresAt`, no later than the
   attestation's `expiresAt`.
4. Render the matrix for every set with `quoin discharge --rmm --pack`.

### Example

This is a real run in an empty git repository with a throwaway home
directory. It records evidence for one Part 11 clause and leaves the rest
open.

```sh
M=$HOME/.ix/filament/modules/spec_clauses_us_health   # installed module path

quire clauses evaluate --module $M --authority us-fda --set 21-cfr-11 \
  --version 2026-11-12 --json \
  --context system_type=closed --context electronic_signatures=not_used \
  > binding.json

cat > facts.json <<'JSON'
[{"kind": "direct", "clauseId": "11.10(a)",
  "evidenceRefs": ["evidence/matrix.json"],
  "attestation": {"attestedBy": "qa@example.com", "authority": "quality-lead",
                  "attestedAt": "2026-11-14T00:00:00Z",
                  "expiresAt": "2027-11-14T00:00:00Z"}}]
JSON

quoin evidence record-discharge --binding binding.json --facts facts.json

quoin discharge --rmm --pack spec_clauses_us_health --repo . \
  --as-of 2026-11-14T00:00:00Z \
  --context system_type=closed --context electronic_signatures=not_used
```

Trimmed output (the other sets' matrices and most rows are left out; the rest
is verbatim, including the Markdown escaping):

```text
# Requirements mapping matrix: us-fda/21-cfr-11@2026-11-12

| Req# | Applicability | Compliance | Evidence | Tailoring Description | Tailoring Rationale |
| --- | --- | --- | --- | --- | --- |
| 11.10\(a\) | Applicable | Compliant | evidence/matrix.json | - | - |
| 11.10\(b\) | Applicable | Not compliant - undischarged: no discharge fact | - | - | - |
| 11.30 | Not applicable | Not applicable | - | Not applicable per binding derivation | no reason given by the binding report |
```

A disposition goes in the same facts file. This one, for a temporary
exception, was accepted by `record-discharge`:

```json
{"kind": "disposition", "clauseId": "11.10(c)", "decision": "temporary_exception",
 "owner": "qa@example.com", "rationale": "Audit trail export is delivered next quarter.",
 "approvalRef": "evidence/approval.json", "decisionExpiresAt": "2027-02-01T00:00:00Z",
 "attestation": {"attestedBy": "qa@example.com", "authority": "quality-lead",
                 "attestedAt": "2026-11-14T00:00:00Z", "expiresAt": "2027-11-14T00:00:00Z"}}
```

It renders as `Tailored`, with the decision and approval reference in the
Tailoring Description column and the rationale in the Tailoring Rationale
column.

The same run lists the 524B clauses as `Unresolved` because the context did
not declare `cyber_device`.

## What each clause set needs

"Tool produces" lists outputs whose catalog entry names a Quoin, Quire or
engineering-assurance command or capability. "You supply" lists everything
else: records you author, documents, procedures and settings. The tool never
fills these in.

Records you author in the shipped record types (requirements, architecture,
security risk, hazard, data-flow and baseline records) are yours. They are
checked against their schema with `quire validate`, which does not judge their
content. "Nothing" under "Tool produces" means no command writes a report for
that clause. It does not mean nothing checks your records.

### 21 CFR Part 11

Context: `system_type`, `electronic_signatures`, `signature_basis`,
`signature_method`, and for open systems one appropriateness choice per
paragraph of 11.10.

| Clauses | Tool produces | You supply | Limits |
| --- | --- | --- | --- |
| 11.10 controls | Test and verification records (`quire matrix`, `quoin matrix`, `quoin evidence record`); audit trail (engineering-assurance `approval-trail` capability) | System validation evidence, access-control settings, written procedures, training records | 11.10(i) and 11.10(j) are your procedures and training |
| 11.30 | Signed-record verification (`signature-verify` capability) | Access-control settings | Open systems only |
| 11.50, 11.70 | Signed-record verification, signer registry and audit trail (`approval-trail`, `signature-verify`), signature meaning (`approval-verify`) | None beyond signing your records | Needs signed commits and an allowed-signers file |
| 11.100 | Signer registry and approval trail (`approval-trail`) | Evidence that the certification was submitted to FDA | The FDA certification is yours |
| 11.200, 11.300 | Signer registry (`approval-trail`) | Access-control settings, written procedures, validation evidence | 11.300(b) and (c) are your procedures |

### 21 CFR Part 820

Context: five `qmsr_*_applicability` choices (traceability, advisory notices,
design and development, life support, servicing).

| Clauses | Tool produces | You supply | Limits |
| --- | --- | --- | --- |
| 820.10 quality system | Release snapshot (`quoin release snapshot`), verification records (`quire matrix`, `quoin evidence record`), risk summary (`quoin risk-summary`) | Requirements and architecture records, device identification, written procedures, traceability, complaint, report and advisory-notice records | Most records are yours |
| 820.35 | Nothing | Complaint, service and device-identification records | Entirely customer records |
| 820.45 | Release snapshot (`quoin release snapshot`) | Written procedures, labeling inspection records | Procedures are yours |

### FD&C Act section 524B

Context: `cyber_device`, `additional_cybersecurity_regulation`.

| Clauses | Tool produces | You supply | Limits |
| --- | --- | --- | --- |
| All 524B clauses | Component report (`quoin soup report`), anomaly report (`quoin anomaly report`), recorded scanner and SBOM results (`quoin evidence record --adapter osv-scanner`, `--adapter sbom`) | Security risk records, the SBOM itself (for example generated with Syft through `producer-execute`), vulnerability-management plan, evidence for any additional requirements FDA issues by regulation | The assessment of each finding is written by a person |

### FDA premarket cybersecurity guidance

Context: `cyber_device`. It affects only VII.C.1 to VII.C.3; the other clauses
do not depend on it.

| Clauses | Tool produces | You supply | Limits |
| --- | --- | --- | --- |
| V.A to V.C | Threat model document (`quoin dossier generate --doc threat-model`), data-flow findings (`quire relations --flow`), SBOM and component report, anomaly report, recorded test results (`quoin evidence record`) | Security risk assessment, architecture views document, dynamic and penetration test results | Threat model needs your security records first |
| VI.B | Nothing | Vulnerability-management plan | Customer document |
| VII.C | Anomaly report, data-flow findings, SBOM and component report, recorded test results | Vulnerability-management plan, security risk assessment | Findings need a person's assessment |

### FDA device-software guidance

Context: `documentation_level` (`basic` or `enhanced`). You choose the level;
the tool never assigns it.

| Clauses | Tool produces | You supply | Limits |
| --- | --- | --- | --- |
| VI.A to VI.J | Risk summary (`quoin risk-summary`), verification records (`quire matrix`, `quoin evidence record`), release snapshot (`quoin release snapshot`), anomaly list (`quoin anomaly report`) | Documentation-level statement, software description, requirements, architecture, design, procedures, configuration-management plan | Enhanced-level clauses apply only if you declare it |

### HIPAA Security Rule

Context: `hipaa_role` (`covered_entity` or `business_associate`). It affects only
164.314(a)(2)(ii) and (iii); the rest of the set does not depend on it. Required
and addressable implementation specifications are handled separately; an
addressable one can be met directly, by an alternative measure, or by a
recorded decision that it is not reasonable and appropriate.

| Clauses | Tool produces | You supply | Limits |
| --- | --- | --- | --- |
| 164.308 administrative | Nothing | Security controls, risk records, written procedures, audit-logging and access-control records | Mostly procedures |
| 164.310 physical | Nothing | Security controls, written procedures | Mostly procedures |
| 164.312 technical | Health-data flow projection (`quire relations --health-data-flows`) | Access-control records, security controls, audit-logging records, procedures | Needs a declared architecture model |
| 164.314, 164.316 | Nothing | Written procedures and documentation | Procedures only |

## What the tool does not do

- It never assigns risk scores, safety or security classes, documentation
  levels or acceptability. People accept risk, choose levels and approve.
- It never decides compliance. A clause state is a report of the evidence you
  recorded, as of the `--as-of` time you give. The matrix prints these states:
  - **Compliant**: a direct fact is recorded and its attestation is current at
    `--as-of`.
  - **Tailored**: a disposition is recorded with an owner, rationale and
    approval reference, and its attestation is current.
  - **Not compliant - undischarged: no discharge fact**: nothing is recorded
    for the clause.
  - **Not compliant - attestation not current**: a fact exists but its
    attestation has expired at `--as-of` (the matrix says "discharge fact is
    expired"). A `temporary_exception` past its end date prints
    **Not compliant - temporary exception expired**.
  - **Undetermined**: a context value the clause depends on is not declared.
    The applicability column shows Unresolved.
  - **Not applicable**: the declared context excludes the clause.

  "Not compliant" only means nothing current is recorded for that clause. It
  is not a finding that you fail the regulation.
- Customer-owned clauses, where every expected output is a procedure, need
  your own written procedures. The pack records that you own them, not that
  they exist or are adequate.
- It is not legal advice and does not certify anything.

## Known limits

- **Evidence checks are shallow.** `quoin discharge` shows a clause as
  compliant when a direct fact with evidence references and an attestation is
  recorded. In a test run on the current release, a reference to a file that does not exist was
  accepted the same way. Check that your evidence is real and sufficient;
  the matrix does not do it for you.
- **Customer-supplied records stay undischarged.** Quoin has no
  customer-artifact record kind yet, so clauses whose outputs are documents,
  procedures or records you supply remain undischarged in the matrix unless
  you record a disposition for them. A direct fact does not turn such an
  output into tool-produced evidence.

## Development

Specification: [`spec/spec.md`](spec/spec.md). Clause data:
`spec_clauses_us_health/clauses/`. Content rules: [`CONTENT_RIGHTS.md`](CONTENT_RIGHTS.md).
Licensed under the AGPL-3.0-or-later.

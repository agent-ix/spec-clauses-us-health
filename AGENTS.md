# spec-clauses-us-health

This repository is spec-first. Keep implementation, CI, clause JSON, and the
reference corpus in their separately scoped tickets.

## Specification commands

```bash
quire validate --scope . --module "$QUIRE_SPEC_ARTIFACTS_ISO_MODULE" "spec/**/*.md"
```

Set `QUIRE_SPEC_ARTIFACTS_ISO_MODULE` to the installed `spec-artifacts-iso`
module directory before running the command.

Use the installed Quire schema and templates when authoring additional spec
artifacts. Clause descriptions must be original wording. Public law may be
named and cited; do not reproduce or paraphrase paywalled standards.

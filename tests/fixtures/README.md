# CPRT test fixture

`cprt-hipaa-nist-relationships.csv` contains only NIST workbook identifiers,
worksheet names, and one-based row numbers. It contains no control descriptions
or HIPAA text.

Source: NIST CPRT, **SP-800-66-Rev-2-to-SP-800-53-Rev-5.1.1**, framework
`SP800-66R2-800-53R5.1.1`, version `1.0.0`, released 2024-03-20:
<https://csrc.nist.gov/csrc/media/Projects/olir/documents/submissions/SP800-53_SecurityRule_Crosswalk_2024.xlsx>

The selected records are the rows whose reference element belongs to §§
164.308, 164.310, 164.312, 164.314(a), or 164.316. The workbook's focal
element is the NIST control; its reference element is the HIPAA Security Rule
identifier. NIST publications are generally public domain in the United States;
see the [NIST publication rights FAQ](https://www.nist.gov/nist-research-library/library-faqs).
Only identifiers and source row locations are retained here.

`cprt-invalid-target-ac-999.json` is a synthetic negative-test input. `AC-999`
is not a row or identifier asserted to be in the NIST source or catalog.

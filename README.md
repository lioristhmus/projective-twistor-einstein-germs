# A Projective Twistor Correspondence for Local Analytic Einstein Germs

**Lior Isthmus** · [ORCID 0009-0004-7908-9876](https://orcid.org/0009-0004-7908-9876)

Publication package for the preprint, **v1.0**.

- [Read the paper (PDF)](release/paper-v1.0/manuscript.pdf)
- [Canonical Markdown](release/paper-v1.0/manuscript.md)
- [Standalone TeX](release/paper-v1.0/manuscript.tex)
- [Finite-readout proof note](release/paper-v1.0/PROOF.md)
- [Notation index](release/paper-v1.0/notation.md)
- [Build and verification instructions](BUILDING.md)

The paper constructs a convergent projective twistor correspondence for marked
four-dimensional local analytic Einstein germs, for prescribed numerical
cosmological constant, including zero and all algebraic Weyl types. It treats
independently admitted ordinary and operator presentations and compares the
source, point, optical and infinity data. A Schwarzschild application gives
calibrated local horizon-crossing comparisons and finite-readout optical
approximation bounds for the specified compact family of nonradial rays.

The scope and hypotheses are stated in the manuscript. The Schwarzschild
approximation uses exact benchmark cuts, coordinate comparisons and Sachs
reference frames.

## Version and provenance

The fixed package is [`release/paper-v1.0`](release/paper-v1.0). Its mathematical
content and AI-use disclosure are unchanged from the internally audited
**v0.2.12-review**. The YAML version is `1.0`, and the manuscript date remains
5 November 2026. Limited prose edits remove repeated emphasis and consolidate
duplicated explanations; their exact reversible ledger is
[`EDITORIAL-CHANGES.json`](release/paper-v1.0/EDITORIAL-CHANGES.json).

[BASELINE.json](release/paper-v1.0/BASELINE.json) records the source hashes.
[RELEASE-NOTES.md](release/paper-v1.0/RELEASE-NOTES.md) describes the transition.
The root [SHA256SUMS](SHA256SUMS) covers the publication files.

The manuscript contains the author's AI-use disclosure. This package includes
internal source/export checks. Lean formalization is a separate future project.

## Build and verify

```sh
python3 scripts/verify_release.py
python3 scripts/build_paper.py
```

The full build regenerates TeX from canonical Markdown using the bundled standard
export profile and the retained export-only layout adjustments. Its outputs go
under `build/`, leaving the fixed release untouched. A shorter build from the
standalone TeX is available:

```sh
python3 scripts/build_paper.py --from-tex
```

## Citation and license

Citation metadata is in [CITATION.cff](CITATION.cff). Archive identifiers and
public-release dates are added when the corresponding deposits are published;
none is inferred from local preparation.

The manuscript, generated TeX/PDF and scholarly documentation use **CC BY 4.0**.
Build and validation code and bundled rendering support use **Apache-2.0**.
See [LICENSE](LICENSE) for the exact file scope.

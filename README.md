# A Projective Twistor Correspondence for Local Analytic Einstein Germs

**Lior Isthmus** · [ORCID 0009-0004-7908-9876](https://orcid.org/0009-0004-7908-9876)

**Paper v1.1**, 13 November 2026.
This revision adds the computational supplement and its manuscript references,
including the SageMath/SymPy verification sentence in the AI-use disclosure.
The mathematical statements, assumptions, proofs and formulas are unchanged from v1.0.

- [Paper PDF](release/paper-v1.1/manuscript.pdf)
- [Canonical Markdown](release/paper-v1.1/manuscript.md) · [Standalone TeX](release/paper-v1.1/manuscript.tex)
- [Computational supplement 0.2.0-r3](computations/README.md)
- [Check-to-formula index](computations/CHECKS.md) · [Independent evidence](computations/INDEPENDENT-EVIDENCE.md)
- [Revision notes](release/paper-v1.1/RELEASE-NOTES.md) · [Build instructions](BUILDING.md)
- [Frozen v1.0](release/paper-v1.0/manuscript.pdf)
- [Finite-readout proof note](release/paper-v1.0/PROOF.md) · [Notation](release/paper-v1.0/notation.md)

The paper constructs a convergent projective twistor correspondence for marked
four-dimensional local analytic Einstein germs, for each prescribed numerical
cosmological constant, including zero and every algebraic Weyl type. It treats
independently admitted ordinary and operator presentations and compares the
source, point, optical and infinity data. The Schwarzschild application uses
exact benchmark cuts, coordinate comparisons and Sachs reference frames.
The scope and hypotheses are stated in the manuscript.

## Computations

The supplement contains SageMath code, fixed inputs, recorded environments,
results and formula locators. Its exact symbolic identities, finite exact
examples and numerical observations have separate evidence roles. The seven
independent geometric witnesses have a separate implementation and recorded
negative controls. The supplement does not certify general estimates or
analytic convergence, and is not a formal verification of the paper.

The supplement is byte-identical to the fixed **0.2.0-r3** package. Its locators
remain tied to the frozen v1.0 source on which the checks were performed. The
v1.1 change ledger reconstructs v1.0 exactly by reversing the supplement and
disclosure edits and restoring the date/version. Equation and theorem numbering are preserved.

## Versions and publication state

- v1.0: [Hexagon](https://hexagonmath.org/2611.00123v1),
  [Zenodo version DOI](https://doi.org/10.5281/zenodo.23975732),
  [GitHub release](https://github.com/lioristhmus/projective-twistor-einstein-germs/releases/tag/paper-v1.0).
- v1.1: [Hexagon 2611.00123v2](https://hexagonmath.org/2611.00123v2),
  [Zenodo version DOI](https://doi.org/10.5281/zenodo.24197319),
  [GitHub release](https://github.com/lioristhmus/projective-twistor-einstein-germs/releases/tag/paper-v1.1),
  with PDF, source archives, computational supplement and SHA-256 checksums.
  Hexagon's v2 is paper v1.1; the version labels belong to different services.
- [All-version DOI](https://doi.org/10.5281/zenodo.23975731).
- The work is listed on the author's [ORCID record](https://orcid.org/0009-0004-7908-9876)
  with the current Hexagon URL. Zenodo also links to that Hexagon version.

Publication links were checked on 14 November 2026. See
[PUBLICATION.md](PUBLICATION.md) and [PUBLICATION-STATUS.json](PUBLICATION-STATUS.json).
The default branch carries current publication metadata; frozen tags and
release assets retain their original bytes, including their checksum files.

## Build and verify

```sh
python3 scripts/verify_release.py
python3 scripts/verify_v1_1.py
python3 scripts/build_paper.py
```

The current standard export uses pdfLaTeX. It writes to `build/` and retains
intermediates in `tmp/`, leaving fixed release artifacts untouched. The original
v1.0 remains available with its XeLaTeX PDF and source. For its original full
build pipeline, use the `paper-v1.0` Git tag.

## Citation and licenses

[CITATION.cff](CITATION.cff) identifies paper v1.1, its version-specific Zenodo
DOI and its Hexagon record. [LICENSE](LICENSE) defines the CC BY 4.0 scholarly
material and Apache-2.0 code scopes. No mathematical job or model call is run by
the release verifiers. Lean formalization is maintained separately.

# Building the paper

The canonical source is `release/paper-v1.0/manuscript.md`. Keep its neighboring
`references.bib` available. The generated `manuscript.tex` is standalone and has
its rendered bibliography embedded.

## Requirements

- Python 3.10 or later (standard library only for build and release verification)
- Pandoc and pandoc-crossref on PATH for a full Markdown build
- XeLaTeX and standard TeX Live packages, including amsart, unicode-math,
  mathtools, booktabs, longtable, microtype and needspace
- Poppler (`pdfinfo`, `pdftotext`, `pdftoppm`) for display checks

Exact tool versions used for preparation are in
`release/paper-v1.0/BUILD-REPORT.json`. No package download or model call is
performed by the build scripts.

## Full regeneration

```sh
python3 scripts/build_paper.py
```

The bundled exporter is the maintained standard Pandoc/XeLaTeX profile as used
for the preceding fixed manuscript. `scripts/prepare_layout.py` applies the
retained manuscript-specific export adjustments: title/contact-footnote
placement, table widths, paragraph/page breaks and equation line wrapping.
It checks ordered labels and mathematical fingerprints during those adjustments.
The original Markdown is not edited. Other exporter profiles are outside this
package's supported build path.

Generated files and logs are written to `build/paper-v1.0/`; intermediate exporter
files are retained under `tmp/`. Successful typesetting verifies the export, not
the mathematical proofs. Byte-identical PDFs across different TeX installations
are not promised.

## Standalone TeX build

```sh
python3 scripts/build_paper.py --from-tex
```

This runs three XeLaTeX passes without shell escape and writes into the same
ignored build directory. It does not require Pandoc or external input files.
For a preprint server, `dist/*-hexagon.zip` contains the standalone manuscript
TeX and its bibliography; the source ZIP is prepared by the maintainer separately.

## Frozen artifact verification

```sh
python3 scripts/verify_release.py
shasum -a 256 -c SHA256SUMS
```

The verifier checks the publication allowlist and hashes, reverses the exact
editorial ledger to the v0.2.12 source, and checks the retained AI paragraph,
source anchors, displayed formulas and dependency data. It does not run
mathematical computation or claim Lean verification.

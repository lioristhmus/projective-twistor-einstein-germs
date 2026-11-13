# Building and verifying v1.1

Canonical source: `release/paper-v1.1/manuscript.md`, with the neighboring
`references.bib`. The generated TeX embeds its bibliography.

Requirements: Python 3.10+, Pandoc, pandoc-crossref, pdfLaTeX and standard
TeX Live packages. Poppler supports PDF inspection. The bundled standard exporter
and generated-TeX repair helper are copies of the maintained research pipeline.
Tool versions and export warnings are in the release's BUILD-REPORT.json.

```sh
python3 scripts/build_paper.py
python3 scripts/build_paper.py --from-tex
```

The first command regenerates from Markdown; the second compiles the fixed
standalone TeX. Both write to `build/paper-v1.1/`. Intermediate files go to
`tmp/`. No download, mathematical computation or model call is performed.
PDF bytes and pagination can vary across TeX installations.

For the old frozen TeX, use `python3 scripts/build_paper.py --version 1.0 --from-tex`.
This uses XeLaTeX. The original full Markdown/layout workflow is preserved at
the immutable `paper-v1.0` tag.

```sh
python3 scripts/verify_release.py
python3 scripts/verify_v1_1.py
python3 computations/code/verify_package.py
shasum -a 256 -c SHA256SUMS
```

Verification checks file hashes, source preservation, ordered labels, recorded
executions and the exact supplement package. It does not execute mathematical
checks or establish the mathematical correctness of all statements. Re-running
the mathematical checks is a separate, resource-limited Docker operation; see
`computations/README.md`.

The source archive contains the paper, supplement and build support with their
respective licenses. The Hexagon archive contains only the standalone paper TeX
and bibliography. No software files with a different license are placed in that
paper submission archive.

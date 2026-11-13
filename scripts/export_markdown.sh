#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./scripts/export_markdown.sh [options] INPUT.md

Options:
  --profile NAME       standard | ccg-jp | arxiv | arxiv-ams | arxiv-strict | ams
                       (default: standard)
  --engine NAME        pdflatex | xelatex for standard/arxiv-ams (default: pdflatex).
  --toc                Ask Pandoc to generate a table of contents.
  --citeproc           Enable citation processing (default).
  --no-citeproc        Disable citation processing.
  --no-tex-adjustments Disable generated-TeX syntax/layout repairs.
  --output-dir DIR     Output directory (default: directory containing INPUT.md).
  --output-stem NAME   Output filename stem.
  --keep-work          Keep LaTeX intermediate files after success.
  --list-profiles      Show available profiles and exit.
  -h, --help           Show this help.

Default output names:
  standard: INPUT.tex, INPUT.pdf
  ccg-jp:   INPUT.ccg-jp.tex, INPUT.ccg-jp.pdf
  arxiv:    INPUT.arxiv.tex, INPUT.arxiv.pdf
  arxiv-ams: INPUT.arxiv-ams.tex, INPUT.arxiv-ams.pdf
  ams:      INPUT.ams.tex, INPUT.ams.pdf

arxiv-strict requires a TeX Live 2025 XeLaTeX wrapper at
scripts/bin/arxiv-xelatex, or in ARXIV_XELATEX.

standard/arxiv-ams repair generated TeX and wrap measured overfull math.
Unresolved warnings retain the work directory for log and PDF inspection.
EOF
}

list_profiles() {
  cat <<'EOF'
standard      AMS mathematical preprint with running heads (pdfLaTeX; --engine xelatex optional).
ccg-jp        Previous CCG Japanese template (LuaLaTeX).
arxiv         Portable English article profile (XeLaTeX).
arxiv-ams     Same as standard, with a profile suffix (pdfLaTeX; --engine xelatex optional).
arxiv-strict  arxiv profile with a required TeX Live 2025 XeLaTeX wrapper.
ams           Existing English amsart profile (LuaLaTeX).
EOF
}

PROFILE="standard"
ENGINE_OVERRIDE=""
TOC=false
CITEPROC=true
OUTPUT_DIR=""
OUTPUT_STEM=""
KEEP_WORK=false
TEX_ADJUSTMENTS=true
INPUT=""

while [ $# -gt 0 ]; do
  case "$1" in
    --profile)
      [ $# -ge 2 ] || { echo "Missing value for --profile" >&2; exit 2; }
      PROFILE="$2"
      shift 2
      ;;
    --toc)
      TOC=true
      shift
      ;;
    --engine)
      [ $# -ge 2 ] || { echo "Missing value for --engine" >&2; exit 2; }
      case "$2" in
        pdflatex|xelatex) ENGINE_OVERRIDE="$2" ;;
        *) echo "--engine must be pdflatex or xelatex: $2" >&2; exit 2 ;;
      esac
      shift 2
      ;;
    --citeproc)
      CITEPROC=true
      shift
      ;;
    --no-citeproc)
      CITEPROC=false
      shift
      ;;
    --no-tex-adjustments)
      TEX_ADJUSTMENTS=false
      shift
      ;;
    --output-dir)
      [ $# -ge 2 ] || { echo "Missing value for --output-dir" >&2; exit 2; }
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --output-stem)
      [ $# -ge 2 ] || { echo "Missing value for --output-stem" >&2; exit 2; }
      OUTPUT_STEM="$2"
      shift 2
      ;;
    --keep-work)
      KEEP_WORK=true
      shift
      ;;
    --list-profiles)
      list_profiles
      exit 0
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [ -n "$INPUT" ]; then
        echo "Only one input Markdown file may be specified." >&2
        exit 2
      fi
      INPUT="$1"
      shift
      ;;
  esac
done

[ -n "$INPUT" ] || { usage >&2; exit 2; }
[ -f "$INPUT" ] || { echo "Input Markdown not found: $INPUT" >&2; exit 3; }

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STYLE_DIR="$ROOT/common/styles"
INPUT_DIR="$(cd "$(dirname "$INPUT")" && pwd)"
INPUT="$INPUT_DIR/$(basename "$INPUT")"
INPUT_BASE="$(basename "${INPUT%.md}")"

if [ -n "$ENGINE_OVERRIDE" ] && [ "$PROFILE" != "standard" ] && [ "$PROFILE" != "arxiv-ams" ]; then
  echo "--engine applies only to standard/arxiv-ams; $PROFILE keeps its own engine." >&2
  exit 2
fi

case "$PROFILE" in
  standard)
    DEFAULT_STEM="$INPUT_BASE"
    ENGINE="$(command -v "${ENGINE_OVERRIDE:-pdflatex}" || true)"
    READER="markdown-fancy_lists+raw_tex+tex_math_dollars+raw_html+footnotes+table_captions"
    ;;
  ccg-jp)
    DEFAULT_STEM="$INPUT_BASE.ccg-jp"
    ENGINE="$ROOT/scripts/bin/lualatex"
    READER="markdown+raw_tex+tex_math_dollars+footnotes+table_captions"
    ;;
  arxiv)
    DEFAULT_STEM="$INPUT_BASE.arxiv"
    ENGINE="$(command -v xelatex || true)"
    READER="markdown-fancy_lists+raw_tex+tex_math_dollars+raw_html+footnotes+table_captions"
    ;;
  arxiv-ams)
    DEFAULT_STEM="$INPUT_BASE.arxiv-ams"
    ENGINE="$(command -v "${ENGINE_OVERRIDE:-pdflatex}" || true)"
    READER="markdown-fancy_lists+raw_tex+tex_math_dollars+raw_html+footnotes+table_captions"
    ;;
  arxiv-strict)
    DEFAULT_STEM="$INPUT_BASE.arxiv-strict"
    ENGINE="${ARXIV_XELATEX:-$ROOT/scripts/bin/arxiv-xelatex}"
    READER="markdown-fancy_lists+raw_tex+tex_math_dollars+raw_html+footnotes+table_captions"
    ;;
  ams)
    DEFAULT_STEM="$INPUT_BASE.ams"
    ENGINE="$ROOT/scripts/bin/lualatex"
    READER="markdown+raw_tex+tex_math_dollars+raw_html+footnotes+table_captions"
    ;;
  *)
    echo "Unknown profile: $PROFILE" >&2
    list_profiles >&2
    exit 2
    ;;
esac

if [ ! -x "$ENGINE" ]; then
  if [ "$PROFILE" = "arxiv-strict" ]; then
    cat >&2 <<EOF
arxiv-strict requires a TeX Live 2025 XeLaTeX wrapper.
Set ARXIV_XELATEX or provide:
  $ROOT/scripts/bin/arxiv-xelatex

The official arXiv compiler source is:
  https://github.com/arXiv/submission-tools
EOF
  else
    echo "TeX engine is not executable: $ENGINE" >&2
  fi
  exit 4
fi

for command_name in pandoc pandoc-crossref; do
  command -v "$command_name" >/dev/null 2>&1 || {
    echo "Required command not found: $command_name" >&2
    exit 4
  }
done

if [ "$PROFILE" = "standard" ] || [ "$PROFILE" = "arxiv-ams" ]; then
  echo "[$PROFILE] TeX engine: $("$ENGINE" --version 2>/dev/null | sed -n '1p')"
  echo "Note: submission servers may use different TeX Live/package versions; pagination can differ." >&2
elif [ "$PROFILE" = "arxiv" ] || [ "$PROFILE" = "arxiv-strict" ]; then
  ENGINE_VERSION="$("$ENGINE" --version 2>/dev/null | sed -n '1p')"
  if [ "$PROFILE" = "arxiv-strict" ] && [[ "$ENGINE_VERSION" != *"TeX Live 2025"* ]]; then
    echo "arxiv-strict requires TeX Live 2025; found: $ENGINE_VERSION" >&2
    exit 4
  fi
  if [ "$PROFILE" = "arxiv" ] \
      && [[ "$ENGINE_VERSION" != *"TeX Live 2025"* ]]; then
    echo "Note: local arxiv profile is using $ENGINE_VERSION" >&2
    echo "      arXiv currently defaults to TeX Live 2025; final validation occurs on arXiv." >&2
  fi
fi

if [ -z "$OUTPUT_DIR" ]; then
  OUTPUT_DIR="$INPUT_DIR"
else
  mkdir -p "$OUTPUT_DIR"
  OUTPUT_DIR="$(cd "$OUTPUT_DIR" && pwd)"
fi

if [ -z "$OUTPUT_STEM" ]; then
  OUTPUT_STEM="$DEFAULT_STEM"
fi

if [[ "$OUTPUT_STEM" == */* ]] || [ "$OUTPUT_STEM" = "." ] || [ "$OUTPUT_STEM" = ".." ]; then
  echo "--output-stem must be a filename stem, not a path: $OUTPUT_STEM" >&2
  exit 2
fi

mkdir -p "$ROOT/tmp" "$OUTPUT_DIR"
WORK_DIR="$(mktemp -d "$ROOT/tmp/markdown-export.XXXXXX")"
SUCCESS=false

cleanup() {
  if $SUCCESS && ! $KEEP_WORK; then
    rm -rf "$WORK_DIR"
  else
    echo "Work directory retained: $WORK_DIR" >&2
  fi
}
trap cleanup EXIT

TEX_WORK="$WORK_DIR/$OUTPUT_STEM.tex"
PDF_WORK="$WORK_DIR/$OUTPUT_STEM.pdf"
LOG_FIRST="$WORK_DIR/latex-pass1.log"
LOG_SECOND="$WORK_DIR/latex-pass2.log"
USE_DISPLAY_JOIN=false

PANDOC_ARGS=(
  "$INPUT"
  --standalone
  --to latex
  --from "$READER"
  --resource-path "$INPUT_DIR:$ROOT"
  --filter pandoc-crossref
  --lua-filter "$STYLE_DIR/pandoc-manual-reference-anchors.lua"
)

case "$PROFILE" in
  ccg-jp)
    PANDOC_ARGS+=(
      --template "$STYLE_DIR/ccg-jp.latex"
      --metadata-file "$STYLE_DIR/pandoc-jp.yaml"
      --include-in-header "$STYLE_DIR/macros.tex"
    )
    ;;
  arxiv|arxiv-strict)
    PANDOC_ARGS+=(
      --metadata-file "$STYLE_DIR/pandoc-arxiv-en.yaml"
      --include-in-header "$STYLE_DIR/arxiv-preamble.tex"
      --include-in-header "$STYLE_DIR/macros.tex"
    )
    ;;
  standard|arxiv-ams)
    USE_DISPLAY_JOIN=true
    PANDOC_ARGS+=(
      --metadata-file "$STYLE_DIR/pandoc-arxiv-ams-en.yaml"
      --lua-filter "$STYLE_DIR/pandoc-promote-topmatter.lua"
      --include-in-header "$STYLE_DIR/arxiv-preamble.tex"
      --include-in-header "$STYLE_DIR/ams-statement-headings.tex"
      --include-in-header "$STYLE_DIR/ams-abstract-heading.tex"
      --include-in-header "$STYLE_DIR/macros.tex"
    )
    ;;
  ams)
    PANDOC_ARGS+=(
      --metadata-file "$STYLE_DIR/pandoc-ams-en.yaml"
      --include-in-header "$STYLE_DIR/ams-preamble.tex"
      --include-in-header "$STYLE_DIR/macros.tex"
    )
    ;;
esac

if $CITEPROC; then
  PANDOC_ARGS+=(--citeproc --lua-filter "$STYLE_DIR/pandoc-bibliography-heading.lua")
fi

if $TOC; then
  PANDOC_ARGS+=(--toc)
fi

if [ -f "$ROOT/common/bib/references.bib" ]; then
  PANDOC_ARGS+=(--bibliography "$ROOT/common/bib/references.bib")
fi

echo "[$PROFILE] Pandoc -> $OUTPUT_STEM.tex"
if $USE_DISPLAY_JOIN; then
  PRE_CROSSREF_JSON="$WORK_DIR/pre-crossref.json"
  CROSSREF_JSON="$WORK_DIR/crossref.json"

  # pandoc-crossref must see standalone equation blocks before the display
  # paragraph filter joins them back to their surrounding prose.
  PANDOC_AST_ARGS=(
    "$INPUT"
    --from "$READER"
    --to json
    --resource-path "$INPUT_DIR:$ROOT"
    --metadata-file "$STYLE_DIR/pandoc-arxiv-ams-en.yaml"
    --lua-filter "$STYLE_DIR/pandoc-promote-topmatter.lua"
    --lua-filter "$STYLE_DIR/pandoc-unnumber-abstract-equations.lua"
  )
  if [ "${ENGINE_OVERRIDE:-pdflatex}" = "pdflatex" ]; then
    PANDOC_AST_ARGS+=(--lua-filter "$STYLE_DIR/pandoc-pdftex-check.lua")
  fi
  if [ -f "$ROOT/common/bib/references.bib" ]; then
    PANDOC_AST_ARGS+=(--bibliography "$ROOT/common/bib/references.bib")
  fi

  pandoc "${PANDOC_AST_ARGS[@]}" --output "$PRE_CROSSREF_JSON"
  pandoc-crossref --pipe latex < "$PRE_CROSSREF_JSON" > "$CROSSREF_JSON"

  PANDOC_WRITER_ARGS=(
    "$CROSSREF_JSON"
    --standalone
    --from json
    --to latex
    --resource-path "$INPUT_DIR:$ROOT"
    --lua-filter "$STYLE_DIR/pandoc-statement-headings.lua"
    --lua-filter "$STYLE_DIR/pandoc-join-display-paragraphs.lua"
    --lua-filter "$STYLE_DIR/pandoc-manual-reference-anchors.lua"
    --include-in-header "$STYLE_DIR/arxiv-preamble.tex"
    --include-in-header "$STYLE_DIR/ams-statement-headings.tex"
    --include-in-header "$STYLE_DIR/ams-abstract-heading.tex"
    --include-in-header "$STYLE_DIR/macros.tex"
  )
  # crossref rewrites Cite nodes; render bibliography citations only afterwards.
  if $CITEPROC; then
    PANDOC_WRITER_ARGS+=(--citeproc --lua-filter "$STYLE_DIR/pandoc-bibliography-heading.lua")
  fi
  if $TOC; then
    PANDOC_WRITER_ARGS+=(--toc)
  fi
  pandoc "${PANDOC_WRITER_ARGS[@]}" --output "$TEX_WORK"
else
  pandoc "${PANDOC_ARGS[@]}" --output "$TEX_WORK"
fi

run_latex() {
  local log_file="$1"
  if ! (
    cd "$WORK_DIR"
    export TEXMFCACHE="./texmf-cache"
    export TEXMFVAR="./texmf-var"
    export TEXINPUTS="$INPUT_DIR:$ROOT:"
    "$ENGINE" \
      -halt-on-error \
      -file-line-error \
      -interaction=nonstopmode \
      -output-directory "$WORK_DIR" \
      "$(basename "$TEX_WORK")"
  ) >"$log_file" 2>&1; then
    echo "LaTeX failed. Last 40 log lines:" >&2
    tail -40 "$log_file" >&2
    return 1
  fi
  if $USE_DISPLAY_JOIN && [ "${ENGINE_OVERRIDE:-pdflatex}" = "pdflatex" ] \
      && grep -q 'Missing character:' "$log_file"; then
    echo "pdfLaTeX reported missing glyphs; outputs were not published. Inspect $log_file" >&2
    return 1
  fi
}

if $USE_DISPLAY_JOIN && $TEX_ADJUSTMENTS; then
  command -v python3 >/dev/null 2>&1 || { echo "Required command not found: python3" >&2; exit 4; }
  ADJUST_REPORT="$WORK_DIR/tex-adjustments.json"
  ADJUST_STATUS="$WORK_DIR/tex-adjustments.status"
  ADJUST_TOOL="$ROOT/scripts/prepare_paper_tex.py"
  python3 "$ADJUST_TOOL" --tex "$TEX_WORK" --report "$ADJUST_REPORT" --status-file "$ADJUST_STATUS"
  echo "[$PROFILE] LaTeX layout pass 1"
  run_latex "$LOG_FIRST"
  LAST_LOG="$LOG_FIRST"
  for ROUND in 1 2 3; do
    python3 "$ADJUST_TOOL" --tex "$TEX_WORK" --report "$ADJUST_REPORT" \
      --status-file "$ADJUST_STATUS" --latex-log "$LAST_LOG" --threshold 2
    [ "$(cat "$ADJUST_STATUS")" = "changed" ] || break
    LAST_LOG="$WORK_DIR/latex-layout-$ROUND.log"
    echo "[$PROFILE] LaTeX layout pass $((ROUND + 1))"
    run_latex "$LAST_LOG"
  done
  echo "[$PROFILE] LaTeX reference pass"
  run_latex "$LOG_SECOND"
  if grep -Eq 'Label\(s\) may have changed|Rerun to get cross-references right' "$LOG_SECOND"; then
    echo "[$PROFILE] LaTeX reference stabilization pass"
    run_latex "$LOG_SECOND"
  fi
  python3 "$ADJUST_TOOL" --tex "$TEX_WORK" --report "$ADJUST_REPORT" \
    --status-file "$ADJUST_STATUS" --latex-log "$LOG_SECOND" --check
  if [ "$(cat "$ADJUST_STATUS")" = "warnings" ]; then
    KEEP_WORK=true
    echo "Layout/reference/font warnings remain; inspect $LOG_SECOND and $ADJUST_REPORT" >&2
  fi
else
  echo "[$PROFILE] LaTeX pass 1/2"
  run_latex "$LOG_FIRST"
  echo "[$PROFILE] LaTeX pass 2/2"
  run_latex "$LOG_SECOND"
fi

[ -f "$PDF_WORK" ] || {
  echo "Expected PDF was not generated: $PDF_WORK" >&2
  exit 5
}

cp "$TEX_WORK" "$OUTPUT_DIR/$OUTPUT_STEM.tex"
cp "$PDF_WORK" "$OUTPUT_DIR/$OUTPUT_STEM.pdf"
SUCCESS=true

echo "Built:"
echo "  $OUTPUT_DIR/$OUTPUT_STEM.tex"
echo "  $OUTPUT_DIR/$OUTPUT_STEM.pdf"

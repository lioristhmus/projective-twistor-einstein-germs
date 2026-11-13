#!/usr/bin/env python3
"""Build a paper copy without overwriting either fixed release."""
import argparse
from pathlib import Path
import shutil
import sys
import subprocess
ROOT = Path(__file__).resolve().parents[1]
def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--version', choices=('1.0', '1.1'), default='1.1')
    p.add_argument('--from-tex', action='store_true')
    args = p.parse_args()
    paper = ROOT / ('release/paper-v' + args.version)
    out = ROOT / ('build/paper-v' + args.version)
    out.mkdir(parents=True, exist_ok=True)
    if args.from_tex or args.version == '1.0':
        shutil.copyfile(paper / 'manuscript.tex', out / 'manuscript.tex')
        engine = 'xelatex' if args.version == '1.0' else 'pdflatex'
        for i in range(3):
            result = subprocess.run([engine, '-no-shell-escape', '-halt-on-error',
                                     '-interaction=nonstopmode', 'manuscript.tex'],
                                    cwd=out, text=True, capture_output=True, timeout=180)
            (out / ('latex-' + str(i + 1) + '.log')).write_text(result.stdout + result.stderr)
            result.check_returncode()
    else:
        subprocess.run(['bash', str(ROOT / 'scripts/export_markdown.sh'),
                        '--profile', 'standard', '--keep-work', '--output-dir', str(out),
                        '--output-stem', 'manuscript', str(paper / 'manuscript.md')],
                       cwd=paper, check=True, timeout=900)
        subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/prepare_release_v1_1.py'),
                        str(out / 'manuscript.tex')], check=True, timeout=30)
        for i in range(3):
            result = subprocess.run(['pdflatex', '-no-shell-escape', '-halt-on-error',
                                     '-interaction=nonstopmode', 'manuscript.tex'],
                                    cwd=out, text=True, capture_output=True, timeout=180)
            (out / ('latex-final-' + str(i + 1) + '.log')).write_text(result.stdout + result.stderr)
            result.check_returncode()
    print(out / 'manuscript.pdf')
if __name__ == '__main__':
    main()

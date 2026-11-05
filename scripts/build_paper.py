#!/usr/bin/env python3
"""Regenerate the release paper without overwriting the frozen artifacts."""
from pathlib import Path
import argparse, os, re, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT/'release/paper-v1.0'

def run(args, **kwargs):
    return subprocess.run(args, check=True, text=True, **kwargs)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--from-tex',action='store_true',help='Compile the frozen standalone TeX only')
    args=parser.parse_args()
    out=ROOT/'build/paper-v1.0';out.mkdir(parents=True,exist_ok=True)
    if args.from_tex:
        shutil.copyfile(PAPER/'manuscript.tex',out/'manuscript.tex')
        for step in (1,2,3):
            result=run(['xelatex','-no-shell-escape','-halt-on-error','-interaction=nonstopmode',
                        '-file-line-error','manuscript.tex'],cwd=out,capture_output=True,timeout=120)
            (out/f'latex-tex-{step}.log').write_text(result.stdout+'\n'+result.stderr)
    else:
        log=out/'export.log'
        with log.open('w') as stream:
            result=subprocess.run(['bash',str(ROOT/'scripts/export_markdown.sh'),'--profile','standard',
                                    '--output-dir',str(out),'--keep-work',str(PAPER/'manuscript.md')],
                                   cwd=PAPER,stdout=stream,stderr=subprocess.STDOUT,text=True,timeout=600)
        text=log.read_text()
        if result.returncode:
            print(text[-5000:],file=sys.stderr);raise SystemExit(result.returncode)
        matches=re.findall(r'Work directory retained: (.+)',text)
        if not matches: raise RuntimeError('Exporter did not report its retained work directory')
        work=Path(matches[-1]).resolve()
        run([sys.executable,str(ROOT/'scripts/prepare_layout.py'),str(work)],cwd=ROOT,timeout=300)
        for name in ['manuscript.tex','manuscript.pdf','MANUAL-TEX-DIFF.patch','MANUAL-TEX-ADJUSTMENTS.json']:
            shutil.copyfile(work/name,out/name)
        for name in ['manuscript.aux','manuscript.toc','latex-final-1.log','latex-final-2.log']:
            shutil.copyfile(work/name,out/name)
        (out/'WORK-DIRECTORY.txt').write_text(str(work)+'\n')
    print(out/'manuscript.pdf')

if __name__=='__main__': main()

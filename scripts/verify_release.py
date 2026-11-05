#!/usr/bin/env python3
"""Check the local publication package using only the Python standard library."""
from pathlib import Path
import hashlib, json, re, sys

ROOT=Path(__file__).resolve().parents[1]
PAPER=ROOT/'release/paper-v1.0'
IGNORED={'.git','build','tmp','dist','__pycache__'}

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(65536),b''):h.update(b)
    return h.hexdigest()

def anchors(text):
    return [a or b for a,b in re.findall(r'<div id="([^"]+)">|\{#([^\s}]+)\}',text)]

def bibliography_core(text):
    for key in ('AdamoEtAl2026v2','Adamo2018SpinorConventions'):
        pattern=r'(?ms)(^@\w+\{'+re.escape(key)+r',\n(?:(?!^\}).)*?^  note = )\{[^\n]*\}'
        text,count=re.subn(pattern,lambda m:m.group(1)+'{<public-note>}',text)
        assert count==1,key
    return text

def main():
    manifest=json.loads((ROOT/'PUBLICATION-MANIFEST.json').read_text())
    names=set()
    for f in manifest['files']:
        rel=Path(f['path'])
        assert not rel.is_absolute() and '..' not in rel.parts
        p=ROOT/rel;assert p.is_file() and not p.is_symlink(),str(rel)
        assert p.stat().st_size==f['bytes'] and digest(p)==f['sha256'],str(rel)
        assert f['path'] not in names;names.add(f['path'])
    actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()
            and not set(p.relative_to(ROOT).parts)&IGNORED}
    assert actual==names|{'PUBLICATION-MANIFEST.json','SHA256SUMS'},sorted(actual^names)
    lines=(ROOT/'SHA256SUMS').read_text().splitlines()
    hashed={}
    for line in lines:
        h,n=line.split('  ',1);assert digest(ROOT/n)==h,n;hashed[n]=h
    assert set(hashed)==names|{'PUBLICATION-MANIFEST.json'}
    baseline=json.loads((PAPER/'BASELINE.json').read_text())
    text=(PAPER/'manuscript.md').read_text()
    assert text.count('version: "1.0"')==1
    editorial=json.loads((PAPER/'EDITORIAL-CHANGES.json').read_text())
    assert digest(PAPER/'manuscript.md')==editorial['result_sha256']
    restored=text
    for event in reversed(editorial['events']):
        assert restored.count(event['after'])==1,event['id']
        restored=restored.replace(event['after'],event['before'],1)
    assert hashlib.sha256(restored.encode()).hexdigest()==editorial['base_sha256']
    restored=restored.replace('version: "1.0"','version: "0.2.12-review"',1)
    assert hashlib.sha256(restored.encode()).hexdigest()==baseline['baseline_files']['manuscript.md']
    for name in ['PROOF.md','notation.md']:
        assert digest(PAPER/name)==baseline['baseline_files'][name],name
    for name in ['PROOF-DAG.json','PROOF-NOTE-DAG.json']:
        s=(PAPER/name).read_text();assert s.count('"version": "1.0"')==1
        old=s.replace('"version": "1.0"','"version": "0.2.12-review"',1)
        assert hashlib.sha256(old.encode()).hexdigest()==baseline['baseline_files'][name],name
    assert json.loads((PAPER/'PROOF-NOTE-DAG.json').read_text())['baseline']=='0.2.7-review'
    expected_ai='AI systems were used extensively throughout this research and the preparation of this manuscript. The models used were GPT-6 Pro, gpt-6.1-sol (xhigh), and Claude Opus 5.5 (xhigh).'
    assert text.count(expected_ai)==1
    assert text.count('[^author-email]: Email: <lioristhmus@proton.me>')==1
    labels=anchors(text);assert len(labels)==len(set(labels))==752
    refs={a or b for a,b in re.findall(r'\]\(#([^)]+)\)|\[@(-?eq:[^\]\s]+)\]',text)}
    assert not refs-set(labels)
    displays=re.findall(r'^\$\$\s*\n(.*?)^\$\$(?:[ \t]+\{#([^}]+)\})?',text,re.M|re.S)
    assert len(displays)==578
    check=json.loads((PAPER/'SOURCE-CHECK.json').read_text())
    bibliography=(PAPER/'references.bib').read_text()
    core=bibliography_core(bibliography)
    assert hashlib.sha256(core.encode()).hexdigest()==check['bibliography_non_note_sha256']
    for key,note in check['bibliography_public_notes'].items():
        pattern=r'(?ms)^@\w+\{'+re.escape(key)+r',\n(?:(?!^\}).)*?^  note = \{([^\n]*)\}'
        assert re.findall(pattern,bibliography)==[note],key
    for key,h in check['main_theorem_blocks_sha256'].items():
        a=text.index('<div id="'+key+'"></div>');b=text.find('<div id="',a+10)
        body=text[a:b if b>=0 else len(text)]
        assert hashlib.sha256(body.encode()).hexdigest()==h,key
    tex=(PAPER/'manuscript.tex').read_text()
    for name,h in check['file_sha256'].items():
        assert digest(PAPER/name)==h,name
    texlabels=re.findall(r'\\label\{([^}]+)\}',tex)
    assert len(texlabels)==len(set(texlabels))==875
    assert r'\author[Lior Isthmus]{Lior Isthmus\textsuperscript{1}}' in tex
    assert 'mailto:lioristhmus@proton.me' in tex
    for n in names:
        if Path(n).suffix in {'.md','.tex','.bib','.json','.cff','.py','.sh','.lua','.yaml'}:
            assert ('/'+'Users'+'/') not in (ROOT/n).read_text(),n
    print(json.dumps({'status':'PASS','publication_files':len(actual),'version':'1.0',
                      'canonical_change':'YAML version and reversible editorial ledger','displayed_formulas':len(displays),
                      'source_anchors':len(labels),'TeX_labels':len(texlabels),
                      'AI_disclosure':'unchanged','main_theorems':'unchanged',
                      'bibliography':'two public-facing note edits only'},indent=2))

if __name__=='__main__':
    try:main()
    except (AssertionError,ValueError,KeyError,OSError) as e:
        print('Verification failed: '+str(e),file=sys.stderr);raise SystemExit(1)

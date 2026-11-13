#!/usr/bin/env python3
"""File and source-preservation QA only; no mathematical programs are executed."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'release/paper-v1.1'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    baseline = json.loads((PAPER / 'BASELINE.json').read_text())
    for name, expected in baseline['frozen_release_files'].items():
        assert digest(ROOT / name) == expected, name
    changes = json.loads((PAPER / 'CHANGES.json').read_text())
    old = (ROOT / 'release/paper-v1.0/manuscript.md').read_text()
    new = (PAPER / 'manuscript.md').read_text()
    restored = new
    for change in reversed(changes['changes']):
        assert restored.count(change['after']) == 1
        restored = restored.replace(change['after'], change['before'], 1)
    assert restored == old
    assert hashlib.sha256(old.encode()).hexdigest() == changes['baseline_markdown_sha256']
    old_bib = (ROOT / 'release/paper-v1.0/references.bib').read_text()
    assert (PAPER / 'references.bib').read_text() == old_bib + changes['added_bibliography_entry']
    assert new.count('[@Isthmus2026LocalComputations]') == 2
    labels = lambda s: re.findall(r'\\label\{([^}]+)\}', s)
    old_tex = (ROOT / 'release/paper-v1.0/manuscript.tex').read_text()
    new_tex = (PAPER / 'manuscript.tex').read_text()
    assert labels(old_tex) == labels(new_tex), 'Ordered TeX labels changed'
    assert 'Isthmus2026LocalComputations' in new_tex
    assert 'mailto:lioristhmus@proton.me' in new_tex
    result = subprocess.run([sys.executable, '-B', str(ROOT / 'computations/code/verify_package.py')],
                            text=True, capture_output=True, check=True, timeout=30)
    comp_qa = json.loads(result.stdout)
    assert comp_qa['status'] == 'PASS'
    source_check = json.loads((PAPER / 'SOURCE-CHECK.json').read_text())
    for name, expected in source_check['file_sha256'].items():
        assert digest(PAPER / name) == expected, name
    print(json.dumps({'status': 'PASS', 'version': '1.1',
                      'baseline_release_files': len(baseline['frozen_release_files']),
                      'manuscript_changes': 'date/version, computational-supplement paragraph, and aligned AI-use disclosure',
                      'original_manuscript_reconstructed_exactly': True,
                      'original_bibliography_entries_unchanged': True,
                      'ordered_TeX_labels_unchanged': len(labels(new_tex)),
                      'computational_supplement_QA': comp_qa['status'],
                      'mathematical_jobs_executed': 0,
                      'publication_performed': False}, indent=2))

if __name__ == '__main__':
    main()

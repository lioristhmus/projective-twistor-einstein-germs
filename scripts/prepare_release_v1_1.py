#!/usr/bin/env python3
"""Retain publication anchors and contact placement; make layout-only repairs."""
from pathlib import Path
import argparse,json,re
import prepare_paper_tex as layout

def fingerprint(tex):
    result=[]
    for region in layout.math_regions(tex):
        body=tex[region.body_start:region.body_end].replace(r'\allowbreak','')
        a,b=layout.core_range(body);result.append(layout.fingerprint(body[a:b]))
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('tex',type=Path);args=p.parse_args()
    before=args.tex.read_text();text=before;events=[]
    def change(a,b,reason):
        nonlocal text
        assert text.count(a)==1,(reason,text.count(a))
        text=text.replace(a,b,1);events.append(reason)
    aliases={
      'coefficient-comparison-with-the-finite-generator':'literal-comparison-with-the-finite-generator',
      'd.3.-the-global-operator-and-its-transition-frames':'d.3.-the-global-operator-and-its-actual-transition-frames',
      'e.2.-whole-short-fibers-and-quotient-overlaps':'e.2.-whole-short-fibers-and-actual-quotient-overlaps'}
    for fresh,old in aliases.items():change(r'\label{'+fresh+'}',r'\label{'+old+'}','Preserve v1.0 heading anchor: '+old)
    change('\\section{A projective twistor correspondence for local analytic Einstein\ngerms}\\label{a-projective-twistor-correspondence-for-local-analytic-einstein-germs}\n\n\\textbf{Lior Isthmus}\\footnote{Email:\n  \\href{mailto:lioristhmus@proton.me}{\\nolinkurl{lioristhmus@proton.me}}}',r'\protect\phantomsection\label{a-projective-twistor-correspondence-for-local-analytic-einstein-germs}','Remove duplicate body title and author while retaining anchor')
    change(r'\author{Lior Isthmus}',r'\author[Lior Isthmus]{Lior Isthmus\textsuperscript{1}}','Retain title author contact marker and plain short author')
    change(r'\maketitle',r'\maketitle'+'\n'+r'\footnotetext[1]{Email: \href{mailto:lioristhmus@proton.me}{\nolinkurl{lioristhmus@proton.me}}}'+'\n'+r'\setcounter{footnote}{1}','Place contact footnote on first page')
    change(r'\subsection{Abstract}\label{abstract}',r'\section*{Abstract}\label{abstract}','Match separate centered Abstract and References headings')
    if r'\subsection*{AI-use disclosure}\label{ai-use-disclosure}' in text:
        change(r'\subsection*{AI-use disclosure}\label{ai-use-disclosure}',r'\begingroup'+'\n'+r'\renewcommand{\addcontentsline}[3]{}'+'\n'+r'\subsection*{AI-use disclosure}\label{ai-use-disclosure}','Honor the unlisted AI disclosure heading')
        change(r'\section*{References}',r'\endgroup'+'\n'+r'\section*{References}','Restore bibliography contents entry after unlisted disclosure')
    else:
        assert r'\textbf{AI-use disclosure.}' in text
    if '% Common LaTeX macros for CCG papers' in text:change('% Common LaTeX macros for CCG papers','% Common mathematics macros','Remove template-origin comment')
    change('Normalized lower stripping contractions',r'Normal\-ized lower stripping contractions','Allow discretionary table-text hyphen')
    change(r'\((s^{-r-2}U_r,s^{-2}\Lambda)\)',r'\((s^{-r-2}U_r,\allowbreak s^{-2}\Lambda)\)','Allow existing tuple-comma line break')
    for expr in [r"\nabla_v\omega^B=-it^{BB'}\pi_{B'}",r"\nabla_v\pi_{B'}=-it^{AA'}P^{\mathrm P}_{AA'BB'}\omega^B",r"\nabla_v(\omega,\pi)^T=-\Omega_v(\omega,\pi)^T"]:
        change(expr,expr.replace('=',r'=\allowbreak',1),'Permit transport equality line break')
    change(r"\(\nabla_v\omega^B=\allowbreak-it^{BB'}\pi_{B'}\)",r"\[\nabla_v\omega^B=-it^{BB'}\pi_{B'}\]",'Retain unnumbered first transport display')
    a=r''' \Phi_{\rm pr}(v,r,\theta,\phi)=
 \left(\tau=i(r-v),\ x=r\sin\theta\cos\phi,
       \ y=r\sin\theta\sin\phi,\ z=r\cos\theta\right).'''
    b=r''' \Phi_{\rm pr}(v,r,\theta,\phi)=
 \left(\begin{aligned}\tau=i(r-v),\ x=r\sin\theta\cos\phi,\\
       \ y=r\sin\theta\sin\phi,\ z=r\cos\theta\end{aligned}\right).'''
    change(a,b,'Reflow source-coordinate tuple')
    a=r''' \tau=\mathrm i(r-v),\quad
 x=r\sin\theta\cos\phi,\quad
 y=r\sin\theta\sin\phi,\quad
 z=r\cos\theta,
 \qquad\varrho=-r.'''
    b=r''' \begin{aligned}
 \tau&=\mathrm i(r-v),\quad x=r\sin\theta\cos\phi,\\
 y&=r\sin\theta\sin\phi,\quad z=r\cos\theta,\qquad\varrho=-r.
 \end{aligned}'''
    change(a,b,'Reflow native-coordinate tuple')
    assert fingerprint(before)==fingerprint(text),'Mathematical fingerprint changed'
    ids=lambda s:[aliases.get(x,x) for x in re.findall(r'\\label\{([^}]+)\}',s)]
    assert ids(before)==ids(text)
    args.tex.write_text(text)
    (args.tex.parent/'EXPORT-ADJUSTMENTS.json').write_text(json.dumps({'events':events,'math_regions':len(fingerprint(text)),'mathematical_fingerprints_preserved':True,'heading_anchor_aliases':aliases},indent=2)+'\n')
if __name__=='__main__':main()

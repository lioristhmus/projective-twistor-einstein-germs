from pathlib import Path
import subprocess,hashlib,json,shutil,importlib.util,sys,re,difflib,os

task=Path(__file__).resolve().parent
w=Path(sys.argv[1]).resolve()
root=task.parent;styles=root/'common/styles'
paper=root/'release/paper-v1.0'
t=w/'manuscript.tex';before=t.read_text();shutil.copyfile(t,w/'manuscript.pipeline.tex');shutil.copyfile(w/'manuscript.pdf',w/'manuscript.pipeline.pdf')
args=['pandoc',str(w/'crossref.json'),'--standalone','--from=json','--to=latex','--resource-path='+str(paper)+':'+str(root)]
for f in ['pandoc-statement-headings.lua','pandoc-join-display-paragraphs.lua','pandoc-manual-reference-anchors.lua']:args+=['--lua-filter',str(styles/f)]
for f in ['arxiv-preamble.tex','ams-statement-headings.tex','macros.tex']:args+=['--include-in-header',str(styles/f)]
args+=['--citeproc','--lua-filter',str(styles/'pandoc-bibliography-heading.lua'),'--output',str(w/'manuscript.raw-reference.tex')]
subprocess.run(args,check=True,capture_output=True,text=True,timeout=45)
raw=(w/'manuscript.raw-reference.tex').read_text();report=json.loads((w/'tex-adjustments.json').read_text())
assert hashlib.sha256(raw.encode()).hexdigest()==report['original_tex_sha256']
spec=importlib.util.spec_from_file_location('paper_tex',root/'scripts/prepare_paper_tex.py');m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
def fp(tex):
 out=[]
 for q in m.math_regions(tex):
  b=tex[q.body_start:q.body_end].replace(r'\allowbreak','');a,z=m.core_range(b);out.append(m.fingerprint(b[a:z]))
 return out
normalized,_=m.normalize(raw);assert fp(normalized)==fp(before)
text=before;events=[]
heading_aliases={
 'coefficient-comparison-with-the-finite-generator':'literal-comparison-with-the-finite-generator',
 'd.3.-the-global-operator-and-its-transition-frames':'d.3.-the-global-operator-and-its-actual-transition-frames',
 'e.2.-whole-short-fibers-and-quotient-overlaps':'e.2.-whole-short-fibers-and-actual-quotient-overlaps',
}
def label_ids(tex):
 return [heading_aliases.get(x,x) for x in re.findall(r'\\label\{([^}]+)\}',tex)]
def change(old,new,event):
 global text
 assert text.count(old)==1,(event,text.count(old))
 text=text.replace(old,new,1);events.append(event)
for fresh,retained in heading_aliases.items():
 change(r'\label{'+fresh+'}',r'\label{'+retained+'}',
        'Retain the existing heading anchor after its editorial wording change: '+retained+'.')
change('\\section{A projective twistor correspondence for local analytic Einstein\ngerms}\\label{a-projective-twistor-correspondence-for-local-analytic-einstein-germs}\n\n\\textbf{Lior Isthmus}\\footnote{Email:\n  \\href{mailto:lioristhmus@proton.me}{\\nolinkurl{lioristhmus@proton.me}}}',
       r'\protect\phantomsection\label{a-projective-twistor-correspondence-for-local-analytic-einstein-germs}',
       'Remove duplicate body title and author; retain maketitle and title labels.')

change(r'\author{Lior Isthmus}',r'\author[Lior Isthmus]{Lior Isthmus\textsuperscript{1}}','Display the canonical author-footnote number in the title author; retain the plain short author and PDF metadata.')
change(r'\maketitle',r'\maketitle'+'\n'+r'\footnotetext[1]{Email: \href{mailto:lioristhmus@proton.me}{\nolinkurl{lioristhmus@proton.me}}}'+'\n'+r'\setcounter{footnote}{1}','Place the corresponding canonical numbered contact footnote at the bottom of page1, after the existing unnumbered date note.')

change(r'\((s^{-r-2}U_r,s^{-2}\Lambda)\)',r'\((s^{-r-2}U_r,\allowbreak s^{-2}\Lambda)\)','Allow line break at the existing finite-scaling tuple comma.')
change('Normalized lower stripping contractions',r'Normal\-ized lower stripping contractions','Discretionary text hyphen in the existing operation table.')
old=r'\(2^{22}m_{r-1}(B)m_t(C)/(t+1)\le K_0m_{r-1}(B)m_t(C)/(t+1)\).'
new=r'\[2^{22}m_{r-1}(B)m_t(C)/(t+1)\le K_0m_{r-1}(B)m_t(C)/(t+1).\]'
change(old,new,'Promote the complete transfer bound to an unnumbered display and retain its sentence-ending period there.')
change(r'\subsection*{AI-use disclosure}\label{ai-use-disclosure}',r'\begingroup'+'\n'+r'\renewcommand{\addcontentsline}[3]{}'+'\n'+r'\subsection*{AI-use disclosure}\label{ai-use-disclosure}','Honor the unlisted AI heading in the AMS TOC.')
change('\\section*{References}\n\\addcontentsline{toc}{section}{References}', '\\par\n\\section*{References}\n\\endgroup\n\\addcontentsline{toc}{section}{References}', 'Suppress the native duplicate References TOC write and retain its single explicit entry.')
old='c^{(m)}_{n,a,j}(w^0)^{n-a}(w^1)^a\\zeta^{-j-1}\\].'
new='c^{(m)}_{n,a,j}(w^0)^{n-a}(w^1)^a\\zeta^{-j-1}.\\]'
change(old,new,'Transfer existing sentence-ending punctuation into the automatically promoted normal-series display.')
start=text.index('\\label{app:gg-notation}');end=text.index('\\label{sec:gg-ai-use-disclosure}')
part=text[start:end];table_count=0
def resize_table(match):
 global table_count
 x=match[0];assert x.count('\\real{0.3333}')==3
 sizes=iter(['0.3333','0.4667','0.2000'])
 x=re.sub(r'\\real\{0\.3333\}',lambda _:r'\real{'+next(sizes)+'}',x);table_count+=1;return x
part=re.sub(r'\\begin\{longtable\}\[\]\{@\{\}(.*?)@\{\}\}',resize_table,part,flags=re.S)
assert table_count==5
text=text[:start]+part+text[end:]
events.append('Widen the Meaning column in all five notation tables, retaining the symbol-column width; no content or formula changes.')
# Keep the compact dependency table together; widen the descriptive operation column.
change(r'\begin{document}',r'\usepackage{needspace}'+'\n'+r'\begin{document}','Load needspace for the generated dependency-table layout.')
change('The main proof dependencies are:',r'\Needspace{26\baselineskip}'+'\n'+'The main proof dependencies are:','Move the complete dependency table with its lead-in when remaining page space is insufficient.')
a=text.index('\\begin{longtable}')
bb=text.index('\\end{longtable}',a)
part=text[a:bb]
assert part.count('\\\\')==8
part=part.replace('\\\\','\\\\*')
text=text[:a]+part+text[bb:]
events.append('Prohibit internal page breaks in the eight-row dependency table.')
a=text.index('\\begin{longtable}',text.index('before its final wire reduction.'))
bb=text.index('\\end{longtable}',a)
part=text[a:bb]
oldwidths=['0.1579','0.2105','0.2105','0.2105','0.2105']
newwidths=iter(['0.3400','0.1600','0.1600','0.1800','0.1600'])
actual=re.findall(r'\\real\{([0-9.]+)\}',part)
assert actual==oldwidths,actual
part=re.sub(r'\\real\{[0-9.]+\}',lambda _:r'\real{'+next(newwidths)+'}',part)
text=text[:a]+part+text[bb:]
events.append('Widen the operation-description column and narrow numerical columns without changing cells.')
a,b=fp(before),fp(text);assert len(a)==len(b)
exceptions=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
assert len(exceptions)==2 and all(b[i]==a[i]+'.' for i in exceptions),exceptions
assert label_ids(before)==label_ids(text)
t.write_text(text)
(w/'MANUAL-TEX-DIFF.patch').write_text(''.join(difflib.unified_diff(before.splitlines(keepends=True),text.splitlines(keepends=True),fromfile='fresh-pipeline.tex',tofile='reviewed-layout.tex')))
(w/'MANUAL-TEX-ADJUSTMENTS.json').write_text(json.dumps({'events':events,'retained_v0212_layout':True,'raw_hash_matched':report['original_tex_sha256'],'math_regions':len(a),'punctuation_only_exceptions':exceptions,'all_other_math_fingerprints_preserved':True,'ordered_labels_preserved_under_declared_heading_aliases':True,'heading_anchor_aliases':heading_aliases},indent=2)+'\n')

# Complete the previously reviewed export-only layout changes in one pass.
a=r'\(A(Dg)(u,v,w)=Dg[u](v,w)+Dg[v](u,w)-Dg[w](u,v)\).'
b=r'\[A(Dg)(u,v,w)=Dg[u](v,w)+Dg[v](u,w)-Dg[w](u,v).\]'
change(a,b,'Promote the unchanged complete Christoffel identity; retain its sentence-ending punctuation.')
a=' C_m=\\operatorname{diag}(I_2,mI_2),\\qquad\n Z_t=C_mZ_u,\\qquad U_t=C_mU_uC_m^{-1},\\qquad\n \\mathcal T_t=m^2\\mathcal T_u.'
b=' \\begin{aligned}\n C_m&=\\operatorname{diag}(I_2,mI_2),\\qquad Z_t=C_mZ_u,\\\\\n U_t&=C_mU_uC_m^{-1},\\qquad \\mathcal T_t=m^2\\mathcal T_u.\n \\end{aligned}'
change(a,b,'Reflow the existing physical/dimensionless phase dictionary into two aligned rows.')
for key in ['app:gg-ordered-jets','sec:sh-integrated-scale','sec:sh-integrated-comparison','sec:sh-integrated-optics','sec:sh-optical-error','sec:sh-r1-primitive-comparison','sec:gg-notation-local-conventions','lem:schw-bc-compatible-local-amplitude','sec:sch-r1-rational-optics']:
 needle=r'\protect\phantomsection\label{'+key+'}'
 if needle in text:change(needle,r'\Needspace{9\baselineskip}'+'\n'+needle,'Keep '+key+' heading with following proof text.')
needle=r'\protect\phantomsection\label{app:sh-schwarzschild}'
change(needle,r'\clearpage'+'\n'+needle,'Start the mathematical Schwarzschild Appendix K on a new page.')
needle=r'\protect\phantomsection\label{app:gg-notation}'
change(needle,r'\clearpage'+'\n'+needle,'Start the final notation Appendix L on a new page.')
a=r''' \begin{aligned}
 a_s=\frac{q^2}{\sqrt2}\bigl[&(z_--z_+)d\tau
   +i(1-z_-z_+)dx+(1+z_-z_+)dy
   +i(z_-+z_+)dz\bigr]\\
 =\frac1{\sqrt2}&(x\,dx+y\,dy+z\,dz-i\varrho\,d\tau)
 =\frac{\varrho}{\sqrt2}(d\varrho-i\,d\tau).
 \end{aligned}'''
b=r''' \begin{aligned}
 a_s&=\frac{q^2}{\sqrt2}\bigl[(z_--z_+)d\tau+i(1-z_-z_+)dx\\
 &\qquad+(1+z_-z_+)dy+i(z_-+z_+)dz\bigr]\\
 &=\frac1{\sqrt2}(x\,dx+y\,dy+z\,dz-i\varrho\,d\tau)\\
 &=\frac{\varrho}{\sqrt2}(d\varrho-i\,d\tau).
 \end{aligned}'''
change(a,b,'Reflow the complete primitive null-form identity into four aligned rows.')

for a in [r"\nabla_v\omega^B=-it^{BB'}\pi_{B'}",r"\nabla_v\pi_{B'}=-it^{AA'}P^{\mathrm P}_{AA'BB'}\omega^B",r"\nabla_v(\omega,\pi)^T=-\Omega_v(\omega,\pi)^T"]:
 b=a.replace('=',r'=\allowbreak',1)
 change(a,b,'Permit the existing equality break in a primary transport comparison.')
a=r""" \Phi_{\rm pr}(v,r,\theta,\phi)=
 \left(\tau=i(r-v),\ x=r\sin\theta\cos\phi,
       \ y=r\sin\theta\sin\phi,\ z=r\cos\theta\right)."""
b=r""" \Phi_{\rm pr}(v,r,\theta,\phi)=
 \left(\begin{aligned}\tau=i(r-v),\ x=r\sin\theta\cos\phi,\\
       \ y=r\sin\theta\sin\phi,\ z=r\cos\theta\end{aligned}\right)."""
change(a,b,'Reflow the unchanged calibrated source-coordinate tuple into two rows.')


a=r"\(\nabla_v\omega^B=\allowbreak-it^{BB'}\pi_{B'}\)";b=r"\[\nabla_v\omega^B=-it^{BB'}\pi_{B'}\]"
change(a,b,'Retain the established unnumbered first-transport display.')
for key in ['sec:gg-notation-bundles','sec:gg-notation-execution','sec:gg-notation-simultaneous-diagram','prop:gg-schwarzschild-finite-readout']:
 a=r'\protect\phantomsection\label{'+key+'}'
 change(a,r'\Needspace{9\baselineskip}'+'\n'+a,'Retain established heading/anchor pagination for '+key+'.')
a=r'\protect\phantomsection\label{app:gg-optical}'
change(a,r'\Needspace{12\baselineskip}'+'\n'+a,'Retain established Appendix D heading pagination.')

x,y=fp(before),fp(text);assert len(x)==len(y)
d=[i for i,(a,b) in enumerate(zip(x,y)) if a!=b]
assert all(y[i]==x[i]+'.' for i in d),d
assert label_ids(before)==label_ids(text)
t.write_text(text)
(w/'MANUAL-TEX-DIFF.patch').write_text(''.join(difflib.unified_diff(before.splitlines(keepends=True),text.splitlines(keepends=True),fromfile='fresh-pipeline.tex',tofile='reviewed-layout.tex')))
(w/'MANUAL-TEX-ADJUSTMENTS.json').write_text(json.dumps({'events':events,'retained_v0212_layout':True,'raw_hash_matched':report['original_tex_sha256'],'math_regions':len(x),'punctuation_only_exceptions':d,'all_other_math_fingerprints_preserved':True,'ordered_labels_preserved_under_declared_heading_aliases':True,'heading_anchor_aliases':heading_aliases},indent=2)+'\n')
env=os.environ.copy();env.update(TEXMFCACHE='./texmf-cache',TEXMFVAR='./texmf-var',TEXINPUTS=str(paper)+':'+str(root)+':')
for i in [1,2]:
 r=subprocess.run(['xelatex','-halt-on-error','-interaction=nonstopmode','-file-line-error',str(t)],cwd=w,env=env,capture_output=True,text=True,timeout=120)
 (w/f'latex-final-{i}.log').write_text(r.stdout+'\n'+r.stderr)
 assert r.returncode==0,r.stdout[-2500:]
print(json.dumps({'manual_events':len(events),'math_regions':len(x),'punctuation_exceptions':d,'work':str(w)}))

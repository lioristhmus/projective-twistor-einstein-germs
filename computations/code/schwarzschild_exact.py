import os,sys,json,time,hashlib
from pathlib import Path
start=time.monotonic()
cg=Path('/sys/fs/cgroup')
limits={n:(cg/n).read_text().strip() for n in ['memory.max','memory.swap.max','cpu.max','pids.max']}
assert int(limits['memory.max'])+int(limits['memory.swap.max'])<=2*1024**3
q,p=limits['cpu.max'].split();assert q!='max' and int(q)<=int(p)
assert int(limits['pids.max'])<=64
import sympy as s
r,m,E,L,u,th=s.symbols('r m E L u theta', nonzero=True, real=True)
f=1-2*m/r
coords=s.symbols('v'),r,th,s.symbols('phi')
g=s.Matrix([[-f,1,0,0],[1,0,0,0],[0,0,r*r,0],[0,0,0,r*r*s.sin(th)**2]])
gi=s.Matrix([[0,1,0,0],[1,f,0,0],[0,0,r**-2,0],[0,0,0,1/(r*r*s.sin(th)**2)]])
assert s.simplify(g*gi)==s.eye(4)
G={}
for a in range(4):
 for b in range(4):
  for c in range(4):
   G[a,b,c]=s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d])) for d in range(4))/2)
R={}
for a in range(4):
 for b in range(4):
  for c in range(4):
   for d in range(4):
    R[a,b,c,d]=s.simplify(s.diff(G[a,d,b],coords[c])-s.diff(G[a,c,b],coords[d])+sum(G[a,c,e]*G[e,d,b]-G[a,d,e]*G[e,c,b] for e in range(4)))
Ric=s.Matrix(4,4,lambda b,c:s.simplify(sum(R[a,c,a,b] for a in range(4))))
assert Ric==s.zeros(4)
k=s.Matrix([(E-u)/f,-u,0,L/r**2])
relation=u*u-(E*E-f*L*L/r**2)
def reduce(x):
 a,b=s.cancel(x).as_numer_denom();a=s.rem(a,s.Poly(relation,u),u);return s.factor(a/b)
assert reduce((k.T*g.subs(th,s.pi/2)*k)[0])==0
out=reduce(sum(R[2,b,2,d].subs(th,s.pi/2)*k[b]*k[d] for b in range(4) for d in range(4)))
assert s.simplify(out-3*m*L*L/r**5)==0,out
# The unit polar screen is parallel along the equatorial ray.
e2=s.Matrix([0,0,1/r,0]);de2=-u*e2.diff(r)
assert all(s.simplify(de2[a]+sum(G[a,b,c].subs(th,s.pi/2)*k[b]*e2[c] for b in range(4) for c in range(4)))==0 for a in range(4))
# Derive radial acceleration from the computed connection, then differentiate
# y=r*sin(phi) using the geodesic equations, without inserting an expected rpp.
rpp=reduce(-sum(G[1,b,c].subs(th,s.pi/2)*k[b]*k[c] for b in range(4) for c in range(4)))
assert s.simplify(rpp-(L*L/r**3-3*m*L*L/r**4))==0
ph=s.symbols('ph');phip=L/r**2;phipp=2*L*u/r**3
jacobi_second=reduce((rpp-r*phip**2)*s.sin(ph)+(-2*u*phip+r*phipp)*s.cos(ph))
assert s.simplify(jacobi_second+3*m*L**2/r**5*r*s.sin(ph))==0
# Scalar curvature conformal law for h=-+++ and h_K=r^-2 h.
logO=-s.log(r)
boxlog=s.simplify(s.diff(r*r*f*s.diff(logO,r),r)/(r*r))
gradlog=s.simplify(f*s.diff(logO,r)**2)
scal=s.simplify(r*r*(-6*boxlog-6*gradlog))
assert scal==12*m/r
boxK_r=s.simplify(r**2*s.diff(f,r));assert boxK_r==2*m
# Direct almost-Einstein check in h_K, sigma=1/r.
gk=g/r**2;gki=gi*r**2
volume=s.sin(th)/r**2
assert s.simplify(volume**2+gk.det())==0
boxK_direct=s.simplify(sum(s.diff(volume*gki[a,b]*s.diff(r,coords[b]),coords[a]) for a in range(4) for b in range(4))/volume)
assert boxK_direct==boxK_r
GK={}
for a in range(4):
 for b in range(4):
  for c in range(4):GK[a,b,c]=s.simplify(sum(gki[a,d]*(s.diff(gk[d,c],coords[b])+s.diff(gk[d,b],coords[c])-s.diff(gk[b,c],coords[d])) for d in range(4))/2)
Rick=s.Matrix(4,4,lambda b,c:s.simplify(sum(s.diff(GK[a,c,b],coords[a])-s.diff(GK[a,a,b],coords[c])+sum(GK[a,a,e]*GK[e,c,b]-GK[a,c,e]*GK[e,a,b] for e in range(4)) for a in range(4))))
scalk=s.simplify(sum(gki[a,b]*Rick[a,b] for a in range(4) for b in range(4)));assert scalk==scal
P=(Rick-scalk*gk/6)/2;sig=1/r
H=s.Matrix(4,4,lambda a,b:s.simplify(s.diff(sig,coords[a],coords[b])-sum(GK[c,a,b]*s.diff(sig,coords[c]) for c in range(4))+P[a,b]*sig))
trH=s.simplify(sum(gki[a,b]*H[a,b] for a in range(4) for b in range(4)))
assert s.simplify(H-gk*trH/4)==s.zeros(4)
rho=-trH/4;grad=s.Matrix([s.diff(sig,c) for c in coords]);norm=s.simplify(2*sig*rho+(grad.T*gki*grad)[0]);assert norm==0
assert s.simplify(rho+f/(2*r))==0
assert s.simplify(H+gk*rho)==s.zeros(4)
raised_mu=gki*grad
assert all(s.simplify(s.diff(rho,coords[a])-sum(P[a,b]*raised_mu[b] for b in range(4)))==0 for a in range(4))
report={'status':'PASS','mathematical_scope':'Exact symbolic identities of a fixed four-dimensional Schwarzschild chart; no general convergence theorem certified.','python':sys.version,'sympy':s.__version__,'cgroup_limits':limits,'metric_signature':'-+++ intermediate; baseline metric is its explicit negation','lapse':str(f),'inverse_metric':True,'Ricci_zero':True,'polar_screen_parallel':True,'polar_tidal_coefficient':str(out),'rotation_Jacobi_check':True,'scalar_curvature_r_minus_2_h':str(scal),'box_r_for_r_minus_2_h':str(boxK_r),'almost_Einstein_sigma':str(sig),'normal_tractor_norm':str(norm),'rho':str(s.factor(rho)),'tractor_all_parallel_equations':True,'laplace_beltrami_r_direct':str(boxK_direct),'seconds':time.monotonic()-start,'network':'none as inspected before container start'}
data=json.dumps(report,indent=2)+'\n';assert len(data.encode())<65536
# Results are captured by the common worker; no writable host mount.
print(data)

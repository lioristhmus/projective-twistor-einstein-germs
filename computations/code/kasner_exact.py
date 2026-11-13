"""Exact finite geometric check. Run only under the isolated job controller.

Compute covariant curvature derivatives of the Kasner vacuum independently of
the record recursion, project the chiral records, and compare the normalized
Spencer recurrence through the requested order. Unscaled spin basis factors
cancel in every homogeneous identity tested below.
"""
import argparse
import itertools as it
import json
import math
import resource
import time
from pathlib import Path

cgroup = Path('/sys/fs/cgroup')
actual_limits = {name:(cgroup/name).read_text().strip() for name in
                 ['memory.max','memory.swap.max','cpu.max','pids.max']}
assert 0 < int(actual_limits['memory.max']) <= 2_000_000_000
assert int(actual_limits['memory.swap.max']) == 0
quota,period = actual_limits['cpu.max'].split()
assert quota != 'max' and 0 < int(quota) <= int(period)
assert int(actual_limits['pids.max']) <= 64
from sage.all import QQ, QuadraticField, matrix

ap = argparse.ArgumentParser()
ap.add_argument('--max-r', type=int, choices=(1, 2, 3), default=1)
args = ap.parse_args()
started = time.monotonic()
K = QuadraticField(-1, 'I')
I = K.gen()
ps = [QQ(0), QQ(-2)/7, QQ(3)/7, QQ(6)/7]
eta = [1, -1, -1, -1]
gamma = {}
structure = {}
for i in range(1, 4):
    gamma[i, 0, i] = ps[i]
    gamma[i, i, 0] = ps[i]
    structure[0, i, i] = -ps[i]
    structure[i, 0, i] = ps[i]
G = lambda a,b,c: gamma.get((a,b,c), QQ(0))
C = lambda a,b,c: structure.get((a,b,c), QQ(0))
R = {}
for a,b,c,d in it.product(range(4), repeat=4):
    R[a,b,c,d] = (-(a == 0)*G(b,c,d)+(b == 0)*G(a,c,d)
        + sum(G(b,c,e)*G(a,e,d)-G(a,c,e)*G(b,e,d)
              - C(a,b,e)*G(e,c,d) for e in range(4)))
assert all(sum(R[a,b,c,a] for a in range(4)) == 0
           for b,c in it.product(range(4), repeat=2))
assert sum(ps) == 1 and sum(p*p for p in ps) == 1

def index(xs):
    k = 0
    for x in xs:
        k = 4*k+x
    return k

D = [[eta[d]*R[a,b,c,d] for a,b,c,d in it.product(range(4), repeat=4)]]
for r in range(1, args.max_r+2):
    old = D[-1]
    rank = r+3
    new = []
    for a in range(4):
        for xs in it.product(range(4), repeat=rank):
            value = -(r+1)*old[index(xs)] if a == 0 else QQ(0)
            if a:
                for j, x in enumerate(xs):
                    if x in (0, a):
                        ys = list(xs)
                        ys[j] = a if x == 0 else 0
                        value -= ps[a]*old[index(ys)]
            new.append(value)
    D.append(new)

# L is sqrt(2) times the normalized spin tangent basis. The raw tensor of
# order r carries a common factor 2^((r+4)/2); every recurrence identity has
# order r+5, so exact raw coefficients can be compared in Q(i).
L = matrix(K, [[1,0,0,1], [0,1,1,0], [0,-I,I,0], [1,0,0,-1]])
Li = L.inverse()
def transform(values, rank):
    arr = [K(v) for v in values]
    for ax in range(rank):
        stride = 4**(rank-ax-1)
        out = [K(0)]*len(arr)
        for pre in range(4**ax):
            offset = pre*4*stride
            for suf in range(stride):
                for s in range(4):
                    out[offset+s*stride+suf] = sum(
                        L[a,s]*arr[offset+a*stride+suf]
                        for a in range(4) if L[a,s])
        arr = out
    return arr

eps = {(0,1): -1, (1,0): 1}
psi = [{}, {}]
for r, vals in enumerate(D):
    arr = transform(vals, r+4)
    for ds in it.product(range(4), repeat=r):
        for bs in it.product(range(2), repeat=4):
            for ch in (0,1):
                value = K(0)
                for (x,y), e in eps.items():
                    for (z,w), f in eps.items():
                        cs = (x,y,z,w)
                        tail = tuple(2*bs[k]+cs[k] if ch == 0
                                     else 2*cs[k]+bs[k] for k in range(4))
                        value -= QQ(e*f)/4*arr[index(ds+tail)]
                psi[ch][r,ds,bs] = value
    del arr

sym_cache = {}
def sym(ch, r, outer=()):
    key = (ch,r,outer)
    if key in sym_cache:
        return sym_cache[key]
    n,m = (r+4,r) if ch == 0 else (r,r+4)
    out = {(u,v):K(0) for u in range(n+1) for v in range(m+1)}
    for ds in it.product(range(4), repeat=r):
        for bs in it.product(range(2), repeat=4):
            u = sum(s//2 for s in ds)+(sum(bs) if ch == 0 else 0)
            v = sum(s%2 for s in ds)+(sum(bs) if ch == 1 else 0)
            out[u,v] += psi[ch][r+len(outer),outer+ds,bs]
    for u,v in out:
        out[u,v] /= math.comb(n,u)*math.comb(m,v)
    sym_cache[key] = out
    return out

def Rspin(a,b):
    op = matrix(K,4,4,lambda d,c:sum(
        L[x,a]*L[y,b]*R[x,y,c,d] for x,y in it.product(range(4),repeat=2)))
    op = Li*op*L
    B = matrix(K,2,2,lambda x,y:sum(op[2*x+k,2*y+k] for k in range(2))/2)
    Bp = matrix(K,2,2,lambda x,y:sum(op[2*k+x,2*k+y] for k in range(2))/2)
    assert op == matrix(K,4,4,lambda x,y:
        (B[x//2,y//2] if x%2 == y%2 else 0)
        +(Bp[x%2,y%2] if x//2 == y//2 else 0))
    return B,Bp

def curvature_action(ch,r,a,b,u,v):
    n,m = (r+4,r) if ch == 0 else (r,r+4)
    U = sym(ch,r)
    B,Bp = Rspin(a,b)
    value = ((n-u)*B[0,0]+u*B[1,1]
              +(m-v)*Bp[0,0]+v*Bp[1,1])*U[u,v]
    if u < n: value += (n-u)*B[1,0]*U[u+1,v]
    if u: value += u*B[0,1]*U[u-1,v]
    if v < m: value += (m-v)*Bp[1,0]*U[u,v+1]
    if v: value += v*Bp[0,1]*U[u,v-1]
    return value

def upper(T,n,m,primed=False):
    out = {}
    for s,u,v in T:
        a,b = s//2,s%2
        if not primed:
            k = u+a
            val = ((n+1-k)*T.get((b,k,v),0)
                    + k*T.get((2+b,k-1,v),0))/(n+1)
        else:
            k = v+b
            val = ((m+1-k)*T.get((2*a,u,k),0)
                    + k*T.get((2*a+1,u,k-1),0))/(m+1)
        out[s,u,v] = val
    return out

# Initial Einstein/Bianchi case is checked explicitly; the later HQ values
# are geometrically differentiated, not polynomial product-rule evaluations.
for ch in (0,1):
    n,m=(4,0) if ch==0 else (0,4)
    U=sym(ch,1)
    assert all(sym(ch,0,(s,))[u,v]-U[u+s//2,v+s%2]==0
               for s,u,v in it.product(range(4),range(n+1),range(m+1)))
results = []
for r in range(1,args.max_r+1):
    for ch in (0,1):
        n,m = (r+4,r) if ch == 0 else (r,r+4)
        U = sym(ch,r+1)
        Q = {(s,u,v):sym(ch,r,(s,))[u,v]-U[u+s//2,v+s%2]
             for s,u,v in it.product(range(4),range(n+1),range(m+1))}
        def HQ(a,b,k,l):
            return (sym(ch,r-1,(a,b))[k,l]
                    - sym(ch,r,(a,))[k+b//2,l+b%2])
        S = {}
        for a,u,v in Q:
            value = K(0)
            for bit,bitp in it.product(range(2),repeat=2):
                k,l = u-bit,v-bitp
                if not (0 <= k < n and 0 <= l < m): continue
                wt = QQ(u if bit else n-u)/n * QQ(v if bitp else m-v)/m
                if not wt: continue
                b = 2*bit+bitp
                value += wt*(HQ(b,a,k,l)-curvature_action(ch,r-1,a,b,k,l))
            S[a,u,v] = value
        Pn = upper(S,n,m)
        Pm = upper(S,n,m,True)
        Pboth = upper(Pn,n,m,True)
        predicted = {}
        for key in S:
            predicted[key] = (QQ(n)/(n+1)*(Pm[key]-Pboth[key])
                + QQ(m)/(m+1)*(Pn[key]-Pboth[key])
                + QQ(n*m)/(n*m-1)*(S[key]-Pn[key]-Pm[key]+Pboth[key]))
        errors = [k for k in Q if Q[k] != predicted[k]]
        upperQ = upper(upper(Q,n,m),n,m,True)
        errors_upper = [k for k in Q if upperQ[k]]
        assert not errors, ('recursion',r,ch,errors[:3])
        assert not errors_upper, ('free projection',r,ch,errors_upper[:3])
        results.append({'r':r,'chirality':'+' if ch == 0 else '-',
                        'components':len(Q),'recursion_residuals':0,
                        'free_projection_residuals':0})

print(json.dumps({'status':'PASS','field':'Q(i)',
    'metric':'dt^2 - sum(t^(2*p_i) dx_i^2)',
    'kasner_exponents':[str(p) for p in ps[1:]],
    'Lambda':0,'at_t':1,'orders':results,
    'max_r':args.max_r,'elapsed_seconds':time.monotonic()-started,
    'runtime_cgroup_limits':actual_limits,
    'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    'Q0_zero_checked':True,'HQ_route':'geometrically differentiated Q, not polynomial record product rule','scope':'finite exact geometric commutator checks on this Einstein metric, not a polynomial all-input or all-order proof'}))

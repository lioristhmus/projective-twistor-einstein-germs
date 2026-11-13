"""Exact low-order free-record tests; execute only in the isolated container.

Independent rational array backend for the published Spencer maps and Cartan
product rule. The nilpotent bookkeeping follows the earlier numerical route;
it is not an independent derivation of the recurrence or an all-order proof.
"""
import itertools as it
from math import comb
import numpy as np
from sage.all import QQ
import report

CH=(1,-1)
EPS=((0,1),(-1,0))
def zero(shape):
    out=np.empty(shape,dtype=object);out.fill(QQ(0));return out
def scale(X,a):
    out=zero(X.shape)
    for i,v in enumerate(X.flat):out.flat[i]=a*v
    return out
def deg(c,r):return (r+4,r) if c==1 else (r,r+4)
def du(P,a):
    n=P.shape[-2]-1
    weights=np.array([QQ(n-k if a==0 else k+1) for k in range(n)],dtype=object)
    return (P[...,:n,:] if a==0 else P[...,1:,:])*weights[:,None]
def dv(P,a):
    n=P.shape[-1]-1
    weights=np.array([QQ(n-k if a==0 else k+1) for k in range(n)],dtype=object)
    return (P[...,:n] if a==0 else P[...,1:])*weights
def mu(P,a):
    shape=list(P.shape);shape[-2]+=1;out=zero(shape)
    if a==0:out[...,:-1,:]=P
    else:out[...,1:,:]=P
    return out
def mv(P,a):
    shape=list(P.shape);shape[-1]+=1;out=zero(shape)
    if a==0:out[...,:-1]=P
    else:out[...,1:]=P
    return out
def jmap(P):
    n=P.shape[-2]-1;m=P.shape[-1]-1
    return scale(np.stack([np.stack([du(dv(P,b),a) for b in range(2)],axis=-3)
                     for a in range(2)],axis=-4),QQ(1)/(n*m))
def jstar(X):
    out=None
    for a,b in it.product(range(2),repeat=2):
        v=mu(mv(X[...,a,b,:,:],b),a)
        out=v if out is None else out+v
    return out
def tau(X):return X.swapaxes(-6,-4).swapaxes(-5,-3)
def upper_u(X):
    n=X.shape[-2]-1
    poly=mu(X[...,0,:,:,:],0)+mu(X[...,1,:,:,:],1)
    return scale(np.stack([du(poly,a) for a in range(2)],axis=-4),QQ(1)/(n+1))
def upper_v(X):
    m=X.shape[-1]-1
    poly=mv(X[...,:,0,:,:],0)+mv(X[...,:,1,:,:],1)
    return scale(np.stack([dv(poly,b) for b in range(2)],axis=-3),QQ(1)/(m+1))
def blocks(X):
    pu=upper_u(X);pp=upper_v(pu);pm=pu-pp
    low=X-pu;mp=upper_v(low);mm=low-mp
    return pp,pm,mp,mm
def Mop(X):
    n=X.shape[-2]-1;m=X.shape[-1]-1
    pp,pm,mp,mm=blocks(X)
    return scale(mp,QQ(n)/(n+1))+scale(pm,QQ(m)/(m+1))+scale(mm,QQ(n*m)/(n*m-1))
def delta(X):
    v=jmap(X);return v-tau(v)
def iszero(X):return all(v==0 for v in X.flat)
def exact(X):return all(v in QQ and not isinstance(v,(float,np.floating)) for v in X.flat)


def beta(p,chir):
    shape=p.shape[:-1];phi=zero(shape+(2,2,2,2))
    for a,b,c in it.product(range(2),repeat=3):
        phi[...,a,b,0,c]=p[...,a+b+c+1]/comb(4,a+b+c+1)
        phi[...,a,b,1,c]=-p[...,a+b+c]/comb(4,a+b+c)
    Bs=zero(shape+(2,)*6);Bt=zero(Bs.shape)
    for a,ap,b,bp,d,c in it.product(range(2),repeat=6):
        if chir==1:Bs[...,a,ap,b,bp,d,c]=-EPS[ap][bp]*phi[...,a,b,d,c]
        else:Bt[...,a,ap,b,bp,d,c]=-EPS[a][b]*phi[...,ap,bp,d,c]
    return Bs,Bt


def spin(P,Bs,Bt):
    n,m=P.shape[-2:];out=zero(P.shape[:-2]+(2,2,2,2,n,m))
    for d,c in it.product(range(2),repeat=2):
        gu=mu(du(P,d),c);gv=mv(dv(P,d),c)
        for a,ap,b,bp in it.product(range(2),repeat=4):
            out[...,a,ap,b,bp,:,:]+=Bs[...,a,ap,b,bp,d,c][...,None,None]*gu
            out[...,a,ap,b,bp,:,:]+=Bt[...,a,ap,b,bp,d,c][...,None,None]*gv
    return out


def subsets(S):
    T=S
    while True:
        yield T
        if T==0:break
        T=(T-1)&S


STATS={}
def curvature_source(X,k,r,co):
    P=X[co,r-1];out=zero(P.shape[:-2]+(2,2,2,2)+P.shape[-2:])
    for cw in CH:
        p=X[cw,0][...,:,0] if cw==1 else X[cw,0][...,0,:]
        Bs,Bt=beta(p,cw)
        for S in range(2**k):
            for T in subsets(S):
                if iszero(p[T]) or iszero(P[S^T]):continue
                out[S]+=spin(P[S^T],Bs[T],Bt[T])
    return out


def Qlist(X,k,R):
    Q=[{co:None for co in CH}]
    for r in range(1,R+1):
        if r>=2:
            Xp={}
            for c in CH:
                for j in range(r-1):
                    base=X[c,j];direction=jmap(X[c,j+1])
                    if Q[j][c] is not None:direction=direction+Q[j][c]
                    new=zero((2**(k+1),)+base.shape[1:-2]+(2,2)+base.shape[-2:])
                    new[:2**k]=base[...,None,None,:,:]
                    new[2**k:]=direction
                    Xp[c,j]=new
            Qd=Qlist(Xp,k+1,r-1)[r-1]
        Qr={}
        for co in CH:
            K=curvature_source(X,k,r,co)
            HQ=Qd[co][2**k:] if r>=2 else zero(K.shape)
            RHS=-K-HQ+tau(HQ)
            assert iszero(jstar(HQ)),('JstarHQ',r,k,co)
            value=Mop(jstar(RHS))
            assert exact(value),('nonexact coefficient',r,k,co)
            assert iszero(delta(value)-RHS),('exact-set',r,k,co)
            assert iszero(blocks(value)[0]),('free projection',r,k,co)
            key=(r,k,co)
            STATS[key]=STATS.get(key,0)+value.size
            Qr[co]=value
        Q.append(Qr)
    return Q


def coherent(c,j,xi,pi):
    n,m=deg(c,j)
    return np.array([[QQ(comb(n,a)*comb(m,b))*xi[0]**(n-a)*xi[1]**a
                      *pi[0]**(m-b)*pi[1]**b for b in range(m+1)]
                     for a in range(n+1)],dtype=object)


def run(profile):
    R=profile['max_r'];projector_rows=[]
    # Entire coefficient bases, rather than one coherent vector, exercise all
    # blocks of the finite Spencer maps. This part does not assume exact-set
    # surjectivity on arbitrary antisymmetric source tensors.
    for r in range(1,R+1):
        for c in CH:
            n,m=deg(c,r);N=4*(n+1)*(m+1)
            X=zero((N,2,2,n+1,m+1))
            for i in range(N):X.reshape(N,N)[i,i]=QQ(1)
            pp,pm,mp,mm=blocks(X)
            assert all(exact(v) for v in (X,pp,pm,mp,mm,jmap(X))), 'nonrational projector coefficient'
            assert iszero(X-pp-pm-mp-mm)
            assert iszero(delta(pp))
            res=Mop(jstar(delta(X)))-(X-pp)
            assert iszero(res),('inverse',r,c,[(i,str(v)) for i,v in enumerate(res.flat) if v!=0][:8])
            assert iszero(jstar(delta(X))-(scale(mp,QQ(n+1)/n)+scale(pm,QQ(m+1)/m)+scale(mm,QQ(n*m-1)/(n*m))))
            for i,B in enumerate((pp,pm,mp,mm)):
                assert iszero(blocks(B)[i]-B)
            projector_rows.append({'r':r,'chirality':c,'basis_dimension':N})
    report.check('AB-PROJECTORS-R'+str(R),'Exact finite-basis Spencer/free projections',True,
                 classification='finite-exact',basis_tests=projector_rows,
                 scope='All basis vectors of D_r for 1<=r<=max_r and both chiralities; no all-order claim.')

    # Every binary quartic basis vector yields a Ricci-free algebraic curvature
    # operator. Check metric skewness and the first Bianchi identity explicitly.
    curvature_components=0
    eta=np.array([[QQ(EPS[a//2][b//2]*EPS[a%2][b%2]) for b in range(4)] for a in range(4)],dtype=object)
    for c in CH:
        for j in range(5):
            p=zero((5,));p[j]=QQ(1);Bs,Bt=beta(p,c)
            O=zero((4,4,4,4))
            for a,b,d,e in it.product(range(4),repeat=4):
                O[a,b,d,e]=(Bs[a//2,a%2,b//2,b%2,d//2,e//2] if d%2==e%2 else 0)
                O[a,b,d,e]+=(Bt[a//2,a%2,b//2,b%2,d%2,e%2] if d//2==e//2 else 0)
            for a,b in it.product(range(4),repeat=2):
                assert iszero(O[a,b]+O[b,a])
                assert iszero(eta@O[a,b]+O[a,b].T@eta)
            for a,b,e,d in it.product(range(4),repeat=4):
                assert O[a,b,d,e]+O[b,e,d,a]+O[e,a,d,b]==0
                curvature_components+=1
            for b,e in it.product(range(4),repeat=2):assert sum(O[a,b,a,e] for a in range(4))==0
            # A compatibility residual alone is insensitive to a simultaneous
            # curvature scaling. Calibrate the actual signed Weyl readout.
            def lowered(a,b,c0,d):return sum(eta[d,e]*O[a,b,e,c0] for e in range(4))
            for output_chirality in CH:
                for fixed in it.product(range(2),repeat=4):
                    value=QQ(0)
                    for free in it.product(range(2),repeat=4):
                        weight=-QQ(EPS[free[0]][free[1]]*EPS[free[2]][free[3]])/4
                        if not weight:continue
                        indices=tuple(2*fixed[z]+free[z] if output_chirality==1
                                      else 2*free[z]+fixed[z] for z in range(4))
                        value+=weight*lowered(*indices)
                    expected=p[sum(fixed)]/comb(4,sum(fixed)) if output_chirality==c else QQ(0)
                    assert value==expected,('Weyl readout',c,j,output_chirality,fixed,value,expected)
    report.check('AB-WEYL-ADMISSIBILITY'+('-R1' if R==1 else ''),'Quartic Weyl inputs: curvature constraints and inverse chiral readout',True,
                 classification='finite-exact',quartic_basis_vectors=10,cyclic_components=curvature_components,inverse_readout_components=320,
                 scope='Complete linear Weyl basis at Lambda=0, including signed -1/4 inverse readout; higher free lists are symmetric spinor coefficients, not arbitrary ordered curvature arrays.')

    labels=[(1,(QQ(1),QQ(0)),(QQ(1),QQ(1)),1),
            (1,(QQ(1),QQ(1)),(QQ(0),QQ(1)),2),
            (-1,(QQ(1),QQ(2)),(QQ(2),QQ(-1)),3)]
    X={}
    for c in CH:
        for j in range(R):
            n,m=deg(c,j);X[c,j]=zero((8,n+1,m+1))
            for i,(ci,xi,pi,z) in enumerate(labels):
                if c==ci:X[c,j][1<<i]=QQ(z)**j*coherent(c,j,xi,pi)
    STATS.clear();Q=Qlist(X,3,R)
    # Explicitly identify the lowest polarized coefficient, with no hidden 1/2.
    y=coherent(1,0,labels[0][1],labels[0][2]);w=coherent(1,0,labels[1][1],labels[1][2])
    By=beta(y[:,0],1);Bw=beta(w[:,0],1)
    ordered_yw=-Mop(jstar(spin(w,*By)))
    ordered_wy=-Mop(jstar(spin(y,*Bw)))
    assert iszero(Q[1][1][3]-ordered_yw-ordered_wy)
    assert not iszero(Q[1][1][3])
    top=[]
    for r in range(1,R+1):
        for c in CH:
            v=Q[r][c]
            top.append({'r':r,'chirality':c,'scalar_coefficients':v.size,
                        'nonzero_coefficients':sum(x!=0 for x in v.flat),
                        'mixed_cubic_nonzero':not iszero(v[7])})
    if R>=4:assert any(row['mixed_cubic_nonzero'] for row in top if row['r']==4)
    report.check('AB-EXACT-SET-R'+str(R),'Exact recurrence on a declared mixed free-record family',True,
                 classification='finite-exact',field='QQ',Lambda=0,max_r=R,
                 algebra='QQ[e0,e1,e2]/(e0^2,e1^2,e2^2); additional square-zero variables implement derivatives',
                 labels=[{'chirality':c,'xi':list(map(str,xi)),'pi':list(map(str,pi)),'order_weight':z} for c,xi,pi,z in labels],
                 checks='delta Q=RHS, Jstar H Q=0, P++Q=0, every coefficient rational',
                 top_level=top,recursive_scalar_tests=sum(STATS.values()),polarization_r1='[e0e1]Q1(e0*y+e1*w)=B(y,w)+B(w,y), explicitly nonzero; no division by 2',
                 admissibility='Free lists lie in W_j by symmetric coherent construction; algebraic curvature constraints checked above. Applicability of formal completion to independent lists and coefficient algebras uses Proposition A.3/A.4, not a new computed metric witness.',
                 exclusions='One explicit finite quotient-algebra input family, Lambda=0. No independently constructed Einstein metric, general differentiated Bianchi completion, atomic mass, all-order estimate or convergence theorem is certified.')

import json
from pathlib import Path

limits = {p: Path('/sys/fs/cgroup', p).read_text().strip()
          for p in ['memory.max', 'memory.swap.max', 'cpu.max', 'pids.max']}
assert int(limits['memory.max']) <= 2_000_000_000
assert limits['memory.swap.max'] == '0'
quota, period = map(int, limits['cpu.max'].split())
assert quota <= period
assert int(limits['pids.max']) <= 32
print('CGROUP ' + json.dumps(limits), flush=True)

from sage.all import CyclotomicField, PolynomialRing, matrix, vector, identity_matrix, diagonal_matrix

K = CyclotomicField(8)
w = K.gen()
ii, sq2 = w**2, w - w**3
assert ii**2 == -1 and sq2**2 == 2
R = PolynomialRing(K, names=('tau', 'x', 'y', 'z', 'r', 'M', 'c', 'a', 'h'))
tau, x, y, z, r, M, c, a, h = R.gens()
F = R.fraction_field()
relation = r*r - x*x - y*y - z*z

def normal(f):
    f = F(f)
    return F(f.numerator().reduce([relation])) / F(f.denominator())

def zero(A):
    return all(normal(v) == 0 for v in A.list())

E = matrix(F, [[0, 1], [-1, 0]])
L = -E
ol = vector(F, [1, 0])
ou = E*ol
eta = matrix(F, 4, 4, lambda j,k: E[j//2,k//2]*E[j%2,k%2])
D = matrix(F, [[1/sq2,0,0,-ii/sq2], [0,ii/sq2,-1/sq2,0],
               [0,ii/sq2,1/sq2,0], [1/sq2,0,0,ii/sq2]])
I4 = identity_matrix(F,4)
assert D.transpose()*eta*D == I4
results = {}

# (2.13): independent scalar coefficients and the Cartesian null one-form.
q2 = (y-ii*x)/2
angle_T_alpha_sq = q2/2
first_coefficient = -2*ii*M / (ii*r*angle_T_alpha_sq)
second_coefficient = -8*M / (r*(y-ii*x))
assert first_coefficient == second_coefficient
assert first_coefficient*q2/2 == -2*M/r
results['2.13'] = {'first_equals_second': True, '2.3_scalar_coefficient_only': True}

# Tetrad metric and Gindikin two-form, using a general rank-one symmetric phi.
phi = h*matrix(F, [[1,a],[a,a*a]])
phiu = E*phi
N = matrix(F,4,4,lambda j,k:ou[j//2]*ol[k//2]*phiu[j%2,k%2])
O = matrix(F,4,4,lambda j,k:ol[j//2]*ol[k//2]*phi[j%2,k%2])
ec = (I4+c*N)*D
assert zero(ec.transpose()*eta*ec-I4-2*c*D.transpose()*O*D)

def wedge(u,v):
    return matrix(F,4,4,lambda j,k:u[j]*v[k]-v[j]*u[k])

def sigma_of_forms(forms):
    return sum((L[j,k]*wedge(forms[j],forms[k])
                for j in range(2) for k in range(2)), matrix(F,4,4,0))

sigma_c = sigma_of_forms([ec.row(2),ec.row(3)])
sigma_flat = sigma_of_forms([D.row(2),D.row(3)])
theta = [D.row(2+j)-sum((phiu[j,k]*D.row(k) for k in range(2)),vector(F,[0]*4))
         for j in range(2)]
sigma_theta = sigma_of_forms(theta)
correction = -sum((phi[d,e]*L[g,k]*wedge(D.row(2*g+d),D.row(2*k+e))
                   for d in range(2) for e in range(2)
                   for g in range(2) for k in range(2)),matrix(F,4,4,0))
sigma_printed = sigma_flat+correction
assert zero(sigma_theta-sigma_printed)
assert zero(sigma_c-sigma_flat-c*correction)
assert not zero(correction)
results['2.24'] = {
    'metric_correction_multiplier': '2*c; c=1/2 matches (2.17)',
    'sigma_correction_multiplier': 'c; printed (2.23) requires c=1',
    'theta_matches_printed_sigma': True,
    'half_tetrad_fails_printed_sigma_generically': True}

# (3.6): no covariant differentiation or choice of connection is involved.
u, v = x+ii*y, x-ii*y
zm, zp = (z+r)/u, (z-r)/u
qu = -ii*u/2
A0, B0 = vector(F,[-zm,1]), vector(F,[-zp,1])
Au, Bu = E*A0, E*B0
Kab = qu*matrix(F,2,2,lambda j,k:(Au[j]*Bu[k]+Au[k]*Bu[j])/2)
X = matrix(F,[[tau-ii*z,ii*x-y],[ii*x+y,tau+ii*z]])/sq2
T = identity_matrix(F,2)/sq2
TX = T*E*X.transpose()  # Lower dotted index to the right.
TX = (TX+TX.transpose())/2
assert zero(Kab+TX)
assert not zero(Kab-TX)
results['3.6'] = {'AB_equals_minus_TX': True,
                 'AB_matrix': str(Kab.apply_map(normal)),
                 'TX_matrix': str(TX)}

# (3.28): radial Laplace-Beltrami operator of the printed (3.20)-(3.21).
HH = 2*M/r
rad = matrix(F,[[1+HH,ii*HH],[ii*HH,1-HH]])/r**2
assert rad.det() == 1/r**4
assert rad.inverse()[1,1] == r**2*(1+HH)
Omega_printed = r/(24*M)
def lap_printed(f):
    return F(r**2)*((1+HH)*F(f).derivative(r)).derivative(r)
assert lap_printed(Omega_printed) == -F(1)/12
lapS_inv_r = F(1/r**2)*(r**2*(1+HH)*F(1/r).derivative(r)).derivative(r)
scalar_printed = -6*r**3*lapS_inv_r
assert scalar_printed == -12*M/r
Omega_consistent = -r/(12*M)
assert lap_printed(Omega_consistent) == F(1)/6
results['3.28'] = {'lap_r_over_24M_with_printed_metric': str(lap_printed(Omega_printed)),
                  'scalar_of_printed_metric': str(scalar_printed),
                  'consistent_Omega': str(Omega_consistent),
                  'consistent_lap_Omega': str(lap_printed(Omega_consistent))}

# Independent re-evaluation of the actual primitive retained in our K.5.
ph = -4*M/r*matrix(F,[[1,zm],[zm,zm**2]])
phraised = E*ph
s = qu*(zm-zp)
assert s == -ii*r
P0 = matrix(F,4,4,lambda j,k:qu*Au[j//2]*B0[k//2]/s
            * (1 if j%2 == k%2 else 0))
NN = matrix(F,4,4,lambda j,k:qu**2*Bu[j//2]*B0[k//2]/s**2
            * phraised[j%2,k%2])
PP = P0+NN
assert zero(PP*PP-PP)
JJ = ii*(I4-2*PP)
WS = matrix(F,4,4,lambda j,k:ii*qu/s**3
            *(A0[j//2]*B0[k//2]+B0[j//2]*A0[k//2])*L[j%2,k%2])
# Connect the adopted component matrix to the actual wedge expression.
omega_from_wedge=sum((ii*qu/s**3*A0[a]*B0[b]*L[ap,bp]
    *wedge(D.row(2*a+ap),D.row(2*b+bp))
    for a in range(2) for b in range(2) for ap in range(2) for bp in range(2)),matrix(F,4,4,0))
assert zero(omega_from_wedge-D.transpose()*WS*D)
assert PP.trace()==2 and zero(JJ*JJ+I4)
G = D.transpose()*WS*JJ*D
k = vector(F,[1,ii*x/r,ii*y/r,ii*z/r])
alpha0 = vector(F,[1,zm])
aa = qu*sum((B0[j]*alpha0[l]*D.row(2*j+l)
             for j in range(2) for l in range(2)),vector(F,[0]*4))
ell = -ii/r*aa
assert all(normal(ell[j]+k[j]/sq2)==0 for j in range(4))
printed_gS = I4+4*M/r*matrix(F,4,4,lambda j,l:ell[j]*ell[l])
assert zero(printed_gS-I4-2*M/r*matrix(F,4,4,lambda j,l:k[j]*k[l]))
GG = -1/r**2*(I4+4*M/r*matrix(F,4,4,lambda j,l:k[j]*k[l]))
assert zero(G-GG)
assert zero(G-G.transpose())
lap_ours = -r**2*((1+4*M/r)*F(r/(24*M)).derivative(r)).derivative(r)
assert lap_ours == F(1)/6

# Our EF pullback, with source mu=M/2, rho=-r, tau=i(r-v).
change = matrix(F,[[-ii,ii],[0,-1]])
kk = vector(F,[1,ii])
source = -2/r**2*(identity_matrix(F,2)-2*M/r
                  *matrix(F,2,2,lambda j,l:kk[j]*kk[l]))
ef = matrix(F,[[1-2*M/r,-1],[-1,0]])
assert zero(change.transpose()*source*change-2/r**2*ef)
results['our_K5'] = {'original_projector_idempotent': True,'projector_trace_two':True,'omega0_wedge_matches_components':True,
                     'G0_equals_minus_r_inv_sq_delta_plus_4mu': True,
                     'G0_symmetric': True,
                     'G0_lap_r_over_24mu': str(lap_ours),
                     'calibrated_EF_pullback': True}

# Full rational curvature check, in the local static chart, w=cos(theta).
# The change is dT=d(tau)+i H/(1+H) dr; both metrics have no T dependence.
R2 = PolynomialRing(K,names=('tt','rr','ww','pp','mm'))
tt,rr,ww,pp,mm=R2.gens()
F2=R2.fraction_field()
coords=[tt,rr,ww,pp]
ff=1+2*mm/rr
gS_static=diagonal_matrix(F2,[ff,1/ff,rr**2/(1-ww**2),rr**2*(1-ww**2)])

def ricci_and_scalar(g):
    gi=g.inverse()
    C={}
    for a0 in range(4):
        for b0 in range(4):
            for c0 in range(4):
                v0=sum((gi[a0,d0]*(g[d0,c0].derivative(coords[b0])
                        +g[d0,b0].derivative(coords[c0])-g[b0,c0].derivative(coords[d0]))
                        for d0 in range(4)),F2(0))/2
                if v0:C[a0,b0,c0]=v0
    def gam(a0,b0,c0):return C.get((a0,b0,c0),F2(0))
    Rc=matrix(F2,4,4,lambda b0,c0:
        sum((gam(a0,b0,c0).derivative(coords[a0])
             -gam(a0,b0,a0).derivative(coords[c0])
             +sum((gam(a0,a0,d0)*gam(d0,b0,c0)
                   -gam(a0,c0,d0)*gam(d0,b0,a0) for d0 in range(4)),F2(0))
             for a0 in range(4)),F2(0)))
    scalar=sum((gi[a0,b0]*Rc[a0,b0] for a0 in range(4) for b0 in range(4)),F2(0))
    return Rc,scalar

ricS,scS=ricci_and_scalar(gS_static)
assert ricS.is_zero() and scS==0
ricK,scK=ricci_and_scalar(gS_static/rr**2)
assert scK==-12*mm/rr
results['printed_metric_bridge']={'ell_equals_minus_k_over_sqrt2':True,
    'gS_Ricci_zero':True,'gK_scalar_direct':str(scK)}
print('RESULT ' + json.dumps(results,ensure_ascii=False),flush=True)
print('MEMORY_PEAK '+Path('/sys/fs/cgroup/memory.peak').read_text().strip(),flush=True)

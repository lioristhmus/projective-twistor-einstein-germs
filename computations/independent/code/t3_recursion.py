"""Audit job T3: exact low-order checks of the Appendix A/B record recursion beyond Kasner.

Independent implementation (shares no code with candidate 0.1.0). Exact rational arithmetic
(gmpy2.mpq if present, else fractions.Fraction). Run only inside the isolated container.

Representation. T in Sym^n S* (x) Sym^m S'* is its generating polynomial T(z,w); key (a,b) holds
the coefficient of z0^(n-a) z1^a w0^(m-b) w1^b.  A V* slot index s=2A+A' means evaluation on the
basis vector e_{AA'}, where eta(e_{AA'},e_{BB'}) = eps_{AB} eps_{A'B'}.
  i_a T          = d_A d_A' T / (deg_z T * deg_w T)                (a = e_{AA'})
  (J Q)(a,b)     = i_b Q_a ;  delta = (1 - tau) J ;  (J* Y)_a = z^B w^B' Y_{a,BB'}
  P_+ (unprimed) Y_{AA'} = d_A (z^B Y_{BA'}) / (n+1) ; same for the primed factor
  M_r            = n/(n+1) P_{-+} + m/(m+1) P_{+-} + nm/(nm-1) P_{--}     (first sign = unprimed)
  R_U(a,b)c      = W_U(a,b)c + (Lambda/3){a eta(b,c) - b eta(a,c)},
  eta(W_U(a,b)c,d) = -Psi+_{ABCD} eps_{A'B'} eps_{C'D'} - Psi-_{A'B'C'D'} eps_{AB} eps_{CD},  Psi = U_0
  V_B T          = beta^D_C z^C d_D T + beta'^D'_C' w^C' d_D' T,  B = beta(x)1 + 1(x)beta'
  K_r(a,b)       = V_{R_U(a,b)} U_{r-1}
  HQ_{r-1}(a,b)  = sum_j D_{U_j} Q_{r-1,b} [ i_a U_{j+1} + Q_{j,a} ]   (both chiralities of U_j)
  Q_r            = M_r J_r^* ( tau HQ_{r-1} - K_r ),  Q_0 = 0.
Checks (all exact):
  SPENCER   M_r J_r^* delta_r = 1 - P_{++} and delta_r P_{++} = 0 on all of V*(x)W_r, r <= 5.
  C0        R_U is an algebraic curvature tensor with Ric = Lambda eta; readout inverts it.
  C1        delta_r Q_r = -K_r - (1-tau) HQ_{r-1}  and  J_r^* HQ_{r-1} = 0  as POLYNOMIAL identities
            in independent symbolic U_0..U_2 of both chiralities and symbolic Lambda, r <= 3.
  NC        negative controls (deliberately wrong conventions) must break C1.
  GEO       exact jets of explicit holomorphic Einstein metrics: Q_0 = 0, the geometric Ricci
            identity, and geometric Q_r = polynomial Q_r evaluated on the geometric records.
"""
import argparse
import itertools as it
import json
import math
import sys
import time

import preflight

preflight.check()
try:
    from gmpy2 import mpq as QN
except ImportError:  # pragma: no cover
    from fractions import Fraction as QN

T0 = time.time()


def out(tag, obj):
    print(tag + ' ' + json.dumps(obj, default=str), flush=True)


ONE = QN(1)
EPS_LO = [[0, 1], [-1, 0]]   # eps_{AB}
EPS_UP = [[0, -1], [1, 0]]   # eps^{AB}
ETA = [[EPS_LO[s // 2][t // 2] * EPS_LO[s % 2][t % 2] for t in range(4)] for s in range(4)]
ETAI = [[EPS_UP[s // 2][t // 2] * EPS_UP[s % 2][t % 2] for t in range(4)] for s in range(4)]
assert all(sum(ETA[a][b] * ETAI[b][c] for b in range(4)) == (a == c) for a in range(4) for c in range(4))

# ------------------------------------------------------------------ sparse polynomials over Q
def padd(acc, p, c=1):
    for mo, v in p.items():
        w = acc.get(mo, 0) + c * v
        if w:
            acc[mo] = w
        else:
            acc.pop(mo, None)
    return acc


def pmul(p, q):
    res = {}
    for m1, a in p.items():
        for m2, b in q.items():
            mo = tuple(sorted(m1 + m2))
            w = res.get(mo, 0) + a * b
            if w:
                res[mo] = w
            else:
                res.pop(mo, None)
    return res


def pscale(p, c):
    return {m: v * c for m, v in p.items()} if c else {}


def pderiv(p, var):
    res = {}
    for mo, val in p.items():
        k = mo.count(var)
        if k:
            lst = list(mo)
            lst.remove(var)
            t = tuple(lst)
            w = res.get(t, 0) + k * val
            if w:
                res[t] = w
            else:
                res.pop(t, None)
    return res


def peval(p, vals):
    tot = QN(0)
    for mo, c in p.items():
        term = c
        for v in mo:
            term = term * vals[v]
        tot += term
    return tot


def const(c):
    return {(): QN(c)} if c else {}


# ------------------------------------------------------------- spinor polynomials W(n,m)
class SP:
    __slots__ = ('n', 'm', 'c')

    def __init__(self, n, m, c=None):
        self.n, self.m, self.c = n, m, (c if c is not None else {})

    def iszero(self):
        return all(not p for p in self.c.values())


def sp_add(X, Y, c=1):
    assert (X.n, X.m) == (Y.n, Y.m)
    for k, p in Y.c.items():
        padd(X.c.setdefault(k, {}), p, c)
    return X


def sp_copy(X, c=1):
    return SP(X.n, X.m, {k: pscale(p, c) for k, p in X.c.items()})


def sp_lin(terms, n, m):
    R = SP(n, m)
    for c, X in terms:
        if c:
            sp_add(R, X, c)
    return R


def sp_polymul(X, p):
    return SP(X.n, X.m, {k: pmul(v, p) for k, v in X.c.items() if v})


def dz(T, A):
    R = SP(T.n - 1, T.m)
    for (a, b), p in T.c.items():
        if not p:
            continue
        if A == 0 and a <= T.n - 1:
            padd(R.c.setdefault((a, b), {}), p, T.n - a)
        elif A == 1 and a >= 1:
            padd(R.c.setdefault((a - 1, b), {}), p, a)
    return R


def dw(T, A):
    R = SP(T.n, T.m - 1)
    for (a, b), p in T.c.items():
        if not p:
            continue
        if A == 0 and b <= T.m - 1:
            padd(R.c.setdefault((a, b), {}), p, T.m - b)
        elif A == 1 and b >= 1:
            padd(R.c.setdefault((a, b - 1), {}), p, b)
    return R


def mz(T, A):
    return SP(T.n + 1, T.m, {((a + A), b): dict(p) for (a, b), p in T.c.items() if p})


def mw(T, A):
    return SP(T.n, T.m + 1, {(a, (b + A)): dict(p) for (a, b), p in T.c.items() if p})


def i_vec(T, s):
    """i_a T for a = e_{AA'}, s = 2A+A'."""
    R = dw(dz(T, s // 2), s % 2)
    return sp_copy(R, QN(1, T.n * T.m))


def deg(ch, r):
    return (r + 4, r) if ch == '+' else (r, r + 4)


# ------------------------------------------------------------- operators on V* (x) W
def Jstar(Y2, n, m):
    """(J* Y)_a = z^B w^B' Y_{a,BB'}; Y2 maps (a,b) -> SP(n-1, m-1); returns a -> SP(n,m)."""
    return {a: sp_lin([(1, mw(mz(Y2[(a, b)], b // 2), b % 2)) for b in range(4)], n, m) for a in range(4)}


def delta(Q):
    n, m = Q[0].n, Q[0].m
    JQ = {(a, b): i_vec(Q[a], b) for a in range(4) for b in range(4)}
    return {(a, b): sp_lin([(1, JQ[(a, b)]), (-1, JQ[(b, a)])], n - 1, m - 1) for a in range(4) for b in range(4)}


def P_u(Y):
    n, m = Y[0].n, Y[0].m
    res = {}
    for Ap in range(2):
        g = sp_lin([(1, mz(Y[2 * A + Ap], A)) for A in range(2)], n + 1, m)
        for A in range(2):
            res[2 * A + Ap] = sp_copy(dz(g, A), QN(1, n + 1))
    return res


def P_w(Y):
    n, m = Y[0].n, Y[0].m
    res = {}
    for A in range(2):
        h = sp_lin([(1, mw(Y[2 * A + Ap], Ap)) for Ap in range(2)], n, m + 1)
        for Ap in range(2):
            res[2 * A + Ap] = sp_copy(dw(h, Ap), QN(1, m + 1))
    return res


def tsub(X, Y):
    return {k: sp_lin([(1, X[k]), (-1, Y[k])], X[k].n, X[k].m) for k in X}


def projections(Y):
    Yu = P_u(Y)
    Yl = tsub(Y, Yu)
    Ppp = P_w(Yu)
    Pmp = P_w(Yl)
    Ppm = tsub(Yu, Ppp)
    Pmm = tsub(Yl, Pmp)
    return Ppp, Pmp, Ppm, Pmm


def Mop(Y, coeffs=None):
    n, m = Y[0].n, Y[0].m
    Ppp, Pmp, Ppm, Pmm = projections(Y)
    cmp_, cpm, cmm = coeffs(n, m) if coeffs else (QN(n, n + 1), QN(m, m + 1), QN(n * m, n * m - 1))
    return {a: sp_lin([(cmp_, Pmp[a]), (cpm, Ppm[a]), (cmm, Pmm[a])], n, m) for a in range(4)}


def all_zero(T):
    return all(X.iszero() for X in T.values())


# ================================================================ SPENCER (linear algebra)
def spencer_checks(rmax=5):
    rows = []
    for r in range(1, rmax + 1):
        for ch in '+-':
            n, m = deg(ch, r)
            ok = True
            nb = 0
            for a0 in range(4):
                for key in it.product(range(n + 1), range(m + 1)):
                    X = {a: SP(n, m) for a in range(4)}
                    X[a0].c[key] = const(1)
                    D = delta(X)
                    back = Mop(Jstar(D, n, m))
                    Ppp = projections(X)[0]
                    ok &= all_zero(tsub(back, tsub(X, Ppp)))
                    ok &= all_zero(delta(Ppp))
                    nb += 1
            rows.append({'r': r, 'chirality': ch, 'basis_elements': nb, 'MJ*delta=1-P++ and delta P++=0': ok})
            assert ok, (r, ch)
    return rows


# ================================================================ symbolic inputs and R_U
class Inputs:
    def __init__(self, jmax):
        self.names = []
        self.vid = {}
        self.U = {}
        for ch in '+-':
            for j in range(jmax + 1):
                n, m = deg(ch, j)
                T = SP(n, m)
                for key in it.product(range(n + 1), range(m + 1)):
                    v = len(self.names)
                    self.names.append('U%s%d_%d%d' % (ch, j, key[0], key[1]))
                    self.vid[(ch, j, key)] = v
                    T.c[key] = {(v,): ONE}
                self.U[(ch, j)] = T
        self.lam = len(self.names)
        self.names.append('Lambda')

    def chir(self, v):
        nm = self.names[v]
        return nm[1] if nm.startswith('U') else 'L'


def psi_component(U0, ch, idx):
    k = sum(idx)
    if ch == '+':
        p = U0.c.get((k, 0), {})
    else:
        p = U0.c.get((0, k), {})
    return pscale(p, QN(1, math.comb(4, k)))


def curvature_operator(Up0, Um0, lam_poly, lam_coeff=QN(1, 3), sign=1):
    """Rm[(a,b)][X][c] = component X of R_U(e_a,e_b) e_c (polynomials)."""
    W = {}
    for a, b, c, d in it.product(range(4), repeat=4):
        A, Ap, B, Bp, C, Cp, D, Dp = a // 2, a % 2, b // 2, b % 2, c // 2, c % 2, d // 2, d % 2
        p = {}
        e1 = EPS_LO[Ap][Bp] * EPS_LO[Cp][Dp]
        if e1:
            padd(p, psi_component(Up0, '+', (A, B, C, D)), -e1)
        e2 = EPS_LO[A][B] * EPS_LO[C][D]
        if e2:
            padd(p, psi_component(Um0, '-', (Ap, Bp, Cp, Dp)), -e2)
        if p:
            W[(a, b, c, d)] = p
    Rm = {}
    for a in range(4):
        for b in range(4):
            M = [[{} for _ in range(4)] for _ in range(4)]
            for X in range(4):
                for c in range(4):
                    acc = {}
                    for e in range(4):
                        if ETAI[e][X] and (a, b, c, e) in W:
                            padd(acc, W[(a, b, c, e)], ETAI[e][X])
                    lc = (X == a) * ETA[b][c] - (X == b) * ETA[a][c]
                    if lc:
                        padd(acc, lam_poly, lam_coeff * lc)
                    M[X][c] = pscale(acc, sign) if sign != 1 else acc
            Rm[(a, b)] = M
    return W, Rm


def split_beta(Rm):
    """B = beta (x) 1 + 1 (x) beta'; returns beta[(a,b)][X][Y], betap[(a,b)][X'][Y'] and checks."""
    beta, betap = {}, {}
    for key, M in Rm.items():
        b1 = [[pscale(padd(dict(M[2 * X][2 * Y]), M[2 * X + 1][2 * Y + 1]), QN(1, 2)) for Y in range(2)] for X in range(2)]
        b2 = [[pscale(padd(dict(M[X][Y]), M[2 + X][2 + Y]), QN(1, 2)) for Y in range(2)] for X in range(2)]
        for s, t in it.product(range(4), repeat=2):
            rebuilt = {}
            if s % 2 == t % 2:
                padd(rebuilt, b1[s // 2][t // 2])
            if s // 2 == t // 2:
                padd(rebuilt, b2[s % 2][t % 2])
            assert not padd(dict(M[s][t]), rebuilt, -1), 'R_U(a,b) is not beta(x)1 + 1(x)beta\''
        beta[key], betap[key] = b1, b2
    return beta, betap


def V_action(beta, betap, T):
    R = SP(T.n, T.m)
    for D, C in it.product(range(2), repeat=2):
        if beta[D][C] and T.n:
            sp_add(R, sp_polymul(mz(dz(T, D), C), beta[D][C]))
        if betap[D][C] and T.m:
            sp_add(R, sp_polymul(mw(dw(T, D), C), betap[D][C]))
    return R


def algebraic_checks(inp):
    W, Rm = curvature_operator(inp.U[('+', 0)], inp.U[('-', 0)], {(inp.lam,): ONE})
    res = {}
    # lowered R_abcd = eta(R(a,b)c, d)
    Rl = {}
    for a, b, c, d in it.product(range(4), repeat=4):
        acc = {}
        for X in range(4):
            if ETA[X][d]:
                padd(acc, Rm[(a, b)][X][c], ETA[X][d])
        Rl[(a, b, c, d)] = acc
    z = lambda p: not p
    res['antisymmetric_ab'] = all(z(padd(dict(Rl[(a, b, c, d)]), Rl[(b, a, c, d)])) for a, b, c, d in it.product(range(4), repeat=4))
    res['eta_skew_cd'] = all(z(padd(dict(Rl[(a, b, c, d)]), Rl[(a, b, d, c)])) for a, b, c, d in it.product(range(4), repeat=4))
    res['first_bianchi'] = all(z(padd(padd(dict(Rl[(a, b, c, d)]), Rl[(b, c, a, d)]), Rl[(c, a, b, d)]))
                               for a, b, c, d in it.product(range(4), repeat=4))
    ric_ok = True
    for b, c in it.product(range(4), repeat=2):
        acc = {}
        for a in range(4):
            padd(acc, Rm[(a, b)][a][c])
        padd(acc, {(inp.lam,): ONE}, -ETA[b][c])
        ric_ok &= not acc
    res['Ric_U = Lambda eta'] = ric_ok
    # readout (eq:gg-weyl-spinor-readout) applied to W recovers U_0
    ro = True
    for A, B, C, D in it.product(range(2), repeat=4):
        acc = {}
        for Ap, Bp, Cp, Dp in it.product(range(2), repeat=4):
            e = EPS_UP[Ap][Bp] * EPS_UP[Cp][Dp]
            if e and (2 * A + Ap, 2 * B + Bp, 2 * C + Cp, 2 * D + Dp) in W:
                padd(acc, W[(2 * A + Ap, 2 * B + Bp, 2 * C + Cp, 2 * D + Dp)], QN(-e, 4))
        ro &= not padd(acc, psi_component(inp.U[('+', 0)], '+', (A, B, C, D)), -1)
        acc = {}  # here A,B,C,D play the primed indices; Ap..Dp are the summed unprimed ones
        for Ap, Bp, Cp, Dp in it.product(range(2), repeat=4):
            e = EPS_UP[Ap][Bp] * EPS_UP[Cp][Dp]
            if e and (2 * Ap + A, 2 * Bp + B, 2 * Cp + C, 2 * Dp + D) in W:
                padd(acc, W[(2 * Ap + A, 2 * Bp + B, 2 * Cp + C, 2 * Dp + D)], QN(-e, 4))
        ro &= not padd(acc, psi_component(inp.U[('-', 0)], '-', (A, B, C, D)), -1)
    res['readout_inverts_decomposition'] = ro
    split_beta(Rm)
    res['so(4) = sl(S)+sl(S\') split exact'] = True
    assert all(res.values()), res
    return res


# ================================================================ the recursion itself
def run_recursion(inp, rmax, lam_coeff=QN(1, 3), sign=1, mcoeffs=None, check=True, label='main'):
    _, Rm = curvature_operator(inp.U[('+', 0)], inp.U[('-', 0)], {(inp.lam,): ONE}, lam_coeff, sign)
    beta, betap = split_beta(Rm)
    Q = {}
    for ch in '+-':
        n, m = deg(ch, 0)
        Q[(ch, 0)] = {a: SP(n, m) for a in range(4)}
    rows = []
    for r in range(1, rmax + 1):
        for ch in '+-':
            n, m = deg(ch, r)
            Uprev = inp.U[(ch, r - 1)]
            K = {(a, b): V_action(beta[(a, b)], betap[(a, b)], Uprev) for a in range(4) for b in range(4)}
            HQ = {(a, b): SP(n - 1, m - 1) for a in range(4) for b in range(4)}
            Qold = Q[(ch, r - 1)]
            for j in range(0, r - 1):
                for c2 in '+-':
                    Uj = inp.U[(c2, j)]
                    for a in range(4):
                        Vdir = sp_lin([(1, i_vec(inp.U[(c2, j + 1)], a)), (1, Q[(c2, j)][a])], Uj.n, Uj.m)
                        for b in range(4):
                            tgt = HQ[(a, b)]
                            for key, p in Qold[b].c.items():
                                if not p:
                                    continue
                                acc = tgt.c.setdefault(key, {})
                                for ukey in Uj.c:
                                    dp = pderiv(p, inp.vid[(c2, j, ukey)])
                                    if dp and Vdir.c.get(ukey):
                                        padd(acc, pmul(dp, Vdir.c[ukey]))
            X = {(a, b): sp_lin([(1, HQ[(b, a)]), (-1, K[(a, b)])], n - 1, m - 1) for a in range(4) for b in range(4)}
            Qr = Mop(Jstar(X, n, m), mcoeffs)
            Q[(ch, r)] = Qr
            row = {'label': label, 'r': r, 'chirality': ch, 'components': 4 * (n + 1) * (m + 1)}
            if check:
                D = delta(Qr)
                RHS = {(a, b): sp_lin([(-1, K[(a, b)]), (-1, HQ[(a, b)]), (1, HQ[(b, a)])], n - 1, m - 1)
                       for a in range(4) for b in range(4)}
                resid = tsub(D, RHS)
                nz = sum(1 for T in resid.values() for p in T.c.values() if p)
                row['delta Q - RHS nonzero coefficient polys'] = nz
                js = Jstar(HQ, n, m)
                row['J* HQ nonzero coefficient polys'] = sum(1 for T in js.values() for p in T.c.values() if p)
                row['P++ Q zero (tautological)'] = all_zero(projections(Qr)[0])
                mons = [mo for T in Qr.values() for p in T.c.values() for mo in p]
                row['monomials_in_Q'] = len(mons)
                row['mixed_chirality_monomials_in_Q'] = sum(1 for mo in mons if {'+', '-'} <= {inp.chir(v) for v in mo})
                row['Lambda_monomials_in_Q'] = sum(1 for mo in mons if inp.lam in mo)
                row['max_degree_in_Q'] = max((len(mo) for mo in mons), default=0)
                row['HQ_nonzero'] = not all_zero(HQ)
            rows.append(row)
            out('ROW', row)
    return Q, rows


# ================================================================ jets for the witnesses
class Jet:
    __slots__ = ('o', 'c')

    def __init__(self, o, c=None):
        self.o, self.c = o, (c if c is not None else {})


NV = 4


def jconst(x, o):
    return Jet(o, {(0,) * NV: QN(x)} if x else {})


def jvar(i, o):
    e = [0] * NV
    e[i] = 1
    return Jet(o, {tuple(e): ONE})


def jadd(a, b, cb=1):
    o = min(a.o, b.o)
    c = {k: v for k, v in a.c.items() if sum(k) <= o}
    for k, v in b.c.items():
        if sum(k) <= o:
            w = c.get(k, 0) + cb * v
            if w:
                c[k] = w
            else:
                c.pop(k, None)
    return Jet(o, c)


def jscale(a, s):
    return Jet(a.o, {k: v * s for k, v in a.c.items()} if s else {})


def jmul(a, b):
    o = min(a.o, b.o)
    c = {}
    for k1, v1 in a.c.items():
        d1 = sum(k1)
        if d1 > o:
            continue
        for k2, v2 in b.c.items():
            if d1 + sum(k2) > o:
                continue
            k = tuple(x + y for x, y in zip(k1, k2))
            w = c.get(k, 0) + v1 * v2
            if w:
                c[k] = w
            else:
                c.pop(k, None)
    return Jet(o, c)


def jder(a, i):
    c = {}
    for k, v in a.c.items():
        if k[i]:
            kk = list(k)
            kk[i] -= 1
            c[tuple(kk)] = v * k[i]
    return Jet(a.o - 1, c)


def jc0(a):
    return a.c.get((0,) * NV, QN(0))


def jinv(a):
    c0 = jc0(a)
    assert c0 != 0
    h = jadd(a, jconst(c0, a.o), -1)
    term = jconst(QN(1) / c0, a.o)
    acc = jconst(QN(1) / c0, a.o)
    for _ in range(a.o):
        term = jscale(jmul(term, h), -QN(1) / c0)
        acc = jadd(acc, term)
    return acc


def jpow1p(x, alpha, o):
    """(1 + x)^alpha for a jet x without constant term, alpha rational."""
    acc = jconst(1, o)
    term = jconst(1, o)
    coef = QN(1)
    for k in range(1, o + 1):
        coef = coef * (QN(alpha) - (k - 1)) / k
        term = jmul(term, x)
        acc = jadd(acc, jscale(term, coef))
    return acc


def mat_inv_exact(M):
    n = len(M)
    A = [[QN(M[i][j]) for j in range(n)] + [QN(int(i == j)) for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = next(i for i in range(col, n) if A[i][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [x / pv for x in A[col]]
        for i in range(n):
            if i != col and A[i][col] != 0:
                f = A[i][col]
                A[i] = [x - f * y for x, y in zip(A[i], A[col])]
    return [row[n:] for row in A]


def geometry(gj, frame, kmax, label):
    """gj: 4x4 metric jets; frame: E[s] coordinate vectors at the point; returns frame data."""
    N = gj[0][0].o
    g0 = [[jc0(gj[i][j]) for j in range(4)] for i in range(4)]
    g0i = mat_inv_exact(g0)
    h = [[jadd(gj[i][j], jconst(g0[i][j], N), -1) for j in range(4)] for i in range(4)]
    term = [[jconst(g0i[i][j], N) for j in range(4)] for i in range(4)]
    gi = [[term[i][j] for j in range(4)] for i in range(4)]
    for _ in range(N):
        prod = [[Jet(N) for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                acc = Jet(N)
                for k in range(4):
                    for l in range(4):
                        if g0i[i][k] and h[k][l].c and term[l][j].c:
                            acc = jadd(acc, jscale(jmul(h[k][l], term[l][j]), -g0i[i][k]))
                prod[i][j] = acc
        term = prod
        gi = [[jadd(gi[i][j], term[i][j]) for j in range(4)] for i in range(4)]
    # frame check
    for s in range(4):
        for t in range(4):
            val = sum(g0[i][j] * frame[s][i] * frame[t][j] for i in range(4) for j in range(4))
            assert val == ETA[s][t], (label, s, t, val)
    dg = [[[jder(gj[i][j], k) for k in range(4)] for j in range(4)] for i in range(4)]
    Gam = [[[None] * 4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(b, 4):
                acc = Jet(N - 1)
                for d in range(4):
                    t3 = jadd(jadd(dg[d][c][b], dg[d][b][c]), dg[b][c][d], -1)
                    if t3.c and gi[a][d].c:
                        acc = jadd(acc, jmul(gi[a][d], t3))
                Gam[a][b][c] = Gam[a][c][b] = jscale(acc, QN(1, 2))
    Rup = {}
    for e, c, a, b in it.product(range(4), repeat=4):
        acc = jadd(jder(Gam[e][b][c], a), jder(Gam[e][a][c], b), -1)
        for f in range(4):
            acc = jadd(acc, jmul(Gam[e][a][f], Gam[f][b][c]))
            acc = jadd(acc, jmul(Gam[e][b][f], Gam[f][a][c]), -1)
        Rup[(e, c, a, b)] = acc
    Rl = {}
    for a, b, c, d in it.product(range(4), repeat=4):
        acc = Jet(N - 2)
        for e in range(4):
            acc = jadd(acc, jmul(gj[d][e], Rup[(e, c, a, b)]))
        Rl[(a, b, c, d)] = acc
    Ric = [[None] * 4 for _ in range(4)]
    for b in range(4):
        for c in range(4):
            acc = Jet(N - 2)
            for a in range(4):
                acc = jadd(acc, Rup[(a, c, a, b)])
            Ric[b][c] = acc
    Scal = Jet(N - 2)
    for b in range(4):
        for c in range(4):
            Scal = jadd(Scal, jmul(gi[b][c], Ric[b][c]))
    lam = jc0(Scal) / 4
    einstein_resid = sum(len(jadd(Ric[b][c], jscale(gj[b][c], lam), -1).c) for b in range(4) for c in range(4))
    P = [[jscale(jadd(Ric[a][b], jscale(jmul(Scal, gj[a][b]), QN(1, 6)), -1), QN(1, 2)) for b in range(4)] for a in range(4)]
    C = {}
    for a, b, c, d in it.product(range(4), repeat=4):
        acc = Rl[(a, b, c, d)]
        acc = jadd(acc, jmul(gj[a][d], P[b][c]), -1)
        acc = jadd(acc, jmul(gj[b][d], P[a][c]))
        acc = jadd(acc, jmul(gj[a][c], P[b][d]))
        acc = jadd(acc, jmul(gj[b][c], P[a][d]), -1)
        if acc.c:
            C[(a, b, c, d)] = acc
    # covariant derivatives, new index first (outermost)
    levels = [C]
    cur = C
    for k in range(1, kmax + 1):
        o = N - 2 - k
        nxt = {}
        keys = list(cur.keys())
        for a in range(4):
            for I in it.product(range(4), repeat=k + 3):
                acc = Jet(o)
                T = cur.get(I)
                if T is not None:
                    acc = jadd(acc, jder(T, a))
                for jpos, ij in enumerate(I):
                    for e in range(4):
                        G = Gam[e][a][ij]
                        if not G.c:
                            continue
                        J = I[:jpos] + (e,) + I[jpos + 1:]
                        T2 = cur.get(J)
                        if T2 is not None:
                            acc = jadd(acc, jmul(G, T2), -1)
                if acc.c:
                    nxt[(a,) + I] = Jet(o, {kk: v for kk, v in acc.c.items() if sum(kk) <= o})
        levels.append(nxt)
        cur = nxt
    # frame components (constants only)
    frames = []
    for k, T in enumerate(levels):
        rank = k + 4
        dense = {I: jc0(J) for I, J in T.items() if jc0(J) != 0}
        for ax in range(rank):
            new = {}
            for I, v in dense.items():
                mu = I[ax]
                for s in range(4):
                    fs = frame[s][mu]
                    if fs:
                        J = I[:ax] + (s,) + I[ax + 1:]
                        w = new.get(J, 0) + v * fs
                        if w:
                            new[J] = w
                        else:
                            new.pop(J, None)
            dense = new
        frames.append(dense)
    # Riemann in the frame (for the geometric Ricci identity)
    Rf = {}
    R0 = {I: jc0(J) for I, J in Rl.items() if jc0(J) != 0}
    for ax in range(4):
        new = {}
        for I, v in R0.items():
            for s in range(4):
                fs = frame[s][I[ax]]
                if fs:
                    J = I[:ax] + (s,) + I[ax + 1:]
                    new[J] = new.get(J, 0) + v * fs
        R0 = {k_: v for k_, v in new.items() if v}
    return {'lambda': lam, 'einstein_residual_terms': einstein_resid, 'frames': frames, 'riemann_frame': R0,
            'scal_derivative_terms': sum(len(jder(Scal, i).c) for i in range(4))}


def records_from_frames(frames, kmax):
    """U[(ch,j)] (j<=kmax) and DU[(ch,j)][a] = nabla_a U_j (j<=kmax-1), DDU[(ch,j)][(a,b)] (j<=kmax-2)."""
    U, DU, DDU = {}, {}, {}
    for k, T in enumerate(frames):
        for ch in '+-':
            for fixed in range(0, min(k, 2) + 1):
                j = k - fixed
                n, m = deg(ch, j)
                acc = {}
                for I, v in T.items():
                    ds, cv = I[:k], I[k:]
                    if ch == '+':
                        e = EPS_UP[cv[0] % 2][cv[1] % 2] * EPS_UP[cv[2] % 2][cv[3] % 2]
                        if not e:
                            continue
                        ua = sum(x // 2 for x in ds[fixed:]) + sum(x // 2 for x in cv)
                        wb = sum(x % 2 for x in ds[fixed:])
                    else:
                        e = EPS_UP[cv[0] // 2][cv[1] // 2] * EPS_UP[cv[2] // 2][cv[3] // 2]
                        if not e:
                            continue
                        ua = sum(x // 2 for x in ds[fixed:])
                        wb = sum(x % 2 for x in ds[fixed:]) + sum(x % 2 for x in cv)
                    key = (ds[:fixed], (ua, wb))
                    acc[key] = acc.get(key, 0) + v * QN(-e, 4)
                spm = {}
                for (pre, kk), v in acc.items():
                    if v:
                        spm.setdefault(pre, SP(n, m)).c[kk] = const(v)
                if fixed == 0:
                    U[(ch, j)] = spm.get((), SP(n, m))
                elif fixed == 1:
                    DU[(ch, j)] = {a: spm.get((a,), SP(n, m)) for a in range(4)}
                else:
                    DDU[(ch, j)] = {(a, b): spm.get((a, b), SP(n, m)) for a in range(4) for b in range(4)}
    return U, DU, DDU


def sp_const_equal(X, Y):
    keys = set(X.c) | set(Y.c)
    return all(peval(X.c.get(k, {}), {}) == peval(Y.c.get(k, {}), {}) for k in keys)


def witness(label, gj, frame, kmax, Qsym, inp, rmax, expect_einstein=True, extras=None):
    t1 = time.time()
    geo = geometry(gj, frame, kmax, label)
    U, DU, DDU = records_from_frames(geo['frames'], kmax)
    lam = geo['lambda']
    rep = {'witness': label, 'Lambda': str(lam), 'einstein_residual_terms': geo['einstein_residual_terms'],
           'U0_plus_nonzero': not U[('+', 0)].iszero(), 'U0_minus_nonzero': not U[('-', 0)].iszero()}
    # geometric Q_j = nabla U_j - i U_{j+1}
    Qg = {}
    for ch in '+-':
        for j in range(kmax):
            Qg[(ch, j)] = {a: sp_lin([(1, DU[(ch, j)][a]), (-1, i_vec(U[(ch, j + 1)], a))], *deg(ch, j)) for a in range(4)}
    rep['Q0_zero(Bianchi)'] = {ch: all_zero(Qg[(ch, 0)]) for ch in '+-'}
    # geometric Ricci identity with the full Riemann tensor (holds on ANY metric)
    Rm = {}
    for a in range(4):
        for b in range(4):
            M = [[{} for _ in range(4)] for _ in range(4)]
            for X in range(4):
                for c in range(4):
                    v = sum(geo['riemann_frame'].get((a, b, c, e), 0) * ETAI[e][X] for e in range(4))
                    M[X][c] = const(v)
            Rm[(a, b)] = M
    beta, betap = split_beta(Rm)
    ricci_id = {}
    for r in range(1, kmax):
        for ch in '+-':
            n, m = deg(ch, r)
            K = {(a, b): V_action(beta[(a, b)], betap[(a, b)], U[(ch, r - 1)]) for a in range(4) for b in range(4)}
            HQg = {(a, b): sp_lin([(1, DDU[(ch, r - 1)][(a, b)]), (-1, i_vec(DU[(ch, r)][a], b))], n - 1, m - 1)
                   for a in range(4) for b in range(4)}
            RHS = {(a, b): sp_lin([(-1, K[(a, b)]), (-1, HQg[(a, b)]), (1, HQg[(b, a)])], n - 1, m - 1)
                   for a in range(4) for b in range(4)}
            D = delta(Qg[(ch, r)])
            ricci_id['r%d%s' % (r, ch)] = all(sp_const_equal(D[k], RHS[k]) for k in D)
    rep['geometric_ricci_identity(any metric)'] = ricci_id
    # polynomial recursion evaluated on the geometric records
    vals = {inp.lam: lam}
    for (ch, j, key), v in inp.vid.items():
        if j <= kmax:
            vals[v] = peval(U[(ch, j)].c.get(key, {}), {})
    cmp_rows = {}
    for r in range(1, rmax + 1):
        for ch in '+-':
            mism = 0
            mixed_nonzero = False
            tot = 0
            for a in range(4):
                Pq = Qsym[(ch, r)][a]
                G = Qg[(ch, r)][a]
                for key in set(Pq.c) | set(G.c):
                    p = Pq.c.get(key, {})
                    pv = peval(p, vals)
                    gv = peval(G.c.get(key, {}), {})
                    tot += 1
                    mism += (pv != gv)
                    mixed = {mo: c for mo, c in p.items() if {'+', '-'} <= {inp.chir(v) for v in mo}}
                    if mixed and peval(mixed, vals) != 0:
                        mixed_nonzero = True
            cmp_rows['r%d%s' % (r, ch)] = {'compared': tot, 'mismatches': mism, 'mixed_terms_nonzero_here': mixed_nonzero}
    rep['poly_Q_vs_geometric_Q'] = cmp_rows
    # deliberately wrong conventions evaluated on the same geometric records (no assertion here)
    nc = {}
    for name, Qx in (extras or {}).items():
        mm = {}
        for r in range(1, rmax + 1):
            for ch in '+-':
                bad = 0
                for a in range(4):
                    P_, G_ = Qx[(ch, r)][a], Qg[(ch, r)][a]
                    for key in set(P_.c) | set(G_.c):
                        bad += peval(P_.c.get(key, {}), vals) != peval(G_.c.get(key, {}), {})
                mm['r%d%s' % (r, ch)] = bad
        nc[name] = mm
    rep['wrong_convention_mismatches'] = nc
    rep['seconds'] = round(time.time() - t1, 1)
    out('WITNESS', rep)
    if expect_einstein:
        assert geo['einstein_residual_terms'] == 0
        assert all(rep['Q0_zero(Bianchi)'].values())
        assert all(v['mismatches'] == 0 for v in cmp_rows.values())
    assert all(ricci_id.values())
    return rep


def metric_kasner(ps, N, signs=(1, -1, 1, -1)):
    d = jvar(0, N)
    diag = [jconst(1, N)] + [jscale(jpow1p(d, 2 * QN(p), N), signs[i + 1]) for i, p in enumerate(ps)]
    gj = [[diag[i] if i == j else Jet(N) for j in range(4)] for i in range(4)]
    frame = [[1, 0, 0, 1], [0, 1, 1, 0], [0, QN(1, 2), QN(-1, 2), 0], [QN(1, 2), 0, 0, QN(-1, 2)]]
    return gj, frame


def metric_two_wave(t, s, N, point=(1, 2, 1, 0), exact_family=True):
    u0, v0, x0, y0 = map(QN, point)
    U_, V_, X_ = (jadd(jconst(c, N), jvar(i, N)) for i, c in ((0, u0), (1, v0), (2, x0)))
    q = jmul(X_, X_)
    if exact_family:
        w = jadd(U_, jscale(jmul(q, V_), QN(s) / 2))
    else:
        w = U_
    F = jscale(jmul(jmul(w, w), w), QN(t))
    Z = Jet(N)
    gj = [[Z, jconst(1, N), Z, Z], [jconst(1, N), jscale(q, QN(s)), Z, Z], [Z, Z, F, jconst(-1, N)], [Z, Z, jconst(-1, N), Z]]
    F0 = jc0(F)
    q0 = jc0(q)
    frame = [[1, 0, 0, 0], [0, 0, 1, F0 / 2], [0, 0, 0, 1], [-QN(s) * q0 / 2, 1, 0, 0]]
    return gj, frame


def metric_kottler(mass, lam_std, r0, z0, N):
    R_ = jadd(jconst(r0, N), jvar(1, N))
    Zc = jadd(jconst(z0, N), jvar(2, N))
    f = jadd(jadd(jconst(1, N), jscale(jinv(R_), 2 * QN(mass)), -1), jscale(jmul(R_, R_), QN(lam_std) / 3), -1)
    oz = jadd(jconst(1, N), jmul(Zc, Zc), -1)
    r2 = jmul(R_, R_)
    Z = Jet(N)
    gj = [[f, Z, Z, Z], [Z, jscale(jinv(f), -1), Z, Z], [Z, Z, jscale(jmul(r2, jinv(oz)), -1), Z], [Z, Z, Z, jmul(r2, oz)]]
    f0 = jc0(f)
    oz0 = 1 - QN(z0) ** 2
    r0 = QN(r0)
    frame = [[1, f0, 0, 0], [0, 0, 1, 1 / oz0], [0, 0, oz0 / (2 * r0 ** 2), -1 / (2 * r0 ** 2)], [1 / (2 * f0), QN(-1, 2), 0, 0]]
    return gj, frame


# ================================================================ App. B arithmetic identities
def appendix_b_arithmetic(R=40):
    res = {}
    ok = True
    for r in range(1, R + 1):
        for j in range(0, r):
            lhs = sum((t + 1) * math.comb(r - t, j) for t in range(1, r - j + 1))
            ok &= lhs == math.comb(r + 1, j + 2) + math.comb(r, j + 1)
            k = r - 1 - j
            val = QN(lhs) * math.factorial(j) * math.factorial(k) / math.factorial(r)
            ok &= val <= 2 * r
    res['eq:gg-budget-quadratic-sum and <=2r bound, r<=%d' % R] = ok
    mins = []
    for r in range(1, R + 1):
        n, m = r + 4, r
        ev = [2 * (1 + QN(1, n)), 2 * (1 + QN(1, m)), 2 * (1 - QN(1, n * m))]
        mins.append(min(ev))
    res['min nonzero eigenvalue of delta*delta >= 8/5 (r<=%d), attained r=1' % R] = (min(mins) == QN(8, 5) and mins[0] == QN(8, 5))
    res['m(n+1)<=2(m+1)^2 diff r^2-r+2; n(m+1)<=2(n+1)^2 diff r^2+15r+46'] = all(
        2 * (r + 1) ** 2 - r * (r + 5) == r * r - r + 2 and 2 * (r + 5) ** 2 - (r + 4) * (r + 1) == r * r + 15 * r + 46
        for r in range(1, R + 1))
    part = sum(QN(1, r * (r + 3)) for r in range(1, 200))
    res['sum 1/(r(r+3)) partial sums < 11/18 and tail formula'] = part < QN(11, 18) and \
        QN(11, 18) - part == sum(QN(1, 3 * k) for k in range(200, 203))
    assert all(res.values()), res
    return res


# ================================================================ main
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--part', default='all')
    ap.add_argument('--rmax-sym', type=int, default=3)
    ap.add_argument('--rmax-geo', type=int, default=2)
    ap.add_argument('--kasner-rmax-geo', type=int, default=2)
    ap.add_argument('--skip-nc', action='store_true')
    args = ap.parse_args()
    out('START', {'numbers': QN.__module__ if hasattr(QN, '__module__') else str(QN), 'args': vars(args)})
    if args.part in ('all', 'algebra'):
        out('APPB_ARITHMETIC', appendix_b_arithmetic())
        out('SPENCER', spencer_checks(5))
        inp = Inputs(max(2, args.rmax_sym - 1))
        out('C0', algebraic_checks(inp))
        Q, rows = run_recursion(inp, args.rmax_sym)
        bad = [r for r in rows if r['delta Q - RHS nonzero coefficient polys'] or r['J* HQ nonzero coefficient polys']]
        out('C1_SUMMARY', {'rmax': args.rmax_sym, 'all_consistent': not bad, 'seconds': round(time.time() - T0, 1)})
        assert not bad, bad
        # negative controls: each deliberately wrong convention must break consistency
        nc = {}
    if args.part in ('all', 'algebra') and not args.skip_nc:
        _, rr = run_recursion(inp, args.rmax_sym, sign=-1, label='NC1 sign of R_U flipped')
        nc['NC1 sign(R_U)->-1'] = {'%d%s' % (r['r'], r['chirality']): r['delta Q - RHS nonzero coefficient polys'] for r in rr}
        _, rr = run_recursion(inp, 2, mcoeffs=lambda n, m: (QN(n, n + 1), QN(m, m + 1), QN(1)), label='NC2 nm/(nm-1)->1')
        nc['NC2 M_r coefficient nm/(nm-1)->1'] = {'%d%s' % (r['r'], r['chirality']): r['delta Q - RHS nonzero coefficient polys'] for r in rr}
        _, rr = run_recursion(inp, args.rmax_sym, lam_coeff=QN(2, 3), label='NC3 Lambda/3->2Lambda/3')
        nc['NC3 Lambda coefficient 1/3->2/3'] = {'%d%s' % (r['r'], r['chirality']): r['delta Q - RHS nonzero coefficient polys'] for r in rr}
        out('NEGATIVE_CONTROLS', nc)
    if args.part in ('all', 'witness'):
        rg = max(args.rmax_geo, args.kasner_rmax_geo)
        inp = Inputs(rg + 1)
        Qsym, _ = run_recursion(inp, rg, check=False, label='for-witness')
        EXTRAS = {'NC1 sign(R_U)->-1': run_recursion(inp, rg, sign=-1, check=False, label='nc1-witness')[0],
                  'NC3 Lambda/3->2Lambda/3': run_recursion(inp, rg, lam_coeff=QN(2, 3), check=False, label='nc3-witness')[0]}
        kmax = args.rmax_geo + 1
        N = kmax + 2
        reps = []
        gj, fr = metric_kasner(['-2/7', '3/7', '6/7'], args.kasner_rmax_geo + 3)
        reps.append(witness('Kasner(-2/7,3/7,6/7) complexified x2->i x2, t=1', gj, fr, args.kasner_rmax_geo + 1, Qsym, inp, args.kasner_rmax_geo, extras=EXTRAS))
        gj, fr = metric_two_wave(3, 5, N)
        reps.append(witness('two-wave exact family F=t(u+s x^2 v/2)^3, q=x^2, t=3,s=5 at (1,2,1,0)', gj, fr, kmax, Qsym, inp, args.rmax_geo, extras=EXTRAS))
        gj, fr = metric_two_wave(3, 0, N)
        reps.append(witness('single wave 1: t=3, s=0', gj, fr, kmax, Qsym, inp, args.rmax_geo))
        gj, fr = metric_two_wave(0, 5, N)
        reps.append(witness('single wave 2: t=0, s=5', gj, fr, kmax, Qsym, inp, args.rmax_geo))
        gj, fr = metric_kottler(1, QN(1, 10), 3, QN(1, 3), N)
        reps.append(witness('Kottler m=1, lambda_std=1/10 complexified phi->i phi, r=3, cos(theta)=1/3', gj, fr, kmax, Qsym, inp, args.rmax_geo, extras=EXTRAS))
        # negative controls: NON-Einstein metrics. The polynomial recursion must fail somewhere,
        # while the geometric Ricci identity (the content of the 0.1.0 Kasner check) still holds.
        gj, fr = metric_kasner(['1/2', '1/3', '1/5'], N)
        reps.append(witness('NEGATIVE CONTROL non-vacuum Kasner(1/2,1/3,1/5)', gj, fr, kmax, Qsym, inp, args.rmax_geo, expect_einstein=False))
        gj, fr = metric_two_wave(3, 5, N, exact_family=False)
        reps.append(witness('NEGATIVE CONTROL paper trial F=t u^3, q=x^2, t=3,s=5 (not Einstein)', gj, fr, kmax, Qsym, inp, args.rmax_geo, expect_einstein=False))
        out('WITNESS_SUMMARY', [{k: r[k] for k in ('witness', 'Lambda', 'einstein_residual_terms', 'Q0_zero(Bianchi)', 'poly_Q_vs_geometric_Q', 'geometric_ricci_identity(any metric)')} for r in reps])
    out('DONE', {'seconds': round(time.time() - T0, 1)})

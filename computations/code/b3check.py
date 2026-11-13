#!/usr/bin/env python3
"""Numerical check of the record-derivation estimate of
'A projective twistor correspondence for local analytic Einstein germs' v0.2.12,
Appendix B (Lemma B.1 recursion, Lemma B.3 inverse-order gain, Theorem B.4 budget).

Scope (stated in README.md): Lambda = 0; degree-2 and degree-3 parts of Q_r only.
Q_r is computed from the paper's recursion
    delta_r Q_r = -K_r - (1 - tau) H Q_{r-1},   Q_r = M_r J_r^* (RHS),
and the residual delta_r Q_r - RHS is printed (consistency = exact-set compatibility).
Degree-2 maps are kept with one coherent label slot and one full slot (matrices L);
degree-3 values are evaluated on three coherent labels y_i = sum_j z_i^j xi_i^{j+4} pi_i^j.

Representation: an element of Sym^n S* (x) Sym^m S'* is the coefficient array P[a,b] of
(u0)^(n-a) (u1)^a (v0)^(m-b) (v1)^b in T(u,v).  V* slots are explicit (A, A') axes.
Usage: python3 b3check.py RMAX SEED CHIRALITIES   (e.g. 6 1 ++-)
"""
import sys, time, resource
import numpy as np
from math import comb, factorial

np.seterr(over='raise', divide='raise', invalid='raise')
def _checked_float(value):
    value=float(value)
    if not np.isfinite(value):raise FloatingPointError('Nonfinite numerical scalar')
    return value


EPS = np.array([[0., 1.], [-1., 0.]])


def deg(c, r):
    return (r + 4, r) if c > 0 else (r, r + 4)


# ---------- polynomial operations: u axis = -2, v axis = -1 ----------
def du(P, A):
    p = P.shape[-2] - 1
    al = np.arange(max(p, 0))
    if A == 0:
        return P[..., :p, :] * (p - al)[:, None]
    return P[..., 1:, :] * (al + 1)[:, None]


def dv(P, A):
    q = P.shape[-1] - 1
    be = np.arange(max(q, 0))
    if A == 0:
        return P[..., :q] * (q - be)
    return P[..., 1:] * (be + 1)


def mu(P, A):
    s = list(P.shape); s[-2] += 1
    out = np.zeros(s)
    if A == 0:
        out[..., :-1, :] = P
    else:
        out[..., 1:, :] = P
    return out


def mv(P, A):
    s = list(P.shape); s[-1] += 1
    out = np.zeros(s)
    if A == 0:
        out[..., :-1] = P
    else:
        out[..., 1:] = P
    return out


def weights(n, m):
    a = np.array([1.0 / comb(n, k) for k in range(n + 1)])
    b = np.array([1.0 / comb(m, k) for k in range(m + 1)])
    return np.outer(a, b)


def hnorm(X):
    n = X.shape[-2] - 1; m = X.shape[-1] - 1
    return _checked_float(np.sqrt(np.sum(X * X * weights(n, m))))


# ---------- the operators of Appendix B ----------
def jmap(P):
    """j: Sym^n (x) Sym^m -> V* (x) Sym^{n-1} (x) Sym^{m-1}  (isometric regrouping)."""
    n = P.shape[-2] - 1; m = P.shape[-1] - 1
    rows = []
    for A in (0, 1):
        rows.append(np.stack([du(dv(P, Ap), A) for Ap in (0, 1)], axis=-3))
    return np.stack(rows, axis=-4) / (n * m)


def jstar(X):
    """adjoint of j = symmetrization: merges the V* pair at axes (-4,-3) into the polynomial."""
    out = 0
    for A in (0, 1):
        for Ap in (0, 1):
            out = out + mu(mv(X[..., A, Ap, :, :], Ap), A)
    return out


def tau(X):
    return X.swapaxes(-6, -4).swapaxes(-5, -3)


def proj_u(Y):
    n = Y.shape[-2] - 1
    Y0 = Y[..., 0, :, :, :]; Y1 = Y[..., 1, :, :, :]
    g = mu(Y0, 0) + mu(Y1, 1)
    up = np.stack([du(g, 0), du(g, 1)], axis=-4) / (n + 1)
    if n == 0:
        low = np.zeros_like(Y)
    else:
        f = (du(Y1, 0) - du(Y0, 1)) / (n + 1)
        low = np.stack([-mu(f, 1), mu(f, 0)], axis=-4)
    return up, low


def proj_v(Y):
    m = Y.shape[-1] - 1
    Y0 = Y[..., :, 0, :, :]; Y1 = Y[..., :, 1, :, :]
    g = mv(Y0, 0) + mv(Y1, 1)
    up = np.stack([dv(g, 0), dv(g, 1)], axis=-3) / (m + 1)
    if m == 0:
        low = np.zeros_like(Y)
    else:
        f = (dv(Y1, 0) - dv(Y0, 1)) / (m + 1)
        low = np.stack([-mv(f, 1), mv(f, 0)], axis=-3)
    return up, low


def blocks(Y):
    uu, ul = proj_u(Y)
    pp, pm = proj_v(uu)      # ++, +-
    mp, mm = proj_v(ul)      # -+, --
    return pp, pm, mp, mm


def Mop(Y):
    n = Y.shape[-2] - 1; m = Y.shape[-1] - 1
    pp, pm, mp, mm = blocks(Y)
    return n / (n + 1) * mp + m / (m + 1) * pm + n * m / (n * m - 1) * mm


def delta(Q):
    JQ = jmap(Q)
    return JQ - tau(JQ)


# ---------- curvature and spin action ----------
def psi_tensor(p):
    T = np.zeros((2, 2, 2, 2))
    for A in (0, 1):
        for B in (0, 1):
            for C in (0, 1):
                for D in (0, 1):
                    k = A + B + C + D
                    T[A, B, C, D] = p[k] / comb(4, k)
    return T


def beta_from(p, chir):
    """R(x,y) for x=(A,A'), y=(B,B'): returns (betaS, betaSp) each [A,A',B,B',D,C]."""
    T = psi_tensor(p)
    phi = np.zeros((2, 2, 2, 2))            # [A,B,D,C]
    phi[:, :, 0, :] = T[:, :, :, 1]
    phi[:, :, 1, :] = -T[:, :, :, 0]
    bS = np.zeros((2, 2, 2, 2, 2, 2)); bSp = np.zeros((2, 2, 2, 2, 2, 2))
    if chir > 0:
        bS = -np.einsum('pq,abdc->apbqdc', EPS, phi)       # -eps[A',B'] phi_{A,B}
    else:
        bSp = -np.einsum('ab,pqdc->apbqdc', EPS, phi)      # -eps[A,B] phi'_{A',B'}
    return bS, bSp


def spin_act_all(P, bS, bSp):
    """K[..., x, y, poly] = V_{R(x,y)} P for P (..., n+1, m+1)."""
    Pu = np.stack([np.stack([mu(du(P, D), C) for C in (0, 1)], 0) for D in (0, 1)], 0)
    Pv = np.stack([np.stack([mv(dv(P, D), C) for C in (0, 1)], 0) for D in (0, 1)], 0)
    K = np.einsum('apbqdc,dc...->...apbq', bS, Pu) + np.einsum('apbqdc,dc...->...apbq', bSp, Pv)
    # move the four V* axes before the polynomial axes
    return np.moveaxis(K, [-4, -3, -2, -1], [-6, -5, -4, -3])


def coh(c, j, xi, pi):
    n, m = deg(c, j)
    a = np.array([comb(n, k) * xi[0] ** (n - k) * xi[1] ** k for k in range(n + 1)])
    b = np.array([comb(m, k) * pi[0] ** (m - k) * pi[1] ** k for k in range(m + 1)])
    return np.outer(a, b)


def order0_p(c, P):
    return P[:, 0] if c > 0 else P[0, :]


# ---------- gather for the linear shift of the full slot ----------
_gcache = {}


def gather_info(c, t):
    key = (c, t)
    if key in _gcache:
        return _gcache[key]
    n, m = deg(c, t)
    Bt = (n + 1) * (m + 1)
    idx = np.zeros((Bt, 2, 2), dtype=np.int64); w = np.zeros((Bt, 2, 2))
    for a in range(n + 1):
        for b in range(m + 1):
            mu_ = a * (m + 1) + b
            for A in (0, 1):
                if A == 0:
                    okA, cA, a2 = a <= n - 1, n - a, a
                else:
                    okA, cA, a2 = a >= 1, a, a - 1
                for Ap in (0, 1):
                    if Ap == 0:
                        okB, cB, b2 = b <= m - 1, m - b, b
                    else:
                        okB, cB, b2 = b >= 1, b, b - 1
                    if okA and okB:
                        idx[mu_, A, Ap] = a2 * m + b2
                        w[mu_, A, Ap] = cA * cB / (n * m)
    _gcache[key] = (idx, w)
    return idx, w


def basis(c, t):
    n, m = deg(c, t)
    B = (n + 1) * (m + 1)
    return np.eye(B).reshape(B, n + 1, m + 1)


# ---------- main computation ----------
def run(RMAX, seed, chir):
    rng = np.random.default_rng(seed)
    CH = [+1, -1]
    labels = []
    for s in chir:
        xi = rng.normal(size=2); xi /= np.linalg.norm(xi)
        pi = rng.normal(size=2); pi /= np.linalg.norm(pi)
        labels.append(dict(c=+1 if s == '+' else -1, xi=xi, pi=pi, ell=np.outer(xi, pi)))
    print(f"# RMAX={RMAX} seed={seed} chiralities={chir}")
    for i, lb in enumerate(labels):
        print(f"# label {i}: c={lb['c']:+d} xi={lb['xi']} pi={lb['pi']}")

    def lab_coh(k, j):
        lb = labels[k]
        return coh(lb['c'], j, lb['xi'], lb['pi'])

    def beta_label(k):
        lb = labels[k]
        return beta_from(order0_p(lb['c'], lab_coh(k, 0)), lb['c'])

    t0 = time.time()
    L = {}           # L[(k,cw,co)] = {t: array (B_t,2,2,u,v)} at the current level r
    F2 = {}          # F2[(i,l,co,t)] = {(ji,jl): array (2,2,u,v)}
    F3prev = {}      # F3 at level r-1: {(co, j): array}
    stats = dict(resL=0.0, resF3=0.0, jsHQ=0.0, sym2=0.0)
    gain_rows = []

    def L_step(k, cw, co, r, Lprev):
        new = {}
        bS_k, bSp_k = beta_label(k)
        ck = labels[k]['c']
        un, um = deg(co, r - 1)
        for t in range(r - 1, -1, -1):
            nb = (deg(cw, t)[0] + 1) * (deg(cw, t)[1] + 1)
            HQ = np.zeros((nb, 2, 2, 2, 2, un + 1, um + 1))
            if Lprev is not None and t <= r - 2:
                HQ += np.einsum('ij,bklmn->bijklmn', labels[k]['ell'], Lprev[t])
            if Lprev is not None and t >= 1:
                idx, w = gather_info(cw, t)
                HQ += w[:, :, :, None, None, None, None] * Lprev[t - 1][idx]
            K = np.zeros_like(HQ)
            if t == r - 1 and co == cw:
                K += spin_act_all(basis(cw, r - 1), bS_k, bSp_k)
            if t == 0 and co == ck:
                yk = lab_coh(k, r - 1)
                E0 = basis(cw, 0)
                for b in range(E0.shape[0]):
                    bS, bSp = beta_from(order0_p(cw, E0[b]), cw)
                    K[b] += spin_act_all(yk, bS, bSp)
            RHS = -K - (HQ - tau(HQ))
            Q = Mop(jstar(RHS))
            res = delta(Q) - RHS
            nr = max(np.sqrt(np.sum(RHS ** 2)), np.sqrt(np.sum(HQ ** 2)), np.sqrt(np.sum(K ** 2))) + 1e-300
            stats['resL'] = max(stats['resL'], _checked_float(np.sqrt(np.sum(res ** 2)) / nr))
            if np.any(HQ):
                stats['jsHQ'] = max(stats['jsHQ'], _checked_float(np.sqrt(np.sum(jstar(HQ) ** 2)) / np.sqrt(np.sum(HQ ** 2))))
            new[t] = Q
            if Lprev is not None and t in Lprev:
                del Lprev[t]          # no longer needed (t is processed in descending order)
        return new

    opcache = {}

    def opnorm_pow(key, Lrt, cw, t, co, r, iters=40):
        if key in opcache:
            return opcache[key]
        n, m = deg(cw, t)
        win = np.sqrt(1.0 / weights(n, m)).ravel()
        wout = np.sqrt(weights(*deg(co, r)))
        Mat = (Lrt * wout).reshape(Lrt.shape[0], -1).T * win[None, :]
        x = np.random.default_rng(0).normal(size=Mat.shape[1])
        x /= np.linalg.norm(x); s = 0.0
        for _ in range(iters):
            y = Mat @ x; s = np.linalg.norm(y)
            if s == 0: break
            x = Mat.T @ (y / s); nx = np.linalg.norm(x)
            if nx == 0: break
            x /= nx
        opcache[key] = _checked_float(s)
        return opcache[key]

    def opnorm_L(Lrt, cw, t, co, r):
        n, m = deg(cw, t)
        win = np.sqrt(1.0 / weights(n, m)).ravel()        # orthonormal input scaling
        wout = np.sqrt(weights(*deg(co, r)))
        Mat = (Lrt * wout).reshape(Lrt.shape[0], -1).T * win[None, :]
        return _checked_float(np.linalg.norm(Mat, 2))

    for r in range(1, RMAX + 1):
        tr = time.time()
        # ---- degree 3 at level r (uses L at level r-1, F2 at t<=r-2, F3 at r-1) ----
        F3cur = {}
        n3max = {}; insmax = {}
        if r >= 3:
            comps = [(a, b, r - 3 - a - b) for a in range(r - 2) for b in range(r - 2 - a)]
            for co in CH:
                un, um = deg(co, r - 1)
                for j in comps:
                    HQ = np.zeros((2, 2, 2, 2, un + 1, um + 1))
                    for i in range(3):
                        if j[i] >= 1:
                            jj = list(j); jj[i] -= 1
                            HQ += np.einsum('ij,klmn->ijklmn', labels[i]['ell'], F3prev[(co, tuple(jj))])
                    for k in range(3):
                        i, l = [x for x in range(3) if x != k]
                        t = j[i] + j[l] + 1
                        for cm in CH:
                            Y = F2[(i, l, cm, t)][(j[i], j[l])]
                            ins = np.einsum('xyb,bklmn->xyklmn', Y.reshape(2, 2, -1), L[(k, cm, co)][t])
                            ni = hnorm(ins)
                            if ni > 0:
                                g = hnorm(Mop(jstar(tau(ins))))
                                fn = np.prod([factorial(x) for x in j]) / factorial(r)
                                lop = opnorm_pow((r - 1, k, cm, co, t), L[(k, cm, co)][t], cm, t, co, r - 1)
                                prod = lop * hnorm(Y)
                                gain_rows.append((r, t, j[k], g / ni, g * fn, ni * fn, g / prod, ni / prod))
                            HQ += ins
                    RHS = -(HQ - tau(HQ))
                    F = Mop(jstar(RHS))
                    res = delta(F) - RHS
                    nr = max(np.sqrt(np.sum(RHS ** 2)), np.sqrt(np.sum(HQ ** 2))) + 1e-300
                    stats['resF3'] = max(stats['resF3'], _checked_float(np.sqrt(np.sum(res ** 2)) / nr))
                    if SUMS:
                        print(f"   RES r={r} co={co:+d} j={j} rel={_checked_float(np.sqrt(np.sum(res ** 2)) / nr):.3e} |RHS|={nr:.3e}")
                    F3cur[(co, j)] = F
                    N3 = hnorm(F) * np.prod([factorial(x) for x in j]) / factorial(r)
                    n3max[(co, j)] = N3
        F3prev = F3cur
        # ---- degree 2: advance L to level r ----
        newL = {}
        for k in range(3):
            for cw in CH:
                for co in CH:
                    newL[(k, cw, co)] = L_step(k, cw, co, r, L.get((k, cw, co)))
        L = newL
        # ---- F2 at level r ----
        n2 = []
        for i in range(3):
            for l in range(i + 1, 3):
                ci, cl = labels[i]['c'], labels[l]['c']
                for co in CH:
                    d = {}
                    for jl in range(r):
                        ji = r - 1 - jl
                        y = lab_coh(l, jl).ravel()
                        v1 = np.einsum('b,b...->...', y, L[(i, cl, co)][jl])
                        v2 = np.einsum('b,b...->...', lab_coh(i, ji).ravel(), L[(l, ci, co)][ji])
                        s = np.sqrt(np.sum((v1 - v2) ** 2)) / (np.sqrt(np.sum(v1 ** 2)) + 1e-300)
                        if np.sum(v1 ** 2) > 0:
                            stats['sym2'] = max(stats['sym2'], _checked_float(s))
                        d[(ji, jl)] = v1
                        n2.append(hnorm(v1) * factorial(ji) * factorial(jl) / factorial(r))
                    F2[(i, l, co, r)] = d
        # full-slot operator norms for label 0
        n2full = 0.0
        for cw in CH:
            for co in CH:
                for t in range(r):
                    nrm = opnorm_L(L[(0, cw, co)][t], cw, t, co, r)
                    n2full = max(n2full, nrm * factorial(t) * factorial(r - 1 - t) / factorial(r))
        n3 = max(n3max.values()) if n3max else 0.0
        if SUMS:
            for co in CH:
                s2 = []
                for (i, l) in ((0, 1), (0, 2), (1, 2)):
                    s2.append(hnorm(sum(F2[(i, l, co, r)].values())))
                s3 = hnorm(sum(v for (c_, j_), v in F3cur.items() if c_ == co)) if F3cur else 0.0
                if F3cur:
                    zs = (2.0, 3.0, 5.0)
                    sz = sum(v * zs[0]**j_[0] * zs[1]**j_[1] * zs[2]**j_[2] for (c_, j_), v in F3cur.items() if c_ == co)
                    print(f"ZSUM r={r} co={co:+d} |sum z^j F3[j]|={hnorm(sz):.6e} (z=2,3,5)")
                    for (c_, j_), v in sorted(F3cur.items()):
                        if c_ == co:
                            RHSn = None
                            print(f"   F3 r={r} co={co:+d} j={j_} |F3|={hnorm(v):.6e}")
                print(f"SUM r={r} co={co:+d}  |e0e1|={s2[0]:.6e} |e0e2|={s2[1]:.6e} "
                      f"|e1e2|={s2[2]:.6e} |e0e1e2|={s3:.6e}")
        mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
        print(f"r={r:2d}  N2max={max(n2):.4e}  N2/r={max(n2)/r:.4e}  N2full={n2full:.4e}  "
              f"N3max={n3:.4e}  N3/r={n3/r:.4e}  resL={stats['resL']:.1e} resF3={stats['resF3']:.1e} "
              f"JsHQ={stats['jsHQ']:.1e} sym2={stats['sym2']:.1e}  dt={time.time()-tr:.1f}s maxrss={mem:.0f}MB",
              flush=True)
    # gain table: aggregate over r for each t
    print("# insertion gain:  t  count  max(|MJ*tau ins|/|ins|)  (t+1)*max  max normalized ins contribution")
    ts = sorted(set(g[1] for g in gain_rows))
    for t in ts:
        rows = [g for g in gain_rows if g[1] == t]
        mx = max(g[3] for g in rows)
        mn = max(g[4] for g in rows)
        mpre = max(g[5] for g in rows)
        r2 = max(g[6] for g in rows); r2b = max(g[7] for g in rows)
        print(f"  t={t:2d}  n={len(rows):4d}  ratio_max={mx:.4e}  (t+1)ratio={mx*(t+1):.4e}  "
              f"ins_after_norm_max={mn:.4e}  ins_before_norm_max={mpre:.4e}  "
              f"after/(|L|op|Y|)max={r2:.4e} (t+1)x={r2*(t+1):.4e}  before/(|L||Y|)max={r2b:.4e}")
    print("# gain by (r,t) at j_k=0 (outer coherent order 0):")
    for g in gain_rows:
        if g[2] == 0:
            pass
    sel = {}
    for g in gain_rows:
        key = (g[0], g[1])
        sel[key] = max(sel.get(key, 0.0), g[3])
    for key in sorted(sel):
        if key[0] == RMAX or key[1] == key[0] - 2:
            print(f"  r={key[0]:2d} t={key[1]:2d} ratio_max={sel[key]:.4e} (t+1)ratio={sel[key]*(key[1]+1):.4e}")
    print(f"# total time {time.time()-t0:.1f}s")


SUMS = False

if __name__ == '__main__':
    RMAX = int(sys.argv[1]); seed = int(sys.argv[2]); chir = sys.argv[3]
    SUMS = len(sys.argv) > 4 and sys.argv[4] == 'sums'
    run(RMAX, seed, chir)

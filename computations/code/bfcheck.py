#!/usr/bin/env python3
"""Second nilpotent evaluation of the Appendix B recursion (Lemma B.1), Lambda = 0.

Q_r(X) is evaluated at a record X whose entries lie in a commutative nilpotent algebra
(generators e_i with e_i^2 = 0; elements stored as arrays over subsets).  The directional
derivative D Q_{r-1}(X)[V] is obtained exactly by adjoining a new generator d:
Q_{r-1}(X + d V) = Q_{r-1}(X) + d * D Q_{r-1}(X)[V].  The free index a of V is a batch axis.
At every level the residual delta_r Q_r - RHS is recorded (consistency).
Mode 'random': random real records of both chiralities.  Mode 'labels': X = sum_i e_i y_i with
the coherent label sequences of b3check.py, so that the e1e2 and e1e2e3 components can be
compared with the polarized F2 / F3 sums.
Usage: python3 bfcheck.py MODE R SEED [CHIR]
"""
import sys, time
import numpy as np
from math import comb

np.seterr(over='raise', divide='raise', invalid='raise')
def _checked_float(value):
    value=float(value)
    if not np.isfinite(value):raise FloatingPointError('Nonfinite numerical scalar')
    return value

from b3check import (deg, du, dv, mu, mv, jmap, jstar, tau, Mop, delta, psi_tensor, coh, hnorm, EPS)

CH = (+1, -1)


def beta_batch(p, chir):
    """p: (..., 5) Weyl coefficients -> (betaS, betaSp) with shape (..., A,A',B,B',D,C)."""
    T = np.zeros(p.shape[:-1] + (2, 2, 2, 2))
    for A in (0, 1):
        for B in (0, 1):
            for C in (0, 1):
                for D in (0, 1):
                    k = A + B + C + D
                    T[..., A, B, C, D] = p[..., k] / comb(4, k)
    phi = np.zeros(p.shape[:-1] + (2, 2, 2, 2))
    phi[..., :, :, 0, :] = T[..., :, :, :, 1]
    phi[..., :, :, 1, :] = -T[..., :, :, :, 0]
    z = np.zeros(p.shape[:-1] + (2, 2, 2, 2, 2, 2))
    if chir > 0:
        return -np.einsum('pq,...abdc->...apbqdc', EPS, phi), z
    return z, -np.einsum('ab,...pqdc->...apbqdc', EPS, phi)


def spin_batch(P, bS, bSp):
    """P (..., n+1, m+1); bS, bSp (..., A,A',B,B',D,C) with the same leading batch."""
    Pu = np.stack([np.stack([mu(du(P, D), C) for C in (0, 1)], -3) for D in (0, 1)], -4)  # (...,D,C,u,v)
    Pv = np.stack([np.stack([mv(dv(P, D), C) for C in (0, 1)], -3) for D in (0, 1)], -4)
    return (np.einsum('...apbqdc,...dcuv->...apbquv', bS, Pu)
            + np.einsum('...apbqdc,...dcuv->...apbquv', bSp, Pv))


def subsets_of(S):
    T = S
    while True:
        yield T
        if T == 0:
            break
        T = (T - 1) & S


def Kterm(X, k, r, co):
    """K = V_{R_{X_0}} X_{r-1} (algebra product).  Output (2^k, *B, 2,2,2,2, W(co,r-1))."""
    out = None
    Xr = X[(co, r - 1)]
    for cw in CH:
        X0 = X[(cw, 0)]
        p = X0[..., :, 0] if cw > 0 else X0[..., 0, :]           # (2^k, *B, 5)
        bS, bSp = beta_batch(p, cw)
        for S in range(2 ** k):
            for T in subsets_of(S):
                if not np.any(p[T]) or not np.any(Xr[S ^ T]):
                    continue
                v = spin_batch(Xr[S ^ T], bS[T], bSp[T])
                if out is None:
                    out = np.zeros((2 ** k,) + v.shape)
                out[S] += v
    if out is None:
        un, um = deg(co, r - 1)
        out = np.zeros((2 ** k,) + Xr.shape[1:-2] + (2, 2, 2, 2, un + 1, um + 1))
    return out


RES = {}


def Qlist(X, k, R):
    """X[(c,j)] arrays (2^k, *B, n+1, m+1) for j<=R-1.  Returns list of dicts Q[r][co]."""
    Q = [dict((co, None) for co in CH)]
    for r in range(1, R + 1):
        Qr = {}
        # direction V_j = i_a X_{j+1} + Q_j(X)_a, j = 0..r-2, free index a as new trailing batch axes
        if r >= 2:
            Xp = {}
            for c in CH:
                for j in range(0, r - 1):
                    base = X[(c, j)]
                    shp = base.shape
                    nb = base.ndim - 3            # number of batch axes after the algebra axis
                    Vj = jmap(X[(c, j + 1)])        # (2^k, *B, 2,2, W_j)
                    if Q[j][c] is not None:
                        Vj = Vj + Q[j][c]
                    new = np.zeros((2 ** (k + 1),) + shp[1:-2] + (2, 2) + shp[-2:])
                    new[:2 ** k] = base[..., None, None, :, :]
                    new[2 ** k:] = Vj
                    Xp[(c, j)] = new
            Qd = Qlist(Xp, k + 1, r - 1)[r - 1]
        for co in CH:
            K = Kterm(X, k, r, co)
            if r >= 2:
                HQ = Qd[co][2 ** k:]               # (2^k, *B, 2,2[a], 2,2[b], W(co,r-1))
            else:
                HQ = np.zeros_like(K)
            RHS = -K - (HQ - tau(HQ))
            Qv = Mop(jstar(RHS))
            res = delta(Qv) - RHS
            nr = _checked_float(np.sqrt(np.sum(RHS ** 2)))
            if nr > 0:
                key = (r, k)
                RES[key] = max(RES.get(key, 0.0), _checked_float(np.sqrt(np.sum(res ** 2)) / nr))
            Qr[co] = Qv
        Q.append(Qr)
    return Q


def main():
    mode, R, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    rng = np.random.default_rng(seed)
    t0 = time.time()
    if mode == 'random':
        X = {}
        for c in CH:
            for j in range(R):
                n, m = deg(c, j)
                X[(c, j)] = rng.normal(size=(1, n + 1, m + 1))
        Q = Qlist(X, 0, R)
        for key in sorted(RES):
            print(f"level r={key[0]} nilpotents={key[1]}  max relative residual {RES[key]:.3e}")
    else:
        chir = sys.argv[4]
        labels = []
        for s in chir:
            xi = rng.normal(size=2); xi /= np.linalg.norm(xi)
            pi = rng.normal(size=2); pi /= np.linalg.norm(pi)
            labels.append((+1 if s == '+' else -1, xi, pi))
        X = {}
        for c in CH:
            for j in range(R):
                n, m = deg(c, j)
                X[(c, j)] = np.zeros((8, n + 1, m + 1))
        zs = [_checked_float(x) for x in sys.argv[5].split(',')] if len(sys.argv) > 5 else [1.0, 1.0, 1.0]
        for i, (c, xi, pi) in enumerate(labels):
            for j in range(R):
                X[(c, j)][1 << i] += zs[i] ** j * coh(c, j, xi, pi)
        Q = Qlist(X, 3, R)
        for key in sorted(RES):
            print(f"level r={key[0]} nilpotents={key[1]}  max relative residual {RES[key]:.3e}")
        for r in range(1, R + 1):
            for co in CH:
                q = Q[r][co]
                print(f"r={r} co={co:+d}  |e0e1|={hnorm(q[3]):.6e} |e0e2|={hnorm(q[5]):.6e} "
                      f"|e1e2|={hnorm(q[6]):.6e} |e0e1e2|={hnorm(q[7]):.6e}")
    print(f"# time {time.time()-t0:.1f}s")


if __name__ == '__main__':
    main()

"""Container-only exact checks of Proposition 9.2's two-wave tensors.

This module must be invoked by the bounded supplement worker, after its
resource and isolation preflight. It uses SymPy exact expressions, not floats.
No manuscript or historical result is read at mathematical run time.
"""
from itertools import product
import sympy as sp
import report


CHECK_IDS = ['S9-WAVE-RICCI', 'S9-MIXED-COTTON', 'S9-MIXED-REPAIR']


def clean(value):
    return sp.factor(sp.cancel(sp.expand(value)))


def equal_matrix(left, right):
    return all(clean(value) == 0 for value in left - right)


def metric(a, b):
    """Coordinates are (u,v,x,y), and g_uv=1, g_xy=-1."""
    return sp.Matrix([[0, 1, 0, 0], [1, b, 0, 0],
                      [0, 0, a, -1], [0, 0, -1, 0]])


def geometry(g, coords):
    """Derive the inverse, all 64 Christoffels and all 16 Ricci entries."""
    gi = g.inv().applyfunc(clean)
    gamma = {}
    for a, b, c in product(range(4), repeat=3):
        gamma[a, b, c] = clean(sum(
            gi[a, d] * (sp.diff(g[d, c], coords[b])
                        + sp.diff(g[d, b], coords[c])
                        - sp.diff(g[b, c], coords[d]))
            for d in range(4)) / 2)
    ricci = sp.Matrix(4, 4, lambda b, c: clean(sum(
        sp.diff(gamma[a, b, c], coords[a])
        - sp.diff(gamma[a, b, a], coords[c])
        + sum(gamma[a, a, d] * gamma[d, b, c]
              - gamma[a, c, d] * gamma[d, b, a] for d in range(4))
        for a in range(4))))
    scalar = clean(sum(gi[a, b] * ricci[a, b]
                       for a, b in product(range(4), repeat=2)))
    return gi, gamma, ricci, scalar


def curvature_support(gamma, coords):
    """The exterior support of R^a_bcd, with c<d; no expected support is used."""
    support = set()
    nonzero_entries = 0
    for a, b, c, d in product(range(4), repeat=4):
        if c >= d:
            continue
        value = clean(sp.diff(gamma[a, b, d], coords[c])
                      - sp.diff(gamma[a, b, c], coords[d])
                      + sum(gamma[a, e, c] * gamma[e, b, d]
                            - gamma[a, e, d] * gamma[e, b, c]
                            for e in range(4)))
        if value != 0:
            support.add((c, d))
            nonzero_entries += 1
    return support, nonzero_entries


def hodge_two_form(form, inverse):
    """Use det(g)=1 and the holomorphic volume du wedge dv wedge dx wedge dy."""
    raised = inverse * form * inverse.T
    return sp.Matrix(4, 4, lambda a, b: clean(sum(
        sp.LeviCivita(a, b, c, d) * raised[c, d] / 2
        for c, d in product(range(4), repeat=2))))


def quotient_ts(value, t, s):
    """Reduce polynomial parameters in C[t,s]/(t^2,s^2), retaining 1,t,s,ts."""
    polynomial = sp.Poly(sp.expand(value), t, s)
    return clean(sum(coefficient * t**i * s**j
                     for (i, j), coefficient in polynomial.terms()
                     if i < 2 and j < 2))


def run(profile=None):
    u, v, x, y, t, s = sp.symbols('u v x y t s')
    coords = (u, v, x, y)
    f = sp.Function('f')(u)
    q = sp.Function('q')(x)
    g = metric(t * f, s * q)
    gi, gamma, ricci, scalar = geometry(g, coords)
    expected_gi = sp.Matrix([[-s*q, 1, 0, 0], [1, 0, 0, 0],
                             [0, 0, 0, -1], [0, 0, -1, -t*f]])
    assert clean(g.det() - 1) == 0
    assert equal_matrix(gi, expected_gi)
    assert equal_matrix(g * gi, sp.eye(4))

    expected_gamma = {
        (1, 2, 2): -t * sp.diff(f, u) / 2,
        (0, 2, 2): t * s * q * sp.diff(f, u) / 2,
        (3, 0, 2): -t * sp.diff(f, u) / 2,
        (3, 2, 0): -t * sp.diff(f, u) / 2,
        (3, 1, 1): s * sp.diff(q, x) / 2,
        (0, 1, 2): s * sp.diff(q, x) / 2,
        (0, 2, 1): s * sp.diff(q, x) / 2,
    }
    assert all(clean(value - expected_gamma.get(key, 0)) == 0
               for key, value in gamma.items())
    order = [2, 1, 0, 3]  # (x,v,u,y); all connection matrices strictly lower triangular.
    assert all(gamma[order[a], order[b], c] == 0
               for a, b, c in product(range(4), repeat=3) if a <= b)
    expected_ricci = sp.zeros(4)
    expected_ricci[2, 2] = t * s * q * sp.diff(f, u, 2) / 2
    assert equal_matrix(ricci, expected_ricci)
    assert scalar == 0
    assert equal_matrix(ricci.subs(s, 0), sp.zeros(4))
    assert equal_matrix(ricci.subs(t, 0), sp.zeros(4))

    # The individual nonzero curvature two-forms have opposite Hodge signs.
    # Coordinate-orientation signs are reported without identifying them with
    # the manuscript's absolute +/- spin-frame labels.
    wave_f_gamma = {key: value.subs(s, 0) for key, value in gamma.items()}
    wave_q_gamma = {key: value.subs(t, 0) for key, value in gamma.items()}
    support_f, entries_f = curvature_support(wave_f_gamma, coords)
    support_q, entries_q = curvature_support(wave_q_gamma, coords)
    assert support_f == {(0, 2)} and entries_f > 0
    assert support_q == {(1, 2)} and entries_q > 0
    form_f = sp.zeros(4)
    form_f[0, 2], form_f[2, 0] = 1, -1  # du wedge dx
    form_q = sp.zeros(4)
    form_q[2, 1], form_q[1, 2] = 1, -1  # dx wedge dv
    assert equal_matrix(hodge_two_form(form_f, gi.subs(s, 0)), form_f)
    assert equal_matrix(hodge_two_form(form_q, gi.subs(t, 0)), -form_q)
    report.check('S9-WAVE-RICCI',
                 'Arbitrary-function two-wave connection, Ricci and relative chirality',
                 True, classification='symbolic-exact',
                 coordinate_order=['u', 'v', 'x', 'y'], determinant='1',
                 christoffel_components_checked=64, ricci_components_checked=16,
                 ricci='(t*s/2)*q(x)*f_second(u)*dx^2', scalar='0',
                 single_wave_curvature_supports=[['u', 'x'], ['v', 'x']],
                 relative_hodge_signs=[1, -1],
                 scope='Exact symbolic identity for arbitrary f(u),q(x) and unrestricted t,s. '
                       'No contact-cocycle admission or cohomology statement is checked.')

    # Re-derive the polynomial specialization, rather than reading expected P.
    gp = metric(t * u**3, s * x**2)
    gip, gammap, riccip, scalarp = geometry(gp, coords)
    schouten = (riccip - scalarp * gp / 6) / 2
    expected_p = sp.zeros(4)
    expected_p[2, 2] = sp.Rational(3, 2) * t * s * u * x**2
    assert equal_matrix(schouten, expected_p)
    assert clean(sum(gip[a, b] * schouten[a, b]
                     for a, b in product(range(4), repeat=2))) == 0

    def covariant_p(a, b, c):
        return clean(sp.diff(schouten[b, c], coords[a])
                     - sum(gammap[d, a, b] * schouten[d, c]
                           + gammap[d, a, c] * schouten[b, d]
                           for d in range(4)))

    cotton = clean(covariant_p(0, 2, 2) - covariant_p(2, 0, 2))
    assert clean(cotton - sp.Rational(3, 2) * t * s * x**2) == 0
    assert quotient_ts(cotton, t, s) == cotton
    assert clean(cotton.diff(t).diff(s).subs({t: 0, s: 0, x: 1})) == sp.Rational(3, 2)
    report.check('S9-MIXED-COTTON',
                 'Nonzero highest mixed Schouten and Cotton coefficients',
                 True, classification='symbolic-exact',
                 f='u^3', q='x^2', ring='C[t,s]/(t^2,s^2)',
                 schouten_ts_xx='3*u*x^2/2', cotton_ts_uxx='3*x^2/2',
                 scope='All 16 Schouten entries and the specified Cotton component. '
                       'The geometric quotient-class nonvanishing argument remains theoretical.')

    H = sp.Rational(3, 2) * u**2 * v * x**2
    flat = metric(0, 0)
    flat_inverse = flat.inv()
    h = sp.zeros(4)
    h[2, 2] = H
    trace_h = clean(sum(flat_inverse[a, b] * h[a, b]
                        for a, b in product(range(4), repeat=2)))
    divergence_h = [clean(sum(flat_inverse[a, c] * sp.diff(h[a, b], coords[c])
                              for a, c in product(range(4), repeat=2)))
                    for b in range(4)]
    box_h = clean(sum(flat_inverse[a, b] * sp.diff(H, coords[a], coords[b])
                      for a, b in product(range(4), repeat=2)))
    assert trace_h == 0 and divergence_h == [0, 0, 0, 0]
    assert clean(box_h - 6*u*x**2) == 0
    eps = sp.symbols('eps')
    _, _, ricci_linear_trial, _ = geometry(metric(eps * H, 0), coords)
    linear_ricci = ricci_linear_trial.diff(eps).subs(eps, 0)
    expected_linear_ricci = sp.zeros(4)
    expected_linear_ricci[2, 2] = -3*u*x**2
    assert equal_matrix(linear_ricci, expected_linear_ricci)

    repaired = gp + t*s*h
    repaired_inverse, _, repaired_ricci, repaired_scalar = geometry(repaired, coords)
    assert equal_matrix(repaired * repaired_inverse, sp.eye(4))
    assert all(quotient_ts(value, t, s) == 0 for value in repaired_ricci)
    assert quotient_ts(repaired_scalar, t, s) == 0
    # Negative control: the same polynomial expression is not an exact vacuum
    # repair over unrestricted parameters. This term is killed specifically by s^2.
    unrestricted_expected = sp.zeros(4)
    unrestricted_expected[2, 2] = sp.Rational(3, 2) * t * s**2 * v * x**4
    assert equal_matrix(repaired_ricci, unrestricted_expected)
    point_ricci = repaired_ricci.subs({t: 1, s: 1, u: 1, v: 1, x: 1, y: 0})
    assert point_ricci[2, 2] == sp.Rational(3, 2)
    report.check('S9-MIXED-REPAIR',
                 'Mixed repair is Ricci-flat in the declared quotient ring',
                 True, classification='symbolic-exact',
                 H='3*u^2*v*x^2/2', flat_trace='0', flat_divergence=[0, 0, 0, 0],
                 flat_box_H='6*u*x^2', linearized_ricci_xx='-3*u*x^2',
                 quotient_ring='C[t,s]/(t^2,s^2)', quotient_ricci_components_checked=16,
                 quotient_ricci_zero=True,
                 unrestricted_ricci_xx='3*t*s^2*v*x^4/2',
                 unrestricted_counterexample={'t': 1, 's': 1, 'u': 1, 'v': 1, 'x': 1,
                                              'y': 0, 'Ricci_xx': '3/2'},
                 scope='A highest mixed correction, not an exact unrestricted-parameter '
                       'vacuum or a fixed-free-record restoration algorithm.')

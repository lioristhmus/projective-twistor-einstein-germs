"""Container-only adapter for Claude's unchanged independent T3 implementation.

The upstream wrong-convention and non-Einstein counts are printed observations.
This adapter makes their distinguishing properties explicit PASS conditions.
It never imports or calls the primary ab_exact.py backend.
"""
import contextlib
import io
import json
import report


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def run(profile):
    rmax = profile['max_r']
    require(rmax == 2, 'Only the audited order-two profile is supported')
    # Keep the upstream source byte-identical; wrap its preflight output in
    # JSON lines, without changing its arithmetic or geometric calculations.
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        import t3_recursion as t
    for line in capture.getvalue().splitlines():
        require(line.startswith('PREFLIGHT '), 'Unexpected upstream import output')
        report.emit({'record': 'independent-library-preflight',
                     'details': json.loads(line[len('PREFLIGHT '):])})
    t.out = lambda tag, value: report.emit(
        {'record': 'independent-calculation', 'tag': tag, 'details': value})
    inp = t.Inputs(rmax + 1)
    good, rows = t.run_recursion(inp, rmax, check=True, label='independent-correct')
    require(all(row['delta Q - RHS nonzero coefficient polys'] == 0
                and row['J* HQ nonzero coefficient polys'] == 0 for row in rows),
            'Correct polynomial compatibility failed')
    extras = {
        'NC1 sign(R_U)->-1':
            t.run_recursion(inp, rmax, sign=-1, check=False, label='independent-NC1')[0],
        'NC3 Lambda/3->2Lambda/3':
            t.run_recursion(inp, rmax, lam_coeff=t.QN(2, 3), check=False,
                            label='independent-NC3')[0]}
    kmax, jet_order = rmax + 1, rmax + 3
    factories = [
        ('kasner', lambda: t.metric_kasner(['-2/7', '3/7', '6/7'], jet_order), True),
        ('two-wave', lambda: t.metric_two_wave(3, 5, jet_order), True),
        ('single-wave-1', lambda: t.metric_two_wave(3, 0, jet_order), True),
        ('single-wave-2', lambda: t.metric_two_wave(0, 5, jet_order), True),
        ('kottler', lambda: t.metric_kottler(1, t.QN(1, 10), 3, t.QN(1, 3),
                                            jet_order), True),
        ('non-Einstein-kasner',
         lambda: t.metric_kasner(['1/2', '1/3', '1/5'], jet_order), False),
        ('non-Einstein-trial',
         lambda: t.metric_two_wave(3, 5, jet_order, exact_family=False), False)]
    reps = {}
    for label, factory, einstein in factories:
        metric, frame = factory()
        controls = extras if label in ('kasner', 'two-wave', 'kottler') else None
        rep = t.witness(label, metric, frame, kmax, good, inp, rmax,
                        expect_einstein=einstein, extras=controls)
        require(all(rep['geometric_ricci_identity(any metric)'].values()),
                label + ': geometric commutator failed')
        if einstein:
            require(rep['einstein_residual_terms'] == 0,
                    label + ': Einstein condition failed')
            require(all(rep['Q0_zero(Bianchi)'].values()), label + ': Q0 nonzero')
            require(all(v['mismatches'] == 0
                        for v in rep['poly_Q_vs_geometric_Q'].values()),
                    label + ': polynomial/geometric mismatch')
        else:
            require(rep['einstein_residual_terms'] > 0,
                    label + ': negative metric is accidentally Einstein')
            require(not any(rep['Q0_zero(Bianchi)'].values()),
                    label + ': negative Q0 control did not distinguish both readouts')
            require(all(v['mismatches'] > 0
                        for v in rep['poly_Q_vs_geometric_Q'].values()),
                    label + ': negative polynomial/geometric control not detected')
        reps[label] = rep
    nc1, nc3 = 'NC1 sign(R_U)->-1', 'NC3 Lambda/3->2Lambda/3'
    for label in ('kasner', 'kottler'):
        require(all(n > 0 for n in reps[label]['wrong_convention_mismatches'][nc1].values()),
                label + ': wrong curvature-action sign was not detected')
    require(reps['two-wave']['wrong_convention_mismatches'][nc1]['r2+'] > 0,
            'Mixed two-wave order-two sign control was not detected')
    require(all(n > 0 for n in reps['kottler']['wrong_convention_mismatches'][nc3].values()),
            'Kottler: doubled Lambda coefficient was not detected')
    for label in ('kasner', 'two-wave'):
        require(all(n == 0 for n in reps[label]['wrong_convention_mismatches'][nc3].values()),
                label + ': Lambda-zero control should be insensitive to its coefficient')
    require(str(reps['kottler']['Lambda']) == '-1/10',
            'Kottler Einstein constant convention changed')
    require(reps['single-wave-1']['U0_plus_nonzero']
            and not reps['single-wave-1']['U0_minus_nonzero'],
            'First single-wave chiral support changed')
    require(reps['single-wave-2']['U0_minus_nonzero']
            and not reps['single-wave-2']['U0_plus_nonzero'],
            'Second single-wave chiral support changed')
    report.check('IW-GEOMETRY-CONTROLS-R2',
                 'Independent finite geometric witnesses with enforced convention controls',
                 True, classification='finite-exact', max_r=rmax,
                 implementation='Claude T3, unchanged; primary ab_exact.py not called',
                 exact_arithmetic=t.QN.__module__,
                 witnesses=reps,
                 enforced_controls=[
                     'Five Einstein witnesses: Einstein residual zero, Q0 zero, polynomial/geometric agreement',
                     'All seven metrics: geometric Ricci identity',
                     'Non-Einstein controls: Einstein residual and Q0 nonzero, polynomial/geometric mismatch',
                     'NC1 sign flip: Kasner/Kottler every tested order/chirality; two-wave r2+',
                     'NC3 doubled Lambda coefficient: Kottler every tested order/chirality',
                     'Lambda-zero Kasner/two-wave: NC3 insensitive, expected zero mismatch',
                     'Opposite single-wave chiral supports and Kottler Lambda=-1/10'],
                 scope='Finite exact witnesses through r=2 in an independent implementation. '
                       'Higher-order Claude results remain historical audit evidence. '
                       'No direct geometric witness test of primary ab_exact.py, all-order estimate or convergence.')


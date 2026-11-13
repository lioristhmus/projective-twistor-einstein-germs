"""Container-only adapters for finite exact checks and numerical diagnostics."""
import contextlib
import importlib
import io
import json
from pathlib import Path
import re
import runpy
import sys
import report

HERE = Path(__file__).resolve().parent


def capture_script(name, args=()):
    old = sys.argv
    stream = io.StringIO()
    try:
        sys.argv = [name, *map(str, args)]
        with contextlib.redirect_stdout(stream):
            runpy.run_path(str(HERE / name), run_name='__main__')
    finally:
        sys.argv = old
    text = stream.getvalue()
    if len(text.encode()) > 200_000:
        raise RuntimeError('Mathematical output exceeds the adapter bound')
    report.emit({'record': 'program-output', 'program': name, 'stdout': text})
    return text


def kasner(profile):
    r = profile['max_r']
    data = json.loads(capture_script('kasner_exact.py', ['--max-r', r]))
    rows = data['orders']
    expected = {(j, c) for j in range(1, r + 1) for c in ('+', '-')}
    ok = (data['status'] == 'PASS' and data['max_r'] == r
          and {(x['r'], x['chirality']) for x in rows} == expected
          and len(rows) == len(expected)
          and all(x['recursion_residuals'] == x['free_projection_residuals'] == 0 for x in rows))
    report.check('KASNER-R' + str(r), 'Kasner geometric derivatives versus Spencer recursion',
                 ok, classification='finite-exact', data=data)


def schwarzschild(profile):
    data = json.loads(capture_script('schwarzschild_exact.py'))
    report.check('SCH-RICCI', 'Coordinate inverse and vacuum Ricci tensor',
                 data['inverse_metric'] and data['Ricci_zero'], classification='symbolic-exact')
    report.check('SCH-SCREEN', 'Parallel polar screen and tidal sign',
                 data['polar_screen_parallel'] and data['rotation_Jacobi_check'],
                 classification='symbolic-exact', polar_tide=data['polar_tidal_coefficient'])
    report.check('SCH-CONFORMAL', 'Conformal scalar, scale equation and null tractor norm',
                 data['status'] == 'PASS' and data['normal_tractor_norm'] == '0',
                 classification='symbolic-exact', data=data,
                 scope='Intermediate signature -+++; the paper uses its explicit negation.')


def adamo(profile):
    text = capture_script('adamo_exact.py')
    entries = [json.loads(x[7:]) for x in text.splitlines() if x.startswith('RESULT ')]
    if len(entries) != 1:
        raise RuntimeError('Missing or duplicate Adamo result')
    data = entries[0]
    report.check('AASS-ALGEBRA', 'Printed external-source algebra under specified conventions',
                 all(data[x] for x in ('2.13', '2.24', '3.6', '3.28')),
                 classification='symbolic-exact', data={k: data[k] for k in ('2.13','2.24','3.6','3.28')},
                 scope='External AASS v2 formulas, not extra claims of the local paper.')
    report.check('AASS-PRINTED-CURVATURE', 'Ricci and scalar of the printed external metric',
                 data['printed_metric_bridge']['gS_Ricci_zero'],
                 classification='symbolic-exact', data=data['printed_metric_bridge'])
    report.check('K5-PROJECTOR', 'Local source projector and symmetric primitive metric',
                 data['our_K5']['original_projector_idempotent']
                 and data['our_K5']['G0_symmetric']
                 and data['our_K5']['G0_equals_minus_r_inv_sq_delta_plus_4mu'],
                 classification='symbolic-exact', data=data['our_K5'])
    # The retained script checks the radial EF block. Check the full angular
    # block and density simultaneously, after its explicit sheet/mass substitution.
    import sympy as s
    r, m, th = s.symbols('r m theta', nonzero=True)
    change = s.Matrix([[-s.I, s.I, 0, 0], [0, -1, 0, 0],
                       [0, 0, 1, 0], [0, 0, 0, 1]])
    k = s.Matrix([1, s.I, 0, 0])
    flat = s.diag(1, 1, r**2, r**2*s.sin(th)**2)
    source = -2/r**2 * (flat - 2*m/r*(k*k.T))
    ef = s.Matrix([[1-2*m/r, -1, 0, 0], [-1, 0, 0, 0],
                   [0, 0, -r**2, 0], [0, 0, 0, -r**2*s.sin(th)**2]])
    pulled = s.simplify(change.T*source*change)
    assert s.simplify(pulled-2/r**2*ef) == s.zeros(4)
    assert s.simplify(pulled/(s.sqrt(2)/r)**2-ef) == s.zeros(4)
    report.check('K5-EF', 'Full EF pullback and calibrated density',
                 data['our_K5']['calibrated_EF_pullback'], classification='symbolic-exact',
                 mu_src='m/2', radial_sheet='varrho=-r', density='sqrt(2)/r',
                 pullback='2*g_m/r^2', scope='Local angular/root chart; no global native gluing tested.')

    # Direct rational residue with abstract independent spinors. This addition
    # tests the contour factor rather than assuming it in the form components.
    a0,a1,b0,b1,w = s.symbols('a0 a1 b0 b1 w')
    A=s.Matrix([a0,a1]); B=s.Matrix([b0,b1]); E=s.Matrix([[0,1],[-1,0]])
    L=-E; lam=A+w*B; span=((E*A).T*B)[0]
    Q=((E*A).T*lam)[0]*((E*B).T*lam)[0]
    D=((E*lam).T*B)[0]
    assert s.expand(Q+span**2*w)==0 and s.expand(D-span)==0
    residue=s.Matrix(2,2,lambda a,b:s.simplify(s.diff(
        s.cancel(w**2*lam[a]*lam[b]*D/Q**2),w).subs(w,0)))
    assert s.simplify(residue-(A*B.T+B*A.T)/span**3)==s.zeros(2)
    basis=[s.eye(4).row(j) for j in range(4)]
    def wedge(u,v):return u.T*v-v.T*u
    H={(a,b):sum((L[p,q]*wedge(basis[2*a+p],basis[2*b+q])
                                  for p in range(2) for q in range(2)),s.zeros(4))
       for a in range(2) for b in range(2)}
    assert H[0,1]==H[1,0]
    integral=sum((s.I*residue[a,b]*H[a,b] for a in range(2) for b in range(2)),s.zeros(4))
    evaluated=sum((s.I*A[a]*B[b]/span**3*H[a,b] for a in range(2) for b in range(2)),s.zeros(4))
    assert s.simplify(integral-2*evaluated)==s.zeros(4)
    assert evaluated != s.zeros(4)
    report.check('K5-RESIDUE', 'One positive contour turn with prefactor 1/(2*pi)',
                 True, classification='symbolic-exact', result='omega_int=2*omega_0',
                 condition='span=<AB> != 0; ordinary exterior-product convention')


def diagnostic(profile):
    import numpy as np
    b = importlib.import_module('b3check')
    run_reporting_guards(diagnostic, globals())
    r=profile['max_r']; seed=profile['seed']; chir=profile['chiralities']
    b.SUMS=profile['crosscheck']
    stream=io.StringIO()
    with contextlib.redirect_stdout(stream):
        b.run(r,seed,chir)
    text=stream.getvalue()
    if len(text.encode())>200_000:raise RuntimeError('Diagnostic output bound')
    report.emit({'record':'program-output','program':'b3check.py','stdout':text})
    rows=[]
    for line in text.splitlines():
        if re.match(r'^r=\s*\d+\s+N2max=',line):
            values={k:float(v.rstrip('sMB')) for k,v in re.findall(r'([A-Za-z0-9/]+)=\s*([^\s]+)',line)}
            expected={'r','N2max','N2/r','N2full','N3max','N3/r','resL','resF3','JsHQ','sym2','dt','maxrss'}
            if set(values)!=expected or not all(np.isfinite(v) for v in values.values()):
                raise RuntimeError('Missing or nonfinite diagnostic field')
            values['r']=int(values['r']);rows.append(values)
    if [x['r'] for x in rows]!=list(range(1,r+1)):
        raise RuntimeError('Missing diagnostic order')
    tol=1e-10
    residuals={key:max(x[key] for x in rows) for key in ('resL','resF3','JsHQ','sym2')}
    ok=all(np.isfinite(v) and v<=tol for v in residuals.values())
    report.check('B-RESIDUAL-R'+str(r),'Finite float64 recursion and quadratic JstarHQ residuals',
                 ok, classification='numerical-diagnostic', tolerance=tol, maxima=residuals,norm='Unweighted Frobenius norm of coefficient arrays, not the weighted tensor norm')
    rng=np.random.default_rng(seed);labels=[]
    for c in chir:
        xi=rng.normal(size=2);xi/=np.linalg.norm(xi)
        pi=rng.normal(size=2);pi/=np.linalg.norm(pi)
        labels.append({'chirality':c,'xi':xi.tolist(),'pi':pi.tolist()})
    gain_lines=[line for line in text.splitlines() if re.match(r'^\s+t=\s*\d+',line)]
    gain_values=[float(v) for line in gain_lines for v in re.findall(r'=\s*([^\s]+)',line)]
    if r>=3 and not gain_lines:raise RuntimeError('Missing insertion table')
    report.check('B-VALUES-R'+str(r),'Sampled coherent values and restricted-slot norm estimates',
                 all(np.isfinite(v) for x in rows for v in x.values()) and all(np.isfinite(v) for v in gain_values),
                 classification='numerical-diagnostic', seed=seed, labels=labels, orders=rows,insertion_table_rows=len(gain_lines),
                 scope='Finite observations of unscaled labeled polarized coefficient sums only. Their coherent values approximate lower bounds on the corresponding polarized maps under the full '
                       'operator norms; no identification with one ordered paper coefficient is asserted. The values have float64 error. '
                       'No upper bound or convergence assertion. Insertion denominators use '
                       '40-step power estimates, not certified operator norms.')
    if not profile['crosscheck']:return
    other=capture_script('bfcheck.py',['labels',r,seed,chir])
    def sums(txt,polarized):
        out={}
        prefix='SUM ' if polarized else ''
        for line in txt.splitlines():
            if re.match('^'+prefix+r'r=\d+ co=[+-]\d',line):
                rr,co=re.search(r'r=(\d+) co=([+-]\d)',line).groups()
                out[int(rr),int(co)]=[float(v) for v in re.findall(r'\|[^|]+\|=([-+0-9.e]+)',line)]
        return out
    p=sums(text,True);q=sums(other,False)
    if set(p)!=set(q) or len(p)!=2*r or any(len(v)!=4 for v in list(p.values())+list(q.values())):
        raise RuntimeError('Incomplete route comparison')
    error=max(abs(a-bb)/max(1,abs(a),abs(bb)) for k in p for a,bb in zip(p[k],q[k]))
    report.check('B-CROSS-R4','Polarized and nilpotent routes: four printed coefficient norms',
                 np.isfinite(error) and error<=1e-5, classification='numerical-diagnostic',
                 max_scaled_difference=error,tolerance=1e-5,
                 scope='Norms of coefficient sums on the same labels; shared projection helpers. '
                       'No componentwise equality or implementation independence claimed.')
    random=capture_script('bfcheck.py',['random',4,7])
    residual=[float(x) for x in re.findall(r'max relative residual (\S+)',random)]
    levels={int(x) for x in re.findall(r'level r=(\d+)',random)}
    report.check('B-RANDOM-R4','Nilpotent recursion on one real random record prefix',
                 levels=={1,2,3,4} and bool(residual) and len(residual)==sum(line.startswith('level ') for line in random.splitlines())
                 and all(np.isfinite(v) and v<=tol for v in residual),
                 classification='numerical-diagnostic',seed=7,max_r=4,
                 maximum=max(residual) if residual else None,tolerance=tol,
                 scope='Float64 operations, including nilpotent directional derivatives; Lambda=0.')


_REPORT_GUARD_ACTIVE = False
_REPORT_GUARD_DONE = False


def _fixture():
    # These values have no mathematical interpretation. Their sole purpose is
    # to exercise the current output protocol with all twelve required fields.
    rows = [
        f'r={r:2d}  N2max=1.0 N2/r=1.0 N2full=1.0 '
        'N3max=0.0 N3/r=0.0 resL=0.0 resF3=0.0 JsHQ=0.0 sym2=0.0 '
        'dt=0.0s maxrss=1MB'
        for r in range(1, 5)
    ]
    gains = [
        f'  t={t:2d} n=1 ratio_max=0.0 (t+1)ratio=0.0 '
        'ins_after_norm_max=0.0 ins_before_norm_max=1.0 '
        'after/(|L|op|Y|)max=0.0 (t+1)x=0.0 before/(|L||Y|)max=1.0'
        for t in (1, 2)
    ]
    sums = [
        f'r={r} co={c:+d} |e0e1|=1.0 |e0e2|=1.0 |e1e2|=1.0 |e0e1e2|=0.0'
        for r in range(1, 5) for c in (1, -1)
    ]
    random = [
        f'level r={r} nilpotents=0  max relative residual 0.0'
        for r in range(1, 5)
    ]
    return {
        'main': '\n'.join(rows + gains + ['SUM ' + s for s in sums]) + '\n',
        'labels': '\n'.join(sums) + '\n',
        'random': '\n'.join(random) + '\n',
    }


def run_reporting_guards(diagnostic, namespace):
    """Reject NaN/Inf/missing fields through production guards, not a copy.

    ``namespace`` must be the actual checks module's globals(). The process is
    serial; this helper must not be used while another Python thread accesses
    the same report module or b3 module. The active flag prevents recursive self-tests
    when the production diagnostic calls this helper again.
    """
    global _REPORT_GUARD_ACTIVE, _REPORT_GUARD_DONE
    if _REPORT_GUARD_ACTIVE or _REPORT_GUARD_DONE:
        return
    if getattr(diagnostic, '__globals__', None) is not namespace:
        raise RuntimeError('The reporting guard requires diagnostic.__globals__')
    b = importlib.import_module('b3check')
    bf = importlib.import_module('bfcheck')
    reporter = namespace['report']
    original = {
        'run': b.run,
        'SUMS': b.SUMS,
        'capture_script': namespace['capture_script'],
        'check': reporter.check,
        'emit': reporter.emit,
    }
    _REPORT_GUARD_ACTIVE = True
    controls = []
    current = None
    observed = None

    def fake_run(*args, **kwargs):
        print(current['main'], end='')

    def fake_capture(name, args=()):
        if name != 'bfcheck.py' or not args or args[0] not in ('labels', 'random'):
            raise RuntimeError('Reporting fixture received an unexpected program request')
        return current[args[0]]

    def record_check(cid, title, ok, info='', **details):
        observed.append((cid, bool(ok)))

    def run_fixture(value):
        nonlocal current, observed
        current = value
        observed = []
        diagnostic({'max_r': 4, 'seed': 1, 'chiralities': '++-', 'crosscheck': True})
        return tuple(observed)

    def require_rejected(name, value):
        try:
            entries = run_fixture(value)
        except (FloatingPointError, RuntimeError, ValueError, KeyError, OverflowError) as exc:
            controls.append({'case': name, 'rejected_by': type(exc).__name__})
            return
        if any(not ok for cid, ok in entries):
            controls.append({'case': name, 'rejected_by': 'failed production report.check'})
            return
        raise RuntimeError('Reporting guard failed to reject synthetic case: ' + name)

    try:
        b.run = fake_run
        namespace['capture_script'] = fake_capture
        reporter.check = record_check
        reporter.emit = lambda value: None

        # Positive control proves that the fixture reaches all intended paths;
        # an unrelated malformed fixture must not count as a negative success.
        clean = _fixture()
        expected = ('B-RESIDUAL-R4', 'B-VALUES-R4', 'B-CROSS-R4', 'B-RANDOM-R4')
        accepted = run_fixture(clean)
        if tuple(cid for cid, ok in accepted) != expected or not all(ok for cid, ok in accepted):
            raise RuntimeError('Finite reporting fixture did not pass the production protocol')

        cases = [
            ('order-row-nan', 'main', 'N2max=1.0', 'N2max=nan'),
            ('order-row-inf', 'main', 'N2full=1.0', 'N2full=inf'),
            ('missing-order-field', 'main', ' N3max=0.0', ''),
            ('insertion-table-nan', 'main', 'ratio_max=0.0', 'ratio_max=nan'),
            ('insertion-table-inf', 'main', 'ins_before_norm_max=1.0', 'ins_before_norm_max=inf'),
            ('random-residual-nan', 'random', 'max relative residual 0.0', 'max relative residual nan'),
            ('random-residual-inf', 'random', 'max relative residual 0.0', 'max relative residual inf'),
        ]
        for name, field, before, after in cases:
            value = dict(clean)
            if before not in value[field]:
                raise RuntimeError('Invalid reporting fixture mutation: ' + name)
            value[field] = value[field].replace(before, after, 1)
            require_rejected(name, value)

        # The entry is absent, rather than malformed or nonfinite.
        missing_table = dict(clean)
        missing_table['main'] = '\n'.join(
            line for line in clean['main'].splitlines() if not line.startswith('  t=')
        ) + '\n'
        require_rejected('missing-insertion-table', missing_table)

        # Directly exercise each real pre-max guard. This never calls bf.main
        # and does not evaluate the polynomial recursion.
        for module in (b, bf):
            if module._checked_float(1.25) != 1.25:
                raise RuntimeError('Finite scalar rejected by production _checked_float')
            for token in ('nan', 'inf', '-inf'):
                try:
                    module._checked_float(token)
                except FloatingPointError:
                    controls.append({'case': module.__name__ + '-scalar-' + token,
                                     'rejected_by': 'FloatingPointError'})
                else:
                    raise RuntimeError('Production _checked_float accepted ' + token)
    finally:
        b.run = original['run']
        b.SUMS = original['SUMS']
        namespace['capture_script'] = original['capture_script']
        reporter.check = original['check']
        reporter.emit = original['emit']
        _REPORT_GUARD_ACTIVE = False

    _REPORT_GUARD_DONE = True
    original['emit']({
        'record': 'reporting-guard-regression',
        'classification': 'reporting-negative-control',
        'status': 'PASS',
        'positive_control': 'All four real diagnostic reporting paths accepted finite synthetic text',
        'negative_controls': controls,
        'mathematical_programs_called': False,
        'new_registered_check_ids': False,
        'scope': 'Production parser and scalar-guard rejection only; not a mathematical check.',
    })

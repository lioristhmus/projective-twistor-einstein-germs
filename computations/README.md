# Computational supplement for local analytic Einstein germs

Local release candidate **0.2.0**, revision 3, accompanying Lior Isthmus, *A projective twistor
correspondence for local analytic Einstein germs*, paper v1.0. The target is
tag `paper-v1.0` at commit `6880bc1085d7faf4dd67c3dd4ef2331126878fb7` of
[the paper repository](https://github.com/lioristhmus/projective-twistor-einstein-germs).
The fixed source and artifact hashes are in [BASELINE.json](BASELINE.json).
This revision is fixed locally for submission/review; it has not been published. Claude completed an independent audit of 0.1.0 and the three added calculations. That audit and its final recommendations have been reconciled here. It was not a line-by-line audit of the final 0.2.0 code; see [REVIEW-STATUS.json](REVIEW-STATUS.json) and [RECONCILIATION.md](RECONCILIATION.md).

The supplement provides reproducible finite checks of selected formulas in
Section 9 and Appendices A/B, D.2 and K, plus numerical diagnostics for the record recursion. It does
not certify the paper's complete analytic or categorical arguments. The twenty-eight registered
records comprise twenty exact checks tied to paper formulas, two external-source
exact comparisons, four numerical residual/crosschecks and two numerical observation
records. The latter test data integrity and do not verify an inequality. [REVIEW-STATUS.json](REVIEW-STATUS.json) records the current independent-review status. The order-one Kasner run is a resource pilot contained in the
order-three test, not an independent geometric example. The exact A/B order-one pilot similarly overlaps the order-four profile.

- [CHECKS.md](CHECKS.md) and [checks.json](checks.json) map every check to stable
  manuscript anchors, explicit formulas, inputs and exclusions.
- [CONVENTIONS.md](CONVENTIONS.md) fixes spinor, curvature and metric conventions.
- [inputs.json](inputs.json), [jobs.json](jobs.json) and [code/](code/) contain the
  input profiles and executable definitions. Symbolic inputs are embedded in the
  listed scripts; no manuscript parser or external download supplies them at run time.
- [RUNS.md](RUNS.md) and [results/](results/) record the fresh runs, actual
  resource limits, source/input hashes, output, exit state and cleanup.
- [provenance.json](provenance.json) identifies inherited scripts and changes.
- [CHANGES.md](CHANGES.md) explains corrected scope and guards;
  [NEW-CHECKS.md](NEW-CHECKS.md) gives the three added calculations.
- [environment.lock.json](environment.lock.json), [LICENSES.md](LICENSES.md) and
  [SHA256SUMS.txt](SHA256SUMS.txt) specify the runtime, licenses and file integrity.

The fresh runs use SageMath 10.9, SymPy 1.14.0, NumPy 2.4.4 and Python 3.12.3 in
the pinned Docker image. Sage's rational number fields and exact symbolic
expressions are used for the exact checks. Appendix B diagnostics use float64.
All primary retained results in `results/` are new executions of the distributed
mathematical code. Historical logs are not relabeled as new results.

## Reproduction

Install Docker and provide the already installed image identified by
[environment.lock.json](environment.lock.json). The runner never pulls an image,
builds one, or changes VM/service limits. The host requires Python 3.9 or later
with its standard library; mathematical libraries run only in the container.
The image is Linux/amd64. Running it on an ARM host requires Docker's existing
amd64 execution support, as in the saved environment records.

From this directory, run one job at a time:

```sh
python3 code/run.py --job ab-r1 --out reproduced/ab-r1
python3 code/run.py --job ab-r4 --out reproduced/ab-r4
python3 code/run.py --job s9-two-wave --out reproduced/s9-two-wave
python3 code/run.py --job d2-schwarzian --out reproduced/d2-schwarzian
python3 code/run.py --job kasner-r1 --out reproduced/kasner-r1
python3 code/run.py --job kasner-r3 --out reproduced/kasner-r3
python3 code/run.py --job schwarzschild --out reproduced/schwarzschild
python3 code/run.py --job adamo --out reproduced/adamo
python3 code/run.py --job b-low4 --out reproduced/b-low4
python3 code/run.py --job b-low8 --out reproduced/b-low8
```

Each output directory must be new. A failed run is not retried automatically.
Run the order-one and order-four pilots first and examine their resource
records before using the larger profiles. No concurrent mathematical job is
permitted, including work from another session or executor.

The machine-wide lock is `$HOME/.local/state/math-job.lock`, acquired atomically
with `mkdir`. Its parent must already exist. Every mathematical executor on the
machine must use this same lock. An existing lock blocks execution and is never
removed by this runner. Only the runner's own lock is removed, after termination
and removal of its container have been confirmed.

Existing running containers block execution by default. Known nonmathematical
services can be identified explicitly by repeated `--allow-service NAME`
arguments. The runner records their limits and current resource use; this option
does not authorize concurrent mathematical work. Service identities are replaced
by numbered aliases in distributed environment records.

Each container has a read-only root and input mount, network `none`, one CPU,
at most 1,999,998,976 bytes of memory plus swap, zero swap, at most 32 PIDs,
OOM killing enabled and no restart. Temporary filesystems total 256 MiB.
Files and captured output have a 1 MiB limit; Docker logs are separately bounded.
The command receives TERM after 117 seconds and KILL three seconds later.
An outer PID1 timeout and the host's 300-second deadline bound the container;
abnormal completion causes the entire container to be killed and inspected.
Actual cgroup and network checks precede mathematical imports. No writable host
output mount is exposed to the mathematical program.

To test failure handling, use a new directory:

```sh
python3 code/run.py --job failure-probe --out reproduced/failure-probe
```

This must return a nonzero exit and store `RUNNER-FAILURE-PROBE: FAIL`. The saved
intentional failure is a runner test, excluded from the twenty-eight registered
record IDs. Exceptions, missing or duplicate IDs, failed checks, OOM, timeouts and
unconfirmed cleanup also force a nonzero result.

## Interpretation

The Kasner tests compare geometrically differentiated curvature with the
normalized Spencer commutator identity at one fixed vacuum metric through order
three. They now check $Q_0=0$ explicitly. Their $HQ$ is differentiated geometrically,
so these tests do not exercise the polynomial product-rule implementation or
independent complex chiral lists. The A/B additions instead apply that product
rule to a declared rational mixed family of independent free records through
order four, verify exact-set compatibility and free projection, and test all
basis vectors of the corresponding finite Spencer maps. Their admissibility
and coefficient-algebra scope are detailed in [NEW-CHECKS.md](NEW-CHECKS.md).

The Section 9 job derives Ricci for arbitrary $f(u),q(x)$, then distinguishes the
specified mixed repair in $\mathbb C[t,s]/(t^2,s^2)$ from its nonzero unrestricted
residual. The D.2 job retains matrix multiplication order in a formal chain-rule
identity and checks a noncommuting rational symmetric matrix example. Conditional
normalization/Jacobi algebra is checked; analytic ODE existence is not executed.
Schwarzschild and source-primitive identities remain local-chart calculations;
they do not execute analytic continuation or global gluing algorithms.

The Appendix B floating-point programs measure **unscaled labeled polarized
coefficient sums**, rather than a code-identified single ordered coefficient
$B^{[d]}_{r,\mathbf j}$ of the paper. For those measured polarized maps, unit
coherent values are lower values for their full operator norms in exact
arithmetic; the saved values have float64 error. Record-order factorials do not
remove polynomial polarization factors. No bridge identifying these maps with
one ordered coefficient is asserted. Restricted-slot singular values and
40-step power estimates are numerical quantities, not certified norm bounds.
The residual tables use unweighted coefficient-array norms, separately from the
weighted tensor norm used for sampled coefficient values. Shared projection
helpers prevent the second recursion route from being an independent
implementation of those helpers. [CONVENTIONS.md](CONVENTIONS.md) gives details.

General differentiated Bianchi completion, analytic realization, atomic diagram
masses, the all-order insertion estimate, Theorem B.4 and convergence remain
mathematical arguments. The selected tests do not certify the entire paper.

## Integrity and licensing

```sh
python3 code/verify_package.py
```

This host-side command checks file hashes, saved result IDs, execution/source
correspondence, local links and privacy patterns. It does not rerun mathematics
or validate the paper's proofs. The saved [QA.json](QA.json) is document/package
QA, separate from the mathematical checks. Rerun outputs belong in a separate
directory and are not part of the frozen package checksum list.

Code is licensed under Apache-2.0; inputs, results and documentation under
CC BY 4.0. See [LICENSES.md](LICENSES.md). External runtimes and the external
Adamo article are not bundled. There is no separate supplement DOI.

## Independent geometric calibration in revision 3

[INDEPENDENT-EVIDENCE.md](INDEPENDENT-EVIDENCE.md) separates one fresh, source-bound
finite witness group from the 28 primary records and from historical audit logs.
It uses Claude's unchanged independent implementation plus a new adapter that
turns the specified sign, Lambda and non-Einstein distinctions into actual PASS
conditions. It never calls the primary A/B backend. Reproduce it with:

    python3 independent/code/run.py --job witness-r2 --out reproduced/independent-witness-r2

The same machine-wide lock and resource/cleanup rules apply. The correct
recursion agrees with five Einstein witnesses through order two; two
non-Einstein metrics retain the geometric Ricci identity but fail Q0 and
polynomial/geometric agreement. Sign reversal is detected on Kasner, Kottler
and the mixed-wave r2+ output; doubling the Lambda coefficient is detected on
Kottler and remains invisible on Lambda-zero witnesses, as expected.

The r>=1 comparison inside the old Kasner check is a geometric Ricci identity
and holds on non-Einstein metrics too. Its original non-vacuum demonstration
removed the vacuum assertions; the current Kasner job separately checks vacuum
conditions and Q0=0. It is not claimed to pass as a whole on a non-Einstein metric.

The primary 320-component signed readout fixes its linear Lambda-zero
Weyl-to-curvature map; compatibility alone cannot fix an independently changed
curvature-action sign. The independent witnesses connect a different
implementation to coordinate geometry. A direct geometric witness comparison
using primary code/ab_exact.py remains outside this package's scope.

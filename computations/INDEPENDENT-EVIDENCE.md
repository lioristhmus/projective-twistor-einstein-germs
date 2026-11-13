# Independent geometric witness evidence

The revision-3 group IW-GEOMETRY-CONTROLS-R2 is separately registered in
[checks.json](checks.json). Its
[adapter](independent/code/witness_controls.py) calls Claude's unchanged
[T3 implementation](independent/code/t3_recursion.py). It never imports
primary code/ab_exact.py. The library and preflight source are byte-identical
to the auditor's final files; the adapter and its fresh execution are new.

The library uses sparse generating polynomials over exact rational arithmetic,
metric jets, coordinate connection/curvature and covariant derivatives,
a constant rational null frame with eta=epsilon tensor epsilon, and the
paper's signed readout and averaged symmetrization. It rebuilds R_U from
the read-out U0 plus Lambda/3 and evaluates the actual polynomial product
rule. The adapter fixes rmax=2, kmax=3 and jet truncation order 5, providing
the derivatives needed for Q2.

## Enforced finite results

| Metric / control | Fresh result through r=2 |
| --- | --- |
| Vacuum Kasner (-2/7,3/7,6/7), t=1, complexified x2 | Lambda=0, Q0=0 and polynomial/geometric Q agree; sign flip mismatches 12 and 40 in each chirality |
| Exact mixed wave F=t(u+s x^2 v/2)^3, q=x^2, t=3,s=5 at (1,2,1,0) | Q0=0 and agreement; sign flip detected in r2+ (2 entries), not required in the insensitive outputs |
| Single wave t=3,s=0 / t=0,s=5 | Q0=0 and agreement; nonzero U0 occurs only in opposite chiralities |
| Kottler m=1, lambda_std=1/10, r=3, cos(theta)=1/3, complexified phi | Einstein constant Lambda=-1/10, Q0=0 and agreement; sign flip and doubled Lambda coefficient each mismatch 4 and 8 entries per chirality |
| Non-Einstein Kasner (1/2,1/3,1/5) | Q0 nonzero; polynomial/geometric mismatches 20 and 40 per chirality |
| Non-Einstein trial F=t u^3, q=x^2, t=3,s=5 | Q0 nonzero; mismatches 2 and 4 per chirality |

Every metric, including the two non-Einstein controls, passes the geometric
Ricci identity. Doubling the Lambda coefficient gives zero mismatches on
the Lambda-zero Kasner/mixed-wave witnesses, as expected. These insensitive
cases are explicitly distinguished from successful detection.
The compared-entry counts use unions of sparse dictionary keys; components
zero in both representations are implicit.

All the stated distinctions are require/exception gates in the adapter
before its single PASS record. The library's original printed counts alone
are not called enforced controls. Correct witness agreement is also asserted
inside the original library. The source guards, report location and exclusions
are mapped in checks.json.

## Execution and safety

Reproduce from the package root with a new output directory:

    python3 independent/code/run.py --job witness-r2 --out reproduced/independent-witness-r2

Known nonmathematical services require the explicit allow-service options
described in the main [README](README.md). The independent execution root
retains its own jobs, inputs and dependency hashes, so the primary runtime
files and all ten primary runs remain unchanged from r2.

The [environment](independent/results/witness-r2/environment.json) binds
all nine executed source/input files. The
[result](independent/results/witness-r2/result.json) binds the exact
[log](independent/results/witness-r2/log.jsonl).
The same pinned SageMath image and unchanged controller/worker/report code
enforce the common mkdir lock, one CPU, memory+swap 1,999,998,976 bytes,
swap zero, PID32, network none, read-only mounts, bounded files/logs,
OOM enabled, no restart, inner 117+3 seconds and outer 300-second deadline.
The fresh job took 10.006 controller seconds, with cgroup peak memory
37,982,208 bytes; no OOM/timeout occurred. Container removal and owned-lock
release were confirmed.

## Historical audit and remaining limits

The original [symbolic r<=4 log](independent/prior-audit/t3_algebra_r4.log)
and [Kasner r<=4 / other witnesses r<=3 log](independent/prior-audit/t3_witness_r3_k4.log)
are retained as historical audit evidence. The auditor states they used the
final source. Their old execution format does not attest all executed input
digests, so current file hashes do not independently prove that old byte-level
attribution. [PROVENANCE](independent/prior-audit/PROVENANCE.json) records
this limit. They are not new accepted runs or extra primary check IDs.
Upstream comments predicting that every wrong convention must break
compatibility are superseded by the actual logs: NC1 and NC3 do not.

The new finite witness group connects the independent T3 recursion to
coordinate geometry. It does not execute or directly calibrate primary
ab_exact.py against those metrics. Its nonzero-Lambda result is not a
nonzero-Lambda extension of that primary backend. The primary 320-component
readout remains a separate linear Lambda-zero calibration.
No arbitrary Einstein-input theorem, general differentiated Bianchi
completion, analytic realization, atomic mass, all-order insertion estimate,
Theorem B.4 or convergence follows from these finite checks.


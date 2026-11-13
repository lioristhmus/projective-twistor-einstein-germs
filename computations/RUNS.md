# Fresh execution record

All ten mathematical jobs were freshly executed for candidate 0.2.0. Earlier
0.1.0 results are not relabeled as new runs. The order-one pilots overlap their
larger profiles. The table's check counts do not measure independent proofs.

| Job | Status | IDs | Controller seconds | Worker seconds | Cgroup memory peak (bytes) |
| --- | --- | ---: | ---: | ---: | ---: |
| [failure-probe](results/failure-probe/result.json) | FAIL (intentional) | 1 | 9.272 | 0.013 | 30384128 |
| [kasner-r1](results/kasner-r1/result.json) | PASS | 1 | 12.346 | 2.932 | 222822400 |
| [kasner-r3](results/kasner-r3/result.json) | PASS | 1 | 14.367 | 5.004 | 261419008 |
| [schwarzschild](results/schwarzschild/result.json) | PASS | 3 | 10.563 | 1.27 | 73211904 |
| [adamo](results/adamo/result.json) | PASS | 5 | 13.342 | 3.927 | 270704640 |
| [b-low4](results/b-low4/result.json) | PASS | 4 | 9.723 | 0.465 | 83251200 |
| [b-low8](results/b-low8/result.json) | PASS | 2 | 10.097 | 0.825 | 80461824 |
| [ab-r1](results/ab-r1/result.json) | PASS | 3 | 12.046 | 2.707 | 235491328 |
| [ab-r4](results/ab-r4/result.json) | PASS | 3 | 30.296 | 20.968 | 601837568 |
| [s9-two-wave](results/s9-two-wave/result.json) | PASS | 3 | 9.511 | 0.325 | 69451776 |
| [d2-schwarzian](results/d2-schwarzian/result.json) | PASS | 3 | 13.015 | 3.8 | 75726848 |

The environment records contain actual Docker limits, in-container cgroup and
network checks, pinned image/library versions, VM capacity, anonymized service
limits/use, source/input hashes and confirmed container termination/removal and
owned-lock release. No accepted run was OOM-killed or timed out. Limits and
existing services were not changed.

The new A/B order-four run covers 880 finite Spencer basis vectors and 7,040
top-level scalar amplitude coefficients; repeated recursive scalar tests are
not counted as independent identities. Its mixed cubic coefficient and the
lowest unscaled polarized sum are explicitly nonzero. The exact Section 9
job retains the nonzero unrestricted repaired Ricci residual, while proving
zero in the specified parameter quotient. D.2 retains noncommuting matrix order
and a noncommuting rational example.

The two `AASS-*` IDs are external-source algebraic comparisons, not verification of local-paper statements. The two `B-VALUES-*` IDs track numerical observations and their integrity; they are not budget inequalities. Their stable IDs are retained for traceability, separately from the twenty paper-exact checks and four numerical residual/crosschecks.

The inherited floating-point programs retain their finite seed-one, Lambda-zero,
degree-two/three scope through order eight. They report polarized coefficient
sums and unweighted coefficient-array residuals. Their values do not certify
an ordered coefficient upper bound, atomic mass or convergence. The direct
four-norm cross-route comparison is not componentwise equality.

Both numerical runs execute production-parser regression controls: a finite
positive fixture and fourteen rejected NaN/Inf/missing-field cases. Their log
records are classified `reporting-negative-control`, not mathematical check IDs.
The intentional `RUNNER-FAILURE-PROBE` returns nonzero and FAIL as required;
it is also excluded from the twenty-eight registered record IDs.

Two failed preacceptance A/B trials and earlier intermediate successful runs
were preserved locally. Only final source-matched accepted results are in this
package; [CHANGES.md](CHANGES.md) and [provenance.json](provenance.json) explain
the arithmetic-type correction. Fresh execution does not complete independent
review: see [REVIEW-STATUS.json](REVIEW-STATUS.json).

## Final integration, revision 3

The ten primary runs and their complete code/input dependency set remain
byte-identical to r2; they were not rerun merely to change review metadata.
One additional source-bound group, IW-GEOMETRY-CONTROLS-R2, ran in its separate
independent execution root, with the same pinned image, runner and limits.
It completed without OOM or timeout, and container removal and lock release
were confirmed. See [the result](independent/results/witness-r2/result.json)
and [environment](independent/results/witness-r2/environment.json).
The upstream printed convention counts are now enforced by the adapter only
at the declared r<=2 witnesses; no historical run is relabeled.

Claude's completed audit covers 0.1.0 and the three additional calculations.
Its higher-order symbolic/witness logs are retained as historical independent
audit evidence with their attribution limits. The final 0.2.0 code did not
receive a full independent line audit. The primary scoped source audit,
targeted independent adapter review and final package QA are separate.

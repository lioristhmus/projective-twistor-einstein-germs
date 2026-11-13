# Check-to-paper and code correspondence

The 28 primary records below retain their stable IDs. Exact paper checks and finite numerical specializations are tied to the fixed source in [BASELINE.json](BASELINE.json); external comparisons and observation records have context-only anchors. [checks.json](checks.json) maps actual assertions, inputs, exclusions and report predicates. [MANUSCRIPT-LOCATORS.json](MANUSCRIPT-LOCATORS.json) contains exact source blocks and hashes, not executed proofs.

| ID | Type / evidence role | Paper anchors | Code / result |
| --- | --- | --- | --- |
| KASNER-R1 | finite-exact / paper-exact-check | lem:gg-budget-spencer; eq:gg-budget-actual-recursion | [code](code/kasner_exact.py), [result](results/kasner-r1/result.json) |
| KASNER-R3 | finite-exact / paper-exact-check | lem:gg-budget-spencer; eq:gg-budget-actual-recursion | [code](code/kasner_exact.py), [result](results/kasner-r3/result.json) |
| SCH-RICCI | symbolic-exact / paper-exact-check | eq:sh-scale-a2; eq:sh-scale-a3 | [code](code/schwarzschild_exact.py), [result](results/schwarzschild/result.json) |
| SCH-SCREEN | symbolic-exact / paper-exact-check | eq:sh-optics-d-10; eq:gg-schwarzschild-main-tide; sec:sh-optics-3 | [code](code/schwarzschild_exact.py), [result](results/schwarzschild/result.json) |
| SCH-CONFORMAL | symbolic-exact / paper-exact-check | prop:sh-scale-1; prop:sh-scale-2; eq:sh-scale-a15; eq:sh-scale-a16; eq:sh-scale-a7; eq:sh-scale-a13; eq:sh-scale-a14 | [code](code/schwarzschild_exact.py), [result](results/schwarzschild/result.json) |
| AASS-ALGEBRA | symbolic-exact / external-exact-comparison | context: sec:sh-r1-primitive-comparison | [code](code/adamo_exact.py), [result](results/adamo/result.json) |
| AASS-PRINTED-CURVATURE | symbolic-exact / external-exact-comparison | context: sec:sh-r1-primitive-comparison | [code](code/adamo_exact.py), [result](results/adamo/result.json) |
| K5-PROJECTOR | symbolic-exact / paper-exact-check | prop:sh-r1-primitive-tensor; eq:sh-r1-primitive-projector; eq:sh-r1-general-source-metric | [code](code/adamo_exact.py), [result](results/adamo/result.json) |
| K5-EF | symbolic-exact / paper-exact-check | prop:gg-schwarzschild-primitive-comparison; thm:sh-r1-calibrated-horizon-map; eq:sh-r1-calibrated-pullback | [code](code/adamo_exact.py), [result](results/adamo/result.json) |
| K5-RESIDUE | symbolic-exact / paper-exact-check | prop:sh-r1-primitive-tensor; eq:sh-r1-residue; eq:sh-r1-contour-value | [code](code/checks.py), [result](results/adamo/result.json) |
| B-RESIDUAL-R4 | numerical-diagnostic / finite-numerical-residual-or-crosscheck | lem:gg-budget-spencer; eq:gg-budget-actual-recursion | [code](code/b3check.py), [result](results/b-low4/result.json) |
| B-VALUES-R4 | numerical-diagnostic / numerical-observation-record | context: lem:gg-budget-transfers; thm:gg-budget-coefficients | [code](code/b3check.py), [result](results/b-low4/result.json) |
| B-RESIDUAL-R8 | numerical-diagnostic / finite-numerical-residual-or-crosscheck | lem:gg-budget-spencer; eq:gg-budget-actual-recursion | [code](code/b3check.py), [result](results/b-low8/result.json) |
| B-VALUES-R8 | numerical-diagnostic / numerical-observation-record | context: lem:gg-budget-transfers; thm:gg-budget-coefficients | [code](code/b3check.py), [result](results/b-low8/result.json) |
| B-CROSS-R4 | numerical-diagnostic / finite-numerical-residual-or-crosscheck | lem:gg-budget-spencer; eq:gg-budget-actual-recursion | [code](code/bfcheck.py), [result](results/b-low4/result.json) |
| B-RANDOM-R4 | numerical-diagnostic / finite-numerical-residual-or-crosscheck | lem:gg-budget-spencer; eq:gg-budget-actual-recursion | [code](code/bfcheck.py), [result](results/b-low4/result.json) |
| AB-PROJECTORS-R1 | finite-exact / paper-exact-check | lem:gg-budget-spencer; eq:gg-budget-spencer-spectrum; eq:gg-budget-actual-recursion | [code](code/ab_exact.py), [result](results/ab-r1/result.json) |
| AB-WEYL-ADMISSIBILITY-R1 | finite-exact / paper-exact-check | eq:gg-weyl-spinor-decomposition; eq:gg-weyl-spinor-readout; prop:gg-polynomial-completion | [code](code/ab_exact.py), [result](results/ab-r1/result.json) |
| AB-EXACT-SET-R1 | finite-exact / paper-exact-check | prop:gg-polynomial-completion; prop:gg-formal-normal-uniqueness; eq:gg-budget-actual-recursion | [code](code/ab_exact.py), [result](results/ab-r1/result.json) |
| AB-PROJECTORS-R4 | finite-exact / paper-exact-check | lem:gg-budget-spencer; eq:gg-budget-spencer-spectrum; eq:gg-budget-actual-recursion | [code](code/ab_exact.py), [result](results/ab-r4/result.json) |
| AB-WEYL-ADMISSIBILITY | finite-exact / paper-exact-check | eq:gg-weyl-spinor-decomposition; eq:gg-weyl-spinor-readout; prop:gg-polynomial-completion | [code](code/ab_exact.py), [result](results/ab-r4/result.json) |
| AB-EXACT-SET-R4 | finite-exact / paper-exact-check | prop:gg-polynomial-completion; prop:gg-formal-normal-uniqueness; eq:gg-budget-actual-recursion | [code](code/ab_exact.py), [result](results/ab-r4/result.json) |
| S9-WAVE-RICCI | symbolic-exact / paper-exact-check | eq:gg-two-wave-trial; eq:gg-two-wave-christoffels; eq:gg-two-wave-ricci | [code](code/two_wave.py), [result](results/s9-two-wave/result.json) |
| S9-MIXED-COTTON | symbolic-exact / paper-exact-check | eq:gg-mixed-cotton | [code](code/two_wave.py), [result](results/s9-two-wave/result.json) |
| S9-MIXED-REPAIR | symbolic-exact / paper-exact-check | eq:gg-mixed-explicit-repair | [code](code/two_wave.py), [result](results/s9-two-wave/result.json) |
| D2-MATRIX-CHAIN-RULE | symbolic-exact / paper-exact-check | eq:gg-intrinsic-matrix-schwarzian; eq:gg-intrinsic-projective-covariance | [code](code/schwarzian_exact.py), [result](results/d2-schwarzian/result.json) |
| D2-JACOBI-ALGEBRA | symbolic-exact / paper-exact-check | eq:gg-intrinsic-jacobi-normalization; eq:gg-intrinsic-jacobi-identities; eq:gg-intrinsic-schwarzian-conjugacy | [code](code/schwarzian_exact.py), [result](results/d2-schwarzian/result.json) |
| D2-RATIONAL-MATRIX | symbolic-exact / paper-exact-check | eq:gg-intrinsic-matrix-schwarzian; eq:gg-intrinsic-jacobi-normalization; eq:gg-intrinsic-jacobi-identities; eq:gg-intrinsic-schwarzian-conjugacy; eq:gg-intrinsic-projective-covariance | [code](code/schwarzian_exact.py), [result](results/d2-schwarzian/result.json) |

Primary roles: 20 paper-exact checks, two external exact comparisons, four numerical residual/crosschecks and two numerical observation records. B-VALUES PASS means finite complete data only. Overlapping pilots and shared implementations are not independent proofs.

KASNER-R1/R3 attribute only the Spencer inverse/geometric specialization of recursion lines 1-3 to their r>=1 residual comparisons. Those comparisons hold on non-Einstein metrics too. Their vacuum and Q0 checks remain separate; the full five-line polynomial recursion is not tested by geometric HQ.

## Separate independent evidence

| ID | Role | Scope | Code / result |
| --- | --- | --- | --- |
| IW-GEOMETRY-CONTROLS-R2 | finite-exact / independent-implementation-witness | Seven metrics, r<=2; positive agreement and enforced convention/non-Einstein controls; primary A/B code not called | [adapter](independent/code/witness_controls.py), [result](independent/results/witness-r2/result.json) |

The extra evidence group is not added to the 28 primary-record count. Historical audit logs and package/reporting QA have separate roles. No atomic-mass inequality, all-order gain, analytic realization, convergence or categorical equivalence is certified by these finite computations.

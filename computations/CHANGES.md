# Changes from candidate 0.1.0

Candidate 0.1.0 and its archive are preserved. The fixed paper v1.0 is unchanged.
This version adds scoped exact calculations for Section 9, Appendix D.2 and
Appendices A/B; see [NEW-CHECKS.md](NEW-CHECKS.md).

The paper-to-code audit made these corrections:

- Numerical `F2` and `F3` values are identified as unscaled labeled polarized
  coefficient sums. Their norm interpretation concerns those maps, not a
  separately identified single ordered coefficient of Appendix B.
- Residual diagnostics are described in their actual unweighted coefficient
  norm. The quadratic `JstarHQ` diagnostic is named directly, rather than
  described as an explicit all-degree free-projection check.
- Nonfinite scalars are rejected before maxima or conditional denominators;
  every required table field and every printed residual is parsed. Insertion
  tables are checked for finiteness. Production-parser regression controls
  include a valid synthetic record and fourteen rejected NaN/Inf/missing-data
  cases; these are reporting QA, separate from mathematical results.
- The Schwarzschild rotational Jacobi calculation derives radial acceleration
  from the computed Christoffels and differentiates the amplitude. The scalar
  Laplacian uses the computed metric determinant/inverse, and all three tractor
  parallel equations are checked in the declared negative-signature auxiliary
  metric. The screen calculation still excludes $f=0$ in its literal velocity
  formula and covers only the polar component.
- The Kasner test explicitly checks $Q_0=0$. Its later $HQ$ is identified as a
  geometric derivative, whereas the new A/B test implements the polynomial
  product rule on independent free inputs. The Kasner chiral records are
  conjugate on the real input and are not advertised as independent lists.
- The actual K.5 wedge expression is compared to the adopted bilinear component
  matrix. The projector trace and $J^2=-I$ are also asserted. External Adamo
  equation (2.13) remains a scalar-coefficient comparison; its result field is
  named accordingly. The Schwarzschild Ricci index no longer suggests that the
  general-lapse static formula was executed.

Two preacceptance trials of the new A/B backend failed when NumPy/Sage scalar
coercion introduced floating-point values into intended rational arrays.
The source and outputs were preserved locally and not counted as accepted
checks. Explicit per-element rational scaling and type assertions corrected
the implementation. No floating tolerance was substituted for exact zero.
This implementation failure did not exhibit a counterexample to the paper.

All adopted mathematical outputs are fresh executions bound to their actual
code and input hashes. Review status is recorded separately in
[REVIEW-STATUS.json](REVIEW-STATUS.json); successful execution is not independent
proof review or publication.

The A/B algebraic input check also inverts the signed Weyl readout on all ten quartic basis inputs. This tests the curvature normalization separately from the recursion compatibility residual, which can be insensitive to a consistent parameter rescaling.

## Revision 3: final secondary-audit reconciliation

The old candidate directory and both provisional ZIPs remain preserved.
All primary mathematical code, inputs, jobs and accepted runs are unchanged.
F1-F7 and the final Section 6 recommendations are dispositioned in
[RECONCILIATION.md](RECONCILIATION.md). Stale pending-review descriptions refer
only to the preserved r2 state.

This revision makes the Einstein-insensitivity of the r>=1 geometric Kasner
comparison explicit. It keeps the vacuum/Q0 checks, the existing corrected
Jacobi calculation, external/observation roles, B-CROSS content, and the exact
norm/polarization distinctions. It adds one separately attributed independent
witness group with enforced r<=2 convention/non-Einstein controls. It does not
upgrade primary ab_exact.py to a metric-witness or nonzero-Lambda test.
No manuscript changes or publication are part of this integration.

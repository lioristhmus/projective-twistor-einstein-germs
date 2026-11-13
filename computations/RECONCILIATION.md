# Final disposition of the independent audit

Claude's completed REVIEW, CHECK-MAPPING and Japanese summary audit frozen
0.1.0 and independently derive/execute the three requested additions. Their
final content and selected source/log hashes are recorded in
[provenance.json](provenance.json). The chief reconciled those findings with
the actual r2 source and saved runs. This is not a new full independent line
audit of final 0.2.0 code, nor human peer review.

## Findings F1-F7

| Finding | Disposition | Final evidence and limit |
| --- | --- | --- |
| F1: Kasner label exceeds the geometric calculation | Adopted; wording completed in r3 | The r>=1 comparison uses geometric R and geometric HQ and holds on non-Einstein metrics. The old non-vacuum demonstration removed the vacuum assertions. Current Kasner jobs additionally check vacuum and Q0=0. Only the geometric specialization of recursion lines 1-3 is attributed to their residuals. Primary A/B separately executes the actual polynomial product rule on its declared finite input family. Independent geometry is separate below. |
| F2: rotational Jacobi assertion was tautological | Already corrected and rerun in r2 | The distributed Schwarzschild code derives radial acceleration from Christoffels and differentiates the amplitude. No duplicate code change in r3. The polar screen/domain exclusions remain. |
| F3: Schwarzschild anchors overstate coverage | Already corrected in r2 | SCH-RICCI no longer targets the arbitrary-lapse static formula. SCH-SCREEN targets the polar tide and parallel polar screen. Claude's broader general-lapse/second-screen results are supporting audit findings, not primary executed checks here. |
| F4: AASS checks do not verify local-paper statements | Already corrected in r2 | Two external-exact-comparison records with context-only anchors; excluded from 20 paper-exact checks. Claude did not re-audit external TeX transcription; that limitation remains. |
| F5: B-VALUES verifies finiteness rather than a budget inequality | Core finding adopted; existing role retained | Stable IDs and raw PASS remain solely for completeness/finiteness of observation data. They are numerical-observation-records, not mathematical inequality checks. Suppressing the IDs/PASS gate was not adopted because it would remove integrity tracking; the meaning is explicit. |
| F6: B-CROSS has limited effective content | Already corrected in r2 | 32 printed norm pairs, 15 at most 1.2e-16 on both routes, 17 outside, one degree-three pair outside. Shared projection helpers and norm-only comparison are disclosed. No additional code change. |
| F7: signature, Laplacian, K.5 and numerical scope | Adopted where relevant; residual scope retained | r2 added the metric-volume Laplacian, rho and third tractor equation, actual wedge/component bridge, trace P=2 and J^2=-I. K5-EF still starts from a polar source tensor, not an executed Cartesian Jacobian; density-root/spin transport is not determined by a squared metric identity. Lambda=0, mixed labels, norm and polarization limits remain. |

None of these findings required a manuscript change. The failed early
second-screen nan and K.5 q-power/syntax attempts were auditor implementation
issues corrected in the final runs; they are not counterexamples to the
paper and are not accepted successful runs.

## Final Section 6 recommendations

1. **Kasner labeling: adopted.** README, CHECKS, checks.json and CONVENTIONS
   now explicitly separate the Einstein-insensitive geometric comparison,
   current vacuum/Q0 conditions, and actual polynomial product rule.
2. **Curvature sign and Lambda normalization: adopted with separate roles.**
   The final audit's observation that compatibility alone cannot calibrate
   these conventions is correct. Its comments about the primary linear
   Weyl map partly predate the r2 320-component signed inverse readout:
   that readout already fixes the abstract linear map at Lambda=0.
   It does not test an isolated sign change in the curvature action against
   coordinate geometry. Claude's algebraic C0 readout/Ricci test also fixes
   abstract normalization. Geometric witnesses add a different connection
   to independently calculated metric curvature. Revision 3 adopts a
   source-bound independent witness group through r=2, with enforced
   convention/non-Einstein controls. It does not execute primary ab_exact.py.
   The direct primary-backend metric bridge and primary nonzero-Lambda
   implementation remain outside the executed scope, rather than being
   silently declared complete.
3. **B-CROSS effective content: already resolved in r2.** Claude's
   "unchanged" description refers to an earlier candidate snapshot;
   current r2 already states 17/32 and the single cubic norm pair.
4. **Optional extra formulas: outside the selected finalization scope.**
   Full second Sachs transport, arbitrary-lapse lists, Cartesian K.5
   Jacobian, general symplectic graph changes and arbitrary F(u,v,x)
   are not added as primary tests. Their availability is recorded;
   they are not needed to close these package corrections.
5. **Secondary status: completed for its actual target.** The completed
   audit of 0.1.0 plus the three additional calculations is acknowledged.
   Final 0.2.0 code has primary scoped static audit, a targeted independent
   review of the new adapter, retained source-bound runs and package QA.
   A complete secondary line audit of that final code was not performed.

## Negative controls and attribution

Upstream wrong_convention_mismatches are printed counts without assertions.
The historical algebraic NC1/NC3 compatibility residuals remain zero and are
insensitive controls, not expected failures. Historical NC2 and witness
mismatch counts are observations, not enforced PASS conditions.

The new adapter explicitly enforces the finite witness distinctions listed
in [INDEPENDENT-EVIDENCE.md](INDEPENDENT-EVIDENCE.md) and was freshly run.
Its source/input hashes and log digest match the distributed files.
Broader r<=4 symbolic and r<=3/4 geometric results remain historical
independent audit evidence, with the original executed-byte attribution
limit recorded. They are not used to expand the primary family or the
new adapter's r<=2 scope.

The Section 9 quotient-ring repair and its nonzero unrestricted residual,
D.2 noncommuting matrix order and conditional Jacobi identities, and A/B
finite-family exact recursion are all retained without changing their
hypotheses or promoting them to all-order estimates or convergence.


# Conventions and domains

The manuscript source, rather than an older draft's page numbers, determines
the locators in this package. The code does not read the manuscript at run time.
[checks.json](checks.json) supplies the precise correspondence and exclusions.

## Curvature and Schwarzschild metric

The curvature operator is $R(X,Y)=[\nabla_X,\nabla_Y]-\nabla_{[X,Y]}$ and
$\operatorname{Ric}(Y,Z)=\operatorname{tr}(X\mapsto R(X,Y)Z)$.
The coordinate script stores $R^a{}_{bcd}$ for $R(\partial_c,\partial_d)\partial_b$.
It works with $h=-f\,dv^2+2\,dv\,dr+r^2d\Omega^2$, $f=1-2m/r$.
The paper's physical metric is $g_E=-h$ of signature $(+,-,-,-)$.
Negation preserves the connection and covariant Ricci tensor and reverses
scalar curvature. Accordingly the program's conformal scalar $12m/r$ becomes
$-12m/r$ for $r^{-2}g_E$.

In the curvature script, the symbol `u` denotes radial speed, not the affine parameter named $u$ in the paper. The polar screen is $e_\theta=r^{-1}\partial_\theta$ at $\theta=\pi/2$.
The code substitutes $k=((E-u)/f,-u,0,L/r^2)$ and reduces polynomial numerators
by $u^2=E^2-fL^2/r^2$. This screen calculation is on $rf\ne0$; its literal
velocity formula is not evaluated at the horizon. The paper's rationalized
velocity and analytic extension supply the horizon argument. Only the polar
coefficient $3mL^2/r^5$, its parallel transport and the rotational
Jacobi identity derived from the computed geodesic acceleration are checked here; no complete second-screen transport or
transfer-matrix estimate is computed.

## Kasner spin readout

The metric is $dt^2-\sum_i t^{2p_i}dx_i^2$ with
$(p_1,p_2,p_3)=(-2/7,3/7,6/7)$, $t=1$ and $\Lambda=0$.
The script computes ordered covariant derivatives, acting on every derivative
and curvature slot, before projecting each chiral spinor. Its spin tangent
matrix is $\sqrt2$ times the normalized spin basis. Every term in each tested
homogeneous identity has the same degree, so this common factor cancels.
The arithmetic is in $\mathbb Q(i)$. The explicit initial assertion now verifies $Q_0=0$. Later $HQ$ values are geometric derivatives, not evaluations of the polynomial product rule. The two chiral outputs of this real Kasner input are conjugate, not independent complex inputs. The output counts 96 components at order
one, 168 at order two and 256 at order three, totaling 520 in the order-three
profile. Components counted in the pilot overlap the larger profile.

## Local source primitive and external comparison

In `adamo_exact.py`, the cyclotomic field contains $i$ and $\sqrt2$ exactly.
Numerators are reduced modulo $r^2-x^2-y^2-z^2$; all displayed denominators
are assumed nonzero. This is an algebraic local-chart calculation, not sampling
at finitely many coordinate points.

The source uses $E=\left(\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\right)$,
$L=-E$, $v^a=E^{ab}v_b$ and $v_a=L_{ab}v^b$. These source arrays differ from
the paper's fixed spin readout in Section 2. A direct wedge calculation is now compared to the actual `D.transpose()*WS*D` matrix, connecting the adopted two-form components to the contour convention. The matrix `WS` is the bilinear
component matrix of $\omega_0$, and `G` in the retained script is $G_0$;
neither symbol already contains the contour factor two. The added rational
residue test in `checks.py` independently obtains $\omega_{\rm int}=2\omega_0$
with one positive contour turn and prefactor $1/(2\pi)$, using the ordinary
exterior product.

The retained script first uses `M` for $\mu_{\rm src}$. In its final EF block,
`M` instead denotes physical mass $m$: the block explicitly substitutes
$\mu_{\rm src}=m/2$, $\varrho=-r$, $\tau=i(r-v)$. The adapter separately checks
the full angular block and density, obtaining $\Phi^*G_{\rm int}=2g_m/r^2$
and $\sigma_*=\sqrt2/r$. This identity holds on the specified local angular
and root chart; it does not provide native gluing over the spatial sphere.

External source locators refer to Adamo, Araneda, Seet and Sharma,
arXiv:2607.06236v2, equations (2.13), (2.24), (3.6), (3.20)–(3.21) and (3.28),
under the index conventions printed above. The external TeX source hash is
recorded in [provenance.json](provenance.json); its text is not redistributed.
The `AASS-*` checks evaluate those expressions literally. They are distinct
from `K5-*`, which check the adopted primitive and calibrated pullback.

## Appendix B numerical representation

A symmetric tensor is stored as its polynomial coefficient array, with squared
Hermitian norm given by the weights
$\binom na^{-1}\binom mb^{-1}$. Symmetrization is averaging; the alternation
is $\delta_r=(1-\tau)J_r$, with no factor $1/2$.
For positive chirality $(n,m)=(r+4,r)$; negative chirality exchanges them.
The two label spinors are independently normalized real vectors and the tested
records are their coherent powers in the indicated chirality.

The `F2` and `F3` arrays are coefficients of distinguished square-zero label
amplitudes. For example, $Q_1(X)=B(X,X)$ gives
$[e_0e_1]Q_1(e_0y+e_1w)=B(y,w)+B(w,y)$. On equal arguments this is twice
the associated symmetric bilinear coefficient. At higher degrees the ordered
positions are summed; no blanket division by $d!$ identifies every ordered map.
The factors $\prod_i j_i!/r!$ in the tables normalize record orders and do not
supply polynomial-degree polarization normalization. The lower-value
interpretation applies to these explicitly measured polarized maps.

All diagnostic arrays use float64. The nilpotent route implements directional
derivatives algebraically without finite differences, but its coefficient
arithmetic is still floating point. Agreement of the four printed coefficient
norms at each level is weaker than componentwise agreement. The residuals `resL`, `resF3`, `JsHQ` and `sym2` use unweighted Frobenius norms of polynomial coefficient arrays; these differ from the weighted tensor norm used by `hnorm`. `JsHQ` is evaluated in quadratic transfers and is not a direct all-degree $P_{++}Q_r$ test. The residual
threshold is $10^{-10}$; the comparison threshold is $10^{-5}$ because the
inherited programs print these norms with seven significant digits.
Neither threshold supplies an interval certificate. No atomic diagram mass is
computed. Insertion tables contain 40-step power estimates in their denominators;
their ratios are finite diagnostics with no certified inequality direction.


## Exact free-record family

The A/B job uses $\Lambda=0$ and the coefficient algebra
$A=\mathbb Q[e_0,e_1,e_2]/(e_0^2,e_1^2,e_2^2)$, with independent chiral
free lists. Its three labels, order weights and all eight amplitude coefficients
are explicit in [inputs.json](inputs.json). They are symmetric free tensors in
$W_j^\pm$, rather than arbitrary arrays declared to be completed curvature
jets. The Weyl-to-curvature map is tested against metric skewness, algebraic
Bianchi and Ricci zero on all ten quartic basis vectors. On the selected finite
family the polynomial product rule generates $Q_r$, and the actual source is
checked to lie in the image of $\delta_r$ by a zero residual. The finite
coefficient-algebra applicability of the paper's formal construction uses
Propositions A.3/A.4; this supplement does not independently construct an
analytic Einstein metric realizing the lists. The selected rational spinors are
not normalized and this exact job makes no norm-budget assertion.

The compact `ab-exact.family` string in `inputs.json` is written in positive-chirality order. Its phrase “designated chirality” includes exchanging the two spin degrees for the negative label, exactly as specified in [NEW-CHECKS.md](NEW-CHECKS.md) and `deg(c,j)` in the code.

In the saved order-four cross-route comparison, 32 printed norm pairs are compared; 15 pairs are at most $1.2\times10^{-16}$ on both routes, while 17 are outside that threshold. Only one degree-three norm pair is above the threshold. These are descriptions of the saved sample, not componentwise equality or exact-zero certificates.

The exact A/B Weyl-basis job applies the paper's signed $-1/4$ readout to recover the original chiral inputs on 320 components. A formal compatibility residual can remain zero after consistent parameter rescaling; it is not a standalone calibration test. Nonzero-$\Lambda$ calibration remains outside this job. In K5-EF the positive density component is selected as an input; equality of squared metric scales does not certify a marked density-root sign or a spin lift.

## Final independent-calibration scope

The r>=1 Kasner geometric residual comparison is valid on non-Einstein metrics
as well. The current Kasner jobs additionally impose their vacuum assumptions
and Q0=0; those checks must not be dropped when describing the whole job.
Only the geometric specialization of lines 1-3 of the recursion display is
attributed to those residuals. The polynomial product rule is tested separately.

Formal compatibility is insensitive to a coherent overall curvature-action
sign change and to renaming a symbolic Lambda parameter. Algebraic inverse
readout/Ricci normalization tests can fix the abstract linear curvature map.
Geometric witnesses test the connection between a recursion and independently
derived coordinate curvature. These are distinct checks.

The revision-3 independent witness group fixes that connection for the listed
metrics through r=2 in Claude's implementation; it does not execute the primary
A/B implementation. Kottler is complexified with Einstein constant -1/10 in
the declared metric convention. The dictionary-key unions counted as compared
entries omit components zero in both sparse representations. Historical
wrong-convention counts are observations; only the adapter's require calls
enforce the new controls. See [INDEPENDENT-EVIDENCE.md](INDEPENDENT-EVIDENCE.md).

B-VALUES retains raw PASS solely as a completeness/finiteness gate on observed
float64 data. It is excluded from the count of mathematical inequalities or
exact paper checks. No change to polarization or norm conventions is made
in revision 3; the 17/32 B-CROSS and one cubic norm comparison remain as above.

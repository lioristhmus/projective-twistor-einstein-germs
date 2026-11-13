# Added exact calculations

All paper anchors refer to the fixed source in [BASELINE.json](BASELINE.json).
[checks.json](checks.json) gives actual assertion locations and exclusions.
The displayed identities below describe the tested targets; PASS additionally
requires a matching saved execution of the distributed code.

## Section 9: mixed Ricci tensor and repair

The coordinates are $(u,v,x,y)$ and the metric is

$$
 g=2\,\mathrm du\,\mathrm dv-2\,\mathrm dx\,\mathrm dy
       +t f(u)\,\mathrm dx^2+s q(x)\,\mathrm dv^2.
$$

The first stage retains arbitrary function symbols $f(u)$ and $q(x)$ and
unrestricted parameters $t,s$. It derives the inverse and determinant, all
64 Christoffels and all 16 Ricci entries from the metric. It checks the
complete connection list in Proposition 9.2, including the zero entries, and
obtains

$$
 \det g=1,\qquad
 \operatorname{Ric}(g)=\tfrac12tsqf''\,\mathrm dx^2,
 \qquad \operatorname{Scal}(g)=0.
$$

The individual wave curvatures are also computed. Their exterior supports
are $\mathrm du\wedge\mathrm dx$ and $\mathrm dx\wedge\mathrm dv$.
With the declared holomorphic coordinate volume their Hodge eigenvalues are
opposite. This checks relative chirality, without identifying that orientation
with an absolute marked spin-frame sign.

The second stage substitutes $f=u^3,q=x^2$. It derives the Schouten tensor
and the covariant Cotton component rather than entering their expected values
as inputs. The resulting highest coefficients are

$$
 [ts]P_{xx}=\tfrac32ux^2,\qquad
 [ts](\nabla_uP_{xx}-\nabla_xP_{ux})=\tfrac32x^2.
$$

For $H=3u^2vx^2/2$ it directly checks the flat trace and divergence, computes
$\Box_\eta H=6ux^2$, and derives the linearized Ricci tensor by differentiating
the metric perturbation. It then computes the entire repaired Ricci tensor
before reducing parameters:

$$
 \operatorname{Ric}(g+tsH\,\mathrm dx^2)
       =\tfrac32ts^2vx^4\,\mathrm dx^2.
$$

Every component vanishes in $\mathbb C[t,s]/(t^2,s^2)$. The unrestricted
tensor is not zero; the code checks its $xx$ value $3/2$ at
$t=s=u=v=x=1,y=0$. This negative control prevents a quotient-order repair
from being reported as an unrestricted exact vacuum solution. Contact-cocycle
admission, the obstruction quotient and restoration of fixed free records
remain mathematical arguments of the paper, outside these tensor tests.

## Appendix D.2: matrix order and covariance

Write $P=S'$, $Q=S''$, $T=S'''$, $H=P^{-1}$ and $A=HQ$.
For $v=f(u)$ set $a=f'\ne0$, $b=f''$, $c=f'''$. The ordered-word program
generates the derivatives by repeatedly applying $D_v=a^{-1}D_u$:

$$
 S_v'=a^{-1}P,\qquad
 S_v''=a^{-2}Q-ba^{-3}P,\qquad
 S_v'''=a^{-3}T-3ba^{-4}Q+(3b^2a^{-5}-ca^{-4})P.
$$

The only adjacent matrix cancellations permitted are $PH=HP=1$.
Inserting these generated expressions into the matrix Schwarzian verifies

$$
 \mathcal S_v(S)=a^{-2}
       \left(\mathcal S_u(S)-\tfrac12\{f,u\}I\right),
 \qquad \mathcal S_u(S)=\tfrac12HT-\tfrac34HQHQ.
$$

No matrix derivatives commute. The same ordered algebra verifies the
conditional normalization/Jacobi identities. In particular, with
$B=-QH/2$ and $Y'=YB$, it obtains

$$
 C:=Y^{-1}RY=-(B^2+B')=\tfrac12TH-\tfrac34QHQH,
 \qquad C^{\mathsf T}=\mathcal S_u(S).
$$

Here $S,P,Q,T,H$ are symmetric for the normalization argument, and
$Y^{\mathsf T}Y=H$ is the Gram condition. Ordinary transpose is essential.
The Gram derivative, both self-Wronskians, cross Wronskian and $Z=YS$ Jacobi
residual are checked. These are conditional algebraic identities; construction
of the analytic normalization solution and ODE uniqueness are not executed.

A separate exact rational calculation uses

$$
 S(u)=\begin{pmatrix}
 1+u/(1-u)&2+u^2/(2(1+u))\\
 2+u^2/(2(1+u))&1+2u+u^3/(3(1-u))
 \end{pmatrix},\qquad f(u)=u+u^2.
$$

The domain is a sufficiently small neighborhood of $u=0$ excluding poles
and zeros of $\det S'$ and $f'$. The code checks that $[S',S''](0)$ and
$[A,A'](0)$ are nonzero, verifies the full rational matrix and half-trace
covariance identities, and checks admissible initial Jacobi jets from
$Y_0=\operatorname{diag}(1,1/\sqrt2)$. It does not replace the matrix test by
a scalar or diagonal example. General symplectic graph-frame changes and
analytic ODE existence remain outside the executed coverage.

## Appendices A/B: finite exact free-record calculations

The new rational backend implements the actual polynomial product rule in
Lemma B.1. First it checks every coefficient-basis vector of
$\mathcal D_r=V^*\otimes W_r$ in both chiralities through $r=4$:

$$
 \delta_r(P_{++}X)=0,\qquad
 M_rJ_r^*\delta_rX=X-P_{++}X.
$$

It also checks block decomposition, block idempotence and the compressed
spectrum. There are 880 basis vectors across these finite spaces; the
order-one pilot overlaps the main profile. No assertion of surjectivity onto
all antisymmetric sources is made.

For algebraic input compatibility, all ten quartic basis vectors of
$W_0^+\oplus W_0^-$ at $\Lambda=0$ are converted to curvature operators.
Antisymmetry, metric skewness, the first Bianchi identity and Ricci zero are
checked explicitly. The signed $-1/4$ readout is then applied to 320 components to recover both chiral inputs, calibrating the normalization separately from compatibility. This covers the linear algebraic curvature conditions on
that span, not differentiated Bianchi completion at every order.

The nonlinear test uses one declared finite coefficient-algebra family,
$A=\mathbb Q[e_0,e_1,e_2]/(e_0^2,e_1^2,e_2^2)$:

| Label | Chirality | $\xi$ | $\pi$ | Order weight $z$ |
| --- | --- | --- | --- | --- |
| $0$ | $+$ | $(1,0)$ | $(1,1)$ | $1$ |
| $1$ | $+$ | $(1,1)$ | $(0,1)$ | $2$ |
| $2$ | $-$ | $(1,2)$ | $(2,-1)$ | $3$ |

For $0\le j\le3$, the positive record is the sum of
$e_i z_i^j\xi_i^{j+4}\pi_i^j$ over positive labels; the negative record uses
$e_i z_i^j\xi_i^j\pi_i^{j+4}$. These are symmetric free tensors by construction,
not arbitrary ordered curvature arrays. The lists are independent complex
lists after scalar extension, with no Lorentz-reality or unit-norm assertion.

Products are coefficient products in $A$. Additional square-zero variables
evaluate directional derivatives exactly, without finite differences. At every
recursive call the code checks

$$
 \delta_rQ_r=-K_r-(1-\tau)\mathsf H Q_{r-1},\qquad
 J_r^*\mathsf H Q_{r-1}=0,\qquad P_{++}Q_r=0,
$$

and rejects nonrational coefficient types. Through order four the top-level
arrays contain 7,040 scalar amplitude coefficients, including zeros and
overlapping lower-order tests. The $e_0e_1e_2$ coefficient is explicitly
required to be nonzero at order four, so the selected mixed cubic test is not
vacuous. At order one it also identifies the unscaled polarization exactly:
$[e_0e_1]Q_1(e_0y+e_1w)=B(y,w)+B(w,y)$, with a nonzero result.
This does not identify every higher ordered coefficient with a polarized sum.

Use of the formal completion on independent lists and commutative coefficient
algebras relies on Propositions A.3/A.4. The code checks exact-set compatibility
on this particular finite family; it does not independently construct an
analytic Einstein metric realizing those inputs. General differentiated Bianchi
completion, nonzero cosmological constant, atomic mass, all-order insertion
gains and analytic convergence are not certified by this calculation.

## Revision-3 independent witness group

The primary three additions and their executed code are unchanged from r2.
The separate [independent witness group](INDEPENDENT-EVIDENCE.md) freshly
executes seven metrics through r=2 and enforces the listed negative controls.
Its nonzero-Lambda Kottler result belongs to that implementation only.
The reported all-input symbolic r<=4 result belongs to Claude's completed
historical audit and is not substituted for the primary finite input family.

---
title: "Finite local readouts for Schwarzschild optical transport"
author: "Lior Isthmus"
language: en
date: "2026-11-05"
bibliography: references.bib
---

<div id="sec:fro-proof-note"></div>

# Finite local readouts for Schwarzschild optical transport

This note proves a finite-local-readout approximation theorem for the entire fixed positive-mass horizon-crossing family of Proposition 10.2 in the accompanying manuscript. The imported results are its complete-record extraction and analytic convergence (§§3 and 6), initialized physical and enriched comparisons (results K.6–K.9), and the explicit Schwarzschild optical calculations and local stability estimates (§K.3, Lemmas K.10–K.11 and Theorem K.12). Those imports retain their fixed-v0.2.7 provenance. All additional finite-cover, switch and accumulated-error arguments are given below. Numbered references use the accompanying manuscript's current display labels; the old-to-new appendix map is recorded in the review response.

| Claim | Required inputs | Conclusion used next |
| --- | --- | --- |
| Theorem A.1 | Exact analytic family, K.6–K.9, compact product | Fixed enlarged slabs, buffered readouts and state neighborhoods |
| Proposition A.2 | Finite-algebra readout and fixed exact coordinate comparisons | Uniform C³ tails with a C⁴ pullback cost |
| Proposition A.3 | Exact physical atlas and the two local tails | Controlled overlap defects; retained exact enriched comparisons |
| Lemma B.1 | Buffered overlaps, K.11 and the actual incoming state | Null/full-frame reset and recorded symplectic Cauchy switch |
| Proposition C.1 | Local state flows, entrance error and reset inequalities | All-slab existence and a finite product/sum state bound |
| Proposition C.2 and Corollary C.3 | C³ stability, state bound and every screen jump | Symplectic full transport with uniform geometric convergence |
| Proposition C.4 | New transfer bound and the original exact endpoint margin | Area, inverse-block and expansion-trace errors |
| Theorem D.1 | The preceding finite construction | Full original-family alternative to a single-readout hypothesis |

The construction uses the fixed exact coordinate comparisons, affine durations and parallel Sachs reference frame of this Schwarzschild benchmark. The approximation is a finite sequence of local metric flows and prescribed covariant Cauchy resets at exact affine cuts. Its full meaning and the distinction from differentiating the nonlinear state reset are stated in Lemma B.1. No mathematical computation program or numerical integration is needed for this proof.

<div id="sec:fro-a-domains-readouts"></div>

## A. Finite readout domains for the complete crossing family

Fix $m>0$ and the ingoing Schwarzschild family of §K.3.2, with

$$
 P=[1,2]\times[1/4,1/2],\qquad
 \lambda=(E,\ell),\qquad L=m\ell,\qquad t=u/m.
$$

Use the dimensionless EF coordinates $x=(V,\rho,\theta,\phi)=(v/m,r/m,\theta,\phi)$. Write $g=g_0=\bar g$ for $m^{-2}g_m$ after expressing $g_m$ in these coordinates with its Jacobian factors. This explicit fixed unit conversion leaves the Levi–Civita connection unchanged. Every metric readout and tail norm in this section is taken after this conversion. The selected physical metric and the physical enriched atlas remain $g_m$; their interpretation undoes the same fixed conversion. All coordinate and tensor norms are auxiliary Euclidean norms, and all constants may depend on this fixed $m$. Let $x_\lambda(t)$ be the exact trajectory and let $\tau(\lambda)$ be its first time at $\rho=3/2$. Thus

$$
 \tau(\lambda)=\int_{3/2}^{5/2}
   \frac{\mathrm d\rho}
    {\sqrt{E^2-\ell^2(\rho-2)/\rho^3}},
 \qquad
 \frac{10}{21}<\tau(\lambda)<\frac{100}{99}.
$$ {#eq:fro-a-duration}

The parameter $s=t/\tau(\lambda)$ will be used only to choose a finite schedule. The metric, geodesic, parallel-frame and Jacobi equations retain the affine clock $t$.

<div id="thm:fro-a-finite-domain-schedule"></div>

**Theorem A.1 (finite buffered readout schedule).**

The whole family from $\rho=5/2$ to $\rho=3/2$, with every $\lambda\in P$, has the following data, chosen before the amplitude truncation degree $N$.

There are finitely many exact local normal-to-EF maps $\chi_i$ and nested complex EF domains

$$
 V_i^0\Subset V_i^1\Subset V_i^2\Subset V_i^3,
$$ {#eq:fro-a-nested-domains}

where $V_i^2$ lies in a $C^3$ metric-control core of a local readout of Lemma K.9 and $V_i^3$ lies in its fixed-coordinate readout parent. The metric and all inverse units needed for that readout have their retained bounds. There are compact parameter cores $P_a$ covering $P$, larger compact parameter neighborhoods $P_a^+$, a single integer $J\ge1$, and a choice $i=i(a,j)$ for $1\le j\le J$, such that the whole exact enlarged slab

$$
 \left\{
  x_\lambda\bigl(\tau(\lambda)s\bigr):
   \lambda\in P_a^+,\quad
   \frac{j-3}{J}\le s\le\frac{j+2}{J}
 \right\}
 \Subset V_{i(a,j)}^0 .
$$ {#eq:fro-a-enlarged-slab}

The extensions in this display are actual short extensions of the exact family. The cuts for $\lambda\in P_a$ are

$$
 t_j(\lambda)=\tau(\lambda)\frac jJ,\qquad
 \frac{10}{21J}<t_j-t_{j-1}<\frac{100}{99J}.
$$ {#eq:fro-a-affine-cuts}

Order the finite parameter cores once and, for each $\lambda\in P$, use the least index $a$ with $\lambda\in P_a$ and its assigned readout list. Every estimate is uniform over all cores; no analytic dependence across these selection seams is required. Adjacent readouts contain a common open time neighborhood of their exact node, with a positive common position buffer. There are also compact enlarged state tubes, uniform vector bounds and positive state buffers for the exact tangent, null companion and parallel screen frame on every assigned slab. All these choices are independent of $N$.

*Proof.* The radicand in [@eq:fro-a-duration] is bounded below by $124/125$ on the original compact parameter/radial rectangle. It stays nonzero on a slightly larger real rectangle and on a complex neighborhood of that rectangle. Fix the positive square-root branch there. The quadratures of §K.3.2, followed by the inverse with $\partial t/\partial\rho=-1/q$, prove real-analytic dependence of $x_\lambda(t)$ and $\tau(\lambda)$ on their arguments near the full compact family.

Choose a compact parameter rectangle $\widehat P$ with $P\subset\operatorname{int}\widehat P$, sufficiently small that this branch and the same initial data remain defined. The regular EF parent of §K.3.2 has positive radial, advanced-time and angular buffers around the original trajectories. Existence and continuous dependence for the exact ODE, compactness and the transverse radial derivative therefore give $\alpha>0$ such that

$$
 \Gamma(\lambda,s)=x_\lambda(\tau(\lambda)s)
$$

is real analytic on an open neighborhood of
$\widehat X=\widehat P\times[-\alpha,1+\alpha]$,
and its image remains in a compact subcore of that regular EF parent. The companion and screen-frame ODEs have the same property: their coefficients and initial data are analytic, all original initial denominators have positive lower bounds, and their solutions are bounded on this compact set. A small further restriction of $\widehat P$ and $\alpha$ makes these choices simultaneous. The sharp rational estimates of §K.3 apply on the original $P$ and its original intervals; the added extensions need only the finite analytic bounds just obtained. The assertion does not ask one ray to remain in the radial strip until the larger terminal time of another ray.

We next construct the readout domains; this step does not assume that one old readout contains any long segment. The compact image $\Gamma(\widehat X)$ lies inside $r>0$ and inside a finite physical core of Theorem K.8 chosen to contain a small neighborhood of this image. Such a core can be chosen with radial endpoints strictly outside $[3m/2,5m/2]$, advanced-time endpoints strictly outside the displayed trajectory range and the whole angular sphere. For the original family choose $m/2<\delta<2m$, $v_-<0$ and $v_+>25m/396$ in that core definition; take the parameter and time extensions small enough to retain strict buffers inside it. Its finite angular charts include the regular strip used here.

At each point of this compact image, choose a marked full-spin frame in one of the finite analytic frame parents. Lemma K.6 extracts a bounded all-record family on a neighborhood of that mark. Propositions 6.1–6.2 and Theorem 6.3 supply the prescribed stored representative over an amplitude disk of radius greater than one, on a sufficiently small spatial neighborhood. Lemma K.9 supplies its holomorphic physical metric readout, bounded inverse units, initialized normal development and independent spatial gaps. This is applicable to these actual bounded original inputs; the amplitude parent is furnished by §§6.1–6.3, rather than added as an assumption about the long tube. The required restrictions decrease space and retain the compact amplitude disk.

At amplitude one, Lemma K.6 and the initialized normal metric comparison preceding Theorem K.7 give an exact normal-to-EF map $\chi$ with analytic inverse $\kappa$. Choose sufficiently small concentric complex EF polydiscs around the marked point. Four nested such polydiscs can be placed inside the physical image of the normal readout parent, so that the second larger polydisc $V^2$ and its closure lie in the image of the normal $C^3$ control core and the largest $V^3$ has a positive gap to the actual readout boundary. Reserve any further spatial Cauchy gap needed below before making this choice. The real locus of the smallest $V^0$ contains the marked point.

These local choices may also be made smaller than the local comparison-star radii in Theorem K.8. Taking a finite subcover of the compact image gives finitely many nested domains as in [@eq:fro-a-nested-domains], with all their exact maps, inverse-unit margins and derivative bounds fixed. In particular the real open sets

$$
 O_i=\Gamma^{-1}(V_i^0)\cap\widehat X
$$

cover $\widehat X$. Give $\widehat X$ the maximum product metric. By the Lebesgue-number lemma there is $d>0$ such that every subset of $\widehat X$ of diameter less than $d$ lies in some $O_i$. This use of compactness is on the parameter-time product, after the readout domains have been fixed.

Let $\Delta_P=\operatorname{dist}_\infty(P,\partial\widehat P)>0$. Choose

$$
 0<r<\min\{d/16,\Delta_P/4\},
 \qquad
 \frac1J<\min\{d/10,\alpha/3\}.
$$ {#eq:fro-a-product-mesh}

Choose finitely many $\lambda_a\in P$ whose open maximum-norm balls of radius $r/2$ cover $P$, and put

$$
 P_a=P\cap\overline B_\infty(\lambda_a,r),\qquad
 P_a^+=\overline B_\infty(\lambda_a,2r)
                              \subset\operatorname{int}\widehat P.
$$

The core $P_a$ has a relative open neighborhood contained in $P_a^+$, and the $P_a$ cover $P$. For each $a,j$ consider the compact product

$$
 C_{aj}=P_a^+\times
          \left[\frac{j-3}{J},\frac{j+2}{J}\right].
$$

It is contained in $\widehat X$: its time endpoints lie between $-2/J$ and $1+2/J$. Its product diameter is at most $\max\{4r,5/J\}<d$. The Lebesgue property therefore assigns a single $i(a,j)$ with $C_{aj}\subset O_{i(a,j)}$. Its image is compact in $V_{i(a,j)}^0$, which proves [@eq:fro-a-enlarged-slab]. This supplies an actual common schedule for the whole slab at every parameter in a parameter core, rather than a different unspecified cover of each individual ray. Equation [@eq:fro-a-affine-cuts] follows from [@eq:fro-a-duration].

For adjacent cells, both enlarged intervals contain $|s-j/J|\le1/J$. Thus their exact images over $P_a^+$ lie in both assigned readouts on this whole node neighborhood. In particular the images over the smaller compact set
$P_a\times\{|s-j/J|\le1/(2J)\}$
are compact in the intersection of the two smallest domains. Their distances to the complements of the two $V^1$ domains have a positive minimum. There are only finitely many such nodes and cells. Taking the minimum of their positive margins gives a common position buffer. Compactness likewise gives a margin between every enlarged slab image and the boundary of its assigned $V^1$.

For clarity, state buffers are chosen separately from these four-dimensional point domains. Use the fixed EF coordinates, affine clock $t$, and the $\bar g$-normalized state $(K,\mathcal N,E_1,E_2)$, where $K=\mathrm dx/\mathrm dt$, $\bar g(K,\mathcal N)=1$ and $\bar g(E_A,E_B)=-\delta_{AB}$. The physical vectors are $(k,n,e_A)=(K,\mathcal N,E_A)/m$, with the same coordinate interpretation; in particular $k=\mathrm dx/\mathrm du$. All four vectors are transported in their own exact normalized frame. This is the fixed mass unit conversion, not a rescaling by $\tau(\lambda)$. Denote the joint exact state by

$$
 Z_\lambda(t)=(x_\lambda(t),K_\lambda(t),
                       \mathcal N_\lambda(t),E_{1,\lambda}(t),E_{2,\lambda}(t)).
$$

Its values on the finitely many enlarged slabs form compact sets. Choose a position radius smaller than one quarter of the common position buffer, and vector radii at most one. Shrink these radii and fix a positive metric-perturbation tolerance $\beta_g$ so that the frame-normalization denominators and Gram-matrix neighborhoods used in Lemma K.11 retain their strict margins for every state in the resulting tubes and every symmetric metric within $\beta_g$ of the exact metric there. This is possible by joint continuity at the exact normalized compact frame family; the normalizing formulas are analytic on an open neighborhood of that family. A common smaller radius $\eta_Z>0$ and a common finite vector bound $V$ exist by taking the finite minima and maxima. The point projections of all these state tubes lie inside the corresponding $V^1$, and hence inside the prescribed $C^3$ cores. The radii, $\beta_g$, $V$, all domain gaps and the schedule have now been fixed without choosing $N$. ∎

<div id="prop:fro-a-finite-readout-tail"></div>

**Proposition A.2 (local finite readouts and common-coordinate tails).**

For every readout retained in Theorem A.1 there is a radius $T_i>1$ and a constant $D_i<\infty$ such that its degree-$N$ finite readout defines a holomorphic symmetric tensor $g_{i,N}$ on $V_i^2$, real on the real slice, with

$$
 \|g_{i,N}-g\|_{C^3(V_i^2)}
 \le\delta_{i,N}
 :=D_i\frac{T_i^{-N-1}}{1-T_i^{-1}}.
$$ {#eq:fro-a-local-tail}

Here the norm is the maximum of the tensor norms and the multilinear derivative norms through order three. The finite readout is performed over its own finite amplitude algebra, followed by coefficient-polynomial evaluation at one. There is a common $T_*=\min_iT_i>1$ and a finite $D_*$ with

$$
 \max_i\delta_{i,N}\le D_*T_*^{-N-1}.
$$ {#eq:fro-a-uniform-tail}

*Proof.* For each fixed original input at the selected mark, use its own amplitude variable $\varepsilon_i$, stored analytic tuple $Y_i$ and finite tuple
$X_{i,N}=q_{i,N}Y_i$, where
$q_{i,N}$ is reduction modulo $\varepsilon_i^{N+1}$.
Choose nested amplitude radii $1<T_i<T_{c,i}<T_{b,i}$ before taking any truncation. Lemma K.9 proves, including its finite inverse and initialized ODE recursions, the coefficient identity

$$
 \mathcal R_{i,N}(X_{i,N})
       =q_{i,N}h_i(\varepsilon_i),
 \qquad
 h_{i,N}=\operatorname{ev}^{\mathrm{poly}}_1
                             (q_{i,N}h_i).
$$ {#eq:fro-a-finite-readout-identity}

Here $h_i$ is $m^{-2}$ times the physical metric in the initialized normal coordinates, and $\mathcal R_{i,N}$ includes this final fixed scalar multiplication. It commutes with finite reduction and coefficient-polynomial evaluation; the bound $H_i$ below includes the factor $m^{-2}$. This identity is an equality of coefficient germs on their common representatives. Inverses use finite nilpotent sums; compositions use only the finitely many amplitude coefficients and derivatives needed at the retained degree; initialized ODE coefficients satisfy unique finite linear inhomogeneous recursions. These are precisely the operations in the readout, so the identity includes its nonlinear metric reconstruction and normal development. Evaluating the stored tuple first and then applying a nonlinear readout would not give this identity.

Write $\kappa_i=\chi_i^{-1}$ for the exact amplitude-one EF-to-normal map. It is fixed for all $\varepsilon_i$ and $N$. The initialized metric isometry gives

$$
 g=\kappa_i^*h_i(1),\qquad
 g_{i,N}
   =\kappa_i^*h_{i,N}
   =\operatorname{ev}^{\mathrm{poly}}_1
                      q_{i,N}\bigl(\kappa_i^*h_i(\varepsilon_i)\bigr).
$$ {#eq:fro-a-fixed-coordinate-readout}

The equality on the right holds because this fixed pullback is linear in the tensor and independent of amplitude. Its finite coordinate factors have their exact values; this is not an approximate coordinate map recomputed from $h_{i,N}$.

Keep a positive normal spatial gap $\rho_i$ around $\kappa_i(\overline V_i^2)$ inside the normal readout parent. Lemma K.9 and amplitude Cauchy estimates give a finite $H_i$ with

$$
 \|D^q(h_i(1)-h_{i,N})\|
 \le 4^q q!\rho_i^{-q}
                  \frac{H_iT_i^{-N-1}}{1-T_i^{-1}},
 \qquad 0\le q\le3,
$$

on this retained normal core. The first spatial loss has already made the nonlinear readout and its inverses bounded; this $\rho_i$ is the independent loss for differentiating its amplitude tail.

We record explicitly the coordinate cost. Put

$$
 B_i=\max\left\{1,\sup_{\overline V_i^2}
                           \|D^q\kappa_i\|:1\le q\le4\right\}<\infty.
$$

Finiteness follows from analyticity on $V_i^3$ and the retained gaps. The coordinate map $\chi_i$ also has finite derivatives through order four on the corresponding compact normal cores, with bounded inverse differential. Either direction of the coordinate comparison is therefore controlled. For a covariant two-tensor $r$, differentiating
$(\kappa_i^*r)(x)(v,w)
=r(\kappa_i(x))(D\kappa_i(x)v,D\kappa_i(x)w)$
three times uses no derivative of $\kappa_i$ above order four. If
$R=\max_{q\le3}\|D^qr\|$,
the chain-rule bounds on $D^a(r\circ\kappa_i)$, for $a=0,1,2,3$, are respectively
$R$, $RB_i$, $2RB_i^2$ and $5RB_i^3$.
The Leibniz rule for these three factors has coefficient sum $3^j\le27$ at order $j\le3$. Consequently the safe bound

$$
 \|\kappa_i^*r\|_{C^3(V_i^2)}
       \le135B_i^5
                    \max_{q\le3}\|D^qr\|
$$ {#eq:fro-a-coordinate-c4-cost}

holds in the stated operator norms. One may therefore take

$$
 D_i=135B_i^5H_i
              \max_{0\le q\le3}(4^q q!\rho_i^{-q}).
$$

This proves [@eq:fro-a-local-tail]. The Lorentz reality assertion in Lemma K.9 and the exact real coordinate map give real symmetric coefficient tensors and hence real $g_{i,N}$.

There are only finitely many readouts. Thus $T_*=\min_iT_i>1$ and
$D_*=\max_i D_i/(1-T_i^{-1})<\infty$
give [@eq:fro-a-uniform-tail]. The constants and domains were fixed before $N$. In particular all strict metric inverse, frame-normalization and state first-exit smallness conditions that use finitely many of these constants can subsequently be imposed by one sufficiently large $N$. This last observation does not itself perform the finite state matching or its error propagation. ∎

<div id="prop:fro-a-overlaps-exact-atlas"></div>

**Proposition A.3 (overlap defect and the retained exact atlas).**

On every common EF overlap of two domains used in the schedule,

$$
 \|g_{i,N}-g_{k,N}\|_{C^3(V_i^2\cap V_k^2)}
     \le\delta_{i,N}+\delta_{k,N}.
$$ {#eq:fro-a-overlap-defect}

At amplitude one the exact local metric comparisons, full-spin lifts, contact and affine comparisons, structured operator comparisons and compact point-module comparisons are those of the finite physical atlas in Theorem K.8, with its actual finite coherence. They can be retained on the compact node neighborhoods of Theorem A.1. Independently truncated metrics need satisfy neither an exact metric cocycle nor a common physical amplitude family.

*Proof.* Both exact amplitude-one tensors in the fixed EF coordinates equal $g$. The triangle inequality applied to the two differences in [@eq:fro-a-local-tail], and to their derivatives, proves [@eq:fro-a-overlap-defect]. There is no coordinate-transition factor in this formula because the two tensors and norms are already in the same EF coordinates. In normal coordinates the equivalent assertion must retain the pullback by the exact transition $\kappa_k\chi_i$, and its coordinate bound; it is not a literal difference of arrays from different coordinate systems.

The exact charts satisfy
$h_i(1)=\chi_i^*g$. Undoing the fixed unit conversion gives the original physical metrics and initialized isometries, with their original root and full-spin calibration. Their coordinate transitions are the actual maps
$\chi_k^{-1}\chi_i$, and their specified full-spin lifts are the changes of the same fixed spin bundle. By Theorems K.7–K.8 they induce the retained contact, affine, infinity, operator and compact point-module comparisons, with actual comparison units and module maps. On a triple their comparisons are the existing finite coherence comparisons, not separately chosen principal-symbol identifications.

Only finitely many chart pairs and node neighborhoods occur in Theorem A.1. Their exact compact node images lie in the interiors of both assigned chart parents and retain positive buffers. Keeping these compact cores and their whole complex skies, apply Theorem K.8's simultaneous finite closed-star refinement to this finite list of maps, inverses and stipulated finite composites. Its parent restrictions retain the required compact sets and all sky fibers. Existing atlas maps are restricted, not altered; an additional local normal representative is compared through its initialized exact metric isometry as in Theorem K.7. Thus the required exact old comparisons and their root/full-spin/module calibrations remain available at every switching node.

No identity between $\varepsilon_iU_i$ and the record family at a different mark is used. The $\varepsilon_i$ are internal construction parameters of the separate readouts; only their amplitude-one exact metrics have been identified. Polynomial evaluation at one preserves their approximation estimates but does not turn the overlap defect into zero or supply a cocycle for the truncated metrics. The finite schedule and node buffers make them suitable inputs for a separate finite matching argument; they do not claim that argument for free. ∎


<div id="sec:fro-b-switches"></div>

## B. Prescribed metric switches and their optical phase maps

<div id="lem:fro-b-cauchy-switch"></div>

**Lemma B.1 (Metric and Cauchy switches).**

Use the finite buffered schedule and local readouts of Theorem A.1 and Propositions A.2–A.3. On a fixed neighborhood of each exact framed node, the formulas below define a locally analytic null-frame reset, a metric-to-metric tangent isometry and an oriented screen identification. Their state and phase errors are bounded by the incoming state error and the two readout metric errors, with constants and positive margins independent of the truncation degree. The prescribed covariant Cauchy-jet rule is well defined on the screen quotient, preserves the same affine-clock Wronskian, and has the symplectic phase matrix $\operatorname{diag}(R,R)$ with $R\in SO(2)$. At exact reference data this phase matrix is the identity. All previously accumulated phase data are transported by that matrix.

*Proof.* We give the normalization, quotient map and phase calculation explicitly.

**Fixed coordinates, clocks and reference data.**

Fix $m>0$ and common dimensionless EF coordinates $x=(V,\rho,\theta,\phi)$, where $V=v/m$ and $\rho=r/m$. Put

$$
 g_0=\bar g=m^{-2}g_m,\qquad t=u/m.
$$

The components of $g_m$ here are expressed in these dimensionless coordinates. Its connection is the connection of $g_0$, since their factor $m^2$ is constant. The reference state is

$$
 Z_*(\lambda,t)=(x_*,K_*,\mathcal N_*,E_{*,1},E_{*,2}),\qquad
 \dot x_*=K_*,
$$

with dot denoting $d/dt$. The vectors are parallel along the reference ray and have Gram matrix

$$
 Q=
 \begin{pmatrix}
 0&1&0&0\\1&0&0&0\\0&0&-1&0\\0&0&0&-1
 \end{pmatrix}.
$$

In particular, $g_0(K_*,\mathcal N_*)=1$. Choose the same global polar-first parallel Sachs screen and null companion as in §K.3, rescaled to this convention. The physical tangent, companion and unit screen vectors are $K_*/m,\mathcal N_*/m,E_{*,A}/m$. The parameter $\lambda$ ranges over the fixed compact family of Proposition 10.2. Its exact dimensionless terminal time is $\tau(\lambda)$.

These reference data are supplied by the already proved first integrals, quadratures and explicit parallel Sachs screen of §K.3, rather than by an unknown Jacobi transfer. For example, with $\ell=L/m$,

$$
 \tau(E,\ell)=\int_{3/2}^{5/2}
 \frac{d\rho}{\sqrt{E^2-(1-2/\rho)\ell^2/\rho^2}}.
$$

The reference companion can also be recovered algebraically from that screen. Put $\widetilde n=-\partial_\rho/\dot V_*$, whose denominator has the positive lower bound of §K.3, and set

$$
 \widetilde{\mathcal N}=\widetilde n+
       \sum_Ag_0(\widetilde n,E_{*,A})E_{*,A},\qquad
 \mathcal N_*=\widetilde{\mathcal N}-\tfrac12g_0(\widetilde{\mathcal N},\widetilde{\mathcal N})K_*.
$$

It is the unique null vector orthogonal to the screen with $g_0(K_*,\mathcal N_*)=1$. Differentiating these conditions, using the parallel $K_*,E_{*,A}$, proves that $\mathcal N_*$ is parallel. Thus specifying the reference columns or the cuts requires no optical observable or Jacobi transfer and is not circular.

Fix a finite integer $J$ and exact cut times $t_j(\lambda)=j\tau(\lambda)/J$. At each cut, the incoming and outgoing coordinate parents have a common overlap containing a fixed positive position buffer around $x_*(\lambda,t_j)$. Retain the finitely many interfaces over compact parameter cores with these uniform margins. A fixed compact state neighborhood and its positive buffer are also retained. Only an interface whose incoming approximate position remains in this overlap is used.

Let $g=g_{i,N}$ and $h=g_{k,N}$ be the incoming and outgoing real symmetric dimensionless metric readouts. They are measured in these same coordinates. On their respective buffered position domains assume

$$
 \|g_{i,N}-g_0\|_{C^3}\le\delta_{i,N},\qquad
 \|g_{k,N}-g_0\|_{C^3}\le\delta_{k,N},\qquad
 d_{ik,N}:=\delta_{i,N}+\delta_{k,N}.
$$

Thus $\|h-g\|_{C^0}$ on the overlap is at most $d_{ik,N}$. The switch below uses only this $C^0$ difference; the $C^3$ bounds are used for the actual flows and tidal estimates between cuts. All constants below may depend on the fixed mass, coordinate and frame bounds, finite interface system and compact reference family, but not on $N$.

**The null-frame reset.**

Suppose the incoming state at the cut is $Z^-=(x,K,\mathcal N,E_1,E_2)$ and the incoming frame $F=(K,\mathcal N,E_1,E_2)$ has Gram matrix $Q$ for $g(x)$. Write $\mathcal E^-=\|Z^--Z_*(\lambda,t_j)\|$ in the maximum of the five fixed coordinate-block norms. All reference vector components in this comparison are taken at the exact cut.

At the approximate position $x$ apply Lemma K.11 with the incoming metric and its actual normalized frame as the reference, and with $h(x)$ as the perturbed metric. Its formulas are as follows. Put

$$
 q=h(K,K),\qquad b_0=h(K,\mathcal N),\qquad d=h(\mathcal N,\mathcal N),\qquad
 a=-\frac{q}{b_0+\sqrt{b_0^2-dq}},\qquad K^+=K+a\mathcal N.
$$

The square root is the positive branch near $1$. This expression is valid also when $d=0$ and is the root tending to zero of $h(K+a\mathcal N,K+a\mathcal N)=0$. Define

$$
 \begin{aligned}
 b&=h(K^+,\mathcal N),&
 \mathcal N^+&=b^{-1}\left(\mathcal N-\frac{h(\mathcal N,\mathcal N)}{2b}K^+\right),\\
 P_h(w)&=w-h(w,\mathcal N^+)K^+-h(w,K^+)\mathcal N^+,&
 W&=(P_h(E_1),P_h(E_2)),\\
 H_{\rm temp}&=-W^ThW,&
 E_{\rm temp}&=W H_{\rm temp}^{-1/2}.
 \end{aligned}
$$

The last inverse square root is the positive symmetric one. The formulas give $h(K^+,K^+)=h(\mathcal N^+,\mathcal N^+)=0$, $h(K^+,\mathcal N^+)=1$, and

$$
 E_{\rm temp}^ThE_{\rm temp}=-I_2,\qquad
 h(E_{{\rm temp},A},K^+)=h(E_{{\rm temp},A},\mathcal N^+)=0.
$$

There are constants $\epsilon_*>0$ and $C_{\rm n}<\infty$, common to all the finitely many interfaces, such that if $\mathcal E^-+d_{ik,N}<\epsilon_*$ these formulas are defined and

$$
 b_0>\tfrac12,\qquad b>\tfrac12,\qquad
 \|H_{\rm temp}-I_2\|<\tfrac12,\qquad
 \|F_{\rm temp}-F\|\le C_{\rm n}d_{ik,N},
 \quad F_{\rm temp}=(K^+,\mathcal N^+,E_{\rm temp}).
$$

Here and below a four-column frame norm is the induced Euclidean operator norm, with fixed finite conversions to the state-block norm. To prove the assertions uniformly, at $h=g$ one has $q=d=a=0$, $b_0=b=1$, $H_{\rm temp}=I_2$ and $F_{\rm temp}=F$. The displayed formulas are real analytic on a fixed neighborhood of the compact reference data. A smaller closed neighborhood keeps the denominators and eigenvalues in the stated margins. Its derivative bounds are finite. Applying the mean-value formula with the source frame held fixed gives the last estimate. For instance, $|q|\le\|h-g\|\|K\|^2$ and the displayed root formula gives $|a|\le2|q|$ once $b_0>1/2$; no inverse power of a metric error is used. This is precisely the uniform version of Lemma K.11, now with the actual incoming frame as reference.

There is no change of the cut time or of the affine clock: the next segment starts at the same $(x,t_j)$ with tangent $K^+$. In particular, $K^+$ is generally different from $K$, but it is not multiplied by an additional affine-scale factor.

Define the full-frame map at this point by

$$
 L=F_{\rm temp}F^{-1}.
$$

It is an actual isometry from $(T_xM,g(x))$ to $(T_xM,h(x))$:

$$
 L^ThL=g,\qquad LK=K^+,\qquad L\mathcal N=\mathcal N^+,\qquad LE_A=E_{{\rm temp},A}.
$$

Moreover $\|L-I_4\|\le C_Ld_{ik,N}$. Indeed $F^{-1}=Q^{-1}F^Tg$, so its norm is uniformly bounded by the retained metric and frame bounds, and $L-I_4=(F_{\rm temp}-F)F^{-1}$. On the small connected neighborhood this map preserves the retained orientation and time orientation. The path obtained by replacing $h$ with $g+s(h-g)$ starts at the identity and specifies its near-identity full spin lift. An existing central spin label is not discarded.

**The target screen and the recorded phase.**

Let $\mathsf E_*=(E_{*,1}(\lambda,t_j),E_{*,2}(\lambda,t_j))$ be the coordinate-component columns of the known exact parallel screen at the cut. For this pointwise operation extend those columns locally as constant coordinate vector fields. Evaluate them at the approximate position $x$, and set

$$
 W_*=(P_h(E_{*,1}),P_h(E_{*,2})),\qquad
 H_*=-W_*^ThW_*,\qquad
 E^+=W_*H_*^{-1/2}.
$$

The constant-coordinate extension is a specified use of the common EF chart, not an assertion that these extended fields are parallel. After the switch, the initial columns $E^+$ are parallel transported by $h$ along the next approximate segment.

At the exact state and exact metric these formulas give $E^+=E_{\rm temp}=\mathsf E_*$. Compactness and a smaller common $\epsilon_*$ give $\|H_*-I_2\|<1/2$ throughout the retained neighborhood. Thus $E^+$ is an oriented orthonormal basis of the same two-plane

$$
 \mathcal S^+=\{w:h(w,K^+)=h(w,\mathcal N^+)=0\}
$$

as $E_{\rm temp}$. Define the actual, computed transition matrix

$$
 R_{AB}=-h(E_A^+,E_{{\rm temp},B}).
$$

Then

$$
 E_{\rm temp}=E^+R,\qquad R^TR=I_2,\qquad \det R=1.
$$

The first identity follows by orthonormal expansion in the common negative-definite plane, and the second by taking its Gram matrix. The sign of the determinant is positive at the reference data and remains so on the retained neighborhood; equivalently require $\|R-I_2\|<1$. Hence $R\in SO(2)$. Its near-identity spin lift, when retained, is specified by the same continuous choice. The target full-spin frame is the lifted temporary frame followed by the lift of $\operatorname{diag}(I_2,R^{-1})$, since $F^+=F_{\rm temp}\operatorname{diag}(I_2,R^{-1})$. Thus its central label is transported from the source lift, not recovered from the target frame columns alone.

There are common constants $A_{\rm sw},B_{\rm sw},C_{\rm ph}$ such that the reset state $Z^+=(x,K^+,\mathcal N^+,E_1^+,E_2^+)$ satisfies

$$
 \begin{aligned}
 \mathcal E^+
   &\le A_{\rm sw}\mathcal E^-+B_{\rm sw}d_{ik,N},\\
 \eta_{ik,N}:=\|\operatorname{diag}(R,R)-I_4\|
   &\le C_{\rm ph}(\mathcal E^-+d_{ik,N}).
 \end{aligned}
$$

For the first bound, the temporary frame differs from the incoming frame by $C_{\rm n}d_{ik,N}$. The target-screen formula is a fixed smooth function of $h(x),K^+,\mathcal N^+$ and the exact reference columns. At the reference data its value is $\mathsf E_*$. Also

$$
 \|h(x)-g_0(x_*)\|
 \le\delta_{k,N}+\|Dg_0\|\,|x-x_*|.
$$

The retained compact derivative bounds therefore give $\|E^+-\mathsf E_*\|\le C(\mathcal E^-+d_{ik,N})$, proving the state bound after including the unchanged position. For the second bound, use

$$
 R-I_2=-(E^+)^Th(E_{\rm temp}-E^+)
$$

and the same bounds for both screen matrices. All these constants are suprema on a fixed compact neighborhood, chosen before $N$. The number of interfaces is finite, so taking their maxima and the smallest of their positive margins preserves this independence.

**Covariant Jacobi jets and the phase switch.**

At a normalized state use the screen quotient

$$
 \mathscr S(K)=K^{\perp_g}/\mathbb RK
$$

with positive metric induced by $-g$. The incoming $E_A$ identify it with $\mathbb R^2$; the companion $\mathcal N$ merely chooses representatives. Along an actual metric-null geodesic, the transverse Jacobi phase consists of the value class $[J]$ and covariant slope class $[V]$, with $V=\nabla_KJ$. Its phase coordinates are $z=(q,p)$, where

$$
 [J]=[Eq],\qquad [V]=[Ep],\qquad p=\dot q
$$

in the parallel screen. Actual Jacobi lifts with these classes may have longitudinal components. The transverse equation and its Cauchy phase do not depend on those components.

Every pair of screen classes has a full Jacobi solution with representatives in $K^\perp$ initially: solve the ordinary Jacobi Cauchy problem with the chosen representatives of its two slots. Metric compatibility and the curvature symmetries keep $g(J,K)=g(V,K)=0$. Changing the initial representatives by multiples of $K$ adds a longitudinal Jacobi field $(a+bt)K$ and hence leaves the transverse solution unchanged.

Prescribe the interface map on covariant Cauchy jets by

$$
 (J,V)^+=(LJ,LV).
$$

Since $L$ is an isometry and $LK=K^+$, it maps $K^{\perp_g}$ to $(K^+)^{\perp_h}$ and $\mathbb RK$ to $\mathbb RK^+$. Consequently the rule induces a well-defined isometry on the screen quotient for each of the two jet slots. Its coordinate rule in the target screen is exactly

$$
 z^+=\mathsf C_{ik,N}z^-,
 \qquad
 \mathsf C_{ik,N}=\operatorname{diag}(R,R).
$$

Indeed $LEq=E_{\rm temp}q=E^+Rq$, and the same computation holds for $V$. Longitudinal representatives map to longitudinal representatives, so they introduce no correction to this formula.

With $\mathbb J=\left(\begin{smallmatrix}0&I_2\\-I_2&0\end{smallmatrix}\right)$,

$$
 \mathsf C_{ik,N}^T\mathbb J\mathsf C_{ik,N}=\mathbb J.
$$

Thus the switch is symplectic and preserves the transverse Jacobi Wronskian. This is also the direct consequence of $L^ThL=g$ applied to $-g(J,\widetilde V)+g(V,\widetilde J)$. There is no derivative-of-$R$ term: the rule specifies Cauchy data at one cut, and the outgoing screen is initialized there and then parallel transported. It is not a time-dependent rotation of a single screen along one uninterrupted segment.

The coordinate derivative corresponding to this covariant jet reset is explicitly

$$
 \dot J^{+\,\mu}=(LV)^\mu
       -\Gamma(h)^\mu_{\alpha\beta}(K^+)^\alpha(LJ)^\beta.
$$

Therefore copying a raw coordinate derivative across a metric switch would generally give a different rule. The formula prescribes a valid Jacobi Cauchy jet for the outgoing metric. It does not differentiate the nonlinear null-frame reset map, nor does it assert $\nabla^h_{K^+}(LJ)=LV$ for a previously chosen field of maps $L$ away from this cut.

The reference switch is the identity: at $Z^-=Z_*$ and $g=h=g_0$ one has $a=0$, $L=I_4$, $E^+=E_{\rm temp}=\mathsf E_*$ and $R=I_2$. This identifies the exact comparison phase without a new screen gauge. The rule is nevertheless nontrivial. If $g=h=g_0$, $K,\mathcal N$ are exact and the incoming screen is $\mathsf E_*R_0$ for a small nonidentity $R_0\in SO(2)$, then $L=I_4$, the target screen is $\mathsf E_*$, and the recorded phase switch is $\operatorname{diag}(R_0,R_0)$. The physical jet is unchanged while its coordinates are correctly carried into the target frame.

**Piecewise propagation and scope.**

On each subinterval integrate the actual null geodesic and parallel frame of its own readout metric, together with the actual transverse Jacobi equation of that metric. Its tidal matrix is real symmetric, so the corresponding four-dimensional transfer $U_{j,N}$ is symplectic. At a cut use the state reset above and record the computed matrix $\mathsf C_{j,N}$. The full optical algorithm uses, in the stipulated order,

$$
 U_{J-1,N}\mathsf C_{J-1,N}U_{J-2,N}
       \cdots \mathsf C_{1,N}U_{0,N}.
$$

Every factor and hence the product is symplectic. Earlier frame and phase discrepancies remain in the incoming state, in $R$, and in this accumulated product. Reinitializing the target frame does not authorize replacing $\mathsf C_{j,N}$ by the identity or resetting the accumulated transfer.

The local state-flow estimates of Theorem K.12 apply on each retained interval with its actual initial error. The two switch inequalities supply the interface contributions to their finite iteration. Neither a missing initial-error term nor a reset-dependent affine rescaling is suppressed.

In the fixed scalar position units used above, $p=dq/dt=m\,dq/du$. If physical unit-screen coefficients are used instead of coefficients in $E_A$, both $q$ and $p$ acquire the same constant factor $m$, which leaves the four-by-four transfer unchanged. Once the position units are fixed, the conversion between $(q,dq/du)$ and $(q,dq/dt)$ is the single global conjugation $\operatorname{diag}(I_2,mI_2)$ of §K.4. No additional clock conversion occurs at an interface.

The construction is an explicitly prescribed piecewise optical approximation. Its position is continuous and each open segment is an actual readout-metric null geodesic; tangents, frames and Jacobi jets have the displayed small interface resets. It need not be a geodesic of a globally glued approximate metric, and its optical transfer is not asserted to be the derivative of a global nonlinear geodesic flow or of the nonlinear state-reset algorithm. The exact cuts and reference parallel-frame values are specified Schwarzschild benchmark data supplied by §K.3, independently of the optical transfer being approximated. The construction does not give a numerical certification from finitely many twistor coefficients alone. These distinctions do not affect the proved state, phase, Wronskian and finite-product rules. ∎


<div id="sec:fro-c-accumulation"></div>

## C. Finite accumulation and full phase observables

Use the finite readouts and reset maps of §§A–B. The reference is the fixed positive-mass Schwarzschild family of §K.3 with signature $(+,-,-,-)$. All comparisons use its original individual affine intervals and exact terminal times.

<div id="sec:fr-opt-c-setting"></div>

### C.1. Fixed finite data and local bounds

Write $\lambda=(E,\ell)\in[1,2]\times[1/4,1/2]$ for the parameters of the original nonradial family. Keep its physical affine parameter $u$, dimensionless time $t=u/m$, entrance $r=5m/2$ and exact final time $\tau_\lambda$, so that

$$
 \tau_-:=\frac{10}{21}<\tau_\lambda<\tau_+:=\frac{100}{99}.
$$ {#eq:fr-opt-c-time-bounds}

Keep the polar-first parallel Sachs frame of §K.3 and a parallel null companion. In the common dimensionless EF coordinates $X=(v/m,r/m,\theta,\phi)$, let

$$
 g_0=\bar g=m^{-2}g_m,\qquad
 Z_\lambda=(X,K,\mathcal N,E_1,E_2),\qquad
 K=dX/dt,\qquad g_0(K,\mathcal N)=1,\qquad
 g_0(E_A,E_B)=-\delta_{AB}.
$$ {#eq:fr-opt-c-dimensionless-convention}

The displayed $g_m$ includes the coordinate Jacobian factors. The physical tangent, companion and unit screen vectors are $(K,\mathcal N,E_1,E_2)/m$, and $u=mt$ throughout. These states and their prescribed coordinate descriptions range over a compact set. The screen phase is a different space: $y=(\xi,p)\in\mathbb R^2\oplus\mathbb R^2$, with $p=d\xi/dt=m\,d\xi/du$. Using physical unit-screen position coefficients instead of the coefficients in $E_A$ multiplies both phase slots by the same constant $m$ and leaves the four-by-four transfer unchanged. Fix one such position convention throughout.

The finite schedule has $J$ slabs and nodes

$$
 t_j(\lambda)=\frac{j\tau_\lambda}{J},\qquad
 h_j=t_{j+1}-t_j,\qquad 0\le j<J.
$$ {#eq:fr-opt-c-schedule}

The parameter set may have finitely many compact cells, with a specified finite list of readouts on each cell. Every bound below is a maximum over this finite list and its compact parameter sets. Neither this list nor $J$, the nodes, parents, exact coordinate comparisons or reset rules depend on $N$.

Here slab $j=0,\ldots,J-1$ uses Theorem A.1's label $i_j=i(a,j+1)$; its nodes and enlarged domains are unchanged.

The exact times $\tau_\lambda$ are the quadratures of §K.3.2, and the reference Sachs frame is the explicit parallel frame of §K.3.3. They, the specified companion and the exact readout-to-physical coordinate comparisons are retained benchmark data. They are not values of the unknown Jacobi transfer obtained in advance: the new $U_N$ below is obtained from the local approximate Jacobi equations and the specified switch maps. The conclusion is an approximation theorem with these exact inputs, not numerical certification from finite source coefficients alone.

For readout $i$, use Proposition A.2 and its finite-algebra readout followed by coefficient-polynomial evaluation at one. In the fixed dimensionless EF coordinates let $g_{i,N}$ be the real tensor obtained after the same constant rescaling by $m^{-2}$. Its exact value at amplitude one is the reference metric $g_0$. The local result supplies, on an inflated inner position domain with a positive additional buffer,

$$
 \|D^s(g_{i,N}-g_0)\|\le D_{i,s}\beta_N,
 \qquad 0\le s\le3,\qquad
 \beta_N=\frac{T_{\min}^{-N-1}}{1-T_{\min}^{-1}},
 \quad T_{\min}>1.
$$ {#eq:fr-opt-c-local-metric-tail}

All $D_{i,s}$ are finite and independent of $N$. Exact coordinate/frame comparisons and the fixed metric factor $m^{-2}$ are included in these bounds before taking finite maxima. Different $g_{i,N}$ need not agree on overlaps. There is no use of a single approximate spacetime metric or of a physical gluing of different source amplitude families away from amplitude one.

On the retained compact state tubes fix uniform metric inverse, connection, derivative and vector bounds. Choose an initial tail threshold $\bar\beta>0$ so that the local real-signature, inverse-unit and null/frame normalizations hold whenever $\beta_N\le\bar\beta$. With $D_0=\max_iD_{i,0}$, also take $D_0\bar\beta<\beta_g$; this condition is automatic if $D_0=0$. These are possible because there are finitely many strictly positive margins. The reference state is interior to each slab and switch domain, and the position projection of the larger state tube is inside that readout's inner $C^3$ domain.

Here are the local state bounds used in the proof. Set $E_j^+=\|Z_N(t_j^+)-Z(t_j)\|$. Up to a possible first exit on slab $j$, the joint geodesic/parallel-frame equation gives

$$
 \sup_{t_j\le t\le t_{j+1}}
       \|Z_N(t)-Z(t)\|
 \le a_j E_j^+ +b_j\beta_N,
 \qquad a_j\ge1,\quad b_j\ge0.
$$ {#eq:fr-opt-c-local-state-flow}

One can take, for example, $a_j=e^{L_j\tau_+/J}$ and
$b_j=e^{L_j\tau_+/J}(\tau_+/J)F_j$, where $L_j$ is a Lipschitz bound for the dimensionless-$t$ state equation on the larger tube and $F_j\beta_N$ bounds the difference of its vector fields there. This follows from the integral inequality with initial error $E_j^+$, not only from a zero-error initialization. At time $t_{j+1}$ write $E_{j+1}^-$ for the incoming error.

The actual reset normalizes this incoming state with the target metric and the same specified affine-clock rule. It uses the small null root, null-companion normalization, positive Gram square root and the prescribed oriented screen alignment. Its compact-neighborhood estimate is

$$
 E_{j+1}^+\le r_{j+1}E_{j+1}^-+c_{j+1}\beta_N,
 \qquad r_{j+1}\ge1,\quad c_{j+1}\ge0.
$$ {#eq:fr-opt-c-local-reset}

These constants exist for the actual finite-matrix reset, rather than for a replacement by the exact state. Indeed its null equation has nonzero derivative at the reference root; its scalar denominators and Gram matrices have the retained nonzero or positive margins. The small root and positive square root are analytic on a common smaller neighborhood. The target screen is obtained by projecting the globally parallel exact Sachs frame into the target screen and normalizing its positive Gram matrix. At the exact metric and exact state all these operations return that same reference state and frame. On a fixed smaller compact neighborhood, suprema of the first derivatives of this finite collection of maps give $r_{j+1}$ and $c_{j+1}$ by the mean-value formula. The metric perturbations at the reset are bounded by the source and target versions of [@eq:fr-opt-c-local-metric-tail]. The incoming error is retained in [@eq:fr-opt-c-local-reset].

For example Lemma B.1's constants permit
$r_{j+1}=\max\{1,A_{{\rm sw},j+1}\}$ and
$c_{j+1}=B_{{\rm sw},j+1}(D_{i_j,0}+D_{i_{j+1},0})$
at an actual switch. The final endpoint convention below has no target readout and uses no such reset.

At the first entrance keep the full initialization estimate

$$
 E_0^+\le c_0\beta_N.
$$ {#eq:fr-opt-c-initial-error}

For example $c_0=C_{\rm init}D_{i_0,0}$, with any fixed coordinate/frame constants included, is permitted by Lemma K.11. This term is not set to zero merely because a later slab has a different central mark.

<div id="prop:fr-opt-c-state-accumulation"></div>

**Proposition C.1 (Finite state accumulation).**

There are a finite $C_Z$ and an integer $N_0$, depending only on the fixed finite schedule, its readouts and buffers, such that every $N\ge N_0$ admits every slab evolution and every prescribed reset on its full scheduled domain. Throughout every slab, and on both sides of every reset,

$$
 \|Z_N-Z\|\le C_Z\beta_N.
$$ {#eq:fr-opt-c-global-state}

*Proof.* For the last endpoint put $r_J=1,c_J=0$, meaning that there is no reset there. For $0\le j<J$ set

$$
 A_j=r_{j+1}a_j,\qquad
 B_j=r_{j+1}b_j+c_{j+1},\qquad
 H_0=c_0,\qquad H_{j+1}=A_jH_j+B_j.
$$ {#eq:fr-opt-c-state-majorant-recursion}

The finite recurrence has the explicit solution

$$
 H_j=c_0\prod_{\ell=0}^{j-1}A_\ell
     +\sum_{k=0}^{j-1}B_k
                    \prod_{\ell=k+1}^{j-1}A_\ell,
 \qquad
 C_Z=\max\left\{\max_{0\le j\le J}H_j,
                  \max_{0\le j<J}(a_jH_j+b_j)\right\}.
$$ {#eq:fr-opt-c-state-product-sum}

Empty products equal one and empty sums zero. Thus all constants are fixed before $N$ is chosen. In particular this bound includes $c_0$ and the error carried through every switch; it does not restart the error estimate at zero.

Choose a single positive tail threshold small enough that $C_Z\beta_N$ is less than half of every retained slab state buffer. Also require it to be less than the position buffers after applying their fixed coordinate comparison bounds. There are finitely many reset-domain tests: their errors are bounded by finite linear combinations of the incoming state error and the source and target metric errors. Decrease the same threshold so that each such combination is less than half its positive margin. More explicitly, if a test requires $\alpha_qE+ d_q\beta_N<\mu_q$ with $\mu_q>0$, impose

$$
 (\alpha_q C_Z+d_q)\beta_N<\mu_q/2.
$$ {#eq:fr-opt-c-margin-test}

Tests with zero left-hand coefficient need no restriction. Include $\beta_N\le\bar\beta$. Their finite minimum is a strictly positive threshold $\beta_*$.

Now prove existence and the bounds together by finite induction. The initial normalization exists at this threshold and [@eq:fr-opt-c-initial-error] gives $E_0^+\le H_0\beta_N$. If the solution on slab $j$ had a first exit before $t_{j+1}$, the integral estimate valid up to that exit would give error at most $(a_jH_j+b_j)\beta_N\le C_Z\beta_N$, strictly inside its retained state and position buffers. This contradicts a first exit. The ODE therefore continues to the slab endpoint inside its compact parent, and $E_{j+1}^-\le(a_jH_j+b_j)\beta_N$.

The reset tests are satisfied by [@eq:fr-opt-c-margin-test], so the actual reset exists. Its bound gives
$E_{j+1}^+\le[A_jH_j+B_j]\beta_N=H_{j+1}\beta_N$,
again strictly inside the next slab's initialization neighborhood. This proves the induction and all switch assertions. Since $T_{\min}>1$, $\beta_N\to0$; choose $N_0$ so that $\beta_N<\beta_*$ for all $N\ge N_0$. Equivalently it suffices to take $T_{\min}^{N+1}>[(1-T_{\min}^{-1})\beta_*]^{-1}$. No numerical value of this sufficient order is asserted. ∎

<div id="sec:fr-opt-c-tidal"></div>

### C.2. Tidal coefficients on the accepted slabs

All local estimates now hold on the whole scheduled slabs. Apply the generic calculations of results K.10–K.12 directly to $g_0$ and $g_{i,N}$ in the $t$-clock and unit-$g_0$ frame convention above. Let $D_s=\max_iD_{i,s}$ and retain common $G,K_s,V,R_0,R_1$ in these coordinates. Thus $\|g_0^{-1}\|\le G$, $\|D^sg_0\|\le K_s$, the reference and approximate vector components have norm at most $V$, and $R_0,R_1$ bound the exact curvature operator and its first coordinate derivative. Fixed mass factors are already included in the coordinate readout constants.

The metric $C^3$ estimate gives a curvature $C^1$ estimate on these tubes. To check this directly, express $\Gamma$ by $g_0^{-1}Dg_0$ and $R$ by $D\Gamma+\Gamma\Gamma$, and use the same formulas for each $g_{i,N}$. Each component of $(R,DR)$ is a finite sum of products of inverse metric entries and metric derivatives of order at most three. On the retained inverse margins, replace one factor at a time and use [@eq:fr-opt-c-local-metric-tail]. The result is a finite constant $C_{R,1}$, independent of $N$, with $\|R_{i,N}-R\|_{C^1}\le C_{R,1}\beta_N$. In particular the exact $R_1$ used to move the evaluation point is bounded on the same tube; this is not inferred from a curvature $C^0$ estimate alone.

For an explicit admissible $C^0$ curvature constant define

$$
 \begin{aligned}
 \gamma_0&=3G(K_1+1),\\
 d_0^*&=6G^2(K_1+1)D_0+3GD_1,\\
 d_1^*&=\{24G^3(K_1+1)^2+6G^2(K_2+1)\}D_0
          +12G^2(K_1+1)D_1+3GD_2,\\
 d_R^*&=2d_1^*+4\gamma_0d_0^*.
 \end{aligned}
$$ {#eq:fr-opt-c-tidal-input-constants}

The smallness conditions in Lemma K.10 are included when choosing $N_0$. Its proof gives $\|R_{i,N}-R\|\le d_R^*\beta_N$. In the present convention the exact tidal matrix is $\mathcal R_{AB,t}=-g_0(R(E_A,K)K,E_B)$. Replacing its metric, curvature and four vector factors and moving the position, exactly as in Theorem K.12, gives on each slab a dimensionless coefficient bound

$$
 \|\mathsf A_{j,N}(t)-\mathsf A_\lambda(t)\|
 \le\kappa_N:=K_{\rm tid}\beta_N,
$$ {#eq:fr-opt-c-coefficient-bound}

where one valid finite choice is

$$
 \begin{aligned}
 K_{\rm tid}=\bigl[&2V^4\{R_0D_0+(K_0+1)d_R^*\}\\
 &+2\{V^4(K_1R_0+K_0R_1)+4K_0R_0V^3\}C_Z\bigr].
 \end{aligned}
$$ {#eq:fr-opt-c-tidal-constant}

Each state norm and coordinate comparison is the one used in obtaining $C_Z$. There is no additional $m^2$ factor here: $-g_0(R(E_A,K)K,E_B)$ is already the dimensionless tidal coefficient, equal to $m^2$ times its physical-$u$, unit-physical-frame counterpart. More generally the same calculation before substituting Proposition C.1 gives a bound $C(\beta_N+\|Z_N-Z\|)$.

On a slab use its own real metric, null tangent and parallel orthonormal screen. Its tidal matrix is symmetric, even though $g_{i,N}$ need not be Einstein. Therefore

$$
 \mathsf A_{j,N}(t)=
 \begin{pmatrix}0&I_2\\-\mathcal R_{j,N,t}(t)&0\end{pmatrix},
 \qquad
 \mathsf A_{j,N}^{\mathsf T}\mathsf J+
                  \mathsf J\mathsf A_{j,N}=0,
 \qquad
 \mathsf J=\begin{pmatrix}0&I_2\\-I_2&0\end{pmatrix}.
$$ {#eq:fr-opt-c-local-hamiltonian}

The matrices in [@eq:fr-opt-c-coefficient-bound] are expressed in the corresponding ordered screen components. The state comparison includes the chosen alignment to the global exact Sachs frame; arbitrary independent screen rotations are not silently suppressed.

<div id="prop:fr-opt-c-phase-accumulation"></div>

**Proposition C.2 (Piecewise Jacobi Cauchy transport).**

Let $V_{j,N}$ be the exact fundamental matrix on slab $j$, initialized by the identity at $t_j$. At switch $j$, use the oriented orthogonal screen identification supplied by the reset construction. In Cauchy components its phase map is

$$
 C_{j,N}=\operatorname{diag}(R_{j,N},R_{j,N}),
 \qquad R_{j,N}\in\operatorname{SO}(2),
 \qquad 1\le j<J.
$$ {#eq:fr-opt-c-screen-jump}

Its exact reference is $C_j=I_4$, because both the temporary and target screen reduce to the same globally parallel exact Sachs frame when the metric errors and incoming state error vanish. There are finite $H_j^{\rm rot}$ such that

$$
 \eta_{j,N}:=\|C_{j,N}-I_4\|
 \le H_j^{\rm rot}\beta_N,\qquad
 H_{\rm rot}:=\sum_{j=1}^{J-1}H_j^{\rm rot}<\infty.
$$ {#eq:fr-opt-c-jump-error}

Define the piecewise Jacobi Cauchy transport by solving the slab Jacobi equation and imposing $y(t_j^+)=C_{j,N}y(t_j^-)$. Its complete endpoint matrix is

$$
 U_N=V_{J-1,N}C_{J-1,N}\cdots C_{1,N}V_{0,N}.
$$ {#eq:fr-opt-c-global-transport}

Then $U_N$ is symplectic and

$$
 \|U_N-\Phi_\lambda(\tau_\lambda,0)\|
 \le e^{(1+\kappa_N)\tau_\lambda}
       \left(\tau_\lambda\kappa_N+
                    \sum_{j=1}^{J-1}\eta_{j,N}\right).
$$ {#eq:fr-opt-c-product-error}

Here $\Phi_\lambda$ is exactly the original §K.3 transport, in its original polar-first screen and dimensionless phase. This Cauchy transport is not asserted to be the derivative of the nonlinear state-reset map.

*Proof.* The oriented screen identification is analytic near the exact framed state: projection, positive Gram normalization and the oriented orthogonal factor are finite matrix operations on the retained positive margins. At the exact state its rotation is the identity. Its derivative is uniformly bounded on the finite compact reset neighborhoods. Its mean-value estimate is

$$
 \eta_{j,N}\le c_j^{\rm rot}
    \bigl(E_j^-+D_{i_{j-1},0}\beta_N+D_{i_j,0}\beta_N\bigr),
$$ {#eq:fr-opt-c-rotation-input-error}

with any finite matrix/coordinate factors included. Proposition C.1 thus permits
$H_j^{\rm rot}=c_j^{\rm rot}(C_Z+D_{i_{j-1},0}+D_{i_j,0})$.
In particular the jump estimate carries the incoming state error; it does not erase it.

With the common $g_0$ and $t$-clock convention, one may take $c_j^{\rm rot}=C_{{\rm ph},j}$ from Lemma B.1. The fixed coordinate/state-block conversions are included in that constant.

Symmetry in [@eq:fr-opt-c-local-hamiltonian] proves $V_{j,N}^{\mathsf T}\mathsf JV_{j,N}=\mathsf J$ by differentiation. Orthogonality gives $C_{j,N}^{\mathsf T}\mathsf JC_{j,N}=\mathsf J$ and $\|C_{j,N}\|=1$. Thus the full product is symplectic. The definition explicitly transports both displacement and slope components with the same orthogonal identification, in the common physical clock $u=mt$. It is a well-defined linear phase model attached to the reset ray/frame. It does not require a derivative of that reset on a family of spacetime rays.

The exact Sachs generator has norm one. By [@eq:fr-opt-c-coefficient-bound], the approximate generator has norm at most $1+\kappa_N$. On a slab of length $h_j$ the two fundamental matrices satisfy

$$
 \|V_{j,N}\|\le e^{(1+\kappa_N)h_j},\qquad
 \|V_j\|\le e^{h_j},\qquad
 \|V_{j,N}-V_j\|\le h_j\kappa_N e^{(1+\kappa_N)h_j}.
$$ {#eq:fr-opt-c-slab-matrix-error}

The last inequality is Duhamel's integral formula. Compare the finite products factor by factor, inserting $I_4$ at each exact switch. A slab-difference term is bounded by $h_j\kappa_N e^{(1+\kappa_N)\tau_\lambda}$; a jump-difference term is bounded by $\eta_{j,N}e^{(1+\kappa_N)\tau_\lambda}$. The remaining jump factors all have norm one, so no product of $1+\eta_{j,N}$ is introduced. Summing and using $\sum_jh_j=\tau_\lambda$ gives [@eq:fr-opt-c-product-error]. The same argument applies to every partial product, with its elapsed time and switches. This also proves exact composition of this piecewise Cauchy transport at any retained cut, including a cut just before or just after a reset. ∎

<div id="cor:fr-opt-c-effective-error"></div>

**Corollary C.3 (A uniform effective coefficient error).**

Put

$$
 \varepsilon_N=\kappa_N+\frac{H_{\rm rot}\beta_N}{\tau_-}
  =\left(K_{\rm tid}+\frac{H_{\rm rot}}{\tau_-}\right)\beta_N.
$$ {#eq:fr-opt-c-effective-epsilon}

For $N\ge N_0$ large enough that $\varepsilon_N\le1/10$, the full transfer satisfies

$$
 \|U_N-\Phi_\lambda(\tau_\lambda,0)\|
 \le4\varepsilon_N=:\delta_N,\qquad \|U_N\|<4,
$$ {#eq:fr-opt-c-four-epsilon}

uniformly for the entire original compact ray family. The transfer inequality is strict when $\varepsilon_N>0$.

*Proof.* Since $\tau_\lambda>\tau_-$,
$\tau_\lambda\kappa_N+\sum_j\eta_{j,N}\le\tau_\lambda\varepsilon_N$.
Moreover $\kappa_N\le\varepsilon_N$. Consequently Proposition C.2 bounds the transfer difference by
$\tau_\lambda\varepsilon_Ne^{(1+\varepsilon_N)\tau_\lambda}$.
Here $(1+\varepsilon_N)\tau_\lambda<10/9$. The elementary estimates
$e<11/4$ and $e^{1/9}\le9/8$ give $e^{10/9}<99/32$, whence

$$
 \tau_\lambda e^{(1+\varepsilon_N)\tau_\lambda}
 <\frac{100}{99}\frac{99}{32}=\frac{25}{8}<4.
$$

The product norm is at most $e^{(1+\kappa_N)\tau_\lambda}<99/32<4$ because every jump has norm one. If $\varepsilon_N=0$, the coefficient and jump errors vanish and the transfer difference is zero. This proves both assertions. All choices remain independent of $N$, and increasing $N$ meets the final smallness condition. ∎

<div id="prop:fr-opt-c-observables"></div>

**Proposition C.4 (Forward observations and conditional inverse observations).**

Under the hypotheses of Corollary C.3, in particular $N\ge N_0$ and $\varepsilon_N\le1/10$, write $\Phi_\lambda=\left(\begin{smallmatrix}A&B\\C&D\end{smallmatrix}\right)$ and $U_N=\left(\begin{smallmatrix}A_N&B_N\\C_N&D_N\end{smallmatrix}\right)$ in the endpoint phases just specified. Let $\delta_N=4\varepsilon_N$. Then the outgoing phase of an initial component vector of norm at most $J_0$ has error at most $J_0\delta_N$. If the initial phase itself is approximated with error $\eta_0$, its total outgoing error is at most $4\eta_0+J_0\delta_N$.

For point-source Cauchy data in this piecewise phase model, $\xi(0)=0$ and $p(0)=m\,d\xi/du(0)$, so its endpoint response block to the physical slope is $mB_N$. The oriented area observations $\mathcal O_N=m^2\det B_N$ and $\mathcal O=m^2\det B$ satisfy

$$
 |\mathcal O_N-\mathcal O|\le9m^2\delta_N.
$$ {#eq:fr-opt-c-area-error}

If additionally $\delta_N\le3/14$, then

$$
 \sigma_{\min}(B_N)\ge\frac3{14},\qquad
 \|B_N^{-1}\|\le\frac{14}{3},\qquad
 \|B_N^{-1}-B^{-1}\|\le\frac{98}{9}\delta_N.
$$ {#eq:fr-opt-c-inverse-error}

The corresponding inverse difference for $mB_N$ is at most $98\delta_N/(9m)$. On the same margin the dimensionless expansion trace also satisfies

$$
 |\operatorname{tr}(D_NB_N^{-1})-
                  \operatorname{tr}(DB^{-1})|
 \le4\delta_N\left\{\frac73+\|D\|\frac{49}{9}\right\}.
$$ {#eq:fr-opt-c-expansion-error}

The physical-$u$ trace has this bound divided by $m$.

*Proof.* Block projections have norm one, so the global transfer bound gives each block error at most $\delta_N$. The outgoing phase bounds follow from
$U_Ny_N-\Phi y=U_N(y_N-y)+(U_N-\Phi)y$.
The phase identification is oriented orthogonal at the switches; it introduces neither a determinant sign nor an affine-clock dilation. Thus the same physical normalization of the original point-source observation gives $mB_N$.

Since $\varepsilon_N\le1/10$, $\delta_N\le2/5<1$. The two-column determinant identity gives

$$
 |\det B_N-\det B|
 \le2\|B\|\delta_N+\delta_N^2.
$$

For the original exact family, §K.3.7 gives $\|B\|<100/33$. Hence the right-hand side is at most $(200/33+1)\delta_N\le9\delta_N$, proving the area bound; the final inequality is strict when $\delta_N>0$. This use of the constant nine is justified by the new full product estimate, not by an assumption that different metric readouts glue.

The same exact family has $\sigma_{\min}(B)>3/7$. Therefore $\delta_N\le3/14$ implies $\sigma_{\min}(B_N)\ge3/14$ and the inverse norm bound. The inverse identity yields

$$
 B_N^{-1}-B^{-1}=-B_N^{-1}(B_N-B)B^{-1},\qquad
 \|B_N^{-1}-B^{-1}\|
 \le\frac{14}{3}\frac73\delta_N=\frac{98}{9}\delta_N.
$$

For the trace, subtract the products as
$(D_N-D)B_N^{-1}+D(B_N^{-1}-B^{-1})$ and use $|\operatorname{tr}M|\le2\|M\|$. This gives exactly [@eq:fr-opt-c-expansion-error]. The physical clock conversion follows from $p=m\,d\xi/du$, with the same fixed positive mass on every slab. ∎

<div id="sec:fr-opt-c-scope"></div>

### C.3. Relations at singular projections and scope

For every $N$ under consideration, $U_N$ is an invertible symplectic map. Its graph is a four-dimensional Lagrangian relation in the product phase space with forms $-\Omega$ and $\Omega$. It carries every initial Lagrangian plane to a Lagrangian plane even when a position projection is singular. The piecewise Cauchy definition and the forward product and determinant estimates remain meaningful there. An inverse endpoint block or expansion trace requires the explicit singular-value margin in Proposition C.4; it does not follow from symplecticity alone. For the original point-source family that margin persists for sufficiently large $N$ by [@eq:fr-opt-c-inverse-error]. No persistence at a prescribed caustic time of a different initial Lagrangian is asserted.

More explicitly, represent any fixed initial Lagrangian plane by a rank-two matrix $Y_0\in\mathbb R^{4\times2}$ with $Y_0^{\mathsf T}\mathsf JY_0=0$. Then $U_NY_0$ has rank two and the same isotropy identity. With $Q=\operatorname{pr}_{\xi}\Phi_\lambda Y_0$ and $Q_N=\operatorname{pr}_{\xi}U_NY_0$, one has

$$
 \|Q_N-Q\|\le\delta_N\|Y_0\|,\qquad
 |\det Q_N-\det Q|
 \le2\|Q\|\delta_N\|Y_0\|+\delta_N^2\|Y_0\|^2.
$$ {#eq:fr-opt-c-lagrangian-projection-error}

These forward inequalities do not divide by $\det Q$ and therefore remain valid when that projection has a caustic. The full transported plane, rather than an inverse of $Q$, is retained.

The final times are the exact scheduled $t_J=\tau_\lambda$, corresponding to $u=m\tau_\lambda$. The approximate endpoint need not lie exactly on $r=3m/2$. Comparing approximate hitting events instead would require additional time-of-hit and matching estimates; none is used here. The approximate piecewise state need not conserve the exact Schwarzschild $E$ and $L$, although its reference ray is exactly the original family with those parameters.

All finite readout constants, reset derivative bounds, buffers, $C_Z$, $K_{\rm tid}$ and $H_{\rm rot}$ are theoretical finite constants. The finite product/sum and the sufficient tail inequalities specify them and a sufficient $N$ in terms of the chosen parents and local data. They have not been numerically evaluated. The rational constants $4$, $9$, $14/3$ and $98/9$ are explicit and apply by the proofs above. No whole-long-family containment in a single local readout, global approximate metric, off-one physical-amplitude gluing, or variational interpretation of the reset derivative is required by these conclusions.


<div id="thm:fro-full-family"></div>

**Theorem D.1 (Finite-readout approximation of the complete crossing family).**

Fix $m>0$ and the full nonradial family of Proposition 10.2, with its specified entrance, $E\in[1,2]$, $L/m\in[1/4,1/2]$, physical affine clock $u$. The construction uses the exact benchmark cuts, initialized coordinate comparisons and polar-first parallel Sachs reference frame specified in §§A–C. There are a finite parameter cover, a finite local-readout schedule and positive spatial, inverse-unit and frame margins, all chosen independently of $N$, with the following property. There are $T_*>1$, finite constants $C_Z,K_{\rm tid},H_{\rm rot}$ and an integer $N_0$ such that for every $N\ge N_0$ the scheduled degree-$N$ metric readouts and their prescribed state and covariant Cauchy resets exist along every original individual interval $0\le t=u/m\le\tau_\lambda$. Put

$$
 \beta_N=\frac{T_*^{-N-1}}{1-T_*^{-1}},\qquad
 \varepsilon_N=\left(K_{\rm tid}+\frac{H_{\rm rot}}{\tau_-}\right)\beta_N,
 \qquad \tau_-=10/21.
$$ {#eq:fro-main-effective-error}

Use the maximum block norm of $Z=(X,K,\mathcal N,E_1,E_2)$ in dimensionless EF coordinates, with $g_0=m^{-2}g_m$, $t=u/m$ and physical frame $(K,\mathcal N,E_A)/m$. The complete piecewise state has error at most $C_Z\beta_N$, on both sides of every switch and inside every slab. Its full Cauchy transport $U_N$ is symplectic. For $N$ sufficiently large that $\varepsilon_N\le1/10$, at the original exact terminal affine time it obeys

$$
 \|U_N-\Phi_\lambda(\tau_\lambda,0)\|
 \le4\varepsilon_N=:\delta_N,\qquad
 \|U_N\|<4,\qquad
 |m^2\det B_N-m^2\det B|\le9m^2\delta_N.
$$ {#eq:fro-main-full-family-estimates}

Here $B_N$ and $B$ are the endpoint position-response blocks in the same dimensionless-clock phases. The physical-slope response blocks are $mB_N$ and $mB$. If also $\delta_N\le3/14$, then

$$
 \sigma_{\min}(B_N)\ge3/14,\qquad
 \|B_N^{-1}\|\le14/3,\qquad
 \|B_N^{-1}-B^{-1}\|\le(98/9)\delta_N.
$$ {#eq:fro-main-full-family-inverses}

All conclusions are uniform over the original entire parameter rectangle. The forward phase and conditional expansion-trace estimates of Proposition C.4, and the Lagrangian-projection estimates [@eq:fr-opt-c-lagrangian-projection-error], hold as well. The retained exact twistor, full-spin, operator and compact point-module comparisons are those of the original physical atlas.

*Proof.* Theorem A.1 constructs the finite cover, enlarged slabs and buffered node overlaps for the whole parameter rectangle, using the original exact family. Proposition A.2 produces the actual finite-algebra metric readouts and a common tail rate $T_*>1$; take $T_{\min}=T_*$ in §C.1 and enlarge the finite constants $D_{i,s}$ if needed. Proposition A.3 gives their common-coordinate overlap defects and retains the original exact enriched atlas. Lemma B.1 supplies the actual null/frame and covariant Cauchy resets in the same affine clock, including their computed screen rotations. Proposition C.1 proves all-slab and all-switch existence by first-exit induction and gives the state bound. The tidal estimate in §C.2 and Proposition C.2 sum every slab and jump error. Corollary C.3 then gives the transfer estimate with the displayed $\varepsilon_N$. Proposition C.4 gives the physical area and conditional inverse bounds from the original exact endpoint margin. The finite minima and maxima include all parameter cells. Since $\beta_N\to0$, one sufficiently large $N$ meets all these finitely many strict domain and non-strict observation margins. ∎

This theorem provides a finite-readout alternative on the whole original crossing family. Proposition 10.3 remains a conditional single-readout result; the present construction does not establish its single-parent spatial inclusion. The short common-source construction of §§K.6–K.7 remains a separate one-source result. The constants, radii and a sufficient truncation degree of this finite-readout construction are theoretical finite data that have not been numerically evaluated. The constructed object is the piecewise metric and Cauchy model of Lemma B.1, rather than a single approximate metric or the differential of the nonlinear state-reset algorithm.


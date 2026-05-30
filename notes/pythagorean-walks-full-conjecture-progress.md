# Pythagorean Walks: Full Conjecture Progress

Date: 2026-05-30

## Scope

The full conjecture says that the only vertices at graph distance $3$ from
$O=(0,0)$ are
$$
(1,0),\qquad (2,0),\qquad (2,1),
$$
and their images under sign changes and coordinate swap.

This note records proof ingredients for the full conjecture beyond the completed
horizontal-axis subproblem. It is not a proof of the full conjecture.

## Plain-Language Current Status

The grand goal is to prove the full Pythagorean-walks conjecture:
every lattice point except the known distance-three orbit has a two-step
Pythagorean-walk certificate.

Equivalently, after the already solved axis cases and the known obstruction
orbit, the remaining goal is to prove that every non-axis target $(g,h)$ outside
the exceptional sign/swap orbit has some midpoint $P$ such that both
$$
O\to P,\qquad P\to (g,h)
$$
are legal Pythagorean steps.

The proof program has made real progress.  The problem is no longer an
undifferentiated search for midpoints.  The current reduction organizes almost
all targets into explicit certificate families: Gaussian divisor certificates,
two-edge lattice certificates, parallel-direction divisor certificates,
standard completions, orthogonal completions, and promoted root-spine line
families.  These families are backed by executable checks, and many of the
certificate identities have already been promoted to Lean theorems.

The main remaining obstruction is now much narrower.  Some targets lie on a
fixed determinant strip where the expected local divisor class fails.  Early in
the project this looked like a failure of the pinned strip method.  The current
work shows that this interpretation was too local: those targets can still be
certified, but sometimes the certificate must come from a different root-spine
line than the pinned strip originally suggests.  The missing theorem is therefore
a **global root-choice theorem**: after the local divisor and structural
branches fail, choose the right alternate root-spine line and prove that it gives
a valid certificate.

This global obstruction has been made much more explicit.  In the main
radius-$500$ guardrail, there are $105337$ pinned divisor-class failures.  Of
these, $105323$ are discharged by local or structural arguments, and only $14$
require a genuinely alternate root choice.  Those $14$ cases are no longer just
examples: they have been compressed into $14$ portable line/strip rows, coming
from $10$ alternate squareclass line rows.  Each row records:

- the failed pinned strip,
- the alternate line direction,
- the squareclass and split factors,
- the paired-factor residue condition,
- the coefficient congruence needed for the alternate line to meet the pinned
  strip,
- and a representative certificate.

The important point is that these rows are executable proof artifacts.  A row is
not merely a discovered target; it is a reusable congruence recipe saying that a
whole alternate line intersects the failed pinned strip in certificate-producing
targets.  On the Lean side, the initial $14$-row frontier is now represented by
concrete certificate theorems and determinant-congruence theorems, packaged as a
single finite-frontier lemma.

The next improvement was to connect these alternate rows to the reason the local
divisor method failed.  The local failure has a short exponent-signature: a
small finite sumset of possible prime-power exponent residues does not contain
the required exponent.  The current audit records those short signatures and the
alternate line templates that fix them.  In the radius-$500$ frontier, the $14$
global rows compress to $10$ short signatures and $10$ alternate line templates.
Thus the target is no longer "search for an alternate root"; it is:

> Given a short exponent-signature left over by the local divisor method,
> construct one of the matching alternate squareclass line templates and prove
> that it meets the original pinned strip in a valid certificate.

This is the key conceptual achievement of the recent work.  It creates a
target-facing interface between the divisor obstruction and the alternate
certificate families.  The root-spine search can now be replaced, inside finite
guardrails, by signature-template tables that choose the alternate line directly.

The first intended Lean milestone has now been reached.  There is a general
line/strip bridge: once an alternate line family proves a valid certificate, and
the first coefficient satisfies the one-variable determinant congruence for the
original pinned strip, Lean derives both the certificate and the required pinned
strip residue.  This means the global-root-choice work no longer has to prove a
new determinant calculation separately for every representative target.

The work has also moved beyond one example family.  A theorem-backed registry
now records thirty normalized alternate line families, together with the Lean
theorem name proving each family.  These include the full radius-$1000$
signature-template frontier, the original large counterexample family of shape
$(1,2)$, all radius-$1250$ signature-template rows, and the first two
normalized families from the radius-$1500$ frontier.  The executable
proved-family branch only uses templates whose normalized family appears in this
registry.

Inside the radius-$1000$ finite scan, the proved-family branch now covers all
$42$ global root-choice rows.  Those $42$ target hits collapse to $40$ distinct
signature-template rows, and every one of those rows is backed by a normalized
Lean family theorem.  In that guardrail, the alternate branch can therefore be
read as theorem-backed signature-template dispatch rather than root-spine
search.

The finite evidence remains useful but still finite.  Signature-template tables
have been checked through increasing boxes.  Through radius $1250$, pinned
signature-template tables replace the root-spine search in the full finite scan.
Starting from the radius-$1250$ table, an iterated closure process also closes
the sampled boxes at radii $1500$, $1750$, and $2000$: each stage records which
new short signatures and line templates appear, adds them, and then covers the
whole finite box with no missing or mismatched global rows.

This should not be mistaken for the full proof.  The frontier still grows as the
box grows.  More finite rows alone will not prove the conjecture.  What the
finite work has achieved is a precise target for the infinite argument:

> Prove parametrically that every short exponent-signature left after the local
> divisor/Kneser discharge belongs to one of the normalized alternate
> squareclass line-template families, and prove that the corresponding
> line/strip congruence gives a valid two-step certificate.

A good next milestone is to turn the theorem-backed registry into a genuine
case theorem for a natural infinite class of short signatures.  The next proof
should not merely add another finite row: it should explain why a recurring
short-signature pattern forces one of the normalized families already in the
registry, or else add a new normalized family together with the arithmetic reason
that the short signature selects it.  That is the remaining step from
theorem-backed finite frontier to an actual global root-choice proof.

## Symmetry Orbit And Current Reduction

The conjectured distance-$3$ orbit is
$$
\begin{gathered}
(\pm1,0),(0,\pm1),\\
(\pm2,0),(0,\pm2),\\
(\pm2,\pm1),(\pm1,\pm2).
\end{gathered}
$$

The horizontal-axis note proves that every horizontal point $(n,0)$ with
$|n|\ge3$ has distance at most $2$; coordinate swap gives the same result for
vertical points. This sign/swap axis reduction is executable as
`axis_orbit_proof_certificate`. The paper proves that $(1,0)$, $(2,0)$, and
$(2,1)$ have no two-step path, and symmetry gives the same lower bound for every
point in the orbit above.

The remaining task is therefore:

**Non-axis target.** For every $g,h\ne0$ with $(|g|,|h|)\notin\{(1,2),(2,1)\}$,
prove that $(g,h)$ has a two-step certificate.

Executable guardrail for the axis reduction:

- `axis_orbit_proof_certificate`
- `test_axis_orbit_proof_certificate`

The same automorphisms also transport any two-step certificate: if
$O\to P\to T$ is valid, then applying sign changes and optionally swapping the
coordinates to both $P$ and $T$ gives another valid two-step certificate.

Executable guardrail for certificate transport:

- `signed_swap_point`
- `sign_swap_certificate`
- `test_sign_swap_certificate_transport`

## Exact Obstruction Side

The paper's lower-bound arguments for the three representative obstruction
vertices are now recorded as an executable symbolic guardrail. Let $P$ be a
hypothetical two-step midpoint, and let
$$
\delta=\bigl||OP|-|TP|\bigr|.
$$
By the triangle inequality, $\delta$ is an integer with
$0\le\delta\le |T|$.

For $T=(1,0)$, the only possible values are $\delta=0,1$:

- $\delta=0$ puts $P$ on the perpendicular bisector $x=1/2$, which has no
  integer points.
- $\delta=1$ is equality in the triangle inequality, so $P$ is collinear with
  $O$ and $T$; the required graph edge is then horizontal and illegal.

For $T=(2,0)$, the possible values are $\delta=0,1,2$:

- $\delta=0$ puts $P$ on $x=1$, so $|OP|^2=1+y^2$, which is strictly between
  consecutive squares for every nonzero integer $y$.
- $\delta=1$ is impossible because the two squared distances have the same
  parity, so the integer distances have the same parity.
- $\delta=2$ again forces collinearity and hence an illegal horizontal edge.

For $T=(2,1)$, the possible values are also $\delta=0,1,2$:

- $\delta=0$ puts $P$ on the perpendicular bisector $4x+2y=5$, which has no
  integer points.
- $\delta=2$ is impossible by parity: $x^2$ and $(x-2)^2$ have the same parity,
  while $y^2$ and $(y-1)^2$ have opposite parity, so the integer distances have
  opposite parity and cannot differ by $2$.
- $\delta=1$ reduces, after the paper's squaring and simplification, to
  $$
  3x^2+4xy-8x-4y+4=0.
  $$
  Viewing this as a quadratic in $x$, the discriminant condition is that
  $y^2-y+1$ be a square. This happens only for $y=0$ or $y=1$: for $y\ge2$ the
  expression lies strictly between $(y-1)^2$ and $y^2$, and for $y<0$, writing
  $t=-y$, it lies strictly between $t^2$ and $(t+1)^2$. The resulting integer
  candidates are $(2,0)$ and $(0,1)$, both of which make one graph edge
  horizontal or vertical.

Sign changes and coordinate swap are graph automorphisms, so the same
obstruction applies to every point in the known orbit. Combined with the
diameter-three path below, these vertices have exact distance $3$.

Executable guardrail:

- `canonical_known_distance_three_representative`
- `possible_integer_distance_differences`
- `y_squared_minus_y_plus_one_is_square`
- `known_distance_three_obstruction_cases`
- `test_known_exception_symbolic_obstruction_cases`
- `test_y_squared_minus_y_plus_one_square_lemma`

## Signed Length-Difference Conic Slices

The distance-difference parameter from the obstruction proof also gives a
constructive search space that is distinct from the existing lattice and strip
families.

Let $T=(g,h)$ and let $P=(x,y)$ be a two-step midpoint. Write
$$
N=|OP|,\qquad d=|OP|-|TP|.
$$
Then $d$ is a signed integer satisfying $|d|\le |T|$, and the second edge
condition is equivalent to
$$
(g-x)^2+(h-y)^2=(N-d)^2.
$$
Using $x^2+y^2=N^2$ and simplifying gives the affine slice
$$
2gx+2hy-2dN=g^2+h^2-d^2.
$$
Thus each fixed signed $d$ cuts the Pythagorean cone
$$
x^2+y^2=N^2
$$
by a plane. This is a conic-slice formulation of the two-step problem.

Parametrize the first edge by a primitive Pythagorean direction
$$
(x,y,N)=K(u,v,c),\qquad K>0,\qquad u^2+v^2=c^2.
$$
The slice condition becomes the divisibility test
$$
2K(gu+hv-dc)=g^2+h^2-d^2.
$$
The signed form of Theorem 3 below is the unit-denominator specialization of
this identity. For positive $g,h$, taking
$$
u=s_xa,\qquad v=s_yb,\qquad K=gh,\qquad d=g-h
$$
turns the denominator condition
$$
gu+hv-dc=1
$$
into
$$
(c-s_xa)g=(c+s_yb)h-1,
$$
which is exactly the paper's relation. The conic-slice route therefore asks
whether the same mechanism can be generalized from denominator $1$ to arbitrary
divisors of $(g^2+h^2-d^2)/2$.

This divisor generalization is now encoded for the $d=g-h$ slice. If
$(a,b,c)$ is a positive Pythagorean triple, $s_x,s_y\in\{-1,1\}$, and
$q\ne0$ satisfies
$$
(c-s_xa)g=(c+s_yb)h-q,
\qquad q\mid gh,
\qquad \frac{gh}{q}>0,
$$
then
$$
P=\left(s_xa\frac{gh}{q},\ s_yb\frac{gh}{q}\right)
$$
is a two-step midpoint unless one of the graph steps degenerates to a
horizontal or vertical edge. The paper's Theorem 3 is exactly the case $q=1$.

More generally, one can fix any legal Pythagorean direction $(u,v)$ with
hypotenuse $c$ and any linear signed-difference choice
$$
d=\alpha g+\beta h.
$$
The exact target-facing criterion is
$$
2(gu+hv-dc)\mid g^2+h^2-d^2,
\qquad
\frac{g^2+h^2-d^2}{2(gu+hv-dc)}>0.
$$
When this holds, the midpoint is
$$
P=\frac{g^2+h^2-d^2}{2(gu+hv-dc)}(u,v),
$$
provided the resulting graph steps are nondegenerate. Fixed choices of
$(u,v)$ and $(\alpha,\beta)$ give infinite divisibility families. The choices
$d=0$, $d=g-h$, $d=h-g$, $d=g$, and $d=h$ account for most of the small-box
delta-slice hits, and the divisor-strengthened Theorem 3 is exactly the
subcase $d=g-h$ with $(u,v)=(s_xa,s_yb)$.

The bounded constructor `delta_slice_certificate` tests this condition over
signed/swapped primitive Pythagorean directions up to a Euclid parameter bound
and signed differences ordered by increasing $|d|$. This is only a discovery
tool at present, but it is useful because it reuses the exact obstruction
parameter constructively rather than adding another target-facing family.

The known distance-three orbit is a negative control: within the tested
primitive-direction bounds, the delta-slice constructor returns no certificate
for those targets. Conversely, the current bounded guardrail certifies every
positive-quadrant non-edge target with $1\le g,h\le40$ outside the exceptional
orbit using directions with Euclid parameter at most $70$. A larger scratch
probe through $1\le g,h\le100$ also found no misses with parameter bound $120$;
the first hits were concentrated at small signed differences. In that scratch
sample, $|d|\le3$ covered $7702$ of the $9872$ positive-quadrant
non-exceptional non-edge targets, and $|d|\le10$ covered $9566$.

This suggests a possible non-family-by-family route: classify integral points
on these conic slices, or equivalently prove that for every non-exceptional
target some signed difference $d$ makes the binary quadratic divisibility
condition soluble. No such classification has been promoted yet.

Executable guardrail:

- `primitive_pythagorean_directions`
- `signed_delta_values`
- `delta_slice_certificate`
- `linear_delta_direction_certificate`
- `test_delta_slice_direction_generator_and_delta_order`
- `test_delta_slice_certificate_formula`
- `test_theorem3_is_unit_delta_slice_case`
- `test_linear_delta_direction_certificate`
- `theorem3_divisor_certificate`
- `test_theorem3_divisor_generalization`
- `test_delta_slice_bounded_discovery_probe`

## Diameter-Three Upper Bound

The paper's proof of $d(\mathcal G)=3$ gives an explicit path for every target.
For $T=(g,h)$,
$$
T=(3g+4h)(3,4)-(3g+4h)(4,3)+(g+h)(4,-3).
$$
Each vector $(3,4)$, $(4,3)$, and $(4,-3)$ is a legal Pythagorean edge vector,
and every nonzero integer multiple remains legal.

Thus the cumulative path obtained from the nonzero summands in the displayed
identity reaches every target in at most three graph steps. In particular, the
known obstruction vertices have exact distance $3$ once the paper's no-two-step
arguments are applied.

Executable guardrail:

- `theorem1_three_step_path`
- `test_theorem1_path_gives_three_step_upper_bound`

## Scaling Reduction

If $P$ is a two-step midpoint for a target $T$, then $kP$ is a two-step midpoint
for $kT$ for every nonzero integer $k$. Both edge vectors are simply multiplied
by $k$, so their squared lengths are multiplied by $k^2$ and remain squares;
nonzero coordinate changes remain nonzero.

This gives an exact reduction for all nonzero multiples of any target already
known to have a two-step certificate. It does not by itself handle multiples of
primitive obstruction directions, because there is no certificate to scale from
$(1,0)$, $(2,0)$, or $(2,1)$.

Executable guardrail:

- `scale_certificate`
- `test_certificate_scaling_preserves_validity`

## Square-Norm Gaussian Transformations

There is a broader exact closure principle than integer scaling. Identify
$(x,y)$ with the Gaussian integer $x+iy$. If
$$
z=a+ib,\qquad a^2+b^2=s^2,
$$
then multiplication by $z$ sends a vector $(x,y)$ to
$$
(ax-by,\ ay+bx)
$$
and scales its squared Euclidean length by $s^2$. Thus a Pythagorean edge
vector is sent to another integer-length vector. If neither transformed
coordinate is zero, it remains a legal graph edge.

Consequently, any two-step certificate
$$
O\to P\to T
$$
produces a two-step certificate
$$
O\to zP\to zT
$$
for every nonzero square-norm Gaussian multiplier $z$, except for the explicit
degenerate cases where one of the two transformed edge vectors becomes
horizontal or vertical.

Applying this to the base certificate
$$
O\to(4,-3)\to(1,1)
$$
gives a target-facing family. For
$$
a=\frac{g+h}{2},\qquad b=\frac{h-g}{2},
$$
if $a,b$ are integers, $a^2+b^2$ is a nonzero square, and the transformed
certificate is nondegenerate, then $(g,h)= (a+ib)(1+i)$ has distance at most
$2$ from the origin. The excluded degenerate multipliers are exactly those that
turn one of the two transformed edge vectors into an axis vector.

Executable guardrail:

- `gaussian_multiply`
- `gaussian_transform_certificate`
- `diagonal_pythagorean_multiplier_certificate`
- `test_gaussian_transform_preserves_certificates_when_nondegenerate`
- `test_diagonal_pythagorean_multiplier_family`

## Target-Facing Gaussian Divisor Criterion

The square-norm Gaussian transformation can also be used as a direct test for a
requested target once a base target has a certificate.

Let
$$
B=(b_1,b_2)
$$
be a target with a known two-step certificate, and let $T=(g,h)$. In Gaussian
integer notation, $T=zB$ for an integer Gaussian multiplier $z=a+ib$ exactly
when
$$
b_1^2+b_2^2 \mid gb_1+hb_2
\qquad\text{and}\qquad
b_1^2+b_2^2 \mid hb_1-gb_2.
$$
In that case
$$
a=\frac{gb_1+hb_2}{b_1^2+b_2^2},\qquad
b=\frac{hb_1-gb_2}{b_1^2+b_2^2}.
$$
If $a^2+b^2$ is a nonzero square, then the Gaussian transform of the base
certificate gives a two-step certificate for $T$, unless a transformed edge
becomes horizontal or vertical.

This turns every known two-step base target into an infinite exact family of
targets, and it strictly generalizes ordinary integer scaling.

Executable guardrail:

- `gaussian_quotient_if_integer`
- `gaussian_divisor_certificate`
- `first_gaussian_divisor_certificate`
- `test_gaussian_divisor_certificate_family`

## Two-Edge Lattice Criterion

Let $U=(u_1,u_2)$ and $V=(v_1,v_2)$ be legal Pythagorean edge vectors. If
$$
T=rU+sV
$$
for nonzero integers $r,s$, then $P=rU$ is a two-step midpoint for $T$:
$$
O\to rU\to rU+sV=T.
$$
Both steps are legal because nonzero integer multiples of legal Pythagorean
edge vectors are again legal.

For linearly independent $U,V$, the coefficients are computed by Cramer's rule.
Writing
$$
\Delta=u_1v_2-u_2v_1,
$$
a target $T=(g,h)$ belongs to the generated lattice exactly when
$$
\Delta\mid gv_2-hv_1,\qquad \Delta\mid u_1h-u_2g.
$$
The corresponding coefficients are
$$
r=\frac{gv_2-hv_1}{\Delta},\qquad
s=\frac{u_1h-u_2g}{\Delta}.
$$

Executable guardrail:

- `lattice_coefficients`
- `lattice_two_step_certificate`
- `test_lattice_coefficients_build_two_step_certificates`

## Parallel-Direction Divisor Reduction

The lattice criterion has a target-facing one-direction form that is more
structured than a box search. Fix a legal Pythagorean direction
$$
U=(u,v),\qquad u^2+v^2=c^2,
$$
and ask whether the first step can be taken on the ray through $U$:
$$
P=rU.
$$
For a target $T=(g,h)$, the second step is legal exactly when
$$
|T-rU|^2=s^2
$$
for some integer $s$, with the usual nonzero-coordinate exclusions.

Set
$$
A=T\cdot U=gu+hv,\qquad D=\det(U,T)=uh-vg.
$$
Multiplying the square condition by $c^2$ gives
$$
(c^2r-A)^2-c^2s^2=-D^2,
$$
and because the Pell coefficient is itself the square $c^2$, this factors over
the integers:
$$
\bigl(cs-(c^2r-A)\bigr)\bigl(cs+(c^2r-A)\bigr)=D^2.
$$
Thus every positive factorization $D^2=FG$ gives at most one candidate
coefficient
$$
r=\frac{(G-F)/2+A}{c^2}.
$$
If this is integral and nonzero, the midpoint $rU$ is checked directly. This
is an exact finite divisor criterion for the fixed direction $U$, not an
unbounded Pell search.

The factorization has a useful geometric interpretation. It chooses a
Pythagorean completion of the determinant leg $D$:
$$
B=\frac{G-F}{2},\qquad H=\frac{G+F}{2},\qquad B^2+D^2=H^2.
$$
The fixed direction $U$ accepts this completion exactly when $c\mid H$ and
$$
B+A\equiv0\pmod {c^2}.
$$
Then $r=(B+A)/c^2$. The executable witness records
$(D,B,H,H/c,r)$, so later proof attempts can reason about Pythagorean
completions of a single leg rather than opaque divisors.

The canonical completion of a leg is now separated as its own exact subfamily.
For odd $D$, the signed standard completions come from factors
$$
1,\quad D^2,
$$
giving $B=\pm(D^2-1)/2$. For even $D$, they come from
$$
2,\quad D^2/2,
$$
giving $B=\pm(D^2/4-1)$. These standard completions explain a visible portion
of the finite-direction hits, but not all of them; for example, some
unit-coordinate rows still require genuinely nonstandard divisors of $D^2$.
This split is useful because it isolates a closed congruence family before the
remaining divisor-structure problem.
The finite-direction standard-completion cover is now encoded separately. The
target $(1,92)$ is a guardrail counterexample to the tempting claim that the
standard completions suffice: with direction $U=(4,3)$ it needs the factor
$F=5$ of $365^2$, giving midpoint $(2176,1632)$.
That example belongs to an exact infinite subfamily. For every integer $t$, set
$$
h=25t+17,\qquad r=40t^2+55t+19.
$$
Then the target $(1,h)$ has the certificate
$$
P=(4r,3r).
$$
Equivalently, this is the fixed parallel-direction construction with
$U=(4,3)$ and nonstandard factor $F=5$ applied to
$D=\det(U,(1,h))=100t+65$. The sign/swap orbit of this family is also
certified.
The Lean row `certificateValid_unitCoordinateFactorFiveParallel` proves the
closed parametric certificate directly: the first step has length $5r$, and the
second step has length $5(40t^2+52t+17)$.  The nonzero coordinate checks reduce
to the factorizations
$$
1-4r=-5(4t+3)(8t+5),\qquad
25t+17-3r=-20(2t+1)(3t+2).
$$

More generally, fixing a direction $U$ and factor $F$ gives a finite list of
residues for the unit-coordinate targets $(1,h)$ modulo $2|U|^2F$. The helper
`unit_coordinate_parallel_factor_residues` enumerates exactly those residues,
and `unit_coordinate_parallel_factor_orbit_certificate` transports the
resulting family by sign changes and coordinate swap. For example,
$U=(4,3)$ and $F=5$ gives
$$
h\equiv17\pmod {25},
$$
while $U=(-3,-4)$ and $F=4$ gives
$$
h\equiv12\pmod {20}.
$$
This turns many unit-coordinate residual rows into named congruence families
rather than isolated midpoint entries.
The latter row has the equally explicit parametrization
$$
h=20t+12,\qquad r=18t^2+16t+3,\qquad P=(-3r,-4r),
$$
proved in Lean as `certificateValid_unitCoordinateFactorFourParallel`.  The
second step has length $90t^2+96t+26$, and its nonzero coordinate checks reduce
to
$$
1+3r=2(3t+1)(9t+5),\qquad
20t+12+4r=12(2t+1)(3t+2).
$$
The factor-one row with $U=(4,-3)$ is larger: it closes a whole residue class
modulo $5$.  For every integer $t$,
$$
h=5t+1,\qquad r=8t^2+5t+1,\qquad P=(4r,-3r)
$$
certifies $(1,h)$, and sign/swap transport certifies the full orbit.  Lean
proves the parametric row as
`certificateValid_unitCoordinateOneModFiveParallel`; the second step has length
$40t^2+28t+5$, and the nonzero checks reduce to
$$
1-4r=-(4t+1)(8t+3),\qquad
5t+1+3r=4(2t+1)(3t+1).
$$
The odd complement in the $h\equiv2,3\pmod5$ layer has another factor-one row.
With $U=(3,4)$, for every integer $t$,
$$
h=10t+7,\qquad r=18t^2+22t+7,\qquad P=(3r,4r)
$$
certifies $(1,h)$, and sign/swap transport also covers the $h\equiv3\pmod
{10}$ orbit.  Lean proves the row as
`certificateValid_unitCoordinateSevenModTenParallel`; the second step has
length $90t^2+102t+29$, and the nonzero coordinate checks reduce to
$$
1-3r=-2(3t+2)(9t+5),\qquad
10t+7-4r=-3(2t+1)(12t+7).
$$
The next even residual row uses the same signed `3-4-5` layer but with a
larger fixed factor.  With $U=(4,-3)$ and $F=25$, for every integer $t$,
$$
h=25t+18,\qquad r=8t^2+9t+2,\qquad P=(4r,-3r)
$$
certifies $(1,h)$.  Sign transport also covers $h\equiv7\pmod {25}$, so this
row reaches new even targets in the remaining $h\equiv2,3\pmod5$ layer.  Lean
proves it as `certificateValid_unitCoordinateFactorTwentyFiveParallel`; the
second step has length $5(8t^2+12t+5)$, and the nonzero checks reduce to
$$
1-4r=-(4t+1)(8t+7),\qquad
25t+18+3r=4(2t+3)(3t+2).
$$
The companion factor-five row with $U=(-4,-3)$ covers a broader congruence
class with one harmless degenerate parameter.  For $t\ne-1$, set
$$
h=25t+22,\qquad r=40t^2+65t+26,\qquad P=(-4r,-3r).
$$
Then $P$ certifies $(1,h)$; the fixed-factor construction degenerates only at
$t=-1$, where the target $(1,-3)$ is already covered by the seven-mod-ten row.
The orbit wrapper therefore certifies every sign/swap image of $h\equiv22\pmod
{25}$, and sign transport also covers $h\equiv3\pmod {25}$.  Lean proves the
nondegenerate fixed row as
`certificateValid_unitCoordinateTwentyTwoModTwentyFiveParallel`; its second
step has length $5(40t^2+68t+29)$, and the nonzero checks reduce to
$$
1+4r=5(4t+3)(8t+7),\qquad
25t+22+3r=20(t+1)(6t+5).
$$
Together, these promoted unit-coordinate rows now give an infinite modular
cover.  The dispatcher
`unit_coordinate_promoted_mod_hundred_certificate` proves that every
unit-coordinate target with nonzero other coordinate is covered unless that
coordinate is congruent to
$$
2,\ 38,\ 62,\ \text{or }98\pmod {100}.
$$
Those four classes are exactly the remaining structural unit-coordinate
residue classes for the current proof program; the known obstructions
$(\pm1,0)$, $(0,\pm1)$, and the sign/swap orbit of $(2,1)$ are outside the
claimed nonzero/nonresidual slice.
The orthogonal lattice layer now pierces all four of those residual classes
with explicit infinite seed rows from the single $(8,15,17)$ row
$h\equiv 38\pmod {289}$.  The helper
`unit_coordinate_residual_orthogonal_seed_certificate` certifies the following
unit-coordinate subfamilies and their sign/swap orbits:
$$
\begin{array}{c|c|c}
h\bmod 100 & h\equiv h_0\pmod M & (a,b,c)\\
\hline
2 & 22002\pmod {28900} & (8,15,17)\\
38 & 38\pmod {28900} & (8,15,17)\\
62 & 4662\pmod {28900} & (8,15,17)\\
98 & 11598\pmod {28900} & (8,15,17).
\end{array}
$$
Each row is an instance of the Lean-backed orthogonal lattice theorem: if
$h\equiv b a^{-1}\pmod {c^2}$, then $(1,h)$ is certified by the Cramer
coefficients in the orthogonal basis $(a,b),(-b,a)$.  The extra factor of
$100$ in the displayed period keeps each seed inside its named mod-$100$
residual class.

The fixed-direction layer now gives a denser residual slice from the
`(15,8,17)` direction.  For every integer $t$, set
$$
h=34t+26,\qquad r=225t^2+338t+127.
$$
Then the midpoint $(15r,8r)$ certifies $(1,h)$; equivalently this is the
parallel-factor construction for direction $(15,8)$ with factor $2$.  The
fixed congruence $h\equiv26\pmod {34}$ intersects the four residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {1700}\\
\hline
2 & 502\\
38 & 638\\
62 & 162\\
98 & 298.
\end{array}
$$
Sign and swap transport give the full orbit, including the companion
unit-coordinate congruence $h\equiv8\pmod {34}$.  Lean proves the fixed row as
`certificateValid_unitCoordinateFifteenEightFactorTwoParallel`, and the Python
wrapper records these residual intersections as
`UNIT_COORDINATE_FIFTEEN_EIGHT_FACTOR_TWO_RESIDUAL_ROWS`.

The `(12,35,37)` direction gives another fixed-direction residual slice with
factor $1$.  For every integer $t$, set
$$
h=37t+25,\qquad r=72t^2+85t+25.
$$
Then the midpoint $(-12r,-35r)$ certifies $(1,h)$.  The second-step
nonzero factors are
$$
1+12r=(12t+7)(72t+43),\qquad
h+35r=12(5t+3)(42t+25),
$$
so there is no integer exceptional parameter.  The congruence
$h\equiv25\pmod {37}$ intersects the four remaining mod-$100$ residual
classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {3700}\\
\hline
2 & 802\\
38 & 1838\\
62 & 62\\
98 & 1098.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateTwelveThirtyFiveFactorOneParallel`, and the
Python wrapper records these intersections as
`UNIT_COORDINATE_TWELVE_THIRTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(40,9,41)` direction gives a second factor-$1$ coprime-period slice.  For
every integer $t$, set
$$
h=41t+23,\qquad r=800t^2+889t+247.
$$
Then the midpoint $(40r,9r)$ certifies $(1,h)$.  The nonzero factors are
$$
1-40r=-(160t+89)(200t+111),\qquad
h-9r=-40(9t+5)(20t+11),
$$
and the coefficient $r$ is always nonzero because
$$
3200r=(1600t+889)^2+79.
$$
The congruence $h\equiv23\pmod {41}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {4100}\\
\hline
2 & 802\\
38 & 638\\
62 & 3262\\
98 & 3098.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateFortyNineFactorOneParallel`, and the Python
wrapper records these intersections as
`UNIT_COORDINATE_FORTY_NINE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(28,45,53)` direction gives a third factor-$1$ coprime-period slice.  For
every integer $t$, set
$$
h=53t+10,\qquad r=392t^2+125t+10.
$$
Then the midpoint $(28r,45r)$ certifies $(1,h)$.  Here
$$
1568r=(784t+125)^2+55,
$$
and the second-step nonzero factors are
$$
1-28r=-(56t+9)(196t+31),\qquad
h-45r=-4(63t+10)(70t+11).
$$
The congruence $h\equiv10\pmod {53}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {5300}\\
\hline
2 & 3402\\
38 & 4038\\
62 & 4462\\
98 & 5098.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateTwentyEightFortyFiveFactorOneParallel`, and
the Python wrapper records these intersections as
`UNIT_COORDINATE_TWENTY_EIGHT_FORTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(60,11,61)` direction gives the next primitive factor-$1$ coprime-period
slice.  For every integer $t$, set
$$
h=61t+39,\qquad r=1800t^2+2291t+729.
$$
Then the midpoint $(60r,11r)$ certifies $(1,h)$.  The coefficient is always
nonzero by
$$
7200r=(3600t+2291)^2+119,
$$
and the second-step nonzero factors are
$$
1-60r=-(300t+191)(360t+229),\qquad
h-11r=-60(11t+7)(30t+19).
$$
The congruence $h\equiv39\pmod {61}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {6100}\\
\hline
2 & 5102\\
38 & 3638\\
62 & 2662\\
98 & 1198.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateSixtyElevenFactorOneParallel`, and the Python
wrapper records these intersections as
`UNIT_COORDINATE_SIXTY_ELEVEN_FACTOR_ONE_RESIDUAL_ROWS`.

The `(48,55,73)` direction gives another primitive factor-$1$ coprime-period
slice.  For every integer $t$, set
$$
h=73t+31,\qquad r=1152t^2+943t+193.
$$
Then the midpoint $(48r,55r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
4608r=(2304t+943)^2+95,
$$
and the second-step nonzero factors are
$$
1-48r=-(144t+59)(384t+157),\qquad
h-55r=-24(22t+9)(120t+49).
$$
The congruence $h\equiv31\pmod {73}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {7300}\\
\hline
2 & 2002\\
38 & 4338\\
62 & 3462\\
98 & 5798.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateFortyEightFiftyFiveFactorOneParallel`, and the
Python wrapper records these intersections as
`UNIT_COORDINATE_FORTY_EIGHT_FIFTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(80,39,89)` direction gives the next primitive factor-$1$ coprime-period
slice.  For every integer $t$, set
$$
h=89t+71,\qquad r=3200t^2+5071t+2009.
$$
Then the midpoint $(80r,39r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
12800r=(6400t+5071)^2+159,
$$
and the second-step nonzero factors are
$$
1-80r=-(400t+317)(640t+507),\qquad
h-39r=-40(24t+19)(130t+103).
$$
The congruence $h\equiv71\pmod {89}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {8900}\\
\hline
2 & 7102\\
38 & 338\\
62 & 1762\\
98 & 3898.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateEightyThirtyNineFactorOneParallel`, and the
Python wrapper records these intersections as
`UNIT_COORDINATE_EIGHTY_THIRTY_NINE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(72,65,97)` direction gives the next primitive factor-$1$ coprime-period
slice.  For every integer $t$, set
$$
h=97t+78,\qquad r=2592t^2+4121t+1638.
$$
Then the midpoint $(72r,65r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
10368r=(5184t+4121)^2+143,
$$
and the second-step nonzero factors are
$$
1-72r=-(288t+229)(648t+515),\qquad
h-65r=-24(39t+31)(180t+143).
$$
The congruence $h\equiv78\pmod {97}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {9700}\\
\hline
2 & 9002\\
38 & 7838\\
62 & 7062\\
98 & 5898.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateSeventyTwoSixtyFiveFactorOneParallel`, and the
Python wrapper records these intersections as
`UNIT_COORDINATE_SEVENTY_TWO_SIXTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(20,99,101)` direction gives another primitive factor-$1$ coprime-period
slice.  For every integer $t$, set
$$
h=101t+60,\qquad r=200t^2+219t+60.
$$
Then the midpoint $(20r,99r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
800r=(400t+219)^2+39,
$$
and the second-step nonzero factors are
$$
1-20r=-(20t+11)(200t+109),\qquad
h-99r=-20(11t+6)(90t+49).
$$
The congruence $h\equiv60\pmod {101}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {10100}\\
\hline
2 & 4302\\
38 & 7938\\
62 & 262\\
98 & 3898.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateTwentyNinetyNineFactorOneParallel`, and the
Python wrapper records these intersections as
`UNIT_COORDINATE_TWENTY_NINETY_NINE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(60,91,109)` direction gives the next primitive factor-$1$ coprime-period
slice.  For every integer $t$, set
$$
h=109t+82,\qquad r=1800t^2+2659t+982.
$$
Then the midpoint $(60r,91r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
7200r=(3600t+2659)^2+119,
$$
and the second-step nonzero factors are
$$
1-60r=-(180t+133)(600t+443),\qquad
h-91r=-60(42t+31)(65t+48).
$$
The congruence $h\equiv82\pmod {109}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {10900}\\
\hline
2 & 8802\\
38 & 9238\\
62 & 2262\\
98 & 2698.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateSixtyNinetyOneFactorOneParallel`, and the
Python wrapper records these intersections as
`UNIT_COORDINATE_SIXTY_NINETY_ONE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(112,15,113)` direction gives another primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=113t+83,\qquad r=6272t^2+9199t+3373.
$$
Then the midpoint $(112r,15r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
25088r=(12544t+9199)^2+223,
$$
and the second-step nonzero factors are
$$
1-112r=-(784t+575)(896t+657),\qquad
h-15r=-112(15t+11)(56t+41).
$$
The congruence $h\equiv83\pmod {113}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {11300}\\
\hline
2 & 7202\\
38 & 4038\\
62 & 9462\\
98 & 6298.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateOneHundredTwelveFifteenFactorOneParallel`, and
the Python wrapper records these intersections as
`UNIT_COORDINATE_ONE_HUNDRED_TWELVE_FIFTEEN_FACTOR_ONE_RESIDUAL_ROWS`.

The `(88,105,137)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=137t+7,\qquad r=3872t^2+329t+7.
$$
Then the midpoint $(88r,105r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
15488r=(7744t+329)^2+175,
$$
and the second-step nonzero factors are
$$
1-88r=-(352t+15)(968t+41),\qquad
h-105r=-8(165t+7)(308t+13).
$$
The congruence $h\equiv7\pmod {137}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {13700}\\
\hline
2 & 4802\\
38 & 8638\\
62 & 2062\\
98 & 5898.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateEightyEightOneHundredFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_EIGHTY_EIGHT_ONE_HUNDRED_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(140,51,149)` direction gives another primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=149t+82,\qquad r=9800t^2+10739t+2942.
$$
Then the midpoint $(140r,51r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
39200r=(19600t+10739)^2+279,
$$
and the second-step nonzero factors are
$$
1-140r=-(980t+537)(1400t+767),\qquad
h-51r=-20(42t+23)(595t+326).
$$
The congruence $h\equiv82\pmod {149}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {14900}\\
\hline
2 & 12002\\
38 & 6638\\
62 & 3062\\
98 & 12598.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateOneHundredFortyFiftyOneFactorOneParallel`, and
the Python wrapper records these intersections as
`UNIT_COORDINATE_ONE_HUNDRED_FORTY_FIFTY_ONE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(132,85,157)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=157t+4,\qquad r=8712t^2+373t+4.
$$
Then the midpoint $(132r,85r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
34848r=(17424t+373)^2+263,
$$
and the second-step nonzero factors are
$$
1-132r=-(792t+17)(1452t+31),\qquad
h-85r=-12(187t+4)(330t+7).
$$
The congruence $h\equiv4\pmod {157}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {15700}\\
\hline
2 & 2202\\
38 & 9738\\
62 & 14762\\
98 & 6598.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateOneHundredThirtyTwoEightyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_ONE_HUNDRED_THIRTY_TWO_EIGHTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(120,119,169)` direction gives another primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=169t+168,\qquad r=7200t^2+14231t+7032.
$$
Then the midpoint $(120r,119r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
28800r=(14400t+14231)^2+239,
$$
and the second-step nonzero factors are
$$
1-120r=-(600t+593)(1440t+1423),\qquad
h-119r=-120(84t+83)(85t+84).
$$
The congruence $h\equiv168\pmod {169}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {16900}\\
\hline
2 & 14702\\
38 & 5238\\
62 & 4562\\
98 & 11998.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateOneHundredTwentyOneHundredNineteenFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_ONE_HUNDRED_TWENTY_ONE_HUNDRED_NINETEEN_FACTOR_ONE_RESIDUAL_ROWS`.

The `(52,165,173)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=173t+28,\qquad r=1352t^2+389t+28.
$$
Then the midpoint $(52r,165r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
5408r=(2704t+389)^2+103,
$$
and the second-step nonzero factors are
$$
1-52r=-(104t+15)(676t+97),\qquad
h-165r=-4(195t+28)(286t+41).
$$
The congruence $h\equiv28\pmod {173}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {17300}\\
\hline
2 & 6602\\
38 & 12138\\
62 & 10062\\
98 & 15598.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateFiftyTwoOneHundredSixtyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_FIFTY_TWO_ONE_HUNDRED_SIXTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(180,19,181)` direction gives another primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=181t+143,\qquad r=16200t^2+25579t+10097.
$$
Then the midpoint $(180r,19r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
64800r=(32400t+25579)^2+359,
$$
and the second-step nonzero factors are
$$
1-180r=-(1620t+1279)(1800t+1421),\qquad
h-19r=-180(19t+15)(90t+71).
$$
The congruence $h\equiv143\pmod {181}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {18100}\\
\hline
2 & 7202\\
38 & 17338\\
62 & 18062\\
98 & 10098.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateOneHundredEightyNineteenFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_ONE_HUNDRED_EIGHTY_NINETEEN_FACTOR_ONE_RESIDUAL_ROWS`.

The `(168,95,193)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=193t+47,\qquad r=14112t^2+6791t+817.
$$
Then the midpoint $(168r,95r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
56448r=(28224t+6791)^2+335,
$$
and the second-step nonzero factors are
$$
1-168r=-(1176t+283)(2016t+485),\qquad
h-95r=-24(133t+32)(420t+101).
$$
The congruence $h\equiv47\pmod {193}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {19300}\\
\hline
2 & 6802\\
38 & 16838\\
62 & 10662\\
98 & 1398.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateOneHundredSixtyEightNinetyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_ONE_HUNDRED_SIXTY_EIGHT_NINETY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(28,195,197)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=197t+112,\qquad r=392t^2+419t+112.
$$
Then the midpoint $(28r,195r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
1568r=(784t+419)^2+55,
$$
and the second-step nonzero factors are
$$
1-28r=-(28t+15)(392t+209),\qquad
h-195r=-28(15t+8)(182t+97).
$$
The congruence $h\equiv112\pmod {197}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {19700}\\
\hline
2 & 13902\\
38 & 11538\\
62 & 9962\\
98 & 7598.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateTwentyEightOneHundredNinetyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_TWENTY_EIGHT_ONE_HUNDRED_NINETY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(60,221,229)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=229t+36,\qquad r=1800t^2+509t+36.
$$
Then the midpoint $(60r,221r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
7200r=(3600t+509)^2+119,
$$
and the second-step nonzero factors are
$$
1-60r=-(120t+17)(900t+127),\qquad
h-221r=-60(78t+11)(85t+12).
$$
The congruence $h\equiv36\pmod {229}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {22900}\\
\hline
2 & 12402\\
38 & 8738\\
62 & 21562\\
98 & 17898.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateSixtyTwoHundredTwentyOneFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_SIXTY_TWO_HUNDRED_TWENTY_ONE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(312,25,313)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=313t+263,\qquad r=48672t^2+81769t+34343.
$$
Then the midpoint $(312r,25r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
194688r=(97344t+81769)^2+623,
$$
and the second-step nonzero factors are
$$
1-312r=-(3744t+3145)(4056t+3407),\qquad
h-25r=-312(25t+21)(156t+131).
$$
The congruence $h\equiv263\pmod {313}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {31300}\\
\hline
2 & 1202\\
38 & 23738\\
62 & 7462\\
98 & 29998.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateThreeHundredTwelveTwentyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_THREE_HUNDRED_TWELVE_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(308,75,317)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=317t+296,\qquad r=47432t^2+88507t+41288.
$$
Then the midpoint $(308r,75r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
189728r=(94864t+88507)^2+615,
$$
and the second-step nonzero factors are
$$
1-308r=-(3388t+3161)(4312t+4023),\qquad
h-75r=-4(462t+431)(1925t+1796).
$$
The congruence $h\equiv296\pmod {317}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {31700}\\
\hline
2 & 6002\\
38 & 8538\\
62 & 31362\\
98 & 2198.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateThreeHundredEightSeventyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_THREE_HUNDRED_EIGHT_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(288,175,337)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=337t+241,\qquad r=41472t^2+59167t+21103.
$$
Then the midpoint $(288r,175r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
165888r=(82944t+59167)^2+575,
$$
and the second-step nonzero factors are
$$
1-288r=-(2592t+1849)(4608t+3287),\qquad
h-175r=-48(150t+107)(1008t+719).
$$
The congruence $h\equiv241\pmod {337}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {33700}\\
\hline
2 & 18102\\
38 & 27538\\
62 & 11362\\
98 & 20798.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateTwoHundredEightyEightOneHundredSeventyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_TWO_HUNDRED_EIGHTY_EIGHT_ONE_HUNDRED_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(180,299,349)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=349t+206,\qquad r=16200t^2+18971t+5554.
$$
Then the midpoint $(180r,299r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
64800r=(32400t+18971)^2+359,
$$
and the second-step nonzero factors are
$$
1-180r=-(900t+527)(3240t+1897),\qquad
h-299r=-60(234t+137)(345t+202).
$$
The congruence $h\equiv206\pmod {349}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {34900}\\
\hline
2 & 1602\\
38 & 23938\\
62 & 15562\\
98 & 2998.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateOneHundredEightyTwoHundredNinetyNineFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_ONE_HUNDRED_EIGHTY_TWO_HUNDRED_NINETY_NINE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(272,225,353)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=353t+49,\qquad r=36992t^2+10097t+689.
$$
Then the midpoint $(272r,225r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
147968r=(73984t+10097)^2+543,
$$
and the second-step nonzero factors are
$$
1-272r=-(2176t+297)(4624t+631),\qquad
h-225r=-16(425t+58)(1224t+167).
$$
The congruence $h\equiv49\pmod {353}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {35300}\\
\hline
2 & 402\\
38 & 4638\\
62 & 7462\\
98 & 11698.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateTwoHundredSeventyTwoTwoHundredTwentyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_TWO_HUNDRED_SEVENTY_TWO_TWO_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(252,275,373)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=373t+151,\qquad r=31752t^2+25523t+5129.
$$
Then the midpoint $(252r,275r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
127008r=(63504t+25523)^2+503,
$$
and the second-step nonzero factors are
$$
1-252r=-(1764t+709)(4536t+1823),\qquad
h-275r=-12(525t+211)(1386t+557).
$$
The congruence $h\equiv151\pmod {373}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {37300}\\
\hline
2 & 32602\\
38 & 7238\\
62 & 2762\\
98 & 14698.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateTwoHundredFiftyTwoTwoHundredSeventyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_TWO_HUNDRED_FIFTY_TWO_TWO_HUNDRED_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(352,135,377)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=377t+299,\qquad r=61952t^2+98143t+38869.
$$
Then the midpoint $(352r,135r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
247808r=(123904t+98143)^2+703,
$$
and the second-step nonzero factors are
$$
1-352r=-(3872t+3067)(5632t+4461),\qquad
h-135r=-8(880t+697)(1188t+941).
$$
The congruence $h\equiv299\pmod {377}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {37700}\\
\hline
2 & 15002\\
38 & 2938\\
62 & 7462\\
98 & 33098.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateThreeHundredFiftyTwoOneHundredThirtyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_THREE_HUNDRED_FIFTY_TWO_ONE_HUNDRED_THIRTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(340,189,389)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=389t+97,\qquad r=57800t^2+28661t+3553.
$$
Then the midpoint $(340r,189r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
231200r=(115600t+28661)^2+679,
$$
and the second-step nonzero factors are
$$
1-340r=-(3400t+843)(5780t+1433),\qquad
h-189r=-20(238t+59)(2295t+569).
$$
The congruence $h\equiv97\pmod {389}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {38900}\\
\hline
2 & 17602\\
38 & 26938\\
62 & 33162\\
98 & 3598.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateThreeHundredFortyOneHundredEightyNineFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_THREE_HUNDRED_FORTY_ONE_HUNDRED_EIGHTY_NINE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(228,325,397)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=397t+141,\qquad r=25992t^2+18277t+3213.
$$
Then the midpoint $(228r,325r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
103968r=(51984t+18277)^2+455,
$$
and the second-step nonzero factors are
$$
1-228r=-(1368t+481)(4332t+1523),\qquad
h-325r=-12(475t+167)(1482t+521).
$$
The congruence $h\equiv141\pmod {397}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {39700}\\
\hline
2 & 5302\\
38 & 538\\
62 & 37062\\
98 & 32298.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateTwoHundredTwentyEightThreeHundredTwentyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_TWO_HUNDRED_TWENTY_EIGHT_THREE_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(40,399,401)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=401t+220,\qquad r=800t^2+839t+220.
$$
Then the midpoint $(40r,399r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
3200r=(1600t+839)^2+79,
$$
and the second-step nonzero factors are
$$
1-40r=-(40t+21)(800t+419),\qquad
h-399r=-40(21t+11)(380t+199).
$$
The congruence $h\equiv220\pmod {401}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {40100}\\
\hline
2 & 33102\\
38 & 7438\\
62 & 17062\\
98 & 31498.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateFortyThreeHundredNinetyNineFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_FORTY_THREE_HUNDRED_NINETY_NINE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(120,391,409)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=409t+302,\qquad r=7200t^2+10519t+3842.
$$
Then the midpoint $(120r,391r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
28800r=(14400t+10519)^2+239,
$$
and the second-step nonzero factors are
$$
1-120r=-(360t+263)(2400t+1753),\qquad
h-391r=-120(115t+84)(204t+149).
$$
The congruence $h\equiv302\pmod {409}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {40900}\\
\hline
2 & 302\\
38 & 1938\\
62 & 16662\\
98 & 18298.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateOneHundredTwentyThreeHundredNinetyOneFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_ONE_HUNDRED_TWENTY_THREE_HUNDRED_NINETY_ONE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(420,29,421)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=421t+363,\qquad r=88200t^2+152069t+65547.
$$
Then the midpoint $(420r,29r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
352800r=(176400t+152069)^2+839,
$$
and the second-step nonzero factors are
$$
1-420r=-(5880t+5069)(6300t+5431),\qquad
h-29r=-420(29t+25)(210t+181).
$$
The congruence $h\equiv363\pmod {421}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {42100}\\
\hline
2 & 25202\\
38 & 31938\\
62 & 8362\\
98 & 15098.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateFourHundredTwentyTwentyNineFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_FOUR_HUNDRED_TWENTY_TWENTY_NINE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(408,145,433)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=433t+39,\qquad r=83232t^2+14857t+663.
$$
Then the midpoint $(408r,145r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
332928r=(166464t+14857)^2+815,
$$
and the second-step nonzero factors are
$$
1-408r=-(4896t+437)(6936t+619),\qquad
h-145r=-24(493t+44)(1020t+91).
$$
The congruence $h\equiv39\pmod {433}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {43300}\\
\hline
2 & 4802\\
38 & 1338\\
62 & 13462\\
98 & 9998.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateFourHundredEightOneHundredFortyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_FOUR_HUNDRED_EIGHT_ONE_HUNDRED_FORTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(280,351,449)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=449t+264,\qquad r=39200t^2+45879t+13424.
$$
Then the midpoint $(280r,351r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
156800r=(78400t+45879)^2+559,
$$
and the second-step nonzero factors are
$$
1-280r=-(1960t+1147)(5600t+3277),\qquad
h-351r=-280(135t+79)(364t+213).
$$
The congruence $h\equiv264\pmod {449}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {44900}\\
\hline
2 & 28102\\
38 & 11938\\
62 & 1162\\
98 & 29898.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateTwoHundredEightyThreeHundredFiftyOneFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_TWO_HUNDRED_EIGHTY_THREE_HUNDRED_FIFTY_ONE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(168,425,457)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=457t+248,\qquad r=14112t^2+15161t+4072.
$$
Then the midpoint $(168r,425r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
56448r=(28224t+15161)^2+335,
$$
and the second-step nonzero factors are
$$
1-168r=-(672t+361)(3528t+1895),\qquad
h-425r=-24(175t+94)(1428t+767).
$$
The congruence $h\equiv248\pmod {457}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {45700}\\
\hline
2 & 10302\\
38 & 32238\\
62 & 1162\\
98 & 23098.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateOneHundredSixtyEightFourHundredTwentyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_ONE_HUNDRED_SIXTY_EIGHT_FOUR_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(380,261,461)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=461t+373,\qquad r=72200t^2+116621t+47093.
$$
Then the midpoint $(380r,261r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
288800r=(144400t+116621)^2+759,
$$
and the second-step nonzero factors are
$$
1-380r=-(3800t+3069)(7220t+5831),\qquad
h-261r=-20(551t+445)(1710t+1381).
$$
The congruence $h\equiv373\pmod {461}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {46100}\\
\hline
2 & 41402\\
38 & 30338\\
62 & 22962\\
98 & 11898.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateThreeHundredEightyTwoHundredSixtyOneFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_THREE_HUNDRED_EIGHTY_TWO_HUNDRED_SIXTY_ONE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(360,319,481)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=481t+23,\qquad r=64800t^2+5959t+137.
$$
Then the midpoint $(360r,319r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
259200r=(129600t+5959)^2+719,
$$
and the second-step nonzero factors are
$$
1-360r=-(3240t+149)(7200t+331),\qquad
h-319r=-120(87t+4)(1980t+91).
$$
The congruence $h\equiv23\pmod {481}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {48100}\\
\hline
2 & 28402\\
38 & 7238\\
62 & 9162\\
98 & 36098.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateThreeHundredSixtyThreeHundredNineteenFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_THREE_HUNDRED_SIXTY_THREE_HUNDRED_NINETEEN_FACTOR_ONE_RESIDUAL_ROWS`.

The `(132,475,493)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=493t+199,\qquad r=8712t^2+6907t+1369.
$$
Then the midpoint $(132r,475r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
34848r=(17424t+6907)^2+263,
$$
and the second-step nonzero factors are
$$
1-132r=-(396t+157)(2904t+1151),\qquad
h-475r=-12(275t+109)(1254t+497).
$$
The congruence $h\equiv199\pmod {493}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {49300}\\
\hline
2 & 35202\\
38 & 11538\\
62 & 45062\\
98 & 21398.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateOneHundredThirtyTwoFourHundredSeventyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_ONE_HUNDRED_THIRTY_TWO_FOUR_HUNDRED_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(220,459,509)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=509t+96,\qquad r=24200t^2+8931t+824.
$$
Then the midpoint $(220r,459r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
96800r=(48400t+8931)^2+439,
$$
and the second-step nonzero factors are
$$
1-220r=-(1100t+203)(4840t+893),\qquad
h-459r=-20(374t+69)(1485t+274).
$$
The congruence $h\equiv96\pmod {509}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {50900}\\
\hline
2 & 17402\\
38 & 19438\\
62 & 37762\\
98 & 39798.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateTwoHundredTwentyFourHundredFiftyNineFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_TWO_HUNDRED_TWENTY_FOUR_HUNDRED_FIFTY_NINE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(440,279,521)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=521t+103,\qquad r=96800t^2+38039t+3737.
$$
Then the midpoint $(440r,279r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
387200r=(193600t+38039)^2+879,
$$
and the second-step nonzero factors are
$$
1-440r=-(4840t+951)(8800t+1729),\qquad
h-279r=-40(341t+67)(1980t+389).
$$
The congruence $h\equiv103\pmod {521}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {52100}\\
\hline
2 & 10002\\
38 & 18338\\
62 & 41262\\
98 & 49598.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateFourHundredFortyTwoHundredSeventyNineFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_FOUR_HUNDRED_FORTY_TWO_HUNDRED_SEVENTY_NINE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(92,525,533)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=533t+78,\qquad r=4232t^2+1149t+78.
$$
Then the midpoint $(92r,525r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
16928r=(8464t+1149)^2+183,
$$
and the second-step nonzero factors are
$$
1-92r=-(184t+25)(2116t+287),\qquad
h-525r=-4(575t+78)(966t+131).
$$
The congruence $h\equiv78\pmod {533}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {53300}\\
\hline
2 & 15002\\
38 & 10738\\
62 & 25662\\
98 & 21398.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateNinetyTwoFiveHundredTwentyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_NINETY_TWO_FIVE_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(420,341,541)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=541t+113,\qquad r=88200t^2+36581t+3793.
$$
Then the midpoint $(420r,341r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
352800r=(176400t+36581)^2+839,
$$
and the second-step nonzero factors are
$$
1-420r=-(4200t+871)(8820t+1829),\qquad
h-341r=-60(217t+45)(2310t+479).
$$
The congruence $h\equiv113\pmod {541}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {54100}\\
\hline
2 & 15802\\
38 & 13638\\
62 & 48262\\
98 & 46098.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateFourHundredTwentyThreeHundredFortyOneFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_FOUR_HUNDRED_TWENTY_THREE_HUNDRED_FORTY_ONE_FACTOR_ONE_RESIDUAL_ROWS`.

The `(532,165,557)` direction gives the next primitive factor-$1$
coprime-period slice.  For every integer $t$, set
$$
h=557t+412,\qquad r=141512t^2+209189t+77308.
$$
Then the midpoint $(532r,165r)$ certifies $(1,h)$.  The coefficient is nonzero
because
$$
566048r=(283024t+209189)^2+1063,
$$
and the second-step nonzero factors are
$$
1-532r=-(7448t+5505)(10108t+7471),\qquad
h-165r=-4(1330t+983)(4389t+3244).
$$
The congruence $h\equiv412\pmod {557}$ intersects the four remaining mod-$100$
residual classes as
$$
\begin{array}{c|c}
h\bmod 100 & h\equiv h_0\pmod {55700}\\
\hline
2 & 39402\\
38 & 10438\\
62 & 28262\\
98 & 54998.
\end{array}
$$
Lean proves the row as
`certificateValid_unitCoordinateFiveHundredThirtyTwoOneHundredSixtyFiveFactorOneParallel`,
and the Python wrapper records these intersections as
`UNIT_COORDINATE_FIVE_HUNDRED_THIRTY_TWO_ONE_HUNDRED_SIXTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`.

The same idea works on any fixed rational ray. Write
$$
R=(p,q),\qquad T=nR,
$$
and keep the direction $U=(u,v)$ and factor $F$ fixed. If
$$
A_0=R\cdot U,\qquad D_0=\det(U,R),
$$
then $A=nA_0$ and $D=nD_0$. Whenever $F\mid n^2D_0^2$, the forced first-step
coefficient is
$$
r(n)=\frac{(n^2D_0^2/F-F)/2+nA_0}{c^2}.
$$
Thus the arithmetic part of this whole ray family depends only on the
multiplier $n$ modulo $2c^2F$. The helper
`ray_parallel_factor_residues` enumerates those multiplier classes, and
`ray_parallel_factor_certificate` then applies the actual graph
nondegeneracy check to the requested target. This is the principled replacement
for asking for a larger target box: each successful direction/factor pair
certifies infinitely many multiples of a slope.

On the exceptional ray $R=(2,1)$ this already gives clean infinite classes
without touching the primitive obstruction. With $U=(4,3)$ and $F=2$,
$$
D_0=-2,\qquad A_0=11,\qquad
r(n)=\frac{n^2+11n-1}{25}.
$$
The exact multiplier residues are
$$
n\equiv2\pmod5
$$
inside the natural modulus $100$. Equivalently, for $n=5t+2$,
$$
r=t^2+3t+1,\qquad
P=(4r,3r),
$$
and all $t\ge1$ pass the graph check; $t=0$ is retained as a degenerate
guardrail because the second step becomes vertical. The signed opposite
direction $U=(-4,-3)$, again with $F=2$, gives the companion class
$n\equiv3\pmod5$ with the same final nondegeneracy check. These ray-level
families are more useful than another finite audit because they expose exactly
which multiplier residue classes remain to be covered on a fixed primitive
slope.

The full two-dimensional fixed direction/factor family is also now named for
the first nonstandard case. The constructor
`four_three_factor_five_parallel_certificate` first checks the periodic
integral-coefficient classes for `parallel_direction_factor_certificate` with
target, direction $(4,3)$, and factor $5$, and then applies the pointwise
certificate check. Its natural modulus is $250$; among the $250^2$ residue
classes, $1250$ have an integral first-step coefficient.

The nondegeneracy part is deliberately not promoted to a residue-class
condition. In the fundamental box, $1188$ of the integral representatives give
valid certificates, but this representative count is diagnostic only: the
class of $(3,6)$ is degenerate at $(3,6)$ while its translate $(253,6)$ has the
valid midpoint $(8808,6606)$. Thus the infinite congruence family is
"integral residue class plus actual graph check", not "valid representative
modulo $250$".

The nonstandard residuals are also structured. In finite probes, after the
standard completions are removed, most remaining witnesses still use small
divisors of $D^2$ and the same $3$-$4$-$5$ direction orbit. The helper
`parallel_direction_bounded_factor_cover_certificate` records this next layer:
it applies the exact same completion criterion, but only to factors bounded by
a chosen constant. The current guardrail checks that standard completions plus
bounded factors up to $1000$ cover the primitive positive-quadrant sample
through $80$, while the full finite-direction divisor cover handles the larger
scratch ranges mentioned below. This is still discovery evidence, but it gives
a sharper proof decomposition:

1. standard determinant-leg completions;
2. bounded nonstandard determinant-leg completions;
3. any remaining large-factor divisor completions.

For fixed $U$ and fixed factor $F$, the arithmetic part depends only on the
target modulo
$$
2c^2F.
$$
Indeed $D^2/F$ is determined modulo $2c^2$ once $D^2$ is known modulo
$2c^2F$, and $A$ is only needed modulo $c^2$. Thus each fixed
direction/factor pair cuts out explicit quadratic congruence classes. The
remaining nonzero and nondegeneracy checks are then applied to the resulting
midpoint.
The helper `parallel_direction_factor_residue_classes` enumerates these classes
for small fixed factors, giving a finite modular object that can be checked
independently of any target-size box. This is the first step toward replacing
the current finite-direction probe by a finite congruence cover.

This reduction explains many of the finite-audit residual rows. More strongly,
the executable probe now checks every primitive positive-quadrant non-edge
target with $1\le g,h\le1000$ and verifies that the parallel-direction divisor
criterion alone, using primitive Pythagorean directions up to Euclid parameter
$8$, covers every target in that sample outside the exceptional orbit. This is
not yet a proof, but it suggests replacing larger target boxes with a finite
direction-cover problem: prove that every non-exceptional primitive ray has at
least one direction $U$ in this fixed finite set, or in a parametrically
described extension of it, for which the determinant-square divisor condition
succeeds.
The candidate constructor `parallel_direction_cover_certificate` records this
finite-direction strategy explicitly; it contains no residual midpoint table,
only the exact divisor criterion above applied to a fixed signed set of
Pythagorean directions.
The companion witness helpers expose the exact arithmetic row behind each hit:
`parallel_direction_witness` returns the first valid factor completion for one
direction, `parallel_direction_cover_witness` adds the finite signed direction
set, and `parallel_direction_primitive_ray_witness` records the primitive
representative and scaling factor. A witness therefore records
$$
(U,F,D,B,H,H/c,r),
$$
not just the final midpoint. This makes the finite-direction cover inspectable
as determinant-leg completions, and gives a concrete object to classify in the
next proof step.
The census helper `parallel_direction_cover_witness_census` turns this into a
reproducible primitive-sample summary. For example, on primitive positive
targets with $1\le g,h\le30$ and direction parameter bound $8$, it finds no
uncovered target among $543$ candidates. The most common first witnesses are
the signed $3$-$4$-$5$ directions:
$$
\begin{array}{c|c}
U & \text{count}\\
\hline
(-4,-3) & 311\\
(-4,3) & 167\\
(-3,-4) & 31\\
(-3,4) & 16.
\end{array}
$$
The leading factor counts are
$$
1:117,\quad 2:47,\quad 3:25,\quad 4:24,\quad 9:21,
$$
with the top direction/factor rows
$$
((-4,-3),1):70,\quad ((-4,-3),2):31,\quad ((-4,3),1):30.
$$
This is still a finite diagnostic, but it points to a sharper proof strategy:
classify the dominant $3$-$4$-$5$ determinant-completion rows first, then
explain the small tail requiring higher Pythagorean directions.

The first such promotion is now explicit. Let
$$
\mathcal U_{345}=\{(\pm4,\pm3),(\pm3,\pm4)\}
$$
with all independent sign choices, and let
$$
\mathcal F_{345}=\{1,2,3,4,5,6,8,9,25\}.
$$
The helper `parallel_direction_promoted_345_factor_certificate` tries exactly
these $8\cdot9=72$ fixed direction/factor rows. Each row is a fixed quadratic
congruence family modulo $2|U|^2F=50F$, followed by the usual nondegeneracy
check. This layer is not allowed to search arbitrary divisors of
$\det(U,T)^2$; it only tests the promoted rows.

On primitive positive targets with $1\le g,h\le50$, this promoted $3$-$4$-$5$
layer certifies $1461$ of the $1529$ nontrivial targets. The remaining $68$
targets are all still certified by the full finite-direction divisor cover with
parameter bound $8$. The first misses are
$$
(1,38),\ (2,29),\ (2,49),\ (5,14),\ (5,26),\ (5,34),\ (5,46),\ (7,10).
$$
Thus the current tail has been isolated: either add more fixed $3$-$4$-$5$
factors, or explain the higher-triple witnesses that the full cover uses for
these residual primitive rays.

A second promoted layer now explains a clean part of that tail without
enlarging the box. The helper `pythagorean_orthogonal_lattice_cover_certificate`
tries only canonical orthogonal pairs
$$
U=(u,v),\qquad U^\perp=(-v,u)
$$
coming from primitive Pythagorean directions up to a fixed Euclid-parameter
bound. These are the zero-other-leg determinant completions in lattice form.
With parameter bound $4$, this layer covers $8$ of the $68$ residual primitive
targets left by the promoted $3$-$4$-$5$ factor rows in the sample
$1\le g,h\le50$:
$$
(1,38),\ (2,29),\ (19,22),\ (22,19),\ (22,31),\ (29,2),\ (31,22),\ (38,1).
$$
The first remaining uncovered residuals after this orthogonal layer are
$$
(2,49),\ (5,14),\ (5,26),\ (5,34),\ (5,46),\ (7,10),\ (7,50),\ (8,9),
$$
and the guardrail count is $60$ remaining residuals in the same sample.

The next layer stops treating those residuals as parallel-factor accidents and
recasts them as two-direction lattices. The helper
`pythagorean_lattice_pair_cover_certificate` enumerates ordered pairs of
primitive Pythagorean directions with bounded Euclid parameter and bounded
lattice index $|\det(U,V)|$, then applies the exact Cramer-coefficient
criterion for $T\in\mathbb ZU+\mathbb ZV$. With parameter bound $25$ and
index bound $1435$, this bounded-index lattice-pair cover closes all $60$ of
the residual primitive targets left by the promoted $3$-$4$-$5$ and orthogonal
layers in the sample $1\le g,h\le50$. On the larger primitive sample
$1\le g,h\le100$, the same three-layer pipeline has only four misses:
$$
(29,98),\ (50,53),\ (53,50),\ (98,29).
$$
This is not a proof of the full conjecture, but it is a principled replacement
for box growth: each accepted row is an infinite lattice congruence family.

The remaining misses in the larger sample are explained by the standard
determinant-completion layer. The fixed helper
`pythagorean_layered_structural_certificate` now applies this stack:

1. promoted signed $3$-$4$-$5$ direction/factor rows;
2. orthogonal Pythagorean lattice rows with parameter bound $4$;
3. bounded-index Pythagorean lattice pairs with parameter bound $25$ and index
   bound $1435$;
4. standard determinant-completion rows over signed Pythagorean directions with
   parameter bound $8$.

On primitive positive targets with $1\le g,h\le300$, excluding one-step targets
and the known distance-three orbit, this fixed structural stack covers all
$54685$ targets. The layer counts are
$$
52549,\quad 40,\quad 2032,\quad 64,
$$
respectively. The last $64$ targets are not new residual table rows: they are
standard determinant completions for small Pythagorean directions.

The next audited frontier keeps the same structural stack and adds a bounded
squareclass split of the determinant-completion factor. Every factor in the
parallel divisor criterion can be written as $q a^2$, with paired factor
$q b^2$ and determinant leg $qab$. The helper
`pythagorean_layered_split_certificate` tests fixed rows with signed
Pythagorean directions up to parameter $8$, squareclass $q\le23$, and
split factor $a\le179$. This closes the primitive positive sample
$1\le g,h\le1000$. The count is
$$
608023=607989+34,
$$
where $607989$ targets are covered by the fixed structural stack above, and
only $34$ require the squareclass split layer. The first few split-layer
targets are
$$
(139,878),\ (151,338),\ (158,391),\ (169,878),\ (218,611),\ (262,601).
$$

The squareclass layer has a more principled normal form than its bounded audit
interface suggests. Fix a legal Pythagorean direction
$$
U=(u,v),\qquad |U|=c,\qquad U^\perp=(-v,u),
$$
a squarefree $q$, a positive split factor $a$, and a signed paired split factor
$b\ne0$. Put
$$
D=qab,\qquad L=\frac{q(b^2-a^2)}2.
$$
If $L$ is integral,
$$
2c\mid q(a^2+b^2)
$$
and
$$
W=\frac{-LU+D U^\perp}{c^2}
$$
is integral, then $W$ is a legal Pythagorean edge vector with length
$q(a^2+b^2)/(2c)$. Therefore every target on the line
$$
T_r=rU+W
$$
has the two-step certificate
$$
O\to rU\to T_r,
$$
except for the usual zero-coordinate degeneracies. Conversely, a target-facing
squareclass split witness is exactly this construction with
$$
b=\frac{\det(U,T)}{qa},\qquad
r=\frac{T\cdot U+L}{c^2}.
$$
Equivalently, writing Gaussian multiplication for lattice vectors,
$$
W=\frac{q\,U\,(a+ib)^2}{2c^2}.
$$
The helper `parallel_direction_squareclass_line_gaussian_numerator` exposes the
numerator $qU(a+ib)^2$ directly. Thus the coordinate part of the problem is a
single Gaussian divisibility condition by the integer $2c^2$, while the length
condition is $2c\mid q(a^2+b^2)$.

For primitive Pythagorean directions this factors one step further. There is a
Gaussian integer $\alpha$ of norm $c$ and a unit $\varepsilon\in\{\pm1,\pm i\}$
such that
$$
U=\varepsilon\alpha^2.
$$
The helper `primitive_pythagorean_direction_gaussian_root` recovers
$(\alpha,\varepsilon)$ from a signed/swapped primitive direction. Then
$$
W=\varepsilon\,
\frac{q(a+ib)^2}{2\overline{\alpha}^{\,2}}.
$$
The helper `parallel_direction_squareclass_line_root_quotient` computes this
quotient directly when it is integral. This is the main structural reduction:
for fixed $U$, the split-line classification asks when
$2\overline{\alpha}^{\,2}$ divides $q(a+ib)^2$ in $\mathbb Z[i]$, followed by
the scalar length condition and finite nondegeneracy exclusions.

Since $\alpha$ and $\overline{\alpha}$ are coprime for primitive Pythagorean
directions, this quotient test separates further. Write
$$
a+ib=\overline{\alpha}\,\beta
$$
when the quotient exists. Then the coordinate and length conditions reduce to
the parity condition
$$
q\beta^2\equiv0\pmod2
$$
in $\mathbb Z[i]$, and
$$
W=\varepsilon\,\frac{q\beta^2}{2}.
$$
The helper `parallel_direction_squareclass_line_split_quotient` computes
$\beta=(a+ib)/\overline\alpha$. Thus the split-line rows are no longer opaque
factor searches: for each primitive direction, admissible split roots
$a+ib$ lie on the Gaussian ideal generated by $\overline\alpha$, with only a
parity condition depending on $q$ and a finite nondegeneracy check left over.

The same reduction can now be run forward. Given $U=\varepsilon\alpha^2$,
a squarefree $q$, and a nonzero Gaussian integer $\beta$, set
$$
a+ib=\overline{\alpha}\beta.
$$
If the real part $a$ is positive and the imaginary part $b$ is nonzero, this
recovers a squareclass split row. The second edge is simply
$$
W=\varepsilon\frac{q\beta^2}{2},
$$
whenever $q\beta^2$ has even Gaussian coordinates; otherwise that beta row is
not integral. The helper `parallel_direction_squareclass_beta_split_root`
recovers $(a,b)$ from $\beta$, `parallel_direction_squareclass_beta_quotient`
computes the unfiltered $W$, and
`parallel_direction_squareclass_beta_second_step` applies the graph-edge
nondegeneracy check. Thus fixed-direction split rows are parameterized by
Gaussian $\beta$ rather than by target-box searches.

The beta filters are elementary. The helper `squareclass_beta_integral` records
the exact integrality condition: if $q$ is even then every nonzero $\beta$ is
allowed, while if $q$ is odd then the real and imaginary parts of $\beta$ must
have the same parity. The helper `beta_square_is_axis_degenerate` records the
only beta shapes whose square has a zero coordinate:
$$
\Re\beta=0,\qquad \Im\beta=0,\qquad\text{or}\qquad |\Re\beta|=|\Im\beta|.
$$
All other integral beta rows give a legal second edge after multiplication by
the unit $\varepsilon$.

The beta form also has a target-facing inverse. For a target $T$, fixed
$(U,q,\beta)$ first computes $W=\varepsilon q\beta^2/2$; then $T$ is certified
by this beta row exactly when
$$
T-W=rU
$$
for some integer $r$. Equivalently, in the rotated Gaussian coordinates,
$$
2\varepsilon^{-1}T-q\beta^2=2r\alpha^2.
$$
The helpers `parallel_direction_squareclass_beta_target_coefficient` and
`parallel_direction_squareclass_beta_target_certificate` implement this inverse
line-membership test. This is now a genuinely target-facing criterion over
$(U,q,\beta)$, with no determinant-factor scan.

There is an even simpler invariant form of the same target-facing test. Since
$U$ is primitive, $T-W$ is an integer multiple of $U$ exactly when
$$
\det(U,T)=\det(U,W).
$$
Thus each admissible beta row is a determinant level set, not a target box. The
helper `parallel_direction_squareclass_beta_determinant_residue` returns this
level $\det(U,W)$, and
`parallel_direction_squareclass_beta_determinant_target_certificate` certifies
a target by matching the determinant level and then recovering the scalar $r$
along $U$. In the older split variables this level is exactly
$$
\det(U,W)=qab,
$$
so the previous target-facing formula
$b=\det(U,T)/(qa)$ is just the same invariant solved for the signed paired
factor.

The ideal-membership part can also be inverted without scanning split boxes.
Write $\alpha=m+in$ and $c=N(\alpha)$. The condition
$a+ib\in(\overline\alpha)$ is equivalent to the single congruence
$$
b\equiv\rho a\pmod c,\qquad
\rho\equiv -n\,m^{-1}\pmod c,\qquad \rho^2\equiv-1\pmod c.
$$
Combining this with the determinant level $D=\det(U,T)=qab$ gives, for fixed
squarefree $q\mid D$,
$$
\frac Dq\equiv \rho a^2\pmod c
$$
or equivalently $a^2\equiv-\rho D/q\pmod c$, with the extra exact-divisor
condition $a\mid D/q$ and $b=D/(qa)$. The helper
`primitive_pythagorean_direction_conjugate_root_residue` returns $(c,\rho)$,
and `parallel_direction_squareclass_conjugate_ideal_split_roots` turns this
into the finite inverse list of legal $(a,b,\beta)$ rows for one determinant
level. The target-facing wrapper
`parallel_direction_squareclass_conjugate_ideal_certificate` then certifies
targets from these divisor roots. This reframes the split layer as modular
square roots inside the determinant leg, rather than as growing boxes in
$(q,a,b)$.

Finally, the squareclass parameter itself is finite and target-facing: any row
with $D=qab$ has squarefree $q\mid D$. The helper `squarefree_divisors`
enumerates those possibilities, and
`parallel_direction_conjugate_ideal_determinant_roots` combines them with the
conjugate-root congruence to list all legal split rows for one fixed
determinant level $(U,D)$. The target wrapper
`parallel_direction_conjugate_ideal_split_roots` just supplies
$D=\det(U,T)$. Thus, for fixed $U$, the split rows depend only on the
one-dimensional determinant coordinate; the remaining target data only decides
the line scalar $r$. The wrapper `parallel_direction_conjugate_ideal_certificate`
is therefore an exact fixed-direction split recognizer with no external bounds
on $q$, $a$, or $b$.

Applying this exact recognizer across the same finite direction set gives a
strictly cleaner fallback than the earlier bounded split box. The helper
`parallel_direction_conjugate_ideal_cover_certificate` scans only primitive
Pythagorean directions up to a Euclid-parameter bound; inside each direction,
the squareclass and split factors are determined from the target determinant.
The layered helper `pythagorean_layered_conjugate_ideal_certificate` now uses
that exact finite-direction split recognition after the fixed structural stack.
The previous six extended frontier rows with $q$ as large as $149$ and
$a$ as large as $401$ are covered by this route with the same direction bound
$8$, without increasing any squareclass or split-factor box.

The direction bound has now been rewritten in the native Gaussian-root
language. The helper `primitive_pythagorean_root_directions` enumerates rows
$(U,\alpha,\varepsilon)$ with $U=\varepsilon\alpha^2$ and bounded coordinates
of $\alpha$. For the tested bounds this gives exactly the same signed direction
set as `primitive_pythagorean_directions`, but it matches the quadratic
identity directly. The root-bounded helpers
`parallel_direction_conjugate_ideal_root_cover_witness` and
`parallel_direction_conjugate_ideal_root_cover_certificate` are now the exact
split-layer interface used by `pythagorean_layered_conjugate_ideal_certificate`.

The exact recognizer now keeps a first-class algebraic witness. A
`ParallelDirectionConjugateIdealWitness` records
$$
(T,U,q,a,b,\beta,r)
$$
and verifies all three equivalent faces of the construction:
$$
D=\det(U,T)=qab,\qquad a+ib=\overline{\alpha}\beta,
$$
and the rotated quadratic decomposition
$$
2\varepsilon^{-1}T=2r\alpha^2+q\beta^2.
$$
The helpers `parallel_direction_squareclass_conjugate_ideal_witness`,
`parallel_direction_conjugate_ideal_witness`, and
`parallel_direction_conjugate_ideal_cover_witness` return this witness data
instead of only the endpoint certificate. This is the useful proof interface
for the next step: choosing directions becomes choosing a Gaussian square
$\alpha^2$ in this binary quadratic decomposition.

The same quadratic identity is executable as a target-facing certificate test.
The helper `parallel_direction_squareclass_beta_quadratic_coefficient` computes
$r$ by dividing
$$
2\varepsilon^{-1}T-q\beta^2
$$
by $\alpha^2$ and checking that the quotient is the even real integer $2r$.
`parallel_direction_squareclass_beta_quadratic_certificate` then builds the
same midpoint certificate. The conjugate-ideal witness path now uses this
quadratic coefficient directly, so the exact split layer is verified through
the Gaussian square decomposition rather than only through determinant-level
line membership.

A scratch primitive-positive census through $1\le g,h\le2000$ found $150$
misses after the fixed structural stack, and all $150$ are covered by
`parallel_direction_conjugate_ideal_cover_witness` with the same root/direction
bound $8$. The dominant Gaussian roots in that diagnostic were
$(-2,\pm3)$, $(-1,\pm4)$, and $(-2,\pm5)$, suggesting that the next proof step
should study root-shape families for $\alpha$ rather than enlarge split boxes.
The helper `parallel_direction_conjugate_ideal_root_cover_census` now records
this kind of diagnostic data reproducibly. In the smaller guardrail through
$1\le g,h\le500$, there are $10$ structural misses, no root-bound-8 misses, and
the root-shape counts split evenly across
$$
(1,4),\quad (2,3),\quad (2,5),\quad (3,8),\quad (4,5).
$$
This makes the next proof question more concrete: replace the finite root list
by families in the root coordinates of $\alpha$.

That replacement has started in executable form. The helper
`primitive_pythagorean_root_shape_directions` generates all signed
$(U,\alpha,\varepsilon)$ rows from an explicit finite set of canonical root
shapes, and
`parallel_direction_conjugate_ideal_root_shape_cover_witness`/
`parallel_direction_conjugate_ideal_root_shape_cover_certificate` run the exact
split recognizer over those shape families. In the $1\le g,h\le1000$
guardrail, the $34$ structural misses are covered by the seven-shape family
$$
(1,4),\ (1,6),\ (2,3),\ (2,5),\ (2,7),\ (3,8),\ (4,5).
$$
This turns the residual fallback into an explicit root-shape-family cover for
the audited range. The helper
`parallel_direction_conjugate_ideal_root_shape_cover_census` records this
statement directly: for that seven-shape family it has no uncovered targets,
and the root-shape counts are
$$
(2,3):8,\quad (1,4):6,\quad (1,6):6,\quad
(2,5):4,\quad (2,7):4,\quad (3,8):4,\quad (4,5):2.
$$

This is the point where the search should stop being "make the box bigger".
The shape-cover data gives a finite list of proof obligations for a
one-dimensional divisor problem. For a fixed root shape
$\alpha=(x,y)$, a unit $\varepsilon$, and $U=\varepsilon\alpha^2$, put
$c=N(\alpha)=x^2+y^2$ and $D=\det(U,T)$. The conjugate-ideal recognizer says
that a two-step certificate exists as soon as one can choose a squarefree
$q\mid D$ and a divisor $a\mid D/q$ such that
$$
a^2\equiv-\rho D/q\pmod c,\qquad b=D/(qa),
$$
and $a+ib$ is divisible by $\overline{\alpha}$, with the quadratic coefficient
$r$ integral in
$$
2\varepsilon^{-1}T=2r\alpha^2+q\beta^2.
$$
Thus a fixed root shape is not a finite certificate table; it is a residue and
divisor theorem for the determinant coordinate $D$. The audited shapes suggest
the first root-shape spines to prove are
$$
(1,2k),\qquad (2,2k+1),
$$
with the observed adjacent or secondary small shapes such as $(3,4)$, $(3,8)$,
and $(4,5)$ handled either as separate lemmas or as the beginning of another
spine. The box audits should now be used only to test which residue classes and
divisor choices each spine must cover.

This candidate is now executable. The helper
`primitive_pythagorean_root_primary_spine_shapes` generates the primary spines
$(1,2k)$ and $(2,2k+1)$ up to a root-coordinate bound, while
`primitive_pythagorean_root_secondary_spine_shapes` records the observed
secondary shapes $(3,4)$, $(3,8)$, and $(4,5)$ when they fit inside that bound.
Their union is `primitive_pythagorean_root_spine_shapes`. The wrappers
`parallel_direction_conjugate_ideal_root_primary_spine_cover_witness` and
`parallel_direction_conjugate_ideal_root_secondary_spine_cover_witness`
separate the primary and secondary cases, while
`parallel_direction_conjugate_ideal_root_spine_cover_witness`,
`parallel_direction_conjugate_ideal_root_spine_cover_certificate`, and
`parallel_direction_conjugate_ideal_root_spine_cover_census` apply the exact
conjugate-ideal recognizer to this generated family. In the scratch
$1\le g,h\le2000$ primitive-positive diagnostic, the two primary spines alone
cover $132$ of the $150$ structural misses; the remaining $18$ are exactly on
the three secondary shapes above, and the generated spine family covers all
$150$ root-bound-8 residuals.

The residue side of the spine problem is also explicit. The helper
`gaussian_root_conjugate_divisibility_residue` computes the congruence
$b\equiv\rho a\pmod c$ directly from $\alpha$. On the two primary spines this
gives
$$
\alpha=(1,2k):\quad c=4k^2+1,\qquad \rho\equiv-2k\pmod c,
$$
and
$$
\alpha=(2,2k+1):\quad c=(2k+1)^2+4,\qquad
\rho\equiv-(2k+1)/2\pmod c.
$$
The sign and unit variants only replace $\rho$ by the corresponding signed
square root of $-1$ modulo $c$.

The witness now exposes this as checkable proof-obligation data:
`root_shape`, `conjugate_root_residue`, `determinant_squareclass_quotient`,
`divisor_root_residue`, `split_root_congruence_holds`, and
`divisor_root_congruence_holds`. For example, the primary residual
$(139,878)$ is carried by shape $(1,4)$ with
$(q,a,b)=(1,449,-11)$, while the secondary residual $(151,338)$ is carried by
shape $(4,5)$ with $(q,a,b)=(2,19,-239)$. These are no longer opaque search
hits: they are named divisor-root congruence obligations.

The first primary spine is now promoted from observed shape family to a uniform
certificate theorem.  For any $k\ge1$ and nonzero integers $q,t,r$, let
$$
U=(1-4k^2,4k),\qquad
\beta=(4kt+2k-1,\,-(2t+1)).
$$
Then $U$ is the Pythagorean direction generated by the root shape $(1,2k)$,
and
$$
T=rU+\frac q2\beta^2
$$
has the two-step certificate with midpoint $rU$.  In coordinates, the second
step is
$$
\left(
2q((2k+1)t+k)((2k-1)t+k-1),\
-q(4kt+2k-1)(2t+1)
\right).
$$
The condition $t\ne0$ is only for the endpoint nondegeneracy of the $k=1$
row.  The Lean theorem `certificateValid_oneEvenRootSpineLine` proves this
whole primary spine, and the Python constructor
`one_even_root_spine_line_certificate` exposes it executable-side.  The
companion orbit constructor
`one_even_root_spine_line_orbit_certificate` transports the certificate across
all sign changes and coordinate swaps of the target.

The companion primary spine is also uniform.  For $k\ge1$, put
$n=2k+1$ and
$$
U=(-4n,4-n^2),\qquad \beta=(1-2nt,\ 4t-1).
$$
For every nonzero $q,t,r$, the target
$$
T=rU+\frac q2 i\beta^2
$$
has midpoint certificate $rU$.  In coordinates, the second step is
$$
\left(
q(4t-1)(2nt-1),\
2qt(n-2)(nt+2t-1)
\right).
$$
The specialization $k=1$ recovers the existing odd-integral $(2,3)$ row.
The Lean theorem `certificateValid_twoOddRootSpineLine` and Python constructor
`two_odd_root_spine_line_certificate` therefore close the second primary spine
$(2,2k+1)$.  The executable constructor
`two_odd_root_spine_line_orbit_certificate` packages the same row with
sign/swap transport, giving the full symmetry orbit of each primary
$(2,2k+1)$ target.

The secondary root shape $(3,4)$ now has the same explicit line-row treatment,
including both even and odd beta branches.
For nonzero $m,r$ and beta coordinates $a,b$ with $ab(a^2-b^2)\ne0$, the
midpoint $r(-7,24)$ certifies
$$
r(-7,24)+m(a^2-b^2,\ 2ab).
$$
For odd beta coordinates $(2a+1,2b+1)$ and
$m r (2a^2+2a-2b^2-2b)\ne0$, the same midpoint certifies
$$
r(-7,24)+m(2a^2+2a-2b^2-2b,\ (2a+1)(2b+1)).
$$
The coordinate-swapped row uses midpoint $r(24,7)$.  Lean proves these as
`certificateValid_threeFourRootSpineLine` and
`certificateValid_threeFourRootSpineLineSwap`, with odd-beta counterparts
`certificateValid_threeFourOddRootSpineLine` and
`certificateValid_threeFourOddRootSpineLineSwap`.  The executable constructors
`three_four_root_spine_line_certificate` and
`three_four_odd_root_spine_line_certificate` expose the rows beside the
existing secondary $(3,8)$ and $(4,5)$ rows.  The promoted root-spine
reconstructor now includes the signed beta images and sign/swap transports of
all three observed secondary rows $(3,4)$, $(3,8)$, and $(4,5)$, so generated
witnesses in their signed orientations reconstruct to their exact two-step
certificates.

The helper
`parallel_direction_conjugate_ideal_root_spine_divisor_obligation_census`
compresses a residual sample to those obligations. In the $1\le g,h\le500$
guardrail, the generated spine family has $10$ structural misses, no uncovered
targets, and only five shape-squareclass buckets:
$$
((2,3),1),\quad ((1,4),2),\quad ((2,5),10),\quad
((4,5),2),\quad ((3,8),1).
$$
Using only the primary spines leaves exactly
$$
(151,338),\ (158,391),\ (338,151),\ (391,158)
$$
uncovered in that range, isolating the first secondary obligations.

Each obligation now has an executable two-stage predicate. The helpers
`parallel_direction_conjugate_ideal_divisor_obligation_strip_modulus` and
`parallel_direction_conjugate_ideal_divisor_obligation_strip_residue` convert
$(q,c,D/q\bmod c)$ into the determinant congruence
$$
\det(U,T)\equiv q(D/q\bmod c)\pmod {qc}.
$$
`parallel_direction_conjugate_ideal_divisor_obligation_strip_holds` checks this
linear strip, and
`parallel_direction_conjugate_ideal_divisor_obligation_divisor_holds` checks
the remaining requirement that $|D/q|$ have a divisor in the recorded
$a\bmod c$ class. This is the precise proof split: determinant strips are
linear congruences in $(g,h)$; the hard part is proving the needed divisor
class occurs on each strip.

The divisor-class test itself is now expressed multiplicatively. The helper
`divisor_residue_classes(n,c)` computes the closure of the prime-power residue
choices of $n$ modulo $c$:
$$
\{\prod p_i^{e_i}\bmod c:0\le e_i\le v_{p_i}(n)\}.
$$
Thus a divisor-obligation failure is exactly the assertion that the recorded
class $a\bmod c$ is missing from this closure. In the pinned strip census,
the $4398$ divisor-class failures have $215$ distinct closures. By failure
mass, the dominant closure sizes are
$$
2:1683,\quad 4:1322,\quad 6:817,\quad 8:305,
$$
followed by smaller tails beginning
$$
3:68,\quad 12:58,\quad 9:22,\quad 16:20.
$$
By distinct closure sets, the largest size buckets are
$$
4:51,\quad 8:49,\quad 6:29,\quad 12:21,\quad 16:10.
$$
For the pinned rows the moduli are prime, so this same closure can be pushed
into the cyclic group $(\mathbb Z/c\mathbb Z)^*$. The helpers
`primitive_root_mod_prime`, `discrete_log_table_mod_prime`, and
`prime_modulus_divisor_exponent_classes` choose generators
$$
(13,2),\quad (17,3),\quad (29,2),\quad (41,6),\quad (73,5)
$$
and rewrite every nonzero divisor residue as an exponent set. The required
missing exponents in the pinned failures are
$$
(13,7):2806,\quad (17,1):626,\quad (73,44):316,\quad
(73,62):259,\quad (41,19):188,\quad (41,9):179,\quad (29,21):24.
$$
Thus the remaining divisor side is no longer an unstructured divisor search:
it is a question about finite sumsets of prime-factor valuation intervals in
cyclic groups.
The first additive-combinatorics guardrail is now executable as well. The
helpers `cyclic_sumset`, `cyclic_subset_stabilizer_step`, and
`cyclic_sumset_kneser_data` compute the exponent sumset, its translation
stabilizer, and its Kneser lower-bound defect. In the pinned failures,
$$
4161\text{ of }4398
$$
have trivial stabilizer, so a proof that only quotients by a nontrivial
subgroup cannot explain the main mass. The nontrivial stabilizer tail is small:
$$
(13,4,3):138,\quad (17,8,2):46,\quad (13,6,2):38,\quad
(17,2,8):10,\quad (41,20,2):4,\quad (73,8,9):1,
$$
where each triple is $(c,\text{stabilizer step},\text{stabilizer size})$.
Kneser-critical failures, with defect $0$, account for $2139$ rows; the largest
defect buckets are
$$
(13,12,1,0):1284,\quad (13,12,1,1):872,\quad
(17,16,1,0):370,\quad (13,12,1,2):354.
$$
This suggests the next theorem should be a critical-pair/near-critical-pair
analysis of short arithmetic-progression sumsets in $\mathbb Z/(c-1)\mathbb Z$,
with only the small periodic tail passing to quotient groups.
The same data now records the saturation obstruction directly. For exponent
summands $A_i$, let
$$
\ell=\sum_i(|A_i|-1).
$$
If the Kneser lower bound reaches $c-1$, the exponent closure is the whole
group and the divisor class cannot be missing. In the pinned failures the
effective lengths are tiny:
$$
c=13:\ell\le7,\quad c=17:\ell\le7,\quad c=29:\ell\le7,\quad
c=41:\ell\le8,\quad c=73:\ell\le9.
$$
The largest failure masses are at $\ell=1,2,3$, for example
$$
(13,1):1194,\quad (13,2):854,\quad (13,3):536,\quad
(73,2):207,\quad (73,3):120.
$$
This turns the divisor side into a bounded-sequence obstruction: for each
prime modulus, failures can only come from short sequences of prime-factor
discrete logs. Long enough determinant factorizations force divisor success by
Kneser saturation before any fallback row is needed.
The strip census now applies this dichotomy before the divisor/fallback split.
Across the $5818$ pinned strip targets, Kneser saturation gives $192$ direct
divisor successes; another $1228$ strip targets are short-log divisor
successes; and all $4398$ divisor failures are short-log rows that are then
handled by the structural fallback stack. By modulus, the saturated branch only
appears for $c=13$ in this pinned sample:
$$
c=13:\quad 192\text{ saturated successes},\quad 742\text{ short successes},
\quad 2806\text{ short failures}.
$$
For $c=17,29,41,73$ every pinned strip target remains below saturation, so the
proof task there is entirely the short-log success/fallback dichotomy.
This gives a sharper arithmetic target for the strip-discharge proof: prove
that missing divisor-root closures on each determinant strip force one of the
explicit structural congruence rows below.

There is now an executable guardrail for the complementary branch as well.
`parallel_direction_conjugate_ideal_divisor_obligation_strip_census` scans the
determinant strips and counts which strip targets pass the divisor-class test,
which fail it, and whether those failures are already handled by the structural
stack. For the ten obligation rows from the $1\le g,h\le500$ residual census,
the strip scan through $1\le g,h\le100$ found no non-structural divisor-class
failures. The structural half is now labeled by
`pythagorean_layered_structural_label`: in that scan the failure counts are
$$
\text{promoted }3\text{-}4\text{-}5:4184,\quad
\text{lattice-pair}:203,\quad
\text{orthogonal}:6,\quad
\text{standard-completion}:5.
$$
The census also records this split per obligation. The two $(2,3)$ strips have
identical fallback structure, each with $1345$ promoted $3$-$4$-$5$ failures,
$53$ lattice-pair failures, $3$ orthogonal failures, and $2$
standard-completion failures. The $(1,4)$, $(2,5)$, $(4,5)$, and $(3,8)$
strips have only promoted $3$-$4$-$5$ and lattice-pair fallback in the pinned
range, except one $(3,8)$ strip with a single standard-completion fallback.
Thus the current proof target has become a named dichotomy: on each obligation
strip, either prove the recorded divisor class occurs, or prove the target
falls into one of these structural families.

The target-facing form of this dichotomy is now factored out of the census.
`PINNED_ROOT_SPINE_DIVISOR_OBLIGATIONS` freezes the ten obligation rows from
the generated-spine residual census, while
`parallel_direction_conjugate_ideal_divisor_obligation_exponent_profile`
records the prime-modulus exponent sumset, required exponent, Kneser lower
bound, and saturation/short branch for one strip target.
`parallel_direction_conjugate_ideal_divisor_obligation_discharge_witness` then
returns the exact theorem branch for a target on a pinned strip: direct divisor
success, promoted signed `3-4-5`, lattice-pair, orthogonal, or
standard-completion. The new guardrail checks one direct divisor success and
one example from every structural fallback family, including the explicit
congruence row each fallback uses. This does not prove the infinite
strip-discharge theorem, but it turns the missing theorem into a target-facing
row classifier rather than logic embedded only inside a bounded census.

A larger determinant-level falsification shows that the strip-local theorem is
not true as stated. The target
$$
T=(108638,24031)
$$
lies on the pinned obligation strip
$$
((4,5),2,41,9,10,33,19)
$$
for direction $U=(-40,-9)$, but the requested divisor class is missing and the
current structural stack returns no fallback. The target is still certified by
a different generated root-spine row: direction $(-3,4)$, root shape $(1,2)$,
squareclass $535$, split factor $1$, paired factor $-947$, and
$\beta=(-379,189)$. The corrected executable branch
`parallel_direction_conjugate_ideal_divisor_obligation_global_discharge_witness`
therefore first tries the local divisor/structural discharge and then allows an
alternate generated root-spine witness. The missing theorem is consequently a
global root-choice theorem, not a theorem that each pinned strip discharges in
isolation.

The observed alternate-root exits are now promoted to explicit infinite line
rows. The `(1,2)` row uses direction $(-3,4)$ and
$\beta=(4t+1,-(2t+1))$. The `(1,4)` row uses directions $(-8,-15)$ and its
coordinate swap $(-15,-8)$; besides the one-parameter row with
$\beta=(8t+3,-(2t+1))$, the even-squareclass row now allows arbitrary
nondegenerate $\beta$. The odd-integral `(2,3)` row uses directions
$(-12,-5)$ and $(-5,-12)$; besides the one-parameter row
$\beta=(1-6t,4t-1)$, the odd-beta row now allows arbitrary odd beta
coordinates. The even `(2,3)` row fixes direction $(-12,-5)$ and uses the
second edge $m i\beta^2$. The `(2,5)` row uses
directions $(-20,21)$ and $(-21,20)$ with even squareclass quotient. The
secondary `(4,5)` and odd-beta `(3,8)` rows now cover the four finite-frontier
non-primary examples. Python constructors check these line formulas against the
alternate-root stress-test witnesses, and Lean proves the corresponding
certificate rows
`certificateValid_oneTwoRootSpineLine`,
`certificateValid_oneFourRootSpineLine`,
`certificateValid_oneFourRootSpineLineSwap`,
`certificateValid_oneFourEvenRootSpineLine`,
`certificateValid_oneFourEvenRootSpineLineSwap`,
`certificateValid_twoThreeOddRootSpineLine`,
`certificateValid_twoThreeOddRootSpineLineSwap`,
`certificateValid_twoThreeOddGeneralRootSpineLine`,
`certificateValid_twoThreeOddGeneralRootSpineLineSwap`,
`certificateValid_twoThreeEvenRootSpineLine`,
`certificateValid_twoFiveRootSpineLine`, and
`certificateValid_twoFiveRootSpineLineSwap`, plus
`certificateValid_threeFourRootSpineLine`,
`certificateValid_threeFourRootSpineLineSwap`,
`certificateValid_threeFourOddRootSpineLine`,
`certificateValid_threeFourOddRootSpineLineSwap`,
`certificateValid_fourFiveRootSpineLine`,
`certificateValid_fourFiveRootSpineLineSwap`,
`certificateValid_threeEightOddRootSpineLine`, and
`certificateValid_threeEightOddRootSpineLineSwap`. The executable helper
`promoted_root_spine_line_certificate_from_witness` now reconstructs these
explicit certificates from a generic root-spine witness; the bounded global
root-choice guardrail checks that every alternate root witness in
`1 <= g,h <= 500` reconstructs this way. This does not close global root
choice, but it replaces the observed alternate-root search output with named
row-family proof obligations.

The next concrete global-choice theorem target is therefore:

> For any primitive target on a pinned divisor-obligation strip, if
> `parallel_direction_conjugate_ideal_divisor_obligation_discharge_witness` is `None`
> then `parallel_direction_conjugate_ideal_divisor_obligation_global_discharge_witness`
> must still succeed, and any non-exceptional alternate branch must lie in one of
> the explicit infinite line families listed above.
>
> The only observed non-primary exceptions (for `1 <= g,h <= 500`) are the four
> targets
> $(151,338)$, $(158,391)$, $(338,151)$, $(391,158)$; these now have explicit
> secondary line rows from shapes `(3,8)` and `(4,5)`.

A perf-scoped regression test in `tests/test_pythagorean_walks.py` currently
checks this target claim on the same `1 <= g,h <= 500` range against all pinned
obligations.

The helper
`parallel_direction_conjugate_ideal_global_root_choice_audit` now extracts the
same global-root-choice guardrail as a direct proof artifact.  Instead of
rescanning the full box for every signed direction, it iterates each pinned
determinant strip by solving the linear congruence
$$
u_xh-u_yg\equiv R\pmod S.
$$
In the `1 <= g,h <= 500` guardrail this audits $105337$ divisor-class failures:
$105323$ discharge through the local divisor/structural stack and the remaining
$14$ discharge through an alternate root-spine witness.  All $14$ alternate
witnesses first pass the target-facing squareclass line-residue certificate
for their recorded $(U,q,a)$ row, then reconstruct through the promoted
explicit line rows; the helper records no missing, residue-line-missing, or
unreconstructed rows.  Their promoted root shapes are
$$
(1,4):4,\quad (2,5):4,\quad (2,3):2,\quad (3,8):2,\quad (4,5):2.
$$
The audit rows also record the minimal paired-factor period and the surviving
paired residue $b\bmod P$ for each alternate line.  By row mass these periods
are
$$
P=17:4,\quad P=29:4,\quad P=146:2,\quad
P=26:1,\quad P=41:1,\quad P=338:1,\quad P=3362:1.
$$
For each such fixed alternate split line, the original failed pinned strip
reduces to the first-coefficient congruence
$$
\det(U,V)r\equiv R-\det(U,W)\pmod S,
$$
where $U$ is the pinned strip direction, $V$ is the alternate line direction,
and $W$ is the alternate second edge.  The audit records no missing
line/strip intersections.  By row mass the resulting coefficient moduli are
$$
13:8,\quad 73:4,\quad 82:2.
$$
Thus the $14$ non-local target hits reduce to $14$ distinct
failed-strip/alternate-line intersection rows but only $10$ distinct alternate
squareclass line rows before the pinned-strip intersection is imposed.
The audit now validates these distinct intersection rows directly: for each
new row key it rebuilds the representative certificate at the recorded
first-coefficient residue and checks that this representative lies on the
original pinned strip.  Thus the row table is not only a summary of target
examples; each row is independently executable as a certificate-producing
line/strip congruence.
The row table is also materialized as
`PINNED_GLOBAL_ROOT_CHOICE_ALTERNATE_LINE_STRIP_ROWS`, and
`pinned_global_root_choice_alternate_line_strip_rows_valid` checks it without
rerunning the target-box audit.  The audit test requires this portable table to
match the discovered rows exactly, giving a finite artifact that can be ported
to a theorem statement separately from the search procedure.  The table
validator also rebuilds the representative
`ParallelDirectionConjugateIdealWitness` for each row and checks that
`promoted_root_spine_line_certificate_from_witness` returns the same
certificate, so the portable rows carry both the line/strip congruence proof and
the promoted explicit-row reconstruction.
The same table is now usable in the target-facing direction via
`pinned_global_root_choice_table_witness` and
`pinned_global_root_choice_table_certificate`.  Given a target, a failed pinned
strip direction, and its divisor obligation, these helpers first verify the
original determinant strip, then try only the matching portable alternate rows.
They enforce the recorded paired-factor residue class, rebuild the squareclass
line certificate, reconstruct the promoted conjugate-ideal witness, and return
only if the promoted certificate agrees exactly.  The audit regression checks
that this table discharge reproduces all fourteen non-local witnesses recorded
by the finite frontier.  The global pinned-obligation discharge now tries this
table before the generic root-spine cover search and records the branch
`alternate_root_spine_table` when it succeeds.  In the 500-box guardrail, every
recorded finite-frontier non-local row takes this table branch; larger examples
that are not in the portable table still fall through to the isolated
`alternate_root_spine` branch.  This separates the already-explicit finite
frontier from the remaining infinite existence problem instead of mixing both
behind one opaque root-spine call.
The helper
`parallel_direction_conjugate_ideal_global_root_choice_branch_audit` exposes
this split directly over pinned strip failures.  At radius $500$ it reports
$105337$ divisor-obligation strip failures, with $105323$ local discharges:
$$
\text{promoted\_345}:100191,\quad
\text{lattice\_pair}:4968,\quad
\text{standard\_completion}:111,\quad
\text{orthogonal}:53,
$$
and $14$ global discharges, all through `alternate_root_spine_table`.  The
same audit also records the alternate root-shape and direction counts for the
global rows, so new non-table rows can be separated by promoted family instead
of rediscovered through the opaque root-spine scan.
The helper
`parallel_direction_conjugate_ideal_global_root_choice_exponent_signature_audit`
now records the divisor-exponent profiles of these non-local rows.  In every
sampled global row through radius $1750$, the local divisor obstruction is a
`short_failure`: the Kneser saturation branch has not fired, and the required
divisor exponent is outside the finite sumset generated by the prime-power
residue choices of the determinant quotient.  At radius $500$, the $14$
global rows compress to $10$ such signatures.  Their effective-length counts
are
$$
1:6,\quad 2:4,\quad 3:4,
$$
and their prime-modulus counts are
$$
13:8,\quad 41:2,\quad 73:4.
$$
This gives a sharper target for the remaining infinite argument: prove an
alternate root-spine construction for the short exponent-signature cases left
after the local divisor/Kneser discharge, rather than for all strip points at
once.
The companion audit
`parallel_direction_conjugate_ideal_global_root_choice_signature_template_audit`
correlates those short signatures with the alternate line templates that
discharge them.  At radius $500$, the $10$ short exponent signatures meet $10$
alternate line templates through $14$ signature-template incidences.  Four
modulus-$13$ signatures each split across two sign/swap-related templates; the
remaining signatures are single-template in this finite frontier.  This is the
first executable interface between the divisor-exponent obstruction and the
alternate root-spine line families: an infinite proof can now aim to construct
one of the recorded line-template types directly from a short exponent
signature, instead of appealing to the root-spine search as a black box.
The signature itself is now exposed independently of any radius audit as
`global_root_choice_short_exponent_signature`.  It returns the tuple
$(p,e,z,\ell,\mathcal S)$ only for profiles whose saturation branch is
`short_failure`; non-short profiles have no short signature.  The target-facing
signature-template path uses this helper directly, so the signature definition
is no longer just an internal byproduct of the finite audit summaries.
This interface is now target-facing as well.  The helper
`global_root_choice_signature_template_witness` takes a target, pinned
obligation, and a table of short-signature/line-template incidences; it computes
the target's divisor-exponent signature, selects matching templates, recomputes
the paired split from the target determinant, and returns the explicit
promoted-line witness when the target lies on one of those templates.  In the
radius-$500$ guardrail, the signature-template rows reconstructed from the
audit reproduce every non-local alternate witness exactly, including the
alternate direction, squareclass, split factors, beta, and first coefficient.
The radius-$500$ signature-template rows are now pinned as
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_500_SIGNATURE_TEMPLATE_ROWS`, and
`parallel_direction_conjugate_ideal_global_root_choice_signature_template_coverage_audit`
measures how far any such table reaches.  Applied at radius $750$, the
radius-$500$ signature-template table covers the original $14$ global rows and
misses exactly the six new generic rows.  The missing short-signature counts
are
$$
(13,7,\{0,1\}+\{0,10\}):2,\quad
(13,7,\{0,6,9\}+\{0,11\}):2,\quad
(17,1,\{0,6\}):2,
$$
with missing root-shape counts $(2,7):4$ and $(2,3):2$.  This turns the next
frontier into a concrete list of short exponent signatures and alternate
templates to construct, instead of another undifferentiated collection of
target examples.
Those six rows are now promoted into
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_SIGNATURE_TEMPLATE_ROWS`: the radius-$750$
signature-template table has $20$ incidences, $13$ distinct short signatures,
and $16$ distinct alternate templates, and it reconstructs all $20$ radius-$750$
global rows with no mismatch.  A probe against the radius-$1000$ branch audit
shows that this $750$ table covers exactly the previous $20$ rows and misses
the next $22$ rows, with missing root-shape counts
$$
(1,6):14,\quad (2,3):6,\quad (2,5):2.
$$
These missing templates are exactly the radius-$1000$ portable-template
frontier, now also visible as a short-signature-template frontier.
The radius-$1000$ frontier has now also been promoted:
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_SIGNATURE_TEMPLATE_ROWS` contains $40$
signature-template incidences, representing $21$ distinct short signatures and
$28$ distinct alternate templates, and it reconstructs all $42$ radius-$1000$
global rows with no mismatch.  Applying this table at radius $1250$ covers the
previous $42$ rows and misses the next $20$ rows, with missing root-shape counts
$$
(2,3):12,\quad (1,4):6,\quad (1,6):2.
$$
Again the missing alternate templates match the independently pinned
radius-$1250$ portable-template frontier.
The helper
`parallel_direction_conjugate_ideal_global_root_choice_iterated_signature_template_closure_audit`
now packages this operation.  For a fixed radius it reuses the global branch
audit, measures which rows a signature-template table covers, extracts the
missing short-signature/template rows from the observed alternate witnesses,
and repeats until the finite box is covered.  The audit now also returns the
actual saturated `final_rows` table and the `new_rows` introduced at each
layer, so the closure output can be fed directly into the no-root-spine
signature-template discharge path instead of remaining only a count summary.
The companion
`parallel_direction_conjugate_ideal_global_root_choice_signature_template_closure_chain_audit`
threads those generated `final_rows` through an increasing sequence of finite
boxes.  This is still a sampled finite process, but it matches the intended
inductive proof shape more closely: each stage is a finite saturation lemma
whose output table becomes the input table for the next radius.
The chain audit also emits a compact ledger row for each stage.  Each row
records the input and output table sizes, the stage's initial nonlocal deficit,
the final coverage counts, the generated signature/template/normalized-shape
projection counts, the reused normalized-shape counts, and the missed
root-shape distribution.  For the sampled radius chain $(1500,1750,2000)$ from
the radius-$1250$ signature-template table, the ledger rows are
$$
\begin{array}{c|c|c|c|c|c|c|c}
R & \text{in} & \text{out} & \text{global} & \text{missed} &
\text{new rows} & \text{new sigs} & \text{new templates}\\
\hline
1500 & 60 & 108 & 112 & 50 & 48 & 18\ (12\ \mathrm{new}) & 30\\
1750 & 108 & 144 & 148 & 36 & 36 & 20\ (8\ \mathrm{new}) & 18\\
2000 & 144 & 192 & 198 & 50 & 48 & 22\ (12\ \mathrm{new}) & 36
\end{array}
$$
All three stages close with zero final misses and zero mismatches; the 2000
stage is the first one in this sampled chain with a reused normalized template
shape.
The same ledger rows now also record normalized-template root-shape projection
counts.  For the three sampled stages the new normalized alternate-template
root-shape counts are
$$
\begin{array}{c|l}
R & \text{new normalized alternate-template root shapes}\\
\hline
1500 & (2,3):10,\ (4,5):4,\ (1,4):2,\ (2,5):2,\ (1,6):1\\
1750 & (2,3):9,\ (2,5):2,\ (4,5):2,\ (1,4):1\\
2000 & (2,3):14,\ (1,4):10,\ (3,4):2
\end{array}
$$
At radius $2000$ the novel counts are the same except that the $(1,4)$ count is
$9$ rather than $10$, because one $(1,4)$ normalized shape was already present
in the input table.  This separates genuinely new root-shape families from
recombinations of already-seen normalized shapes.
The ledger also records the divisor-modulus projection of the generated short
signatures.  The novel short-signature modulus counts in the same sampled
chain are
$$
\begin{array}{c|l}
1500 & 13:6,\ 73:4,\ 17:2\\
1750 & 13:2,\ 17:2,\ 41:2,\ 73:2\\
2000 & 41:6,\ 73:3,\ 13:2,\ 29:1
\end{array}
$$
Thus the radius-$2000$ stage is also the first sampled stage in this chain that
introduces modulus $29$, while most genuinely new signatures in that layer sit
over modulus $41$.  The ledger further records the combined modulus/root-shape
projection for normalized short-signature/template shapes.  In the radius
$2000$ stage the first $(3,4)$ normalized signature-template shapes all occur
over modulus $41$:
$$
(41,(3,4)):2.
$$
The only reused normalized short-signature/template cross-cell in that stage is
$$
(13,(1,4)):1.
$$
This is the current smallest arithmetic split separating the new $(3,4)$
frontier from the reused $(1,4)$ shape.
Finally, the ledger records the pinned divisor-obligation keys responsible for
the stage's initial deficit.  The sampled chain is still concentrated on a
small number of obligation families: six at radius $1500$, eight at radius
$1750$, and nine at radius $2000$.  The radius-$2000$ deficit is dominated by
the two $(2,3)$ modulus-$13$ obligations, with $14$ targets each, followed by
the two $(4,5)$ modulus-$41$ obligations, with $5$ targets each.  The first
modulus-$29$ obligation appears there as a single $(2,5)$ frontier target:
$$
((2,5),10,29,17,12,28,17):1.
$$
At radius $1000$, starting from
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_SIGNATURE_TEMPLATE_ROWS`, one iteration
closes the box:
$$
20\ \text{input rows},\quad 22\ \text{missed global rows},\quad
20\ \text{new signature-template rows},\quad 40\ \text{output rows}.
$$
The final coverage audit then covers all $42$ radius-$1000$ global rows with no
misses or mismatches, and the saturated `final_rows` are exactly
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_SIGNATURE_TEMPLATE_ROWS`.  This is still
finite, but it makes the target-facing signature-template saturation step
explicit and reusable.
The same iterative mechanism closes the radius-$1500$ branch audit from the
radius-$1250$ signature-template table in one layer:
$$
60\ \text{input rows},\quad 50\ \text{missed global rows},\quad
48\ \text{new signature-template rows},\quad 108\ \text{output rows}.
$$
The final coverage audit covers all $112$ radius-$1500$ global rows with no
misses or mismatches.  The fact that $50$ missed targets yield $48$ new
signature-template rows records the first small collision in this target-facing
closure format.  Projecting this layer gives $18$ distinct short signatures,
$12$ genuinely new short signatures, $30$ alternate line templates, $19$
normalized alternate-template shapes, and $33$ normalized
short-signature/template shapes.  All $30$ templates and all normalized shapes
in the layer are new relative to the radius-$1250$ input table.
Feeding the generated radius-$1500$ `final_rows` table into the radius-$1750$
branch audit closes the next sampled box in one layer as well:
$$
108\ \text{input rows},\quad 36\ \text{missed global rows},\quad
36\ \text{new signature-template rows},\quad 144\ \text{output rows}.
$$
The final coverage audit covers all $148$ radius-$1750$ global rows with no
misses or mismatches.  In contrast to the radius-$1500$ layer, the $36$ missed
targets give $36$ distinct new signature-template rows.  Projecting the new
layer gives $20$ distinct short signatures, $8$ genuinely new short signatures,
$18$ alternate line templates, $14$ normalized alternate-template shapes, and
$28$ normalized short-signature/template shapes; again all templates and
normalized shapes in the layer are new relative to the input table.  The
normalized shape summary of the resulting $144$-row table has $47$ short
signatures, $88$
alternate templates, $60$ normalized alternate-template shapes, and $105$
normalized short-signature/template shapes, with root-shape counts
$$
(2,3):64,\quad (1,4):20,\quad (2,5):20,\quad (4,5):18,\quad
(1,6):16,\quad (2,7):4,\quad (3,8):2.
$$
The next sampled layer, from the generated radius-$1750$ table to radius
$2000$, also closes in one iteration:
$$
144\ \text{input rows},\quad 50\ \text{missed global rows},\quad
48\ \text{new signature-template rows},\quad 192\ \text{output rows}.
$$
The final coverage audit covers all $198$ radius-$2000$ global rows with no
misses or mismatches.  Its missed root-shape counts are
$$
(2,3):26,\quad (1,4):22,\quad (3,4):2,
$$
so this sample is the first target-facing signature-template layer in this
chain that introduces the promoted $(3,4)$ root shape.  Projecting the layer
gives $22$ distinct short signatures, $12$ genuinely new short signatures,
$36$ alternate line templates, $26$ normalized alternate-template shapes, and
$39$ normalized short-signature/template shapes.  Here one normalized
alternate-template shape and one normalized short-signature/template shape are
already present in the input table, so the novelty counts are $25$ and $38$,
respectively.  The repeated normalized template is
$$
((1,4),\ 17,\ (1,1033),\ 34),
$$
and the repeated normalized short-signature/template shape is obtained by
prefixing it with the short signature
$$
(13,\ 7,\ \mathrm{False},\ 1,\ ((0,11),)).
$$
The normalized shape summary of the resulting $192$-row table has $59$ short
signatures, $124$ alternate templates, $85$ normalized alternate-template
shapes, and $143$ normalized short-signature/template shapes, with root-shape
counts
$$
(2,3):90,\quad (1,4):40,\quad (2,5):20,\quad (4,5):18,\quad
(1,6):16,\quad (2,7):4,\quad (3,4):2,\quad (3,8):2.
$$
The same promotion has now been made at radius $1250$:
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_SIGNATURE_TEMPLATE_ROWS` has $60$
signature-template incidences, $27$ distinct short signatures, and $40$
distinct alternate templates, and it reconstructs all $62$ radius-$1250$
global rows with no mismatch.  Applied to the radius-$1500$ branch audit, this
table covers the previous $62$ rows and misses the next $50$ rows, whose
root-shape counts are
$$
(2,3):28,\quad (4,5):10,\quad (2,5):6,\quad (1,4):4,\quad (1,6):2.
$$
This is the same residual layer already seen in the radius-$1500$ portable
template audit, but expressed in target-facing short-signature form.
The helper `global_root_choice_signature_template_shape_audit` now records a
coarser case count by suppressing signs and split-factor order in each
alternate line template while retaining the root shape, squareclass, split pair,
and period.  On the radius-$1250$ signature-template table this reduces the
$60$ raw incidences to $27$ normalized template shapes and $44$ normalized
short-signature/template shapes.  This normalization is not yet a proof of
symmetry equivalence, but it identifies the smaller collection of arithmetic
template shapes that a parametric argument would need to explain.
There is also now a direct discharge helper,
`parallel_direction_conjugate_ideal_divisor_obligation_signature_template_discharge_witness`,
which performs the local divisor/structural checks and then uses a supplied
signature-template table for the alternate branch, without calling the
root-spine cover search.  The radius-$1250$ guardrail verifies that
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_SIGNATURE_TEMPLATE_ROWS` reconstructs
the exact structural row for every one of the $62$ global rows through this
no-root-spine-search discharge path.
The finite scan itself can also be run without the root-spine search:
`parallel_direction_conjugate_ideal_signature_template_branch_audit` iterates
the pinned strip failures, applies the local discharge stack, and uses only a
supplied signature-template table for the remaining branch.  At radius $500$,
using `PINNED_GLOBAL_ROOT_CHOICE_RADIUS_500_SIGNATURE_TEMPLATE_ROWS`, this
no-root audit has the same $105337$ checked strip failures, the same $105323$
local discharges, and $14$ alternate discharges through
`alternate_signature_template`; its global structural rows match the original
root-spine branch audit exactly.
The same no-root finite scan is now checked at radius $750$ with
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_SIGNATURE_TEMPLATE_ROWS`: it sees
$233598$ checked strip failures, $233578$ local discharges, and all $20$
non-local rows discharge through `alternate_signature_template`, again with no
missing rows and structural rows matching the original root-spine branch audit.
At radius $1000$, the no-root finite scan using
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_SIGNATURE_TEMPLATE_ROWS` likewise
matches the original branch audit on the checked strip failures and local
discharges, and discharges all $42$ non-local rows through
`alternate_signature_template` with matching structural rows.  Thus the
target-facing signature-template tables replace the root-spine search in the
full finite branch scan through radius $1000$.
The same replacement has now been checked at radius $1250$ with
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_SIGNATURE_TEMPLATE_ROWS`: the no-root
scan has the same checked strip failures and local discharges as the original
branch audit, discharges all $62$ non-local rows through
`alternate_signature_template`, and has no missing or unreconstructed rows.
Using the concrete `final_rows` produced by the radius-$1500$ iterated
signature-template closure gives the analogous finite branch-scan replacement
at radius $1500$: all $112$ non-local rows discharge through
`alternate_signature_template`, with structural rows matching the original
root-spine branch audit.  This extends the no-root-spine finite guardrail from
the pinned tables to a table generated by the saturation closure itself.
The reconstruction check now has a final explicit beta-line tier:
`promoted_root_spine_line_certificate_from_witness` first tries the named
promoted rows and their sign/swap orbits, and if those do not cover the witness
it rebuilds the direct
`parallel_direction_squareclass_beta_line_certificate` from the witness's
direction, squareclass, beta, and first coefficient.  This is still conditional
on having an alternate root-spine witness, but once the witness exists the
certificate itself is no longer search-only.  The branch audit records
`unreconstructed_rows`; the radius-$500$ and radius-$750$ regressions both
require this list to be empty.  At radius $750$ the first six non-table global
rows appear, with shapes $(2,7),(2,3),(2,3),(2,7),(2,7),(2,7)$, and all six
reconstruct through the promoted/beta-line path.
These first six non-table rows are now also converted into portable
line/strip rows by
`global_root_choice_branch_row_alternate_line_strip_row` and pinned as
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_GENERIC_LINE_STRIP_ROWS`.  Each row
passes the same `pinned_global_root_choice_alternate_line_strip_row_valid`
validator as the original $14$-row finite frontier, and an extended row table
consisting of the original $14$ rows plus these six rows discharges the six
radius-$750$ generic branches target-facing.  This is not an infinite
existence theorem, but it turns the next observed generic fallback layer into
the same finite line/strip certificate format used by the explicit frontier.
The portable-row growth is now measured separately by
`parallel_direction_conjugate_ideal_global_root_choice_portable_row_audit`.
Relative to the original $14$ rows, radius $750$ has $20$ distinct global
line/strip rows and exactly the six pinned new rows above; relative to the
extended $20$-row table it has no new rows.  The six new radius-$750$ rows have
root-shape counts
$$
(2,7):4,\quad (2,3):2,
$$
and alternate-direction counts
$$
(-45,28):2,\quad (-28,45):2,\quad (-12,5):1,\quad (-5,12):1.
$$
At radius $1000$, however, the same extended table sees $42$ distinct global
line/strip rows, hence $22$ new valid portable rows.  Their root-shape counts
are
$$
(1,6):14,\quad (2,3):6,\quad (2,5):2,
$$
with the dominant new alternate directions $(-35,12):6$ and $(-12,35):6$.
At the line-template level these $22$ rows compress to $12$ templates.  The
four dominant templates each account for three pinned strip intersections:
$$
((-35,12),1,89,-349,74,21),\quad
((-35,12),10,3583,-1,37,36),
$$
$$
((-12,35),1,349,-89,74,59),\quad
((-12,35),10,1,-3583,2738,1893).
$$
Here each tuple records
$(\text{alternate direction},q,a,b,\text{paired period},\text{paired residue})$.
The helper `global_root_choice_line_template_strip_rows` now expands such a
template across all pinned divisor-obligation strips.  For the four dominant
templates above, the expansions have sizes $24,40,24,40$ respectively.  All
expanded rows pass the portable row validator; rows with coefficient residue
$0$ use the coefficient modulus as the nonzero representative certificate
coefficient, preserving the congruence while avoiding a degenerate midpoint.
The union helper `global_root_choice_line_template_table_rows` deduplicates
these expansions into $128$ valid portable rows.  Adding those template rows to
the $20$-row radius-$750$ table reduces the radius-$1000$ deficit from $22$ new
rows to $10$, with remaining root-shape counts
$$
(2,3):6,\quad (1,6):2,\quad (2,5):2.
$$
Those ten remaining rows are pinned as the residual template set
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_RESIDUAL_LINE_TEMPLATES`; its eight
templates expand to $192$ valid portable rows.  Together,
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_DOMINANT_LINE_TEMPLATES` and the
residual templates expand to $320$ valid portable rows, and adding those rows
to the $20$-row radius-$750$ table closes the radius-$1000$ portable-row audit:
$42$ global rows, $42$ distinct rows, and $0$ new rows.
This closure can also be reproduced automatically by
`parallel_direction_conjugate_ideal_global_root_choice_iterated_template_closure_audit`:
starting from the $20$-row table, its first layer observes $22$ new rows,
compresses them to $12$ line templates, expands those templates to $320$ valid
portable rows, and closes with a $340$-row finite table and no remaining
radius-$1000$ deficit.  This records the finite template-saturation operation
as a reusable audit rather than only as a manually staged list of template
constants.
The same template audit has now been pushed to radius $1250$.  After the
radius-$1000$ template closure, the residual radius-$1250$ frontier has $20$
new rows with root-shape counts
$$
(2,3):12,\quad (1,4):6,\quad (1,6):2.
$$
These compress to
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_RESIDUAL_LINE_TEMPLATES`, a set of $12$
line templates whose pinned-strip expansion contains $352$ valid portable rows.
Adding those rows closes the radius-$1250$ portable-row audit: $62$ global
rows, $62$ distinct rows, and $0$ new rows.  The helper
`parallel_direction_conjugate_ideal_global_root_choice_template_closure_audit`
packages this operation: it expands a given template set, adds it to a base
portable table, and returns the remaining portable-row audit.  This shows
finite template closures can be built at increasing radii, but also that the
template frontier continues to grow; the remaining proof needs a parametric
existence mechanism for these growing line/strip families, not just more finite
template enumeration.
The next closure layer is also recorded.  After the radius-$1250$ template
closure, the radius-$1500$ frontier has $50$ new rows with root-shape counts
$$
(2,3):28,\quad (4,5):10,\quad (2,5):6,\quad (1,4):4,\quad (1,6):2.
$$
These compress to
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1500_RESIDUAL_LINE_TEMPLATES`, a set of $30$
line templates whose pinned-strip expansion contains $823$ valid portable rows.
Adding those rows closes the radius-$1500$ portable-row audit: $112$ global
rows, $112$ distinct rows, and $0$ new rows.
The next sampled layer has the same shape.  After the radius-$1500$ template
closure, the radius-$1750$ frontier has $36$ new rows with root-shape counts
$$
(2,3):16,\quad (2,5):8,\quad (1,4):6,\quad (4,5):6.
$$
These compress to
`PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1750_RESIDUAL_LINE_TEMPLATES`, a set of $18$
line templates whose pinned-strip expansion contains $523$ valid portable rows.
Adding those rows closes the radius-$1750$ portable-row audit: $148$ global
rows, $148$ distinct rows, and $0$ new rows.  A smaller radius-$1600$ probe
found only the first four of these templates, accounting for $8$ new rows, so
the finite frontiers are still appearing in bounded layers rather than
stabilizing to a fixed table.
On the Lean side, the ten distinct alternate squareclass line rows are now
also represented by concrete certificate theorems
`certificateValid_pinnedGlobalRootChoiceAlternateLineRow01` through
`certificateValid_pinnedGlobalRootChoiceAlternateLineRow10`.  Each theorem is
proved by specializing the corresponding promoted root-spine family theorem,
so the finite table is tied directly to the named Lean proof rows rather than
to arithmetic replay alone.  The fourteen original pinned strip intersections
are represented by the companion Lean congruence theorems
`pinnedGlobalRootChoiceAlternateLineRow01_strip` through
`pinnedGlobalRootChoiceAlternateLineRow14_strip`, each proving the required
determinant residue for the row representative.  These are also packaged as
combined row theorems
`pinnedGlobalRootChoiceAlternateLineRow01_valid` through
`pinnedGlobalRootChoiceAlternateLineRow14_valid`, whose conclusion contains
both the certificate and the pinned-strip congruence for the representative.
The aggregate theorem `pinnedGlobalRootChoiceAlternateLineRows_valid` packages
all fourteen combined rows into one finite-frontier lemma.
The first target-facing Lean bridge is now parametric.  The theorem
`lineStripCertificateValid` proves the generic row-validity step used by the
alternate template program: once the alternate direction and second step are
legal graph edges, a nonzero first coefficient, a recorded paired-factor
residue, and the one-variable line/strip coefficient congruence imply both
`certificateValid` for the line target and the required pinned
determinant-strip congruence.  The companion `lineStripRowValid` packages the
same determinant-strip conclusion when a promoted line theorem has already
proved `certificateValid`, and `det_add_smul_line` supplies the linear
determinant expansion behind both bridges.
One recurrent normalized `(2,3)` family from the frontier is also ported:
`certificateValid_twoThreeOddSplitElevenResidueOneThirtyThreeLineStrip`
covers the alternate direction `(-12,-5)` with squareclass `1`, split `11`,
and signed paired factor `338t+133`, i.e. the normalized residue class
`b ≡ 133 mod 338`.  For every nonzero first coefficient satisfying the
line/strip coefficient congruence, the theorem produces the certificate and
the pinned-strip residue.  This replaces another representative pin for that
family with a theorem over the full residue line.
The companion swapped-direction split-$11$ line is now ported as
`certificateValid_twoThreeOddSplitElevenResidueTwentyThreeLineStrip`.  It
covers direction `(-5,-12)` with second step
`(2(t+3)(5t+4), (-6t-7)(-4t-1))` and paired factor `26t+23`, hence the
normalized residue class `b ≡ 23 mod 26`.  The only extra degeneracy excluded
by the underlying promoted root-spine theorem is `t != -3`; under that
condition, a nonzero first coefficient and the same one-variable line/strip
coefficient congruence imply the certificate, pinned determinant residue, and
paired-residue congruence.
The next recurrent normalized family is now ported too:
`certificateValid_oneFourEvenSplitTwoFortyOneLineStrip` packages the two
orientation lemmas for root shape `(1,4)`, squareclass `2`, split pair
`(5,241)`, and paired-factor period `17`.  The `(-15,-8)` orientation uses
paired factor `17t+12` and excludes only the degenerate parameter `t = 56`;
the `(-8,-15)` orientation uses paired factor `17t+5` and excludes only
`t = -57`.  Away from those axis-degenerate second-step parameters, each
orientation proves the line certificate, the pinned determinant residue, and
the paired-residue congruence from the same line/strip coefficient congruence.
The largest remaining radius-$1000$ normalized family is now ported directly:
`certificateValid_oneSixSplitEightyNineThreeFortyNineLineStrip` covers root
shape `(1,6)`, squareclass `1`, split pair `(89,349)`, and paired-factor
period `74`.  The `(-35,12)` orientation uses paired factor `74t+21` and
second step `(70t^2-18t-112,-24t^2-182t-15)`; the `(-12,35)` orientation uses
paired factor `74t+59` and second step
`(24t^2-622t-1045,-70t^2-338t+1332)`.  Both second-step vectors are proved
legal directly by polynomial nonzero factorizations and square-norm identities,
then fed through `lineStripCertificateValid`.  This avoids relying on the
fallback beta-line reconstruction for this family.
Two adjacent `(1,6)` split-$3583$ families are also ported with direct
line/strip proofs.  The period-$37$ family
`certificateValid_oneSixSplitThirtyFiveEightyThreeResidueThirtySixLineStrip`
covers direction `(-35,12)`, squareclass `10`, split `3583`, and paired
factor `37t+36`; it excludes only the axis-degenerate parameter `t=-582`.
The period-$2738$ family
`certificateValid_oneSixSplitThirtyFiveEightyThreeResidueEighteenNinetyThreeLineStrip`
covers direction `(-12,35)`, squareclass `10`, split `1`, and paired factor
`2738t+1893`.  Both use explicit beta-square second steps and the generic
`lineStripCertificateValid` bridge.
The signed-direction `(1,6)` split-$2917$ family is ported similarly as
`certificateValid_oneSixSplitTwentyNineSeventeenLineStrip`, covering
directions `(-35,-12)` and `(-12,-35)` with squareclass `7`, split pair
`(1,2917)`, period `74`, and paired residues `43` and `31`.
The `(2,3)` squareclass-$13$ split-$473$ family is now theorem-backed as
`certificateValid_twoThreeOddSquareclassThirteenSplitFourSeventyThreeLineStrip`.
It covers directions `(-12,5)` and `(-5,12)` with paired residues `21` and
`25` modulo `26`, excluding only the two axis-degenerate parameters in the
corresponding orientation formulas.
The clean `(2,5)` split-$1583$ family is also theorem-backed:
`certificateValid_twoFiveSplitOneFifteenEightyThreeLineStrip` packages the two
orientations with squareclass `10`, split pair `(1,1583)`, and paired-factor
period `29`.  The `(-21,20)` orientation has paired factor `29t+12` and
specializes `certificateValid_twoFiveRootSpineLineSwap` with beta
`(5t+2,-2t-1)`; the `(-20,21)` orientation has paired factor `29t+28` and
specializes `certificateValid_twoFiveRootSpineLine` with beta
`(-5t-114,-2t+271)`.  Both orientations have nonzero and non-axis hypotheses
discharged arithmetically for all integer `t`, so the theorem only needs the
nonzero first coefficient and the line/strip coefficient congruence.
The `(2,5)` squareclass-$23$ split-$1549$ family is now ported as
`certificateValid_twoFiveOddSquareclassTwentyThreeSplitFifteenFortyNineLineStrip`.
It packages directions `(-21,20)` and `(-20,21)` with paired residues `57`
and `17` modulo `58`, proving the beta-square legal-step witnesses directly
and then discharging the pinned strip row through `lineStripCertificateValid`.
The two recurrent `(2,7)` doubletons are now ported the same way.  The odd
split pair `(179,229)` is
`certificateValid_twoSevenOddSplitOneSeventyNineTwoTwentyNineLineStrip`, with
directions `(-45,28)` and `(-28,45)` and paired residues `89` and `33`
modulo `106`.  The squareclass-$2$ split pair `(19,1153)` is
`certificateValid_twoSevenEvenSplitNineteenElevenFiftyThreeLineStrip`, with
the same two directions and paired residues `13` and `34` modulo `53`.
The six remaining radius-$1000$ singleton normalized shapes are now ported as
theorem-backed line/strip families as well: the `(2,3)` odd split rows
`certificateValid_twoThreeOddSplitOneHundredSevenOneFifteenResidueTwoThirtyOneLineStrip`,
`certificateValid_twoThreeOddSplitTwentyThreeFiveThirtyFiveResidueOneFortyOneLineStrip`,
`certificateValid_twoThreeOddSplitElevenTwoFiftySevenResidueEightyOneLineStrip`,
and `certificateValid_twoThreeOddSplitElevenTwoFiftySevenResidueTwentyThreeLineStrip`,
plus the `(4,5)` squareclass-$2$ rows
`certificateValid_fourFiveEvenSplitNineteenTwoThirtyNineResidueThirtyOneTwentyThreeLineStrip`
and `certificateValid_fourFiveEvenSplitNineteenTwoThirtyNineResidueTwentyTwoLineStrip`.
The period-$26$ split-$257$ row excludes the same axis-degenerate parameter
`t=-3` as the earlier period-$26$ split-$881$ row, and the period-$41$
split-$239$ row excludes its axis-degenerate parameter `t=-53`; the other four
singleton rows have all axis and nonzero conditions discharged for every
integer parameter.
The largest missing radius-$1250$ normalized shape is now theorem-backed too:
`certificateValid_oneFourOddSquareclassSeventeenSplitTenThirtyThreeLineStrip`
covers root shape `(1,4)`, squareclass `17`, split pair `(1,1033)`, and
period `34`.  Its two orientations have directions `(-15,8)` and `(-8,15)`
with paired residues `33` and `21`, and their second-step legal-edge
conditions are discharged directly for every integer parameter.  This adds
the six radius-$1250$ signature-template incidences for that normalized shape
to the proved signature-template row set.
The next radius-$1250$ squareclass-$13$ `(2,3)` family is now ported as two
period-specific theorem rows:
`certificateValid_twoThreeOddSquareclassThirteenSplitNineOhFiveResidueOneOhNineLineStrip`
for direction `(-12,-5)`, period `338`, residue `109`, and
`certificateValid_twoThreeOddSquareclassThirteenSplitNineOhFiveResidueTwentyOneLineStrip`
for direction `(-5,-12)`, period `26`, residue `21`.  Together they cover the
six split-$905$ radius-$1250$ signature-template incidences, with only the
period-$26$ orientation excluding its axis-degenerate parameter `t=-1`.
The rest of the radius-$1250$ frontier is now theorem-backed as well.  The
remaining `(2,3)` shapes are
`certificateValid_twoThreeEvenSplitSeventyOneOneTwentyOneLineStrip`,
`certificateValid_twoThreeSquareclassFiveSplitNineteenOneSeventyThreeLineStrip`,
and `certificateValid_twoThreeSquareclassFortySixSplitThreeSeventeenLineStrip`,
covering normalized templates `((2,3),2,(71,121),13)`,
`((2,3),5,(19,173),26)`, and `((2,3),46,(1,317),13)`.  The two split-$475$
`(1,6)` rows are ported as
`certificateValid_oneSixSquareclassTenSplitFourSeventyFiveResidueOneLineStrip`
and
`certificateValid_oneSixSquareclassTenSplitFourSeventyFiveResidueTwentySevenThirtySevenLineStrip`.
After these ports, the proved signature-template row set covers all $60$
radius-$1250$ signature-template rows, plus the large pre-existing
counterexample row.
The first radius-$1500$ normalized frontier family is now theorem-backed:
`certificateValid_twoThreeEvenSplitNineteenSixFortyOneLineStrip` covers root
shape `(2,3)`, squareclass `2`, split pair `(19,641)`, and period `13`.
Its two orientations have directions `(-12,5)` and `(-5,12)` with paired
residues `9` and `7`; the only axis-degenerate parameters excluded are
`t=-8` and `t=246`.  This adds the six matching radius-$1500$
signature-template incidences to the proved row set.
The next four-incidence radius-$1500$ `(2,3)` family is also ported:
`certificateValid_twoThreeOddSplitSixtySevenTwoFiftySevenLineStrip` covers
squareclass `1`, split pair `(67,257)`, and period `26`.  Its orientations
have paired residues `3` and `11`; the only axis-degenerate parameters are
`t=-13` and `t=49`.
The large pre-existing local-discharge counterexample now has its own
theorem-backed normalized family:
`certificateValid_oneTwoSquareclassFiveThirtyFiveSplitNineFortySevenResidueThreeLineStrip`.
It covers direction `(-3,4)`, squareclass `535`, split pair `(1,947)`, paired
residue `3` modulo `50`, and excludes only the degenerate representative
`t=0`.  The executable template witness was tightened accordingly: instead of
requiring the residue-class enumerator to accept the least representative, it
constructs the certificate from the actual paired determinant factor and then
validates the resulting line certificate.  This lets the proved
signature-template branch discharge the counterexample row with structural
data `((-3,4),(1,2),535,1,-947,(-379,189),9586654)` without invoking the
root-spine search.
The `(3,8)` split-$1531$ family is now ported as
`certificateValid_threeEightOddSplitNineteenFifteenThirtyOneLineStrip`.  It
packages the `(-55,48)` orientation with paired factor `146t+127` and the
`(-48,55)` orientation with paired factor `146t+75`, both by specializing the
odd `(3,8)` root-spine line theorem and then applying `lineStripRowValid`.
The executable side now has the matching radius-independent proved-family
registry:
`GLOBAL_ROOT_CHOICE_PROVED_NORMALIZED_LINE_FAMILIES`.  It records the
thirty
normalized template shapes
$$
((1,4),2,(5,241),17),\qquad
((1,4),17,(1,1033),34),\qquad
((1,6),1,(89,349),74),\qquad
((1,6),10,(1,3583),37),\qquad
((1,6),10,(1,3583),2738),\qquad
((1,6),10,(1,475),37),\qquad
((1,6),10,(1,475),2738),\qquad
((1,6),7,(1,2917),74),\qquad
((1,2),535,(1,947),50),\qquad
((2,3),1,(11,881),338),\qquad ((2,3),1,(11,881),26),\qquad
((2,3),1,(11,257),338),\qquad ((2,3),1,(11,257),26),\qquad
((2,3),1,(23,535),338),\qquad ((2,3),1,(67,257),26),\qquad
((2,3),1,(107,115),338),\qquad
((2,3),13,(1,473),26),\qquad
((2,3),13,(1,905),338),\qquad ((2,3),13,(1,905),26),\qquad
((2,3),2,(71,121),13),\qquad
((2,3),2,(19,641),13),\qquad
((2,3),5,(19,173),26),\qquad
((2,3),46,(1,317),13),\qquad
((2,5),10,(1,1583),29),\qquad
((2,5),23,(1,1549),58),\qquad
((2,7),1,(179,229),106),\qquad
((2,7),2,(19,1153),53),\qquad
((4,5),2,(19,239),3362),\qquad
((4,5),2,(19,239),41),\qquad
((3,8),1,(19,1531),146)
$$
together with the Lean theorem names above.  The radius-$1000$
signature-template regression checks that all forty distinct
signature-template frontier rows with the radius-$1000$ subset of these
normalized shapes are exactly the
two split-$11$ short signatures
$(13,7,\mathrm{False},1,((0,5),(0,)))$ and
$(17,1,\mathrm{False},1,((0,14),(0,)))$ paired with the two proved normalized
families, the six split-$349$ rows on signatures
$(13,7,\mathrm{False},1,((0,11),))$,
$(17,1,\mathrm{False},1,((0,14),))$, and
$(73,\{44,62\},\mathrm{False},2,((0,31),(0,39)))$, the four split-$241$ rows
on signatures
$(13,7,\mathrm{False},3,((0,1),(0,9),(0,1)))$,
$(73,44,\mathrm{False},2,((0,4),(0,30)))$, and
$(73,62,\mathrm{False},2,((0,4),(0,30)))$, the four split-$3583$ rows on
signatures $(13,7,\mathrm{False},1,((0,11),))$ and
$(41,\{9,19\},\mathrm{False},2,((0,39),(0,29)))$, the two split-$2917$ rows
on signature $(13,7,\mathrm{False},1,((0,11),))$, the two squareclass-$13$
split-$473$ rows on signature $(13,7,\mathrm{False},2,((0,1),(0,10)))$, plus
the four split-$1583$
rows on
signatures $(13,7,\mathrm{False},2,((0,9),(0,2)))$ and
$(13,7,\mathrm{False},3,((0,6,9),(0,5)))$, the two squareclass-$23$
split-$1549$ rows on signature
$(13,7,\mathrm{False},2,((0,9),(0,8)))$, the two odd split-$(179,229)$ rows
on signature $(17,1,\mathrm{False},1,((0,6),))$, the two squareclass-$2$
split-$(19,1153)$ rows on signature
$(13,7,\mathrm{False},3,((0,6,9),(0,11)))$, the four singleton `(2,3)` rows
on signatures $(17,1,\mathrm{False},1,((0,14),))$ and
$(41,\{9,19\},\mathrm{False},1,((0,8),))$, the two singleton `(4,5)` rows on
$(73,\{44,62\},\mathrm{False},1,((0,34)))$, and the two split-$1531$ rows on
$(13,7,\mathrm{False},1,((0,11),))$.  This keeps the finite table as a
frontier audit while making the ported normalized-family case split explicit.
The helper `global_root_choice_proved_signature_template_witness` is the
target-facing version of this registry: it uses the short signature to select
candidate template rows, but only attempts rows whose normalized template has a
Lean theorem in `GLOBAL_ROOT_CHOICE_PROVED_NORMALIZED_LINE_FAMILIES`.  The
companion discharge wrapper records the branch
`alternate_proved_signature_template`.  In the radius-$1000$ regression this
proved-family path covers all $42$ branch rows, collapsing to exactly the
forty distinct frontier rows above and no unproved normalized templates.
This separates theorem-backed parametric cases from the remaining finite
evidence.
The Python helper `pinned_global_root_choice_alternate_line_strip_summary`
exposes the matching compact finite artifact: $14$ row-table entries, $10$
distinct alternate line rows, $14$ distinct failed-strip intersections,
coefficient moduli $13:8$, $73:4$, and $82:2$, with the portable row-table
validator passing.  Its obligation distribution is concentrated on six pinned
obligations:
$$
((2,3),1,13,5,7,4,11):4,\quad
((2,3),1,13,8,6,4,11):4,
$$
$$
((4,5),2,41,9,10,33,19):1,\quad
((4,5),2,41,32,10,8,34):1,
$$
$$
((3,8),1,73,27,38,69,19):2,\quad
((3,8),1,73,46,38,4,71):2.
$$
This is still finite evidence, not the infinite global root-choice theorem, but
it makes the exact non-local frontier auditable without relying on the older
opaque nested search loop.

The largest fallback bucket is no longer opaque. Since the promoted
$3$-$4$-$5$ layer is itself a finite table of signed directions and determinant
factors, the strip census also records its aggregate decomposition. In the same
guardrail, the $4184$ promoted failures split by signed direction as
$$
(-4,-3):1617,\ (-4,3):993,\ (-3,-4):630,\ (-3,4):354,
$$
$$
(3,-4):310,\ (3,4):145,\ (4,-3):104,\ (4,3):31,
$$
and by factor as
$$
1:1517,\ 2:714,\ 4:424,\ 3:343,\ 5:318,\ 8:307,\ 9:204,\ 25:181,\ 6:176.
$$
This points to a finite discharging proof rather than a larger box: each
determinant strip should be partitioned into a divisor-class-success part and
intersections with these promoted $3$-$4$-$5$ congruence rows, plus the much
smaller lattice-pair, orthogonal, and standard-completion fallback rows.

The fixed direction/factor rows now have a closed congruence form. For a legal
direction $V=(u,v)$ of length $c$, a factor $F>0$, and a target $T=(g,h)$, put
$$
D=\det(V,T),\qquad A=V\cdot T.
$$
The factor-row integrality condition is equivalent to $D\ne0$ and the two
congruences
$$
D^2+F^2\equiv0\pmod {2cF},
$$
$$
D^2-F^2+2FA\equiv0\pmod {2Fc^2}.
$$
The helper `parallel_direction_factor_congruence_holds` implements this
predicate, and `parallel_direction_factor_residue_classes` now uses it directly.
This removes another layer of opaque factor-search logic: promoted rows are
explicit quadratic congruence rows in $(g,h)$.

For primitive $V$, the row has an even smaller determinant parametrization.
Modulo $c^2$, the target lattice itself forces
$$
A\equiv vu^{-1}D\pmod {c^2},
$$
because
$$
c^2 g=uA-vD,\qquad c^2h=vA+uD.
$$
Thus a fixed factor row can be listed by determinant residues
$D_0\bmod M$, where $M=2c^2F$, for which the factor-forced dot class
$$
A\equiv (F^2-D_0^2)/(2F)\pmod {c^2}
$$
agrees with $vu^{-1}D_0$. The helper
`parallel_direction_primitive_factor_determinant_residue_rows` returns these
$(D_0,A_0)$ rows, and
`parallel_direction_primitive_factor_determinant_residue_holds` checks a target
against them. For example, the $(3,4),F=1$ row has only five determinant rows
modulo $50$:
$$
(7,1),(17,6),(27,11),(37,16),(47,21),
$$
each representing $50$ target residue classes. The promoted $3$-$4$-$5$
integrality rows in the executable guardrail all satisfy this same compression:
the number of modular target residues is exactly $M$ times the number of
determinant rows, before the pointwise certificate nondegeneracy check.

The strip intersection count can also use this determinant parametrization.
For a fixed determinant row $D_0$, choose $E$ with $\det(V,E)=1$. Targets in
that row are represented modulo $M$ by
$$
T\equiv D_0E+kV\pmod M.
$$
Intersecting with a divisor-obligation strip
$\det(U,T)\equiv R\pmod S$ leaves the single linear congruence
$$
\det(U,V)k\equiv R-D_0\det(U,E)\pmod {\gcd(M,S)}.
$$
Each compatible $k$ lifts to $S/\gcd(M,S)$ residue classes modulo
${\rm lcm}(M,S)$. The helper
`parallel_direction_primitive_factor_integrality_strip_intersection_linear_rows` returns
the explicit rows
$$
(D_0,\ k_0,\ m,\ \#),
$$
where $k\equiv k_0\pmod m$ is the surviving linear congruence and $\#$ is the
number of target residue classes it represents modulo ${\rm lcm}(M,S)$. The
wrapper `parallel_direction_primitive_factor_integrality_strip_intersection_residue_count`
sums these integrality row counts and is checked against the older target-residue
CRT counter on promoted-row intersections for representative divisor
obligations.
For the sample strip $U=(-12,-5)$, $S=13$, $R=7$ intersected with
$V=(-4,-3),F=1$, the five determinant rows are
$$
(3,0,1,650),(13,0,1,650),(23,0,1,650),(33,0,1,650),(43,0,1,650),
$$
which sum to $3250$ residue classes modulo $650$.
The companion helper
`parallel_direction_primitive_factor_integrality_strip_intersection_linear_row_witness`
classifies an individual target by this same row format. In the sample above,
$(1,15)$ lies in the row $(43,0,1,650)$, while targets that satisfy only the
factor row or only the strip return no row. Thus the linear-row format is both
an integrality counting object and a target-facing integrality predicate.

The strip-failure census now records how the actual promoted fallbacks land in
these integrality linear rows after they have already been certified by the
promoted witness constructor. In the pinned $1\le g,h\le100$ guardrail for the
ten divisor-obligation rows, all $4184$ promoted $3$-$4$-$5$ strip failures have
an integrality linear-row witness. The full row list is too large to be a good
proof artifact:
it uses $2668$ distinct
$(\text{obligation},U,V,F,D_0,k_0,m)$ rows. The useful compression is the
modulus distribution. By failure mass, the row moduli are
$$
m=1:3714,\quad m=2:449,\quad m=5:16,\quad m=10:5,
$$
and by distinct rows they are
$$
m=1:2305,\quad m=2:342,\quad m=5:16,\quad m=10:5.
$$
So this fallback branch is not a small finite table, but it has a simple
one-dimensional shape: almost all promoted fallback points satisfy the strip
automatically once the determinant row is chosen, and the remaining cases only
impose moduli $2$, $5$, or $10$ on the parameter $k$.

The next fallback bucket, lattice-pair, is much smaller and now has its own
compact census. All $203$ lattice-pair strip failures in the same guardrail
have an exact `pythagorean_lattice_pair_witness`. By failure mass, their
determinants are
$$
7:51,\ 13:36,\ 55:18,\ 47:16,\ 31:12,\ 17:9,\ 73:7,
$$
$$
23:6,\ 155:6,\ 185:6,\ 475:4,\ 817:4,\ 841:4,
$$
$$
16:2,\ 107:2,\ 109:2,\ 115:2,\ 157:2,\ 311:2,\ 443:2,
$$
$$
515:2,\ 989:2,\ 1369:2,\ 1435:2,\ 36:1,\ 68:1.
$$
After identifying repeated ordered direction pairs, these failures use only
$63$ distinct lattice-pair rows over $26$ determinant values, with determinant
distribution
$$
47:6,\ 13:4,\ 31:4,\ 55:4,\ 73:4,\ 155:4,
$$
$$
7:2,\ 17:2,\ 23:2,\ 107:2,\ 109:2,\ 115:2,\ 157:2,\ 185:2,
$$
$$
311:2,\ 443:2,\ 475:2,\ 515:2,\ 817:2,\ 841:2,\ 989:2,
$$
$$
1369:2,\ 1435:2,\ 16:1,\ 36:1,\ 68:1.
$$
The lattice-pair/strip intersection is now explicit too. If a lattice-pair row
uses legal directions $A,B$ with determinant $\Delta$ and a target is written
as
$$
T=mA+nB,
$$
then an obligation strip
$$
\det(U,T)\equiv R\pmod S
$$
is just the coefficient congruence
$$
\det(U,A)m+\det(U,B)n\equiv R\pmod S.
$$
The helper `pythagorean_lattice_pair_strip_linear_congruence` returns this
row, and `pythagorean_lattice_pair_strip_intersection_residue_count` counts the
combined target residues modulo $L=\operatorname{lcm}(\Delta,S)$. Writing
$$
G=\gcd(\det(U,A),\det(U,B),S),
$$
the intersection is empty unless $G\mid R$, and otherwise has
$$
\frac{L^2G}{S\Delta}
$$
target residue classes modulo $L$. In the pinned strip census, this congruence
is primitive for $202$ of the $203$ lattice-pair failures; the remaining one
has $G=2$. By distinct strip/pair congruence rows, the distribution is
$177$ primitive rows and one $G=2$ row. This makes the lattice-pair fallback
another one-dimensional congruence branch rather than a bounded pair search.

So the residual proof should not be "search a larger box". It should be a
finite discharging theorem for each divisor-obligation strip:

1. prove the recorded divisor class occurs; or
2. prove the target lies in one of the promoted $3$-$4$-$5$ determinant rows;
   or
3. prove it lies in one of the finitely many lattice-pair determinant rows,
   with the orthogonal and standard-completion rows handled as the final small
   exceptional families.

The guardrail has already checked this discharge pattern on the pinned strips:
there are no non-structural strip failures in the scan, every promoted failure
has a linear-row witness, and every lattice-pair failure has both a lattice-pair
witness and the coefficient-congruence row above.

The two final small buckets now have row forms as well. Orthogonal fallbacks are
just the special lattice-pair case $B=iA$, so the same coefficient congruence
applies. The six pinned orthogonal strip failures are all primitive
coefficient rows: by failure mass and by distinct rows, $G=1$ in every case.

For standard-completion fallbacks, fix a legal direction $V$ of length $c$ and
write
$$
D=\det(V,T),\qquad A=V\cdot T.
$$
The two standard completions of the determinant leg are encoded by a branch
$\sigma\in\{+1,-1\}$. If $D$ is odd, the row conditions are
$$
D^2+1\equiv0\pmod {2c},\qquad
A+\sigma\frac{D^2-1}{2}\equiv0\pmod {c^2}.
$$
If $D$ is even, they are
$$
D^2+4\equiv0\pmod {4c},\qquad
A+\sigma\frac{D^2-4}{4}\equiv0\pmod {c^2}.
$$
The helper `parallel_direction_standard_completion_quadratic_rows` enumerates
these branch rows modulo $4c^2$, and
`parallel_direction_standard_completion_quadratic_row_witness` classifies a
target by its $(D\bmod 4c^2,A\bmod c^2)$ row. In the pinned strip census, the
five standard-completion failures use four direction/branch pairs and five
distinct quadratic rows, with row moduli $676=4\cdot13^2$ twice and
$1156=4\cdot17^2$ three times.
The helper `parallel_direction_standard_completion_determinant_rows` then
filters those rows to the determinant residues compatible with the target
lattice, and
`parallel_direction_standard_completion_strip_intersection_linear_rows`
intersects them with a divisor-obligation strip by the same one-parameter
$k$ congruence used for the promoted rows. The five pinned
standard-completion failures all have such a linear-row witness; by failure
mass and by distinct rows the surviving $k$-moduli are
$$
m=1:3,\qquad m=13:2.
$$

At this point the pinned strip census has no residual opaque fallback:
promoted $3$-$4$-$5$, lattice-pair, orthogonal, and standard-completion
failures all have explicit congruence-row witnesses.

The promoted-row integrality intersections can also be computed exactly,
without scanning targets. Suppose a promoted direction/factor integrality row is
periodic modulo $M$ and an
obligation strip is
$$
\det(U,T)\equiv R\pmod S.
$$
Writing $G=\gcd(M,S)$, a promoted row residue $T_0\bmod M$ has lifts to the
strip modulo $\operatorname{lcm}(M,S)$ exactly when
$$
\det(U,T_0)\equiv R\pmod G.
$$
When this compatibility holds, it contributes $S/G$ lifted residue classes.
The helper `parallel_direction_factor_integrality_strip_intersection_residue_count`
implements this CRT count for any determinant strip and factor integrality row, and
`parallel_direction_conjugate_ideal_promoted_345_integrality_strip_intersection_counts`
applies it to all signed promoted $3$-$4$-$5$ rows for one divisor obligation.
For example, the obligation
$$
((4,5),2,41,9,10,33,19)
$$
has $288$ possible signed-strip/promoted integrality-row intersections; the CRT
compatibility test eliminates $80$ of them before any target box is used,
leaving $208$ nonzero congruence-row intersections to discharge.

In this formulation, a principled route to the conjecture is:

1. keep the existing structural stack for the large solved region;
2. for each remaining primitive ray, choose a root-shape spine for $\alpha$;
3. prove that the associated determinant $D$ has the required squarefree
   divisor $q$ and divisor root $a$ in the congruence above;
4. verify the finitely many degeneracies where $q\beta^2$ makes an axis edge
   or where the sign of $r$ fails.

This would replace larger-box searches by a finite set of root-shape family
lemmas plus finite degeneration checks.

After clearing the single factor of $2$, this Gaussian divisibility condition
and the length condition become the congruence system
$$
q(b^2-a^2)\equiv0\pmod2,
$$
$$
q(a^2+b^2)\equiv0\pmod {2c},
$$
$$
q((b^2-a^2)u+2abv)\equiv0\pmod {2c^2},
$$
and
$$
q((b^2-a^2)v-2abu)\equiv0\pmod {2c^2}.
$$
The helper `parallel_direction_squareclass_line_congruence_holds` is the direct
predicate for this system. The helper
`parallel_direction_squareclass_line_second_step` then returns $W$ exactly when
these congruences produce an integral legal Pythagorean edge. This distinction
separates true residue failures from finite degeneracies: for example
$(U,q,a)=((-9,40),2,19)$ accepts the congruence class $b\equiv7\pmod {41}$,
but the lift $b=171$ gives the vertical vector $W=(0,-722)$ and is excluded
only by the graph-edge nondegeneracy rule.
The helper `parallel_direction_squareclass_line_certificate` builds this
line-family certificate directly, and
`ParallelDirectionSquareclassSplitWitness.signed_paired_split_factor` exposes
the signed value of $b$ recovered from a target-facing witness.

For fixed $U,q,a$, the conditions above are periodic in the signed paired
factor $b$ modulo
$$
2|U|^2=2c^2.
$$
Indeed, replacing $b$ by $b+2c^2$ preserves the parity of $L$, the condition
$2c\mid q(a^2+b^2)$, and the two $c^2$-divisibility conditions defining $W$.
The helper `parallel_direction_squareclass_line_residue_classes` computes the
resulting minimal residue period, and
`parallel_direction_squareclass_line_residue_certificate` turns it back into a
target-facing certificate by testing
$$
\frac{\det(U,T)}{qa}\pmod m.
$$
For example, two of the first frontier rows compress to a single residue class:
$$
(U,q,a)=((-40,9),149,401):\quad b\equiv81\pmod {82},
$$
and
$$
(U,q,a)=((-24,7),34,41):\quad b\equiv13\pmod {25}.
$$
Thus the split layer can be studied as determinant-residue strips for fixed
$(U,q,a)$, with $q$ and $a$ later promoted by structural rules.

This is the stronger route to test next: classify these determinant-squareclass
line families, or their residue classes in the free parameter $b$, instead of
only enlarging $(q,a)$ boxes. A scratch primitive-positive census through
$1\le g,h\le2000$ found $150$ misses after the fixed structural stack. The
current bounded split rows with $q\le23$ and $a\le179$ miss only six of those,
and all six are already explained by the same line-family normal form with
slightly larger parameters:
$$
\begin{array}{c|c|c|c|c|c}
T & U & q & a & b & r\\
\hline
(199,1462) & (-24,-7) & 115 & 1 & -293 & 7874\\
(941,1282) & (-40,9) & 149 & 401 & -1 & -7142\\
(1262,1781) & (-24,7) & 34 & 41 & -37 & -37
\end{array}
$$
and their coordinate-swap/sign-symmetric partners. This is evidence against
making the proof target "larger and larger boxes": the parameters $q$ and $b$
should be variables in a line-family or congruence classification, while the
box counts remain guardrails.

The full `pythagorean_layered_parallel_certificate` still keeps the exact
finite-direction divisor cover as a theorem-candidate fallback beyond the
audited frontier, but no target in this sample needs that last fallback.

The scaling closure can now be applied before this finite-direction test. The
helper `parallel_direction_primitive_ray_certificate` reduces a nonzero target
$T$ to its primitive representative $T_0$, applies
`parallel_direction_cover_certificate(T_0, 8)`, and scales the resulting
certificate back to $T$. Axis targets and solved non-primitive exceptional-ray
targets are handled first by the theorem-level helpers. Thus the remaining
finite-direction problem is genuinely a primitive-ray problem: once a primitive
representative is accepted by the divisor-completion cover, every nonzero
multiple of that representative follows automatically.

Executable guardrail:

- `positive_divisors`
- `ParallelDirectionFactorWitness`
- `standard_pythagorean_completion_factors`
- `parallel_direction_factor_witness`
- `parallel_direction_standard_completion_certificate`
- `parallel_direction_standard_completion_cover_certificate`
- `parallel_direction_standard_completion_witness`
- `parallel_direction_standard_completion_cover_witness`
- `parallel_direction_standard_completion_branch`
- `parallel_direction_standard_completion_quadratic_rows`
- `parallel_direction_standard_completion_determinant_rows`
- `parallel_direction_standard_completion_quadratic_row_witness`
- `parallel_direction_standard_completion_strip_intersection_linear_rows`
- `parallel_direction_standard_completion_strip_intersection_linear_row_witness`
- `certificateValid_unitCoordinateFactorFiveParallel`
- `certificateValid_unitCoordinateFactorFourParallel`
- `certificateValid_unitCoordinateOneModFiveParallel`
- `certificateValid_unitCoordinateSevenModTenParallel`
- `certificateValid_unitCoordinateFactorTwentyFiveParallel`
- `certificateValid_unitCoordinateTwentyTwoModTwentyFiveParallel`
- `unit_coordinate_factor_five_parallel_certificate`
- `unit_coordinate_factor_five_parallel_orbit_certificate`
- `unit_coordinate_factor_four_parallel_certificate`
- `unit_coordinate_factor_four_parallel_orbit_certificate`
- `unit_coordinate_factor_twenty_five_parallel_certificate`
- `unit_coordinate_factor_twenty_five_parallel_orbit_certificate`
- `unit_coordinate_twenty_two_mod_twenty_five_parallel_certificate`
- `unit_coordinate_twenty_two_mod_twenty_five_parallel_orbit_certificate`
- `UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES`
- `unit_coordinate_promoted_mod_hundred_certificate`
- `UNIT_COORDINATE_RESIDUAL_ORTHOGONAL_SEED_ROWS`
- `unit_coordinate_residual_orthogonal_seed_certificate`
- `unit_coordinate_one_mod_five_parallel_certificate`
- `unit_coordinate_one_mod_five_parallel_orbit_certificate`
- `unit_coordinate_seven_mod_ten_parallel_certificate`
- `unit_coordinate_seven_mod_ten_parallel_orbit_certificate`
- `unit_coordinate_parallel_factor_residues`
- `unit_coordinate_parallel_factor_orbit_certificate`
- `ray_multiplier`
- `ray_parallel_factor_residues`
- `ray_parallel_factor_certificate`
- `four_three_factor_five_parallel_certificate`
- `PARALLEL_DIRECTION_PROMOTED_345_FACTOR_ROWS`
- `parallel_direction_promoted_345_factor_witness`
- `parallel_direction_promoted_345_factor_certificate`
- `parallel_direction_bounded_factor_cover_certificate`
- `parallel_direction_factor_modulus`
- `parallel_direction_factor_congruence_holds`
- `parallel_direction_primitive_factor_determinant_residue_rows`
- `parallel_direction_primitive_factor_determinant_residue_holds`
- `parallel_direction_primitive_factor_integrality_strip_intersection_linear_rows`
- `parallel_direction_primitive_factor_integrality_strip_intersection_linear_row_witness`
- `parallel_direction_primitive_factor_integrality_strip_intersection_residue_count`
- `parallel_direction_factor_coefficient`
- `parallel_direction_factor_residue_classes`
- `parallel_direction_factor_certificate_residue_classes`
- `parallel_direction_factor_residue_certificate`
- `parallel_direction_factor_integrality_strip_intersection_residue_count`
- `parallel_direction_conjugate_ideal_promoted_345_integrality_strip_intersection_counts`
- `parallel_direction_factor_certificate`
- `parallel_direction_certificate`
- `parallel_direction_cover_certificate`
- `parallel_direction_witness`
- `parallel_direction_cover_witness`
- `ParallelDirectionCoverWitnessCensus`
- `parallel_direction_cover_witness_census`
- `PrimitiveRayParallelDirectionWitness`
- `parallel_direction_primitive_ray_witness`
- `parallel_direction_primitive_ray_certificate`
- `PythagoreanLatticePairWitness`
- `pythagorean_lattice_pair_strip_linear_congruence`
- `pythagorean_lattice_pair_strip_intersection_holds`
- `pythagorean_lattice_pair_strip_intersection_residue_count`
- `pythagorean_orthogonal_lattice_witness`
- `ParallelDirectionSquareclassSplitWitness`
- `ParallelDirectionConjugateIdealWitness`
- `ParallelDirectionConjugateIdealRootCoverCensus`
- `ParallelDirectionConjugateIdealRootShapeCoverCensus`
- `PYTHAGOREAN_LAYERED_ORTHOGONAL_MAX_PARAMETER`
- `PYTHAGOREAN_LAYERED_LATTICE_PAIR_MAX_PARAMETER`
- `PYTHAGOREAN_LAYERED_LATTICE_PAIR_MAX_DETERMINANT`
- `PYTHAGOREAN_LAYERED_STANDARD_COMPLETION_MAX_PARAMETER`
- `PYTHAGOREAN_LAYERED_SPLIT_MAX_SQUARECLASS`
- `PYTHAGOREAN_LAYERED_SPLIT_MAX_FACTOR`
- `PYTHAGOREAN_LAYERED_PARALLEL_MAX_PARAMETER`
- `PYTHAGOREAN_LAYERED_CONJUGATE_ROOT_MAX_COORDINATE`
- `squareclass_decomposition`
- `squarefree_numbers`
- `squarefree_divisors`
- `pythagorean_orthogonal_lattice_cover_certificate`
- `pythagorean_lattice_direction_pairs`
- `pythagorean_lattice_pair_witness`
- `pythagorean_lattice_pair_cover_certificate`
- `parallel_direction_squareclass_split_witness`
- `parallel_direction_squareclass_split_certificate`
- `primitive_pythagorean_direction_gaussian_root`
- `gaussian_root_shape`
- `primitive_pythagorean_root_directions`
- `primitive_pythagorean_root_shape_directions`
- `parallel_direction_squareclass_line_gaussian_numerator`
- `parallel_direction_squareclass_line_split_quotient`
- `parallel_direction_squareclass_line_root_quotient`
- `primitive_pythagorean_direction_conjugate_root_residue`
- `squareclass_beta_integral`
- `beta_square_is_axis_degenerate`
- `parallel_direction_squareclass_beta_split_root`
- `parallel_direction_squareclass_beta_quotient`
- `parallel_direction_squareclass_beta_second_step`
- `parallel_direction_squareclass_beta_line_certificate`
- `parallel_direction_squareclass_beta_target_coefficient`
- `parallel_direction_squareclass_beta_target_certificate`
- `parallel_direction_squareclass_beta_determinant_residue`
- `parallel_direction_squareclass_beta_determinant_target_coefficient`
- `parallel_direction_squareclass_beta_determinant_target_certificate`
- `parallel_direction_squareclass_beta_quadratic_coefficient`
- `parallel_direction_squareclass_beta_quadratic_certificate`
- `parallel_direction_squareclass_conjugate_ideal_split_roots`
- `parallel_direction_squareclass_conjugate_ideal_certificate`
- `parallel_direction_squareclass_conjugate_ideal_witness`
- `parallel_direction_conjugate_ideal_determinant_roots`
- `parallel_direction_conjugate_ideal_split_roots`
- `parallel_direction_conjugate_ideal_certificate`
- `parallel_direction_conjugate_ideal_witness`
- `parallel_direction_conjugate_ideal_cover_certificate`
- `parallel_direction_conjugate_ideal_cover_witness`
- `parallel_direction_conjugate_ideal_root_cover_certificate`
- `parallel_direction_conjugate_ideal_root_cover_witness`
- `parallel_direction_conjugate_ideal_root_shape_cover_certificate`
- `parallel_direction_conjugate_ideal_root_shape_cover_witness`
- `parallel_direction_conjugate_ideal_root_shape_cover_census`
- `parallel_direction_conjugate_ideal_root_cover_census`
- `parallel_direction_squareclass_line_congruence_holds`
- `parallel_direction_squareclass_line_second_step`
- `parallel_direction_squareclass_line_certificate`
- `parallel_direction_squareclass_line_residue_classes`
- `parallel_direction_squareclass_line_residue_certificate`
- `parallel_direction_squareclass_split_cover_witness`
- `parallel_direction_squareclass_split_cover_certificate`
- `pythagorean_layered_structural_certificate`
- `pythagorean_layered_split_certificate`
- `pythagorean_layered_conjugate_ideal_certificate`
- `pythagorean_layered_parallel_certificate`
- `test_parallel_direction_divisor_reduction`
- `test_parallel_direction_standard_completion_family`
- `test_parallel_direction_standard_completion_cover_probe`
- `test_unit_coordinate_factor_five_parallel_family`
- `test_unit_coordinate_factor_four_parallel_family`
- `test_unit_coordinate_one_mod_five_parallel_family`
- `test_unit_coordinate_seven_mod_ten_parallel_family`
- `test_unit_coordinate_factor_twenty_five_parallel_family`
- `test_unit_coordinate_twenty_two_mod_twenty_five_parallel_family`
- `test_unit_coordinate_promoted_mod_hundred_cover`
- `test_unit_coordinate_residual_orthogonal_seed_rows`
- `test_unit_coordinate_parallel_factor_residue_family`
- `test_ray_parallel_factor_residue_family`
- `test_four_three_factor_five_parallel_congruence_family`
- `test_parallel_direction_promoted_345_factor_cover`
- `test_parallel_direction_bounded_factor_cover_probe`
- `test_parallel_direction_factor_residue_classes`
- `test_parallel_direction_candidate_cover_probe`
- `test_parallel_direction_primitive_ray_lift`
- `test_pythagorean_orthogonal_lattice_cover`
- `test_pythagorean_lattice_pair_cover_closes_promoted_residual_tail`
- `test_pythagorean_layered_structural_cover_closes_sample_to_300`
- `test_pythagorean_layered_split_cover_closes_sample_to_1000`
- `test_squareclass_split_extended_frontier_examples`

## Orthogonal Triple Lattices

Every positive Pythagorean triple gives a canonical two-edge lattice family. Let
$$
a^2+b^2=c^2,\qquad a,b,c>0,
$$
and use the legal directions
$$
U=(a,b),\qquad V=(-b,a).
$$
Their determinant is
$$
\det(U,V)=a^2+b^2=c^2.
$$
For a target $T=(g,h)$, Cramer's rule gives
$$
r=\frac{ag+bh}{c^2},\qquad s=\frac{ah-bg}{c^2}.
$$
Thus $T$ is in the lattice $\mathbb ZU+\mathbb ZV$ exactly when
$$
c^2\mid ag+bh
\qquad\text{and}\qquad
c^2\mid ah-bg.
$$
If $r$ and $s$ are both nonzero, then
$$
O\to r(a,b)\to r(a,b)+s(-b,a)=T
$$
is a two-step certificate. If one coefficient is zero and $T\ne O$, the target
is already a scalar multiple of one of the legal directions and is a one-step
target.

This is an infinite exact family indexed by all Pythagorean triples. It is a
composite-determinant counterpart to the prime-residue lines below.
The target-facing cover helper now enumerates these canonical orthogonal pairs
up to a chosen Euclid-parameter bound and returns the first valid lattice
certificate.

Executable guardrail:

- `pythagorean_triple_orthogonal_lattice_certificate`
- `pythagorean_orthogonal_lattice_cover_certificate`
- `test_pythagorean_triple_orthogonal_lattice_family`
- `test_pythagorean_orthogonal_lattice_cover`

## Bounded-Index Pythagorean Lattice Pairs

The orthogonal lattice family is only one special case of the lattice method.
For any two legal Pythagorean directions $U=(u_1,u_2)$ and $V=(v_1,v_2)$ with
nonzero determinant $\Delta=\det(U,V)$, Cramer's rule gives
$$
r=\frac{\det(T,V)}{\Delta},\qquad s=\frac{\det(U,T)}{\Delta}.
$$
Whenever $r,s\in\mathbb Z\setminus\{0\}$, the path
$$
O\to rU\to rU+sV=T
$$
is a valid two-step certificate. Thus one pair $(U,V)$ proves an infinite
congruence lattice, whether $\Delta$ is prime or composite.

The helper `pythagorean_lattice_direction_pairs` enumerates these pairs by
Euclid-parameter bound and optional determinant-index bound, while
`pythagorean_lattice_pair_witness` records the exact pair, determinant, and
Cramer coefficients used for a target. The current guardrail uses parameter
bound $25$ and determinant bound $1435$ as a structural residual layer after
the promoted $3$-$4$-$5$ rows and the orthogonal rows.

Executable guardrail:

- `PythagoreanLatticePairWitness`
- `pythagorean_lattice_direction_pairs`
- `pythagorean_lattice_pair_witness`
- `pythagorean_lattice_pair_cover_certificate`
- `test_pythagorean_lattice_pair_cover_closes_promoted_residual_tail`

## Prime-Determinant Lattice Lines

The lattice criterion has a useful finite-field form. Let $U,V$ be legal
Pythagorean edge vectors with
$$
|\det(U,V)|=p
$$
prime. Then the lattice $\mathbb ZU+\mathbb ZV$ has index $p$ in
$\mathbb Z^2$. Modulo $p$, the vectors $U$ and $V$ are nonzero and linearly
dependent, so the image of this lattice is exactly the residue line spanned by
$U$.

Therefore every target $T$ satisfying
$$
\det(T,U)\equiv0\pmod p
$$
belongs to $\mathbb ZU+\mathbb ZV$. If the Cramer coefficients are both nonzero,
the lattice criterion gives a two-step certificate. If one coefficient is zero,
the target is already a one-step scalar multiple of one of the legal edge
vectors.

The determinant-$7$, determinant-$13$, and determinant-$17$ families below are
instances of this prime-determinant line criterion.

Executable guardrail:

- `is_prime`
- `determinant`
- `same_projective_class_mod`
- `prime_determinant_lattice_certificate`
- `test_prime_determinant_lattice_line_criterion`

## Determinant-Seven Congruence Families

The two 3-4-5 direction pairs
$$
U=(3,4),\quad V=(4,3)
$$
and
$$
U'=(3,-4),\quad V'=(4,-3)
$$
have determinants $-7$ and $7$, respectively.

For the first pair, Cramer's rule gives
$$
r=\frac{4h-3g}{7},\qquad s=\frac{4g-3h}{7}.
$$
These are integers exactly when $g+h\equiv0\pmod7$. Hence every target with
$g+h\equiv0\pmod7$ is either a two-step target by the lattice criterion
($r,s\ne0$) or a one-step target when one of $r,s$ is zero, because then it is a
nonzero multiple of $(3,4)$ or $(4,3)$.

For the second pair,
$$
r=-\frac{3g+4h}{7},\qquad s=\frac{4g+3h}{7},
$$
which are integers exactly when $g-h\equiv0\pmod7$. The same zero-coefficient
split handles the one-step edge cases.

Therefore every nonzero target satisfying
$$
g+h\equiv0\pmod7\qquad\text{or}\qquad g-h\equiv0\pmod7
$$
has distance at most $2$ from the origin.

This is a genuine infinite two-dimensional family, not a bounded search result.
It does not cover the exceptional orbit: none of $(1,0)$, $(2,0)$, $(2,1)$, or
their sign/swap images satisfies either congruence.

Executable guardrail:

- `DETERMINANT_SEVEN_DIRECTION_PAIRS`
- `determinant_seven_lattice_certificate`
- `test_determinant_seven_congruence_families`

## Consecutive-Leg Swap Lattices

The determinant-$7$ family is the first case of a broader exact construction.
Let $(a,a+1,c)$ be a Pythagorean triple with consecutive legs, and set
$$
z=2a+1.
$$
Equivalently,
$$
z^2-2c^2=-1.
$$
Starting from $(z,c)=(7,5)$, the recurrence
$$
z'=3z+4c,\qquad c'=2z+3c
$$
generates further positive solutions and hence the triples
$$
(3,4,5),(20,21,29),(119,120,169),(696,697,985),\ldots.
$$

Use the swapped pair
$$
U=(a,a+1),\qquad V=(a+1,a).
$$
Its determinant is
$$
\det(U,V)=a^2-(a+1)^2=-z.
$$
For a target $T=(g,h)$, Cramer's numerators are
$$
ag-(a+1)h,\qquad ah-(a+1)g.
$$
Modulo $z=2a+1$, we have $a+1\equiv -a$, and $\gcd(a,z)=1$. Therefore both
numerators are divisible by $z$ exactly when
$$
g+h\equiv0\pmod z.
$$
When the resulting Cramer coefficients are nonzero, this gives a two-step
certificate. If one coefficient is zero, the target is already a scalar multiple
of one of the legal directions $U$ or $V$.

The signed swapped pair
$$
U'=(a,-a-1),\qquad V'=(a+1,-a)
$$
has the same determinant up to sign and similarly covers the line
$$
g-h\equiv0\pmod z.
$$

Thus every nonzero target satisfying either congruence has distance at most $2$.
This is an infinite exact family of lattices; it is not limited to prime
determinants.

Executable guardrail:

- `consecutive_leg_pythagorean_triple`
- `consecutive_leg_swap_lattice_certificate`
- `test_consecutive_leg_swap_lattice_family`

## Determinant-Thirteen Congruence Families

The same lattice criterion gives four more congruence classes using 3-4-5 and
8-15-17 directions:
$$
\begin{array}{c|c|c}
U & V & \text{covered congruence}\\
\hline
(3,4) & (8,15) & g\equiv 4h\pmod {13}\\
(3,-4) & (8,-15) & g\equiv -4h\pmod {13}\\
(4,3) & (15,8) & g\equiv -3h\pmod {13}\\
(4,-3) & (15,-8) & g\equiv 3h\pmod {13}
\end{array}
$$
Each pair has determinant $\pm13$. Since $13$ is prime, the lattice generated
by each pair is exactly the residue line spanned by either basis vector modulo
$13$. If the corresponding Cramer coefficients are both nonzero, the lattice
criterion gives a two-step certificate; if one coefficient is zero, the target
is a one-step scalar multiple of one of the displayed legal edge vectors.

Therefore every nonzero target satisfying
$$
g\equiv \pm3h\pmod {13}
\qquad\text{or}\qquad
g\equiv \pm4h\pmod {13}
$$
has distance at most $2$ from the origin. These congruence classes also avoid
the conjectured exceptional orbit.

Executable guardrail:

- `DETERMINANT_THIRTEEN_DIRECTION_PAIRS`
- `determinant_thirteen_lattice_certificate`
- `test_determinant_thirteen_congruence_families`

## Determinant-Seventeen Congruence Families

The same method gives four further classes from the pairs
$$
\begin{array}{c|c|c}
U & V & \text{covered congruence}\\
\hline
(3,4) & (20,21) & g\equiv 5h\pmod {17}\\
(3,-4) & (20,-21) & g\equiv -5h\pmod {17}\\
(4,3) & (21,20) & g\equiv 7h\pmod {17}\\
(4,-3) & (21,-20) & g\equiv -7h\pmod {17}
\end{array}
$$
Each displayed pair has determinant $\pm17$. As in the determinant-$13$ case,
each lattice is exactly the residue line spanned by the first vector modulo
$17$. Nonzero Cramer coefficients give a two-step certificate; a zero
coefficient means the target is a one-step scalar multiple of one of the
displayed legal edge vectors.

Therefore every nonzero target satisfying
$$
g\equiv \pm5h\pmod {17}
\qquad\text{or}\qquad
g\equiv \pm7h\pmod {17}
$$
has distance at most $2$ from the origin. These classes avoid the conjectured
exceptional orbit.

Executable guardrail:

- `DETERMINANT_SEVENTEEN_DIRECTION_PAIRS`
- `determinant_seventeen_lattice_certificate`
- `test_determinant_seventeen_congruence_families`

## Additional Small-Prime Lattice Lines

The same prime-determinant criterion gives further exact congruence families.
The following finite table is now encoded:
$$
\begin{array}{c|c|c}
p & U,V & \text{covered congruence}\\
\hline
23 & (3,-4),(28,-45) & g\equiv 5h\pmod {23}\\
23 & (3,4),(28,45) & g\equiv -5h\pmod {23}\\
23 & (4,3),(45,28) & g\equiv 9h\pmod {23}\\
23 & (4,-3),(45,-28) & g\equiv -9h\pmod {23}\\
31 & (5,12),(12,35) & g\equiv 3h\pmod {31}\\
31 & (5,-12),(12,-35) & g\equiv -3h\pmod {31}\\
31 & (12,-5),(35,-12) & g\equiv 10h\pmod {31}\\
31 & (12,5),(35,12) & g\equiv -10h\pmod {31}\\
37 & (3,4),(88,105) & g\equiv 10h\pmod {37}\\
37 & (3,-4),(88,-105) & g\equiv -10h\pmod {37}\\
37 & (4,-3),(105,-88) & g\equiv 11h\pmod {37}\\
37 & (4,3),(105,88) & g\equiv -11h\pmod {37}\\
41 & (20,-21),(21,-20) & g\equiv h\pmod {41}\\
41 & (20,21),(21,20) & g\equiv -h\pmod {41}\\
43 & (3,-4),(104,-153) & g\equiv 10h\pmod {43}\\
43 & (4,-3),(153,-104) & g\equiv 13h\pmod {43}\\
43 & (24,-7),(35,-12) & g\equiv 15h\pmod {43}\\
43 & (7,24),(12,35) & g\equiv 20h\pmod {43}\\
43 & (7,-24),(12,-35) & g\equiv -20h\pmod {43}\\
43 & (24,7),(35,12) & g\equiv -15h\pmod {43}\\
43 & (4,3),(153,104) & g\equiv -13h\pmod {43}\\
43 & (3,4),(104,153) & g\equiv -10h\pmod {43}\\
47 & (15,-8),(56,-33) & g\equiv 4h\pmod {47}\\
47 & (12,-5),(77,-36) & g\equiv 7h\pmod {47}\\
47 & (3,-4),(140,-171) & g\equiv 11h\pmod {47}\\
47 & (8,-15),(33,-56) & g\equiv 12h\pmod {47}\\
47 & (4,3),(171,140) & g\equiv 17h\pmod {47}\\
47 & (5,12),(36,77) & g\equiv 20h\pmod {47}\\
47 & (5,-12),(36,-77) & g\equiv -20h\pmod {47}\\
47 & (4,-3),(171,-140) & g\equiv -17h\pmod {47}\\
47 & (8,15),(33,56) & g\equiv -12h\pmod {47}\\
47 & (3,4),(140,171) & g\equiv -11h\pmod {47}\\
47 & (12,5),(77,36) & g\equiv -7h\pmod {47}\\
47 & (15,8),(56,33) & g\equiv -4h\pmod {47}\\
53 & (3,4),(160,231) & g\equiv 14h\pmod {53}\\
53 & (4,3),(231,160) & g\equiv 19h\pmod {53}\\
53 & (4,-3),(231,-160) & g\equiv -19h\pmod {53}\\
53 & (3,-4),(160,-231) & g\equiv -14h\pmod {53}\\
67 & (3,-4),(280,-351) & g\equiv 16h\pmod {67}\\
67 & (4,-3),(351,-280) & g\equiv 21h\pmod {67}\\
67 & (4,3),(351,280) & g\equiv -21h\pmod {67}\\
67 & (3,4),(280,351) & g\equiv -16h\pmod {67}\\
73 & (9,40),(16,63) & g\equiv 13h\pmod {73}\\
73 & (12,5),(187,84) & g\equiv 17h\pmod {73}\\
73 & (40,-9),(63,-16) & g\equiv 28h\pmod {73}\\
73 & (5,-12),(84,-187) & g\equiv 30h\pmod {73}\\
73 & (5,12),(84,187) & g\equiv -30h\pmod {73}\\
73 & (40,9),(63,16) & g\equiv -28h\pmod {73}\\
73 & (12,-5),(187,-84) & g\equiv -17h\pmod {73}\\
73 & (9,-40),(16,-63) & g\equiv -13h\pmod {73}\\
83 & (28,45),(33,56) & g\equiv 8h\pmod {83}\\
83 & (12,5),(247,96) & g\equiv 19h\pmod {83}\\
83 & (45,-28),(56,-33) & g\equiv 31h\pmod {83}\\
83 & (5,12),(96,247) & g\equiv 35h\pmod {83}\\
83 & (5,-12),(96,-247) & g\equiv -35h\pmod {83}\\
83 & (45,28),(56,33) & g\equiv -31h\pmod {83}\\
83 & (12,-5),(247,-96) & g\equiv -19h\pmod {83}\\
83 & (28,-45),(33,-56) & g\equiv -8h\pmod {83}\\
89 & (15,8),(208,105) & g\equiv 13h\pmod {89}\\
89 & (8,-15),(105,-208) & g\equiv 41h\pmod {89}\\
89 & (8,15),(105,208) & g\equiv -41h\pmod {89}\\
89 & (15,-8),(208,-105) & g\equiv -13h\pmod {89}\\
107 & (7,-24),(60,-221) & g\equiv 22h\pmod {107}\\
107 & (24,7),(221,60) & g\equiv 34h\pmod {107}\\
107 & (24,-7),(221,-60) & g\equiv -34h\pmod {107}\\
107 & (7,24),(60,221) & g\equiv -22h\pmod {107}\\
109 & (5,-12),(168,-425) & g\equiv 45h\pmod {109}\\
109 & (12,5),(425,168) & g\equiv 46h\pmod {109}\\
109 & (12,-5),(425,-168) & g\equiv -46h\pmod {109}\\
109 & (5,12),(168,425) & g\equiv -45h\pmod {109}\\
149 & (15,-8),(572,-315) & g\equiv 54h\pmod {149}\\
149 & (8,-15),(315,-572) & g\equiv 69h\pmod {149}\\
149 & (8,15),(315,572) & g\equiv -69h\pmod {149}\\
149 & (15,8),(572,315) & g\equiv -54h\pmod {149}\\
157 & (20,-21),(297,-304) & g\equiv 14h\pmod {157}\\
157 & (24,-7),(475,-132) & g\equiv 19h\pmod {157}\\
157 & (7,24),(132,475) & g\equiv 33h\pmod {157}\\
157 & (21,20),(304,297) & g\equiv 56h\pmod {157}\\
157 & (84,-13),(143,-24) & g\equiv 66h\pmod {157}\\
157 & (13,-84),(24,-143) & g\equiv 69h\pmod {157}\\
157 & (13,84),(24,143) & g\equiv -69h\pmod {157}\\
157 & (84,13),(143,24) & g\equiv -66h\pmod {157}\\
157 & (21,-20),(304,-297) & g\equiv -56h\pmod {157}\\
157 & (7,-24),(132,-475) & g\equiv -33h\pmod {157}\\
157 & (24,7),(475,132) & g\equiv -19h\pmod {157}\\
157 & (20,21),(297,304) & g\equiv -14h\pmod {157}\\
173 & (48,-55),(133,-156) & g\equiv 18h\pmod {173}\\
173 & (40,-9),(357,-76) & g\equiv 34h\pmod {173}\\
173 & (55,48),(156,133) & g\equiv 48h\pmod {173}\\
173 & (9,-40),(76,-357) & g\equiv 56h\pmod {173}\\
173 & (9,40),(76,357) & g\equiv -56h\pmod {173}\\
173 & (55,-48),(156,-133) & g\equiv -48h\pmod {173}\\
173 & (40,9),(357,76) & g\equiv -34h\pmod {173}\\
173 & (48,55),(133,156) & g\equiv -18h\pmod {173}\\
179 & (35,-12),(408,-145) & g\equiv 12h\pmod {179}\\
179 & (12,-35),(145,-408) & g\equiv 15h\pmod {179}\\
179 & (12,35),(145,408) & g\equiv -15h\pmod {179}\\
179 & (35,12),(408,145) & g\equiv -12h\pmod {179}\\
191 & (35,-12),(468,-155) & g\equiv 13h\pmod {191}\\
191 & (12,35),(155,468) & g\equiv 44h\pmod {191}\\
191 & (21,20),(460,429) & g\equiv 87h\pmod {191}\\
191 & (20,-21),(429,-460) & g\equiv 90h\pmod {191}\\
191 & (20,21),(429,460) & g\equiv -90h\pmod {191}\\
191 & (21,-20),(460,-429) & g\equiv -87h\pmod {191}\\
191 & (12,-35),(155,-468) & g\equiv -44h\pmod {191}\\
191 & (35,12),(468,155) & g\equiv -13h\pmod {191}\\
193 & (117,44),(140,51) & g\equiv 86h\pmod {193}\\
193 & (44,-117),(51,-140) & g\equiv 92h\pmod {193}\\
193 & (44,117),(51,140) & g\equiv -92h\pmod {193}\\
193 & (117,-44),(140,-51) & g\equiv -86h\pmod {193}\\
211 & (15,112),(28,195) & g\equiv 51h\pmod {211}\\
211 & (112,-15),(195,-28) & g\equiv 91h\pmod {211}\\
211 & (112,15),(195,28) & g\equiv -91h\pmod {211}\\
211 & (15,-112),(28,-195) & g\equiv -51h\pmod {211}\\
239 & (119,-120),(120,-119) & g\equiv h\pmod {239}\\
239 & (119,120),(120,119) & g\equiv -h\pmod {239}\\
241 & (15,-112),(32,-255) & g\equiv 101h\pmod {241}\\
241 & (112,-15),(255,-32) & g\equiv 105h\pmod {241}\\
241 & (112,15),(255,32) & g\equiv -105h\pmod {241}\\
241 & (15,112),(32,255) & g\equiv -101h\pmod {241}\\
251 & (60,91),(161,240) & g\equiv 31h\pmod {251}\\
251 & (91,60),(240,161) & g\equiv 81h\pmod {251}\\
251 & (91,-60),(240,-161) & g\equiv -81h\pmod {251}\\
251 & (60,-91),(161,-240) & g\equiv -31h\pmod {251}\\
269 & (72,-65),(275,-252) & g\equiv 32h\pmod {269}\\
269 & (65,72),(252,275) & g\equiv 42h\pmod {269}\\
269 & (65,-72),(252,-275) & g\equiv -42h\pmod {269}\\
269 & (72,65),(275,252) & g\equiv -32h\pmod {269}
\end{array}
$$
Each displayed pair has determinant $\pm p$. Thus every nonzero target on one
of these residue lines has distance at most $2$, except that the zero
coefficient cases are already one-step scalar multiples of one of the displayed
legal directions.

These are theorem-level infinite families because the determinant and residue
conditions are exact. They are not a finite coverage claim for all remaining
targets.

Executable guardrail:

- `SMALL_PRIME_DETERMINANT_DIRECTION_PAIRS`
- `small_prime_lattice_certificate`
- `test_additional_small_prime_congruence_families`

The finite audit tables below are cumulative explicit fallback tables. Later
infinite families, such as newly added prime-determinant rows, may make some
earlier fallback entries redundant; the entries are retained because each is an
independently checked two-step midpoint identity.

## Exact Finite Audit In The Box $|g|,|h|\le20$

The theorem-level families above already cover most small targets. An exact
finite audit now covers the whole box
$$
|g|,|h|\le20
$$
apart from the known distance-three orbit and the origin. One-step targets are
handled directly by the graph predicate. The remaining non-edge targets are
covered by these exact constructors:

- the axis-orbit certificate;
- the determinant-$7$, determinant-$13$, determinant-$17$, and small-prime
  lattice families;
- the even and explicit-base families on the $(2,1)$ ray;
- the residual midpoint table below, transported by sign changes and coordinate
  swap.

The residual table records only one representative per sign/swap orbit:
$$
\begin{array}{c|c}
T & P\\
\hline
(10,5) & (-20,21)\\
(13,7) & (-351,280)\\
(13,10) & (-195,400)\\
(16,3) & (-624,315)\\
(16,15) & (-704,840)\\
(17,5) & (-400,561)\\
(17,13) & (-844,633)\\
(20,3) & (-864,990)\\
(20,9) & (-684,912)
\end{array}
$$
For each displayed row, both $OP$ and $PT$ are legal Pythagorean edges; applying
the graph automorphisms gives every signed/swapped residual case. This is a
finite exact verification, not an extrapolated bounded-search claim.

Executable guardrail:

- `BOX_TWENTY_RESIDUAL_CERTIFICATES`
- `box_twenty_residual_certificate`
- `box_twenty_audit_certificate`
- `test_box_twenty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le30$

The same exact audit has been extended to the larger box
$$
|g|,|h|\le30.
$$
The audit again excludes only the origin and the known distance-three orbit,
and treats one-step targets by the graph predicate. The exact constructors used
before handle most of the enlarged box. Beyond the box-$20$ residual rows, the
following additional representatives complete the sign/swap residual cases:
$$
\begin{array}{c|c}
T & P\\
\hline
(22,11) & (-110,96)\\
(23,3) & (-805,348)\\
(23,11) & (-180,-385)\\
(25,1) & (-875,-300)\\
(25,14) & (-95,-168)\\
(26,7) & (-754,672)\\
(26,14) & (-702,560)\\
(26,20) & (-825,440)\\
(26,21) & (-330,288)\\
(26,25) & (-532,-855)\\
(28,3) & (-620,-861)\\
(28,17) & (-452,339)\\
(28,27) & (-732,549)\\
(29,2) & (-195,-28)\\
(30,13) & (-936,-75)
\end{array}
$$
Each row is an explicit two-step midpoint identity; sign changes and coordinate
swap cover the whole residual orbit. This remains a finite exact verification,
not evidence for a pattern outside the audited box.

Executable guardrail:

- `BOX_THIRTY_RESIDUAL_CERTIFICATES`
- `box_thirty_residual_certificate`
- `box_thirty_audit_certificate`
- `test_box_thirty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le40$

The finite-audit layer now reaches
$$
|g|,|h|\le40.
$$
The audit has the same scope as the earlier boxes: it excludes only the origin
and the known distance-three orbit, treats one-step targets by the graph
predicate, and uses exact certificate constructors plus explicit residual
midpoint rows. Beyond the box-$30$ residual rows, the additional representatives
are:
$$
\begin{array}{c|c}
T & P\\
\hline
(32,6) & (-1248,630)\\
(32,30) & (-1860,1395)\\
(33,17) & (-264,77)\\
(34,10) & (-800,1122)\\
(34,26) & (-1688,1266)\\
(35,2) & (-1645,492)\\
(35,4) & (-1197,304)\\
(35,8) & (-1485,1148)\\
(35,26) & (-520,-546)\\
(35,33) & (-1325,-1092)\\
(37,3) & (-1628,-885)\\
(37,10) & (-299,-180)\\
(37,25) & (-572,-555)\\
(37,27) & (-1924,-693)\\
(38,1) & (-42,40)\\
(38,15) & (-1798,120)\\
(38,19) & (-342,280)\\
(39,21) & (-1573,-264)\\
(39,23) & (-1404,-53)\\
(39,30) & (-585,1200)\\
(40,6) & (-1728,1980)\\
(40,18) & (-1368,1824)
\end{array}
$$
Every row is checked as a concrete two-step certificate, and sign/swap
transport supplies the symmetric residual cases. No claim is made beyond the
finite box.

Executable guardrail:

- `BOX_FORTY_RESIDUAL_CERTIFICATES`
- `box_forty_residual_certificate`
- `box_forty_audit_certificate`
- `test_box_forty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le50$

The finite-audit layer now reaches
$$
|g|,|h|\le50.
$$
The audit uses the same rule as the smaller boxes: remove the origin and the
known distance-three orbit, accept one-step targets by the graph predicate, then
use exact certificate constructors plus residual midpoint rows. Beyond the
box-$40$ residual rows, the new representatives are:
$$
\begin{array}{c|c}
T & P\\
\hline
(41,9) & (-1980,189)\\
(41,12) & (-4560,-4788)\\
(41,14) & (-1240,1722)\\
(43,7) & (-2204,3003)\\
(43,9) & (-4104,3705)\\
(43,30) & (-2024,3990)\\
(44,17) & (-4092,-256)\\
(44,27) & (-4240,4452)\\
(44,29) & (-3036,-1027)\\
(44,31) & (-4180,399)\\
(45,29) & (-2835,-972)\\
(46,6) & (-4320,-2106)\\
(46,22) & (-2024,1518)\\
(46,29) & (-2550,1976)\\
(47,8) & (-4386,752)\\
(47,10) & (-3297,-3140)\\
(47,13) & (-3081,4108)\\
(47,21) & (-4453,-804)\\
(47,22) & (-1929,2572)\\
(47,25) & (-748,-1035)\\
(47,29) & (-3553,-396)\\
(47,42) & (-3080,-294)\\
(47,43) & (-2748,-1145)\\
(48,9) & (-4488,-4941)\\
(48,37) & (-4488,-665)\\
(48,45) & (-4320,-279)\\
(49,2) & (-575,-48)\\
(49,5) & (-3003,-4900)\\
(49,29) & (-2915,-2544)\\
(49,36) & (-3605,1236)\\
(49,45) & (-1095,2628)\\
(50,2) & (-3150,800)\\
(50,17) & (-1480,969)\\
(50,23) & (-2860,1575)\\
(50,25) & (-3096,553)\\
(50,28) & (-3975,1408)
\end{array}
$$
Each row is an explicit two-step midpoint identity. The test checks the rows,
their sign/swap orbits, and every target in the finite box. No claim is made
beyond the finite box.

Executable guardrail:

- `BOX_FIFTY_RESIDUAL_CERTIFICATES`
- `box_fifty_residual_certificate`
- `box_fifty_audit_certificate`
- `test_box_fifty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le60$

The finite-audit layer now reaches
$$
|g|,|h|\le60.
$$
The same finite rule is used: the origin and known distance-three orbit are
excluded, one-step targets are accepted by the graph predicate, and every
remaining target is handled by exact constructors or residual midpoint rows.
Beyond the box-$50$ residual rows, the new representatives are:
$$
\begin{array}{c|c}
T & P\\
\hline
(51,11) & (-12,-5)\\
(51,13) & (-9,-12)\\
(51,15) & (-9,40)\\
(51,20) & (6,-8)\\
(51,38) & (-165,-52)\\
(51,39) & (-36,-77)\\
(52,14) & (12,5)\\
(52,21) & (12,-9)\\
(52,28) & (24,7)\\
(52,40) & (-8,15)\\
(52,42) & (-20,21)\\
(52,43) & (-12,-5)\\
(52,50) & (-20,-15)\\
(53,2) & (5,-12)\\
(53,33) & (-55,-48)\\
(53,47) & (-7735,-4968)\\
(53,50) & (-51,-1300)\\
(55,26) & (-65,-156)\\
(55,46) & (-200,-1242)\\
(56,6) & (20,-21)\\
(56,17) & (12,-16)\\
(56,34) & (24,10)\\
(56,37) & (-40,9)\\
(56,47) & (-40,75)\\
(56,54) & (-8,6)\\
(57,17) & (-159,212)\\
(57,44) & (12,-16)\\
(57,49) & (-3,4)\\
(57,56) & (18,-24)\\
(58,4) & (-5,-12)\\
(58,13) & (406,-792)\\
(59,13) & (-4,-3)\\
(59,33) & (35,-12)\\
(59,43) & (-645,-860)\\
(59,49) & (-2385,-1484)\\
(59,51) & (4,3)\\
(59,58) & (35,-12)\\
(60,9) & (12,-5)\\
(60,13) & (-36,-15)\\
(60,26) & (-12,5)\\
(60,27) & (12,-9)
\end{array}
$$
Every displayed row is validated as a concrete two-step certificate, and
sign/swap transport covers its full orbit. The audit remains a finite statement
only.

Executable guardrail:

- `BOX_SIXTY_RESIDUAL_CERTIFICATES`
- `box_sixty_residual_certificate`
- `box_sixty_audit_certificate`
- `test_box_sixty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le70$

The finite-audit layer now reaches
$$
|g|,|h|\le70.
$$
The same exact finite rule is used: discard the origin and the known
distance-three orbit, accept one-step targets separately, and require every
remaining target to be certified by an exact constructor or an explicit
residual midpoint row. Beyond the box-$60$ residual rows, the new
representatives are:
$$
\begin{array}{c|c}
T & P\\
\hline
(61,7) & (861,-1148)\\
(61,11) & (21,20)\\
(61,22) & (21,-20)\\
(61,39) & (45,-24)\\
(61,46) & (-56,90)\\
(61,48) & (-16,12)\\
(61,57) & (-308,-435)\\
(62,19) & (20,-21)\\
(62,33) & (-110,-96)\\
(62,37) & (18,-80)\\
(62,45) & (-10,24)\\
(62,49) & (-210,-176)\\
(63,11) & (-105,-88)\\
(63,23) & (-189,-252)\\
(64,12) & (20,-21)\\
(64,19) & (24,10)\\
(64,39) & (8,6)\\
(64,60) & (4,-3)\\
(65,8) & (-75,-40)\\
(65,11) & (-75,-40)\\
(65,27) & (-12,-9)\\
(65,35) & (-195,104)\\
(65,46) & (-40,-42)\\
(65,50) & (9,-40)\\
(66,34) & (-222,-296)\\
(66,47) & (24,7)\\
(67,9) & (-5,-12)\\
(67,35) & (7,24)\\
(67,49) & (7,24)\\
(67,65) & (-308,-435)\\
(68,7) & (20,21)\\
(68,11) & (-52,-39)\\
(68,15) & (20,-21)\\
(68,20) & (-100,-75)\\
(68,21) & (20,-15)\\
(68,39) & (8,-6)\\
(68,52) & (-51,-68)\\
(69,9) & (-36,-27)\\
(69,11) & (-48,55)\\
(69,32) & (-6,-8)\\
(69,33) & (9,-12)\\
(69,35) & (21,-20)\\
(69,59) & (36,15)\\
(70,1) & (10,-24)\\
(70,4) & (-35,-84)\\
(70,8) & (7,24)\\
(70,16) & (-35,-84)\\
(70,23) & (840,-1081)\\
(70,47) & (-714,152)\\
(70,52) & (-5,12)\\
(70,66) & (-40,-30)
\end{array}
$$
Every displayed row is validated directly as a concrete two-step certificate,
then sign/swap transport supplies the symmetric residual cases. The audit is
finite and exact; it is not an asymptotic proof.

Executable guardrail:

- `BOX_SEVENTY_RESIDUAL_CERTIFICATES`
- `box_seventy_residual_certificate`
- `box_seventy_audit_certificate`
- `test_box_seventy_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le80$

The finite-audit layer now reaches
$$
|g|,|h|\le80.
$$
This audit uses the exact constructors already recorded above, the
unit-coordinate finite audit where applicable, the target-facing half-leg and
affine strip recognizers with fixed finite parameter ranges, and the box-$70$
fallback table. The remaining sign/swap representatives are:
$$
\begin{array}{c|c}
T & P\\
\hline
(71,14) & (-49,-168)\\
(71,25) & (15,-8)\\
(71,46) & (39,-80)\\
(71,61) & (9815,-10872)\\
(72,25) & (24,45)\\
(72,35) & (-24,7)\\
(73,5) & (48,-55)\\
(73,12) & (-32,-24)\\
(73,34) & (-488,-366)\\
(73,55) & (52,-165)\\
(74,6) & (-30,-72)\\
(74,19) & (-36,-77)\\
(74,20) & (42,-40)\\
(74,41) & (-70,24)\\
(74,50) & (24,-70)\\
(74,65) & (-2368,345)\\
(74,69) & (-36,-27)\\
(75,3) & (15,-8)\\
(75,28) & (-15,-20)\\
(75,42) & (35,12)\\
(75,46) & (-45,24)\\
(76,2) & (-8,15)\\
(76,3) & (36,-27)\\
(76,30) & (-24,-45)\\
(76,53) & (12,5)\\
(76,61) & (-12,-5)\\
(77,15) & (-28,-21)\\
(77,19) & (-595,204)\\
(77,24) & (35,-120)\\
(77,27) & (-35,12)\\
(77,53) & (5,-12)\\
(77,59) & (-7,24)\\
(77,64) & (-3,4)\\
(78,46) & (6,-8)\\
(78,60) & (30,40)\\
(78,63) & (-42,-56)\\
(78,73) & (6,8)\\
(79,6) & (7,-24)\\
(79,31) & (-956,-717)\\
(79,45) & (7,24)\\
(79,52) & (-50,-120)\\
(79,63) & (275,-252)\\
(80,12) & (32,-24)\\
(80,15) & (8,-6)\\
(80,41) & (-40,-9)\\
(80,63) & (32,-126)\\
(80,75) & (-32,60)\\
(80,79) & (32,24)
\end{array}
$$
Every row is validated directly as a two-step midpoint identity, and the test
enumerates the full finite box while keeping one-step targets and the known
distance-three orbit separate. No statement beyond this finite box is claimed.

Executable guardrail:

- `BOX_EIGHTY_RESIDUAL_CERTIFICATES`
- `box_eighty_residual_certificate`
- `box_eighty_audit_certificate`
- `test_box_eighty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le90$

The finite-audit layer now reaches
$$
|g|,|h|\le90.
$$
This audit reuses the box-$80$ audit and then applies the exact axis, lattice,
ray, unit-coordinate, diagonal, half-leg strip, affine strip, and Theorem 3
quadratic-strip constructors to the new outer ring. The remaining sign/swap
representatives are:
$$
\begin{array}{c|c}
T & P\\
\hline
(81,19) & (9,40)\\
(81,47) & (60,-25)\\
(82,11) & (12,35)\\
(82,24) & (5,-12)\\
(82,59) & (12,35)\\
(83,18) & (-216,-162)\\
(83,51) & (216,-405)\\
(84,9) & (36,-27)\\
(84,25) & (12,-5)\\
(84,51) & (8,-6)\\
(84,55) & (24,10)\\
(84,79) & (36,15)\\
(84,81) & (4,-3)\\
(85,9) & (-175,-60)\\
(85,19) & (40,-9)\\
(85,26) & (-1595,-1092)\\
(85,32) & (15,8)\\
(85,46) & (-155,-372)\\
(85,65) & (-812,-3315)\\
(85,74) & (-195,-28)\\
(86,13) & (20,-99)\\
(86,14) & (456,-1330)\\
(86,18) & (14,48)\\
(86,60) & (119,-120)\\
(86,69) & (14,48)\\
(86,81) & (10,24)\\
(87,34) & (15,-20)\\
(87,35) & (12,-5)\\
(87,50) & (15,20)\\
(87,86) & (63,16)\\
(88,7) & (120,-119)\\
(88,34) & (-8,-6)\\
(88,54) & (8,-6)\\
(88,58) & (24,10)\\
(88,62) & (12,5)\\
(88,65) & (40,-75)\\
(89,24) & (-16,-12)\\
(89,25) & (5,12)\\
(89,29) & (-11692,8769)\\
(89,49) & (33,-56)\\
(89,64) & (-7,24)\\
(89,78) & (-455,528)\\
(89,87) & (-76,-57)\\
(90,7) & (-120,119)\\
(90,47) & (30,-16)\\
(90,58) & (-54,-72)
\end{array}
$$
Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is a finite exact statement only.

Executable guardrail:

- `BOX_NINETY_RESIDUAL_CERTIFICATES`
- `box_ninety_residual_certificate`
- `box_ninety_audit_certificate`
- `test_box_ninety_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le100$

The finite-audit layer now reaches
$$
|g|,|h|\le100.
$$
This audit reuses the box-$90$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are:
$$
\begin{array}{c|c}
T & P\\
\hline
(91,10) & (4371,3220)\\
(91,16) & (-455,-504)\\
(91,17) & (-8789,-3948)\\
(91,24) & (-3584,2688)\\
(91,27) & (575,-1260)\\
(91,48) & (-259,888)\\
(91,53) & (735,1088)\\
(91,71) & (3003,8096)\\
(92,12) & (308,75)\\
(92,44) & (12,5)\\
(92,58) & (-1404,-2747)\\
(92,63) & (56,90)\\
(92,73) & (-1060,1113)\\
(93,92) & (-1767,-900)\\
(94,7) & (376,-2193)\\
(94,20) & (-221,-60)\\
(94,26) & (6256,-8190)\\
(94,42) & (-144,858)\\
(94,50) & (1590,2120)\\
(94,58) & (366,-488)\\
(94,71) & (2632,1551)\\
(94,75) & (3572,-765)\\
(94,85) & (1576,-2955)\\
(94,86) & (5590,2376)\\
(95,26) & (-2040,-1222)\\
(95,34) & (-1105,1224)\\
(95,44) & (63,-16)\\
(95,63) & (-180,-189)\\
(95,71) & (-325,-780)\\
(95,72) & (-5665,-3792)\\
(95,91) & (35,-84)\\
(95,93) & (-3820,2865)\\
(96,18) & (12,5)\\
(96,74) & (1284,-535)\\
(96,83) & (240,100)\\
(96,90) & (-2280,-117)\\
(97,32) & (5152,-2664)\\
(97,87) & (7337,1716)\\
(97,95) & (949,2580)\\
(98,4) & (-133,-156)\\
(98,10) & (-462,-1040)\\
(98,29) & (230,504)\\
(98,58) & (5928,5146)\\
(98,87) & (-4214,552)\\
(98,90) & (-126,120)\\
(99,5) & (-189,180)\\
(99,10) & (-2565,2100)\\
(99,25) & (1659,-2900)\\
(99,31) & (-4620,-5029)\\
(99,51) & (-265,636)\\
(99,68) & (714,2552)\\
(99,73) & (-2484,-2387)\\
(100,4) & (-4040,7575)\\
(100,15) & (2160,4959)\\
(100,34) & (960,-9191)\\
(100,56) & (3235,-7764)\\
(100,57) & (56,90)\\
(100,67) & (-140,-171)
\end{array}
$$
Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_ONE_HUNDRED_RESIDUAL_CERTIFICATES`
- `box_one_hundred_residual_certificate`
- `box_one_hundred_audit_certificate`
- `test_box_one_hundred_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le110$

The finite-audit layer now reaches
$$
|g|,|h|\le110.
$$
This audit reuses the box-$100$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are:
$$
\begin{array}{c|c}
T & P\\
\hline
(101,6) & (296,222)\\
(101,15) & (156,-117)\\
(101,16) & (2390,5736)\\
(101,71) & (22940,-30381)\\
(101,98) & (-760,-522)\\
(101,99) & (4313,-40860)\\
(102,13) & (126,-32)\\
(102,22) & (2016,270)\\
(102,26) & (-41706,39720)\\
(102,37) & (18,24)\\
(102,40) & (29205,-5900)\\
(102,77) & (-654,-35640)\\
(102,78) & (936,1190)\\
(103,15) & (-1517,-156)\\
(103,18) & (40,-198)\\
(103,28) & (13312,-2784)\\
(103,34) & (8008,-10506)\\
(103,50) & (2079,2600)\\
(103,67) & (-22448,30135)\\
(103,71) & (280,-165)\\
(103,91) & (1720,-1449)\\
(104,42) & (-5880,7182)\\
(104,47) & (440,99)\\
(104,49) & (224,168)\\
(104,80) & (159,212)\\
(104,84) & (56,-105)\\
(104,86) & (17292,-12805)\\
(104,93) & (4888,-495)\\
(105,12) & (-19530,15456)\\
(105,24) & (-1200,-900)\\
(105,31) & (11025,-2800)\\
(105,37) & (22680,-43127)\\
(105,76) & (-23625,1820)\\
(105,78) & (385,180)\\
(105,99) & (10480,-15561)\\
(106,4) & (4528,-3396)\\
(106,51) & (3060,10179)\\
(106,66) & (1602,2136)\\
(106,67) & (126,-32)\\
(106,75) & (5452,1155)\\
(106,77) & (-1680,1925)\\
(106,94) & (-46854,-10472)\\
(106,100) & (-3815,5328)\\
(107,13) & (10728,9685)\\
(107,21) & (-4465,-3408)\\
(107,24) & (1440,-420)\\
(107,55) & (72,-65)\\
(107,83) & (-2725,34008)\\
(107,88) & (315,-572)\\
(107,102) & (-7725,14976)\\
(107,106) & (8352,-986)\\
(108,19) & (684,-1463)\\
(108,61) & (-720,1540)\\
(108,65) & (38040,-8559)\\
(108,83) & (-21120,-49022)\\
(109,12) & (-35,120)\\
(109,40) & (-18915,14308)\\
(109,47) & (1305,-1900)\\
(109,51) & (-8151,-1368)\\
(109,90) & (-91,-60)\\
(109,92) & (159,212)\\
(110,52) & (-17490,-28424)\\
(110,53) & (-12084,-7987)\\
(110,81) & (1978,-1320)\\
(110,92) & (33005,-11316)
\end{array}
$$
Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_ONE_TEN_RESIDUAL_CERTIFICATES`
- `box_one_ten_residual_certificate`
- `box_one_ten_audit_certificate`
- `test_box_one_ten_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le120$

The finite-audit layer now reaches
$$
|g|,|h|\le120.
$$
This audit reuses the box-$110$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are:
$$
\begin{array}{c|c}
T & P\\
\hline
(111,9) & (1420,7029)\\
(111,30) & (-8529,11372)\\
(111,61) & (-2520,3569)\\
(111,65) & (-2760,-4807)\\
(111,75) & (9615,-5128)\\
(111,103) & (240,275)\\
(112,9) & (1232,-399)\\
(112,12) & (567,540)\\
(112,34) & (1168,-876)\\
(112,51) & (140,147)\\
(112,55) & (21112,-13920)\\
(112,68) & (-156,-133)\\
(112,81) & (-248,-465)\\
(112,94) & (-308,435)\\
(112,95) & (-47520,24140)\\
(112,99) & (672,1260)\\
(112,108) & (32,24)\\
(113,35) & (-9432,-15865)\\
(113,37) & (-18915,14308)\\
(113,46) & (-7,24)\\
(113,58) & (-160,-78)\\
(113,63) & (9653,33096)\\
(113,70) & (-559,840)\\
(113,108) & (2068,-4176)\\
(114,13) & (1206,1608)\\
(114,29) & (-11940,2189)\\
(114,34) & (3138,-4184)\\
(114,45) & (-1998,-2664)\\
(114,88) & (189,648)\\
(114,98) & (24354,-42120)\\
(115,9) & (-11820,-12411)\\
(115,15) & (52,675)\\
(115,26) & (-13160,16074)\\
(115,29) & (12400,-3195)\\
(115,55) & (-900,-1925)\\
(115,61) & (-24704,33153)\\
(115,63) & (3395,8148)\\
(115,68) & (-50,120)\\
(115,78) & (-341,420)\\
(115,93) & (135,72)\\
(115,106) & (16395,-8744)\\
(116,26) & (-4024,3018)\\
(116,33) & (-3420,10560)\\
(116,71) & (1476,-1357)\\
(116,79) & (3096,-3050)\\
(116,99) & (636,-477)\\
(116,105) & (-304,-570)\\
(117,11) & (6105,-2484)\\
(117,17) & (-12276,5957)\\
(117,38) & (576,350)\\
(117,43) & (-1044,-517)\\
(117,46) & (-12243,13024)\\
(117,69) & (-20475,13500)\\
(117,73) & (-3015,-1232)\\
(117,90) & (1456,5310)\\
(118,11) & (-3710,-1584)\\
(118,25) & (-50,120)\\
(118,26) & (2328,18746)\\
(118,47) & (-22448,30135)\\
(118,51) & (954,-1272)\\
(118,59) & (-3422,2640)\\
(118,86) & (-46632,19430)\\
(118,98) & (17598,-23464)\\
(118,102) & (-800,-1122)\\
(118,116) & (-23325,12440)\\
(118,117) & (-4466,8712)\\
(119,9) & (135,72)\\
(119,11) & (-8169,-7780)\\
(119,25) & (-21829,31140)\\
(119,27) & (308,75)\\
(119,38) & (-11305,-27132)\\
(119,48) & (-5600,-17052)\\
(119,62) & (39,80)\\
(119,69) & (17199,46368)\\
(119,75) & (4396,-7065)\\
(119,93) & (483,720)\\
(119,104) & (273,-736)\\
(119,116) & (159,212)\\
(120,11) & (12432,-23074)\\
(120,18) & (-38640,-47196)
\end{array}
$$
Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_ONE_TWENTY_RESIDUAL_CERTIFICATES`
- `box_one_twenty_residual_certificate`
- `box_one_twenty_audit_certificate`
- `test_box_one_twenty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le130$

The finite-audit layer now reaches
$$
|g|,|h|\le130.
$$
This audit reuses the box-$120$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are:
$$
\begin{array}{c|c}
T & P\\
\hline
(121,4) & (-3266,-4512)\\
(121,17) & (3300,-1411)\\
(121,35) & (4005,2948)\\
(121,50) & (576,350)\\
(121,57) & (396,297)\\
(121,69) & (7268,-24435)\\
(121,87) & (1581,-1008)\\
(121,91) & (9333,-6344)\\
(121,97) & (3553,396)\\
(121,119) & (85,-204)\\
(122,22) & (-294,-21608)\\
(122,23) & (-18582,24776)\\
(122,44) & (369,1640)\\
(122,78) & (-6566,-2088)\\
(122,79) & (-238,-240)\\
(122,96) & (320,-240)\\
(122,114) & (5850,-22440)\\
(123,36) & (-4389,26352)\\
(123,56) & (-675,816)\\
(123,68) & (-11100,-8512)\\
(123,100) & (-567,1020)\\
(123,107) & (159,212)\\
(124,27) & (-100,-105)\\
(124,38) & (7600,6195)\\
(124,39) & (-4536,11223)\\
(124,71) & (684,-3040)\\
(124,74) & (16872,-4921)\\
(124,85) & (-104,-1350)\\
(124,90) & (3204,47472)\\
(124,98) & (-336,-385)\\
(124,113) & (-2976,-15232)\\
(125,5) & (825,260)\\
(125,14) & (240,-238)\\
(125,16) & (-495,-1472)\\
(125,53) & (29645,-3432)\\
(125,61) & (10653,10396)\\
(125,70) & (-3808,-3150)\\
(125,74) & (2600,4662)\\
(125,91) & (1113,-1184)\\
(125,101) & (309,-412)\\
(125,108) & (-11484,19488)\\
(126,22) & (29526,-5368)\\
(126,31) & (2076,-865)\\
(126,43) & (3276,33043)\\
(126,46) & (-4098,5464)\\
(127,10) & (47271,-45020)\\
(127,18) & (5447,35196)\\
(127,33) & (22204,-29403)\\
(127,70) & (15631,-7308)\\
(127,72) & (-21608,-15840)\\
(127,75) & (-1160,2175)\\
(127,88) & (1026,-13832)\\
(127,93) & (11160,5049)\\
(127,117) & (260,273)\\
(128,24) & (-14432,-9576)\\
(128,78) & (4860,-8073)\\
(128,95) & (-304,-570)\\
(128,120) & (320,-240)\\
(129,7) & (-6171,10472)\\
(129,8) & (-831,1108)\\
(129,20) & (309,-412)\\
(129,21) & (-9387,2384)\\
(129,26) & (-3663,-7084)\\
(129,27) & (-4536,11223)\\
(129,90) & (-46935,16092)\\
(129,92) & (-567,1020)\\
(129,128) & (39,80)\\
(130,16) & (-3266,-4512)\\
(130,22) & (-6126,-8168)\\
(130,54) & (-13200,-40194)\\
(130,57) & (-5036,3777)\\
(130,92) & (15265,-7980)\\
(130,100) & (690,304)\\
(130,105) & (6916,2145)\\
(130,107) & (-2460,-781)\\
(130,113) & (44460,7553)
\end{array}
$$
Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_ONE_THIRTY_RESIDUAL_CERTIFICATES`
- `box_one_thirty_residual_certificate`
- `box_one_thirty_audit_certificate`
- `test_box_one_thirty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le140$

The finite-audit layer now reaches
$$
|g|,|h|\le140.
$$
This audit reuses the box-$130$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are:
$$
\begin{array}{c|c}
T & P\\
\hline
(131,14) & (-133,-156)\\
(131,27) & (-3213,-3240)\\
(131,28) & (1001,-6468)\\
(131,38) & (456,-190)\\
(131,53) & (1671,2228)\\
(131,92) & (-43,924)\\
(131,102) & (-800,1122)\\
(131,119) & (-24805,7392)\\
(132,51) & (-308,435)\\
(132,67) & (-7920,23552)\\
(132,68) & (7188,-20965)\\
(132,81) & (8832,15776)\\
(132,87) & (2860,-3168)\\
(132,93) & (2860,-7161)\\
(132,94) & (-1008,-3055)\\
(132,95) & (1980,400)\\
(132,115) & (1632,3060)\\
(133,8) & (-441,-1960)\\
(133,11) & (15753,-11704)\\
(133,18) & (616,-1638)\\
(133,29) & (43165,-3720)\\
(133,33) & (23485,-13728)\\
(133,73) & (-5180,-1887)\\
(133,78) & (-2835,-5148)\\
(133,101) & (4840,21021)\\
(133,102) & (1640,-8118)\\
(133,124) & (1456,960)\\
(133,125) & (13,-84)\\
(133,130) & (5005,-1716)\\
(134,9) & (5402,3960)\\
(134,18) & (-34,288)\\
(134,39) & (-238,-240)\\
(134,47) & (110,-96)\\
(134,70) & (14,48)\\
(134,73) & (-1026,-368)\\
(134,91) & (3686,-9048)\\
(134,98) & (374,168)\\
(134,121) & (24,-143)\\
(134,130) & (25944,35530)\\
(135,13) & (-4965,-6620)\\
(135,43) & (4371,3220)\\
(135,49) & (-2736,-323)\\
(135,62) & (-14040,-11970)\\
(135,87) & (-4845,-1988)\\
(135,101) & (-18180,38885)\\
(136,7) & (-26520,24640)\\
(136,14) & (-29120,-12936)\\
(136,22) & (-260,-825)\\
(136,30) & (80,-60)\\
(136,78) & (-1736,1023)\\
(136,104) & (-1235,1932)\\
(136,117) & (9416,11235)\\
(136,131) & (-2424,707)\\
(137,35) & (-91,-60)\\
(137,42) & (-2320,-882)\\
(137,65) & (-1320,689)\\
(137,72) & (17633,-23256)\\
(137,82) & (-424,-318)\\
(137,103) & (15204,33847)\\
(138,18) & (1656,1242)\\
(138,22) & (864,990)\\
(138,53) & (1380,253)\\
(138,66) & (-3192,-2006)\\
(138,87) & (-19992,-38369)\\
(138,118) & (3960,-6578)\\
(139,31) & (7,-24)\\
(139,35) & (51,140)\\
(139,52) & (75,100)\\
(139,59) & (-4385,10524)\\
(139,73) & (-1316,2013)\\
(139,84) & (209,-1140)\\
(139,109) & (-11088,745)\\
(139,112) & (22525,-11040)\\
(140,2) & (-4060,-768)\\
(140,15) & (108,-45)\\
(140,16) & (308,-144)\\
(140,32) & (159,212)\\
(140,46) & (-40660,24651)\\
(140,47) & (300,125)\\
(140,85) & (-924,2080)\\
(140,94) & (31388,43680)\\
(140,104) & (3234,26312)\\
(140,109) & (1848,-11786)\\
(140,123) & (4560,-10944)\\
(140,127) & (-10500,8800)\\
(140,132) & (-260,-288)\\
(140,135) & (-280,450)
\end{array}
$$
Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_ONE_FORTY_RESIDUAL_CERTIFICATES`
- `box_one_forty_residual_certificate`
- `box_one_forty_audit_certificate`
- `test_box_one_forty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le150$

The finite-audit layer now reaches
$$
|g|,|h|\le150.
$$
This audit reuses the box-$140$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are:
$$
\begin{array}{c|c}
T & P\\
\hline
(141,2) & (261,-348)\\
(141,14) & (-19008,39294)\\
(141,30) & (21,-20)\\
(141,37) & (24,-7)\\
(141,39) & (-1364,-477)\\
(141,56) & (-31779,38380)\\
(141,63) & (21945,-12740)\\
(141,74) & (-5355,16104)\\
(141,75) & (-1208,-2265)\\
(141,87) & (889,-3048)\\
(141,91) & (6045,-3224)\\
(141,129) & (-17227,25680)\\
(141,131) & (-27,36)\\
(141,133) & (1680,-1127)\\
(142,15) & (-33408,29295)\\
(142,28) & (-13685,-23436)\\
(142,31) & (20892,-8705)\\
(142,50) & (4158,-7480)\\
(142,71) & (32470,29256)\\
(142,91) & (40194,-8120)\\
(142,92) & (-1392,-3220)\\
(142,122) & (-19488,21866)\\
(143,6) & (2400,-1170)\\
(143,28) & (-91,-60)\\
(143,29) & (-1677,164)\\
(143,30) & (4959,2160)\\
(143,42) & (23903,-41340)\\
(143,63) & (8883,11844)\\
(143,82) & (-3360,-5822)\\
(143,106) & (1007,-1224)\\
(143,110) & (-1032,14774)\\
(143,111) & (-38940,44955)\\
(143,126) & (-1072,-8946)\\
(143,131) & (-38857,-8580)\\
(144,19) & (18744,1370)\\
(144,27) & (-3600,-2415)\\
(144,37) & (-28284,37712)\\
(144,50) & (40800,-6660)\\
(144,70) & (72,-65)\\
(144,89) & (-4728,6304)\\
(144,111) & (-6600,-1856)\\
(144,135) & (21840,-35100)\\
(145,49) & (-12180,1885)\\
(145,53) & (4005,2948)\\
(145,64) & (-495,-1472)\\
(145,76) & (75,100)\\
(145,102) & (19240,31062)\\
(145,106) & (-3855,2056)\\
(145,119) & (-41615,408)\\
(145,134) & (-25935,-12580)\\
(145,139) & (-35,120)\\
(146,5) & (-11550,9680)\\
(146,10) & (90,400)\\
(146,21) & (4416,1485)\\
(146,24) & (8096,-6528)\\
(146,31) & (-2190,5104)\\
(146,68) & (-12720,-44044)\\
(146,110) & (-1150,13200)\\
(147,2) & (-9408,8694)\\
(147,6) & (-645,812)\\
(147,15) & (6615,4180)\\
(147,20) & (-40320,45240)\\
(147,46) & (75,100)\\
(147,50) & (1995,2660)\\
(147,61) & (-897,496)\\
(147,87) & (-10661,36552)\\
(147,109) & (10395,6148)\\
(147,134) & (-47040,-15106)\\
(147,135) & (-189,180)\\
(148,12) & (8840,3927)\\
(148,38) & (7332,-28249)\\
(148,40) & (-900,-1925)\\
(148,51) & (108,-45)\\
(148,53) & (17292,-12805)\\
(148,81) & (-100,-105)\\
(148,82) & (268,201)\\
(148,100) & (-7076,5307)\\
(148,121) & (-8880,1876)\\
(148,130) & (88,105)\\
(148,138) & (728,-1254)\\
(149,35) & (-48151,20160)\\
(149,36) & (261,-348)\\
(149,43) & (-17451,4432)\\
(149,46) & (3405,1816)\\
(149,77) & (1689,2252)\\
(149,94) & (221,-60)\\
(149,98) & (3224,7350)\\
(149,104) & (10640,-35316)\\
(149,118) & (429,460)\\
(149,120) & (1391,5640)\\
(149,123) & (-711,9348)\\
(150,6) & (3870,-5160)\\
(150,23) & (-1560,-4081)\\
(150,51) & (-550,480)\\
(150,56) & (-135,-324)\\
(150,84) & (-19530,15456)\\
(150,92) & (-22881,30800)\\
(150,103) & (90,400)
\end{array}
$$
Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_ONE_FIFTY_RESIDUAL_CERTIFICATES`
- `box_one_fifty_residual_certificate`
- `box_one_fifty_audit_certificate`
- `test_box_one_fifty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le160$

The finite-audit layer now reaches
$$
|g|,|h|\le160.
$$
This audit reuses the box-$150$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are:
$$
\begin{array}{c|c}
T & P\\
\hline
(151,34) & (-5336,-2550)\\
(151,49) & (63,1984)\\
(151,64) & (-4728,6304)\\
(151,83) & (3976,-4257)\\
(151,86) & (-3776,-6450)\\
(151,103) & (-260,651)\\
(151,121) & (180,-299)\\
(151,127) & (-2948,-4005)\\
(151,131) & (-10925,-912)\\
(151,147) & (-14240,20559)\\
(152,4) & (14472,15040)\\
(152,6) & (-308,435)\\
(152,21) & (-260,-288)\\
(152,59) & (-20680,19899)\\
(152,60) & (737,-2184)\\
(152,69) & (7344,6075)\\
(152,83) & (-11440,4578)\\
(152,106) & (-5568,1624)\\
(152,113) & (-2208,644)\\
(152,122) & (708,-295)\\
(153,28) & (5148,-8400)\\
(153,33) & (7425,-2088)\\
(153,39) & (932,699)\\
(153,60) & (-135,-324)\\
(153,65) & (-4095,3900)\\
(153,80) & (16470,14960)\\
(153,88) & (-22881,30800)\\
(153,115) & (4320,5671)\\
(153,117) & (16065,-14248)\\
(153,143) & (-9675,5508)\\
(154,9) & (-24704,33153)\\
(154,30) & (1666,1680)\\
(154,37) & (-2772,5605)\\
(154,38) & (-15006,11408)\\
(154,48) & (-3266,-4512)\\
(154,53) & (-22092,49181)\\
(154,54) & (-630,11016)\\
(154,87) & (-2576,3255)\\
(154,93) & (6750,-8160)\\
(154,101) & (22410,11336)\\
(154,106) & (29760,4498)\\
(154,118) & (-2142,-23360)\\
(154,128) & (3234,-1312)\\
(155,11) & (-1672,1575)\\
(155,12) & (12110,28704)\\
(155,18) & (-12248,-9186)\\
(155,21) & (-18900,45753)\\
(155,52) & (189,340)\\
(155,59) & (11859,15812)\\
(155,63) & (56,-105)\\
(155,72) & (26400,5940)\\
(155,79) & (3795,-1400)\\
(155,149) & (-20680,13113)\\
(156,35) & (576,350)\\
(156,63) & (-1736,-1302)\\
(156,92) & (-2169,9640)\\
(156,109) & (-1716,-16687)\\
(156,120) & (8736,1352)\\
(156,126) & (4020,-26784)\\
(156,129) & (22620,48177)\\
(156,146) & (1368,651)\\
(157,2) & (6240,158)\\
(157,19) & (184,-345)\\
(157,27) & (-42291,5712)\\
(157,47) & (-299,180)\\
(157,50) & (33925,36900)\\
(157,92) & (4125,7268)\\
(157,110) & (-6968,22110)\\
(157,117) & (-4491,-5988)\\
(157,154) & (-800,-1122)\\
(158,2) & (198,-40)\\
(158,12) & (-117,-240)\\
(158,13) & (1106,-6192)\\
(158,23) & (-1738,6120)\\
(158,37) & (33162,-44216)\\
(158,41) & (-46740,-14839)\\
(158,51) & (-6200,-2805)\\
(158,62) & (6054,8072)\\
(158,79) & (-6162,4720)\\
(158,90) & (-1170,-2400)\\
(158,104) & (-6532,9024)\\
(158,113) & (-34252,25689)\\
(158,121) & (-1482,-1160)\\
(158,126) & (6840,-43050)\\
(158,155) & (308,75)\\
(159,6) & (1071,272)\\
(159,7) & (6039,10248)\\
(159,49) & (483,-644)\\
(159,52) & (-567,1020)\\
(159,99) & (324,243)\\
(159,137) & (375,200)\\
(159,141) & (236,177)\\
(159,150) & (18744,1370)\\
(159,154) & (7056,4158)\\
(160,24) & (-1404,1197)\\
(160,30) & (-288,-384)\\
(160,82) & (-8060,-1425)\\
(160,89) & (33480,-12361)\\
(160,93) & (29920,1038)\\
(160,126) & (10800,-35190)\\
(160,150) & (17920,-39000)\\
(160,158) & (46360,-31842)
\end{array}
$$
Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_ONE_SIXTY_RESIDUAL_CERTIFICATES`
- `box_one_sixty_residual_certificate`
- `box_one_sixty_audit_certificate`
- `test_box_one_sixty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le170$

The finite-audit layer now reaches
$$
|g|,|h|\le170.
$$
This audit reuses the box-$160$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are:
$$
\begin{array}{c|c}
T & P\\
\hline
(161,10) & (105,100)\\
(161,16) & (43995,-36872)\\
(161,27) & (13,-84)\\
(161,34) & (105,-56)\\
(161,47) & (-30156,4667)\\
(161,53) & (1421,4872)\\
(161,65) & (-22791,-16960)\\
(161,82) & (560,-1518)\\
(161,86) & (-672,-754)\\
(161,87) & (11501,-24168)\\
(161,139) & (3128,4095)\\
(161,151) & (1176,343)\\
(162,35) & (-2412,-4165)\\
(162,38) & (42,-144)\\
(162,94) & (5202,-6936)\\
(163,14) & (-14397,19196)\\
(163,25) & (20068,26565)\\
(163,27) & (28,-45)\\
(163,46) & (8008,10506)\\
(163,48) & (32558,44400)\\
(163,95) & (2295,1100)\\
(163,126) & (39347,18396)\\
(163,130) & (-10469,4560)\\
(163,153) & (15228,2121)\\
(163,157) & (2368,345)\\
(164,5) & (-32956,-46545)\\
(164,22) & (6644,4983)\\
(164,48) & (308,-144)\\
(164,51) & (-1552,-18786)\\
(164,69) & (864,-360)\\
(164,91) & (35588,-15141)\\
(164,103) & (-7116,-9488)\\
(164,105) & (-3276,-2793)\\
(164,113) & (200,-210)\\
(164,118) & (-760,-522)\\
(164,125) & (-24168,11501)\\
(164,155) & (312,266)\\
(165,47) & (-1296,1995)\\
(165,58) & (-576,-1482)\\
(165,78) & (-13475,-1560)\\
(165,85) & (9405,-2244)\\
(165,106) & (-6435,-12852)\\
(165,138) & (7480,-10350)\\
(166,15) & (-23754,30240)\\
(166,36) & (1995,1296)\\
(166,55) & (9780,-1793)\\
(166,59) & (-4814,6048)\\
(166,63) & (374,168)\\
(166,85) & (1020,3757)\\
(166,102) & (432,-810)\\
(166,109) & (156,133)\\
(166,119) & (-5538,-7384)\\
(167,9) & (23172,-17379)\\
(167,12) & (16836,19152)\\
(167,25) & (21171,28228)\\
(167,40) & (966,-920)\\
(167,56) & (80,-60)\\
(167,63) & (572,315)\\
(167,74) & (95,228)\\
(167,82) & (2415,1768)\\
(167,105) & (16147,26796)\\
(167,133) & (300,589)\\
(167,156) & (130,840)\\
(168,18) & (-1404,1197)\\
(168,19) & (432,5824)\\
(168,50) & (15960,24206)\\
(168,51) & (-4144,4692)\\
(168,53) & (11484,-12960)\\
(168,97) & (-17472,30096)\\
(168,102) & (18816,-2912)\\
(168,110) & (-840,704)\\
(168,125) & (-22632,15785)\\
(168,141) & (-3312,3795)\\
(168,151) & (17952,37111)\\
(168,158) & (6720,-328)\\
(168,162) & (-960,1008)\\
(169,14) & (-143,924)\\
(169,23) & (-22035,-29380)\\
(169,38) & (23104,3990)\\
(169,67) & (633,844)\\
(169,79) & (-260,651)\\
(169,81) & (-936,-24327)\\
(169,94) & (5016,7990)\\
(169,119) & (7029,-2380)\\
(169,138) & (1664,-1710)\\
(169,151) & (3117,4156)\\
(169,161) & (-3212,-35259)\\
(170,8) & (-4345,3792)\\
(170,18) & (35090,-6384)\\
(170,21) & (-600,-1827)\\
(170,38) & (90,56)\\
(170,52) & (20090,-3600)\\
(170,64) & (-3510,3496)\\
(170,77) & (2850,680)\\
(170,92) & (40625,28500)\\
(170,97) & (1490,3576)\\
(170,130) & (7130,2160)\\
(170,143) & (5270,12648)\\
(170,148) & (-11235,27520)\\
(170,167) & (-14110,336)
\end{array}
$$
Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_ONE_SEVENTY_RESIDUAL_CERTIFICATES`
- `box_one_seventy_residual_certificate`
- `box_one_seventy_audit_certificate`
- `test_box_one_seventy_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le180$

The finite-audit layer now reaches
$$
|g|,|h|\le180.
$$
This audit reuses the box-$170$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are:
$$
\begin{array}{c|c}
T & P\\
\hline
(171,35) & (-6321,-18900)\\
(171,49) & (38316,-20295)\\
(171,51) & (-9072,-3425)\\
(171,55) & (351,-1560)\\
(171,64) & (-22881,30800)\\
(171,100) & (-1920,560)\\
(171,104) & (12441,-6440)\\
(171,128) & (-60,-32)\\
(171,132) & (6750,-14896)\\
(171,147) & (7315,-3420)\\
(172,13) & (-29172,-27104)\\
(172,26) & (40,-198)\\
(172,28) & (7984,-5988)\\
(172,36) & (-260,-288)\\
(172,89) & (3840,-25456)\\
(172,91) & (-40232,5226)\\
(172,107) & (5152,1020)\\
(172,120) & (-1428,-279)\\
(172,138) & (-2688,5850)\\
(172,149) & (1920,1904)\\
(172,161) & (312,266)\\
(172,162) & (-8892,6960)\\
(173,22) & (29576,-22182)\\
(173,31) & (6840,4675)\\
(173,35) & (19173,43160)\\
(173,41) & (-37228,27921)\\
(173,48) & (1581,-1008)\\
(173,84) & (-11132,8976)\\
(173,97) & (5360,2613)\\
(173,126) & (-3675,-1260)\\
(173,136) & (572,96)\\
(173,137) & (-532,-855)\\
(173,141) & (-14740,20025)\\
(173,150) & (144,-270)\\
(173,171) & (-135,-324)\\
(174,39) & (-10980,18239)\\
(174,53) & (156,133)\\
(174,61) & (-5220,6669)\\
(174,68) & (261,-348)\\
(174,70) & (864,990)\\
(174,77) & (-150,-616)\\
(174,95) & (1974,1880)\\
(174,100) & (159,212)\\
(174,172) & (-2466,3288)\\
(175,19) & (1275,160)\\
(175,20) & (-260,-288)\\
(175,23) & (-30381,22940)\\
(175,40) & (4305,2296)\\
(175,46) & (5215,12516)\\
(175,51) & (10115,24276)\\
(175,74) & (-22640,-5094)\\
(175,117) & (-22540,6237)\\
(175,121) & (7923,-24464)\\
(175,130) & (-600,-2210)\\
(175,165) & (-24656,-31155)\\
(176,14) & (56,-105)\\
(176,19) & (-23140,-6141)\\
(176,23) & (-26964,6848)\\
(176,33) & (-40,-30)\\
(176,39) & (-260,-288)\\
(176,68) & (159,212)\\
(176,108) & (8816,-2412)\\
(176,116) & (80,396)\\
(176,124) & (-10432,7824)\\
(176,130) & (308,75)\\
(176,137) & (14916,-19888)\\
(176,165) & (-1984,-63)\\
(177,10) & (672,-90)\\
(177,39) & (29925,3000)\\
(177,55) & (4389,-1340)\\
(177,73) & (405,-252)\\
(177,94) & (744,-1850)\\
(177,112) & (4257,860)\\
(177,129) & (4437,21216)\\
(177,139) & (69,-92)\\
(177,147) & (16225,-14868)\\
(177,153) & (-600,-1827)\\
(177,160) & (3927,-8840)\\
(177,164) & (6240,9180)\\
(177,174) & (-175,-15312)\\
(178,2) & (-702,560)\\
(178,19) & (19558,-9144)\\
(178,37) & (6006,4408)\\
(178,48) & (-110,264)\\
(178,50) & (4600,3450)\\
(178,58) & (23586,-31448)\\
(178,98) & (490,-168)\\
(178,119) & (-20262,-34384)\\
(178,128) & (-43712,32784)\\
(178,139) & (-12282,3160)\\
(178,156) & (4130,1416)\\
(178,174) & (330,288)\\
(179,20) & (18120,-24160)\\
(179,34) & (11424,-12818)\\
(179,37) & (7604,-5703)\\
(179,49) & (43071,-32120)\\
(179,111) & (25724,-19293)\\
(179,112) & (-15405,11800)\\
(179,135) & (-13096,24555)\\
(179,166) & (42936,17890)\\
(180,11) & (2640,1036)\\
(180,14) & (-828,-896)\\
(180,27) & (9900,8640)\\
(180,94) & (-2520,-1677)\\
(180,116) & (-675,816)\\
(180,119) & (720,-448)
\end{array}
$$
Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_ONE_EIGHTY_RESIDUAL_CERTIFICATES`
- `box_one_eighty_residual_certificate`
- `box_one_eighty_audit_certificate`
- `test_box_one_eighty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le190$

The finite-audit layer now reaches
$$
|g|,|h|\le190.
$$
This audit reuses the box-$180$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 141 rows stored in `BOX_ONE_NINETY_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_ONE_NINETY_RESIDUAL_CERTIFICATES`
- `box_one_ninety_residual_certificate`
- `box_one_ninety_audit_certificate`
- `test_box_one_ninety_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le200$

The finite-audit layer now reaches
$$
|g|,|h|\le200.
$$
This audit reuses the box-$190$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 110 rows stored in `BOX_TWO_HUNDRED_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_TWO_HUNDRED_RESIDUAL_CERTIFICATES`
- `box_two_hundred_residual_certificate`
- `box_two_hundred_audit_certificate`
- `test_box_two_hundred_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le210$

The finite-audit layer now reaches
$$
|g|,|h|\le210.
$$
This audit reuses the box-$200$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 129 rows stored in `BOX_TWO_TEN_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_TWO_TEN_RESIDUAL_CERTIFICATES`
- `box_two_ten_residual_certificate`
- `box_two_ten_audit_certificate`
- `test_box_two_ten_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le220$

The finite-audit layer now reaches
$$
|g|,|h|\le220.
$$
This audit reuses the box-$210$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 134 rows stored in `BOX_TWO_TWENTY_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_TWO_TWENTY_RESIDUAL_CERTIFICATES`
- `box_two_twenty_residual_certificate`
- `box_two_twenty_audit_certificate`
- `test_box_two_twenty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le230$

The finite-audit layer now reaches
$$
|g|,|h|\le230.
$$
This audit reuses the box-$220$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 163 rows stored in `BOX_TWO_THIRTY_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_TWO_THIRTY_RESIDUAL_CERTIFICATES`
- `box_two_thirty_residual_certificate`
- `box_two_thirty_audit_certificate`
- `test_box_two_thirty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le240$

The finite-audit layer now reaches
$$
|g|,|h|\le240.
$$
This audit reuses the box-$230$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 162 rows stored in `BOX_TWO_FORTY_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_TWO_FORTY_RESIDUAL_CERTIFICATES`
- `box_two_forty_residual_certificate`
- `box_two_forty_audit_certificate`
- `test_box_two_forty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le250$

The finite-audit layer now reaches
$$
|g|,|h|\le250.
$$
This audit reuses the box-$240$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 173 rows stored in `BOX_TWO_FIFTY_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_TWO_FIFTY_RESIDUAL_CERTIFICATES`
- `box_two_fifty_residual_certificate`
- `box_two_fifty_audit_certificate`
- `test_box_two_fifty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le260$

The finite-audit layer now reaches
$$
|g|,|h|\le260.
$$
This audit reuses the box-$250$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 167 rows stored in `BOX_TWO_SIXTY_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_TWO_SIXTY_RESIDUAL_CERTIFICATES`
- `box_two_sixty_residual_certificate`
- `box_two_sixty_audit_certificate`
- `test_box_two_sixty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le270$

The finite-audit layer now reaches
$$
|g|,|h|\le270.
$$
This audit reuses the box-$260$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 173 rows stored in `BOX_TWO_SEVENTY_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_TWO_SEVENTY_RESIDUAL_CERTIFICATES`
- `box_two_seventy_residual_certificate`
- `box_two_seventy_audit_certificate`
- `test_box_two_seventy_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le280$

The finite-audit layer now reaches
$$
|g|,|h|\le280.
$$
This audit reuses the box-$270$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 178 rows stored in `BOX_TWO_EIGHTY_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_TWO_EIGHTY_RESIDUAL_CERTIFICATES`
- `box_two_eighty_residual_certificate`
- `box_two_eighty_audit_certificate`
- `test_box_two_eighty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le290$

The finite-audit layer now reaches
$$
|g|,|h|\le290.
$$
This audit reuses the box-$280$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 197 rows stored in `BOX_TWO_NINETY_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_TWO_NINETY_RESIDUAL_CERTIFICATES`
- `box_two_ninety_residual_certificate`
- `box_two_ninety_audit_certificate`
- `test_box_two_ninety_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le300$

The finite-audit layer now reaches
$$
|g|,|h|\le300.
$$
This audit reuses the box-$290$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 192 rows stored in `BOX_THREE_HUNDRED_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_THREE_HUNDRED_RESIDUAL_CERTIFICATES`
- `box_three_hundred_residual_certificate`
- `box_three_hundred_audit_certificate`
- `test_box_three_hundred_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le310$

The finite-audit layer now reaches
$$
|g|,|h|\le310.
$$
This audit reuses the box-$300$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 219 rows stored in `BOX_THREE_TEN_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_THREE_TEN_RESIDUAL_CERTIFICATES`
- `box_three_ten_residual_certificate`
- `box_three_ten_audit_certificate`
- `test_box_three_ten_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le320$

The finite-audit layer now reaches
$$
|g|,|h|\le320.
$$
This audit reuses the box-$310$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 206 rows stored in `BOX_THREE_TWENTY_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_THREE_TWENTY_RESIDUAL_CERTIFICATES`
- `box_three_twenty_residual_certificate`
- `box_three_twenty_audit_certificate`
- `test_box_three_twenty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le330$

The finite-audit layer now reaches
$$
|g|,|h|\le330.
$$
This audit reuses the box-$320$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 231 rows stored in `BOX_THREE_THIRTY_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_THREE_THIRTY_RESIDUAL_CERTIFICATES`
- `box_three_thirty_residual_certificate`
- `box_three_thirty_audit_certificate`
- `test_box_three_thirty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le340$

The finite-audit layer now reaches
$$
|g|,|h|\le340.
$$
This audit reuses the box-$330$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 237 rows stored in `BOX_THREE_FORTY_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_THREE_FORTY_RESIDUAL_CERTIFICATES`
- `box_three_forty_residual_certificate`
- `box_three_forty_audit_certificate`
- `test_box_three_forty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le350$

The finite-audit layer now reaches
$$
|g|,|h|\le350.
$$
This audit reuses the box-$340$ audit and then applies the same exact
constructors to the new outer ring. The remaining sign/swap representatives
are the 246 rows stored in `BOX_THREE_FIFTY_RESIDUAL_CERTIFICATES`; each row
records a target $T$ and midpoint $P$.

Every row is validated directly as a two-step midpoint identity, and the test
enumerates the whole finite box while keeping one-step targets and known
distance-three targets separate. This is still only a finite exact audit.

Executable guardrail:

- `BOX_THREE_FIFTY_RESIDUAL_CERTIFICATES`
- `box_three_fifty_residual_certificate`
- `box_three_fifty_audit_certificate`
- `test_box_three_fifty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le360$

The finite-audit layer now reaches
$$
|g|,|h|\le360.
$$
This audit reuses the box-$350$ audit and then applies the same exact
constructors to the new outer ring. The finite-direction parallel-cover
constructor with parameter bound $8$ certifies the remaining shell targets, so
`BOX_THREE_SIXTY_RESIDUAL_CERTIFICATES` has no residual midpoint rows.

Every returned certificate is validated directly as a two-step midpoint
identity, and the test enumerates the whole finite box while keeping one-step
targets and known distance-three targets separate. This is still only a finite
exact audit; bounded success of the finite direction set is not promoted to an
unbounded theorem.

Executable guardrail:

- `BOX_THREE_SIXTY_RESIDUAL_CERTIFICATES`
- `box_three_sixty_residual_certificate`
- `box_three_sixty_audit_certificate`
- `test_box_three_sixty_finite_audit`

## Exact Finite Audit In The Box $|g|,|h|\le500$

The finite-audit layer now reaches
$$
|g|,|h|\le500.
$$
This audit reuses the box-$360$ audit and then applies the same exact
constructors to the remaining finite box. The finite-direction parallel-cover
constructor with parameter bound $8$ certifies every remaining nontrivial
target in the box, so `BOX_FIVE_HUNDRED_RESIDUAL_CERTIFICATES` has no residual
midpoint rows.

Every returned certificate is validated directly as a two-step midpoint
identity. The guardrail enumerates the whole signed box, keeps one-step targets
and known distance-three targets separate, and checks that out-of-box targets
are rejected. This is still only a finite exact audit; it is not a proof that
the finite direction set covers all targets.

Executable guardrail:

- `BOX_FIVE_HUNDRED_RESIDUAL_CERTIFICATES`
- `box_five_hundred_residual_certificate`
- `box_five_hundred_audit_certificate`
- `test_box_five_hundred_finite_audit`

## Primitive-Ray Lift Of The Box-500 Audit

The box-500 audit is finite, but each primitive certificate in it has an
unbounded consequence. If a nonzero target $T=(g,h)$ has
$$
d=\gcd(|g|,|h|),\qquad T=dT_0,
$$
and the primitive representative $T_0$ has a two-step certificate with midpoint
$P_0$, then
$$
P=dP_0
$$
is a two-step midpoint for $T$. Both edge lengths are scaled by $d$.

The helper `box_five_hundred_ray_lift_certificate` makes this explicit. It first
uses the theorem-level axis and exceptional-ray helpers, then reduces a target
to its primitive representative. If that representative lies in the audited
signed box $|g|,|h|\le500$ and has a box-audit certificate, the helper scales
that certificate back to the original target. Thus the finite box is no longer
only a bounded target statement: it is also a seed list for infinitely many
whole rays. Targets whose primitive representative is already a one-step
Pythagorean edge need no two-step certificate from this helper, and the known
distance-three representatives are still deliberately rejected.

This does not close the full conjecture, because primitive representatives
outside the audited box still need structural coverage. It does sharpen the next
target: prove that every remaining primitive non-exception ray is either in an
existing theorem-level family or can be generated by a new exact ray mechanism.

Executable guardrail:

- `box_five_hundred_ray_lift_certificate`
- `test_box_five_hundred_ray_lift_promotes_primitive_seeds`

## General Euclid Strip Template

The affine consecutive-hypotenuse family below is a specialization of a more
general strip construction.

Fix a legal Pythagorean edge vector
$$
U=(u,v).
$$
Choose nonzero integers $q$ and $A$, and set
$$
B=uA-q.
$$
The vector
$$
Q=(2AB,\ B^2-A^2)
$$
is a Euclid-form Pythagorean vector whenever $B\ne0$ and
$B^2-A^2\ne0$. If
$$
v\mid q-(B^2-A^2),
$$
set
$$
r=\frac{q-(B^2-A^2)}v.
$$
Then
$$
P=rU,\qquad P+Q=(ru+2AB,\ q).
$$
Therefore, whenever $r\ne0$, $B\ne0$, and $B^2-A^2\ne0$, the target
$$
(ru+2AB,\ q)
$$
has distance at most $2$ from the origin.

A useful specialization appears when $u$ is odd and $v$ is even. Put
$$
A=\frac{vt}{2}.
$$
If $v\mid q(1-q)$, then the divisibility condition above is automatic and
$$
r=\frac{q(1-q)}v+uqt-\frac{(u^2-1)vt^2}{4}.
$$
The certified target is
$$
\left(
u\frac{q(1-q)}v+qt(u^2-v)+\frac{uv(1+2v-u^2)t^2}{4},
\ q
\right),
$$
again subject only to the same nondegeneracy conditions. This is an exact
infinite family for every odd-even Pythagorean direction.

This half-leg specialization also has a target-facing quadratic recognizer.
For a requested target $(g,q)$ with $q\ne0$, first require
$$
v\mid q(1-q).
$$
Set
$$
a=\frac{uv(1+2v-u^2)}4,\qquad b=q(u^2-v),\qquad
c=u\frac{q(1-q)}v.
$$
The target lies in the fixed-direction half-leg strip exactly when
$$
at^2+bt+c=g
$$
has a nonzero integral solution $t$ and the resulting strip certificate is
nondegenerate. If $a\ne0$, this is checked by the square discriminant
condition
$$
b^2+4a(g-c)=\square
$$
and divisibility of $-b\pm\sqrt{b^2+4a(g-c)}$ by $2a$. If $a=0$, the condition
reduces to the linear divisibility $b\mid g-c$. Sign changes and coordinate
swap give the symmetric target-facing recognizer.

For example, using $U=(15,8)$ from the $8$-$15$-$17$ triple and $q=1$ gives
$$
(-6240t^2+217t,\ 1)
$$
for every nonzero integer $t$. Sign changes and coordinate swap give the
corresponding symmetric strip points.

Executable guardrail:

- `euclid_strip_certificate`
- `half_leg_strip_certificate`
- `half_leg_strip_target_certificate`
- `half_leg_strip_orbit_certificate`
- `test_euclid_strip_template`
- `test_half_leg_strip_family`
- `test_half_leg_strip_target_solver`

## Half-Leg Unit-Coordinate Families

The half-leg strip has a useful unit-coordinate specialization beyond the
consecutive-hypotenuse case below. Let $U=(u,v)$ be any legal Pythagorean
direction with $u$ odd and $v$ even. In the half-leg strip, set $q=1$ and
$A=vt/2$ for nonzero integer $t$. Since $v\mid q(1-q)=0$, the divisibility
condition is automatic.

The certified target is
$$
\left(
t(u^2-v)+\frac{uv(1+2v-u^2)t^2}{4},\ 1
\right),
$$
and when $v=4z$ the same target can be written without division by putting
$$
A=2zt,\qquad B=uA-1,\qquad R=ut-z(u^2-1)t^2.
$$
Then the midpoint is $(uR,4zR)$ and the second edge is $(2AB,B^2-A^2)$.
The Lean row `certificateValid_halfLegUnitCoordinate` proves that the standard
strip nondegeneracy conditions are automatic for odd $u$ and nonzero $z,t$:
$R\ne0$ by parity, while $B$ and $B\pm A$ are odd. The coordinate swap and
sign-change symmetries give the corresponding families with one coordinate
$\pm1$.

This family now also has a target-facing recognizer. For a requested
unit-coordinate target $(g,1)$, set
$$
a=\frac{uv(1+2v-u^2)}4,\qquad b=u^2-v.
$$
The target is in this half-leg family exactly when the quadratic
$$
at^2+bt=g
$$
has a nonzero integral solution $t$ and the resulting strip certificate is
nondegenerate. Equivalently, when $a\ne0$, the discriminant
$$
b^2+4ag
$$
must be a square and one of $(-b\pm\sqrt{b^2+4ag})/(2a)$ must be integral. If
$a=0$, this reduces to the linear divisibility condition $b\mid g$. Sign
changes and coordinate swap give the orbit recognizer.

When $U$ comes from consecutive Euclid parameters $(m,m-1)$, so
$$
u=2m-1,\qquad v=2m(m-1),
$$
the quadratic coefficient vanishes because $1+2v-u^2=0$. This recovers the
linear consecutive-hypotenuse family $(ct,1)$ with
$c=m^2+(m-1)^2$.

Executable guardrail:

- `certificateValid_halfLegUnitCoordinate`
- `half_leg_unit_coordinate_certificate`
- `half_leg_unit_coordinate_target_certificate`
- `half_leg_unit_coordinate_orbit_certificate`
- `test_half_leg_unit_coordinate_family`
- `test_half_leg_unit_coordinate_target_solver`

## Exact Unit-Coordinate Audit Through $|n|\le500$

The unit-coordinate slice contains the primitive obstruction $(2,1)$, so it is
useful to keep a separate finite audit for this line. The current exact audit
certifies every target in the sign/swap orbit of $(n,1)$ with $|n|\le500$,
except for the known distance-three orbit. The audit first applies the exact
lattice, ray, diagonal, half-leg unit-coordinate, affine consecutive
hypotenuse, and Theorem 3 quadratic-strip families. The remaining sign/swap
representatives are:
$$
\begin{array}{c|c}
T & P\\
\hline
(38,1) & (8,-15)\\
(79,1) & (-5,-12)\\
(89,1) & (5,-12)\\
(93,1) & (9,-12)\\
(128,1) & (-40,96)\\
(136,1) & (16,-63)\\
(151,1) & (-16653,12604)\\
(203,1) & (60,25)\\
(259,1) & (-2345,804)\\
(261,1) & (9,40)\\
(266,1) & (90,-56)\\
(326,1) & (-37830,-28616)\\
(353,1) & (24153,-32204)\\
(371,1) & (-85,-132)\\
(376,1) & (-240,364)\\
(389,1) & (104,153)\\
(392,1) & (-160,231)\\
(422,1) & (-6888,-5375)\\
(436,1) & (16,30)\\
(441,1) & (21,-28)\\
(473,1) & (-1435,-4080)\\
(476,1) & (140,-51)
\end{array}
$$
Every row is directly validated as a two-step midpoint identity, and sign/swap
transport covers $(\pm n,\pm1)$ and $(\pm1,\pm n)$. This is a finite exact
statement only.

Executable guardrail:

- `UNIT_COORDINATE_500_RESIDUAL_CERTIFICATES`
- `unit_coordinate_500_residual_certificate`
- `unit_coordinate_500_audit_certificate`
- `test_unit_coordinate_finite_audit_to_500`

## Solved Consecutive-Direction Strip

The general Euclid strip can be solved directly for the Euclid parameter in the
consecutive-direction case.

Let $u\ge3$ be odd and set
$$
v=\frac{u^2-1}{2}.
$$
Then $U=(u,v)$ is a legal Pythagorean edge vector. In the notation of the
general strip, with
$$
B=uA-q,\qquad r=\frac{q-(B^2-A^2)}v,
$$
the target's first coordinate simplifies to
$$
ru+2AB=\frac{q(A(u^2+1)-u(q-1))}{v}.
$$
Therefore a requested target $(g,q)$ with $q\ne0$ is certified by this
consecutive direction whenever
$$
q(u^2+1)\mid vg+uq(q-1),
$$
with
$$
A=\frac{vg+uq(q-1)}{q(u^2+1)},
$$
and the resulting Euclid strip is nondegenerate.

This is a target-facing form of the strip template: it gives a direct
divisibility test for a two-step certificate instead of requiring a search over
the Euclid parameter $A$.

Executable guardrail:

- `consecutive_direction_strip_certificate`
- `test_consecutive_direction_strip_solver`

## Rational-Slope Consecutive Ray Families

The solved consecutive-direction strip also gives a target-facing family on
every nonhorizontal rational ray. Fix an integer ray vector $(p,q)$ with
$q\ne0$, a nonzero integer multiplier $n$, and an odd $u\ge3$. Put
$$
v=\frac{u^2-1}{2},\qquad M=u^2+1.
$$
For the target $(pn,qn)$, using the direction $(u,v)$ in the solved strip gives
the Euclid parameter
$$
A=\frac{vp+uq(qn-1)}{qM},
$$
so this direction certifies $(pn,qn)$ whenever
$$
qM\mid vp+uq(qn-1)
$$
and the underlying Euclid strip is nondegenerate.

Using the signed direction $(-u,v)$ instead gives
$$
A=\frac{vp-uq(qn-1)}{qM},
$$
and hence the companion divisibility condition
$$
qM\mid vp-uq(qn-1).
$$
In either case the target is produced by the same Euclid strip identity as
above, so the only exclusions are exactly the standard strip degeneracies
$A=0$, $B=0$, $B^2=A^2$, or zero first-step coefficient.

When $q=1$, this reduces to the integer-slope classes
$$
n\equiv 1+kuv\pmod M
\qquad\text{and}\qquad
n\equiv 1-kuv\pmod M.
$$
The previous exceptional-ray construction is the specialization $(p,q)=(2,1)$.

Executable guardrail:

- `rational_slope_consecutive_ray_certificate`
- `integer_slope_consecutive_ray_certificate`
- `test_rational_slope_consecutive_ray_family`
- `test_integer_slope_consecutive_ray_family`

## Consecutive Strip On The Exceptional Ray

The solved consecutive-direction strip gives exact families on the ray through
the primitive obstruction $(2,1)$. This does not certify the primitive point
itself, but it proves further nontrivial multiples have distance at most $2$.

Fix odd $u\ge3$ and an integer $t\ge1$. Set
$$
n=t(u^2+1)-2u+1.
$$
For the target $(2n,n)$, the solved strip condition gives
$$
A=\frac{\frac{u^2-1}{2}(2n)+un(n-1)}{n(u^2+1)}
=tu-1.
$$
With
$$
v=\frac{u^2-1}{2},\qquad B=uA-n,
$$
we get
$$
B=u-t-1,\qquad r=\frac{n-(B^2-A^2)}v=2(t^2+t-1).
$$
Thus the strip midpoint $P=r(u,v)$ reaches $(2n,n)$ whenever the Euclid vector
is nondegenerate. For $t\ge1$, $A\ne0$ and $r\ne0$; also
$|B|\ne |A|$. The only remaining degeneration is
$$
B=0\qquad\Longleftrightarrow\qquad t=u-1.
$$
Therefore, for every odd $u\ge3$ and every $t\ge1$ with $t\ne u-1$, the target
$$
(2n,n),\qquad n=t(u^2+1)-2u+1,
$$
has distance at most $2$ from the origin. Sign changes and coordinate swap give
the same conclusion for the corresponding images of this ray.

The opposite signed consecutive direction gives a companion family. With the
same odd $u\ge3$, set
$$
n=t(u^2+1)+2u+1,\qquad t\ge0.
$$
Using $U=(-u,v)$ and
$$
A=-tu-1
$$
in the Euclid strip gives
$$
B=-t-u-1,\qquad r=2(t^2+t-1),
$$
and the first coordinate again simplifies to $2n$. In this companion family,
$A$, $B$, and $B^2-A^2$ are all nonzero for every $t\ge0$. Hence these
$(2n,n)$ targets and their sign/swap images also have distance at most $2$.

Executable guardrail:

- `two_one_ray_consecutive_certificate`
- `two_one_ray_consecutive_orbit_certificate`
- `test_two_one_ray_consecutive_family`

## Three-Mod-Four Multipliers On The Exceptional Ray

The companion consecutive-strip family has a simple congruence corollary. Let
$$
n\equiv3\pmod4,\qquad n\ge7,
$$
and set
$$
u=\frac{n-1}{2}.
$$
Then $u$ is odd and at least $3$, and the companion family above is the case
$t=0$ of
$$
n=t(u^2+1)+2u+1.
$$
The corresponding midpoint simplifies to
$$
P=(2u,1-u^2)
  =\left(n-1,\,1-\left(\frac{n-1}{2}\right)^2\right).
$$
The two edge squares are
$$
(2u)^2+(1-u^2)^2=(u^2+1)^2
$$
and
$$
(2u+2)^2+(u^2+2u)^2=(u^2+2u+2)^2,
$$
with all coordinate differences nonzero for $u\ge3$. Thus every
$(2n,n)$ with $n\equiv3\pmod4$ and $n\ge7$ has distance at most $2$.
The remaining congruent multiplier $n=3$ is covered by the explicit base row
$(12,-5)$, so all positive multipliers $n\equiv3\pmod4$ on this ray are now
covered. Sign changes and coordinate swap give the same result on the full
orbit of the ray.

Executable guardrail:

- `two_one_ray_three_mod_four_certificate`
- `two_one_ray_three_mod_four_orbit_certificate`
- `test_two_one_ray_three_mod_four_family`

## Five-Or-Seventeen-Mod-Twenty Multipliers On The Exceptional Ray

The same consecutive-strip formulas give a direct corollary for two of the
remaining $1\pmod4$ multiplier classes. Specialize the odd leg to $u=3$, so
$v=4$ and $u^2+1=10$.

For
$$
n\equiv5\pmod {20},
$$
write
$$
n=10t-5,\qquad t\ge1.
$$
Here $t$ is odd, so the degeneration $t=u-1=2$ cannot occur. The first
signed strip family gives coefficient
$$
r=2(t^2+t-1)
$$
and midpoint
$$
P=(3r,4r).
$$

For
$$
n\equiv17\pmod {20},
$$
write
$$
n=10t+7,\qquad t\ge1.
$$
The companion signed strip family gives the same coefficient
$$
r=2(t^2+t-1)
$$
and midpoint
$$
P=(-3r,4r).
$$
In both cases the certificate is the corresponding $u=3$ consecutive-strip
certificate and is nondegenerate. Thus all positive multipliers
$n\equiv5,17\pmod {20}$ on the ray $(2n,n)$ have distance at most $2$.
Sign changes and coordinate swap again give the full orbit.

Executable guardrail:

- `two_one_ray_five_or_seventeen_mod_twenty_certificate`
- `two_one_ray_five_or_seventeen_mod_twenty_orbit_certificate`
- `test_two_one_ray_five_or_seventeen_mod_twenty_family`

## Even Multiples Of The Exceptional Ray

Every even positive multiple of the primitive obstruction direction $(2,1)$ is
also covered. The paper records a two-step certificate for $(2,4)$:
$$
O\to(77,-36)\to(2,4).
$$
Swapping coordinates gives
$$
O\to(-36,77)\to(4,2).
$$
By the scaling reduction, for every integer $m\ge1$,
$$
O\to(-36m,77m)\to(4m,2m)
$$
is a valid two-step path. Therefore $(2n,n)$ has distance at most $2$ for every
even $n\ge2$. Sign changes and coordinate swap give the corresponding orbit.

This statement is separate from the consecutive-strip subfamilies above: it
covers all even multipliers on the ray, while the strip families cover many odd
multipliers without touching the primitive obstruction.

Executable guardrail:

- `two_one_ray_even_certificate`
- `two_one_ray_even_orbit_certificate`
- `test_two_one_ray_even_family`

## Two/Three-Mod-Five Parallel Slice On The Exceptional Ray

The signed $3$-$4$-$5$ fixed-direction parallel-factor layer also closes a
clean pair of residue classes on the exceptional ray.  For $n\equiv2\pmod5$
and $n\ge7$, the direction $U=(4,3)$ with factor $F=2$ certifies
$(2n,n)$.  For $n\equiv3\pmod5$ and $n\ge8$, the signed direction
$U=(-4,-3)$ with the same factor certifies $(2n,n)$.  The first two
representatives are the only pointwise degeneracies for these fixed-factor
rows: $n=2$ is already covered by the even-ray theorem, and $n=3$ by the
Theorem 3 multiple-of-three row.

Thus every positive multiplier
$$
n\equiv2\text{ or }3\pmod5
$$
has a two-step certificate on the $(2,1)$ ray, and sign/swap transport gives
the whole orbit.  The helper
`two_one_ray_two_or_three_mod_five_parallel_certificate` exposes this slice
directly instead of hiding it inside the larger mod-$20$ skeleton.

Executable guardrail:

- `two_one_ray_two_or_three_mod_five_parallel_certificate`
- `two_one_ray_two_or_three_mod_five_parallel_orbit_certificate`
- `test_two_one_ray_two_or_three_mod_five_parallel_family`

## Mod-20 Skeleton On The Exceptional Ray

The exact ray families above now combine with the fixed parallel-factor
residue family to give a cleaner modular reduction of the exceptional ray.
Every even multiplier is covered, and every multiplier
$n\equiv3\pmod4$ is covered. The consecutive-strip specialization with
$u=3$ covers
$$
n\equiv5,17\pmod {20}.
$$
The parallel-direction ray family with $U=(-4,-3)$ and $F=2$ covers the
remaining class
$$
n\equiv13\pmod {20}.
$$
Indeed, for $n=5t+3$ the divisor reduction gives
$$
r=t^2-t-1,\qquad P=(-4r,-3r).
$$
The first residue $n=3$ is the only degenerate representative for this
parallel family, and it is already covered by the $3\pmod4$ formula. Therefore
all positive multipliers on the $(2,1)$ ray are covered by theorem-level
families except the two classes
$$
n\equiv1,9\pmod {20}.
$$
This is a sharper target than the finite audit: the unresolved part of the
exceptional ray is now two explicit residue classes rather than all odd
multipliers outside the primitive obstruction. The helper
`two_one_ray_mod20_skeleton_residues` records this finite residue split exactly
as all classes modulo $20$ except $1$ and $9$.

Executable guardrail:

- `two_one_ray_mod20_skeleton_certificate`
- `two_one_ray_mod20_skeleton_orbit_certificate`
- `two_one_ray_mod20_skeleton_residues`
- `test_two_one_ray_mod20_skeleton_family`

## Theorem 3 Multiples Of Three On The Exceptional Ray

The divisor-strengthened signed Theorem 3 gives a direct infinite subray inside
the exceptional direction. Use the triple $(12,5,13)$ with signs
$(s_x,s_y)=(1,-1)$. For $n=3m$ with $m\ge1$, the target is
$$
T=(2n,n)=(6m,3m).
$$
The ray divisor is
$$
((13-5)\cdot1-(13-12)\cdot2)n=6n=18m,
$$
and it divides $T_xT_y=18m^2$. The Theorem 3 divisor coefficient is $m$, so the
midpoint is
$$
P=(12m,-5m).
$$
Directly,
$$
12^2m^2+(-5)^2m^2=(13m)^2,\qquad
(6m-12m)^2+(3m+5m)^2=(10m)^2.
$$
All coordinate differences are nonzero for $m\ne0$. Hence every positive
multiplier divisible by $3$ on the $(2,1)$ ray has distance at most $2$, and
sign changes plus coordinate swap give the corresponding orbit. The Lean row
`certificateValid_twoOneRayMultipleOfThree` now proves the scaled midpoint
identity for every nonzero integer $m$.

Combining this row with the mod-$20$ skeleton gives a mod-$60$ refinement. The
old skeleton missed the two classes $1,9\pmod {20}$; after adding this Theorem
3 row, the only classes left modulo $60$ are
$$
1,\ 29,\ 41,\ 49 \pmod {60}.
$$
The helper `two_one_ray_mod60_theorem3_skeleton_residues` records exactly this
finite residue split.

Executable guardrail:

- `certificateValid_twoOneRayMultipleOfThree`
- `two_one_ray_multiple_of_three_theorem3_certificate`
- `two_one_ray_multiple_of_three_theorem3_orbit_certificate`
- `two_one_ray_mod60_theorem3_skeleton_certificate`
- `two_one_ray_mod60_theorem3_skeleton_orbit_certificate`
- `two_one_ray_mod60_theorem3_skeleton_residues`
- `test_two_one_ray_multiple_of_three_theorem3_family`
- `test_two_one_ray_mod60_theorem3_skeleton_family`

## Mod-260 Skeleton On The Exceptional Ray

The fixed consecutive-strip direction $u=5$ gives a further exact refinement
inside the two unresolved mod-$20$ classes. Since $u^2+1=26$, combine its
period with the mod-$20$ skeleton and work modulo
$$
\operatorname{lcm}(20,26)=260.
$$
The $u=5$ strip covers the additional residue classes
$$
n\equiv69,89,121,141\pmod {260},
$$
with midpoint examples
$$
\begin{array}{c|c}
n & P\\
\hline
69 & (110,264)\\
89 & (-110,264)\\
121 & (290,696)\\
141 & (-290,696).
\end{array}
$$
Together with the mod-$20$ skeleton, this leaves exactly the following residue
classes modulo $260$:
$$
\begin{gathered}
1,9,21,29,41,49,61,81,101,109,129,149,\\
161,169,181,189,201,209,221,229,241,249.
\end{gathered}
$$
The helper `two_one_ray_mod260_skeleton_residues` records this finite split
exactly. This is still not a proof of the whole exceptional ray; it is a
sharper exact modular target for the remaining work.

Executable guardrail:

- `two_one_ray_mod260_skeleton_certificate`
- `two_one_ray_mod260_skeleton_orbit_certificate`
- `two_one_ray_mod260_skeleton_residues`
- `test_two_one_ray_mod260_skeleton_family`

## Mod-Ten Divisor Family On The Exceptional Ray

The fixed parallel-direction method gives a broader divisor criterion on the
same ray. Write a positive multiplier as
$$
n=dq.
$$
If
$$
q\equiv3\pmod {10},
$$
take $U=(3,-4)$ and factor $F=d$. For the target $(2n,n)$ one has
$$
D=11dq,\qquad A=2dq,
$$
and the divisor reduction gives
$$
r=\frac{d(121q^2+4q-1)}{50}.
$$
The numerator is divisible by $50$ for every $q\equiv3\pmod {10}$, so
$P=r(3,-4)$ is an exact two-step certificate.

If instead
$$
q\equiv7\pmod {10},
$$
take $U=(-3,4)$ and the same factor $F=d$. Then
$$
D=-11dq,\qquad A=-2dq,\qquad
r=\frac{d(121q^2-4q-1)}{50},
$$
which is integral for every $q\equiv7\pmod {10}$. Thus any multiplier with a
divisor $3$ or $7$ modulo $10$ is covered by an exact parallel-direction
certificate.

This sharpens the remaining exceptional-ray problem again. Inside the two
mod-$20$ classes left by the skeleton, every multiplier with a divisor
$3$ or $7$ modulo $10$ is now covered. Therefore any still-uncovered positive
multiplier on this ray must have all divisors congruent to $1$ or $9$ modulo
$10$; equivalently, in the odd non-multiple-of-$5$ residual setting, all prime
factors are $1$ or $9$ modulo $10$. This is now the natural number-theoretic
target replacing the previous finite-audit residual set. The helpers
`has_divisor_three_or_seven_mod_ten` and
`all_prime_factors_one_or_nine_mod_ten` record this multiplicative reduction
as an exact arithmetic guardrail.

Executable guardrail:

- `has_divisor_three_or_seven_mod_ten`
- `all_prime_factors_one_or_nine_mod_ten`
- `prime_factors`
- `two_one_ray_complement_divisor_residues`
- `two_one_ray_complement_divisor_certificate`
- `two_one_ray_mod_ten_divisor_certificate`
- `two_one_ray_mod_ten_divisor_orbit_certificate`
- `test_two_one_ray_mod_ten_divisor_family`
- `test_mod_ten_divisor_residual_prime_factor_reduction`

## Mod-26 Divisor Family On The Exceptional Ray

The same complement-factor construction has a second small instance from the
$5$-$12$-$13$ directions. For $n=dq$, use factor $F=d$. The four signed
directions give the quotient classes
$$
\begin{array}{c|c}
q \pmod {26} & U\\
\hline
3 & (5,12)\\
7 & (-5,12)\\
19 & (5,-12)\\
23 & (-5,-12).
\end{array}
$$
For example, with $U=(5,12)$ one has
$$
D=-19dq,\qquad A=22dq,\qquad
r=\frac{d(361q^2+44q-1)}{338},
$$
which is integral for every $q\equiv3\pmod {26}$. The other three rows are the
same divisor reduction with the corresponding signed direction.

Thus any multiplier having a divisor in one of the classes
$$
3,7,19,23\pmod {26}
$$
is covered by an exact parallel-direction certificate. This is not a fixed
residue class modulo $260$ for the multiplier itself; it is a multiplicative
divisor sieve, so translated representatives can enter or leave depending on
their factorization.

Executable guardrail:

- `two_one_ray_mod_twenty_six_divisor_certificate`
- `two_one_ray_mod_twenty_six_divisor_orbit_certificate`
- `test_two_one_ray_mod_twenty_six_divisor_family`

## Square-Determinant Factor On The Exceptional Ray

The complement-divisor sieve fixes the small factor $F=1$ for a prime
multiplier. The same parallel-direction identity has another natural factor
choice. For $T=n(2,1)$ and a direction $U=(u,v)$, put
$$
A=2u+v,\qquad B=u-2v,\qquad c^2=u^2+v^2.
$$
Since $\det(U,T)=nB$, choosing the divisor factor
$$
F=B^2
$$
leaves paired factor $n^2$ and forces the first-step coefficient
$$
r=\frac{n^2-B^2+2nA}{2c^2}.
$$
Whenever this is integral and nondegenerate, $P=rU$ is an exact two-step
certificate.
The integrality condition has a simple root form because
$A^2+B^2=5c^2$:
$$
n^2+2An-B^2=(n+A)^2-5c^2.
$$
Thus the arithmetic period for a direction is the parity-compatible lift of
$$
n\equiv -A\pmod c
$$
modulo $2c$. This mirrors the complement-divisor root formula but uses the
large determinant-square factor $B^2$ instead of factor $1$. The executable
guardrail checks this period formula against direct factor-witness enumeration
for all primitive signed directions with Euclid parameter at most $12$ and
hypotenuse at most $250$.

The same scaling idea turns this into a divisor sieve. If $n=dq$ and $q$ is in
the square-factor class for $U$, choose factor
$$
F=dB^2.
$$
Then the paired factor is $dq^2$, and the first-step coefficient is $d$ times
the base coefficient for $q$. Therefore any multiplier with a divisor in one of
these square-factor classes is certified, apart from the same pointwise
degeneracies that the certificate checker rejects.

As with the complement-divisor layers, one can collect all signed directions
with a fixed hypotenuse. The first promoted square-factor hypotenuse layers are:
$$
\begin{array}{c|c}
c & q\text{-classes}\\
\hline
13 & 6,9,10,11,15,16,17,20\pmod {26}\\
17 & 5,13,14,16,18,20,21,29\pmod {34}\\
37 & 21,22,26,29,45,48,52,53\pmod {74}\\
41 & 17,19,30,34,48,52,63,65\pmod {82}.
\end{array}
$$

The first useful exceptional-ray instance is the $5$-$12$-$13$ direction
$$
U=(5,-12),\qquad A=-2,\qquad B=29,\qquad c=13.
$$
Here $F=29^2=841$ and
$$
r=\frac{n^2-4n-841}{338}.
$$
For
$$
n=26t+15
$$
this becomes
$$
r=2(t^2+t-1),
$$
so every positive multiplier $n\equiv15\pmod {26}$ is certified except the
single degenerate case $n=145$, where the second step becomes vertical. For
example, $5449=26\cdot209+15$ gives
$$
r=87778,\qquad P=(438890,-1053336).
$$
This is a different exact route from the quotient-divisor classes
$3,7,19,23\pmod {26}$: it uses a non-complement factor of the determinant
square and therefore catches a residue class that the complement-divisor layer
does not.
With the promoted square-factor hypotenuse layers and the next inverse-root
seed extension below, the divisor-lift audit now has no unresolved multiplier in
the interval $2\le n<3000$.

Executable guardrail:

- `two_one_ray_square_determinant_factor_certificate`
- `two_one_ray_square_determinant_divisor_certificate`
- `two_one_ray_square_determinant_factor_sieve_certificate`
- `two_one_ray_square_determinant_factor_period`
- `two_one_ray_square_determinant_factor_residues`
- `two_one_ray_hypotenuse_square_factor_directions`
- `two_one_ray_hypotenuse_square_factor_residue_classes`
- `two_one_ray_hypotenuse_square_factor_certificate`
- `TWO_ONE_RAY_PROMOTED_SQUARE_FACTOR_HYPOTENUSES`
- `two_one_ray_promoted_square_factor_certificate`
- `two_one_ray_mod_twenty_six_square_factor_certificate`
- `test_two_one_ray_mod_twenty_six_square_factor_family`

## Scaled Fixed-Factor Residues On The Exceptional Ray

The complement-divisor and square-determinant constructions are both instances
of a more general scaling principle. Fix a direction $U$ and a positive factor
$F_0$. Suppose the multiplier $q$ on the exceptional ray has a valid
parallel-direction certificate using this fixed factor $F_0$. If $n=dq$, then
the multiplier $n$ has a certificate using factor
$$
F=dF_0,
$$
and the midpoint coefficient is $d$ times the base coefficient. Thus every
fixed direction/factor residue class can be promoted into a divisor sieve:
$$
\exists q\mid n,\qquad q\in R(U,F_0).
$$
The helper `ray_parallel_factor_residues` already computes the exact arithmetic
classes modulo $2|U|^2F_0$, and the scaled certificate helper then checks the
actual target to discard pointwise degeneracies.

The first promoted scaled-factor layers are small:
$$
\begin{array}{c|c|c}
U & F_0 & q\text{-class}\\
\hline
(-12,5) & 22 & q\equiv5\pmod {13}\\
(-12,-5) & 2 & q\equiv8\pmod {13}\\
(20,-21) & 2 & q\equiv23\pmod {29}.
\end{array}
$$
These catch the previous next-frontier primes $3229$, $4649$, and $3329$,
respectively. With these layers, the promoted square-factor layers, and the
inverse-root seed layers, the divisor-lift audit has no unresolved multiplier
for $2\le n<5000$. A diagnostic scan then showed the next remaining prime
multipliers below $10000$ were $5849,7669,9749$.

Executable guardrail:

- `two_one_ray_scaled_factor_divisor_certificate`
- `TWO_ONE_RAY_PROMOTED_SCALED_FACTOR_LAYERS`
- `two_one_ray_promoted_scaled_factor_certificate`
- `test_two_one_ray_promoted_scaled_factor_layers`

## Determinant Split-Factor Layers On The Exceptional Ray

The fixed-factor layers above still left the impression of isolated interior
factor choices. The determinant coordinates show that these are not isolated.
Fix a Pythagorean direction $U=(u,v)$ with hypotenuse $c$, and write
$$
A=2u+v,\qquad B=u-2v.
$$
For a quotient multiplier $q$, choose a base factor $F_0$ which divides
$B^2$, and put
$$
F_0H=B^2.
$$
The parallel-direction factor equations for $q(2,1)$ become
$$
Hq^2+F_0\equiv0\pmod {2c}
$$
for the completed hypotenuse, and
$$
Hq^2+2Aq-F_0\equiv0\pmod {2c^2}
$$
for the first-step coefficient. The discriminant of the second congruence is
$$
(2A)^2+4HF_0=4(A^2+B^2)=20c^2.
$$
Thus, when $\gcd(H,c)=1$, the quadratic has a double root modulo $c$:
$$
qH+A\equiv0\pmod c.
$$
Only the two parity lifts modulo $2c$ remain to be checked against the exact
factor and coefficient congruences. This recovers the earlier endpoints:

- $F_0=1$ is the complement-divisor construction;
- $F_0=B^2$ is the square-determinant factor construction;
- intermediate divisors $1<F_0<B^2$ are the scaled fixed-factor layers.

Once a quotient $q$ is certified by this split factor, every multiplier
$n=dq$ is certified by using the scaled factor $dF_0$. This is the principled
replacement for extending midpoint boxes: small promoted hypotenuses now
generate all their determinant-square factor splits.

The promoted split-factor hypotenuses are now
$$
c=17,29,37,41,53,61,73,89,97,197,401.
$$
The first diagnostic frontier below $10000$ was covered without adding a
larger box:
$$
\begin{array}{c|c|c|c}
q & U & F_0 & q\text{-class}\\
\hline
7669 & (8,-15) & 2 & q\equiv2\pmod {17}\\
5849 & (20,21) & 2 & q\equiv20\pmod {29}\\
9749 & (-40,-9) & 22 & q\equiv32\pmod {41}.
\end{array}
$$
Closing the next determinant split hypotenuses removes the later prime-seed
frontier in the same way:
$$
\begin{array}{c|c|c|c}
q & U & F_0 & q\text{-class}\\
\hline
10061 & (45,-28) & 10201 & q\equiv97\pmod {106}\\
23869 & (195,-28) & 63001 & q\equiv229\pmod {394}\\
40429 & (-40,-399) & 2 & q\equiv329\pmod {401}.
\end{array}
$$
With these determinant split-factor layers included, the direct divisor-lift
audit has no unresolved multiplier for $2\le n<10000$ on the exceptional ray,
and the prime-seed audit has no unresolved prime for $10000\le p<1000000$
after adding the lift-three family below.
By divisor-lift closure, that proves the same range of multipliers once prime
seeds are considered.
The next diagnostic prime frontier starts at $110161$; its first hits again
come from determinant split hypotenuses, for example $c=233,277,169$ for
$110161,110501,133121$ respectively.
The helper `two_one_ray_determinant_split_factor_witness` makes this
target-facing: given a multiplier and a hypotenuse bound, it scans quotient
divisors and determinant split layers, then returns the first exact
certificate row. This is still not a proof of global coverage, but it replaces
manual frontier inspection by a reproducible algebraic inverse problem.
For the next frontier it returns, for example,
$$
\begin{array}{c|c|c|c|c}
q & c & U & F_0 & q\text{-class}\\
\hline
110161 & 233 & (-105,-208) & 96721 & q\equiv185\pmod {466}\\
110501 & 277 & (-115,252) & 383161 & q\equiv255\pmod {554}\\
133121 & 169 & (-119,120) & 128881 & q\equiv287\pmod {338}.
\end{array}
$$
There is an even sharper inverse form if the paired factor $H$ is fixed. Since
the split root is
$$
A\equiv -qH\pmod c,
$$
the finitely many lifts $A=-qH+\ell c$ with $|A|<\sqrt5c$ determine
$$
B^2=5c^2-A^2.
$$
Thus a candidate row is recovered exactly by requiring $B^2$ to be a square,
$H\mid B^2$, and the usual modulo-$5$ reconstruction of
$$
u=\frac{2A+B}{5},\qquad v=\frac{A-2B}{5}.
$$
The helper `two_one_ray_determinant_paired_factor_root` implements this
calculation, and `two_one_ray_paired_factor_split_factor_witness` wraps it into
a certificate search over quotient divisors and hypotenuses. This is a smaller
inverse problem than enumerating all directions and all split factors in a
hypotenuse layer. It explains the common square-factor endpoint $H=1$ for
diagnostic primes such as $10061,23869,110161,110501,133121$.
Fixing the lift
$$
k=\frac{A+qH}{c}
$$
shrinks the inverse problem again. With $D=k^2-5$ and
$$
X=Dc-kqH,
$$
the determinant norm is exactly
$$
X^2+D B^2=5q^2H^2.
$$
For $D>0$ this gives a finite conic search in $B$ with no hypotenuse scan.
The helper `two_one_ray_determinant_paired_factor_lift_root` implements this
lift-facing inverse and reconstructs $(U,F_0,c)$ from $(q,H,k)$. The
determinant-split test verifies this identity for all recorded frontier rows,
including even-first-coordinate split directions that are not complement-root
directions.
The first lift is especially simple. If $H=1$ and $k=3$, then
$$
A=3c-q.
$$
For any Pythagorean direction $U=(u,v)$ with hypotenuse $c$ and
$A=2u+v$, the multiplier
$$
q=3c-A=3c-(2u+v)
$$
has the two-step certificate
$$
P=2U.
$$
Indeed,
$$
|2U|=2c,\qquad |q(2,1)-2U|=|3q-2c|.
$$
This is the lift-three square-endpoint family. The helper
`two_one_ray_double_direction_certificate` builds the row from $U$, and
`two_one_ray_lift_three_square_endpoint_certificate` uses the lift-conic
inverse as a prime-seed recognizer. It catches the next prime frontier with
small midpoints, for example
$$
\begin{array}{c|c|c}
q & U & P=2U\\
\hline
110161 & (-4275,-25132) & (-8550,-50264)\\
110501 & (-16965,31948) & (-33930,63896)\\
133121 & (-8475,57148) & (-16950,114296)\\
159769 & (188469,43700) & (376938,87400).
\end{array}
$$
With this family in the seed constructor, the executable prime-seed audit has
no unresolved prime for $10000\le p<1000000$.

More importantly, this is not just another large audit. For every odd prime
$p\equiv1\pmod4$, Fermat's two-square theorem gives
$$
p=x^2+z^2.
$$
Exactly one of $x,z$ is even, so write the even one as $2y$:
$$
p=x^2+4y^2.
$$
Set $m=x+y$ and $n=y$. Then
$$
c=m^2+n^2=x^2+2xy+2y^2,
$$
and for the Euclid direction
$$
U=(m^2-n^2,2mn)=(x^2+2xy,2xy+2y^2)
$$
one has
$$
3c-(2u+v)=x^2+4y^2=p.
$$
Thus every prime $p\equiv1\pmod4$ is a double-direction seed. The other prime
classes on the exceptional ray were already seed classes: $p=2$ is even, and
$p\equiv3\pmod4$ is covered by the three-mod-four formula. Therefore every
prime multiplier $p>1$ on the $(2,1)$ ray now has an exact two-step seed
certificate, and divisor-lift closure gives every composite multiplier
$n>1$ on the ray. The primitive multiplier $n=1$ remains the known
distance-three obstruction.

The executable form is now direct rather than another larger search. The helper
`two_one_ray_prime_divisor_lift_certificate` factors $n>1$, takes a prime
divisor $p$, invokes the seed certificate for $p$, and scales that certificate
by $n/p$. The companion orbit helper transports this certificate across signs
and coordinate swaps. The remaining finite ranges are guardrails for the
implementation, not the mechanism of the proof.

The $H=1$ endpoint has a useful Pell interpretation. A determinant-slice root
$(A,B,c)$ already lies on
$$
A^2-5c^2=-B^2.
$$
The complement-divisor certificate uses factor $1$ and the root
$qB^2+A\equiv0\pmod c$. The square endpoint instead uses factor $B^2$ and the
linear class
$$
q+A\equiv0\pmod c,
$$
with the parity lift modulo $2c$. Thus the same fixed-$B$ Pell orbit that
advances complement roots also advances square-endpoint split layers. For
example, the reduced slice
$$
(A,B,c)=(-118,-359,169)
$$
has square-endpoint class $q\equiv287\pmod {338}$ and certifies $q=133121$ by
the midpoint $(-36852158,37161840)$. The conjugate slice
$(118,359,169)$ has class $q\equiv51\pmod {338}$ and catches the later
diagnostic prime $307969$. The helpers now expose this directly through
`TwoOneRayDeterminantSliceRoot.square_endpoint_certificate` and
`two_one_ray_determinant_square_endpoint_orbit_certificate`.

Executable guardrail:

- `TwoOneRayDeterminantSplitFactorWitness`
- `TwoOneRayDeterminantSliceRoot.square_endpoint_certificate`
- `two_one_ray_determinant_square_endpoint_orbit_certificate`
- `two_one_ray_double_direction_certificate`
- `two_one_ray_lift_three_square_endpoint_certificate`
- `two_one_ray_prime_one_mod_four_double_direction_certificate`
- `two_one_ray_prime_divisor_lift_certificate`
- `two_one_ray_prime_divisor_lift_orbit_certificate`
- `two_one_ray_paired_factor_lift_witness`
- `two_one_ray_determinant_paired_factor_lift_root`
- `two_one_ray_determinant_paired_factor_root`
- `two_one_ray_determinant_split_factor_period`
- `two_one_ray_determinant_split_factor_certificate`
- `two_one_ray_hypotenuse_determinant_split_factor_layers`
- `two_one_ray_hypotenuse_determinant_split_factor_certificate`
- `two_one_ray_determinant_split_factor_witness`
- `two_one_ray_paired_factor_split_factor_witness`
- `TWO_ONE_RAY_PROMOTED_DETERMINANT_SPLIT_FACTOR_HYPOTENUSES`
- `two_one_ray_promoted_determinant_split_factor_certificate`
- `test_two_one_ray_determinant_split_factor_layers`

## Combined Mod-130 Divisor Sieve On The Exceptional Ray

Combining the mod-$10$ and mod-$26$ divisor sieves is equivalent to checking
divisor residues modulo
$$
\operatorname{lcm}(10,26)=130.
$$
The exact covered residue classes are
$$
\begin{gathered}
3,7,13,17,19,23,27,29,33,37,43,45,47,49,53,55,57,59,63,67,\\
71,73,75,77,81,83,85,87,93,97,101,103,107,111,113,117,123,127
\pmod {130}.
\end{gathered}
$$
Thus the combined test is still a multiplicative divisor sieve, not a
periodic condition on the multiplier itself. The helper
`two_one_ray_mod_130_divisor_residues` records the residue set, while
`has_divisor_in_residue_classes` and `has_two_one_ray_mod_130_divisor` test
the exact divisor condition for a given multiplier.

This combined filter is stronger than the mod-$10$ prime-factor residual
condition alone. For instance, $361=19^2$ has prime factors congruent to
$9\pmod {10}$, but it is caught by the combined sieve because $19$ is one of
the covered divisor residues modulo $130$.

This is not a proof of the entire $(2,1)$ ray. It is an exact arithmetic
filter for the portion already certified by the two divisor constructions.

Executable guardrail:

- `has_divisor_in_residue_classes`
- `two_one_ray_mod_130_divisor_residues`
- `has_two_one_ray_mod_130_divisor`
- `test_combined_mod_130_divisor_residual_reduction`

## Complement-Divisor Sieve And Mod-34 Family

The previous mod-$10$ and mod-$26$ constructions are instances of a more
systematic sieve. Fix a Pythagorean direction $U$ and write a multiplier as
$$
n=dq.
$$
The complement-divisor construction uses the divisor complement $d$ as the
parallel factor. For each signed direction $U$, the base case $d=1$ gives a
finite quotient residue set modulo $2|U|^2$; when that set is periodic with a
smaller period, it can be compressed to the minimal quotient period. Therefore
any finite direction set gives an exact divisor criterion:
$$
\exists q\mid n,\qquad q\bmod m_U\in R_U
$$
for one of the direction periods $(m_U,R_U)$.

The quotient class is now computed directly. For $U=(u,v)$, put
$$
c^2=u^2+v^2,\qquad a=2u+v,\qquad b=u-2v.
$$
The factor-one integrality condition for $q(2,1)$ is
$$
b^2q^2+2aq-1\equiv0\pmod {2c^2}.
$$
If $u$ is odd and $\gcd(b,c)=1$, this has one odd quotient class modulo $2c$:
$$
q\equiv -a(b^2)^{-1}\pmod c,\qquad q\equiv1\pmod2.
$$
If $u$ is even or $\gcd(b,c)>1$, the current complement-divisor root formula
returns no class. The test suite checks this formula against direct quadratic
congruence enumeration for all primitive signed directions with Euclid
parameter at most $20$ and hypotenuse at most $300$.

This also gives a hypotenuse-layer formulation. For a fixed hypotenuse $c$,
collect every primitive signed Pythagorean direction $U$ with $|U|=c$, keep the
directions whose root formula returns a class, and take their union modulo
$2c$. For example:
$$
\begin{array}{c|c}
c & q\text{-classes}\\
\hline
5 & 3,7\pmod {10}\\
13 & 3,7,19,23\pmod {26}\\
17 & 7,13,21,27\pmod {34}\\
29 & 7,25,33,51\pmod {58}\\
37 & 7,23,51,67\pmod {74}\\
41 & 13,29,53,69\pmod {82}.
\end{array}
$$
The helper `two_one_ray_hypotenuse_divisor_certificate` certifies any
multiplier having a divisor in one of the classes for that hypotenuse. This is
the reusable layer behind the named mod-$34$, mod-$58$, mod-$74$, and mod-$82$
families.

The first five small direction layers are:
$$
\begin{array}{c|c|c}
\text{triple} & U & q\text{-classes}\\
\hline
3\text{-}4\text{-}5 & (3,-4),(-3,4) & 3,7\pmod {10}\\
5\text{-}12\text{-}13 & (5,12),(-5,12),(5,-12),(-5,-12)
  & 3,7,19,23\pmod {26}\\
8\text{-}15\text{-}17 & (15,-8),(15,8),(-15,-8),(-15,8)
  & 7,13,21,27\pmod {34}\\
20\text{-}21\text{-}29 & (-21,-20),(-21,20),(21,-20),(21,20)
  & 7,25,33,51\pmod {58}\\
12\text{-}35\text{-}37 & (-35,12),(-35,-12),(35,12),(35,-12)
  & 7,23,51,67\pmod {74}\\
9\text{-}40\text{-}41 & (9,-40),(9,40),(-9,-40),(-9,40)
  & 13,29,53,69\pmod {82}.
\end{array}
$$
For example, with $U=(15,-8)$ one has
$$
D=31dq,\qquad A=22dq,\qquad
r=\frac{d(961q^2+44q-1)}{578},
$$
which is integral for every $q\equiv7\pmod {34}$. The other three
$8$-$15$-$17$ rows are the signed variants, giving classes
$13,21,27\pmod {34}$.

The next layer uses the $20$-$21$-$29$ directions. With $U=(-21,-20)$,
$$
D=19dq,\qquad A=-62dq,\qquad
r=\frac{d(361q^2-124q-1)}{1682},
$$
which is integral for every $q\equiv7\pmod {58}$. The other three signed
directions give quotient classes $25,33,51\pmod {58}$.

The $12$-$35$-$37$ layer is similar. With $U=(-35,12)$,
$$
D=-59dq,\qquad A=-58dq,\qquad
r=\frac{d(3481q^2-116q-1)}{2738},
$$
which is integral for every $q\equiv7\pmod {74}$. The other signed directions
give quotient classes $23,51,67\pmod {74}$.

The $9$-$40$-$41$ layer gives another exact quotient sieve without being folded
into the large combined-period tuple. With $U=(9,-40)$,
$$
D=-98dq,\qquad A=-22dq,\qquad
r=\frac{d(9604q^2-44q-1)}{3362},
$$
which is integral for every $q\equiv13\pmod {82}$. The other signed directions
give quotient classes $29,53,69\pmod {82}$. This catches the former residual
prime multipliers $521$, $1201$, and $1669$.

The combined small-direction sieve has quotient period
$$
\operatorname{lcm}(10,26,34,58,74)=2371330.
$$
The covered quotient-divisor residues are exactly the classes that are
$3$ or $7$ modulo $10$, or $3,7,19,23$ modulo $26$, or $7,13,21,27$ modulo
$34$, or $7,25,33,51$ modulo $58$, or $7,23,51,67$ modulo $74$; this is a set
of $896090$ residue classes modulo $2371330$.
This number is not a search box and not a periodic claim about $n$ itself. It
is only a compact representation of the divisor classes certified by the
directions through the $12$-$35$-$37$ layer. The mod-$82$ layer is kept as a
separate exact family because adding it to the combined tuple would multiply
the period by $41$. These families immediately promote former finite-audit
residuals such as $41$, $61$, $89$, $109$, $181$, $199$, $229$, and $239$ to
infinite divisor families, because those multipliers themselves are divisors
in one of the certified quotient classes.

This gives a more principled route than enlarging boxes: classify the quotient
classes $(m_U,R_U)$ produced by signed Pythagorean directions, then prove that
every multiplier left by the modular skeleton either has a divisor in one of
those classes or belongs to a separate structural family. The current code now
tests this route as a divisor sieve over directions, not as a bounded midpoint
search.

Executable guardrail:

- `minimal_periodic_residue_classes`
- `periodic_residue_union`
- `pythagorean_directions_for_hypotenuse`
- `two_one_ray_complement_divisor_root`
- `two_one_ray_complement_divisor_period`
- `two_one_ray_complement_divisor_sieve_residue_classes`
- `two_one_ray_complement_divisor_sieve_certificate`
- `two_one_ray_hypotenuse_divisor_directions`
- `two_one_ray_hypotenuse_divisor_residue_classes`
- `two_one_ray_hypotenuse_divisor_certificate`
- `two_one_ray_mod_2210_divisor_residues`
- `has_two_one_ray_mod_2210_divisor`
- `two_one_ray_mod_64090_divisor_residues`
- `has_two_one_ray_mod_64090_divisor`
- `two_one_ray_mod_2371330_divisor_residues`
- `has_two_one_ray_mod_2371330_divisor`
- `two_one_ray_mod_thirty_four_divisor_certificate`
- `two_one_ray_mod_thirty_four_divisor_orbit_certificate`
- `two_one_ray_mod_fifty_eight_divisor_certificate`
- `two_one_ray_mod_fifty_eight_divisor_orbit_certificate`
- `two_one_ray_mod_seventy_four_divisor_certificate`
- `two_one_ray_mod_seventy_four_divisor_orbit_certificate`
- `two_one_ray_mod_eighty_two_divisor_certificate`
- `two_one_ray_mod_eighty_two_divisor_orbit_certificate`
- `test_two_one_ray_mod_thirty_four_divisor_family`
- `test_two_one_ray_mod_fifty_eight_divisor_family`
- `test_two_one_ray_mod_seventy_four_divisor_family`
- `test_two_one_ray_mod_eighty_two_divisor_family`
- `test_two_one_ray_complement_divisor_root_formula`
- `test_two_one_ray_hypotenuse_divisor_layer`
- `test_complement_divisor_sieve_residue_compression`

## Divisor-Lift Reduction To Prime Multipliers

There is another multiplicative closure that is independent of the particular
parallel direction used to certify a base multiplier. If $q\mid n$ and
$(2q,q)$ has a two-step certificate with midpoint $P$, then scaling the whole
certificate by $n/q$ gives a certificate for $(2n,n)$:
$$
P\longmapsto \frac{n}{q}P.
$$
Both edge lengths scale by $n/q$, so square lengths remain square. Therefore
the exceptional-ray problem reduces to seed certificates for prime multipliers:
once every prime $p>1$ on the ray is certified, every composite multiplier is
certified by scaling a certified prime divisor.

The helper `two_one_ray_divisor_lift_certificate` makes this closure
executable. It first tries the current exact seed families:

- the mod-$260$ skeleton;
- the mod-$10$, mod-$26$, mod-$34$, mod-$58$, mod-$74$, and mod-$82$
  complement-divisor sieves;
- the promoted square-determinant factor divisor layers;
- the promoted scaled fixed-factor divisor layers;
- the promoted determinant split-factor layers;
- the Fermat double-direction family for primes $p\equiv1\pmod4$;
- the promoted exact base rows.

If none applies directly, it recursively checks proper divisors and scales the
first certified divisor certificate it finds. For instance, $6241=79^2$ is not
a current seed multiplier, but $79$ is certified by an exact ray family, so
scaling the certificate for $(158,79)$ by $79$ certifies $(12482,6241)$.
The newer helper `two_one_ray_prime_divisor_lift_certificate` expresses the
final theorem more directly: for $n>1$ it chooses a prime divisor $p$ of $n$,
uses the structural prime-seed classification for $p$, and scales by $n/p$.
It does not need to search the lattice, enlarge a midpoint box, or walk through
proper divisors recursively.

This is a principled narrowing of the remaining target. Before promoting the
inverse-root layers described next, the multipliers below $2000$ that still
failed the divisor-lift constructor were exactly
$$
\begin{gathered}
269,281,389,509,941,1009,1049,1249,1289,1321,\\
1361,1409,1481,1549,1601,1861,1949,
\end{gathered}
$$
and every one of these is prime. The inverse-root construction below promotes
these diagnostic primes into exact Euclid-parameter seed layers; with those
layers included, the current divisor-lift constructor leaves no unresolved
multiplier $2\le n<2000$ on the exceptional ray. The later square-factor,
scaled-factor, and determinant split-factor promotions extend the executable
empty divisor-lift audit to $2\le n<10000$, and the lift-three square-endpoint
family leaves no unresolved prime seed for $10000\le p<1000000$. The Fermat
double-direction formula closes the remaining prime class, so the final
exceptional-ray mechanism is no longer a larger-box search: prime multipliers
are classified, and composite multipliers are scaled from any certified prime
divisor.

Executable guardrail:

- `two_one_ray_seed_certificate`
- `two_one_ray_divisor_lift_certificate`
- `two_one_ray_divisor_lift_orbit_certificate`
- `two_one_ray_prime_divisor_lift_certificate`
- `two_one_ray_prime_divisor_lift_orbit_certificate`
- `test_two_one_ray_divisor_lift_reduces_remaining_ray_to_primes`

## Inverse-Root Reduction For Exceptional-Ray Primes

The complement-divisor formula can be used in the opposite direction. Instead
of adding more finite boxes, fix a multiplier $p$ and search for Euclid
parameters that make $p$ itself one of the root classes.

Let $m>k>0$ be coprime and of opposite parity. Put
$$
o=m^2-k^2,\qquad e=2mk,\qquad c=m^2+k^2,
$$
and take an odd-first-coordinate signed direction
$$
U=(u,v)=(\sigma o,\tau e),\qquad \sigma,\tau\in\{\pm1\}.
$$
As before, set
$$
A=2u+v,\qquad B=u-2v.
$$
These are the coordinates naturally attached to the ray $(2,1)$: $A$ is the
dot product against the ray and $B$ is the determinant factor. Equivalently,
in Gaussian-integer notation,
$$
A+iB=(2+i)(u-iv).
$$
Therefore
$$
A^2+B^2=5c^2,
$$
and conversely a triple $(A,B,c)$ with this identity reconstructs
$$
u=\frac{2A+B}{5},\qquad v=\frac{A-2B}{5}
$$
when the two displayed numerators are divisible by $5$. Thus a fixed
determinant factor $B$ is a one-dimensional negative-Pell slice
$$
A^2-5c^2=-B^2.
$$

When $\gcd(B,c)=1$, this direction has root
$$
R_{\sigma,\tau}(m,k)\equiv -A(B^2)^{-1}\pmod c,
\qquad R_{\sigma,\tau}(m,k)\equiv1\pmod2.
$$
Therefore every multiplier satisfying
$$
p\equiv R_{\sigma,\tau}(m,k)\pmod {2c}
$$
has the explicit factor-one midpoint
$$
P=
\frac{p^2B^2+2pA-1}{2c^2}\,U.
$$
The divisibility by $c^2$ follows directly from the determinant-slice
identity: if $pB^2+A=ct$, then
$$
B^2(p^2B^2+2pA-1)=(pB^2+A)^2-(A^2+B^2)=c^2(t^2-5),
$$
and $\gcd(B,c)=1$. The parity condition supplies the remaining factor $2$ for
primitive odd-first-coordinate directions.

There is also a useful $p$-facing form. Reducing $A^2+B^2=5c^2$ modulo $c$
and using $A\equiv -pB^2\pmod c$ gives
$$
c\mid p^2B^2+1.
$$
In Euclid parameters this says that $pB$ is one of the canonical square roots
of $-1$ modulo $c$:
$$
pB\equiv \pm m k^{-1}\pmod c.
$$
More explicitly, for
$$
u=s_o(m^2-k^2),\qquad v=s_e(2mk),\qquad s_o,s_e\in\{\pm1\},
$$
one has
$$
B=s_o(m^2-k^2)-2s_e(2mk),
$$
and the quotient root is the odd lift of
$$
p\equiv s_os_e\,m\,k^{-1}B^{-1}\pmod c.
$$
This is the cleanest modular form of the inverse-root condition so far: the
sign is simply whether the two Euclid-leg signs agree.
Equivalently, every primitive Euclid parameter pair $(m,k)$ now gives an exact
four-class quotient divisor family modulo $2c$. For example,
$$
(m,k)=(7,2)\quad\Rightarrow\quad q\equiv31,47,59,75\pmod {106},
$$
which is the $c=53$ layer; and
$$
(m,k)=(6,5)\quad\Rightarrow\quad q\equiv29,53,69,93\pmod {122},
$$
which is the $c=61$ layer. These classes certify, for instance, the former
residual primes $1409,1861$ and $1249,1289$ respectively.
Conversely, if a proposed hypotenuse $c$ divides $p^2B^2+1$, one only has to
check the finitely many lifts of
$$
A\equiv -pB^2\pmod c,\qquad |A|<\sqrt5\,c,
$$
against $A^2+B^2=5c^2$ and the modulo-$5$ direction reconstruction conditions.
So the inverse-root problem for a residual prime can be attacked as a divisor
problem for $p^2B^2+1$, with the Pell slice supplying the compatibility test.

Each fixed-$B$ slice is not merely a bounded search list. Multiplication by the
Pell unit $161+72\sqrt5$ advances the slice:
$$
A' = 161A+360c,\qquad c'=72A+161c,\qquad B'=B.
$$
The choice of this square unit preserves both
$A^2-5c^2=-B^2$ and the modulo-$5$ conditions needed to recover integral
$(u,v)$. Some intermediate Pell rows can be degenerate or fail
$\gcd(B,c)=1$, so the executable successor skips to the next valid root. Thus
a determinant-slice seed yields a Pell orbit of exact quotient classes.

This already connects some formerly separate layers. In the $B=-11$ slice,
the mod-$74$ row
$$
(A,B,c)=(-82,-11,37)
$$
has successor
$$
(A',B',c')=(118,-11,53),
$$
which is the direction $(45,28)$ with root $31\pmod {106}$ and certifies the
former residual prime $1409$ because $1409\equiv31\pmod {106}$. Thus the new
$c=53$ witness is not an isolated larger search hit; it is the next Pell-orbit
root after an already promoted small divisor layer.

The backward square-unit reduction gives a useful diagnostic. Among the
pre-promotion divisor-lift residual primes below $2000$, only $1409$ reduces to an already
promoted small-layer seed in this way. The other inverse-root witnesses in the
table below are reduced roots for their square-unit determinant-slice orbits.
Thus the remaining task has split again: either produce new exact mechanisms
for these reduced determinant-slice seeds, or prove that another independent
family catches the same prime classes.

This is a sharper target than a bounded midpoint search: after the divisor-lift
reduction, it is enough to prove that every remaining prime lies in one of the
negative-Pell determinant slices with the displayed root congruence, or in some
other exact prime family.

The current inverse-root probe catches every pre-promotion divisor-lift residual
prime below $2000$ with Euclid parameter at most $300$:
$$
\begin{array}{c|c|c|c|c}
p & (m,k) & U & c & R\\
\hline
269 & (116,35) & (12231,8120) & 14681 & 269\\
281 & (19,4) & (345,-152) & 377 & 281\\
389 & (15,4) & (209,-120) & 241 & 389\\
509 & (34,19) & (-795,-1292) & 1517 & 509\\
941 & (15,8) & (-161,240) & 289 & 363\\
1009 & (73,62) & (-1485,9052) & 9173 & 1009\\
1049 & (13,8) & (105,-208) & 233 & 117\\
1249 & (6,5) & (-11,-60) & 61 & 29\\
1289 & (6,5) & (11,-60) & 61 & 69\\
1321 & (37,2) & (1365,148) & 1373 & 1321\\
1361 & (41,20) & (-1281,1640) & 2081 & 1361\\
1409 & (7,2) & (45,28) & 53 & 31\\
1481 & (289,266) & (12765,153748) & 154277 & 1481\\
1549 & (17,12) & (145,408) & 433 & 683\\
1601 & (24,19) & (215,912) & 937 & 1601\\
1861 & (7,2) & (45,-28) & 53 & 59\\
1949 & (15,8) & (161,-240) & 289 & 215.
\end{array}
$$
Rows with $R\ne p$ are still exact hits because the criterion is
$p\equiv R\pmod {2c}$. For example, $941\equiv363\pmod {578}$.
The same inverse-root mechanism also catches the three primes left in
$2000\le n<3000$ after the square-factor promotion:
$$
\begin{array}{c|c|c|c|c}
p & (m,k) & U & c & R\\
\hline
2549 & (8,3) & (55,48) & 73 & 67\\
2621 & (8,5) & (39,80) & 89 & 129\\
2729 & (20,1) & (-399,-40) & 401 & 323.
\end{array}
$$
The distinct parameter pairs in these tables are now promoted into exact seed
layers:
$$
\begin{gathered}
(7,2),(6,5),(13,8),(15,4),(15,8),(19,4),(17,12),\\
(24,19),(37,2),(34,19),(41,20),(73,62),(116,35),(289,266),\\
(8,3),(8,5),(20,1).
\end{gathered}
$$
This is an infinite-family promotion, not a finite audit: each pair contributes
its four quotient classes modulo $2(m^2+k^2)$, and divisor-lift scaling then
covers any multiplier with a certified divisor in one of those classes. The
executable audit now verifies that the exceptional-ray divisor-lift constructor
has no remaining failures for $2\le n<3000$.

Executable guardrail:

- `TwoOneRayDeterminantSliceRoot`
- `two_one_ray_determinant_coordinates`
- `euclid_sqrt_minus_one_residues`
- `two_one_ray_signed_euclid_root`
- `two_one_ray_euclid_parameter_roots`
- `two_one_ray_euclid_parameter_residue_classes`
- `two_one_ray_euclid_parameter_certificate`
- `TWO_ONE_RAY_PROMOTED_INVERSE_ROOT_PARAMETERS`
- `two_one_ray_promoted_inverse_root_certificate`
- `two_one_ray_determinant_slice_root`
- `two_one_ray_determinant_factor_roots`
- `two_one_ray_determinant_slice_successor`
- `two_one_ray_determinant_slice_predecessor`
- `two_one_ray_determinant_slice_reduced_root`
- `two_one_ray_determinant_slice_orbit`
- `two_one_ray_determinant_slice_orbit_certificate`
- `two_one_ray_determinant_divisor_root`
- `two_one_ray_determinant_divisor_certificate`
- `two_one_ray_determinant_factor_certificate`
- `TwoOneRayInverseRootWitness`
- `two_one_ray_inverse_root_witness`
- `test_two_one_ray_determinant_slice_root_formula`
- `test_two_one_ray_inverse_root_witness_probe`

## Explicit Base Multipliers On The Exceptional Ray

A finite table of additional exact base certificates gives more scaling
families on the same ray:
$$
\begin{array}{c|c}
n & \text{midpoint for }(2n,n)\\
\hline
3 & (12,-5)\\
29 & (-12,5)\\
41 & (-8,-15)\\
53 & (-20,21)\\
61 & (-10,-24)\\
73 & (-30,16)
\end{array}
$$
Each row is checked by direct square identities. For example, the row $n=3$
uses
$$
12^2+(-5)^2=13^2,\qquad (6-12)^2+(3+5)^2=10^2.
$$
Scaling any row by a positive integer gives a two-step certificate for every
multiple of that base multiplier. Sign changes and coordinate swap again give
the corresponding orbit.

This table was promoted only as a finite list of exact base certificates. It is
not a claim that these are all remaining base multipliers on the ray.

Executable guardrail:

- `EXPLICIT_TWO_ONE_RAY_BASE_CERTIFICATES`
- `two_one_ray_explicit_base_certificate`
- `two_one_ray_explicit_base_orbit_certificate`
- `test_two_one_ray_explicit_base_table`

## Finite Audit On The Exceptional Ray

Combining the exact families already recorded above with a finite table of
additional exact certificates now covers every multiplier
$$
2\le n\le500
$$
on the ray $(2n,n)$. This is a finite audit only; it is not a proof of all
multipliers on the ray.

The additional base rows used only for this finite audit are:
$$
\begin{array}{c|c}
n & \text{midpoint for }(2n,n)\\
\hline
109 & (-42,40)\\
113 & (-14,-48)\\
149 & (-42,-40)\\
181 & (-798,-80)\\
209 & (1150,-96)\\
233 & (-80,-39)\\
241 & (330,-104)\\
269 & (-60,-91)\\
281 & (-110,96)\\
293 & (510,-64)\\
313 & (-760,-39)\\
353 & (-144,17)\\
361 & (-2670,-1424)\\
373 & (-154,72)\\
409 & (680,-111)\\
421 & (-28,-195)\\
449 & (-182,120)\\
461 & (-180,-19)\\
473 & (286,48)
\end{array}
$$
Each row is an exact midpoint and is validated by the square identities in the
certificate checker. Scaling a row covers its multiples, and sign changes plus
coordinate swap give the corresponding orbit.

The bounded search that found these rows remains only a discovery tool. The
promoted claim is the explicit finite table together with the audited range
$2\le n\le500$.

Executable guardrail:

- `EXPLICIT_TWO_ONE_RAY_FINITE_AUDIT_CERTIFICATES`
- `two_one_ray_finite_audit_certificate`
- `two_one_ray_finite_audit_orbit_certificate`
- `test_two_one_ray_finite_audit_to_500`

## Affine Consecutive-Hypotenuse Strip Family

The consecutive-hypotenuse case gives a particularly clean affine strip not
captured by a homogeneous lattice congruence. Fix $m\ge2$ and set
$$
u=2m-1,\qquad v=2m(m-1),\qquad c=m^2+(m-1)^2.
$$
Then $(u,v,c)$ is the Pythagorean triple from consecutive Euclid parameters
$(m,m-1)$.

Let $q,t$ be nonzero integers such that
$$
v\mid q(1-q).
$$
Set
$$
L=\frac{q(1-q)}v,\qquad A=m(m-1)t,\qquad B=uA-q,\qquad
r=L+uqt-2A^2.
$$
Use
$$
P=r(u,v),\qquad Q=(2AB,\ B^2-A^2).
$$
The vector $Q$ is a legal Pythagorean edge vector because it is one of Euclid's
standard forms whenever $A$, $B$, and $B^2-A^2$ are nonzero. The first step is
legal whenever $r\ne0$.

Since
$$
u^2-1=2v,\qquad 2A=vt,\qquad u^2-v=c,
$$
we get
$$
\begin{aligned}
P_y+Q_y
&=vr+B^2-A^2\\
&=v(L+uqt-2A^2)+(uA-q)^2-A^2\\
&=q,
\end{aligned}
$$
and
$$
\begin{aligned}
P_x+Q_x
&=ur+2AB\\
&=u(L+uqt-2A^2)+2A(uA-q)\\
&=uL+(u^2-v)qt\\
&=uL+cqt.
\end{aligned}
$$
Thus
$$
P+Q=\left(cqt+u\frac{q(1-q)}v,\ q\right).
$$

Therefore the displayed affine strip point has distance at most $2$ whenever
$r\ne0$, $B\ne0$, and $B^2-A^2\ne0$.

The quotient-form Lean row
`certificateValid_affineConsecutiveHypotenuseStrip` proves this identity with an
explicit integer $L$ satisfying $q(1-q)=vL$, avoiding any hidden integer-division
assumption.  The executable constructor computes that quotient when
$v\mid q(1-q)$ and applies the same nondegeneracy checks.

The same formula now has a target-facing recognition form. For a requested
target $(g,q)$ with $q\ne0$, the fixed-$m$ strip applies exactly when
$$
v\mid q(1-q)
$$
and
$$
cq\mid g-u\frac{q(1-q)}v.
$$
In that case
$$
t=\frac{g-uq(1-q)/v}{cq},
$$
and the certificate is the affine strip certificate above, including the same
nondegeneracy checks. Coordinate swap gives the symmetric target-facing
recognizer for strips whose fixed coordinate is first rather than second.

Executable guardrail:

- `certificateValid_affineConsecutiveHypotenuseStrip`
- `affine_consecutive_hypotenuse_target_certificate`
- `affine_consecutive_hypotenuse_orbit_certificate`
- `test_affine_consecutive_hypotenuse_target_solver`

The unit-coordinate family is the specialization $q=1$. It gives
$(ct,1)$ for every nonzero $t$, and sign changes plus coordinate swap give the
same conclusion for $(\pm ct,\pm1)$ and $(\pm1,\pm ct)$.
In this specialization $L=0$ and the midpoint is
$$
\left((2m-1)R,\ 2m(m-1)R\right),\qquad
R=(2m-1)t-2(m(m-1)t)^2.
$$
The Lean row `certificateValid_consecutiveHypotenuseUnitCoordinate` proves that
the nondegeneracy conditions $R\ne0$, $B\ne0$, and $B^2-A^2\ne0$ are automatic
for $m\ge2$ and $t\ne0$.

The previous multiple-of-five strip is the first case $m=2$, where $c=5$.

Executable guardrail:

- `affine_consecutive_hypotenuse_certificate`
- `certificateValid_affineConsecutiveHypotenuseStrip`
- `certificateValid_consecutiveHypotenuseUnitCoordinate`
- `consecutive_hypotenuse_unit_coordinate_certificate`
- `unit_coordinate_consecutive_hypotenuse_certificate`
- `unit_coordinate_multiple_of_five_certificate`
- `test_affine_consecutive_hypotenuse_family`
- `test_unit_coordinate_consecutive_hypotenuse_family`
- `test_unit_coordinate_multiple_of_five_family`

## Signed Form Of The Paper's Theorem 3

Let $(a,b,c)$ be a positive Pythagorean triple, let $g,h\ne0$, and choose signs
$s_x,s_y\in\{-1,1\}$. If
$$
(c-s_xa)g=(c+s_yb)h-1,
$$
then
$$
P=(s_xagh,\ s_ybgh)
$$
is a two-step midpoint for the target $(g,h)$.

Indeed,
$$
|OP|^2=a^2g^2h^2+b^2g^2h^2=c^2g^2h^2.
$$
For the second step,
$$
\begin{aligned}
|P-(g,h)|^2
&=(s_xagh-g)^2+(s_ybgh-h)^2\\
&=c^2g^2h^2+2gh(-s_xag-s_ybh)+g^2+h^2.
\end{aligned}
$$
The signed linear relation is equivalent to
$$
-s_xag-s_ybh=c(h-g)-1.
$$
Substitution gives
$$
|P-(g,h)|^2
=c^2g^2h^2+2cgh(h-g)-2gh+g^2+h^2
=(cgh+h-g)^2.
$$
Both coordinate changes in both steps are nonzero: $a,b,g,h$ are nonzero, and
no positive Pythagorean-triple leg is $1$.

This signed formulation matches the examples following Theorem 3 in the paper.
For example:

- $(a,b,c)=(4,3,5)$, $s_x=1$, $s_y=-1$ gives
  $g=2h-1$ and the midpoint $(4gh,-3gh)$.
- $(a,b,c)=(3,4,5)$, $s_x=1$, $s_y=-1$ gives
  $2g=h-1$ and the midpoint $(3gh,-4gh)$.
- $(a,b,c)=(3,4,5)$, $s_x=-1$, $s_y=-1$ gives
  $8g=h-1$ and the midpoint $(-3gh,-4gh)$.
- $(a,b,c)=(8,15,17)$, $s_x=1$, $s_y=-1$ gives
  $9g=2h-1$ and the midpoint $(8gh,-15gh)$.

The same relation can be used as an explicit line generator. For fixed
$(a,b,c)$ and signs, choose a nonzero integer $h$. If
$$
c-s_xa \mid (c+s_yb)h-1,
$$
then
$$
g=\frac{(c+s_yb)h-1}{c-s_xa}
$$
is integral, and if $g\ne0$ the displayed midpoint gives a two-step certificate
for $(g,h)$. This is the parametrized form of the same theorem, not an
additional hypothesis.

The conic-slice divisor strengthening replaces the constant $1$ by any
nonzero divisor $q$ of $gh$:
$$
(c-s_xa)g=(c+s_yb)h-q,\qquad q\mid gh,\qquad gh/q>0.
$$
Then
$$
P=\left(s_xa\frac{gh}{q},\ s_yb\frac{gh}{q}\right)
$$
is a valid two-step midpoint whenever neither step is horizontal or vertical.
This gives a principled enlargement of Theorem 3: the original paper's family
is the subcase $q=1$.

There is also a ray-facing form. For a primitive non-axis ray $(p,q)$ and
target $(pn,qn)$, define
$$
L=(c+s_yb)q-(c-s_xa)p.
$$
Then the divisor in the strengthened theorem is $nL$. Hence the chosen triple
and signs certify every multiplier $n$ for which
$$
L\mid pqn
$$
and the resulting graph steps are nondegenerate. If $|L|=1$, the whole ray is
covered. For example, the slope $(3,1)$ has $L=1$ using
$(a,b,c)=(5,12,13)$ with $s_x=s_y=1$, so every nonzero multiple of $(3,1)$ has
a two-step certificate from this single ray family.

The sign/swapped companion is now promoted as a named full-ray theorem. For
the ray $(1,3)$, take $(a,b,c)=(3,4,5)$ and signs $(1,-1)$. Then
$$
L=(5-4)\cdot3-(5-3)\cdot1=1.
$$
Thus every positive target
$$
T=(n,3n)
$$
has the explicit midpoint
$$
P=(9n,-12n).
$$
Indeed,
$$
(9n)^2+(-12n)^2=(15n)^2,\qquad
(n-9n)^2+(3n+12n)^2=(17n)^2.
$$
The Lean row `certificateValid_oneThreeRayTheorem3` proves the scaled identity
for every nonzero integer multiplier, and sign changes plus coordinate swap
give the full orbit of the $(1,3)$ and $(3,1)$ rays.

The same signed $(3,4,5)$ divisor row actually closes the full unit-divisor
table obtained from the four sign choices. For a positive ray $R=(p,q)$, the
fixed divisor is
$$
L=(5+s_y4)q-(5-s_x3)p.
$$
Solving $L=1$ gives four infinite ray fans:
$$
\begin{array}{c|c|c}
R & (s_x,s_y) & \text{parameter range}\\
\hline
(p,2p+1) & (1,-1) & p\ge1\\
(p,8p+1) & (-1,-1) & p\ge1\\
(9t+4,2t+1) & (1,1) & t\ge0\\
(9t+1,8t+1) & (-1,1) & t\ge0.
\end{array}
$$
For every positive multiplier $n$, the target $nR$ has midpoint
$$
P=(3s_xpqn,\ 4s_ypqn).
$$
The divisor-strengthened Theorem 3 row gives coefficient $pqn$, and the
parametric Lean rows
`certificateValid_threeFourFiveOddSlopeRay`,
`certificateValid_threeFourFiveSteepOddSlopeRay`,
`certificateValid_threeFourFiveWideOddSlopeRay`, and
`certificateValid_threeFourFiveNearDiagonalRay` prove the nondegenerate
certificate identities for the four rows. The Python table constructor
`three_four_five_unit_divisor_ray_certificate` exposes the construction, and
`three_four_five_unit_divisor_ray_orbit_certificate` recognizes the full
sign/swap orbit. The promoted $(1,3)$ ray is the first case of the first row.

The next primitive triple gives a second complete unit-divisor table. For
$(a,b,c)=(5,12,13)$, the fixed divisor is
$$
L=(13+s_y12)q-(13-s_x5)p.
$$
Solving $L=1$ gives
$$
\begin{array}{c|c|c}
R & (s_x,s_y) & \text{parameter range}\\
\hline
(p,8p+1) & (1,-1) & p\ge1\\
(p,18p+1) & (-1,-1) & p\ge1\\
(25t+3,8t+1) & (1,1) & t\ge0\\
(25t+18,18t+13) & (-1,1) & t\ge0.
\end{array}
$$
For every positive multiplier $n$, the target $nR$ has midpoint
$$
P=(5s_xpqn,\ 12s_ypqn).
$$
The Lean rows `certificateValid_fiveTwelveThirteenEightSlopeRay`,
`certificateValid_fiveTwelveThirteenEighteenSlopeRay`,
`certificateValid_fiveTwelveThirteenTwentyFiveEightRay`, and
`certificateValid_fiveTwelveThirteenTwentyFiveEighteenRay` prove the four
parametric identities and nondegeneracy checks. The Python table constructor
`five_twelve_thirteen_unit_divisor_ray_certificate` and orbit recognizer
`five_twelve_thirteen_unit_divisor_ray_orbit_certificate` expose the theorem.

The same signed unit-divisor computation now gives a new table from the
$(8,15,17)$ triple.  Here
$$
L=(17+s_y15)q-(17-s_x8)p.
$$
Solving $L=1$ gives
$$
\begin{array}{c|c|c}
R & (s_x,s_y) & \text{parameter range}\\
\hline
(2t+1,9t+5) & (1,-1) & t\ge0\\
(2t+1,25t+13) & (-1,-1) & t\ge0\\
(32t+7,9t+2) & (1,1) & t\ge0\\
(32t+23,25t+18) & (-1,1) & t\ge0.
\end{array}
$$
For every positive multiplier $n$, the target $nR$ has midpoint
$$
P=(8s_xpqn,\ 15s_ypqn).
$$
The existing Lean theorem `certificateValid_theorem3Divisor` is the formal
kernel for these rows, and the Python constructor
`eight_fifteen_seventeen_unit_divisor_ray_certificate` checks each row against
the generic Theorem 3 divisor constructor.  The orbit recognizer
`eight_fifteen_seventeen_unit_divisor_ray_orbit_certificate` exposes the full
sign/swap theorem slice.

These explicit tables are now instances of a generic signed unit-divisor
progression.  For any positive Pythagorean triple $(a,b,c)$ and signs
$(s_x,s_y)$, set
$$
A=c-s_xa,\qquad B=c+s_yb.
$$
If a positive seed ray $(p_0,q_0)$ satisfies
$$
Bq_0-Ap_0=1,
$$
then every ray
$$
R_t=(p_0+Bt,\ q_0+At),\qquad t\ge0,
$$
has the same unit ray divisor.  Thus every positive multiplier $n$ has midpoint
$$
P=(s_xapqn,\ s_ybpqn),\qquad (p,q)=R_t,
$$
and sign/swap transport gives the full orbit for nonzero multipliers.  The Lean
theorem `certificateValid_theorem3UnitDivisorProgression` packages this
progression by reducing it to `certificateValid_theorem3Divisor`; the Python
recognizer `theorem3_unit_divisor_progression_orbit_certificate` recovers the
multiplier from $By-Ax$.

For primitive triples the seed condition is automatic.  If $d$ divides both
$A=c-s_xa$ and $B=c+s_yb$, then $c\equiv s_xa\pmod d$ and
$c\equiv -s_yb\pmod d$.  The identity $a^2+b^2=c^2$ then gives
$d\mid b^2$ and $d\mid a^2$, so primitivity forces $d=1$.  Hence
$\gcd(A,B)=1$ for every primitive triple and sign choice.  The constructive
seed used by `theorem3_coprime_unit_divisor_seed` is $(1,A+1)$ when $B=1$; when
$B>1$ it takes $p_0\equiv -A^{-1}\pmod B$ with $1\le p_0<B$ and
$q_0=(1+Ap_0)/B$.  This promotes the signed Theorem 3 unit-divisor layer from
small tables to one infinite fan for every primitive Pythagorean triple/sign
row.

There is also a uniform first-row theorem for all consecutive Euclid triples.
For $r\ge1$, set
$$
a=2r+1,\qquad b=2r(r+1),\qquad c=2r^2+2r+1.
$$
Then $a^2+b^2=c^2$, $c-b=1$, and $c-a=2r^2$.  With signs $(1,-1)$, every ray
$$
R=(p,2r^2p+1),\qquad p\ge1,
$$
has fixed divisor
$$
L=(c-b)(2r^2p+1)-(c-a)p=1.
$$
Thus every positive multiplier $n$ has midpoint
$$
P=((2r+1)p(2r^2p+1)n,\ -2r(r+1)p(2r^2p+1)n).
$$
The Lean row `certificateValid_consecutiveEuclidUnitDivisorRay` proves the
identity and nondegeneracy checks for all $r,p>0$, and the Python constructor
`consecutive_euclid_unit_divisor_ray_certificate` plus orbit recognizer expose
the full sign/swap orbit. The cases $r=1,2$ recover the first rows of the
`3-4-5` and `5-12-13` unit-divisor tables; all $r\ge3$ are new infinite fans.

The swapped-leg consecutive-Euclid branch also gives a uniform affine strip. For
$r\ge1$, use
$$
a=2r(r+1),\qquad b=2r+1,\qquad c=2r^2+2r+1.
$$
Then $c-a=1$ and $c-b=2r^2$.  With signs $(1,-1)$, every target
$$
T=(2r^2h-1,\ h),\qquad h\ge1,
$$
has unit divisor and midpoint
$$
P=(2r(r+1)(2r^2h-1)h,\ -(2r+1)(2r^2h-1)h).
$$
The Lean row `certificateValid_consecutiveEuclidAffineStrip` proves the
parametric certificate, while
`consecutive_euclid_affine_strip_certificate` and
`consecutive_euclid_affine_strip_orbit_certificate` expose the strip and its
full sign/swap orbit.  This is the theorem-shaped version of the corresponding
quadratic-strip constructor.

On the exceptional ray $(2,1)$, the same framework gives infinite multiplier
classes such as $3\mid n$ from $(a,b,c)=(12,5,13)$ with signs $(1,-1)$, and
$29\mid n$ from $(15,112,113)$ with signs $(1,1)$; it still does not certify
the primitive obstruction.

Equivalently, a fixed ray divisor has an exact multiplier modulus
$$
M=\frac{|L|}{\gcd(|L|,|pq|)}.
$$
All multipliers divisible by $M$ pass the ray-divisibility test, subject only to
the sign condition $pq\,n/L>0$ and the standard nondegeneracy checks. This is a
more useful object than another box: it asks for residue-class covers of each
primitive ray.

There is also a Pell-type parametrization of a large subfamily of these ray
divisors. Put $m=x+y$ and $n=y$ with $x,y>0$. For the Euclid triple
$$
a=m^2-n^2=x(x+2y),\qquad b=2mn=2y(x+y),\qquad c=m^2+n^2,
$$
and signs $(s_x,s_y)=(1,-1)$, one has
$$
c-a=2y^2,\qquad c-b=x^2,
$$
so the ray divisor becomes
$$
L=qx^2-2py^2.
$$
If the two legs are swapped, the companion branch gives
$$
L=2qy^2-px^2.
$$
Thus, for a primitive ray $(p,q)$, any solution of one of the divisor conditions
$$
qx^2-2py^2\mid pq
\qquad\text{or}\qquad
2qy^2-px^2\mid pq
$$
certifies the primitive target and hence, by scaling, the entire ray. More
certifies the primitive target, subject to the same sign and nondegeneracy
conditions, and hence by scaling certifies the entire ray. More generally the
same $L$ certifies the multiplier class $M\mid n$ above. This turns the ray
problem into a Pell/divisor problem rather than a two-dimensional box search.
For instance, the swapped branch with $(p,q)=(2,1)$ and $(x,y)=(1,2)$ gives
$L=6$ and therefore the exact class $3\mid n$, recovering the midpoint
$(12,-5)$ for $(6,3)$.

There is a useful quadratic-strip corollary obtained by taking the consecutive
Euclid parameters $(n+1,n)$ with $n\ge1$. The resulting hypotenuse is
$$
c_n=2n^2+2n+1.
$$
With legs
$$
a_n=2n(n+1),\qquad b_n=2n+1,
$$
we have
$$
c_n-a_n=1,\qquad c_n-b_n=2n^2.
$$
Using $s_x=1$ and $s_y=-1$ in Theorem 3 gives
$$
g=(c_n-b_n)h-1=2hn^2-1.
$$
Thus every target
$$
(2hn^2-1,\ h),\qquad h\ne0,\ n\ge1,
$$
has a two-step certificate.

Swapping the two legs in the same triple gives
$$
c_n-(2n+1)=2n^2,\qquad c_n-2n(n+1)=1,
$$
and hence the companion family
$$
(g,\ 2gn^2+1),\qquad g\ne0,\ n\ge1.
$$
The sign/swap transport above promotes both formulas to their full symmetry
orbits.

Executable guardrail:

- `theorem3_certificate`
- `theorem3_certificates`
- `theorem3_divisor_certificate`
- `theorem3_line_certificate`
- `theorem3_ray_divisor`
- `theorem3_ray_divisor_certificate`
- `theorem3_ray_divisor_modulus`
- `theorem3_ray_pell_divisor_certificate`
- `one_three_ray_theorem3_certificate`
- `one_three_ray_theorem3_orbit_certificate`
- `three_four_five_unit_divisor_ray_certificate`
- `three_four_five_unit_divisor_ray_orbit_certificate`
- `five_twelve_thirteen_unit_divisor_ray_certificate`
- `five_twelve_thirteen_unit_divisor_ray_orbit_certificate`
- `eight_fifteen_seventeen_unit_divisor_ray_certificate`
- `eight_fifteen_seventeen_unit_divisor_ray_orbit_certificate`
- `theorem3_unit_divisor_progression_certificate`
- `theorem3_unit_divisor_progression_orbit_certificate`
- `theorem3_coprime_unit_divisor_seed`
- `theorem3_coprime_unit_divisor_progression_certificate`
- `theorem3_coprime_unit_divisor_progression_orbit_certificate`
- `consecutive_euclid_unit_divisor_ray_certificate`
- `consecutive_euclid_unit_divisor_ray_orbit_certificate`
- `consecutive_euclid_affine_strip_certificate`
- `consecutive_euclid_affine_strip_orbit_certificate`
- `three_four_five_odd_slope_ray_certificate`
- `three_four_five_odd_slope_ray_orbit_certificate`
- `theorem3_quadratic_strip_certificate`
- `theorem3_quadratic_strip_orbit_certificate`
- `test_paper_theorem3_signed_certificate_examples`
- `test_theorem3_divisor_generalization`
- `test_theorem3_ray_divisor_family`
- `test_theorem3_ray_divisor_modulus`
- `test_theorem3_ray_pell_divisor_family`
- `test_one_three_ray_theorem3_family`
- `test_three_four_five_unit_divisor_ray_table`
- `test_five_twelve_thirteen_unit_divisor_ray_table`
- `test_eight_fifteen_seventeen_unit_divisor_ray_table`
- `test_theorem3_unit_divisor_progression_family`
- `test_theorem3_coprime_unit_divisor_progression_family`
- `test_consecutive_euclid_unit_divisor_ray_family`
- `test_consecutive_euclid_affine_strip_family`
- `test_three_four_five_odd_slope_ray_family`
- `test_paper_theorem3_line_constructor`
- `test_theorem3_quadratic_strip_family`
- `test_paper_theorem3_rejects_non_matching_relations`

## Remaining Gap

The signed Theorem 3 family is an exact infinite family, but it is not yet a
classification. It covers targets satisfying one of the displayed linear
relations produced by a Pythagorean triple and a sign pair. The full conjecture
still needs a proof that every non-axis target outside the exceptional orbit is
covered either by this family or by additional exact two-step constructions.

Bounded searches should continue to be used only to discover or falsify proposed
families. Any family promoted into the proof must have the same kind of algebraic
statement and executable guardrail recorded here.

# Pythagorean Walks: Full Conjecture Progress

Date: 2026-05-28

## Scope

The full conjecture says that the only vertices at graph distance $3$ from
$O=(0,0)$ are
$$
(1,0),\qquad (2,0),\qquad (2,1),
$$
and their images under sign changes and coordinate swap.

This note records proof ingredients for the full conjecture beyond the completed
horizontal-axis subproblem. It is not a proof of the full conjecture.

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

Executable guardrail:

- `positive_divisors`
- `ParallelDirectionFactorWitness`
- `standard_pythagorean_completion_factors`
- `parallel_direction_factor_witness`
- `parallel_direction_standard_completion_certificate`
- `parallel_direction_standard_completion_cover_certificate`
- `unit_coordinate_factor_five_parallel_certificate`
- `unit_coordinate_factor_five_parallel_orbit_certificate`
- `unit_coordinate_parallel_factor_residues`
- `unit_coordinate_parallel_factor_orbit_certificate`
- `ray_multiplier`
- `ray_parallel_factor_residues`
- `ray_parallel_factor_certificate`
- `four_three_factor_five_parallel_certificate`
- `parallel_direction_bounded_factor_cover_certificate`
- `parallel_direction_factor_modulus`
- `parallel_direction_factor_coefficient`
- `parallel_direction_factor_residue_classes`
- `parallel_direction_factor_certificate_residue_classes`
- `parallel_direction_factor_residue_certificate`
- `parallel_direction_factor_certificate`
- `parallel_direction_certificate`
- `parallel_direction_cover_certificate`
- `test_parallel_direction_divisor_reduction`
- `test_parallel_direction_standard_completion_family`
- `test_parallel_direction_standard_completion_cover_probe`
- `test_unit_coordinate_factor_five_parallel_family`
- `test_unit_coordinate_parallel_factor_residue_family`
- `test_ray_parallel_factor_residue_family`
- `test_four_three_factor_five_parallel_congruence_family`
- `test_parallel_direction_bounded_factor_cover_probe`
- `test_parallel_direction_factor_residue_classes`
- `test_parallel_direction_candidate_cover_probe`

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

Executable guardrail:

- `pythagorean_triple_orthogonal_lattice_certificate`
- `test_pythagorean_triple_orthogonal_lattice_family`

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
subject only to the standard strip nondegeneracy conditions. The coordinate
swap and sign-change symmetries give the corresponding families with one
coordinate $\pm1$.

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

The first three small direction layers are:
$$
\begin{array}{c|c|c}
\text{triple} & U & q\text{-classes}\\
\hline
3\text{-}4\text{-}5 & (3,-4),(-3,4) & 3,7\pmod {10}\\
5\text{-}12\text{-}13 & (5,12),(-5,12),(5,-12),(-5,-12)
  & 3,7,19,23\pmod {26}\\
8\text{-}15\text{-}17 & (15,-8),(15,8),(-15,-8),(-15,8)
  & 7,13,21,27\pmod {34}.
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

The combined small-direction sieve has quotient period
$$
\operatorname{lcm}(10,26,34)=2210.
$$
The covered quotient-divisor residues are exactly the classes that are
$3$ or $7$ modulo $10$, or $3,7,19,23$ modulo $26$, or $7,13,21,27$ modulo
$34$; this is a set of $754$ residue classes modulo $2210$.
This number is not a search box and not a periodic claim about $n$ itself. It
is only a compact representation of the divisor classes already certified by
the finite direction set. It immediately promotes former finite-audit
residuals such as $41$, $61$, $89$, and $109$ to infinite divisor families,
because those multipliers themselves are divisors in one of the mod-$34$
classes.

This gives a more principled route than enlarging boxes: classify the quotient
classes $(m_U,R_U)$ produced by signed Pythagorean directions, then prove that
every multiplier left by the modular skeleton either has a divisor in one of
those classes or belongs to a separate structural family. The current code now
tests this route as a divisor sieve over directions, not as a bounded midpoint
search.

Executable guardrail:

- `minimal_periodic_residue_classes`
- `periodic_residue_union`
- `two_one_ray_complement_divisor_period`
- `two_one_ray_complement_divisor_sieve_residue_classes`
- `two_one_ray_complement_divisor_sieve_certificate`
- `two_one_ray_mod_2210_divisor_residues`
- `has_two_one_ray_mod_2210_divisor`
- `two_one_ray_mod_thirty_four_divisor_certificate`
- `two_one_ray_mod_thirty_four_divisor_orbit_certificate`
- `test_two_one_ray_mod_thirty_four_divisor_family`
- `test_complement_divisor_sieve_residue_compression`

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

- `affine_consecutive_hypotenuse_target_certificate`
- `affine_consecutive_hypotenuse_orbit_certificate`
- `test_affine_consecutive_hypotenuse_target_solver`

The unit-coordinate family is the specialization $q=1$. It gives
$(ct,1)$ for every nonzero $t$, and sign changes plus coordinate swap give the
same conclusion for $(\pm ct,\pm1)$ and $(\pm1,\pm ct)$.

The previous multiple-of-five strip is the first case $m=2$, where $c=5$.

Executable guardrail:

- `affine_consecutive_hypotenuse_certificate`
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
a two-step certificate from this single ray family. On the exceptional ray
$(2,1)$, the same framework gives infinite multiplier classes such as $3\mid n$
from $(a,b,c)=(12,5,13)$ with signs $(1,-1)$, and $29\mid n$ from
$(15,112,113)$ with signs $(1,1)$; it still does not certify the primitive
obstruction.

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
- `theorem3_quadratic_strip_certificate`
- `theorem3_quadratic_strip_orbit_certificate`
- `test_paper_theorem3_signed_certificate_examples`
- `test_theorem3_divisor_generalization`
- `test_theorem3_ray_divisor_family`
- `test_theorem3_ray_divisor_modulus`
- `test_theorem3_ray_pell_divisor_family`
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

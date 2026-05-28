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
193 & (117,-44),(140,-51) & g\equiv -86h\pmod {193}
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

For example, using $U=(15,8)$ from the $8$-$15$-$17$ triple and $q=1$ gives
$$
(-6240t^2+217t,\ 1)
$$
for every nonzero integer $t$. Sign changes and coordinate swap give the
corresponding symmetric strip points.

Executable guardrail:

- `euclid_strip_certificate`
- `half_leg_strip_certificate`
- `test_euclid_strip_template`
- `test_half_leg_strip_family`

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

When $U$ comes from consecutive Euclid parameters $(m,m-1)$, so
$$
u=2m-1,\qquad v=2m(m-1),
$$
the quadratic coefficient vanishes because $1+2v-u^2=0$. This recovers the
linear consecutive-hypotenuse family $(ct,1)$ with
$c=m^2+(m-1)^2$.

Executable guardrail:

- `half_leg_unit_coordinate_certificate`
- `test_half_leg_unit_coordinate_family`

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
- `theorem3_line_certificate`
- `theorem3_quadratic_strip_certificate`
- `theorem3_quadratic_strip_orbit_certificate`
- `test_paper_theorem3_signed_certificate_examples`
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

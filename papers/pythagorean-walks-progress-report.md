# Pythagorean Walks On `Z^2`: Current Progress Report

Date: 2026-05-29

This report consolidates the parts of the repository that are currently written
as proofs rather than only as proof-search notes.  It is intended to be read
beside Jan Willemson's paper "Pythagorean walks on `Z^2`"
(`arXiv:2605.20831v1`, 20 May 2026).

The report does not prove the full conjecture.  It records the complete
theorem slices that are now part of this workspace, including:

1. the axis slice;
2. full sign/swap ray and ray-fan slices from the signed Theorem 3 rows;
3. consecutive-Euclid and consecutive-hypotenuse strip slices;
4. unit-coordinate congruence rows from fixed-direction parallel factors and
   orthogonal lattices;
5. the determinant-seven lattice congruence slice;
6. the non-primitive part of the exceptional `(2,1)` ray.

The broader non-axis proof program is summarized at the end, with explicit
separation between theorem-level statements and finite computational guardrails.

## 1. The Graph And Two-Step Certificates

Let `G` be the graph with vertex set `Z^2`.  Two vertices are adjacent when their
difference `(a,b)` satisfies

```text
a != 0, b != 0, and a^2 + b^2 is a square.
```

Such a difference will be called a legal Pythagorean edge.  We write
`O=(0,0)`.

For a target `T=(g,h)`, a two-step certificate is an integer midpoint
`P=(x,y)` such that both differences

```text
P=(x,y),        T-P=(g-x,h-y)
```

are legal Pythagorean edges.  Equivalently,

```text
x != 0, y != 0, g-x != 0, h-y != 0,
x^2 + y^2 is a square,
(g-x)^2 + (h-y)^2 is a square.
```

This is the basic object checked by `Certificate.valid()` in the executable
workspace.

## 2. Symmetry And Scaling

The graph is invariant under independent sign changes of the two coordinates
and under coordinate swap.  Therefore, if `P` certifies `T`, the transformed
midpoint certifies the transformed target.

The graph also has a scaling closure.  If `P` certifies `T` and `k` is a
nonzero integer, then `kP` certifies `kT`: both squared edge lengths are
multiplied by `k^2`, and nonzero coordinate differences remain nonzero.

These two elementary closures are the reason the arguments below are stated for
positive representatives and then promoted to the full sign/swap orbit.

Executable guardrails:

- `sign_swap_certificate`
- `scale_certificate`
- `test_sign_swap_certificate_transport`
- `test_certificate_scaling_preserves_validity`

## 3. Known Distance-Three Orbit

The paper proves that `(1,0)`, `(2,0)`, and `(2,1)` have no two-step path from
the origin.  By the symmetries above, the same lower bound holds for

```text
(+/-1,0), (0,+/-1),
(+/-2,0), (0,+/-2),
(+/-2,+/-1), (+/-1,+/-2).
```

The paper also gives the diameter-three identity

```text
(g,h) = (3g+4h)(3,4) - (3g+4h)(4,3) + (g+h)(4,-3).
```

Each displayed direction is a legal Pythagorean edge direction, and every
nonzero integer multiple of a legal direction is legal.  Omitting zero
coefficients gives a path of length at most three to every target.  Hence the
vertices in the orbit above have exact distance three.

The remaining conjectural task is therefore:

```text
For every g,h != 0 with (|g|,|h|) not in {(1,2),(2,1)},
prove that (g,h) has a two-step certificate.
```

Executable guardrails:

- `known_distance_three_obstruction_cases`
- `theorem1_three_step_path`
- `test_known_exception_symbolic_obstruction_cases`
- `test_theorem1_path_gives_three_step_upper_bound`

## 4. The Axis Theorem

The first complete new theorem in this workspace is the horizontal-axis slice.

**Theorem 4.1.**  For every integer `n >= 3`, the target `(n,0)` has distance at
most two from the origin.

The proof has three cases.

### 4.1. Even Targets

Let `n=2a` with `a>=3`.  Every integer `a>=3` is a leg of an integer right
triangle.

If `a` is odd, then

```text
a^2 + ((a^2-1)/2)^2 = ((a^2+1)/2)^2.
```

If `a=2k` is even, then

```text
(2k)^2 + (k^2-1)^2 = (k^2+1)^2.
```

Choose the corresponding nonzero partner leg `y` and put `P=(a,y)`.  Then

```text
|P|^2 = a^2 + y^2,
|(2a,0)-P|^2 = a^2 + y^2.
```

Both graph edges are legal because `a != 0`, `a != 2a`, and `y != 0`.  Thus
every even target `n>=6` is certified.

The remaining even target in the theorem is `n=4`, where the explicit midpoint

```text
P=(-5,12)
```

works since

```text
(-5)^2 + 12^2 = 13^2,
(4-(-5))^2 + 12^2 = 15^2.
```

### 4.2. Odd Targets

Let `n>=3` be odd and set

```text
alpha = (n-1)/2,     beta = (n+1)/2.
```

Use Euclid triples from consecutive parameter pairs:

```text
(2n+1)^2 + (2n(n+1))^2 = (2n^2+2n+1)^2,
(2n-1)^2 + (2n(n-1))^2 = (2n^2-2n+1)^2.
```

Scale the first triple by `alpha` and the second by `beta`.  Their even legs
become equal:

```text
alpha * 2n(n+1) = beta * 2n(n-1) = n(n^2-1).
```

Define

```text
a = alpha(2n+1),
b = beta(2n-1),
y = n(n^2-1).
```

Then the scaled triples give

```text
a^2 + y^2 is a square,
b^2 + y^2 is a square.
```

Their horizontal legs differ by exactly `n`:

```text
b-a = ((n+1)(2n-1) - (n-1)(2n+1))/2 = n.
```

Therefore

```text
P=(-a,y)
```

certifies `(n,0)`, because the first horizontal displacement has length `a`
and the second has length `b=a+n`.  The edge restrictions hold since
`a>0`, `b>0`, and `y>0`.

This proves Theorem 4.1.

By sign changes and coordinate swap, every horizontal or vertical target with
absolute nonzero coordinate at least three has a two-step certificate.  The
paper's obstruction proof for `(1,0)` and `(2,0)` then completes the
classification of all axis vertices.

Written source:

- `notes/pythagorean-walks-axis-subproblem.md`

Executable guardrails:

- `horizontal_axis_proof_certificate`
- `axis_orbit_proof_certificate`
- `test_horizontal_axis_proof_certificate_case_split`
- `test_axis_orbit_proof_certificate`

## 4.5. The Full `(1,3)` Ray

The signed Theorem 3 divisor row also closes a complete non-axis ray.

**Theorem 4.2.**  For every integer `N` with `|N|>0`, the target `(N,3N)` and
every sign/swap image of it has distance at most two from the origin.

It is enough to prove the positive case.  For `N>0`, put

```text
P=(9N,-12N).
```

Then

```text
(9N)^2 + (-12N)^2 = (15N)^2,
(N-9N)^2 + (3N+12N)^2 = (17N)^2.
```

All coordinate differences are nonzero.  Thus `P` is a two-step certificate for
`(N,3N)`.  The same row is the modulus-one case of the divisor-strengthened
signed Theorem 3 with triple `(3,4,5)` and signs `(1,-1)`, since the ray
divisor is

```text
(5-4)*3 - (5-3)*1 = 1.
```

Sign changes and coordinate swap give the full orbit, including the `(3,1)`
ray.

Executable guardrails:

- `one_three_ray_theorem3_certificate`
- `one_three_ray_theorem3_orbit_certificate`
- `test_one_three_ray_theorem3_family`

## 4.6. The Signed `3-4-5` Unit-Divisor Ray-Fan Table

The preceding ray is the first member of a complete unit-divisor table for the
signed `(3,4,5)` Theorem 3 row.

**Theorem 4.3.**  Let `N` be a nonzero integer.  If `R` is one of

```text
(p,2p+1),      p >= 1,
(p,8p+1),      p >= 1,
(9t+4,2t+1),   t >= 0,
(9t+1,8t+1),   t >= 0,
```

then the target `N R` and every sign/swap image of it has distance at most two
from the origin.

For `N>0`, each row has fixed divisor `L=1` in

```text
L=(5+s_y*4)q - (5-s_x*3)p.
```

The table is:

```text
ray R              signs (s_x,s_y)     midpoint P for target N R
(p,2p+1)           ( 1,-1)              ( 3pqN,-4pqN)
(p,8p+1)           (-1,-1)              (-3pqN,-4pqN)
(9t+4,2t+1)        ( 1, 1)              ( 3pqN, 4pqN)
(9t+1,8t+1)        (-1, 1)              (-3pqN, 4pqN)
```

Here `(p,q)=R`.  Each displayed row satisfies `L=1`, so the
divisor-strengthened Theorem 3 certificate has coefficient `pqN`.  The Lean
rows
`certificateValid_threeFourFiveOddSlopeRay`,
`certificateValid_threeFourFiveSteepOddSlopeRay`,
`certificateValid_threeFourFiveWideOddSlopeRay`, and
`certificateValid_threeFourFiveNearDiagonalRay` prove the four parametric
certificate identities and nondegeneracy checks.  Sign changes and coordinate
swap give the full orbit.

Executable guardrails:

- `certificateValid_threeFourFiveOddSlopeRay`
- `certificateValid_threeFourFiveSteepOddSlopeRay`
- `certificateValid_threeFourFiveWideOddSlopeRay`
- `certificateValid_threeFourFiveNearDiagonalRay`
- `three_four_five_unit_divisor_ray_certificate`
- `three_four_five_unit_divisor_ray_orbit_certificate`
- `test_three_four_five_unit_divisor_ray_table`

## 4.7. The Signed `5-12-13` Unit-Divisor Ray-Fan Table

The same unit-divisor mechanism gives a second explicit table from the
`(5,12,13)` triple.

**Theorem 4.4.**  Let `N` be a nonzero integer.  If `R` is one of

```text
(p,8p+1),           p >= 1,
(p,18p+1),          p >= 1,
(25t+3,8t+1),       t >= 0,
(25t+18,18t+13),    t >= 0,
```

then the target `N R` and every sign/swap image of it has distance at most two
from the origin.

For `N>0`, each row has fixed divisor `L=1` in

```text
L=(13+s_y*12)q - (13-s_x*5)p.
```

The table is:

```text
ray R                 signs (s_x,s_y)     midpoint P for target N R
(p,8p+1)              ( 1,-1)              ( 5pqN,-12pqN)
(p,18p+1)             (-1,-1)              (-5pqN,-12pqN)
(25t+3,8t+1)          ( 1, 1)              ( 5pqN, 12pqN)
(25t+18,18t+13)       (-1, 1)              (-5pqN, 12pqN)
```

Here `(p,q)=R`.  Each row satisfies `L=1`, so the
divisor-strengthened Theorem 3 certificate has coefficient `pqN`.  The Lean
rows `certificateValid_fiveTwelveThirteenEightSlopeRay`,
`certificateValid_fiveTwelveThirteenEighteenSlopeRay`,
`certificateValid_fiveTwelveThirteenTwentyFiveEightRay`, and
`certificateValid_fiveTwelveThirteenTwentyFiveEighteenRay` prove the four
parametric certificate identities and nondegeneracy checks.  Sign changes and
coordinate swap give the full orbit.

Executable guardrails:

- `certificateValid_fiveTwelveThirteenEightSlopeRay`
- `certificateValid_fiveTwelveThirteenEighteenSlopeRay`
- `certificateValid_fiveTwelveThirteenTwentyFiveEightRay`
- `certificateValid_fiveTwelveThirteenTwentyFiveEighteenRay`
- `five_twelve_thirteen_unit_divisor_ray_certificate`
- `five_twelve_thirteen_unit_divisor_ray_orbit_certificate`
- `test_five_twelve_thirteen_unit_divisor_ray_table`

The same calculation also gives a signed `(8,15,17)` unit-divisor table.

**Additional Theorem.**  Let `N` be a nonzero integer.  If `R` is one of

```text
(2t+1,9t+5),          t >= 0,
(2t+1,25t+13),        t >= 0,
(32t+7,9t+2),         t >= 0,
(32t+23,25t+18),      t >= 0,
```

then the target `N R` and every sign/swap image of it has distance at most two
from the origin.

For `N>0`, each row has fixed divisor `L=1` in

```text
L=(17+s_y*15)q - (17-s_x*8)p.
```

The table is:

```text
ray R                 signs (s_x,s_y)     midpoint P for target N R
(2t+1,9t+5)           ( 1,-1)              ( 8pqN,-15pqN)
(2t+1,25t+13)         (-1,-1)              (-8pqN,-15pqN)
(32t+7,9t+2)          ( 1, 1)              ( 8pqN, 15pqN)
(32t+23,25t+18)       (-1, 1)              (-8pqN, 15pqN)
```

Here `(p,q)=R`.  The existing Lean theorem
`certificateValid_theorem3Divisor` is the formal kernel for these rows; the
executable table checks the four parametric identities against the generic
Theorem 3 divisor constructor.  Sign changes and coordinate swap give the full
orbit.

Executable guardrails:

- `eight_fifteen_seventeen_unit_divisor_ray_certificate`
- `eight_fifteen_seventeen_unit_divisor_ray_orbit_certificate`
- `test_eight_fifteen_seventeen_unit_divisor_ray_table`

The tables above are now instances of a single signed unit-divisor progression.

**Generic Progression Theorem.**  Let `(a,b,c)` be a positive Pythagorean triple and let
`sx,sy in {-1,1}`.  Put

```text
A = c - sx*a,       B = c + sy*b.
```

Assume `(p0,q0)` is a positive seed ray satisfying

```text
B*q0 - A*p0 = 1.
```

Then for every `t >= 0`, every nonzero integer `N`, and

```text
R_t = (p0+B*t, q0+A*t),
```

the target `N R_t` and every sign/swap image of it has distance at most two
from the origin.

For `N>0`, write `R_t=(p,q)`.  The midpoint is

```text
P=(sx*a*p*q*N, sy*b*p*q*N).
```

The relation `B*q - A*p = 1` is preserved because the progression adds
`(B,A)` to the seed ray.  Thus the divisor-strengthened Theorem 3 row has
divisor `N` and coefficient `p*q*N`.  The Lean theorem
`certificateValid_theorem3UnitDivisorProgression` packages this arithmetic
progression and calls `certificateValid_theorem3Divisor`; the Python recognizer
recovers the multiplier from `B*y - A*x`.

For primitive triples this progression is always available.  Indeed, if a
positive integer `d` divides both `A=c-sx*a` and `B=c+sy*b`, then
`c == sx*a mod d` and `c == -sy*b mod d`.  Since `a^2+b^2=c^2`, the first
congruence gives `d | b^2` and the second gives `d | a^2`.  Primitivity
therefore forces `d=1`, so `gcd(A,B)=1`.

The canonical positive seed is explicit:

```text
if B=1:  (p0,q0)=(1,A+1),
if B>1:  p0 == -A^(-1) mod B, 1 <= p0 < B, and q0=(1+A*p0)/B.
```

This gives a primitive signed unit-divisor fan for every primitive
Pythagorean triple and every sign choice, not just the small tabulated triples.

Executable guardrails:

- `certificateValid_theorem3UnitDivisorProgression`
- `theorem3_unit_divisor_progression_ray`
- `theorem3_unit_divisor_progression_certificate`
- `theorem3_unit_divisor_progression_orbit_certificate`
- `theorem3_coprime_unit_divisor_seed`
- `theorem3_coprime_unit_divisor_progression_certificate`
- `test_theorem3_unit_divisor_progression_family`
- `test_theorem3_coprime_unit_divisor_progression_family`

## 4.8. The Consecutive-Euclid Unit-Divisor Ray Fan

The table pattern has a uniform first-row form for every consecutive Euclid
triple.

**Theorem 4.5.**  Let `r,p` be integers with `r,p >= 1`, and let `N` be a
nonzero integer.  Put

```text
R=(p,(2r^2)p+1).
```

Then the target `N R` and every sign/swap image of it has distance at most two
from the origin.

For `N>0`, take the consecutive Euclid triple

```text
a=2r+1,      b=2r(r+1),      c=2r^2+2r+1.
```

Since `c-b=1` and `c-a=2r^2`, the signed Theorem 3 ray divisor with signs
`(1,-1)` is

```text
L=(c-b)((2r^2)p+1) - (c-a)p = 1.
```

Thus the midpoint is

```text
P=((2r+1)p((2r^2)p+1)N, -2r(r+1)p((2r^2)p+1)N).
```

The Lean row `certificateValid_consecutiveEuclidUnitDivisorRay` proves this
parametric certificate and the nondegeneracy conditions.  The first cases
`r=1` and `r=2` recover the first rows of the signed `3-4-5` and `5-12-13`
tables; every `r>=3` gives a new infinite ray fan.

Executable guardrails:

- `certificateValid_consecutiveEuclidUnitDivisorRay`
- `consecutive_euclid_unit_divisor_ray_certificate`
- `consecutive_euclid_unit_divisor_ray_orbit_certificate`
- `test_consecutive_euclid_unit_divisor_ray_family`

## 4.9. The Swapped-Leg Consecutive-Euclid Affine Strip

The swapped-leg branch of the same consecutive Euclid triple gives an affine
strip rather than a ray.

**Theorem 4.6.**  Let `r,h` be integers with `r,h >= 1`.  Then the target
`(2r^2h-1,h)` and every sign/swap image of it has distance at most two from the
origin.

For the consecutive Euclid triple

```text
a=2r(r+1),      b=2r+1,      c=2r^2+2r+1,
```

we have `c-a=1` and `c-b=2r^2`.  With signs `(1,-1)`, the signed Theorem 3
unit-divisor relation is

```text
(c-a)(2r^2h-1) = (c-b)h - 1.
```

Thus the midpoint is

```text
P=(2r(r+1)(2r^2h-1)h, -(2r+1)(2r^2h-1)h).
```

The Lean row `certificateValid_consecutiveEuclidAffineStrip` proves this
parametric certificate and the nondegeneracy checks.  Sign changes and
coordinate swap give the full orbit.

Executable guardrails:

- `certificateValid_consecutiveEuclidAffineStrip`
- `consecutive_euclid_affine_strip_certificate`
- `consecutive_euclid_affine_strip_orbit_certificate`
- `test_consecutive_euclid_affine_strip_family`

## 4.10. The Affine Consecutive-Hypotenuse Strip

The consecutive-hypotenuse Euclid triple gives another infinite affine strip,
now promoted to a Lean row.  For `m >= 2`, set

```text
u=2m-1,      v=2m(m-1),      c=m^2+(m-1)^2.
```

Let `q,t` be nonzero integers with `v | q(1-q)`, and write
`ell = q(1-q)/v`.  Put

```text
A=m(m-1)t,      B=uA-q,      r=ell+uqt-2A^2.
```

Whenever `r`, `B`, and `B^2-A^2` are nonzero, the target

```text
(cqt + u*ell, q)
```

has midpoint `r(u,v)` and second edge `(2AB, B^2-A^2)`.  Both are
Pythagorean: `(u,v,c)` is the consecutive-hypotenuse triple and the second edge
is Euclid's `(2AB, B^2-A^2)` form.

The Lean row `certificateValid_affineConsecutiveHypotenuseStrip` proves the
quotient-form certificate identity and nondegeneracy hypotheses.  The executable
constructors retain the target-facing recognizer and coordinate-swap wrapper.

Executable guardrails:

- `certificateValid_affineConsecutiveHypotenuseStrip`
- `affine_consecutive_hypotenuse_certificate`
- `affine_consecutive_hypotenuse_target_certificate`
- `affine_consecutive_hypotenuse_orbit_certificate`
- `test_affine_consecutive_hypotenuse_family`
- `test_affine_consecutive_hypotenuse_target_solver`

## 4.11. The Consecutive-Hypotenuse Unit-Coordinate Subline

The unit-coordinate specialization of Section 4.10 is now a named infinite
slice.  For `m >= 2`, let

```text
c=m^2+(m-1)^2,      u=2m-1,      v=2m(m-1).
```

Then every nonzero integer `t` gives a two-step certificate for `(ct,1)`.
The midpoint is

```text
((2m-1)R, 2m(m-1)R),
R=(2m-1)t - 2(m(m-1)t)^2.
```

The second edge is Euclid's

```text
(2AB, B^2-A^2),      A=m(m-1)t,      B=(2m-1)A-1.
```

The Lean row `certificateValid_consecutiveHypotenuseUnitCoordinate` proves that
the affine-strip nondegeneracy hypotheses are automatic for `q=1` and `t != 0`.
The Python wrapper `unit_coordinate_consecutive_hypotenuse_certificate` gives
the sign/swap orbit; the case `m=2` recovers the multiple-of-five
unit-coordinate family.

Executable guardrails:

- `certificateValid_consecutiveHypotenuseUnitCoordinate`
- `consecutive_hypotenuse_unit_coordinate_certificate`
- `unit_coordinate_consecutive_hypotenuse_certificate`
- `unit_coordinate_multiple_of_five_certificate`
- `test_unit_coordinate_consecutive_hypotenuse_family`
- `test_unit_coordinate_multiple_of_five_family`

## 4.12. The Half-Leg Unit-Coordinate Row

The generic half-leg strip also gives a Lean-backed unit-coordinate theorem.
Let `(u,4z)` be a Pythagorean edge direction with `u` odd and `u,z != 0`.  For
every nonzero integer `t`, put

```text
A=2zt,      B=uA-1,      R=ut-z(u^2-1)t^2.
```

Then the target

```text
(uR+2AB, 1)
```

has midpoint `(uR,4zR)`.  The second edge is `(2AB,B^2-A^2)`, so it is a
Pythagorean edge by Euclid's formula.  The parity constraints make the usual
strip nondegeneracy automatic: `R` cannot vanish because it would force an odd
integer to equal an even one, and `B-A` and `B+A` are odd.

The Lean row `certificateValid_halfLegUnitCoordinate` proves the full
parametric row.  The executable target-facing solver recognizes the same
quadratic family and the orbit wrapper applies sign changes and coordinate
swap.

Executable guardrails:

- `certificateValid_halfLegUnitCoordinate`
- `half_leg_unit_coordinate_certificate`
- `half_leg_unit_coordinate_target_certificate`
- `half_leg_unit_coordinate_orbit_certificate`
- `test_half_leg_unit_coordinate_family`
- `test_half_leg_unit_coordinate_target_solver`

## 4.13. The Factor-Five Unit-Coordinate Congruence Row

The first nonstandard fixed-direction parallel-factor unit-coordinate family is
also now Lean-backed. For every integer `t`, set

```text
h=25t+17,      r=40t^2+55t+19.
```

Then `(1,h)` has midpoint `(4r,3r)`.  The second edge is

```text
(1-4r, h-3r),
```

and its squared length is

```text
(5(40t^2+52t+17))^2.
```

The Lean row `certificateValid_unitCoordinateFactorFiveParallel` proves the
parametric identity and nondegeneracy checks.  This is exactly the `(4,3)`
fixed-direction parallel-factor construction with factor `5`; the Python orbit
wrapper gives all sign/swap images.

Executable guardrails:

- `certificateValid_unitCoordinateFactorFiveParallel`
- `unit_coordinate_factor_five_parallel_certificate`
- `unit_coordinate_factor_five_parallel_orbit_certificate`
- `test_unit_coordinate_factor_five_parallel_family`

## 4.14. The Factor-Four Unit-Coordinate Congruence Row

The companion fixed-direction parallel-factor row uses direction `(-3,-4)` and
factor `4`.  For every integer `t`, set

```text
h=20t+12,      r=18t^2+16t+3.
```

Then `(1,h)` has midpoint `(-3r,-4r)`.  The second edge is

```text
(1+3r, h+4r),
```

with squared length

```text
(90t^2+96t+26)^2.
```

The Lean row `certificateValid_unitCoordinateFactorFourParallel` proves the
parametric identity and nondegeneracy checks.  The Python constructor exposes
the same row and the orbit wrapper gives all sign/swap images.

Executable guardrails:

- `certificateValid_unitCoordinateFactorFourParallel`
- `unit_coordinate_factor_four_parallel_certificate`
- `unit_coordinate_factor_four_parallel_orbit_certificate`
- `test_unit_coordinate_factor_four_parallel_family`

## 4.15. The One-Mod-Five Unit-Coordinate Congruence Row

The factor-one fixed-direction parallel-factor row with direction `(4,-3)`
closes an entire unit-coordinate residue class modulo `5`. For every integer
`t`, set

```text
h=5t+1,      r=8t^2+5t+1.
```

Then `(1,h)` has midpoint `(4r,-3r)`. The second edge is

```text
(1-4r, h+3r),
```

with squared length

```text
(40t^2+28t+5)^2.
```

The Lean row `certificateValid_unitCoordinateOneModFiveParallel` proves the
parametric identity and nondegeneracy checks. The Python constructor exposes
the same row and the orbit wrapper gives all sign/swap images.

Executable guardrails:

- `certificateValid_unitCoordinateOneModFiveParallel`
- `unit_coordinate_one_mod_five_parallel_certificate`
- `unit_coordinate_one_mod_five_parallel_orbit_certificate`
- `test_unit_coordinate_one_mod_five_parallel_family`

## 4.16. The Seven-Mod-Ten Unit-Coordinate Congruence Row

The factor-one fixed-direction parallel-factor row with direction `(3,4)`
closes the odd part of the `h ≡ 2,3 mod 5` unit-coordinate layer.

For every integer `t`, set

```text
h=10t+7,      r=18t^2+22t+7.
```

Then `(1,h)` has midpoint

```text
P=(3r,4r).
```

The first edge is legal.  Indeed,

```text
|P|^2=(3r)^2+(4r)^2=(5r)^2,
```

and `r` is positive for every integer `t`, since

```text
72r=(36t+22)^2+20.
```

The second displacement is

```text
(1,h)-P=(1-3r,h-4r).
```

Its two coordinates are nonzero because

```text
1-3r       = -2(3t+2)(9t+5),
h-4r       = -3(2t+1)(12t+7),
```

and none of the four displayed linear factors can vanish at an integer `t`.
A direct expansion gives the square-length identity

```text
(1-3r)^2+(h-4r)^2=(90t^2+102t+29)^2.
```

Thus `P` is a two-step certificate for `(1,10t+7)`.

By the sign/swap transport from Section 2, the same proof gives every
sign/swap image.  In particular, changing the sign of the second coordinate
changes `10t+7` into a number congruent to `3 mod 10`, so the orbit form covers
both unit-coordinate classes `h ≡ 7` and `h ≡ 3 mod 10`.

This written proof is the prose version of the Lean theorem
`certificateValid_unitCoordinateSevenModTenParallel`, which proves the
parametric square identity and all nondegeneracy checks.  The orbit step uses
the same sign/swap proof infrastructure as Section 2
(`certificateValid_signedSwapPoint` and the Python `sign_swap_certificate`).
The Python constructor exposes the base row, and the orbit wrapper applies
those existing transport proofs to all sign/swap images.

Executable guardrails:

- `certificateValid_unitCoordinateSevenModTenParallel`
- `unit_coordinate_seven_mod_ten_parallel_certificate`
- `unit_coordinate_seven_mod_ten_parallel_orbit_certificate`
- `test_unit_coordinate_seven_mod_ten_parallel_family`

## 4.17. The Factor-Twenty-Five Unit-Coordinate Congruence Row

The next signed `3-4-5` fixed-direction row uses direction `(4,-3)` and
factor `25`.  It reaches the even part of the remaining `h ≡ 2,3 mod 5`
unit-coordinate layer.

For every integer `t`, set

```text
h=25t+18,      r=8t^2+9t+2.
```

Then `(1,h)` has midpoint

```text
P=(4r,-3r).
```

The first edge is legal because `|P|^2=(5r)^2`, and `r>0` for every integer
`t`: if `t>=0` this is immediate from `8t^2+9t+2`, while if `t<=-1` then

```text
r=8(t+1)^2-7(t+1)+1.
```

The second displacement is

```text
(1,h)-P=(1-4r,h+3r).
```

Its coordinates are nonzero because

```text
1-4r        = -(4t+1)(8t+7),
h+3r        = 4(2t+3)(3t+2),
```

and no displayed linear factor has an integer zero.  A direct expansion gives

```text
(1-4r)^2+(h+3r)^2=(5(8t^2+12t+5))^2.
```

Thus `P` is a two-step certificate for `(1,25t+18)`.  Sign/swap transport also
covers the congruence class `h ≡ 7 mod 25`, including further even residual
unit-coordinate targets outside the earlier mod-20 factor-four rows.

The Lean theorem `certificateValid_unitCoordinateFactorTwentyFiveParallel`
proves the parametric square identity and nondegeneracy checks.  The Python
constructor exposes the base row, and the orbit wrapper applies the existing
sign/swap transport.

Executable guardrails:

- `certificateValid_unitCoordinateFactorTwentyFiveParallel`
- `unit_coordinate_factor_twenty_five_parallel_certificate`
- `unit_coordinate_factor_twenty_five_parallel_orbit_certificate`
- `test_unit_coordinate_factor_twenty_five_parallel_family`

## 4.18. The Twenty-Two-Mod-Twenty-Five Unit-Coordinate Row

The companion factor-five row uses direction `(-4,-3)` and factor `5`.  It
closes the congruence class `h ≡ 22 mod 25` with one degenerate fixed-factor
parameter that is already covered by Section 4.16.

For every integer `t != -1`, set

```text
h=25t+22,      r=40t^2+65t+26.
```

Then `(1,h)` has midpoint

```text
P=(-4r,-3r).
```

The first edge is legal because `|P|^2=(5r)^2`, and `r>0` for every admissible
integer `t`. The second displacement is

```text
(1,h)-P=(1+4r,h+3r).
```

Its coordinates are nonzero because

```text
1+4r        = 5(4t+3)(8t+7),
h+3r        = 20(t+1)(6t+5),
```

where the factor `t+1` is nonzero by the hypothesis `t != -1`. A direct
expansion gives

```text
(1+4r)^2+(h+3r)^2=(5(40t^2+68t+29))^2.
```

The missing fixed-factor parameter is `t=-1`, giving target `(1,-3)`, and
Section 4.16 already certifies it. Thus the orbit wrapper covers every
sign/swap image of `h ≡ 22 mod 25`; sign transport also gives the class
`h ≡ 3 mod 25`.

The Lean theorem
`certificateValid_unitCoordinateTwentyTwoModTwentyFiveParallel` proves the
nondegenerate fixed row. The Python orbit wrapper composes it with the
seven-mod-ten fallback at the single degenerate parameter.

Executable guardrails:

- `certificateValid_unitCoordinateTwentyTwoModTwentyFiveParallel`
- `unit_coordinate_twenty_two_mod_twenty_five_parallel_certificate`
- `unit_coordinate_twenty_two_mod_twenty_five_parallel_orbit_certificate`
- `test_unit_coordinate_twenty_two_mod_twenty_five_parallel_family`

## 4.19. The Promoted Unit-Coordinate Mod-100 Cover

The preceding promoted rows can be composed into a single infinite residue
cover.  Let `T` be a unit-coordinate target: up to sign and coordinate swap,
write it as `(1,h)`.  If `h != 0` and

```text
h mod 100 notin {2, 38, 62, 98},
```

then `T` has a two-step certificate.

The executable dispatcher
`unit_coordinate_promoted_mod_hundred_certificate` is deliberately small: it
first rejects the zero coordinate and the four residual classes, then tries the
already promoted unit-coordinate constructors:

```text
multiple-of-five,
factor-five,
factor-four,
one-mod-five,
seven-mod-ten,
factor-twenty-five,
twenty-two-mod-twenty-five.
```

Each branch is backed by a parametric Lean row or by an already documented
specialization.  The test `test_unit_coordinate_promoted_mod_hundred_cover`
checks the exact residue discharge modulo `100` and sign/swap transport.  This
is an infinite theorem slice, not a target-box audit: the finite computation is
only the residue-class selection over already-parametric constructors.

The four classes

```text
2, 38, 62, 98 mod 100
```

are now the remaining unit-coordinate residue classes for this proof program.
They include the known obstruction orbit at `h=±2`, but the residue classes
themselves still contain non-obstruction targets needing a separate mechanism.

Executable guardrails:

- `UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES`
- `unit_coordinate_promoted_mod_hundred_certificate`
- `test_unit_coordinate_promoted_mod_hundred_cover`

## 4.20. Orthogonal Seeds In The Four Residual Classes

The orthogonal lattice construction also supplies explicit infinite seed rows
inside all four residual mod-100 classes left by Section 4.19.  In fact, the
single `(8,15,17)` row `h ≡ 38 mod 289` meets all four classes once the period
is refined to `100*17^2 = 28900`.  The rows are:

```text
h ≡ 22002  mod 28900,  triple (8,15,17),
h ≡ 38     mod 28900,  triple (8,15,17),
h ≡ 4662   mod 28900,  triple (8,15,17),
h ≡ 11598  mod 28900,  triple (8,15,17).
```

The first column of residues modulo `100` is respectively

```text
2, 38, 62, 98.
```

Thus each of the four residual classes now contains a named infinite
orthogonal-lattice subfamily.  The proof mechanism is uniform: for a triple
`(a,b,c)`, the congruence

```text
h ≡ b*a^(-1) mod c^2
```

puts `(1,h)` in the lattice spanned by `(a,b)` and `(-b,a)`.  The displayed
period is `100c^2`, so each selected intersection remains inside its mod-100
residual class.  The existing Lean Cramer/lattice rows prove the certificate
once the integer coefficients are known.

The executable wrapper `unit_coordinate_residual_orthogonal_seed_certificate`
checks exactly these four rows and then applies sign/swap transport.

Executable guardrails:

- `UNIT_COORDINATE_RESIDUAL_ORTHOGONAL_SEED_ROWS`
- `unit_coordinate_residual_orthogonal_seed_certificate`
- `test_unit_coordinate_residual_orthogonal_seed_rows`

### 4.20.1. A Factor-Two Residual Enlargement

The fixed-direction parallel-factor construction gives a denser
unit-coordinate slice through the same residual layer.  Use the legal direction
`(15,8)` of length `17` and the factor `2`.  For every integer `t`, set

```text
h = 34t + 26,
r = 225t^2 + 338t + 127.
```

Then

```text
P = (15r, 8r)
```

certifies `(1,h)`.  The first step has length `17r`, and a direct expansion
gives

```text
(1-15r)^2 + (h-8r)^2 = (3825t^2 + 5730t + 2146)^2.
```

The nonzero checks factor as

```text
1-15r = -(45t+34)(75t+56),
h-8r = -30(4t+3)(15t+11),
```

so no integer parameter degenerates.  This is exactly the
`parallel_direction_factor_certificate` row for direction `(15,8)` and factor
`2`; the congruence class is `h ≡ 26 mod 34`, with sign transport adding
`h ≡ 8 mod 34`.

The fixed row intersects the four mod-100 residual classes as

```text
2  mod 100: h ≡ 502 mod 1700,
38 mod 100: h ≡ 638 mod 1700,
62 mod 100: h ≡ 162 mod 1700,
98 mod 100: h ≡ 298 mod 1700.
```

Executable guardrails:

- `certificateValid_unitCoordinateFifteenEightFactorTwoParallel`
- `UNIT_COORDINATE_FIFTEEN_EIGHT_FACTOR_TWO_RESIDUAL_ROWS`
- `unit_coordinate_fifteen_eight_factor_two_parallel_certificate`
- `unit_coordinate_fifteen_eight_factor_two_parallel_orbit_certificate`
- `test_unit_coordinate_fifteen_eight_factor_two_parallel_family`

### 4.20.2. A Factor-One Residual Row

The same fixed-direction mechanism gives a coprime-period residual row from
the legal direction `(-12,-35)` of length `37`.  For every integer `t`, set

```text
h = 37t + 25,
r = 72t^2 + 85t + 25.
```

Then

```text
P = (-12r, -35r)
```

certifies `(1,h)`.  A direct expansion gives

```text
(1+12r)^2 + (h+35r)^2 = (2664t^2 + 3180t + 949)^2.
```

The nonzero checks factor as

```text
1+12r = (12t+7)(72t+43),
h+35r = 12(5t+3)(42t+25),
```

so no integer parameter degenerates.  This is exactly the
`parallel_direction_factor_certificate` row for direction `(-12,-35)` and
factor `1`; the congruence class is `h ≡ 25 mod 37`.

Since `gcd(37,100)=1`, this single fixed row intersects all four mod-100
residual classes as

```text
2  mod 100: h ≡ 802  mod 3700,
38 mod 100: h ≡ 1838 mod 3700,
62 mod 100: h ≡ 62   mod 3700,
98 mod 100: h ≡ 1098 mod 3700.
```

Executable guardrails:

- `certificateValid_unitCoordinateTwelveThirtyFiveFactorOneParallel`
- `UNIT_COORDINATE_TWELVE_THIRTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_twelve_thirty_five_factor_one_parallel_certificate`
- `unit_coordinate_twelve_thirty_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_twelve_thirty_five_factor_one_parallel_family`

### 4.20.3. A Forty-Nine Factor-One Residual Row

The legal direction `(40,9)` of length `41` gives another factor-one
unit-coordinate row.  For every integer `t`, set

```text
h = 41t + 23,
r = 800t^2 + 889t + 247.
```

Then

```text
P = (40r, 9r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-40r)^2 + (h-9r)^2 = (32800t^2 + 36440t + 10121)^2.
```

The nonzero checks are

```text
1-40r = -(160t+89)(200t+111),
h-9r = -40(9t+5)(20t+11),
3200r = (1600t+889)^2 + 79.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(40,9)` and factor
`1`; the congruence class is `h ≡ 23 mod 41`.

Since `gcd(41,100)=1`, this row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 802  mod 4100,
38 mod 100: h ≡ 638  mod 4100,
62 mod 100: h ≡ 3262 mod 4100,
98 mod 100: h ≡ 3098 mod 4100.
```

Executable guardrails:

- `certificateValid_unitCoordinateFortyNineFactorOneParallel`
- `UNIT_COORDINATE_FORTY_NINE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_forty_nine_factor_one_parallel_certificate`
- `unit_coordinate_forty_nine_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_forty_nine_factor_one_parallel_family`

### 4.20.4. A Twenty-Eight Forty-Five Factor-One Row

The legal direction `(28,45)` of length `53` gives another coprime-period
unit-coordinate row.  For every integer `t`, set

```text
h = 53t + 10,
r = 392t^2 + 125t + 10.
```

Then

```text
P = (28r, 45r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-28r)^2 + (h-45r)^2 = (20776t^2 + 6580t + 521)^2.
```

The nonzero checks are

```text
1-28r = -(56t+9)(196t+31),
h-45r = -4(63t+10)(70t+11),
1568r = (784t+125)^2 + 55.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(28,45)` and factor
`1`; the congruence class is `h ≡ 10 mod 53`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 3402 mod 5300,
38 mod 100: h ≡ 4038 mod 5300,
62 mod 100: h ≡ 4462 mod 5300,
98 mod 100: h ≡ 5098 mod 5300.
```

Executable guardrails:

- `certificateValid_unitCoordinateTwentyEightFortyFiveFactorOneParallel`
- `UNIT_COORDINATE_TWENTY_EIGHT_FORTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_twenty_eight_forty_five_factor_one_parallel_certificate`
- `unit_coordinate_twenty_eight_forty_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_twenty_eight_forty_five_factor_one_parallel_family`

### 4.20.5. A Sixty-Eleven Factor-One Row

The legal direction `(60,11)` of length `61` continues the coprime-period
unit-coordinate residual pattern.  For every integer `t`, set

```text
h = 61t + 39,
r = 1800t^2 + 2291t + 729.
```

Then

```text
P = (60r, 11r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-60r)^2 + (h-11r)^2 = (109800t^2 + 139740t + 44461)^2.
```

The nonzero checks are

```text
1-60r = -(300t+191)(360t+229),
h-11r = -60(11t+7)(30t+19),
7200r = (3600t+2291)^2 + 119.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(60,11)` and factor
`1`; the congruence class is `h ≡ 39 mod 61`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 5102 mod 6100,
38 mod 100: h ≡ 3638 mod 6100,
62 mod 100: h ≡ 2662 mod 6100,
98 mod 100: h ≡ 1198 mod 6100.
```

Executable guardrails:

- `certificateValid_unitCoordinateSixtyElevenFactorOneParallel`
- `UNIT_COORDINATE_SIXTY_ELEVEN_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_sixty_eleven_factor_one_parallel_certificate`
- `unit_coordinate_sixty_eleven_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_sixty_eleven_factor_one_parallel_family`

### 4.20.6. A Forty-Eight Fifty-Five Factor-One Row

The legal direction `(48,55)` of length `73` gives another coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 73t + 31,
r = 1152t^2 + 943t + 193.
```

Then

```text
P = (48r, 55r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-48r)^2 + (h-55r)^2 = (84096t^2 + 68784t + 14065)^2.
```

The nonzero checks are

```text
1-48r = -(144t+59)(384t+157),
h-55r = -24(22t+9)(120t+49),
4608r = (2304t+943)^2 + 95.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(48,55)` and factor
`1`; the congruence class is `h ≡ 31 mod 73`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 2002 mod 7300,
38 mod 100: h ≡ 4338 mod 7300,
62 mod 100: h ≡ 3462 mod 7300,
98 mod 100: h ≡ 5798 mod 7300.
```

Executable guardrails:

- `certificateValid_unitCoordinateFortyEightFiftyFiveFactorOneParallel`
- `UNIT_COORDINATE_FORTY_EIGHT_FIFTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_forty_eight_fifty_five_factor_one_parallel_certificate`
- `unit_coordinate_forty_eight_fifty_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_forty_eight_fifty_five_factor_one_parallel_family`

### 4.20.7. An Eighty-Thirty-Nine Factor-One Row

The legal direction `(80,39)` of length `89` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 89t + 71,
r = 3200t^2 + 5071t + 2009.
```

Then

```text
P = (80r, 39r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-80r)^2 + (h-39r)^2 = (284800t^2 + 451280t + 178769)^2.
```

The nonzero checks are

```text
1-80r = -(400t+317)(640t+507),
h-39r = -40(24t+19)(130t+103),
12800r = (6400t+5071)^2 + 159.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(80,39)` and factor
`1`; the congruence class is `h ≡ 71 mod 89`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 7102 mod 8900,
38 mod 100: h ≡ 338 mod 8900,
62 mod 100: h ≡ 1762 mod 8900,
98 mod 100: h ≡ 3898 mod 8900.
```

Executable guardrails:

- `certificateValid_unitCoordinateEightyThirtyNineFactorOneParallel`
- `UNIT_COORDINATE_EIGHTY_THIRTY_NINE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_eighty_thirty_nine_factor_one_parallel_certificate`
- `unit_coordinate_eighty_thirty_nine_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_eighty_thirty_nine_factor_one_parallel_family`

### 4.20.8. A Seventy-Two Sixty-Five Factor-One Row

The legal direction `(72,65)` of length `97` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 97t + 78,
r = 2592t^2 + 4121t + 1638.
```

Then

```text
P = (72r, 65r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-72r)^2 + (h-65r)^2 = (251424t^2 + 399672t + 158833)^2.
```

The nonzero checks are

```text
1-72r = -(288t+229)(648t+515),
h-65r = -24(39t+31)(180t+143),
10368r = (5184t+4121)^2 + 143.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(72,65)` and factor
`1`; the congruence class is `h ≡ 78 mod 97`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 9002 mod 9700,
38 mod 100: h ≡ 7838 mod 9700,
62 mod 100: h ≡ 7062 mod 9700,
98 mod 100: h ≡ 5898 mod 9700.
```

Executable guardrails:

- `certificateValid_unitCoordinateSeventyTwoSixtyFiveFactorOneParallel`
- `UNIT_COORDINATE_SEVENTY_TWO_SIXTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_seventy_two_sixty_five_factor_one_parallel_certificate`
- `unit_coordinate_seventy_two_sixty_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_seventy_two_sixty_five_factor_one_parallel_family`

### 4.20.9. A Twenty-Ninety-Nine Factor-One Row

The legal direction `(20,99)` of length `101` gives another coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 101t + 60,
r = 200t^2 + 219t + 60.
```

Then

```text
P = (20r, 99r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-20r)^2 + (h-99r)^2 = (20200t^2 + 22020t + 6001)^2.
```

The nonzero checks are

```text
1-20r = -(20t+11)(200t+109),
h-99r = -20(11t+6)(90t+49),
800r = (400t+219)^2 + 39.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(20,99)` and factor
`1`; the congruence class is `h ≡ 60 mod 101`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 4302 mod 10100,
38 mod 100: h ≡ 7938 mod 10100,
62 mod 100: h ≡ 262 mod 10100,
98 mod 100: h ≡ 3898 mod 10100.
```

Executable guardrails:

- `certificateValid_unitCoordinateTwentyNinetyNineFactorOneParallel`
- `UNIT_COORDINATE_TWENTY_NINETY_NINE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_twenty_ninety_nine_factor_one_parallel_certificate`
- `unit_coordinate_twenty_ninety_nine_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_twenty_ninety_nine_factor_one_parallel_family`

### 4.20.10. A Sixty-Ninety-One Factor-One Row

The legal direction `(60,91)` of length `109` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 109t + 82,
r = 1800t^2 + 2659t + 982.
```

Then

```text
P = (60r, 91r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-60r)^2 + (h-91r)^2 = (196200t^2 + 289740t + 106969)^2.
```

The nonzero checks are

```text
1-60r = -(180t+133)(600t+443),
h-91r = -60(42t+31)(65t+48),
7200r = (3600t+2659)^2 + 119.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(60,91)` and factor
`1`; the congruence class is `h ≡ 82 mod 109`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 8802 mod 10900,
38 mod 100: h ≡ 9238 mod 10900,
62 mod 100: h ≡ 2262 mod 10900,
98 mod 100: h ≡ 2698 mod 10900.
```

Executable guardrails:

- `certificateValid_unitCoordinateSixtyNinetyOneFactorOneParallel`
- `UNIT_COORDINATE_SIXTY_NINETY_ONE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_sixty_ninety_one_factor_one_parallel_certificate`
- `unit_coordinate_sixty_ninety_one_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_sixty_ninety_one_factor_one_parallel_family`

### 4.20.11. A One-Hundred-Twelve Fifteen Factor-One Row

The legal direction `(112,15)` of length `113` gives another coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 113t + 83,
r = 6272t^2 + 9199t + 3373.
```

Then

```text
P = (112r, 15r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-112r)^2 + (h-15r)^2 = (708736t^2 + 1039472t + 381137)^2.
```

The nonzero checks are

```text
1-112r = -(784t+575)(896t+657),
h-15r = -112(15t+11)(56t+41),
25088r = (12544t+9199)^2 + 223.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(112,15)` and
factor `1`; the congruence class is `h ≡ 83 mod 113`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 7202 mod 11300,
38 mod 100: h ≡ 4038 mod 11300,
62 mod 100: h ≡ 9462 mod 11300,
98 mod 100: h ≡ 6298 mod 11300.
```

Executable guardrails:

- `certificateValid_unitCoordinateOneHundredTwelveFifteenFactorOneParallel`
- `UNIT_COORDINATE_ONE_HUNDRED_TWELVE_FIFTEEN_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_one_hundred_twelve_fifteen_factor_one_parallel_certificate`
- `unit_coordinate_one_hundred_twelve_fifteen_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_one_hundred_twelve_fifteen_factor_one_parallel_family`

### 4.20.12. An Eighty-Eight One-Hundred-Five Factor-One Row

The legal direction `(88,105)` of length `137` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 137t + 7,
r = 3872t^2 + 329t + 7.
```

Then

```text
P = (88r, 105r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-88r)^2 + (h-105r)^2 = (530464t^2 + 44968t + 953)^2.
```

The nonzero checks are

```text
1-88r = -(352t+15)(968t+41),
h-105r = -8(165t+7)(308t+13),
15488r = (7744t+329)^2 + 175.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(88,105)` and
factor `1`; the congruence class is `h ≡ 7 mod 137`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 4802 mod 13700,
38 mod 100: h ≡ 8638 mod 13700,
62 mod 100: h ≡ 2062 mod 13700,
98 mod 100: h ≡ 5898 mod 13700.
```

Executable guardrails:

- `certificateValid_unitCoordinateEightyEightOneHundredFiveFactorOneParallel`
- `UNIT_COORDINATE_EIGHTY_EIGHT_ONE_HUNDRED_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_eighty_eight_one_hundred_five_factor_one_parallel_certificate`
- `unit_coordinate_eighty_eight_one_hundred_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_eighty_eight_one_hundred_five_factor_one_parallel_family`

### 4.20.13. A One-Hundred-Forty Fifty-One Factor-One Row

The legal direction `(140,51)` of length `149` gives another coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 149t + 82,
r = 9800t^2 + 10739t + 2942.
```

Then

```text
P = (140r, 51r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-140r)^2 + (h-51r)^2 = (1460200t^2 + 1600060t + 438329)^2.
```

The nonzero checks are

```text
1-140r = -(980t+537)(1400t+767),
h-51r = -20(42t+23)(595t+326),
39200r = (19600t+10739)^2 + 279.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(140,51)` and
factor `1`; the congruence class is `h ≡ 82 mod 149`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 12002 mod 14900,
38 mod 100: h ≡ 6638 mod 14900,
62 mod 100: h ≡ 3062 mod 14900,
98 mod 100: h ≡ 12598 mod 14900.
```

Executable guardrails:

- `certificateValid_unitCoordinateOneHundredFortyFiftyOneFactorOneParallel`
- `UNIT_COORDINATE_ONE_HUNDRED_FORTY_FIFTY_ONE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_one_hundred_forty_fifty_one_factor_one_parallel_certificate`
- `unit_coordinate_one_hundred_forty_fifty_one_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_one_hundred_forty_fifty_one_factor_one_parallel_family`

### 4.20.14. A One-Hundred-Thirty-Two Eighty-Five Factor-One Row

The legal direction `(132,85)` of length `157` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 157t + 4,
r = 8712t^2 + 373t + 4.
```

Then

```text
P = (132r, 85r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-132r)^2 + (h-85r)^2 = (1367784t^2 + 58476t + 625)^2.
```

The nonzero checks are

```text
1-132r = -(792t+17)(1452t+31),
h-85r = -12(187t+4)(330t+7),
34848r = (17424t+373)^2 + 263.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(132,85)` and
factor `1`; the congruence class is `h ≡ 4 mod 157`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 2202 mod 15700,
38 mod 100: h ≡ 9738 mod 15700,
62 mod 100: h ≡ 14762 mod 15700,
98 mod 100: h ≡ 6598 mod 15700.
```

Executable guardrails:

- `certificateValid_unitCoordinateOneHundredThirtyTwoEightyFiveFactorOneParallel`
- `UNIT_COORDINATE_ONE_HUNDRED_THIRTY_TWO_EIGHTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_one_hundred_thirty_two_eighty_five_factor_one_parallel_certificate`
- `unit_coordinate_one_hundred_thirty_two_eighty_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_one_hundred_thirty_two_eighty_five_factor_one_parallel_family`

### 4.20.15. A One-Hundred-Twenty One-Hundred-Nineteen Factor-One Row

The legal direction `(120,119)` of length `169` gives another coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 169t + 168,
r = 7200t^2 + 14231t + 7032.
```

Then

```text
P = (120r, 119r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-120r)^2 + (h-119r)^2 = (1216800t^2 + 2404920t + 1188289)^2.
```

The nonzero checks are

```text
1-120r = -(600t+593)(1440t+1423),
h-119r = -120(84t+83)(85t+84),
28800r = (14400t+14231)^2 + 239.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(120,119)` and
factor `1`; the congruence class is `h ≡ 168 mod 169`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 14702 mod 16900,
38 mod 100: h ≡ 5238 mod 16900,
62 mod 100: h ≡ 4562 mod 16900,
98 mod 100: h ≡ 11998 mod 16900.
```

Executable guardrails:

- `certificateValid_unitCoordinateOneHundredTwentyOneHundredNineteenFactorOneParallel`
- `UNIT_COORDINATE_ONE_HUNDRED_TWENTY_ONE_HUNDRED_NINETEEN_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_one_hundred_twenty_one_hundred_nineteen_factor_one_parallel_certificate`
- `unit_coordinate_one_hundred_twenty_one_hundred_nineteen_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_one_hundred_twenty_one_hundred_nineteen_factor_one_parallel_family`

### 4.20.16. A Fifty-Two One-Hundred-Sixty-Five Factor-One Row

The legal direction `(52,165)` of length `173` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 173t + 28,
r = 1352t^2 + 389t + 28.
```

Then

```text
P = (52r, 165r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-52r)^2 + (h-165r)^2 = (233896t^2 + 67132t + 4817)^2.
```

The nonzero checks are

```text
1-52r = -(104t+15)(676t+97),
h-165r = -4(195t+28)(286t+41),
5408r = (2704t+389)^2 + 103.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(52,165)` and
factor `1`; the congruence class is `h ≡ 28 mod 173`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 6602 mod 17300,
38 mod 100: h ≡ 12138 mod 17300,
62 mod 100: h ≡ 10062 mod 17300,
98 mod 100: h ≡ 15598 mod 17300.
```

Executable guardrails:

- `certificateValid_unitCoordinateFiftyTwoOneHundredSixtyFiveFactorOneParallel`
- `UNIT_COORDINATE_FIFTY_TWO_ONE_HUNDRED_SIXTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_fifty_two_one_hundred_sixty_five_factor_one_parallel_certificate`
- `unit_coordinate_fifty_two_one_hundred_sixty_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_fifty_two_one_hundred_sixty_five_factor_one_parallel_family`

### 4.20.17. A One-Hundred-Eighty Nineteen Factor-One Row

The legal direction `(180,19)` of length `181` gives another coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 181t + 143,
r = 16200t^2 + 25579t + 10097.
```

Then

```text
P = (180r, 19r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-180r)^2 + (h-19r)^2 = (2932200t^2 + 4629780t + 1827541)^2.
```

The nonzero checks are

```text
1-180r = -(1620t+1279)(1800t+1421),
h-19r = -180(19t+15)(90t+71),
64800r = (32400t+25579)^2 + 359.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(180,19)` and
factor `1`; the congruence class is `h ≡ 143 mod 181`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 7202 mod 18100,
38 mod 100: h ≡ 17338 mod 18100,
62 mod 100: h ≡ 18062 mod 18100,
98 mod 100: h ≡ 10098 mod 18100.
```

Executable guardrails:

- `certificateValid_unitCoordinateOneHundredEightyNineteenFactorOneParallel`
- `UNIT_COORDINATE_ONE_HUNDRED_EIGHTY_NINETEEN_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_one_hundred_eighty_nineteen_factor_one_parallel_certificate`
- `unit_coordinate_one_hundred_eighty_nineteen_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_one_hundred_eighty_nineteen_factor_one_parallel_family`

### 4.20.18. A One-Hundred-Sixty-Eight Ninety-Five Factor-One Row

The legal direction `(168,95)` of length `193` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 193t + 47,
r = 14112t^2 + 6791t + 817.
```

Then

```text
P = (168r, 95r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-168r)^2 + (h-95r)^2 = (2723616t^2 + 1310568t + 157657)^2.
```

The nonzero checks are

```text
1-168r = -(1176t+283)(2016t+485),
h-95r = -24(133t+32)(420t+101),
56448r = (28224t+6791)^2 + 335.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(168,95)` and
factor `1`; the congruence class is `h ≡ 47 mod 193`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 6802 mod 19300,
38 mod 100: h ≡ 16838 mod 19300,
62 mod 100: h ≡ 10662 mod 19300,
98 mod 100: h ≡ 1398 mod 19300.
```

Executable guardrails:

- `certificateValid_unitCoordinateOneHundredSixtyEightNinetyFiveFactorOneParallel`
- `UNIT_COORDINATE_ONE_HUNDRED_SIXTY_EIGHT_NINETY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_one_hundred_sixty_eight_ninety_five_factor_one_parallel_certificate`
- `unit_coordinate_one_hundred_sixty_eight_ninety_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_one_hundred_sixty_eight_ninety_five_factor_one_parallel_family`

### 4.20.19. A Twenty-Eight One-Hundred-Ninety-Five Factor-One Row

The legal direction `(28,195)` of length `197` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 197t + 112,
r = 392t^2 + 419t + 112.
```

Then

```text
P = (28r, 195r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-28r)^2 + (h-195r)^2 = (77224t^2 + 82348t + 21953)^2.
```

The nonzero checks are

```text
1-28r = -(28t+15)(392t+209),
h-195r = -28(15t+8)(182t+97),
1568r = (784t+419)^2 + 55.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(28,195)` and
factor `1`; the congruence class is `h ≡ 112 mod 197`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 13902 mod 19700,
38 mod 100: h ≡ 11538 mod 19700,
62 mod 100: h ≡ 9962 mod 19700,
98 mod 100: h ≡ 7598 mod 19700.
```

Executable guardrails:

- `certificateValid_unitCoordinateTwentyEightOneHundredNinetyFiveFactorOneParallel`
- `UNIT_COORDINATE_TWENTY_EIGHT_ONE_HUNDRED_NINETY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_twenty_eight_one_hundred_ninety_five_factor_one_parallel_certificate`
- `unit_coordinate_twenty_eight_one_hundred_ninety_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_twenty_eight_one_hundred_ninety_five_factor_one_parallel_family`

### 4.20.20. A Sixty Two-Hundred-Twenty-One Factor-One Row

The legal direction `(60,221)` of length `229` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 229t + 36,
r = 1800t^2 + 509t + 36.
```

Then

```text
P = (60r, 221r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-60r)^2 + (h-221r)^2 = (412200t^2 + 116340t + 8209)^2.
```

The nonzero checks are

```text
1-60r = -(120t+17)(900t+127),
h-221r = -60(78t+11)(85t+12),
7200r = (3600t+509)^2 + 119.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(60,221)` and
factor `1`; the congruence class is `h ≡ 36 mod 229`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 12402 mod 22900,
38 mod 100: h ≡ 8738 mod 22900,
62 mod 100: h ≡ 21562 mod 22900,
98 mod 100: h ≡ 17898 mod 22900.
```

Executable guardrails:

- `certificateValid_unitCoordinateSixtyTwoHundredTwentyOneFactorOneParallel`
- `UNIT_COORDINATE_SIXTY_TWO_HUNDRED_TWENTY_ONE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_sixty_two_hundred_twenty_one_factor_one_parallel_certificate`
- `unit_coordinate_sixty_two_hundred_twenty_one_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_sixty_two_hundred_twenty_one_factor_one_parallel_family`

### 4.20.21. A Three-Hundred-Twelve Twenty-Five Factor-One Row

The legal direction `(312,25)` of length `313` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 313t + 263,
r = 48672t^2 + 81769t + 34343.
```

Then

```text
P = (312r, 25r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-312r)^2 + (h-25r)^2 = (15234336t^2 + 25593672t + 10749337)^2.
```

The nonzero checks are

```text
1-312r = -(3744t+3145)(4056t+3407),
h-25r = -312(25t+21)(156t+131),
194688r = (97344t+81769)^2 + 623.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(312,25)` and
factor `1`; the congruence class is `h ≡ 263 mod 313`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 1202 mod 31300,
38 mod 100: h ≡ 23738 mod 31300,
62 mod 100: h ≡ 7462 mod 31300,
98 mod 100: h ≡ 29998 mod 31300.
```

Executable guardrails:

- `certificateValid_unitCoordinateThreeHundredTwelveTwentyFiveFactorOneParallel`
- `UNIT_COORDINATE_THREE_HUNDRED_TWELVE_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_three_hundred_twelve_twenty_five_factor_one_parallel_certificate`
- `unit_coordinate_three_hundred_twelve_twenty_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_three_hundred_twelve_twenty_five_factor_one_parallel_family`

### 4.20.22. A Three-Hundred-Eight Seventy-Five Factor-One Row

The legal direction `(308,75)` of length `317` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 317t + 296,
r = 47432t^2 + 88507t + 41288.
```

Then

```text
P = (308r, 75r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-308r)^2 + (h-75r)^2 = (15035944t^2 + 28056644t + 13088225)^2.
```

The nonzero checks are

```text
1-308r = -(3388t+3161)(4312t+4023),
h-75r = -4(462t+431)(1925t+1796),
189728r = (94864t+88507)^2 + 615.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(308,75)` and
factor `1`; the congruence class is `h ≡ 296 mod 317`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 6002 mod 31700,
38 mod 100: h ≡ 8538 mod 31700,
62 mod 100: h ≡ 31362 mod 31700,
98 mod 100: h ≡ 2198 mod 31700.
```

Executable guardrails:

- `certificateValid_unitCoordinateThreeHundredEightSeventyFiveFactorOneParallel`
- `UNIT_COORDINATE_THREE_HUNDRED_EIGHT_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_three_hundred_eight_seventy_five_factor_one_parallel_certificate`
- `unit_coordinate_three_hundred_eight_seventy_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_three_hundred_eight_seventy_five_factor_one_parallel_family`

### 4.20.23. A Two-Hundred-Eighty-Eight One-Hundred-Seventy-Five Factor-One Row

The legal direction `(288,175)` of length `337` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 337t + 241,
r = 41472t^2 + 59167t + 21103.
```

Then

```text
P = (288r, 175r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-288r)^2 + (h-175r)^2 = (13976064t^2 + 19939104t + 7111585)^2.
```

The nonzero checks are

```text
1-288r = -(2592t+1849)(4608t+3287),
h-175r = -48(150t+107)(1008t+719),
165888r = (82944t+59167)^2 + 575.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(288,175)` and
factor `1`; the congruence class is `h ≡ 241 mod 337`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 18102 mod 33700,
38 mod 100: h ≡ 27538 mod 33700,
62 mod 100: h ≡ 11362 mod 33700,
98 mod 100: h ≡ 20798 mod 33700.
```

Executable guardrails:

- `certificateValid_unitCoordinateTwoHundredEightyEightOneHundredSeventyFiveFactorOneParallel`
- `UNIT_COORDINATE_TWO_HUNDRED_EIGHTY_EIGHT_ONE_HUNDRED_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_two_hundred_eighty_eight_one_hundred_seventy_five_factor_one_parallel_certificate`
- `unit_coordinate_two_hundred_eighty_eight_one_hundred_seventy_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_two_hundred_eighty_eight_one_hundred_seventy_five_factor_one_parallel_family`

### 4.20.24. A One-Hundred-Eighty Two-Hundred-Ninety-Nine Factor-One Row

The legal direction `(180,299)` of length `349` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 349t + 206,
r = 16200t^2 + 18971t + 5554.
```

Then

```text
P = (180r, 299r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-180r)^2 + (h-299r)^2 = (5653800t^2 + 6620580t + 1938169)^2.
```

The nonzero checks are

```text
1-180r = -(900t+527)(3240t+1897),
h-299r = -60(234t+137)(345t+202),
64800r = (32400t+18971)^2 + 359.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(180,299)` and
factor `1`; the congruence class is `h ≡ 206 mod 349`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 1602 mod 34900,
38 mod 100: h ≡ 23938 mod 34900,
62 mod 100: h ≡ 15562 mod 34900,
98 mod 100: h ≡ 2998 mod 34900.
```

Executable guardrails:

- `certificateValid_unitCoordinateOneHundredEightyTwoHundredNinetyNineFactorOneParallel`
- `UNIT_COORDINATE_ONE_HUNDRED_EIGHTY_TWO_HUNDRED_NINETY_NINE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_one_hundred_eighty_two_hundred_ninety_nine_factor_one_parallel_certificate`
- `unit_coordinate_one_hundred_eighty_two_hundred_ninety_nine_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_one_hundred_eighty_two_hundred_ninety_nine_factor_one_parallel_family`

### 4.20.25. A Two-Hundred-Seventy-Two Two-Hundred-Twenty-Five Factor-One Row

The legal direction `(272,225)` of length `353` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 353t + 49,
r = 36992t^2 + 10097t + 689.
```

Then

```text
P = (272r, 225r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-272r)^2 + (h-225r)^2 = (13058176t^2 + 3564016t + 243185)^2.
```

The nonzero checks are

```text
1-272r = -(2176t+297)(4624t+631),
h-225r = -16(425t+58)(1224t+167),
147968r = (73984t+10097)^2 + 543.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(272,225)` and
factor `1`; the congruence class is `h ≡ 49 mod 353`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 402 mod 35300,
38 mod 100: h ≡ 4638 mod 35300,
62 mod 100: h ≡ 7462 mod 35300,
98 mod 100: h ≡ 11698 mod 35300.
```

Executable guardrails:

- `certificateValid_unitCoordinateTwoHundredSeventyTwoTwoHundredTwentyFiveFactorOneParallel`
- `UNIT_COORDINATE_TWO_HUNDRED_SEVENTY_TWO_TWO_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_two_hundred_seventy_two_two_hundred_twenty_five_factor_one_parallel_certificate`
- `unit_coordinate_two_hundred_seventy_two_two_hundred_twenty_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_two_hundred_seventy_two_two_hundred_twenty_five_factor_one_parallel_family`

### 4.20.26. A Two-Hundred-Fifty-Two Two-Hundred-Seventy-Five Factor-One Row

The legal direction `(252,275)` of length `373` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 373t + 151,
r = 31752t^2 + 25523t + 5129.
```

Then

```text
P = (252r, 275r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-252r)^2 + (h-275r)^2 = (11843496t^2 + 9519804t + 1913005)^2.
```

The nonzero checks are

```text
1-252r = -(1764t+709)(4536t+1823),
h-275r = -12(525t+211)(1386t+557),
127008r = (63504t+25523)^2 + 503.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(252,275)` and
factor `1`; the congruence class is `h ≡ 151 mod 373`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 32602 mod 37300,
38 mod 100: h ≡ 7238 mod 37300,
62 mod 100: h ≡ 2762 mod 37300,
98 mod 100: h ≡ 14698 mod 37300.
```

Executable guardrails:

- `certificateValid_unitCoordinateTwoHundredFiftyTwoTwoHundredSeventyFiveFactorOneParallel`
- `UNIT_COORDINATE_TWO_HUNDRED_FIFTY_TWO_TWO_HUNDRED_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_two_hundred_fifty_two_two_hundred_seventy_five_factor_one_parallel_certificate`
- `unit_coordinate_two_hundred_fifty_two_two_hundred_seventy_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_two_hundred_fifty_two_two_hundred_seventy_five_factor_one_parallel_family`

### 4.20.27. A Three-Hundred-Fifty-Two One-Hundred-Thirty-Five Factor-One Row

The legal direction `(352,135)` of length `377` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 377t + 299,
r = 61952t^2 + 98143t + 38869.
```

Then

```text
P = (352r, 135r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-352r)^2 + (h-135r)^2 = (23355904t^2 + 36999776t + 14653505)^2.
```

The nonzero checks are

```text
1-352r = -(3872t+3067)(5632t+4461),
h-135r = -8(880t+697)(1188t+941),
247808r = (123904t+98143)^2 + 703.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(352,135)` and
factor `1`; the congruence class is `h ≡ 299 mod 377`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 15002 mod 37700,
38 mod 100: h ≡ 2938 mod 37700,
62 mod 100: h ≡ 7462 mod 37700,
98 mod 100: h ≡ 33098 mod 37700.
```

Executable guardrails:

- `certificateValid_unitCoordinateThreeHundredFiftyTwoOneHundredThirtyFiveFactorOneParallel`
- `UNIT_COORDINATE_THREE_HUNDRED_FIFTY_TWO_ONE_HUNDRED_THIRTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_three_hundred_fifty_two_one_hundred_thirty_five_factor_one_parallel_certificate`
- `unit_coordinate_three_hundred_fifty_two_one_hundred_thirty_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_three_hundred_fifty_two_one_hundred_thirty_five_factor_one_parallel_family`

### 4.20.28. A Three-Hundred-Forty One-Hundred-Eighty-Nine Factor-One Row

The legal direction `(340,189)` of length `389` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 389t + 97,
r = 57800t^2 + 28661t + 3553.
```

Then

```text
P = (340r, 189r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-340r)^2 + (h-189r)^2 = (22484200t^2 + 11148940t + 1382069)^2.
```

The nonzero checks are

```text
1-340r = -(3400t+843)(5780t+1433),
h-189r = -20(238t+59)(2295t+569),
231200r = (115600t+28661)^2 + 679.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(340,189)` and
factor `1`; the congruence class is `h ≡ 97 mod 389`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 17602 mod 38900,
38 mod 100: h ≡ 26938 mod 38900,
62 mod 100: h ≡ 33162 mod 38900,
98 mod 100: h ≡ 3598 mod 38900.
```

Executable guardrails:

- `certificateValid_unitCoordinateThreeHundredFortyOneHundredEightyNineFactorOneParallel`
- `UNIT_COORDINATE_THREE_HUNDRED_FORTY_ONE_HUNDRED_EIGHTY_NINE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_three_hundred_forty_one_hundred_eighty_nine_factor_one_parallel_certificate`
- `unit_coordinate_three_hundred_forty_one_hundred_eighty_nine_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_three_hundred_forty_one_hundred_eighty_nine_factor_one_parallel_family`

### 4.20.29. A Two-Hundred-Twenty-Eight Three-Hundred-Twenty-Five Factor-One Row

The legal direction `(228,325)` of length `397` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 397t + 141,
r = 25992t^2 + 18277t + 3213.
```

Then

```text
P = (228r, 325r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-228r)^2 + (h-325r)^2 = (10318824t^2 + 7255644t + 1275445)^2.
```

The nonzero checks are

```text
1-228r = -(1368t+481)(4332t+1523),
h-325r = -12(475t+167)(1482t+521),
103968r = (51984t+18277)^2 + 455.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(228,325)` and
factor `1`; the congruence class is `h ≡ 141 mod 397`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 5302 mod 39700,
38 mod 100: h ≡ 538 mod 39700,
62 mod 100: h ≡ 37062 mod 39700,
98 mod 100: h ≡ 32298 mod 39700.
```

Executable guardrails:

- `certificateValid_unitCoordinateTwoHundredTwentyEightThreeHundredTwentyFiveFactorOneParallel`
- `UNIT_COORDINATE_TWO_HUNDRED_TWENTY_EIGHT_THREE_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_two_hundred_twenty_eight_three_hundred_twenty_five_factor_one_parallel_certificate`
- `unit_coordinate_two_hundred_twenty_eight_three_hundred_twenty_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_two_hundred_twenty_eight_three_hundred_twenty_five_factor_one_parallel_family`

### 4.20.30. A Forty Three-Hundred-Ninety-Nine Factor-One Row

The legal direction `(40,399)` of length `401` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 401t + 220,
r = 800t^2 + 839t + 220.
```

Then

```text
P = (40r, 399r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-40r)^2 + (h-399r)^2 = (320800t^2 + 336040t + 88001)^2.
```

The nonzero checks are

```text
1-40r = -(40t+21)(800t+419),
h-399r = -40(21t+11)(380t+199),
3200r = (1600t+839)^2 + 79.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(40,399)` and
factor `1`; the congruence class is `h ≡ 220 mod 401`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 33102 mod 40100,
38 mod 100: h ≡ 7438 mod 40100,
62 mod 100: h ≡ 17062 mod 40100,
98 mod 100: h ≡ 31498 mod 40100.
```

Executable guardrails:

- `certificateValid_unitCoordinateFortyThreeHundredNinetyNineFactorOneParallel`
- `UNIT_COORDINATE_FORTY_THREE_HUNDRED_NINETY_NINE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_forty_three_hundred_ninety_nine_factor_one_parallel_certificate`
- `unit_coordinate_forty_three_hundred_ninety_nine_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_forty_three_hundred_ninety_nine_factor_one_parallel_family`

### 4.20.31. A One-Hundred-Twenty Three-Hundred-Ninety-One Factor-One Row

The legal direction `(120,391)` of length `409` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 409t + 302,
r = 7200t^2 + 10519t + 3842.
```

Then

```text
P = (120r, 391r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-120r)^2 + (h-391r)^2 = (2944800t^2 + 4301880t + 1571089)^2.
```

The nonzero checks are

```text
1-120r = -(360t+263)(2400t+1753),
h-391r = -120(115t+84)(204t+149),
28800r = (14400t+10519)^2 + 239.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(120,391)` and
factor `1`; the congruence class is `h ≡ 302 mod 409`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 302 mod 40900,
38 mod 100: h ≡ 1938 mod 40900,
62 mod 100: h ≡ 16662 mod 40900,
98 mod 100: h ≡ 18298 mod 40900.
```

Executable guardrails:

- `certificateValid_unitCoordinateOneHundredTwentyThreeHundredNinetyOneFactorOneParallel`
- `UNIT_COORDINATE_ONE_HUNDRED_TWENTY_THREE_HUNDRED_NINETY_ONE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_one_hundred_twenty_three_hundred_ninety_one_factor_one_parallel_certificate`
- `unit_coordinate_one_hundred_twenty_three_hundred_ninety_one_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_one_hundred_twenty_three_hundred_ninety_one_factor_one_parallel_family`

### 4.20.32. A Four-Hundred-Twenty Twenty-Nine Factor-One Row

The legal direction `(420,29)` of length `421` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 421t + 363,
r = 88200t^2 + 152069t + 65547.
```

Then

```text
P = (420r, 29r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-420r)^2 + (h-29r)^2 = (37132200t^2 + 64021020t + 27595261)^2.
```

The nonzero checks are

```text
1-420r = -(5880t+5069)(6300t+5431),
h-29r = -420(29t+25)(210t+181),
352800r = (176400t+152069)^2 + 839.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(420,29)` and
factor `1`; the congruence class is `h ≡ 363 mod 421`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 25202 mod 42100,
38 mod 100: h ≡ 31938 mod 42100,
62 mod 100: h ≡ 8362 mod 42100,
98 mod 100: h ≡ 15098 mod 42100.
```

Executable guardrails:

- `certificateValid_unitCoordinateFourHundredTwentyTwentyNineFactorOneParallel`
- `UNIT_COORDINATE_FOUR_HUNDRED_TWENTY_TWENTY_NINE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_four_hundred_twenty_twenty_nine_factor_one_parallel_certificate`
- `unit_coordinate_four_hundred_twenty_twenty_nine_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_four_hundred_twenty_twenty_nine_factor_one_parallel_family`

### 4.20.33. A Four-Hundred-Eight One-Hundred-Forty-Five Factor-One Row

The legal direction `(408,145)` of length `433` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 433t + 39,
r = 83232t^2 + 14857t + 663.
```

Then

```text
P = (408r, 145r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-408r)^2 + (h-145r)^2 = (36039456t^2 + 6432936t + 287065)^2.
```

The nonzero checks are

```text
1-408r = -(4896t+437)(6936t+619),
h-145r = -24(493t+44)(1020t+91),
332928r = (166464t+14857)^2 + 815.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(408,145)` and
factor `1`; the congruence class is `h ≡ 39 mod 433`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 4802 mod 43300,
38 mod 100: h ≡ 1338 mod 43300,
62 mod 100: h ≡ 13462 mod 43300,
98 mod 100: h ≡ 9998 mod 43300.
```

Executable guardrails:

- `certificateValid_unitCoordinateFourHundredEightOneHundredFortyFiveFactorOneParallel`
- `UNIT_COORDINATE_FOUR_HUNDRED_EIGHT_ONE_HUNDRED_FORTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_four_hundred_eight_one_hundred_forty_five_factor_one_parallel_certificate`
- `unit_coordinate_four_hundred_eight_one_hundred_forty_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_four_hundred_eight_one_hundred_forty_five_factor_one_parallel_family`

### 4.20.34. A Two-Hundred-Eighty Three-Hundred-Fifty-One Factor-One Row

The legal direction `(280,351)` of length `449` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 449t + 264,
r = 39200t^2 + 45879t + 13424.
```

Then

```text
P = (280r, 351r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-280r)^2 + (h-351r)^2 = (17600800t^2 + 20599320t + 6027169)^2.
```

The nonzero checks are

```text
1-280r = -(1960t+1147)(5600t+3277),
h-351r = -280(135t+79)(364t+213),
156800r = (78400t+45879)^2 + 559.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(280,351)` and
factor `1`; the congruence class is `h ≡ 264 mod 449`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 28102 mod 44900,
38 mod 100: h ≡ 11938 mod 44900,
62 mod 100: h ≡ 1162 mod 44900,
98 mod 100: h ≡ 29898 mod 44900.
```

Executable guardrails:

- `certificateValid_unitCoordinateTwoHundredEightyThreeHundredFiftyOneFactorOneParallel`
- `UNIT_COORDINATE_TWO_HUNDRED_EIGHTY_THREE_HUNDRED_FIFTY_ONE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_two_hundred_eighty_three_hundred_fifty_one_factor_one_parallel_certificate`
- `unit_coordinate_two_hundred_eighty_three_hundred_fifty_one_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_two_hundred_eighty_three_hundred_fifty_one_factor_one_parallel_family`

### 4.20.35. A One-Hundred-Sixty-Eight Four-Hundred-Twenty-Five Factor-One Row

The legal direction `(168,425)` of length `457` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 457t + 248,
r = 14112t^2 + 15161t + 4072.
```

Then

```text
P = (168r, 425r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-168r)^2 + (h-425r)^2 = (6449184t^2 + 6928152t + 1860673)^2.
```

The nonzero checks are

```text
1-168r = -(672t+361)(3528t+1895),
h-425r = -24(175t+94)(1428t+767),
56448r = (28224t+15161)^2 + 335.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(168,425)` and
factor `1`; the congruence class is `h ≡ 248 mod 457`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 10302 mod 45700,
38 mod 100: h ≡ 32238 mod 45700,
62 mod 100: h ≡ 1162 mod 45700,
98 mod 100: h ≡ 23098 mod 45700.
```

Executable guardrails:

- `certificateValid_unitCoordinateOneHundredSixtyEightFourHundredTwentyFiveFactorOneParallel`
- `UNIT_COORDINATE_ONE_HUNDRED_SIXTY_EIGHT_FOUR_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_one_hundred_sixty_eight_four_hundred_twenty_five_factor_one_parallel_certificate`
- `unit_coordinate_one_hundred_sixty_eight_four_hundred_twenty_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_one_hundred_sixty_eight_four_hundred_twenty_five_factor_one_parallel_family`

### 4.20.36. A Three-Hundred-Eighty Two-Hundred-Sixty-One Factor-One Row

The legal direction `(380,261)` of length `461` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 461t + 373,
r = 72200t^2 + 116621t + 47093.
```

Then

```text
P = (380r, 261r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-380r)^2 + (h-261r)^2 = (33284200t^2 + 53762020t + 21709661)^2.
```

The nonzero checks are

```text
1-380r = -(3800t+3069)(7220t+5831),
h-261r = -20(551t+445)(1710t+1381),
288800r = (144400t+116621)^2 + 759.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(380,261)` and
factor `1`; the congruence class is `h ≡ 373 mod 461`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 41402 mod 46100,
38 mod 100: h ≡ 30338 mod 46100,
62 mod 100: h ≡ 22962 mod 46100,
98 mod 100: h ≡ 11898 mod 46100.
```

Executable guardrails:

- `certificateValid_unitCoordinateThreeHundredEightyTwoHundredSixtyOneFactorOneParallel`
- `UNIT_COORDINATE_THREE_HUNDRED_EIGHTY_TWO_HUNDRED_SIXTY_ONE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_three_hundred_eighty_two_hundred_sixty_one_factor_one_parallel_certificate`
- `unit_coordinate_three_hundred_eighty_two_hundred_sixty_one_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_three_hundred_eighty_two_hundred_sixty_one_factor_one_parallel_family`

### 4.20.37. A Three-Hundred-Sixty Three-Hundred-Nineteen Factor-One Row

The legal direction `(360,319)` of length `481` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 481t + 23,
r = 64800t^2 + 5959t + 137.
```

Then

```text
P = (360r, 319r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-360r)^2 + (h-319r)^2 = (31168800t^2 + 2865960t + 65881)^2.
```

The nonzero checks are

```text
1-360r = -(3240t+149)(7200t+331),
h-319r = -120(87t+4)(1980t+91),
259200r = (129600t+5959)^2 + 719.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(360,319)` and
factor `1`; the congruence class is `h ≡ 23 mod 481`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 28402 mod 48100,
38 mod 100: h ≡ 7238 mod 48100,
62 mod 100: h ≡ 9162 mod 48100,
98 mod 100: h ≡ 36098 mod 48100.
```

Executable guardrails:

- `certificateValid_unitCoordinateThreeHundredSixtyThreeHundredNineteenFactorOneParallel`
- `UNIT_COORDINATE_THREE_HUNDRED_SIXTY_THREE_HUNDRED_NINETEEN_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_three_hundred_sixty_three_hundred_nineteen_factor_one_parallel_certificate`
- `unit_coordinate_three_hundred_sixty_three_hundred_nineteen_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_three_hundred_sixty_three_hundred_nineteen_factor_one_parallel_family`

### 4.20.38. A One-Hundred-Thirty-Two Four-Hundred-Seventy-Five Factor-One Row

The legal direction `(132,475)` of length `493` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 493t + 199,
r = 8712t^2 + 6907t + 1369.
```

Then

```text
P = (132r, 475r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-132r)^2 + (h-475r)^2 = (4295016t^2 + 3404676t + 674725)^2.
```

The nonzero checks are

```text
1-132r = -(396t+157)(2904t+1151),
h-475r = -12(275t+109)(1254t+497),
34848r = (17424t+6907)^2 + 263.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(132,475)` and
factor `1`; the congruence class is `h ≡ 199 mod 493`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 35202 mod 49300,
38 mod 100: h ≡ 11538 mod 49300,
62 mod 100: h ≡ 45062 mod 49300,
98 mod 100: h ≡ 21398 mod 49300.
```

Executable guardrails:

- `certificateValid_unitCoordinateOneHundredThirtyTwoFourHundredSeventyFiveFactorOneParallel`
- `UNIT_COORDINATE_ONE_HUNDRED_THIRTY_TWO_FOUR_HUNDRED_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_one_hundred_thirty_two_four_hundred_seventy_five_factor_one_parallel_certificate`
- `unit_coordinate_one_hundred_thirty_two_four_hundred_seventy_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_one_hundred_thirty_two_four_hundred_seventy_five_factor_one_parallel_family`

### 4.20.39. A Two-Hundred-Twenty Four-Hundred-Fifty-Nine Factor-One Row

The legal direction `(220,459)` of length `509` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 509t + 96,
r = 24200t^2 + 8931t + 824.
```

Then

```text
P = (220r, 459r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-220r)^2 + (h-459r)^2 = (12317800t^2 + 4545420t + 419329)^2.
```

The nonzero checks are

```text
1-220r = -(1100t+203)(4840t+893),
h-459r = -20(374t+69)(1485t+274),
96800r = (48400t+8931)^2 + 439.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(220,459)` and
factor `1`; the congruence class is `h ≡ 96 mod 509`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 17402 mod 50900,
38 mod 100: h ≡ 19438 mod 50900,
62 mod 100: h ≡ 37762 mod 50900,
98 mod 100: h ≡ 39798 mod 50900.
```

Executable guardrails:

- `certificateValid_unitCoordinateTwoHundredTwentyFourHundredFiftyNineFactorOneParallel`
- `UNIT_COORDINATE_TWO_HUNDRED_TWENTY_FOUR_HUNDRED_FIFTY_NINE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_two_hundred_twenty_four_hundred_fifty_nine_factor_one_parallel_certificate`
- `unit_coordinate_two_hundred_twenty_four_hundred_fifty_nine_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_two_hundred_twenty_four_hundred_fifty_nine_factor_one_parallel_family`

### 4.20.40. A Four-Hundred-Forty Two-Hundred-Seventy-Nine Factor-One Row

The legal direction `(440,279)` of length `521` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 521t + 103,
r = 96800t^2 + 38039t + 3737.
```

Then

```text
P = (440r, 279r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-440r)^2 + (h-279r)^2 = (50432800t^2 + 19818040t + 1946921)^2.
```

The nonzero checks are

```text
1-440r = -(4840t+951)(8800t+1729),
h-279r = -40(341t+67)(1980t+389),
387200r = (193600t+38039)^2 + 879.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(440,279)` and
factor `1`; the congruence class is `h ≡ 103 mod 521`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 10002 mod 52100,
38 mod 100: h ≡ 18338 mod 52100,
62 mod 100: h ≡ 41262 mod 52100,
98 mod 100: h ≡ 49598 mod 52100.
```

Executable guardrails:

- `certificateValid_unitCoordinateFourHundredFortyTwoHundredSeventyNineFactorOneParallel`
- `UNIT_COORDINATE_FOUR_HUNDRED_FORTY_TWO_HUNDRED_SEVENTY_NINE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_four_hundred_forty_two_hundred_seventy_nine_factor_one_parallel_certificate`
- `unit_coordinate_four_hundred_forty_two_hundred_seventy_nine_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_four_hundred_forty_two_hundred_seventy_nine_factor_one_parallel_family`

### 4.20.41. A Ninety-Two Five-Hundred-Twenty-Five Factor-One Row

The legal direction `(92,525)` of length `533` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 533t + 78,
r = 4232t^2 + 1149t + 78.
```

Then

```text
P = (92r, 525r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-92r)^2 + (h-525r)^2 = (2255656t^2 + 611892t + 41497)^2.
```

The nonzero checks are

```text
1-92r = -(184t+25)(2116t+287),
h-525r = -4(575t+78)(966t+131),
16928r = (8464t+1149)^2 + 183.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(92,525)` and
factor `1`; the congruence class is `h ≡ 78 mod 533`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 15002 mod 53300,
38 mod 100: h ≡ 10738 mod 53300,
62 mod 100: h ≡ 25662 mod 53300,
98 mod 100: h ≡ 21398 mod 53300.
```

Executable guardrails:

- `certificateValid_unitCoordinateNinetyTwoFiveHundredTwentyFiveFactorOneParallel`
- `UNIT_COORDINATE_NINETY_TWO_FIVE_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_ninety_two_five_hundred_twenty_five_factor_one_parallel_certificate`
- `unit_coordinate_ninety_two_five_hundred_twenty_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_ninety_two_five_hundred_twenty_five_factor_one_parallel_family`

### 4.20.42. A Four-Hundred-Twenty Three-Hundred-Forty-One Factor-One Row

The legal direction `(420,341)` of length `541` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 541t + 113,
r = 88200t^2 + 36581t + 3793.
```

Then

```text
P = (420r, 341r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-420r)^2 + (h-341r)^2 = (47716200t^2 + 19789980t + 2051941)^2.
```

The nonzero checks are

```text
1-420r = -(4200t+871)(8820t+1829),
h-341r = -60(217t+45)(2310t+479),
352800r = (176400t+36581)^2 + 839.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(420,341)` and
factor `1`; the congruence class is `h ≡ 113 mod 541`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 15802 mod 54100,
38 mod 100: h ≡ 13638 mod 54100,
62 mod 100: h ≡ 48262 mod 54100,
98 mod 100: h ≡ 46098 mod 54100.
```

Executable guardrails:

- `certificateValid_unitCoordinateFourHundredTwentyThreeHundredFortyOneFactorOneParallel`
- `UNIT_COORDINATE_FOUR_HUNDRED_TWENTY_THREE_HUNDRED_FORTY_ONE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_four_hundred_twenty_three_hundred_forty_one_factor_one_parallel_certificate`
- `unit_coordinate_four_hundred_twenty_three_hundred_forty_one_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_four_hundred_twenty_three_hundred_forty_one_factor_one_parallel_family`

### 4.20.43. A Five-Hundred-Thirty-Two One-Hundred-Sixty-Five Factor-One Row

The legal direction `(532,165)` of length `557` gives the next coprime-period
unit-coordinate residual row.  For every integer `t`, set

```text
h = 557t + 412,
r = 141512t^2 + 209189t + 77308.
```

Then

```text
P = (532r, 165r)
```

certifies `(1,h)`.  The second-step identity is

```text
(1-532r)^2 + (h-165r)^2 = (78822184t^2 + 116518108t + 43060433)^2.
```

The nonzero checks are

```text
1-532r = -(7448t+5505)(10108t+7471),
h-165r = -4(1330t+983)(4389t+3244),
566048r = (283024t+209189)^2 + 1063.
```

Thus no integer parameter degenerates.  This is the
`parallel_direction_factor_certificate` row for direction `(532,165)` and
factor `1`; the congruence class is `h ≡ 412 mod 557`.

The row intersects all four mod-100 residual classes:

```text
2  mod 100: h ≡ 39402 mod 55700,
38 mod 100: h ≡ 10438 mod 55700,
62 mod 100: h ≡ 28262 mod 55700,
98 mod 100: h ≡ 54998 mod 55700.
```

Executable guardrails:

- `certificateValid_unitCoordinateFiveHundredThirtyTwoOneHundredSixtyFiveFactorOneParallel`
- `UNIT_COORDINATE_FIVE_HUNDRED_THIRTY_TWO_ONE_HUNDRED_SIXTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS`
- `unit_coordinate_five_hundred_thirty_two_one_hundred_sixty_five_factor_one_parallel_certificate`
- `unit_coordinate_five_hundred_thirty_two_one_hundred_sixty_five_factor_one_parallel_orbit_certificate`
- `test_unit_coordinate_five_hundred_thirty_two_one_hundred_sixty_five_factor_one_parallel_family`

## 4.21. Orthogonal Unit-Coordinate Congruence Classes

Every primitive Pythagorean triple also gives a complete unit-coordinate
congruence class through the orthogonal lattice construction.

**Theorem 4.7.**  Let `(a,b,c)` be a primitive positive Pythagorean triple.  If
an integer `h` satisfies

```text
a*h == b mod c^2,
```

then `(1,h)` and every sign/swap image of it has distance at most two from the
origin.

Since the triple is primitive, `gcd(a,c)=1`.  Therefore the congruence is the
same as one residue class

```text
h == b*a^(-1) mod c^2.
```

Put

```text
r = (a + b*h)/c^2,      s = (a*h - b)/c^2.
```

The hypothesis makes `s` an integer.  It also makes `r` an integer: multiplying
`a*h == b mod c^2` by `b` gives `a*b*h == b^2 mod c^2`, hence

```text
a*(a+b*h) == a^2+b^2 == c^2 == 0 mod c^2.
```

Because `gcd(a,c^2)=1`, this forces `c^2 | a+b*h`.

Now take the legal orthogonal directions

```text
U=(a,b),      V=(-b,a).
```

Their determinant is `c^2`, and Cramer's rule gives

```text
rU+sV
  = ((r*a-s*b), (r*b+s*a))
  = (1,h).
```

Thus the midpoint

```text
P=rU=(ra,rb)
```

is a two-step certificate, provided both coefficients are nonzero.  This
nondegeneracy is automatic.  If `r=0`, then `a+b*h=0`, so `b | a`; primitivity
would force `b=1`, impossible for a positive Pythagorean leg.  If `s=0`, then
`a*h=b`, so `a | b`; primitivity would force `a=1`, also impossible.  Hence both
steps are nonzero integer multiples of legal directions.

For example, the triple `(8,15,17)` gives

```text
h == 38 mod 289.
```

Every target `(1,38+289t)` is certified by

```text
r=2+15t,      s=1+8t,      P=(8r,15r).
```

Sign changes and coordinate swap give the full orbit of each congruence class.
This is the unit-coordinate specialization of the orthogonal triple lattice
construction, now recorded as a named infinite theorem slice.

Executable guardrails:

- `latticeCertificateValid_of_cramer`
- `certificateValid_latticeMidpointData`
- `exists_latticeCertificateValid_of_cramer`
- `pythagorean_triple_orthogonal_lattice_certificate`
- `pythagorean_orthogonal_lattice_cover_certificate`
- `test_pythagorean_triple_orthogonal_lattice_family`
- `test_pythagorean_orthogonal_lattice_cover`

## 4.19. The Determinant-Seven Lattice Congruence Slice

The first full two-dimensional lattice congruence slice comes from the
`3-4-5` directions

```text
U=(3,4),      V=(4,3),
U'=(3,-4),    V'=(4,-3).
```

The determinants are

```text
det(U,V)=-7,      det(U',V')=7.
```

**Theorem 4.8.**  Let `(g,h)` be a nonzero integer target.  If

```text
g+h == 0 mod 7      or      g-h == 0 mod 7,
```

then `(g,h)` has distance at most two from the origin.

First suppose `g+h == 0 mod 7`.  Put

```text
r=(4h-3g)/7,      s=(4g-3h)/7.
```

These are integers because `g+h` is divisible by `7`.  A direct calculation
gives

```text
rU+sV=(g,h).
```

If `r` and `s` are both nonzero, then

```text
P=rU=(3r,4r)
```

is a two-step midpoint: the first edge is the nonzero multiple `rU` of a
`3-4-5` direction, and the second edge is the nonzero multiple `sV` of another
`3-4-5` direction.  If one of `r,s` is zero, then `(g,h)` is already a nonzero
integer multiple of `U` or `V`, hence is a one-step target.

Now suppose `g-h == 0 mod 7`.  Put

```text
r=-(3g+4h)/7,      s=(4g+3h)/7.
```

Again these are integers, and

```text
rU'+sV'=(g,h).
```

The same argument gives a two-step certificate when both coefficients are
nonzero and a one-step legal edge when one coefficient vanishes.  Since the
target is assumed nonzero, the one-step coefficient is nonzero in the latter
case.

This proves Theorem 4.8.  The known distance-three obstruction orbit is not in
this slice: none of the sign/swap images of `(1,0)`, `(2,0)`, or `(2,1)`
satisfies either congruence.

Executable guardrails:

- `lattice_two_step_certificate`
- `prime_determinant_lattice_certificate`
- `DETERMINANT_SEVEN_DIRECTION_PAIRS`
- `determinant_seven_lattice_certificate`
- `test_prime_determinant_lattice_line_criterion`
- `test_determinant_seven_congruence_families`

## 5. The Exceptional `(2,1)` Ray

The primitive target `(2,1)` is a known distance-three obstruction.  A complete
theorem in this workspace is that every non-primitive multiple of that ray has
a two-step certificate.

**Theorem 5.1.**  For every integer `N` with `|N|>1`, the target `(2N,N)` and
every sign/swap image of it has distance at most two from the origin.

It is enough to prove the theorem for positive `N`.  Sign changes and coordinate
swap then give the full orbit.

### 5.1. Reduction To Prime Multipliers

Suppose `q` divides `N` and `P` certifies `(2q,q)`.  By scaling, `(N/q)P`
certifies `(2N,N)`.

Therefore it is enough to certify `(2p,p)` for every prime `p`.  Composite
multipliers then follow by choosing any prime divisor.

### 5.2. The Prime `p=2`

The target `(4,2)` has midpoint

```text
P=(-36,77).
```

Indeed,

```text
(-36)^2 + 77^2 = 85^2,
(4-(-36))^2 + (2-77)^2 = 40^2 + (-75)^2 = 85^2.
```

Thus `p=2` is certified.

### 5.3. Primes `p == 3 mod 4`

First handle `p=3` by the explicit midpoint

```text
P=(12,-5)
```

for target `(6,3)`, since

```text
12^2 + (-5)^2 = 13^2,
(6-12)^2 + (3-(-5))^2 = (-6)^2 + 8^2 = 10^2.
```

The divisor-strengthened signed Theorem 3 in fact proves the whole
multiple-of-three subray.  For `N=3m` with `m != 0`, the midpoint

```text
P=(12m,-5m)
```

certifies `(6m,3m)=(2N,N)`, because the two edge lengths are `13|m|` and
`10|m|`.  This gives a standalone infinite theorem slice, and the sign/swap
orbit follows from the symmetries in Section 2.

The signed `3-4-5` fixed-direction parallel-factor layer gives another clean
exceptional-ray slice.  For positive multipliers `N ≡ 2 mod 5`, the tail
`N>=7` is certified by direction `(4,3)` with factor `2`; for
`N ≡ 3 mod 5`, the tail `N>=8` is certified by direction `(-4,-3)` with
factor `2`.  The first representatives are the only pointwise degeneracies:
`N=2` is covered by the even-ray theorem, and `N=3` by the multiple-of-three
Theorem 3 row above.  Hence every nonzero multiplier in the two residue classes

```text
N ≡ 2 or 3 mod 5
```

has a two-step certificate on the `(2,1)` ray, and sign/swap transport gives
the full orbit.

Executable guardrails:

- `two_one_ray_two_or_three_mod_five_parallel_certificate`
- `two_one_ray_two_or_three_mod_five_parallel_orbit_certificate`
- `test_two_one_ray_two_or_three_mod_five_parallel_family`

Now let `p>=7` be a prime with `p == 3 mod 4`, and set

```text
u = (p-1)/2.
```

Then `u>=3` is odd, and the midpoint

```text
P=(2u, 1-u^2)
```

certifies `(2p,p)`.  Since `p=2u+1`, the first edge has squared length

```text
(2u)^2 + (1-u^2)^2 = (u^2+1)^2,
```

and the second edge has displacement

```text
(2p,p)-P = (2u+2, u^2+2u),
```

whose squared length is

```text
(2u+2)^2 + (u^2+2u)^2 = (u^2+2u+2)^2.
```

All coordinate differences are nonzero for `u>=3`.  Hence every prime
`p == 3 mod 4` is certified.

### 5.4. Primes `p == 1 mod 4`

The remaining prime class is handled by a double-direction construction.

Let `U=(r,s)` be a legal Pythagorean direction with length `c`, so

```text
r^2+s^2=c^2.
```

Put

```text
A = 2r+s,       q = 3c-A.
```

If `q>0` and the coordinate differences are nonzero, then `P=2U` certifies
`(2q,q)`.  The first edge has length `2c`.  For the second edge,

```text
|(2q,q)-2U|^2
  = 5q^2 - 4q(2r+s) + 4c^2
  = 5q^2 - 4qA + 4c^2.
```

Since `q=3c-A`, this becomes

```text
5q^2 - 4q(3c-q) + 4c^2 = (3q-2c)^2.
```

Thus the second edge also has integer length.

Now let `p` be an odd prime with `p == 1 mod 4`.  By Fermat's two-square
theorem, write

```text
p = x^2 + z^2.
```

Exactly one of `x,z` is even.  Write the even one as `2y`, so

```text
p = x^2 + 4y^2
```

with positive integers `x,y` and `x` odd.  Set

```text
m = x+y,        k = y,
U = (m^2-k^2, 2mk).
```

Then

```text
U = (x^2+2xy, 2xy+2y^2),
c = m^2+k^2 = x^2+2xy+2y^2.
```

For this direction,

```text
3c - (2r+s) = x^2 + 4y^2 = p.
```

Therefore the double-direction lemma gives a two-step certificate for `(2p,p)`
with midpoint `P=2U`.

The nonzero-coordinate conditions are automatic here.  The first edge has both
coordinates positive.  The second edge has coordinates

```text
2p-2r = 4y(2y-x),
p-2s = x(x-4y).
```

Neither can vanish: `x` is odd, while `2y` and `4y` are even.

Thus every prime `p == 1 mod 4` is certified.

### 5.5. Completion Of The Exceptional-Ray Theorem

Every prime multiplier `p>1` is now certified:

- `p=2` by the explicit midpoint for `(4,2)`;
- primes `p == 3 mod 4` by the formula in Section 5.3;
- primes `p == 1 mod 4` by Fermat's two-square theorem and the
  double-direction construction.

If `N>1` is composite, choose a prime divisor `p` of `N`.  Scale the certificate
for `(2p,p)` by `N/p`.  This gives a certificate for `(2N,N)`.

The primitive multiplier `N=1` remains the known distance-three obstruction.
This proves Theorem 5.1.

Written source:

- `notes/pythagorean-walks-full-conjecture-progress.md`, especially
  "Three-Mod-Four Multipliers On The Exceptional Ray",
  "Even Multiples Of The Exceptional Ray",
  "Determinant Split-Factor Layers On The Exceptional Ray", and
  "Divisor-Lift Reduction To Prime Multipliers".

Executable guardrails:

- `two_one_ray_even_certificate`
- `two_one_ray_multiple_of_three_theorem3_certificate`
- `two_one_ray_mod60_theorem3_skeleton_certificate`
- `two_one_ray_three_mod_four_certificate`
- `two_one_ray_double_direction_certificate`
- `two_one_ray_prime_one_mod_four_double_direction_certificate`
- `two_one_ray_prime_divisor_lift_certificate`
- `two_one_ray_prime_divisor_lift_orbit_certificate`
- `test_two_one_ray_even_family`
- `test_two_one_ray_multiple_of_three_theorem3_family`
- `test_two_one_ray_mod60_theorem3_skeleton_family`
- `test_two_one_ray_three_mod_four_family`
- `test_two_one_ray_determinant_split_factor_layers`
- `test_two_one_ray_divisor_lift_reduces_remaining_ray_to_primes`

## 6. What Remains Open

The full conjecture still requires a proof that every non-axis target outside
the known distance-three orbit has a two-step certificate:

```text
g,h != 0,   (|g|,|h|) not in {(1,2),(2,1)}.
```

The repository contains many exact families that cover large parts of this
remaining problem: Gaussian transformations, lattice criteria, Euclid strips,
parallel-direction divisor families, signed versions of the paper's Theorem 3,
and determinant-squareclass line families.

The strongest current proof program is the fixed-direction parallel-divisor
approach.  The research notebook records a layered structural stack that covers
all tested primitive positive-quadrant samples through `1 <= g,h <= 1000`, and
newer Gaussian-root reductions explain the next frontier more algebraically.
These are proof leads, not yet a global theorem.

The latest proof-search step makes this frontier much more concrete.  For a
primitive Pythagorean direction written in Gaussian form as

```text
U = epsilon * alpha^2,
```

with `c = N(alpha)` and `D = det(U,T)`, the conjugate-ideal recognizer reduces
the split condition to divisor data in the single integer `D`.  A certificate is
obtained once one finds a squarefree `q | D` and a divisor `a | D/q` satisfying

```text
a^2 == -rho*(D/q) mod c,
```

where `b == rho*a mod c` is the divisibility condition for `a+i*b` by
`conj(alpha)`.  The resulting witness also verifies the Gaussian quadratic
identity

```text
2*epsilon^-1*T = 2*r*alpha^2 + q*beta^2.
```

Thus, for a fixed root shape, the problem is no longer a bounded split-factor
search.  It is a determinant-divisor theorem for `D`.

The current residual audits suggest two primary root-shape spines:

```text
(1,2k),        (2,2k+1),
```

with the first secondary shapes `(3,4)`, `(3,8)`, and `(4,5)`.  In the scratch
primitive-positive diagnostic through `1 <= g,h <= 2000`, there are `150`
targets left after the structural stack; the two primary spines cover `132`,
and the generated spine family including the three secondary shapes covers all
`150`.  In the pinned `1 <= g,h <= 1000` guardrail, the `34` structural misses
are covered by seven explicit root shapes:

```text
(1,4), (1,6), (2,3), (2,5), (2,7), (3,8), (4,5).
```

The next proof obligation is therefore not to increase the target box.  It is
to prove the divisor-root congruence on the root-shape spines and then discharge
the complementary cases.  The new obligation helpers split each row into:

1. a linear determinant strip `det(U,T) == R mod S`;
2. a divisor-class condition saying that `|D/q|` has a divisor in the recorded
   `a mod c` class.

## 4.31. The First Primary Gaussian-Root Spine

The first primary spine now has a uniform theorem-level row.  Fix `k >= 1` and
put

```text
U = (1 - 4k^2, 4k).
```

This is the Pythagorean direction generated by the Gaussian root shape
`(1,2k)`.  For nonzero integers `q,t,r`, set

```text
beta = (4kt + 2k - 1, -(2t + 1)).
```

Then the target

```text
T = rU + q*beta^2/2
```

has the two-step certificate with midpoint `rU`.  Written without Gaussian
division, the second step is

```text
(
  2q((2k+1)t+k)((2k-1)t+k-1),
  -q(4kt+2k-1)(2t+1)
).
```

The length identity is

```text
|q*beta^2/2|
  = |q|*(8k^2t^2 + 8k^2t + 2k^2 - 4kt - 2k + 2t^2 + 2t + 1).
```

The `t != 0` hypothesis is a simple uniform nondegeneracy guard: for `k=1`,
the second-step horizontal coordinate vanishes at `t=0`; for `k>1` this
parameter is harmless but excluding it keeps one clean statement.  The row
specializes to the existing `(1,2)` formula when `k=1` and supplies the first
complete primary-spine family rather than a finite root-shape table.

Executable guardrails:

- `certificateValid_oneEvenRootSpineLine`
- `one_even_root_spine_line_certificate`
- `one_even_root_spine_line_orbit_certificate`
- `test_one_even_root_spine_line_certificate`

## 4.32. The Companion Primary Gaussian-Root Spine

The second primary spine has the same status.  Fix `k >= 1` and write

```text
n = 2k + 1,
U = (-4n, 4 - n^2).
```

This direction is generated by the root shape `(2,2k+1)`, up to the fixed unit
used by the existing `(2,3)` row.  For nonzero integers `q,t,r`, set

```text
beta = (1 - 2nt, 4t - 1).
```

Then

```text
T = rU + q*i*beta^2/2
```

has the two-step certificate with midpoint `rU`.  The second step is

```text
(
  q(4t-1)(2nt-1),
  2qt(n-2)(nt+2t-1)
).
```

Its length is

```text
|q|*(8k^2t^2 + 8kt^2 - 4kt + 10t^2 - 6t + 1).
```

The nonzero factors are automatic from `k >= 1` and `t != 0`; the `k=1`
specialization is the previously explicit odd-integral `(2,3)` row.  Together
with Section 4.31, this closes the two primary Gaussian-root spine families
advertised by the residual-spine program.

Executable guardrails:

- `certificateValid_twoOddRootSpineLine`
- `two_odd_root_spine_line_certificate`
- `two_odd_root_spine_line_orbit_certificate`
- `test_two_odd_root_spine_line_certificate`

Both primary rows are now packaged with sign/swap orbit constructors.  These
constructors transport the canonical row certificate to any target in its graph
automorphism orbit and accept only when the transported midpoint is valid, so
the primary-spine theorem is executable in full symmetry.

## 4.33. The Three-Four Secondary Root Shape

The secondary root shape `(3,4)` now has named infinite line rows as well.
Use the direction

```text
U = (-7, 24),
```

which is one unit multiple of `(3+4i)^2`.  For nonzero integers `m,r` and
beta coordinates `a,b` satisfying `a*b*(a^2-b^2) != 0`, the target

```text
rU + m*(a^2-b^2, 2ab)
```

has the two-step certificate with midpoint `rU`.  The second step has length
`|m|*(a^2+b^2)`, and the first step has length `25|r|`.  Swapping coordinates
gives the companion direction `(24,7)`.

The odd-beta half-square branch is also closed.  For beta coordinates
`(2a+1,2b+1)` and nonzero `m,r` with
`2a^2+2a-2b^2-2b != 0`, the target

```text
rU + m*(2a^2+2a-2b^2-2b, (2a+1)(2b+1))
```

has the same midpoint certificate.

This closes the missing named row among the three observed secondary shapes
`(3,4)`, `(3,8)`, and `(4,5)`: the latter two already had explicit row
constructors and Lean certificate proofs.

Executable guardrails:

- `certificateValid_threeFourRootSpineLine`
- `certificateValid_threeFourRootSpineLineSwap`
- `certificateValid_threeFourOddRootSpineLine`
- `certificateValid_threeFourOddRootSpineLineSwap`
- `three_four_root_spine_line_certificate`
- `three_four_odd_root_spine_line_certificate`
- `test_secondary_root_spine_line_certificates`

The executable promotion layer recognizes the signed orbit of the observed
secondary rows `(3,4)`, `(3,8)`, and `(4,5)` by combining beta sign images with
`sign_swap_certificate` and requiring equality with the generated root-spine
witness certificate. Thus these rows are not only available in canonical
orientation; their signed witness reconstructions are covered by the same
theorem slice.

The pinned strip census shows that failures of the divisor-class condition are
not currently opaque: they fall into named structural families.  The largest
fallback is the promoted signed `3-4-5` direction/factor table.  Its
intersections with determinant strips are now computed by CRT and compressed to
linear rows `(D0,k0,modulus,count)`, with observed parameter moduli only
`1`, `2`, `5`, and `10` in the pinned scan.  The smaller lattice-pair fallback
is also row-level: the `203` pinned lattice-pair failures compress to `63`
ordered direction-pair rows over `26` determinant values, and each strip
intersection is one coefficient congruence in `T=mA+nB`.  Orthogonal fallbacks
are the quarter-turn special case of the same row mechanism, while
standard-completion fallbacks are now quadratic rows in `det(U,T)` and
`U dot T` modulo `4|U|^2`.

This reframes the remaining conjecture as a finite discharging problem on
determinant strips and structural row families.  The box audits remain useful
as regression tests, but the proposed proof objects are now congruence rows and
root-shape divisor lemmas.

The divisor-class side has also been separated into a theorem-level saturation
branch and a bounded short-log branch.  For prime moduli, divisor residues are
represented as exponent sumsets in the cyclic group `(Z/(c-1)Z)`.  Kneser's
theorem supplies a lower bound for these sumsets.  When that bound saturates
the whole group, the required divisor class must occur, so the strip target is
a direct divisor success before any structural fallback is needed.

The target-facing strip census now applies this Kneser test before the
divisor/fallback split.  In the pinned prime-modulus strip guardrail, the
classification is:

```text
192  Kneser-saturated divisor successes,
1228 short-log divisor successes,
4398 short-log divisor failures, all structurally discharged.
```

The implementation asserts that a saturated exponent sumset cannot enter the
divisor-failure branch.  Thus the remaining divisor proof route is cleaner:
prove direct success from saturation, and handle the unsaturated cases as short
bounded sequences of prime-factor discrete logs.  The current data says those
short-log failures are exactly the cases discharged by the existing structural
row families.

The strip-discharge branch is now target-facing in the executable workspace:
the ten pinned root-spine obligations are named directly, the prime-modulus
exponent profile is exposed for an individual strip target, and a discharge
witness returns either direct divisor success or the exact promoted `3-4-5`,
lattice-pair, orthogonal, or standard-completion congruence row.  This is still
a proof object for the remaining program rather than a proof of the full
conjecture, but it separates the missing theorem from the bounded census.

This also falsified a tempting stronger formulation.  The pinned strips do not
each discharge independently: `(108638,24031)` lies on the pinned
`((4,5),2,41,9,10,33,19)` strip for direction `(-40,-9)`, misses the required
divisor class, and has no local structural fallback.  It is certified only
after choosing a different generated root-spine row, namely direction `(-3,4)`
with root shape `(1,2)` and squareclass `535`.  The remaining proof must
therefore be stated as a global root-choice theorem.

The currently observed alternate-root exits have now been promoted from
examples to explicit infinite line rows.  Lean proves the `(1,2)` direction
`(-3,4)`, both `(1,4)` orientations `(-8,-15)` and `(-15,-8)`, both
odd-integral `(2,3)` orientations `(-12,-5)` and `(-5,-12)`, and the even
`(2,3)` beta-square branch in direction `(-12,-5)`.  The corresponding rows are
`certificateValid_oneTwoRootSpineLine`,
`certificateValid_oneFourRootSpineLine`,
`certificateValid_oneFourRootSpineLineSwap`,
`certificateValid_twoThreeOddRootSpineLine`,
`certificateValid_twoThreeOddRootSpineLineSwap`, and
`certificateValid_twoThreeEvenRootSpineLine`.  These rows cover the six
alternate-root witnesses found by the pinned-strip stress test.  They do not
close global root choice, but they remove the known alternate-root exits from
the finite-certificate bucket.

The discipline used in this workspace is:

```text
bounded audits are evidence and regression tests;
algebraic formula families are proof candidates;
only written algebraic classifications are theorem-level results.
```

## 7. How To Check The Report

The report can be checked at two levels.

First, the mathematical chain above should be readable without executing code:
each theorem gives an explicit midpoint formula or an explicit reduction to a
previous formula.

Second, the formulas are mirrored by executable guardrails.  From the repository
root, run:

```bash
python3 -m unittest discover -s tests -v
```

The most important source files are:

- `experiments/pythagorean_walks.py`: certificate constructors and validators;
- `tests/test_pythagorean_walks.py`: formula tests and finite guardrails;
- `notes/pythagorean-walks-axis-subproblem.md`: detailed axis proof notebook;
- `notes/pythagorean-walks-full-conjecture-progress.md`: research notebook for
  the remaining conjecture and exceptional-ray development;
- `notes/verification-changelog.md`: audit trail for promoted lemmas,
  corrections, and guardrails.

The repository also has a Lean 4/mathlib formalization of the core certificate
algebra used by the proof program:

- `PythagoreanWalks/Certificate.lean`: definitions of integer points, legal
  Pythagorean steps, and two-step certificate validity;
- Lean-proved scaling closure for legal steps and certificates, corresponding
  to `normSq_smul`, `legalStep_smul`, and `certificateValid_smul`;
- Lean-proved sign/swap transport for legal steps and certificates,
  corresponding to `normSq_signedSwapPoint`,
  `legalStep_signedSwapPoint`, and `certificateValid_signedSwapPoint`;
- Lean-proved combined scale and sign/swap transport, corresponding to
  `signedSwapPoint_smul` and `certificateValid_signedSwapPoint_smul`;
- Lean-proved row constructors for the axis proof program:
  `certificateValid_evenAxisMidpoint`,
  `certificateValid_axisDifferenceOfSharedLeg`, and
  `certificateValid_axisSumOfSharedLeg`;
- Lean-proved Gaussian multiplication and Gaussian-divisor certificate
  transport, including `normSq_gaussianMul`,
  `certificateValid_gaussianMul`,
  `gaussianMul_eq_of_quotient_components`, and
  `certificateValid_gaussianDivisor_of_quotient_components`;
- Lean-proved diagonal Gaussian row certificates:
  `diagonalBaseCertificateValid`, `certificateValid_diagonalGaussianMultiplier`,
  and `certificateValid_diagonalGaussianRow`;
- Lean-proved signed length-difference and signed Theorem 3 row constructors:
  `certificateValid_linearDeltaDirection`,
  `certificateValid_theorem3Divisor`, `certificateValid_theorem3Unit`,
  `certificateValid_theorem3UnitDivisorProgression`, and the explicit ray rows
  `certificateValid_twoOneRayMultipleOfThree` and
  `certificateValid_oneThreeRayTheorem3`;
- Lean-proved affine consecutive-hypotenuse strip row:
  `certificateValid_affineConsecutiveHypotenuseStrip` and
  `certificateValid_consecutiveHypotenuseUnitCoordinate`;
- Lean-proved half-leg unit-coordinate row:
  `certificateValid_halfLegUnitCoordinate`;
- Lean-proved factor-five unit-coordinate row:
  `certificateValid_unitCoordinateFactorFiveParallel`;
- Lean-proved factor-four unit-coordinate row:
  `certificateValid_unitCoordinateFactorFourParallel`;
- Lean-proved one-mod-five unit-coordinate row:
  `certificateValid_unitCoordinateOneModFiveParallel`;
- Lean-proved seven-mod-ten unit-coordinate row:
  `certificateValid_unitCoordinateSevenModTenParallel`;
- Lean-proved factor-twenty-five unit-coordinate row:
  `certificateValid_unitCoordinateFactorTwentyFiveParallel`;
- Lean-proved twenty-two-mod-twenty-five unit-coordinate row:
  `certificateValid_unitCoordinateTwentyTwoModTwentyFiveParallel`;
- Lean-proved Cramer/lattice certificate constructors:
  `cramerTarget_eq_add_smul`, `latticeCertificateValid`,
  `latticeCertificateValid_of_cramer`,
  `certificateValid_latticeMidpointData`, and
  `exists_latticeCertificateValid_of_cramer`;
- Lean-proved fixed-direction parallel-factor certificate machinery:
  `normSq_mul_normSq_sub_smul`,
  `normSq_sub_smul_of_parallelFactor`,
  `isIntSquare_sub_smul_of_parallelFactor`,
  `parallelFactorCertificateValid_of_nondegenerate`,
  `sq_add_sq_of_factorPair`, `parallelFactorCompletion_of_factorPair`,
  `parallelFactorCertificateValid_of_factorPair`, and
  `parallelFactorCertificateValid_of_factorPairRow`;
- Lean-proved CRT and root-residue algebra:
  `crtModEq_compat`, `exists_int_crt_of_gcd_modEq`, and
  `gaussianRootResidue_sq_neg_one`;
- Lean-proved Gaussian root-spine line rows:
  `certificateValid_oneTwoRootSpineLine`,
  `certificateValid_oneFourRootSpineLine`,
  `certificateValid_oneFourRootSpineLineSwap`,
  `certificateValid_twoThreeOddRootSpineLine`,
  `certificateValid_twoThreeOddRootSpineLineSwap`, and
  `certificateValid_twoThreeEvenRootSpineLine`;
- `lakefile.toml`, `lean-toolchain`, and `lake-manifest.json`: Lake/mathlib
  project metadata.

These Lean checks prove reusable algebraic constructors, row certificates, and
congruence lemmas. They now cover theorem-level rows used inside the written
axis and non-axis proof program, but they do not yet formalize Theorem 4.1,
Theorem 5.1, or the paper's distance-three obstruction proofs as end-to-end
Lean statements.

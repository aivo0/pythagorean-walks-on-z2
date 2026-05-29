# Pythagorean Walks On `Z^2`: Current Progress Report

Date: 2026-05-29

This report consolidates the parts of the repository that are currently written
as proofs rather than only as proof-search notes.  It is intended to be read
beside Jan Willemson's paper "Pythagorean walks on `Z^2`"
(`arXiv:2605.20831v1`, 20 May 2026).

The report does not prove the full conjecture.  It proves two complete slices
that are now part of this workspace:

1. the axis slice;
2. the non-primitive part of the exceptional `(2,1)` ray.

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

## 5. The Exceptional `(2,1)` Ray

The primitive target `(2,1)` is a known distance-three obstruction.  The newest
complete theorem in this workspace is that every non-primitive multiple of that
ray has a two-step certificate.

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
- `two_one_ray_three_mod_four_certificate`
- `two_one_ray_double_direction_certificate`
- `two_one_ray_prime_one_mod_four_double_direction_certificate`
- `two_one_ray_prime_divisor_lift_certificate`
- `two_one_ray_prime_divisor_lift_orbit_certificate`
- `test_two_one_ray_even_family`
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
- Lean-proved Gaussian multiplication and Gaussian-divisor certificate
  transport, including `normSq_gaussianMul`,
  `certificateValid_gaussianMul`,
  `gaussianMul_eq_of_quotient_components`, and
  `certificateValid_gaussianDivisor_of_quotient_components`;
- Lean-proved diagonal Gaussian row certificates:
  `diagonalBaseCertificateValid`, `certificateValid_diagonalGaussianMultiplier`,
  and `certificateValid_diagonalGaussianRow`;
- Lean-proved Cramer/lattice certificate constructors:
  `cramerTarget_eq_add_smul`, `latticeCertificateValid`,
  `latticeCertificateValid_of_cramer`, and
  `exists_latticeCertificateValid_of_cramer`;
- Lean-proved fixed-direction parallel-factor certificate machinery:
  `normSq_mul_normSq_sub_smul`,
  `normSq_sub_smul_of_parallelFactor`,
  `isIntSquare_sub_smul_of_parallelFactor`, and
  `parallelFactorCertificateValid_of_nondegenerate`;
- Lean-proved CRT and root-residue algebra:
  `crtModEq_compat`, `exists_int_crt_of_gcd_modEq`, and
  `gaussianRootResidue_sq_neg_one`;
- `lakefile.toml`, `lean-toolchain`, and `lake-manifest.json`: Lake/mathlib
  project metadata.

These Lean checks prove reusable algebraic constructors and congruence lemmas.
They do not yet formalize Theorem 4.1, Theorem 5.1, or the paper's
distance-three obstruction proofs as end-to-end Lean statements.

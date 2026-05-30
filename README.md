# Pythagorean Walks Research Workspace

This repository studies the Pythagorean-walk graph on `Z^2` from Jan
Willemson's paper `Pythagorean walks on Z^2`
(`arXiv:2605.20831v1`, 20 May 2026).

The graph has an edge for a displacement `(dx, dy)` exactly when both coordinate
changes are nonzero and `dx^2 + dy^2` is a square. In other words, legal moves
are non-horizontal, non-vertical Pythagorean jumps.

The paper proves that the graph has diameter `3`, proves that `(1,0)`, `(2,0)`,
and `(2,1)` are distance-`3` representatives, gives one infinite family of
two-step certificates, and conjectures that these representatives and their
sign/swap images are the only distance-`3` vertices.

## Proof Report

Start with [papers/pythagorean-walks-progress-report.md](papers/pythagorean-walks-progress-report.md)
for a paper-style account of the current proved results and how to check them.
It consolidates the definitions, symmetry reductions, axis theorem, full
`(1,3)` ray theorem, non-primitive exceptional-ray theorem, executable
guardrails, and Lean theorem-kernel checks. The longer full-conjecture note
remains the research notebook for proof-search machinery and open directions.

## ELI5 Visualization

![ELI5 animation of Pythagorean walks](assets/pythagorean-walks-eli5.gif)

The animation shows the core idea: dots are lattice points, allowed jumps are
non-horizontal/non-vertical Pythagorean jumps, nearby points can still need
detours, and the known distance-`3` candidates are tiny points near the origin.

## Current Status

The full conjecture is still open in this workspace. The remaining global task
is to prove that every non-axis primitive target outside the known
distance-`3` orbit has a two-step certificate.

What is now proved or encoded:

- The known distance-`3` orbit is explicit:
  `(+/-1,0)`, `(0,+/-1)`, `(+/-2,0)`, `(0,+/-2)`, `(+/-2,+/-1)`, and
  `(+/-1,+/-2)`.
- The full axis case is classified. Every horizontal or vertical target with
  absolute nonzero coordinate at least `3` has a two-step certificate.
- The full `(1,3)` ray orbit is classified. Every nonzero multiple of `(1,3)`
  and every sign/swap image has a two-step certificate from the signed
  Theorem 3 divisor row.
- The signed `3-4-5` row now closes the full unit-divisor ray-fan table:
  `(p,2p+1)`, `(p,8p+1)`, `(9t+4,2t+1)`, and `(9t+1,8t+1)`, with their
  sign/swap orbits.
- The signed `5-12-13` row now closes its unit-divisor ray-fan table:
  `(p,8p+1)`, `(p,18p+1)`, `(25t+3,8t+1)`, and `(25t+18,18t+13)`, with their
  sign/swap orbits.
- The signed `8-15-17` row now closes another unit-divisor ray-fan table:
  `(2t+1,9t+5)`, `(2t+1,25t+13)`, `(32t+7,9t+2)`, and
  `(32t+23,25t+18)`, with their sign/swap orbits.
- The generic signed Theorem 3 unit-divisor progression is closed: whenever a
  signed triple row has one positive seed ray with divisor `1`, the full
  arithmetic progression of seed rays and all nonzero multiples have two-step
  certificates.
- For every primitive Pythagorean triple and every sign choice, the signed
  Theorem 3 unit-divisor seed is now constructive: the coprime coefficients
  `A=c-sx*a`, `B=c+sy*b` determine a canonical positive seed ray, hence an
  infinite unit-divisor fan.
- The consecutive-Euclid unit-divisor fan is closed: for every `r,p >= 1`,
  every nonzero multiple of `(p, 2r^2 p + 1)` and every sign/swap image has a
  two-step certificate from the triple `(2r+1, 2r(r+1), 2r^2+2r+1)`.
- The swapped-leg consecutive-Euclid affine strip is closed: for every
  `r,h >= 1`, `(2r^2 h - 1,h)` and its sign/swap orbit has a two-step
  certificate.
- The consecutive-hypotenuse unit-coordinate subline is closed: for every
  `m >= 2` and nonzero `t`, with `c=m^2+(m-1)^2`, `(ct,1)` and its sign/swap
  orbit has a two-step certificate.
- The half-leg unit-coordinate row is Lean-backed for every odd Pythagorean
  direction `(u,4z)`: all nonzero parameters `t` in the half-leg formula have
  two-step certificates, with automatic nondegeneracy.
- The nonstandard factor-five unit-coordinate congruence row is closed:
  `(1,25t+17)` and its sign/swap orbit have two-step certificates for every
  integer `t`.
- The companion factor-four unit-coordinate congruence row is closed:
  `(1,20t+12)` and its sign/swap orbit have two-step certificates for every
  integer `t`.
- The factor-one one-mod-five unit-coordinate congruence row is closed:
  `(1,5t+1)` and its sign/swap orbit have two-step certificates for every
  integer `t`.
- The factor-one seven-mod-ten unit-coordinate congruence row is closed:
  `(1,10t+7)` and its sign/swap orbit have two-step certificates for every
  integer `t`.
- The factor-twenty-five unit-coordinate congruence row is closed:
  `(1,25t+18)` and its sign/swap orbit have two-step certificates for every
  integer `t`.
- The twenty-two-mod-twenty-five unit-coordinate congruence row is closed:
  `(1,25t+22)` and its sign/swap orbit have two-step certificates for every
  integer `t`; the single degenerate fixed-factor parameter is discharged by
  the seven-mod-ten row.
- The promoted unit-coordinate row package now gives an infinite mod-100 cover:
  every unit-coordinate target with nonzero other coordinate outside
  `2,38,62,98 mod 100` has a two-step certificate.
- The `(8,15,17)` orthogonal lattice row now gives named infinite subfamilies
  inside all four remaining unit-coordinate mod-100 residual classes.
- The `(15,8,17)` factor-two parallel row closes the unit-coordinate class
  `(1,34t+26)` and its sign/swap orbit; its fixed row intersects all four
  remaining mod-100 residual classes with period `1700`.
- The `(12,35,37)` factor-one parallel row closes the unit-coordinate class
  `(1,37t+25)` and its sign/swap orbit; because `gcd(37,100)=1`, it also
  cuts through all four remaining mod-100 residual classes with period `3700`.
- The `(40,9,41)` factor-one parallel row closes the unit-coordinate class
  `(1,41t+23)` and its sign/swap orbit, adding another coprime-period slice
  through all four mod-100 residual classes.
- The `(28,45,53)` factor-one parallel row closes the unit-coordinate class
  `(1,53t+10)` and its sign/swap orbit, giving a third coprime-period slice
  through the same residual layer.
- The `(60,11,61)` factor-one parallel row closes the unit-coordinate class
  `(1,61t+39)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(48,55,73)` factor-one parallel row closes the unit-coordinate class
  `(1,73t+31)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(80,39,89)` factor-one parallel row closes the unit-coordinate class
  `(1,89t+71)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(72,65,97)` factor-one parallel row closes the unit-coordinate class
  `(1,97t+78)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(20,99,101)` factor-one parallel row closes the unit-coordinate class
  `(1,101t+60)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(60,91,109)` factor-one parallel row closes the unit-coordinate class
  `(1,109t+82)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(112,15,113)` factor-one parallel row closes the unit-coordinate class
  `(1,113t+83)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(88,105,137)` factor-one parallel row closes the unit-coordinate class
  `(1,137t+7)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(140,51,149)` factor-one parallel row closes the unit-coordinate class
  `(1,149t+82)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(132,85,157)` factor-one parallel row closes the unit-coordinate class
  `(1,157t+4)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(120,119,169)` factor-one parallel row closes the unit-coordinate class
  `(1,169t+168)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(52,165,173)` factor-one parallel row closes the unit-coordinate class
  `(1,173t+28)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(180,19,181)` factor-one parallel row closes the unit-coordinate class
  `(1,181t+143)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(168,95,193)` factor-one parallel row closes the unit-coordinate class
  `(1,193t+47)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(28,195,197)` factor-one parallel row closes the unit-coordinate class
  `(1,197t+112)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(60,221,229)` factor-one parallel row closes the unit-coordinate class
  `(1,229t+36)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(312,25,313)` factor-one parallel row closes the unit-coordinate class
  `(1,313t+263)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(308,75,317)` factor-one parallel row closes the unit-coordinate class
  `(1,317t+296)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(288,175,337)` factor-one parallel row closes the unit-coordinate class
  `(1,337t+241)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(180,299,349)` factor-one parallel row closes the unit-coordinate class
  `(1,349t+206)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(272,225,353)` factor-one parallel row closes the unit-coordinate class
  `(1,353t+49)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(252,275,373)` factor-one parallel row closes the unit-coordinate class
  `(1,373t+151)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(352,135,377)` factor-one parallel row closes the unit-coordinate class
  `(1,377t+299)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(340,189,389)` factor-one parallel row closes the unit-coordinate class
  `(1,389t+97)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(228,325,397)` factor-one parallel row closes the unit-coordinate class
  `(1,397t+141)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(40,399,401)` factor-one parallel row closes the unit-coordinate class
  `(1,401t+220)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(120,391,409)` factor-one parallel row closes the unit-coordinate class
  `(1,409t+302)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(420,29,421)` factor-one parallel row closes the unit-coordinate class
  `(1,421t+363)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(408,145,433)` factor-one parallel row closes the unit-coordinate class
  `(1,433t+39)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(280,351,449)` factor-one parallel row closes the unit-coordinate class
  `(1,449t+264)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(168,425,457)` factor-one parallel row closes the unit-coordinate class
  `(1,457t+248)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(380,261,461)` factor-one parallel row closes the unit-coordinate class
  `(1,461t+373)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(360,319,481)` factor-one parallel row closes the unit-coordinate class
  `(1,481t+23)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(132,475,493)` factor-one parallel row closes the unit-coordinate class
  `(1,493t+199)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(220,459,509)` factor-one parallel row closes the unit-coordinate class
  `(1,509t+96)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(440,279,521)` factor-one parallel row closes the unit-coordinate class
  `(1,521t+103)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(92,525,533)` factor-one parallel row closes the unit-coordinate class
  `(1,533t+78)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The `(420,341,541)` factor-one parallel row closes the unit-coordinate class
  `(1,541t+113)` and its sign/swap orbit, continuing the primitive
  coprime-period residual sequence.
- The `(532,165,557)` factor-one parallel row closes the unit-coordinate class
  `(1,557t+412)` and its sign/swap orbit, adding the next primitive
  coprime-period residual slice.
- The exceptional `(2,1)` ray has a named fixed-direction parallel-factor
  slice for multipliers `n ≡ 2,3 mod 5`; the infinite tails use signed
  `3-4-5` directions with factor `2`, and the small boundary multipliers are
  discharged by earlier theorem rows.
- The first full Gaussian-root primary spine is closed: for every `k >= 1`
  and nonzero `q,t,r`, the `(1,2k)` root-spine line from direction
  `(1-4k^2,4k)` and beta `(4kt+2k-1,-(2t+1))` has a two-step certificate,
  as do all sign/swap images of the target.
- The companion Gaussian-root primary spine is closed: for every `k >= 1`
  and nonzero `q,t,r`, the `(2,2k+1)` root-spine line from direction
  `(-4(2k+1),4-(2k+1)^2)` and beta `(1-2(2k+1)t,4t-1)` has a two-step
  certificate, again with its full sign/swap target orbit.
- The secondary Gaussian-root shape `(3,4)` now has named even- and odd-beta
  line rows: midpoint `r(-7,24)` certifies both the integral beta-square
  translate and the odd-beta half-square translate, with swapped forms. The
  promotion helper recognizes the full signed beta and sign/swap orbits of the
  observed secondary rows `(3,4)`, `(3,8)`, and `(4,5)`.
- The full exceptional `(2,1)` ray is classified. For every integer `n` with
  `|n| > 1`, the target `(2n,n)` and all sign/swap images have two-step
  certificates; the primitive `|n| = 1` targets are exactly the known
  distance-`3` obstructions on that ray.
- The paper's diameter-`3` construction is executable for every target, and
  the paper's no-two-step arguments for `(1,0)`, `(2,0)`, and `(2,1)` are
  tracked as symbolic guardrails.
- Exact finite audits certify every non-exception target in the signed box
  `|g|, |h| <= 500` and every non-exception unit-coordinate target with
  `|n| <= 500`.
- Scaling promotes audited primitive certificates to entire rays: if a
  primitive representative has an audited two-step certificate, every nonzero
  multiple of that representative has one too.
- A finite-direction parallel-divisor cover is now ray-lifted as a theorem
  candidate: proving the primitive representative is covered immediately
  certifies every nonzero multiple of that representative.
- The Lean formalization now proves the core certificate algebra used by the
  proof program: scaling and sign/swap transport, Gaussian multiplication and
  divisor transport, an explicit diagonal Gaussian row, Cramer-style lattice
  certificates, fixed-direction parallel-factor certificates, CRT compatibility
  and existence, affine consecutive-hypotenuse strip and unit-coordinate rows,
  the half-leg unit-coordinate row, the
  factor-five/factor-four/one-mod-five/seven-mod-ten/factor-twenty-five/
  twenty-two-mod-twenty-five unit-coordinate rows, and a Gaussian root-residue
  lemma. It also now proves several theorem-shaped certificate rows used by
  the written proof program: even-axis midpoint
  certificates, shared-leg
  axis difference/sum rows, signed length-difference rows,
  signed/divisor-strengthened Theorem 3 rows, and factor-pair parallel rows.

## Main Complete Results

The horizontal-axis theorem is the first complete theorem added here:

```text
For every integer n with |n| >= 3, d((0,0),(n,0)) <= 2.
```

The proof splits into odd targets, even targets at least `6`, and the special
target `4`. By coordinate swap it also proves the vertical axis. Together with
the paper's obstruction proof for `(1,0)` and `(2,0)`, this resolves the axis
part of the conjecture.

The full `(1,3)` ray theorem is a complete non-axis ray slice:

```text
For every integer n with |n| > 0, d((0,0),(n,3n)) <= 2.
```

The midpoint `(9n,-12n)` gives edge lengths `15|n|` and `17|n|`, and sign/swap
transport covers the full orbit.

The signed `3-4-5` unit-divisor theorem extends that ray to a table of
infinite fans:

```text
For every nonzero n, d((0,0), nR) <= 2 whenever R is one of
(p,2p+1), (p,8p+1), (9t+4,2t+1), or (9t+1,8t+1),
with p >= 1 and t >= 0.
```

The midpoint is the signed `(3,4)` direction scaled by the product of the ray
coordinates and `|n|`; sign/swap transport covers the full orbit.

The signed `5-12-13` unit-divisor theorem gives the companion table:

```text
For every nonzero n, d((0,0), nR) <= 2 whenever R is one of
(p,8p+1), (p,18p+1), (25t+3,8t+1), or (25t+18,18t+13),
with p >= 1 and t >= 0.
```

The midpoint is the signed `(5,12)` direction scaled by the product of the ray
coordinates and `|n|`.

The generic signed Theorem 3 unit-divisor progression now explains these tables
uniformly. For a triple `(a,b,c)` and signs `(sx,sy)`, put
`A=c-sx*a` and `B=c+sy*b`. If a positive seed ray `(p0,q0)` satisfies
`B*q0 - A*p0 = 1`, then every ray
`(p0+B*t, q0+A*t)` with `t >= 0` and every nonzero multiplier is certified by
the signed `(a,b)` midpoint scaled by the product of the ray coordinates.

In particular, every primitive Pythagorean triple/sign row has such a seed:
any common divisor of `A=c-sx*a` and `B=c+sy*b` divides both `a^2` and `b^2`,
so primitivity forces `gcd(A,B)=1`. The seed is computed by a modular inverse
when `B>1`, and by `(1,A+1)` when `B=1`.

The consecutive-Euclid unit-divisor theorem packages the first row of every
consecutive Euclid triple:

```text
For every r,p >= 1 and every integer n with |n| > 0,
d((0,0), n(p, 2r^2 p + 1)) <= 2.
```

The midpoint is `(2r+1, -2r(r+1))` scaled by `p(2r^2p+1)|n|`; sign/swap
transport covers the full orbit.

The swapped-leg consecutive-Euclid affine-strip theorem is the companion unit
row:

```text
For every r,h >= 1, d((0,0),(2r^2h-1,h)) <= 2.
```

The midpoint is `(2r(r+1), -(2r+1))` scaled by `(2r^2h-1)h`; sign/swap
transport covers the full orbit.

The exceptional-ray theorem is the largest complete classification:

```text
For every integer n with |n| > 1, d((0,0),(2n,n)) <= 2.
```

The proof reduces multipliers to prime seeds. Even multipliers and primes
`p == 3 mod 4` have direct certificate families. For primes `p == 1 mod 4`,
Fermat's two-square theorem gives `p = x^2 + 4y^2`, which feeds a
double-direction Pythagorean certificate. Composite multipliers scale a
certified prime divisor. Sign changes and coordinate swap transport the result
to the whole exceptional orbit.

## Non-Axis Proof Program

The repository now contains several exact two-step certificate mechanisms beyond
the original paper:

- certificate transport under sign changes and coordinate swap;
- scaling of any two-step certificate by a nonzero integer;
- square-norm Gaussian transforms and target-facing Gaussian divisibility;
- two-edge lattice membership tests;
- fixed-direction parallel divisor criteria;
- signed length-difference conic-slice probes;
- Euclid-strip, affine consecutive-hypotenuse, half-leg, unit-coordinate, and
  consecutive-direction families;
- signed and divisor-strengthened versions of the paper's Theorem 3.

The strongest current candidate for the remaining non-axis work is the
parallel-direction divisor program. In primitive positive-quadrant samples, a
layered structural stack covers all tested nontrivial targets through
`1 <= g,h <= 1000`: promoted `3-4-5` rows, orthogonal lattice rows, bounded
Pythagorean lattice-pair rows, standard determinant completions, and a bounded
squareclass split layer. This is strong evidence and a useful proof roadmap,
but it is not yet a global theorem.

The squareclass split layer has also been rewritten as infinite line families
and then as Gaussian/beta congruence data. That makes the next proof target more
specific: classify the fixed-direction congruence families, rather than grow
larger midpoint or target boxes.

The newest reduction removes the squareclass/split-factor bounds for a fixed
first-step direction. Writing a primitive Pythagorean direction as
`U = unit*alpha^2`, the split condition becomes a conjugate-root divisor problem
in the one-dimensional determinant `D = det(U,T)`. The witness now records the
exact divisor-root congruence, including the identity
`2*unit^-1*T = 2*r*alpha^2 + q*beta^2`.

That turns the current frontier into a root-shape problem instead of a larger
box search. The audited residuals are covered by primary Gaussian-root spines
`(1,2k)` and `(2,2k+1)`, plus the observed secondary shapes `(3,4)`, `(3,8)`,
and `(4,5)`. A scratch census through `1 <= g,h <= 2000` found `150`
post-structural misses: the primary spines cover `132`, and the generated spine
family covers all `150`. In the pinned `1 <= g,h <= 1000` guardrail, seven root
shapes cover all `34` structural misses.

The remaining proof target is now a finite discharging problem on congruence
rows. Divisor-obligation helpers split each residual row into a linear
determinant strip and a divisor-class condition. Strip failures in the pinned
guardrail fall into named structural families: promoted `3-4-5` integrality
rows, lattice-pair rows, orthogonal rows, or standard-completion rows. The
promoted-row counts are modular integrality counts; certificate use still goes
through the pointwise nondegeneracy check. Each fallback now has its own
determinant or coefficient-row form. The standard-completion rows are filtered
to target-compatible determinant residues and then intersected with strips as
one-parameter linear rows, so the next proof step can work with explicit
congruences rather than target-box scans.
The divisor-class side is also multiplicative now:
`divisor_residue_classes(n,c)` computes the closure of prime-power residues
represented by divisors of `n` modulo `c`. In the pinned strip guardrail, all
divisor-class failures are classified by the missing closure of the required
root-divisor class, with `215` distinct closure sets. Since the pinned moduli
are prime, the same failures are also recorded as missing exponent classes in
the cyclic groups `(Z/cZ)^*`, with primitive roots fixed for each modulus. The
new cyclic-sumset guardrail records stabilizers and Kneser defects, showing that
the main divisor side is a critical or near-critical sumset problem rather than
a larger-box search. It also records Kneser saturation gaps: once the lower
bound fills `(Z/(c-1)Z)`, divisor success is forced, so remaining failures are
short bounded sequences of prime-factor discrete logs. The strip census now
tracks this before fallback: in the pinned guardrail, `192` strip rows are
Kneser-forced divisor successes, `1228` are short-log divisor successes, and
all `4398` divisor failures are short-log rows discharged structurally.

## Finite Audits

The finite audits are exact statements: every returned row is an explicit
midpoint identity, and every certificate is checked directly.

Current finite guardrails:

- every non-exception target with `|g|, |h| <= 500`;
- every non-exception target in the sign/swap orbit of `(n,1)` with
  `|n| <= 500`;
- every multiplier `2 <= n <= 500` on the exceptional ray `(2n,n)`;
- layered structural coverage of primitive positive-quadrant samples through
  `1 <= g,h <= 1000`.

Except where a theorem is stated explicitly above, finite audits are not
extrapolated outside their stated ranges.

## Layout

- `papers/pythagorean-walks-progress-report.md`: paper-style proof report for
  the current theorem-level progress and checker workflow.

- `papers/pythagorean-walks-on-z2.md`: Markdown notes/transcription from Jan
  Willemson's paper.

- `notes/pythagorean-walks-axis-subproblem.md`: main proof notebook for the
  horizontal-axis subproblem.

- `notes/pythagorean-walks-full-conjecture-progress.md`: current non-axis proof
  notebook: symmetry reduction, exact obstruction guardrails, certificate
  families, finite audits, exceptional-ray classification, and remaining gap.

- `notes/verification-changelog.md`: audit trail for corrected hypotheses,
  promoted lemmas, and executable guardrails.

- `experiments/pythagorean_walks.py`: reusable predicates, certificate
  validators, bounded searches, and parametrized certificate generators.

- `experiments/render_eli5_gif.py`: reproducible renderer for the README
  animation.

- `tests/test_pythagorean_walks.py`: verification suite for graph predicates,
  paper examples, known exceptions, explicit certificates, formula families,
  and bounded coverage audits.

- `rust/pythagorean_walks_fast`: PyO3/maturin extension with compiled kernels
  for the performance-sensitive test guards. Build it with
  `maturin develop --release`; the Python helpers fall back to pure Python if
  the extension is not installed.

- `assets/pythagorean-walks-eli5.gif`: ELI5 animation for the problem
  statement.

- `data/horizontal_axis_certificates.json`: reusable two-step certificates for
  `3 <= n <= 20` and known horizontal-axis exceptions.

- `data/shared_leg_residue_coverage.md`: bounded residue witness table for the
  quadratic family and shared-leg generator.

- `PythagoreanWalks/Certificate.lean`: Lean/mathlib formalization of
  certificate validity and algebraic certificate constructors: scaling,
  sign/swap transport, Gaussian transport and divisibility, a diagonal Gaussian
  row, Cramer/lattice constructors, axis row constructors,
  signed-delta/Theorem 3 row constructors, fixed-direction parallel-factor
  certificates, CRT lemmas, and a Gaussian root-residue lemma.

- `lakefile.toml` and `lean-toolchain`: Lake project configuration for the Lean
  formalization.

## Test Workflow

Install the Rust-backed accelerator before running the frequently used Python
suite:

```bash
maturin develop --release
pytest -q --durations=20
```

The pytest configuration in `pyproject.toml` sets the repository root on
`PYTHONPATH` and registers the `perf` marker for exhaustive guardrail tests.

## Lean Formalization

This repository includes a Lean 4/mathlib project for theorem-kernel checks of
the algebraic reductions. `PythagoreanWalks/Certificate.lean` currently proves:

- the core definitions of points, legal Pythagorean steps, and two-step
  certificate validity;
- scaling of legal steps and certificates by any nonzero integer;
- independent sign-change and coordinate-swap transport for legal steps and
  certificates;
- the combined scale-and-sign/swap transport pattern used by orbit and ray-lift
  constructors;
- row-level axis certificate constructors: the even-axis midpoint row and the
  shared-leg difference/sum rows behind the consecutive-parameter odd-axis
  formula;
- Gaussian multiplication preserving square norms, plus certificate transport
  through square-norm Gaussian multipliers;
- a target-facing Gaussian-divisor criterion from dot/determinant quotient
  components;
- the base diagonal certificate for `(1,1)` and its parametrized Gaussian row;
- the signed length-difference row behind `linear_delta_direction_certificate`;
- the affine consecutive-hypotenuse strip row
  `certificateValid_affineConsecutiveHypotenuseStrip` and its unit-coordinate
  specialization `certificateValid_consecutiveHypotenuseUnitCoordinate`;
- the half-leg unit-coordinate row `certificateValid_halfLegUnitCoordinate`;
- the factor-five unit-coordinate parallel row
  `certificateValid_unitCoordinateFactorFiveParallel`;
- the factor-four unit-coordinate parallel row
  `certificateValid_unitCoordinateFactorFourParallel`;
- the one-mod-five unit-coordinate parallel row
  `certificateValid_unitCoordinateOneModFiveParallel`;
- the seven-mod-ten unit-coordinate parallel row
  `certificateValid_unitCoordinateSevenModTenParallel`;
- the factor-twenty-five unit-coordinate parallel row
  `certificateValid_unitCoordinateFactorTwentyFiveParallel`;
- the twenty-two-mod-twenty-five unit-coordinate parallel row
  `certificateValid_unitCoordinateTwentyTwoModTwentyFiveParallel`;
- the `(15,8,17)` factor-two unit-coordinate parallel row
  `certificateValid_unitCoordinateFifteenEightFactorTwoParallel`;
- the `(8,15,17)` orthogonal-lattice seed row inside all four remaining
  unit-coordinate mod-100 residual classes, backed by the existing
  Cramer/lattice certificate rows;
- signed and divisor-strengthened Theorem 3 certificate rows, including the
  primitive coprime unit-divisor fan, the signed `8-15-17` ray fan, the full
  `(1,3)` ray row, and an explicit multiple-of-three row on the exceptional
  `(2,1)` ray;
- the generic `(1,2k)` Gaussian-root primary spine row
  `certificateValid_oneEvenRootSpineLine`;
- the generic `(2,2k+1)` Gaussian-root primary spine row
  `certificateValid_twoOddRootSpineLine`;
- the secondary `(3,4)` Gaussian-root row
  `certificateValid_threeFourRootSpineLine`, its swapped form, and the odd-beta
  variants;
- Cramer-style two-edge lattice certificate constructors;
- a fixed-direction parallel-factor certificate criterion, including
  factor-pair row data matching the executable witness format;
- integer CRT compatibility and existence lemmas;
- a Gaussian root-residue lemma proving that a conjugate-divisibility residue is
  a square root of `-1` modulo the Gaussian norm.
- explicit Gaussian root-spine line rows:
  `certificateValid_oneTwoRootSpineLine`,
  `certificateValid_oneFourRootSpineLine`,
  `certificateValid_oneFourRootSpineLineSwap`,
  `certificateValid_twoThreeOddRootSpineLine`,
  `certificateValid_twoThreeOddRootSpineLineSwap`, and
  `certificateValid_twoThreeEvenRootSpineLine`.

These Lean row proofs cover more of the algebra used in the written axis and
non-axis proof program. The full axis theorem, the non-primitive exceptional-ray
classification, and the paper's distance-three obstruction proofs are still not
formalized as end-to-end Lean statements.

Lean setup follows the mathlib downstream-project pattern:

```bash
lake update
lake exe cache get
lake build
```

## Verification

Run:

```bash
python3 -m unittest discover -s tests -v
```

Current expected result:

```text
Ran 146 tests
OK
```

## Evidence Discipline

Bounded searches are treated as falsification tools and discovery aids, not
proofs. A result such as `not_found_within_bound` means only that the current
search box found no certificate. Exact algebraic lemmas are recorded separately
in the proof notes and backed by formula tests where possible.

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
It consolidates the definitions, symmetry reductions, axis theorem,
non-primitive exceptional-ray theorem, and executable guardrails. The longer
full-conjecture note remains the research notebook for proof-search machinery
and open directions.

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

## Main Complete Results

The horizontal-axis theorem is the first complete theorem added here:

```text
For every integer n with |n| >= 3, d((0,0),(n,0)) <= 2.
```

The proof splits into odd targets, even targets at least `6`, and the special
target `4`. By coordinate swap it also proves the vertical axis. Together with
the paper's obstruction proof for `(1,0)` and `(2,0)`, this resolves the axis
part of the conjecture.

The exceptional-ray theorem is the newest complete classification:

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
- Euclid-strip, half-leg, unit-coordinate, and consecutive-direction families;
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
first-step direction. If `U = unit*alpha^2`, then `a+i*b` lies in
`(conj(alpha))` exactly when `b == rho*a mod |U|`; for target determinant
`D = det(U,T)` and squarefree `q | D`, this becomes the divisor-root condition
`a^2 == -rho*D/q mod |U|` with `a | D/q`. The exact finite-direction fallback
now scans bounded Gaussian roots `alpha` rather than split boxes, and derives
`q,a,b` from determinant divisors. For a fixed root direction, those rows
depend only on the one-dimensional value `det(U,T)`. Its witness object also verifies
`2*unit^-1*T = 2*r*alpha^2 + q*beta^2`, making the remaining direction choice
an explicit Gaussian square-decomposition problem. A scratch census through
`1 <= g,h <= 2000` found 150 structural misses and all 150 are covered by this
exact root-bound-8 layer. The root-cover census now records which `alpha`
families appear; through `1 <= g,h <= 500`, the 10 structural misses are all
covered by five canonical root shapes. A shape-family cover is now executable:
through `1 <= g,h <= 1000`, the 34 structural misses are covered by seven
explicit root shapes, with `q,a,b` still derived from determinant divisors. The
shape-cover census records the exact per-shape counts for that audited range.

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

- `assets/pythagorean-walks-eli5.gif`: ELI5 animation for the problem
  statement.

- `data/horizontal_axis_certificates.json`: reusable two-step certificates for
  `3 <= n <= 20` and known horizontal-axis exceptions.

- `data/shared_leg_residue_coverage.md`: bounded residue witness table for the
  quadratic family and shared-leg generator.

## Verification

Run:

```bash
python3 -m unittest discover -s tests -v
```

Current expected result:

```text
Ran 144 tests
OK
```

## Evidence Discipline

Bounded searches are treated as falsification tools and discovery aids, not
proofs. A result such as `not_found_within_bound` means only that the current
search box found no certificate. Exact algebraic lemmas are recorded separately
in the proof notes and backed by formula tests where possible.

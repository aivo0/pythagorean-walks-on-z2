# Pythagorean Walks Research Workspace

This workspace studies the Pythagorean-walk graph on $\mathbb{Z}^2$. The
horizontal-axis subproblem is proved, and the current proof effort is extending
the same executable discipline to non-axis targets.

$$
\text{For every integer } n\ge3,\qquad d((0,0),(n,0))\le2.
$$

The graph has an edge for a displacement $(dx,dy)$ exactly when both coordinate
changes are nonzero and $dx^2+dy^2$ is a square.

## Current Status

- The paper's known distance-$3$ representatives are tracked with exact
  symbolic obstruction cases: $(1,0)$, $(2,0)$, and $(2,1)$.
- The horizontal-axis target is proved for every integer $n\ge3$.
- The horizontal-axis proof is exposed with sign/swap symmetry as an executable
  axis-orbit certificate for all axis targets outside $(\pm1,0)$, $(\pm2,0)$,
  $(0,\pm1)$, and $(0,\pm2)$.
- Every odd horizontal target $n\ge3$ is covered by a consecutive-parameter
  Euclid construction.
- The horizontal-axis target $n=4$ has an explicit two-step certificate.
- Every even horizontal target $n\ge6$ is covered by the midpoint lemma.
- The paper's diameter-three spanning path is encoded as an executable upper
  bound for every target.
- Certificate transport under sign changes and coordinate swap is encoded as a
  reusable proof helper.
- Two-step certificates can be scaled by any nonzero integer; this exact
  reduction is encoded and tested.
- Two-step certificates can also be transformed by square-norm Gaussian
  multipliers; the diagonal family from the $(1,1)$ certificate and a
  target-facing Gaussian divisor criterion are encoded.
- A two-edge lattice criterion is encoded, including a prime-determinant
  residue-line form and determinant-$7$, determinant-$13$, and determinant-$17$
  congruence families, plus additional small-prime congruence families modulo
  $23$, $31$, $37$, $41$, $43$, $47$, $73$, $83$, $89$, $107$, $109$, $157$,
  $173$, $179$, $191$, and $193$.
- Exact finite audits now cover every non-exception target in the boxes
  $|g|,|h|\le20$, $|g|,|h|\le30$, $|g|,|h|\le40$, $|g|,|h|\le50$, and
  $|g|,|h|\le60$, using existing exact families plus residual sign/swap-orbit
  midpoint rows.
- Every positive Pythagorean triple now gives an orthogonal lattice family with
  an exact divisibility criterion modulo the square of its hypotenuse.
- A consecutive-leg swap-lattice family is encoded; it gives exact two-step
  coverage on the lines $g+h\equiv0$ and $g-h\equiv0$ modulo each
  Pell-generated sum of consecutive Pythagorean legs.
- A general Euclid strip template is encoded; its half-leg specialization
  gives exact quadratic strip families for every odd-even Pythagorean
  direction, including non-consecutive triples, and its consecutive-direction
  specialization gives a direct divisibility test for strip targets.
- The half-leg strip has a named unit-coordinate specialization, giving exact
  quadratic families $(x(t),1)$ from every odd-even Pythagorean direction.
- The consecutive-direction strip now has a target-facing rational-ray form
  for multiples of any nonhorizontal ray, giving exact residue classes on that
  ray; the integer-slope case $(kn,n)$ is a specialization.
- A consecutive-strip subfamily is encoded for nontrivial multiples of the
  primitive obstruction direction $(2,1)$ and its sign/swap images, now using
  both signed consecutive-direction residue families.
- All even positive multiples of the primitive obstruction direction $(2,1)$
  and their sign/swap images are covered by scaling the paper's $(2,4)$
  certificate after coordinate swap.
- A finite exact base table covers additional multiplier families on the
  $(2,1)$ ray by scaling the rows $n=3,29,41,53,61,73$.
- An exact finite audit certifies every multiplier $2\le n\le500$ on the
  $(2,1)$ ray using the encoded families plus an explicit finite-audit table.
- An affine consecutive-hypotenuse strip template is encoded; its
  unit-coordinate specialization covers one coordinate $\pm1$ and the other a
  nonzero multiple of $m^2+(m-1)^2$ for every $m\ge2$.
- The signed form of the paper's Theorem 3 is encoded both as a target-facing
  predicate and as an explicit line-family constructor.
- A quadratic-strip corollary of Theorem 3 is encoded: for every integer
  $n\ge1$, the sign/swap orbit of $(2hn^2-1,h)$ and $(g,2gn^2+1)$ is covered
  whenever the fixed coordinate is nonzero.
- The shared-leg generator and residue audit are retained as proof-search
  artifacts; bounded searches are not used as proof.
- The full conjecture is not yet proved in this workspace.

## Layout

- `papers/pythagorean-walks-on-z2.md`  
  Markdown notes/transcription from Jan Willemson's paper.

- `notes/pythagorean-walks-axis-subproblem.md`  
  Main proof notebook for the horizontal-axis subproblem.

- `notes/pythagorean-walks-full-conjecture-progress.md`
  Current non-axis proof notebook: symmetry reduction, diameter-three upper
  bound, lattice families, Euclid strip templates, signed Theorem 3
  certificates, and remaining gap.

- `notes/verification-changelog.md`  
  Audit trail for corrected hypotheses, promoted lemmas, and executable
  guardrails.

- `experiments/pythagorean_walks.py`  
  Reusable predicates, certificate validators, bounded searches, and
  parametrized certificate generators.

- `tests/test_pythagorean_walks.py`  
  Verification suite for graph predicates, paper examples, known exceptions,
  explicit certificates, formula families, and bounded coverage audits.

- `data/horizontal_axis_certificates.json`  
  Reusable two-step certificates for $3\le n\le20$ and known horizontal-axis
  exceptions.

- `data/shared_leg_residue_coverage.md`  
  Bounded residue witness table for the quadratic family and shared-leg
  generator.

## Verification

Run:

```bash
python3 -m unittest discover -s tests -v
```

Current expected result:

```text
Ran 59 tests
OK
```

## Evidence Discipline

Bounded searches are treated as falsification tools, not proofs. A result such
as `not_found_within_bound` means only that the current search box found no
certificate. Exact algebraic lemmas are recorded separately in the proof notes
and backed by formula tests where possible.

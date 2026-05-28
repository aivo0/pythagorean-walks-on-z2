# Pythagorean Walks Research Workspace

This workspace studies the Pythagorean-walk graph on $\mathbb{Z}^2$, with the
current proof effort centered on the horizontal-axis subproblem:

$$
\text{For every integer } n\ge3,\qquad d((0,0),(n,0))\le2.
$$

The graph has an edge for a displacement $(dx,dy)$ exactly when both coordinate
changes are nonzero and $dx^2+dy^2$ is a square.

## Current Status

- The paper's known distance-$3$ representatives are tracked:
  $(1,0)$, $(2,0)$, and $(2,1)$.
- The horizontal-axis target is proved for every integer $n\ge3$.
- Every odd horizontal target $n\ge3$ is covered by a consecutive-parameter
  Euclid construction.
- The horizontal-axis target $n=4$ has an explicit two-step certificate.
- Every even horizontal target $n\ge6$ is covered by the midpoint lemma.
- The shared-leg generator and residue audit are retained as proof-search
  artifacts; bounded searches are not used as proof.

## Layout

- `papers/pythagorean-walks-on-z2.md`  
  Markdown notes/transcription from Jan Willemson's paper.

- `notes/pythagorean-walks-axis-subproblem.md`  
  Main proof notebook for the horizontal-axis subproblem.

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
Ran 19 tests
OK
```

## Evidence Discipline

Bounded searches are treated as falsification tools, not proofs. A result such
as `not_found_within_bound` means only that the current search box found no
certificate. Exact algebraic lemmas are recorded separately in the proof notes
and backed by formula tests where possible.

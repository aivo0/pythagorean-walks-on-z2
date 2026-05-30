Agent Goal

  Make publishable progress toward the Pythagorean-walk conjecture by closing
  named infinite theorem slices. New finite audits, helper predicates, fast
  kernels, or Lean row lemmas count as progress only when they directly reduce
  or prove a chosen theorem slice.

Strategic Focus

  The repository already has many promoted algebraic rows and only a few
  end-to-end theorem slices. The agent should therefore choose a natural
  infinite target class first, then seek a parametric or structural certificate
  mechanism that covers the whole class. Individual certificates and finite
  tables are allowed only as probes, counterexamples, or finite boundary checks.
  Promote only the algebra needed to prove that mechanism generically.

Preferred Slices

  1. Full unit-coordinate line beyond the current finite audit.
  2. Gaussian-root spine families: primary shapes `(1,2k)` and `(2,2k+1)`,
     plus secondary shapes when they admit clean statements.
  3. A clean fixed-direction divisor/congruence slice from the
     parallel-direction program.
  4. A named infinite part of the signed `3-4-5` parallel-factor layer.
  5. Stronger ray theorems using the divisor-strengthened Theorem 3 machinery.

Operating Loop

  1. State the intended theorem before adding infrastructure.
  2. Use Python to find certificates, falsify naive hypotheses, compare
     decompositions, and identify the minimal covering mechanism.
  3. Use Rust fast paths for expensive kernels: divisor/residue computations,
     lattice-pair probes, parallel-direction covers, certificate validation,
     and finite audit dispatch. Keep Python fallbacks correct and add
     Rust/Python parity for new accelerated paths.
  4. Convert successful experimental coverage into a written theorem with the
     target class, hypotheses, construction, exceptions, and proof reason.
  5. Promote the minimum Lean/mathlib rows needed for that theorem. Avoid
     standalone lemma work unless it serves the selected slice.
  6. Prefer congruence, divisor, and ray statements over target-box scans.
     Bounded computation is evidence, counterexample search, or finite
     verification, not an unqualified proof of an infinite class.

Verification

  Iterate with narrower commands, but before integrating a theorem slice run the
  relevant full stack:

  maturin develop --release
  cargo test --release
  python -m py_compile experiments/pythagorean_walks.py tests/test_pythagorean_walks.py tests/test_pythagorean_walks_fast.py
  pytest -q tests/test_pythagorean_walks_fast.py
  pytest -q -m perf tests/test_pythagorean_walks.py --durations=10
  pytest -q --durations=20
  lake build

Definition Of Progress

  A useful step leaves a theorem-shaped artifact: a written infinite statement,
  an executable certificate constructor or finite-discharge checker, targeted
  tests, minimal Lean support, and a progress-report update explaining exactly
  which part of the conjecture moved from search toward theorem-level proof.



Grand Goal

  Prove the full Pythagorean-walks conjecture: every lattice point except the known distance-three orbit has a valid two-step Pythagorean-walk certificate.

  Target Goal

  Eliminate the remaining global-root-choice fallback as an obstruction to that grand goal.

  Concretely: prove that whenever a pinned divisor obligation reaches the short_failure branch after the local divisor/structural stack, its exponent signature forces membership in
  one of the normalized alternate squareclass line-template families, and that this template produces a valid two-step certificate satisfying the original pinned strip congruence.

  Success criteria:

  - Define the short exponent signature and normalized alternate template data independently of any search radius.
  - Prove a general line/strip lemma: paired-factor residue + line/strip coefficient congruence implies certificateValid and the required determinant strip condition.
  - Prove at least one recurrent normalized family parametrically, instead of pinning more representatives.
  - Use finite tables only as regression evidence and base-frontier documentation, not as the proof mechanism.
  - End with the root-spine search removed from the target-facing global discharge path, replaced by a finite parametric case split over signature-template families.

  Completed milestone: the general line/strip row-validity bridge is now in Lean,
  and the theorem-backed normalized-family registry covers the full radius-1000
  global root-choice branch scan, all radius-1250 signature-template rows, the
  original large counterexample row, and the first two normalized families from
  the radius-1500 frontier.

  Next milestone: turn one recurring short-signature pattern into a genuine
  parametric case theorem. The proof should explain why the signature selects a
  normalized alternate family, not merely add another finite template row.

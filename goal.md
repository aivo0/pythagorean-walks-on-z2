Agent Goal

  Make progress toward the final Pythagorean-walk proof using the full updated stack: Lean/mathlib as the proof kernel, Python as the research orchestration and regression layer, and the Rust/PyO3 accelerator as the required engine for expensive finite
  searches, parity checks, and performance-sensitive audits.

  Operating Loop

  1. Use Python to explore proof candidates, generate row families, run finite audits, and compare structural decompositions.
  2. Use the Rust fast paths for heavy kernels whenever available: divisor/residue computations, lattice-pair probes, parallel-direction covers, certificate validation, and finite audit dispatch. Do not silently rely on slow fallback behavior for serious
  searches.
  3. Maintain Python fallback correctness, but treat Rust/Python parity as mandatory. Any new accelerated path must have fallback parity tests, including edge cases and representative large cases.
  4. Use Lean/mathlib to promote discovered algebra into theorem-level statements. Python and Rust may generate candidates and finite data; Lean should verify the generic mathematical reduction or the finite-discharge theorem.
  5. Prefer proof steps that reduce search:
      - replace target-box scans with congruence-row statements,
      - replace repeated lower-box traversal with the canonical cached audit dispatcher,
      - replace opaque Rust/Python enumeration with named predicates and Lean lemmas,
      - keep bounded computation as evidence or finite verification, not as an unqualified proof.

  6. Work creatively but systematically: for each candidate family, first seek counterexamples with the accelerated search stack, then compress the successful cases into algebraic rows, then formalize the row theorem or finite discharge in Lean.

  Required Verification Discipline

  Before trusting a result, run the relevant subset of the updated workflow:

  maturin develop --release
  cargo test --release
  python -m py_compile experiments/pythagorean_walks.py tests/test_pythagorean_walks.py tests/test_pythagorean_walks_fast.py
  pytest -q tests/test_pythagorean_walks_fast.py
  pytest -q -m perf tests/test_pythagorean_walks.py --durations=10
  pytest -q --durations=20
  lake build

  Use narrower commands while iterating, but the full stack must pass before considering the proof step integrated.

  Near-Term Proof Targets

  1. Formalize certificate validity, scaling, and sign/swap transport in Lean.
  2. Formalize the two-edge lattice certificate criterion, using Python/Rust audits only to generate examples and regression cases.
  3. Formalize fixed-direction factor integrality rows and their distinction from pointwise certificate nondegeneracy.
  4. Use Rust-accelerated censuses to identify compact determinant-strip CRT obligations, then prove the generic CRT row lemma in Lean.
  5. Use the Rust/Python dispatcher to stress-test Gaussian-root spine obligations, then promote stable divisor-residue claims into Lean.

  Definition Of Progress

  A useful step leaves behind all three artifacts: a passing Rust/Python regression or parity test, a Lean theorem or clearly isolated Lean TODO, and a short note explaining which part of the final conjecture moved from experimental search toward
  theorem-level proof.
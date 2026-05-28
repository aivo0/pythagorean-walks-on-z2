# Verification Changelog

This file records proof-search claims that affected the executable workspace.
The goal is to keep false starts cheap to detect and hard to reintroduce.

## 2026-05-28

### Corrected: Midpoint Coverage For Even Targets

Earlier note: the midpoint construction was said not to cover all even $n$.

Correction: every integer $a\ge3$ is a Pythagorean leg, so the midpoint
certificate covers every even target $n=2a\ge6$.

Executable guardrail:

- `midpoint_axis_certificate`
- `test_midpoint_formula_covers_even_axis_points_from_six`
- `test_every_integer_from_three_has_a_pythagorean_leg_completion`

### Guardrail: Bounded Search Is Not Impossibility

Risk: bounded failure to find a certificate can be mistaken for a proof that no
certificate exists.

Correction: bounded search results now use the explicit status
`not_found_within_bound`.

Executable guardrail:

- `BoundedSearchResult`
- `bounded_two_step_search`
- `test_bounded_search_result_labels_are_not_proofs`

### Added: Shared-Leg Generator

Claim under test: two Pythagorean triples sharing a vertical leg generate
horizontal-axis certificates by taking either the sum or difference of their
horizontal legs.

Executable guardrail:

- `shared_leg_axis_certificate_records`
- `shared_leg_axis_certificate_table`
- `test_shared_leg_generator_records_are_valid`
- `test_shared_leg_generator_bounded_odd_axis_coverage`

### Added: Quadratic Shared-Leg Family

Symbolic family:
$$
n=t(m^2+mt+1),\qquad m\ge2,\quad t\ge1.
$$

This follows from scaling the Euclid triples with parameters $(m,1)$ and
$(m+t,1)$ to the common vertical leg $2m(m+t)$.

Executable guardrail:

- `euclid_parameter_difference_certificate`
- `test_euclid_parameter_difference_family`

### Added: Residue Audit Modulo 24

Observation: both the quadratic family and the bounded shared-leg generator
hit every odd residue class modulo $24$ within the recorded bounds.

This was explicitly not a proof of the odd case. It ruled out a simple
modulo-$24$ obstruction in the sampled data.

Executable guardrail:

- `odd_residues`
- `residue_witnesses`
- `missing_residues`
- `test_residue_witnesses_for_odd_classes_mod_24`

Artifact:

- `data/shared_leg_residue_coverage.md`

### Promoted: Consecutive-Parameter Formula For Odd Targets

The odd horizontal-axis case is now proved by scaling the Euclid triples with
parameter pairs $(n+1,n)$ and $(n,n-1)$.

For every odd $n\ge3$, set
$$
a=\frac{(n-1)(2n+1)}2,\qquad
b=\frac{(n+1)(2n-1)}2,\qquad
y=n(n^2-1).
$$
Then $b-a=n$, and the scaled Euclid identities give a shared-leg certificate
$$
(0,0)\to(-a,y)\to(n,0).
$$

Executable guardrail:

- `consecutive_parameter_odd_axis_certificate`
- `test_consecutive_parameter_formula_covers_odd_axis_points`

### Promoted: Full Horizontal-Axis Case Split

The final proof now covers:

- $n=3$ by the odd formula;
- $n=4$ by the explicit certificate $(-5,12)$;
- even $n\ge6$ by the midpoint lemma;
- odd $n\ge5$ by the odd formula.

Executable guardrail:

- `explicit_axis_certificate`
- `horizontal_axis_proof_certificate`
- `test_explicit_axis_certificate_covers_four`
- `test_horizontal_axis_proof_certificate_case_split`

# Verification Changelog

This file records proof-search claims that affected the executable workspace.
The goal is to keep false starts cheap to detect and hard to reintroduce.

## 2026-05-28

### Added: Full-Conjecture Symmetry Orbit

The conjectured distance-$3$ representatives are now expanded into the exact
orbit under sign changes and coordinate swap:
$$
(\pm1,0),(0,\pm1),(\pm2,0),(0,\pm2),(\pm2,\pm1),(\pm1,\pm2).
$$

Executable guardrail:

- `sign_swap_orbit`
- `KNOWN_DISTANCE_THREE_ORBIT`
- `test_known_exception_orbit_under_stated_symmetries`

### Added: Exact Obstruction Guardrail For Known Distance-Three Vertices

The paper's no-two-step arguments for $(1,0)$, $(2,0)$, and $(2,1)$ are now
tracked as symbolic obstruction cases rather than only as bounded failed
searches. The guardrail records the possible integer distance differences from
the triangle inequality and the exact contradiction used in each case.

The nontrivial $(2,1)$ case includes the lemma that $y^2-y+1$ is a square only
for $y=0$ or $y=1$; those candidates force an illegal horizontal or vertical
edge.

Executable guardrail:

- `canonical_known_distance_three_representative`
- `possible_integer_distance_differences`
- `y_squared_minus_y_plus_one_is_square`
- `known_distance_three_obstruction_cases`
- `test_known_exception_symbolic_obstruction_cases`
- `test_y_squared_minus_y_plus_one_square_lemma`

### Added: Diameter-Three Path Constructor

The paper's spanning identity
$$
(g,h)=(3g+4h)(3,4)-(3g+4h)(4,3)+(g+h)(4,-3)
$$
is now executable. Zero coefficients are omitted, giving a path of length at
most $3$ for every target. This supplies the upper-bound side for the known
distance-$3$ vertices when combined with the paper's no-two-step arguments.

Executable guardrail:

- `theorem1_three_step_path`
- `test_theorem1_path_gives_three_step_upper_bound`

### Added: Certificate Scaling Reduction

Any two-step certificate for $T$ scales to a two-step certificate for $kT$ for
every nonzero integer $k$. This is now recorded as an exact reduction for
non-axis work; it cannot be applied to primitive obstruction directions until an
independent certificate is known for a nontrivial multiple.

Executable guardrail:

- `scale_certificate`
- `test_certificate_scaling_preserves_validity`

### Added: Square-Norm Gaussian Certificate Transform

Any valid two-step certificate can be multiplied by a Gaussian integer
$a+ib$ with $a^2+b^2$ a nonzero square. This scales all squared edge lengths by
$a^2+b^2$, so transformed edges keep integer length. The constructor returns no
certificate only when a transformed edge becomes horizontal or vertical.

Applying this to the base certificate
$(0,0)\to(4,-3)\to(1,1)$ gives an exact diagonal family: for
$a=(g+h)/2$ and $b=(h-g)/2$, targets $(g,h)$ are covered whenever $a,b$ are
integers, $a^2+b^2$ is a nonzero square, and the transformed certificate is
nondegenerate.

Executable guardrail:

- `gaussian_multiply`
- `gaussian_transform_certificate`
- `diagonal_pythagorean_multiplier_certificate`
- `test_gaussian_transform_preserves_certificates_when_nondegenerate`
- `test_diagonal_pythagorean_multiplier_family`

### Added: Target-Facing Gaussian Divisor Criterion

For any base target $B=(b_1,b_2)$ with a valid two-step certificate, a requested
target $T=(g,h)$ is now checked for exact Gaussian divisibility by $B$. The
quotient is
$$
\left(\frac{gb_1+hb_2}{b_1^2+b_2^2},\
\frac{hb_1-gb_2}{b_1^2+b_2^2}\right)
$$
when both coordinates are integral. If that quotient has nonzero square norm,
the square-norm Gaussian transform gives a certificate unless it degenerates to
an axis edge.

Executable guardrail:

- `gaussian_quotient_if_integer`
- `gaussian_divisor_certificate`
- `first_gaussian_divisor_certificate`
- `test_gaussian_divisor_certificate_family`

### Added: Two-Edge Lattice Criterion

If a target $T$ can be written as $rU+sV$ for legal Pythagorean edge vectors
$U,V$ and nonzero integers $r,s$, then $rU$ is a two-step midpoint for $T$.
Cramer's rule is now implemented for the associated lattice membership check.

Executable guardrail:

- `lattice_coefficients`
- `lattice_two_step_certificate`
- `test_lattice_coefficients_build_two_step_certificates`

### Added: Prime-Determinant Lattice Line Criterion

When legal edge vectors $U,V$ have $|\det(U,V)|=p$ prime, their generated
lattice is exactly one residue line modulo $p$. Targets on that line are
certified by the lattice criterion unless they are already one-step scalar
multiples of $U$ or $V$.

Executable guardrail:

- `is_prime`
- `determinant`
- `same_projective_class_mod`
- `prime_determinant_lattice_certificate`
- `test_prime_determinant_lattice_line_criterion`

### Added: Determinant-Seven Congruence Families

The 3-4-5 direction pairs $(3,4),(4,3)$ and $(3,-4),(4,-3)$ prove distance
$\leq2$ for every nonzero target satisfying $g+h\equiv0\pmod7$ or
$g-h\equiv0\pmod7$. Zero coefficient cases are exactly one-step scalar
multiples of one of the basis directions.

Executable guardrail:

- `DETERMINANT_SEVEN_DIRECTION_PAIRS`
- `determinant_seven_lattice_certificate`
- `test_determinant_seven_congruence_families`

### Added: Determinant-Thirteen Congruence Families

The direction pairs $(3,4),(8,15)$, $(3,-4),(8,-15)$, $(4,3),(15,8)$, and
$(4,-3),(15,-8)$ prove distance $\leq2$ for every nonzero target satisfying
$g\equiv\pm3h\pmod {13}$ or $g\equiv\pm4h\pmod {13}$. Zero coefficient cases
are one-step scalar multiples of one of the basis directions.

Executable guardrail:

- `DETERMINANT_THIRTEEN_DIRECTION_PAIRS`
- `determinant_thirteen_lattice_certificate`
- `test_determinant_thirteen_congruence_families`

### Added: Determinant-Seventeen Congruence Families

The direction pairs $(3,4),(20,21)$, $(3,-4),(20,-21)$, $(4,3),(21,20)$, and
$(4,-3),(21,-20)$ prove distance $\leq2$ for every nonzero target satisfying
$g\equiv\pm5h\pmod {17}$ or $g\equiv\pm7h\pmod {17}$. Zero coefficient cases
are one-step scalar multiples of one of the basis directions.

Executable guardrail:

- `DETERMINANT_SEVENTEEN_DIRECTION_PAIRS`
- `determinant_seventeen_lattice_certificate`
- `test_determinant_seventeen_congruence_families`

### Added: Additional Small-Prime Congruence Families

The prime-determinant lattice criterion now has an encoded table for additional
moduli:

- modulo $23$: $g\equiv\pm5h$ or $g\equiv\pm9h$;
- modulo $31$: $g\equiv\pm3h$ or $g\equiv\pm10h$;
- modulo $37$: $g\equiv\pm10h$ or $g\equiv\pm11h$;
- modulo $41$: $g\equiv\pm h$;
- modulo $43$: $g\equiv\pm10h$, $\pm13h$, $\pm15h$, or $\pm20h$;
- modulo $47$: $g\equiv\pm4h$, $\pm7h$, $\pm11h$, $\pm12h$, $\pm17h$, or
  $\pm20h$.

Each row is backed by an explicit pair of legal Pythagorean directions with
determinant $\pm p$. As before, zero coefficient cases are one-step scalar
multiples of a basis direction.

Executable guardrail:

- `SMALL_PRIME_DETERMINANT_DIRECTION_PAIRS`
- `small_prime_lattice_certificate`
- `test_additional_small_prime_congruence_families`

### Added: General Euclid Strip Template

For any legal direction $U=(u,v)$, nonzero strip coordinate $q$, and nonzero
Euclid parameter $A$, the choice $B=uA-q$ gives a certificate for
$(ru+2AB,q)$ when $r=(q-(B^2-A^2))/v$ is a nonzero integer and the Euclid
vector $(2AB,B^2-A^2)$ is nondegenerate.

The half-leg specialization $A=vt/2$ is now encoded for odd-even directions.
For example, $U=(15,8)$ proves the exact unit-coordinate family
$(-6240t^2+217t,1)$ for every nonzero integer $t$, with symmetric variants
coming from sign changes and coordinate swap.

Executable guardrail:

- `euclid_strip_certificate`
- `half_leg_strip_certificate`
- `test_euclid_strip_template`
- `test_half_leg_strip_family`

### Added: Solved Consecutive-Direction Strip

For every odd $u\ge3$, the consecutive direction
$U=(u,(u^2-1)/2)$ makes the Euclid strip equation linear in the parameter $A$.
A target $(g,q)$ with $q\ne0$ is covered whenever
$$
q(u^2+1)\mid \frac{u^2-1}{2}g+uq(q-1),
$$
subject to the same nondegeneracy conditions as the general strip.

Executable guardrail:

- `consecutive_direction_strip_certificate`
- `test_consecutive_direction_strip_solver`

### Added: Consecutive Strip Family On The $(2,1)$ Ray

The solved consecutive-direction strip now has promoted subfamilies on the ray
through the primitive obstruction. For odd $u\ge3$ and $t\ge1$, set
$$
n=t(u^2+1)-2u+1.
$$
If $t\ne u-1$, then $(2n,n)$ and its sign/swap images have two-step
certificates. The excluded case is exactly the Euclid-parameter degeneration
$B=0$ in this construction; it is not an impossibility claim for those targets.
The opposite signed consecutive direction also covers
$$
n=t(u^2+1)+2u+1,\qquad t\ge0,
$$
with no additional degeneration.

Executable guardrail:

- `two_one_ray_consecutive_certificate`
- `two_one_ray_consecutive_orbit_certificate`
- `test_two_one_ray_consecutive_family`

### Added: Even Multiples Of The $(2,1)$ Ray

The paper's certificate for $(2,4)$ swaps to a certificate for $(4,2)$, and the
scaling reduction covers every $(4m,2m)$ with $m\ge1$. Sign changes and
coordinate swap give the same result for the full orbit of these even
multipliers.

Executable guardrail:

- `two_one_ray_even_certificate`
- `two_one_ray_even_orbit_certificate`
- `test_two_one_ray_even_family`

### Added: Explicit Base Multipliers On The $(2,1)$ Ray

A finite table of exact base certificates is now promoted for
$n\in\{3,29,41,53,61,73\}$ on the targets $(2n,n)$. Scaling each base row gives
an infinite family of multiples, and sign/swap images are handled by symmetry.

These rows were found during proof search but promoted only after exact
certificate validation. No claim is made that the table is complete.

Executable guardrail:

- `EXPLICIT_TWO_ONE_RAY_BASE_CERTIFICATES`
- `two_one_ray_explicit_base_certificate`
- `two_one_ray_explicit_base_orbit_certificate`
- `test_two_one_ray_explicit_base_table`

### Added: Finite Audit On The $(2,1)$ Ray Up To 500

The existing ray families, together with a new finite-audit table of exact base
certificates, now certify every target $(2n,n)$ for $2\le n\le500$. The new table
adds the base multipliers
$$
109,113,149,181,209,233,241,269,281,293,313,353,361,373,409,421,449,461,473.
$$

The bounded search that discovered these rows is not used as proof. Only the
explicit rows and their certificate identities are promoted, with no claim beyond
$n=500$.

Executable guardrail:

- `EXPLICIT_TWO_ONE_RAY_FINITE_AUDIT_CERTIFICATES`
- `two_one_ray_finite_audit_certificate`
- `two_one_ray_finite_audit_orbit_certificate`
- `test_two_one_ray_finite_audit_to_500`

### Deferred: Small-Direction Euclid Strip Cover

After adding the general strip template, I ran a bounded scan using primitive
directions from Euclid parameters up to $8$ and strip parameters
$|A|\le60$ over the box $|g|,|h|\le30$. The templates supplied additional
certificates but still left many uncovered targets in that box.

This was only a coverage probe for possible corollaries. No finite-cover claim
or impossibility claim was promoted from it.

### Added: Affine Consecutive-Hypotenuse Strip Family

For every $m\ge2$, let
$u=2m-1$, $v=2m(m-1)$, and $c=m^2+(m-1)^2$. The affine template
$$
\left(cqt+u\frac{q(1-q)}v,\ q\right),
\qquad v\mid q(1-q),
$$
now has an explicit Euclid-parameter certificate whenever the displayed edge
vectors are nondegenerate. The unit-coordinate family is the specialization
$q=1$, and the earlier multiple-of-five strip is the first case $m=2$.

Executable guardrail:

- `affine_consecutive_hypotenuse_certificate`
- `consecutive_hypotenuse_unit_coordinate_certificate`
- `unit_coordinate_consecutive_hypotenuse_certificate`
- `unit_coordinate_multiple_of_five_certificate`
- `test_affine_consecutive_hypotenuse_family`
- `test_unit_coordinate_consecutive_hypotenuse_family`
- `test_unit_coordinate_multiple_of_five_family`

### Deferred: Broad Unit-Coordinate Strip Table Search

I attempted to generate a finite table of affine Euclid-factor formulas for the
whole strip $(n,1)$. The unrestricted symbolic search was too broad to promote:
it did not produce a clean audited table before becoming a performance sink.

No theorem or test was added for that attempted table. The result promoted from
that line of search was only the explicit consecutive-hypotenuse family above.

### Added: Signed Theorem 3 Certificate Family

The paper's Theorem 3 is now represented as an actual midpoint constructor.
For a Pythagorean triple $(a,b,c)$, signs $s_x,s_y\in\{-1,1\}$, and non-axis
target $(g,h)$, the relation
$$
(c-s_xa)g=(c+s_yb)h-1
$$
produces the midpoint
$$
(s_xagh,\ s_ybgh).
$$

This note uses the signed midpoint convention from
`notes/pythagorean-walks-full-conjecture-progress.md`; it matches the mixed-sign
examples after Theorem 3 in the paper.

Executable guardrail:

- `theorem3_certificate`
- `theorem3_certificates`
- `test_paper_theorem3_signed_certificate_examples`
- `test_paper_theorem3_rejects_non_matching_relations`

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

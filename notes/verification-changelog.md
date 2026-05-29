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

### Added: Axis-Orbit Proof Certificate

The completed horizontal-axis proof now has an executable sign/swap wrapper.
`axis_orbit_proof_certificate` returns valid two-step certificates for every
horizontal or vertical target with absolute nonzero coordinate at least $3$, and
returns no certificate for the axis obstruction coordinates $\pm1,\pm2$.

Executable guardrail:

- `axis_orbit_proof_certificate`
- `test_axis_orbit_proof_certificate`

### Added: Sign/Swap Certificate Transport

Any valid two-step certificate can be transported under the graph automorphisms
given by sign changes and coordinate swap. This is now encoded once as a
reusable helper instead of being rederived in each symmetric family.

Executable guardrail:

- `signed_swap_point`
- `sign_swap_certificate`
- `test_sign_swap_certificate_transport`

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

### Added: Signed Length-Difference Conic Slice Probe

The distance-difference parameter from the known obstruction proof is now also
used constructively. For a target $T=(g,h)$, midpoint
$P=K(u,v)$, primitive Pythagorean direction $(u,v,c)$, and signed length
difference $d=|OP|-|TP|$, the two-step condition reduces to
$$
2K(gu+hv-dc)=g^2+h^2-d^2.
$$

The bounded constructor tests this divisibility condition over primitive
Pythagorean directions and signed $d$ values ordered by increasing $|d|$. This
is intentionally recorded as a discovery/probe layer rather than a theorem-level
classification.

The signed form of Theorem 3 is now recognized as the unit-denominator case of
the same identity: for positive $g,h$, use $K=gh$ and $d=g-h$, so
`gu + hv - dc = 1` is exactly the paper's linear relation after substituting
the signed Pythagorean direction.

The first exact lift from this viewpoint is the divisor-strengthened Theorem 3:
replace the constant $1$ by a nonzero divisor $q$ of $gh$. The midpoint is
scaled down from the paper's $gh$ coefficient to $gh/q$, and degenerate
horizontal or vertical graph steps are rejected.

The same strengthened theorem now has a ray-facing constructor. For target
$n(p,q)$, the divisor is $nL$, where
$$
L=(c+s_yb)q-(c-s_xa)p.
$$
Thus a fixed triple and sign pair certifies all multipliers with $L\mid pqn$.
The case $|L|=1$ covers an entire ray; on the exceptional ray $(2,1)$ this
recovers infinite multiplier classes without touching the primitive obstruction.
The fixed-divisor calculation is now exposed separately as the multiplier
modulus $|L|/\gcd(|L|,|pq|)$, so a ray family can be tracked as an exact
residue-class statement instead of as repeated pointwise searches.

A Pell-parametrized subfamily of the ray divisors is also encoded. Taking
Euclid parameters $m=x+y$, $n=y$ and signs $(1,-1)$ gives
$L=qx^2-2py^2$; swapping the Euclid legs gives $L=2qy^2-px^2$. Thus primitive
ray coverage can be attacked through divisor conditions for these binary
quadratic forms, while multiplier coverage uses the same modulus formula.

The same calculation is now exposed in a more general fixed-linear-delta
recognizer. For a fixed legal direction $(u,v)$ and
$d=\alpha g+\beta h$, the divisibility condition
$$
2(gu+hv-dc)\mid g^2+h^2-d^2
$$
gives a direct two-step midpoint when the quotient is positive and
nondegenerate.

Executable guardrail:

- `primitive_pythagorean_directions`
- `signed_delta_values`
- `delta_slice_certificate`
- `linear_delta_direction_certificate`
- `test_delta_slice_direction_generator_and_delta_order`
- `test_delta_slice_certificate_formula`
- `test_theorem3_is_unit_delta_slice_case`
- `test_linear_delta_direction_certificate`
- `theorem3_divisor_certificate`
- `test_theorem3_divisor_generalization`
- `theorem3_ray_divisor`
- `theorem3_ray_divisor_certificate`
- `theorem3_ray_divisor_modulus`
- `theorem3_ray_pell_divisor_certificate`
- `test_theorem3_ray_divisor_family`
- `test_theorem3_ray_divisor_modulus`
- `test_theorem3_ray_pell_divisor_family`
- `test_delta_slice_bounded_discovery_probe`

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

### Added: Parallel-Direction Divisor Reduction

The one-direction version of the lattice problem is now encoded as an exact
divisor criterion. Fix a legal direction $U=(u,v)$ with $u^2+v^2=c^2$ and look
for a midpoint $rU$. For target $T=(g,h)$, write
$$
A=T\cdot U,\qquad D=\det(U,T).
$$
The condition $|T-rU|^2=s^2$ is equivalent to
$$
(c^2r-A)^2-c^2s^2=-D^2,
$$
which factors as
$$
\bigl(cs-(c^2r-A)\bigr)\bigl(cs+(c^2r-A)\bigr)=D^2.
$$
Thus a positive divisor of $D^2$ determines a candidate first-step coefficient
$r$, and the certificate checker validates the resulting midpoint. This gives a
finite target-facing divisor test for every fixed first-step direction.
The divisor data is now represented as a Pythagorean-completion witness:
if $D^2=FG$, then $B=(G-F)/2$ and $H=(G+F)/2$ satisfy $B^2+D^2=H^2$; the
direction accepts the completion when $H$ is divisible by the direction length
and $B+T\cdot U$ is divisible by the squared direction length.
The signed standard completions of a leg are also named separately: factors
$1,D^2$ for odd determinant legs, and $2,D^2/2$ for even determinant legs.
This gives a closed congruence subfamily inside the broader divisor-completion
criterion.
The finite-direction standard-completion cover is separated from the full
divisor cover. It has an explicit guardrail counterexample: $(1,92)$ is not
covered by standard completions for parameter bound $8$, while the full
direction cover succeeds using direction $(4,3)$ and the nonstandard factor
$5$ of $365^2$.
That counterexample is now generalized: for every integer $t$, the target
$(1,25t+17)$ is certified by direction $(4,3)$, factor $5$, and midpoint
$(4r,3r)$ with $r=40t^2+55t+19$. The sign/swap orbit is handled by a
target-facing constructor.
The next residual layer is now represented by a bounded-factor cover helper:
after standard completions, the helper tries only nonstandard factors up to a
fixed bound. The guardrail records that standard completions plus bounded
factors through $1000$ cover the primitive positive-quadrant sample through
$80$, again as discovery evidence rather than a proof.
For the unit-coordinate slice, fixed direction/factor pairs now expose their
accepted residue classes for $(1,h)$ directly. This promotes examples such as
the factor-five family $h\equiv17\pmod {25}$ and the factor-four family
$h\equiv12\pmod {20}$ into reusable congruence families with sign/swap
transport.
The same fixed direction/factor criterion is now ray-facing. For a ray
$R=(p,q)$ and target $T=nR$, put
$$
A_0=R\cdot U,\qquad D_0=\det(U,R).
$$
The forced coefficient is
$$
r(n)=\frac{(n^2D_0^2/F-F)/2+nA_0}{c^2},
$$
when $F\mid n^2D_0^2$, so the arithmetic condition depends only on the
multiplier $n$ modulo $2c^2F$. The new ray helper enumerates those multiplier
classes and then runs the ordinary certificate check on the actual target.
On the exceptional ray $(2,1)$, direction $(4,3)$ with factor $2$ gives the
exact class $n\equiv2\pmod5$ in natural modulus $100$, while direction
$(-4,-3)$ with factor $2$ gives $n\equiv3\pmod5$; the primitive obstruction is
not hidden, because the final graph check still rejects the degenerate first
representatives.
The full two-dimensional direction $(4,3)$, factor-$5$ congruence family is
also named. Its modulus is $250$; exactly $1250$ residue classes have integral
first-step coefficients, and $1188$ of them produce valid nondegenerate
certificates in the fundamental representative box.

Corrected guardrail: the $1188$ valid-representative count is not itself a
periodic certificate-class condition. Nondegeneracy is pointwise after the
periodic integrality check. The class represented by $(3,6)$ is the retained
counterexample: $(3,6)$ has an integral coefficient but a degenerate graph
step, while the same residue class contains the valid translated target
$(253,6)$ with midpoint $(8808,6606)$.
For fixed direction and factor, the arithmetic conditions are now exposed with
their natural modulus $2c^2F$, making each such subfamily an explicit quadratic
congruence class before the final nondegeneracy check. Small fixed-factor
residue classes can now be enumerated directly, separating modular coverage
from target-size searches.
The finite-direction candidate constructor applies this exact test over all
signed primitive Pythagorean directions up to a chosen Euclid parameter. With
parameter $8$, the guardrail covers primitive positive-quadrant non-edge targets
through $1000$ without using residual midpoint tables. This remains bounded
evidence only, but the former scratch range is now an executable guardrail.

Executable guardrail:

- `positive_divisors`
- `ParallelDirectionFactorWitness`
- `standard_pythagorean_completion_factors`
- `parallel_direction_factor_witness`
- `parallel_direction_standard_completion_certificate`
- `parallel_direction_standard_completion_cover_certificate`
- `unit_coordinate_factor_five_parallel_certificate`
- `unit_coordinate_factor_five_parallel_orbit_certificate`
- `unit_coordinate_parallel_factor_residues`
- `unit_coordinate_parallel_factor_orbit_certificate`
- `ray_multiplier`
- `ray_parallel_factor_residues`
- `ray_parallel_factor_certificate`
- `four_three_factor_five_parallel_certificate`
- `parallel_direction_bounded_factor_cover_certificate`
- `parallel_direction_factor_modulus`
- `parallel_direction_factor_coefficient`
- `parallel_direction_factor_residue_classes`
- `parallel_direction_factor_certificate_residue_classes`
- `parallel_direction_factor_residue_certificate`
- `parallel_direction_factor_certificate`
- `parallel_direction_certificate`
- `parallel_direction_cover_certificate`
- `test_parallel_direction_divisor_reduction`
- `test_parallel_direction_standard_completion_family`
- `test_parallel_direction_standard_completion_cover_probe`
- `test_unit_coordinate_factor_five_parallel_family`
- `test_unit_coordinate_parallel_factor_residue_family`
- `test_ray_parallel_factor_residue_family`
- `test_four_three_factor_five_parallel_congruence_family`
- `test_parallel_direction_bounded_factor_cover_probe`
- `test_parallel_direction_factor_residue_classes`
- `test_parallel_direction_candidate_cover_probe`

### Added: Orthogonal Triple Lattice Family

Every positive Pythagorean triple $(a,b,c)$ now gives a target-facing exact
lattice criterion. The directions $(a,b)$ and $(-b,a)$ have determinant $c^2$,
so a target $(g,h)$ is covered whenever
$$
c^2\mid ag+bh
\qquad\text{and}\qquad
c^2\mid ah-bg.
$$
Nonzero Cramer coefficients give a two-step certificate; zero coefficients are
already one-step scalar multiples of a legal direction.

Executable guardrail:

- `pythagorean_triple_orthogonal_lattice_certificate`
- `test_pythagorean_triple_orthogonal_lattice_family`

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

### Added: Consecutive-Leg Swap Lattice Family

Consecutive-leg Pythagorean triples $(a,a+1,c)$ now generate exact swap-lattice
families. With $z=2a+1$, the pair $(a,a+1),(a+1,a)$ covers targets with
$g+h\equiv0\pmod z$, and the signed pair $(a,-a-1),(a+1,-a)$ covers
$g-h\equiv0\pmod z$, apart from zero-coefficient cases that are already
one-step targets.

The consecutive triples are generated by the Pell recurrence
$$
z'=3z+4c,\qquad c'=2z+3c
$$
from $(z,c)=(7,5)$. This promotes an infinite exact family and explains the
determinant-$7$ and determinant-$41$ swap rows as initial cases.

Executable guardrail:

- `consecutive_leg_pythagorean_triple`
- `consecutive_leg_swap_lattice_certificate`
- `test_consecutive_leg_swap_lattice_family`

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
  $\pm20h$;
- modulo $73$: $g\equiv\pm13h$, $\pm17h$, $\pm28h$, or $\pm30h$;
- modulo $83$: $g\equiv\pm8h$, $\pm19h$, $\pm31h$, or $\pm35h$;
- modulo $89$: $g\equiv\pm13h$ or $\pm41h$;
- modulo $107$: $g\equiv\pm22h$ or $\pm34h$;
- modulo $109$: $g\equiv\pm45h$ or $\pm46h$;
- modulo $157$: $g\equiv\pm14h$, $\pm19h$, $\pm33h$, $\pm56h$, $\pm66h$, or
  $\pm69h$;
- modulo $173$: $g\equiv\pm18h$, $\pm34h$, $\pm48h$, or $\pm56h$;
- modulo $179$: $g\equiv\pm12h$ or $\pm15h$;
- modulo $191$: $g\equiv\pm13h$, $\pm44h$, $\pm87h$, or $\pm90h$;
- modulo $193$: $g\equiv\pm86h$ or $\pm92h$.

Each row is backed by an explicit pair of legal Pythagorean directions with
determinant $\pm p$. As before, zero coefficient cases are one-step scalar
multiples of a basis direction.

Executable guardrail:

- `SMALL_PRIME_DETERMINANT_DIRECTION_PAIRS`
- `small_prime_lattice_certificate`
- `test_additional_small_prime_congruence_families`

### Added: Exact Box-20 Finite Audit

The exact constructors now certify every non-exception target in the finite box
$|g|,|h|\le20$. One-step targets are handled by the graph predicate. The
remaining non-edge cases are covered by the existing axis, lattice, and
$(2,1)$-ray families plus a residual table of nine explicit midpoint rows,
transported under sign changes and coordinate swap.

The residual rows were discovered computationally, but the promoted audit uses
only the explicit midpoint identities and the exact constructors listed above;
it makes no claim outside this finite box.

Executable guardrail:

- `BOX_TWENTY_RESIDUAL_CERTIFICATES`
- `box_twenty_residual_certificate`
- `box_twenty_audit_certificate`
- `test_box_twenty_finite_audit`

### Added: Exact Box-30 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le30$. The box-$20$ residual table is reused, and fifteen additional
explicit midpoint representatives complete the sign/swap residual cases in the
larger box.

As with the box-$20$ audit, the promoted claim is finite and exact: each
residual row is validated as a two-step certificate, and the test checks every
target in the finite box against the exact constructors or the graph's one-step
predicate.

Executable guardrail:

- `BOX_THIRTY_RESIDUAL_CERTIFICATES`
- `box_thirty_residual_certificate`
- `box_thirty_audit_certificate`
- `test_box_thirty_finite_audit`

### Added: Exact Box-40 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le40$. The box-$30$ residual table is reused, and twenty-two additional
explicit midpoint representatives complete the sign/swap residual cases in the
larger box.

This remains a finite exact claim: each residual row is validated directly, and
the test checks every target in the finite box against either the graph's
one-step predicate or an exact certificate constructor.

Executable guardrail:

- `BOX_FORTY_RESIDUAL_CERTIFICATES`
- `box_forty_residual_certificate`
- `box_forty_audit_certificate`
- `test_box_forty_finite_audit`

### Added: Exact Box-50 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le50$. The box-$40$ residual table is reused, and thirty-six additional
explicit midpoint representatives complete the sign/swap residual cases in the
larger box.

The promoted claim remains finite and exact: every residual midpoint row is
validated directly, and the test enumerates the whole finite box while keeping
one-step targets and the known distance-three orbit separate.

Executable guardrail:

- `BOX_FIFTY_RESIDUAL_CERTIFICATES`
- `box_fifty_residual_certificate`
- `box_fifty_audit_certificate`
- `test_box_fifty_finite_audit`

### Added: Exact Box-60 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le60$. The box-$50$ residual table is reused, and forty-one additional
explicit midpoint representatives complete the sign/swap residual cases in the
larger box.

As before, this is not an extrapolated bounded-search statement: every residual
row is an explicit midpoint identity, and the test enumerates the finite box
while keeping one-step targets and the known distance-three orbit separate.

Executable guardrail:

- `BOX_SIXTY_RESIDUAL_CERTIFICATES`
- `box_sixty_residual_certificate`
- `box_sixty_audit_certificate`
- `test_box_sixty_finite_audit`

### Added: Exact Box-70 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le70$. The box-$60$ residual table is reused, and fifty-one additional
explicit midpoint representatives complete the sign/swap residual cases in the
larger box.

The promoted statement is still deliberately finite: every residual row is an
explicit midpoint identity, and the test enumerates the entire box while
separating one-step targets from the known distance-three orbit.

Executable guardrail:

- `BOX_SEVENTY_RESIDUAL_CERTIFICATES`
- `box_seventy_residual_certificate`
- `box_seventy_audit_certificate`
- `test_box_seventy_finite_audit`

### Added: Determinant-53 And Determinant-67 Congruence Families

The prime-determinant lattice table now includes exact congruence families
modulo $53$ and modulo $67$:

- modulo $53$: $g\equiv\pm14h$ or $g\equiv\pm19h$;
- modulo $67$: $g\equiv\pm16h$ or $g\equiv\pm21h$.

Each congruence line is backed by an explicit pair of legal Pythagorean
directions with determinant $\pm p$, so this is an infinite lattice-family
extension rather than a bounded search claim.

Some older finite fallback rows now lie in these new congruence families. They
remain in the cumulative audit tables as directly checked midpoint identities;
the finite tables are not asserted to be minimal.

Executable guardrail:

- `SMALL_PRIME_DETERMINANT_DIRECTION_PAIRS`
- `small_prime_lattice_certificate`
- `test_additional_small_prime_congruence_families`

### Added: Further Prime-Determinant Congruence Families

The prime-determinant lattice table now includes another exact batch:

- modulo $149$: $g\equiv\pm54h$ or $g\equiv\pm69h$;
- modulo $211$: $g\equiv\pm51h$ or $g\equiv\pm91h$;
- modulo $239$: $g\equiv\pm h$;
- modulo $241$: $g\equiv\pm101h$ or $g\equiv\pm105h$;
- modulo $251$: $g\equiv\pm31h$ or $g\equiv\pm81h$;
- modulo $269$: $g\equiv\pm32h$ or $g\equiv\pm42h$.

As before, every row is an explicit pair of legal Pythagorean directions with
determinant $\pm p$, so the promoted claim is an infinite congruence-family
claim, not bounded evidence.

Executable guardrail:

- `SMALL_PRIME_DETERMINANT_DIRECTION_PAIRS`
- `small_prime_lattice_certificate`
- `test_additional_small_prime_congruence_families`

### Added: Exact Box-80 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le80$. This layer reuses the exact families, the unit-coordinate
finite audit, target-facing strip recognizers over fixed finite parameter
ranges, and the box-$70$ residual table, then adds forty-eight explicit
residual midpoint representatives.

The promoted statement is finite and exact: the test enumerates the whole box,
keeps one-step targets and known distance-three targets separate, and validates
each returned two-step certificate.

Executable guardrail:

- `BOX_EIGHTY_RESIDUAL_CERTIFICATES`
- `box_eighty_residual_certificate`
- `box_eighty_audit_certificate`
- `test_box_eighty_finite_audit`

### Added: Exact Box-90 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le90$. This layer reuses the box-$80$ audit, applies the exact
constructors to the new outer ring, and adds forty-six explicit residual
midpoint representatives.

The promoted statement is finite and exact: the test enumerates the whole box,
keeps one-step targets and known distance-three targets separate, and validates
each returned two-step certificate.

Executable guardrail:

- `BOX_NINETY_RESIDUAL_CERTIFICATES`
- `box_ninety_residual_certificate`
- `box_ninety_audit_certificate`
- `test_box_ninety_finite_audit`

### Added: Exact Box-100 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le100$. This layer reuses the box-$90$ audit, applies the same exact
constructors to the new outer ring, and adds fifty-eight explicit residual
midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_ONE_HUNDRED_RESIDUAL_CERTIFICATES`
- `box_one_hundred_residual_certificate`
- `box_one_hundred_audit_certificate`
- `test_box_one_hundred_finite_audit`

### Added: Exact Box-110 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le110$. This layer reuses the box-$100$ audit, applies the same exact
constructors to the new outer ring, and adds sixty-five explicit residual
midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_ONE_TEN_RESIDUAL_CERTIFICATES`
- `box_one_ten_residual_certificate`
- `box_one_ten_audit_certificate`
- `test_box_one_ten_finite_audit`

### Added: Exact Box-120 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le120$. This layer reuses the box-$110$ audit, applies the same exact
constructors to the new outer ring, and adds eighty explicit residual midpoint
representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_ONE_TWENTY_RESIDUAL_CERTIFICATES`
- `box_one_twenty_residual_certificate`
- `box_one_twenty_audit_certificate`
- `test_box_one_twenty_finite_audit`

### Added: Exact Box-130 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le130$. This layer reuses the box-$120$ audit, applies the same exact
constructors to the new outer ring, and adds seventy-six explicit residual
midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_ONE_THIRTY_RESIDUAL_CERTIFICATES`
- `box_one_thirty_residual_certificate`
- `box_one_thirty_audit_certificate`
- `test_box_one_thirty_finite_audit`

### Added: Exact Box-140 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le140$. This layer reuses the box-$130$ audit, applies the same exact
constructors to the new outer ring, and adds eighty-seven explicit residual
midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_ONE_FORTY_RESIDUAL_CERTIFICATES`
- `box_one_forty_residual_certificate`
- `box_one_forty_audit_certificate`
- `test_box_one_forty_finite_audit`

### Added: Exact Box-150 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le150$. This layer reuses the box-$140$ audit, applies the same exact
constructors to the new outer ring, and adds ninety-eight explicit residual
midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_ONE_FIFTY_RESIDUAL_CERTIFICATES`
- `box_one_fifty_residual_certificate`
- `box_one_fifty_audit_certificate`
- `test_box_one_fifty_finite_audit`

### Added: Exact Box-160 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le160$. This layer reuses the box-$150$ audit, applies the same exact
constructors to the new outer ring, and adds one hundred two explicit residual
midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_ONE_SIXTY_RESIDUAL_CERTIFICATES`
- `box_one_sixty_residual_certificate`
- `box_one_sixty_audit_certificate`
- `test_box_one_sixty_finite_audit`

### Added: Exact Box-170 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le170$. This layer reuses the box-$160$ audit, applies the same exact
constructors to the new outer ring, and adds one hundred explicit residual
midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_ONE_SEVENTY_RESIDUAL_CERTIFICATES`
- `box_one_seventy_residual_certificate`
- `box_one_seventy_audit_certificate`
- `test_box_one_seventy_finite_audit`

### Added: Exact Box-180 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le180$. This layer reuses the box-$170$ audit, applies the same exact
constructors to the new outer ring, and adds one hundred six explicit residual
midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_ONE_EIGHTY_RESIDUAL_CERTIFICATES`
- `box_one_eighty_residual_certificate`
- `box_one_eighty_audit_certificate`
- `test_box_one_eighty_finite_audit`

### Added: Exact Box-190 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le190$. This layer reuses the box-$180$ audit, applies the same exact
constructors to the new outer ring, and adds one hundred forty-one explicit
residual midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_ONE_NINETY_RESIDUAL_CERTIFICATES`
- `box_one_ninety_residual_certificate`
- `box_one_ninety_audit_certificate`
- `test_box_one_ninety_finite_audit`

### Added: Exact Box-200 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le200$. This layer reuses the box-$190$ audit, applies the same exact
constructors to the new outer ring, and adds one hundred ten explicit residual
midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_TWO_HUNDRED_RESIDUAL_CERTIFICATES`
- `box_two_hundred_residual_certificate`
- `box_two_hundred_audit_certificate`
- `test_box_two_hundred_finite_audit`

### Added: Exact Box-210 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le210$. This layer reuses the box-$200$ audit, applies the same exact
constructors to the new outer ring, and adds one hundred twenty-nine explicit
residual midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_TWO_TEN_RESIDUAL_CERTIFICATES`
- `box_two_ten_residual_certificate`
- `box_two_ten_audit_certificate`
- `test_box_two_ten_finite_audit`

### Added: Exact Box-220 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le220$. This layer reuses the box-$210$ audit, applies the same exact
constructors to the new outer ring, and adds one hundred thirty-four explicit
residual midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_TWO_TWENTY_RESIDUAL_CERTIFICATES`
- `box_two_twenty_residual_certificate`
- `box_two_twenty_audit_certificate`
- `test_box_two_twenty_finite_audit`

### Added: Exact Box-230 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le230$. This layer reuses the box-$220$ audit, applies the same exact
constructors to the new outer ring, and adds one hundred sixty-three explicit
residual midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_TWO_THIRTY_RESIDUAL_CERTIFICATES`
- `box_two_thirty_residual_certificate`
- `box_two_thirty_audit_certificate`
- `test_box_two_thirty_finite_audit`

### Added: Exact Box-240 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le240$. This layer reuses the box-$230$ audit, applies the same exact
constructors to the new outer ring, and adds one hundred sixty-two explicit
residual midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_TWO_FORTY_RESIDUAL_CERTIFICATES`
- `box_two_forty_residual_certificate`
- `box_two_forty_audit_certificate`
- `test_box_two_forty_finite_audit`

### Added: Exact Box-250 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le250$. This layer reuses the box-$240$ audit, applies the same exact
constructors to the new outer ring, and adds one hundred seventy-three explicit
residual midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_TWO_FIFTY_RESIDUAL_CERTIFICATES`
- `box_two_fifty_residual_certificate`
- `box_two_fifty_audit_certificate`
- `test_box_two_fifty_finite_audit`

### Added: Exact Box-260 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le260$. This layer reuses the box-$250$ audit, applies the same exact
constructors to the new outer ring, and adds one hundred sixty-seven explicit
residual midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_TWO_SIXTY_RESIDUAL_CERTIFICATES`
- `box_two_sixty_residual_certificate`
- `box_two_sixty_audit_certificate`
- `test_box_two_sixty_finite_audit`

### Added: Exact Box-270 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le270$. This layer reuses the box-$260$ audit, applies the same exact
constructors to the new outer ring, and adds one hundred seventy-three explicit
residual midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_TWO_SEVENTY_RESIDUAL_CERTIFICATES`
- `box_two_seventy_residual_certificate`
- `box_two_seventy_audit_certificate`
- `test_box_two_seventy_finite_audit`

### Added: Exact Box-280 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le280$. This layer reuses the box-$270$ audit, applies the same exact
constructors to the new outer ring, and adds one hundred seventy-eight explicit
residual midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_TWO_EIGHTY_RESIDUAL_CERTIFICATES`
- `box_two_eighty_residual_certificate`
- `box_two_eighty_audit_certificate`
- `test_box_two_eighty_finite_audit`

### Added: Exact Box-290 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le290$. This layer reuses the box-$280$ audit, applies the same exact
constructors to the new outer ring, and adds one hundred ninety-seven explicit
residual midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_TWO_NINETY_RESIDUAL_CERTIFICATES`
- `box_two_ninety_residual_certificate`
- `box_two_ninety_audit_certificate`
- `test_box_two_ninety_finite_audit`

### Added: Exact Box-300 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le300$. This layer reuses the box-$290$ audit, applies the same exact
constructors to the new outer ring, and adds one hundred ninety-two explicit
residual midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_THREE_HUNDRED_RESIDUAL_CERTIFICATES`
- `box_three_hundred_residual_certificate`
- `box_three_hundred_audit_certificate`
- `test_box_three_hundred_finite_audit`

### Added: Exact Box-310 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le310$. This layer reuses the box-$300$ audit, applies the same exact
constructors to the new outer ring, and adds two hundred nineteen explicit
residual midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_THREE_TEN_RESIDUAL_CERTIFICATES`
- `box_three_ten_residual_certificate`
- `box_three_ten_audit_certificate`
- `test_box_three_ten_finite_audit`

### Added: Exact Box-320 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le320$. This layer reuses the box-$310$ audit, applies the same exact
constructors to the new outer ring, and adds two hundred six explicit residual
midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_THREE_TWENTY_RESIDUAL_CERTIFICATES`
- `box_three_twenty_residual_certificate`
- `box_three_twenty_audit_certificate`
- `test_box_three_twenty_finite_audit`

### Added: Exact Box-330 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le330$. This layer reuses the box-$320$ audit, applies the same exact
constructors to the new outer ring, and adds two hundred thirty-one explicit
residual midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_THREE_THIRTY_RESIDUAL_CERTIFICATES`
- `box_three_thirty_residual_certificate`
- `box_three_thirty_audit_certificate`
- `test_box_three_thirty_finite_audit`

### Added: Exact Box-340 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le340$. This layer reuses the box-$330$ audit, applies the same exact
constructors to the new outer ring, and adds two hundred thirty-seven explicit
residual midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_THREE_FORTY_RESIDUAL_CERTIFICATES`
- `box_three_forty_residual_certificate`
- `box_three_forty_audit_certificate`
- `test_box_three_forty_finite_audit`

### Added: Exact Box-350 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le350$. This layer reuses the box-$340$ audit, applies the same exact
constructors to the new outer ring, and adds two hundred forty-six explicit
residual midpoint representatives.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate.

Executable guardrail:

- `BOX_THREE_FIFTY_RESIDUAL_CERTIFICATES`
- `box_three_fifty_residual_certificate`
- `box_three_fifty_audit_certificate`
- `test_box_three_fifty_finite_audit`

### Added: Exact Box-360 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le360$. This layer reuses the box-$350$ audit, applies the same exact
constructors to the new outer ring, and then uses the finite-direction
parallel-cover constructor with parameter bound $8$ for the remaining shell
targets. No residual midpoint rows are needed in
`BOX_THREE_SIXTY_RESIDUAL_CERTIFICATES`.

The promoted statement remains finite and exact: the test enumerates the whole
box, keeps one-step targets and known distance-three targets separate, and
validates each returned two-step certificate. The finite-direction cover remains
a theorem candidate, not an unbounded proof.

Executable guardrail:

- `BOX_THREE_SIXTY_RESIDUAL_CERTIFICATES`
- `box_three_sixty_residual_certificate`
- `box_three_sixty_audit_certificate`
- `test_box_three_sixty_finite_audit`

### Added: Exact Box-500 Finite Audit

The finite audit now extends to every non-exception target with
$|g|,|h|\le500$. This layer reuses the box-$360$ audit, applies the same exact
constructors to the remaining finite box, and then uses the finite-direction
parallel-cover constructor with parameter bound $8$ for all remaining targets.
No residual midpoint rows are needed in `BOX_FIVE_HUNDRED_RESIDUAL_CERTIFICATES`.

The promoted statement remains finite and exact: the test enumerates the whole
signed box, keeps one-step targets and known distance-three targets separate,
validates each returned two-step certificate, and checks rejection outside the
box. The finite-direction cover remains a theorem candidate, not an unbounded
proof.

Executable guardrail:

- `BOX_FIVE_HUNDRED_RESIDUAL_CERTIFICATES`
- `box_five_hundred_residual_certificate`
- `box_five_hundred_audit_certificate`
- `test_box_five_hundred_finite_audit`

### Added: Primitive-Ray Lift Of Box-500 Seeds

The finite box-500 audit now has an explicit unbounded ray consequence. For a
target $T=dT_0$ with primitive representative $T_0$, any audited two-step
certificate for $T_0$ scales to a two-step certificate for $T$. The helper
`box_five_hundred_ray_lift_certificate` applies the theorem-level axis and
exceptional-ray helpers first, then scales the box-audit certificate whenever
$T_0$ lies in $|g|,|h|\le500$.

This is not a new larger box: it promotes the existing finite primitive seeds
into whole certified rays. Primitive representatives outside the audited box
remain the next structural target.

Executable guardrail:

- `box_five_hundred_ray_lift_certificate`
- `test_box_five_hundred_ray_lift_promotes_primitive_seeds`

### Added: Primitive-Ray Lift Of The Finite-Direction Cover

The finite-direction parallel-cover candidate is now separated from target
scale. The helper `parallel_direction_primitive_ray_certificate` reduces a
nonzero target $T=dT_0$ to its primitive representative, applies the exact
parallel-direction divisor cover to $T_0$, and scales the primitive certificate
by $d$. Axis targets and solved non-primitive exceptional-ray targets are
handled first by their theorem-level helpers.

This keeps the remaining candidate theorem focused on primitive rays: proving
that the finite direction set covers a primitive representative immediately
certifies every nonzero multiple of that representative.

The witness layer is now exposed as well. `parallel_direction_witness` returns
the first valid determinant-leg completion for one fixed direction,
`parallel_direction_cover_witness` records the corresponding row for the finite
direction set, and `parallel_direction_primitive_ray_witness` records the
primitive representative, scale, and base completion. These helpers make the
finite-direction cover auditable by direction and factor instead of only by the
final midpoint certificate.

The new `parallel_direction_cover_witness_census` summarizes this witness data
over primitive positive-quadrant samples. The guardrail records that the
$1\le g,h\le30$ primitive sample has $543$ nontrivial targets and no uncovered
target for parameter bound $8$, with the leading witness rows concentrated in
the signed $3$-$4$-$5$ directions and small factors.

The dominant signed $3$-$4$-$5$ rows are now promoted as their own fixed cover:
`PARALLEL_DIRECTION_PROMOTED_345_FACTOR_ROWS` contains the eight signed
$3$-$4$-$5$ directions and the factors $1,2,3,4,5,6,8,9,25$. The helper
`parallel_direction_promoted_345_factor_certificate` tests only those fixed
rows. On the primitive positive sample $1\le g,h\le50$, this layer certifies
$1461$ of $1529$ nontrivial targets; the remaining $68$ are verified to be
covered by the full finite-direction divisor cover.

The residual tail is now being attacked by named structure rather than larger
boxes. `pythagorean_orthogonal_lattice_cover_certificate` tests canonical
orthogonal pairs $U=(u,v)$ and $U^\perp=(-v,u)$ from primitive Pythagorean
directions. With parameter bound $4$, it covers $8$ of the $68$ residual
primitive targets left by the promoted $3$-$4$-$5$ layer in the sample
$1\le g,h\le50$:
$(1,38)$, $(2,29)$, $(19,22)$, $(22,19)$, $(22,31)$, $(29,2)$, $(31,22)$,
and $(38,1)$. The guardrail records $60$ residual targets remaining after this
orthogonal layer, with first misses
$(2,49)$, $(5,14)$, $(5,26)$, $(5,34)$, $(5,46)$, $(7,10)$, $(7,50)$,
and $(8,9)$.

The remaining residuals now have a second structural explanation:
`pythagorean_lattice_pair_cover_certificate` enumerates bounded-index pairs of
primitive Pythagorean directions and applies the exact lattice coefficient
criterion. With Euclid-parameter bound $25$ and determinant bound $1435$, the
guardrail table has $38240$ ordered direction pairs. This layer covers all
$60$ residual primitive targets left in the $1\le g,h\le50$ sample after the
promoted $3$-$4$-$5$ and orthogonal layers. On the larger primitive sample
$1\le g,h\le100$, the same three-layer pipeline leaves only
$(29,98)$, $(50,53)$, $(53,50)$, and $(98,29)$.

Those four misses, and the later misses through $1\le g,h\le300$, are covered
by the standard determinant-completion layer over signed Pythagorean directions
with parameter bound $8$. The fixed helper
`pythagorean_layered_structural_certificate` now runs the promoted $3$-$4$-$5$
rows, the parameter-$4$ orthogonal lattice rows, the parameter-$25$/index-$1435$
lattice-pair rows, and then this standard-completion layer. On the primitive
positive sample $1\le g,h\le300$, excluding one-step targets and the known
distance-three orbit, the guardrail count is:
$$
54685=52549+40+2032+64.
$$
Thus the current fixed structural stack closes that entire primitive sample
without adding a larger midpoint or target box.

The structural stack was then tested against a wider primitive positive sample.
Through $1\le g,h\le1000$, it covers $607989$ of $608023$ nontrivial primitive
targets. The remaining $34$ targets are all covered by a bounded squareclass
split layer: write the determinant-completion factor as $q a^2$, with paired
factor $q b^2$ and determinant leg $qab$. The fixed layer uses signed
Pythagorean directions up to parameter $8$, squareclass $q\le23$, and split
factor $a\le179$, encoded as `pythagorean_layered_split_certificate`. The
full `pythagorean_layered_parallel_certificate` still keeps the exact
finite-direction divisor criterion as a theorem-candidate fallback beyond this
audited frontier.

Executable guardrail:

- `PrimitiveRayParallelDirectionWitness`
- `ParallelDirectionCoverWitnessCensus`
- `PythagoreanLatticePairWitness`
- `ParallelDirectionSquareclassSplitWitness`
- `PARALLEL_DIRECTION_PROMOTED_345_FACTOR_ROWS`
- `PYTHAGOREAN_LAYERED_ORTHOGONAL_MAX_PARAMETER`
- `PYTHAGOREAN_LAYERED_LATTICE_PAIR_MAX_PARAMETER`
- `PYTHAGOREAN_LAYERED_LATTICE_PAIR_MAX_DETERMINANT`
- `PYTHAGOREAN_LAYERED_STANDARD_COMPLETION_MAX_PARAMETER`
- `PYTHAGOREAN_LAYERED_SPLIT_MAX_SQUARECLASS`
- `PYTHAGOREAN_LAYERED_SPLIT_MAX_FACTOR`
- `PYTHAGOREAN_LAYERED_PARALLEL_MAX_PARAMETER`
- `squareclass_decomposition`
- `squarefree_numbers`
- `parallel_direction_witness`
- `parallel_direction_cover_witness`
- `parallel_direction_cover_witness_census`
- `parallel_direction_promoted_345_factor_witness`
- `parallel_direction_promoted_345_factor_certificate`
- `pythagorean_orthogonal_lattice_cover_certificate`
- `pythagorean_lattice_direction_pairs`
- `pythagorean_lattice_pair_witness`
- `pythagorean_lattice_pair_cover_certificate`
- `parallel_direction_squareclass_split_witness`
- `parallel_direction_squareclass_split_certificate`
- `parallel_direction_squareclass_split_cover_witness`
- `parallel_direction_squareclass_split_cover_certificate`
- `pythagorean_layered_structural_certificate`
- `pythagorean_layered_split_certificate`
- `pythagorean_layered_parallel_certificate`
- `parallel_direction_primitive_ray_witness`
- `parallel_direction_primitive_ray_certificate`
- `test_parallel_direction_cover_witness_census`
- `test_parallel_direction_promoted_345_factor_cover`
- `test_pythagorean_orthogonal_lattice_cover`
- `test_pythagorean_lattice_pair_cover_closes_promoted_residual_tail`
- `test_pythagorean_layered_structural_cover_closes_sample_to_300`
- `test_pythagorean_layered_split_cover_closes_sample_to_1000`
- `test_parallel_direction_primitive_ray_lift`

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

### Added: Half-Leg Unit-Coordinate Families

The half-leg Euclid strip now has a named unit-coordinate constructor. For every
legal odd-even Pythagorean direction $(u,v)$ and every nonzero integer $t$, it
certifies
$$
\left(
t(u^2-v)+\frac{uv(1+2v-u^2)t^2}{4},\ 1
\right),
$$
subject only to the standard nondegeneracy checks. The consecutive-hypotenuse
unit-coordinate family is exactly the specialization where the quadratic
coefficient is zero.

Executable guardrail:

- `half_leg_unit_coordinate_certificate`
- `test_half_leg_unit_coordinate_family`

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

### Added: Rational-Slope Consecutive Ray Families

The solved consecutive-direction strip is now promoted from the special
$(2,1)$ ray to every nonhorizontal rational ray $(pn,qn)$. For odd $u\ge3$,
$v=(u^2-1)/2$, and $M=u^2+1$, the signed consecutive directions cover the exact
divisibility conditions
$$
qM\mid vp+uq(qn-1)
\qquad\text{and}\qquad
qM\mid vp-uq(qn-1),
$$
subject only to the standard Euclid-strip nondegeneracy checks.

The integer-slope residue classes are the specialization $q=1$.

Executable guardrail:

- `rational_slope_consecutive_ray_certificate`
- `integer_slope_consecutive_ray_certificate`
- `test_rational_slope_consecutive_ray_family`
- `test_integer_slope_consecutive_ray_family`

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

### Added: Three-Mod-Four Multipliers On The $(2,1)$ Ray

The companion consecutive-strip family now has a named congruence corollary:
every positive multiplier $n\equiv3\pmod4$ on the target ray $(2n,n)$ has a
two-step certificate. For $n\ge7$, write $u=(n-1)/2$ and use the explicit
midpoint
$$
P=(2u,1-u^2).
$$
The edge lengths are $u^2+1$ and $u^2+2u+2$. The remaining case $n=3$ is
handled by the existing exact base row. Sign/swap images are handled by the
orbit constructor.

Executable guardrail:

- `two_one_ray_three_mod_four_certificate`
- `two_one_ray_three_mod_four_orbit_certificate`
- `test_two_one_ray_three_mod_four_family`

### Added: Five-Or-Seventeen-Mod-Twenty Multipliers On The $(2,1)$ Ray

The odd-leg $u=3$ consecutive-strip specialization now has a named corollary:
every positive multiplier $n\equiv5$ or $17\pmod {20}$ on the target ray
$(2n,n)$ has a two-step certificate. For $n=10t-5$, use
$$
P=(3r,4r),\qquad r=2(t^2+t-1),
$$
and for $n=10t+7$, use
$$
P=(-3r,4r),\qquad r=2(t^2+t-1).
$$
The excluded degeneration in the general first signed strip would require
$t=2$, which is not in the $5\pmod {20}$ subfamily. Sign/swap images are
handled by the orbit constructor.

Executable guardrail:

- `two_one_ray_five_or_seventeen_mod_twenty_certificate`
- `two_one_ray_five_or_seventeen_mod_twenty_orbit_certificate`
- `test_two_one_ray_five_or_seventeen_mod_twenty_family`

### Added: Mod-20 Skeleton On The $(2,1)$ Ray

The exact ray families now reduce the positive multiplier problem on the
exceptional ray to two residue classes. Even multipliers, the
$3\pmod4$ family, and the $5$/$17\pmod {20}$ consecutive-strip family cover all
classes modulo $20$ except $1,9,13$. The fixed parallel-direction family with
$U=(-4,-3)$ and factor $2$ covers the remaining class $13\pmod {20}$: for
$n=5t+3$ it gives
$$
r=t^2-t-1,\qquad P=(-4r,-3r).
$$
The degenerate representative $n=3$ is already handled by the $3\pmod4$
family. Thus the only multiplier classes not covered by this modular skeleton
are
$$
n\equiv1,9\pmod {20}.
$$
This is an infinite-family reduction, not a finite audit.
The helper `two_one_ray_mod20_skeleton_residues` records the exact finite
residue split modulo $20$, so this statement is not inferred from the bounded
multiplier loop in the test.

Executable guardrail:

- `two_one_ray_mod20_skeleton_certificate`
- `two_one_ray_mod20_skeleton_orbit_certificate`
- `two_one_ray_mod20_skeleton_residues`
- `test_two_one_ray_mod20_skeleton_family`

### Added: Mod-260 Skeleton On The $(2,1)$ Ray

The fixed $u=5$ consecutive-strip specialization refines the mod-$20$
skeleton. Combining periods modulo $\operatorname{lcm}(20,26)=260$, the
additional residue classes
$$
n\equiv69,89,121,141\pmod {260}
$$
are covered. The exact uncovered residue list modulo $260$ is now recorded in
`two_one_ray_mod260_skeleton_residues`, leaving
$$
\begin{gathered}
1,9,21,29,41,49,61,81,101,109,129,149,\\
161,169,181,189,201,209,221,229,241,249.
\end{gathered}
$$

Executable guardrail:

- `two_one_ray_mod260_skeleton_certificate`
- `two_one_ray_mod260_skeleton_orbit_certificate`
- `two_one_ray_mod260_skeleton_residues`
- `test_two_one_ray_mod260_skeleton_family`

### Added: Mod-Ten Divisor Family On The $(2,1)$ Ray

The parallel-direction divisor method now gives a divisor criterion on the
exceptional ray. Write $n=dq$. If $q\equiv3\pmod {10}$, use direction
$U=(3,-4)$ and factor $F=d$; then
$$
r=\frac{d(121q^2+4q-1)}{50}.
$$
If $q\equiv7\pmod {10}$, use $U=(-3,4)$ and factor $F=d$; then
$$
r=\frac{d(121q^2-4q-1)}{50}.
$$
The congruence on $q$ makes the relevant numerator divisible by $50$, and the
ordinary certificate checker verifies the nondegenerate graph steps.

Consequently every positive multiplier with a divisor $3$ or $7$ modulo $10$
is covered. After the mod-$20$ skeleton, any still-uncovered multiplier on the
exceptional ray must therefore have all divisors congruent to $1$ or $9$ modulo
$10$; for the odd non-multiple-of-$5$ residuals, equivalently all prime factors
are $1$ or $9$ modulo $10$. The new arithmetic helpers make this residual
condition executable instead of leaving it as prose.

Executable guardrail:

- `has_divisor_three_or_seven_mod_ten`
- `all_prime_factors_one_or_nine_mod_ten`
- `prime_factors`
- `two_one_ray_complement_divisor_residues`
- `two_one_ray_complement_divisor_certificate`
- `two_one_ray_mod_ten_divisor_certificate`
- `two_one_ray_mod_ten_divisor_orbit_certificate`
- `test_two_one_ray_mod_ten_divisor_family`
- `test_mod_ten_divisor_residual_prime_factor_reduction`

### Added: Mod-26 Divisor Family On The $(2,1)$ Ray

The complement-factor parallel construction now has a second small instance
from the $5$-$12$-$13$ directions. For $n=dq$, use factor $F=d$. The quotient
classes and directions are
$$
\begin{array}{c|c}
q \pmod {26} & U\\
\hline
3 & (5,12)\\
7 & (-5,12)\\
19 & (5,-12)\\
23 & (-5,-12).
\end{array}
$$
Thus every positive multiplier with a divisor in one of those four classes has
an exact two-step certificate. This is recorded as a divisor/factorization
sieve, not as a periodic condition on the multiplier.

Executable guardrail:

- `two_one_ray_mod_twenty_six_divisor_certificate`
- `two_one_ray_mod_twenty_six_divisor_orbit_certificate`
- `test_two_one_ray_mod_twenty_six_divisor_family`

### Added: Combined Mod-130 Divisor Sieve On The $(2,1)$ Ray

The mod-$10$ and mod-$26$ divisor sieves now have a combined arithmetic
guardrail modulo
$$
\operatorname{lcm}(10,26)=130.
$$
The covered divisor residues are
$$
\begin{gathered}
3,7,13,17,19,23,27,29,33,37,43,45,47,49,53,55,57,59,63,67,\\
71,73,75,77,81,83,85,87,93,97,101,103,107,111,113,117,123,127
\pmod {130}.
\end{gathered}
$$
This records the combined result as an exact factorization sieve rather than a
periodic condition on the multiplier. It also catches examples such as
$361=19^2$: the mod-$10$ residual prime-factor condition alone would not
exclude it, but divisor $19$ is covered modulo $130$.

Executable guardrail:

- `has_divisor_in_residue_classes`
- `two_one_ray_mod_130_divisor_residues`
- `has_two_one_ray_mod_130_divisor`
- `test_combined_mod_130_divisor_residual_reduction`

### Added: Complement-Divisor Sieve And Mod-34 Family

The complement-factor construction is now represented as a reusable divisor
sieve over signed Pythagorean directions. For each direction, the factor-one
quotient residues are compressed from their natural modulus $2|U|^2$ to the
minimal period when possible, and finite direction sets can be combined by
taking a periodic residue union.

The quotient classes are no longer discovered by scanning the natural modulus.
For $U=(u,v)$, set $c^2=u^2+v^2$, $a=2u+v$, and $b=u-2v$. The factor-one
condition for $q(2,1)$ is
$$
b^2q^2+2aq-1\equiv0\pmod {2c^2}.
$$
When $u$ is odd and $\gcd(b,c)=1$, the helper computes the unique odd class
modulo $2c$ from
$$
q\equiv-a(b^2)^{-1}\pmod c,\qquad q\equiv1\pmod2.
$$
The test suite checks this root formula against direct quadratic-congruence
enumeration for primitive signed directions with Euclid parameter at most $20$
and hypotenuse at most $300$.

The same formula now has a hypotenuse-layer interface: for a fixed hypotenuse
$c$, generate every primitive signed Pythagorean direction with that
hypotenuse, retain the directions with a root, and union their quotient classes
modulo $2c$. This produces the named divisor layers from one reusable
constructor; for example $c=41$ gives
$13,29,53,69\pmod {82}$.

The new $8$-$15$-$17$ instance gives:
$$
\begin{array}{c|c}
q \pmod {34} & U\\
\hline
7 & (15,-8)\\
13 & (15,8)\\
21 & (-15,-8)\\
27 & (-15,8).
\end{array}
$$
Thus every positive multiplier with a divisor in one of those four classes has
an exact two-step certificate.

The next $20$-$21$-$29$ layer gives:
$$
\begin{array}{c|c}
q \pmod {58} & U\\
\hline
7 & (-21,-20)\\
25 & (-21,20)\\
33 & (21,-20)\\
51 & (21,20).
\end{array}
$$
Together with the mod-$10$, mod-$26$, and mod-$34$ divisor families, this gives
an exact divisor layer for every multiplier having a divisor
$7,25,33$, or $51$ modulo $58$.

The $12$-$35$-$37$ layer gives:
$$
\begin{array}{c|c}
q \pmod {74} & U\\
\hline
7 & (-35,12)\\
23 & (-35,-12)\\
51 & (35,12)\\
67 & (35,-12).
\end{array}
$$
Together with the earlier divisor families, this gives a combined
small-direction quotient period
$$
\operatorname{lcm}(10,26,34,58,74)=2371330.
$$
The covered quotient-divisor residues are exactly the classes that are
$3$ or $7$ modulo $10$, or $3,7,19,23$ modulo $26$, or $7,13,21,27$ modulo
$34$, or $7,25,33,51$ modulo $58$, or $7,23,51,67$ modulo $74$; this gives
$896090$ residue classes modulo $2371330$.
The period is only a compact way to store divisor classes; it is not a finite
box and not a periodic condition on the multiplier itself.

The next $9$-$40$-$41$ layer gives:
$$
\begin{array}{c|c}
q \pmod {82} & U\\
\hline
13 & (9,-40)\\
29 & (9,40)\\
53 & (-9,-40)\\
69 & (-9,40).
\end{array}
$$
This layer is retained as a separate exact family rather than folded into the
combined tuple, because the combined period would gain a factor $41$. It
removes the former residual prime multipliers $521$, $1201$, and $1669$ below
$2000$.

Executable guardrail:

- `minimal_periodic_residue_classes`
- `periodic_residue_union`
- `pythagorean_directions_for_hypotenuse`
- `two_one_ray_complement_divisor_root`
- `two_one_ray_complement_divisor_period`
- `two_one_ray_complement_divisor_sieve_residue_classes`
- `two_one_ray_complement_divisor_sieve_certificate`
- `two_one_ray_hypotenuse_divisor_directions`
- `two_one_ray_hypotenuse_divisor_residue_classes`
- `two_one_ray_hypotenuse_divisor_certificate`
- `two_one_ray_mod_2210_divisor_residues`
- `has_two_one_ray_mod_2210_divisor`
- `two_one_ray_mod_64090_divisor_residues`
- `has_two_one_ray_mod_64090_divisor`
- `two_one_ray_mod_2371330_divisor_residues`
- `has_two_one_ray_mod_2371330_divisor`
- `two_one_ray_mod_thirty_four_divisor_certificate`
- `two_one_ray_mod_thirty_four_divisor_orbit_certificate`
- `two_one_ray_mod_fifty_eight_divisor_certificate`
- `two_one_ray_mod_fifty_eight_divisor_orbit_certificate`
- `two_one_ray_mod_seventy_four_divisor_certificate`
- `two_one_ray_mod_seventy_four_divisor_orbit_certificate`
- `two_one_ray_mod_eighty_two_divisor_certificate`
- `two_one_ray_mod_eighty_two_divisor_orbit_certificate`
- `test_two_one_ray_mod_thirty_four_divisor_family`
- `test_two_one_ray_mod_fifty_eight_divisor_family`
- `test_two_one_ray_mod_seventy_four_divisor_family`
- `test_two_one_ray_mod_eighty_two_divisor_family`
- `test_two_one_ray_complement_divisor_root_formula`
- `test_two_one_ray_hypotenuse_divisor_layer`
- `test_complement_divisor_sieve_residue_compression`

### Added: Divisor-Lift Reduction On The $(2,1)$ Ray

Any certified multiplier on the $(2,1)$ ray now acts as a certified divisor
seed. If $q\mid n$ and $(2q,q)$ has midpoint $P$, then scaling by $n/q$
certifies $(2n,n)$. The new divisor-lift constructor first tries the current
exact seed families, then recursively scales the first certified proper divisor.

This changes the residual target from all leftover multipliers to leftover
prime multipliers. At that stage, before the inverse-root seed promotion below,
the multipliers below $2000$ not covered by divisor-lift were exactly
$$
\begin{gathered}
269,281,389,509,941,1009,1049,1249,1289,1321,\\
1361,1409,1481,1549,1601,1861,1949,
\end{gathered}
$$
and all are prime. Composite examples such as $6241=79^2$ are certified by
scaling a smaller seed certificate rather than by adding midpoint rows.

Executable guardrail:

- `two_one_ray_seed_certificate`
- `two_one_ray_divisor_lift_certificate`
- `two_one_ray_divisor_lift_orbit_certificate`
- `test_two_one_ray_divisor_lift_reduces_remaining_ray_to_primes`

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

### Added: Target-Facing Affine Consecutive-Hypotenuse Solver

The affine consecutive-hypotenuse strip now has a direct recognizer for a
requested target $(g,q)$. For fixed $m\ge2$, with
$u=2m-1$, $v=2m(m-1)$, and $c=m^2+(m-1)^2$, it checks exactly
$$
v\mid q(1-q),\qquad cq\mid g-uq(1-q)/v,
$$
then recovers $t$ and delegates to the explicit affine certificate. A symmetric
wrapper also applies coordinate swap.

Executable guardrail:

- `affine_consecutive_hypotenuse_target_certificate`
- `affine_consecutive_hypotenuse_orbit_certificate`
- `test_affine_consecutive_hypotenuse_target_solver`

### Added: Target-Facing Half-Leg Strip Solver

The half-leg strip now has an exact recognizer for arbitrary nonzero strip
coordinate $q$, not just the unit-coordinate specialization. For fixed
odd-even legal direction $U=(u,v)$ and target $(g,q)$, it first checks
$v\mid q(1-q)$, then solves the resulting quadratic in $t$:
$$
\frac{uv(1+2v-u^2)}4t^2+q(u^2-v)t+u\frac{q(1-q)}v=g.
$$
The solver delegates any integral root to the existing half-leg certificate,
so all standard nondegeneracy checks remain centralized.

Executable guardrail:

- `half_leg_strip_target_certificate`
- `half_leg_strip_orbit_certificate`
- `test_half_leg_strip_target_solver`

### Added: Target-Facing Half-Leg Unit-Coordinate Solver

The half-leg unit-coordinate family now has an exact recognizer. For a legal
odd-even direction $U=(u,v)$ and target $(g,1)$, it solves
$$
\frac{uv(1+2v-u^2)}4t^2+(u^2-v)t=g
$$
by the discriminant criterion, then delegates to the existing explicit
half-leg certificate. A sign/swap wrapper gives the corresponding symmetric
unit-coordinate targets.

Executable guardrail:

- `half_leg_unit_coordinate_target_certificate`
- `half_leg_unit_coordinate_orbit_certificate`
- `test_half_leg_unit_coordinate_target_solver`

### Added: Exact Unit-Coordinate Audit Through 500

The unit-coordinate slice now has a finite exact audit: every target in the
sign/swap orbit of $(n,1)$ with $|n|\le500$ is certified, except for the known
distance-three orbit. The audit uses existing exact families first and then
twenty-two explicit residual midpoint representatives.

This is a finite statement only. The residual rows are retained as directly
checked midpoint identities, not as a claim that the unit-coordinate line has
been classified.

Executable guardrail:

- `UNIT_COORDINATE_500_RESIDUAL_CERTIFICATES`
- `unit_coordinate_500_residual_certificate`
- `unit_coordinate_500_audit_certificate`
- `test_unit_coordinate_finite_audit_to_500`

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

The same theorem is also exposed as a line constructor using $h$ as the free
parameter, with the exact divisibility condition
$$
c-s_xa \mid (c+s_yb)h-1.
$$

Executable guardrail:

- `theorem3_certificate`
- `theorem3_certificates`
- `theorem3_line_certificate`
- `test_paper_theorem3_signed_certificate_examples`
- `test_paper_theorem3_line_constructor`
- `test_paper_theorem3_rejects_non_matching_relations`

### Added: Theorem 3 Quadratic-Strip Corollary

The consecutive Euclid triples from parameters $(n+1,n)$ promote two explicit
quadratic strip families from Theorem 3:
$$
(2hn^2-1,h)
\qquad\text{and}\qquad
(g,2gn^2+1),
$$
with $n\ge1$ and the fixed coordinate nonzero. The reusable sign/swap transport
then covers their full symmetry orbits.

Executable guardrail:

- `theorem3_quadratic_strip_certificate`
- `theorem3_quadratic_strip_orbit_certificate`
- `test_theorem3_quadratic_strip_family`

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

### Added: Inverse-Root Probe For Exceptional-Ray Primes

The complement-divisor root formula is now executable in the inverse direction.
For Euclid parameters $(m,k)$ and an odd-first-coordinate signed direction
$U=(u,v)$, the probe computes the root class
$$
R\equiv -(2u+v)(u-2v)^{-2}\pmod {m^2+k^2},
\qquad R\equiv1\pmod2.
$$
If a multiplier $p$ satisfies $p\equiv R\pmod {2(m^2+k^2)}$, the factor-one
parallel certificate is validated directly. This reframes the remaining
exceptional-ray prime problem as an inverse congruence problem over Euclid
parameters rather than a larger midpoint-box search.

The guardrail records witnesses for every pre-promotion divisor-lift residual
prime below $2000$ using Euclid parameter at most $300$.

The same root condition is also recorded in ray-adapted determinant
coordinates
$$
A=2u+v,\qquad B=u-2v,\qquad A^2+B^2=5c^2.
$$
Equivalently, these are Gaussian coordinates
$$
A+iB=(2+i)(u-iv),
$$
so the determinant-slice norm identity is a Gaussian norm identity, not an
independent coincidence.
For fixed $B$, this is the negative-Pell slice
$$
A^2-5c^2=-B^2.
$$
The root congruence becomes $pB^2+A\equiv0\pmod c$, and the factor-one
midpoint is
$$
\frac{p^2B^2+2pA-1}{2c^2}(u,v).
$$
Reducing the slice identity modulo $c$ gives the sharper divisor condition
$$
c\mid p^2B^2+1.
$$
Equivalently, for Euclid parameters $(m,k)$, the inverse-root witness satisfies
$$
pB\equiv \pm m k^{-1}\pmod c.
$$
For signed odd-leg-first directions
$$
u=s_o(m^2-k^2),\qquad v=s_e(2mk),
$$
the sign is $s_os_e$, so the root is the odd lift of
$$
p\equiv s_os_e\,m\,k^{-1}B^{-1}\pmod c.
$$
This has been promoted to a Euclid-parameter quotient layer. The pair
$(7,2)$ produces classes $31,47,59,75\pmod {106}$ and certifies examples
$1409$ and $1861$; the pair $(6,5)$ produces
$29,53,69,93\pmod {122}$ and certifies examples $1249$ and $1289$.
The test suite now checks this square-root-of-minus-one form for the current
residual-prime witnesses.
The distinct inverse-root witness parameters are now promoted into exact seed
layers:
$$
\begin{gathered}
(7,2),(6,5),(13,8),(15,4),(15,8),(19,4),(17,12),\\
(24,19),(37,2),(34,19),(41,20),(73,62),(116,35),(289,266),\\
(8,3),(8,5),(20,1).
\end{gathered}
$$
Each promoted pair is an infinite four-class quotient-divisor family modulo
$2(m^2+k^2)$. Together with the promoted square-factor hypotenuse layers below,
these additions leave no divisor-lift failures for $2\le n<3000$ on the
exceptional ray.
The new p-facing helper reconstructs the possible lifts of
$A\equiv -pB^2\pmod c$ and validates the determinant slice directly.
The successor
$$
A' = 161A+360c,\qquad c'=72A+161c,\qquad B'=B
$$
uses the square Pell unit and preserves the integral direction conditions. Some
intermediate rows can be degenerate or non-coprime, so the executable successor
skips to the next valid root. This lets a determinant-slice seed generate a
Pell orbit of exact quotient classes.
The guardrail now records this as an orbit certificate. In particular, the
$B=-11$ mod-$74$ seed $(-82,-11,37)$ has successor $(118,-11,53)$, whose root
class catches the former residual prime $1409$.
The inverse direction is executable too: the predecessor/reduced-root helpers
show that, among the pre-promotion divisor-lift residual primes below $2000$, only
$1409$ reduces to an already promoted small-layer seed under this square-unit
orbit; the other recorded inverse-root witnesses are reduced roots for their
own determinant-slice orbits.
This gives a one-dimensional determinant-factor route to search and prove the
exceptional-ray prime cases.

Executable guardrail:

- `TwoOneRayDeterminantSliceRoot`
- `two_one_ray_determinant_coordinates`
- `euclid_sqrt_minus_one_residues`
- `two_one_ray_signed_euclid_root`
- `two_one_ray_euclid_parameter_roots`
- `two_one_ray_euclid_parameter_residue_classes`
- `two_one_ray_euclid_parameter_certificate`
- `TWO_ONE_RAY_PROMOTED_INVERSE_ROOT_PARAMETERS`
- `two_one_ray_promoted_inverse_root_certificate`
- `two_one_ray_determinant_slice_root`
- `two_one_ray_determinant_factor_roots`
- `two_one_ray_determinant_slice_successor`
- `two_one_ray_determinant_slice_predecessor`
- `two_one_ray_determinant_slice_reduced_root`
- `two_one_ray_determinant_slice_orbit`
- `two_one_ray_determinant_slice_orbit_certificate`
- `two_one_ray_determinant_divisor_root`
- `two_one_ray_determinant_divisor_certificate`
- `two_one_ray_determinant_factor_certificate`
- `TwoOneRayInverseRootWitness`
- `two_one_ray_inverse_root_witness`
- `test_two_one_ray_determinant_slice_root_formula`
- `test_two_one_ray_inverse_root_witness_probe`

### Added: Square-Determinant Factor On The $(2,1)$ Ray

The exceptional-ray parallel-direction identity now has a second promoted factor
choice beyond the complement-divisor case. For $T=n(2,1)$ and
$U=(u,v)$, write
$$
A=2u+v,\qquad B=u-2v,\qquad c^2=u^2+v^2.
$$
Choosing factor $F=B^2$ leaves paired factor $n^2$ and gives
$$
r=\frac{n^2-B^2+2nA}{2c^2}.
$$
Since $A^2+B^2=5c^2$, this numerator is $(n+A)^2-5c^2$.
So the arithmetic root is the parity-compatible lift of
$$
n\equiv -A\pmod c
$$
modulo $2c$. The guardrail now checks this formula against direct
factor-witness enumeration for all primitive signed directions with Euclid
parameter at most $12$ and hypotenuse at most $250$.
The same construction is now a divisor sieve: if $n=dq$ and $q$ lies in the
square-factor class for $U$, choosing $F=dB^2$ scales the base $q$ certificate.
The first promoted hypotenuse layers are
$$
\begin{array}{c|c}
c & q\text{-classes}\\
\hline
13 & 6,9,10,11,15,16,17,20\pmod {26}\\
17 & 5,13,14,16,18,20,21,29\pmod {34}\\
37 & 21,22,26,29,45,48,52,53\pmod {74}\\
41 & 17,19,30,34,48,52,63,65\pmod {82}.
\end{array}
$$
For $U=(5,-12)$ this is
$$
r=\frac{n^2-4n-841}{338}.
$$
Thus $n=26t+15$ gives $r=2(t^2+t-1)$, so every positive
$n\equiv15\pmod {26}$ is certified except the degenerate case $n=145$.
This catches the next-frontier outlier $5449$ with midpoint
$(438890,-1053336)$ without adding a larger inverse-root parameter box.
With these promoted hypotenuse layers included in the seed constructor, the
only remaining failures in $2000\le n<3000$ were $2549,2621,2729$; the
inverse-root promotion above now catches those three as exact Euclid-parameter
layers.

Executable guardrail:

- `two_one_ray_square_determinant_factor_certificate`
- `two_one_ray_square_determinant_divisor_certificate`
- `two_one_ray_square_determinant_factor_sieve_certificate`
- `two_one_ray_square_determinant_factor_period`
- `two_one_ray_square_determinant_factor_residues`
- `two_one_ray_hypotenuse_square_factor_directions`
- `two_one_ray_hypotenuse_square_factor_residue_classes`
- `two_one_ray_hypotenuse_square_factor_certificate`
- `TWO_ONE_RAY_PROMOTED_SQUARE_FACTOR_HYPOTENUSES`
- `two_one_ray_promoted_square_factor_certificate`
- `two_one_ray_mod_twenty_six_square_factor_certificate`
- `test_two_one_ray_mod_twenty_six_square_factor_family`

### Added: Scaled Fixed-Factor Divisor Layers On The $(2,1)$ Ray

The fixed-factor parallel-direction residue classes now have a general divisor
promotion. If $q(2,1)$ is certified by a fixed direction $U$ with factor $F_0$,
then $n=dq$ is certified by the same direction using factor $dF_0$. The helper
uses `ray_parallel_factor_residues` for the exact arithmetic classes and checks
the scaled target directly to reject degeneracies.

The first promoted layers are:
$$
\begin{array}{c|c|c}
U & F_0 & q\text{-class}\\
\hline
(-12,5) & 22 & q\equiv5\pmod {13}\\
(-12,-5) & 2 & q\equiv8\pmod {13}\\
(20,-21) & 2 & q\equiv23\pmod {29}.
\end{array}
$$
They catch the previous next-frontier primes $3229$, $4649$, and $3329$.
Together with the square-factor and inverse-root promotions, the divisor-lift
audit has no remaining failures for $2\le n<5000$ on the exceptional ray; a
diagnostic scan leaves only $5849,7669,9749$ below $10000$.

Executable guardrail:

- `two_one_ray_scaled_factor_divisor_certificate`
- `TWO_ONE_RAY_PROMOTED_SCALED_FACTOR_LAYERS`
- `two_one_ray_promoted_scaled_factor_certificate`
- `test_two_one_ray_promoted_scaled_factor_layers`

### Added: Determinant Split-Factor Layers On The $(2,1)$ Ray

The fixed-factor layers have been folded into a closed determinant-square
split. For a direction $U=(u,v)$, write
$$
A=2u+v,\qquad B=u-2v,\qquad |U|=c.
$$
If $F_0H=B^2$ and $\gcd(H,c)=1$, then the fixed-factor coefficient condition
for the quotient $q(2,1)$ has discriminant
$$
4(A^2+HF_0)=20c^2,
$$
so the quotient class is the double root
$$
qH+A\equiv0\pmod c,
$$
with the two parity lifts modulo $2c$ checked against the exact factor and
coefficient congruences. This unifies the complement factor $F_0=1$, the
square factor $F_0=B^2$, and the interior factors promoted earlier.

The promoted split hypotenuses are now
$$
17,29,37,41,53,61,73,89,97,197,401.
$$
The low hypotenuses $17,29,41$ cover the previous diagnostic frontier below
$10000$:
$$
\begin{array}{c|c|c|c}
q & U & F_0 & q\text{-class}\\
\hline
7669 & (8,-15) & 2 & q\equiv2\pmod {17}\\
5849 & (20,21) & 2 & q\equiv20\pmod {29}\\
9749 & (-40,-9) & 22 & q\equiv32\pmod {41}.
\end{array}
$$
The enlarged split closure also catches the next seed frontier, for example:
$$
\begin{array}{c|c|c|c}
q & U & F_0 & q\text{-class}\\
\hline
10061 & (45,-28) & 10201 & q\equiv97\pmod {106}\\
23869 & (195,-28) & 63001 & q\equiv229\pmod {394}\\
40429 & (-40,-399) & 2 & q\equiv329\pmod {401}.
\end{array}
$$
With these layers included, the divisor-lift audit has no remaining failures
for $2\le n<10000$ on the exceptional ray, and the prime-seed audit has no
remaining failures for $10000\le p<1000000$ after the lift-three family below.
The target-facing helper `two_one_ray_determinant_split_factor_witness` now
turns the next frontier into exact determinant-coordinate rows rather than
manual midpoint searches. For instance, it extracts
$$
\begin{array}{c|c|c|c|c}
q & c & U & F_0 & q\text{-class}\\
\hline
110161 & 233 & (-105,-208) & 96721 & q\equiv185\pmod {466}\\
110501 & 277 & (-115,252) & 383161 & q\equiv255\pmod {554}\\
133121 & 169 & (-119,120) & 128881 & q\equiv287\pmod {338}.
\end{array}
$$
The paired-factor inverse records the sharper calculation. Fix
$H=B^2/F_0$. Then a quotient $q$ and hypotenuse $c$ force
$$
A\equiv -qH\pmod c,
$$
and the determinant norm gives $B^2=5c^2-A^2$. The helper
`two_one_ray_determinant_paired_factor_root` checks the finitely many lifts of
$A$, square-ness of $B^2$, divisibility by $H$, and the modulo-$5$
reconstruction of $(u,v)$. The wrapper
`two_one_ray_paired_factor_split_factor_witness` turns this into a certificate
search over quotient divisors and hypotenuses, and the test verifies that it
recovers the same determinant split witnesses for the recorded frontier rows.
Fixing the lift $k=(A+qH)/c$ gives the still smaller conic
$$
X^2+(k^2-5)B^2=5q^2H^2,\qquad X=(k^2-5)c-kqH.
$$
The helper `two_one_ray_determinant_paired_factor_lift_root` solves this
finite equation for $k^2>5$ and reconstructs $(U,F_0,c)$ from $(q,H,k)$. The
test now checks this norm identity for each recorded frontier witness.
For $H=1$ and $k=3$, the construction becomes the explicit double-direction
family. If $U=(u,v)$ has hypotenuse $c$ and $A=2u+v$, then
$$
q=3c-A
$$
is certified by midpoint $P=2U$, because
$$
|2U|=2c,\qquad |q(2,1)-2U|=|3q-2c|.
$$
The helper `two_one_ray_double_direction_certificate` builds this row from
$U$, while `two_one_ray_lift_three_square_endpoint_certificate` recognizes the
prime-seed case through the lift conic. With this constructor in the seed
path, the test verifies that no prime seed gaps remain for
$10000\le p<1000000$.
The promoted theorem-level form uses Fermat's two-square theorem. For every
prime $p\equiv1\pmod4$, write $p=x^2+4y^2$ and set $m=x+y$, $n=y$. The
direction
$$
U=(m^2-n^2,2mn)
$$
satisfies $p=3|U|-(2u+v)$, so $P=2U$ certifies $(2p,p)$. Together with the
existing even and $3\pmod4$ prime seed families, this supplies a seed
certificate for every prime multiplier $p>1$ on the exceptional ray; divisor
lift then covers every composite multiplier $n>1$ on the ray.
The direct helper `two_one_ray_prime_divisor_lift_certificate` now records this
as executable structure: factor $n$, certify one prime divisor, and scale by the
quotient. Its orbit helper applies the same certificate across sign and swap
images, so bounded boxes are retained only as implementation guardrails.

The $H=1$ square endpoint is now linked directly to determinant-slice Pell
orbits. A slice root $(A,B,c)$ has the square endpoint class
$$
q+A\equiv0\pmod c
$$
using factor $B^2$, while the existing square-unit successor preserves
$A^2-5c^2=-B^2$. The test records the reduced slice
$(A,B,c)=(-118,-359,169)$, whose square endpoint class
$q\equiv287\pmod {338}$ certifies $133121$ with midpoint
$(-36852158,37161840)$; its conjugate class
$q\equiv51\pmod {338}$ certifies the later diagnostic prime $307969$.

Executable guardrail:

- `TwoOneRayDeterminantSplitFactorWitness`
- `TwoOneRayDeterminantSliceRoot.square_endpoint_certificate`
- `two_one_ray_determinant_square_endpoint_orbit_certificate`
- `two_one_ray_double_direction_certificate`
- `two_one_ray_lift_three_square_endpoint_certificate`
- `two_one_ray_prime_one_mod_four_double_direction_certificate`
- `two_one_ray_prime_divisor_lift_certificate`
- `two_one_ray_prime_divisor_lift_orbit_certificate`
- `two_one_ray_paired_factor_lift_witness`
- `two_one_ray_determinant_paired_factor_lift_root`
- `two_one_ray_determinant_paired_factor_root`
- `two_one_ray_determinant_split_factor_period`
- `two_one_ray_determinant_split_factor_certificate`
- `two_one_ray_hypotenuse_determinant_split_factor_layers`
- `two_one_ray_hypotenuse_determinant_split_factor_certificate`
- `two_one_ray_determinant_split_factor_witness`
- `two_one_ray_paired_factor_split_factor_witness`
- `TWO_ONE_RAY_PROMOTED_DETERMINANT_SPLIT_FACTOR_HYPOTENUSES`
- `two_one_ray_promoted_determinant_split_factor_certificate`
- `test_two_one_ray_determinant_split_factor_layers`

## Determinant-Squareclass Line Families

The bounded squareclass split layer has been promoted to an explicit
line-family normal form. For a legal direction $U$, squarefree $q$, positive
split factor $a$, signed paired factor $b$, and first coefficient $r$, the new
helper `parallel_direction_squareclass_line_certificate` constructs the target
$$
T_r=rU+\frac{-LU+qab\,U^\perp}{|U|^2},
\qquad L=\frac{q(b^2-a^2)}2,
$$
whenever the divisibility conditions make the second edge integral and
Pythagorean. This records the intended generalization: split rows are infinite
parallel line families, not just bounded target-facing factor searches.

`ParallelDirectionSquareclassSplitWitness.signed_paired_split_factor` now
recovers the signed $b$ from a target-facing witness, and the squareclass cover
skips impossible rows unless `q*a` divides the determinant leg. The focused
guardrail `test_squareclass_split_extended_frontier_examples` records the six
first current split misses beyond the default `q <= 23`, `a <= 179` layer and
verifies their exact line-family certificates with parameters up to
`q <= 149`, `a <= 401`.

The split-line normal form has also been inverted into determinant-residue
strips. For fixed `U,q,a`, the accepted signed paired factors are periodic
modulo `2|U|^2`; `parallel_direction_squareclass_line_residue_classes`
compresses those classes to their minimal period, and
`parallel_direction_squareclass_line_residue_certificate` tests a target by
reducing `det(U,T)/(q*a)` modulo that period. The first useful frontier
examples include the single-class strips `b == 81 mod 82` for
`((-40, 9), 149, 401)` and `b == 13 mod 25` for `((-24, 7), 34, 41)`.

The residue computation now uses `parallel_direction_squareclass_line_second_step`,
which exposes the congruence-defined second edge $W$ directly. This separates
the algebraic line-family predicate from the later target-facing certificate
construction and gives the next proof search an explicit congruence system to
classify.

The congruence predicate itself is now exposed as
`parallel_direction_squareclass_line_congruence_holds`. Tests distinguish a
true residue failure from a finite graph-edge degeneracy: for
`((-9, 40), 2, 19)`, `b = -238` fails the congruences, while `b = 171`
satisfies them but produces the vertical vector `(0, -722)`.

The same split-line system is now recorded in Gaussian normal form. The helper
`parallel_direction_squareclass_line_gaussian_numerator` returns
`q*U*(a+i*b)^2`, so the second edge is this numerator divided by `2|U|^2`.
This turns the two coordinate congruences into one Gaussian divisibility test,
leaving only the length divisibility and graph-edge nondegeneracy as separate
checks.

Primitive Pythagorean directions are now factored as Gaussian squares. The
helper `primitive_pythagorean_direction_gaussian_root` returns
`(alpha, unit)` with `U = unit*alpha^2`, and
`parallel_direction_squareclass_line_root_quotient` computes the equivalent
quotient `unit*q*(a+i*b)^2/(2*conj(alpha)^2)`. This makes the remaining split
classification a Gaussian prime-factor divisibility problem.

The quotient has now been split once more. The helper
`parallel_direction_squareclass_line_split_quotient` computes
`beta = (a+i*b)/conj(alpha)`. The congruence predicate is tested against the
criterion that this quotient exists and `q*beta^2` has even Gaussian
coordinates. This turns the fixed-direction split rows into an ideal-membership
condition plus parity and finite graph-edge nondegeneracy.

The beta form is also executable in the forward direction. The helpers
`parallel_direction_squareclass_beta_split_root`,
`parallel_direction_squareclass_beta_quotient`,
`parallel_direction_squareclass_beta_second_step`, and
`parallel_direction_squareclass_beta_line_certificate` construct the split root
and line certificate from a chosen `beta`. Existing frontier rows are now tested
both from their old `(a,b)` split data and from the beta parametrization.

The inverse target-facing beta test is also executable. The helpers
`parallel_direction_squareclass_beta_target_coefficient` and
`parallel_direction_squareclass_beta_target_certificate` compute
`W = unit*q*beta^2/2` and then test whether `T-W` is an integer multiple of the
direction `U`. This records the split layer as a direct line-membership problem
over `(U,q,beta)`.

That line-membership problem is now recorded in determinant-level form as well.
For primitive `U`, the equality `T-W = rU` is equivalent to
`det(U,T) == det(U,W)`. The helper
`parallel_direction_squareclass_beta_determinant_residue` returns the level
`det(U,W)`, while
`parallel_direction_squareclass_beta_determinant_target_coefficient` and
`parallel_direction_squareclass_beta_determinant_target_certificate` use that
level to recover the first-step scalar and certificate. The tests check that
this level agrees with the old split determinant leg `q*a*b`.

The determinant-level inverse has also been reduced to a square-root
congruence in the conjugate-root ideal. The helper
`primitive_pythagorean_direction_conjugate_root_residue` returns `(c,rho)` such
that `a+i*b` is divisible by `conj(alpha)` exactly when
`b == rho*a mod c`. For a fixed determinant leg `D` and squareclass `q`, this
means `D/q == rho*a^2 mod c` with `a | D/q`. The helper
`parallel_direction_squareclass_conjugate_ideal_split_roots` enumerates these
legal divisor roots directly, and
`parallel_direction_squareclass_conjugate_ideal_certificate` turns them into a
target-facing certificate.

The fixed-squareclass inverse has been wrapped over the only possible
squareclasses for a target: squarefree divisors of the determinant leg. The
helper `squarefree_divisors` supplies those values, and
`parallel_direction_conjugate_ideal_split_roots` lists all legal
`(q,a,b,beta)` rows for one fixed target and direction. The certificate wrapper
`parallel_direction_conjugate_ideal_certificate` is consequently an exact
fixed-direction split recognizer, not a bounded `q,a` search.

The exact recognizer has been promoted to the finite-direction layer.
`parallel_direction_conjugate_ideal_cover_certificate` scans the same bounded
primitive direction table, but no longer accepts squareclass or split-factor
bounds. `pythagorean_layered_conjugate_ideal_certificate` places this after the
structural stack, and `pythagorean_layered_parallel_certificate` now tries it
before the older all-factor fixed-direction fallback. The sample-to-1000
guardrail still passes, and the six extended split frontier examples are
covered without enlarging any `q,a` box.

The beta integrality and nondegeneracy filters are now standalone helpers.
`squareclass_beta_integral` records that even `q` accepts every nonzero beta,
while odd `q` requires same-parity beta coordinates. `beta_square_is_axis_degenerate`
records the only beta shapes whose square has a zero coordinate: horizontal,
vertical, or diagonal beta.

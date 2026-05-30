import json
from math import gcd, isqrt, lcm
from pathlib import Path
import unittest

import pytest

from experiments.pythagorean_walks import (
    Certificate,
    BOX_EIGHTY_RESIDUAL_CERTIFICATES,
    BOX_FIFTY_RESIDUAL_CERTIFICATES,
    BOX_FIVE_HUNDRED_RESIDUAL_CERTIFICATES,
    BOX_FORTY_RESIDUAL_CERTIFICATES,
    BOX_NINETY_RESIDUAL_CERTIFICATES,
    BOX_ONE_EIGHTY_RESIDUAL_CERTIFICATES,
    BOX_ONE_FIFTY_RESIDUAL_CERTIFICATES,
    BOX_ONE_FORTY_RESIDUAL_CERTIFICATES,
    BOX_ONE_HUNDRED_RESIDUAL_CERTIFICATES,
    BOX_ONE_NINETY_RESIDUAL_CERTIFICATES,
    BOX_ONE_SEVENTY_RESIDUAL_CERTIFICATES,
    BOX_ONE_SIXTY_RESIDUAL_CERTIFICATES,
    BOX_ONE_TEN_RESIDUAL_CERTIFICATES,
    BOX_ONE_THIRTY_RESIDUAL_CERTIFICATES,
    BOX_ONE_TWENTY_RESIDUAL_CERTIFICATES,
    BOX_SEVENTY_RESIDUAL_CERTIFICATES,
    BOX_SIXTY_RESIDUAL_CERTIFICATES,
    BOX_THREE_FIFTY_RESIDUAL_CERTIFICATES,
    BOX_THREE_HUNDRED_RESIDUAL_CERTIFICATES,
    BOX_THREE_SIXTY_RESIDUAL_CERTIFICATES,
    BOX_THREE_FORTY_RESIDUAL_CERTIFICATES,
    BOX_THREE_TEN_RESIDUAL_CERTIFICATES,
    BOX_THREE_THIRTY_RESIDUAL_CERTIFICATES,
    BOX_THREE_TWENTY_RESIDUAL_CERTIFICATES,
    BOX_THIRTY_RESIDUAL_CERTIFICATES,
    BOX_TWENTY_RESIDUAL_CERTIFICATES,
    BOX_TWO_EIGHTY_RESIDUAL_CERTIFICATES,
    BOX_TWO_FIFTY_RESIDUAL_CERTIFICATES,
    BOX_TWO_FORTY_RESIDUAL_CERTIFICATES,
    BOX_TWO_HUNDRED_RESIDUAL_CERTIFICATES,
    BOX_TWO_SEVENTY_RESIDUAL_CERTIFICATES,
    BOX_TWO_NINETY_RESIDUAL_CERTIFICATES,
    BOX_TWO_SIXTY_RESIDUAL_CERTIFICATES,
    BOX_TWO_TEN_RESIDUAL_CERTIFICATES,
    BOX_TWO_THIRTY_RESIDUAL_CERTIFICATES,
    BOX_TWO_TWENTY_RESIDUAL_CERTIFICATES,
    EXPLICIT_TWO_ONE_RAY_BASE_CERTIFICATES,
    EXPLICIT_TWO_ONE_RAY_FINITE_AUDIT_CERTIFICATES,
    KNOWN_DISTANCE_THREE_ORBIT,
    KNOWN_DISTANCE_THREE_REPRESENTATIVES,
    PythagoreanTriple,
    PythagoreanLatticePairWitness,
    ParallelDirectionFactorWitness,
    ParallelDirectionConjugateIdealDivisorObligationCensus,
    ParallelDirectionConjugateIdealDivisorObligationStripCensus,
    ParallelDirectionConjugateIdealWitness,
    ParallelDirectionConjugateIdealRootCoverCensus,
    ParallelDirectionConjugateIdealRootShapeCoverCensus,
    ParallelDirectionSquareclassSplitWitness,
    ParallelDirectionCoverWitnessCensus,
    PrimitiveRayParallelDirectionWitness,
    PARALLEL_DIRECTION_PROMOTED_345_DIRECTIONS,
    PARALLEL_DIRECTION_PROMOTED_345_FACTORS,
    PARALLEL_DIRECTION_PROMOTED_345_FACTOR_ROWS,
    PYTHAGOREAN_LAYERED_LATTICE_PAIR_MAX_DETERMINANT,
    PYTHAGOREAN_LAYERED_LATTICE_PAIR_MAX_PARAMETER,
    PYTHAGOREAN_LAYERED_CONJUGATE_ROOT_MAX_COORDINATE,
    PYTHAGOREAN_LAYERED_ORTHOGONAL_MAX_PARAMETER,
    PYTHAGOREAN_LAYERED_PARALLEL_MAX_PARAMETER,
    PYTHAGOREAN_LAYERED_SPLIT_MAX_FACTOR,
    PYTHAGOREAN_LAYERED_SPLIT_MAX_SQUARECLASS,
    PYTHAGOREAN_LAYERED_STANDARD_COMPLETION_MAX_PARAMETER,
    SMALL_PRIME_DETERMINANT_DIRECTION_PAIRS,
    TwoOneRayDeterminantSliceRoot,
    TwoOneRayInverseRootWitness,
    UNIT_COORDINATE_500_RESIDUAL_CERTIFICATES,
    affine_consecutive_hypotenuse_certificate,
    affine_consecutive_hypotenuse_orbit_certificate,
    affine_consecutive_hypotenuse_target_certificate,
    axis_orbit_proof_certificate,
    box_eighty_audit_certificate,
    box_eighty_residual_certificate,
    box_fifty_audit_certificate,
    box_fifty_residual_certificate,
    box_five_hundred_audit_certificate,
    box_five_hundred_ray_lift_certificate,
    box_five_hundred_residual_certificate,
    box_forty_audit_certificate,
    box_forty_residual_certificate,
    box_ninety_audit_certificate,
    box_ninety_residual_certificate,
    box_one_eighty_audit_certificate,
    box_one_eighty_residual_certificate,
    box_one_fifty_audit_certificate,
    box_one_fifty_residual_certificate,
    box_one_forty_audit_certificate,
    box_one_forty_residual_certificate,
    box_one_hundred_audit_certificate,
    box_one_hundred_residual_certificate,
    box_one_ninety_audit_certificate,
    box_one_ninety_residual_certificate,
    box_one_seventy_audit_certificate,
    box_one_seventy_residual_certificate,
    box_one_sixty_audit_certificate,
    box_one_sixty_residual_certificate,
    box_one_ten_audit_certificate,
    box_one_ten_residual_certificate,
    box_one_thirty_audit_certificate,
    box_one_thirty_residual_certificate,
    box_one_twenty_audit_certificate,
    box_one_twenty_residual_certificate,
    box_seventy_audit_certificate,
    box_seventy_residual_certificate,
    box_sixty_audit_certificate,
    box_sixty_residual_certificate,
    box_three_fifty_audit_certificate,
    box_three_fifty_residual_certificate,
    box_three_hundred_audit_certificate,
    box_three_hundred_residual_certificate,
    box_three_sixty_audit_certificate,
    box_three_sixty_residual_certificate,
    box_three_forty_audit_certificate,
    box_three_forty_residual_certificate,
    box_three_ten_audit_certificate,
    box_three_ten_residual_certificate,
    box_three_thirty_audit_certificate,
    box_three_thirty_residual_certificate,
    box_three_twenty_audit_certificate,
    box_three_twenty_residual_certificate,
    box_thirty_audit_certificate,
    box_thirty_residual_certificate,
    box_twenty_audit_certificate,
    box_twenty_residual_certificate,
    box_two_eighty_audit_certificate,
    box_two_eighty_residual_certificate,
    box_two_fifty_audit_certificate,
    box_two_fifty_residual_certificate,
    box_two_forty_audit_certificate,
    box_two_forty_residual_certificate,
    box_two_hundred_audit_certificate,
    box_two_hundred_residual_certificate,
    box_two_seventy_audit_certificate,
    box_two_seventy_residual_certificate,
    box_two_ninety_audit_certificate,
    box_two_ninety_residual_certificate,
    box_two_sixty_audit_certificate,
    box_two_sixty_residual_certificate,
    box_two_ten_audit_certificate,
    box_two_ten_residual_certificate,
    box_two_thirty_audit_certificate,
    box_two_thirty_residual_certificate,
    box_two_twenty_audit_certificate,
    box_two_twenty_residual_certificate,
    bounded_two_step_search,
    canonical_known_distance_three_representative,
    consecutive_direction_strip_certificate,
    consecutive_euclid_affine_strip_certificate,
    consecutive_euclid_affine_strip_orbit_certificate,
    consecutive_euclid_unit_divisor_ray_certificate,
    consecutive_euclid_unit_divisor_ray_orbit_certificate,
    consecutive_leg_pythagorean_triple,
    consecutive_leg_swap_lattice_certificate,
    consecutive_parameter_odd_axis_certificate,
    consecutive_hypotenuse_unit_coordinate_certificate,
    diagonal_pythagorean_multiplier_certificate,
    determinant,
    divisor_residue_classes,
    DivisorObligationGlobalRootChoiceBranchAuditRow,
    discrete_log_table_mod_prime,
    determinant_seven_lattice_certificate,
    determinant_seventeen_lattice_certificate,
    determinant_thirteen_lattice_certificate,
    delta_slice_certificate,
    edge,
    eight_fifteen_seventeen_unit_divisor_ray_certificate,
    eight_fifteen_seventeen_unit_divisor_ray_data,
    eight_fifteen_seventeen_unit_divisor_ray_orbit_certificate,
    euclid_sqrt_minus_one_residues,
    euclid_strip_certificate,
    euclid_parameter_difference_certificate,
    explicit_axis_certificate,
    first_gaussian_divisor_certificate,
    find_two_step_certificate,
    five_twelve_thirteen_unit_divisor_ray_certificate,
    five_twelve_thirteen_unit_divisor_ray_data,
    five_twelve_thirteen_unit_divisor_ray_orbit_certificate,
    four_three_factor_five_parallel_certificate,
    four_five_root_spine_line_certificate,
    gaussian_root_conjugate_divisibility_residue,
    gaussian_divisor_certificate,
    gaussian_multiply,
    gaussian_quotient_if_integer,
    gaussian_root_shape,
    gaussian_transform_certificate,
    half_leg_strip_orbit_certificate,
    half_leg_strip_certificate,
    half_leg_strip_target_certificate,
    half_leg_unit_coordinate_certificate,
    half_leg_unit_coordinate_orbit_certificate,
    half_leg_unit_coordinate_target_certificate,
    all_prime_factors_one_or_nine_mod_ten,
    cyclic_subset_stabilizer_step,
    cyclic_sumset,
    cyclic_sumset_effective_length,
    cyclic_sumset_kneser_data,
    cyclic_sumset_saturation_gap,
    has_divisor_in_residue_classes,
    has_divisor_three_or_seven_mod_ten,
    has_two_one_ray_mod_130_divisor,
    has_two_one_ray_mod_2210_divisor,
    has_two_one_ray_mod_2371330_divisor,
    has_two_one_ray_mod_64090_divisor,
    horizontal_axis_certificate_table,
    horizontal_axis_proof_certificate,
    is_prime,
    is_square,
    is_two_step_certificate,
    integer_slope_consecutive_ray_certificate,
    lattice_coefficient_cramer_data,
    lattice_coefficients,
    lattice_two_step_certificate,
    linear_delta_direction_certificate,
    missing_residues,
    minimal_periodic_residue_classes,
    prime_modulus_divisor_exponent_classes,
    prime_modulus_divisor_exponent_summands,
    primitive_root_mod_prime,
    midpoint_axis_certificate,
    odd_residues,
    one_three_ray_theorem3_certificate,
    one_three_ray_theorem3_orbit_certificate,
    one_four_even_root_spine_line_certificate,
    one_four_root_spine_line_certificate,
    one_even_root_spine_line_certificate,
    one_even_root_spine_line_orbit_certificate,
    one_two_root_spine_line_certificate,
    two_five_root_spine_line_certificate,
    two_odd_root_spine_line_orbit_certificate,
    two_three_odd_general_root_spine_line_certificate,
    three_four_odd_root_spine_line_certificate,
    three_four_root_spine_line_certificate,
    three_eight_odd_root_spine_line_certificate,
    path_is_valid,
    PINNED_GLOBAL_ROOT_CHOICE_ALTERNATE_LINE_STRIP_ROWS,
    PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_GENERIC_LINE_STRIP_ROWS,
    PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_DOMINANT_LINE_TEMPLATES,
    PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_RESIDUAL_LINE_TEMPLATES,
    PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_RESIDUAL_LINE_TEMPLATES,
    PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1500_RESIDUAL_LINE_TEMPLATES,
    PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1750_RESIDUAL_LINE_TEMPLATES,
    PINNED_GLOBAL_ROOT_CHOICE_RADIUS_500_SIGNATURE_TEMPLATE_ROWS,
    PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_SIGNATURE_TEMPLATE_ROWS,
    PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_SIGNATURE_TEMPLATE_ROWS,
    PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_SIGNATURE_TEMPLATE_ROWS,
    PINNED_ROOT_SPINE_DIVISOR_OBLIGATIONS,
    PINNED_STRIP_LOCAL_DISCHARGE_COUNTEREXAMPLE,
    GLOBAL_ROOT_CHOICE_PROVED_SIGNATURE_TEMPLATE_ROWS,
    GLOBAL_ROOT_CHOICE_PROVED_NORMALIZED_LINE_FAMILIES,
    GLOBAL_ROOT_CHOICE_PROVED_NORMALIZED_LINE_TEMPLATES,
    global_root_choice_branch_row_signature_template,
    global_root_choice_branch_row_alternate_line_strip_row,
    global_root_choice_line_template_table_rows,
    global_root_choice_line_template_strip_rows,
    global_root_choice_normalized_line_template,
    global_root_choice_proved_normalized_line_family_theorem,
    global_root_choice_proved_signature_template_witness,
    global_root_choice_short_exponent_signature,
    global_root_choice_signature_template_witness,
    global_root_choice_signature_template_shape_audit,
    pinned_global_root_choice_alternate_line_strip_row_valid,
    pinned_global_root_choice_alternate_line_strip_row_witness,
    pinned_global_root_choice_alternate_line_strip_rows_valid,
    pinned_global_root_choice_alternate_line_strip_summary,
    pinned_global_root_choice_table_certificate,
    pinned_global_root_choice_table_witness,
    parallel_direction_certificate,
    beta_square_is_axis_degenerate,
    parallel_direction_bounded_factor_cover_certificate,
    gaussian_root_shape,
    parallel_direction_conjugate_ideal_certificate,
    parallel_direction_conjugate_ideal_divisor_obligation_discharge_witness,
    parallel_direction_conjugate_ideal_divisor_obligation_global_discharge_witness,
    parallel_direction_conjugate_ideal_divisor_obligation_proved_signature_template_discharge_witness,
    parallel_direction_conjugate_ideal_divisor_obligation_signature_template_discharge_witness,
    parallel_direction_conjugate_ideal_divisor_obligation_divisor_holds,
    parallel_direction_conjugate_ideal_divisor_obligation_directions,
    parallel_direction_conjugate_ideal_divisor_obligation_exponent_profile,
    parallel_direction_conjugate_ideal_global_root_choice_branch_audit,
    parallel_direction_conjugate_ideal_global_root_choice_exponent_signature_audit,
    parallel_direction_conjugate_ideal_global_root_choice_signature_template_closure_chain_audit,
    parallel_direction_conjugate_ideal_global_root_choice_iterated_signature_template_closure_audit,
    parallel_direction_conjugate_ideal_global_root_choice_iterated_template_closure_audit,
    parallel_direction_conjugate_ideal_global_root_choice_portable_row_audit,
    parallel_direction_conjugate_ideal_global_root_choice_signature_template_coverage_audit,
    parallel_direction_conjugate_ideal_global_root_choice_signature_template_audit,
    parallel_direction_conjugate_ideal_global_root_choice_template_closure_audit,
    parallel_direction_conjugate_ideal_global_root_choice_audit,
    parallel_direction_conjugate_ideal_signature_template_branch_audit,
    parallel_direction_conjugate_ideal_divisor_obligation_key,
    parallel_direction_conjugate_ideal_divisor_obligation_strip_census,
    parallel_direction_conjugate_ideal_divisor_obligation_strip_holds,
    parallel_direction_conjugate_ideal_divisor_obligation_strip_modulus,
    parallel_direction_conjugate_ideal_divisor_obligation_strip_residue,
    parallel_direction_conjugate_ideal_cover_certificate,
    parallel_direction_conjugate_ideal_cover_witness,
    parallel_direction_conjugate_ideal_determinant_roots,
    parallel_direction_conjugate_ideal_root_cover_certificate,
    parallel_direction_conjugate_ideal_root_cover_census,
    parallel_direction_conjugate_ideal_root_shape_cover_witness,
    parallel_direction_conjugate_ideal_root_cover_witness,
    parallel_direction_conjugate_ideal_root_primary_spine_cover_certificate,
    parallel_direction_conjugate_ideal_root_primary_spine_cover_witness,
    parallel_direction_conjugate_ideal_root_secondary_spine_cover_certificate,
    parallel_direction_conjugate_ideal_root_secondary_spine_cover_witness,
    parallel_direction_conjugate_ideal_root_shape_divisor_obligation_census,
    parallel_direction_conjugate_ideal_root_spine_cover_certificate,
    parallel_direction_conjugate_ideal_root_spine_cover_census,
    parallel_direction_conjugate_ideal_root_spine_divisor_obligation_census,
    parallel_direction_conjugate_ideal_root_spine_cover_witness,
    parallel_direction_conjugate_ideal_promoted_345_integrality_strip_intersection_counts,
    parallel_direction_conjugate_ideal_split_roots,
    parallel_direction_conjugate_ideal_witness,
    parallel_direction_cover_certificate,
    parallel_direction_factor_coefficient,
    parallel_direction_factor_certificate,
    parallel_direction_factor_certificate_residue_classes,
    parallel_direction_factor_congruence_data,
    parallel_direction_factor_congruence_holds,
    parallel_direction_factor_modulus,
    parallel_direction_factor_pair_row_from_congruence_data,
    parallel_direction_primitive_factor_determinant_residue_holds,
    parallel_direction_primitive_factor_determinant_residue_rows,
    parallel_direction_factor_residue_certificate,
    parallel_direction_factor_residue_classes,
    parallel_direction_factor_integrality_strip_intersection_residue_count,
    parallel_direction_primitive_factor_integrality_strip_intersection_linear_rows,
    parallel_direction_primitive_factor_integrality_strip_intersection_linear_row_witness,
    parallel_direction_primitive_factor_integrality_strip_intersection_residue_count,
    parallel_direction_factor_witness,
    parallel_direction_squareclass_split_certificate,
    parallel_direction_squareclass_split_cover_certificate,
    parallel_direction_squareclass_split_cover_witness,
    parallel_direction_squareclass_conjugate_ideal_certificate,
    parallel_direction_squareclass_conjugate_ideal_split_roots,
    parallel_direction_squareclass_conjugate_ideal_witness,
    parallel_direction_squareclass_beta_determinant_residue,
    parallel_direction_squareclass_beta_determinant_target_certificate,
    parallel_direction_squareclass_beta_determinant_target_coefficient,
    parallel_direction_squareclass_beta_line_certificate,
    parallel_direction_squareclass_beta_quotient,
    parallel_direction_squareclass_beta_quadratic_certificate,
    parallel_direction_squareclass_beta_quadratic_coefficient,
    parallel_direction_squareclass_beta_second_step,
    parallel_direction_squareclass_beta_split_root,
    parallel_direction_squareclass_beta_target_certificate,
    parallel_direction_squareclass_beta_target_coefficient,
    parallel_direction_squareclass_line_gaussian_numerator,
    parallel_direction_squareclass_line_congruence_holds,
    parallel_direction_squareclass_line_certificate,
    parallel_direction_squareclass_line_residue_certificate,
    parallel_direction_squareclass_line_residue_classes,
    parallel_direction_squareclass_line_root_quotient,
    parallel_direction_squareclass_line_split_quotient,
    parallel_direction_squareclass_line_second_step,
    parallel_direction_squareclass_split_witness,
    primitive_pythagorean_direction_conjugate_root_residue,
    parallel_direction_cover_witness_census,
    parallel_direction_promoted_345_factor_certificate,
    parallel_direction_promoted_345_factor_witness,
    promoted_root_spine_line_certificate_from_witness,
    parallel_direction_primitive_ray_certificate,
    parallel_direction_primitive_ray_witness,
    parallel_direction_standard_completion_cover_certificate,
    parallel_direction_standard_completion_cover_witness,
    parallel_direction_standard_completion_branch,
    parallel_direction_standard_completion_determinant_rows,
    parallel_direction_standard_completion_certificate,
    parallel_direction_standard_completion_quadratic_row_witness,
    parallel_direction_standard_completion_quadratic_rows,
    parallel_direction_standard_completion_strip_intersection_linear_rows,
    parallel_direction_standard_completion_strip_intersection_linear_row_witness,
    parallel_direction_standard_completion_witness,
    parallel_direction_witness,
    parallel_direction_cover_witness,
    periodic_residue_union,
    positive_divisors,
    possible_integer_distance_differences,
    prime_factors,
    primitive_pythagorean_direction_gaussian_root,
    primitive_pythagorean_directions,
    primitive_pythagorean_root_directions,
    primitive_pythagorean_root_primary_spine_shapes,
    primitive_pythagorean_root_secondary_spine_shapes,
    primitive_pythagorean_root_spine_shapes,
    primitive_pythagorean_root_shape_directions,
    pythagorean_leg_completion,
    pythagorean_directions_for_hypotenuse,
    pythagorean_layered_parallel_certificate,
    pythagorean_layered_conjugate_ideal_certificate,
    pythagorean_layered_split_certificate,
    pythagorean_layered_structural_certificate,
    pythagorean_layered_structural_label,
    pythagorean_triple_orthogonal_lattice_certificate,
    pythagorean_orthogonal_lattice_cover_certificate,
    pythagorean_orthogonal_lattice_witness,
    pythagorean_lattice_direction_pairs,
    pythagorean_lattice_pair_cover_certificate,
    pythagorean_lattice_pair_strip_intersection_holds,
    pythagorean_lattice_pair_strip_intersection_residue_count,
    pythagorean_lattice_pair_strip_crt_data,
    pythagorean_lattice_pair_strip_linear_congruence,
    pythagorean_lattice_pair_same_strip_combined_linear_congruence,
    pythagorean_lattice_pair_same_strip_intersection_residue_count,
    pythagorean_lattice_pair_witness,
    two_variable_linear_congruence_gcd,
    two_variable_linear_congruence_pair_data,
    prime_determinant_lattice_certificate,
    rational_slope_consecutive_ray_certificate,
    ray_multiplier,
    ray_parallel_factor_certificate,
    ray_parallel_factor_residues,
    residue_witnesses,
    scale_certificate,
    scale_signed_swap_certificate,
    same_projective_class_mod,
    shared_leg_axis_certificate_records,
    shared_leg_axis_certificate_table,
    sign_swap_certificate,
    sign_swap_orbit,
    signed_delta_values,
    signed_swap_point,
    small_prime_lattice_certificate,
    squareclass_beta_integral,
    squareclass_decomposition,
    squarefree_divisors,
    squarefree_numbers,
    standard_pythagorean_completion_factors,
    theorem1_three_step_path,
    theorem3_certificate,
    theorem3_certificates,
    theorem3_divisor_certificate,
    theorem3_line_certificate,
    theorem3_ray_divisor,
    theorem3_quadratic_strip_certificate,
    theorem3_quadratic_strip_orbit_certificate,
    theorem3_ray_divisor_certificate,
    theorem3_ray_divisor_modulus,
    theorem3_ray_pell_divisor_certificate,
    theorem3_coprime_unit_divisor_progression_certificate,
    theorem3_coprime_unit_divisor_progression_orbit_certificate,
    theorem3_coprime_unit_divisor_progression_ray,
    theorem3_coprime_unit_divisor_seed,
    theorem3_unit_divisor_step_coefficients,
    theorem3_unit_divisor_progression_certificate,
    theorem3_unit_divisor_progression_orbit_certificate,
    theorem3_unit_divisor_progression_parameters_for_base,
    theorem3_unit_divisor_progression_ray,
    three_four_five_unit_divisor_ray_certificate,
    three_four_five_unit_divisor_ray_data,
    three_four_five_unit_divisor_ray_orbit_certificate,
    three_four_five_odd_slope_ray_certificate,
    three_four_five_odd_slope_ray_orbit_certificate,
    TwoOneRayDeterminantSplitFactorWitness,
    TWO_ONE_RAY_PROMOTED_DETERMINANT_SPLIT_FACTOR_HYPOTENUSES,
    TWO_ONE_RAY_PROMOTED_INVERSE_ROOT_PARAMETERS,
    TWO_ONE_RAY_PROMOTED_SCALED_FACTOR_LAYERS,
    TWO_ONE_RAY_PROMOTED_SQUARE_FACTOR_HYPOTENUSES,
    two_one_ray_consecutive_certificate,
    two_one_ray_consecutive_orbit_certificate,
    two_one_ray_divisor_lift_certificate,
    two_one_ray_divisor_lift_orbit_certificate,
    two_one_ray_even_certificate,
    two_one_ray_even_orbit_certificate,
    two_one_ray_explicit_base_certificate,
    two_one_ray_explicit_base_orbit_certificate,
    two_one_ray_five_or_seventeen_mod_twenty_certificate,
    two_one_ray_five_or_seventeen_mod_twenty_orbit_certificate,
    two_one_ray_finite_audit_certificate,
    two_one_ray_finite_audit_orbit_certificate,
    two_one_ray_hypotenuse_divisor_certificate,
    two_one_ray_hypotenuse_divisor_directions,
    two_one_ray_hypotenuse_divisor_residue_classes,
    two_one_ray_hypotenuse_determinant_split_factor_certificate,
    two_one_ray_hypotenuse_determinant_split_factor_layers,
    two_one_ray_hypotenuse_square_factor_certificate,
    two_one_ray_hypotenuse_square_factor_directions,
    two_one_ray_hypotenuse_square_factor_residue_classes,
    two_one_ray_inverse_root_witness,
    two_one_ray_lift_three_square_endpoint_certificate,
    two_one_ray_mod20_skeleton_certificate,
    two_one_ray_mod20_skeleton_orbit_certificate,
    two_one_ray_mod20_skeleton_residues,
    two_one_ray_mod60_theorem3_skeleton_certificate,
    two_one_ray_mod60_theorem3_skeleton_orbit_certificate,
    two_one_ray_mod60_theorem3_skeleton_residues,
    two_one_ray_mod260_skeleton_certificate,
    two_one_ray_mod260_skeleton_orbit_certificate,
    two_one_ray_mod260_skeleton_residues,
    two_one_ray_mod_2210_divisor_residues,
    two_one_ray_mod_2371330_divisor_residues,
    two_one_ray_mod_64090_divisor_residues,
    two_one_ray_complement_divisor_certificate,
    two_one_ray_complement_divisor_period,
    two_one_ray_complement_divisor_residues,
    two_one_ray_complement_divisor_root,
    two_one_ray_complement_divisor_sieve_certificate,
    two_one_ray_complement_divisor_sieve_residue_classes,
    two_one_ray_determinant_coordinates,
    two_one_ray_determinant_factor_certificate,
    two_one_ray_determinant_factor_roots,
    two_one_ray_determinant_divisor_certificate,
    two_one_ray_determinant_divisor_root,
    two_one_ray_determinant_paired_factor_lift_root,
    two_one_ray_determinant_paired_factor_root,
    two_one_ray_determinant_split_factor_certificate,
    two_one_ray_determinant_split_factor_period,
    two_one_ray_determinant_split_factor_witness,
    two_one_ray_determinant_slice_orbit,
    two_one_ray_determinant_slice_orbit_certificate,
    two_one_ray_determinant_slice_predecessor,
    two_one_ray_determinant_slice_reduced_root,
    two_one_ray_determinant_square_endpoint_orbit_certificate,
    two_one_ray_determinant_slice_successor,
    two_one_ray_determinant_slice_root,
    two_one_ray_euclid_parameter_certificate,
    two_one_ray_euclid_parameter_residue_classes,
    two_one_ray_euclid_parameter_roots,
    two_one_ray_mod_130_divisor_residues,
    two_one_ray_mod_ten_divisor_certificate,
    two_one_ray_mod_ten_divisor_orbit_certificate,
    two_one_ray_two_or_three_mod_five_parallel_certificate,
    two_one_ray_two_or_three_mod_five_parallel_orbit_certificate,
    two_one_ray_mod_eighty_two_divisor_certificate,
    two_one_ray_mod_eighty_two_divisor_orbit_certificate,
    two_one_ray_mod_thirty_four_divisor_certificate,
    two_one_ray_mod_thirty_four_divisor_orbit_certificate,
    two_one_ray_mod_fifty_eight_divisor_certificate,
    two_one_ray_mod_fifty_eight_divisor_orbit_certificate,
    two_one_ray_mod_seventy_four_divisor_certificate,
    two_one_ray_mod_seventy_four_divisor_orbit_certificate,
    two_one_ray_mod_twenty_six_divisor_certificate,
    two_one_ray_mod_twenty_six_divisor_orbit_certificate,
    two_one_ray_mod_twenty_six_square_factor_certificate,
    two_one_ray_paired_factor_split_factor_witness,
    two_one_ray_paired_factor_lift_witness,
    two_one_ray_prime_divisor_lift_certificate,
    two_one_ray_prime_divisor_lift_orbit_certificate,
    two_one_ray_prime_one_mod_four_double_direction_certificate,
    two_one_ray_promoted_determinant_split_factor_certificate,
    two_one_ray_promoted_inverse_root_certificate,
    two_one_ray_promoted_scaled_factor_certificate,
    two_one_ray_promoted_square_factor_certificate,
    two_one_ray_seed_certificate,
    two_one_ray_scaled_factor_divisor_certificate,
    two_one_ray_double_direction_certificate,
    two_one_ray_signed_euclid_root,
    two_one_ray_square_determinant_divisor_certificate,
    two_one_ray_square_determinant_factor_certificate,
    two_one_ray_square_determinant_factor_period,
    two_one_ray_square_determinant_factor_residues,
    two_one_ray_multiple_of_three_theorem3_certificate,
    two_one_ray_multiple_of_three_theorem3_orbit_certificate,
    two_one_ray_three_mod_four_certificate,
    two_one_ray_three_mod_four_orbit_certificate,
    two_three_even_root_spine_line_certificate,
    two_odd_root_spine_line_certificate,
    two_three_odd_root_spine_line_certificate,
    unit_coordinate_500_audit_certificate,
    unit_coordinate_500_residual_certificate,
    unit_coordinate_consecutive_hypotenuse_certificate,
    unit_coordinate_factor_four_parallel_certificate,
    unit_coordinate_factor_four_parallel_orbit_certificate,
    unit_coordinate_factor_five_parallel_certificate,
    unit_coordinate_factor_five_parallel_orbit_certificate,
    unit_coordinate_fifteen_eight_factor_two_parallel_certificate,
    unit_coordinate_fifteen_eight_factor_two_parallel_orbit_certificate,
    UNIT_COORDINATE_FIFTEEN_EIGHT_FACTOR_TWO_RESIDUAL_ROWS,
    unit_coordinate_twelve_thirty_five_factor_one_parallel_certificate,
    unit_coordinate_twelve_thirty_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_TWELVE_THIRTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_forty_nine_factor_one_parallel_certificate,
    unit_coordinate_forty_nine_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_FORTY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_twenty_eight_forty_five_factor_one_parallel_certificate,
    unit_coordinate_twenty_eight_forty_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_TWENTY_EIGHT_FORTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_sixty_eleven_factor_one_parallel_certificate,
    unit_coordinate_sixty_eleven_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_SIXTY_ELEVEN_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_forty_eight_fifty_five_factor_one_parallel_certificate,
    unit_coordinate_forty_eight_fifty_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_FORTY_EIGHT_FIFTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_eighty_thirty_nine_factor_one_parallel_certificate,
    unit_coordinate_eighty_thirty_nine_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_EIGHTY_THIRTY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_seventy_two_sixty_five_factor_one_parallel_certificate,
    unit_coordinate_seventy_two_sixty_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_SEVENTY_TWO_SIXTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_twenty_ninety_nine_factor_one_parallel_certificate,
    unit_coordinate_twenty_ninety_nine_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_TWENTY_NINETY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_sixty_ninety_one_factor_one_parallel_certificate,
    unit_coordinate_sixty_ninety_one_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_SIXTY_NINETY_ONE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_one_hundred_twelve_fifteen_factor_one_parallel_certificate,
    unit_coordinate_one_hundred_twelve_fifteen_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_ONE_HUNDRED_TWELVE_FIFTEEN_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_eighty_eight_one_hundred_five_factor_one_parallel_certificate,
    unit_coordinate_eighty_eight_one_hundred_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_EIGHTY_EIGHT_ONE_HUNDRED_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_one_hundred_forty_fifty_one_factor_one_parallel_certificate,
    unit_coordinate_one_hundred_forty_fifty_one_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_ONE_HUNDRED_FORTY_FIFTY_ONE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_one_hundred_thirty_two_eighty_five_factor_one_parallel_certificate,
    unit_coordinate_one_hundred_thirty_two_eighty_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_ONE_HUNDRED_THIRTY_TWO_EIGHTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_one_hundred_twenty_one_hundred_nineteen_factor_one_parallel_certificate,
    unit_coordinate_one_hundred_twenty_one_hundred_nineteen_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_ONE_HUNDRED_TWENTY_ONE_HUNDRED_NINETEEN_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_fifty_two_one_hundred_sixty_five_factor_one_parallel_certificate,
    unit_coordinate_fifty_two_one_hundred_sixty_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_FIFTY_TWO_ONE_HUNDRED_SIXTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_one_hundred_eighty_nineteen_factor_one_parallel_certificate,
    unit_coordinate_one_hundred_eighty_nineteen_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_ONE_HUNDRED_EIGHTY_NINETEEN_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_one_hundred_sixty_eight_ninety_five_factor_one_parallel_certificate,
    unit_coordinate_one_hundred_sixty_eight_ninety_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_ONE_HUNDRED_SIXTY_EIGHT_NINETY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_twenty_eight_one_hundred_ninety_five_factor_one_parallel_certificate,
    unit_coordinate_twenty_eight_one_hundred_ninety_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_TWENTY_EIGHT_ONE_HUNDRED_NINETY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_sixty_two_hundred_twenty_one_factor_one_parallel_certificate,
    unit_coordinate_sixty_two_hundred_twenty_one_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_SIXTY_TWO_HUNDRED_TWENTY_ONE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_three_hundred_twelve_twenty_five_factor_one_parallel_certificate,
    unit_coordinate_three_hundred_twelve_twenty_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_THREE_HUNDRED_TWELVE_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_three_hundred_eight_seventy_five_factor_one_parallel_certificate,
    unit_coordinate_three_hundred_eight_seventy_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_THREE_HUNDRED_EIGHT_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_two_hundred_eighty_eight_one_hundred_seventy_five_factor_one_parallel_certificate,
    unit_coordinate_two_hundred_eighty_eight_one_hundred_seventy_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_TWO_HUNDRED_EIGHTY_EIGHT_ONE_HUNDRED_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_one_hundred_eighty_two_hundred_ninety_nine_factor_one_parallel_certificate,
    unit_coordinate_one_hundred_eighty_two_hundred_ninety_nine_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_ONE_HUNDRED_EIGHTY_TWO_HUNDRED_NINETY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_two_hundred_seventy_two_two_hundred_twenty_five_factor_one_parallel_certificate,
    unit_coordinate_two_hundred_seventy_two_two_hundred_twenty_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_TWO_HUNDRED_SEVENTY_TWO_TWO_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_two_hundred_fifty_two_two_hundred_seventy_five_factor_one_parallel_certificate,
    unit_coordinate_two_hundred_fifty_two_two_hundred_seventy_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_TWO_HUNDRED_FIFTY_TWO_TWO_HUNDRED_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_three_hundred_fifty_two_one_hundred_thirty_five_factor_one_parallel_certificate,
    unit_coordinate_three_hundred_fifty_two_one_hundred_thirty_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_THREE_HUNDRED_FIFTY_TWO_ONE_HUNDRED_THIRTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_three_hundred_forty_one_hundred_eighty_nine_factor_one_parallel_certificate,
    unit_coordinate_three_hundred_forty_one_hundred_eighty_nine_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_THREE_HUNDRED_FORTY_ONE_HUNDRED_EIGHTY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_two_hundred_twenty_eight_three_hundred_twenty_five_factor_one_parallel_certificate,
    unit_coordinate_two_hundred_twenty_eight_three_hundred_twenty_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_TWO_HUNDRED_TWENTY_EIGHT_THREE_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_forty_three_hundred_ninety_nine_factor_one_parallel_certificate,
    unit_coordinate_forty_three_hundred_ninety_nine_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_FORTY_THREE_HUNDRED_NINETY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_one_hundred_twenty_three_hundred_ninety_one_factor_one_parallel_certificate,
    unit_coordinate_one_hundred_twenty_three_hundred_ninety_one_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_ONE_HUNDRED_TWENTY_THREE_HUNDRED_NINETY_ONE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_four_hundred_twenty_twenty_nine_factor_one_parallel_certificate,
    unit_coordinate_four_hundred_twenty_twenty_nine_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_FOUR_HUNDRED_TWENTY_TWENTY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_four_hundred_eight_one_hundred_forty_five_factor_one_parallel_certificate,
    unit_coordinate_four_hundred_eight_one_hundred_forty_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_FOUR_HUNDRED_EIGHT_ONE_HUNDRED_FORTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_two_hundred_eighty_three_hundred_fifty_one_factor_one_parallel_certificate,
    unit_coordinate_two_hundred_eighty_three_hundred_fifty_one_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_TWO_HUNDRED_EIGHTY_THREE_HUNDRED_FIFTY_ONE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_one_hundred_sixty_eight_four_hundred_twenty_five_factor_one_parallel_certificate,
    unit_coordinate_one_hundred_sixty_eight_four_hundred_twenty_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_ONE_HUNDRED_SIXTY_EIGHT_FOUR_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_three_hundred_eighty_two_hundred_sixty_one_factor_one_parallel_certificate,
    unit_coordinate_three_hundred_eighty_two_hundred_sixty_one_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_THREE_HUNDRED_EIGHTY_TWO_HUNDRED_SIXTY_ONE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_three_hundred_sixty_three_hundred_nineteen_factor_one_parallel_certificate,
    unit_coordinate_three_hundred_sixty_three_hundred_nineteen_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_THREE_HUNDRED_SIXTY_THREE_HUNDRED_NINETEEN_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_one_hundred_thirty_two_four_hundred_seventy_five_factor_one_parallel_certificate,
    unit_coordinate_one_hundred_thirty_two_four_hundred_seventy_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_ONE_HUNDRED_THIRTY_TWO_FOUR_HUNDRED_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_two_hundred_twenty_four_hundred_fifty_nine_factor_one_parallel_certificate,
    unit_coordinate_two_hundred_twenty_four_hundred_fifty_nine_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_TWO_HUNDRED_TWENTY_FOUR_HUNDRED_FIFTY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_four_hundred_forty_two_hundred_seventy_nine_factor_one_parallel_certificate,
    unit_coordinate_four_hundred_forty_two_hundred_seventy_nine_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_FOUR_HUNDRED_FORTY_TWO_HUNDRED_SEVENTY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_ninety_two_five_hundred_twenty_five_factor_one_parallel_certificate,
    unit_coordinate_ninety_two_five_hundred_twenty_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_NINETY_TWO_FIVE_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_four_hundred_twenty_three_hundred_forty_one_factor_one_parallel_certificate,
    unit_coordinate_four_hundred_twenty_three_hundred_forty_one_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_FOUR_HUNDRED_TWENTY_THREE_HUNDRED_FORTY_ONE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_five_hundred_thirty_two_one_hundred_sixty_five_factor_one_parallel_certificate,
    unit_coordinate_five_hundred_thirty_two_one_hundred_sixty_five_factor_one_parallel_orbit_certificate,
    UNIT_COORDINATE_FIVE_HUNDRED_THIRTY_TWO_ONE_HUNDRED_SIXTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
    unit_coordinate_factor_twenty_five_parallel_certificate,
    unit_coordinate_factor_twenty_five_parallel_orbit_certificate,
    unit_coordinate_one_mod_five_parallel_certificate,
    unit_coordinate_one_mod_five_parallel_orbit_certificate,
    unit_coordinate_promoted_mod_hundred_certificate,
    UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES,
    unit_coordinate_parallel_factor_orbit_certificate,
    unit_coordinate_parallel_factor_residues,
    unit_coordinate_residual_orthogonal_seed_certificate,
    UNIT_COORDINATE_RESIDUAL_ORTHOGONAL_SEED_ROWS,
    unit_coordinate_seven_mod_ten_parallel_certificate,
    unit_coordinate_seven_mod_ten_parallel_orbit_certificate,
    unit_coordinate_twenty_two_mod_twenty_five_parallel_certificate,
    unit_coordinate_twenty_two_mod_twenty_five_parallel_orbit_certificate,
    unit_coordinate_multiple_of_five_certificate,
    known_distance_three_obstruction_cases,
    y_squared_minus_y_plus_one_is_square,
)


ARTIFACT_DIR = Path(__file__).resolve().parents[1] / "data"


def assert_finite_box_audit(bound, audit_certificate):
    """Shared finite-box audit check with low per-target assertion overhead."""

    origin = (0, 0)
    known_orbit = KNOWN_DISTANCE_THREE_ORBIT
    for g in range(-bound, bound + 1):
        for h in range(-bound, bound + 1):
            target = (g, h)
            certificate = audit_certificate(target)

            if target == origin or target in known_orbit:
                assert certificate is None, target
                continue

            if edge(origin, target):
                if certificate is not None:
                    assert certificate.target == target
                    assert certificate.valid(), target
                continue

            assert certificate is not None, target
            assert certificate.target == target
            assert certificate.valid(), target


class BasicGraphPredicateTests(unittest.TestCase):
    def test_square_detection(self):
        self.assertTrue(is_square(0))
        self.assertTrue(is_square(25))
        self.assertFalse(is_square(26))
        self.assertFalse(is_square(-1))

    def test_edges_require_nonzero_coordinate_changes(self):
        self.assertTrue(edge((0, 0), (3, 4)))
        self.assertTrue(edge((0, 0), (4, -3)))
        self.assertFalse(edge((0, 0), (5, 0)))
        self.assertFalse(edge((0, 0), (0, 5)))
        self.assertFalse(edge((0, 0), (1, 1)))

    def test_known_three_step_path_to_1_0(self):
        self.assertTrue(path_is_valid([(0, 0), (9, 12), (-3, 3), (1, 0)]))

    def test_known_exception_orbit_under_stated_symmetries(self):
        expected_orbit = {
            (-2, -1), (-2, 0), (-2, 1),
            (-1, -2), (-1, 0), (-1, 2),
            (0, -2), (0, -1), (0, 1), (0, 2),
            (1, -2), (1, 0), (1, 2),
            (2, -1), (2, 0), (2, 1),
        }
        self.assertEqual(sign_swap_orbit((2, 1)), {
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1),
        })
        self.assertEqual(KNOWN_DISTANCE_THREE_ORBIT, expected_orbit)

    def test_theorem1_path_gives_three_step_upper_bound(self):
        for target in KNOWN_DISTANCE_THREE_ORBIT:
            path = theorem1_three_step_path(target)
            self.assertEqual(path[0], (0, 0))
            self.assertEqual(path[-1], target)
            self.assertLessEqual(len(path) - 1, 3)
            self.assertTrue(path_is_valid(path))

        for target in KNOWN_DISTANCE_THREE_REPRESENTATIVES:
            self.assertEqual(len(theorem1_three_step_path(target)) - 1, 3)

    def test_known_exception_symbolic_obstruction_cases(self):
        self.assertEqual(
            possible_integer_distance_differences((1, 0)),
            (0, 1),
        )
        self.assertEqual(
            possible_integer_distance_differences((2, 0)),
            (0, 1, 2),
        )
        self.assertEqual(
            possible_integer_distance_differences((2, 1)),
            (0, 1, 2),
        )

        expected_case_counts = {
            (1, 0): 2,
            (2, 0): 3,
            (2, 1): 3,
        }
        for target in KNOWN_DISTANCE_THREE_ORBIT:
            representative = canonical_known_distance_three_representative(target)
            self.assertIn(representative, expected_case_counts)
            self.assertEqual(
                len(known_distance_three_obstruction_cases(target)),
                expected_case_counts[representative],
            )

        for target in ((1, 1), (3, 0), (3, 1), (4, 2)):
            self.assertIsNone(canonical_known_distance_three_representative(target))
            self.assertEqual(known_distance_three_obstruction_cases(target), ())

    def test_y_squared_minus_y_plus_one_square_lemma(self):
        for y in range(-500, 501):
            value = y * y - y + 1
            self.assertEqual(
                y_squared_minus_y_plus_one_is_square(y),
                is_square(value),
            )
            self.assertEqual(
                y_squared_minus_y_plus_one_is_square(y),
                y in (0, 1),
            )


class CertificateTests(unittest.TestCase):
    def test_paper_two_step_examples(self):
        self.assertTrue(is_two_step_certificate((1, 1), (4, -3)))
        self.assertTrue(is_two_step_certificate((2, 4), (77, -36)))
        self.assertTrue(is_two_step_certificate((2111, 569), (-50643549, 196449668)))

    def test_certificate_lengths_are_squares(self):
        cert = Certificate(target=(2, 4), midpoint=(77, -36))
        self.assertTrue(cert.valid())
        self.assertEqual(cert.first_length_squared, 85 * 85)
        self.assertEqual(cert.second_length_squared, 85 * 85)

    def test_certificate_scaling_preserves_validity(self):
        base = Certificate(target=(1, 1), midpoint=(4, -3))
        self.assertTrue(base.valid())

        for factor in (-10, -1, 2, 17):
            scaled = scale_certificate(base, factor)
            self.assertEqual(scaled.target, (factor, factor))
            self.assertEqual(scaled.midpoint, (4 * factor, -3 * factor))
            self.assertTrue(scaled.valid())

        with self.assertRaises(ValueError):
            scale_certificate(base, 0)

    def test_certificate_scale_sign_swap_transport(self):
        base = Certificate(target=(3, 2), midpoint=(24, -18))
        self.assertTrue(base.valid())

        for factor, x_sign, y_sign, swap in ((5, -1, 1, False), (-7, 1, -1, True)):
            transformed = scale_signed_swap_certificate(base, factor, x_sign, y_sign, swap)
            scaled = scale_certificate(base, factor)
            self.assertEqual(
                transformed.target,
                signed_swap_point(scaled.target, x_sign, y_sign, swap),
            )
            self.assertEqual(
                transformed.midpoint,
                signed_swap_point(scaled.midpoint, x_sign, y_sign, swap),
            )
            self.assertTrue(transformed.valid())

        with self.assertRaises(ValueError):
            scale_signed_swap_certificate(base, 0, 1, 1)
        with self.assertRaises(ValueError):
            scale_signed_swap_certificate(base, 1, 0, 1)

    def test_sign_swap_certificate_transport(self):
        base = Certificate(target=(3, 2), midpoint=(24, -18))
        self.assertTrue(base.valid())

        for swap in (False, True):
            for x_sign in (-1, 1):
                for y_sign in (-1, 1):
                    target = signed_swap_point(base.target, x_sign, y_sign, swap)
                    transformed = sign_swap_certificate(base, target)
                    self.assertIsNotNone(transformed)
                    self.assertEqual(transformed.target, target)
                    self.assertEqual(
                        transformed.midpoint,
                        signed_swap_point(base.midpoint, x_sign, y_sign, swap),
                    )
                    self.assertTrue(transformed.valid())

        self.assertIsNone(sign_swap_certificate(base, (5, 5)))
        with self.assertRaises(ValueError):
            signed_swap_point((1, 2), 0, 1)

    def test_delta_slice_direction_generator_and_delta_order(self):
        directions = primitive_pythagorean_directions(5)
        root_directions = primitive_pythagorean_root_directions(5)
        self.assertIn((3, 4, 5, 2, 1), directions)
        self.assertIn((-4, 3, 5, 2, 1), directions)
        self.assertIn((5, 12, 13, 3, 2), directions)
        self.assertIn((3, 4, 5, (-1, 2), (-1, 0)), root_directions)
        self.assertIn((5, 12, 13, (-2, 3), (-1, 0)), root_directions)

        self.assertEqual(
            {(u, v, hypotenuse) for u, v, hypotenuse, _a, _b in directions},
            {
                (u, v, hypotenuse)
                for u, v, hypotenuse, _root, _unit in root_directions
            },
        )
        shape_directions = primitive_pythagorean_root_shape_directions(
            ((1, 4), (2, 3))
        )
        self.assertEqual(len(shape_directions), 16)
        self.assertEqual(
            {
                gaussian_root_shape(root)
                for _u, _v, _hypotenuse, root, _unit in shape_directions
            },
            {(1, 4), (2, 3)},
        )
        self.assertLessEqual(
            {
                (u, v, hypotenuse)
                for u, v, hypotenuse, _root, _unit in shape_directions
            },
            {
                (u, v, hypotenuse)
                for u, v, hypotenuse, _root, _unit in root_directions
            },
        )
        self.assertEqual(
            primitive_pythagorean_root_spine_shapes(8),
            (
                (1, 2),
                (2, 3),
                (1, 4),
                (3, 4),
                (2, 5),
                (1, 6),
                (4, 5),
                (2, 7),
                (1, 8),
                (3, 8),
            ),
        )
        self.assertEqual(
            primitive_pythagorean_root_primary_spine_shapes(8),
            ((1, 2), (2, 3), (1, 4), (2, 5), (1, 6), (2, 7), (1, 8)),
        )
        self.assertEqual(
            primitive_pythagorean_root_secondary_spine_shapes(8),
            ((3, 4), (4, 5), (3, 8)),
        )

        for u, v, hypotenuse, parameter_a, parameter_b in directions:
            self.assertGreater(parameter_a, parameter_b)
            self.assertEqual(u * u + v * v, hypotenuse * hypotenuse)
            self.assertNotEqual(u, 0)
            self.assertNotEqual(v, 0)

        for u, v, hypotenuse, root, unit in root_directions:
            self.assertEqual(gaussian_multiply(unit, gaussian_multiply(root, root)), (u, v))
            self.assertEqual(root[0] * root[0] + root[1] * root[1], hypotenuse)
            self.assertIn(unit, ((1, 0), (-1, 0), (0, 1), (0, -1)))

        self.assertEqual(signed_delta_values(3), (0, 1, -1, 2, -2, 3, -3))
        with self.assertRaises(ValueError):
            primitive_pythagorean_directions(1)
        with self.assertRaises(ValueError):
            primitive_pythagorean_root_directions(1)
        with self.assertRaises(ValueError):
            primitive_pythagorean_root_spine_shapes(1)
        with self.assertRaises(ValueError):
            primitive_pythagorean_root_primary_spine_shapes(1)
        with self.assertRaises(ValueError):
            primitive_pythagorean_root_secondary_spine_shapes(1)
        with self.assertRaises(ValueError):
            primitive_pythagorean_root_shape_directions(((2, 4),))
        with self.assertRaises(ValueError):
            primitive_pythagorean_root_shape_directions(((1, 3),))
        with self.assertRaises(ValueError):
            signed_delta_values(-1)

    def test_delta_slice_certificate_formula(self):
        examples = (
            ((1, 1), 2, 0),
            ((2, 5), 2, 5),
            ((16, 3), 8, 1),
            ((23, 3), 41, 0),
            ((25, 1), 50, 0),
            ((38, 1), 10, 3),
            ((109, 1), 2, 30),
        )
        for target, max_parameter, max_abs_delta in examples:
            certificate = delta_slice_certificate(
                target,
                max_parameter=max_parameter,
                max_abs_delta=max_abs_delta,
            )
            self.assertIsNotNone(certificate, target)
            self.assertEqual(certificate.target, target)
            self.assertTrue(certificate.valid())

            first_length = isqrt(certificate.first_length_squared)
            second_length = isqrt(certificate.second_length_squared)
            self.assertEqual(first_length * first_length, certificate.first_length_squared)
            self.assertEqual(second_length * second_length, certificate.second_length_squared)
            self.assertLessEqual(abs(first_length - second_length), max_abs_delta)

        for target in KNOWN_DISTANCE_THREE_ORBIT:
            self.assertIsNone(delta_slice_certificate(target, max_parameter=80))

        with self.assertRaises(ValueError):
            delta_slice_certificate((1, 1), max_parameter=1)
        with self.assertRaises(ValueError):
            delta_slice_certificate((1, 1), max_parameter=2, max_abs_delta=-1)

    def test_theorem3_is_unit_delta_slice_case(self):
        examples = (
            ((2, 5), PythagoreanTriple(3, 4, 5), 1, -1),
            ((5, 3), PythagoreanTriple(4, 3, 5), 1, -1),
            ((1, 9), PythagoreanTriple(3, 4, 5), -1, -1),
            ((1, 5), PythagoreanTriple(8, 15, 17), 1, -1),
        )
        for target, triple, x_sign, y_sign in examples:
            certificate = theorem3_certificate(target, triple, x_sign, y_sign)
            self.assertIsNotNone(certificate, target)
            self.assertTrue(certificate.valid())

            g, h = target
            signed_delta = g - h
            u = x_sign * triple.leg_a
            v = y_sign * triple.leg_b
            self.assertEqual(
                g * u + h * v - signed_delta * triple.hypotenuse,
                1,
            )

            first_length = isqrt(certificate.first_length_squared)
            second_length = isqrt(certificate.second_length_squared)
            self.assertEqual(first_length - second_length, signed_delta)
            self.assertEqual(first_length, triple.hypotenuse * g * h)

    def test_linear_delta_direction_certificate(self):
        examples = (
            ((1, 1), (-3, 4), (0, 0)),
            ((2, 5), (3, -4), (1, -1)),
            ((1, 10), (-3, -4), (1, -1)),
            ((3, 6), (-5, 12), (1, 0)),
            ((2, 5), (3, 4), (0, 1)),
        )
        for target, direction, delta_coefficients in examples:
            certificate = linear_delta_direction_certificate(
                target,
                direction,
                delta_coefficients,
            )
            self.assertIsNotNone(certificate, target)
            self.assertEqual(certificate.target, target)
            self.assertTrue(certificate.valid())

            g, h = target
            alpha, beta = delta_coefficients
            signed_delta = alpha * g + beta * h
            first_length = isqrt(certificate.first_length_squared)
            second_length = isqrt(certificate.second_length_squared)
            self.assertEqual(first_length - second_length, signed_delta)

        large_target = (3_000_000_000_000_000_000, 3_000_000_000_000_000_000)
        large_certificate = linear_delta_direction_certificate(
            large_target,
            (-3, 4),
            (0, 0),
        )
        self.assertIsNotNone(large_certificate)
        self.assertEqual(
            large_certificate.midpoint,
            (-9_000_000_000_000_000_000, 12_000_000_000_000_000_000),
        )
        self.assertGreater(abs(large_certificate.midpoint[1]), (1 << 63) - 1)
        self.assertTrue(large_certificate.valid())

        self.assertIsNone(linear_delta_direction_certificate((2, 1), (3, 4), (0, 0)))
        self.assertIsNone(linear_delta_direction_certificate((1, 8), (3, 4), (1, -1)))
        with self.assertRaises(ValueError):
            linear_delta_direction_certificate((1, 1), (1, 1), (0, 0))

    def test_delta_slice_bounded_discovery_probe(self):
        for g in range(1, 41):
            for h in range(1, 41):
                target = (g, h)
                if target in KNOWN_DISTANCE_THREE_ORBIT or edge((0, 0), target):
                    continue

                certificate = delta_slice_certificate(target, max_parameter=70)
                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

    def test_gaussian_transform_preserves_certificates_when_nondegenerate(self):
        base = Certificate(target=(1, 1), midpoint=(4, -3))
        self.assertEqual(gaussian_multiply((1, 1), (5, 12)), (-7, 17))

        for multiplier in ((1, 0), (0, 1), (5, 12), (12, 5), (-7, 24), (20, -21)):
            transformed = gaussian_transform_certificate(base, multiplier)
            self.assertIsNotNone(transformed)
            self.assertEqual(
                transformed.target,
                gaussian_multiply(base.target, multiplier),
            )
            self.assertEqual(
                transformed.midpoint,
                gaussian_multiply(base.midpoint, multiplier),
            )
            self.assertTrue(transformed.valid())

            multiplier_norm = multiplier[0] * multiplier[0] + multiplier[1] * multiplier[1]
            self.assertEqual(
                transformed.first_length_squared,
                base.first_length_squared * multiplier_norm,
            )
            self.assertEqual(
                transformed.second_length_squared,
                base.second_length_squared * multiplier_norm,
            )

        for degenerate_multiplier in ((3, 4), (4, 3), (3, -4), (-4, 3)):
            self.assertIsNone(gaussian_transform_certificate(base, degenerate_multiplier))

        with self.assertRaises(ValueError):
            gaussian_transform_certificate(base, (1, 1))
        with self.assertRaises(ValueError):
            gaussian_transform_certificate(Certificate(target=(1, 0), midpoint=(1, 1)), (1, 0))

    def test_gaussian_divisor_certificate_family(self):
        bases = (
            Certificate(target=(1, 1), midpoint=(4, -3)),
            Certificate(target=(2, 4), midpoint=(77, -36)),
            Certificate(target=(3, 2), midpoint=(24, -18)),
        )

        self.assertEqual(gaussian_quotient_if_integer((-7, 17), (1, 1)), (5, 12))
        self.assertEqual(gaussian_quotient_if_integer((-10, 20), (2, 4)), (3, 4))
        self.assertIsNone(gaussian_quotient_if_integer((1, 2), (2, 4)))
        with self.assertRaises(ValueError):
            gaussian_quotient_if_integer((1, 2), (0, 0))

        for base in bases:
            self.assertTrue(base.valid())
            for multiplier in ((1, 0), (0, 1), (3, 4), (5, 12), (-12, 5)):
                target = gaussian_multiply(base.target, multiplier)
                cert = gaussian_divisor_certificate(target, base)
                if cert is None:
                    self.assertIsNone(gaussian_transform_certificate(base, multiplier))
                    continue

                self.assertEqual(cert.target, target)
                self.assertEqual(
                    cert,
                    gaussian_transform_certificate(base, multiplier),
                )
                self.assertTrue(cert.valid())
                self.assertEqual(
                    first_gaussian_divisor_certificate(target, (base,)),
                    cert,
                )

        base = Certificate(target=(2, 4), midpoint=(77, -36))
        self.assertIsNone(gaussian_divisor_certificate(gaussian_multiply((2, 4), (1, 1)), base))
        self.assertIsNone(first_gaussian_divisor_certificate((1, 2), bases))
        with self.assertRaises(ValueError):
            gaussian_divisor_certificate((1, 1), Certificate(target=(1, 0), midpoint=(1, 1)))

    def test_primitive_pythagorean_direction_gaussian_root(self):
        for direction in ((-9, 40), (-24, 7), (-40, 9), (3, 4), (4, -3)):
            root, unit = primitive_pythagorean_direction_gaussian_root(direction)
            root_square = gaussian_multiply(root, root)
            self.assertEqual(gaussian_multiply(unit, root_square), direction)
            self.assertEqual(root[0] * root[0] + root[1] * root[1], isqrt(
                direction[0] * direction[0] + direction[1] * direction[1]
            ))
            self.assertIn(unit, ((1, 0), (-1, 0), (0, 1), (0, -1)))

        self.assertEqual(
            primitive_pythagorean_direction_conjugate_root_residue((-9, 40)),
            (41, 9),
        )
        self.assertEqual(
            primitive_pythagorean_direction_conjugate_root_residue((-24, 7)),
            (25, 18),
        )
        self.assertEqual(
            gaussian_root_conjugate_divisibility_residue((1, 4)),
            (17, 13),
        )
        for k in range(1, 5):
            modulus, residue = gaussian_root_conjugate_divisibility_residue((1, 2 * k))
            self.assertEqual(modulus, 4 * k * k + 1)
            self.assertEqual(residue, (modulus - 2 * k) % modulus)
        for k in range(1, 4):
            root_imaginary = 2 * k + 1
            modulus, residue = gaussian_root_conjugate_divisibility_residue(
                (2, root_imaginary)
            )
            self.assertEqual(modulus, root_imaginary * root_imaginary + 4)
            self.assertEqual(residue, (-root_imaginary * pow(2, -1, modulus)) % modulus)
        self.assertEqual(gaussian_root_shape((-2, 3)), (2, 3))
        self.assertEqual(gaussian_root_shape((-3, -2)), (2, 3))
        with self.assertRaises(ValueError):
            gaussian_root_shape((0, 3))
        with self.assertRaises(ValueError):
            gaussian_root_conjugate_divisibility_residue((2, 4))
        for direction, split_root in (
            ((-9, 40), (19, -239)),
            ((-24, 7), (41, -37)),
            ((-40, 9), (401, 81)),
        ):
            modulus, residue = primitive_pythagorean_direction_conjugate_root_residue(
                direction
            )
            self.assertEqual((residue * residue + 1) % modulus, 0)
            self.assertEqual(
                (split_root[1] - residue * split_root[0]) % modulus,
                0,
            )
            self.assertIsNotNone(
                parallel_direction_squareclass_line_split_quotient(
                    direction,
                    *split_root,
                )
            )

        witness = parallel_direction_conjugate_ideal_witness((151, 338), (-9, 40))
        self.assertIsNotNone(witness)
        self.assertEqual(witness.root_shape, (4, 5))
        self.assertEqual(witness.conjugate_root_residue, (41, 9))
        self.assertEqual(witness.determinant_squareclass_quotient, -4541)
        self.assertEqual(witness.divisor_root_residue, 33)
        self.assertTrue(witness.split_root_congruence_holds)
        self.assertTrue(witness.divisor_root_congruence_holds)

        with self.assertRaises(ValueError):
            primitive_pythagorean_direction_gaussian_root((6, 8))
        with self.assertRaises(ValueError):
            primitive_pythagorean_direction_gaussian_root((1, 1))

    def test_diagonal_pythagorean_multiplier_family(self):
        for multiplier in ((1, 0), (0, 1), (5, 12), (12, 5), (-7, 24), (20, -21)):
            target = gaussian_multiply((1, 1), multiplier)
            cert = diagonal_pythagorean_multiplier_certificate(target)
            self.assertIsNotNone(cert)
            self.assertEqual(cert.target, target)
            self.assertTrue(cert.valid())

        for target in ((2, 1), (1, 2), (3, 5), (-1, 7), (7, 1)):
            self.assertIsNone(diagonal_pythagorean_multiplier_certificate(target))

    def test_lattice_coefficients_build_two_step_certificates(self):
        self.assertEqual(lattice_coefficients((7, 0), (3, 4), (4, 3)), (-3, 4))
        self.assertEqual(
            lattice_coefficient_cramer_data((7, 0), (3, 4), (4, 3)),
            (-7, 21, -28, True, True, -3, 4),
        )
        cert = lattice_two_step_certificate((7, 0), (3, 4), (4, 3))
        self.assertIsNotNone(cert)
        self.assertEqual(cert.midpoint, (-9, -12))
        self.assertTrue(cert.valid())

        self.assertEqual(lattice_coefficients((1, 1), (3, -4), (4, -3)), (-1, 1))
        self.assertEqual(
            lattice_coefficient_cramer_data((1, 1), (3, -4), (4, -3)),
            (7, -7, 7, True, True, -1, 1),
        )
        cert = lattice_two_step_certificate((1, 1), (3, -4), (4, -3))
        self.assertIsNotNone(cert)
        self.assertEqual(cert.midpoint, (-3, 4))
        self.assertTrue(cert.valid())

        self.assertIsNone(lattice_coefficients((1, 0), (3, 4), (4, 3)))
        self.assertEqual(
            lattice_coefficient_cramer_data((1, 0), (3, 4), (4, 3)),
            (-7, 3, -4, False, False, None, None),
        )
        first_coefficient = (1 << 63) + 5
        second_coefficient = -(1 << 63) - 9
        large_target = (
            3 * first_coefficient + 4 * second_coefficient,
            4 * first_coefficient + 3 * second_coefficient,
        )
        self.assertEqual(
            lattice_coefficient_cramer_data(large_target, (3, 4), (4, 3)),
            (
                -7,
                -7 * first_coefficient,
                -7 * second_coefficient,
                True,
                True,
                first_coefficient,
                second_coefficient,
            ),
        )
        with self.assertRaises(ValueError):
            lattice_coefficient_cramer_data((1, 1), (1, 1), (4, 4))
        with self.assertRaises(ValueError):
            lattice_two_step_certificate((1, 1), (1, 1), (4, 3))

    def test_parallel_direction_divisor_reduction(self):
        self.assertEqual(positive_divisors(36), (1, 2, 3, 4, 6, 9, 12, 18, 36))
        with self.assertRaises(ValueError):
            positive_divisors(0)
        self.assertEqual(squareclass_decomposition(201601), (1, 449))
        self.assertEqual(squareclass_decomposition(722), (2, 19))
        self.assertEqual(squarefree_numbers(10), (1, 2, 3, 5, 6, 7, 10))
        self.assertEqual(squarefree_divisors(72), (1, 2, 3, 6))
        self.assertEqual(divisor_residue_classes(36, 13), (1, 2, 3, 4, 5, 6, 9, 10, 12))
        self.assertEqual(divisor_residue_classes(175, 13), (1, 5, 6, 7, 9, 12))
        self.assertEqual(primitive_root_mod_prime(13), 2)
        self.assertEqual(primitive_root_mod_prime(17), 3)
        log_table = discrete_log_table_mod_prime(13)
        self.assertEqual(log_table[1], 0)
        self.assertEqual(log_table[2], 1)
        self.assertEqual(log_table[11], 7)
        self.assertEqual(
            prime_modulus_divisor_exponent_summands(175, 13),
            (
                False,
                (
                    (5, 9, 2, (0, 6, 9)),
                    (7, 11, 1, (0, 11)),
                ),
            ),
        )
        self.assertEqual(
            prime_modulus_divisor_exponent_classes(175, 13),
            (False, (0, 5, 6, 8, 9, 11)),
        )
        self.assertEqual(
            cyclic_sumset(12, ((0, 6, 9), (0, 11))),
            (0, 5, 6, 8, 9, 11),
        )
        self.assertEqual(
            cyclic_subset_stabilizer_step(12, (0, 5, 6, 8, 9, 11)),
            12,
        )
        self.assertEqual(
            cyclic_sumset_kneser_data(12, ((0, 6, 9), (0, 11))),
            (12, 4, 2),
        )
        self.assertEqual(
            cyclic_sumset_effective_length(((0, 6, 9), (0, 11))),
            3,
        )
        self.assertEqual(
            cyclic_sumset_saturation_gap(12, ((0, 6, 9), (0, 11))),
            (3, 4, 8),
        )
        self.assertEqual(
            cyclic_sumset_kneser_data(12, ((0, 4, 8), (0, 9))),
            (4, 6, 0),
        )
        self.assertEqual(
            prime_modulus_divisor_exponent_classes(13 * 25, 13),
            (True, (0, 6, 9)),
        )
        self.assertTrue(has_divisor_in_residue_classes(175, 13, (7,)))
        self.assertFalse(has_divisor_in_residue_classes(175, 13, (11,)))
        with self.assertRaises(ValueError):
            squareclass_decomposition(0)
        with self.assertRaises(ValueError):
            squarefree_numbers(0)
        with self.assertRaises(ValueError):
            squarefree_divisors(0)
        with self.assertRaises(ValueError):
            divisor_residue_classes(0, 13)
        with self.assertRaises(ValueError):
            divisor_residue_classes(36, 0)
        with self.assertRaises(ValueError):
            primitive_root_mod_prime(15)
        with self.assertRaises(ValueError):
            prime_modulus_divisor_exponent_classes(36, 15)
        with self.assertRaises(ValueError):
            cyclic_sumset(0, ((0,),))
        with self.assertRaises(ValueError):
            cyclic_subset_stabilizer_step(12, ())
        with self.assertRaises(ValueError):
            cyclic_sumset_kneser_data(12, ((0,), ()))
        with self.assertRaises(ValueError):
            cyclic_sumset_effective_length(((0,), ()))
        with self.assertRaises(ValueError):
            cyclic_sumset_saturation_gap(12, ((0,), ()))

        self.assertEqual(parallel_direction_factor_modulus((3, 4), 648), 32400)
        self.assertEqual(parallel_direction_factor_coefficient((39, 64), (3, 4), 648), 2)
        self.assertEqual(
            parallel_direction_factor_congruence_data((39, 64), (3, 4), 648),
            (36, 65, 2),
        )
        self.assertEqual(
            parallel_direction_factor_pair_row_from_congruence_data(
                (39, 64),
                (3, 4),
                648,
            ),
            (36, 2, -323, 325, 65, 2),
        )
        witness = parallel_direction_factor_witness((39, 64), (3, 4), 648)
        self.assertEqual(
            witness,
            ParallelDirectionFactorWitness(
                target=(39, 64),
                direction=(3, 4),
                factor=648,
                determinant_leg=36,
                other_leg=-323,
                scaled_hypotenuse=325,
                second_length=65,
                first_coefficient=2,
            ),
        )
        self.assertEqual(witness.midpoint, (6, 8))
        self.assertTrue(witness.certificate.valid())
        self.assertEqual(
            parallel_direction_witness((39, 64), (3, 4)),
            ParallelDirectionFactorWitness(
                target=(39, 64),
                direction=(3, 4),
                factor=8,
                determinant_leg=36,
                other_leg=77,
                scaled_hypotenuse=85,
                second_length=17,
                first_coefficient=18,
            ),
        )

        certificate = parallel_direction_factor_certificate((39, 64), (3, 4), 648)
        self.assertIsNotNone(certificate)
        self.assertEqual(certificate.midpoint, (6, 8))
        self.assertTrue(certificate.valid())

        split_witness = parallel_direction_squareclass_split_witness(
            (151, 338),
            (-9, 40),
            2,
            19,
        )
        self.assertEqual(
            split_witness,
            ParallelDirectionSquareclassSplitWitness(
                squareclass=2,
                split_factor=19,
                paired_split_factor=239,
                factor_witness=ParallelDirectionFactorWitness(
                    target=(151, 338),
                    direction=(-9, 40),
                    factor=722,
                    determinant_leg=-9082,
                    other_leg=56760,
                    scaled_hypotenuse=57482,
                    second_length=1402,
                    first_coefficient=41,
                ),
            ),
        )
        self.assertEqual(split_witness.midpoint, (-369, 1640))
        self.assertEqual(split_witness.signed_paired_split_factor, -239)
        self.assertTrue(split_witness.certificate.valid())
        self.assertEqual(
            parallel_direction_squareclass_split_certificate((151, 338), (-9, 40), 2, 19),
            split_witness.certificate,
        )
        line_certificate = parallel_direction_squareclass_line_certificate(
            (-9, 40),
            2,
            19,
            -239,
            41,
        )
        self.assertEqual(
            parallel_direction_squareclass_line_gaussian_numerator(
                (-9, 40),
                2,
                19,
                -239,
            ),
            (1748240, -4377324),
        )
        self.assertEqual(
            parallel_direction_squareclass_line_second_step((-9, 40), 2, 19, -239),
            (520, -1302),
        )
        self.assertEqual(
            parallel_direction_squareclass_line_root_quotient((-9, 40), 2, 19, -239),
            (520, -1302),
        )
        self.assertEqual(
            parallel_direction_squareclass_line_split_quotient((-9, 40), 19, -239),
            (-31, 21),
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_split_root((-9, 40), (-31, 21)),
            (19, -239),
        )
        self.assertTrue(squareclass_beta_integral(2, (-31, 21)))
        self.assertTrue(squareclass_beta_integral(1, (19, -19)))
        self.assertFalse(squareclass_beta_integral(1, (-31, 22)))
        self.assertFalse(beta_square_is_axis_degenerate((-31, 21)))
        self.assertTrue(beta_square_is_axis_degenerate((19, -19)))
        self.assertTrue(beta_square_is_axis_degenerate((19, 0)))
        self.assertEqual(
            parallel_direction_squareclass_beta_quotient((-9, 40), 2, (-31, 21)),
            (520, -1302),
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_second_step((-9, 40), 2, (-31, 21)),
            (520, -1302),
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_determinant_residue(
                (-9, 40),
                2,
                (-31, 21),
            ),
            -9082,
        )
        self.assertEqual(determinant((-9, 40), (151, 338)), -9082)
        self.assertEqual(
            parallel_direction_squareclass_conjugate_ideal_split_roots(
                (-9, 40),
                -9082,
                2,
            ),
            ((19, -239, (-31, 21)),),
        )
        self.assertIn(
            (2, 19, -239, (-31, 21)),
            parallel_direction_conjugate_ideal_split_roots((151, 338), (-9, 40)),
        )
        self.assertEqual(
            parallel_direction_conjugate_ideal_split_roots((151, 338), (-9, 40)),
            parallel_direction_conjugate_ideal_determinant_roots((-9, 40), -9082),
        )
        ideal_witness = ParallelDirectionConjugateIdealWitness(
            target=(151, 338),
            direction=(-9, 40),
            squareclass=2,
            split_factor=19,
            signed_paired_split_factor=-239,
            beta=(-31, 21),
            first_coefficient=41,
        )
        self.assertTrue(ideal_witness.valid())
        self.assertEqual(ideal_witness.root, (-4, -5))
        self.assertEqual(ideal_witness.unit, (1, 0))
        self.assertEqual(ideal_witness.gaussian_quadratic_left, (302, 676))
        self.assertEqual(
            ideal_witness.gaussian_quadratic_left,
            ideal_witness.gaussian_quadratic_right,
        )
        self.assertEqual(
            parallel_direction_squareclass_conjugate_ideal_witness(
                (151, 338),
                (-9, 40),
                2,
            ),
            ideal_witness,
        )
        self.assertEqual(
            parallel_direction_conjugate_ideal_witness((151, 338), (-9, 40)),
            ideal_witness,
        )
        self.assertEqual(
            parallel_direction_conjugate_ideal_cover_witness((151, 338), 8),
            ideal_witness,
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_line_certificate(
                (-9, 40),
                2,
                (-31, 21),
                41,
            ),
            line_certificate,
        )
        self.assertEqual(
            parallel_direction_conjugate_ideal_certificate((151, 338), (-9, 40)),
            line_certificate,
        )
        self.assertEqual(
            parallel_direction_squareclass_conjugate_ideal_certificate(
                (151, 338),
                (-9, 40),
                2,
            ),
            line_certificate,
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_target_coefficient(
                (151, 338),
                (-9, 40),
                2,
                (-31, 21),
            ),
            41,
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_determinant_target_coefficient(
                (151, 338),
                (-9, 40),
                2,
                (-31, 21),
            ),
            41,
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_quadratic_coefficient(
                (151, 338),
                (-9, 40),
                2,
                (-31, 21),
            ),
            41,
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_target_certificate(
                (151, 338),
                (-9, 40),
                2,
                (-31, 21),
            ),
            line_certificate,
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_quadratic_certificate(
                (151, 338),
                (-9, 40),
                2,
                (-31, 21),
            ),
            line_certificate,
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_determinant_target_certificate(
                (151, 338),
                (-9, 40),
                2,
                (-31, 21),
            ),
            line_certificate,
        )
        self.assertTrue(
            parallel_direction_squareclass_line_congruence_holds((-9, 40), 2, 19, -239)
        )
        self.assertEqual(line_certificate, split_witness.certificate)
        shifted_line_certificate = parallel_direction_squareclass_line_certificate(
            (-9, 40),
            2,
            19,
            -239,
            42,
        )
        self.assertIsNotNone(shifted_line_certificate)
        self.assertEqual(shifted_line_certificate.target, (142, 378))
        self.assertEqual(shifted_line_certificate.midpoint, (-378, 1680))
        self.assertTrue(shifted_line_certificate.valid())
        self.assertEqual(
            parallel_direction_squareclass_beta_target_coefficient(
                (142, 378),
                (-9, 40),
                2,
                (-31, 21),
            ),
            42,
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_determinant_target_coefficient(
                (142, 378),
                (-9, 40),
                2,
                (-31, 21),
            ),
            42,
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_quadratic_coefficient(
                (142, 378),
                (-9, 40),
                2,
                (-31, 21),
            ),
            42,
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_target_certificate(
                (142, 378),
                (-9, 40),
                2,
                (-31, 21),
            ),
            shifted_line_certificate,
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_quadratic_certificate(
                (142, 378),
                (-9, 40),
                2,
                (-31, 21),
            ),
            shifted_line_certificate,
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_determinant_target_certificate(
                (142, 378),
                (-9, 40),
                2,
                (-31, 21),
            ),
            shifted_line_certificate,
        )
        self.assertIsNone(
            parallel_direction_squareclass_beta_target_certificate(
                (151, 339),
                (-9, 40),
                2,
                (-31, 21),
            )
        )
        self.assertIsNone(
            parallel_direction_squareclass_beta_determinant_target_certificate(
                (151, 339),
                (-9, 40),
                2,
                (-31, 21),
            )
        )
        self.assertIsNone(
            parallel_direction_squareclass_beta_quadratic_certificate(
                (151, 339),
                (-9, 40),
                2,
                (-31, 21),
            )
        )

        period, residues = parallel_direction_squareclass_line_residue_classes(
            (-9, 40),
            2,
            19,
        )
        self.assertEqual(period, 3362)
        self.assertEqual(len(residues), 81)
        self.assertIn((-239) % period, residues)
        self.assertNotIn((-238) % period, residues)
        self.assertEqual(
            parallel_direction_squareclass_line_residue_certificate(
                (151, 338),
                (-9, 40),
                2,
                19,
            ),
            split_witness.certificate,
        )
        self.assertEqual(
            parallel_direction_squareclass_line_residue_certificate(
                (142, 378),
                (-9, 40),
                2,
                19,
            ),
            shifted_line_certificate,
        )
        self.assertIsNone(
            parallel_direction_squareclass_line_residue_certificate(
                (151, 339),
                (-9, 40),
                2,
                19,
            )
        )
        self.assertEqual(
            parallel_direction_squareclass_line_residue_classes((-40, 9), 149, 401),
            (82, (81,)),
        )
        self.assertEqual(
            parallel_direction_squareclass_line_residue_classes((-24, 7), 34, 41),
            (25, (13,)),
        )
        for direction, squareclass, split_factor in (
            ((-9, 40), 2, 19),
            ((-40, 9), 149, 401),
            ((-24, 7), 34, 41),
        ):
            modulus = 2 * (direction[0] * direction[0] + direction[1] * direction[1])
            for residue in range(modulus):
                paired = residue if residue else modulus
                split_quotient = parallel_direction_squareclass_line_split_quotient(
                    direction,
                    split_factor,
                    paired,
                )
                expected = False
                if split_quotient is not None:
                    quotient_square = gaussian_multiply(split_quotient, split_quotient)
                    expected = (
                        (squareclass * quotient_square[0]) % 2 == 0
                        and (squareclass * quotient_square[1]) % 2 == 0
                    )
                self.assertEqual(
                    parallel_direction_squareclass_line_congruence_holds(
                        direction,
                        squareclass,
                        split_factor,
                        paired,
                    ),
                    expected,
                    (direction, squareclass, split_factor, paired),
                )

        frontier_line_examples = (
            ((199, 1462), (-24, -7), 115, 1, -293, 7874),
            ((1262, 1781), (-24, 7), 34, 41, -37, -37),
        )
        for target, direction, squareclass, split_factor, paired, coefficient in (
            frontier_line_examples
        ):
            certificate = parallel_direction_squareclass_line_certificate(
                direction,
                squareclass,
                split_factor,
                paired,
                coefficient,
            )
            self.assertIsNotNone(certificate, target)
            self.assertEqual(certificate.target, target)
            self.assertTrue(certificate.valid())
            gaussian_numerator = parallel_direction_squareclass_line_gaussian_numerator(
                direction,
                squareclass,
                split_factor,
                paired,
            )
            gaussian_denominator = 2 * (
                direction[0] * direction[0] + direction[1] * direction[1]
            )
            self.assertEqual(
                (
                    gaussian_numerator[0] // gaussian_denominator,
                    gaussian_numerator[1] // gaussian_denominator,
                ),
                (target[0] - certificate.midpoint[0], target[1] - certificate.midpoint[1]),
            )
            self.assertEqual(
                parallel_direction_squareclass_line_root_quotient(
                    direction,
                    squareclass,
                    split_factor,
                    paired,
                ),
                (target[0] - certificate.midpoint[0], target[1] - certificate.midpoint[1]),
            )
            split_quotient = parallel_direction_squareclass_line_split_quotient(
                direction,
                split_factor,
                paired,
            )
            self.assertIsNotNone(split_quotient, target)
            self.assertEqual(
                parallel_direction_squareclass_beta_split_root(direction, split_quotient),
                (split_factor, paired),
            )
            self.assertEqual(
                parallel_direction_squareclass_beta_quotient(
                    direction,
                    squareclass,
                    split_quotient,
                ),
                (target[0] - certificate.midpoint[0], target[1] - certificate.midpoint[1]),
            )
            self.assertEqual(
                parallel_direction_squareclass_beta_second_step(
                    direction,
                    squareclass,
                    split_quotient,
                ),
                (target[0] - certificate.midpoint[0], target[1] - certificate.midpoint[1]),
            )
            self.assertEqual(
                parallel_direction_squareclass_beta_determinant_residue(
                    direction,
                    squareclass,
                    split_quotient,
                ),
                squareclass * split_factor * paired,
            )
            self.assertEqual(
                parallel_direction_squareclass_beta_determinant_residue(
                    direction,
                    squareclass,
                    split_quotient,
                ),
                determinant(direction, target),
            )
            self.assertIn(
                (split_factor, paired, split_quotient),
                parallel_direction_squareclass_conjugate_ideal_split_roots(
                    direction,
                    determinant(direction, target),
                    squareclass,
                ),
            )
            self.assertIn(
                (squareclass, split_factor, paired, split_quotient),
                parallel_direction_conjugate_ideal_split_roots(target, direction),
            )
            self.assertEqual(
                parallel_direction_conjugate_ideal_split_roots(target, direction),
                parallel_direction_conjugate_ideal_determinant_roots(
                    direction,
                    determinant(direction, target),
                ),
            )
            squareclass_ideal_witness = (
                parallel_direction_squareclass_conjugate_ideal_witness(
                    target,
                    direction,
                    squareclass,
                )
            )
            self.assertIsNotNone(squareclass_ideal_witness, target)
            self.assertEqual(squareclass_ideal_witness.direction, direction)
            self.assertEqual(squareclass_ideal_witness.squareclass, squareclass)
            self.assertEqual(squareclass_ideal_witness.split_factor, split_factor)
            self.assertEqual(
                squareclass_ideal_witness.signed_paired_split_factor,
                paired,
            )
            self.assertEqual(squareclass_ideal_witness.beta, split_quotient)
            self.assertEqual(squareclass_ideal_witness.first_coefficient, coefficient)
            self.assertEqual(
                squareclass_ideal_witness.gaussian_quadratic_left,
                squareclass_ideal_witness.gaussian_quadratic_right,
            )
            self.assertTrue(squareclass_ideal_witness.valid())
            self.assertEqual(
                parallel_direction_conjugate_ideal_witness(target, direction),
                squareclass_ideal_witness,
            )
            self.assertEqual(
                parallel_direction_squareclass_beta_line_certificate(
                    direction,
                    squareclass,
                    split_quotient,
                    coefficient,
                ),
                certificate,
            )
            self.assertEqual(
                parallel_direction_conjugate_ideal_certificate(target, direction),
                certificate,
            )
            self.assertEqual(
                parallel_direction_squareclass_conjugate_ideal_certificate(
                    target,
                    direction,
                    squareclass,
                ),
                certificate,
            )
            self.assertEqual(
                parallel_direction_squareclass_beta_target_coefficient(
                    target,
                    direction,
                    squareclass,
                    split_quotient,
                ),
                coefficient,
            )
            self.assertEqual(
                parallel_direction_squareclass_beta_determinant_target_coefficient(
                    target,
                    direction,
                    squareclass,
                    split_quotient,
                ),
                coefficient,
            )
            self.assertEqual(
                parallel_direction_squareclass_beta_quadratic_coefficient(
                    target,
                    direction,
                    squareclass,
                    split_quotient,
                ),
                coefficient,
            )
            self.assertEqual(
                parallel_direction_squareclass_beta_target_certificate(
                    target,
                    direction,
                    squareclass,
                    split_quotient,
                ),
                certificate,
            )
            self.assertEqual(
                parallel_direction_squareclass_beta_quadratic_certificate(
                    target,
                    direction,
                    squareclass,
                    split_quotient,
                ),
                certificate,
            )
            self.assertEqual(
                parallel_direction_squareclass_beta_determinant_target_certificate(
                    target,
                    direction,
                    squareclass,
                    split_quotient,
                ),
                certificate,
            )
            quotient_square = gaussian_multiply(split_quotient, split_quotient)
            self.assertEqual(
                (squareclass * quotient_square[0]) % 2,
                0,
            )
            self.assertEqual(
                (squareclass * quotient_square[1]) % 2,
                0,
            )
            self.assertEqual(
                parallel_direction_squareclass_line_residue_certificate(
                    target,
                    direction,
                    squareclass,
                    split_factor,
                ),
                certificate,
            )

        self.assertIsNone(
            parallel_direction_squareclass_line_certificate((-9, 40), 2, 19, -238, 41)
        )
        self.assertIsNone(
            parallel_direction_squareclass_line_second_step((-9, 40), 2, 19, -238)
        )
        self.assertFalse(
            parallel_direction_squareclass_line_congruence_holds((-9, 40), 2, 19, -238)
        )
        self.assertTrue(
            parallel_direction_squareclass_line_congruence_holds((-9, 40), 2, 19, 171)
        )
        self.assertEqual(
            parallel_direction_squareclass_line_root_quotient((-9, 40), 2, 19, 171),
            (0, -722),
        )
        self.assertEqual(
            parallel_direction_squareclass_line_split_quotient((-9, 40), 19, 171),
            (19, -19),
        )
        self.assertEqual(
            parallel_direction_squareclass_beta_split_root((-9, 40), (19, -19)),
            (19, 171),
        )
        self.assertTrue(squareclass_beta_integral(2, (19, -19)))
        self.assertTrue(beta_square_is_axis_degenerate((19, -19)))
        self.assertEqual(
            parallel_direction_squareclass_beta_quotient((-9, 40), 2, (19, -19)),
            (0, -722),
        )
        self.assertIsNone(
            parallel_direction_squareclass_beta_second_step((-9, 40), 2, (19, -19))
        )
        self.assertIsNone(
            parallel_direction_squareclass_beta_determinant_residue(
                (-9, 40),
                2,
                (19, -19),
            )
        )
        self.assertEqual(
            parallel_direction_squareclass_conjugate_ideal_split_roots(
                (-9, 40),
                2 * 19 * 171,
                2,
            ),
            (),
        )
        self.assertIsNone(
            parallel_direction_squareclass_line_second_step((-9, 40), 2, 19, 171)
        )
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_split_witness((151, 338), (-9, 40), 4, 1)
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_split_witness((151, 338), (-9, 40), 2, 0)
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_line_certificate((-9, 40), 4, 1, 1, 1)
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_line_certificate((-9, 40), 2, 1, 0, 1)
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_line_second_step((-9, 40), 4, 1, 1)
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_line_second_step((-9, 40), 2, 1, 0)
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_line_congruence_holds((-9, 40), 4, 1, 1)
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_line_congruence_holds((-9, 40), 2, 1, 0)
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_line_gaussian_numerator((-9, 40), 4, 1, 1)
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_line_gaussian_numerator((-9, 40), 2, 1, 0)
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_line_root_quotient((-9, 40), 4, 1, 1)
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_line_root_quotient((-9, 40), 2, 1, 0)
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_line_split_quotient((-9, 40), 0, 1)
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_line_split_quotient((-9, 40), 1, 0)
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_beta_split_root((-9, 40), (0, 0))
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_beta_quotient((-9, 40), 4, (1, 1))
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_beta_quotient((-9, 40), 2, (0, 0))
        with self.assertRaises(ValueError):
            squareclass_beta_integral(4, (1, 1))
        with self.assertRaises(ValueError):
            squareclass_beta_integral(1, (0, 0))
        with self.assertRaises(ValueError):
            beta_square_is_axis_degenerate((0, 0))
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_beta_target_certificate(
                (151, 338),
                (-9, 40),
                4,
                (1, 1),
            )
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_beta_determinant_target_certificate(
                (151, 338),
                (-9, 40),
                4,
                (1, 1),
            )
        with self.assertRaises(ValueError):
            parallel_direction_squareclass_beta_quadratic_certificate(
                (151, 338),
                (-9, 40),
                4,
                (1, 1),
            )

        searched = parallel_direction_certificate((39, 64), (3, 4))
        self.assertIsNotNone(searched)
        self.assertEqual(searched.target, (39, 64))
        self.assertTrue(searched.valid())

        certificate = parallel_direction_factor_certificate((6, 101), (3, 4), 27)
        self.assertIsNotNone(certificate)
        self.assertEqual(certificate.midpoint, (222, 296))
        self.assertTrue(certificate.valid())
        self.assertEqual(
            parallel_direction_factor_congruence_data((6, 101), (3, 4), 27),
            (279, 291, 74),
        )
        self.assertEqual(
            parallel_direction_factor_pair_row_from_congruence_data(
                (6, 101),
                (3, 4),
                27,
            ),
            (279, 2883, 1428, 1455, 291, 74),
        )

        modulus = parallel_direction_factor_modulus((3, 4), 27)
        shifted_target = (6 + 2 * modulus, 101 - modulus)
        self.assertIsNotNone(
            parallel_direction_factor_coefficient(shifted_target, (3, 4), 27)
        )
        shifted_certificate = parallel_direction_factor_certificate(
            shifted_target,
            (3, 4),
            27,
        )
        self.assertIsNotNone(shifted_certificate)
        self.assertEqual(shifted_certificate.target, shifted_target)
        self.assertTrue(shifted_certificate.valid())

        large_fallback_target = (
            6 + (1 << 63) * modulus,
            101 - (1 << 63) * modulus,
        )
        large_fallback_row = parallel_direction_factor_pair_row_from_congruence_data(
            large_fallback_target,
            (3, 4),
            27,
        )
        self.assertIsNotNone(large_fallback_row)
        (
            determinant_leg,
            paired_factor,
            other_leg,
            scaled_hypotenuse,
            second_length,
            first_coefficient,
        ) = large_fallback_row
        self.assertEqual(determinant_leg * determinant_leg, 27 * paired_factor)
        self.assertEqual(paired_factor - 27, 2 * other_leg)
        self.assertEqual(27 + paired_factor, 2 * scaled_hypotenuse)
        self.assertEqual(
            (determinant_leg, second_length, first_coefficient),
            parallel_direction_factor_congruence_data(
                large_fallback_target,
                (3, 4),
                27,
            ),
        )

        self.assertIsNone(parallel_direction_factor_certificate((39, 64), (3, 4), 5))
        self.assertIsNone(parallel_direction_factor_congruence_data((39, 64), (3, 4), 5))
        self.assertIsNone(
            parallel_direction_factor_pair_row_from_congruence_data(
                (39, 64),
                (3, 4),
                5,
            )
        )
        self.assertIsNone(parallel_direction_certificate((6, 8), (3, 4)))
        self.assertIsNone(parallel_direction_witness((6, 8), (3, 4)))
        with self.assertRaises(ValueError):
            parallel_direction_factor_certificate((39, 64), (1, 1), 1)
        with self.assertRaises(ValueError):
            parallel_direction_factor_certificate((39, 64), (3, 4), 0)
        with self.assertRaises(ValueError):
            parallel_direction_factor_modulus((1, 1), 1)
        with self.assertRaises(ValueError):
            parallel_direction_factor_coefficient((39, 64), (3, 4), 0)
        with self.assertRaises(ValueError):
            parallel_direction_factor_congruence_data((39, 64), (1, 1), 1)
        with self.assertRaises(ValueError):
            parallel_direction_factor_congruence_data((39, 64), (3, 4), 0)
        with self.assertRaises(ValueError):
            parallel_direction_factor_pair_row_from_congruence_data((39, 64), (1, 1), 1)
        with self.assertRaises(ValueError):
            parallel_direction_factor_pair_row_from_congruence_data((39, 64), (3, 4), 0)
        with self.assertRaises(ValueError):
            parallel_direction_witness((39, 64), (1, 1))

    def test_parallel_direction_standard_completion_family(self):
        self.assertEqual(standard_pythagorean_completion_factors(0), ())
        self.assertEqual(standard_pythagorean_completion_factors(5), (1, 25))
        self.assertEqual(standard_pythagorean_completion_factors(-6), (2, 18))
        self.assertEqual(standard_pythagorean_completion_factors(2), (2,))

        examples = (
            ((1, 5), (-4, -3), (-20, -15)),
            ((1, 14), (-4, -3), (232, 174)),
            ((5, 17), (-4, -3), (236, 177)),
            ((4, 13), (-4, 3), (160, -120)),
        )
        for target, direction, midpoint in examples:
            witness = parallel_direction_standard_completion_witness(
                target,
                direction,
            )
            self.assertIsNotNone(witness, (target, direction))
            branch = parallel_direction_standard_completion_branch(
                witness.determinant_leg,
                witness.factor,
            )
            self.assertIn(branch, (0, 1))
            self.assertIsNotNone(
                parallel_direction_standard_completion_quadratic_row_witness(
                    target,
                    direction,
                    branch,
                )
            )
            certificate = parallel_direction_standard_completion_certificate(
                target,
                direction,
            )
            self.assertIsNotNone(certificate, (target, direction))
            self.assertEqual(certificate.midpoint, midpoint)
            self.assertTrue(certificate.valid())

        self.assertIn(
            (31, 142, 676),
            parallel_direction_standard_completion_determinant_rows((-12, 5), 1)[1],
        )
        self.assertGreater(
            len(parallel_direction_standard_completion_quadratic_rows((-12, 5), 1)[1]),
            len(parallel_direction_standard_completion_determinant_rows((-12, 5), 1)[1]),
        )
        self.assertEqual(
            parallel_direction_standard_completion_quadratic_row_witness(
                (29, 98),
                (-12, 5),
                1,
            ),
            (31, 142, 676),
        )
        self.assertEqual(
            parallel_direction_standard_completion_quadratic_row_witness(
                (98, 29),
                (-5, 12),
                0,
            ),
            (31, 27, 676),
        )
        self.assertEqual(
            parallel_direction_standard_completion_strip_intersection_linear_row_witness(
                (29, 98),
                (-5, 12),
                13,
                7,
                (-12, 5),
                1,
            ),
            (31, 2, 13, 52),
        )
        self.assertEqual(
            parallel_direction_standard_completion_strip_intersection_linear_rows(
                (-5, 12),
                13,
                7,
                (-12, 5),
                1,
            )[0],
            676,
        )
        self.assertEqual(
            len(
                parallel_direction_standard_completion_strip_intersection_linear_rows(
                    (-5, 12),
                    13,
                    7,
                    (-12, 5),
                    1,
                )[1]
            ),
            52,
        )
        self.assertIsNone(
            parallel_direction_standard_completion_quadratic_row_witness(
                (1, 8),
                (-4, -3),
                0,
            )
        )
        self.assertIsNone(
            parallel_direction_standard_completion_certificate((1, 8), (-4, -3))
        )
        with self.assertRaises(ValueError):
            parallel_direction_standard_completion_certificate((1, 5), (1, 1))

    def test_parallel_direction_standard_completion_cover_probe(self):
        for target in ((1, 5), (1, 14), (5, 17), (4, 13), (39, 64)):
            certificate = parallel_direction_standard_completion_cover_certificate(
                target,
                8,
            )
            self.assertIsNotNone(certificate, target)
            self.assertEqual(certificate.target, target)
            self.assertTrue(certificate.valid())
            self.assertIsNotNone(
                parallel_direction_standard_completion_cover_witness(target, 8),
                target,
            )

        nonstandard_target = (1, 92)
        self.assertIsNone(
            parallel_direction_standard_completion_cover_certificate(
                nonstandard_target,
                8,
            )
        )
        witness = parallel_direction_factor_witness(nonstandard_target, (4, 3), 5)
        self.assertIsNotNone(witness)
        self.assertEqual(witness.first_coefficient, 544)
        self.assertTrue(witness.certificate.valid())

        certificate = parallel_direction_cover_certificate(nonstandard_target, 8)
        self.assertIsNotNone(certificate)
        self.assertEqual(certificate.midpoint, (2176, 1632))
        self.assertTrue(certificate.valid())
        cover_witness = parallel_direction_cover_witness(nonstandard_target, 8)
        self.assertIsNotNone(cover_witness)
        self.assertEqual(cover_witness.direction, (-4, -3))
        self.assertEqual(cover_witness.factor, 26645)
        self.assertEqual(cover_witness.midpoint, (2176, 1632))
        self.assertEqual(cover_witness.certificate, certificate)

        with self.assertRaises(ValueError):
            parallel_direction_standard_completion_cover_certificate((1, 5), 1)
        with self.assertRaises(ValueError):
            parallel_direction_cover_witness((1, 5), 1)

    def test_unit_coordinate_factor_five_parallel_family(self):
        for parameter_t in range(-20, 21):
            target = (1, 25 * parameter_t + 17)
            first_coefficient = 40 * parameter_t * parameter_t + 55 * parameter_t + 19
            certificate = unit_coordinate_factor_five_parallel_certificate(parameter_t)
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (4 * first_coefficient, 3 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (4, 3), 5),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = unit_coordinate_factor_five_parallel_orbit_certificate(
                    orbit_target
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        self.assertIsNone(unit_coordinate_factor_five_parallel_orbit_certificate((1, 16)))

    def test_unit_coordinate_factor_four_parallel_family(self):
        for parameter_t in range(-20, 21):
            target = (1, 20 * parameter_t + 12)
            first_coefficient = 18 * parameter_t * parameter_t + 16 * parameter_t + 3
            certificate = unit_coordinate_factor_four_parallel_certificate(parameter_t)
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (-3 * first_coefficient, -4 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (-3, -4), 4),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = unit_coordinate_factor_four_parallel_orbit_certificate(
                    orbit_target
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        self.assertIsNone(unit_coordinate_factor_four_parallel_orbit_certificate((1, 11)))

    def test_unit_coordinate_one_mod_five_parallel_family(self):
        for parameter_t in range(-30, 31):
            target = (1, 5 * parameter_t + 1)
            first_coefficient = 8 * parameter_t * parameter_t + 5 * parameter_t + 1
            certificate = unit_coordinate_one_mod_five_parallel_certificate(parameter_t)
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (4 * first_coefficient, -3 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (4, -3), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_one_mod_five_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        self.assertIsNone(
            unit_coordinate_one_mod_five_parallel_orbit_certificate((1, 2))
        )

    def test_unit_coordinate_seven_mod_ten_parallel_family(self):
        for parameter_t in range(-30, 31):
            target = (1, 10 * parameter_t + 7)
            first_coefficient = 18 * parameter_t * parameter_t + 22 * parameter_t + 7
            certificate = unit_coordinate_seven_mod_ten_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (3 * first_coefficient, 4 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (3, 4), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_seven_mod_ten_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        self.assertIsNone(
            unit_coordinate_seven_mod_ten_parallel_orbit_certificate((1, 2))
        )

    def test_unit_coordinate_factor_twenty_five_parallel_family(self):
        for parameter_t in range(-30, 31):
            target = (1, 25 * parameter_t + 18)
            first_coefficient = 8 * parameter_t * parameter_t + 9 * parameter_t + 2
            certificate = unit_coordinate_factor_twenty_five_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (4 * first_coefficient, -3 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (4, -3), 25),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_factor_twenty_five_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        self.assertIsNone(
            unit_coordinate_factor_twenty_five_parallel_orbit_certificate((1, 2))
        )

    def test_unit_coordinate_twenty_two_mod_twenty_five_parallel_family(self):
        for parameter_t in range(-20, 21):
            target = (1, 25 * parameter_t + 22)
            certificate = (
                unit_coordinate_twenty_two_mod_twenty_five_parallel_certificate(
                    parameter_t
                )
            )
            if parameter_t == -1:
                self.assertIsNone(certificate)
                self.assertIsNone(
                    parallel_direction_factor_certificate(target, (-4, -3), 5)
                )
                orbit_certificate = (
                    unit_coordinate_twenty_two_mod_twenty_five_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, target)
                self.assertTrue(orbit_certificate.valid())
                for orbit_target in sign_swap_orbit(target):
                    orbit_certificate = (
                        unit_coordinate_twenty_two_mod_twenty_five_parallel_orbit_certificate(
                            orbit_target
                        )
                    )
                    self.assertIsNotNone(orbit_certificate)
                    self.assertEqual(orbit_certificate.target, orbit_target)
                    self.assertTrue(orbit_certificate.valid())
                continue

            first_coefficient = (
                40 * parameter_t * parameter_t + 65 * parameter_t + 26
            )
            self.assertIsNotNone(certificate)
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (-4 * first_coefficient, -3 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (-4, -3), 5),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_twenty_two_mod_twenty_five_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        self.assertIsNone(
            unit_coordinate_twenty_two_mod_twenty_five_parallel_orbit_certificate(
                (1, 18)
            )
        )

    def test_unit_coordinate_promoted_mod_hundred_cover(self):
        self.assertEqual(
            UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES,
            frozenset({2, 38, 62, 98}),
        )

        for other_coordinate in range(-300, 301):
            target = (1, other_coordinate)
            certificate = unit_coordinate_promoted_mod_hundred_certificate(target)
            if (
                other_coordinate == 0
                or other_coordinate % 100
                in UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES
            ):
                self.assertIsNone(certificate, target)
                continue

            self.assertIsNotNone(certificate, target)
            self.assertEqual(certificate.target, target)
            self.assertTrue(certificate.valid())
            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = unit_coordinate_promoted_mod_hundred_certificate(
                    orbit_target
                )
                self.assertIsNotNone(orbit_certificate, orbit_target)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue in range(100):
            if residue == 0:
                target = (1, 100)
            else:
                target = (1, residue)
            certificate = unit_coordinate_promoted_mod_hundred_certificate(target)
            if residue in UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES:
                self.assertIsNone(certificate, residue)
            else:
                self.assertIsNotNone(certificate, residue)
                self.assertTrue(certificate.valid())

        self.assertIsNone(unit_coordinate_promoted_mod_hundred_certificate((2, 3)))

    def test_unit_coordinate_residual_orthogonal_seed_rows(self):
        self.assertEqual(
            UNIT_COORDINATE_RESIDUAL_ORTHOGONAL_SEED_ROWS,
            (
                (2, 22_002, 28_900, (8, 15, 17)),
                (38, 38, 28_900, (8, 15, 17)),
                (62, 4_662, 28_900, (8, 15, 17)),
                (98, 11_598, 28_900, (8, 15, 17)),
            ),
        )
        self.assertEqual(
            {residue for residue, _base, _period, _triple in (
                UNIT_COORDINATE_RESIDUAL_ORTHOGONAL_SEED_ROWS
            )},
            UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES,
        )

        for residue, base, period, triple_data in (
            UNIT_COORDINATE_RESIDUAL_ORTHOGONAL_SEED_ROWS
        ):
            triple = PythagoreanTriple(*triple_data)
            self.assertTrue(triple.valid())
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 100 * triple.hypotenuse * triple.hypotenuse)

            for parameter_t in range(-2, 3):
                target = (1, base + period * parameter_t)
                self.assertIsNone(unit_coordinate_promoted_mod_hundred_certificate(target))
                certificate = unit_coordinate_residual_orthogonal_seed_certificate(target)
                explicit = pythagorean_triple_orthogonal_lattice_certificate(
                    target,
                    triple,
                )
                self.assertEqual(certificate, explicit)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

                for orbit_target in sign_swap_orbit(target):
                    orbit_certificate = unit_coordinate_residual_orthogonal_seed_certificate(
                        orbit_target
                    )
                    self.assertIsNotNone(orbit_certificate)
                    self.assertEqual(orbit_certificate.target, orbit_target)
                    self.assertTrue(orbit_certificate.valid())

        self.assertEqual(
            unit_coordinate_residual_orthogonal_seed_certificate((1, 38)).midpoint,
            (16, 30),
        )
        self.assertIsNone(
            unit_coordinate_residual_orthogonal_seed_certificate((1, 138))
        )
        self.assertIsNone(
            unit_coordinate_residual_orthogonal_seed_certificate((2, 3))
        )

    def test_unit_coordinate_twelve_thirty_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((-12, -35), 1),
            tuple(range(25, 2_738, 37)),
        )
        self.assertEqual(
            UNIT_COORDINATE_TWELVE_THIRTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 802, 3_700),
                (38, 1_838, 3_700),
                (62, 62, 3_700),
                (98, 1_098, 3_700),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 37 * parameter_t + 25
            first_coefficient = (
                72 * parameter_t * parameter_t + 85 * parameter_t + 25
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_twelve_thirty_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (-12 * first_coefficient, -35 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (-12, -35), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_twelve_thirty_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_TWELVE_THIRTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 3_700)
            self.assertEqual((base - 25) % 37, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_twelve_thirty_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_twelve_thirty_five_factor_one_parallel_orbit_certificate(
                (1, -12)
            )
        )
        self.assertIsNone(
            unit_coordinate_twelve_thirty_five_factor_one_parallel_orbit_certificate(
                (1, 24)
            )
        )
        self.assertIsNone(
            unit_coordinate_twelve_thirty_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_forty_nine_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((40, 9), 1),
            tuple(range(23, 3_362, 41)),
        )
        self.assertEqual(
            UNIT_COORDINATE_FORTY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 802, 4_100),
                (38, 638, 4_100),
                (62, 3_262, 4_100),
                (98, 3_098, 4_100),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 41 * parameter_t + 23
            first_coefficient = (
                800 * parameter_t * parameter_t + 889 * parameter_t + 247
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_forty_nine_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (40 * first_coefficient, 9 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (40, 9), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_forty_nine_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_FORTY_NINE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 4_100)
            self.assertEqual((base - 23) % 41, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_forty_nine_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_forty_nine_factor_one_parallel_orbit_certificate(
                (1, -18)
            )
        )
        self.assertIsNone(
            unit_coordinate_forty_nine_factor_one_parallel_orbit_certificate(
                (1, 22)
            )
        )
        self.assertIsNone(
            unit_coordinate_forty_nine_factor_one_parallel_orbit_certificate((2, 3))
        )

    def test_unit_coordinate_twenty_eight_forty_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((28, 45), 1),
            tuple(range(10, 5_618, 53)),
        )
        self.assertEqual(
            UNIT_COORDINATE_TWENTY_EIGHT_FORTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 3_402, 5_300),
                (38, 4_038, 5_300),
                (62, 4_462, 5_300),
                (98, 5_098, 5_300),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 53 * parameter_t + 10
            first_coefficient = (
                392 * parameter_t * parameter_t + 125 * parameter_t + 10
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_twenty_eight_forty_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (28 * first_coefficient, 45 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (28, 45), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_twenty_eight_forty_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_TWENTY_EIGHT_FORTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 5_300)
            self.assertEqual((base - 10) % 53, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_twenty_eight_forty_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_twenty_eight_forty_five_factor_one_parallel_orbit_certificate(
                (1, -43)
            )
        )
        self.assertIsNone(
            unit_coordinate_twenty_eight_forty_five_factor_one_parallel_orbit_certificate(
                (1, 9)
            )
        )
        self.assertIsNone(
            unit_coordinate_twenty_eight_forty_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_sixty_eleven_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((60, 11), 1),
            tuple(range(39, 7_442, 61)),
        )
        self.assertEqual(
            UNIT_COORDINATE_SIXTY_ELEVEN_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 5_102, 6_100),
                (38, 3_638, 6_100),
                (62, 2_662, 6_100),
                (98, 1_198, 6_100),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 61 * parameter_t + 39
            first_coefficient = (
                1800 * parameter_t * parameter_t + 2291 * parameter_t + 729
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_sixty_eleven_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (60 * first_coefficient, 11 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (60, 11), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_sixty_eleven_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in UNIT_COORDINATE_SIXTY_ELEVEN_FACTOR_ONE_RESIDUAL_ROWS:
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 6_100)
            self.assertEqual((base - 39) % 61, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_sixty_eleven_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_sixty_eleven_factor_one_parallel_orbit_certificate(
                (1, -22)
            )
        )
        self.assertIsNone(
            unit_coordinate_sixty_eleven_factor_one_parallel_orbit_certificate(
                (1, 38)
            )
        )
        self.assertIsNone(
            unit_coordinate_sixty_eleven_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_forty_eight_fifty_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((48, 55), 1),
            tuple(range(31, 10_658, 73)),
        )
        self.assertEqual(
            UNIT_COORDINATE_FORTY_EIGHT_FIFTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 2_002, 7_300),
                (38, 4_338, 7_300),
                (62, 3_462, 7_300),
                (98, 5_798, 7_300),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 73 * parameter_t + 31
            first_coefficient = (
                1152 * parameter_t * parameter_t + 943 * parameter_t + 193
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_forty_eight_fifty_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (48 * first_coefficient, 55 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (48, 55), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_forty_eight_fifty_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_FORTY_EIGHT_FIFTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 7_300)
            self.assertEqual((base - 31) % 73, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_forty_eight_fifty_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_forty_eight_fifty_five_factor_one_parallel_orbit_certificate(
                (1, -42)
            )
        )
        self.assertIsNone(
            unit_coordinate_forty_eight_fifty_five_factor_one_parallel_orbit_certificate(
                (1, 30)
            )
        )
        self.assertIsNone(
            unit_coordinate_forty_eight_fifty_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_eighty_thirty_nine_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((80, 39), 1),
            tuple(range(71, 15_842, 89)),
        )
        self.assertEqual(
            UNIT_COORDINATE_EIGHTY_THIRTY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 7_102, 8_900),
                (38, 338, 8_900),
                (62, 1_762, 8_900),
                (98, 3_898, 8_900),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 89 * parameter_t + 71
            first_coefficient = (
                3200 * parameter_t * parameter_t + 5071 * parameter_t + 2009
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_eighty_thirty_nine_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (80 * first_coefficient, 39 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (80, 39), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_eighty_thirty_nine_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_EIGHTY_THIRTY_NINE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 8_900)
            self.assertEqual((base - 71) % 89, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_eighty_thirty_nine_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_eighty_thirty_nine_factor_one_parallel_orbit_certificate(
                (1, -18)
            )
        )
        self.assertIsNone(
            unit_coordinate_eighty_thirty_nine_factor_one_parallel_orbit_certificate(
                (1, 70)
            )
        )
        self.assertIsNone(
            unit_coordinate_eighty_thirty_nine_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_seventy_two_sixty_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((72, 65), 1),
            tuple(range(78, 18_818, 97)),
        )
        self.assertEqual(
            UNIT_COORDINATE_SEVENTY_TWO_SIXTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 9_002, 9_700),
                (38, 7_838, 9_700),
                (62, 7_062, 9_700),
                (98, 5_898, 9_700),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 97 * parameter_t + 78
            first_coefficient = (
                2592 * parameter_t * parameter_t + 4121 * parameter_t + 1638
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_seventy_two_sixty_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (72 * first_coefficient, 65 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (72, 65), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_seventy_two_sixty_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_SEVENTY_TWO_SIXTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 9_700)
            self.assertEqual((base - 78) % 97, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_seventy_two_sixty_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_seventy_two_sixty_five_factor_one_parallel_orbit_certificate(
                (1, -19)
            )
        )
        self.assertIsNone(
            unit_coordinate_seventy_two_sixty_five_factor_one_parallel_orbit_certificate(
                (1, 77)
            )
        )
        self.assertIsNone(
            unit_coordinate_seventy_two_sixty_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_twenty_ninety_nine_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((20, 99), 1),
            tuple(range(60, 20_402, 101)),
        )
        self.assertEqual(
            UNIT_COORDINATE_TWENTY_NINETY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 4_302, 10_100),
                (38, 7_938, 10_100),
                (62, 262, 10_100),
                (98, 3_898, 10_100),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 101 * parameter_t + 60
            first_coefficient = 200 * parameter_t * parameter_t + 219 * parameter_t + 60
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_twenty_ninety_nine_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (20 * first_coefficient, 99 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (20, 99), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_twenty_ninety_nine_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_TWENTY_NINETY_NINE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 10_100)
            self.assertEqual((base - 60) % 101, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_twenty_ninety_nine_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_twenty_ninety_nine_factor_one_parallel_orbit_certificate(
                (1, -41)
            )
        )
        self.assertIsNone(
            unit_coordinate_twenty_ninety_nine_factor_one_parallel_orbit_certificate(
                (1, 59)
            )
        )
        self.assertIsNone(
            unit_coordinate_twenty_ninety_nine_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_sixty_ninety_one_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((60, 91), 1),
            tuple(range(82, 23_844, 109)),
        )
        self.assertEqual(
            UNIT_COORDINATE_SIXTY_NINETY_ONE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 8_802, 10_900),
                (38, 9_238, 10_900),
                (62, 2_262, 10_900),
                (98, 2_698, 10_900),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 109 * parameter_t + 82
            first_coefficient = (
                1800 * parameter_t * parameter_t + 2659 * parameter_t + 982
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_sixty_ninety_one_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (60 * first_coefficient, 91 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (60, 91), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_sixty_ninety_one_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_SIXTY_NINETY_ONE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 10_900)
            self.assertEqual((base - 82) % 109, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_sixty_ninety_one_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_sixty_ninety_one_factor_one_parallel_orbit_certificate(
                (1, -27)
            )
        )
        self.assertIsNone(
            unit_coordinate_sixty_ninety_one_factor_one_parallel_orbit_certificate(
                (1, 81)
            )
        )
        self.assertIsNone(
            unit_coordinate_sixty_ninety_one_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_one_hundred_twelve_fifteen_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((112, 15), 1),
            tuple(range(83, 25_538, 113)),
        )
        self.assertEqual(
            UNIT_COORDINATE_ONE_HUNDRED_TWELVE_FIFTEEN_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 7_202, 11_300),
                (38, 4_038, 11_300),
                (62, 9_462, 11_300),
                (98, 6_298, 11_300),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 113 * parameter_t + 83
            first_coefficient = (
                6272 * parameter_t * parameter_t + 9199 * parameter_t + 3373
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_one_hundred_twelve_fifteen_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (112 * first_coefficient, 15 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (112, 15), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_one_hundred_twelve_fifteen_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_ONE_HUNDRED_TWELVE_FIFTEEN_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 11_300)
            self.assertEqual((base - 83) % 113, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_one_hundred_twelve_fifteen_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_one_hundred_twelve_fifteen_factor_one_parallel_orbit_certificate(
                (1, -30)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_twelve_fifteen_factor_one_parallel_orbit_certificate(
                (1, 82)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_twelve_fifteen_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_eighty_eight_one_hundred_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((88, 105), 1),
            tuple(range(7, 37_545, 137)),
        )
        self.assertEqual(
            UNIT_COORDINATE_EIGHTY_EIGHT_ONE_HUNDRED_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 4_802, 13_700),
                (38, 8_638, 13_700),
                (62, 2_062, 13_700),
                (98, 5_898, 13_700),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 137 * parameter_t + 7
            first_coefficient = (
                3872 * parameter_t * parameter_t + 329 * parameter_t + 7
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_eighty_eight_one_hundred_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (88 * first_coefficient, 105 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (88, 105), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_eighty_eight_one_hundred_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_EIGHTY_EIGHT_ONE_HUNDRED_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 13_700)
            self.assertEqual((base - 7) % 137, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_eighty_eight_one_hundred_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_eighty_eight_one_hundred_five_factor_one_parallel_orbit_certificate(
                (1, -130)
            )
        )
        self.assertIsNone(
            unit_coordinate_eighty_eight_one_hundred_five_factor_one_parallel_orbit_certificate(
                (1, 6)
            )
        )
        self.assertIsNone(
            unit_coordinate_eighty_eight_one_hundred_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_one_hundred_forty_fifty_one_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((140, 51), 1),
            tuple(range(82, 44_484, 149)),
        )
        self.assertEqual(
            UNIT_COORDINATE_ONE_HUNDRED_FORTY_FIFTY_ONE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 12_002, 14_900),
                (38, 6_638, 14_900),
                (62, 3_062, 14_900),
                (98, 12_598, 14_900),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 149 * parameter_t + 82
            first_coefficient = (
                9800 * parameter_t * parameter_t + 10739 * parameter_t + 2942
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_one_hundred_forty_fifty_one_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (140 * first_coefficient, 51 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (140, 51), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_one_hundred_forty_fifty_one_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_ONE_HUNDRED_FORTY_FIFTY_ONE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 14_900)
            self.assertEqual((base - 82) % 149, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_one_hundred_forty_fifty_one_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_one_hundred_forty_fifty_one_factor_one_parallel_orbit_certificate(
                (1, -67)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_forty_fifty_one_factor_one_parallel_orbit_certificate(
                (1, 81)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_forty_fifty_one_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_one_hundred_thirty_two_eighty_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((132, 85), 1),
            tuple(range(4, 49_302, 157)),
        )
        self.assertEqual(
            UNIT_COORDINATE_ONE_HUNDRED_THIRTY_TWO_EIGHTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 2_202, 15_700),
                (38, 9_738, 15_700),
                (62, 14_762, 15_700),
                (98, 6_598, 15_700),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 157 * parameter_t + 4
            first_coefficient = (
                8712 * parameter_t * parameter_t + 373 * parameter_t + 4
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_one_hundred_thirty_two_eighty_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (132 * first_coefficient, 85 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (132, 85), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_one_hundred_thirty_two_eighty_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_ONE_HUNDRED_THIRTY_TWO_EIGHTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 15_700)
            self.assertEqual((base - 4) % 157, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_one_hundred_thirty_two_eighty_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_one_hundred_thirty_two_eighty_five_factor_one_parallel_orbit_certificate(
                (1, -153)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_thirty_two_eighty_five_factor_one_parallel_orbit_certificate(
                (1, 3)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_thirty_two_eighty_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_one_hundred_twenty_one_hundred_nineteen_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((120, 119), 1),
            tuple(range(168, 57_290, 169)),
        )
        self.assertEqual(
            UNIT_COORDINATE_ONE_HUNDRED_TWENTY_ONE_HUNDRED_NINETEEN_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 14_702, 16_900),
                (38, 5_238, 16_900),
                (62, 4_562, 16_900),
                (98, 11_998, 16_900),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 169 * parameter_t + 168
            first_coefficient = (
                7200 * parameter_t * parameter_t + 14231 * parameter_t + 7032
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_one_hundred_twenty_one_hundred_nineteen_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (120 * first_coefficient, 119 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (120, 119), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_one_hundred_twenty_one_hundred_nineteen_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_ONE_HUNDRED_TWENTY_ONE_HUNDRED_NINETEEN_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 16_900)
            self.assertEqual((base - 168) % 169, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_one_hundred_twenty_one_hundred_nineteen_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_one_hundred_twenty_one_hundred_nineteen_factor_one_parallel_orbit_certificate(
                (1, -1)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_twenty_one_hundred_nineteen_factor_one_parallel_orbit_certificate(
                (1, 167)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_twenty_one_hundred_nineteen_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_fifty_two_one_hundred_sixty_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((52, 165), 1),
            tuple(range(28, 59_886, 173)),
        )
        self.assertEqual(
            UNIT_COORDINATE_FIFTY_TWO_ONE_HUNDRED_SIXTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 6_602, 17_300),
                (38, 12_138, 17_300),
                (62, 10_062, 17_300),
                (98, 15_598, 17_300),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 173 * parameter_t + 28
            first_coefficient = (
                1352 * parameter_t * parameter_t + 389 * parameter_t + 28
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_fifty_two_one_hundred_sixty_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (52 * first_coefficient, 165 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (52, 165), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_fifty_two_one_hundred_sixty_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_FIFTY_TWO_ONE_HUNDRED_SIXTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 17_300)
            self.assertEqual((base - 28) % 173, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_fifty_two_one_hundred_sixty_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_fifty_two_one_hundred_sixty_five_factor_one_parallel_orbit_certificate(
                (1, -145)
            )
        )
        self.assertIsNone(
            unit_coordinate_fifty_two_one_hundred_sixty_five_factor_one_parallel_orbit_certificate(
                (1, 27)
            )
        )
        self.assertIsNone(
            unit_coordinate_fifty_two_one_hundred_sixty_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_one_hundred_eighty_nineteen_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((180, 19), 1),
            tuple(range(143, 65_665, 181)),
        )
        self.assertEqual(
            UNIT_COORDINATE_ONE_HUNDRED_EIGHTY_NINETEEN_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 7_202, 18_100),
                (38, 17_338, 18_100),
                (62, 18_062, 18_100),
                (98, 10_098, 18_100),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 181 * parameter_t + 143
            first_coefficient = (
                16200 * parameter_t * parameter_t + 25579 * parameter_t + 10097
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_one_hundred_eighty_nineteen_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (180 * first_coefficient, 19 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (180, 19), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_one_hundred_eighty_nineteen_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_ONE_HUNDRED_EIGHTY_NINETEEN_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 18_100)
            self.assertEqual((base - 143) % 181, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_one_hundred_eighty_nineteen_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_one_hundred_eighty_nineteen_factor_one_parallel_orbit_certificate(
                (1, -38)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_eighty_nineteen_factor_one_parallel_orbit_certificate(
                (1, 142)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_eighty_nineteen_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_one_hundred_sixty_eight_ninety_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((168, 95), 1),
            tuple(range(47, 74_545, 193)),
        )
        self.assertEqual(
            UNIT_COORDINATE_ONE_HUNDRED_SIXTY_EIGHT_NINETY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 6_802, 19_300),
                (38, 16_838, 19_300),
                (62, 10_662, 19_300),
                (98, 1_398, 19_300),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 193 * parameter_t + 47
            first_coefficient = (
                14112 * parameter_t * parameter_t + 6791 * parameter_t + 817
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_one_hundred_sixty_eight_ninety_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (168 * first_coefficient, 95 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (168, 95), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_one_hundred_sixty_eight_ninety_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_ONE_HUNDRED_SIXTY_EIGHT_NINETY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 19_300)
            self.assertEqual((base - 47) % 193, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_one_hundred_sixty_eight_ninety_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_one_hundred_sixty_eight_ninety_five_factor_one_parallel_orbit_certificate(
                (1, -146)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_sixty_eight_ninety_five_factor_one_parallel_orbit_certificate(
                (1, 46)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_sixty_eight_ninety_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_twenty_eight_one_hundred_ninety_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((28, 195), 1),
            tuple(range(112, 77_730, 197)),
        )
        self.assertEqual(
            UNIT_COORDINATE_TWENTY_EIGHT_ONE_HUNDRED_NINETY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 13_902, 19_700),
                (38, 11_538, 19_700),
                (62, 9_962, 19_700),
                (98, 7_598, 19_700),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 197 * parameter_t + 112
            first_coefficient = (
                392 * parameter_t * parameter_t + 419 * parameter_t + 112
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_twenty_eight_one_hundred_ninety_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (28 * first_coefficient, 195 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (28, 195), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_twenty_eight_one_hundred_ninety_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_TWENTY_EIGHT_ONE_HUNDRED_NINETY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 19_700)
            self.assertEqual((base - 112) % 197, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_twenty_eight_one_hundred_ninety_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_twenty_eight_one_hundred_ninety_five_factor_one_parallel_orbit_certificate(
                (1, -85)
            )
        )
        self.assertIsNone(
            unit_coordinate_twenty_eight_one_hundred_ninety_five_factor_one_parallel_orbit_certificate(
                (1, 111)
            )
        )
        self.assertIsNone(
            unit_coordinate_twenty_eight_one_hundred_ninety_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_sixty_two_hundred_twenty_one_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((60, 221), 1),
            tuple(range(36, 104_918, 229)),
        )
        self.assertEqual(
            UNIT_COORDINATE_SIXTY_TWO_HUNDRED_TWENTY_ONE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 12_402, 22_900),
                (38, 8_738, 22_900),
                (62, 21_562, 22_900),
                (98, 17_898, 22_900),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 229 * parameter_t + 36
            first_coefficient = (
                1800 * parameter_t * parameter_t + 509 * parameter_t + 36
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_sixty_two_hundred_twenty_one_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (60 * first_coefficient, 221 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (60, 221), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_sixty_two_hundred_twenty_one_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_SIXTY_TWO_HUNDRED_TWENTY_ONE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 22_900)
            self.assertEqual((base - 36) % 229, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_sixty_two_hundred_twenty_one_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_sixty_two_hundred_twenty_one_factor_one_parallel_orbit_certificate(
                (1, -193)
            )
        )
        self.assertIsNone(
            unit_coordinate_sixty_two_hundred_twenty_one_factor_one_parallel_orbit_certificate(
                (1, 35)
            )
        )
        self.assertIsNone(
            unit_coordinate_sixty_two_hundred_twenty_one_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_three_hundred_twelve_twenty_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((312, 25), 1),
            tuple(range(263, 196_201, 313)),
        )
        self.assertEqual(
            UNIT_COORDINATE_THREE_HUNDRED_TWELVE_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 1_202, 31_300),
                (38, 23_738, 31_300),
                (62, 7_462, 31_300),
                (98, 29_998, 31_300),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 313 * parameter_t + 263
            first_coefficient = (
                48672 * parameter_t * parameter_t + 81769 * parameter_t + 34343
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_three_hundred_twelve_twenty_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (312 * first_coefficient, 25 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (312, 25), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_three_hundred_twelve_twenty_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_THREE_HUNDRED_TWELVE_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 31_300)
            self.assertEqual((base - 263) % 313, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_three_hundred_twelve_twenty_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_three_hundred_twelve_twenty_five_factor_one_parallel_orbit_certificate(
                (1, -50)
            )
        )
        self.assertIsNone(
            unit_coordinate_three_hundred_twelve_twenty_five_factor_one_parallel_orbit_certificate(
                (1, 262)
            )
        )
        self.assertIsNone(
            unit_coordinate_three_hundred_twelve_twenty_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_three_hundred_eight_seventy_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((308, 75), 1),
            tuple(range(296, 200_958, 317)),
        )
        self.assertEqual(
            UNIT_COORDINATE_THREE_HUNDRED_EIGHT_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 6_002, 31_700),
                (38, 8_538, 31_700),
                (62, 31_362, 31_700),
                (98, 2_198, 31_700),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 317 * parameter_t + 296
            first_coefficient = (
                47432 * parameter_t * parameter_t + 88507 * parameter_t + 41288
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_three_hundred_eight_seventy_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (308 * first_coefficient, 75 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (308, 75), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_three_hundred_eight_seventy_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_THREE_HUNDRED_EIGHT_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 31_700)
            self.assertEqual((base - 296) % 317, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_three_hundred_eight_seventy_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_three_hundred_eight_seventy_five_factor_one_parallel_orbit_certificate(
                (1, -21)
            )
        )
        self.assertIsNone(
            unit_coordinate_three_hundred_eight_seventy_five_factor_one_parallel_orbit_certificate(
                (1, 295)
            )
        )
        self.assertIsNone(
            unit_coordinate_three_hundred_eight_seventy_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_two_hundred_eighty_eight_one_hundred_seventy_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((288, 175), 1),
            tuple(range(241, 227_043, 337)),
        )
        self.assertEqual(
            UNIT_COORDINATE_TWO_HUNDRED_EIGHTY_EIGHT_ONE_HUNDRED_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 18_102, 33_700),
                (38, 27_538, 33_700),
                (62, 11_362, 33_700),
                (98, 20_798, 33_700),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 337 * parameter_t + 241
            first_coefficient = (
                41472 * parameter_t * parameter_t + 59167 * parameter_t + 21103
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_two_hundred_eighty_eight_one_hundred_seventy_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (288 * first_coefficient, 175 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (288, 175), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_two_hundred_eighty_eight_one_hundred_seventy_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_TWO_HUNDRED_EIGHTY_EIGHT_ONE_HUNDRED_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 33_700)
            self.assertEqual((base - 241) % 337, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_two_hundred_eighty_eight_one_hundred_seventy_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_two_hundred_eighty_eight_one_hundred_seventy_five_factor_one_parallel_orbit_certificate(
                (1, -96)
            )
        )
        self.assertIsNone(
            unit_coordinate_two_hundred_eighty_eight_one_hundred_seventy_five_factor_one_parallel_orbit_certificate(
                (1, 240)
            )
        )
        self.assertIsNone(
            unit_coordinate_two_hundred_eighty_eight_one_hundred_seventy_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_one_hundred_eighty_two_hundred_ninety_nine_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((180, 299), 1),
            tuple(range(206, 243_460, 349)),
        )
        self.assertEqual(
            UNIT_COORDINATE_ONE_HUNDRED_EIGHTY_TWO_HUNDRED_NINETY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 1_602, 34_900),
                (38, 23_938, 34_900),
                (62, 15_562, 34_900),
                (98, 2_998, 34_900),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 349 * parameter_t + 206
            first_coefficient = (
                16200 * parameter_t * parameter_t + 18971 * parameter_t + 5554
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_one_hundred_eighty_two_hundred_ninety_nine_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (180 * first_coefficient, 299 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (180, 299), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_one_hundred_eighty_two_hundred_ninety_nine_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_ONE_HUNDRED_EIGHTY_TWO_HUNDRED_NINETY_NINE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 34_900)
            self.assertEqual((base - 206) % 349, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_one_hundred_eighty_two_hundred_ninety_nine_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_one_hundred_eighty_two_hundred_ninety_nine_factor_one_parallel_orbit_certificate(
                (1, -143)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_eighty_two_hundred_ninety_nine_factor_one_parallel_orbit_certificate(
                (1, 205)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_eighty_two_hundred_ninety_nine_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_two_hundred_seventy_two_two_hundred_twenty_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((272, 225), 1),
            tuple(range(49, 248_915, 353)),
        )
        self.assertEqual(
            UNIT_COORDINATE_TWO_HUNDRED_SEVENTY_TWO_TWO_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 402, 35_300),
                (38, 4_638, 35_300),
                (62, 7_462, 35_300),
                (98, 11_698, 35_300),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 353 * parameter_t + 49
            first_coefficient = (
                36992 * parameter_t * parameter_t + 10097 * parameter_t + 689
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_two_hundred_seventy_two_two_hundred_twenty_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (272 * first_coefficient, 225 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (272, 225), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_two_hundred_seventy_two_two_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_TWO_HUNDRED_SEVENTY_TWO_TWO_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 35_300)
            self.assertEqual((base - 49) % 353, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_two_hundred_seventy_two_two_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_two_hundred_seventy_two_two_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                (1, -304)
            )
        )
        self.assertIsNone(
            unit_coordinate_two_hundred_seventy_two_two_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                (1, 48)
            )
        )
        self.assertIsNone(
            unit_coordinate_two_hundred_seventy_two_two_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_two_hundred_fifty_two_two_hundred_seventy_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((252, 275), 1),
            tuple(range(151, 278_037, 373)),
        )
        self.assertEqual(
            UNIT_COORDINATE_TWO_HUNDRED_FIFTY_TWO_TWO_HUNDRED_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 32_602, 37_300),
                (38, 7_238, 37_300),
                (62, 2_762, 37_300),
                (98, 14_698, 37_300),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 373 * parameter_t + 151
            first_coefficient = (
                31752 * parameter_t * parameter_t + 25523 * parameter_t + 5129
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_two_hundred_fifty_two_two_hundred_seventy_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (252 * first_coefficient, 275 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (252, 275), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_two_hundred_fifty_two_two_hundred_seventy_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_TWO_HUNDRED_FIFTY_TWO_TWO_HUNDRED_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 37_300)
            self.assertEqual((base - 151) % 373, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_two_hundred_fifty_two_two_hundred_seventy_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_two_hundred_fifty_two_two_hundred_seventy_five_factor_one_parallel_orbit_certificate(
                (1, -222)
            )
        )
        self.assertIsNone(
            unit_coordinate_two_hundred_fifty_two_two_hundred_seventy_five_factor_one_parallel_orbit_certificate(
                (1, 150)
            )
        )
        self.assertIsNone(
            unit_coordinate_two_hundred_fifty_two_two_hundred_seventy_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_three_hundred_fifty_two_one_hundred_thirty_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((352, 135), 1),
            tuple(range(299, 284_181, 377)),
        )
        self.assertEqual(
            UNIT_COORDINATE_THREE_HUNDRED_FIFTY_TWO_ONE_HUNDRED_THIRTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 15_002, 37_700),
                (38, 2_938, 37_700),
                (62, 7_462, 37_700),
                (98, 33_098, 37_700),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 377 * parameter_t + 299
            first_coefficient = (
                61952 * parameter_t * parameter_t + 98143 * parameter_t + 38869
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_three_hundred_fifty_two_one_hundred_thirty_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (352 * first_coefficient, 135 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (352, 135), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_three_hundred_fifty_two_one_hundred_thirty_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_THREE_HUNDRED_FIFTY_TWO_ONE_HUNDRED_THIRTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 37_700)
            self.assertEqual((base - 299) % 377, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_three_hundred_fifty_two_one_hundred_thirty_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_three_hundred_fifty_two_one_hundred_thirty_five_factor_one_parallel_orbit_certificate(
                (1, -78)
            )
        )
        self.assertIsNone(
            unit_coordinate_three_hundred_fifty_two_one_hundred_thirty_five_factor_one_parallel_orbit_certificate(
                (1, 298)
            )
        )
        self.assertIsNone(
            unit_coordinate_three_hundred_fifty_two_one_hundred_thirty_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_three_hundred_forty_one_hundred_eighty_nine_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((340, 189), 1),
            tuple(range(97, 302_351, 389)),
        )
        self.assertEqual(
            UNIT_COORDINATE_THREE_HUNDRED_FORTY_ONE_HUNDRED_EIGHTY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 17_602, 38_900),
                (38, 26_938, 38_900),
                (62, 33_162, 38_900),
                (98, 3_598, 38_900),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 389 * parameter_t + 97
            first_coefficient = (
                57800 * parameter_t * parameter_t + 28661 * parameter_t + 3553
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_three_hundred_forty_one_hundred_eighty_nine_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (340 * first_coefficient, 189 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (340, 189), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_three_hundred_forty_one_hundred_eighty_nine_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_THREE_HUNDRED_FORTY_ONE_HUNDRED_EIGHTY_NINE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 38_900)
            self.assertEqual((base - 97) % 389, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_three_hundred_forty_one_hundred_eighty_nine_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_three_hundred_forty_one_hundred_eighty_nine_factor_one_parallel_orbit_certificate(
                (1, -292)
            )
        )
        self.assertIsNone(
            unit_coordinate_three_hundred_forty_one_hundred_eighty_nine_factor_one_parallel_orbit_certificate(
                (1, 96)
            )
        )
        self.assertIsNone(
            unit_coordinate_three_hundred_forty_one_hundred_eighty_nine_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_two_hundred_twenty_eight_three_hundred_twenty_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((228, 325), 1),
            tuple(range(141, 314_963, 397)),
        )
        self.assertEqual(
            UNIT_COORDINATE_TWO_HUNDRED_TWENTY_EIGHT_THREE_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 5_302, 39_700),
                (38, 538, 39_700),
                (62, 37_062, 39_700),
                (98, 32_298, 39_700),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 397 * parameter_t + 141
            first_coefficient = (
                25992 * parameter_t * parameter_t + 18277 * parameter_t + 3213
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_two_hundred_twenty_eight_three_hundred_twenty_five_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (228 * first_coefficient, 325 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (228, 325), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_two_hundred_twenty_eight_three_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_TWO_HUNDRED_TWENTY_EIGHT_THREE_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 39_700)
            self.assertEqual((base - 141) % 397, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_two_hundred_twenty_eight_three_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_two_hundred_twenty_eight_three_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                (1, -256)
            )
        )
        self.assertIsNone(
            unit_coordinate_two_hundred_twenty_eight_three_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                (1, 140)
            )
        )
        self.assertIsNone(
            unit_coordinate_two_hundred_twenty_eight_three_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_forty_three_hundred_ninety_nine_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((40, 399), 1),
            tuple(range(220, 321_422, 401)),
        )
        self.assertEqual(
            UNIT_COORDINATE_FORTY_THREE_HUNDRED_NINETY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 33_102, 40_100),
                (38, 7_438, 40_100),
                (62, 17_062, 40_100),
                (98, 31_498, 40_100),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 401 * parameter_t + 220
            first_coefficient = 800 * parameter_t * parameter_t + 839 * parameter_t + 220
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_forty_three_hundred_ninety_nine_factor_one_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (40 * first_coefficient, 399 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (40, 399), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_forty_three_hundred_ninety_nine_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_FORTY_THREE_HUNDRED_NINETY_NINE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 40_100)
            self.assertEqual((base - 220) % 401, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_forty_three_hundred_ninety_nine_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_forty_three_hundred_ninety_nine_factor_one_parallel_orbit_certificate(
                (1, -181)
            )
        )
        self.assertIsNone(
            unit_coordinate_forty_three_hundred_ninety_nine_factor_one_parallel_orbit_certificate(
                (1, 219)
            )
        )
        self.assertIsNone(
            unit_coordinate_forty_three_hundred_ninety_nine_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_one_hundred_twenty_three_hundred_ninety_one_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((120, 391), 1),
            tuple(range(302, 334_456, 409)),
        )
        self.assertEqual(
            UNIT_COORDINATE_ONE_HUNDRED_TWENTY_THREE_HUNDRED_NINETY_ONE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 302, 40_900),
                (38, 1_938, 40_900),
                (62, 16_662, 40_900),
                (98, 18_298, 40_900),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 409 * parameter_t + 302
            first_coefficient = (
                7200 * parameter_t * parameter_t + 10519 * parameter_t + 3842
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_one_hundred_twenty_three_hundred_ninety_one_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (120 * first_coefficient, 391 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (120, 391), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_one_hundred_twenty_three_hundred_ninety_one_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_ONE_HUNDRED_TWENTY_THREE_HUNDRED_NINETY_ONE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 40_900)
            self.assertEqual((base - 302) % 409, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_one_hundred_twenty_three_hundred_ninety_one_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_one_hundred_twenty_three_hundred_ninety_one_factor_one_parallel_orbit_certificate(
                (1, -107)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_twenty_three_hundred_ninety_one_factor_one_parallel_orbit_certificate(
                (1, 301)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_twenty_three_hundred_ninety_one_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_four_hundred_twenty_twenty_nine_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((420, 29), 1),
            tuple(range(363, 354_482, 421)),
        )
        self.assertEqual(
            UNIT_COORDINATE_FOUR_HUNDRED_TWENTY_TWENTY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 25_202, 42_100),
                (38, 31_938, 42_100),
                (62, 8_362, 42_100),
                (98, 15_098, 42_100),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 421 * parameter_t + 363
            first_coefficient = (
                88_200 * parameter_t * parameter_t
                + 152_069 * parameter_t
                + 65_547
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_four_hundred_twenty_twenty_nine_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (420 * first_coefficient, 29 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (420, 29), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_four_hundred_twenty_twenty_nine_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_FOUR_HUNDRED_TWENTY_TWENTY_NINE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 42_100)
            self.assertEqual((base - 363) % 421, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_four_hundred_twenty_twenty_nine_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_four_hundred_twenty_twenty_nine_factor_one_parallel_orbit_certificate(
                (1, -58)
            )
        )
        self.assertIsNone(
            unit_coordinate_four_hundred_twenty_twenty_nine_factor_one_parallel_orbit_certificate(
                (1, 362)
            )
        )
        self.assertIsNone(
            unit_coordinate_four_hundred_twenty_twenty_nine_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_four_hundred_eight_one_hundred_forty_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((408, 145), 1),
            tuple(range(39, 375_017, 433)),
        )
        self.assertEqual(
            UNIT_COORDINATE_FOUR_HUNDRED_EIGHT_ONE_HUNDRED_FORTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 4_802, 43_300),
                (38, 1_338, 43_300),
                (62, 13_462, 43_300),
                (98, 9_998, 43_300),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 433 * parameter_t + 39
            first_coefficient = (
                83_232 * parameter_t * parameter_t
                + 14_857 * parameter_t
                + 663
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_four_hundred_eight_one_hundred_forty_five_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (408 * first_coefficient, 145 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (408, 145), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_four_hundred_eight_one_hundred_forty_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_FOUR_HUNDRED_EIGHT_ONE_HUNDRED_FORTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 43_300)
            self.assertEqual((base - 39) % 433, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_four_hundred_eight_one_hundred_forty_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_four_hundred_eight_one_hundred_forty_five_factor_one_parallel_orbit_certificate(
                (1, -394)
            )
        )
        self.assertIsNone(
            unit_coordinate_four_hundred_eight_one_hundred_forty_five_factor_one_parallel_orbit_certificate(
                (1, 38)
            )
        )
        self.assertIsNone(
            unit_coordinate_four_hundred_eight_one_hundred_forty_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_two_hundred_eighty_three_hundred_fifty_one_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((280, 351), 1),
            tuple(range(264, 403_466, 449)),
        )
        self.assertEqual(
            UNIT_COORDINATE_TWO_HUNDRED_EIGHTY_THREE_HUNDRED_FIFTY_ONE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 28_102, 44_900),
                (38, 11_938, 44_900),
                (62, 1_162, 44_900),
                (98, 29_898, 44_900),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 449 * parameter_t + 264
            first_coefficient = (
                39_200 * parameter_t * parameter_t
                + 45_879 * parameter_t
                + 13_424
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_two_hundred_eighty_three_hundred_fifty_one_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (280 * first_coefficient, 351 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (280, 351), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_two_hundred_eighty_three_hundred_fifty_one_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_TWO_HUNDRED_EIGHTY_THREE_HUNDRED_FIFTY_ONE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 44_900)
            self.assertEqual((base - 264) % 449, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_two_hundred_eighty_three_hundred_fifty_one_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_two_hundred_eighty_three_hundred_fifty_one_factor_one_parallel_orbit_certificate(
                (1, -185)
            )
        )
        self.assertIsNone(
            unit_coordinate_two_hundred_eighty_three_hundred_fifty_one_factor_one_parallel_orbit_certificate(
                (1, 263)
            )
        )
        self.assertIsNone(
            unit_coordinate_two_hundred_eighty_three_hundred_fifty_one_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_one_hundred_sixty_eight_four_hundred_twenty_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((168, 425), 1),
            tuple(range(248, 417_946, 457)),
        )
        self.assertEqual(
            UNIT_COORDINATE_ONE_HUNDRED_SIXTY_EIGHT_FOUR_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 10_302, 45_700),
                (38, 32_238, 45_700),
                (62, 1_162, 45_700),
                (98, 23_098, 45_700),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 457 * parameter_t + 248
            first_coefficient = (
                14_112 * parameter_t * parameter_t
                + 15_161 * parameter_t
                + 4_072
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_one_hundred_sixty_eight_four_hundred_twenty_five_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (168 * first_coefficient, 425 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (168, 425), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_one_hundred_sixty_eight_four_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_ONE_HUNDRED_SIXTY_EIGHT_FOUR_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 45_700)
            self.assertEqual((base - 248) % 457, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_one_hundred_sixty_eight_four_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_one_hundred_sixty_eight_four_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                (1, -209)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_sixty_eight_four_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                (1, 247)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_sixty_eight_four_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_three_hundred_eighty_two_hundred_sixty_one_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((380, 261), 1),
            tuple(range(373, 425_415, 461)),
        )
        self.assertEqual(
            UNIT_COORDINATE_THREE_HUNDRED_EIGHTY_TWO_HUNDRED_SIXTY_ONE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 41_402, 46_100),
                (38, 30_338, 46_100),
                (62, 22_962, 46_100),
                (98, 11_898, 46_100),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 461 * parameter_t + 373
            first_coefficient = (
                72_200 * parameter_t * parameter_t
                + 116_621 * parameter_t
                + 47_093
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_three_hundred_eighty_two_hundred_sixty_one_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (380 * first_coefficient, 261 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (380, 261), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_three_hundred_eighty_two_hundred_sixty_one_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_THREE_HUNDRED_EIGHTY_TWO_HUNDRED_SIXTY_ONE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 46_100)
            self.assertEqual((base - 373) % 461, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_three_hundred_eighty_two_hundred_sixty_one_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_three_hundred_eighty_two_hundred_sixty_one_factor_one_parallel_orbit_certificate(
                (1, -88)
            )
        )
        self.assertIsNone(
            unit_coordinate_three_hundred_eighty_two_hundred_sixty_one_factor_one_parallel_orbit_certificate(
                (1, 372)
            )
        )
        self.assertIsNone(
            unit_coordinate_three_hundred_eighty_two_hundred_sixty_one_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_three_hundred_sixty_three_hundred_nineteen_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((360, 319), 1),
            tuple(range(23, 462_745, 481)),
        )
        self.assertEqual(
            UNIT_COORDINATE_THREE_HUNDRED_SIXTY_THREE_HUNDRED_NINETEEN_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 28_402, 48_100),
                (38, 7_238, 48_100),
                (62, 9_162, 48_100),
                (98, 36_098, 48_100),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 481 * parameter_t + 23
            first_coefficient = (
                64_800 * parameter_t * parameter_t
                + 5_959 * parameter_t
                + 137
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_three_hundred_sixty_three_hundred_nineteen_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (360 * first_coefficient, 319 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (360, 319), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_three_hundred_sixty_three_hundred_nineteen_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_THREE_HUNDRED_SIXTY_THREE_HUNDRED_NINETEEN_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 48_100)
            self.assertEqual((base - 23) % 481, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_three_hundred_sixty_three_hundred_nineteen_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_three_hundred_sixty_three_hundred_nineteen_factor_one_parallel_orbit_certificate(
                (1, -458)
            )
        )
        self.assertIsNone(
            unit_coordinate_three_hundred_sixty_three_hundred_nineteen_factor_one_parallel_orbit_certificate(
                (1, 22)
            )
        )
        self.assertIsNone(
            unit_coordinate_three_hundred_sixty_three_hundred_nineteen_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_one_hundred_thirty_two_four_hundred_seventy_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((132, 475), 1),
            tuple(range(199, 486_297, 493)),
        )
        self.assertEqual(
            UNIT_COORDINATE_ONE_HUNDRED_THIRTY_TWO_FOUR_HUNDRED_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 35_202, 49_300),
                (38, 11_538, 49_300),
                (62, 45_062, 49_300),
                (98, 21_398, 49_300),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 493 * parameter_t + 199
            first_coefficient = (
                8_712 * parameter_t * parameter_t
                + 6_907 * parameter_t
                + 1_369
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_one_hundred_thirty_two_four_hundred_seventy_five_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (132 * first_coefficient, 475 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (132, 475), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_one_hundred_thirty_two_four_hundred_seventy_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_ONE_HUNDRED_THIRTY_TWO_FOUR_HUNDRED_SEVENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 49_300)
            self.assertEqual((base - 199) % 493, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_one_hundred_thirty_two_four_hundred_seventy_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_one_hundred_thirty_two_four_hundred_seventy_five_factor_one_parallel_orbit_certificate(
                (1, -294)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_thirty_two_four_hundred_seventy_five_factor_one_parallel_orbit_certificate(
                (1, 198)
            )
        )
        self.assertIsNone(
            unit_coordinate_one_hundred_thirty_two_four_hundred_seventy_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_two_hundred_twenty_four_hundred_fifty_nine_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((220, 459), 1),
            tuple(range(96, 518_258, 509)),
        )
        self.assertEqual(
            UNIT_COORDINATE_TWO_HUNDRED_TWENTY_FOUR_HUNDRED_FIFTY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 17_402, 50_900),
                (38, 19_438, 50_900),
                (62, 37_762, 50_900),
                (98, 39_798, 50_900),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 509 * parameter_t + 96
            first_coefficient = (
                24_200 * parameter_t * parameter_t
                + 8_931 * parameter_t
                + 824
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_two_hundred_twenty_four_hundred_fifty_nine_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (220 * first_coefficient, 459 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (220, 459), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_two_hundred_twenty_four_hundred_fifty_nine_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_TWO_HUNDRED_TWENTY_FOUR_HUNDRED_FIFTY_NINE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 50_900)
            self.assertEqual((base - 96) % 509, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_two_hundred_twenty_four_hundred_fifty_nine_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_two_hundred_twenty_four_hundred_fifty_nine_factor_one_parallel_orbit_certificate(
                (1, -413)
            )
        )
        self.assertIsNone(
            unit_coordinate_two_hundred_twenty_four_hundred_fifty_nine_factor_one_parallel_orbit_certificate(
                (1, 95)
            )
        )
        self.assertIsNone(
            unit_coordinate_two_hundred_twenty_four_hundred_fifty_nine_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_four_hundred_forty_two_hundred_seventy_nine_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((440, 279), 1),
            tuple(range(103, 542_985, 521)),
        )
        self.assertEqual(
            UNIT_COORDINATE_FOUR_HUNDRED_FORTY_TWO_HUNDRED_SEVENTY_NINE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 10_002, 52_100),
                (38, 18_338, 52_100),
                (62, 41_262, 52_100),
                (98, 49_598, 52_100),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 521 * parameter_t + 103
            first_coefficient = (
                96_800 * parameter_t * parameter_t
                + 38_039 * parameter_t
                + 3_737
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_four_hundred_forty_two_hundred_seventy_nine_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (440 * first_coefficient, 279 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (440, 279), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_four_hundred_forty_two_hundred_seventy_nine_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_FOUR_HUNDRED_FORTY_TWO_HUNDRED_SEVENTY_NINE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 52_100)
            self.assertEqual((base - 103) % 521, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_four_hundred_forty_two_hundred_seventy_nine_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_four_hundred_forty_two_hundred_seventy_nine_factor_one_parallel_orbit_certificate(
                (1, -418)
            )
        )
        self.assertIsNone(
            unit_coordinate_four_hundred_forty_two_hundred_seventy_nine_factor_one_parallel_orbit_certificate(
                (1, 102)
            )
        )
        self.assertIsNone(
            unit_coordinate_four_hundred_forty_two_hundred_seventy_nine_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_ninety_two_five_hundred_twenty_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((92, 525), 1),
            tuple(range(78, 568_256, 533)),
        )
        self.assertEqual(
            UNIT_COORDINATE_NINETY_TWO_FIVE_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 15_002, 53_300),
                (38, 10_738, 53_300),
                (62, 25_662, 53_300),
                (98, 21_398, 53_300),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 533 * parameter_t + 78
            first_coefficient = (
                4_232 * parameter_t * parameter_t + 1_149 * parameter_t + 78
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_ninety_two_five_hundred_twenty_five_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (92 * first_coefficient, 525 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (92, 525), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_ninety_two_five_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_NINETY_TWO_FIVE_HUNDRED_TWENTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 53_300)
            self.assertEqual((base - 78) % 533, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_ninety_two_five_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_ninety_two_five_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                (1, -455)
            )
        )
        self.assertIsNone(
            unit_coordinate_ninety_two_five_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                (1, 77)
            )
        )
        self.assertIsNone(
            unit_coordinate_ninety_two_five_hundred_twenty_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_four_hundred_twenty_three_hundred_forty_one_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((420, 341), 1),
            tuple(range(113, 585_475, 541)),
        )
        self.assertEqual(
            UNIT_COORDINATE_FOUR_HUNDRED_TWENTY_THREE_HUNDRED_FORTY_ONE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 15_802, 54_100),
                (38, 13_638, 54_100),
                (62, 48_262, 54_100),
                (98, 46_098, 54_100),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 541 * parameter_t + 113
            first_coefficient = (
                88_200 * parameter_t * parameter_t
                + 36_581 * parameter_t
                + 3_793
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_four_hundred_twenty_three_hundred_forty_one_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (420 * first_coefficient, 341 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (420, 341), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_four_hundred_twenty_three_hundred_forty_one_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_FOUR_HUNDRED_TWENTY_THREE_HUNDRED_FORTY_ONE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 54_100)
            self.assertEqual((base - 113) % 541, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_four_hundred_twenty_three_hundred_forty_one_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_four_hundred_twenty_three_hundred_forty_one_factor_one_parallel_orbit_certificate(
                (1, -428)
            )
        )
        self.assertIsNone(
            unit_coordinate_four_hundred_twenty_three_hundred_forty_one_factor_one_parallel_orbit_certificate(
                (1, 112)
            )
        )
        self.assertIsNone(
            unit_coordinate_four_hundred_twenty_three_hundred_forty_one_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_five_hundred_thirty_two_one_hundred_sixty_five_factor_one_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((532, 165), 1),
            tuple(range(412, 620_910, 557)),
        )
        self.assertEqual(
            UNIT_COORDINATE_FIVE_HUNDRED_THIRTY_TWO_ONE_HUNDRED_SIXTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS,
            (
                (2, 39_402, 55_700),
                (38, 10_438, 55_700),
                (62, 28_262, 55_700),
                (98, 54_998, 55_700),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 557 * parameter_t + 412
            first_coefficient = (
                141_512 * parameter_t * parameter_t
                + 209_189 * parameter_t
                + 77_308
            )
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_five_hundred_thirty_two_one_hundred_sixty_five_factor_one_parallel_certificate(
                parameter_t
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (532 * first_coefficient, 165 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (532, 165), 1),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_five_hundred_thirty_two_one_hundred_sixty_five_factor_one_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_FIVE_HUNDRED_THIRTY_TWO_ONE_HUNDRED_SIXTY_FIVE_FACTOR_ONE_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 55_700)
            self.assertEqual((base - 412) % 557, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_five_hundred_thirty_two_one_hundred_sixty_five_factor_one_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_five_hundred_thirty_two_one_hundred_sixty_five_factor_one_parallel_orbit_certificate(
                (1, -145)
            )
        )
        self.assertIsNone(
            unit_coordinate_five_hundred_thirty_two_one_hundred_sixty_five_factor_one_parallel_orbit_certificate(
                (1, 411)
            )
        )
        self.assertIsNone(
            unit_coordinate_five_hundred_thirty_two_one_hundred_sixty_five_factor_one_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_unit_coordinate_fifteen_eight_factor_two_parallel_family(self):
        self.assertEqual(
            unit_coordinate_parallel_factor_residues((15, 8), 2),
            tuple(range(26, 1_156, 34)),
        )
        self.assertEqual(
            UNIT_COORDINATE_FIFTEEN_EIGHT_FACTOR_TWO_RESIDUAL_ROWS,
            (
                (2, 502, 1_700),
                (38, 638, 1_700),
                (62, 162, 1_700),
                (98, 298, 1_700),
            ),
        )

        for parameter_t in range(-5, 6):
            fixed_coordinate = 34 * parameter_t + 26
            first_coefficient = (
                225 * parameter_t * parameter_t + 338 * parameter_t + 127
            )
            target = (1, fixed_coordinate)
            certificate = (
                unit_coordinate_fifteen_eight_factor_two_parallel_certificate(
                    parameter_t
                )
            )
            self.assertEqual(certificate.target, target)
            self.assertEqual(
                certificate.midpoint,
                (15 * first_coefficient, 8 * first_coefficient),
            )
            self.assertTrue(certificate.valid())
            self.assertEqual(
                parallel_direction_factor_certificate(target, (15, 8), 2),
                certificate,
            )

            for orbit_target in sign_swap_orbit(target):
                orbit_certificate = (
                    unit_coordinate_fifteen_eight_factor_two_parallel_orbit_certificate(
                        orbit_target
                    )
                )
                self.assertIsNotNone(orbit_certificate)
                self.assertEqual(orbit_certificate.target, orbit_target)
                self.assertTrue(orbit_certificate.valid())

        for residue, base, period in (
            UNIT_COORDINATE_FIFTEEN_EIGHT_FACTOR_TWO_RESIDUAL_ROWS
        ):
            self.assertIn(residue, UNIT_COORDINATE_PROMOTED_MOD_HUNDRED_RESIDUES)
            self.assertEqual(base % 100, residue)
            self.assertEqual(period, 1_700)
            self.assertEqual((base - 26) % 34, 0)

            for parameter_t in range(-2, 3):
                fixed_coordinate = base + period * parameter_t
                target = (1, fixed_coordinate)
                self.assertIsNone(
                    unit_coordinate_promoted_mod_hundred_certificate(target)
                )
                certificate = (
                    unit_coordinate_fifteen_eight_factor_two_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNotNone(
            unit_coordinate_fifteen_eight_factor_two_parallel_orbit_certificate(
                (1, 8)
            )
        )
        self.assertIsNone(
            unit_coordinate_fifteen_eight_factor_two_parallel_orbit_certificate(
                (1, 10)
            )
        )
        self.assertIsNone(
            unit_coordinate_fifteen_eight_factor_two_parallel_orbit_certificate(
                (2, 3)
            )
        )

    def test_four_three_factor_five_parallel_congruence_family(self):
        modulus = parallel_direction_factor_modulus((4, 3), 5)
        residues = parallel_direction_factor_residue_classes((4, 3), 5)
        certificate_residues = parallel_direction_factor_certificate_residue_classes(
            (4, 3),
            5,
        )
        self.assertEqual(modulus, 250)
        self.assertEqual(len(residues), 1250)
        self.assertEqual(len(certificate_residues), 1188)
        self.assertLess(certificate_residues, residues)
        self.assertIn((1, 17), certificate_residues)
        self.assertIn((3, 6), residues)
        self.assertNotIn((3, 6), certificate_residues)

        examples = (
            ((1, 17), (76, 57)),
            ((1, 92), (2176, 1632)),
            ((3, 31), (228, 171)),
            ((5, 20), (80, 60)),
        )
        for target, midpoint in examples:
            certificate = four_three_factor_five_parallel_certificate(target)
            self.assertIsNotNone(certificate, target)
            self.assertEqual(certificate.target, target)
            self.assertEqual(certificate.midpoint, midpoint)
            self.assertTrue(certificate.valid())

            shifted_target = (target[0] + 2 * modulus, target[1] - 3 * modulus)
            shifted = four_three_factor_five_parallel_certificate(shifted_target)
            self.assertIsNotNone(shifted, shifted_target)
            self.assertEqual(shifted.target, shifted_target)
            self.assertTrue(shifted.valid())

        self.assertIsNone(four_three_factor_five_parallel_certificate((1, 16)))
        self.assertIsNone(four_three_factor_five_parallel_certificate((3, 6)))
        self.assertIsNotNone(parallel_direction_factor_coefficient((3, 6), (4, 3), 5))

        degenerate_residue_translate = four_three_factor_five_parallel_certificate(
            (3 + modulus, 6)
        )
        self.assertIsNotNone(degenerate_residue_translate)
        self.assertEqual(degenerate_residue_translate.target, (3 + modulus, 6))
        self.assertEqual(degenerate_residue_translate.midpoint, (8808, 6606))
        self.assertTrue(degenerate_residue_translate.valid())

    def test_unit_coordinate_parallel_factor_residue_family(self):
        residues = unit_coordinate_parallel_factor_residues((4, 3), 5)
        self.assertEqual(residues, tuple(range(17, 250, 25)))
        for fixed_coordinate in (-233, -208, 17, 42, 92, 242, 267):
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_parallel_factor_orbit_certificate(
                target,
                (4, 3),
                5,
            )
            self.assertIsNotNone(certificate, target)
            self.assertEqual(certificate.target, target)
            self.assertTrue(certificate.valid())

        factor_four_residues = unit_coordinate_parallel_factor_residues((-3, -4), 4)
        self.assertEqual(factor_four_residues, tuple(range(12, 200, 20)))
        for fixed_coordinate in (-68, -8, 12, 32, 92, 112, 212):
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_parallel_factor_orbit_certificate(
                target,
                (-3, -4),
                4,
            )
            explicit = unit_coordinate_factor_four_parallel_certificate(
                (fixed_coordinate - 12) // 20
            )
            self.assertEqual(certificate, explicit)
            self.assertIsNotNone(certificate)
            self.assertTrue(certificate.valid())

        one_mod_five_residues = unit_coordinate_parallel_factor_residues((4, -3), 1)
        self.assertEqual(one_mod_five_residues, tuple(range(1, 50, 5)))
        for fixed_coordinate in (-24, -4, 1, 6, 16, 26, 51):
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_parallel_factor_orbit_certificate(
                target,
                (4, -3),
                1,
            )
            explicit = unit_coordinate_one_mod_five_parallel_certificate(
                (fixed_coordinate - 1) // 5
            )
            self.assertEqual(certificate, explicit)
            self.assertIsNotNone(certificate)
            self.assertTrue(certificate.valid())

        seven_mod_ten_residues = unit_coordinate_parallel_factor_residues((3, 4), 1)
        self.assertEqual(seven_mod_ten_residues, tuple(range(7, 50, 10)))
        for fixed_coordinate in (-23, -3, 7, 17, 27, 37, 57):
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_parallel_factor_orbit_certificate(
                target,
                (3, 4),
                1,
            )
            explicit = unit_coordinate_seven_mod_ten_parallel_certificate(
                (fixed_coordinate - 7) // 10
            )
            self.assertEqual(certificate, explicit)
            self.assertIsNotNone(certificate)
            self.assertTrue(certificate.valid())

        factor_twenty_five_residues = unit_coordinate_parallel_factor_residues(
            (4, -3),
            25,
        )
        self.assertEqual(factor_twenty_five_residues, tuple(range(18, 1250, 25)))
        for fixed_coordinate in (-32, -7, 18, 43, 68, 93, 118):
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_parallel_factor_orbit_certificate(
                target,
                (4, -3),
                25,
            )
            explicit = unit_coordinate_factor_twenty_five_parallel_certificate(
                (fixed_coordinate - 18) // 25
            )
            self.assertEqual(certificate, explicit)
            self.assertIsNotNone(certificate)
            self.assertTrue(certificate.valid())

        twenty_two_mod_twenty_five_residues = unit_coordinate_parallel_factor_residues(
            (-4, -3),
            5,
        )
        self.assertEqual(
            twenty_two_mod_twenty_five_residues,
            tuple(range(22, 250, 25)),
        )
        for fixed_coordinate in (-53, -28, -3, 22, 47, 72, 97, 122):
            target = (1, fixed_coordinate)
            certificate = unit_coordinate_parallel_factor_orbit_certificate(
                target,
                (-4, -3),
                5,
            )
            explicit = unit_coordinate_twenty_two_mod_twenty_five_parallel_certificate(
                (fixed_coordinate - 22) // 25
            )
            self.assertEqual(certificate, explicit)
            if fixed_coordinate == -3:
                self.assertIsNone(certificate)
            else:
                self.assertIsNotNone(certificate)
                self.assertTrue(certificate.valid())

        self.assertIsNone(
            unit_coordinate_parallel_factor_orbit_certificate((1, 16), (4, 3), 5)
        )
        with self.assertRaises(ValueError):
            unit_coordinate_parallel_factor_residues((1, 1), 5)

    def test_ray_parallel_factor_residue_family(self):
        self.assertEqual(ray_multiplier((14, 7), (2, 1)), 7)
        self.assertEqual(ray_multiplier((-14, -7), (2, 1)), -7)
        self.assertIsNone(ray_multiplier((14, 8), (2, 1)))
        with self.assertRaises(ValueError):
            ray_multiplier((1, 1), (0, 0))

        residues = ray_parallel_factor_residues((2, 1), (4, 3), 2)
        self.assertEqual(residues, tuple(range(2, 100, 5)))

        for multiplier, midpoint in (
            (7, (20, 15)),
            (12, (44, 33)),
            (107, (2020, 1515)),
        ):
            target = (2 * multiplier, multiplier)
            certificate = ray_parallel_factor_certificate(
                target,
                (2, 1),
                (4, 3),
                2,
            )
            self.assertIsNotNone(certificate, target)
            self.assertEqual(certificate.target, target)
            self.assertEqual(certificate.midpoint, midpoint)
            self.assertTrue(certificate.valid())

        opposite_residues = ray_parallel_factor_residues((2, 1), (-4, -3), 2)
        self.assertEqual(opposite_residues, tuple(range(3, 100, 5)))
        opposite = ray_parallel_factor_certificate((16, 8), (2, 1), (-4, -3), 2)
        self.assertIsNotNone(opposite)
        self.assertEqual(opposite.midpoint, (4, 3))
        self.assertTrue(opposite.valid())

        self.assertIsNone(
            ray_parallel_factor_certificate((4, 2), (2, 1), (4, 3), 2)
        )
        self.assertIsNone(
            ray_parallel_factor_certificate((14, 8), (2, 1), (4, 3), 2)
        )
        self.assertIsNone(
            ray_parallel_factor_certificate((0, 0), (2, 1), (4, 3), 2)
        )
        with self.assertRaises(ValueError):
            ray_parallel_factor_residues((0, 0), (4, 3), 2)

    def test_parallel_direction_bounded_factor_cover_probe(self):
        examples = (
            ((1, 92), 4, (-1065, -1420)),
            ((4, 115), 4, (-3956, -2967)),
            ((10, 33), 6, (-116, -87)),
        )
        for target, max_factor, midpoint in examples:
            certificate = parallel_direction_bounded_factor_cover_certificate(
                target,
                8,
                max_factor,
            )
            self.assertIsNotNone(certificate, (target, max_factor))
            self.assertEqual(certificate.midpoint, midpoint)
            self.assertTrue(certificate.valid())

        self.assertIsNone(parallel_direction_bounded_factor_cover_certificate((1, 92), 8, 3))
        bounded = parallel_direction_bounded_factor_cover_certificate((1, 92), 8, 4)
        self.assertIsNotNone(bounded)
        self.assertTrue(bounded.valid())

        covered_count = 0
        for g in range(1, 81):
            for h in range(1, 81):
                target = (g, h)
                if target in KNOWN_DISTANCE_THREE_ORBIT or edge((0, 0), target):
                    continue
                if gcd(g, h) != 1:
                    continue

                certificate = (
                    parallel_direction_standard_completion_cover_certificate(target, 8)
                    or parallel_direction_bounded_factor_cover_certificate(target, 8, 1000)
                )
                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())
                covered_count += 1

        self.assertGreater(covered_count, 3800)

        with self.assertRaises(ValueError):
            parallel_direction_bounded_factor_cover_certificate((1, 92), 1, 5)
        with self.assertRaises(ValueError):
            parallel_direction_bounded_factor_cover_certificate((1, 92), 8, 0)

    def test_parallel_direction_factor_residue_classes(self):
        direction = (3, 4)
        factor = 1
        modulus = parallel_direction_factor_modulus(direction, factor)
        residues = parallel_direction_factor_residue_classes(direction, factor)
        self.assertEqual(modulus, 50)
        self.assertGreater(len(residues), 0)
        self.assertLess(len(residues), modulus * modulus)
        self.assertEqual(
            parallel_direction_primitive_factor_determinant_residue_rows(
                direction,
                factor,
            ),
            ((7, 1), (17, 6), (27, 11), (37, 16), (47, 21)),
        )

        for g in range(-75, 76):
            for h in range(-75, 76):
                target = (g, h)
                expected = (
                    parallel_direction_factor_coefficient(target, direction, factor)
                    is not None
                )
                self.assertEqual(
                    parallel_direction_factor_congruence_holds(
                        target,
                        direction,
                        factor,
                    ),
                    expected,
                )
                self.assertEqual(
                    parallel_direction_primitive_factor_determinant_residue_holds(
                        target,
                        direction,
                        factor,
                    ),
                    expected,
                )
                self.assertEqual(
                    (target[0] % modulus, target[1] % modulus) in residues,
                    expected,
                )

        for direction, factor in PARALLEL_DIRECTION_PROMOTED_345_FACTOR_ROWS:
            determinant_rows = (
                parallel_direction_primitive_factor_determinant_residue_rows(
                    direction,
                    factor,
                )
            )
            self.assertEqual(
                len(determinant_rows)
                * parallel_direction_factor_modulus(direction, factor),
                len(parallel_direction_factor_residue_classes(direction, factor)),
            )
            for g in range(-25, 26):
                for h in range(-25, 26):
                    target = (g, h)
                    expected = (
                        parallel_direction_factor_coefficient(
                            target,
                            direction,
                            factor,
                        )
                        is not None
                    )
                    self.assertEqual(
                        parallel_direction_factor_congruence_holds(
                            target,
                            direction,
                            factor,
                        ),
                        expected,
                    )
                    self.assertEqual(
                        parallel_direction_primitive_factor_determinant_residue_holds(
                            target,
                            direction,
                            factor,
                        ),
                        expected,
                    )

        base = parallel_direction_factor_residue_certificate((1, 5), (-4, -3), 1)
        self.assertIsNotNone(base)
        self.assertEqual(base.midpoint, (-20, -15))
        self.assertTrue(base.valid())

        shifted = parallel_direction_factor_residue_certificate(
            (1 + 3 * modulus, 5 - 2 * modulus),
            (-4, -3),
            1,
        )
        self.assertIsNotNone(shifted)
        self.assertTrue(shifted.valid())

    @pytest.mark.perf
    def test_parallel_direction_factor_integrality_strip_intersection_residue_count(self):
        self.assertEqual(
            parallel_direction_factor_integrality_strip_intersection_residue_count(
                (3, 4),
                2,
                1,
                (-4, -3),
                1,
            ),
            (50, 125),
        )

        strip_direction = (-12, -5)
        strip_modulus = 13
        strip_residue = 7
        factor_direction = (-4, -3)
        factor = 1
        lcm_modulus, residue_count = (
            parallel_direction_factor_integrality_strip_intersection_residue_count(
                strip_direction,
                strip_modulus,
                strip_residue,
                factor_direction,
                factor,
            )
        )
        self.assertEqual((lcm_modulus, residue_count), (650, 3250))
        self.assertEqual(
            parallel_direction_primitive_factor_integrality_strip_intersection_residue_count(
                strip_direction,
                strip_modulus,
                strip_residue,
                factor_direction,
                factor,
            ),
            (lcm_modulus, residue_count),
        )
        linear_modulus, linear_rows = (
            parallel_direction_primitive_factor_integrality_strip_intersection_linear_rows(
                strip_direction,
                strip_modulus,
                strip_residue,
                factor_direction,
                factor,
            )
        )
        self.assertEqual(linear_modulus, lcm_modulus)
        self.assertEqual(
            linear_rows,
            (
                (3, 0, 1, 650),
                (13, 0, 1, 650),
                (23, 0, 1, 650),
                (33, 0, 1, 650),
                (43, 0, 1, 650),
            ),
        )
        self.assertEqual(sum(row[-1] for row in linear_rows), residue_count)

        factor_modulus = parallel_direction_factor_modulus(factor_direction, factor)
        factor_residues = parallel_direction_factor_residue_classes(
            factor_direction,
            factor,
        )
        brute_count = 0
        for g in range(lcm_modulus):
            for h in range(lcm_modulus):
                target = (g, h)
                expected = (
                    (g % factor_modulus, h % factor_modulus) in factor_residues
                    and determinant(strip_direction, target) % strip_modulus
                    == strip_residue
                )
                row_witness = (
                    parallel_direction_primitive_factor_integrality_strip_intersection_linear_row_witness(
                        target,
                        strip_direction,
                        strip_modulus,
                        strip_residue,
                        factor_direction,
                        factor,
                    )
                )
                self.assertEqual(row_witness is not None, expected)
                if (g % factor_modulus, h % factor_modulus) not in factor_residues:
                    continue
                if determinant(strip_direction, target) % strip_modulus != strip_residue:
                    continue
                brute_count += 1
        self.assertEqual(brute_count, residue_count)
        self.assertEqual(
            parallel_direction_primitive_factor_integrality_strip_intersection_linear_row_witness(
                (1, 15),
                strip_direction,
                strip_modulus,
                strip_residue,
                factor_direction,
                factor,
            ),
            (43, 0, 1, 650),
        )

        for obligation in (
            ((2, 3), 1, 13, 5, 7, 4, 11),
            ((4, 5), 2, 41, 9, 10, 33, 19),
        ):
            strip_modulus = (
                parallel_direction_conjugate_ideal_divisor_obligation_strip_modulus(
                    obligation
                )
            )
            strip_residue = (
                parallel_direction_conjugate_ideal_divisor_obligation_strip_residue(
                    obligation
                )
            )
            for strip_direction in (
                parallel_direction_conjugate_ideal_divisor_obligation_directions(
                    obligation
                )
            ):
                for factor_direction, factor in PARALLEL_DIRECTION_PROMOTED_345_FACTOR_ROWS:
                    self.assertEqual(
                        parallel_direction_primitive_factor_integrality_strip_intersection_residue_count(
                            strip_direction,
                            strip_modulus,
                            strip_residue,
                            factor_direction,
                            factor,
                        ),
                        parallel_direction_factor_integrality_strip_intersection_residue_count(
                            strip_direction,
                            strip_modulus,
                            strip_residue,
                            factor_direction,
                            factor,
                        ),
                    )
                    linear_modulus, linear_rows = (
                        parallel_direction_primitive_factor_integrality_strip_intersection_linear_rows(
                            strip_direction,
                            strip_modulus,
                            strip_residue,
                            factor_direction,
                            factor,
                        )
                    )
                    self.assertEqual(
                        (
                            linear_modulus,
                            sum(row[-1] for row in linear_rows),
                        ),
                        parallel_direction_factor_integrality_strip_intersection_residue_count(
                            strip_direction,
                            strip_modulus,
                            strip_residue,
                            factor_direction,
                            factor,
                        ),
                    )

        with self.assertRaises(ValueError):
            parallel_direction_factor_integrality_strip_intersection_residue_count(
                (1, 1),
                13,
                7,
                factor_direction,
                factor,
            )
        with self.assertRaises(ValueError):
            parallel_direction_factor_congruence_holds((1, 1), (1, 1), 1)
        with self.assertRaises(ValueError):
            parallel_direction_factor_congruence_holds((1, 1), (3, 4), 0)
        with self.assertRaises(ValueError):
            parallel_direction_primitive_factor_determinant_residue_rows((6, 8), 1)
        with self.assertRaises(ValueError):
            parallel_direction_primitive_factor_integrality_strip_intersection_residue_count(
                strip_direction,
                strip_modulus,
                strip_residue,
                (6, 8),
                factor,
            )
        with self.assertRaises(ValueError):
            parallel_direction_primitive_factor_integrality_strip_intersection_linear_rows(
                strip_direction,
                strip_modulus,
                strip_residue,
                (6, 8),
                factor,
            )
        with self.assertRaises(ValueError):
            parallel_direction_factor_integrality_strip_intersection_residue_count(
                strip_direction,
                1,
                0,
                factor_direction,
                factor,
            )

        obligation_rows = (
            parallel_direction_conjugate_ideal_promoted_345_integrality_strip_intersection_counts(
                ((4, 5), 2, 41, 9, 10, 33, 19)
            )
        )
        self.assertEqual(len(obligation_rows), 288)
        self.assertEqual(
            obligation_rows[:3],
            (
                ((-40, -9), (-4, -3), 1, 2050, 0),
                ((-40, -9), (-4, -3), 2, 4100, 41000),
                ((-40, -9), (-4, -3), 3, 6150, 0),
            ),
        )
        self.assertEqual(
            obligation_rows[72:75],
            (
                ((-9, 40), (-4, -3), 1, 2050, 5125),
                ((-9, 40), (-4, -3), 2, 4100, 20500),
                ((-9, 40), (-4, -3), 3, 6150, 15375),
            ),
        )
        self.assertEqual(
            sum(1 for row in obligation_rows if row[-1] != 0),
            208,
        )
        self.assertEqual(
            sum(1 for row in obligation_rows if row[-1] == 0),
            80,
        )

    @pytest.mark.perf
    def test_parallel_direction_candidate_cover_probe(self):
        for target in KNOWN_DISTANCE_THREE_ORBIT:
            self.assertIsNone(parallel_direction_cover_certificate(target, 8), target)

        covered_count = 0
        for g in range(1, 1001):
            for h in range(1, 1001):
                target = (g, h)
                if target in KNOWN_DISTANCE_THREE_ORBIT or edge((0, 0), target):
                    continue
                if gcd(g, h) != 1:
                    continue

                certificate = parallel_direction_cover_certificate(target, 8)
                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())
                covered_count += 1

        self.assertGreater(covered_count, 600000)
        with self.assertRaises(ValueError):
            parallel_direction_cover_certificate((1, 1), 1)

    def test_parallel_direction_cover_witness_census(self):
        census = parallel_direction_cover_witness_census(30, 8)
        self.assertIsInstance(census, ParallelDirectionCoverWitnessCensus)
        self.assertEqual(census.max_coordinate, 30)
        self.assertEqual(census.max_parameter, 8)
        self.assertEqual(census.target_count, 543)
        self.assertEqual(census.uncovered_targets, ())
        self.assertEqual(
            census.direction_counts[:6],
            (
                ((-4, -3), 311),
                ((-4, 3), 167),
                ((-3, -4), 31),
                ((-3, 4), 16),
                ((-12, 5), 5),
                ((-12, -5), 4),
            ),
        )
        self.assertEqual(
            census.factor_counts[:8],
            (
                (1, 117),
                (2, 47),
                (3, 25),
                (4, 24),
                (9, 21),
                (5, 17),
                (8, 14),
                (25, 14),
            ),
        )
        self.assertEqual(
            census.direction_factor_counts[:8],
            (
                ((-4, -3), 1, 70),
                ((-4, -3), 2, 31),
                ((-4, 3), 1, 30),
                ((-4, -3), 3, 16),
                ((-4, 3), 2, 15),
                ((-4, -3), 4, 13),
                ((-4, -3), 25, 11),
                ((-4, -3), 9, 10),
            ),
        )

        smaller = parallel_direction_cover_witness_census(30, 2)
        self.assertGreater(len(smaller.uncovered_targets), 0)
        self.assertIn((2, 29), smaller.uncovered_targets)

        with self.assertRaises(ValueError):
            parallel_direction_cover_witness_census(0, 8)
        with self.assertRaises(ValueError):
            parallel_direction_cover_witness_census(30, 1)

    def test_parallel_direction_promoted_345_factor_cover(self):
        self.assertEqual(
            PARALLEL_DIRECTION_PROMOTED_345_DIRECTIONS,
            (
                (-4, -3),
                (-4, 3),
                (-3, -4),
                (-3, 4),
                (3, -4),
                (3, 4),
                (4, -3),
                (4, 3),
            ),
        )
        self.assertEqual(
            PARALLEL_DIRECTION_PROMOTED_345_FACTORS,
            (1, 2, 3, 4, 5, 6, 8, 9, 25),
        )
        self.assertEqual(len(PARALLEL_DIRECTION_PROMOTED_345_FACTOR_ROWS), 72)
        self.assertIn(
            ((-4, -3), 1),
            PARALLEL_DIRECTION_PROMOTED_345_FACTOR_ROWS,
        )
        self.assertIn(
            ((4, 3), 25),
            PARALLEL_DIRECTION_PROMOTED_345_FACTOR_ROWS,
        )

        expected_witnesses = (
            ((1, 5), (-4, -3), 1, (-20, -15)),
            ((1, 17), (3, 4), 1, (141, 188)),
            ((1, 92), (-3, -4), 4, (-1065, -1420)),
            ((5, 20), (4, 3), 5, (80, 60)),
        )
        for target, direction, factor, midpoint in expected_witnesses:
            witness = parallel_direction_promoted_345_factor_witness(target)
            self.assertIsNotNone(witness, target)
            self.assertEqual(witness.direction, direction)
            self.assertEqual(witness.factor, factor)
            self.assertEqual(witness.midpoint, midpoint)
            certificate = parallel_direction_promoted_345_factor_certificate(target)
            self.assertEqual(certificate, witness.certificate)
            self.assertTrue(certificate.valid())

        self.assertIsNone(parallel_direction_promoted_345_factor_certificate((2, 29)))
        self.assertIsNone(parallel_direction_promoted_345_factor_witness((2, 29)))
        self.assertIsNotNone(parallel_direction_cover_certificate((2, 29), 8))

        covered_count = 0
        misses: list[Point] = []
        for g in range(1, 51):
            for h in range(1, 51):
                target = (g, h)
                if target in KNOWN_DISTANCE_THREE_ORBIT or edge((0, 0), target):
                    continue
                if gcd(g, h) != 1:
                    continue

                certificate = parallel_direction_promoted_345_factor_certificate(target)
                if certificate is None:
                    misses.append(target)
                    continue
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())
                covered_count += 1

        self.assertEqual(covered_count, 1461)
        self.assertEqual(len(misses), 68)
        self.assertEqual(
            tuple(misses[:8]),
            (
                (1, 38),
                (2, 29),
                (2, 49),
                (5, 14),
                (5, 26),
                (5, 34),
                (5, 46),
                (7, 10),
            ),
        )
        for target in misses:
            certificate = parallel_direction_cover_certificate(target, 8)
            self.assertIsNotNone(certificate, target)
            self.assertTrue(certificate.valid())

    def test_parallel_direction_primitive_ray_lift(self):
        for target in ((0, 0), (1, 0), (2, 0), (2, 1)):
            self.assertIsNone(parallel_direction_primitive_ray_certificate(target, 8))

        for target in ((1000, 0), (0, -1000), (4000, 2000), (-2000, 4000)):
            cert = parallel_direction_primitive_ray_certificate(target, 8)
            self.assertIsNotNone(cert, target)
            self.assertEqual(cert.target, target)
            self.assertTrue(cert.valid())

        examples = (
            ((1, 501), 23),
            ((601, 1000), 7),
            ((997, 983), 11),
            ((-1000, 601), 13),
            ((14, 25), 29),
            ((158, 391), 31),
        )
        for primitive, multiplier in examples:
            target = (multiplier * primitive[0], multiplier * primitive[1])
            base = parallel_direction_cover_certificate(primitive, 8)
            self.assertIsNotNone(base, primitive)
            cert = parallel_direction_primitive_ray_certificate(target, 8)
            self.assertEqual(cert, scale_certificate(base, multiplier))
            self.assertEqual(cert.target, target)
            self.assertTrue(cert.valid())

            base_witness = parallel_direction_cover_witness(primitive, 8)
            self.assertIsNotNone(base_witness, primitive)
            lifted_witness = parallel_direction_primitive_ray_witness(target, 8)
            self.assertEqual(
                lifted_witness,
                PrimitiveRayParallelDirectionWitness(
                    target=target,
                    primitive=primitive,
                    scale=multiplier,
                    base_witness=base_witness,
                ),
            )
            self.assertEqual(lifted_witness.certificate, cert)

        witness = parallel_direction_primitive_ray_witness((23, 23 * 501), 8)
        self.assertIsNotNone(witness)
        self.assertEqual(witness.primitive, (1, 501))
        self.assertEqual(witness.scale, 23)
        self.assertEqual(witness.base_witness.direction, (-4, -3))
        self.assertEqual(witness.base_witness.factor, 3)

        lifted_failures: list[Point] = []
        for g in range(1, 61):
            for h in range(1, 61):
                primitive = (g, h)
                if primitive in KNOWN_DISTANCE_THREE_ORBIT or edge((0, 0), primitive):
                    continue
                if gcd(g, h) != 1:
                    continue

                target = (19 * g, 19 * h)
                cert = parallel_direction_primitive_ray_certificate(target, 8)
                if cert is None or cert.target != target or not cert.valid():
                    lifted_failures.append(target)
        self.assertEqual(tuple(lifted_failures), ())

        with self.assertRaises(ValueError):
            parallel_direction_primitive_ray_certificate((1, 1), 1)
        with self.assertRaises(ValueError):
            parallel_direction_primitive_ray_witness((1, 1), 1)

    def test_pythagorean_triple_orthogonal_lattice_family(self):
        triples = (
            PythagoreanTriple(3, 4, 5),
            PythagoreanTriple(5, 12, 13),
            PythagoreanTriple(8, 15, 17),
            PythagoreanTriple(7, 24, 25),
        )

        for triple in triples:
            leg_a, leg_b = triple.legs
            rotation = (-leg_b, leg_a)
            modulus = triple.hypotenuse * triple.hypotenuse
            self.assertEqual(determinant((leg_a, leg_b), rotation), modulus)

            for r in range(-5, 6):
                for s in range(-5, 6):
                    if r == 0 and s == 0:
                        continue

                    target = (
                        r * leg_a - s * leg_b,
                        r * leg_b + s * leg_a,
                    )
                    self.assertEqual(
                        lattice_coefficients(target, (leg_a, leg_b), rotation),
                        (r, s),
                    )

                    cert = pythagorean_triple_orthogonal_lattice_certificate(
                        target,
                        triple,
                    )
                    if r == 0 or s == 0:
                        self.assertIsNone(cert)
                        self.assertTrue(edge((0, 0), target))
                    else:
                        self.assertIsNotNone(cert)
                        self.assertEqual(cert.target, target)
                        self.assertEqual(cert.midpoint, (r * leg_a, r * leg_b))
                        self.assertTrue(cert.valid())

            for g in range(-70, 71):
                for h in range(-70, 71):
                    target = (g, h)
                    if target == (0, 0):
                        continue

                    covered = (
                        (leg_a * g + leg_b * h) % modulus == 0
                        and (leg_a * h - leg_b * g) % modulus == 0
                    )
                    cert = pythagorean_triple_orthogonal_lattice_certificate(
                        target,
                        triple,
                    )
                    if not covered:
                        self.assertIsNone(cert)
                    elif cert is None:
                        self.assertTrue(edge((0, 0), target))
                    else:
                        self.assertEqual(cert.target, target)
                        self.assertTrue(cert.valid())

        with self.assertRaises(ValueError):
            pythagorean_triple_orthogonal_lattice_certificate(
                (1, 1),
                PythagoreanTriple(1, 1, 2),
            )

    def test_pythagorean_orthogonal_lattice_cover(self):
        examples = (
            ((1, 38), (-15, 8), (-15, 8)),
            ((2, 29), (-12, -5), (12, 5)),
            ((22, 19), (-12, 5), (12, -5)),
            ((29, 2), (-12, 5), (24, -10)),
            ((38, 1), (-15, -8), (30, 16)),
        )
        for target, direction, midpoint in examples:
            witness = pythagorean_orthogonal_lattice_witness(target, 4)
            self.assertIsNotNone(witness)
            self.assertEqual(witness.first_direction, direction)
            self.assertEqual(witness.second_direction, (-direction[1], direction[0]))
            self.assertEqual(witness.midpoint, midpoint)
            self.assertTrue(witness.certificate.valid())
            certificate = pythagorean_orthogonal_lattice_cover_certificate(target, 4)
            self.assertIsNotNone(certificate)
            self.assertEqual(certificate.target, target)
            self.assertEqual(certificate.midpoint, midpoint)
            self.assertTrue(certificate.valid())
            self.assertEqual(certificate, witness.certificate)
            self.assertEqual(
                lattice_two_step_certificate(
                    target,
                    direction,
                    (-direction[1], direction[0]),
                ),
                certificate,
            )

        residual_covered: list[Point] = []
        residual_uncovered: list[Point] = []
        for g in range(1, 51):
            for h in range(1, 51):
                target = (g, h)
                if target in KNOWN_DISTANCE_THREE_ORBIT or edge((0, 0), target):
                    continue
                if gcd(g, h) != 1:
                    continue
                if parallel_direction_promoted_345_factor_certificate(target) is not None:
                    continue

                certificate = pythagorean_orthogonal_lattice_cover_certificate(target, 4)
                if certificate is None:
                    residual_uncovered.append(target)
                else:
                    self.assertTrue(certificate.valid())
                    residual_covered.append(target)

        self.assertEqual(
            tuple(residual_covered),
            (
                (1, 38),
                (2, 29),
                (19, 22),
                (22, 19),
                (22, 31),
                (29, 2),
                (31, 22),
                (38, 1),
            ),
        )
        self.assertEqual(len(residual_uncovered), 60)
        self.assertEqual(
            tuple(residual_uncovered[:8]),
            (
                (2, 49),
                (5, 14),
                (5, 26),
                (5, 34),
                (5, 46),
                (7, 10),
                (7, 50),
                (8, 9),
            ),
        )

        self.assertIsNone(pythagorean_orthogonal_lattice_cover_certificate((1, 38), 3))
        with self.assertRaises(ValueError):
            pythagorean_orthogonal_lattice_cover_certificate((1, 1), 1)

    def test_pythagorean_lattice_pair_cover_closes_promoted_residual_tail(self):
        pairs = pythagorean_lattice_direction_pairs(25, 1435)
        self.assertEqual(len(pairs), 38240)
        self.assertIn(((-21, -20), (-40, 9)), pairs)
        self.assertIn(((-15, 8), (-644, 333)), pairs)
        self.assertNotIn(((-4, 3), (4, -3)), pairs)

        examples = (
            ((2, 49), (-21, -20), (-40, 9), 989, (-2, 1), (42, 40)),
            ((10, 13), (-15, -8), (-340, -189), 115, (22, -1), (-330, -176)),
            ((10, 47), (-15, 8), (-644, 333), 157, (214, -5), (-3210, 1712)),
            ((14, 25), (-91, -60), (-168, -95), 1435, (-2, 1), (182, 120)),
            ((17, 50), (-12, -5), (-391, -120), 515, (-34, 1), (408, 170)),
            ((25, 26), (-45, -28), (-440, -279), 235, (19, -2), (-855, -532)),
            ((50, 17), (-5, -12), (-120, -391), 515, (-34, 1), (170, 408)),
        )
        for (
            target,
            first_direction,
            second_direction,
            determinant_value,
            coefficients,
            midpoint,
        ) in examples:
            witness = pythagorean_lattice_pair_witness(target, 25, 1435)
            self.assertEqual(
                witness,
                PythagoreanLatticePairWitness(
                    target=target,
                    first_direction=first_direction,
                    second_direction=second_direction,
                    determinant=determinant_value,
                    first_coefficient=coefficients[0],
                    second_coefficient=coefficients[1],
                ),
            )
            self.assertEqual(witness.midpoint, midpoint)
            self.assertTrue(witness.certificate.valid())
            self.assertEqual(
                pythagorean_lattice_pair_cover_certificate(target, 25, 1435),
                witness.certificate,
            )

        strip_direction = (-12, -5)
        strip_modulus = 13
        strip_residue = 7
        first_direction = (-4, -3)
        second_direction = (-3, -4)
        self.assertEqual(
            pythagorean_lattice_pair_strip_linear_congruence(
                strip_direction,
                strip_modulus,
                strip_residue,
                first_direction,
                second_direction,
            ),
            (3, 7, 7, 13, 1),
        )
        self.assertEqual(two_variable_linear_congruence_gcd(3, 7, 7, 13), (1, True))
        self.assertEqual(
            two_variable_linear_congruence_gcd(18, 18, 30, 34),
            (2, True),
        )
        self.assertEqual(
            two_variable_linear_congruence_gcd(4, 6, 5, 12),
            (2, False),
        )
        self.assertEqual(two_variable_linear_congruence_gcd(0, 0, 0, 9), (9, True))
        self.assertEqual(two_variable_linear_congruence_gcd(0, 0, 4, 9), (9, False))
        self.assertEqual(
            two_variable_linear_congruence_gcd(0, 12, -18, 30),
            (6, True),
        )
        self.assertEqual(
            two_variable_linear_congruence_gcd(2**70, 2**69, 2**68 + 1, 2**66),
            (2**66, False),
        )
        with self.assertRaises(ValueError):
            two_variable_linear_congruence_gcd(1, 2, 3, 0)

        def brute_pair_solvable(
            first_step: int,
            second_step: int,
            first_residue: int,
            first_modulus: int,
            second_residue: int,
            second_modulus: int,
        ) -> bool:
            coefficient_period = lcm(first_modulus, second_modulus)
            return any(
                (
                    (first_step * r + second_step * s - first_residue)
                    % first_modulus
                    == 0
                    and (
                        first_step * r + second_step * s - second_residue
                    )
                    % second_modulus
                    == 0
                )
                for r in range(coefficient_period)
                for s in range(coefficient_period)
            )

        pair_rows = (
            ((3, 7, 7, 13, 2, 5), (1, 65, 1, 7, True, True)),
            ((4, 6, 2, 8, 5, 12), (4, 24, 2, None, False, False)),
            ((4, 6, 1, 4, 1, 6), (2, 12, 2, 1, True, False)),
            ((0, 0, 0, 4, 0, 6), (2, 12, 12, 0, True, True)),
            ((0, 0, 1, 4, 1, 6), (2, 12, 12, 1, True, False)),
        )
        for args, expected in pair_rows:
            self.assertEqual(two_variable_linear_congruence_pair_data(*args), expected)
            combined_residue = expected[3]
            if combined_residue is None:
                self.assertFalse(expected[4])
            else:
                self.assertEqual(combined_residue % args[3], args[2] % args[3])
                self.assertEqual(combined_residue % args[5], args[4] % args[5])
                self.assertEqual(expected[-1], combined_residue % expected[2] == 0)
                for shift in (-2, -1, 0, 1, 3):
                    shifted_witness = combined_residue + shift * expected[1]
                    self.assertEqual(shifted_witness % args[3], args[2] % args[3])
                    self.assertEqual(shifted_witness % args[5], args[4] % args[5])
                    self.assertEqual(
                        expected[-1],
                        shifted_witness % expected[2] == 0,
                    )
            self.assertEqual(expected[-1], brute_pair_solvable(*args))
        self.assertEqual(
            two_variable_linear_congruence_pair_data(
                2**70,
                2**69,
                1,
                4,
                1,
                6,
            ),
            (2, 12, 4, 1, True, False),
        )
        with self.assertRaises(ValueError):
            two_variable_linear_congruence_pair_data(1, 2, 3, 0, 5, 7)

        strip_crt_data = pythagorean_lattice_pair_strip_crt_data(
            strip_direction,
            13,
            7,
            5,
            2,
            first_direction,
            second_direction,
        )
        self.assertEqual(strip_crt_data, (16, 33, 1, 65, 1, 7, True, True))
        self.assertEqual(
            strip_crt_data[2:],
            two_variable_linear_congruence_pair_data(16, 33, 7, 13, 2, 5),
        )
        self.assertEqual(
            pythagorean_lattice_pair_same_strip_combined_linear_congruence(
                strip_direction,
                13,
                7,
                5,
                2,
                first_direction,
                second_direction,
            ),
            (16, 33, 7, 65, 1),
        )
        self.assertEqual(
            pythagorean_lattice_pair_same_strip_intersection_residue_count(
                strip_direction,
                13,
                7,
                5,
                2,
                first_direction,
                second_direction,
            ),
            (455, 455),
        )
        self.assertEqual(
            pythagorean_lattice_pair_strip_crt_data(
                strip_direction,
                10,
                7,
                15,
                8,
                first_direction,
                second_direction,
            ),
            (16, 33, 5, 30, 1, None, False, False),
        )
        self.assertEqual(
            pythagorean_lattice_pair_same_strip_combined_linear_congruence(
                strip_direction,
                10,
                7,
                15,
                8,
                first_direction,
                second_direction,
            ),
            None,
        )
        self.assertEqual(
            pythagorean_lattice_pair_same_strip_intersection_residue_count(
                strip_direction,
                10,
                7,
                15,
                8,
                first_direction,
                second_direction,
            ),
            (210, 0),
        )
        self.assertEqual(
            pythagorean_lattice_pair_strip_crt_data(
                (-8, -15),
                4,
                1,
                6,
                1,
                (-4, 3),
                (-12, 5),
            ),
            (-84, -220, 2, 12, 4, 1, True, False),
        )
        self.assertEqual(
            pythagorean_lattice_pair_same_strip_combined_linear_congruence(
                (-8, -15),
                4,
                1,
                6,
                1,
                (-4, 3),
                (-12, 5),
            ),
            (0, 8, 1, 12, 4),
        )
        self.assertEqual(
            pythagorean_lattice_pair_same_strip_intersection_residue_count(
                (-8, -15),
                4,
                1,
                6,
                1,
                (-4, 3),
                (-12, 5),
            ),
            (48, 0),
        )
        scale = 2**63
        self.assertEqual(
            pythagorean_lattice_pair_strip_crt_data(
                (3 * scale, 4 * scale),
                4,
                0,
                6,
                0,
                (3, 4),
                (5, 12),
            ),
            (0, 16 * scale, 2, 12, 4, 0, True, True),
        )
        self.assertEqual(
            pythagorean_lattice_pair_same_strip_combined_linear_congruence(
                (3 * scale, 4 * scale),
                4,
                0,
                6,
                0,
                (3, 4),
                (5, 12),
            ),
            (0, 8, 0, 12, 4),
        )
        self.assertEqual(
            pythagorean_lattice_pair_same_strip_intersection_residue_count(
                (3 * scale, 4 * scale),
                4,
                0,
                6,
                0,
                (3, 4),
                (5, 12),
            ),
            (48, 48),
        )
        with self.assertRaises(ValueError):
            pythagorean_lattice_pair_strip_crt_data(
                (1, 1),
                13,
                7,
                5,
                2,
                first_direction,
                second_direction,
            )
        self.assertEqual(
            pythagorean_lattice_pair_strip_intersection_residue_count(
                strip_direction,
                strip_modulus,
                strip_residue,
                first_direction,
                second_direction,
            ),
            (91, 91),
        )
        self.assertTrue(
            pythagorean_lattice_pair_strip_intersection_holds(
                (5, 86),
                strip_direction,
                strip_modulus,
                strip_residue,
                first_direction,
                second_direction,
            )
        )
        self.assertFalse(
            pythagorean_lattice_pair_strip_intersection_holds(
                (-7, -7),
                strip_direction,
                strip_modulus,
                strip_residue,
                first_direction,
                second_direction,
            )
        )
        brute_force_count = 0
        for g in range(91):
            for h in range(91):
                if pythagorean_lattice_pair_strip_intersection_holds(
                    (g, h),
                    strip_direction,
                    strip_modulus,
                    strip_residue,
                    first_direction,
                    second_direction,
                ):
                    brute_force_count += 1
        self.assertEqual(brute_force_count, 91)

        self.assertEqual(
            pythagorean_lattice_pair_strip_linear_congruence(
                (-8, -15),
                34,
                30,
                (-4, 3),
                (-12, 5),
            ),
            (18, 18, 30, 34, 2),
        )
        self.assertEqual(
            pythagorean_lattice_pair_strip_intersection_residue_count(
                (-8, -15),
                34,
                30,
                (-4, 3),
                (-12, 5),
            ),
            (272, 272),
        )
        self.assertTrue(
            pythagorean_lattice_pair_strip_intersection_holds(
                (28, 19),
                (-8, -15),
                34,
                30,
                (-4, 3),
                (-12, 5),
            )
        )

        residual_covered: list[Point] = []
        residual_uncovered: list[Point] = []
        for g in range(1, 51):
            for h in range(1, 51):
                target = (g, h)
                if target in KNOWN_DISTANCE_THREE_ORBIT or edge((0, 0), target):
                    continue
                if gcd(g, h) != 1:
                    continue
                if parallel_direction_promoted_345_factor_certificate(target) is not None:
                    continue
                if pythagorean_orthogonal_lattice_cover_certificate(target, 4) is not None:
                    continue

                certificate = pythagorean_lattice_pair_cover_certificate(target, 25, 1435)
                if certificate is None:
                    residual_uncovered.append(target)
                else:
                    self.assertTrue(certificate.valid())
                    residual_covered.append(target)

        self.assertEqual(len(residual_covered), 60)
        self.assertEqual(tuple(residual_uncovered), ())

        larger_sample_misses: list[Point] = []
        for g in range(1, 101):
            for h in range(1, 101):
                target = (g, h)
                if target in KNOWN_DISTANCE_THREE_ORBIT or edge((0, 0), target):
                    continue
                if gcd(g, h) != 1:
                    continue
                if parallel_direction_promoted_345_factor_certificate(target) is not None:
                    continue
                if pythagorean_orthogonal_lattice_cover_certificate(target, 4) is not None:
                    continue
                if pythagorean_lattice_pair_cover_certificate(target, 25, 1435) is not None:
                    continue
                larger_sample_misses.append(target)

        self.assertEqual(
            tuple(larger_sample_misses),
            ((29, 98), (50, 53), (53, 50), (98, 29)),
        )

        self.assertIsNone(pythagorean_lattice_pair_cover_certificate((50, 53), 25, 1435))
        with self.assertRaises(ValueError):
            pythagorean_lattice_direction_pairs(1, 1435)
        with self.assertRaises(ValueError):
            pythagorean_lattice_direction_pairs(25, 0)

    def test_pythagorean_layered_structural_cover_closes_sample_to_300(self):
        self.assertEqual(PYTHAGOREAN_LAYERED_ORTHOGONAL_MAX_PARAMETER, 4)
        self.assertEqual(PYTHAGOREAN_LAYERED_LATTICE_PAIR_MAX_PARAMETER, 25)
        self.assertEqual(PYTHAGOREAN_LAYERED_LATTICE_PAIR_MAX_DETERMINANT, 1435)
        self.assertEqual(PYTHAGOREAN_LAYERED_STANDARD_COMPLETION_MAX_PARAMETER, 8)

        standard_tail_examples = (
            ((29, 98), (61944, -25810)),
            ((50, 53), (4110, 2192)),
            ((53, 50), (2192, 4110)),
            ((98, 29), (-25810, 61944)),
        )
        for target, midpoint in standard_tail_examples:
            certificate = pythagorean_layered_structural_certificate(target)
            self.assertIsNotNone(certificate)
            self.assertEqual(certificate.target, target)
            self.assertEqual(certificate.midpoint, midpoint)
            self.assertTrue(certificate.valid())
            self.assertIsNone(pythagorean_lattice_pair_cover_certificate(target, 25, 1435))

        counts = {
            "total": 0,
            "promoted_345": 0,
            "orthogonal": 0,
            "lattice_pair": 0,
            "standard_completion": 0,
        }
        for g in range(1, 301):
            for h in range(1, 301):
                target = (g, h)
                if target in KNOWN_DISTANCE_THREE_ORBIT or edge((0, 0), target):
                    continue
                if gcd(g, h) != 1:
                    continue

                counts["total"] += 1
                certificate = pythagorean_layered_structural_certificate(target)
                self.assertIsNotNone(certificate, target)
                self.assertTrue(certificate.valid())

                if parallel_direction_promoted_345_factor_certificate(target) is not None:
                    counts["promoted_345"] += 1
                elif pythagorean_orthogonal_lattice_cover_certificate(target, 4) is not None:
                    counts["orthogonal"] += 1
                elif pythagorean_lattice_pair_cover_certificate(target, 25, 1435) is not None:
                    counts["lattice_pair"] += 1
                else:
                    self.assertIsNotNone(
                        parallel_direction_standard_completion_cover_certificate(target, 8),
                        target,
                    )
                    counts["standard_completion"] += 1

        self.assertEqual(
            counts,
            {
                "total": 54685,
                "promoted_345": 52549,
                "orthogonal": 40,
                "lattice_pair": 2032,
                "standard_completion": 64,
            },
        )
        self.assertIsNone(pythagorean_layered_structural_certificate((2, 1)))

    @pytest.mark.perf
    def test_pythagorean_layered_split_cover_closes_sample_to_1000(self):
        self.assertEqual(PYTHAGOREAN_LAYERED_SPLIT_MAX_SQUARECLASS, 23)
        self.assertEqual(PYTHAGOREAN_LAYERED_SPLIT_MAX_FACTOR, 179)
        self.assertEqual(PYTHAGOREAN_LAYERED_PARALLEL_MAX_PARAMETER, 8)
        self.assertEqual(PYTHAGOREAN_LAYERED_CONJUGATE_ROOT_MAX_COORDINATE, 8)

        structural_misses: list[Point] = []
        split_examples = {
            (139, 878): ((8, 15), 1, 11, 449, (3184, 5970)),
            (151, 338): ((-9, 40), 2, 19, 239, (-369, 1640)),
            (398, 751): ((-35, 12), 1, 89, 349, (-1330, 456)),
            (850, 887): ((21, -20), 23, 1, 1549, (689010, -656200)),
        }
        counts = {"total": 0, "structural": 0, "split": 0}
        for g in range(1, 1001):
            for h in range(1, 1001):
                target = (g, h)
                if target in KNOWN_DISTANCE_THREE_ORBIT or edge((0, 0), target):
                    continue
                if gcd(g, h) != 1:
                    continue

                counts["total"] += 1
                structural = pythagorean_layered_structural_certificate(target)
                certificate = pythagorean_layered_split_certificate(target)
                conjugate_ideal = pythagorean_layered_conjugate_ideal_certificate(target)
                self.assertIsNotNone(certificate, target)
                self.assertTrue(certificate.valid())
                self.assertIsNotNone(conjugate_ideal, target)
                self.assertTrue(conjugate_ideal.valid())
                self.assertEqual(
                    pythagorean_layered_parallel_certificate(target),
                    conjugate_ideal,
                )

                if structural is None:
                    structural_misses.append(target)
                    split_witness = parallel_direction_squareclass_split_cover_witness(
                        target,
                        8,
                        23,
                        179,
                    )
                    self.assertIsNotNone(split_witness, target)
                    self.assertEqual(certificate, split_witness.certificate)
                    exact_direction_split = parallel_direction_conjugate_ideal_cover_certificate(
                        target,
                        8,
                    )
                    self.assertIsNotNone(exact_direction_split, target)
                    self.assertTrue(exact_direction_split.valid())
                    exact_root_split = parallel_direction_conjugate_ideal_root_cover_certificate(
                        target,
                        8,
                    )
                    self.assertEqual(exact_root_split, exact_direction_split)
                    exact_shape_split = (
                        parallel_direction_conjugate_ideal_root_spine_cover_certificate(
                            target,
                            8,
                        )
                    )
                    self.assertIsNotNone(exact_shape_split, target)
                    self.assertTrue(exact_shape_split.valid())
                    counts["split"] += 1
                    if target in split_examples:
                        direction, squareclass, split_factor, paired_split_factor, midpoint = (
                            split_examples[target]
                        )
                        self.assertEqual(split_witness.direction, direction)
                        self.assertEqual(split_witness.squareclass, squareclass)
                        self.assertEqual(split_witness.split_factor, split_factor)
                        self.assertEqual(split_witness.paired_split_factor, paired_split_factor)
                        self.assertEqual(split_witness.midpoint, midpoint)
                else:
                    self.assertEqual(certificate, structural)
                    self.assertEqual(conjugate_ideal, structural)
                    counts["structural"] += 1

        self.assertEqual(
            tuple(structural_misses),
            (
                (139, 878),
                (151, 338),
                (158, 391),
                (169, 878),
                (218, 611),
                (262, 601),
                (265, 346),
                (325, 334),
                (334, 325),
                (338, 151),
                (346, 265),
                (370, 403),
                (391, 158),
                (398, 751),
                (403, 370),
                (482, 611),
                (530, 713),
                (559, 842),
                (601, 262),
                (611, 218),
                (611, 482),
                (658, 809),
                (710, 757),
                (713, 530),
                (734, 845),
                (751, 398),
                (757, 710),
                (809, 658),
                (842, 559),
                (845, 734),
                (850, 887),
                (878, 139),
                (878, 169),
                (887, 850),
            ),
        )
        self.assertEqual(
            counts,
            {
                "total": 608023,
                "structural": 607989,
                "split": 34,
            },
        )
        self.assertEqual(
            parallel_direction_conjugate_ideal_root_cover_census(500, 8),
            ParallelDirectionConjugateIdealRootCoverCensus(
                max_coordinate=500,
                max_root_coordinate=8,
                target_count=152049,
                structural_miss_count=10,
                uncovered_targets=(),
                root_counts=(
                    ((-4, -5), 1),
                    ((-4, 5), 1),
                    ((-3, -8), 1),
                    ((-3, 8), 1),
                    ((-2, -5), 1),
                    ((-2, -3), 1),
                    ((-2, 3), 1),
                    ((-2, 5), 1),
                    ((-1, -4), 1),
                    ((-1, 4), 1),
                ),
                root_shape_counts=(
                    ((1, 4), 2),
                    ((2, 3), 2),
                    ((2, 5), 2),
                    ((3, 8), 2),
                    ((4, 5), 2),
                ),
                squareclass_counts=((1, 4), (2, 4), (10, 2)),
                direction_counts=(
                    ((-55, 48), 1),
                    ((-48, 55), 1),
                    ((-40, 9), 1),
                    ((-21, 20), 1),
                    ((-20, 21), 1),
                    ((-15, -8), 1),
                    ((-12, -5), 1),
                    ((-9, 40), 1),
                    ((-8, -15), 1),
                    ((-5, -12), 1),
                ),
            ),
        )
        self.assertEqual(
            parallel_direction_conjugate_ideal_root_spine_cover_census(
                1000,
                8,
            ),
            ParallelDirectionConjugateIdealRootShapeCoverCensus(
                max_coordinate=1000,
                root_shapes=(
                    (1, 2),
                    (2, 3),
                    (1, 4),
                    (3, 4),
                    (2, 5),
                    (1, 6),
                    (4, 5),
                    (2, 7),
                    (1, 8),
                    (3, 8),
                ),
                target_count=608023,
                structural_miss_count=34,
                uncovered_targets=(),
                root_shape_counts=(
                    ((2, 3), 8),
                    ((1, 4), 6),
                    ((1, 6), 6),
                    ((2, 5), 4),
                    ((2, 7), 4),
                    ((3, 8), 4),
                    ((4, 5), 2),
                ),
                squareclass_counts=((1, 18), (2, 6), (10, 4), (7, 2), (13, 2), (23, 2)),
                direction_counts=(
                    ((-15, -8), 3),
                    ((-8, -15), 3),
                    ((-45, 28), 2),
                    ((-35, 12), 2),
                    ((-28, 45), 2),
                    ((-21, 20), 2),
                    ((-20, 21), 2),
                    ((-12, -5), 2),
                    ((-12, 5), 2),
                    ((-12, 35), 2),
                    ((-5, -12), 2),
                    ((-5, 12), 2),
                    ((-55, -48), 1),
                    ((-55, 48), 1),
                    ((-48, -55), 1),
                    ((-48, 55), 1),
                    ((-40, 9), 1),
                    ((-35, -12), 1),
                    ((-12, -35), 1),
                    ((-9, 40), 1),
                ),
            ),
        )

    def test_divisor_obligation_discharge_witnesses(self):
        obligations = tuple(
            row[:-1]
            for row in parallel_direction_conjugate_ideal_root_spine_divisor_obligation_census(
                500,
                8,
            ).obligation_counts
        )
        self.assertEqual(obligations, PINNED_ROOT_SPINE_DIVISOR_OBLIGATIONS)

        divisor_witness = (
            parallel_direction_conjugate_ideal_divisor_obligation_discharge_witness(
                (151, 338),
                (-9, 40),
                PINNED_ROOT_SPINE_DIVISOR_OBLIGATIONS[6],
            )
        )
        self.assertIsNotNone(divisor_witness)
        self.assertEqual(divisor_witness.branch, "divisor")
        self.assertEqual(divisor_witness.determinant_leg, -9082)
        self.assertEqual(divisor_witness.quotient, 4541)
        self.assertIsNone(divisor_witness.structural_row)
        self.assertIsNotNone(divisor_witness.exponent_profile)
        self.assertEqual(divisor_witness.exponent_profile.saturation_branch, "short_success")
        self.assertEqual(divisor_witness.exponent_profile.required_exponent, 9)
        self.assertEqual(divisor_witness.exponent_profile.exponent_closure, (0, 9, 19, 28))

        fallback_examples = (
            (
                "promoted_345",
                (1, 15),
                (-12, -5),
                ((-4, -3), 1, 43, 0, 1, 650),
            ),
            (
                "lattice_pair",
                (2, 49),
                (-12, -5),
                ((-21, -20), (-40, 9), 989, 5, 4, 7, 13, 1),
            ),
            (
                "orthogonal",
                (38, 1),
                (-5, 12),
                ((-15, -8), (8, -15), 289, 12, 5, 7, 13, 1),
            ),
            (
                "standard_completion",
                (119, 62),
                (-12, -5),
                ((-21, -20), 0, 1078, 466, 3364, 1078, 0, 1, 43732),
            ),
        )
        for branch, target, direction, row in fallback_examples:
            with self.subTest(branch=branch):
                witness = (
                    parallel_direction_conjugate_ideal_divisor_obligation_discharge_witness(
                        target,
                        direction,
                        PINNED_ROOT_SPINE_DIVISOR_OBLIGATIONS[0],
                    )
                )
                self.assertIsNotNone(witness)
                self.assertEqual(witness.branch, branch)
                self.assertEqual(witness.structural_row, row)
                self.assertIsNotNone(witness.exponent_profile)
                self.assertEqual(witness.exponent_profile.saturation_branch, "short_failure")

        profile = parallel_direction_conjugate_ideal_divisor_obligation_exponent_profile(
            (1, 15),
            (-12, -5),
            PINNED_ROOT_SPINE_DIVISOR_OBLIGATIONS[0],
        )
        self.assertIsNotNone(profile)
        self.assertEqual(profile.modulus, 13)
        self.assertEqual(profile.generator, 2)
        self.assertEqual(profile.required_exponent, 7)
        self.assertEqual(profile.effective_length, 3)
        self.assertEqual(profile.kneser_lower_bound, 4)
        self.assertEqual(profile.saturation_gap, 8)
        self.assertEqual(profile.saturation_branch, "short_failure")
        self.assertEqual(
            global_root_choice_short_exponent_signature(profile),
            (13, 7, False, 3, ((0, 1), (0, 9), (0, 1))),
        )

    def test_pinned_strip_local_discharge_counterexample(self):
        target, direction, obligation = PINNED_STRIP_LOCAL_DISCHARGE_COUNTEREXAMPLE
        self.assertEqual(target, (108638, 24031))
        self.assertEqual(direction, (-40, -9))
        self.assertEqual(obligation, PINNED_ROOT_SPINE_DIVISOR_OBLIGATIONS[6])
        self.assertTrue(
            parallel_direction_conjugate_ideal_divisor_obligation_strip_holds(
                target,
                direction,
                obligation,
            )
        )
        self.assertFalse(
            parallel_direction_conjugate_ideal_divisor_obligation_divisor_holds(
                target,
                direction,
                obligation,
            )
        )
        self.assertIsNone(
            parallel_direction_conjugate_ideal_divisor_obligation_discharge_witness(
                target,
                direction,
                obligation,
            )
        )
        self.assertIsNone(pythagorean_layered_structural_label(target))

        global_discharge = (
            parallel_direction_conjugate_ideal_divisor_obligation_global_discharge_witness(
                target,
                direction,
                obligation,
            )
        )
        self.assertIsNotNone(global_discharge)
        self.assertEqual(global_discharge.branch, "alternate_root_spine")
        self.assertEqual(global_discharge.determinant_leg, 16502)
        self.assertEqual(global_discharge.quotient, 8251)
        self.assertEqual(global_discharge.exponent_profile.saturation_branch, "short_failure")

        alternate_witness = parallel_direction_conjugate_ideal_root_spine_cover_witness(
            target,
            8,
        )
        self.assertIsNotNone(alternate_witness)
        self.assertTrue(alternate_witness.certificate.valid())
        self.assertEqual(alternate_witness.direction, (-3, 4))
        self.assertEqual(alternate_witness.root_shape, (1, 2))
        self.assertEqual(alternate_witness.squareclass, 535)
        self.assertEqual(alternate_witness.split_factor, 1)
        self.assertEqual(alternate_witness.signed_paired_split_factor, -947)
        self.assertEqual(alternate_witness.beta, (-379, 189))
        promoted_certificate = promoted_root_spine_line_certificate_from_witness(
            alternate_witness
        )
        self.assertIsNotNone(promoted_certificate)
        self.assertEqual(promoted_certificate, alternate_witness.certificate)
        self.assertEqual(
            global_discharge.structural_row,
            ((-3, 4), (1, 2), 535, 1, -947, (-379, 189), 9586654),
        )
        proved_discharge = (
            parallel_direction_conjugate_ideal_divisor_obligation_proved_signature_template_discharge_witness(
                target,
                direction,
                obligation,
                GLOBAL_ROOT_CHOICE_PROVED_SIGNATURE_TEMPLATE_ROWS,
            )
        )
        self.assertIsNotNone(proved_discharge)
        self.assertEqual(proved_discharge.branch, "alternate_proved_signature_template")
        self.assertEqual(proved_discharge.structural_row, global_discharge.structural_row)
        self.assertEqual(proved_discharge.determinant_leg, global_discharge.determinant_leg)
        self.assertEqual(proved_discharge.quotient, global_discharge.quotient)
        counterexample_signature_template = global_root_choice_branch_row_signature_template(
            DivisorObligationGlobalRootChoiceBranchAuditRow(
                target=target,
                direction=direction,
                obligation=obligation,
                branch=proved_discharge.branch,
                structural_row=proved_discharge.structural_row,
            )
        )
        self.assertEqual(
            counterexample_signature_template,
            (41, 9, False, 2, ((0, 32), (0, 16)), (-3, 4), 535, 1, -947, 50, 3),
        )
        self.assertIn(
            counterexample_signature_template,
            GLOBAL_ROOT_CHOICE_PROVED_SIGNATURE_TEMPLATE_ROWS,
        )
        self.assertEqual(
            parallel_direction_conjugate_ideal_divisor_obligation_key(
                alternate_witness
            ),
            ((1, 2), 535, 5, 3, 3, 1, 1),
        )
        self.assertEqual(
            pythagorean_layered_parallel_certificate(target),
            alternate_witness.certificate,
        )

    @pytest.mark.perf
    def test_pinned_strip_global_root_choice_coverage(self):
        max_coordinate = 500
        finite_root_shape_exceptions = {
            (151, 338),
            (158, 391),
            (338, 151),
            (391, 158),
        }
        primary_root_shape_families = {
            (1, 2),
            (1, 4),
            (2, 3),
            (2, 5),
        }
        exceptional_secondary_shapes = {
            (3, 8),
            (4, 5),
        }

        for obligation in PINNED_ROOT_SPINE_DIVISOR_OBLIGATIONS:
            for direction in parallel_direction_conjugate_ideal_divisor_obligation_directions(
                obligation
            ):
                for g in range(1, max_coordinate + 1):
                    for h in range(1, max_coordinate + 1):
                        target = (g, h)
                        if target in KNOWN_DISTANCE_THREE_ORBIT or edge((0, 0), target):
                            continue
                        if gcd(g, h) != 1:
                            continue
                        if not parallel_direction_conjugate_ideal_divisor_obligation_strip_holds(
                            target,
                            direction,
                            obligation,
                        ):
                            continue
                        if parallel_direction_conjugate_ideal_divisor_obligation_divisor_holds(
                            target,
                            direction,
                            obligation,
                        ):
                            continue

                        local_witness = (
                            parallel_direction_conjugate_ideal_divisor_obligation_discharge_witness(
                                target,
                                direction,
                                obligation,
                            )
                        )
                        if local_witness is not None:
                            continue

                        global_witness = parallel_direction_conjugate_ideal_divisor_obligation_global_discharge_witness(
                            target,
                            direction,
                            obligation,
                        )
                        self.assertIsNotNone(
                            global_witness,
                            msg=f"no global branch for {target} with U={direction} on {obligation}",
                        )
                        table_witness = pinned_global_root_choice_table_witness(
                            target,
                            direction,
                            obligation,
                        )
                        expected_branch = (
                            "alternate_root_spine_table"
                            if table_witness is not None
                            else "alternate_root_spine"
                        )
                        self.assertEqual(
                            global_witness.branch,
                            expected_branch,
                            msg=f"non-local discharge used wrong root-spine branch for {target} with U={direction} on {obligation}",
                        )
                        self.assertIsNotNone(
                            global_witness.structural_row,
                            msg=f"alternate root spine missing data for {target} with U={direction} on {obligation}",
                        )
                        alternate_witness = parallel_direction_conjugate_ideal_root_spine_cover_witness(
                            target,
                            8,
                        )
                        self.assertIsNotNone(alternate_witness)
                        self.assertEqual(
                            promoted_root_spine_line_certificate_from_witness(
                                alternate_witness
                            ),
                            alternate_witness.certificate,
                            msg=(
                                f"alternate root spine not reconstructed by promoted line "
                                f"for {target} with U={direction} on {obligation}"
                            ),
                        )
                        alternate_root_shape = gaussian_root_shape(global_witness.structural_row[1])
                        if target in finite_root_shape_exceptions:
                            self.assertIn(
                                alternate_root_shape,
                                exceptional_secondary_shapes,
                                msg=(
                                    f"expected exceptional secondary family for {target} with "
                                    f"U={direction} on {obligation}"
                                ),
                            )
                            continue
                        self.assertIn(
                            alternate_root_shape,
                            primary_root_shape_families,
                            msg=(
                                f"unexpected global branch {alternate_root_shape} for {target} with "
                                f"U={direction} on {obligation}"
                            ),
                        )

    @pytest.mark.perf
    def test_pinned_strip_global_root_choice_audit_rows(self):
        branch_audit = parallel_direction_conjugate_ideal_global_root_choice_branch_audit(
            500
        )
        self.assertEqual(branch_audit.checked_strip_failures, 105337)
        self.assertEqual(branch_audit.local_discharge_count, 105323)
        self.assertEqual(branch_audit.global_discharge_count, 14)
        self.assertEqual(
            branch_audit.local_branch_counts,
            (
                ("promoted_345", 100191),
                ("lattice_pair", 4968),
                ("standard_completion", 111),
                ("orthogonal", 53),
            ),
        )
        self.assertEqual(
            branch_audit.global_branch_counts,
            (("alternate_root_spine_table", 14),),
        )
        self.assertEqual(
            branch_audit.global_root_shape_counts,
            (((1, 4), 4), ((2, 5), 4), ((2, 3), 2), ((3, 8), 2), ((4, 5), 2)),
        )
        self.assertEqual(
            branch_audit.global_direction_counts,
            (
                ((-21, 20), 2),
                ((-20, 21), 2),
                ((-15, -8), 2),
                ((-8, -15), 2),
                ((-55, 48), 1),
                ((-48, 55), 1),
                ((-40, 9), 1),
                ((-12, -5), 1),
                ((-9, 40), 1),
                ((-5, -12), 1),
            ),
        )
        self.assertEqual(branch_audit.missing_rows, ())
        self.assertEqual(branch_audit.unreconstructed_rows, ())
        exponent_signature_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_exponent_signature_audit(
                500,
                branch_audit=branch_audit,
            )
        )
        self.assertEqual(exponent_signature_audit.global_row_count, 14)
        self.assertEqual(exponent_signature_audit.missing_row_count, 0)
        self.assertEqual(
            exponent_signature_audit.saturation_branch_counts,
            (("short_failure", 14),),
        )
        self.assertEqual(
            exponent_signature_audit.modulus_counts,
            ((13, 8), (73, 4), (41, 2)),
        )
        self.assertEqual(
            exponent_signature_audit.effective_length_counts,
            ((1, 6), (2, 4), (3, 4)),
        )
        self.assertEqual(
            exponent_signature_audit.summand_count_counts,
            ((1, 6), (2, 6), (3, 2)),
        )
        self.assertEqual(len(exponent_signature_audit.signature_counts), 10)
        self.assertEqual(
            exponent_signature_audit.signature_counts[:4],
            (
                (13, 7, False, 1, ((0, 11),), 2),
                (13, 7, False, 2, ((0, 9), (0, 2)), 2),
                (13, 7, False, 3, ((0, 1), (0, 9), (0, 1)), 2),
                (13, 7, False, 3, ((0, 6, 9), (0, 5)), 2),
            ),
        )
        signature_template_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_signature_template_audit(
                500,
                branch_audit=branch_audit,
            )
        )
        self.assertEqual(signature_template_audit.global_row_count, 14)
        self.assertEqual(signature_template_audit.missing_row_count, 0)
        self.assertEqual(signature_template_audit.signature_count, 10)
        self.assertEqual(signature_template_audit.template_count, 10)
        self.assertEqual(signature_template_audit.signature_template_count, 14)
        self.assertEqual(
            signature_template_audit.signatures_with_multiple_templates,
            (
                (13, 7, False, 1, ((0, 11),), 2),
                (13, 7, False, 2, ((0, 9), (0, 2)), 2),
                (13, 7, False, 3, ((0, 1), (0, 9), (0, 1)), 2),
                (13, 7, False, 3, ((0, 6, 9), (0, 5)), 2),
            ),
        )
        self.assertEqual(
            signature_template_audit.template_counts[:4],
            (
                ((-21, 20), 10, 1, -1583, 29, 12, 2),
                ((-20, 21), 10, 1583, -1, 29, 28, 2),
                ((-15, -8), 2, 241, -5, 17, 12, 2),
                ((-8, -15), 2, 241, 5, 17, 5, 2),
            ),
        )
        signature_template_rows = tuple(
            row[:-1] for row in signature_template_audit.signature_template_counts
        )
        self.assertEqual(
            signature_template_rows,
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_500_SIGNATURE_TEMPLATE_ROWS,
        )
        signature_template_coverage = (
            parallel_direction_conjugate_ideal_global_root_choice_signature_template_coverage_audit(
                500,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_500_SIGNATURE_TEMPLATE_ROWS,
                branch_audit=branch_audit,
            )
        )
        self.assertEqual(signature_template_coverage.global_row_count, 14)
        self.assertEqual(signature_template_coverage.covered_count, 14)
        self.assertEqual(signature_template_coverage.missing_count, 0)
        self.assertEqual(signature_template_coverage.mismatch_count, 0)
        self.assertEqual(signature_template_coverage.missing_root_shape_counts, ())
        self.assertEqual(signature_template_coverage.missing_signature_counts, ())
        self.assertEqual(signature_template_coverage.missing_template_counts, ())
        signature_template_branch_audit = (
            parallel_direction_conjugate_ideal_signature_template_branch_audit(
                500,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_500_SIGNATURE_TEMPLATE_ROWS,
            )
        )
        self.assertEqual(signature_template_branch_audit.checked_strip_failures, 105337)
        self.assertEqual(signature_template_branch_audit.local_discharge_count, 105323)
        self.assertEqual(signature_template_branch_audit.global_discharge_count, 14)
        self.assertEqual(
            signature_template_branch_audit.global_branch_counts,
            (("alternate_signature_template", 14),),
        )
        self.assertEqual(signature_template_branch_audit.missing_rows, ())
        self.assertEqual(signature_template_branch_audit.unreconstructed_rows, ())
        self.assertEqual(
            tuple(
                (row.target, row.direction, row.obligation, row.structural_row)
                for row in signature_template_branch_audit.global_rows
            ),
            tuple(
                (row.target, row.direction, row.obligation, row.structural_row)
                for row in branch_audit.global_rows
            ),
        )
        for row in branch_audit.global_rows:
            witness = global_root_choice_signature_template_witness(
                row.target,
                row.direction,
                row.obligation,
                signature_template_rows,
            )
            self.assertIsNotNone(witness)
            self.assertEqual(
                (
                    witness.direction,
                    witness.squareclass,
                    witness.split_factor,
                    witness.signed_paired_split_factor,
                    witness.beta,
                    witness.first_coefficient,
                ),
                (
                    row.structural_row[0],
                    row.structural_row[2],
                    row.structural_row[3],
                    row.structural_row[4],
                    row.structural_row[5],
                    row.structural_row[6],
                ),
            )

        audit = parallel_direction_conjugate_ideal_global_root_choice_audit(500)
        self.assertEqual(audit.checked_strip_failures, 105337)
        self.assertEqual(audit.local_discharge_count, 105323)
        self.assertEqual(audit.alternate_root_spine_count, 14)
        self.assertEqual(audit.missing_rows, ())
        self.assertEqual(audit.row_family_certificate_miss_rows, ())
        self.assertEqual(audit.strip_intersection_miss_rows, ())
        self.assertEqual(audit.residue_line_miss_rows, ())
        self.assertEqual(audit.unreconstructed_rows, ())
        self.assertEqual(
            audit.alternate_root_shape_counts,
            (((1, 4), 4), ((2, 5), 4), ((2, 3), 2), ((3, 8), 2), ((4, 5), 2)),
        )
        self.assertEqual(
            audit.alternate_direction_counts,
            (
                ((-21, 20), 2),
                ((-20, 21), 2),
                ((-15, -8), 2),
                ((-8, -15), 2),
                ((-55, 48), 1),
                ((-48, 55), 1),
                ((-40, 9), 1),
                ((-12, -5), 1),
                ((-9, 40), 1),
                ((-5, -12), 1),
            ),
        )
        self.assertEqual(
            audit.alternate_residue_period_counts,
            (
                (17, 4),
                (29, 4),
                (146, 2),
                (26, 1),
                (41, 1),
                (338, 1),
                (3362, 1),
            ),
        )
        self.assertEqual(
            audit.alternate_coefficient_modulus_counts,
            ((13, 8), (73, 4), (82, 2)),
        )
        self.assertEqual(audit.distinct_alternate_line_strip_row_count, 14)
        summary = pinned_global_root_choice_alternate_line_strip_summary()
        self.assertEqual(summary.row_count, 14)
        self.assertEqual(summary.distinct_alternate_line_row_count, 10)
        self.assertEqual(summary.distinct_failed_strip_intersection_row_count, 14)
        self.assertEqual(
            summary.obligation_counts,
            (
                (((2, 3), 1, 13, 5, 7, 4, 11), 4),
                (((2, 3), 1, 13, 8, 6, 4, 11), 4),
                (((4, 5), 2, 41, 9, 10, 33, 19), 1),
                (((4, 5), 2, 41, 32, 10, 8, 34), 1),
                (((3, 8), 1, 73, 27, 38, 69, 19), 2),
                (((3, 8), 1, 73, 46, 38, 4, 71), 2),
            ),
        )
        self.assertEqual(
            summary.strip_direction_counts,
            (
                ((5, 12), 2),
                ((12, 5), 2),
                ((-55, 48), 1),
                ((-48, -55), 1),
                ((-48, 55), 1),
                ((-12, -5), 1),
                ((-12, 5), 1),
                ((-5, -12), 1),
                ((5, -12), 1),
                ((9, -40), 1),
                ((40, -9), 1),
                ((55, 48), 1),
            ),
        )
        self.assertEqual(summary.coefficient_modulus_counts, ((13, 8), (73, 4), (82, 2)))
        self.assertTrue(summary.row_table_valid)
        self.assertEqual(
            audit.distinct_alternate_line_row_counts,
            (
                ((-21, 20), 10, 1, 29, 12, 2),
                ((-20, 21), 10, 1583, 29, 28, 2),
                ((-15, -8), 2, 241, 17, 12, 2),
                ((-8, -15), 2, 241, 17, 5, 2),
                ((-55, 48), 1, 1531, 146, 127, 1),
                ((-48, 55), 1, 19, 146, 75, 1),
                ((-40, 9), 2, 239, 41, 22, 1),
                ((-12, -5), 1, 11, 338, 81, 1),
                ((-9, 40), 2, 19, 3362, 3123, 1),
                ((-5, -12), 1, 11, 26, 23, 1),
            ),
        )
        self.assertTrue(pinned_global_root_choice_alternate_line_strip_rows_valid())
        for row in PINNED_GLOBAL_ROOT_CHOICE_ALTERNATE_LINE_STRIP_ROWS:
            witness = pinned_global_root_choice_alternate_line_strip_row_witness(row)
            self.assertIsNotNone(witness)
            self.assertEqual(
                promoted_root_spine_line_certificate_from_witness(witness),
                witness.certificate,
            )
        self.assertEqual(
            PINNED_GLOBAL_ROOT_CHOICE_ALTERNATE_LINE_STRIP_ROWS,
            tuple(
                (
                    row.obligation,
                    row.direction,
                    row.alternate_direction,
                    row.alternate_squareclass,
                    row.alternate_split_factor,
                    row.alternate_signed_paired_split_factor,
                    row.alternate_residue_period,
                    row.alternate_paired_residue,
                    row.alternate_coefficient_residue,
                    row.alternate_coefficient_modulus,
                )
                for row in audit.rows
            ),
        )
        table_witnesses = tuple(
            pinned_global_root_choice_table_witness(
                row.target,
                row.direction,
                row.obligation,
            )
            for row in audit.rows
        )
        self.assertTrue(all(witness is not None for witness in table_witnesses))
        self.assertEqual(
            tuple(
                (
                    witness.certificate.target,
                    witness.direction,
                    witness.squareclass,
                    witness.split_factor,
                    witness.signed_paired_split_factor,
                    witness.beta,
                    witness.first_coefficient,
                )
                for witness in table_witnesses
                if witness
            ),
            tuple(
                (
                    row.target,
                    row.alternate_direction,
                    row.alternate_squareclass,
                    row.alternate_split_factor,
                    row.alternate_signed_paired_split_factor,
                    row.alternate_beta,
                    row.alternate_first_coefficient,
                )
                for row in audit.rows
            ),
        )
        self.assertEqual(
            tuple(
                pinned_global_root_choice_table_certificate(
                    row.target,
                    row.direction,
                    row.obligation,
                )
                for row in audit.rows
            ),
            tuple(witness.certificate for witness in table_witnesses if witness),
        )
        self.assertEqual(
            tuple(
                parallel_direction_conjugate_ideal_divisor_obligation_global_discharge_witness(
                    row.target,
                    row.direction,
                    row.obligation,
                    8,
                ).branch
                for row in audit.rows
            ),
            ("alternate_root_spine_table",) * 14,
        )
        self.assertEqual(
            tuple(row.target for row in audit.rows),
            (
                (391, 158),
                (370, 403),
                (334, 325),
                (403, 370),
                (403, 370),
                (158, 391),
                (325, 334),
                (370, 403),
                (265, 346),
                (346, 265),
                (325, 334),
                (338, 151),
                (334, 325),
                (151, 338),
            ),
        )
        self.assertEqual(
            tuple(
                (
                    row.target,
                    row.alternate_direction,
                    row.alternate_squareclass,
                    row.alternate_split_factor,
                    row.alternate_signed_paired_split_factor,
                    row.alternate_residue_period,
                    row.alternate_paired_residue,
                    row.alternate_beta,
                    row.alternate_first_coefficient,
                )
                for row in audit.rows
            ),
            (
                ((391, 158), (-48, 55), 1, 19, -1531, 146, 75, (167, 65), 218),
                ((370, 403), (-20, 21), 10, 1583, -1, 29, 28, (-109, 273), -14897),
                ((334, 325), (-8, -15), 2, 241, 5, 17, 5, (-13, -57), -227),
                ((403, 370), (-21, 20), 10, 1, -1583, 29, 12, (-273, 109), 14897),
                ((403, 370), (-21, 20), 10, 1, -1583, 29, 12, (-273, 109), 14897),
                ((158, 391), (-55, 48), 1, 1531, -19, 146, 127, (-65, -167), -218),
                ((325, 334), (-15, -8), 2, 241, -5, 17, 12, (-13, 57), -227),
                ((370, 403), (-20, 21), 10, 1583, -1, 29, 28, (-109, 273), -14897),
                ((265, 346), (-12, -5), 1, 11, -257, 338, 81, (-61, 37), 166),
                ((346, 265), (-5, -12), 1, 11, 257, 26, 23, (-61, -37), 166),
                ((325, 334), (-15, -8), 2, 241, -5, 17, 12, (-13, 57), -227),
                ((338, 151), (-40, 9), 2, 239, -19, 41, 22, (-21, 31), -41),
                ((334, 325), (-8, -15), 2, 241, 5, 17, 5, (-13, -57), -227),
                ((151, 338), (-9, 40), 2, 19, -239, 3362, 3123, (-31, 21), 41),
            ),
        )
        self.assertEqual(
            tuple(
                (
                    row.target,
                    row.alternate_strip_step,
                    row.alternate_strip_residue,
                    row.alternate_strip_modulus,
                    row.alternate_strip_gcd,
                    row.alternate_coefficient_residue,
                    row.alternate_coefficient_modulus,
                    row.alternate_first_coefficient,
                )
                for row in audit.rows
            ),
            (
                ((391, 158), 10, 9, 13, 1, 10, 13, 218),
                ((370, 403), 8, 8, 13, 1, 1, 13, -14897),
                ((334, 325), 3, 8, 13, 1, 7, 13, -227),
                ((403, 370), 7, 6, 13, 1, 12, 13, 14897),
                ((403, 370), 8, 5, 13, 1, 12, 13, 14897),
                ((158, 391), 10, 4, 13, 1, 3, 13, -218),
                ((325, 334), 10, 5, 13, 1, 7, 13, -227),
                ((370, 403), 7, 7, 13, 1, 1, 13, -14897),
                ((265, 346), 49, 16, 82, 1, 2, 82, 166),
                ((346, 265), 49, 16, 82, 1, 2, 82, 166),
                ((325, 334), 41, 37, 73, 1, 65, 73, -227),
                ((338, 151), 6, 46, 73, 1, 32, 73, -41),
                ((334, 325), 41, 37, 73, 1, 65, 73, -227),
                ((151, 338), 67, 46, 73, 1, 41, 73, 41),
            ),
        )

    @pytest.mark.perf
    def test_pinned_strip_global_root_choice_branch_audit_750(self):
        branch_audit = parallel_direction_conjugate_ideal_global_root_choice_branch_audit(
            750
        )
        self.assertEqual(branch_audit.checked_strip_failures, 233598)
        self.assertEqual(branch_audit.local_discharge_count, 233578)
        self.assertEqual(branch_audit.global_discharge_count, 20)
        self.assertEqual(
            branch_audit.global_branch_counts,
            (("alternate_root_spine_table", 14), ("alternate_root_spine", 6)),
        )
        self.assertEqual(branch_audit.missing_rows, ())
        self.assertEqual(branch_audit.unreconstructed_rows, ())
        self.assertEqual(
            branch_audit.global_root_shape_counts,
            (
                ((1, 4), 4),
                ((2, 3), 4),
                ((2, 5), 4),
                ((2, 7), 4),
                ((3, 8), 2),
                ((4, 5), 2),
            ),
        )
        self.assertEqual(
            tuple(
                (row.target, row.branch, row.structural_row[1])
                for row in branch_audit.global_rows
                if row.branch == "alternate_root_spine"
            ),
            (
                ((530, 713), "alternate_root_spine", (2, 7)),
                ((601, 262), "alternate_root_spine", (2, 3)),
                ((262, 601), "alternate_root_spine", (2, 3)),
                ((713, 530), "alternate_root_spine", (2, 7)),
                ((611, 482), "alternate_root_spine", (2, 7)),
                ((482, 611), "alternate_root_spine", (2, 7)),
            ),
        )
        signature_template_coverage = (
            parallel_direction_conjugate_ideal_global_root_choice_signature_template_coverage_audit(
                750,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_500_SIGNATURE_TEMPLATE_ROWS,
                branch_audit=branch_audit,
            )
        )
        self.assertEqual(signature_template_coverage.global_row_count, 20)
        self.assertEqual(signature_template_coverage.covered_count, 14)
        self.assertEqual(signature_template_coverage.missing_count, 6)
        self.assertEqual(signature_template_coverage.mismatch_count, 0)
        self.assertEqual(
            signature_template_coverage.missing_root_shape_counts,
            (((2, 7), 4), ((2, 3), 2)),
        )
        self.assertEqual(
            signature_template_coverage.missing_signature_counts,
            (
                (13, 7, False, 2, ((0, 1), (0, 10)), 2),
                (13, 7, False, 3, ((0, 6, 9), (0, 11)), 2),
                (17, 1, False, 1, ((0, 6),), 2),
            ),
        )
        signature_template_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_signature_template_audit(
                750,
                branch_audit=branch_audit,
            )
        )
        self.assertEqual(signature_template_audit.global_row_count, 20)
        self.assertEqual(signature_template_audit.signature_count, 13)
        self.assertEqual(signature_template_audit.template_count, 16)
        self.assertEqual(signature_template_audit.signature_template_count, 20)
        self.assertEqual(
            tuple(row[:-1] for row in signature_template_audit.signature_template_counts),
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_SIGNATURE_TEMPLATE_ROWS,
        )
        extended_signature_template_coverage = (
            parallel_direction_conjugate_ideal_global_root_choice_signature_template_coverage_audit(
                750,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_SIGNATURE_TEMPLATE_ROWS,
                branch_audit=branch_audit,
            )
        )
        self.assertEqual(extended_signature_template_coverage.covered_count, 20)
        self.assertEqual(extended_signature_template_coverage.missing_count, 0)
        self.assertEqual(extended_signature_template_coverage.mismatch_count, 0)
        signature_template_branch_audit = (
            parallel_direction_conjugate_ideal_signature_template_branch_audit(
                750,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_SIGNATURE_TEMPLATE_ROWS,
            )
        )
        self.assertEqual(signature_template_branch_audit.checked_strip_failures, 233598)
        self.assertEqual(signature_template_branch_audit.local_discharge_count, 233578)
        self.assertEqual(signature_template_branch_audit.global_discharge_count, 20)
        self.assertEqual(
            signature_template_branch_audit.global_branch_counts,
            (("alternate_signature_template", 20),),
        )
        self.assertEqual(signature_template_branch_audit.missing_rows, ())
        self.assertEqual(signature_template_branch_audit.unreconstructed_rows, ())
        self.assertEqual(
            tuple(
                (row.target, row.direction, row.obligation, row.structural_row)
                for row in signature_template_branch_audit.global_rows
            ),
            tuple(
                (row.target, row.direction, row.obligation, row.structural_row)
                for row in branch_audit.global_rows
            ),
        )
        generic_rows = tuple(
            global_root_choice_branch_row_alternate_line_strip_row(row)
            for row in branch_audit.global_rows
            if row.branch == "alternate_root_spine"
        )
        self.assertEqual(
            generic_rows,
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_GENERIC_LINE_STRIP_ROWS,
        )
        self.assertTrue(
            all(
                pinned_global_root_choice_alternate_line_strip_row_valid(row)
                for row in PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_GENERIC_LINE_STRIP_ROWS
            )
        )
        extended_rows = (
            PINNED_GLOBAL_ROOT_CHOICE_ALTERNATE_LINE_STRIP_ROWS
            + PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_GENERIC_LINE_STRIP_ROWS
        )
        self.assertEqual(
            tuple(
                pinned_global_root_choice_table_witness(
                    row.target,
                    row.direction,
                    row.obligation,
                    extended_rows,
                ).certificate
                for row in branch_audit.global_rows
                if row.branch == "alternate_root_spine"
            ),
            tuple(
                ParallelDirectionConjugateIdealWitness(
                    target=row.target,
                    direction=row.structural_row[0],
                    squareclass=row.structural_row[2],
                    split_factor=row.structural_row[3],
                    signed_paired_split_factor=row.structural_row[4],
                    beta=row.structural_row[5],
                    first_coefficient=row.structural_row[6],
                ).certificate
                for row in branch_audit.global_rows
                if row.branch == "alternate_root_spine"
            ),
        )
        original_row_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_portable_row_audit(
                750
            )
        )
        self.assertEqual(original_row_audit.global_row_count, 20)
        self.assertEqual(original_row_audit.distinct_row_count, 20)
        self.assertEqual(original_row_audit.base_table_row_count, 14)
        self.assertEqual(original_row_audit.new_row_count, 6)
        self.assertEqual(
            original_row_audit.new_root_shape_counts,
            (((2, 7), 4), ((2, 3), 2)),
        )
        self.assertEqual(
            original_row_audit.new_alternate_direction_counts,
            (((-45, 28), 2), ((-28, 45), 2), ((-12, 5), 1), ((-5, 12), 1)),
        )
        self.assertEqual(
            original_row_audit.new_rows,
            tuple(sorted(PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_GENERIC_LINE_STRIP_ROWS)),
        )
        self.assertEqual(original_row_audit.invalid_rows, ())

        extended_row_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_portable_row_audit(
                750,
                extended_rows,
            )
        )
        self.assertEqual(extended_row_audit.global_row_count, 20)
        self.assertEqual(extended_row_audit.distinct_row_count, 20)
        self.assertEqual(extended_row_audit.base_table_row_count, 20)
        self.assertEqual(extended_row_audit.new_row_count, 0)
        self.assertEqual(extended_row_audit.new_root_shape_counts, ())
        self.assertEqual(extended_row_audit.new_alternate_direction_counts, ())
        self.assertEqual(extended_row_audit.new_obligation_counts, ())
        self.assertEqual(extended_row_audit.new_line_template_counts, ())
        self.assertEqual(extended_row_audit.new_rows, ())
        self.assertEqual(extended_row_audit.invalid_rows, ())

    @pytest.mark.perf
    def test_pinned_strip_global_root_choice_portable_row_audit_1000(self):
        extended_rows = (
            PINNED_GLOBAL_ROOT_CHOICE_ALTERNATE_LINE_STRIP_ROWS
            + PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_GENERIC_LINE_STRIP_ROWS
        )
        row_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_portable_row_audit(
                1000,
                extended_rows,
            )
        )
        self.assertEqual(row_audit.global_row_count, 42)
        self.assertEqual(row_audit.distinct_row_count, 42)
        self.assertEqual(row_audit.base_table_row_count, 20)
        self.assertEqual(row_audit.new_row_count, 22)
        self.assertEqual(
            row_audit.new_root_shape_counts,
            (((1, 6), 14), ((2, 3), 6), ((2, 5), 2)),
        )
        self.assertEqual(
            row_audit.new_alternate_direction_counts,
            (
                ((-35, 12), 6),
                ((-12, 35), 6),
                ((-12, -5), 2),
                ((-5, -12), 2),
                ((-35, -12), 1),
                ((-21, 20), 1),
                ((-20, 21), 1),
                ((-12, -35), 1),
                ((-12, 5), 1),
                ((-5, 12), 1),
            ),
        )
        self.assertEqual(
            row_audit.new_line_template_counts,
            (
                ((-35, 12), 1, 89, -349, 74, 21, 3),
                ((-35, 12), 10, 3583, -1, 37, 36, 3),
                ((-12, 35), 1, 349, -89, 74, 59, 3),
                ((-12, 35), 10, 1, -3583, 2738, 1893, 3),
                ((-12, -5), 1, 11, -881, 338, 133, 2),
                ((-5, -12), 1, 11, 881, 26, 23, 2),
                ((-35, -12), 7, 1, -2917, 74, 43, 1),
                ((-21, 20), 23, 1549, -1, 58, 57, 1),
                ((-20, 21), 23, 1, -1549, 58, 17, 1),
                ((-12, -35), 7, 1, 2917, 74, 31, 1),
                ((-12, 5), 1, 115, -107, 338, 231, 1),
                ((-5, 12), 1, 23, -535, 338, 141, 1),
            ),
        )
        self.assertEqual(row_audit.invalid_rows, ())
        dominant_templates = tuple(
            row[:6]
            for row in row_audit.new_line_template_counts
            if row[-1] == 3
        )
        self.assertEqual(
            dominant_templates,
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_DOMINANT_LINE_TEMPLATES,
        )
        self.assertEqual(
            tuple(
                len(global_root_choice_line_template_strip_rows(template))
                for template in dominant_templates
            ),
            (24, 40, 24, 40),
        )
        dominant_template_rows = global_root_choice_line_template_table_rows(
            dominant_templates
        )
        self.assertEqual(len(dominant_template_rows), 128)
        self.assertTrue(
            all(
                pinned_global_root_choice_alternate_line_strip_row_valid(row)
                for row in dominant_template_rows
            )
        )
        template_extended_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_portable_row_audit(
                1000,
                extended_rows + dominant_template_rows,
            )
        )
        self.assertEqual(template_extended_audit.global_row_count, 42)
        self.assertEqual(template_extended_audit.distinct_row_count, 42)
        self.assertEqual(template_extended_audit.new_row_count, 10)
        self.assertEqual(
            template_extended_audit.new_root_shape_counts,
            (((2, 3), 6), ((1, 6), 2), ((2, 5), 2)),
        )
        branch_audit = parallel_direction_conjugate_ideal_global_root_choice_branch_audit(
            1000
        )
        signature_template_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_signature_template_audit(
                1000,
                branch_audit=branch_audit,
            )
        )
        self.assertEqual(signature_template_audit.global_row_count, 42)
        self.assertEqual(signature_template_audit.signature_count, 21)
        self.assertEqual(signature_template_audit.template_count, 28)
        self.assertEqual(signature_template_audit.signature_template_count, 40)
        self.assertEqual(
            tuple(row[:-1] for row in signature_template_audit.signature_template_counts),
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_SIGNATURE_TEMPLATE_ROWS,
        )
        self.assertEqual(
            GLOBAL_ROOT_CHOICE_PROVED_NORMALIZED_LINE_TEMPLATES,
            (
                ((1, 4), 2, (5, 241), 17),
                ((1, 4), 17, (1, 1033), 34),
                ((1, 6), 1, (89, 349), 74),
                ((1, 6), 10, (1, 3583), 37),
                ((1, 6), 10, (1, 3583), 2738),
                ((1, 6), 10, (1, 475), 37),
                ((1, 6), 10, (1, 475), 2738),
                ((1, 6), 7, (1, 2917), 74),
                ((1, 2), 535, (1, 947), 50),
                ((2, 3), 1, (11, 881), 338),
                ((2, 3), 1, (11, 881), 26),
                ((2, 3), 1, (11, 257), 338),
                ((2, 3), 1, (11, 257), 26),
                ((2, 3), 1, (23, 535), 338),
                ((2, 3), 1, (67, 257), 26),
                ((2, 3), 1, (107, 115), 338),
                ((2, 3), 13, (1, 473), 26),
                ((2, 3), 13, (1, 905), 338),
                ((2, 3), 13, (1, 905), 26),
                ((2, 3), 2, (71, 121), 13),
                ((2, 3), 2, (19, 641), 13),
                ((2, 3), 5, (19, 173), 26),
                ((2, 3), 46, (1, 317), 13),
                ((2, 5), 10, (1, 1583), 29),
                ((2, 5), 23, (1, 1549), 58),
                ((2, 7), 1, (179, 229), 106),
                ((2, 7), 2, (19, 1153), 53),
                ((4, 5), 2, (19, 239), 3362),
                ((4, 5), 2, (19, 239), 41),
                ((3, 8), 1, (19, 1531), 146),
            ),
        )
        self.assertEqual(
            tuple(
                (template, theorem_name)
                for template, theorem_name in GLOBAL_ROOT_CHOICE_PROVED_NORMALIZED_LINE_FAMILIES
            ),
            (
                (
                    ((1, 4), 2, (5, 241), 17),
                    "certificateValid_oneFourEvenSplitTwoFortyOneLineStrip",
                ),
                (
                    ((1, 4), 17, (1, 1033), 34),
                    "certificateValid_oneFourOddSquareclassSeventeenSplitTenThirtyThreeLineStrip",
                ),
                (
                    ((1, 6), 1, (89, 349), 74),
                    "certificateValid_oneSixSplitEightyNineThreeFortyNineLineStrip",
                ),
                (
                    ((1, 6), 10, (1, 3583), 37),
                    "certificateValid_oneSixSplitThirtyFiveEightyThreeResidueThirtySixLineStrip",
                ),
                (
                    ((1, 6), 10, (1, 3583), 2738),
                    "certificateValid_oneSixSplitThirtyFiveEightyThreeResidueEighteenNinetyThreeLineStrip",
                ),
                (
                    ((1, 6), 10, (1, 475), 37),
                    "certificateValid_oneSixSquareclassTenSplitFourSeventyFiveResidueOneLineStrip",
                ),
                (
                    ((1, 6), 10, (1, 475), 2738),
                    "certificateValid_oneSixSquareclassTenSplitFourSeventyFiveResidueTwentySevenThirtySevenLineStrip",
                ),
                (
                    ((1, 6), 7, (1, 2917), 74),
                    "certificateValid_oneSixSplitTwentyNineSeventeenLineStrip",
                ),
                (
                    ((1, 2), 535, (1, 947), 50),
                    "certificateValid_oneTwoSquareclassFiveThirtyFiveSplitNineFortySevenResidueThreeLineStrip",
                ),
                (
                    ((2, 3), 1, (11, 881), 338),
                    "certificateValid_twoThreeOddSplitElevenResidueOneThirtyThreeLineStrip",
                ),
                (
                    ((2, 3), 1, (11, 881), 26),
                    "certificateValid_twoThreeOddSplitElevenResidueTwentyThreeLineStrip",
                ),
                (
                    ((2, 3), 1, (11, 257), 338),
                    "certificateValid_twoThreeOddSplitElevenTwoFiftySevenResidueEightyOneLineStrip",
                ),
                (
                    ((2, 3), 1, (11, 257), 26),
                    "certificateValid_twoThreeOddSplitElevenTwoFiftySevenResidueTwentyThreeLineStrip",
                ),
                (
                    ((2, 3), 1, (23, 535), 338),
                    "certificateValid_twoThreeOddSplitTwentyThreeFiveThirtyFiveResidueOneFortyOneLineStrip",
                ),
                (
                    ((2, 3), 1, (67, 257), 26),
                    "certificateValid_twoThreeOddSplitSixtySevenTwoFiftySevenLineStrip",
                ),
                (
                    ((2, 3), 1, (107, 115), 338),
                    "certificateValid_twoThreeOddSplitOneHundredSevenOneFifteenResidueTwoThirtyOneLineStrip",
                ),
                (
                    ((2, 3), 13, (1, 473), 26),
                    "certificateValid_twoThreeOddSquareclassThirteenSplitFourSeventyThreeLineStrip",
                ),
                (
                    ((2, 3), 13, (1, 905), 338),
                    "certificateValid_twoThreeOddSquareclassThirteenSplitNineOhFiveResidueOneOhNineLineStrip",
                ),
                (
                    ((2, 3), 13, (1, 905), 26),
                    "certificateValid_twoThreeOddSquareclassThirteenSplitNineOhFiveResidueTwentyOneLineStrip",
                ),
                (
                    ((2, 3), 2, (71, 121), 13),
                    "certificateValid_twoThreeEvenSplitSeventyOneOneTwentyOneLineStrip",
                ),
                (
                    ((2, 3), 2, (19, 641), 13),
                    "certificateValid_twoThreeEvenSplitNineteenSixFortyOneLineStrip",
                ),
                (
                    ((2, 3), 5, (19, 173), 26),
                    "certificateValid_twoThreeSquareclassFiveSplitNineteenOneSeventyThreeLineStrip",
                ),
                (
                    ((2, 3), 46, (1, 317), 13),
                    "certificateValid_twoThreeSquareclassFortySixSplitThreeSeventeenLineStrip",
                ),
                (
                    ((2, 5), 10, (1, 1583), 29),
                    "certificateValid_twoFiveSplitOneFifteenEightyThreeLineStrip",
                ),
                (
                    ((2, 5), 23, (1, 1549), 58),
                    "certificateValid_twoFiveOddSquareclassTwentyThreeSplitFifteenFortyNineLineStrip",
                ),
                (
                    ((2, 7), 1, (179, 229), 106),
                    "certificateValid_twoSevenOddSplitOneSeventyNineTwoTwentyNineLineStrip",
                ),
                (
                    ((2, 7), 2, (19, 1153), 53),
                    "certificateValid_twoSevenEvenSplitNineteenElevenFiftyThreeLineStrip",
                ),
                (
                    ((4, 5), 2, (19, 239), 3362),
                    "certificateValid_fourFiveEvenSplitNineteenTwoThirtyNineResidueThirtyOneTwentyThreeLineStrip",
                ),
                (
                    ((4, 5), 2, (19, 239), 41),
                    "certificateValid_fourFiveEvenSplitNineteenTwoThirtyNineResidueTwentyTwoLineStrip",
                ),
                (
                    ((3, 8), 1, (19, 1531), 146),
                    "certificateValid_threeEightOddSplitNineteenFifteenThirtyOneLineStrip",
                ),
            ),
        )
        proved_template_rows = tuple(
            (
                row[:5],
                row[5:],
                global_root_choice_normalized_line_template(row[5:]),
                global_root_choice_proved_normalized_line_family_theorem(row[5:]),
            )
            for row in PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_SIGNATURE_TEMPLATE_ROWS
            if (
                global_root_choice_proved_normalized_line_family_theorem(row[5:])
                is not None
            )
        )
        self.assertEqual(
            proved_template_rows,
            (
                (
                    (13, 7, False, 1, ((0, 11),)),
                    ((-35, 12), 10, 3583, -1, 37, 36),
                    ((1, 6), 10, (1, 3583), 37),
                    "certificateValid_oneSixSplitThirtyFiveEightyThreeResidueThirtySixLineStrip",
                ),
                (
                    (13, 7, False, 1, ((0, 11),)),
                    ((-12, 35), 10, 1, -3583, 2738, 1893),
                    ((1, 6), 10, (1, 3583), 2738),
                    "certificateValid_oneSixSplitThirtyFiveEightyThreeResidueEighteenNinetyThreeLineStrip",
                ),
                (
                    (13, 7, False, 1, ((0, 5), (0,))),
                    ((-12, -5), 1, 11, -881, 338, 133),
                    ((2, 3), 1, (11, 881), 338),
                    "certificateValid_twoThreeOddSplitElevenResidueOneThirtyThreeLineStrip",
                ),
                (
                    (13, 7, False, 1, ((0, 5), (0,))),
                    ((-5, -12), 1, 11, 881, 26, 23),
                    ((2, 3), 1, (11, 881), 26),
                    "certificateValid_twoThreeOddSplitElevenResidueTwentyThreeLineStrip",
                ),
                (
                    (13, 7, False, 1, ((0, 11),)),
                    ((-55, 48), 1, 1531, -19, 146, 127),
                    ((3, 8), 1, (19, 1531), 146),
                    "certificateValid_threeEightOddSplitNineteenFifteenThirtyOneLineStrip",
                ),
                (
                    (13, 7, False, 1, ((0, 11),)),
                    ((-48, 55), 1, 19, -1531, 146, 75),
                    ((3, 8), 1, (19, 1531), 146),
                    "certificateValid_threeEightOddSplitNineteenFifteenThirtyOneLineStrip",
                ),
                (
                    (13, 7, False, 1, ((0, 11),)),
                    ((-35, -12), 7, 1, -2917, 74, 43),
                    ((1, 6), 7, (1, 2917), 74),
                    "certificateValid_oneSixSplitTwentyNineSeventeenLineStrip",
                ),
                (
                    (13, 7, False, 1, ((0, 11),)),
                    ((-35, 12), 1, 89, -349, 74, 21),
                    ((1, 6), 1, (89, 349), 74),
                    "certificateValid_oneSixSplitEightyNineThreeFortyNineLineStrip",
                ),
                (
                    (13, 7, False, 1, ((0, 11),)),
                    ((-12, -35), 7, 1, 2917, 74, 31),
                    ((1, 6), 7, (1, 2917), 74),
                    "certificateValid_oneSixSplitTwentyNineSeventeenLineStrip",
                ),
                (
                    (13, 7, False, 1, ((0, 11),)),
                    ((-12, 35), 1, 349, -89, 74, 59),
                    ((1, 6), 1, (89, 349), 74),
                    "certificateValid_oneSixSplitEightyNineThreeFortyNineLineStrip",
                ),
                (
                    (13, 7, False, 2, ((0, 1), (0, 10))),
                    ((-12, 5), 13, 1, -473, 26, 21),
                    ((2, 3), 13, (1, 473), 26),
                    "certificateValid_twoThreeOddSquareclassThirteenSplitFourSeventyThreeLineStrip",
                ),
                (
                    (13, 7, False, 2, ((0, 1), (0, 10))),
                    ((-5, 12), 13, 473, -1, 26, 25),
                    ((2, 3), 13, (1, 473), 26),
                    "certificateValid_twoThreeOddSquareclassThirteenSplitFourSeventyThreeLineStrip",
                ),
                (
                    (13, 7, False, 2, ((0, 9), (0, 2))),
                    ((-21, 20), 10, 1, -1583, 29, 12),
                    ((2, 5), 10, (1, 1583), 29),
                    "certificateValid_twoFiveSplitOneFifteenEightyThreeLineStrip",
                ),
                (
                    (13, 7, False, 2, ((0, 9), (0, 2))),
                    ((-20, 21), 10, 1583, -1, 29, 28),
                    ((2, 5), 10, (1, 1583), 29),
                    "certificateValid_twoFiveSplitOneFifteenEightyThreeLineStrip",
                ),
                (
                    (13, 7, False, 2, ((0, 9), (0, 8))),
                    ((-21, 20), 23, 1549, -1, 58, 57),
                    ((2, 5), 23, (1, 1549), 58),
                    "certificateValid_twoFiveOddSquareclassTwentyThreeSplitFifteenFortyNineLineStrip",
                ),
                (
                    (13, 7, False, 2, ((0, 9), (0, 8))),
                    ((-20, 21), 23, 1, -1549, 58, 17),
                    ((2, 5), 23, (1, 1549), 58),
                    "certificateValid_twoFiveOddSquareclassTwentyThreeSplitFifteenFortyNineLineStrip",
                ),
                (
                    (13, 7, False, 3, ((0, 1), (0, 9), (0, 1))),
                    ((-15, -8), 2, 241, -5, 17, 12),
                    ((1, 4), 2, (5, 241), 17),
                    "certificateValid_oneFourEvenSplitTwoFortyOneLineStrip",
                ),
                (
                    (13, 7, False, 3, ((0, 1), (0, 9), (0, 1))),
                    ((-8, -15), 2, 241, 5, 17, 5),
                    ((1, 4), 2, (5, 241), 17),
                    "certificateValid_oneFourEvenSplitTwoFortyOneLineStrip",
                ),
                (
                    (13, 7, False, 3, ((0, 6, 9), (0, 5))),
                    ((-21, 20), 10, 1, -1583, 29, 12),
                    ((2, 5), 10, (1, 1583), 29),
                    "certificateValid_twoFiveSplitOneFifteenEightyThreeLineStrip",
                ),
                (
                    (13, 7, False, 3, ((0, 6, 9), (0, 5))),
                    ((-20, 21), 10, 1583, -1, 29, 28),
                    ((2, 5), 10, (1, 1583), 29),
                    "certificateValid_twoFiveSplitOneFifteenEightyThreeLineStrip",
                ),
                (
                    (13, 7, False, 3, ((0, 6, 9), (0, 11))),
                    ((-45, 28), 2, 19, -1153, 53, 13),
                    ((2, 7), 2, (19, 1153), 53),
                    "certificateValid_twoSevenEvenSplitNineteenElevenFiftyThreeLineStrip",
                ),
                (
                    (13, 7, False, 3, ((0, 6, 9), (0, 11))),
                    ((-28, 45), 2, 1153, -19, 53, 34),
                    ((2, 7), 2, (19, 1153), 53),
                    "certificateValid_twoSevenEvenSplitNineteenElevenFiftyThreeLineStrip",
                ),
                (
                    (17, 1, False, 1, ((0, 6),)),
                    ((-45, 28), 1, 179, -229, 106, 89),
                    ((2, 7), 1, (179, 229), 106),
                    "certificateValid_twoSevenOddSplitOneSeventyNineTwoTwentyNineLineStrip",
                ),
                (
                    (17, 1, False, 1, ((0, 6),)),
                    ((-28, 45), 1, 229, -179, 106, 33),
                    ((2, 7), 1, (179, 229), 106),
                    "certificateValid_twoSevenOddSplitOneSeventyNineTwoTwentyNineLineStrip",
                ),
                (
                    (17, 1, False, 1, ((0, 14),)),
                    ((-35, 12), 1, 89, -349, 74, 21),
                    ((1, 6), 1, (89, 349), 74),
                    "certificateValid_oneSixSplitEightyNineThreeFortyNineLineStrip",
                ),
                (
                    (17, 1, False, 1, ((0, 14),)),
                    ((-12, 5), 1, 115, -107, 338, 231),
                    ((2, 3), 1, (107, 115), 338),
                    "certificateValid_twoThreeOddSplitOneHundredSevenOneFifteenResidueTwoThirtyOneLineStrip",
                ),
                (
                    (17, 1, False, 1, ((0, 14),)),
                    ((-12, 35), 1, 349, -89, 74, 59),
                    ((1, 6), 1, (89, 349), 74),
                    "certificateValid_oneSixSplitEightyNineThreeFortyNineLineStrip",
                ),
                (
                    (17, 1, False, 1, ((0, 14),)),
                    ((-5, 12), 1, 23, -535, 338, 141),
                    ((2, 3), 1, (23, 535), 338),
                    "certificateValid_twoThreeOddSplitTwentyThreeFiveThirtyFiveResidueOneFortyOneLineStrip",
                ),
                (
                    (17, 1, False, 1, ((0, 14), (0,))),
                    ((-12, -5), 1, 11, -881, 338, 133),
                    ((2, 3), 1, (11, 881), 338),
                    "certificateValid_twoThreeOddSplitElevenResidueOneThirtyThreeLineStrip",
                ),
                (
                    (17, 1, False, 1, ((0, 14), (0,))),
                    ((-5, -12), 1, 11, 881, 26, 23),
                    ((2, 3), 1, (11, 881), 26),
                    "certificateValid_twoThreeOddSplitElevenResidueTwentyThreeLineStrip",
                ),
                (
                    (41, 9, False, 1, ((0, 8),)),
                    ((-12, -5), 1, 11, -257, 338, 81),
                    ((2, 3), 1, (11, 257), 338),
                    "certificateValid_twoThreeOddSplitElevenTwoFiftySevenResidueEightyOneLineStrip",
                ),
                (
                    (41, 9, False, 2, ((0, 39), (0, 29))),
                    ((-35, 12), 10, 3583, -1, 37, 36),
                    ((1, 6), 10, (1, 3583), 37),
                    "certificateValid_oneSixSplitThirtyFiveEightyThreeResidueThirtySixLineStrip",
                ),
                (
                    (41, 19, False, 1, ((0, 8),)),
                    ((-5, -12), 1, 11, 257, 26, 23),
                    ((2, 3), 1, (11, 257), 26),
                    "certificateValid_twoThreeOddSplitElevenTwoFiftySevenResidueTwentyThreeLineStrip",
                ),
                (
                    (41, 19, False, 2, ((0, 39), (0, 29))),
                    ((-12, 35), 10, 1, -3583, 2738, 1893),
                    ((1, 6), 10, (1, 3583), 2738),
                    "certificateValid_oneSixSplitThirtyFiveEightyThreeResidueEighteenNinetyThreeLineStrip",
                ),
                (
                    (73, 44, False, 1, ((0, 34),)),
                    ((-9, 40), 2, 19, -239, 3362, 3123),
                    ((4, 5), 2, (19, 239), 3362),
                    "certificateValid_fourFiveEvenSplitNineteenTwoThirtyNineResidueThirtyOneTwentyThreeLineStrip",
                ),
                (
                    (73, 44, False, 2, ((0, 4), (0, 30))),
                    ((-8, -15), 2, 241, 5, 17, 5),
                    ((1, 4), 2, (5, 241), 17),
                    "certificateValid_oneFourEvenSplitTwoFortyOneLineStrip",
                ),
                (
                    (73, 44, False, 2, ((0, 31), (0, 39))),
                    ((-35, 12), 1, 89, -349, 74, 21),
                    ((1, 6), 1, (89, 349), 74),
                    "certificateValid_oneSixSplitEightyNineThreeFortyNineLineStrip",
                ),
                (
                    (73, 62, False, 1, ((0, 34),)),
                    ((-40, 9), 2, 239, -19, 41, 22),
                    ((4, 5), 2, (19, 239), 41),
                    "certificateValid_fourFiveEvenSplitNineteenTwoThirtyNineResidueTwentyTwoLineStrip",
                ),
                (
                    (73, 62, False, 2, ((0, 4), (0, 30))),
                    ((-15, -8), 2, 241, -5, 17, 12),
                    ((1, 4), 2, (5, 241), 17),
                    "certificateValid_oneFourEvenSplitTwoFortyOneLineStrip",
                ),
                (
                    (73, 62, False, 2, ((0, 31), (0, 39))),
                    ((-12, 35), 1, 349, -89, 74, 59),
                    ((1, 6), 1, (89, 349), 74),
                    "certificateValid_oneSixSplitEightyNineThreeFortyNineLineStrip",
                ),
            ),
        )
        proved_signature_template_rows = tuple(
            row
            for row in PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_SIGNATURE_TEMPLATE_ROWS
            if (
                global_root_choice_proved_normalized_line_family_theorem(row[5:])
                is not None
            )
        )
        proved_witness_signature_rows = []
        for row in branch_audit.global_rows:
            witness = global_root_choice_proved_signature_template_witness(
                row.target,
                row.direction,
                row.obligation,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_SIGNATURE_TEMPLATE_ROWS,
            )
            proved_discharge = (
                parallel_direction_conjugate_ideal_divisor_obligation_proved_signature_template_discharge_witness(
                    row.target,
                    row.direction,
                    row.obligation,
                    PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_SIGNATURE_TEMPLATE_ROWS,
                )
            )
            if witness is None:
                self.assertIsNone(proved_discharge)
                continue
            self.assertIsNotNone(proved_discharge)
            self.assertEqual(proved_discharge.branch, "alternate_proved_signature_template")
            self.assertEqual(proved_discharge.structural_row, row.structural_row)
            self.assertEqual(witness.certificate.valid(), True)
            self.assertEqual(
                (
                    witness.direction,
                    witness.squareclass,
                    witness.split_factor,
                    witness.signed_paired_split_factor,
                    witness.beta,
                    witness.first_coefficient,
                ),
                (
                    row.structural_row[0],
                    row.structural_row[2],
                    row.structural_row[3],
                    row.structural_row[4],
                    row.structural_row[5],
                    row.structural_row[6],
                ),
            )
            signature_template_row = global_root_choice_branch_row_signature_template(row)
            self.assertIsNotNone(signature_template_row)
            proved_witness_signature_rows.append(signature_template_row)
        self.assertEqual(
            set(proved_witness_signature_rows),
            set(proved_signature_template_rows),
        )
        self.assertEqual(len(set(proved_witness_signature_rows)), 40)
        self.assertEqual(len(proved_witness_signature_rows), 42)
        signature_template_coverage = (
            parallel_direction_conjugate_ideal_global_root_choice_signature_template_coverage_audit(
                1000,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_SIGNATURE_TEMPLATE_ROWS,
                branch_audit=branch_audit,
            )
        )
        self.assertEqual(signature_template_coverage.covered_count, 42)
        self.assertEqual(signature_template_coverage.missing_count, 0)
        self.assertEqual(signature_template_coverage.mismatch_count, 0)
        signature_template_branch_audit = (
            parallel_direction_conjugate_ideal_signature_template_branch_audit(
                1000,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_SIGNATURE_TEMPLATE_ROWS,
            )
        )
        self.assertEqual(
            signature_template_branch_audit.checked_strip_failures,
            branch_audit.checked_strip_failures,
        )
        self.assertEqual(
            signature_template_branch_audit.local_discharge_count,
            branch_audit.local_discharge_count,
        )
        self.assertEqual(signature_template_branch_audit.global_discharge_count, 42)
        self.assertEqual(
            signature_template_branch_audit.global_branch_counts,
            (("alternate_signature_template", 42),),
        )
        self.assertEqual(signature_template_branch_audit.missing_rows, ())
        self.assertEqual(signature_template_branch_audit.unreconstructed_rows, ())
        self.assertEqual(
            tuple(
                (row.target, row.direction, row.obligation, row.structural_row)
                for row in signature_template_branch_audit.global_rows
            ),
            tuple(
                (row.target, row.direction, row.obligation, row.structural_row)
                for row in branch_audit.global_rows
            ),
        )
        iterated_signature_template_closure = (
            parallel_direction_conjugate_ideal_global_root_choice_iterated_signature_template_closure_audit(
                1000,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_SIGNATURE_TEMPLATE_ROWS,
                max_iterations=2,
                branch_audit=branch_audit,
            )
        )
        self.assertTrue(iterated_signature_template_closure.closed)
        self.assertEqual(iterated_signature_template_closure.base_row_count, 20)
        self.assertEqual(iterated_signature_template_closure.final_row_count, 40)
        self.assertEqual(
            iterated_signature_template_closure.final_rows,
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_SIGNATURE_TEMPLATE_ROWS,
        )
        self.assertEqual(iterated_signature_template_closure.iteration_count, 1)
        self.assertEqual(
            iterated_signature_template_closure.final_coverage_audit.covered_count,
            42,
        )
        self.assertEqual(
            iterated_signature_template_closure.final_coverage_audit.missing_count,
            0,
        )
        self.assertEqual(
            tuple(
                (
                    layer.iteration,
                    layer.input_row_count,
                    layer.missing_count,
                    layer.new_row_count,
                    layer.output_row_count,
                )
                for layer in iterated_signature_template_closure.layers
            ),
            ((1, 20, 22, 20, 40),),
        )
        self.assertEqual(len(iterated_signature_template_closure.layers[0].new_rows), 20)
        self.assertTrue(
            set(iterated_signature_template_closure.layers[0].new_rows).isdisjoint(
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_SIGNATURE_TEMPLATE_ROWS
            )
        )
        self.assertEqual(
            iterated_signature_template_closure.layers[0].missing_root_shape_counts,
            (((1, 6), 14), ((2, 3), 6), ((2, 5), 2)),
        )
        residual_template_rows = global_root_choice_line_template_table_rows(
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_RESIDUAL_LINE_TEMPLATES
        )
        self.assertEqual(len(residual_template_rows), 192)
        self.assertTrue(
            all(
                pinned_global_root_choice_alternate_line_strip_row_valid(row)
                for row in residual_template_rows
            )
        )
        radius_1000_template_rows = global_root_choice_line_template_table_rows(
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_DOMINANT_LINE_TEMPLATES
            + PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_RESIDUAL_LINE_TEMPLATES
        )
        self.assertEqual(len(radius_1000_template_rows), 320)
        iterated_closure_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_iterated_template_closure_audit(
                1000,
                extended_rows,
                max_iterations=2,
            )
        )
        self.assertTrue(iterated_closure_audit.closed)
        self.assertEqual(iterated_closure_audit.base_row_count, 20)
        self.assertEqual(iterated_closure_audit.final_row_count, 340)
        self.assertEqual(iterated_closure_audit.iteration_count, 1)
        self.assertEqual(iterated_closure_audit.final_portable_row_audit.global_row_count, 42)
        self.assertEqual(
            iterated_closure_audit.final_portable_row_audit.distinct_row_count,
            42,
        )
        self.assertEqual(iterated_closure_audit.final_portable_row_audit.new_row_count, 0)
        self.assertEqual(
            iterated_closure_audit.final_portable_row_audit.new_root_shape_counts,
            (),
        )
        self.assertEqual(
            iterated_closure_audit.final_portable_row_audit.new_line_template_counts,
            (),
        )
        self.assertEqual(
            tuple(
                (
                    layer.iteration,
                    layer.input_row_count,
                    layer.new_row_count,
                    layer.new_template_count,
                    layer.template_expanded_row_count,
                    layer.output_row_count,
                )
                for layer in iterated_closure_audit.layers
            ),
            ((1, 20, 22, 12, 320, 340),),
        )
        self.assertEqual(
            iterated_closure_audit.layers[0].new_root_shape_counts,
            (((1, 6), 14), ((2, 3), 6), ((2, 5), 2)),
        )
        observed_new_rows = set(row_audit.new_rows)
        for template in dominant_templates:
            expanded_rows = global_root_choice_line_template_strip_rows(template)
            self.assertEqual(
                sum(
                    1
                    for row in observed_new_rows
                    if (row[2], row[3], row[4], row[5], row[6], row[7])
                    == template
                ),
                3,
            )
            self.assertTrue(observed_new_rows.intersection(expanded_rows))
            self.assertTrue(
                all(
                    pinned_global_root_choice_alternate_line_strip_row_valid(row)
                    for row in expanded_rows
                )
            )

    @pytest.mark.perf
    def test_pinned_strip_global_root_choice_portable_row_audit_1250(self):
        extended_rows = (
            PINNED_GLOBAL_ROOT_CHOICE_ALTERNATE_LINE_STRIP_ROWS
            + PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_GENERIC_LINE_STRIP_ROWS
        )
        radius_1000_template_rows = global_root_choice_line_template_table_rows(
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_DOMINANT_LINE_TEMPLATES
            + PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_RESIDUAL_LINE_TEMPLATES
        )
        row_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_portable_row_audit(
                1250,
                extended_rows + radius_1000_template_rows,
            )
        )
        self.assertEqual(row_audit.global_row_count, 62)
        self.assertEqual(row_audit.distinct_row_count, 62)
        self.assertEqual(row_audit.new_row_count, 20)
        self.assertEqual(
            row_audit.new_root_shape_counts,
            (((2, 3), 12), ((1, 4), 6), ((1, 6), 2)),
        )
        self.assertEqual(
            row_audit.new_line_template_counts,
            (
                ((-15, 8), 17, 1033, -1, 34, 33, 3),
                ((-12, -5), 13, 1, -905, 338, 109, 3),
                ((-8, 15), 17, 1, -1033, 34, 21, 3),
                ((-5, -12), 13, 1, 905, 26, 21, 3),
                ((-35, -12), 10, 475, 1, 37, 1, 1),
                ((-12, -35), 10, 475, -1, 2738, 2737, 1),
                ((-12, 5), 2, 71, -121, 13, 9, 1),
                ((-12, 5), 5, 19, -173, 26, 9, 1),
                ((-12, 5), 46, 1, -317, 13, 8, 1),
                ((-5, 12), 2, 121, -71, 13, 7, 1),
                ((-5, 12), 5, 173, -19, 26, 7, 1),
                ((-5, 12), 46, 317, -1, 13, 12, 1),
            ),
        )
        radius_1250_template_rows = global_root_choice_line_template_table_rows(
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_RESIDUAL_LINE_TEMPLATES
        )
        self.assertEqual(len(radius_1250_template_rows), 352)
        self.assertTrue(
            all(
                pinned_global_root_choice_alternate_line_strip_row_valid(row)
                for row in radius_1250_template_rows
            )
        )
        closed_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_portable_row_audit(
                1250,
                extended_rows + radius_1000_template_rows + radius_1250_template_rows,
            )
        )
        self.assertEqual(closed_audit.global_row_count, 62)
        self.assertEqual(closed_audit.distinct_row_count, 62)
        self.assertEqual(closed_audit.new_row_count, 0)
        self.assertEqual(closed_audit.new_root_shape_counts, ())
        self.assertEqual(closed_audit.new_line_template_counts, ())
        closure_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_template_closure_audit(
                1250,
                extended_rows + radius_1000_template_rows,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_RESIDUAL_LINE_TEMPLATES,
            )
        )
        self.assertEqual(closure_audit.template_count, 12)
        self.assertEqual(closure_audit.template_expanded_row_count, 352)
        self.assertEqual(closure_audit.portable_row_audit.new_row_count, 0)
        branch_audit = parallel_direction_conjugate_ideal_global_root_choice_branch_audit(
            1250
        )
        signature_template_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_signature_template_audit(
                1250,
                branch_audit=branch_audit,
            )
        )
        self.assertEqual(signature_template_audit.global_row_count, 62)
        self.assertEqual(signature_template_audit.signature_count, 27)
        self.assertEqual(signature_template_audit.template_count, 40)
        self.assertEqual(signature_template_audit.signature_template_count, 60)
        self.assertEqual(
            tuple(row[:-1] for row in signature_template_audit.signature_template_counts),
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_SIGNATURE_TEMPLATE_ROWS,
        )
        signature_template_coverage = (
            parallel_direction_conjugate_ideal_global_root_choice_signature_template_coverage_audit(
                1250,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_SIGNATURE_TEMPLATE_ROWS,
                branch_audit=branch_audit,
            )
        )
        self.assertEqual(signature_template_coverage.covered_count, 62)
        self.assertEqual(signature_template_coverage.missing_count, 0)
        self.assertEqual(signature_template_coverage.mismatch_count, 0)
        for row in branch_audit.global_rows:
            signature_discharge = (
                parallel_direction_conjugate_ideal_divisor_obligation_signature_template_discharge_witness(
                    row.target,
                    row.direction,
                    row.obligation,
                    PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_SIGNATURE_TEMPLATE_ROWS,
                )
            )
            self.assertIsNotNone(signature_discharge)
            self.assertEqual(signature_discharge.branch, "alternate_signature_template")
            self.assertEqual(signature_discharge.structural_row, row.structural_row)
        signature_template_branch_audit = (
            parallel_direction_conjugate_ideal_signature_template_branch_audit(
                1250,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_SIGNATURE_TEMPLATE_ROWS,
            )
        )
        self.assertEqual(
            signature_template_branch_audit.checked_strip_failures,
            branch_audit.checked_strip_failures,
        )
        self.assertEqual(
            signature_template_branch_audit.local_discharge_count,
            branch_audit.local_discharge_count,
        )
        self.assertEqual(signature_template_branch_audit.global_discharge_count, 62)
        self.assertEqual(
            signature_template_branch_audit.global_branch_counts,
            (("alternate_signature_template", 62),),
        )
        self.assertEqual(signature_template_branch_audit.missing_rows, ())
        self.assertEqual(signature_template_branch_audit.unreconstructed_rows, ())
        self.assertEqual(
            tuple(
                (row.target, row.direction, row.obligation, row.structural_row)
                for row in signature_template_branch_audit.global_rows
            ),
            tuple(
                (row.target, row.direction, row.obligation, row.structural_row)
                for row in branch_audit.global_rows
            ),
        )
        signature_template_shape_audit = global_root_choice_signature_template_shape_audit(
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_SIGNATURE_TEMPLATE_ROWS
        )
        self.assertEqual(signature_template_shape_audit.row_count, 60)
        self.assertEqual(signature_template_shape_audit.signature_count, 27)
        self.assertEqual(signature_template_shape_audit.template_count, 40)
        self.assertEqual(
            signature_template_shape_audit.normalized_template_shape_count,
            27,
        )
        self.assertEqual(
            signature_template_shape_audit.normalized_signature_template_shape_count,
            44,
        )
        self.assertEqual(
            signature_template_shape_audit.root_shape_counts,
            (
                ((2, 3), 22),
                ((1, 6), 14),
                ((1, 4), 10),
                ((2, 5), 6),
                ((2, 7), 4),
                ((3, 8), 2),
                ((4, 5), 2),
            ),
        )

    @pytest.mark.perf
    def test_pinned_strip_global_root_choice_portable_row_audit_1500(self):
        extended_rows = (
            PINNED_GLOBAL_ROOT_CHOICE_ALTERNATE_LINE_STRIP_ROWS
            + PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_GENERIC_LINE_STRIP_ROWS
        )
        prior_template_rows = global_root_choice_line_template_table_rows(
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_DOMINANT_LINE_TEMPLATES
            + PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_RESIDUAL_LINE_TEMPLATES
            + PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_RESIDUAL_LINE_TEMPLATES
        )
        row_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_portable_row_audit(
                1500,
                extended_rows + prior_template_rows,
            )
        )
        self.assertEqual(row_audit.global_row_count, 112)
        self.assertEqual(row_audit.distinct_row_count, 112)
        self.assertEqual(row_audit.new_row_count, 50)
        self.assertEqual(
            row_audit.new_root_shape_counts,
            (((2, 3), 28), ((4, 5), 10), ((2, 5), 6), ((1, 4), 4), ((1, 6), 2)),
        )
        self.assertEqual(
            tuple(row[:6] for row in row_audit.new_line_template_counts),
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1500_RESIDUAL_LINE_TEMPLATES,
        )
        radius_1500_template_rows = global_root_choice_line_template_table_rows(
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1500_RESIDUAL_LINE_TEMPLATES
        )
        self.assertEqual(len(radius_1500_template_rows), 823)
        self.assertTrue(
            all(
                pinned_global_root_choice_alternate_line_strip_row_valid(row)
                for row in radius_1500_template_rows
            )
        )
        closure_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_template_closure_audit(
                1500,
                extended_rows + prior_template_rows,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1500_RESIDUAL_LINE_TEMPLATES,
            )
        )
        self.assertEqual(closure_audit.template_count, 30)
        self.assertEqual(closure_audit.template_expanded_row_count, 823)
        self.assertEqual(closure_audit.portable_row_audit.global_row_count, 112)
        self.assertEqual(closure_audit.portable_row_audit.distinct_row_count, 112)
        self.assertEqual(closure_audit.portable_row_audit.new_row_count, 0)
        self.assertEqual(closure_audit.portable_row_audit.new_root_shape_counts, ())
        self.assertEqual(closure_audit.portable_row_audit.new_line_template_counts, ())
        branch_audit = parallel_direction_conjugate_ideal_global_root_choice_branch_audit(
            1500
        )
        iterated_signature_template_closure = (
            parallel_direction_conjugate_ideal_global_root_choice_iterated_signature_template_closure_audit(
                1500,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_SIGNATURE_TEMPLATE_ROWS,
                max_iterations=2,
                branch_audit=branch_audit,
            )
        )
        self.assertTrue(iterated_signature_template_closure.closed)
        self.assertEqual(iterated_signature_template_closure.base_row_count, 60)
        self.assertEqual(iterated_signature_template_closure.final_row_count, 108)
        self.assertEqual(len(iterated_signature_template_closure.final_rows), 108)
        self.assertTrue(
            set(PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_SIGNATURE_TEMPLATE_ROWS).issubset(
                iterated_signature_template_closure.final_rows
            )
        )
        self.assertEqual(iterated_signature_template_closure.iteration_count, 1)
        self.assertEqual(
            iterated_signature_template_closure.final_coverage_audit.global_row_count,
            112,
        )
        self.assertEqual(
            iterated_signature_template_closure.final_coverage_audit.covered_count,
            112,
        )
        self.assertEqual(
            iterated_signature_template_closure.final_coverage_audit.missing_count,
            0,
        )
        self.assertEqual(
            iterated_signature_template_closure.final_coverage_audit.mismatch_count,
            0,
        )
        self.assertEqual(
            tuple(
                (
                    layer.iteration,
                    layer.input_row_count,
                    layer.missing_count,
                    layer.new_row_count,
                    layer.output_row_count,
                )
                for layer in iterated_signature_template_closure.layers
            ),
            ((1, 60, 50, 48, 108),),
        )
        self.assertEqual(len(iterated_signature_template_closure.layers[0].new_rows), 48)
        self.assertTrue(
            set(iterated_signature_template_closure.layers[0].new_rows).isdisjoint(
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_SIGNATURE_TEMPLATE_ROWS
            )
        )
        self.assertEqual(
            iterated_signature_template_closure.layers[0].missing_root_shape_counts,
            (((2, 3), 28), ((4, 5), 10), ((2, 5), 6), ((1, 4), 4), ((1, 6), 2)),
        )
        self.assertEqual(
            (
                iterated_signature_template_closure.layers[0].new_signature_count,
                iterated_signature_template_closure.layers[0].novel_signature_count,
                iterated_signature_template_closure.layers[0].new_template_count,
                iterated_signature_template_closure.layers[0].novel_template_count,
                iterated_signature_template_closure.layers[
                    0
                ].new_normalized_template_shape_count,
                iterated_signature_template_closure.layers[
                    0
                ].novel_normalized_template_shape_count,
                iterated_signature_template_closure.layers[
                    0
                ].new_normalized_signature_template_shape_count,
                iterated_signature_template_closure.layers[
                    0
                ].novel_normalized_signature_template_shape_count,
            ),
            (18, 12, 30, 30, 19, 19, 33, 33),
        )
        signature_template_branch_audit = (
            parallel_direction_conjugate_ideal_signature_template_branch_audit(
                1500,
                iterated_signature_template_closure.final_rows,
            )
        )
        self.assertEqual(
            signature_template_branch_audit.checked_strip_failures,
            branch_audit.checked_strip_failures,
        )
        self.assertEqual(
            signature_template_branch_audit.local_discharge_count,
            branch_audit.local_discharge_count,
        )
        self.assertEqual(signature_template_branch_audit.global_discharge_count, 112)
        self.assertEqual(
            signature_template_branch_audit.global_branch_counts,
            (("alternate_signature_template", 112),),
        )
        self.assertEqual(signature_template_branch_audit.missing_rows, ())
        self.assertEqual(signature_template_branch_audit.unreconstructed_rows, ())
        self.assertEqual(
            tuple(
                (row.target, row.direction, row.obligation, row.structural_row)
                for row in signature_template_branch_audit.global_rows
            ),
            tuple(
                (row.target, row.direction, row.obligation, row.structural_row)
                for row in branch_audit.global_rows
            ),
        )

    @pytest.mark.perf
    def test_pinned_strip_global_root_choice_portable_row_audit_1750(self):
        extended_rows = (
            PINNED_GLOBAL_ROOT_CHOICE_ALTERNATE_LINE_STRIP_ROWS
            + PINNED_GLOBAL_ROOT_CHOICE_RADIUS_750_GENERIC_LINE_STRIP_ROWS
        )
        prior_template_rows = global_root_choice_line_template_table_rows(
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_DOMINANT_LINE_TEMPLATES
            + PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1000_RESIDUAL_LINE_TEMPLATES
            + PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_RESIDUAL_LINE_TEMPLATES
            + PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1500_RESIDUAL_LINE_TEMPLATES
        )
        row_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_portable_row_audit(
                1750,
                extended_rows + prior_template_rows,
            )
        )
        self.assertEqual(row_audit.global_row_count, 148)
        self.assertEqual(row_audit.distinct_row_count, 148)
        self.assertEqual(row_audit.new_row_count, 36)
        self.assertEqual(
            row_audit.new_root_shape_counts,
            (((2, 3), 16), ((2, 5), 8), ((1, 4), 6), ((4, 5), 6)),
        )
        self.assertEqual(
            tuple(row[:6] for row in row_audit.new_line_template_counts),
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1750_RESIDUAL_LINE_TEMPLATES,
        )
        radius_1750_template_rows = global_root_choice_line_template_table_rows(
            PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1750_RESIDUAL_LINE_TEMPLATES
        )
        self.assertEqual(len(radius_1750_template_rows), 523)
        self.assertTrue(
            all(
                pinned_global_root_choice_alternate_line_strip_row_valid(row)
                for row in radius_1750_template_rows
            )
        )
        closure_audit = (
            parallel_direction_conjugate_ideal_global_root_choice_template_closure_audit(
                1750,
                extended_rows + prior_template_rows,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1750_RESIDUAL_LINE_TEMPLATES,
            )
        )
        self.assertEqual(closure_audit.template_count, 18)
        self.assertEqual(closure_audit.template_expanded_row_count, 523)
        self.assertEqual(closure_audit.portable_row_audit.global_row_count, 148)
        self.assertEqual(closure_audit.portable_row_audit.distinct_row_count, 148)
        self.assertEqual(closure_audit.portable_row_audit.new_row_count, 0)
        self.assertEqual(closure_audit.portable_row_audit.new_root_shape_counts, ())
        self.assertEqual(closure_audit.portable_row_audit.new_line_template_counts, ())
        branch_audit_1500 = (
            parallel_direction_conjugate_ideal_global_root_choice_branch_audit(1500)
        )
        signature_template_closure_1500 = (
            parallel_direction_conjugate_ideal_global_root_choice_iterated_signature_template_closure_audit(
                1500,
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_SIGNATURE_TEMPLATE_ROWS,
                max_iterations=2,
                branch_audit=branch_audit_1500,
            )
        )
        self.assertTrue(signature_template_closure_1500.closed)
        self.assertEqual(signature_template_closure_1500.final_row_count, 108)
        branch_audit_1750 = (
            parallel_direction_conjugate_ideal_global_root_choice_branch_audit(1750)
        )
        signature_template_closure_1750 = (
            parallel_direction_conjugate_ideal_global_root_choice_iterated_signature_template_closure_audit(
                1750,
                signature_template_closure_1500.final_rows,
                max_iterations=2,
                branch_audit=branch_audit_1750,
            )
        )
        self.assertTrue(signature_template_closure_1750.closed)
        self.assertEqual(signature_template_closure_1750.base_row_count, 108)
        self.assertEqual(signature_template_closure_1750.final_row_count, 144)
        self.assertEqual(signature_template_closure_1750.iteration_count, 1)
        self.assertEqual(
            signature_template_closure_1750.final_coverage_audit.global_row_count,
            148,
        )
        self.assertEqual(
            signature_template_closure_1750.final_coverage_audit.covered_count,
            148,
        )
        self.assertEqual(
            signature_template_closure_1750.final_coverage_audit.missing_count,
            0,
        )
        self.assertEqual(
            signature_template_closure_1750.final_coverage_audit.mismatch_count,
            0,
        )
        self.assertEqual(
            tuple(
                (
                    layer.iteration,
                    layer.input_row_count,
                    layer.missing_count,
                    layer.new_row_count,
                    layer.output_row_count,
                )
                for layer in signature_template_closure_1750.layers
            ),
            ((1, 108, 36, 36, 144),),
        )
        self.assertEqual(
            signature_template_closure_1750.layers[0].missing_root_shape_counts,
            (((2, 3), 16), ((2, 5), 8), ((1, 4), 6), ((4, 5), 6)),
        )
        self.assertEqual(
            (
                signature_template_closure_1750.layers[0].new_signature_count,
                signature_template_closure_1750.layers[0].novel_signature_count,
                signature_template_closure_1750.layers[0].new_template_count,
                signature_template_closure_1750.layers[0].novel_template_count,
                signature_template_closure_1750.layers[
                    0
                ].new_normalized_template_shape_count,
                signature_template_closure_1750.layers[
                    0
                ].novel_normalized_template_shape_count,
                signature_template_closure_1750.layers[
                    0
                ].new_normalized_signature_template_shape_count,
                signature_template_closure_1750.layers[
                    0
                ].novel_normalized_signature_template_shape_count,
            ),
            (20, 8, 18, 18, 14, 14, 28, 28),
        )
        signature_template_shape_audit = global_root_choice_signature_template_shape_audit(
            signature_template_closure_1750.final_rows
        )
        self.assertEqual(signature_template_shape_audit.row_count, 144)
        self.assertEqual(signature_template_shape_audit.signature_count, 47)
        self.assertEqual(signature_template_shape_audit.template_count, 88)
        self.assertEqual(
            signature_template_shape_audit.normalized_template_shape_count,
            60,
        )
        self.assertEqual(
            signature_template_shape_audit.normalized_signature_template_shape_count,
            105,
        )
        self.assertEqual(
            signature_template_shape_audit.root_shape_counts,
            (
                ((2, 3), 64),
                ((1, 4), 20),
                ((2, 5), 20),
                ((4, 5), 18),
                ((1, 6), 16),
                ((2, 7), 4),
                ((3, 8), 2),
            ),
        )

    @pytest.mark.perf
    def test_pinned_strip_global_root_choice_signature_template_closure_2000(self):
        signature_template_closure_chain = (
            parallel_direction_conjugate_ideal_global_root_choice_signature_template_closure_chain_audit(
                (1500, 1750, 2000),
                PINNED_GLOBAL_ROOT_CHOICE_RADIUS_1250_SIGNATURE_TEMPLATE_ROWS,
                max_iterations_per_radius=2,
            )
        )
        self.assertTrue(signature_template_closure_chain.closed)
        self.assertEqual(signature_template_closure_chain.base_row_count, 60)
        self.assertEqual(signature_template_closure_chain.final_row_count, 192)
        self.assertEqual(len(signature_template_closure_chain.final_rows), 192)
        self.assertEqual(
            tuple(stage.max_coordinate for stage in signature_template_closure_chain.stages),
            (1500, 1750, 2000),
        )
        self.assertEqual(
            tuple(stage.final_row_count for stage in signature_template_closure_chain.stages),
            (108, 144, 192),
        )
        self.assertEqual(
            tuple(
                (
                    row.max_coordinate,
                    row.input_row_count,
                    row.output_row_count,
                    row.global_row_count,
                    row.covered_count,
                    row.final_missing_count,
                    row.mismatch_count,
                    row.iteration_count,
                    row.initial_missing_count,
                    row.new_row_count,
                    row.new_row_modulus_counts,
                    row.new_signature_count,
                    row.novel_signature_count,
                    row.new_signature_modulus_counts,
                    row.novel_signature_modulus_counts,
                    row.new_template_count,
                    row.novel_template_count,
                    row.new_normalized_template_shape_count,
                    row.novel_normalized_template_shape_count,
                    row.new_normalized_template_root_shape_counts,
                    row.novel_normalized_template_root_shape_counts,
                    row.new_normalized_signature_template_shape_count,
                    row.novel_normalized_signature_template_shape_count,
                    row.new_normalized_signature_template_root_shape_counts,
                    row.novel_normalized_signature_template_root_shape_counts,
                    row.new_normalized_signature_template_modulus_root_shape_counts,
                    row.novel_normalized_signature_template_modulus_root_shape_counts,
                    row.reused_normalized_template_shape_count,
                    row.reused_normalized_signature_template_shape_count,
                    row.reused_normalized_template_root_shape_counts,
                    row.reused_normalized_signature_template_root_shape_counts,
                    row.reused_normalized_signature_template_modulus_root_shape_counts,
                    row.missing_root_shape_counts,
                    row.missing_obligation_counts,
                )
                for row in signature_template_closure_chain.ledger_rows
            ),
            (
                (
                    1500,
                    60,
                    108,
                    112,
                    112,
                    0,
                    0,
                    1,
                    50,
                    48,
                    ((13, 34), (17, 10), (73, 4)),
                    18,
                    12,
                    ((13, 10), (17, 4), (73, 4)),
                    ((13, 6), (73, 4), (17, 2)),
                    30,
                    30,
                    19,
                    19,
                    (
                        ((2, 3), 10),
                        ((4, 5), 4),
                        ((1, 4), 2),
                        ((2, 5), 2),
                        ((1, 6), 1),
                    ),
                    (
                        ((2, 3), 10),
                        ((4, 5), 4),
                        ((1, 4), 2),
                        ((2, 5), 2),
                        ((1, 6), 1),
                    ),
                    33,
                    33,
                    (
                        ((2, 3), 20),
                        ((4, 5), 7),
                        ((2, 5), 3),
                        ((1, 4), 2),
                        ((1, 6), 1),
                    ),
                    (
                        ((2, 3), 20),
                        ((4, 5), 7),
                        ((2, 5), 3),
                        ((1, 4), 2),
                        ((1, 6), 1),
                    ),
                    (
                        (13, (2, 3), 13),
                        (13, (4, 5), 6),
                        (73, (2, 3), 4),
                        (17, (2, 3), 3),
                        (13, (2, 5), 2),
                        (13, (1, 4), 1),
                        (13, (1, 6), 1),
                        (17, (1, 4), 1),
                        (17, (2, 5), 1),
                        (17, (4, 5), 1),
                    ),
                    (
                        (13, (2, 3), 13),
                        (13, (4, 5), 6),
                        (73, (2, 3), 4),
                        (17, (2, 3), 3),
                        (13, (2, 5), 2),
                        (13, (1, 4), 1),
                        (13, (1, 6), 1),
                        (17, (1, 4), 1),
                        (17, (2, 5), 1),
                        (17, (4, 5), 1),
                    ),
                    0,
                    0,
                    (),
                    (),
                    (),
                    (
                        ((2, 3), 28),
                        ((4, 5), 10),
                        ((2, 5), 6),
                        ((1, 4), 4),
                        ((1, 6), 2),
                    ),
                    (
                        (((2, 3), 1, 13, 5, 7, 4, 11), 18),
                        (((2, 3), 1, 13, 8, 6, 4, 11), 18),
                        (((1, 4), 2, 17, 4, 2, 9, 3), 5),
                        (((1, 4), 2, 17, 13, 15, 9, 3), 5),
                        (((3, 8), 1, 73, 27, 38, 69, 19), 2),
                        (((3, 8), 1, 73, 46, 38, 4, 71), 2),
                    ),
                ),
                (
                    1750,
                    108,
                    144,
                    148,
                    148,
                    0,
                    0,
                    1,
                    36,
                    36,
                    ((13, 20), (17, 8), (41, 4), (73, 4)),
                    20,
                    8,
                    ((13, 8), (17, 4), (41, 4), (73, 4)),
                    ((13, 2), (17, 2), (41, 2), (73, 2)),
                    18,
                    18,
                    14,
                    14,
                    (((2, 3), 9), ((2, 5), 2), ((4, 5), 2), ((1, 4), 1)),
                    (((2, 3), 9), ((2, 5), 2), ((4, 5), 2), ((1, 4), 1)),
                    28,
                    28,
                    (((2, 3), 14), ((4, 5), 6), ((1, 4), 4), ((2, 5), 4)),
                    (((2, 3), 14), ((4, 5), 6), ((1, 4), 4), ((2, 5), 4)),
                    (
                        (13, (2, 3), 9),
                        (13, (1, 4), 2),
                        (13, (2, 5), 2),
                        (13, (4, 5), 2),
                        (17, (2, 5), 2),
                        (17, (4, 5), 2),
                        (41, (2, 3), 2),
                        (41, (4, 5), 2),
                        (73, (1, 4), 2),
                        (73, (2, 3), 2),
                        (17, (2, 3), 1),
                    ),
                    (
                        (13, (2, 3), 9),
                        (13, (1, 4), 2),
                        (13, (2, 5), 2),
                        (13, (4, 5), 2),
                        (17, (2, 5), 2),
                        (17, (4, 5), 2),
                        (41, (2, 3), 2),
                        (41, (4, 5), 2),
                        (73, (1, 4), 2),
                        (73, (2, 3), 2),
                        (17, (2, 3), 1),
                    ),
                    0,
                    0,
                    (),
                    (),
                    (),
                    (((2, 3), 16), ((2, 5), 8), ((1, 4), 6), ((4, 5), 6)),
                    (
                        (((2, 3), 1, 13, 5, 7, 4, 11), 10),
                        (((2, 3), 1, 13, 8, 6, 4, 11), 10),
                        (((1, 4), 2, 17, 4, 2, 9, 3), 4),
                        (((1, 4), 2, 17, 13, 15, 9, 3), 4),
                        (((3, 8), 1, 73, 27, 38, 69, 19), 2),
                        (((3, 8), 1, 73, 46, 38, 4, 71), 2),
                        (((4, 5), 2, 41, 9, 10, 33, 19), 2),
                        (((4, 5), 2, 41, 32, 10, 8, 34), 2),
                    ),
                ),
                (
                    2000,
                    144,
                    192,
                    198,
                    198,
                    0,
                    0,
                    1,
                    50,
                    48,
                    ((13, 26), (41, 10), (17, 8), (73, 3), (29, 1)),
                    22,
                    12,
                    ((13, 8), (41, 8), (73, 3), (17, 2), (29, 1)),
                    ((41, 6), (73, 3), (13, 2), (29, 1)),
                    36,
                    36,
                    26,
                    25,
                    (((2, 3), 14), ((1, 4), 10), ((3, 4), 2)),
                    (((2, 3), 14), ((1, 4), 9), ((3, 4), 2)),
                    39,
                    38,
                    (((2, 3), 22), ((1, 4), 15), ((3, 4), 2)),
                    (((2, 3), 22), ((1, 4), 14), ((3, 4), 2)),
                    (
                        (13, (2, 3), 12),
                        (13, (1, 4), 6),
                        (17, (2, 3), 4),
                        (41, (1, 4), 4),
                        (41, (2, 3), 4),
                        (17, (1, 4), 3),
                        (41, (3, 4), 2),
                        (73, (1, 4), 2),
                        (29, (2, 3), 1),
                        (73, (2, 3), 1),
                    ),
                    (
                        (13, (2, 3), 12),
                        (13, (1, 4), 5),
                        (17, (2, 3), 4),
                        (41, (1, 4), 4),
                        (41, (2, 3), 4),
                        (17, (1, 4), 3),
                        (41, (3, 4), 2),
                        (73, (1, 4), 2),
                        (29, (2, 3), 1),
                        (73, (2, 3), 1),
                    ),
                    1,
                    1,
                    (((1, 4), 1),),
                    (((1, 4), 1),),
                    ((13, (1, 4), 1),),
                    (((2, 3), 26), ((1, 4), 22), ((3, 4), 2)),
                    (
                        (((2, 3), 1, 13, 5, 7, 4, 11), 14),
                        (((2, 3), 1, 13, 8, 6, 4, 11), 14),
                        (((4, 5), 2, 41, 9, 10, 33, 19), 5),
                        (((4, 5), 2, 41, 32, 10, 8, 34), 5),
                        (((1, 4), 2, 17, 4, 2, 9, 3), 4),
                        (((1, 4), 2, 17, 13, 15, 9, 3), 4),
                        (((3, 8), 1, 73, 27, 38, 69, 19), 2),
                        (((2, 5), 10, 29, 17, 12, 28, 17), 1),
                        (((3, 8), 1, 73, 46, 38, 4, 71), 1),
                    ),
                ),
            ),
        )
        (
            signature_template_closure_1500,
            signature_template_closure_1750,
            signature_template_closure_2000,
        ) = signature_template_closure_chain.stages
        self.assertTrue(signature_template_closure_1500.closed)
        self.assertEqual(signature_template_closure_1500.final_row_count, 108)
        self.assertTrue(signature_template_closure_1750.closed)
        self.assertEqual(signature_template_closure_1750.final_row_count, 144)
        self.assertTrue(signature_template_closure_2000.closed)
        self.assertEqual(signature_template_closure_2000.base_row_count, 144)
        self.assertEqual(signature_template_closure_2000.final_row_count, 192)
        self.assertEqual(signature_template_closure_2000.iteration_count, 1)
        self.assertEqual(
            signature_template_closure_2000.final_coverage_audit.global_row_count,
            198,
        )
        self.assertEqual(
            signature_template_closure_2000.final_coverage_audit.covered_count,
            198,
        )
        self.assertEqual(
            signature_template_closure_2000.final_coverage_audit.missing_count,
            0,
        )
        self.assertEqual(
            signature_template_closure_2000.final_coverage_audit.mismatch_count,
            0,
        )
        self.assertEqual(
            tuple(
                (
                    layer.iteration,
                    layer.input_row_count,
                    layer.missing_count,
                    layer.new_row_count,
                    layer.output_row_count,
                )
                for layer in signature_template_closure_2000.layers
            ),
            ((1, 144, 50, 48, 192),),
        )
        self.assertEqual(
            signature_template_closure_2000.layers[0].missing_root_shape_counts,
            (((2, 3), 26), ((1, 4), 22), ((3, 4), 2)),
        )
        self.assertEqual(
            signature_template_closure_2000.layers[
                0
            ].reused_normalized_template_shapes,
            (((1, 4), 17, (1, 1033), 34),),
        )
        self.assertEqual(
            signature_template_closure_2000.layers[
                0
            ].reused_normalized_signature_template_shapes,
            ((13, 7, False, 1, ((0, 11),), (1, 4), 17, (1, 1033), 34),),
        )
        self.assertEqual(
            (
                signature_template_closure_2000.layers[0].new_signature_count,
                signature_template_closure_2000.layers[0].novel_signature_count,
                signature_template_closure_2000.layers[0].new_template_count,
                signature_template_closure_2000.layers[0].novel_template_count,
                signature_template_closure_2000.layers[
                    0
                ].new_normalized_template_shape_count,
                signature_template_closure_2000.layers[
                    0
                ].novel_normalized_template_shape_count,
                signature_template_closure_2000.layers[
                    0
                ].new_normalized_signature_template_shape_count,
                signature_template_closure_2000.layers[
                    0
                ].novel_normalized_signature_template_shape_count,
            ),
            (22, 12, 36, 36, 26, 25, 39, 38),
        )
        signature_template_shape_audit = global_root_choice_signature_template_shape_audit(
            signature_template_closure_2000.final_rows
        )
        self.assertEqual(signature_template_shape_audit.row_count, 192)
        self.assertEqual(signature_template_shape_audit.signature_count, 59)
        self.assertEqual(signature_template_shape_audit.template_count, 124)
        self.assertEqual(
            signature_template_shape_audit.normalized_template_shape_count,
            85,
        )
        self.assertEqual(
            signature_template_shape_audit.normalized_signature_template_shape_count,
            143,
        )
        self.assertEqual(
            signature_template_shape_audit.root_shape_counts,
            (
                ((2, 3), 90),
                ((1, 4), 40),
                ((2, 5), 20),
                ((4, 5), 18),
                ((1, 6), 16),
                ((2, 7), 4),
                ((3, 4), 2),
                ((3, 8), 2),
            ),
        )

    def test_one_two_root_spine_line_certificate(self):
        counterexample_certificate = one_two_root_spine_line_certificate(
            535,
            -95,
            9586654,
        )
        self.assertIsNotNone(counterexample_certificate)
        self.assertEqual(counterexample_certificate.target, (108638, 24031))
        self.assertEqual(counterexample_certificate.midpoint, (-28759962, 38346616))
        self.assertTrue(counterexample_certificate.valid())

        for q, t, r in (
            (1, 1, 1),
            (-3, 2, 5),
            (6, -2, -7),
            (11, 3, -13),
        ):
            with self.subTest(q=q, t=t, r=r):
                certificate = one_two_root_spine_line_certificate(q, t, r)
                self.assertIsNotNone(certificate)
                self.assertTrue(certificate.valid())
                self.assertEqual(certificate.midpoint, (-3 * r, 4 * r))

        self.assertIsNone(one_two_root_spine_line_certificate(0, 1, 1))
        self.assertIsNone(one_two_root_spine_line_certificate(1, 0, 1))
        self.assertIsNone(one_two_root_spine_line_certificate(1, 1, 0))

    def test_one_even_root_spine_line_certificate(self):
        for spine_parameter_k in range(1, 8):
            first_direction = (
                1 - 4 * spine_parameter_k * spine_parameter_k,
                4 * spine_parameter_k,
            )
            self.assertTrue(edge((0, 0), first_direction))

            for q, t, r in (
                (1, 1, 1),
                (-3, 2, 5),
                (6, -2, -7),
                (11, 3, -13),
            ):
                with self.subTest(k=spine_parameter_k, q=q, t=t, r=r):
                    certificate = one_even_root_spine_line_certificate(
                        spine_parameter_k,
                        q,
                        t,
                        r,
                    )
                    self.assertIsNotNone(certificate)
                    self.assertEqual(
                        certificate.midpoint,
                        (first_direction[0] * r, first_direction[1] * r),
                    )
                    self.assertTrue(certificate.valid())
                    for orbit_target in sign_swap_orbit(certificate.target):
                        orbit_certificate = one_even_root_spine_line_orbit_certificate(
                            spine_parameter_k,
                            q,
                            t,
                            r,
                            orbit_target,
                        )
                        self.assertIsNotNone(orbit_certificate)
                        self.assertEqual(orbit_certificate.target, orbit_target)
                        self.assertTrue(orbit_certificate.valid())

        for q, t, r in ((1, 1, 1), (-3, 2, 5), (6, -2, -7)):
            self.assertEqual(
                one_even_root_spine_line_certificate(1, q, t, r),
                one_two_root_spine_line_certificate(q, t, r),
            )

        certificate = one_even_root_spine_line_certificate(2, 269, 124, 8317762)
        self.assertIsNotNone(certificate)
        self.assertEqual(
            certificate.target,
            (52_798, -103_999),
        )
        self.assertEqual(certificate.midpoint, (-124766430, 66542096))
        self.assertTrue(certificate.valid())

        self.assertIsNone(one_even_root_spine_line_certificate(1, 0, 1, 1))
        self.assertIsNone(one_even_root_spine_line_certificate(1, 1, 0, 1))
        self.assertIsNone(one_even_root_spine_line_certificate(1, 1, 1, 0))
        self.assertIsNone(
            one_even_root_spine_line_orbit_certificate(1, 0, 1, 1, (1, 1))
        )
        self.assertIsNone(
            one_even_root_spine_line_orbit_certificate(1, 1, 1, 1, (1, 1))
        )
        with self.assertRaises(ValueError):
            one_even_root_spine_line_certificate(0, 1, 1, 1)

    def test_one_four_root_spine_line_certificate(self):
        base_certificate = one_four_root_spine_line_certificate(
            269,
            124,
            8317762,
        )
        self.assertIsNotNone(base_certificate)
        self.assertEqual(base_certificate.target, (103999, 52798))
        self.assertEqual(base_certificate.midpoint, (-66542096, -124766430))
        self.assertTrue(base_certificate.valid())

        swapped_certificate = one_four_root_spine_line_certificate(
            269,
            124,
            8317762,
            swap_coordinates=True,
        )
        self.assertIsNotNone(swapped_certificate)
        self.assertEqual(swapped_certificate.target, (52798, 103999))
        self.assertEqual(swapped_certificate.midpoint, (-124766430, -66542096))
        self.assertTrue(swapped_certificate.valid())

        for q, t, r, swap_coordinates in (
            (1, 0, 1, False),
            (-3, 2, 5, True),
            (6, -2, -7, False),
            (11, 3, -13, True),
        ):
            with self.subTest(q=q, t=t, r=r, swap_coordinates=swap_coordinates):
                certificate = one_four_root_spine_line_certificate(
                    q,
                    t,
                    r,
                    swap_coordinates=swap_coordinates,
                )
                self.assertIsNotNone(certificate)
                self.assertTrue(certificate.valid())

        self.assertIsNone(one_four_root_spine_line_certificate(0, 1, 1))
        self.assertIsNone(one_four_root_spine_line_certificate(1, 1, 0))

    def test_two_three_root_spine_line_certificates(self):
        base_certificate = two_three_odd_root_spine_line_certificate(
            11,
            459,
            4619042,
        )
        self.assertIsNotNone(base_certificate)
        self.assertEqual(base_certificate.target, (140801, 69602))
        self.assertEqual(base_certificate.midpoint, (-55428504, -23095210))
        self.assertTrue(base_certificate.valid())

        swapped_certificate = two_three_odd_root_spine_line_certificate(
            11,
            459,
            4619042,
            swap_coordinates=True,
        )
        self.assertIsNotNone(swapped_certificate)
        self.assertEqual(swapped_certificate.target, (69602, 140801))
        self.assertEqual(swapped_certificate.midpoint, (-23095210, -55428504))
        self.assertTrue(swapped_certificate.valid())

        even_certificate = two_three_even_root_spine_line_certificate(
            1,
            -953,
            425,
            22769,
        )
        self.assertIsNotNone(even_certificate)
        self.assertEqual(even_certificate.target, (536822, 613739))
        self.assertEqual(even_certificate.midpoint, (-273228, -113845))
        self.assertTrue(even_certificate.valid())

        for q, t, r, swap_coordinates in (
            (1, 1, 1, False),
            (-3, 2, 5, True),
            (6, -2, -7, False),
            (11, 3, -13, True),
        ):
            with self.subTest(q=q, t=t, r=r, swap_coordinates=swap_coordinates):
                certificate = two_three_odd_root_spine_line_certificate(
                    q,
                    t,
                    r,
                    swap_coordinates=swap_coordinates,
                )
                self.assertIsNotNone(certificate)
                self.assertTrue(certificate.valid())

        for m, beta_x, beta_y, r in (
            (1, 2, 3, 1),
            (-3, -5, 7, 11),
            (6, 4, -9, -13),
        ):
            with self.subTest(m=m, beta_x=beta_x, beta_y=beta_y, r=r):
                certificate = two_three_even_root_spine_line_certificate(
                    m,
                    beta_x,
                    beta_y,
                    r,
                )
                self.assertIsNotNone(certificate)
                self.assertTrue(certificate.valid())

        self.assertIsNone(two_three_odd_root_spine_line_certificate(0, 1, 1))
        self.assertIsNone(two_three_odd_root_spine_line_certificate(1, 0, 1))
        self.assertIsNone(two_three_odd_root_spine_line_certificate(1, 1, 0))
        self.assertIsNone(two_three_even_root_spine_line_certificate(0, 1, 2, 1))
        self.assertIsNone(two_three_even_root_spine_line_certificate(1, 0, 2, 1))
        self.assertIsNone(two_three_even_root_spine_line_certificate(1, 2, 0, 1))
        self.assertIsNone(two_three_even_root_spine_line_certificate(1, 2, 2, 1))
        self.assertIsNone(two_three_even_root_spine_line_certificate(1, 1, 2, 0))

    def test_two_odd_root_spine_line_certificate(self):
        for spine_parameter_k in range(1, 8):
            odd_coordinate = 2 * spine_parameter_k + 1
            first_direction = (-4 * odd_coordinate, 4 - odd_coordinate * odd_coordinate)
            self.assertTrue(edge((0, 0), first_direction))

            for q, t, r, swap_coordinates in (
                (1, 1, 1, False),
                (-3, 2, 5, True),
                (6, -2, -7, False),
                (11, 3, -13, True),
            ):
                with self.subTest(
                    k=spine_parameter_k,
                    q=q,
                    t=t,
                    r=r,
                    swap_coordinates=swap_coordinates,
                ):
                    certificate = two_odd_root_spine_line_certificate(
                        spine_parameter_k,
                        q,
                        t,
                        r,
                        swap_coordinates=swap_coordinates,
                    )
                    self.assertIsNotNone(certificate)
                    if swap_coordinates:
                        self.assertEqual(
                            certificate.midpoint,
                            (first_direction[1] * r, first_direction[0] * r),
                        )
                    else:
                        self.assertEqual(
                            certificate.midpoint,
                            (first_direction[0] * r, first_direction[1] * r),
                        )
                    self.assertTrue(certificate.valid())
                    for orbit_target in sign_swap_orbit(certificate.target):
                        orbit_certificate = two_odd_root_spine_line_orbit_certificate(
                            spine_parameter_k,
                            q,
                            t,
                            r,
                            orbit_target,
                            swap_coordinates=swap_coordinates,
                        )
                        self.assertIsNotNone(orbit_certificate)
                        self.assertEqual(orbit_certificate.target, orbit_target)
                        self.assertTrue(orbit_certificate.valid())

        for q, t, r, swap_coordinates in (
            (1, 1, 1, False),
            (-3, 2, 5, True),
            (6, -2, -7, False),
        ):
            self.assertEqual(
                two_odd_root_spine_line_certificate(
                    1,
                    q,
                    t,
                    r,
                    swap_coordinates=swap_coordinates,
                ),
                two_three_odd_root_spine_line_certificate(
                    q,
                    t,
                    r,
                    swap_coordinates=swap_coordinates,
                ),
            )

        certificate = two_odd_root_spine_line_certificate(2, 5, -3, 11)
        self.assertIsNotNone(certificate)
        self.assertEqual(certificate.target, (1_795, 1_749))
        self.assertEqual(certificate.midpoint, (-220, -231))
        self.assertTrue(certificate.valid())

        self.assertIsNone(two_odd_root_spine_line_certificate(1, 0, 1, 1))
        self.assertIsNone(two_odd_root_spine_line_certificate(1, 1, 0, 1))
        self.assertIsNone(two_odd_root_spine_line_certificate(1, 1, 1, 0))
        self.assertIsNone(
            two_odd_root_spine_line_orbit_certificate(1, 0, 1, 1, (1, 1))
        )
        self.assertIsNone(
            two_odd_root_spine_line_orbit_certificate(1, 1, 1, 1, (1, 1))
        )
        with self.assertRaises(ValueError):
            two_odd_root_spine_line_certificate(0, 1, 1, 1)

    def test_two_five_root_spine_line_certificate(self):
        counterexample_certificate = two_five_root_spine_line_certificate(
            5,
            -109,
            273,
            -14897,
        )
        self.assertIsNotNone(counterexample_certificate)
        self.assertEqual(counterexample_certificate.target, (370, 403))
        self.assertEqual(counterexample_certificate.midpoint, (297940, -312837))
        self.assertTrue(counterexample_certificate.valid())

        swapped_certificate = two_five_root_spine_line_certificate(
            5,
            -273,
            109,
            14897,
            swap_coordinates=True,
        )
        self.assertIsNotNone(swapped_certificate)
        self.assertEqual(swapped_certificate.target, (403, 370))
        self.assertEqual(swapped_certificate.midpoint, (-312837, 297940))
        self.assertTrue(swapped_certificate.valid())

        for m, beta_x, beta_y, r, swap_coordinates in (
            (1, 1, 2, 1, False),
            (2, -3, 4, -5, False),
            (3, -5, 4, 7, True),
            (7, 9, 4, -11, True),
        ):
            with self.subTest(
                m=m,
                beta_x=beta_x,
                beta_y=beta_y,
                r=r,
                swap_coordinates=swap_coordinates,
            ):
                certificate = two_five_root_spine_line_certificate(
                    m,
                    beta_x,
                    beta_y,
                    r,
                    swap_coordinates=swap_coordinates,
                )
                self.assertIsNotNone(certificate)
                self.assertTrue(certificate.valid())

        self.assertIsNone(two_five_root_spine_line_certificate(0, 1, 2, 1))
        self.assertIsNone(two_five_root_spine_line_certificate(1, 0, 2, 1))
        self.assertIsNone(two_five_root_spine_line_certificate(1, 1, 0, 1))
        self.assertIsNone(two_five_root_spine_line_certificate(1, 1, 1, 0))

    def test_secondary_root_spine_line_certificates(self):
        one_four_even = one_four_even_root_spine_line_certificate(
            1,
            -13,
            -57,
            -227,
        )
        self.assertIsNotNone(one_four_even)
        self.assertEqual(one_four_even.target, (334, 325))
        self.assertEqual(one_four_even.midpoint, (1816, 3405))
        self.assertTrue(one_four_even.valid())

        one_four_even_swapped = one_four_even_root_spine_line_certificate(
            1,
            -13,
            57,
            -227,
            swap_coordinates=True,
        )
        self.assertIsNotNone(one_four_even_swapped)
        self.assertEqual(one_four_even_swapped.target, (325, 334))
        self.assertEqual(one_four_even_swapped.midpoint, (3405, 1816))
        self.assertTrue(one_four_even_swapped.valid())

        two_three_general = two_three_odd_general_root_spine_line_certificate(
            1,
            -31,
            18,
            166,
        )
        self.assertIsNotNone(two_three_general)
        self.assertEqual(two_three_general.target, (265, 346))
        self.assertEqual(two_three_general.midpoint, (-1992, -830))
        self.assertTrue(two_three_general.valid())

        two_three_general_swapped = two_three_odd_general_root_spine_line_certificate(
            1,
            -31,
            -19,
            166,
            swap_coordinates=True,
        )
        self.assertIsNotNone(two_three_general_swapped)
        self.assertEqual(two_three_general_swapped.target, (346, 265))
        self.assertEqual(two_three_general_swapped.midpoint, (-830, -1992))
        self.assertTrue(two_three_general_swapped.valid())

        four_five_certificate = four_five_root_spine_line_certificate(
            1,
            -31,
            21,
            41,
        )
        self.assertIsNotNone(four_five_certificate)
        self.assertEqual(four_five_certificate.target, (151, 338))
        self.assertEqual(four_five_certificate.midpoint, (-369, 1640))
        self.assertTrue(four_five_certificate.valid())

        four_five_swapped = four_five_root_spine_line_certificate(
            1,
            -21,
            31,
            -41,
            swap_coordinates=True,
        )
        self.assertIsNotNone(four_five_swapped)
        self.assertEqual(four_five_swapped.target, (338, 151))
        self.assertEqual(four_five_swapped.midpoint, (1640, -369))
        self.assertTrue(four_five_swapped.valid())

        for target in sign_swap_orbit((151, 338)):
            witness = parallel_direction_conjugate_ideal_root_spine_cover_witness(
                target,
                8,
            )
            self.assertIsNotNone(witness)
            self.assertEqual(gaussian_root_shape(witness.root_shape), (4, 5))
            self.assertEqual(
                promoted_root_spine_line_certificate_from_witness(witness),
                witness.certificate,
            )

        three_four_certificate = three_four_root_spine_line_certificate(
            1,
            5,
            7,
            11,
        )
        self.assertIsNotNone(three_four_certificate)
        self.assertEqual(three_four_certificate.target, (-101, 334))
        self.assertEqual(three_four_certificate.midpoint, (-77, 264))
        self.assertTrue(three_four_certificate.valid())

        three_four_swapped = three_four_root_spine_line_certificate(
            3,
            -5,
            4,
            7,
            swap_coordinates=True,
        )
        self.assertIsNotNone(three_four_swapped)
        self.assertEqual(three_four_swapped.target, (48, 22))
        self.assertEqual(three_four_swapped.midpoint, (168, 49))
        self.assertTrue(three_four_swapped.valid())

        three_four_odd = three_four_odd_root_spine_line_certificate(
            37,
            -16,
            11,
            1130,
        )
        self.assertIsNotNone(three_four_odd)
        self.assertEqual(three_four_odd.target, (82, 739))
        self.assertEqual(three_four_odd.midpoint, (-7910, 27120))
        self.assertTrue(three_four_odd.valid())

        signed_three_four_targets = (
            (2, 701),
            (5, 14),
            (14, 5),
            (14, 365),
            (22, 119),
            (34, 385),
            (41, 718),
            (50, 77),
            (62, 401),
            (77, 50),
        )
        for target in signed_three_four_targets:
            witness = parallel_direction_conjugate_ideal_root_spine_cover_witness(
                target,
                8,
            )
            self.assertIsNotNone(witness)
            self.assertEqual(gaussian_root_shape(witness.root_shape), (3, 4))
            self.assertEqual(
                promoted_root_spine_line_certificate_from_witness(witness),
                witness.certificate,
            )

        three_eight_certificate = three_eight_odd_root_spine_line_certificate(
            1,
            -33,
            -84,
            -218,
        )
        self.assertIsNotNone(three_eight_certificate)
        self.assertEqual(three_eight_certificate.target, (158, 391))
        self.assertEqual(three_eight_certificate.midpoint, (11990, -10464))
        self.assertTrue(three_eight_certificate.valid())

        three_eight_swapped = three_eight_odd_root_spine_line_certificate(
            1,
            83,
            32,
            218,
            swap_coordinates=True,
        )
        self.assertIsNotNone(three_eight_swapped)
        self.assertEqual(three_eight_swapped.target, (391, 158))
        self.assertEqual(three_eight_swapped.midpoint, (-10464, 11990))
        self.assertTrue(three_eight_swapped.valid())

        for target in sign_swap_orbit((158, 391)):
            witness = parallel_direction_conjugate_ideal_root_spine_cover_witness(
                target,
                8,
            )
            self.assertIsNotNone(witness)
            self.assertEqual(gaussian_root_shape(witness.root_shape), (3, 8))
            self.assertEqual(
                promoted_root_spine_line_certificate_from_witness(witness),
                witness.certificate,
            )

        self.assertIsNone(four_five_root_spine_line_certificate(0, 1, 2, 1))
        self.assertIsNone(four_five_root_spine_line_certificate(1, 0, 2, 1))
        self.assertIsNone(four_five_root_spine_line_certificate(1, 1, 0, 1))
        self.assertIsNone(four_five_root_spine_line_certificate(1, 1, 1, 1))
        self.assertIsNone(three_four_root_spine_line_certificate(0, 1, 2, 1))
        self.assertIsNone(three_four_root_spine_line_certificate(1, 0, 2, 1))
        self.assertIsNone(three_four_root_spine_line_certificate(1, 1, 0, 1))
        self.assertIsNone(three_four_root_spine_line_certificate(1, 1, 1, 1))
        self.assertIsNone(three_four_odd_root_spine_line_certificate(0, 1, 2, 1))
        self.assertIsNone(three_four_odd_root_spine_line_certificate(1, 1, 2, 0))
        self.assertIsNone(three_four_odd_root_spine_line_certificate(1, 0, 0, 1))
        self.assertIsNone(one_four_even_root_spine_line_certificate(0, 1, 2, 1))
        self.assertIsNone(one_four_even_root_spine_line_certificate(1, 0, 2, 1))
        self.assertIsNone(one_four_even_root_spine_line_certificate(1, 1, 0, 1))
        self.assertIsNone(one_four_even_root_spine_line_certificate(1, 1, 1, 1))
        self.assertIsNone(two_three_odd_general_root_spine_line_certificate(0, 1, 2, 1))
        self.assertIsNone(two_three_odd_general_root_spine_line_certificate(1, 1, 2, 0))
        self.assertIsNone(two_three_odd_general_root_spine_line_certificate(1, 0, 0, 1))
        self.assertIsNone(three_eight_odd_root_spine_line_certificate(0, 1, 2, 1))
        self.assertIsNone(three_eight_odd_root_spine_line_certificate(1, 1, 2, 0))
        self.assertIsNone(three_eight_odd_root_spine_line_certificate(1, 0, 0, 1))

    @pytest.mark.perf
    def test_conjugate_ideal_divisor_obligation_census(self):
        witness = parallel_direction_conjugate_ideal_witness((151, 338), (-9, 40))
        self.assertIsNotNone(witness)
        obligation = parallel_direction_conjugate_ideal_divisor_obligation_key(witness)
        self.assertEqual(obligation, ((4, 5), 2, 41, 9, 10, 33, 19))
        self.assertEqual(
            parallel_direction_conjugate_ideal_divisor_obligation_strip_modulus(
                obligation
            ),
            82,
        )
        self.assertEqual(
            parallel_direction_conjugate_ideal_divisor_obligation_strip_residue(
                obligation
            ),
            20,
        )
        self.assertTrue(
            parallel_direction_conjugate_ideal_divisor_obligation_strip_holds(
                (151, 338),
                (-9, 40),
                obligation,
            )
        )
        self.assertTrue(
            parallel_direction_conjugate_ideal_divisor_obligation_divisor_holds(
                (151, 338),
                (-9, 40),
                obligation,
            )
        )
        self.assertTrue(
            parallel_direction_conjugate_ideal_divisor_obligation_strip_holds(
                (1, 48),
                (-9, 40),
                obligation,
            )
        )
        self.assertFalse(
            parallel_direction_conjugate_ideal_divisor_obligation_divisor_holds(
                (1, 48),
                (-9, 40),
                obligation,
            )
        )
        self.assertEqual(pythagorean_layered_structural_label((1, 48)), "promoted_345")
        self.assertIsNone(pythagorean_layered_structural_label((151, 338)))
        self.assertFalse(
            parallel_direction_conjugate_ideal_divisor_obligation_strip_holds(
                (151, 339),
                (-9, 40),
                obligation,
            )
        )

        self.assertEqual(
            parallel_direction_conjugate_ideal_root_spine_divisor_obligation_census(
                500,
                8,
            ),
            ParallelDirectionConjugateIdealDivisorObligationCensus(
                max_coordinate=500,
                root_shapes=(
                    (1, 2),
                    (2, 3),
                    (1, 4),
                    (3, 4),
                    (2, 5),
                    (1, 6),
                    (4, 5),
                    (2, 7),
                    (1, 8),
                    (3, 8),
                ),
                target_count=152049,
                structural_miss_count=10,
                uncovered_targets=(),
                shape_squareclass_counts=(
                    ((2, 3), 1, 2),
                    ((1, 4), 2, 2),
                    ((2, 5), 10, 2),
                    ((4, 5), 2, 2),
                    ((3, 8), 1, 2),
                ),
                obligation_counts=(
                    ((2, 3), 1, 13, 5, 7, 4, 11, 1),
                    ((2, 3), 1, 13, 8, 6, 4, 11, 1),
                    ((1, 4), 2, 17, 4, 2, 9, 3, 1),
                    ((1, 4), 2, 17, 13, 15, 9, 3, 1),
                    ((2, 5), 10, 29, 12, 12, 1, 1, 1),
                    ((2, 5), 10, 29, 17, 12, 28, 17, 1),
                    ((4, 5), 2, 41, 9, 10, 33, 19, 1),
                    ((4, 5), 2, 41, 32, 10, 8, 34, 1),
                    ((3, 8), 1, 73, 27, 38, 69, 19, 1),
                    ((3, 8), 1, 73, 46, 38, 4, 71, 1),
                ),
            ),
        )

        primary_census = (
            parallel_direction_conjugate_ideal_root_shape_divisor_obligation_census(
                500,
                primitive_pythagorean_root_primary_spine_shapes(8),
            )
        )
        self.assertEqual(
            primary_census.uncovered_targets,
            ((151, 338), (158, 391), (338, 151), (391, 158)),
        )
        self.assertEqual(
            primary_census.shape_squareclass_counts,
            (((2, 3), 1, 2), ((1, 4), 2, 2), ((2, 5), 10, 2)),
        )
        obligations = tuple(
            row[:-1]
            for row in parallel_direction_conjugate_ideal_root_spine_divisor_obligation_census(
                500,
                8,
            ).obligation_counts
        )
        self.assertEqual(
            parallel_direction_conjugate_ideal_divisor_obligation_directions(
                obligations[0]
            ),
            ((-12, -5), (-5, 12), (5, -12), (12, 5)),
        )
        self.assertEqual(
            parallel_direction_conjugate_ideal_divisor_obligation_strip_census(
                100,
                obligations,
            ),
            ParallelDirectionConjugateIdealDivisorObligationStripCensus(
                max_coordinate=100,
                obligation_rows=(
                    ((2, 3), 1, 13, 5, 7, 4, 11, 1870, 467, 1403, 1403, 0),
                    ((2, 3), 1, 13, 8, 6, 4, 11, 1870, 467, 1403, 1403, 0),
                    ((1, 4), 2, 17, 4, 2, 9, 3, 472, 159, 313, 313, 0),
                    ((1, 4), 2, 17, 13, 15, 9, 3, 472, 159, 313, 313, 0),
                    ((2, 5), 10, 29, 12, 12, 1, 1, 44, 44, 0, 0, 0),
                    ((2, 5), 10, 29, 17, 12, 28, 17, 44, 20, 24, 24, 0),
                    ((4, 5), 2, 41, 9, 10, 33, 19, 196, 17, 179, 179, 0),
                    ((4, 5), 2, 41, 32, 10, 8, 34, 196, 8, 188, 188, 0),
                    ((3, 8), 1, 73, 27, 38, 69, 19, 327, 68, 259, 259, 0),
                    ((3, 8), 1, 73, 46, 38, 4, 71, 327, 11, 316, 316, 0),
                ),
                obligation_structural_failure_family_counts=(
                    (((2, 3), 1, 13, 5, 7, 4, 11), "lattice_pair", 53),
                    (((2, 3), 1, 13, 5, 7, 4, 11), "orthogonal", 3),
                    (((2, 3), 1, 13, 5, 7, 4, 11), "promoted_345", 1345),
                    (((2, 3), 1, 13, 5, 7, 4, 11), "standard_completion", 2),
                    (((2, 3), 1, 13, 8, 6, 4, 11), "lattice_pair", 53),
                    (((2, 3), 1, 13, 8, 6, 4, 11), "orthogonal", 3),
                    (((2, 3), 1, 13, 8, 6, 4, 11), "promoted_345", 1345),
                    (((2, 3), 1, 13, 8, 6, 4, 11), "standard_completion", 2),
                    (((1, 4), 2, 17, 4, 2, 9, 3), "lattice_pair", 23),
                    (((1, 4), 2, 17, 4, 2, 9, 3), "promoted_345", 290),
                    (((1, 4), 2, 17, 13, 15, 9, 3), "lattice_pair", 23),
                    (((1, 4), 2, 17, 13, 15, 9, 3), "promoted_345", 290),
                    (((2, 5), 10, 29, 17, 12, 28, 17), "lattice_pair", 3),
                    (((2, 5), 10, 29, 17, 12, 28, 17), "promoted_345", 21),
                    (((4, 5), 2, 41, 9, 10, 33, 19), "lattice_pair", 13),
                    (((4, 5), 2, 41, 9, 10, 33, 19), "promoted_345", 166),
                    (((4, 5), 2, 41, 32, 10, 8, 34), "lattice_pair", 14),
                    (((4, 5), 2, 41, 32, 10, 8, 34), "promoted_345", 174),
                    (((3, 8), 1, 73, 27, 38, 69, 19), "lattice_pair", 9),
                    (((3, 8), 1, 73, 27, 38, 69, 19), "promoted_345", 250),
                    (((3, 8), 1, 73, 46, 38, 4, 71), "lattice_pair", 12),
                    (((3, 8), 1, 73, 46, 38, 4, 71), "promoted_345", 303),
                    (((3, 8), 1, 73, 46, 38, 4, 71), "standard_completion", 1),
                ),
                structural_failure_family_counts=(
                    ("promoted_345", 4184),
                    ("lattice_pair", 203),
                    ("orthogonal", 6),
                    ("standard_completion", 5),
                ),
                divisor_failure_residue_closure_size_counts=(
                    (2, 1683),
                    (4, 1322),
                    (6, 817),
                    (8, 305),
                    (3, 68),
                    (12, 58),
                    (9, 22),
                    (16, 20),
                    (11, 16),
                    (10, 14),
                    (15, 13),
                    (5, 12),
                    (7, 12),
                    (13, 8),
                    (18, 5),
                    (20, 5),
                    (14, 2),
                    (22, 2),
                    (23, 2),
                    (24, 2),
                    (26, 2),
                    (29, 2),
                    (32, 2),
                    (19, 1),
                    (28, 1),
                    (33, 1),
                    (48, 1),
                ),
                divisor_failure_distinct_residue_closure_count=215,
                divisor_failure_distinct_residue_closure_size_counts=(
                    (4, 51),
                    (8, 49),
                    (6, 29),
                    (12, 21),
                    (16, 10),
                    (2, 9),
                    (15, 6),
                    (3, 5),
                    (10, 4),
                    (11, 4),
                    (7, 3),
                    (9, 3),
                    (13, 3),
                    (20, 3),
                    (5, 2),
                    (18, 2),
                    (14, 1),
                    (19, 1),
                    (22, 1),
                    (23, 1),
                    (24, 1),
                    (26, 1),
                    (28, 1),
                    (29, 1),
                    (32, 1),
                    (33, 1),
                    (48, 1),
                ),
                divisor_failure_prime_modulus_generators=(
                    (13, 2),
                    (17, 3),
                    (29, 2),
                    (41, 6),
                    (73, 5),
                ),
                divisor_failure_required_exponent_counts=(
                    (13, 7, 2806),
                    (17, 1, 626),
                    (73, 44, 316),
                    (73, 62, 259),
                    (41, 19, 188),
                    (41, 9, 179),
                    (29, 21, 24),
                ),
                divisor_failure_exponent_closure_size_counts=(
                    (2, 1683),
                    (4, 1322),
                    (6, 817),
                    (8, 305),
                    (3, 68),
                    (12, 58),
                    (9, 22),
                    (16, 20),
                    (11, 16),
                    (10, 14),
                    (15, 13),
                    (5, 12),
                    (7, 12),
                    (13, 8),
                    (18, 5),
                    (20, 5),
                    (14, 2),
                    (22, 2),
                    (23, 2),
                    (24, 2),
                    (26, 2),
                    (29, 2),
                    (32, 2),
                    (19, 1),
                    (28, 1),
                    (33, 1),
                    (48, 1),
                ),
                divisor_failure_distinct_exponent_closure_count=215,
                divisor_failure_distinct_exponent_closure_size_counts=(
                    (4, 51),
                    (8, 49),
                    (6, 29),
                    (12, 21),
                    (16, 10),
                    (2, 9),
                    (15, 6),
                    (3, 5),
                    (10, 4),
                    (11, 4),
                    (7, 3),
                    (9, 3),
                    (13, 3),
                    (20, 3),
                    (5, 2),
                    (18, 2),
                    (14, 1),
                    (19, 1),
                    (22, 1),
                    (23, 1),
                    (24, 1),
                    (26, 1),
                    (28, 1),
                    (29, 1),
                    (32, 1),
                    (33, 1),
                    (48, 1),
                ),
                divisor_failure_exponent_stabilizer_counts=(
                    (13, 12, 1, 2630),
                    (73, 72, 1, 574),
                    (17, 16, 1, 570),
                    (41, 40, 1, 363),
                    (13, 4, 3, 138),
                    (17, 8, 2, 46),
                    (13, 6, 2, 38),
                    (29, 28, 1, 24),
                    (17, 2, 8, 10),
                    (41, 20, 2, 4),
                    (73, 8, 9, 1),
                ),
                divisor_failure_exponent_kneser_defect_counts=(
                    (13, 12, 1, 0, 1284),
                    (13, 12, 1, 1, 872),
                    (17, 16, 1, 0, 370),
                    (13, 12, 1, 2, 354),
                    (73, 72, 1, 1, 193),
                    (73, 72, 1, 0, 160),
                    (13, 4, 3, 0, 138),
                    (41, 40, 1, 1, 126),
                    (17, 16, 1, 1, 96),
                    (73, 72, 1, 4, 87),
                    (13, 12, 1, 3, 84),
                    (41, 40, 1, 0, 82),
                    (17, 16, 1, 2, 72),
                    (17, 8, 2, 0, 46),
                    (41, 40, 1, 2, 46),
                    (73, 72, 1, 2, 41),
                    (41, 40, 1, 4, 39),
                    (13, 6, 2, 0, 38),
                    (13, 12, 1, 4, 36),
                    (73, 72, 1, 7, 32),
                    (41, 40, 1, 3, 20),
                    (41, 40, 1, 6, 14),
                    (41, 40, 1, 7, 14),
                    (17, 16, 1, 6, 12),
                    (73, 72, 1, 3, 11),
                    (73, 72, 1, 10, 11),
                    (17, 2, 8, 0, 10),
                    (17, 16, 1, 3, 10),
                    (17, 16, 1, 4, 10),
                    (29, 28, 1, 0, 10),
                    (73, 72, 1, 6, 9),
                    (29, 28, 1, 2, 8),
                    (73, 72, 1, 8, 8),
                    (41, 40, 1, 8, 6),
                    (41, 40, 1, 10, 6),
                    (73, 72, 1, 11, 6),
                    (41, 20, 2, 2, 4),
                    (73, 72, 1, 18, 4),
                    (29, 28, 1, 1, 3),
                    (29, 28, 1, 4, 3),
                    (41, 40, 1, 13, 3),
                    (41, 40, 1, 5, 2),
                    (41, 40, 1, 12, 2),
                    (41, 40, 1, 15, 2),
                    (73, 72, 1, 5, 2),
                    (73, 72, 1, 17, 2),
                    (73, 72, 1, 22, 2),
                    (73, 72, 1, 25, 2),
                    (41, 40, 1, 14, 1),
                    (73, 8, 9, 0, 1),
                    (73, 72, 1, 9, 1),
                    (73, 72, 1, 19, 1),
                    (73, 72, 1, 26, 1),
                    (73, 72, 1, 40, 1),
                ),
                divisor_failure_exponent_effective_length_counts=(
                    (13, 1, 1194),
                    (13, 2, 854),
                    (13, 3, 536),
                    (13, 4, 146),
                    (13, 5, 60),
                    (13, 7, 16),
                    (17, 1, 266),
                    (17, 2, 156),
                    (17, 3, 106),
                    (17, 4, 52),
                    (17, 5, 32),
                    (17, 6, 4),
                    (17, 7, 10),
                    (29, 1, 7),
                    (29, 2, 3),
                    (29, 3, 11),
                    (29, 7, 3),
                    (41, 1, 70),
                    (41, 2, 126),
                    (41, 3, 83),
                    (41, 4, 47),
                    (41, 5, 24),
                    (41, 6, 8),
                    (41, 7, 3),
                    (41, 8, 6),
                    (73, 1, 146),
                    (73, 2, 207),
                    (73, 3, 120),
                    (73, 4, 50),
                    (73, 5, 28),
                    (73, 6, 13),
                    (73, 7, 7),
                    (73, 8, 3),
                    (73, 9, 1),
                ),
                divisor_failure_exponent_saturation_gap_counts=(
                    (13, 4, 3, 6, 138),
                    (13, 6, 2, 8, 38),
                    (13, 12, 1, 4, 16),
                    (13, 12, 1, 6, 60),
                    (13, 12, 1, 7, 140),
                    (13, 12, 1, 8, 404),
                    (13, 12, 1, 9, 816),
                    (13, 12, 1, 10, 1194),
                    (17, 2, 8, 8, 10),
                    (17, 8, 2, 12, 46),
                    (17, 16, 1, 9, 4),
                    (17, 16, 1, 10, 32),
                    (17, 16, 1, 11, 52),
                    (17, 16, 1, 12, 106),
                    (17, 16, 1, 13, 110),
                    (17, 16, 1, 14, 266),
                    (29, 28, 1, 20, 3),
                    (29, 28, 1, 24, 11),
                    (29, 28, 1, 25, 3),
                    (29, 28, 1, 26, 7),
                    (41, 20, 2, 34, 4),
                    (41, 40, 1, 31, 6),
                    (41, 40, 1, 32, 3),
                    (41, 40, 1, 33, 8),
                    (41, 40, 1, 34, 24),
                    (41, 40, 1, 35, 47),
                    (41, 40, 1, 36, 79),
                    (41, 40, 1, 37, 126),
                    (41, 40, 1, 38, 70),
                    (73, 8, 9, 54, 1),
                    (73, 72, 1, 63, 3),
                    (73, 72, 1, 64, 7),
                    (73, 72, 1, 65, 13),
                    (73, 72, 1, 66, 28),
                    (73, 72, 1, 67, 50),
                    (73, 72, 1, 68, 120),
                    (73, 72, 1, 69, 207),
                    (73, 72, 1, 70, 146),
                ),
                divisor_exponent_saturation_branch_counts=(
                    ("short_failure", 4398),
                    ("short_success", 1228),
                    ("saturation_success", 192),
                ),
                divisor_exponent_saturation_branch_modulus_counts=(
                    (13, "saturation_success", 192),
                    (13, "short_failure", 2806),
                    (13, "short_success", 742),
                    (17, "short_failure", 626),
                    (17, "short_success", 318),
                    (29, "short_failure", 24),
                    (29, "short_success", 64),
                    (41, "short_failure", 367),
                    (41, "short_success", 25),
                    (73, "short_failure", 575),
                    (73, "short_success", 79),
                ),
                promoted_345_failure_direction_counts=(
                    ((-4, -3), 1617),
                    ((-4, 3), 993),
                    ((-3, -4), 630),
                    ((-3, 4), 354),
                    ((3, -4), 310),
                    ((3, 4), 145),
                    ((4, -3), 104),
                    ((4, 3), 31),
                ),
                promoted_345_failure_factor_counts=(
                    (1, 1517),
                    (2, 714),
                    (4, 424),
                    (3, 343),
                    (5, 318),
                    (8, 307),
                    (9, 204),
                    (25, 181),
                    (6, 176),
                ),
                promoted_345_failure_integrality_linear_row_modulus_counts=(
                    (1, 3714),
                    (2, 449),
                    (5, 16),
                    (10, 5),
                ),
                promoted_345_failure_distinct_integrality_linear_row_count=2668,
                promoted_345_failure_distinct_integrality_linear_row_modulus_counts=(
                    (1, 2305),
                    (2, 342),
                    (5, 16),
                    (10, 5),
                ),
                lattice_pair_failure_determinant_counts=(
                    (7, 51),
                    (13, 36),
                    (55, 18),
                    (47, 16),
                    (31, 12),
                    (17, 9),
                    (73, 7),
                    (23, 6),
                    (155, 6),
                    (185, 6),
                    (475, 4),
                    (817, 4),
                    (841, 4),
                    (16, 2),
                    (107, 2),
                    (109, 2),
                    (115, 2),
                    (157, 2),
                    (311, 2),
                    (443, 2),
                    (515, 2),
                    (989, 2),
                    (1369, 2),
                    (1435, 2),
                    (36, 1),
                    (68, 1),
                ),
                lattice_pair_failure_distinct_pair_count=63,
                lattice_pair_failure_distinct_pair_determinant_counts=(
                    (47, 6),
                    (13, 4),
                    (31, 4),
                    (55, 4),
                    (73, 4),
                    (155, 4),
                    (7, 2),
                    (17, 2),
                    (23, 2),
                    (107, 2),
                    (109, 2),
                    (115, 2),
                    (157, 2),
                    (185, 2),
                    (311, 2),
                    (443, 2),
                    (475, 2),
                    (515, 2),
                    (817, 2),
                    (841, 2),
                    (989, 2),
                    (1369, 2),
                    (1435, 2),
                    (16, 1),
                    (36, 1),
                    (68, 1),
                ),
                lattice_pair_failure_linear_gcd_counts=((1, 202), (2, 1)),
                lattice_pair_failure_distinct_linear_congruence_count=178,
                lattice_pair_failure_distinct_linear_gcd_counts=((1, 177), (2, 1)),
                orthogonal_failure_linear_gcd_counts=((1, 6),),
                orthogonal_failure_distinct_linear_congruence_count=6,
                orthogonal_failure_distinct_linear_gcd_counts=((1, 6),),
                standard_completion_failure_direction_branch_counts=(
                    ((-8, -15), 1, 2),
                    ((-15, -8), 1, 1),
                    ((-12, 5), 1, 1),
                    ((-5, 12), 0, 1),
                ),
                standard_completion_failure_distinct_quadratic_row_count=5,
                standard_completion_failure_distinct_quadratic_row_modulus_counts=(
                    (1156, 3),
                    (676, 2),
                ),
                standard_completion_failure_linear_row_modulus_counts=((1, 3), (13, 2)),
                standard_completion_failure_distinct_linear_row_count=5,
                standard_completion_failure_distinct_linear_row_modulus_counts=(
                    (1, 3),
                    (13, 2),
                ),
                nonstructural_failure_examples=(),
            ),
        )

    def test_squareclass_split_extended_frontier_examples(self):
        examples = {
            (199, 1462): ((-24, -7), 115, 1, -293, (-188976, -55118)),
            (941, 1282): ((-40, 9), 149, 401, -1, (285680, -64278)),
            (1262, 1781): ((-24, 7), 34, 41, -37, (888, -259)),
            (1282, 941): ((-9, 40), 149, 1, -401, (-64278, 285680)),
            (1462, 199): ((-7, -24), 115, 1, 293, (-55118, -188976)),
            (1781, 1262): ((-7, 24), 34, 37, -41, (-259, 888)),
        }
        for target, expected in examples.items():
            self.assertIsNone(pythagorean_layered_split_certificate(target), target)
            witness = parallel_direction_squareclass_split_cover_witness(
                target,
                8,
                149,
                401,
            )
            self.assertIsNotNone(witness, target)
            direction, squareclass, split_factor, paired, midpoint = expected
            self.assertEqual(witness.direction, direction)
            self.assertEqual(witness.squareclass, squareclass)
            self.assertEqual(witness.split_factor, split_factor)
            self.assertEqual(witness.signed_paired_split_factor, paired)
            self.assertEqual(witness.midpoint, midpoint)
            self.assertTrue(witness.certificate.valid())
            split_quotient = parallel_direction_squareclass_line_split_quotient(
                direction,
                split_factor,
                paired,
            )
            self.assertIn(
                (squareclass, split_factor, paired, split_quotient),
                parallel_direction_conjugate_ideal_split_roots(target, direction),
            )
            self.assertEqual(
                parallel_direction_conjugate_ideal_certificate(target, direction),
                witness.certificate,
            )
            exact_layered = pythagorean_layered_conjugate_ideal_certificate(target)
            self.assertIsNotNone(exact_layered, target)
            self.assertTrue(exact_layered.valid())

        exact_direction_examples = {
            (1, 1298): ((-40, -9), 1, 2257, -23, (-223, -273), -1522),
            (55, 1906): ((-5, 12), 10, 1019, -1, (-157, -235), -30587),
            (182, 1489): ((-12, 5), 82, 229, -1, (-35, 53), -12691),
            (230, 1367): ((-5, 12), 5, 1, -1919, (-443, 295), 54566),
        }
        for target, expected in exact_direction_examples.items():
            witness = parallel_direction_conjugate_ideal_cover_witness(target, 8)
            root_witness = parallel_direction_conjugate_ideal_root_cover_witness(target, 8)
            shape_witness = parallel_direction_conjugate_ideal_root_shape_cover_witness(
                target,
                ((2, 3), (4, 5)),
            )
            spine_witness = parallel_direction_conjugate_ideal_root_spine_cover_witness(
                target,
                8,
            )
            self.assertIsNotNone(witness, target)
            self.assertEqual(root_witness, witness)
            self.assertIsNotNone(shape_witness, target)
            self.assertTrue(shape_witness.valid())
            self.assertIsNotNone(spine_witness, target)
            self.assertTrue(spine_witness.valid())
            direction, squareclass, split_factor, paired, beta, coefficient = expected
            self.assertEqual(witness.direction, direction)
            self.assertEqual(witness.squareclass, squareclass)
            self.assertEqual(witness.split_factor, split_factor)
            self.assertEqual(witness.signed_paired_split_factor, paired)
            self.assertEqual(witness.beta, beta)
            self.assertEqual(witness.first_coefficient, coefficient)
            self.assertEqual(
                witness.gaussian_quadratic_left,
                witness.gaussian_quadratic_right,
            )
            self.assertTrue(witness.valid())
            self.assertTrue(witness.certificate.valid())

        primary_target = (139, 878)
        primary_witness = parallel_direction_conjugate_ideal_root_primary_spine_cover_witness(
            primary_target,
            8,
        )
        self.assertIsNotNone(primary_witness)
        self.assertEqual(primary_witness.root_shape, (1, 4))
        self.assertIsNone(
            parallel_direction_conjugate_ideal_root_secondary_spine_cover_certificate(
                primary_target,
                8,
            )
        )

        secondary_target = (151, 338)
        secondary_witness = (
            parallel_direction_conjugate_ideal_root_secondary_spine_cover_witness(
                secondary_target,
                8,
            )
        )
        self.assertIsNotNone(secondary_witness)
        self.assertEqual(secondary_witness.root_shape, (4, 5))
        self.assertIsNone(
            parallel_direction_conjugate_ideal_root_primary_spine_cover_certificate(
                secondary_target,
                8,
            )
        )

    def test_prime_determinant_lattice_line_criterion(self):
        self.assertTrue(is_prime(17))
        self.assertFalse(is_prime(21))
        self.assertEqual(determinant((3, 4), (20, 21)), -17)
        self.assertTrue(same_projective_class_mod((6, 8), (3, 4), 17))
        self.assertTrue(same_projective_class_mod((17, 0), (3, 4), 17))
        self.assertFalse(same_projective_class_mod((1, 0), (3, 4), 17))

        pairs = (
            ((3, 4), (4, 3)),
            ((3, 4), (8, 15)),
            ((3, 4), (20, 21)),
            ((-28, 45), (-3, 4)),
            ((-12, -35), (-5, -12)),
        )
        for first_direction, second_direction in pairs:
            modulus = abs(determinant(first_direction, second_direction))
            self.assertTrue(is_prime(modulus))
            for g in range(-50, 51):
                for h in range(-50, 51):
                    target = (g, h)
                    if target == (0, 0):
                        continue
                    if not same_projective_class_mod(target, first_direction, modulus):
                        self.assertIsNone(
                            prime_determinant_lattice_certificate(
                                target,
                                first_direction,
                                second_direction,
                            )
                        )
                        continue

                    cert = prime_determinant_lattice_certificate(
                        target,
                        first_direction,
                        second_direction,
                    )
                    if cert is None:
                        self.assertTrue(edge((0, 0), target))
                    else:
                        self.assertEqual(cert.target, target)
                        self.assertTrue(cert.valid())

        with self.assertRaises(ValueError):
            prime_determinant_lattice_certificate((1, 1), (3, 4), (5, 12))

    def test_determinant_seven_congruence_families(self):
        for g in range(-80, 81):
            for h in range(-80, 81):
                target = (g, h)
                if target == (0, 0):
                    continue
                if (g + h) % 7 != 0 and (g - h) % 7 != 0:
                    continue

                cert = determinant_seven_lattice_certificate(target)
                if cert is None:
                    self.assertTrue(edge((0, 0), target))
                else:
                    self.assertEqual(cert.target, target)
                    self.assertTrue(cert.valid())

    def test_consecutive_leg_swap_lattice_family(self):
        expected_triples = [
            PythagoreanTriple(3, 4, 5),
            PythagoreanTriple(20, 21, 29),
            PythagoreanTriple(119, 120, 169),
            PythagoreanTriple(696, 697, 985),
            PythagoreanTriple(4059, 4060, 5741),
        ]
        for index, expected in enumerate(expected_triples):
            triple = consecutive_leg_pythagorean_triple(index)
            self.assertEqual(triple, expected)
            self.assertTrue(triple.valid())
            self.assertEqual(triple.leg_b, triple.leg_a + 1)
            self.assertEqual(
                (triple.leg_a + triple.leg_b) ** 2
                - 2 * triple.hypotenuse * triple.hypotenuse,
                -1,
            )

        for index in range(4):
            triple = consecutive_leg_pythagorean_triple(index)
            modulus = triple.leg_a + triple.leg_b
            for g in range(-140, 141):
                for h in range(-140, 141):
                    target = (g, h)
                    if target == (0, 0):
                        continue

                    covered = (g + h) % modulus == 0 or (g - h) % modulus == 0
                    cert = consecutive_leg_swap_lattice_certificate(target, index)
                    if not covered:
                        self.assertIsNone(cert)
                    elif cert is None:
                        self.assertTrue(edge((0, 0), target))
                    else:
                        self.assertEqual(cert.target, target)
                        self.assertTrue(cert.valid())

        cert = consecutive_leg_swap_lattice_certificate((240, -1), 2)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.target, (240, -1))
        self.assertTrue(cert.valid())

        with self.assertRaises(ValueError):
            consecutive_leg_pythagorean_triple(-1)
        with self.assertRaises(ValueError):
            consecutive_leg_swap_lattice_certificate((1, 1), -1)

    def test_determinant_thirteen_congruence_families(self):
        for g in range(-80, 81):
            for h in range(-80, 81):
                target = (g, h)
                if target == (0, 0):
                    continue
                if all((g + sign * multiplier * h) % 13 != 0
                       for sign in (-1, 1)
                       for multiplier in (3, 4)):
                    continue

                cert = determinant_thirteen_lattice_certificate(target)
                if cert is None:
                    self.assertTrue(edge((0, 0), target))
                else:
                    self.assertEqual(cert.target, target)
                    self.assertTrue(cert.valid())

    def test_determinant_seventeen_congruence_families(self):
        for g in range(-80, 81):
            for h in range(-80, 81):
                target = (g, h)
                if target == (0, 0):
                    continue
                if all((g + sign * multiplier * h) % 17 != 0
                       for sign in (-1, 1)
                       for multiplier in (5, 7)):
                    continue

                cert = determinant_seventeen_lattice_certificate(target)
                if cert is None:
                    self.assertTrue(edge((0, 0), target))
                else:
                    self.assertEqual(cert.target, target)
                    self.assertTrue(cert.valid())

    def test_additional_small_prime_congruence_families(self):
        self.assertEqual(len(SMALL_PRIME_DETERMINANT_DIRECTION_PAIRS), 128)

        slopes_by_modulus = {}
        for first_direction, second_direction in SMALL_PRIME_DETERMINANT_DIRECTION_PAIRS:
            modulus = abs(determinant(first_direction, second_direction))
            self.assertTrue(is_prime(modulus))
            self.assertIn(
                modulus,
                {
                    23, 31, 37, 41, 43, 47, 53, 67, 73, 83, 89, 107, 109,
                    149, 157, 173, 179, 191, 193, 211, 239, 241, 251, 269,
                },
            )

            first_x, first_y = first_direction
            slope = (first_x * pow(first_y, -1, modulus)) % modulus
            slopes_by_modulus.setdefault(modulus, set()).add(slope)

        self.assertEqual(
            slopes_by_modulus,
            {
                23: {5, 9, 14, 18},
                31: {3, 10, 21, 28},
                37: {10, 11, 26, 27},
                41: {1, 40},
                43: {10, 13, 15, 20, 23, 28, 30, 33},
                47: {4, 7, 11, 12, 17, 20, 27, 30, 35, 36, 40, 43},
                53: {14, 19, 34, 39},
                67: {16, 21, 46, 51},
                73: {13, 17, 28, 30, 43, 45, 56, 60},
                83: {8, 19, 31, 35, 48, 52, 64, 75},
                89: {13, 41, 48, 76},
                107: {22, 34, 73, 85},
                109: {45, 46, 63, 64},
                149: {54, 69, 80, 95},
                157: {14, 19, 33, 56, 66, 69, 88, 91, 101, 124, 138, 143},
                173: {18, 34, 48, 56, 117, 125, 139, 155},
                179: {12, 15, 164, 167},
                191: {13, 44, 87, 90, 101, 104, 147, 178},
                193: {86, 92, 101, 107},
                211: {51, 91, 120, 160},
                239: {1, 238},
                241: {101, 105, 136, 140},
                251: {31, 81, 170, 220},
                269: {32, 42, 227, 237},
            },
        )

        for g in range(-80, 81):
            for h in range(-80, 81):
                target = (g, h)
                if target == (0, 0):
                    continue

                covered = any(
                    same_projective_class_mod(
                        target,
                        first_direction,
                        abs(determinant(first_direction, second_direction)),
                    )
                    for first_direction, second_direction
                    in SMALL_PRIME_DETERMINANT_DIRECTION_PAIRS
                )
                if not covered:
                    continue

                cert = small_prime_lattice_certificate(target)
                if cert is None:
                    self.assertTrue(edge((0, 0), target))
                else:
                    self.assertEqual(cert.target, target)
                    self.assertTrue(cert.valid())

    def test_box_twenty_finite_audit(self):
        self.assertEqual(
            set(BOX_TWENTY_RESIDUAL_CERTIFICATES),
            {
                (10, 5),
                (13, 7),
                (13, 10),
                (16, 3),
                (16, 15),
                (17, 5),
                (17, 13),
                (20, 3),
                (20, 9),
            },
        )

        for base_target, midpoint in BOX_TWENTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_twenty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-20, 21):
            for h in range(-20, 21):
                target = (g, h)
                certificate = box_twenty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_twenty_audit_certificate((21, 1)))

    def test_box_thirty_finite_audit(self):
        additional_targets = {
            (22, 11),
            (23, 3),
            (23, 11),
            (25, 1),
            (25, 14),
            (26, 7),
            (26, 14),
            (26, 20),
            (26, 21),
            (26, 25),
            (28, 3),
            (28, 17),
            (28, 27),
            (29, 2),
            (30, 13),
        }
        self.assertEqual(
            set(BOX_THIRTY_RESIDUAL_CERTIFICATES),
            set(BOX_TWENTY_RESIDUAL_CERTIFICATES) | additional_targets,
        )

        for base_target, midpoint in BOX_THIRTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_thirty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-30, 31):
            for h in range(-30, 31):
                target = (g, h)
                certificate = box_thirty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_thirty_audit_certificate((31, 1)))

    def test_box_forty_finite_audit(self):
        additional_targets = {
            (32, 6),
            (32, 30),
            (33, 17),
            (34, 10),
            (34, 26),
            (35, 2),
            (35, 4),
            (35, 8),
            (35, 26),
            (35, 33),
            (37, 3),
            (37, 10),
            (37, 25),
            (37, 27),
            (38, 1),
            (38, 15),
            (38, 19),
            (39, 21),
            (39, 23),
            (39, 30),
            (40, 6),
            (40, 18),
        }
        self.assertEqual(
            set(BOX_FORTY_RESIDUAL_CERTIFICATES),
            set(BOX_THIRTY_RESIDUAL_CERTIFICATES) | additional_targets,
        )

        for base_target, midpoint in BOX_FORTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_forty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-40, 41):
            for h in range(-40, 41):
                target = (g, h)
                certificate = box_forty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_forty_audit_certificate((41, 1)))

    def test_box_fifty_finite_audit(self):
        additional_targets = {
            (41, 9),
            (41, 12),
            (41, 14),
            (43, 7),
            (43, 9),
            (43, 30),
            (44, 17),
            (44, 27),
            (44, 29),
            (44, 31),
            (45, 29),
            (46, 6),
            (46, 22),
            (46, 29),
            (47, 8),
            (47, 10),
            (47, 13),
            (47, 21),
            (47, 22),
            (47, 25),
            (47, 29),
            (47, 42),
            (47, 43),
            (48, 9),
            (48, 37),
            (48, 45),
            (49, 2),
            (49, 5),
            (49, 29),
            (49, 36),
            (49, 45),
            (50, 2),
            (50, 17),
            (50, 23),
            (50, 25),
            (50, 28),
        }
        self.assertEqual(
            set(BOX_FIFTY_RESIDUAL_CERTIFICATES),
            set(BOX_FORTY_RESIDUAL_CERTIFICATES) | additional_targets,
        )

        for base_target, midpoint in BOX_FIFTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_fifty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-50, 51):
            for h in range(-50, 51):
                target = (g, h)
                certificate = box_fifty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_fifty_audit_certificate((51, 1)))

    def test_box_sixty_finite_audit(self):
        additional_targets = {
            (51, 11),
            (51, 13),
            (51, 15),
            (51, 20),
            (51, 38),
            (51, 39),
            (52, 14),
            (52, 21),
            (52, 28),
            (52, 40),
            (52, 42),
            (52, 43),
            (52, 50),
            (53, 2),
            (53, 33),
            (53, 47),
            (53, 50),
            (55, 26),
            (55, 46),
            (56, 6),
            (56, 17),
            (56, 34),
            (56, 37),
            (56, 47),
            (56, 54),
            (57, 17),
            (57, 44),
            (57, 49),
            (57, 56),
            (58, 4),
            (58, 13),
            (59, 13),
            (59, 33),
            (59, 43),
            (59, 49),
            (59, 51),
            (59, 58),
            (60, 9),
            (60, 13),
            (60, 26),
            (60, 27),
        }
        self.assertEqual(
            set(BOX_SIXTY_RESIDUAL_CERTIFICATES),
            set(BOX_FIFTY_RESIDUAL_CERTIFICATES) | additional_targets,
        )

        for base_target, midpoint in BOX_SIXTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_sixty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-60, 61):
            for h in range(-60, 61):
                target = (g, h)
                certificate = box_sixty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_sixty_audit_certificate((61, 1)))

    def test_box_seventy_finite_audit(self):
        additional_targets = {
            (61, 7),
            (61, 11),
            (61, 22),
            (61, 39),
            (61, 46),
            (61, 48),
            (61, 57),
            (62, 19),
            (62, 33),
            (62, 37),
            (62, 45),
            (62, 49),
            (63, 11),
            (63, 23),
            (64, 12),
            (64, 19),
            (64, 39),
            (64, 60),
            (65, 8),
            (65, 11),
            (65, 27),
            (65, 35),
            (65, 46),
            (65, 50),
            (66, 34),
            (66, 47),
            (67, 9),
            (67, 35),
            (67, 49),
            (67, 65),
            (68, 7),
            (68, 11),
            (68, 15),
            (68, 20),
            (68, 21),
            (68, 39),
            (68, 52),
            (69, 9),
            (69, 11),
            (69, 32),
            (69, 33),
            (69, 35),
            (69, 59),
            (70, 1),
            (70, 4),
            (70, 8),
            (70, 16),
            (70, 23),
            (70, 47),
            (70, 52),
            (70, 66),
        }
        self.assertEqual(
            set(BOX_SEVENTY_RESIDUAL_CERTIFICATES),
            set(BOX_SIXTY_RESIDUAL_CERTIFICATES) | additional_targets,
        )

        for base_target, midpoint in BOX_SEVENTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_seventy_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-70, 71):
            for h in range(-70, 71):
                target = (g, h)
                certificate = box_seventy_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_seventy_audit_certificate((71, 1)))

    def test_box_eighty_finite_audit(self):
        self.assertEqual(
            set(BOX_EIGHTY_RESIDUAL_CERTIFICATES),
            {
                (71, 14),
                (71, 25),
                (71, 46),
                (71, 61),
                (72, 25),
                (72, 35),
                (73, 5),
                (73, 12),
                (73, 34),
                (73, 55),
                (74, 6),
                (74, 19),
                (74, 20),
                (74, 41),
                (74, 50),
                (74, 65),
                (74, 69),
                (75, 3),
                (75, 28),
                (75, 42),
                (75, 46),
                (76, 2),
                (76, 3),
                (76, 30),
                (76, 53),
                (76, 61),
                (77, 15),
                (77, 19),
                (77, 24),
                (77, 27),
                (77, 53),
                (77, 59),
                (77, 64),
                (78, 46),
                (78, 60),
                (78, 63),
                (78, 73),
                (79, 6),
                (79, 31),
                (79, 45),
                (79, 52),
                (79, 63),
                (80, 12),
                (80, 15),
                (80, 41),
                (80, 63),
                (80, 75),
                (80, 79),
            },
        )

        for base_target, midpoint in BOX_EIGHTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_eighty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-80, 81):
            for h in range(-80, 81):
                target = (g, h)
                certificate = box_eighty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_eighty_audit_certificate((81, 1)))

    def test_box_ninety_finite_audit(self):
        self.assertEqual(
            set(BOX_NINETY_RESIDUAL_CERTIFICATES),
            {
                (81, 19),
                (81, 47),
                (82, 11),
                (82, 24),
                (82, 59),
                (83, 18),
                (83, 51),
                (84, 9),
                (84, 25),
                (84, 51),
                (84, 55),
                (84, 79),
                (84, 81),
                (85, 9),
                (85, 19),
                (85, 26),
                (85, 32),
                (85, 46),
                (85, 65),
                (85, 74),
                (86, 13),
                (86, 14),
                (86, 18),
                (86, 60),
                (86, 69),
                (86, 81),
                (87, 34),
                (87, 35),
                (87, 50),
                (87, 86),
                (88, 7),
                (88, 34),
                (88, 54),
                (88, 58),
                (88, 62),
                (88, 65),
                (89, 24),
                (89, 25),
                (89, 29),
                (89, 49),
                (89, 64),
                (89, 78),
                (89, 87),
                (90, 7),
                (90, 47),
                (90, 58),
            },
        )

        for base_target, midpoint in BOX_NINETY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_ninety_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-90, 91):
            for h in range(-90, 91):
                target = (g, h)
                certificate = box_ninety_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_ninety_audit_certificate((91, 1)))

    def test_box_one_hundred_finite_audit(self):
        self.assertEqual(
            set(BOX_ONE_HUNDRED_RESIDUAL_CERTIFICATES),
            {
                (91, 10),
                (91, 16),
                (91, 17),
                (91, 24),
                (91, 27),
                (91, 48),
                (91, 53),
                (91, 71),
                (92, 12),
                (92, 44),
                (92, 58),
                (92, 63),
                (92, 73),
                (93, 92),
                (94, 7),
                (94, 20),
                (94, 26),
                (94, 42),
                (94, 50),
                (94, 58),
                (94, 71),
                (94, 75),
                (94, 85),
                (94, 86),
                (95, 26),
                (95, 34),
                (95, 44),
                (95, 63),
                (95, 71),
                (95, 72),
                (95, 91),
                (95, 93),
                (96, 18),
                (96, 74),
                (96, 83),
                (96, 90),
                (97, 32),
                (97, 87),
                (97, 95),
                (98, 4),
                (98, 10),
                (98, 29),
                (98, 58),
                (98, 87),
                (98, 90),
                (99, 5),
                (99, 10),
                (99, 25),
                (99, 31),
                (99, 51),
                (99, 68),
                (99, 73),
                (100, 4),
                (100, 15),
                (100, 34),
                (100, 56),
                (100, 57),
                (100, 67),
            },
        )

        for base_target, midpoint in BOX_ONE_HUNDRED_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_one_hundred_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-100, 101):
            for h in range(-100, 101):
                target = (g, h)
                certificate = box_one_hundred_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_one_hundred_audit_certificate((101, 1)))

    def test_box_one_ten_finite_audit(self):
        self.assertEqual(
            set(BOX_ONE_TEN_RESIDUAL_CERTIFICATES),
            {
                (101, 6),
                (101, 15),
                (101, 16),
                (101, 71),
                (101, 98),
                (101, 99),
                (102, 13),
                (102, 22),
                (102, 26),
                (102, 37),
                (102, 40),
                (102, 77),
                (102, 78),
                (103, 15),
                (103, 18),
                (103, 28),
                (103, 34),
                (103, 50),
                (103, 67),
                (103, 71),
                (103, 91),
                (104, 42),
                (104, 47),
                (104, 49),
                (104, 80),
                (104, 84),
                (104, 86),
                (104, 93),
                (105, 12),
                (105, 24),
                (105, 31),
                (105, 37),
                (105, 76),
                (105, 78),
                (105, 99),
                (106, 4),
                (106, 51),
                (106, 66),
                (106, 67),
                (106, 75),
                (106, 77),
                (106, 94),
                (106, 100),
                (107, 13),
                (107, 21),
                (107, 24),
                (107, 55),
                (107, 83),
                (107, 88),
                (107, 102),
                (107, 106),
                (108, 19),
                (108, 61),
                (108, 65),
                (108, 83),
                (109, 12),
                (109, 40),
                (109, 47),
                (109, 51),
                (109, 90),
                (109, 92),
                (110, 52),
                (110, 53),
                (110, 81),
                (110, 92),
            },
        )

        for base_target, midpoint in BOX_ONE_TEN_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_one_ten_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-110, 111):
            for h in range(-110, 111):
                target = (g, h)
                certificate = box_one_ten_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_one_ten_audit_certificate((111, 1)))

    def test_box_one_twenty_finite_audit(self):
        self.assertEqual(
            set(BOX_ONE_TWENTY_RESIDUAL_CERTIFICATES),
            {
                (111, 9),
                (111, 30),
                (111, 61),
                (111, 65),
                (111, 75),
                (111, 103),
                (112, 9),
                (112, 12),
                (112, 34),
                (112, 51),
                (112, 55),
                (112, 68),
                (112, 81),
                (112, 94),
                (112, 95),
                (112, 99),
                (112, 108),
                (113, 35),
                (113, 37),
                (113, 46),
                (113, 58),
                (113, 63),
                (113, 70),
                (113, 108),
                (114, 13),
                (114, 29),
                (114, 34),
                (114, 45),
                (114, 88),
                (114, 98),
                (115, 9),
                (115, 15),
                (115, 26),
                (115, 29),
                (115, 55),
                (115, 61),
                (115, 63),
                (115, 68),
                (115, 78),
                (115, 93),
                (115, 106),
                (116, 26),
                (116, 33),
                (116, 71),
                (116, 79),
                (116, 99),
                (116, 105),
                (117, 11),
                (117, 17),
                (117, 38),
                (117, 43),
                (117, 46),
                (117, 69),
                (117, 73),
                (117, 90),
                (118, 11),
                (118, 25),
                (118, 26),
                (118, 47),
                (118, 51),
                (118, 59),
                (118, 86),
                (118, 98),
                (118, 102),
                (118, 116),
                (118, 117),
                (119, 9),
                (119, 11),
                (119, 25),
                (119, 27),
                (119, 38),
                (119, 48),
                (119, 62),
                (119, 69),
                (119, 75),
                (119, 93),
                (119, 104),
                (119, 116),
                (120, 11),
                (120, 18),
            },
        )

        for base_target, midpoint in BOX_ONE_TWENTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_one_twenty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-120, 121):
            for h in range(-120, 121):
                target = (g, h)
                certificate = box_one_twenty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_one_twenty_audit_certificate((121, 1)))

    def test_box_one_thirty_finite_audit(self):
        self.assertEqual(
            set(BOX_ONE_THIRTY_RESIDUAL_CERTIFICATES),
            {
                (121, 4),
                (121, 17),
                (121, 35),
                (121, 50),
                (121, 57),
                (121, 69),
                (121, 87),
                (121, 91),
                (121, 97),
                (121, 119),
                (122, 22),
                (122, 23),
                (122, 44),
                (122, 78),
                (122, 79),
                (122, 96),
                (122, 114),
                (123, 36),
                (123, 56),
                (123, 68),
                (123, 100),
                (123, 107),
                (124, 27),
                (124, 38),
                (124, 39),
                (124, 71),
                (124, 74),
                (124, 85),
                (124, 90),
                (124, 98),
                (124, 113),
                (125, 5),
                (125, 14),
                (125, 16),
                (125, 53),
                (125, 61),
                (125, 70),
                (125, 74),
                (125, 91),
                (125, 101),
                (125, 108),
                (126, 22),
                (126, 31),
                (126, 43),
                (126, 46),
                (127, 10),
                (127, 18),
                (127, 33),
                (127, 70),
                (127, 72),
                (127, 75),
                (127, 88),
                (127, 93),
                (127, 117),
                (128, 24),
                (128, 78),
                (128, 95),
                (128, 120),
                (129, 7),
                (129, 8),
                (129, 20),
                (129, 21),
                (129, 26),
                (129, 27),
                (129, 90),
                (129, 92),
                (129, 128),
                (130, 16),
                (130, 22),
                (130, 54),
                (130, 57),
                (130, 92),
                (130, 100),
                (130, 105),
                (130, 107),
                (130, 113),
            },
        )

        for base_target, midpoint in BOX_ONE_THIRTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_one_thirty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-130, 131):
            for h in range(-130, 131):
                target = (g, h)
                certificate = box_one_thirty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_one_thirty_audit_certificate((131, 1)))

    def test_box_one_forty_finite_audit(self):
        self.assertEqual(
            set(BOX_ONE_FORTY_RESIDUAL_CERTIFICATES),
            {
                (131, 14),
                (131, 27),
                (131, 28),
                (131, 38),
                (131, 53),
                (131, 92),
                (131, 102),
                (131, 119),
                (132, 51),
                (132, 67),
                (132, 68),
                (132, 81),
                (132, 87),
                (132, 93),
                (132, 94),
                (132, 95),
                (132, 115),
                (133, 8),
                (133, 11),
                (133, 18),
                (133, 29),
                (133, 33),
                (133, 73),
                (133, 78),
                (133, 101),
                (133, 102),
                (133, 124),
                (133, 125),
                (133, 130),
                (134, 9),
                (134, 18),
                (134, 39),
                (134, 47),
                (134, 70),
                (134, 73),
                (134, 91),
                (134, 98),
                (134, 121),
                (134, 130),
                (135, 13),
                (135, 43),
                (135, 49),
                (135, 62),
                (135, 87),
                (135, 101),
                (136, 7),
                (136, 14),
                (136, 22),
                (136, 30),
                (136, 78),
                (136, 104),
                (136, 117),
                (136, 131),
                (137, 35),
                (137, 42),
                (137, 65),
                (137, 72),
                (137, 82),
                (137, 103),
                (138, 18),
                (138, 22),
                (138, 53),
                (138, 66),
                (138, 87),
                (138, 118),
                (139, 31),
                (139, 35),
                (139, 52),
                (139, 59),
                (139, 73),
                (139, 84),
                (139, 109),
                (139, 112),
                (140, 2),
                (140, 15),
                (140, 16),
                (140, 32),
                (140, 46),
                (140, 47),
                (140, 85),
                (140, 94),
                (140, 104),
                (140, 109),
                (140, 123),
                (140, 127),
                (140, 132),
                (140, 135),
            },
        )

        for base_target, midpoint in BOX_ONE_FORTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_one_forty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-140, 141):
            for h in range(-140, 141):
                target = (g, h)
                certificate = box_one_forty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_one_forty_audit_certificate((141, 1)))

    def test_box_one_fifty_finite_audit(self):
        self.assertEqual(
            set(BOX_ONE_FIFTY_RESIDUAL_CERTIFICATES),
            {
                (141, 2),
                (141, 14),
                (141, 30),
                (141, 37),
                (141, 39),
                (141, 56),
                (141, 63),
                (141, 74),
                (141, 75),
                (141, 87),
                (141, 91),
                (141, 129),
                (141, 131),
                (141, 133),
                (142, 15),
                (142, 28),
                (142, 31),
                (142, 50),
                (142, 71),
                (142, 91),
                (142, 92),
                (142, 122),
                (143, 6),
                (143, 28),
                (143, 29),
                (143, 30),
                (143, 42),
                (143, 63),
                (143, 82),
                (143, 106),
                (143, 110),
                (143, 111),
                (143, 126),
                (143, 131),
                (144, 19),
                (144, 27),
                (144, 37),
                (144, 50),
                (144, 70),
                (144, 89),
                (144, 111),
                (144, 135),
                (145, 49),
                (145, 53),
                (145, 64),
                (145, 76),
                (145, 102),
                (145, 106),
                (145, 119),
                (145, 134),
                (145, 139),
                (146, 5),
                (146, 10),
                (146, 21),
                (146, 24),
                (146, 31),
                (146, 68),
                (146, 110),
                (147, 2),
                (147, 6),
                (147, 15),
                (147, 20),
                (147, 46),
                (147, 50),
                (147, 61),
                (147, 87),
                (147, 109),
                (147, 134),
                (147, 135),
                (148, 12),
                (148, 38),
                (148, 40),
                (148, 51),
                (148, 53),
                (148, 81),
                (148, 82),
                (148, 100),
                (148, 121),
                (148, 130),
                (148, 138),
                (149, 35),
                (149, 36),
                (149, 43),
                (149, 46),
                (149, 77),
                (149, 94),
                (149, 98),
                (149, 104),
                (149, 118),
                (149, 120),
                (149, 123),
                (150, 6),
                (150, 23),
                (150, 51),
                (150, 56),
                (150, 84),
                (150, 92),
                (150, 103),
            },
        )

        for base_target, midpoint in BOX_ONE_FIFTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_one_fifty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-150, 151):
            for h in range(-150, 151):
                target = (g, h)
                certificate = box_one_fifty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_one_fifty_audit_certificate((151, 1)))

    def test_box_one_sixty_finite_audit(self):
        self.assertEqual(
            set(BOX_ONE_SIXTY_RESIDUAL_CERTIFICATES),
            {
                (151, 34),
                (151, 49),
                (151, 64),
                (151, 83),
                (151, 86),
                (151, 103),
                (151, 121),
                (151, 127),
                (151, 131),
                (151, 147),
                (152, 4),
                (152, 6),
                (152, 21),
                (152, 59),
                (152, 60),
                (152, 69),
                (152, 83),
                (152, 106),
                (152, 113),
                (152, 122),
                (153, 28),
                (153, 33),
                (153, 39),
                (153, 60),
                (153, 65),
                (153, 80),
                (153, 88),
                (153, 115),
                (153, 117),
                (153, 143),
                (154, 9),
                (154, 30),
                (154, 37),
                (154, 38),
                (154, 48),
                (154, 53),
                (154, 54),
                (154, 87),
                (154, 93),
                (154, 101),
                (154, 106),
                (154, 118),
                (154, 128),
                (155, 11),
                (155, 12),
                (155, 18),
                (155, 21),
                (155, 52),
                (155, 59),
                (155, 63),
                (155, 72),
                (155, 79),
                (155, 149),
                (156, 35),
                (156, 63),
                (156, 92),
                (156, 109),
                (156, 120),
                (156, 126),
                (156, 129),
                (156, 146),
                (157, 2),
                (157, 19),
                (157, 27),
                (157, 47),
                (157, 50),
                (157, 92),
                (157, 110),
                (157, 117),
                (157, 154),
                (158, 2),
                (158, 12),
                (158, 13),
                (158, 23),
                (158, 37),
                (158, 41),
                (158, 51),
                (158, 62),
                (158, 79),
                (158, 90),
                (158, 104),
                (158, 113),
                (158, 121),
                (158, 126),
                (158, 155),
                (159, 6),
                (159, 7),
                (159, 49),
                (159, 52),
                (159, 99),
                (159, 137),
                (159, 141),
                (159, 150),
                (159, 154),
                (160, 24),
                (160, 30),
                (160, 82),
                (160, 89),
                (160, 93),
                (160, 126),
                (160, 150),
                (160, 158),
            },
        )

        for base_target, midpoint in BOX_ONE_SIXTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_one_sixty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-160, 161):
            for h in range(-160, 161):
                target = (g, h)
                certificate = box_one_sixty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_one_sixty_audit_certificate((161, 1)))

    def test_box_one_seventy_finite_audit(self):
        self.assertEqual(
            set(BOX_ONE_SEVENTY_RESIDUAL_CERTIFICATES),
            {
                (161, 10),
                (161, 16),
                (161, 27),
                (161, 34),
                (161, 47),
                (161, 53),
                (161, 65),
                (161, 82),
                (161, 86),
                (161, 87),
                (161, 139),
                (161, 151),
                (162, 35),
                (162, 38),
                (162, 94),
                (163, 14),
                (163, 25),
                (163, 27),
                (163, 46),
                (163, 48),
                (163, 95),
                (163, 126),
                (163, 130),
                (163, 153),
                (163, 157),
                (164, 5),
                (164, 22),
                (164, 48),
                (164, 51),
                (164, 69),
                (164, 91),
                (164, 103),
                (164, 105),
                (164, 113),
                (164, 118),
                (164, 125),
                (164, 155),
                (165, 47),
                (165, 58),
                (165, 78),
                (165, 85),
                (165, 106),
                (165, 138),
                (166, 15),
                (166, 36),
                (166, 55),
                (166, 59),
                (166, 63),
                (166, 85),
                (166, 102),
                (166, 109),
                (166, 119),
                (167, 9),
                (167, 12),
                (167, 25),
                (167, 40),
                (167, 56),
                (167, 63),
                (167, 74),
                (167, 82),
                (167, 105),
                (167, 133),
                (167, 156),
                (168, 18),
                (168, 19),
                (168, 50),
                (168, 51),
                (168, 53),
                (168, 97),
                (168, 102),
                (168, 110),
                (168, 125),
                (168, 141),
                (168, 151),
                (168, 158),
                (168, 162),
                (169, 14),
                (169, 23),
                (169, 38),
                (169, 67),
                (169, 79),
                (169, 81),
                (169, 94),
                (169, 119),
                (169, 138),
                (169, 151),
                (169, 161),
                (170, 8),
                (170, 18),
                (170, 21),
                (170, 38),
                (170, 52),
                (170, 64),
                (170, 77),
                (170, 92),
                (170, 97),
                (170, 130),
                (170, 143),
                (170, 148),
                (170, 167),
            },
        )

        for base_target, midpoint in BOX_ONE_SEVENTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_one_seventy_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-170, 171):
            for h in range(-170, 171):
                target = (g, h)
                certificate = box_one_seventy_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_one_seventy_audit_certificate((171, 1)))

    def test_box_one_eighty_finite_audit(self):
        self.assertEqual(
            set(BOX_ONE_EIGHTY_RESIDUAL_CERTIFICATES),
            {
                (171, 35),
                (171, 49),
                (171, 51),
                (171, 55),
                (171, 64),
                (171, 100),
                (171, 104),
                (171, 128),
                (171, 132),
                (171, 147),
                (172, 13),
                (172, 26),
                (172, 28),
                (172, 36),
                (172, 89),
                (172, 91),
                (172, 107),
                (172, 120),
                (172, 138),
                (172, 149),
                (172, 161),
                (172, 162),
                (173, 22),
                (173, 31),
                (173, 35),
                (173, 41),
                (173, 48),
                (173, 84),
                (173, 97),
                (173, 126),
                (173, 136),
                (173, 137),
                (173, 141),
                (173, 150),
                (173, 171),
                (174, 39),
                (174, 53),
                (174, 61),
                (174, 68),
                (174, 70),
                (174, 77),
                (174, 95),
                (174, 100),
                (174, 172),
                (175, 19),
                (175, 20),
                (175, 23),
                (175, 40),
                (175, 46),
                (175, 51),
                (175, 74),
                (175, 117),
                (175, 121),
                (175, 130),
                (175, 165),
                (176, 14),
                (176, 19),
                (176, 23),
                (176, 33),
                (176, 39),
                (176, 68),
                (176, 108),
                (176, 116),
                (176, 124),
                (176, 130),
                (176, 137),
                (176, 165),
                (177, 10),
                (177, 39),
                (177, 55),
                (177, 73),
                (177, 94),
                (177, 112),
                (177, 129),
                (177, 139),
                (177, 147),
                (177, 153),
                (177, 160),
                (177, 164),
                (177, 174),
                (178, 2),
                (178, 19),
                (178, 37),
                (178, 48),
                (178, 50),
                (178, 58),
                (178, 98),
                (178, 119),
                (178, 128),
                (178, 139),
                (178, 156),
                (178, 174),
                (179, 20),
                (179, 34),
                (179, 37),
                (179, 49),
                (179, 111),
                (179, 112),
                (179, 135),
                (179, 166),
                (180, 11),
                (180, 14),
                (180, 27),
                (180, 94),
                (180, 116),
                (180, 119),
            },
        )

        for base_target, midpoint in BOX_ONE_EIGHTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_one_eighty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-180, 181):
            for h in range(-180, 181):
                target = (g, h)
                certificate = box_one_eighty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_one_eighty_audit_certificate((181, 1)))

    def test_box_one_ninety_finite_audit(self):
        self.assertEqual(len(BOX_ONE_NINETY_RESIDUAL_CERTIFICATES), 141)
        self.assertTrue(
            all(
                181 <= max(target) <= 190
                for target in BOX_ONE_NINETY_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_ONE_NINETY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_one_ninety_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-190, 191):
            for h in range(-190, 191):
                target = (g, h)
                certificate = box_one_ninety_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_one_ninety_audit_certificate((191, 1)))

    def test_box_two_hundred_finite_audit(self):
        self.assertEqual(len(BOX_TWO_HUNDRED_RESIDUAL_CERTIFICATES), 110)
        self.assertTrue(
            all(
                191 <= max(target) <= 200
                for target in BOX_TWO_HUNDRED_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_TWO_HUNDRED_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_two_hundred_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-200, 201):
            for h in range(-200, 201):
                target = (g, h)
                certificate = box_two_hundred_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_two_hundred_audit_certificate((201, 1)))

    def test_box_two_ten_finite_audit(self):
        self.assertEqual(len(BOX_TWO_TEN_RESIDUAL_CERTIFICATES), 129)
        self.assertTrue(
            all(201 <= max(target) <= 210 for target in BOX_TWO_TEN_RESIDUAL_CERTIFICATES)
        )

        for base_target, midpoint in BOX_TWO_TEN_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_two_ten_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-210, 211):
            for h in range(-210, 211):
                target = (g, h)
                certificate = box_two_ten_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_two_ten_audit_certificate((211, 1)))

    def test_box_two_twenty_finite_audit(self):
        self.assertEqual(len(BOX_TWO_TWENTY_RESIDUAL_CERTIFICATES), 134)
        self.assertTrue(
            all(
                211 <= max(target) <= 220
                for target in BOX_TWO_TWENTY_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_TWO_TWENTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_two_twenty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-220, 221):
            for h in range(-220, 221):
                target = (g, h)
                certificate = box_two_twenty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_two_twenty_audit_certificate((221, 1)))

    def test_box_two_thirty_finite_audit(self):
        self.assertEqual(len(BOX_TWO_THIRTY_RESIDUAL_CERTIFICATES), 163)
        self.assertTrue(
            all(
                221 <= max(target) <= 230
                for target in BOX_TWO_THIRTY_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_TWO_THIRTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_two_thirty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-230, 231):
            for h in range(-230, 231):
                target = (g, h)
                certificate = box_two_thirty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_two_thirty_audit_certificate((231, 1)))

    def test_box_two_forty_finite_audit(self):
        self.assertEqual(len(BOX_TWO_FORTY_RESIDUAL_CERTIFICATES), 162)
        self.assertTrue(
            all(
                231 <= max(target) <= 240
                for target in BOX_TWO_FORTY_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_TWO_FORTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_two_forty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-240, 241):
            for h in range(-240, 241):
                target = (g, h)
                certificate = box_two_forty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_two_forty_audit_certificate((241, 1)))

    def test_box_two_fifty_finite_audit(self):
        self.assertEqual(len(BOX_TWO_FIFTY_RESIDUAL_CERTIFICATES), 173)
        self.assertTrue(
            all(
                241 <= max(target) <= 250
                for target in BOX_TWO_FIFTY_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_TWO_FIFTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_two_fifty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-250, 251):
            for h in range(-250, 251):
                target = (g, h)
                certificate = box_two_fifty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_two_fifty_audit_certificate((251, 1)))

    def test_box_two_sixty_finite_audit(self):
        self.assertEqual(len(BOX_TWO_SIXTY_RESIDUAL_CERTIFICATES), 167)
        self.assertTrue(
            all(
                251 <= max(target) <= 260
                for target in BOX_TWO_SIXTY_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_TWO_SIXTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_two_sixty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-260, 261):
            for h in range(-260, 261):
                target = (g, h)
                certificate = box_two_sixty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_two_sixty_audit_certificate((261, 1)))

    def test_box_two_seventy_finite_audit(self):
        self.assertEqual(len(BOX_TWO_SEVENTY_RESIDUAL_CERTIFICATES), 173)
        self.assertTrue(
            all(
                261 <= max(target) <= 270
                for target in BOX_TWO_SEVENTY_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_TWO_SEVENTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_two_seventy_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-270, 271):
            for h in range(-270, 271):
                target = (g, h)
                certificate = box_two_seventy_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_two_seventy_audit_certificate((271, 1)))

    def test_box_two_eighty_finite_audit(self):
        self.assertEqual(len(BOX_TWO_EIGHTY_RESIDUAL_CERTIFICATES), 178)
        self.assertTrue(
            all(
                271 <= max(target) <= 280
                for target in BOX_TWO_EIGHTY_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_TWO_EIGHTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_two_eighty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-280, 281):
            for h in range(-280, 281):
                target = (g, h)
                certificate = box_two_eighty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_two_eighty_audit_certificate((281, 1)))

    def test_box_two_ninety_finite_audit(self):
        self.assertEqual(len(BOX_TWO_NINETY_RESIDUAL_CERTIFICATES), 197)
        self.assertTrue(
            all(
                281 <= max(target) <= 290
                for target in BOX_TWO_NINETY_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_TWO_NINETY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_two_ninety_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-290, 291):
            for h in range(-290, 291):
                target = (g, h)
                certificate = box_two_ninety_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_two_ninety_audit_certificate((291, 1)))

    def test_box_three_hundred_finite_audit(self):
        self.assertEqual(len(BOX_THREE_HUNDRED_RESIDUAL_CERTIFICATES), 192)
        self.assertTrue(
            all(
                291 <= max(target) <= 300
                for target in BOX_THREE_HUNDRED_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_THREE_HUNDRED_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_three_hundred_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-300, 301):
            for h in range(-300, 301):
                target = (g, h)
                certificate = box_three_hundred_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_three_hundred_audit_certificate((301, 1)))

    def test_box_three_ten_finite_audit(self):
        self.assertEqual(len(BOX_THREE_TEN_RESIDUAL_CERTIFICATES), 219)
        self.assertTrue(
            all(
                301 <= max(target) <= 310
                for target in BOX_THREE_TEN_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_THREE_TEN_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_three_ten_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-310, 311):
            for h in range(-310, 311):
                target = (g, h)
                certificate = box_three_ten_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_three_ten_audit_certificate((311, 1)))

    def test_box_three_twenty_finite_audit(self):
        self.assertEqual(len(BOX_THREE_TWENTY_RESIDUAL_CERTIFICATES), 206)
        self.assertTrue(
            all(
                311 <= max(target) <= 320
                for target in BOX_THREE_TWENTY_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_THREE_TWENTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_three_twenty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-320, 321):
            for h in range(-320, 321):
                target = (g, h)
                certificate = box_three_twenty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_three_twenty_audit_certificate((321, 1)))

    def test_box_three_thirty_finite_audit(self):
        self.assertEqual(len(BOX_THREE_THIRTY_RESIDUAL_CERTIFICATES), 231)
        self.assertTrue(
            all(
                321 <= max(target) <= 330
                for target in BOX_THREE_THIRTY_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_THREE_THIRTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_three_thirty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-330, 331):
            for h in range(-330, 331):
                target = (g, h)
                certificate = box_three_thirty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_three_thirty_audit_certificate((331, 1)))

    def test_box_three_forty_finite_audit(self):
        self.assertEqual(len(BOX_THREE_FORTY_RESIDUAL_CERTIFICATES), 237)
        self.assertTrue(
            all(
                331 <= max(target) <= 340
                for target in BOX_THREE_FORTY_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_THREE_FORTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_three_forty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-340, 341):
            for h in range(-340, 341):
                target = (g, h)
                certificate = box_three_forty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_three_forty_audit_certificate((341, 1)))

    def test_box_three_fifty_finite_audit(self):
        self.assertEqual(len(BOX_THREE_FIFTY_RESIDUAL_CERTIFICATES), 246)
        self.assertTrue(
            all(
                341 <= max(target) <= 350
                for target in BOX_THREE_FIFTY_RESIDUAL_CERTIFICATES
            )
        )

        for base_target, midpoint in BOX_THREE_FIFTY_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = box_three_fifty_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        for g in range(-350, 351):
            for h in range(-350, 351):
                target = (g, h)
                certificate = box_three_fifty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_three_fifty_audit_certificate((351, 1)))

    def test_box_three_sixty_finite_audit(self):
        self.assertEqual(BOX_THREE_SIXTY_RESIDUAL_CERTIFICATES, {})
        self.assertIsNone(box_three_sixty_residual_certificate((360, 1)))

        for g in range(-360, 361):
            for h in range(-360, 361):
                target = (g, h)
                certificate = box_three_sixty_audit_certificate(target)

                if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
                    self.assertIsNone(certificate)
                    continue

                if edge((0, 0), target):
                    if certificate is not None:
                        self.assertEqual(certificate.target, target)
                        self.assertTrue(certificate.valid())
                    continue

                self.assertIsNotNone(certificate, target)
                self.assertEqual(certificate.target, target)
                self.assertTrue(certificate.valid())

        self.assertIsNone(box_three_sixty_audit_certificate((361, 1)))

    @pytest.mark.perf
    def test_box_five_hundred_finite_audit(self):
        self.assertEqual(BOX_FIVE_HUNDRED_RESIDUAL_CERTIFICATES, {})
        self.assertIsNone(box_five_hundred_residual_certificate((500, 1)))

        assert_finite_box_audit(500, box_five_hundred_audit_certificate)

        self.assertIsNone(box_five_hundred_audit_certificate((501, 1)))

    def test_box_five_hundred_ray_lift_promotes_primitive_seeds(self):
        self.assertIsNone(box_five_hundred_ray_lift_certificate((0, 0)))
        for target in KNOWN_DISTANCE_THREE_ORBIT:
            self.assertIsNone(box_five_hundred_ray_lift_certificate(target))

        examples = (
            ((38, 1), 100, (3800, 100)),
            ((79, 1), 37, (2923, 37)),
            ((401, 237), 19, (7619, 4503)),
            ((-233, 377), 23, (-5359, 8671)),
        )
        for primitive, multiplier, target in examples:
            base = box_five_hundred_audit_certificate(primitive)
            self.assertIsNotNone(base, primitive)
            cert = box_five_hundred_ray_lift_certificate(target)
            self.assertEqual(cert, scale_certificate(base, multiplier))
            self.assertEqual(cert.target, target)
            self.assertTrue(cert.valid())

        for target in ((1000, 0), (0, -1000), (4000, 2000), (-2000, 4000)):
            cert = box_five_hundred_ray_lift_certificate(target)
            self.assertIsNotNone(cert, target)
            self.assertEqual(cert.target, target)
            self.assertTrue(cert.valid())

        lifted_failures: list[Point] = []
        for g in range(-40, 41):
            for h in range(-40, 41):
                primitive = (g, h)
                if primitive == (0, 0) or gcd(abs(g), abs(h)) != 1:
                    continue
                if primitive in KNOWN_DISTANCE_THREE_ORBIT:
                    continue
                if edge((0, 0), primitive):
                    continue

                target = (17 * g, 17 * h)
                cert = box_five_hundred_ray_lift_certificate(target)
                if cert is None or cert.target != target or not cert.valid():
                    lifted_failures.append(target)

        self.assertEqual(tuple(lifted_failures), ())
        self.assertIsNone(box_five_hundred_ray_lift_certificate((501, 1)))

    def test_unit_coordinate_finite_audit_to_500(self):
        self.assertEqual(
            set(UNIT_COORDINATE_500_RESIDUAL_CERTIFICATES),
            {
                (38, 1),
                (79, 1),
                (89, 1),
                (93, 1),
                (128, 1),
                (136, 1),
                (151, 1),
                (203, 1),
                (259, 1),
                (261, 1),
                (266, 1),
                (326, 1),
                (353, 1),
                (371, 1),
                (376, 1),
                (389, 1),
                (392, 1),
                (422, 1),
                (436, 1),
                (441, 1),
                (473, 1),
                (476, 1),
            },
        )

        for base_target, midpoint in UNIT_COORDINATE_500_RESIDUAL_CERTIFICATES.items():
            base_certificate = Certificate(target=base_target, midpoint=midpoint)
            self.assertTrue(base_certificate.valid())
            for orbit_target in sign_swap_orbit(base_target):
                certificate = unit_coordinate_500_residual_certificate(orbit_target)
                self.assertIsNotNone(certificate)
                self.assertEqual(certificate.target, orbit_target)
                self.assertTrue(certificate.valid())

        targets = {
            (n, sign)
            for n in range(-500, 501)
            for sign in (-1, 1)
        } | {
            (sign, n)
            for n in range(-500, 501)
            for sign in (-1, 1)
        }
        for target in targets:
            certificate = unit_coordinate_500_audit_certificate(target)

            if target in KNOWN_DISTANCE_THREE_ORBIT:
                self.assertIsNone(certificate)
                continue

            self.assertIsNotNone(certificate, target)
            self.assertEqual(certificate.target, target)
            self.assertTrue(certificate.valid())

        self.assertIsNone(unit_coordinate_500_audit_certificate((501, 1)))
        self.assertIsNone(unit_coordinate_500_audit_certificate((3, 2)))

    def test_euclid_strip_template(self):
        for direction in ((3, 4), (15, 8), (-5, 12), (7, -24)):
            u, v = direction
            for q in range(-20, 21):
                for parameter_a in range(-12, 13):
                    cert = euclid_strip_certificate(direction, q, parameter_a)
                    if q == 0 or parameter_a == 0:
                        self.assertIsNone(cert)
                        continue

                    parameter_b = u * parameter_a - q
                    second_y = parameter_b * parameter_b - parameter_a * parameter_a
                    coefficient_numerator = q - second_y
                    if (
                        coefficient_numerator % v != 0
                        or coefficient_numerator // v == 0
                        or parameter_b == 0
                        or abs(parameter_b) == abs(parameter_a)
                    ):
                        self.assertIsNone(cert)
                        continue

                    coefficient = coefficient_numerator // v
                    self.assertIsNotNone(cert)
                    self.assertEqual(
                        cert.target,
                        (
                            u * coefficient + 2 * parameter_a * parameter_b,
                            q,
                        ),
                    )
                    self.assertEqual(cert.midpoint, (u * coefficient, v * coefficient))
                    self.assertTrue(cert.valid())

        with self.assertRaises(ValueError):
            euclid_strip_certificate((1, 1), 1, 1)

    def test_half_leg_strip_family(self):
        for direction in ((3, 4), (5, 12), (15, 8), (7, 24), (21, 20)):
            u, v = direction
            for q in range(-35, 36):
                for t in range(-12, 13):
                    cert = half_leg_strip_certificate(direction, q, t)
                    if q == 0 or t == 0 or (q * (1 - q)) % v != 0:
                        self.assertIsNone(cert)
                        continue

                    parameter_a = v * t // 2
                    parameter_b = u * parameter_a - q
                    coefficient = (
                        q * (1 - q) // v
                        + u * q * t
                        - (u * u - 1) * v * t * t // 4
                    )
                    if coefficient == 0 or parameter_b == 0 or abs(parameter_b) == abs(parameter_a):
                        self.assertIsNone(cert)
                        continue

                    expected_x = (
                        u * q * (1 - q) // v
                        + q * t * (u * u - v)
                        + u * v * (1 + 2 * v - u * u) * t * t // 4
                    )
                    self.assertIsNotNone(cert)
                    self.assertEqual(cert.target, (expected_x, q))
                    self.assertEqual(cert.midpoint, (u * coefficient, v * coefficient))
                    self.assertTrue(cert.valid())

        for bad_direction in ((8, 15), (6, 8), (1, 1)):
            with self.assertRaises(ValueError):
                half_leg_strip_certificate(bad_direction, 1, 1)

    def test_half_leg_strip_target_solver(self):
        for direction in ((3, 4), (5, 12), (15, 8), (7, 24), (21, 20), (-3, 4), (5, -12)):
            u, v = direction
            quadratic_coefficient = u * v * (1 + 2 * v - u * u) // 4
            for q in range(-30, 31):
                for g in range(-900, 901):
                    target = (g, q)
                    cert = half_leg_strip_target_certificate(target, direction)

                    expected = None
                    candidate_parameters = set()
                    if q != 0 and (q * (1 - q)) % v == 0:
                        constant = u * q * (1 - q) // v
                        linear_coefficient = q * (u * u - v)
                        target_offset = g - constant
                        if quadratic_coefficient == 0:
                            if (
                                linear_coefficient != 0
                                and target_offset % linear_coefficient == 0
                            ):
                                candidate_parameters.add(target_offset // linear_coefficient)
                        else:
                            discriminant = (
                                linear_coefficient * linear_coefficient
                                + 4 * quadratic_coefficient * target_offset
                            )
                            if discriminant >= 0:
                                root = isqrt(discriminant)
                                if root * root == discriminant:
                                    denominator = 2 * quadratic_coefficient
                                    for numerator in (
                                        -linear_coefficient + root,
                                        -linear_coefficient - root,
                                    ):
                                        if numerator % denominator == 0:
                                            candidate_parameters.add(numerator // denominator)

                    for t in sorted(candidate_parameters):
                        candidate = half_leg_strip_certificate(direction, q, t)
                        if candidate is not None and candidate.target == target:
                            expected = candidate
                            break

                    self.assertEqual(cert, expected)
                    if cert is not None:
                        self.assertEqual(cert.target, target)
                        self.assertTrue(cert.valid())

            for q in range(-24, 25):
                for t in range(-12, 13):
                    base = half_leg_strip_certificate(direction, q, t)
                    if base is None:
                        continue
                    for orbit_target in sign_swap_orbit(base.target):
                        cert = half_leg_strip_orbit_certificate(orbit_target, direction)
                        self.assertIsNotNone(cert)
                        self.assertEqual(cert.target, orbit_target)
                        self.assertTrue(cert.valid())

        for bad_direction in ((8, 15), (6, 8), (1, 1)):
            with self.assertRaises(ValueError):
                half_leg_strip_target_certificate((5, 1), bad_direction)
            with self.assertRaises(ValueError):
                half_leg_strip_orbit_certificate((5, 1), bad_direction)

    def test_half_leg_unit_coordinate_family(self):
        for direction in ((3, 4), (5, 12), (15, 8), (7, 24), (21, 20), (-3, 4), (5, -12)):
            u, v = direction
            for t in range(-25, 26):
                cert = half_leg_unit_coordinate_certificate(direction, t)
                if t == 0:
                    self.assertIsNone(cert)
                    continue

                expected_x = (
                    t * (u * u - v)
                    + u * v * (1 + 2 * v - u * u) * t * t // 4
                )
                z = v // 4
                coefficient = u * t - z * (u * u - 1) * t * t
                expected = half_leg_strip_certificate(direction, 1, t)
                self.assertEqual(cert, expected)
                self.assertIsNotNone(cert)
                self.assertEqual(cert.target, (expected_x, 1))
                self.assertEqual(cert.midpoint, (u * coefficient, v * coefficient))
                self.assertTrue(cert.valid())

        for m in range(2, 18):
            direction = (2 * m - 1, 2 * m * (m - 1))
            for t in range(-20, 21):
                self.assertEqual(
                    half_leg_unit_coordinate_certificate(direction, t),
                    consecutive_hypotenuse_unit_coordinate_certificate(m, t),
                )

        for bad_direction in ((8, 15), (6, 8), (1, 1)):
            with self.assertRaises(ValueError):
                half_leg_unit_coordinate_certificate(bad_direction, 1)

    def test_half_leg_unit_coordinate_target_solver(self):
        for direction in ((3, 4), (5, 12), (15, 8), (7, 24), (21, 20), (-3, 4), (5, -12)):
            u, v = direction
            linear_coefficient = u * u - v
            quadratic_coefficient = u * v * (1 + 2 * v - u * u) // 4
            for g in range(-2000, 2001):
                target = (g, 1)
                cert = half_leg_unit_coordinate_target_certificate(target, direction)

                expected = None
                candidate_parameters = set()
                if quadratic_coefficient == 0:
                    if linear_coefficient != 0 and g % linear_coefficient == 0:
                        candidate_parameters.add(g // linear_coefficient)
                else:
                    discriminant = (
                        linear_coefficient * linear_coefficient
                        + 4 * quadratic_coefficient * g
                    )
                    if discriminant >= 0:
                        root = isqrt(discriminant)
                        if root * root == discriminant:
                            denominator = 2 * quadratic_coefficient
                            for numerator in (
                                -linear_coefficient + root,
                                -linear_coefficient - root,
                            ):
                                if numerator % denominator == 0:
                                    candidate_parameters.add(numerator // denominator)

                for t in sorted(candidate_parameters):
                    candidate = half_leg_unit_coordinate_certificate(direction, t)
                    if candidate is not None and candidate.target == target:
                        expected = candidate
                        break

                self.assertEqual(cert, expected)
                if cert is not None:
                    self.assertEqual(cert.target, target)
                    self.assertTrue(cert.valid())

            for t in range(-35, 36):
                base = half_leg_unit_coordinate_certificate(direction, t)
                if base is None:
                    continue
                for orbit_target in sign_swap_orbit(base.target):
                    cert = half_leg_unit_coordinate_orbit_certificate(orbit_target, direction)
                    self.assertIsNotNone(cert)
                    self.assertEqual(cert.target, orbit_target)
                    self.assertTrue(cert.valid())

        for bad_direction in ((8, 15), (6, 8), (1, 1)):
            with self.assertRaises(ValueError):
                half_leg_unit_coordinate_target_certificate((5, 1), bad_direction)
            with self.assertRaises(ValueError):
                half_leg_unit_coordinate_orbit_certificate((5, 1), bad_direction)

    def test_consecutive_direction_strip_solver(self):
        for odd_leg in range(3, 40, 2):
            even_leg = (odd_leg * odd_leg - 1) // 2
            for q in range(-18, 19):
                for g in range(-160, 161):
                    target = (g, q)
                    cert = consecutive_direction_strip_certificate(target, odd_leg)
                    if q == 0:
                        self.assertIsNone(cert)
                        continue

                    numerator = even_leg * g + odd_leg * q * (q - 1)
                    denominator = q * (odd_leg * odd_leg + 1)
                    if numerator % denominator != 0:
                        self.assertIsNone(cert)
                        continue

                    expected = euclid_strip_certificate(
                        (odd_leg, even_leg),
                        q,
                        numerator // denominator,
                    )
                    self.assertEqual(cert, expected)
                    if cert is not None:
                        self.assertEqual(cert.target, target)
                        self.assertTrue(cert.valid())

        for odd_leg, q, parameter_a in (
            (3, -1, -1),
            (5, -7, -2),
            (7, -17, -3),
            (9, -17, -1),
        ):
            raw = euclid_strip_certificate(
                (odd_leg, (odd_leg * odd_leg - 1) // 2),
                q,
                parameter_a,
            )
            self.assertIsNotNone(raw)
            solved = consecutive_direction_strip_certificate(raw.target, odd_leg)
            self.assertEqual(solved, raw)
            self.assertTrue(solved.valid())

        for bad_odd_leg in (1, 2, 4):
            with self.assertRaises(ValueError):
                consecutive_direction_strip_certificate((5, 1), bad_odd_leg)

    def test_integer_slope_consecutive_ray_family(self):
        for odd_leg in range(3, 28, 2):
            even_leg = (odd_leg * odd_leg - 1) // 2
            modulus = odd_leg * odd_leg + 1
            for slope in range(-6, 7):
                for multiplier in range(-90, 91):
                    cert = integer_slope_consecutive_ray_certificate(
                        slope,
                        multiplier,
                        odd_leg,
                    )

                    expected = None
                    if multiplier != 0:
                        target = (slope * multiplier, multiplier)
                        for direction_sign in (1, -1):
                            numerator = (
                                even_leg * slope
                                + direction_sign * odd_leg * (multiplier - 1)
                            )
                            if numerator % modulus != 0:
                                continue

                            expected = euclid_strip_certificate(
                                (direction_sign * odd_leg, even_leg),
                                multiplier,
                                numerator // modulus,
                            )
                            if expected is not None:
                                self.assertEqual(expected.target, target)
                                break

                    self.assertEqual(cert, expected)
                    if cert is not None:
                        self.assertTrue(cert.valid())

            for slope in range(-4, 5):
                for direction_sign in (1, -1):
                    residue = (
                        1
                        + direction_sign * slope * odd_leg * even_leg
                    ) % modulus
                    for quotient in range(-6, 7):
                        multiplier = quotient * modulus + residue
                        if multiplier == 0:
                            continue

                        cert = integer_slope_consecutive_ray_certificate(
                            slope,
                            multiplier,
                            odd_leg,
                        )
                        raw = euclid_strip_certificate(
                            (direction_sign * odd_leg, even_leg),
                            multiplier,
                            (
                                even_leg * slope
                                + direction_sign * odd_leg * (multiplier - 1)
                            ) // modulus,
                        )
                        if raw is not None:
                            self.assertIsNotNone(cert)
                            self.assertEqual(cert.target, (slope * multiplier, multiplier))
                            self.assertTrue(cert.valid())

        for odd_leg in range(3, 30, 2):
            for multiplier in range(1, 250):
                self.assertEqual(
                    integer_slope_consecutive_ray_certificate(2, multiplier, odd_leg),
                    two_one_ray_consecutive_certificate(multiplier, odd_leg),
                )

        self.assertIsNone(integer_slope_consecutive_ray_certificate(2, 0, 3))
        for bad_odd_leg in (1, 2, 4):
            with self.assertRaises(ValueError):
                integer_slope_consecutive_ray_certificate(2, 5, bad_odd_leg)

    def test_rational_slope_consecutive_ray_family(self):
        rays = (
            (1, 2),
            (2, 3),
            (5, 2),
            (-3, 2),
            (4, -3),
            (-5, -2),
        )
        for odd_leg in range(3, 22, 2):
            even_leg = (odd_leg * odd_leg - 1) // 2
            modulus = odd_leg * odd_leg + 1
            for ray in rays:
                ray_x, ray_y = ray
                for multiplier in range(-45, 46):
                    cert = rational_slope_consecutive_ray_certificate(
                        ray,
                        multiplier,
                        odd_leg,
                    )

                    expected = None
                    if multiplier != 0:
                        target = (ray_x * multiplier, ray_y * multiplier)
                        for direction_sign in (1, -1):
                            numerator = (
                                even_leg * ray_x
                                + direction_sign
                                * odd_leg
                                * ray_y
                                * (ray_y * multiplier - 1)
                            )
                            denominator = ray_y * modulus
                            if numerator % denominator != 0:
                                continue

                            expected = euclid_strip_certificate(
                                (direction_sign * odd_leg, even_leg),
                                ray_y * multiplier,
                                numerator // denominator,
                            )
                            if expected is not None:
                                self.assertEqual(expected.target, target)
                                break

                    self.assertEqual(cert, expected)
                    if cert is not None:
                        self.assertTrue(cert.valid())

        for odd_leg in range(3, 24, 2):
            for slope in range(-5, 6):
                for multiplier in range(-60, 61):
                    self.assertEqual(
                        rational_slope_consecutive_ray_certificate(
                            (slope, 1),
                            multiplier,
                            odd_leg,
                        ),
                        integer_slope_consecutive_ray_certificate(
                            slope,
                            multiplier,
                            odd_leg,
                        ),
                    )

        self.assertIsNone(rational_slope_consecutive_ray_certificate((3, 0), 5, 3))
        self.assertIsNone(rational_slope_consecutive_ray_certificate((3, 2), 0, 3))
        for bad_odd_leg in (1, 2, 4):
            with self.assertRaises(ValueError):
                rational_slope_consecutive_ray_certificate((3, 2), 5, bad_odd_leg)

    def test_two_one_ray_consecutive_family(self):
        for odd_leg in range(3, 42, 2):
            for t in range(1, 18):
                multiplier = t * (odd_leg * odd_leg + 1) - 2 * odd_leg + 1
                cert = two_one_ray_consecutive_certificate(multiplier, odd_leg)

                if t == odd_leg - 1:
                    self.assertIsNone(cert)
                    continue

                self.assertIsNotNone(cert)
                self.assertEqual(cert.target, (2 * multiplier, multiplier))
                self.assertTrue(cert.valid())

                for target in (
                    (2 * multiplier, multiplier),
                    (-2 * multiplier, multiplier),
                    (2 * multiplier, -multiplier),
                    (multiplier, 2 * multiplier),
                    (-multiplier, 2 * multiplier),
                    (multiplier, -2 * multiplier),
                ):
                    orbit_cert = two_one_ray_consecutive_orbit_certificate(target, odd_leg)
                    self.assertIsNotNone(orbit_cert)
                    self.assertEqual(orbit_cert.target, target)
                    self.assertTrue(orbit_cert.valid())

            for t in range(0, 18):
                multiplier = t * (odd_leg * odd_leg + 1) + 2 * odd_leg + 1
                cert = two_one_ray_consecutive_certificate(multiplier, odd_leg)
                self.assertIsNotNone(cert)
                self.assertEqual(cert.target, (2 * multiplier, multiplier))
                self.assertTrue(cert.valid())

                for target in (
                    (2 * multiplier, multiplier),
                    (-2 * multiplier, multiplier),
                    (2 * multiplier, -multiplier),
                    (multiplier, 2 * multiplier),
                    (-multiplier, 2 * multiplier),
                    (multiplier, -2 * multiplier),
                ):
                    orbit_cert = two_one_ray_consecutive_orbit_certificate(target, odd_leg)
                    self.assertIsNotNone(orbit_cert)
                    self.assertEqual(orbit_cert.target, target)
                    self.assertTrue(orbit_cert.valid())

        self.assertIsNone(two_one_ray_consecutive_certificate(1, 3))
        self.assertIsNone(two_one_ray_consecutive_certificate(0, 3))
        self.assertIsNone(two_one_ray_consecutive_orbit_certificate((3, 1), 3))
        self.assertIsNone(two_one_ray_consecutive_orbit_certificate((2, 1), 3))

        for bad_odd_leg in (1, 2, 4):
            with self.assertRaises(ValueError):
                two_one_ray_consecutive_certificate(5, bad_odd_leg)
            with self.assertRaises(ValueError):
                two_one_ray_consecutive_orbit_certificate((10, 5), bad_odd_leg)

    def test_two_one_ray_three_mod_four_family(self):
        base_three = two_one_ray_three_mod_four_certificate(3)
        self.assertIsNotNone(base_three)
        self.assertEqual(base_three.midpoint, (12, -5))
        self.assertTrue(base_three.valid())

        for multiplier in range(7, 400, 4):
            odd_leg = (multiplier - 1) // 2
            cert = two_one_ray_three_mod_four_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(
                cert.midpoint,
                (2 * odd_leg, 1 - odd_leg * odd_leg),
            )
            self.assertTrue(cert.valid())
            self.assertEqual(
                cert,
                two_one_ray_consecutive_certificate(multiplier, odd_leg),
            )

            for target in (
                (2 * multiplier, multiplier),
                (-2 * multiplier, multiplier),
                (2 * multiplier, -multiplier),
                (multiplier, 2 * multiplier),
                (-multiplier, 2 * multiplier),
                (multiplier, -2 * multiplier),
            ):
                orbit_cert = two_one_ray_three_mod_four_orbit_certificate(target)
                self.assertIsNotNone(orbit_cert)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        for multiplier in (0, 1, 5, 9, 13, 101):
            self.assertIsNone(two_one_ray_three_mod_four_certificate(multiplier))

        for target in ((2, 1), (10, 5), (18, 9), (7, 1), (0, 3), (6, 0)):
            self.assertIsNone(two_one_ray_three_mod_four_orbit_certificate(target))

    def test_two_one_ray_five_or_seventeen_mod_twenty_family(self):
        for multiplier in range(5, 500, 20):
            parameter_t = (multiplier + 5) // 10
            coefficient = 2 * (parameter_t * parameter_t + parameter_t - 1)
            cert = two_one_ray_five_or_seventeen_mod_twenty_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(cert.midpoint, (3 * coefficient, 4 * coefficient))
            self.assertTrue(cert.valid())
            self.assertEqual(cert, two_one_ray_consecutive_certificate(multiplier, 3))

            for target in (
                (2 * multiplier, multiplier),
                (-2 * multiplier, multiplier),
                (2 * multiplier, -multiplier),
                (multiplier, 2 * multiplier),
                (-multiplier, 2 * multiplier),
                (multiplier, -2 * multiplier),
            ):
                orbit_cert = (
                    two_one_ray_five_or_seventeen_mod_twenty_orbit_certificate(target)
                )
                self.assertIsNotNone(orbit_cert)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        for multiplier in range(17, 500, 20):
            parameter_t = (multiplier - 7) // 10
            coefficient = 2 * (parameter_t * parameter_t + parameter_t - 1)
            cert = two_one_ray_five_or_seventeen_mod_twenty_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(cert.midpoint, (-3 * coefficient, 4 * coefficient))
            self.assertTrue(cert.valid())
            self.assertEqual(cert, two_one_ray_consecutive_certificate(multiplier, 3))

            for target in (
                (2 * multiplier, multiplier),
                (-2 * multiplier, multiplier),
                (2 * multiplier, -multiplier),
                (multiplier, 2 * multiplier),
                (-multiplier, 2 * multiplier),
                (multiplier, -2 * multiplier),
            ):
                orbit_cert = (
                    two_one_ray_five_or_seventeen_mod_twenty_orbit_certificate(target)
                )
                self.assertIsNotNone(orbit_cert)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        for multiplier in (0, 1, 3, 7, 9, 13, 21):
            self.assertIsNone(
                two_one_ray_five_or_seventeen_mod_twenty_certificate(multiplier)
            )

        for target in ((2, 1), (6, 3), (14, 7), (18, 9), (26, 13), (0, 5), (10, 0)):
            self.assertIsNone(
                two_one_ray_five_or_seventeen_mod_twenty_orbit_certificate(target)
            )

    def test_two_one_ray_two_or_three_mod_five_parallel_family(self):
        for multiplier in range(2, 500):
            cert = two_one_ray_two_or_three_mod_five_parallel_certificate(multiplier)
            if multiplier % 5 not in (2, 3):
                self.assertIsNone(cert, multiplier)
                continue

            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertTrue(cert.valid())

            if multiplier == 2:
                self.assertEqual(cert, two_one_ray_even_certificate(multiplier))
            elif multiplier == 3:
                self.assertEqual(
                    cert,
                    two_one_ray_multiple_of_three_theorem3_certificate(multiplier),
                )
            elif multiplier % 5 == 2:
                self.assertEqual(
                    cert,
                    ray_parallel_factor_certificate(
                        (2 * multiplier, multiplier),
                        (2, 1),
                        (4, 3),
                        2,
                    ),
                )
            else:
                self.assertEqual(
                    cert,
                    ray_parallel_factor_certificate(
                        (2 * multiplier, multiplier),
                        (2, 1),
                        (-4, -3),
                        2,
                    ),
                )

            for target in (
                (2 * multiplier, multiplier),
                (-2 * multiplier, multiplier),
                (2 * multiplier, -multiplier),
                (multiplier, 2 * multiplier),
                (-multiplier, 2 * multiplier),
                (multiplier, -2 * multiplier),
            ):
                orbit_cert = (
                    two_one_ray_two_or_three_mod_five_parallel_orbit_certificate(
                        target
                    )
                )
                self.assertIsNotNone(orbit_cert, target)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        self.assertEqual(
            two_one_ray_two_or_three_mod_five_parallel_certificate(7).midpoint,
            (20, 15),
        )
        self.assertEqual(
            two_one_ray_two_or_three_mod_five_parallel_certificate(8).midpoint,
            (4, 3),
        )
        for target in ((2, 1), (10, 5), (18, 9), (7, 1), (0, 3), (6, 0)):
            self.assertIsNone(
                two_one_ray_two_or_three_mod_five_parallel_orbit_certificate(
                    target
                )
            )

    def test_two_one_ray_mod20_skeleton_family(self):
        self.assertEqual(
            two_one_ray_mod20_skeleton_residues(),
            tuple(residue for residue in range(20) if residue not in (1, 9)),
        )

        examples = (
            (5, (6, 8)),
            (13, (-4, -3)),
            (17, (-6, 8)),
            (25, (66, 88)),
            (33, (-116, -87)),
            (45, (174, 232)),
        )
        for multiplier, midpoint in examples:
            cert = two_one_ray_mod20_skeleton_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(cert.midpoint, midpoint)
            self.assertTrue(cert.valid())

        for multiplier in range(2, 500):
            cert = two_one_ray_mod20_skeleton_certificate(multiplier)
            if multiplier % 20 in (1, 9):
                self.assertIsNone(cert, multiplier)
                continue

            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertTrue(cert.valid())

            for target in (
                (2 * multiplier, multiplier),
                (-2 * multiplier, multiplier),
                (2 * multiplier, -multiplier),
                (multiplier, 2 * multiplier),
                (-multiplier, 2 * multiplier),
                (multiplier, -2 * multiplier),
            ):
                orbit_cert = two_one_ray_mod20_skeleton_orbit_certificate(target)
                self.assertIsNotNone(orbit_cert, target)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        for target in ((2, 1), (18, 9), (42, 21), (7, 1), (0, 5), (10, 0)):
            self.assertIsNone(two_one_ray_mod20_skeleton_orbit_certificate(target))

    def test_two_one_ray_multiple_of_three_theorem3_family(self):
        triple = PythagoreanTriple(12, 5, 13)
        for multiplier in (3, 6, 9, 12, 21, 69, 3003):
            cert = two_one_ray_multiple_of_three_theorem3_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            parameter = multiplier // 3
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(cert.midpoint, (12 * parameter, -5 * parameter))
            self.assertTrue(cert.valid())
            self.assertEqual(
                cert,
                theorem3_ray_divisor_certificate((2, 1), multiplier, triple, 1, -1),
            )

        for multiplier in (-3, 0, 1, 2, 4, 5, 10):
            self.assertIsNone(
                two_one_ray_multiple_of_three_theorem3_certificate(multiplier)
            )

        for target in (
            (18, 9),
            (-18, 9),
            (18, -9),
            (9, 18),
            (-9, 18),
            (9, -18),
            (42, -21),
        ):
            orbit_cert = two_one_ray_multiple_of_three_theorem3_orbit_certificate(
                target
            )
            self.assertIsNotNone(orbit_cert, target)
            self.assertEqual(orbit_cert.target, target)
            self.assertTrue(orbit_cert.valid())

        for target in ((2, 1), (10, 5), (29, 1), (0, 3), (6, 0)):
            self.assertIsNone(
                two_one_ray_multiple_of_three_theorem3_orbit_certificate(target)
            )

    def test_two_one_ray_mod60_theorem3_skeleton_family(self):
        missing_residues = (1, 29, 41, 49)
        self.assertEqual(
            two_one_ray_mod60_theorem3_skeleton_residues(),
            tuple(residue for residue in range(60) if residue not in missing_residues),
        )

        for multiplier in (9, 21):
            cert = two_one_ray_mod60_theorem3_skeleton_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(
                cert,
                two_one_ray_multiple_of_three_theorem3_certificate(multiplier),
            )

        for multiplier in range(2, 240):
            cert = two_one_ray_mod60_theorem3_skeleton_certificate(multiplier)
            if multiplier % 60 in missing_residues:
                self.assertIsNone(cert, multiplier)
                continue

            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertTrue(cert.valid())

            for target in (
                (2 * multiplier, multiplier),
                (-2 * multiplier, multiplier),
                (2 * multiplier, -multiplier),
                (multiplier, 2 * multiplier),
                (-multiplier, 2 * multiplier),
                (multiplier, -2 * multiplier),
            ):
                orbit_cert = two_one_ray_mod60_theorem3_skeleton_orbit_certificate(
                    target
                )
                self.assertIsNotNone(orbit_cert, target)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        for target in ((2, 1), (58, 29), (82, 41), (98, 49), (0, 5), (10, 0)):
            self.assertIsNone(
                two_one_ray_mod60_theorem3_skeleton_orbit_certificate(target)
            )

    def test_two_one_ray_mod260_skeleton_family(self):
        missing_residues = (
            1,
            9,
            21,
            29,
            41,
            49,
            61,
            81,
            101,
            109,
            129,
            149,
            161,
            169,
            181,
            189,
            201,
            209,
            221,
            229,
            241,
            249,
        )
        self.assertEqual(
            two_one_ray_mod260_skeleton_residues(),
            tuple(residue for residue in range(260) if residue not in missing_residues),
        )

        examples = (
            (69, (110, 264)),
            (89, (-110, 264)),
            (121, (290, 696)),
            (141, (-290, 696)),
        )
        for multiplier, midpoint in examples:
            cert = two_one_ray_mod260_skeleton_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(cert.midpoint, midpoint)
            self.assertTrue(cert.valid())
            self.assertEqual(cert, two_one_ray_consecutive_certificate(multiplier, 5))

        for multiplier in range(2, 800):
            cert = two_one_ray_mod260_skeleton_certificate(multiplier)
            if multiplier % 260 in missing_residues:
                self.assertIsNone(cert, multiplier)
                continue

            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertTrue(cert.valid())

            for target in (
                (2 * multiplier, multiplier),
                (-2 * multiplier, multiplier),
                (2 * multiplier, -multiplier),
                (multiplier, 2 * multiplier),
                (-multiplier, 2 * multiplier),
                (multiplier, -2 * multiplier),
            ):
                orbit_cert = two_one_ray_mod260_skeleton_orbit_certificate(target)
                self.assertIsNotNone(orbit_cert, target)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        for target in ((2, 1), (18, 9), (58, 29), (82, 41), (0, 5), (10, 0)):
            self.assertIsNone(two_one_ray_mod260_skeleton_orbit_certificate(target))

    def test_two_one_ray_mod_ten_divisor_family(self):
        self.assertEqual(
            two_one_ray_complement_divisor_residues((3, -4)),
            tuple(range(3, 50, 10)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((-3, 4)),
            tuple(range(7, 50, 10)),
        )

        examples = (
            (3, (66, -88)),
            (7, (-354, 472)),
            (9, (198, -264)),
            (21, (462, -616)),
        )
        for multiplier, midpoint in examples:
            cert = two_one_ray_mod_ten_divisor_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(cert.midpoint, midpoint)
            self.assertTrue(cert.valid())

        for multiplier in range(1, 800):
            has_mod_ten_divisor = any(
                divisor % 10 in (3, 7)
                for divisor in positive_divisors(multiplier)
            )
            cert = two_one_ray_mod_ten_divisor_certificate(multiplier)
            if not has_mod_ten_divisor:
                self.assertIsNone(cert, multiplier)
                continue

            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertTrue(cert.valid())

            for target in (
                (2 * multiplier, multiplier),
                (-2 * multiplier, multiplier),
                (2 * multiplier, -multiplier),
                (multiplier, 2 * multiplier),
                (-multiplier, 2 * multiplier),
                (multiplier, -2 * multiplier),
            ):
                orbit_cert = two_one_ray_mod_ten_divisor_orbit_certificate(target)
                self.assertIsNotNone(orbit_cert, target)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        self.assertEqual(
            two_one_ray_mod_ten_divisor_certificate(21),
            two_one_ray_complement_divisor_certificate(21, (3, -4)),
        )
        for target in ((2, 1), (58, 29), (82, 41), (0, 3), (6, 0)):
            self.assertIsNone(two_one_ray_mod_ten_divisor_orbit_certificate(target))

    def test_two_one_ray_mod_twenty_six_divisor_family(self):
        self.assertEqual(
            two_one_ray_complement_divisor_residues((5, 12)),
            tuple(range(3, 338, 26)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((-5, 12)),
            tuple(range(7, 338, 26)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((5, -12)),
            tuple(range(19, 338, 26)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((-5, -12)),
            tuple(range(23, 338, 26)),
        )

        examples = (
            (29, (4510, 10824)),
            (101, (-54410, -130584)),
            (149, (276190, -662856)),
            (241, (-722590, 1734216)),
        )
        for multiplier, midpoint in examples:
            cert = two_one_ray_mod_twenty_six_divisor_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(cert.midpoint, midpoint)
            self.assertTrue(cert.valid())

        for multiplier in range(1, 800):
            has_mod_twenty_six_divisor = any(
                divisor % 26 in (3, 7, 19, 23)
                for divisor in positive_divisors(multiplier)
            )
            cert = two_one_ray_mod_twenty_six_divisor_certificate(multiplier)
            if not has_mod_twenty_six_divisor:
                self.assertIsNone(cert, multiplier)
                continue

            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertTrue(cert.valid())

            for target in (
                (2 * multiplier, multiplier),
                (-2 * multiplier, multiplier),
                (2 * multiplier, -multiplier),
                (multiplier, 2 * multiplier),
                (-multiplier, 2 * multiplier),
                (multiplier, -2 * multiplier),
            ):
                orbit_cert = two_one_ray_mod_twenty_six_divisor_orbit_certificate(
                    target
                )
                self.assertIsNotNone(orbit_cert, target)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        for target in ((2, 1), (82, 41), (122, 61), (0, 29), (58, 0)):
            self.assertIsNone(
                two_one_ray_mod_twenty_six_divisor_orbit_certificate(target)
            )

    def test_two_one_ray_mod_twenty_six_square_factor_family(self):
        self.assertEqual(
            two_one_ray_square_determinant_factor_period((5, -12)),
            (26, (15,)),
        )
        self.assertEqual(
            two_one_ray_square_determinant_factor_residues((5, -12)),
            tuple(range(15, 338, 26)),
        )
        self.assertEqual(
            two_one_ray_hypotenuse_square_factor_directions(13),
            pythagorean_directions_for_hypotenuse(13),
        )
        self.assertEqual(
            two_one_ray_hypotenuse_square_factor_residue_classes(13),
            (26, (6, 9, 10, 11, 15, 16, 17, 20)),
        )
        self.assertEqual(
            two_one_ray_hypotenuse_square_factor_residue_classes(17),
            (34, (5, 13, 14, 16, 18, 20, 21, 29)),
        )
        self.assertEqual(
            TWO_ONE_RAY_PROMOTED_SQUARE_FACTOR_HYPOTENUSES,
            (13, 17, 37, 41),
        )
        self.assertEqual(
            two_one_ray_square_determinant_factor_certificate(41, (5, -12)),
            Certificate(target=(82, 41), midpoint=(10, -24)),
        )
        self.assertEqual(
            two_one_ray_square_determinant_divisor_certificate(45, (5, -12)),
            Certificate(target=(90, 45), midpoint=(-30, 72)),
        )
        self.assertIsNone(
            two_one_ray_square_determinant_factor_certificate(41, (8, 15))
        )
        self.assertIsNone(two_one_ray_mod_twenty_six_square_factor_certificate(145))
        self.assertIsNone(two_one_ray_mod_twenty_six_square_factor_certificate(290))

        example = two_one_ray_mod_twenty_six_square_factor_certificate(5449)
        self.assertIsNotNone(example)
        self.assertEqual(example.target, (10898, 5449))
        self.assertEqual(example.midpoint, (438890, -1053336))
        self.assertTrue(example.valid())

        promoted_examples = (
            (2141, (-66410, -159384)),
            (2341, (144870, -77264)),
            (3301, (-132370, -45384)),
            (5101, (-68058, -302480)),
        )
        for multiplier, midpoint in promoted_examples:
            cert = two_one_ray_promoted_square_factor_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(cert.midpoint, midpoint)
            self.assertTrue(cert.valid())

        for multiplier in range(1, 1000):
            cert = two_one_ray_mod_twenty_six_square_factor_certificate(multiplier)
            has_square_factor_divisor = any(
                divisor % 26 == 15 and divisor != 145
                for divisor in positive_divisors(multiplier)
            )
            if not has_square_factor_divisor:
                self.assertIsNone(cert, multiplier)
                continue

            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertTrue(cert.valid())

        for hypotenuse in TWO_ONE_RAY_PROMOTED_SQUARE_FACTOR_HYPOTENUSES:
            for multiplier in range(1, 800):
                cert = two_one_ray_hypotenuse_square_factor_certificate(
                    multiplier,
                    hypotenuse,
                )
                has_square_factor_divisor = any(
                    any(
                        two_one_ray_square_determinant_factor_certificate(
                            divisor,
                            direction,
                        )
                        is not None
                        for direction in two_one_ray_hypotenuse_square_factor_directions(
                            hypotenuse
                        )
                    )
                    for divisor in positive_divisors(multiplier)
                )
                if not has_square_factor_divisor:
                    self.assertIsNone(cert, (multiplier, hypotenuse))
                    continue

                self.assertIsNotNone(cert, (multiplier, hypotenuse))
                self.assertEqual(cert.target, (2 * multiplier, multiplier))
                self.assertTrue(cert.valid())

        checked = 0
        for u, v, c, _parameter_m, _parameter_k in primitive_pythagorean_directions(12):
            if c > 250:
                continue

            direction = (u, v)
            linear_factor = 2 * u + v
            determinant_factor = u - 2 * v
            modulus, residues = two_one_ray_square_determinant_factor_period(
                direction
            )
            if determinant_factor == 0:
                self.assertEqual((modulus, residues), (1, ()))
                continue

            root = residues[0]
            self.assertEqual(modulus, 2 * c)
            self.assertEqual(root % c, (-linear_factor) % c)
            self.assertEqual(root % 2, determinant_factor % 2)
            self.assertEqual(
                two_one_ray_square_determinant_factor_residues(direction),
                tuple(range(root, 2 * c * c, 2 * c)),
            )

            brute_witness_roots = tuple(
                residue
                for residue in range(2 * c)
                if parallel_direction_factor_witness(
                    (2 * (residue if residue else 2 * c), residue if residue else 2 * c),
                    direction,
                    determinant_factor * determinant_factor,
                )
                is not None
            )
            self.assertEqual(brute_witness_roots, residues, direction)
            checked += 1

        self.assertEqual(checked, 240)

    def test_two_one_ray_promoted_scaled_factor_layers(self):
        self.assertEqual(
            TWO_ONE_RAY_PROMOTED_SCALED_FACTOR_LAYERS,
            (
                ((-12, 5), 22),
                ((-12, -5), 2),
                ((20, -21), 2),
            ),
        )
        self.assertEqual(
            minimal_periodic_residue_classes(
                parallel_direction_factor_modulus((-12, 5), 22),
                ray_parallel_factor_residues((2, 1), (-12, 5), 22),
            ),
            (13, (5,)),
        )
        self.assertEqual(
            minimal_periodic_residue_classes(
                parallel_direction_factor_modulus((-12, -5), 2),
                ray_parallel_factor_residues((2, 1), (-12, -5), 2),
            ),
            (13, (8,)),
        )
        self.assertEqual(
            minimal_periodic_residue_classes(
                parallel_direction_factor_modulus((20, -21), 2),
                ray_parallel_factor_residues((2, 1), (20, -21), 2),
            ),
            (29, (23,)),
        )
        self.assertIsNone(
            two_one_ray_scaled_factor_divisor_certificate(5, (-12, 5), 22)
        )

        examples = (
            (3229, ((-12, 5), 22), (-8139372, 3391405)),
            (3329, ((20, -21), 2), (253272220, -265935831)),
            (4649, ((-12, -5), 2), (-1525092, -635455)),
        )
        for multiplier, layer, midpoint in examples:
            direct = two_one_ray_scaled_factor_divisor_certificate(
                multiplier,
                *layer,
            )
            promoted = two_one_ray_promoted_scaled_factor_certificate(multiplier)
            self.assertIsNotNone(direct, multiplier)
            self.assertEqual(direct.target, (2 * multiplier, multiplier))
            self.assertEqual(direct.midpoint, midpoint)
            self.assertTrue(direct.valid())
            self.assertEqual(promoted, direct)

    def test_two_one_ray_determinant_split_factor_layers(self):
        self.assertEqual(
            TWO_ONE_RAY_PROMOTED_DETERMINANT_SPLIT_FACTOR_HYPOTENUSES,
            (17, 29, 37, 41, 53, 61, 73, 89, 97, 197, 401),
        )
        self.assertEqual(
            two_one_ray_determinant_split_factor_period((3, -4), 1),
            two_one_ray_complement_divisor_period((3, -4)),
        )
        self.assertEqual(
            two_one_ray_determinant_split_factor_period((5, -12), 841),
            two_one_ray_square_determinant_factor_period((5, -12)),
        )
        self.assertEqual(
            two_one_ray_determinant_split_factor_period((-12, 5), 22),
            (13, (5,)),
        )
        self.assertEqual(
            two_one_ray_determinant_split_factor_period((8, -15), 2),
            (17, (2,)),
        )
        self.assertEqual(
            two_one_ray_determinant_split_factor_period((20, 21), 2),
            (29, (20,)),
        )
        self.assertEqual(
            two_one_ray_determinant_split_factor_period((-40, -9), 22),
            (41, (32,)),
        )
        self.assertEqual(
            two_one_ray_double_direction_certificate((3, 4)),
            Certificate(target=(10, 5), midpoint=(6, 8)),
        )
        double_direction_examples = (
            ((-4275, -25132), 110161, (-8550, -50264)),
            ((-16965, 31948), 110501, (-33930, 63896)),
            ((-8475, 57148), 133121, (-16950, 114296)),
            ((188469, 43700), 159769, (376938, 87400)),
        )
        for direction, multiplier, midpoint in double_direction_examples:
            cert = two_one_ray_double_direction_certificate(direction)
            self.assertIsNotNone(cert, direction)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(cert.midpoint, midpoint)
            self.assertTrue(cert.valid())
            one_mod_four = (
                two_one_ray_prime_one_mod_four_double_direction_certificate(
                    multiplier
                )
            )
            self.assertIsNotNone(one_mod_four, multiplier)
            self.assertEqual(one_mod_four.target, cert.target)
            self.assertTrue(one_mod_four.valid())
            lifted = two_one_ray_lift_three_square_endpoint_certificate(multiplier)
            self.assertEqual(lifted, cert)
            self.assertEqual(two_one_ray_seed_certificate(multiplier), one_mod_four)
        self.assertIsNone(
            two_one_ray_prime_one_mod_four_double_direction_certificate(9)
        )
        self.assertIsNone(
            two_one_ray_prime_one_mod_four_double_direction_certificate(19)
        )
        one_mod_four_examples = (
            (5, (6, 8)),
            (13, (30, 16)),
            (17, (10, 24)),
            (29, (70, 24)),
            (37, (14, 48)),
        )
        for multiplier, midpoint in one_mod_four_examples:
            cert = two_one_ray_prime_one_mod_four_double_direction_certificate(
                multiplier
            )
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(cert.midpoint, midpoint)
            self.assertTrue(cert.valid())
        for multiplier in range(2, 5000):
            cert = two_one_ray_prime_one_mod_four_double_direction_certificate(
                multiplier
            )
            if not (is_prime(multiplier) and multiplier % 4 == 1):
                self.assertIsNone(cert, multiplier)
                continue

            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertTrue(cert.valid())

        sample_layers = (
            ((8, -15), 2),
            ((20, 21), 2),
            ((-40, -9), 22),
        )
        for direction, base_factor in sample_layers:
            self.assertEqual(
                two_one_ray_determinant_split_factor_period(
                    direction,
                    base_factor,
                ),
                minimal_periodic_residue_classes(
                    parallel_direction_factor_modulus(direction, base_factor),
                    ray_parallel_factor_residues((2, 1), direction, base_factor),
                ),
            )

        self.assertIn(
            ((8, -15), 2),
            two_one_ray_hypotenuse_determinant_split_factor_layers(17),
        )
        self.assertIn(
            ((20, 21), 2),
            two_one_ray_hypotenuse_determinant_split_factor_layers(29),
        )
        self.assertIn(
            ((-40, -9), 22),
            two_one_ray_hypotenuse_determinant_split_factor_layers(41),
        )
        self.assertEqual(
            len(two_one_ray_hypotenuse_determinant_split_factor_layers(17)),
            32,
        )
        self.assertEqual(
            len(two_one_ray_hypotenuse_determinant_split_factor_layers(29)),
            36,
        )
        self.assertEqual(
            len(two_one_ray_hypotenuse_determinant_split_factor_layers(41)),
            36,
        )

        examples = (
            (5849, 29, (98450980, 103373529)),
            (7669, 17, (587728808, -1101991515)),
            (9749, 41, (-24856760, -5592771)),
            (10061, 53, (820710, -510664)),
            (23869, 197, (1474590, -211736)),
            (40429, 401, (-58403063560, -582570559011)),
        )
        for multiplier, hypotenuse, midpoint in examples:
            hypotenuse_cert = (
                two_one_ray_hypotenuse_determinant_split_factor_certificate(
                    multiplier,
                    hypotenuse,
                )
            )
            promoted = two_one_ray_promoted_determinant_split_factor_certificate(
                multiplier
            )
            self.assertIsNotNone(hypotenuse_cert, multiplier)
            self.assertEqual(hypotenuse_cert.target, (2 * multiplier, multiplier))
            self.assertEqual(hypotenuse_cert.midpoint, midpoint)
            self.assertTrue(hypotenuse_cert.valid())
            self.assertIsNotNone(promoted, multiplier)
            self.assertEqual(promoted.target, (2 * multiplier, multiplier))
            self.assertTrue(promoted.valid())

        witness_examples = {
            5849: (41, 5849, (20, 21), 29, 2, 242, 29, 20),
            7669: (41, 7669, (8, -15), 17, 2, 722, 17, 2),
            9749: (41, 9749, (8, -15), 17, 722, 2, 17, 8),
            10061: (100, 10061, (45, -28), 53, 10201, 1, 106, 97),
            23869: (250, 23869, (195, -28), 197, 63001, 1, 394, 229),
            40429: (500, 40429, (-40, -399), 401, 2, 287282, 401, 329),
            110161: (300, 110161, (-105, -208), 233, 96721, 1, 466, 185),
            110501: (300, 110501, (-115, 252), 277, 383161, 1, 554, 255),
            133121: (300, 133121, (-119, 120), 169, 128881, 1, 338, 287),
        }
        for multiplier, expected in witness_examples.items():
            (
                max_hypotenuse,
                quotient,
                direction,
                hypotenuse,
                base_factor,
                paired_factor,
                period,
                residue,
            ) = expected
            witness = two_one_ray_determinant_split_factor_witness(
                multiplier,
                max_hypotenuse,
            )
            self.assertIsInstance(witness, TwoOneRayDeterminantSplitFactorWitness)
            self.assertEqual(
                (
                    witness.quotient,
                    witness.direction,
                    witness.hypotenuse,
                    witness.base_factor,
                    witness.paired_factor,
                    witness.period,
                    witness.residue,
                ),
                (
                    quotient,
                    direction,
                    hypotenuse,
                    base_factor,
                    paired_factor,
                    period,
                    residue,
                ),
            )
            self.assertEqual(witness.target, (2 * multiplier, multiplier))
            self.assertEqual(witness.quotient % witness.period, witness.residue)
            self.assertEqual(
                witness.base_factor * witness.paired_factor,
                witness.determinant_factor * witness.determinant_factor,
            )
            self.assertEqual(
                (
                    witness.quotient * witness.paired_factor
                    + witness.linear_factor
                )
                % witness.hypotenuse,
                0,
            )
            self.assertEqual(
                witness.lift_parameter,
                (
                    witness.quotient * witness.paired_factor
                    + witness.linear_factor
                )
                // witness.hypotenuse,
            )
            lift_discriminant = witness.lift_parameter * witness.lift_parameter - 5
            lift_x = (
                lift_discriminant * witness.hypotenuse
                - witness.lift_parameter
                * witness.quotient
                * witness.paired_factor
            )
            self.assertEqual(
                lift_x * lift_x
                + lift_discriminant
                * witness.determinant_factor
                * witness.determinant_factor,
                5
                * witness.quotient
                * witness.quotient
                * witness.paired_factor
                * witness.paired_factor,
            )
            self.assertTrue(witness.valid())
            self.assertEqual(witness.certificate.target, witness.target)

            self.assertEqual(
                two_one_ray_determinant_paired_factor_root(
                    witness.quotient,
                    witness.paired_factor,
                    witness.hypotenuse,
                ),
                (witness.direction, witness.base_factor),
            )
            paired_witness = two_one_ray_paired_factor_split_factor_witness(
                multiplier,
                paired_factor,
                max_hypotenuse,
            )
            self.assertEqual(paired_witness, witness)
            if witness.lift_parameter <= 2000:
                lift_witness = two_one_ray_paired_factor_lift_witness(
                    multiplier,
                    paired_factor,
                    witness.lift_parameter,
                )
                self.assertIsNotNone(lift_witness, multiplier)
                self.assertEqual(lift_witness.target, witness.target)
                self.assertLessEqual(
                    lift_witness.lift_parameter,
                    witness.lift_parameter,
                )
                self.assertTrue(lift_witness.valid())
            self.assertEqual(
                two_one_ray_determinant_paired_factor_lift_root(
                    witness.quotient,
                    witness.paired_factor,
                    witness.lift_parameter,
                ),
                (witness.direction, witness.base_factor, witness.hypotenuse),
            )

        self.assertEqual(
            tuple(
                multiplier
                for multiplier in range(10000, 1000000)
                if (
                    is_prime(multiplier)
                    and two_one_ray_seed_certificate(multiplier) is None
                )
            ),
            (),
        )

    def test_two_one_ray_mod_thirty_four_divisor_family(self):
        self.assertEqual(
            two_one_ray_complement_divisor_residues((15, -8)),
            tuple(range(7, 578, 34)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((15, 8)),
            tuple(range(13, 578, 34)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((-15, -8)),
            tuple(range(21, 578, 34)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((-15, 8)),
            tuple(range(27, 578, 34)),
        )

        self.assertEqual(
            two_one_ray_complement_divisor_period((15, -8)),
            (34, (7,)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_sieve_residue_classes(
                ((15, -8), (15, 8), (-15, -8), (-15, 8))
            ),
            (34, (7, 13, 21, 27)),
        )

        examples = (
            (41, (41970, -22384)),
            (149, (870, 464)),
            (89, (-30, -16)),
            (61, (-92730, 49456)),
        )
        for multiplier, midpoint in examples:
            cert = two_one_ray_mod_thirty_four_divisor_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(cert.midpoint, midpoint)
            self.assertTrue(cert.valid())

        for multiplier in range(1, 800):
            has_mod_thirty_four_divisor = any(
                divisor % 34 in (7, 13, 21, 27)
                for divisor in positive_divisors(multiplier)
            )
            cert = two_one_ray_mod_thirty_four_divisor_certificate(multiplier)
            if not has_mod_thirty_four_divisor:
                self.assertIsNone(cert, multiplier)
                continue

            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertTrue(cert.valid())

            for target in (
                (2 * multiplier, multiplier),
                (-2 * multiplier, multiplier),
                (2 * multiplier, -multiplier),
                (multiplier, 2 * multiplier),
                (-multiplier, 2 * multiplier),
                (multiplier, -2 * multiplier),
            ):
                orbit_cert = two_one_ray_mod_thirty_four_divisor_orbit_certificate(
                    target
                )
                self.assertIsNotNone(orbit_cert, target)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        for target in ((2, 1), (10, 5), (22, 11), (58, 29), (0, 41), (82, 0)):
            self.assertIsNone(
                two_one_ray_mod_thirty_four_divisor_orbit_certificate(target)
            )

    def test_two_one_ray_mod_fifty_eight_divisor_family(self):
        self.assertEqual(
            two_one_ray_complement_divisor_residues((-21, -20)),
            tuple(range(7, 1682, 58)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((-21, 20)),
            tuple(range(25, 1682, 58)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((21, -20)),
            tuple(range(33, 1682, 58)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((21, 20)),
            tuple(range(51, 1682, 58)),
        )

        self.assertEqual(
            two_one_ray_complement_divisor_period((-21, -20)),
            (58, (7,)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_sieve_residue_classes(
                ((-21, -20), (-21, 20), (21, -20), (21, 20))
            ),
            (58, (7, 25, 33, 51)),
        )

        examples = (
            (7, (-210, -200)),
            (25, (-29022, 27640)),
            (33, (50610, -48200)),
            (51, (11802, 11240)),
        )
        for multiplier, midpoint in examples:
            cert = two_one_ray_mod_fifty_eight_divisor_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(cert.midpoint, midpoint)
            self.assertTrue(cert.valid())

        for multiplier in range(1, 800):
            has_mod_fifty_eight_divisor = any(
                divisor % 58 in (7, 25, 33, 51)
                for divisor in positive_divisors(multiplier)
            )
            cert = two_one_ray_mod_fifty_eight_divisor_certificate(multiplier)
            if not has_mod_fifty_eight_divisor:
                self.assertIsNone(cert, multiplier)
                continue

            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertTrue(cert.valid())

            for target in (
                (2 * multiplier, multiplier),
                (-2 * multiplier, multiplier),
                (2 * multiplier, -multiplier),
                (multiplier, 2 * multiplier),
                (-multiplier, 2 * multiplier),
                (multiplier, -2 * multiplier),
            ):
                orbit_cert = two_one_ray_mod_fifty_eight_divisor_orbit_certificate(
                    target
                )
                self.assertIsNotNone(orbit_cert, target)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        for target in ((2, 1), (22, 11), (158, 79), (0, 7), (14, 0)):
            self.assertIsNone(
                two_one_ray_mod_fifty_eight_divisor_orbit_certificate(target)
            )

    def test_two_one_ray_mod_seventy_four_divisor_family(self):
        self.assertEqual(
            two_one_ray_complement_divisor_residues((-35, 12)),
            tuple(range(7, 2738, 74)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((-35, -12)),
            tuple(range(23, 2738, 74)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((35, 12)),
            tuple(range(51, 2738, 74)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((35, -12)),
            tuple(range(67, 2738, 74)),
        )

        self.assertEqual(
            two_one_ray_complement_divisor_period((-35, 12)),
            (74, (7,)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_sieve_residue_classes(
                ((-35, 12), (-35, -12), (35, 12), (35, -12))
            ),
            (74, (7, 23, 51, 67)),
        )

        examples = (
            (7, (-2170, 744)),
            (23, (-770, -264)),
            (51, (4130, 1416)),
            (67, (199850, -68520)),
        )
        for multiplier, midpoint in examples:
            cert = two_one_ray_mod_seventy_four_divisor_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(cert.midpoint, midpoint)
            self.assertTrue(cert.valid())

        for multiplier in range(1, 800):
            has_mod_seventy_four_divisor = any(
                divisor % 74 in (7, 23, 51, 67)
                for divisor in positive_divisors(multiplier)
            )
            cert = two_one_ray_mod_seventy_four_divisor_certificate(multiplier)
            if not has_mod_seventy_four_divisor:
                self.assertIsNone(cert, multiplier)
                continue

            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertTrue(cert.valid())

            for target in (
                (2 * multiplier, multiplier),
                (-2 * multiplier, multiplier),
                (2 * multiplier, -multiplier),
                (multiplier, 2 * multiplier),
                (-multiplier, 2 * multiplier),
                (multiplier, -2 * multiplier),
            ):
                orbit_cert = two_one_ray_mod_seventy_four_divisor_orbit_certificate(
                    target
                )
                self.assertIsNotNone(orbit_cert, target)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        for target in ((2, 1), (22, 11), (158, 79), (0, 7), (14, 0)):
            self.assertIsNone(
                two_one_ray_mod_seventy_four_divisor_orbit_certificate(target)
            )

    def test_two_one_ray_mod_eighty_two_divisor_family(self):
        self.assertEqual(
            two_one_ray_complement_divisor_residues((9, -40)),
            tuple(range(13, 3362, 82)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((9, 40)),
            tuple(range(29, 3362, 82)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((-9, -40)),
            tuple(range(53, 3362, 82)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_residues((-9, 40)),
            tuple(range(69, 3362, 82)),
        )

        self.assertEqual(
            two_one_ray_complement_divisor_period((9, -40)),
            (82, (13,)),
        )
        self.assertEqual(
            two_one_ray_complement_divisor_sieve_residue_classes(
                ((9, -40), (9, 40), (-9, -40), (-9, 40))
            ),
            (82, (13, 29, 53, 69)),
        )

        examples = (
            (13, (3582, -15920)),
            (29, (11358, 50480)),
            (53, (-37890, -168400)),
            (69, (-100962, 448720)),
        )
        for multiplier, midpoint in examples:
            cert = two_one_ray_mod_eighty_two_divisor_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(cert.midpoint, midpoint)
            self.assertTrue(cert.valid())

        for multiplier in range(1, 800):
            has_mod_eighty_two_divisor = any(
                divisor % 82 in (13, 29, 53, 69)
                for divisor in positive_divisors(multiplier)
            )
            cert = two_one_ray_mod_eighty_two_divisor_certificate(multiplier)
            if not has_mod_eighty_two_divisor:
                self.assertIsNone(cert, multiplier)
                continue

            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertTrue(cert.valid())

            for target in (
                (2 * multiplier, multiplier),
                (-2 * multiplier, multiplier),
                (2 * multiplier, -multiplier),
                (multiplier, 2 * multiplier),
                (-multiplier, 2 * multiplier),
                (multiplier, -2 * multiplier),
            ):
                orbit_cert = two_one_ray_mod_eighty_two_divisor_orbit_certificate(
                    target
                )
                self.assertIsNotNone(orbit_cert, target)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        for target in ((2, 1), (22, 11), (158, 79), (0, 13), (26, 0)):
            self.assertIsNone(
                two_one_ray_mod_eighty_two_divisor_orbit_certificate(target)
            )

    def test_two_one_ray_complement_divisor_root_formula(self):
        self.assertEqual(two_one_ray_complement_divisor_root((3, -4)), 3)
        self.assertEqual(two_one_ray_complement_divisor_root((-3, 4)), 7)
        self.assertIsNone(two_one_ray_complement_divisor_root((8, 15)))

        checked = 0
        nonempty = 0
        for u, v, c, parameter_m, parameter_k in primitive_pythagorean_directions(20):
            if c > 300:
                continue

            linear = 2 * u + v
            determinant_factor = u - 2 * v
            modulus = 2 * c * c
            brute_roots = tuple(
                residue
                for residue in range(2 * c)
                if (
                    determinant_factor
                    * determinant_factor
                    * residue
                    * residue
                    + 2 * linear * residue
                    - 1
                )
                % modulus
                == 0
            )
            root = two_one_ray_complement_divisor_root((u, v))
            if root is None:
                self.assertEqual(brute_roots, (), (u, v, c))
                self.assertEqual(two_one_ray_complement_divisor_period((u, v)), (1, ()))
                self.assertEqual(two_one_ray_complement_divisor_residues((u, v)), ())
            else:
                nonempty += 1
                self.assertEqual(brute_roots, (root,), (u, v, c))
                self.assertEqual(root % 2, 1)
                self.assertEqual(
                    root % c,
                    (
                        -linear
                        * pow(
                            (determinant_factor * determinant_factor) % c,
                            -1,
                            c,
                        )
                    )
                    % c,
                )
                self.assertEqual(
                    two_one_ray_complement_divisor_period((u, v)),
                    (2 * c, (root,)),
                )
                self.assertEqual(
                    two_one_ray_complement_divisor_residues((u, v)),
                    tuple(range(root, 2 * c * c, 2 * c)),
                )
                cert = two_one_ray_complement_divisor_certificate(root, (u, v))
                self.assertIsNotNone(cert, (u, v, c))
                self.assertTrue(cert.valid())

            checked += 1

        self.assertEqual(checked, 376)
        self.assertEqual(nonempty, 158)

    def test_two_one_ray_hypotenuse_divisor_layer(self):
        self.assertEqual(
            pythagorean_directions_for_hypotenuse(5),
            ((-4, -3), (-4, 3), (-3, -4), (-3, 4), (3, -4), (3, 4), (4, -3), (4, 3)),
        )
        self.assertEqual(two_one_ray_hypotenuse_divisor_directions(5), ((-3, 4), (3, -4)))
        self.assertEqual(two_one_ray_hypotenuse_divisor_residue_classes(5), (10, (3, 7)))
        self.assertEqual(
            two_one_ray_hypotenuse_divisor_residue_classes(13),
            (26, (3, 7, 19, 23)),
        )
        self.assertEqual(
            two_one_ray_hypotenuse_divisor_residue_classes(17),
            (34, (7, 13, 21, 27)),
        )
        self.assertEqual(
            two_one_ray_hypotenuse_divisor_residue_classes(29),
            (58, (7, 25, 33, 51)),
        )
        self.assertEqual(
            two_one_ray_hypotenuse_divisor_residue_classes(37),
            (74, (7, 23, 51, 67)),
        )
        self.assertEqual(
            two_one_ray_hypotenuse_divisor_residue_classes(41),
            (82, (13, 29, 53, 69)),
        )
        self.assertEqual(two_one_ray_hypotenuse_divisor_residue_classes(11), (1, ()))

        named_layers = (
            (17, two_one_ray_mod_thirty_four_divisor_certificate),
            (29, two_one_ray_mod_fifty_eight_divisor_certificate),
            (37, two_one_ray_mod_seventy_four_divisor_certificate),
            (41, two_one_ray_mod_eighty_two_divisor_certificate),
        )
        for hypotenuse, named_constructor in named_layers:
            for multiplier in range(1, 800):
                generic = two_one_ray_hypotenuse_divisor_certificate(
                    multiplier,
                    hypotenuse,
                )
                named = named_constructor(multiplier)
                self.assertEqual(generic is not None, named is not None, multiplier)
                if generic is not None:
                    self.assertEqual(generic.target, (2 * multiplier, multiplier))
                    self.assertTrue(generic.valid())

        example = two_one_ray_hypotenuse_divisor_certificate(521, 41)
        self.assertIsNotNone(example)
        self.assertEqual(example.target, (1042, 521))
        self.assertTrue(example.valid())

    def test_two_one_ray_determinant_slice_root_formula(self):
        self.assertIsNone(two_one_ray_determinant_slice_root(0, 1, 1))

        root = two_one_ray_determinant_slice_root(118, -11, 53)
        self.assertIsInstance(root, TwoOneRayDeterminantSliceRoot)
        self.assertEqual(root.direction, (45, 28))
        self.assertEqual(root.root, 31)
        self.assertEqual(root.modulus, 106)
        self.assertEqual(root.sqrt_minus_one_residue, 30)
        self.assertEqual(euclid_sqrt_minus_one_residues(7, 2), (23, 30))
        self.assertEqual(
            two_one_ray_euclid_parameter_residue_classes(7, 2),
            (106, (31, 47, 59, 75)),
        )
        self.assertEqual(
            two_one_ray_euclid_parameter_residue_classes(6, 5),
            (122, (29, 53, 69, 93)),
        )
        self.assertEqual(
            tuple(
                parameter_root.direction
                for parameter_root in two_one_ray_euclid_parameter_roots(7, 2)
            ),
            ((45, 28), (-45, 28), (45, -28), (-45, -28)),
        )
        self.assertEqual(
            two_one_ray_euclid_parameter_residue_classes(7, 2),
            two_one_ray_hypotenuse_divisor_residue_classes(53),
        )
        self.assertEqual(
            two_one_ray_euclid_parameter_residue_classes(6, 5),
            two_one_ray_hypotenuse_divisor_residue_classes(61),
        )
        self.assertEqual(root.certificate(1409).target, (2818, 1409))
        self.assertTrue(root.certificate(1409).valid())
        self.assertIsNone(root.certificate(1408))

        successor = two_one_ray_determinant_slice_successor(root)
        self.assertEqual(
            successor,
            TwoOneRayDeterminantSliceRoot(
                linear_factor=38078,
                determinant_factor=-11,
                hypotenuse=17029,
                direction=(15229, 7620),
                root=9959,
            ),
        )
        self.assertEqual(successor.modulus, 34058)
        self.assertEqual(successor.certificate(9959).target, (19918, 9959))
        self.assertTrue(successor.certificate(9959).valid())
        self.assertEqual(two_one_ray_determinant_slice_predecessor(successor), root)

        degenerate_step_seed = two_one_ray_determinant_slice_root(-38, 1, 17)
        degenerate_step_successor = two_one_ray_determinant_slice_successor(
            degenerate_step_seed
        )
        self.assertEqual(
            degenerate_step_successor,
            TwoOneRayDeterminantSliceRoot(
                linear_factor=682,
                determinant_factor=1,
                hypotenuse=305,
                direction=(273, 136),
                root=233,
            ),
        )
        self.assertEqual(
            two_one_ray_determinant_slice_predecessor(degenerate_step_successor),
            degenerate_step_seed,
        )
        self.assertEqual(
            two_one_ray_determinant_slice_reduced_root(degenerate_step_successor),
            degenerate_step_seed,
        )

        mod_seventy_four_seed = two_one_ray_determinant_slice_root(-82, -11, 37)
        self.assertEqual(
            two_one_ray_determinant_slice_orbit(mod_seventy_four_seed, 2),
            (
                mod_seventy_four_seed,
                root,
            ),
        )
        orbit_certificate = two_one_ray_determinant_slice_orbit_certificate(
            1409,
            mod_seventy_four_seed,
            2,
        )
        self.assertIsNotNone(orbit_certificate)
        self.assertEqual(orbit_certificate.target, (2818, 1409))
        self.assertTrue(orbit_certificate.valid())
        self.assertIsNone(
            two_one_ray_determinant_slice_orbit_certificate(
                269,
                mod_seventy_four_seed,
                2,
            )
        )
        self.assertEqual(
            two_one_ray_determinant_slice_predecessor(root),
            mod_seventy_four_seed,
        )
        self.assertEqual(
            two_one_ray_determinant_slice_reduced_root(root),
            mod_seventy_four_seed,
        )
        self.assertEqual(
            two_one_ray_determinant_slice_reduced_root(successor),
            mod_seventy_four_seed,
        )

        square_endpoint_seed = two_one_ray_determinant_slice_root(-118, -359, 169)
        self.assertEqual(square_endpoint_seed.square_endpoint_base_factor, 128881)
        self.assertEqual(square_endpoint_seed.square_endpoint_period, (338, (287,)))
        square_endpoint_certificate = square_endpoint_seed.square_endpoint_certificate(
            133121
        )
        self.assertIsNotNone(square_endpoint_certificate)
        self.assertEqual(
            square_endpoint_certificate.midpoint,
            (-36852158, 37161840),
        )
        self.assertTrue(square_endpoint_certificate.valid())
        self.assertIsNone(square_endpoint_seed.square_endpoint_certificate(307969))
        self.assertEqual(
            two_one_ray_determinant_square_endpoint_orbit_certificate(
                133121,
                square_endpoint_seed,
                1,
            ),
            square_endpoint_certificate,
        )
        conjugate_square_endpoint_seed = two_one_ray_determinant_slice_root(
            118,
            359,
            169,
        )
        self.assertEqual(
            conjugate_square_endpoint_seed.square_endpoint_period,
            (338, (51,)),
        )
        conjugate_square_endpoint_certificate = (
            conjugate_square_endpoint_seed.square_endpoint_certificate(307969)
        )
        self.assertIsNotNone(conjugate_square_endpoint_certificate)
        self.assertTrue(conjugate_square_endpoint_certificate.valid())

        divisor_root = two_one_ray_determinant_divisor_root(1409, -11, 53)
        self.assertEqual(divisor_root, root)
        self.assertEqual((1409 * 1409 * 11 * 11 + 1) % 53, 0)
        self.assertEqual(divisor_root.certificate(1409).target, (2818, 1409))
        self.assertTrue(divisor_root.certificate(1409).valid())
        self.assertIsNone(two_one_ray_determinant_divisor_root(1409, -11, 52))
        self.assertIsNone(two_one_ray_determinant_divisor_root(1408, -11, 53))

        checked = 0
        nonempty = 0
        for (
            u,
            v,
            c,
            parameter_m,
            parameter_k,
        ) in primitive_pythagorean_directions(20):
            if c > 300:
                continue

            linear_factor, determinant_factor, coordinate_hypotenuse = (
                two_one_ray_determinant_coordinates((u, v))
            )
            self.assertEqual(coordinate_hypotenuse, c)
            self.assertEqual(
                (linear_factor, determinant_factor),
                gaussian_multiply((2, 1), (u, -v)),
            )
            self.assertEqual(
                gaussian_quotient_if_integer(
                    (linear_factor, determinant_factor),
                    (2, 1),
                ),
                (u, -v),
            )
            self.assertEqual(
                linear_factor * linear_factor
                + determinant_factor * determinant_factor,
                5 * c * c,
            )
            slice_root = two_one_ray_determinant_slice_root(
                linear_factor,
                determinant_factor,
                c,
            )
            direction_root = two_one_ray_complement_divisor_root((u, v))
            if direction_root is None:
                self.assertIsNone(slice_root, (u, v, c))
            else:
                nonempty += 1
                self.assertEqual(slice_root.direction, (u, v))
                self.assertEqual(slice_root.root, direction_root)
                odd_leg = parameter_m * parameter_m - parameter_k * parameter_k
                even_leg = 2 * parameter_m * parameter_k
                self.assertEqual(abs(u), odd_leg)
                self.assertEqual(abs(v), even_leg)
                signed_euclid_root = two_one_ray_signed_euclid_root(
                    parameter_m,
                    parameter_k,
                    1 if u > 0 else -1,
                    1 if v > 0 else -1,
                )
                self.assertEqual(signed_euclid_root, slice_root)
                self.assertEqual(
                    slice_root.certificate(direction_root).target,
                    (2 * direction_root, direction_root),
                )
                self.assertTrue(slice_root.certificate(direction_root).valid())

            checked += 1

        self.assertEqual(checked, 376)
        self.assertEqual(nonempty, 158)

        roots = two_one_ray_determinant_factor_roots(-11, 100)
        self.assertIn(
            TwoOneRayDeterminantSliceRoot(
                linear_factor=118,
                determinant_factor=-11,
                hypotenuse=53,
                direction=(45, 28),
                root=31,
            ),
            roots,
        )
        certificate = two_one_ray_determinant_factor_certificate(1409, -11, 100)
        self.assertIsNotNone(certificate)
        self.assertEqual(certificate.target, (2818, 1409))
        self.assertTrue(certificate.valid())
        self.assertIsNone(
            two_one_ray_determinant_factor_certificate(269, -11, 100)
        )

        divisor_certificate = two_one_ray_determinant_divisor_certificate(
            1409,
            -11,
            100,
        )
        self.assertIsNotNone(divisor_certificate)
        self.assertEqual(divisor_certificate.target, (2818, 1409))
        self.assertTrue(divisor_certificate.valid())
        self.assertIsNone(
            two_one_ray_determinant_divisor_certificate(269, -11, 100)
        )

        euclid_examples = (
            (1409, (7, 2)),
            (1861, (7, 2)),
            (1249, (6, 5)),
            (1289, (6, 5)),
        )
        for multiplier, parameters in euclid_examples:
            certificate = two_one_ray_euclid_parameter_certificate(
                multiplier,
                *parameters,
            )
            self.assertIsNotNone(certificate, multiplier)
            self.assertEqual(certificate.target, (2 * multiplier, multiplier))
            self.assertTrue(certificate.valid())
        self.assertIsNone(two_one_ray_euclid_parameter_certificate(269, 7, 2))

    def test_two_one_ray_inverse_root_witness_probe(self):
        self.assertIsNone(two_one_ray_inverse_root_witness(0, 20))
        self.assertIsNone(two_one_ray_inverse_root_witness(269, 20))

        residual_witnesses = {
            269: ((116, 35), (12231, 8120), 14681, 269),
            281: ((19, 4), (345, -152), 377, 281),
            389: ((15, 4), (209, -120), 241, 389),
            509: ((34, 19), (-795, -1292), 1517, 509),
            941: ((15, 8), (-161, 240), 289, 363),
            1009: ((73, 62), (-1485, 9052), 9173, 1009),
            1049: ((13, 8), (105, -208), 233, 117),
            1249: ((6, 5), (-11, -60), 61, 29),
            1289: ((6, 5), (11, -60), 61, 69),
            1321: ((37, 2), (1365, 148), 1373, 1321),
            1361: ((41, 20), (-1281, 1640), 2081, 1361),
            1409: ((7, 2), (45, 28), 53, 31),
            1481: ((289, 266), (12765, 153748), 154277, 1481),
            1549: ((17, 12), (145, 408), 433, 683),
            1601: ((24, 19), (215, 912), 937, 1601),
            1861: ((7, 2), (45, -28), 53, 59),
            1949: ((15, 8), (161, -240), 289, 215),
            2549: ((8, 3), (55, 48), 73, 67),
            2621: ((8, 5), (39, 80), 89, 129),
            2729: ((20, 1), (-399, -40), 401, 323),
        }
        self.assertEqual(
            TWO_ONE_RAY_PROMOTED_INVERSE_ROOT_PARAMETERS,
            (
                (7, 2),
                (6, 5),
                (13, 8),
                (15, 4),
                (15, 8),
                (19, 4),
                (17, 12),
                (24, 19),
                (37, 2),
                (34, 19),
                (41, 20),
                (73, 62),
                (116, 35),
                (289, 266),
                (8, 3),
                (8, 5),
                (20, 1),
            ),
        )
        for multiplier, expected in residual_witnesses.items():
            witness = two_one_ray_inverse_root_witness(multiplier, 300)
            self.assertIsInstance(witness, TwoOneRayInverseRootWitness)
            self.assertEqual(
                (
                    witness.euclid_parameters,
                    witness.direction,
                    witness.hypotenuse,
                    witness.root,
                ),
                expected,
            )
            self.assertEqual(multiplier % (2 * witness.hypotenuse), witness.root)
            sqrt_residues = euclid_sqrt_minus_one_residues(
                *witness.euclid_parameters
            )
            odd_leg = (
                witness.euclid_parameters[0] * witness.euclid_parameters[0]
                - witness.euclid_parameters[1] * witness.euclid_parameters[1]
            )
            even_leg = 2 * witness.euclid_parameters[0] * witness.euclid_parameters[1]
            self.assertEqual(abs(witness.direction[0]), odd_leg)
            self.assertEqual(abs(witness.direction[1]), even_leg)
            self.assertEqual(
                two_one_ray_signed_euclid_root(
                    *witness.euclid_parameters,
                    1 if witness.direction[0] > 0 else -1,
                    1 if witness.direction[1] > 0 else -1,
                ),
                witness.determinant_slice_root,
            )
            self.assertIn(
                witness.determinant_slice_root.sqrt_minus_one_residue,
                sqrt_residues,
            )
            self.assertEqual(
                (
                    witness.determinant_slice_root.sqrt_minus_one_residue
                    * witness.determinant_slice_root.sqrt_minus_one_residue
                )
                % witness.hypotenuse,
                witness.hypotenuse - 1,
            )
            self.assertEqual(
                (multiplier * witness.determinant_factor) % witness.hypotenuse,
                witness.determinant_slice_root.sqrt_minus_one_residue,
            )
            self.assertEqual(witness.target, (2 * multiplier, multiplier))
            self.assertEqual(witness.certificate.target, witness.target)
            self.assertEqual(
                witness.determinant_slice_root.direction,
                witness.direction,
            )
            self.assertEqual(witness.determinant_slice_root.root, witness.root)
            self.assertEqual(
                witness.determinant_divisor_root,
                witness.determinant_slice_root,
            )
            self.assertEqual(
                (
                    multiplier
                    * multiplier
                    * witness.determinant_factor
                    * witness.determinant_factor
                    + 1
                )
                % witness.hypotenuse,
                0,
            )
            if multiplier == 1409:
                self.assertEqual(
                    witness.reduced_determinant_slice_root,
                    TwoOneRayDeterminantSliceRoot(
                        linear_factor=-82,
                        determinant_factor=-11,
                        hypotenuse=37,
                        direction=(-35, -12),
                        root=23,
                    ),
                )
            else:
                self.assertEqual(
                    witness.reduced_determinant_slice_root,
                    witness.determinant_slice_root,
                )
            promoted = two_one_ray_promoted_inverse_root_certificate(multiplier)
            self.assertIsNotNone(promoted, multiplier)
            self.assertEqual(promoted.target, witness.target)
            self.assertTrue(promoted.valid())
            self.assertTrue(witness.valid())

    def test_complement_divisor_sieve_residue_compression(self):
        self.assertEqual(
            minimal_periodic_residue_classes(12, (1, 5, 7, 11)),
            (6, (1, 5)),
        )
        self.assertEqual(
            periodic_residue_union(((10, (3, 7)), (26, (3, 7, 19, 23)))),
            (130, two_one_ray_mod_130_divisor_residues()),
        )
        self.assertEqual(two_one_ray_complement_divisor_period((3, -4)), (10, (3,)))
        self.assertEqual(two_one_ray_complement_divisor_period((-3, 4)), (10, (7,)))
        self.assertEqual(two_one_ray_complement_divisor_period((5, 12)), (26, (3,)))
        self.assertEqual(two_one_ray_complement_divisor_period((-5, 12)), (26, (7,)))
        self.assertEqual(two_one_ray_complement_divisor_period((5, -12)), (26, (19,)))
        self.assertEqual(two_one_ray_complement_divisor_period((-5, -12)), (26, (23,)))

        directions = (
            (3, -4),
            (-3, 4),
            (5, 12),
            (-5, 12),
            (5, -12),
            (-5, -12),
            (15, -8),
            (15, 8),
            (-15, -8),
            (-15, 8),
            (-21, -20),
            (-21, 20),
            (21, -20),
            (21, 20),
        )
        modulus, residues = two_one_ray_complement_divisor_sieve_residue_classes(
            directions
        )
        expected_residues = tuple(
            residue
            for residue in range(64090)
            if (
                residue % 10 in (3, 7)
                or residue % 26 in (3, 7, 19, 23)
                or residue % 34 in (7, 13, 21, 27)
                or residue % 58 in (7, 25, 33, 51)
            )
        )
        self.assertEqual(modulus, 64090)
        self.assertEqual(residues, expected_residues)
        self.assertEqual(two_one_ray_mod_64090_divisor_residues(), expected_residues)
        self.assertEqual(len(two_one_ray_mod_64090_divisor_residues()), 23270)
        self.assertEqual(len(two_one_ray_mod_2210_divisor_residues()), 754)

        for n in range(1, 2000):
            expected = any(
                divisor % 10 in (3, 7)
                or divisor % 26 in (3, 7, 19, 23)
                or divisor % 34 in (7, 13, 21, 27)
                or divisor % 58 in (7, 25, 33, 51)
                for divisor in positive_divisors(n)
            )
            previous_expected = any(
                divisor % 10 in (3, 7)
                or divisor % 26 in (3, 7, 19, 23)
                or divisor % 34 in (7, 13, 21, 27)
                for divisor in positive_divisors(n)
            )
            self.assertEqual(
                has_two_one_ray_mod_2210_divisor(n),
                previous_expected,
                n,
            )
            self.assertEqual(has_two_one_ray_mod_64090_divisor(n), expected, n)
            self.assertEqual(
                has_divisor_in_residue_classes(n, modulus, residues),
                expected,
                n,
            )
            self.assertEqual(
                two_one_ray_complement_divisor_sieve_certificate(n, directions)
                is not None,
                expected,
                n,
            )

        directions_through_seventy_four = directions + (
            (-35, 12),
            (-35, -12),
            (35, 12),
            (35, -12),
        )
        modulus, residues = two_one_ray_complement_divisor_sieve_residue_classes(
            directions_through_seventy_four
        )
        expected_residues = tuple(
            residue
            for residue in range(2371330)
            if (
                residue % 10 in (3, 7)
                or residue % 26 in (3, 7, 19, 23)
                or residue % 34 in (7, 13, 21, 27)
                or residue % 58 in (7, 25, 33, 51)
                or residue % 74 in (7, 23, 51, 67)
            )
        )
        self.assertEqual(modulus, 2371330)
        self.assertEqual(residues, expected_residues)
        self.assertEqual(
            two_one_ray_mod_2371330_divisor_residues(),
            expected_residues,
        )
        self.assertEqual(len(two_one_ray_mod_2371330_divisor_residues()), 896090)

        for multiplier in (7, 23, 51, 67, 81, 97, 133, 229, 273, 421):
            self.assertTrue(has_two_one_ray_mod_2371330_divisor(multiplier))
        for multiplier in (1, 5, 11, 31, 79, 121, 131, 139, 151):
            self.assertFalse(has_two_one_ray_mod_2371330_divisor(multiplier))

    def test_two_one_ray_divisor_lift_reduces_remaining_ray_to_primes(self):
        self.assertIsNotNone(two_one_ray_seed_certificate(6241))
        examples = (
            (121, (290, 696)),
            (869, (-11210, 26904)),
            (961, (-21948, 9145)),
            (6241, (-4266790, -3723744)),
            (1669, (-2173452, 905605)),
            (1889, (54010, 129624)),
        )
        for multiplier, midpoint in examples:
            cert = two_one_ray_divisor_lift_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(cert.midpoint, midpoint)
            self.assertTrue(cert.valid())

            for target in (
                (2 * multiplier, multiplier),
                (-2 * multiplier, multiplier),
                (2 * multiplier, -multiplier),
                (multiplier, 2 * multiplier),
                (-multiplier, 2 * multiplier),
                (multiplier, -2 * multiplier),
            ):
                orbit_cert = two_one_ray_divisor_lift_orbit_certificate(target)
                self.assertIsNotNone(orbit_cert, target)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        self.assertIsNone(two_one_ray_prime_divisor_lift_certificate(1))
        for multiplier in (2, 3, 5, 11, 17, 121, 361, 6241, 110161, 1872737):
            prime = prime_factors(multiplier)[0]
            base = two_one_ray_seed_certificate(prime)
            self.assertIsNotNone(base, prime)
            cert = two_one_ray_prime_divisor_lift_certificate(multiplier)
            self.assertEqual(cert, scale_certificate(base, multiplier // prime))
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertTrue(cert.valid())

        direct_failures: list[int] = []
        for multiplier in range(2, 10000):
            cert = two_one_ray_prime_divisor_lift_certificate(multiplier)
            if (
                cert is None
                or cert.target != (2 * multiplier, multiplier)
                or not cert.valid()
            ):
                direct_failures.append(multiplier)
        self.assertEqual(tuple(direct_failures), ())

        for target in (
            (242, 121),
            (-242, 121),
            (242, -121),
            (-242, -121),
            (121, 242),
            (-121, 242),
            (121, -242),
            (-121, -242),
            (538, 269),
        ):
            orbit_cert = two_one_ray_prime_divisor_lift_orbit_certificate(target)
            self.assertIsNotNone(orbit_cert, target)
            self.assertEqual(orbit_cert.target, target)
            self.assertTrue(orbit_cert.valid())

        former_residual_primes = (
            269,
            281,
            389,
            509,
            941,
            1009,
            1049,
            1249,
            1289,
            1321,
            1361,
            1409,
            1481,
            1549,
            1601,
            1861,
            1949,
        )
        for multiplier in former_residual_primes:
            cert = two_one_ray_promoted_inverse_root_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertTrue(cert.valid())

        self.assertEqual(
            tuple(
                multiplier
                for multiplier in range(2, 2000)
                if two_one_ray_divisor_lift_certificate(multiplier) is None
            ),
            (),
        )
        self.assertEqual(
            tuple(
                multiplier
                for multiplier in range(2000, 3000)
                if two_one_ray_divisor_lift_certificate(multiplier) is None
            ),
            (),
        )
        self.assertEqual(
            tuple(
                multiplier
                for multiplier in range(3000, 5000)
                if two_one_ray_divisor_lift_certificate(multiplier) is None
            ),
            (),
        )
        self.assertEqual(
            tuple(
                multiplier
                for multiplier in range(5000, 10000)
                if two_one_ray_divisor_lift_certificate(multiplier) is None
            ),
            (),
        )
        self.assertTrue(all(is_prime(multiplier) for multiplier in former_residual_primes))

        former_residual_orbit = two_one_ray_divisor_lift_orbit_certificate((538, 269))
        self.assertIsNotNone(former_residual_orbit)
        self.assertEqual(former_residual_orbit.target, (538, 269))
        self.assertTrue(former_residual_orbit.valid())

        for target in ((2, 1), (0, 121), (242, 0)):
            self.assertIsNone(two_one_ray_divisor_lift_orbit_certificate(target))
            self.assertIsNone(two_one_ray_prime_divisor_lift_orbit_certificate(target))

    def test_mod_ten_divisor_residual_prime_factor_reduction(self):
        self.assertEqual(prime_factors(1), ())
        self.assertEqual(prime_factors(9801), (3, 11))
        self.assertTrue(all_prime_factors_one_or_nine_mod_ten(1))
        self.assertTrue(all_prime_factors_one_or_nine_mod_ten(11 * 19 * 29))
        self.assertFalse(all_prime_factors_one_or_nine_mod_ten(3 * 11))
        self.assertFalse(all_prime_factors_one_or_nine_mod_ten(7 * 19))

        for n in range(1, 2000):
            if gcd(n, 10) != 1:
                continue
            self.assertEqual(
                not has_divisor_three_or_seven_mod_ten(n),
                all_prime_factors_one_or_nine_mod_ten(n),
                n,
            )
            self.assertEqual(
                two_one_ray_mod_ten_divisor_certificate(n) is not None,
                has_divisor_three_or_seven_mod_ten(n),
                n,
            )

        residual_examples = (1, 11, 19, 29, 121, 209, 361, 551)
        for multiplier in residual_examples:
            self.assertTrue(all_prime_factors_one_or_nine_mod_ten(multiplier))
            self.assertFalse(has_divisor_three_or_seven_mod_ten(multiplier))

    def test_combined_mod_130_divisor_residual_reduction(self):
        expected_residues = tuple(
            residue
            for residue in range(130)
            if residue % 10 in (3, 7) or residue % 26 in (3, 7, 19, 23)
        )
        self.assertEqual(two_one_ray_mod_130_divisor_residues(), expected_residues)
        self.assertEqual(
            two_one_ray_mod_130_divisor_residues(),
            (
                3,
                7,
                13,
                17,
                19,
                23,
                27,
                29,
                33,
                37,
                43,
                45,
                47,
                49,
                53,
                55,
                57,
                59,
                63,
                67,
                71,
                73,
                75,
                77,
                81,
                83,
                85,
                87,
                93,
                97,
                101,
                103,
                107,
                111,
                113,
                117,
                123,
                127,
            ),
        )

        with self.assertRaises(ValueError):
            has_divisor_in_residue_classes(10, 0, (1,))

        for n in range(1, 2000):
            expected = (
                two_one_ray_mod_ten_divisor_certificate(n) is not None
                or two_one_ray_mod_twenty_six_divisor_certificate(n) is not None
            )
            self.assertEqual(has_two_one_ray_mod_130_divisor(n), expected, n)
            self.assertEqual(
                has_divisor_in_residue_classes(
                    n,
                    130,
                    two_one_ray_mod_130_divisor_residues(),
                ),
                expected,
                n,
            )

        residual_examples = (1, 11, 31, 41, 61, 89, 121, 181, 229, 349)
        for multiplier in residual_examples:
            self.assertFalse(has_two_one_ray_mod_130_divisor(multiplier))
        self.assertTrue(has_two_one_ray_mod_130_divisor(361))

    def test_two_one_ray_even_family(self):
        for multiplier in range(2, 202, 2):
            cert = two_one_ray_even_certificate(multiplier)
            self.assertIsNotNone(cert)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertEqual(
                cert.midpoint,
                (-18 * multiplier, 77 * multiplier // 2),
            )
            self.assertTrue(cert.valid())

            for target in (
                (2 * multiplier, multiplier),
                (-2 * multiplier, multiplier),
                (2 * multiplier, -multiplier),
                (multiplier, 2 * multiplier),
                (-multiplier, 2 * multiplier),
                (multiplier, -2 * multiplier),
            ):
                orbit_cert = two_one_ray_even_orbit_certificate(target)
                self.assertIsNotNone(orbit_cert)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        for multiplier in (0, 1, 3, 5, 101):
            self.assertIsNone(two_one_ray_even_certificate(multiplier))

        for target in ((2, 1), (6, 3), (3, 1), (0, 2), (2, 0)):
            self.assertIsNone(two_one_ray_even_orbit_certificate(target))

    def test_two_one_ray_explicit_base_table(self):
        expected = {
            3: (12, -5),
            29: (-12, 5),
            41: (-8, -15),
            53: (-20, 21),
            61: (-10, -24),
            73: (-30, 16),
        }
        self.assertEqual(EXPLICIT_TWO_ONE_RAY_BASE_CERTIFICATES, expected)

        for base_multiplier, midpoint in EXPLICIT_TWO_ONE_RAY_BASE_CERTIFICATES.items():
            base = Certificate(
                target=(2 * base_multiplier, base_multiplier),
                midpoint=midpoint,
            )
            self.assertTrue(base.valid())
            self.assertEqual(
                two_one_ray_explicit_base_certificate(base_multiplier),
                base,
            )

            for scale in range(1, 16):
                multiplier = base_multiplier * scale
                scaled_base = scale_certificate(base, scale)
                self.assertTrue(scaled_base.valid())

                cert = two_one_ray_explicit_base_certificate(multiplier)
                self.assertIsNotNone(cert)
                self.assertEqual(cert.target, (2 * multiplier, multiplier))
                self.assertTrue(cert.valid())

                for target in (
                    (2 * multiplier, multiplier),
                    (-2 * multiplier, multiplier),
                    (2 * multiplier, -multiplier),
                    (multiplier, 2 * multiplier),
                    (-multiplier, 2 * multiplier),
                    (multiplier, -2 * multiplier),
                ):
                    orbit_cert = two_one_ray_explicit_base_orbit_certificate(target)
                    self.assertIsNotNone(orbit_cert)
                    self.assertEqual(orbit_cert.target, target)
                    self.assertTrue(orbit_cert.valid())

        for multiplier in (1, 5, 7, 11, 17, 19, 23):
            self.assertIsNone(two_one_ray_explicit_base_certificate(multiplier))

        for target in ((2, 1), (10, 5), (7, 1), (0, 3), (6, 0)):
            self.assertIsNone(two_one_ray_explicit_base_orbit_certificate(target))

    def test_two_one_ray_finite_audit_to_500(self):
        expected = {
            109: (-42, 40),
            113: (-14, -48),
            149: (-42, -40),
            181: (-798, -80),
            209: (1150, -96),
            233: (-80, -39),
            241: (330, -104),
            269: (-60, -91),
            281: (-110, 96),
            293: (510, -64),
            313: (-760, -39),
            353: (-144, 17),
            361: (-2670, -1424),
            373: (-154, 72),
            409: (680, -111),
            421: (-28, -195),
            449: (-182, 120),
            461: (-180, -19),
            473: (286, 48),
        }
        self.assertEqual(EXPLICIT_TWO_ONE_RAY_FINITE_AUDIT_CERTIFICATES, expected)

        for base_multiplier, midpoint in EXPLICIT_TWO_ONE_RAY_FINITE_AUDIT_CERTIFICATES.items():
            base = Certificate(
                target=(2 * base_multiplier, base_multiplier),
                midpoint=midpoint,
            )
            self.assertTrue(base.valid())
            self.assertEqual(
                two_one_ray_finite_audit_certificate(base_multiplier),
                base,
            )

            for target in (
                (2 * base_multiplier, base_multiplier),
                (-2 * base_multiplier, base_multiplier),
                (2 * base_multiplier, -base_multiplier),
                (base_multiplier, 2 * base_multiplier),
                (-base_multiplier, 2 * base_multiplier),
                (base_multiplier, -2 * base_multiplier),
            ):
                orbit_cert = two_one_ray_finite_audit_orbit_certificate(target)
                self.assertIsNotNone(orbit_cert)
                self.assertEqual(orbit_cert.target, target)
                self.assertTrue(orbit_cert.valid())

        def first_ray_certificate(multiplier):
            for constructor in (
                two_one_ray_even_certificate,
                two_one_ray_three_mod_four_certificate,
                two_one_ray_five_or_seventeen_mod_twenty_certificate,
                two_one_ray_mod20_skeleton_certificate,
                two_one_ray_mod_ten_divisor_certificate,
                two_one_ray_mod_twenty_six_divisor_certificate,
                two_one_ray_mod_thirty_four_divisor_certificate,
                two_one_ray_mod_fifty_eight_divisor_certificate,
                two_one_ray_mod_seventy_four_divisor_certificate,
                two_one_ray_divisor_lift_certificate,
                two_one_ray_explicit_base_certificate,
                two_one_ray_finite_audit_certificate,
            ):
                cert = constructor(multiplier)
                if cert is not None:
                    return cert

            target = (2 * multiplier, multiplier)
            for constructor in (
                determinant_seven_lattice_certificate,
                determinant_thirteen_lattice_certificate,
                determinant_seventeen_lattice_certificate,
                small_prime_lattice_certificate,
            ):
                cert = constructor(target)
                if cert is not None:
                    return cert

            for odd_leg in range(3, 502, 2):
                cert = two_one_ray_consecutive_certificate(multiplier, odd_leg)
                if cert is not None:
                    return cert

            return None

        for multiplier in range(2, 501):
            cert = first_ray_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (2 * multiplier, multiplier))
            self.assertTrue(cert.valid())

        self.assertIsNone(two_one_ray_finite_audit_certificate(1))
        self.assertIsNone(two_one_ray_finite_audit_orbit_certificate((2, 1)))
        self.assertIsNone(two_one_ray_finite_audit_orbit_certificate((7, 1)))

    def test_unit_coordinate_multiple_of_five_family(self):
        for t in range(-80, 81):
            if t == 0:
                continue
            for target in ((5 * t, 1), (5 * t, -1), (1, 5 * t), (-1, 5 * t)):
                cert = unit_coordinate_multiple_of_five_certificate(target)
                self.assertIsNotNone(cert)
                self.assertEqual(cert.target, target)
                self.assertTrue(cert.valid())

        for target in ((0, 1), (5, 2), (6, 1), (1, 0), (2, 1)):
            self.assertIsNone(unit_coordinate_multiple_of_five_certificate(target))

    def test_affine_consecutive_hypotenuse_family(self):
        for m in range(2, 16):
            odd_leg = 2 * m - 1
            even_leg = 2 * m * (m - 1)
            hypotenuse = m * m + (m - 1) * (m - 1)
            for q in range(-60, 61):
                for t in range(-20, 21):
                    cert = affine_consecutive_hypotenuse_certificate(m, q, t)
                    if q == 0 or t == 0 or (q * (1 - q)) % even_leg != 0:
                        self.assertIsNone(cert)
                        continue

                    parameter_a = m * (m - 1) * t
                    parameter_b = odd_leg * parameter_a - q
                    coefficient = (
                        q * (1 - q) // even_leg
                        + odd_leg * q * t
                        - 2 * parameter_a * parameter_a
                    )
                    if coefficient == 0 or parameter_b == 0 or abs(parameter_b) == abs(parameter_a):
                        self.assertIsNone(cert)
                        continue

                    self.assertIsNotNone(cert)
                    self.assertEqual(
                        cert.target,
                        (
                            hypotenuse * q * t
                            + odd_leg * q * (1 - q) // even_leg,
                            q,
                        ),
                    )
                    self.assertEqual(
                        cert.midpoint,
                        (odd_leg * coefficient, even_leg * coefficient),
                    )
                    self.assertTrue(cert.valid())

        with self.assertRaises(ValueError):
            affine_consecutive_hypotenuse_certificate(1, 1, 1)

    def test_affine_consecutive_hypotenuse_target_solver(self):
        for m in range(2, 12):
            odd_leg = 2 * m - 1
            even_leg = 2 * m * (m - 1)
            hypotenuse = m * m + (m - 1) * (m - 1)
            for q in range(-30, 31):
                for g in range(-500, 501):
                    target = (g, q)
                    cert = affine_consecutive_hypotenuse_target_certificate(target, m)

                    expected = None
                    if q != 0 and (q * (1 - q)) % even_leg == 0:
                        offset = odd_leg * q * (1 - q) // even_leg
                        denominator = hypotenuse * q
                        if (g - offset) % denominator == 0:
                            expected = affine_consecutive_hypotenuse_certificate(
                                m,
                                q,
                                (g - offset) // denominator,
                            )

                    self.assertEqual(cert, expected)
                    if cert is not None:
                        self.assertEqual(cert.target, target)
                        self.assertTrue(cert.valid())

                    orbit_cert = affine_consecutive_hypotenuse_orbit_certificate(target, m)
                    swapped_expected = affine_consecutive_hypotenuse_target_certificate(
                        (q, g),
                        m,
                    )
                    if expected is None and swapped_expected is None:
                        self.assertIsNone(orbit_cert)
                    else:
                        self.assertIsNotNone(orbit_cert)
                        self.assertEqual(orbit_cert.target, target)
                        self.assertTrue(orbit_cert.valid())

        with self.assertRaises(ValueError):
            affine_consecutive_hypotenuse_target_certificate((5, 1), 1)
        with self.assertRaises(ValueError):
            affine_consecutive_hypotenuse_orbit_certificate((5, 1), 1)

    def test_unit_coordinate_consecutive_hypotenuse_family(self):
        for m in range(2, 30):
            hypotenuse = m * m + (m - 1) * (m - 1)
            for t in range(-25, 26):
                if t == 0:
                    self.assertIsNone(consecutive_hypotenuse_unit_coordinate_certificate(m, t))
                    continue

                base = consecutive_hypotenuse_unit_coordinate_certificate(m, t)
                self.assertIsNotNone(base)
                coefficient = (2 * m - 1) * t - 2 * (m * (m - 1) * t) ** 2
                self.assertEqual(base.target, (hypotenuse * t, 1))
                self.assertEqual(
                    base.midpoint,
                    (
                        (2 * m - 1) * coefficient,
                        2 * m * (m - 1) * coefficient,
                    ),
                )
                self.assertTrue(base.valid())

                for target in (
                    (hypotenuse * t, 1),
                    (hypotenuse * t, -1),
                    (1, hypotenuse * t),
                    (-1, hypotenuse * t),
                ):
                    cert = unit_coordinate_consecutive_hypotenuse_certificate(target, m)
                    self.assertIsNotNone(cert)
                    self.assertEqual(cert.target, target)
                    self.assertTrue(cert.valid())

        with self.assertRaises(ValueError):
            consecutive_hypotenuse_unit_coordinate_certificate(1, 1)
        with self.assertRaises(ValueError):
            unit_coordinate_consecutive_hypotenuse_certificate((5, 1), 1)

    def test_paper_theorem3_signed_certificate_examples(self):
        triple_4_3_5 = PythagoreanTriple(4, 3, 5)
        cert = theorem3_certificate((1, 1), triple_4_3_5, x_sign=1, y_sign=-1)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.midpoint, (4, -3))
        self.assertTrue(cert.valid())

        cert = theorem3_certificate((3, 2), triple_4_3_5, x_sign=1, y_sign=-1)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.midpoint, (24, -18))
        self.assertTrue(cert.valid())

        triple_3_4_5 = PythagoreanTriple(3, 4, 5)
        cert = theorem3_certificate((1, 3), triple_3_4_5, x_sign=1, y_sign=-1)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.midpoint, (9, -12))
        self.assertTrue(cert.valid())

        cert = theorem3_certificate((1, 9), triple_3_4_5, x_sign=-1, y_sign=-1)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.midpoint, (-27, -36))
        self.assertTrue(cert.valid())

        triple_8_15_17 = PythagoreanTriple(8, 15, 17)
        cert = theorem3_certificate((1, 5), triple_8_15_17, x_sign=1, y_sign=-1)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.midpoint, (40, -75))
        self.assertTrue(cert.valid())

        large_g = 3_037_000_499
        large_target = (large_g, 2 * large_g + 1)
        cert = theorem3_certificate(large_target, triple_3_4_5, x_sign=1, y_sign=-1)
        self.assertIsNotNone(cert)
        coefficient = large_target[0] * large_target[1]
        self.assertEqual(cert.midpoint, (3 * coefficient, -4 * coefficient))
        self.assertGreater(abs(cert.midpoint[0]), (1 << 63) - 1)
        self.assertTrue(cert.valid())

    def test_theorem3_divisor_generalization(self):
        examples = (
            ((1, 10), PythagoreanTriple(3, 4, 5), -1, -1, 2),
            ((1, 12), PythagoreanTriple(3, 4, 5), -1, -1, 4),
            ((3, 33), PythagoreanTriple(3, 4, 5), -1, -1, 9),
            ((2, 5), PythagoreanTriple(3, 4, 5), 1, -1, 1),
            ((5, 3), PythagoreanTriple(4, 3, 5), 1, -1, 1),
        )
        for target, triple, x_sign, y_sign, divisor in examples:
            certificate = theorem3_divisor_certificate(
                target,
                triple,
                x_sign,
                y_sign,
                divisor,
            )
            self.assertIsNotNone(certificate, target)
            self.assertEqual(certificate.target, target)
            self.assertTrue(certificate.valid())

            g, h = target
            coefficient = g * h // divisor
            self.assertGreater(coefficient, 0)
            self.assertEqual(
                certificate.midpoint,
                (
                    x_sign * triple.leg_a * coefficient,
                    y_sign * triple.leg_b * coefficient,
                ),
            )
            self.assertEqual(
                (triple.hypotenuse - x_sign * triple.leg_a) * g,
                (triple.hypotenuse + y_sign * triple.leg_b) * h - divisor,
            )
            self.assertEqual(
                certificate,
                linear_delta_direction_certificate(
                    target,
                    (x_sign * triple.leg_a, y_sign * triple.leg_b),
                    (1, -1),
                ),
            )

        large_target = (3_000_000_000, 24_000_000_006)
        large_divisor = 6
        large_certificate = theorem3_divisor_certificate(
            large_target,
            PythagoreanTriple(3, 4, 5),
            -1,
            -1,
            large_divisor,
        )
        self.assertIsNotNone(large_certificate)
        large_coefficient = large_target[0] * large_target[1] // large_divisor
        self.assertEqual(large_certificate.midpoint, (-3 * large_coefficient, -4 * large_coefficient))
        self.assertGreater(abs(large_certificate.midpoint[0]), (1 << 63) - 1)
        self.assertTrue(large_certificate.valid())

        self.assertEqual(
            theorem3_divisor_certificate((2, 5), PythagoreanTriple(3, 4, 5), 1, -1, 1),
            theorem3_certificate((2, 5), PythagoreanTriple(3, 4, 5), 1, -1),
        )
        self.assertIsNone(
            theorem3_divisor_certificate((1, 10), PythagoreanTriple(3, 4, 5), -1, -1, 3)
        )
        self.assertIsNone(
            theorem3_divisor_certificate((1, 10), PythagoreanTriple(3, 4, 5), 1, -1, 2)
        )
        with self.assertRaises(ValueError):
            theorem3_divisor_certificate((1, 10), PythagoreanTriple(3, 4, 5), -1, -1, 0)
        with self.assertRaises(ValueError):
            theorem3_divisor_certificate((1, 10), PythagoreanTriple(1, 1, 2), -1, -1, 2)
        with self.assertRaises(ValueError):
            theorem3_divisor_certificate((1, 10), PythagoreanTriple(3, 4, 5), 0, -1, 2)

    def test_theorem3_ray_divisor_family(self):
        examples = (
            ((3, 1), 1, PythagoreanTriple(5, 12, 13), 1, 1),
            ((3, 1), 17, PythagoreanTriple(5, 12, 13), 1, 1),
            ((2, 1), 3, PythagoreanTriple(12, 5, 13), 1, -1),
            ((2, 1), 29, PythagoreanTriple(15, 112, 113), 1, 1),
            ((1, 2), 5, PythagoreanTriple(3, 4, 5), -1, 1),
        )
        for ray, multiplier, triple, x_sign, y_sign in examples:
            certificate = theorem3_ray_divisor_certificate(
                ray,
                multiplier,
                triple,
                x_sign,
                y_sign,
            )
            self.assertIsNotNone(certificate, (ray, multiplier))
            self.assertEqual(
                certificate.target,
                (ray[0] * multiplier, ray[1] * multiplier),
            )
            self.assertTrue(certificate.valid())

        self.assertIsNone(
            theorem3_ray_divisor_certificate(
                (2, 1),
                1,
                PythagoreanTriple(3, 4, 5),
                1,
                -1,
            )
        )
        self.assertIsNone(
            theorem3_ray_divisor_certificate(
                (2, 1),
                2,
                PythagoreanTriple(3, 4, 5),
                1,
                -1,
            )
        )
        self.assertIsNone(
            theorem3_ray_divisor_certificate((0, 1), 3, PythagoreanTriple(3, 4, 5), 1, -1)
        )
        self.assertIsNone(
            theorem3_ray_divisor_certificate((2, 1), 0, PythagoreanTriple(3, 4, 5), 1, -1)
        )
        with self.assertRaises(ValueError):
            theorem3_ray_divisor_certificate((2, 1), 3, PythagoreanTriple(1, 1, 2), 1, -1)
        with self.assertRaises(ValueError):
            theorem3_ray_divisor_certificate((2, 1), 3, PythagoreanTriple(3, 4, 5), 0, -1)

    def test_theorem3_ray_divisor_modulus(self):
        triple_5_12_13 = PythagoreanTriple(5, 12, 13)
        self.assertEqual(theorem3_ray_divisor((3, 1), triple_5_12_13, 1, 1), 1)
        self.assertEqual(theorem3_ray_divisor_modulus((3, 1), triple_5_12_13, 1, 1), 1)

        triple_12_5_13 = PythagoreanTriple(12, 5, 13)
        self.assertEqual(theorem3_ray_divisor((2, 1), triple_12_5_13, 1, -1), 6)
        self.assertEqual(theorem3_ray_divisor_modulus((2, 1), triple_12_5_13, 1, -1), 3)
        self.assertIsNotNone(
            theorem3_ray_divisor_certificate((2, 1), 3, triple_12_5_13, 1, -1)
        )
        self.assertIsNone(
            theorem3_ray_divisor_certificate((2, 1), 1, triple_12_5_13, 1, -1)
        )

        triple_3_4_5 = PythagoreanTriple(3, 4, 5)
        self.assertEqual(theorem3_ray_divisor((1, 2), triple_3_4_5, -1, 1), 10)
        self.assertEqual(theorem3_ray_divisor_modulus((1, 2), triple_3_4_5, -1, 1), 5)
        self.assertIsNone(theorem3_ray_divisor_modulus((0, 1), triple_3_4_5, 1, -1))

    def test_theorem3_unit_divisor_progression_family(self):
        rows = (
            (PythagoreanTriple(3, 4, 5), 1, -1, (1, 3)),
            (PythagoreanTriple(5, 12, 13), 1, 1, (3, 1)),
            (PythagoreanTriple(8, 15, 17), -1, 1, (23, 18)),
        )

        for triple, x_sign, y_sign, base_ray in rows:
            a, b, c = triple.leg_a, triple.leg_b, triple.hypotenuse
            p_step = c + y_sign * b
            q_step = c - x_sign * a
            for parameter in (0, 1, 7):
                ray = theorem3_unit_divisor_progression_ray(
                    triple,
                    x_sign,
                    y_sign,
                    base_ray,
                    parameter,
                )
                self.assertEqual(
                    ray,
                    (
                        base_ray[0] + p_step * parameter,
                        base_ray[1] + q_step * parameter,
                    ),
                )
                self.assertEqual(theorem3_ray_divisor(ray, triple, x_sign, y_sign), 1)

                for multiplier in (1, 2, 101):
                    certificate = theorem3_unit_divisor_progression_certificate(
                        triple,
                        x_sign,
                        y_sign,
                        base_ray,
                        parameter,
                        multiplier,
                    )
                    self.assertEqual(
                        certificate,
                        theorem3_ray_divisor_certificate(
                            ray,
                            multiplier,
                            triple,
                            x_sign,
                            y_sign,
                        ),
                    )
                    self.assertIsNotNone(certificate)
                    self.assertEqual(
                        certificate.target,
                        (ray[0] * multiplier, ray[1] * multiplier),
                    )
                    self.assertTrue(certificate.valid())
                    self.assertEqual(
                        theorem3_unit_divisor_progression_parameters_for_base(
                            ray[0] * multiplier,
                            ray[1] * multiplier,
                            triple,
                            x_sign,
                            y_sign,
                            base_ray,
                        ),
                        (parameter, multiplier),
                    )

                    orbit_target = (-ray[1] * multiplier, ray[0] * multiplier)
                    orbit_certificate = theorem3_unit_divisor_progression_orbit_certificate(
                        orbit_target,
                        triple,
                        x_sign,
                        y_sign,
                        base_ray,
                    )
                    self.assertIsNotNone(orbit_certificate)
                    self.assertEqual(orbit_certificate.target, orbit_target)
                    self.assertTrue(orbit_certificate.valid())

        self.assertEqual(
            theorem3_unit_divisor_progression_certificate(
                PythagoreanTriple(8, 15, 17),
                1,
                -1,
                (1, 5),
                3,
                17,
            ),
            eight_fifteen_seventeen_unit_divisor_ray_certificate(
                "two_nine",
                3,
                17,
            ),
        )
        self.assertIsNone(
            theorem3_unit_divisor_progression_ray(
                PythagoreanTriple(3, 4, 5),
                1,
                -1,
                (1, 3),
                -1,
            )
        )
        self.assertIsNone(
            theorem3_unit_divisor_progression_ray(
                PythagoreanTriple(3, 4, 5),
                1,
                -1,
                (2, 1),
                0,
            )
        )
        self.assertIsNone(
            theorem3_unit_divisor_progression_parameters_for_base(
                2,
                1,
                PythagoreanTriple(3, 4, 5),
                1,
                -1,
                (1, 3),
            )
        )
        with self.assertRaises(ValueError):
            theorem3_unit_divisor_progression_ray(
                PythagoreanTriple(3, 4, 5),
                0,
                -1,
                (1, 3),
                0,
            )

    def test_theorem3_coprime_unit_divisor_progression_family(self):
        triples = (
            PythagoreanTriple(3, 4, 5),
            PythagoreanTriple(5, 12, 13),
            PythagoreanTriple(7, 24, 25),
            PythagoreanTriple(20, 21, 29),
        )

        for triple in triples:
            self.assertEqual(gcd(triple.leg_a, triple.leg_b), 1)
            for x_sign in (-1, 1):
                for y_sign in (-1, 1):
                    q_step, p_step = theorem3_unit_divisor_step_coefficients(
                        triple,
                        x_sign,
                        y_sign,
                    )
                    self.assertEqual(gcd(q_step, p_step), 1)
                    seed = theorem3_coprime_unit_divisor_seed(
                        triple,
                        x_sign,
                        y_sign,
                    )
                    self.assertIsNotNone(seed, (triple, x_sign, y_sign))
                    self.assertEqual(
                        theorem3_ray_divisor(seed, triple, x_sign, y_sign),
                        1,
                    )

                    for parameter in (0, 1, 4):
                        ray = theorem3_coprime_unit_divisor_progression_ray(
                            triple,
                            x_sign,
                            y_sign,
                            parameter,
                        )
                        self.assertEqual(
                            ray,
                            (
                                seed[0] + p_step * parameter,
                                seed[1] + q_step * parameter,
                            ),
                        )
                        self.assertEqual(
                            theorem3_ray_divisor(ray, triple, x_sign, y_sign),
                            1,
                        )
                        for multiplier in (1, 3, 77):
                            certificate = (
                                theorem3_coprime_unit_divisor_progression_certificate(
                                    triple,
                                    x_sign,
                                    y_sign,
                                    parameter,
                                    multiplier,
                                )
                            )
                            self.assertIsNotNone(certificate)
                            self.assertEqual(
                                certificate.target,
                                (ray[0] * multiplier, ray[1] * multiplier),
                            )
                            self.assertTrue(certificate.valid())

                            orbit_target = (
                                ray[1] * multiplier,
                                -ray[0] * multiplier,
                            )
                            orbit_certificate = (
                                theorem3_coprime_unit_divisor_progression_orbit_certificate(
                                    orbit_target,
                                    triple,
                                    x_sign,
                                    y_sign,
                                )
                            )
                            self.assertIsNotNone(orbit_certificate)
                            self.assertEqual(orbit_certificate.target, orbit_target)
                            self.assertTrue(orbit_certificate.valid())

        self.assertEqual(
            theorem3_coprime_unit_divisor_seed(PythagoreanTriple(3, 4, 5), 1, -1),
            (1, 3),
        )
        self.assertEqual(
            theorem3_coprime_unit_divisor_seed(PythagoreanTriple(8, 15, 17), -1, 1),
            (23, 18),
        )
        self.assertEqual(
            theorem3_coprime_unit_divisor_progression_certificate(
                PythagoreanTriple(8, 15, 17),
                1,
                -1,
                3,
                17,
            ),
            eight_fifteen_seventeen_unit_divisor_ray_certificate(
                "two_nine",
                3,
                17,
            ),
        )
        self.assertIsNone(
            theorem3_coprime_unit_divisor_seed(PythagoreanTriple(6, 8, 10), 1, -1)
        )
        with self.assertRaises(ValueError):
            theorem3_coprime_unit_divisor_seed(PythagoreanTriple(3, 4, 5), 0, -1)
        with self.assertRaises(ValueError):
            theorem3_coprime_unit_divisor_seed(PythagoreanTriple(1, 1, 2), 1, -1)

    def test_theorem3_ray_pell_divisor_family(self):
        certificate = theorem3_ray_pell_divisor_certificate((1, 3), 1, 1, 1)
        self.assertIsNotNone(certificate)
        self.assertEqual(certificate.target, (1, 3))
        self.assertEqual(certificate.midpoint, (9, -12))
        self.assertTrue(certificate.valid())

        unswapped_triple = PythagoreanTriple(3, 4, 5)
        self.assertEqual(theorem3_ray_divisor((1, 3), unswapped_triple, 1, -1), 1)

        swapped_certificate = theorem3_ray_pell_divisor_certificate(
            (2, 1),
            3,
            1,
            2,
            swap_legs=True,
        )
        self.assertIsNotNone(swapped_certificate)
        self.assertEqual(swapped_certificate.target, (6, 3))
        self.assertEqual(swapped_certificate.midpoint, (12, -5))
        self.assertTrue(swapped_certificate.valid())

        swapped_triple = PythagoreanTriple(12, 5, 13)
        self.assertEqual(theorem3_ray_divisor((2, 1), swapped_triple, 1, -1), 6)
        with self.assertRaises(ValueError):
            theorem3_ray_pell_divisor_certificate((1, 3), 1, 0, 1)

    def test_one_three_ray_theorem3_family(self):
        triple = PythagoreanTriple(3, 4, 5)
        self.assertEqual(theorem3_ray_divisor((1, 3), triple, 1, -1), 1)
        self.assertEqual(theorem3_ray_divisor_modulus((1, 3), triple, 1, -1), 1)

        for multiplier in (1, 2, 5, 17, 3003):
            cert = one_three_ray_theorem3_certificate(multiplier)
            self.assertIsNotNone(cert, multiplier)
            self.assertEqual(cert.target, (multiplier, 3 * multiplier))
            self.assertEqual(cert.midpoint, (9 * multiplier, -12 * multiplier))
            self.assertTrue(cert.valid())
            self.assertEqual(
                cert,
                theorem3_ray_divisor_certificate((1, 3), multiplier, triple, 1, -1),
            )

        for multiplier in (-1, 0):
            self.assertIsNone(one_three_ray_theorem3_certificate(multiplier))

        for target in (
            (1, 3),
            (-1, 3),
            (1, -3),
            (3, 1),
            (-3, 1),
            (3, -1),
            (17, -51),
            (-51, -17),
        ):
            orbit_cert = one_three_ray_theorem3_orbit_certificate(target)
            self.assertIsNotNone(orbit_cert, target)
            self.assertEqual(orbit_cert.target, target)
            self.assertTrue(orbit_cert.valid())

        for target in ((2, 1), (1, 2), (0, 3), (3, 0)):
            self.assertIsNone(one_three_ray_theorem3_orbit_certificate(target))

    def test_three_four_five_odd_slope_ray_family(self):
        triple = PythagoreanTriple(3, 4, 5)

        for ray_parameter in (1, 2, 5, 17):
            ray = (ray_parameter, 2 * ray_parameter + 1)
            self.assertEqual(theorem3_ray_divisor(ray, triple, 1, -1), 1)
            self.assertEqual(theorem3_ray_divisor_modulus(ray, triple, 1, -1), 1)

            for multiplier in (1, 2, 11, 3003):
                cert = three_four_five_odd_slope_ray_certificate(
                    ray_parameter,
                    multiplier,
                )
                self.assertIsNotNone(cert, (ray_parameter, multiplier))
                product = ray_parameter * (2 * ray_parameter + 1) * multiplier
                self.assertEqual(
                    cert.target,
                    (ray_parameter * multiplier, (2 * ray_parameter + 1) * multiplier),
                )
                self.assertEqual(cert.midpoint, (3 * product, -4 * product))
                self.assertTrue(cert.valid())
                self.assertEqual(
                    cert,
                    theorem3_ray_divisor_certificate(ray, multiplier, triple, 1, -1),
                )

        for ray_parameter, multiplier in ((0, 1), (-1, 1), (1, 0), (1, -1)):
            self.assertIsNone(
                three_four_five_odd_slope_ray_certificate(
                    ray_parameter,
                    multiplier,
                )
            )

        for target in (
            (1, 3),
            (-1, 3),
            (1, -3),
            (3, 1),
            (-3, 1),
            (3, -1),
            (4, 10),
            (-10, -4),
            (55, -25),
            (-35, 15),
        ):
            orbit_cert = three_four_five_odd_slope_ray_orbit_certificate(target)
            self.assertIsNotNone(orbit_cert, target)
            self.assertEqual(orbit_cert.target, target)
            self.assertTrue(orbit_cert.valid())

        for target in ((2, 1), (1, 2), (3, 10), (2, 7), (0, 3), (3, 0)):
            self.assertIsNone(
                three_four_five_odd_slope_ray_orbit_certificate(target)
            )

    def test_three_four_five_unit_divisor_ray_table(self):
        triple = PythagoreanTriple(3, 4, 5)
        families = {
            "odd_slope": ((1, 2, 9), 1, -1),
            "steep_odd_slope": ((1, 2, 7), -1, -1),
            "wide_odd_slope": ((0, 1, 6), 1, 1),
            "near_diagonal": ((0, 1, 5), -1, 1),
        }

        for family, (parameters, x_sign, y_sign) in families.items():
            for parameter in parameters:
                data = three_four_five_unit_divisor_ray_data(family, parameter)
                self.assertIsNotNone(data, (family, parameter))
                ray, row_x_sign, row_y_sign = data
                self.assertEqual((row_x_sign, row_y_sign), (x_sign, y_sign))
                self.assertEqual(
                    theorem3_ray_divisor(ray, triple, x_sign, y_sign),
                    1,
                    (family, parameter),
                )
                self.assertEqual(
                    theorem3_ray_divisor_modulus(ray, triple, x_sign, y_sign),
                    1,
                    (family, parameter),
                )

                for multiplier in (1, 2, 13, 3003):
                    cert = three_four_five_unit_divisor_ray_certificate(
                        family,
                        parameter,
                        multiplier,
                    )
                    self.assertIsNotNone(cert, (family, parameter, multiplier))
                    product = ray[0] * ray[1] * multiplier
                    self.assertEqual(
                        cert.target,
                        (ray[0] * multiplier, ray[1] * multiplier),
                    )
                    self.assertEqual(
                        cert.midpoint,
                        (x_sign * 3 * product, y_sign * 4 * product),
                    )
                    self.assertTrue(cert.valid())
                    self.assertEqual(
                        cert,
                        theorem3_ray_divisor_certificate(
                            ray,
                            multiplier,
                            triple,
                            x_sign,
                            y_sign,
                        ),
                    )

        self.assertIsNone(
            three_four_five_unit_divisor_ray_certificate("odd_slope", 0, 1)
        )
        self.assertIsNone(
            three_four_five_unit_divisor_ray_certificate("wide_odd_slope", -1, 1)
        )
        self.assertIsNone(
            three_four_five_unit_divisor_ray_certificate("near_diagonal", 0, 0)
        )
        with self.assertRaises(ValueError):
            three_four_five_unit_divisor_ray_data("missing", 1)

        for target in (
            (1, 3),
            (3, 1),
            (2, 17),
            (-17, -2),
            (4, 1),
            (-4, 1),
            (26, -6),
            (10, 9),
            (-45, 50),
            (116, -26),
            (55, -25),
        ):
            orbit_cert = three_four_five_unit_divisor_ray_orbit_certificate(target)
            self.assertIsNotNone(orbit_cert, target)
            self.assertEqual(orbit_cert.target, target)
            self.assertTrue(orbit_cert.valid())

        for target in ((2, 1), (1, 2), (3, 10), (2, 7), (11, 10), (0, 3), (3, 0)):
            self.assertIsNone(
                three_four_five_unit_divisor_ray_orbit_certificate(target)
            )

    def test_five_twelve_thirteen_unit_divisor_ray_table(self):
        triple = PythagoreanTriple(5, 12, 13)
        families = {
            "eight_slope": ((1, 2, 9), 1, -1),
            "eighteen_slope": ((1, 2, 5), -1, -1),
            "twentyfive_eight": ((0, 1, 6), 1, 1),
            "twentyfive_eighteen": ((0, 1, 4), -1, 1),
        }

        for family, (parameters, x_sign, y_sign) in families.items():
            for parameter in parameters:
                data = five_twelve_thirteen_unit_divisor_ray_data(family, parameter)
                self.assertIsNotNone(data, (family, parameter))
                ray, row_x_sign, row_y_sign = data
                self.assertEqual((row_x_sign, row_y_sign), (x_sign, y_sign))
                self.assertEqual(
                    theorem3_ray_divisor(ray, triple, x_sign, y_sign),
                    1,
                    (family, parameter),
                )
                self.assertEqual(
                    theorem3_ray_divisor_modulus(ray, triple, x_sign, y_sign),
                    1,
                    (family, parameter),
                )

                for multiplier in (1, 2, 17, 3003):
                    cert = five_twelve_thirteen_unit_divisor_ray_certificate(
                        family,
                        parameter,
                        multiplier,
                    )
                    self.assertIsNotNone(cert, (family, parameter, multiplier))
                    product = ray[0] * ray[1] * multiplier
                    self.assertEqual(
                        cert.target,
                        (ray[0] * multiplier, ray[1] * multiplier),
                    )
                    self.assertEqual(
                        cert.midpoint,
                        (x_sign * 5 * product, y_sign * 12 * product),
                    )
                    self.assertTrue(cert.valid())
                    self.assertEqual(
                        cert,
                        theorem3_ray_divisor_certificate(
                            ray,
                            multiplier,
                            triple,
                            x_sign,
                            y_sign,
                        ),
                    )

        self.assertIsNone(
            five_twelve_thirteen_unit_divisor_ray_certificate("eight_slope", 0, 1)
        )
        self.assertIsNone(
            five_twelve_thirteen_unit_divisor_ray_certificate(
                "twentyfive_eight",
                -1,
                1,
            )
        )
        self.assertIsNone(
            five_twelve_thirteen_unit_divisor_ray_certificate(
                "twentyfive_eighteen",
                0,
                0,
            )
        )
        with self.assertRaises(ValueError):
            five_twelve_thirteen_unit_divisor_ray_data("missing", 1)

        for target in (
            (1, 9),
            (9, 1),
            (2, 17),
            (1, 19),
            (-19, -1),
            (3, 1),
            (-28, 9),
            (56, -18),
            (18, 13),
            (13, 18),
            (86, -62),
        ):
            orbit_cert = five_twelve_thirteen_unit_divisor_ray_orbit_certificate(
                target
            )
            self.assertIsNotNone(orbit_cert, target)
            self.assertEqual(orbit_cert.target, target)
            self.assertTrue(orbit_cert.valid())

        for target in ((2, 1), (1, 2), (3, 10), (2, 7), (11, 10), (1, 18), (0, 9)):
            self.assertIsNone(
                five_twelve_thirteen_unit_divisor_ray_orbit_certificate(target)
            )

    def test_eight_fifteen_seventeen_unit_divisor_ray_table(self):
        triple = PythagoreanTriple(8, 15, 17)
        families = {
            "two_nine": ((0, 1, 8), 1, -1),
            "two_twentyfive": ((0, 1, 5), -1, -1),
            "thirtytwo_nine": ((0, 1, 3), 1, 1),
            "thirtytwo_twentyfive": ((0, 1, 4), -1, 1),
        }

        for family, (parameters, x_sign, y_sign) in families.items():
            for parameter in parameters:
                data = eight_fifteen_seventeen_unit_divisor_ray_data(
                    family,
                    parameter,
                )
                self.assertIsNotNone(data, (family, parameter))
                ray, row_x_sign, row_y_sign = data
                self.assertEqual((row_x_sign, row_y_sign), (x_sign, y_sign))
                self.assertEqual(
                    theorem3_ray_divisor(ray, triple, x_sign, y_sign),
                    1,
                    (family, parameter),
                )
                self.assertEqual(
                    theorem3_ray_divisor_modulus(ray, triple, x_sign, y_sign),
                    1,
                    (family, parameter),
                )

                for multiplier in (1, 2, 17, 3003):
                    cert = eight_fifteen_seventeen_unit_divisor_ray_certificate(
                        family,
                        parameter,
                        multiplier,
                    )
                    self.assertIsNotNone(cert, (family, parameter, multiplier))
                    product = ray[0] * ray[1] * multiplier
                    self.assertEqual(
                        cert.target,
                        (ray[0] * multiplier, ray[1] * multiplier),
                    )
                    self.assertEqual(
                        cert.midpoint,
                        (x_sign * 8 * product, y_sign * 15 * product),
                    )
                    self.assertTrue(cert.valid())
                    self.assertEqual(
                        cert,
                        theorem3_ray_divisor_certificate(
                            ray,
                            multiplier,
                            triple,
                            x_sign,
                            y_sign,
                        ),
                    )

        self.assertIsNone(
            eight_fifteen_seventeen_unit_divisor_ray_certificate("two_nine", -1, 1)
        )
        self.assertIsNone(
            eight_fifteen_seventeen_unit_divisor_ray_certificate(
                "thirtytwo_nine",
                0,
                0,
            )
        )
        with self.assertRaises(ValueError):
            eight_fifteen_seventeen_unit_divisor_ray_data("missing", 1)

        for target in (
            (1, 5),
            (5, 1),
            (2, 10),
            (1, 13),
            (-13, -1),
            (7, 2),
            (-14, -4),
            (39, 11),
            (11, 39),
            (23, 18),
            (110, -86),
        ):
            orbit_cert = eight_fifteen_seventeen_unit_divisor_ray_orbit_certificate(
                target
            )
            self.assertIsNotNone(orbit_cert, target)
            self.assertEqual(orbit_cert.target, target)
            self.assertTrue(orbit_cert.valid())

        for target in ((2, 1), (1, 2), (3, 10), (1, 9), (11, 10), (0, 5)):
            self.assertIsNone(
                eight_fifteen_seventeen_unit_divisor_ray_orbit_certificate(target)
            )

    def test_consecutive_euclid_unit_divisor_ray_family(self):
        for euclid_parameter in (1, 2, 3, 7):
            triple = PythagoreanTriple(
                2 * euclid_parameter + 1,
                2 * euclid_parameter * (euclid_parameter + 1),
                2 * euclid_parameter * euclid_parameter + 2 * euclid_parameter + 1,
            )
            self.assertTrue(triple.valid())
            for ray_parameter in (1, 2, 11):
                ray = (
                    ray_parameter,
                    2 * euclid_parameter * euclid_parameter * ray_parameter + 1,
                )
                self.assertEqual(theorem3_ray_divisor(ray, triple, 1, -1), 1)
                self.assertEqual(
                    theorem3_ray_divisor_modulus(ray, triple, 1, -1),
                    1,
                )

                for multiplier in (1, 2, 19, 3003):
                    cert = consecutive_euclid_unit_divisor_ray_certificate(
                        euclid_parameter,
                        ray_parameter,
                        multiplier,
                    )
                    self.assertIsNotNone(
                        cert,
                        (euclid_parameter, ray_parameter, multiplier),
                    )
                    product = ray[0] * ray[1] * multiplier
                    self.assertEqual(
                        cert.target,
                        (ray[0] * multiplier, ray[1] * multiplier),
                    )
                    self.assertEqual(
                        cert.midpoint,
                        (
                            (2 * euclid_parameter + 1) * product,
                            -2
                            * euclid_parameter
                            * (euclid_parameter + 1)
                            * product,
                        ),
                    )
                    self.assertTrue(cert.valid())
                    self.assertEqual(
                        cert,
                        theorem3_ray_divisor_certificate(
                            ray,
                            multiplier,
                            triple,
                            1,
                            -1,
                        ),
                    )

        for args in ((0, 1, 1), (1, 0, 1), (1, 1, 0)):
            self.assertIsNone(consecutive_euclid_unit_divisor_ray_certificate(*args))

        for target in (
            (1, 3),
            (2, 17),
            (1, 19),
            (3, 151),
            (-151, -3),
            (37, -2),
            (3, 295),
            (295, 3),
        ):
            orbit_cert = consecutive_euclid_unit_divisor_ray_orbit_certificate(
                target
            )
            self.assertIsNotNone(orbit_cert, target)
            self.assertEqual(orbit_cert.target, target)
            self.assertTrue(orbit_cert.valid())

        for target in ((2, 1), (1, 2), (3, 10), (2, 7), (1, 18), (0, 3)):
            self.assertIsNone(
                consecutive_euclid_unit_divisor_ray_orbit_certificate(target)
            )

    def test_consecutive_euclid_affine_strip_family(self):
        for euclid_parameter in (1, 2, 3, 7):
            triple = PythagoreanTriple(
                2 * euclid_parameter * (euclid_parameter + 1),
                2 * euclid_parameter + 1,
                2 * euclid_parameter * euclid_parameter + 2 * euclid_parameter + 1,
            )
            self.assertTrue(triple.valid())

            for free_coordinate in (1, 2, 11, 3003):
                target = (
                    2 * euclid_parameter * euclid_parameter * free_coordinate - 1,
                    free_coordinate,
                )
                cert = consecutive_euclid_affine_strip_certificate(
                    euclid_parameter,
                    free_coordinate,
                )
                self.assertIsNotNone(cert, (euclid_parameter, free_coordinate))
                coefficient = target[0] * target[1]
                self.assertEqual(cert.target, target)
                self.assertEqual(
                    cert.midpoint,
                    (
                        2
                        * euclid_parameter
                        * (euclid_parameter + 1)
                        * coefficient,
                        -(2 * euclid_parameter + 1) * coefficient,
                    ),
                )
                self.assertTrue(cert.valid())
                self.assertEqual(
                    cert,
                    theorem3_certificate(target, triple, 1, -1),
                )
                self.assertEqual(
                    cert,
                    theorem3_quadratic_strip_certificate(target, euclid_parameter),
                )

                for orbit_target in sign_swap_orbit(target):
                    orbit_cert = consecutive_euclid_affine_strip_orbit_certificate(
                        orbit_target,
                        euclid_parameter,
                    )
                    self.assertIsNotNone(orbit_cert, orbit_target)
                    self.assertEqual(orbit_cert.target, orbit_target)
                    self.assertTrue(orbit_cert.valid())

        for args in ((0, 1), (1, 0), (1, -1)):
            self.assertIsNone(consecutive_euclid_affine_strip_certificate(*args))
        with self.assertRaises(ValueError):
            consecutive_euclid_affine_strip_orbit_certificate((1, 1), 0)

        self.assertIsNone(consecutive_euclid_affine_strip_orbit_certificate((1, 3), 1))
        self.assertIsNone(consecutive_euclid_affine_strip_orbit_certificate((2, 1), 1))
        self.assertIsNone(consecutive_euclid_affine_strip_orbit_certificate((3, 10), 2))

    def test_paper_theorem3_line_constructor(self):
        triples = (
            PythagoreanTriple(4, 3, 5),
            PythagoreanTriple(3, 4, 5),
            PythagoreanTriple(8, 15, 17),
            PythagoreanTriple(5, 12, 13),
        )
        for triple in triples:
            a, b, c = triple.leg_a, triple.leg_b, triple.hypotenuse
            for x_sign in (-1, 1):
                for y_sign in (-1, 1):
                    denominator = c - x_sign * a
                    for h in range(-60, 61):
                        cert = theorem3_line_certificate(triple, x_sign, y_sign, h)
                        if h == 0:
                            self.assertIsNone(cert)
                            continue

                        numerator = (c + y_sign * b) * h - 1
                        if numerator % denominator != 0:
                            self.assertIsNone(cert)
                            continue

                        g = numerator // denominator
                        if g == 0:
                            self.assertIsNone(cert)
                            continue

                        expected = theorem3_certificate((g, h), triple, x_sign, y_sign)
                        self.assertEqual(cert, expected)
                        self.assertIsNotNone(cert)
                        self.assertEqual(cert.target, (g, h))
                        self.assertTrue(cert.valid())

        self.assertEqual(
            theorem3_line_certificate(PythagoreanTriple(4, 3, 5), 1, -1, 2),
            theorem3_certificate((3, 2), PythagoreanTriple(4, 3, 5), 1, -1),
        )
        self.assertIsNone(theorem3_line_certificate(PythagoreanTriple(4, 3, 5), 1, -1, 0))
        with self.assertRaises(ValueError):
            theorem3_line_certificate(PythagoreanTriple(1, 1, 2), 1, -1, 1)
        with self.assertRaises(ValueError):
            theorem3_line_certificate(PythagoreanTriple(3, 4, 5), 0, -1, 1)

    def test_theorem3_quadratic_strip_family(self):
        for parameter_n in range(1, 10):
            hypotenuse = 2 * parameter_n * parameter_n + 2 * parameter_n + 1
            first_triple = PythagoreanTriple(
                2 * parameter_n * (parameter_n + 1),
                2 * parameter_n + 1,
                hypotenuse,
            )
            second_triple = PythagoreanTriple(
                2 * parameter_n + 1,
                2 * parameter_n * (parameter_n + 1),
                hypotenuse,
            )
            self.assertTrue(first_triple.valid())
            self.assertTrue(second_triple.valid())

            for h in range(-20, 21):
                if h == 0:
                    continue
                target = (2 * h * parameter_n * parameter_n - 1, h)
                cert = theorem3_quadratic_strip_certificate(target, parameter_n)
                self.assertEqual(
                    cert,
                    theorem3_certificate(target, first_triple, 1, -1),
                )
                self.assertIsNotNone(cert)
                self.assertTrue(cert.valid())

                for orbit_target in sign_swap_orbit(target):
                    orbit_cert = theorem3_quadratic_strip_orbit_certificate(
                        orbit_target,
                        parameter_n,
                    )
                    self.assertIsNotNone(orbit_cert)
                    self.assertEqual(orbit_cert.target, orbit_target)
                    self.assertTrue(orbit_cert.valid())

            for g in range(-20, 21):
                if g == 0:
                    continue
                target = (g, 2 * g * parameter_n * parameter_n + 1)
                cert = theorem3_quadratic_strip_certificate(target, parameter_n)
                self.assertEqual(
                    cert,
                    theorem3_certificate(target, second_triple, 1, -1),
                )
                self.assertIsNotNone(cert)
                self.assertTrue(cert.valid())

                for orbit_target in sign_swap_orbit(target):
                    orbit_cert = theorem3_quadratic_strip_orbit_certificate(
                        orbit_target,
                        parameter_n,
                    )
                    self.assertIsNotNone(orbit_cert)
                    self.assertEqual(orbit_cert.target, orbit_target)
                    self.assertTrue(orbit_cert.valid())

        self.assertIsNone(theorem3_quadratic_strip_certificate((2, 1), 1))
        self.assertIsNone(theorem3_quadratic_strip_orbit_certificate((2, 1), 1))
        with self.assertRaises(ValueError):
            theorem3_quadratic_strip_certificate((1, 1), 0)
        with self.assertRaises(ValueError):
            theorem3_quadratic_strip_orbit_certificate((1, 1), 0)

    def test_paper_theorem3_rejects_non_matching_relations(self):
        triples = [PythagoreanTriple(3, 4, 5), PythagoreanTriple(4, 3, 5)]
        self.assertEqual(theorem3_certificates((2, 1), triples), ())

    def test_small_horizontal_axis_certificates(self):
        expected = {
            3: (-7, 24),
            4: (-5, 12),
            5: (-22, 120),
            6: (3, 4),
            7: (-9, 12),
            8: (4, 3),
            9: (-6, 8),
            10: (5, 12),
            11: (-5, 12),
            12: (6, 8),
            13: (-32, 24),
            14: (5, 12),
            15: (-90, 56),
            16: (8, 6),
            17: (7, 24),
            18: (9, 12),
            19: (-16, 12),
            20: (10, 24),
        }
        table = horizontal_axis_certificate_table(3, 20, bound=2000)
        self.assertEqual(table, expected)
        for n, midpoint in table.items():
            self.assertTrue(is_two_step_certificate((n, 0), midpoint))

    def test_axis_certificate_artifact_validates(self):
        artifact = ARTIFACT_DIR / "horizontal_axis_certificates.json"
        data = json.loads(artifact.read_text())
        certificates = {
            int(row["n"]): tuple(row["midpoint"])
            for row in data["certificates"]
        }

        self.assertEqual(set(certificates), set(range(3, 21)))
        for n, midpoint in certificates.items():
            self.assertTrue(is_two_step_certificate((n, 0), midpoint))


class AxisFamilyTests(unittest.TestCase):
    def test_every_integer_from_three_has_a_pythagorean_leg_completion(self):
        for leg in range(3, 201):
            partner_leg, hypotenuse = pythagorean_leg_completion(leg)
            self.assertGreater(partner_leg, 0)
            self.assertEqual(leg * leg + partner_leg * partner_leg, hypotenuse * hypotenuse)

    def test_midpoint_formula_covers_even_axis_points_from_six(self):
        for n in range(6, 402, 2):
            cert = midpoint_axis_certificate(n)
            self.assertIsNotNone(cert)
            self.assertEqual(cert.target, (n, 0))
            self.assertEqual(cert.midpoint[0], n // 2)
            self.assertTrue(cert.valid())

        for n in (3, 4, 5):
            self.assertIsNone(midpoint_axis_certificate(n))

    def test_explicit_axis_certificate_covers_four(self):
        cert = explicit_axis_certificate(4)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.target, (4, 0))
        self.assertEqual(cert.midpoint, (-5, 12))
        self.assertTrue(cert.valid())

        for n in (1, 2, 3, 5, 6):
            self.assertIsNone(explicit_axis_certificate(n))

    def test_consecutive_parameter_formula_covers_odd_axis_points(self):
        for n in range(3, 402, 2):
            record = consecutive_parameter_odd_axis_certificate(n)
            self.assertIsNotNone(record)

            first_horizontal = (n - 1) * (2 * n + 1) // 2
            second_horizontal = (n + 1) * (2 * n - 1) // 2
            shared_leg = n * (n * n - 1)

            self.assertEqual(record.target_n, n)
            self.assertEqual(record.midpoint, (-first_horizontal, shared_leg))
            self.assertEqual(record.first_horizontal_leg, first_horizontal)
            self.assertEqual(record.second_horizontal_leg, second_horizontal)
            self.assertEqual(
                record.first_hypotenuse,
                (n - 1) * (2 * n * n + 2 * n + 1) // 2,
            )
            self.assertEqual(
                record.second_hypotenuse,
                (n + 1) * (2 * n * n - 2 * n + 1) // 2,
            )
            self.assertEqual(second_horizontal - first_horizontal, n)
            self.assertTrue(record.valid())

        for n in (1, 2, 4, 6):
            self.assertIsNone(consecutive_parameter_odd_axis_certificate(n))

    def test_horizontal_axis_proof_certificate_case_split(self):
        for n in range(3, 502):
            cert = horizontal_axis_proof_certificate(n)
            self.assertIsNotNone(cert)
            self.assertEqual(cert.target, (n, 0))
            self.assertTrue(cert.valid())

        for n in (1, 2):
            self.assertIsNone(horizontal_axis_proof_certificate(n))

    def test_axis_orbit_proof_certificate(self):
        for n in range(3, 302):
            base = horizontal_axis_proof_certificate(n)
            self.assertIsNotNone(base)

            for target in ((n, 0), (-n, 0), (0, n), (0, -n)):
                cert = axis_orbit_proof_certificate(target)
                self.assertIsNotNone(cert)
                self.assertEqual(cert.target, target)
                self.assertTrue(cert.valid())

            positive_vertical = axis_orbit_proof_certificate((0, n))
            self.assertEqual(
                positive_vertical.midpoint,
                (base.midpoint[1], base.midpoint[0]),
            )

            negative_horizontal = axis_orbit_proof_certificate((-n, 0))
            self.assertEqual(
                negative_horizontal.midpoint,
                (-base.midpoint[0], base.midpoint[1]),
            )

        for target in (
            (0, 0),
            (1, 0),
            (2, 0),
            (0, 1),
            (0, 2),
            (1, 1),
            (2, 1),
        ):
            self.assertIsNone(axis_orbit_proof_certificate(target))

    def test_shared_leg_generator_records_are_valid(self):
        records = shared_leg_axis_certificate_records(m_limit=12, scale_limit=6, n_max=80)
        self.assertTrue(records)

        for record in records:
            self.assertIn(record.relation, {"difference", "sum"})
            self.assertTrue(record.valid())

        covered = {record.target_n for record in records}
        for n in (3, 4, 5, 7, 9, 11, 17, 25, 35):
            self.assertIn(n, covered)

    def test_shared_leg_generator_bounded_odd_axis_coverage(self):
        table = shared_leg_axis_certificate_table(m_limit=30, scale_limit=10, n_max=200)
        missing_odd = [n for n in range(3, 201, 2) if n not in table]

        self.assertEqual(missing_odd, [])
        for n in range(3, 201, 2):
            self.assertTrue(table[n].valid())

    def test_euclid_parameter_difference_family(self):
        for m in range(2, 50):
            for t in range(1, 20):
                record = euclid_parameter_difference_certificate(m, t)
                self.assertEqual(record.target_n, t * (m * m + m * t + 1))
                self.assertTrue(record.valid())

        first_targets = [
            euclid_parameter_difference_certificate(m, 1).target_n
            for m in range(2, 8)
        ]
        self.assertEqual(first_targets, [7, 13, 21, 31, 43, 57])

    def test_residue_witnesses_for_odd_classes_mod_24(self):
        residues = odd_residues(24)

        euclid_records = [
            euclid_parameter_difference_certificate(m, t)
            for m in range(2, 81)
            for t in range(1, 81)
        ]
        euclid_witnesses = residue_witnesses(euclid_records, 24, residues)
        self.assertEqual(set(euclid_witnesses), set(residues))

        shared_leg_records = shared_leg_axis_certificate_records(
            m_limit=30,
            scale_limit=10,
            n_max=200,
        )
        self.assertEqual(missing_residues(shared_leg_records, 24, residues), ())

        for residue, record in residue_witnesses(shared_leg_records, 24, residues).items():
            self.assertEqual(record.target_n % 24, residue)
            self.assertTrue(record.valid())


class FalsificationTests(unittest.TestCase):
    def test_known_distance_three_examples_have_no_small_two_step_certificate(self):
        # This is bounded falsification, not a proof. The paper gives exact
        # arguments for these three obstructions.
        for target in KNOWN_DISTANCE_THREE_REPRESENTATIVES:
            self.assertIsNone(find_two_step_certificate(target, bound=200))

    def test_bad_hypothesis_all_axis_points_need_three_steps_after_two_is_false(self):
        self.assertEqual(find_two_step_certificate((3, 0), bound=50), (-7, 24))

    def test_bounded_search_result_labels_are_not_proofs(self):
        found = bounded_two_step_search((3, 0), bound=50)
        self.assertEqual(found.status, "found")
        self.assertEqual(found.certificate, (-7, 24))

        not_found = bounded_two_step_search((1, 0), bound=50)
        self.assertEqual(not_found.status, "not_found_within_bound")
        self.assertFalse(not_found.found)


if __name__ == "__main__":
    unittest.main()

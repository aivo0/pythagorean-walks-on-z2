import json
from math import gcd, isqrt
from pathlib import Path
import unittest

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
    ParallelDirectionFactorWitness,
    SMALL_PRIME_DETERMINANT_DIRECTION_PAIRS,
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
    consecutive_leg_pythagorean_triple,
    consecutive_leg_swap_lattice_certificate,
    consecutive_parameter_odd_axis_certificate,
    consecutive_hypotenuse_unit_coordinate_certificate,
    diagonal_pythagorean_multiplier_certificate,
    determinant,
    determinant_seven_lattice_certificate,
    determinant_seventeen_lattice_certificate,
    determinant_thirteen_lattice_certificate,
    delta_slice_certificate,
    edge,
    euclid_strip_certificate,
    euclid_parameter_difference_certificate,
    explicit_axis_certificate,
    first_gaussian_divisor_certificate,
    find_two_step_certificate,
    four_three_factor_five_parallel_certificate,
    gaussian_divisor_certificate,
    gaussian_multiply,
    gaussian_quotient_if_integer,
    gaussian_transform_certificate,
    half_leg_strip_orbit_certificate,
    half_leg_strip_certificate,
    half_leg_strip_target_certificate,
    half_leg_unit_coordinate_certificate,
    half_leg_unit_coordinate_orbit_certificate,
    half_leg_unit_coordinate_target_certificate,
    all_prime_factors_one_or_nine_mod_ten,
    has_divisor_in_residue_classes,
    has_divisor_three_or_seven_mod_ten,
    has_two_one_ray_mod_130_divisor,
    has_two_one_ray_mod_2210_divisor,
    horizontal_axis_certificate_table,
    horizontal_axis_proof_certificate,
    is_prime,
    is_square,
    is_two_step_certificate,
    integer_slope_consecutive_ray_certificate,
    lattice_coefficients,
    lattice_two_step_certificate,
    linear_delta_direction_certificate,
    missing_residues,
    minimal_periodic_residue_classes,
    midpoint_axis_certificate,
    odd_residues,
    path_is_valid,
    parallel_direction_certificate,
    parallel_direction_bounded_factor_cover_certificate,
    parallel_direction_cover_certificate,
    parallel_direction_factor_coefficient,
    parallel_direction_factor_certificate,
    parallel_direction_factor_certificate_residue_classes,
    parallel_direction_factor_modulus,
    parallel_direction_factor_residue_certificate,
    parallel_direction_factor_residue_classes,
    parallel_direction_factor_witness,
    parallel_direction_standard_completion_cover_certificate,
    parallel_direction_standard_completion_certificate,
    periodic_residue_union,
    positive_divisors,
    possible_integer_distance_differences,
    prime_factors,
    primitive_pythagorean_directions,
    pythagorean_leg_completion,
    pythagorean_triple_orthogonal_lattice_certificate,
    prime_determinant_lattice_certificate,
    rational_slope_consecutive_ray_certificate,
    ray_multiplier,
    ray_parallel_factor_certificate,
    ray_parallel_factor_residues,
    residue_witnesses,
    scale_certificate,
    same_projective_class_mod,
    shared_leg_axis_certificate_records,
    shared_leg_axis_certificate_table,
    sign_swap_certificate,
    sign_swap_orbit,
    signed_delta_values,
    signed_swap_point,
    small_prime_lattice_certificate,
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
    two_one_ray_consecutive_certificate,
    two_one_ray_consecutive_orbit_certificate,
    two_one_ray_even_certificate,
    two_one_ray_even_orbit_certificate,
    two_one_ray_explicit_base_certificate,
    two_one_ray_explicit_base_orbit_certificate,
    two_one_ray_five_or_seventeen_mod_twenty_certificate,
    two_one_ray_five_or_seventeen_mod_twenty_orbit_certificate,
    two_one_ray_finite_audit_certificate,
    two_one_ray_finite_audit_orbit_certificate,
    two_one_ray_mod20_skeleton_certificate,
    two_one_ray_mod20_skeleton_orbit_certificate,
    two_one_ray_mod20_skeleton_residues,
    two_one_ray_mod260_skeleton_certificate,
    two_one_ray_mod260_skeleton_orbit_certificate,
    two_one_ray_mod260_skeleton_residues,
    two_one_ray_mod_2210_divisor_residues,
    two_one_ray_complement_divisor_certificate,
    two_one_ray_complement_divisor_period,
    two_one_ray_complement_divisor_residues,
    two_one_ray_complement_divisor_sieve_certificate,
    two_one_ray_complement_divisor_sieve_residue_classes,
    two_one_ray_mod_130_divisor_residues,
    two_one_ray_mod_ten_divisor_certificate,
    two_one_ray_mod_ten_divisor_orbit_certificate,
    two_one_ray_mod_thirty_four_divisor_certificate,
    two_one_ray_mod_thirty_four_divisor_orbit_certificate,
    two_one_ray_mod_twenty_six_divisor_certificate,
    two_one_ray_mod_twenty_six_divisor_orbit_certificate,
    two_one_ray_three_mod_four_certificate,
    two_one_ray_three_mod_four_orbit_certificate,
    unit_coordinate_500_audit_certificate,
    unit_coordinate_500_residual_certificate,
    unit_coordinate_consecutive_hypotenuse_certificate,
    unit_coordinate_factor_five_parallel_certificate,
    unit_coordinate_factor_five_parallel_orbit_certificate,
    unit_coordinate_parallel_factor_orbit_certificate,
    unit_coordinate_parallel_factor_residues,
    unit_coordinate_multiple_of_five_certificate,
    known_distance_three_obstruction_cases,
    y_squared_minus_y_plus_one_is_square,
)


ARTIFACT_DIR = Path(__file__).resolve().parents[1] / "data"


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
        self.assertIn((3, 4, 5, 2, 1), directions)
        self.assertIn((-4, 3, 5, 2, 1), directions)
        self.assertIn((5, 12, 13, 3, 2), directions)

        for u, v, hypotenuse, parameter_a, parameter_b in directions:
            self.assertGreater(parameter_a, parameter_b)
            self.assertEqual(u * u + v * v, hypotenuse * hypotenuse)
            self.assertNotEqual(u, 0)
            self.assertNotEqual(v, 0)

        self.assertEqual(signed_delta_values(3), (0, 1, -1, 2, -2, 3, -3))
        with self.assertRaises(ValueError):
            primitive_pythagorean_directions(1)
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
        cert = lattice_two_step_certificate((7, 0), (3, 4), (4, 3))
        self.assertIsNotNone(cert)
        self.assertEqual(cert.midpoint, (-9, -12))
        self.assertTrue(cert.valid())

        self.assertEqual(lattice_coefficients((1, 1), (3, -4), (4, -3)), (-1, 1))
        cert = lattice_two_step_certificate((1, 1), (3, -4), (4, -3))
        self.assertIsNotNone(cert)
        self.assertEqual(cert.midpoint, (-3, 4))
        self.assertTrue(cert.valid())

        self.assertIsNone(lattice_coefficients((1, 0), (3, 4), (4, 3)))
        with self.assertRaises(ValueError):
            lattice_two_step_certificate((1, 1), (1, 1), (4, 3))

    def test_parallel_direction_divisor_reduction(self):
        self.assertEqual(positive_divisors(36), (1, 2, 3, 4, 6, 9, 12, 18, 36))
        with self.assertRaises(ValueError):
            positive_divisors(0)

        self.assertEqual(parallel_direction_factor_modulus((3, 4), 648), 32400)
        self.assertEqual(parallel_direction_factor_coefficient((39, 64), (3, 4), 648), 2)
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

        certificate = parallel_direction_factor_certificate((39, 64), (3, 4), 648)
        self.assertIsNotNone(certificate)
        self.assertEqual(certificate.midpoint, (6, 8))
        self.assertTrue(certificate.valid())

        searched = parallel_direction_certificate((39, 64), (3, 4))
        self.assertIsNotNone(searched)
        self.assertEqual(searched.target, (39, 64))
        self.assertTrue(searched.valid())

        certificate = parallel_direction_factor_certificate((6, 101), (3, 4), 27)
        self.assertIsNotNone(certificate)
        self.assertEqual(certificate.midpoint, (222, 296))
        self.assertTrue(certificate.valid())

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

        self.assertIsNone(parallel_direction_factor_certificate((39, 64), (3, 4), 5))
        self.assertIsNone(parallel_direction_certificate((6, 8), (3, 4)))
        with self.assertRaises(ValueError):
            parallel_direction_factor_certificate((39, 64), (1, 1), 1)
        with self.assertRaises(ValueError):
            parallel_direction_factor_certificate((39, 64), (3, 4), 0)
        with self.assertRaises(ValueError):
            parallel_direction_factor_modulus((1, 1), 1)
        with self.assertRaises(ValueError):
            parallel_direction_factor_coefficient((39, 64), (3, 4), 0)

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
            certificate = parallel_direction_standard_completion_certificate(
                target,
                direction,
            )
            self.assertIsNotNone(certificate, (target, direction))
            self.assertEqual(certificate.midpoint, midpoint)
            self.assertTrue(certificate.valid())

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

        with self.assertRaises(ValueError):
            parallel_direction_standard_completion_cover_certificate((1, 5), 1)

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
        certificate = unit_coordinate_parallel_factor_orbit_certificate(
            (1, 92),
            (-3, -4),
            4,
        )
        self.assertIsNotNone(certificate)
        self.assertEqual(certificate.midpoint, (-1065, -1420))
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

        for g in range(-75, 76):
            for h in range(-75, 76):
                target = (g, h)
                expected = (
                    parallel_direction_factor_coefficient(target, direction, factor)
                    is not None
                )
                self.assertEqual(
                    (target[0] % modulus, target[1] % modulus) in residues,
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

    def test_box_five_hundred_finite_audit(self):
        self.assertEqual(BOX_FIVE_HUNDRED_RESIDUAL_CERTIFICATES, {})
        self.assertIsNone(box_five_hundred_residual_certificate((500, 1)))

        for g in range(-500, 501):
            for h in range(-500, 501):
                target = (g, h)
                certificate = box_five_hundred_audit_certificate(target)

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

        self.assertIsNone(box_five_hundred_audit_certificate((501, 1)))

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
                expected = half_leg_strip_certificate(direction, 1, t)
                self.assertEqual(cert, expected)
                self.assertIsNotNone(cert)
                self.assertEqual(cert.target, (expected_x, 1))
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
        )
        modulus, residues = two_one_ray_complement_divisor_sieve_residue_classes(
            directions
        )
        expected_residues = tuple(
            residue
            for residue in range(2210)
            if (
                residue % 10 in (3, 7)
                or residue % 26 in (3, 7, 19, 23)
                or residue % 34 in (7, 13, 21, 27)
            )
        )
        self.assertEqual(modulus, 2210)
        self.assertEqual(residues, expected_residues)
        self.assertEqual(two_one_ray_mod_2210_divisor_residues(), expected_residues)
        self.assertEqual(len(two_one_ray_mod_2210_divisor_residues()), 754)

        for n in range(1, 2000):
            expected = any(
                divisor % 10 in (3, 7)
                or divisor % 26 in (3, 7, 19, 23)
                or divisor % 34 in (7, 13, 21, 27)
                for divisor in positive_divisors(n)
            )
            self.assertEqual(has_two_one_ray_mod_2210_divisor(n), expected, n)
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
                self.assertEqual(base.target, (hypotenuse * t, 1))
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

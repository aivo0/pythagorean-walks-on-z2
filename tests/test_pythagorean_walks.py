import json
from pathlib import Path
import unittest

from experiments.pythagorean_walks import (
    Certificate,
    EXPLICIT_TWO_ONE_RAY_BASE_CERTIFICATES,
    EXPLICIT_TWO_ONE_RAY_FINITE_AUDIT_CERTIFICATES,
    KNOWN_DISTANCE_THREE_ORBIT,
    KNOWN_DISTANCE_THREE_REPRESENTATIVES,
    PythagoreanTriple,
    SMALL_PRIME_DETERMINANT_DIRECTION_PAIRS,
    affine_consecutive_hypotenuse_certificate,
    bounded_two_step_search,
    canonical_known_distance_three_representative,
    consecutive_direction_strip_certificate,
    consecutive_parameter_odd_axis_certificate,
    consecutive_hypotenuse_unit_coordinate_certificate,
    diagonal_pythagorean_multiplier_certificate,
    determinant,
    determinant_seven_lattice_certificate,
    determinant_seventeen_lattice_certificate,
    determinant_thirteen_lattice_certificate,
    edge,
    euclid_strip_certificate,
    euclid_parameter_difference_certificate,
    explicit_axis_certificate,
    first_gaussian_divisor_certificate,
    find_two_step_certificate,
    gaussian_divisor_certificate,
    gaussian_multiply,
    gaussian_quotient_if_integer,
    gaussian_transform_certificate,
    half_leg_strip_certificate,
    horizontal_axis_certificate_table,
    horizontal_axis_proof_certificate,
    is_prime,
    is_square,
    is_two_step_certificate,
    lattice_coefficients,
    lattice_two_step_certificate,
    missing_residues,
    midpoint_axis_certificate,
    odd_residues,
    path_is_valid,
    possible_integer_distance_differences,
    pythagorean_leg_completion,
    prime_determinant_lattice_certificate,
    residue_witnesses,
    scale_certificate,
    same_projective_class_mod,
    shared_leg_axis_certificate_records,
    shared_leg_axis_certificate_table,
    sign_swap_orbit,
    small_prime_lattice_certificate,
    theorem1_three_step_path,
    theorem3_certificate,
    theorem3_certificates,
    two_one_ray_consecutive_certificate,
    two_one_ray_consecutive_orbit_certificate,
    two_one_ray_even_certificate,
    two_one_ray_even_orbit_certificate,
    two_one_ray_explicit_base_certificate,
    two_one_ray_explicit_base_orbit_certificate,
    two_one_ray_finite_audit_certificate,
    two_one_ray_finite_audit_orbit_certificate,
    unit_coordinate_consecutive_hypotenuse_certificate,
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
        slopes_by_modulus = {}
        for first_direction, second_direction in SMALL_PRIME_DETERMINANT_DIRECTION_PAIRS:
            modulus = abs(determinant(first_direction, second_direction))
            self.assertTrue(is_prime(modulus))
            self.assertIn(modulus, {23, 31, 37, 41, 43, 47})

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

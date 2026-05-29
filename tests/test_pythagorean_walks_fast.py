from math import isqrt

import pytest

from experiments import pythagorean_walks as py

fast = pytest.importorskip("pythagorean_walks_fast")


def test_fast_arithmetic_matches_python_reference():
    previous_fast = py._fast
    py._fast = None
    try:
        assert fast.signed_swap_point((2, -3), -1, 1) == py.signed_swap_point(
            (2, -3),
            -1,
            1,
        )
        assert fast.signed_swap_point((2, -3), -1, 1, True) == py.signed_swap_point(
            (2, -3),
            -1,
            1,
            True,
        )
        with pytest.raises(ValueError):
            fast.signed_swap_point((1, 2), 0, 1)

        for dx, dy in ((3, 4), (4, 3), (5, 0), (6, 8), (-7, 24), (12, -35)):
            assert fast.edge_delta(dx, dy) == py.edge_delta(dx, dy)

        examples = (
            ((20, 1), (-24, -32)),
            ((2, 29), (12, 5)),
            ((151, 338), (-369, 1640)),
        )
        for target, midpoint in examples:
            assert fast.certificate_valid(target, midpoint) == py.Certificate(
                target,
                midpoint,
            ).valid()

        for certificate, factor in (
            (py.Certificate((1, 1), (4, -3)), -10),
            (py.Certificate((1, 1), (4, -3)), -1),
            (py.Certificate((1, 1), (4, -3)), 17),
            (
                py.Certificate(
                    (3_037_000_499, -3_037_000_500),
                    (3_037_000_500, 3_037_000_499),
                ),
                -3_037_000_499,
            ),
        ):
            expected = py.scale_certificate(certificate, factor)
            assert fast.scale_certificate_data(
                certificate.target,
                certificate.midpoint,
                factor,
            ) == (expected.target, expected.midpoint)
        with pytest.raises(ValueError):
            fast.scale_certificate_data((1, 1), (4, -3), 0)

        for certificate, factor, x_sign, y_sign, swap in (
            (py.Certificate((1, 1), (4, -3)), 17, -1, 1, False),
            (py.Certificate((3, 2), (24, -18)), -11, 1, -1, True),
            (
                py.Certificate(
                    (3_037_000_499, -3_037_000_500),
                    (3_037_000_500, 3_037_000_499),
                ),
                3_037_000_499,
                -1,
                -1,
                True,
            ),
        ):
            expected = py.scale_signed_swap_certificate(
                certificate,
                factor,
                x_sign,
                y_sign,
                swap,
            )
            assert fast.scale_signed_swap_certificate_data(
                certificate.target,
                certificate.midpoint,
                factor,
                x_sign,
                y_sign,
                swap,
            ) == (expected.target, expected.midpoint)
        with pytest.raises(ValueError):
            fast.scale_signed_swap_certificate_data((1, 1), (4, -3), 0, 1, 1)
        with pytest.raises(ValueError):
            fast.scale_signed_swap_certificate_data((1, 1), (4, -3), 1, 0, 1)

        for n in (2, 3, 4, 6, 8, 10, 400, 18_000_000_000):
            expected = py.midpoint_axis_certificate(n)
            assert fast.even_axis_certificate_midpoint(n) == (
                None if expected is None else expected.midpoint
            )

        for n in (1, 2, 3, 5, 401, 3_037_000_499):
            expected = py.consecutive_parameter_odd_axis_certificate(n)
            assert fast.consecutive_odd_axis_certificate_data(n) == (
                None
                if expected is None
                else (
                    expected.target_n,
                    expected.midpoint[0],
                    expected.midpoint[1],
                    expected.shared_leg,
                    expected.first_horizontal_leg,
                    expected.second_horizontal_leg,
                    expected.first_hypotenuse,
                    expected.second_hypotenuse,
                )
            )

        for point, multiplier in (
            ((1, 1), (5, 12)),
            ((151, 338), (-4, -5)),
            ((3_037_000_499, 3_037_000_500), (3_037_000_500, -3_037_000_499)),
        ):
            assert fast.gaussian_multiply(point, multiplier) == py.gaussian_multiply(
                point,
                multiplier,
            )

        large_base = py.scale_certificate(
            py.Certificate((1, 1), (4, -3)),
            3_000_000_000,
        )
        for certificate, multiplier in (
            (py.Certificate((1, 1), (4, -3)), (5, 12)),
            (py.Certificate((1, 1), (4, -3)), (3, 4)),
            (py.Certificate((3, 2), (24, -18)), (-12, 5)),
            (large_base, (4_500_000_000, 6_000_000_000)),
        ):
            expected = py.gaussian_transform_certificate(certificate, multiplier)
            assert fast.gaussian_transform_certificate_data(
                certificate.target,
                certificate.midpoint,
                multiplier,
            ) == (None if expected is None else (expected.target, expected.midpoint))
        with pytest.raises(ValueError):
            fast.gaussian_transform_certificate_data((1, 1), (4, -3), (1, 1))
        with pytest.raises(ValueError):
            fast.gaussian_transform_certificate_data((1, 0), (1, 1), (1, 0))

        for target, divisor in (
            ((-7, 17), (1, 1)),
            ((-10, 20), (2, 4)),
            ((1, 2), (2, 4)),
            ((9_000_000_000_000_000_001, -9_000_000_000_000_000_000), (1, 0)),
        ):
            assert fast.gaussian_quotient_components(target, divisor) == (
                py.gaussian_quotient_components(target, divisor)
            )
            assert fast.gaussian_quotient_if_integer(target, divisor) == (
                py.gaussian_quotient_if_integer(target, divisor)
            )
        with pytest.raises(ValueError):
            fast.gaussian_quotient_components((1, 2), (0, 0))
        with pytest.raises(ValueError):
            fast.gaussian_quotient_if_integer((1, 2), (0, 0))

        for target, base_target, base_midpoint in (
            ((-7, 17), (1, 1), (4, -3)),
            ((-10, 20), (2, 4), (77, -36)),
            ((4, 6), (2, 4), (77, -36)),
            ((1, 2), (2, 4), (77, -36)),
        ):
            expected = py.gaussian_divisor_certificate(
                target,
                py.Certificate(base_target, base_midpoint),
            )
            assert fast.gaussian_divisor_certificate_midpoint(
                target,
                base_target,
                base_midpoint,
            ) == (None if expected is None else expected.midpoint)
        with pytest.raises(ValueError):
            fast.gaussian_divisor_certificate_midpoint((1, 1), (1, 0), (1, 1))

        diagonal_targets = tuple(
            py.gaussian_multiply((1, 1), multiplier)
            for multiplier in (
                (1, 0),
                (0, 1),
                (5, 12),
                (12, 5),
                (-7, 24),
                (20, -21),
                (3_037_000_499, 3_037_000_500),
            )
        ) + ((2, 1), (1, 2), (3, 5), (-1, 7), (7, 1))
        for target in diagonal_targets:
            expected = py.diagonal_pythagorean_multiplier_certificate(target)
            assert fast.diagonal_pythagorean_multiplier_midpoint(target) == (
                None if expected is None else expected.midpoint
            )

        for target, triple, x_sign, y_sign in (
            ((2, 5), py.PythagoreanTriple(3, 4, 5), 1, -1),
            ((1, 9), py.PythagoreanTriple(3, 4, 5), -1, -1),
            ((3_037_000_499, 6_074_000_999), py.PythagoreanTriple(3, 4, 5), 1, -1),
            ((2, 1), py.PythagoreanTriple(3, 4, 5), 1, -1),
            ((0, 5), py.PythagoreanTriple(3, 4, 5), 1, -1),
        ):
            expected = py.theorem3_certificate(target, triple, x_sign, y_sign)
            assert fast.theorem3_certificate_midpoint(
                target,
                (triple.leg_a, triple.leg_b, triple.hypotenuse),
                x_sign,
                y_sign,
            ) == (None if expected is None else expected.midpoint)
        with pytest.raises(ValueError):
            fast.theorem3_certificate_midpoint((1, 1), (1, 1, 2), 1, -1)
        with pytest.raises(ValueError):
            fast.theorem3_certificate_midpoint((1, 1), (3, 4, 5), 0, -1)

        for target, triple, x_sign, y_sign, divisor in (
            ((1, 10), py.PythagoreanTriple(3, 4, 5), -1, -1, 2),
            ((3, 33), py.PythagoreanTriple(3, 4, 5), -1, -1, 9),
            ((3_000_000_000, 24_000_000_006), py.PythagoreanTriple(3, 4, 5), -1, -1, 6),
            ((1, 10), py.PythagoreanTriple(3, 4, 5), -1, -1, 3),
            ((-3, -6), py.PythagoreanTriple(3, 4, 5), -1, -1, 18),
        ):
            expected = py.theorem3_divisor_certificate(
                target,
                triple,
                x_sign,
                y_sign,
                divisor,
            )
            assert fast.theorem3_divisor_certificate_midpoint(
                target,
                (triple.leg_a, triple.leg_b, triple.hypotenuse),
                x_sign,
                y_sign,
                divisor,
            ) == (None if expected is None else expected.midpoint)
        with pytest.raises(ValueError):
            fast.theorem3_divisor_certificate_midpoint((1, 10), (3, 4, 5), -1, -1, 0)
        with pytest.raises(ValueError):
            fast.theorem3_divisor_certificate_midpoint((1, 10), (1, 1, 2), -1, -1, 2)
        with pytest.raises(ValueError):
            fast.theorem3_divisor_certificate_midpoint((1, 10), (3, 4, 5), 0, -1, 2)

        for target, direction, delta_coefficients in (
            ((1, 1), (-3, 4), (0, 0)),
            ((2, 5), (3, -4), (1, -1)),
            ((3, 6), (-5, 12), (1, 0)),
            ((3_000_000_000_000_000_000, 3_000_000_000_000_000_000), (-3, 4), (0, 0)),
            ((2, 1), (3, 4), (0, 0)),
            ((1, 8), (3, 4), (1, -1)),
        ):
            expected = py.linear_delta_direction_certificate(
                target,
                direction,
                delta_coefficients,
            )
            assert fast.linear_delta_direction_midpoint(
                target,
                direction,
                delta_coefficients,
            ) == (None if expected is None else expected.midpoint)
        with pytest.raises(ValueError):
            fast.linear_delta_direction_midpoint((1, 1), (1, 1), (0, 0))

        base = py.Certificate(target=(3, 2), midpoint=(24, -18))
        for swap in (False, True):
            for x_sign in (-1, 1):
                for y_sign in (-1, 1):
                    target = py.signed_swap_point(base.target, x_sign, y_sign, swap)
                    expected = py.sign_swap_certificate(base, target)
                    assert expected is not None
                    assert fast.sign_swap_certificate_midpoint(
                        base.target,
                        base.midpoint,
                        target,
                    ) == expected.midpoint
        assert fast.sign_swap_certificate_midpoint(
            base.target,
            base.midpoint,
            (5, 5),
        ) is None
        with pytest.raises(AssertionError):
            fast.sign_swap_certificate_midpoint((1, 0), (1, 1), (1, 0))

        for target, first, second in (
            ((7, 0), (3, 4), (4, 3)),
            ((1, 1), (3, -4), (4, -3)),
            ((1, 0), (3, 4), (4, 3)),
            ((10, 10), (3, 4), (6, 8)),
        ):
            assert fast.lattice_coefficients(target, first, second) == (
                py.lattice_coefficients(target, first, second)
            )
            expected = py.lattice_two_step_certificate(target, first, second)
            assert fast.lattice_certificate_midpoint(target, first, second) == (
                None if expected is None else expected.midpoint
            )

        for target, first, second in (
            ((7, 0), (3, 4), (4, 3)),
            ((1, 1), (3, -4), (4, -3)),
            ((1, 0), (3, 4), (4, 3)),
        ):
            assert fast.lattice_coefficient_cramer_data(target, first, second) == (
                py.lattice_coefficient_cramer_data(target, first, second)
            )
        with pytest.raises(ValueError):
            fast.lattice_coefficient_cramer_data((10, 10), (3, 4), (6, 8))

        first = (3, 4)
        second = (4, 3)
        first_coefficient = 1_234_567_890_123
        second_coefficient = -987_654_321_011
        large_target = (
            first_coefficient * first[0] + second_coefficient * second[0],
            first_coefficient * first[1] + second_coefficient * second[1],
        )
        assert fast.lattice_coefficients(large_target, first, second) == (
            first_coefficient,
            second_coefficient,
        )
        assert fast.lattice_coefficients(large_target, first, second) == (
            py.lattice_coefficients(large_target, first, second)
        )
        assert fast.lattice_coefficient_cramer_data(large_target, first, second) == (
            py.lattice_coefficient_cramer_data(large_target, first, second)
        )
        expected = py.lattice_two_step_certificate(large_target, first, second)
        assert expected is not None
        assert fast.lattice_certificate_midpoint(large_target, first, second) == (
            expected.midpoint
        )
        with pytest.raises(ValueError):
            fast.lattice_certificate_midpoint((1, 1), (1, 1), (4, 3))

        for target, direction, factor in (
            ((39, 64), (3, 4), 648),
            ((39, 64), (3, 4), 5),
            ((6, 101), (3, 4), 27),
            ((1_000_006, -1_999_899), (3, 4), 1),
        ):
            assert fast.parallel_direction_factor_congruence_holds(
                target,
                direction,
                factor,
            ) == py.parallel_direction_factor_congruence_holds(
                target,
                direction,
                factor,
            )
            assert fast.parallel_direction_factor_congruence_data(
                target,
                direction,
                factor,
            ) == py.parallel_direction_factor_congruence_data(
                target,
                direction,
                factor,
            )

        with pytest.raises(ValueError):
            fast.parallel_direction_factor_congruence_holds((1, 1), (1, 1), 1)
        with pytest.raises(ValueError):
            fast.parallel_direction_factor_congruence_holds((1, 1), (3, 4), 0)
        with pytest.raises(ValueError):
            fast.parallel_direction_factor_congruence_data((1, 1), (1, 1), 1)
        with pytest.raises(ValueError):
            fast.parallel_direction_factor_congruence_data((1, 1), (3, 4), 0)

        for direction, factor in (
            ((3, 4), 1),
            ((4, 3), 5),
            ((-4, -3), 1),
            ((20, -21), 2),
        ):
            assert tuple(
                tuple(row)
                for row in fast.parallel_direction_primitive_factor_determinant_residue_rows(
                    direction,
                    factor,
                )
            ) == py.parallel_direction_primitive_factor_determinant_residue_rows(
                direction,
                factor,
            )
        with pytest.raises(ValueError):
            fast.parallel_direction_primitive_factor_determinant_residue_rows((1, 1), 1)
        with pytest.raises(ValueError):
            fast.parallel_direction_primitive_factor_determinant_residue_rows((6, 8), 1)
        with pytest.raises(ValueError):
            fast.parallel_direction_primitive_factor_determinant_residue_rows((3, 4), 0)

        modulus = py.parallel_direction_factor_modulus((3, 4), 27)
        shifted_target = (6 + 10_000_000 * modulus, 101 - 7_000_000 * modulus)
        large_shifted_target = (
            6 + 1_000_000_000_000_000 * modulus,
            101 - 1_000_000_000_000_000 * modulus,
        )
        for target, direction, factor in (
            ((39, 64), (3, 4), 648),
            ((39, 64), (3, 4), 5),
            ((6, 8), (3, 4), 1),
            ((6, 101), (3, 4), 27),
            (shifted_target, (3, 4), 27),
            (large_shifted_target, (3, 4), 27),
        ):
            expected = py.parallel_direction_factor_witness(target, direction, factor)
            congruence_data = fast.parallel_direction_factor_congruence_data(
                target,
                direction,
                factor,
            )
            assert congruence_data == py.parallel_direction_factor_congruence_data(
                target,
                direction,
                factor,
            )
            assert fast.parallel_direction_factor_pair_row_from_congruence_data(
                target,
                direction,
                factor,
            ) == py.parallel_direction_factor_pair_row_from_congruence_data(
                target,
                direction,
                factor,
            )
            assert fast.parallel_direction_factor_witness_data(
                target,
                direction,
                factor,
            ) == (
                None
                if expected is None
                else (
                    expected.determinant_leg,
                    expected.other_leg,
                    expected.scaled_hypotenuse,
                    expected.second_length,
                    expected.first_coefficient,
                )
            )

            expected_row = py.parallel_direction_factor_witness_row_data(
                target,
                direction,
                factor,
            )
            assert fast.parallel_direction_factor_witness_row_data(
                target,
                direction,
                factor,
            ) == expected_row
            if expected_row is not None:
                (
                    determinant_leg,
                    paired_factor,
                    other_leg,
                    scaled_hypotenuse,
                    second_length,
                    first_coefficient,
                ) = expected_row
                assert congruence_data == (
                    determinant_leg,
                    second_length,
                    first_coefficient,
                )
                u, v = direction
                c = isqrt(u * u + v * v)
                dot_product = target[0] * u + target[1] * v
                assert determinant_leg * determinant_leg == factor * paired_factor
                assert paired_factor - factor == 2 * other_leg
                assert factor + paired_factor == 2 * scaled_hypotenuse
                assert scaled_hypotenuse == c * second_length
                assert (
                    paired_factor - factor + 2 * dot_product
                    == 2 * first_coefficient * c * c
                )

        with pytest.raises(ValueError):
            fast.parallel_direction_factor_witness_data((1, 1), (1, 1), 1)
        with pytest.raises(ValueError):
            fast.parallel_direction_factor_witness_data((1, 1), (3, 4), 0)
        with pytest.raises(ValueError):
            fast.parallel_direction_factor_witness_row_data((1, 1), (1, 1), 1)
        with pytest.raises(ValueError):
            fast.parallel_direction_factor_witness_row_data((1, 1), (3, 4), 0)
        with pytest.raises(ValueError):
            fast.parallel_direction_factor_pair_row_from_congruence_data(
                (1, 1),
                (1, 1),
                1,
            )
        with pytest.raises(ValueError):
            fast.parallel_direction_factor_pair_row_from_congruence_data(
                (1, 1),
                (3, 4),
                0,
            )

        for args in (
            ((3, 4), 2, 1, (-4, -3), 1),
            ((-12, -5), 13, 7, (-4, -3), 1),
            ((4, 3), 10, 3, (3, 4), 8),
        ):
            assert fast.parallel_direction_factor_integrality_strip_intersection_residue_count(
                *args
            ) == py.parallel_direction_factor_integrality_strip_intersection_residue_count(
                *args
            )

        with pytest.raises(ValueError):
            fast.parallel_direction_factor_integrality_strip_intersection_residue_count(
                (1, 1),
                13,
                7,
                (-4, -3),
                1,
            )
        with pytest.raises(ValueError):
            fast.parallel_direction_factor_integrality_strip_intersection_residue_count(
                (3, 4),
                1,
                0,
                (-4, -3),
                1,
            )

        for args in (
            (3, 7, 7, 13),
            (18, 18, 30, 34),
            (4, 6, 5, 12),
            (4, 6, 8, 12),
            (0, 0, 0, 9),
            (0, 0, 4, 9),
            (0, 12, -18, 30),
            (-14, 21, -35, 28),
            (
                9_223_372_036_854_775_000,
                -9_223_372_036_854_774_998,
                14,
                42,
            ),
        ):
            assert fast.two_variable_linear_congruence_gcd(
                *args
            ) == py.two_variable_linear_congruence_gcd(*args)
        with pytest.raises(ValueError):
            fast.two_variable_linear_congruence_gcd(1, 2, 3, 0)

        for args in (
            (3, 7, 7, 13, 2, 5),
            (4, 6, 2, 8, 5, 12),
            (4, 6, 1, 4, 1, 6),
            (0, 0, 0, 4, 0, 6),
            (0, 0, 1, 4, 1, 6),
            (-14, 21, -35, 28, 7, 20),
            (
                9_223_372_036_854_775_000,
                -9_223_372_036_854_774_998,
                -35,
                28,
                7,
                20,
            ),
        ):
            actual = fast.two_variable_linear_congruence_pair_data(*args)
            expected = py.two_variable_linear_congruence_pair_data(*args)
            assert actual == expected
            combined_residue = actual[3]
            if combined_residue is not None:
                assert combined_residue % args[3] == args[2] % args[3]
                assert combined_residue % args[5] == args[4] % args[5]
                assert actual[-1] == (combined_residue % actual[2] == 0)
        with pytest.raises(ValueError):
            fast.two_variable_linear_congruence_pair_data(1, 2, 3, 0, 5, 7)
        with pytest.raises(ValueError):
            fast.two_variable_linear_congruence_pair_data(1, 2, 3, 5, 7, 0)

        for args in (
            ((-12, -5), 13, 7, 5, 2, (-4, -3), (-3, -4)),
            ((-12, -5), 10, 7, 15, 8, (-4, -3), (-3, -4)),
            ((-8, -15), 4, 1, 6, 1, (-4, 3), (-12, 5)),
            ((20, -21), 58, -11, 14, 3, (5, 12), (-8, 15)),
        ):
            actual = fast.pythagorean_lattice_pair_strip_crt_data(*args)
            expected = py.pythagorean_lattice_pair_strip_crt_data(*args)
            assert actual == expected
            assert actual[2:] == py.two_variable_linear_congruence_pair_data(
                actual[0],
                actual[1],
                args[2],
                args[1],
                args[4],
                args[3],
            )
            combined = fast.pythagorean_lattice_pair_same_strip_combined_linear_congruence(
                *args
            )
            assert combined == py.pythagorean_lattice_pair_same_strip_combined_linear_congruence(
                *args
            )
            if combined is None:
                assert not actual[6]
            else:
                assert actual[6]
                assert combined == (
                    actual[0] % actual[3],
                    actual[1] % actual[3],
                    actual[5],
                    actual[3],
                    actual[4],
                )
            assert fast.pythagorean_lattice_pair_same_strip_intersection_residue_count(
                *args
            ) == py.pythagorean_lattice_pair_same_strip_intersection_residue_count(
                *args
            )
        with pytest.raises(ValueError):
            fast.pythagorean_lattice_pair_strip_crt_data(
                (1, 1),
                13,
                7,
                5,
                2,
                (-4, -3),
                (-3, -4),
            )
        with pytest.raises(ValueError):
            fast.pythagorean_lattice_pair_same_strip_intersection_residue_count(
                (1, 1),
                13,
                7,
                5,
                2,
                (-4, -3),
                (-3, -4),
            )
        with pytest.raises(ValueError):
            fast.pythagorean_lattice_pair_same_strip_combined_linear_congruence(
                (1, 1),
                13,
                7,
                5,
                2,
                (-4, -3),
                (-3, -4),
            )
        with pytest.raises(ValueError):
            fast.pythagorean_lattice_pair_strip_crt_data(
                (-12, -5),
                1,
                7,
                5,
                2,
                (-4, -3),
                (-3, -4),
            )
        with pytest.raises(ValueError):
            fast.pythagorean_lattice_pair_same_strip_combined_linear_congruence(
                (-12, -5),
                1,
                7,
                5,
                2,
                (-4, -3),
                (-3, -4),
            )
        with pytest.raises(ValueError):
            fast.pythagorean_lattice_pair_same_strip_intersection_residue_count(
                (-12, -5),
                1,
                7,
                5,
                2,
                (-4, -3),
                (-3, -4),
            )

        for args in (
            ((-12, -5), 13, 7, (-4, -3), (-3, -4)),
            ((-8, -15), 34, 30, (-4, 3), (-12, 5)),
            ((20, -21), 58, -11, (5, 12), (-8, 15)),
        ):
            assert fast.pythagorean_lattice_pair_strip_linear_congruence(
                *args
            ) == py.pythagorean_lattice_pair_strip_linear_congruence(*args)
        with pytest.raises(ValueError):
            fast.pythagorean_lattice_pair_strip_linear_congruence(
                (1, 1),
                13,
                7,
                (-4, -3),
                (-3, -4),
            )
        with pytest.raises(ValueError):
            fast.pythagorean_lattice_pair_strip_linear_congruence(
                (-12, -5),
                1,
                7,
                (-4, -3),
                (-3, -4),
            )
        with pytest.raises(ValueError):
            fast.pythagorean_lattice_pair_strip_linear_congruence(
                (-12, -5),
                13,
                7,
                (1, 1),
                (-3, -4),
            )
        with pytest.raises(ValueError):
            fast.pythagorean_lattice_pair_strip_linear_congruence(
                (-12, -5),
                13,
                7,
                (-4, -3),
                (-8, -6),
            )

        for root in (
            (1, 4),
            (-4, -5),
            (2, 7),
            (1_234_567, 8_901_234),
            (3_037_000_499, 3_037_000_500),
        ):
            assert fast.gaussian_root_conjugate_divisibility_residue(root) == (
                py.gaussian_root_conjugate_divisibility_residue(root)
            )

        with pytest.raises(ValueError):
            fast.gaussian_root_conjugate_divisibility_residue((0, 3))
        with pytest.raises(ValueError):
            fast.gaussian_root_conjugate_divisibility_residue((2, 4))

        for n in (1, 12, 9801, 110161):
            assert tuple(fast.prime_factors(n)) == py.prime_factors(n)
            assert tuple(tuple(row) for row in fast.prime_power_factorization(n)) == (
                py.prime_power_factorization(n)
            )
            assert tuple(fast.positive_divisors(n)) == py.positive_divisors(n)
            assert tuple(fast.divisor_residue_classes(n, 130)) == (
                py.divisor_residue_classes(n, 130)
            )
    finally:
        py._fast = previous_fast


def test_fast_cover_kernels_match_python_reference():
    previous_fast = py._fast
    py._fast = None
    try:
        for target in ((2, 29), (39, 64), (151, 338)):
            expected = py.parallel_direction_cover_certificate(target, 8)
            midpoint = fast.parallel_direction_cover_midpoint(target, 8)
            assert (None if expected is None else expected.midpoint) == midpoint

        for target in ((2, 49), (10, 13), (50, 17)):
            expected = py.pythagorean_lattice_pair_witness(target, 25, 1435)
            row = fast.pythagorean_lattice_pair_witness(target, 25, 1435)
            assert row is not None
            assert expected is not None
            first, second, determinant, first_coefficient, second_coefficient = row
            assert expected.first_direction == first
            assert expected.second_direction == second
            assert expected.determinant == determinant
            assert expected.first_coefficient == first_coefficient
            assert expected.second_coefficient == second_coefficient

        assert tuple(fast.ray_parallel_factor_residues((2, 1), (3, -4), 1)) == (
            py.ray_parallel_factor_residues((2, 1), (3, -4), 1)
        )
    finally:
        py._fast = previous_fast

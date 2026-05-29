import pytest

from experiments import pythagorean_walks as py

fast = pytest.importorskip("pythagorean_walks_fast")


def test_fast_arithmetic_matches_python_reference():
    previous_fast = py._fast
    py._fast = None
    try:
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

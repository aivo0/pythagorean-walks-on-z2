"""Verification helpers for Pythagorean walks on Z^2.

The graph has an edge for a displacement (dx, dy) exactly when dx and dy are
both nonzero and dx^2 + dy^2 is a square.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import isqrt
from typing import Iterable


Point = tuple[int, int]

KNOWN_DISTANCE_THREE_REPRESENTATIVES: frozenset[Point] = frozenset({
    (1, 0),
    (2, 0),
    (2, 1),
})


def sign_swap_orbit(point: Point) -> frozenset[Point]:
    """Return all images of a point under sign changes and coordinate swap."""

    x, y = point
    orbit: set[Point] = set()
    for a, b in ((x, y), (y, x)):
        for sx in (-1, 1):
            for sy in (-1, 1):
                orbit.add((sx * a, sy * b))
    return frozenset(orbit)


def signed_swap_point(point: Point, x_sign: int, y_sign: int, swap: bool = False) -> Point:
    """Apply a sign-change and optional coordinate-swap graph automorphism."""

    if x_sign not in (-1, 1) or y_sign not in (-1, 1):
        raise ValueError("x_sign and y_sign must be -1 or 1")

    x, y = point
    if swap:
        x, y = y, x
    return (x_sign * x, y_sign * y)


KNOWN_DISTANCE_THREE_ORBIT: frozenset[Point] = frozenset(
    point
    for representative in KNOWN_DISTANCE_THREE_REPRESENTATIVES
    for point in sign_swap_orbit(representative)
)


def canonical_known_distance_three_representative(target: Point) -> Point | None:
    """Return the positive sign/swap representative for a known obstruction."""

    abs_x, abs_y = abs(target[0]), abs(target[1])
    representative = (max(abs_x, abs_y), min(abs_x, abs_y))
    if representative in KNOWN_DISTANCE_THREE_REPRESENTATIVES:
        return representative
    return None


def possible_integer_distance_differences(target: Point) -> tuple[int, ...]:
    """Integer values possible for ||OP| - |TP|| by the triangle inequality."""

    norm_squared = target[0] * target[0] + target[1] * target[1]
    return tuple(range(isqrt(norm_squared) + 1))


def y_squared_minus_y_plus_one_is_square(y: int) -> bool:
    """Exact lemma used in the paper's obstruction proof for (2, 1).

    The value y^2 - y + 1 is a square only for y = 0 or y = 1.  For y >= 2 it
    lies strictly between (y - 1)^2 and y^2; for y < 0, writing t = -y puts it
    strictly between t^2 and (t + 1)^2.
    """

    return y in (0, 1)


def known_distance_three_obstruction_cases(target: Point) -> tuple[str, ...]:
    """Return the exact no-two-step obstruction cases for a known representative.

    These are the symbolic cases from the paper's proof, normalized by sign
    changes and coordinate swap.  An empty tuple means the target is not one of
    the known obstruction classes.
    """

    representative = canonical_known_distance_three_representative(target)
    if representative == (1, 0):
        return (
            "delta=0: the perpendicular bisector has half-integral x-coordinate",
            "delta=1: equality in the triangle inequality forces an illegal axis edge",
        )
    if representative == (2, 0):
        return (
            "delta=0: the bisector line x=1 gives y^2+1 strictly between squares",
            "delta=1: the two candidate integer lengths would have opposite parity",
            "delta=2: equality in the triangle inequality forces an illegal axis edge",
        )
    if representative == (2, 1):
        return (
            "delta=0: the perpendicular bisector 4x+2y=5 has no integer point",
            "delta=1: the quadratic case reduces to y^2-y+1 being square",
            "delta=2: the two candidate integer lengths would have opposite parity",
        )
    return ()


def is_square(n: int) -> bool:
    if n < 0:
        return False
    root = isqrt(n)
    return root * root == n


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    factor = 3
    while factor * factor <= n:
        if n % factor == 0:
            return False
        factor += 2
    return True


def edge_delta(dx: int, dy: int) -> bool:
    return dx != 0 and dy != 0 and is_square(dx * dx + dy * dy)


def edge(a: Point, b: Point) -> bool:
    return edge_delta(b[0] - a[0], b[1] - a[1])


def path_is_valid(path: Iterable[Point]) -> bool:
    pts = list(path)
    return all(edge(a, b) for a, b in zip(pts, pts[1:]))


def theorem1_three_step_path(target: Point) -> tuple[Point, ...]:
    """Return the spanning path from the paper's diameter-three proof.

    The identity

        (g, h) = (3g + 4h)(3, 4)
              - (3g + 4h)(4, 3)
              + (g + h)(4, -3)

    writes every target as a sum of at most three scalar multiples of
    Pythagorean edge vectors.  Zero coefficients are omitted, so the returned
    path may have fewer than three edges.
    """

    g, h = target
    steps = (
        (3 * g + 4 * h, (3, 4)),
        (-(3 * g + 4 * h), (4, 3)),
        (g + h, (4, -3)),
    )

    current = (0, 0)
    path = [current]
    for coefficient, vector in steps:
        if coefficient == 0:
            continue
        current = (
            current[0] + coefficient * vector[0],
            current[1] + coefficient * vector[1],
        )
        path.append(current)

    if current != target:
        raise AssertionError("theorem 1 path identity failed")
    return tuple(path)


def is_two_step_certificate(target: Point, midpoint: Point) -> bool:
    return edge((0, 0), midpoint) and edge(midpoint, target)


def find_two_step_certificate(target: Point, bound: int) -> Point | None:
    """Search for a two-step certificate with |x|, |y| <= bound.

    This is intentionally plain exhaustive search. It is a falsification tool:
    if a claimed obstruction has a small certificate, this will find it.
    """

    gx, gy = target
    for y_abs in range(1, bound + 1):
        for y in (y_abs, -y_abs):
            for x in range(-bound, bound + 1):
                midpoint = (x, y)
                if is_two_step_certificate((gx, gy), midpoint):
                    return midpoint
    return None


@dataclass(frozen=True)
class BoundedSearchResult:
    target: Point
    bound: int
    certificate: Point | None

    @property
    def found(self) -> bool:
        return self.certificate is not None

    @property
    def status(self) -> str:
        if self.found:
            return "found"
        return "not_found_within_bound"


def bounded_two_step_search(target: Point, bound: int) -> BoundedSearchResult:
    """Run bounded certificate search and label the evidential status."""

    return BoundedSearchResult(
        target=target,
        bound=bound,
        certificate=find_two_step_certificate(target, bound),
    )


def horizontal_axis_certificate_table(n_min: int, n_max: int, bound: int) -> dict[int, Point | None]:
    return {
        n: find_two_step_certificate((n, 0), bound)
        for n in range(n_min, n_max + 1)
    }


@dataclass(frozen=True)
class Certificate:
    target: Point
    midpoint: Point

    @property
    def first_length_squared(self) -> int:
        x, y = self.midpoint
        return x * x + y * y

    @property
    def second_length_squared(self) -> int:
        gx, gy = self.target
        x, y = self.midpoint
        return (gx - x) * (gx - x) + (gy - y) * (gy - y)

    def valid(self) -> bool:
        return is_two_step_certificate(self.target, self.midpoint)


def scale_certificate(certificate: Certificate, factor: int) -> Certificate:
    """Scale a two-step certificate by a nonzero integer factor."""

    if factor == 0:
        raise ValueError("certificate scaling factor must be nonzero")

    target_x, target_y = certificate.target
    midpoint_x, midpoint_y = certificate.midpoint
    return Certificate(
        target=(factor * target_x, factor * target_y),
        midpoint=(factor * midpoint_x, factor * midpoint_y),
    )


def sign_swap_certificate(certificate: Certificate, target: Point) -> Certificate | None:
    """Transport a certificate to a requested sign/swap image of its target."""

    for swap in (False, True):
        for x_sign in (-1, 1):
            for y_sign in (-1, 1):
                transformed_target = signed_swap_point(
                    certificate.target,
                    x_sign,
                    y_sign,
                    swap,
                )
                if transformed_target != target:
                    continue

                transformed = Certificate(
                    target=target,
                    midpoint=signed_swap_point(
                        certificate.midpoint,
                        x_sign,
                        y_sign,
                        swap,
                    ),
                )
                if not transformed.valid():
                    raise AssertionError("sign/swap transform produced an invalid certificate")
                return transformed

    return None


def gaussian_multiply(point: Point, multiplier: Point) -> Point:
    """Multiply lattice points as Gaussian integers."""

    x, y = point
    a, b = multiplier
    return (a * x - b * y, a * y + b * x)


def gaussian_transform_certificate(
    certificate: Certificate,
    multiplier: Point,
) -> Certificate | None:
    """Transform a certificate by a Gaussian multiplier with square norm.

    Multiplication by (a, b) scales squared lengths by a^2 + b^2.  If that norm
    is a square, Pythagorean edge lengths stay integral.  The transformed edge
    may still become horizontal or vertical; in that degenerate case this
    constructor returns None.
    """

    if not certificate.valid():
        raise ValueError("certificate must be valid before transformation")

    a, b = multiplier
    multiplier_norm = a * a + b * b
    if multiplier_norm == 0 or not is_square(multiplier_norm):
        raise ValueError("Gaussian multiplier must have nonzero square norm")

    transformed = Certificate(
        target=gaussian_multiply(certificate.target, multiplier),
        midpoint=gaussian_multiply(certificate.midpoint, multiplier),
    )
    if not transformed.valid():
        return None
    return transformed


def gaussian_quotient_if_integer(target: Point, divisor: Point) -> Point | None:
    """Return target / divisor in Gaussian integers, if the quotient is integral."""

    divisor_norm = divisor[0] * divisor[0] + divisor[1] * divisor[1]
    if divisor_norm == 0:
        raise ValueError("Gaussian divisor must be nonzero")

    target_x, target_y = target
    divisor_x, divisor_y = divisor
    real_numerator = target_x * divisor_x + target_y * divisor_y
    imaginary_numerator = target_y * divisor_x - target_x * divisor_y
    if real_numerator % divisor_norm != 0 or imaginary_numerator % divisor_norm != 0:
        return None

    return (
        real_numerator // divisor_norm,
        imaginary_numerator // divisor_norm,
    )


def gaussian_divisor_certificate(
    target: Point,
    base_certificate: Certificate,
) -> Certificate | None:
    """Use a certified base target when target is a square-norm Gaussian multiple."""

    if not base_certificate.valid():
        raise ValueError("base certificate must be valid")

    multiplier = gaussian_quotient_if_integer(target, base_certificate.target)
    if multiplier is None:
        return None

    multiplier_norm = multiplier[0] * multiplier[0] + multiplier[1] * multiplier[1]
    if multiplier_norm == 0 or not is_square(multiplier_norm):
        return None

    return gaussian_transform_certificate(base_certificate, multiplier)


def first_gaussian_divisor_certificate(
    target: Point,
    base_certificates: Iterable[Certificate],
) -> Certificate | None:
    """Return the first square-norm Gaussian divisor certificate from known bases."""

    for base_certificate in base_certificates:
        certificate = gaussian_divisor_certificate(target, base_certificate)
        if certificate is not None:
            return certificate
    return None


def diagonal_pythagorean_multiplier_certificate(target: Point) -> Certificate | None:
    """Certificate for targets obtained from (1, 1) by square-norm multiplication."""

    g, h = target
    if (g + h) % 2 != 0 or (h - g) % 2 != 0:
        return None

    multiplier = ((g + h) // 2, (h - g) // 2)
    multiplier_norm = multiplier[0] * multiplier[0] + multiplier[1] * multiplier[1]
    if multiplier_norm == 0 or not is_square(multiplier_norm):
        return None

    base = Certificate(target=(1, 1), midpoint=(4, -3))
    return gaussian_transform_certificate(base, multiplier)


def lattice_coefficients(
    target: Point,
    first_direction: Point,
    second_direction: Point,
) -> tuple[int, int] | None:
    """Express target in the lattice generated by two directions, if possible."""

    gx, gy = target
    ux, uy = first_direction
    vx, vy = second_direction
    determinant = ux * vy - uy * vx
    if determinant == 0:
        return None

    first_numerator = gx * vy - gy * vx
    second_numerator = ux * gy - uy * gx
    if first_numerator % determinant != 0 or second_numerator % determinant != 0:
        return None
    return (first_numerator // determinant, second_numerator // determinant)


def determinant(first_direction: Point, second_direction: Point) -> int:
    ux, uy = first_direction
    vx, vy = second_direction
    return ux * vy - uy * vx


def same_projective_class_mod(first: Point, second: Point, modulus: int) -> bool:
    """Check whether two points lie on the same residue line modulo modulus.

    The zero residue is treated as lying on every line.
    """

    if modulus <= 1:
        raise ValueError("modulus must be greater than 1")

    first_zero = first[0] % modulus == 0 and first[1] % modulus == 0
    second_zero = second[0] % modulus == 0 and second[1] % modulus == 0
    if first_zero or second_zero:
        return True

    return determinant(first, second) % modulus == 0


def lattice_two_step_certificate(
    target: Point,
    first_direction: Point,
    second_direction: Point,
) -> Certificate | None:
    """Build a two-step certificate from two Pythagorean edge directions."""

    if not edge_delta(*first_direction) or not edge_delta(*second_direction):
        raise ValueError("directions must be legal Pythagorean edge vectors")

    coefficients = lattice_coefficients(target, first_direction, second_direction)
    if coefficients is None:
        return None

    first_coefficient, second_coefficient = coefficients
    if first_coefficient == 0 or second_coefficient == 0:
        return None

    ux, uy = first_direction
    certificate = Certificate(
        target=target,
        midpoint=(first_coefficient * ux, first_coefficient * uy),
    )
    if not certificate.valid():
        raise AssertionError("lattice decomposition did not produce a valid certificate")
    return certificate


def prime_determinant_lattice_certificate(
    target: Point,
    first_direction: Point,
    second_direction: Point,
) -> Certificate | None:
    """Certificate for the prime-determinant residue line generated by two directions."""

    lattice_determinant = abs(determinant(first_direction, second_direction))
    if not is_prime(lattice_determinant):
        raise ValueError("direction determinant must have prime absolute value")
    if not same_projective_class_mod(target, first_direction, lattice_determinant):
        return None
    return lattice_two_step_certificate(target, first_direction, second_direction)


DETERMINANT_SEVEN_DIRECTION_PAIRS: tuple[tuple[Point, Point], ...] = (
    ((3, 4), (4, 3)),
    ((3, -4), (4, -3)),
)

DETERMINANT_THIRTEEN_DIRECTION_PAIRS: tuple[tuple[Point, Point], ...] = (
    ((3, 4), (8, 15)),
    ((3, -4), (8, -15)),
    ((4, 3), (15, 8)),
    ((4, -3), (15, -8)),
)

DETERMINANT_SEVENTEEN_DIRECTION_PAIRS: tuple[tuple[Point, Point], ...] = (
    ((3, 4), (20, 21)),
    ((3, -4), (20, -21)),
    ((4, 3), (21, 20)),
    ((4, -3), (21, -20)),
)

EXPLICIT_TWO_ONE_RAY_BASE_CERTIFICATES: dict[int, Point] = {
    3: (12, -5),
    29: (-12, 5),
    41: (-8, -15),
    53: (-20, 21),
    61: (-10, -24),
    73: (-30, 16),
}

EXPLICIT_TWO_ONE_RAY_FINITE_AUDIT_CERTIFICATES: dict[int, Point] = {
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

SMALL_PRIME_DETERMINANT_DIRECTION_PAIRS: tuple[tuple[Point, Point], ...] = (
    ((3, -4), (28, -45)),
    ((3, 4), (28, 45)),
    ((4, 3), (45, 28)),
    ((4, -3), (45, -28)),
    ((5, 12), (12, 35)),
    ((5, -12), (12, -35)),
    ((12, -5), (35, -12)),
    ((12, 5), (35, 12)),
    ((3, 4), (88, 105)),
    ((3, -4), (88, -105)),
    ((4, -3), (105, -88)),
    ((4, 3), (105, 88)),
    ((20, -21), (21, -20)),
    ((20, 21), (21, 20)),
    ((3, -4), (104, -153)),
    ((4, -3), (153, -104)),
    ((24, -7), (35, -12)),
    ((7, 24), (12, 35)),
    ((7, -24), (12, -35)),
    ((24, 7), (35, 12)),
    ((4, 3), (153, 104)),
    ((3, 4), (104, 153)),
    ((15, -8), (56, -33)),
    ((12, -5), (77, -36)),
    ((3, -4), (140, -171)),
    ((8, -15), (33, -56)),
    ((4, 3), (171, 140)),
    ((5, 12), (36, 77)),
    ((5, -12), (36, -77)),
    ((4, -3), (171, -140)),
    ((8, 15), (33, 56)),
    ((3, 4), (140, 171)),
    ((12, 5), (77, 36)),
    ((15, 8), (56, 33)),
    ((9, 40), (16, 63)),
    ((12, 5), (187, 84)),
    ((40, -9), (63, -16)),
    ((5, -12), (84, -187)),
    ((5, 12), (84, 187)),
    ((40, 9), (63, 16)),
    ((12, -5), (187, -84)),
    ((9, -40), (16, -63)),
    ((28, 45), (33, 56)),
    ((12, 5), (247, 96)),
    ((45, -28), (56, -33)),
    ((5, 12), (96, 247)),
    ((5, -12), (96, -247)),
    ((45, 28), (56, 33)),
    ((12, -5), (247, -96)),
    ((28, -45), (33, -56)),
    ((15, 8), (208, 105)),
    ((8, -15), (105, -208)),
    ((8, 15), (105, 208)),
    ((15, -8), (208, -105)),
    ((7, -24), (60, -221)),
    ((24, 7), (221, 60)),
    ((24, -7), (221, -60)),
    ((7, 24), (60, 221)),
    ((5, -12), (168, -425)),
    ((12, 5), (425, 168)),
    ((12, -5), (425, -168)),
    ((5, 12), (168, 425)),
    ((20, -21), (297, -304)),
    ((24, -7), (475, -132)),
    ((7, 24), (132, 475)),
    ((21, 20), (304, 297)),
    ((84, -13), (143, -24)),
    ((13, -84), (24, -143)),
    ((13, 84), (24, 143)),
    ((84, 13), (143, 24)),
    ((21, -20), (304, -297)),
    ((7, -24), (132, -475)),
    ((24, 7), (475, 132)),
    ((20, 21), (297, 304)),
    ((48, -55), (133, -156)),
    ((40, -9), (357, -76)),
    ((55, 48), (156, 133)),
    ((9, -40), (76, -357)),
    ((9, 40), (76, 357)),
    ((55, -48), (156, -133)),
    ((40, 9), (357, 76)),
    ((48, 55), (133, 156)),
    ((35, -12), (408, -145)),
    ((12, -35), (145, -408)),
    ((12, 35), (145, 408)),
    ((35, 12), (408, 145)),
    ((35, -12), (468, -155)),
    ((12, 35), (155, 468)),
    ((21, 20), (460, 429)),
    ((20, -21), (429, -460)),
    ((20, 21), (429, 460)),
    ((21, -20), (460, -429)),
    ((12, -35), (155, -468)),
    ((35, 12), (468, 155)),
    ((117, 44), (140, 51)),
    ((44, -117), (51, -140)),
    ((44, 117), (51, 140)),
    ((117, -44), (140, -51)),
)


BOX_TWENTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (10, 5): (-20, 21),
    (13, 7): (-351, 280),
    (13, 10): (-195, 400),
    (16, 3): (-624, 315),
    (16, 15): (-704, 840),
    (17, 5): (-400, 561),
    (17, 13): (-844, 633),
    (20, 3): (-864, 990),
    (20, 9): (-684, 912),
}


BOX_THIRTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    **BOX_TWENTY_RESIDUAL_CERTIFICATES,
    (22, 11): (-110, 96),
    (23, 3): (-805, 348),
    (23, 11): (-180, -385),
    (25, 1): (-875, -300),
    (25, 14): (-95, -168),
    (26, 7): (-754, 672),
    (26, 14): (-702, 560),
    (26, 20): (-825, 440),
    (26, 21): (-330, 288),
    (26, 25): (-532, -855),
    (28, 3): (-620, -861),
    (28, 17): (-452, 339),
    (28, 27): (-732, 549),
    (29, 2): (-195, -28),
    (30, 13): (-936, -75),
}


BOX_FORTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    **BOX_THIRTY_RESIDUAL_CERTIFICATES,
    (32, 6): (-1248, 630),
    (32, 30): (-1860, 1395),
    (33, 17): (-264, 77),
    (34, 10): (-800, 1122),
    (34, 26): (-1688, 1266),
    (35, 2): (-1645, 492),
    (35, 4): (-1197, 304),
    (35, 8): (-1485, 1148),
    (35, 26): (-520, -546),
    (35, 33): (-1325, -1092),
    (37, 3): (-1628, -885),
    (37, 10): (-299, -180),
    (37, 25): (-572, -555),
    (37, 27): (-1924, -693),
    (38, 1): (-42, 40),
    (38, 15): (-1798, 120),
    (38, 19): (-342, 280),
    (39, 21): (-1573, -264),
    (39, 23): (-1404, -53),
    (39, 30): (-585, 1200),
    (40, 6): (-1728, 1980),
    (40, 18): (-1368, 1824),
}


BOX_FIFTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    **BOX_FORTY_RESIDUAL_CERTIFICATES,
    (41, 9): (-1980, 189),
    (41, 12): (-4560, -4788),
    (41, 14): (-1240, 1722),
    (43, 7): (-2204, 3003),
    (43, 9): (-4104, 3705),
    (43, 30): (-2024, 3990),
    (44, 17): (-4092, -256),
    (44, 27): (-4240, 4452),
    (44, 29): (-3036, -1027),
    (44, 31): (-4180, 399),
    (45, 29): (-2835, -972),
    (46, 6): (-4320, -2106),
    (46, 22): (-2024, 1518),
    (46, 29): (-2550, 1976),
    (47, 8): (-4386, 752),
    (47, 10): (-3297, -3140),
    (47, 13): (-3081, 4108),
    (47, 21): (-4453, -804),
    (47, 22): (-1929, 2572),
    (47, 25): (-748, -1035),
    (47, 29): (-3553, -396),
    (47, 42): (-3080, -294),
    (47, 43): (-2748, -1145),
    (48, 9): (-4488, -4941),
    (48, 37): (-4488, -665),
    (48, 45): (-4320, -279),
    (49, 2): (-575, -48),
    (49, 5): (-3003, -4900),
    (49, 29): (-2915, -2544),
    (49, 36): (-3605, 1236),
    (49, 45): (-1095, 2628),
    (50, 2): (-3150, 800),
    (50, 17): (-1480, 969),
    (50, 23): (-2860, 1575),
    (50, 25): (-3096, 553),
    (50, 28): (-3975, 1408),
}


BOX_SIXTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    **BOX_FIFTY_RESIDUAL_CERTIFICATES,
    (51, 11): (-12, -5),
    (51, 13): (-9, -12),
    (51, 15): (-9, 40),
    (51, 20): (6, -8),
    (51, 38): (-165, -52),
    (51, 39): (-36, -77),
    (52, 14): (12, 5),
    (52, 21): (12, -9),
    (52, 28): (24, 7),
    (52, 40): (-8, 15),
    (52, 42): (-20, 21),
    (52, 43): (-12, -5),
    (52, 50): (-20, -15),
    (53, 2): (5, -12),
    (53, 33): (-55, -48),
    (53, 47): (-7735, -4968),
    (53, 50): (-51, -1300),
    (55, 26): (-65, -156),
    (55, 46): (-200, -1242),
    (56, 6): (20, -21),
    (56, 17): (12, -16),
    (56, 34): (24, 10),
    (56, 37): (-40, 9),
    (56, 47): (-40, 75),
    (56, 54): (-8, 6),
    (57, 17): (-159, 212),
    (57, 44): (12, -16),
    (57, 49): (-3, 4),
    (57, 56): (18, -24),
    (58, 4): (-5, -12),
    (58, 13): (406, -792),
    (59, 13): (-4, -3),
    (59, 33): (35, -12),
    (59, 43): (-645, -860),
    (59, 49): (-2385, -1484),
    (59, 51): (4, 3),
    (59, 58): (35, -12),
    (60, 9): (12, -5),
    (60, 13): (-36, -15),
    (60, 26): (-12, 5),
    (60, 27): (12, -9),
}


def first_lattice_certificate(
    target: Point,
    direction_pairs: Iterable[tuple[Point, Point]],
) -> Certificate | None:
    """Return the first two-edge lattice certificate from a list of pairs."""

    for first_direction, second_direction in direction_pairs:
        pair_determinant = abs(determinant(first_direction, second_direction))
        if is_prime(pair_determinant):
            certificate = prime_determinant_lattice_certificate(
                target,
                first_direction,
                second_direction,
            )
        else:
            certificate = lattice_two_step_certificate(
                target,
                first_direction,
                second_direction,
            )
        if certificate is not None:
            return certificate
    return None


def determinant_seven_lattice_certificate(target: Point) -> Certificate | None:
    """Two-step certificate for the 3-4-5 determinant-seven congruence families.

    The first pair covers targets with g + h divisible by 7.  The second pair
    covers targets with g - h divisible by 7.  If the target is a scalar
    multiple of one of the basis directions, the target is already one step
    from the origin and this two-step certificate constructor returns None.
    """

    return first_lattice_certificate(target, DETERMINANT_SEVEN_DIRECTION_PAIRS)


def determinant_thirteen_lattice_certificate(target: Point) -> Certificate | None:
    """Two-step certificate for determinant-thirteen lattice families.

    These 3-4-5 and 8-15-17 direction pairs cover targets with
    g congruent to one of +/-3h or +/-4h modulo 13, except for scalar
    multiples of the basis directions, which are already one-step targets.
    """

    return first_lattice_certificate(target, DETERMINANT_THIRTEEN_DIRECTION_PAIRS)


def determinant_seventeen_lattice_certificate(target: Point) -> Certificate | None:
    """Two-step certificate for determinant-seventeen lattice families.

    These direction pairs cover targets with g congruent to one of
    +/-5h or +/-7h modulo 17, except for scalar multiples of the basis
    directions, which are already one-step targets.
    """

    return first_lattice_certificate(target, DETERMINANT_SEVENTEEN_DIRECTION_PAIRS)


def small_prime_lattice_certificate(target: Point) -> Certificate | None:
    """Two-step certificate for additional small prime-determinant families.

    The encoded table covers the residue lines g/h congruent to:
    - +/-5 and +/-9 modulo 23;
    - +/-3 and +/-10 modulo 31;
    - +/-10 and +/-11 modulo 37;
    - +/-1 modulo 41;
    - +/-10, +/-13, +/-15, and +/-20 modulo 43;
    - +/-4, +/-7, +/-11, +/-12, +/-17, and +/-20 modulo 47;
    - +/-13, +/-17, +/-28, and +/-30 modulo 73;
    - +/-8, +/-19, +/-31, and +/-35 modulo 83;
    - +/-13 and +/-41 modulo 89;
    - +/-22 and +/-34 modulo 107;
    - +/-45 and +/-46 modulo 109;
    - +/-14, +/-19, +/-33, +/-56, +/-66, and +/-69 modulo 157;
    - +/-18, +/-34, +/-48, and +/-56 modulo 173;
    - +/-12 and +/-15 modulo 179;
    - +/-13, +/-44, +/-87, and +/-90 modulo 191;
    - +/-86 and +/-92 modulo 193.
    Scalar multiples of the basis directions are already one-step targets and
    return None from this two-step constructor.
    """

    return first_lattice_certificate(target, SMALL_PRIME_DETERMINANT_DIRECTION_PAIRS)


def euclid_strip_certificate(
    direction: Point,
    q: int,
    parameter_a: int,
) -> Certificate | None:
    """Build a strip certificate from one fixed direction and one Euclid vector.

    Let direction U=(u,v) be a legal Pythagorean edge vector.  For a requested
    final y-coordinate q and Euclid parameter A, set B = uA - q.  If

        r v + (B^2 - A^2) = q,

    then rU followed by the Euclid vector (2AB, B^2 - A^2) reaches
    (ru + 2AB, q).
    """

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")
    if q == 0 or parameter_a == 0:
        return None

    u, v = direction
    parameter_b = u * parameter_a - q
    second_y = parameter_b * parameter_b - parameter_a * parameter_a
    coefficient_numerator = q - second_y
    if coefficient_numerator % v != 0:
        return None

    coefficient = coefficient_numerator // v
    if (
        coefficient == 0
        or parameter_b == 0
        or abs(parameter_b) == abs(parameter_a)
    ):
        return None

    certificate = Certificate(
        target=(
            u * coefficient + 2 * parameter_a * parameter_b,
            q,
        ),
        midpoint=(u * coefficient, v * coefficient),
    )
    if not certificate.valid():
        raise AssertionError("Euclid strip formula produced an invalid certificate")
    return certificate


def half_leg_strip_certificate(
    direction: Point,
    q: int,
    t: int,
) -> Certificate | None:
    """Specialize the Euclid strip with A = vt/2 for odd-even directions."""

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")

    u, v = direction
    if u % 2 == 0 or v % 2 != 0:
        raise ValueError("direction must have odd first coordinate and even second coordinate")
    if q == 0 or t == 0:
        return None
    if (q * (1 - q)) % v != 0:
        return None

    return euclid_strip_certificate(direction, q, v * t // 2)


def half_leg_unit_coordinate_certificate(direction: Point, t: int) -> Certificate | None:
    """Unit-coordinate specialization of the half-leg strip family."""

    return half_leg_strip_certificate(direction, q=1, t=t)


def consecutive_direction_strip_certificate(
    target: Point,
    odd_leg: int,
) -> Certificate | None:
    """Solve the Euclid strip for a consecutive direction.

    For odd u >= 3, set v = (u^2 - 1) / 2.  The direction (u, v) is
    Pythagorean and the Euclid strip target equation is linear in A:

        g = q(A(u^2 + 1) - u(q - 1)) / v.

    This returns the corresponding certificate when A is integral and the
    underlying Euclid strip is nondegenerate.
    """

    if odd_leg < 3 or odd_leg % 2 == 0:
        raise ValueError("odd_leg must be an odd integer at least 3")

    g, q = target
    if q == 0:
        return None

    even_leg = (odd_leg * odd_leg - 1) // 2
    numerator = even_leg * g + odd_leg * q * (q - 1)
    denominator = q * (odd_leg * odd_leg + 1)
    if numerator % denominator != 0:
        return None

    return euclid_strip_certificate(
        (odd_leg, even_leg),
        q,
        numerator // denominator,
    )


def integer_slope_consecutive_ray_certificate(
    slope: int,
    multiplier: int,
    odd_leg: int,
) -> Certificate | None:
    """Certificate for targets (slope * n, n) from signed consecutive strips."""

    return rational_slope_consecutive_ray_certificate(
        (slope, 1),
        multiplier,
        odd_leg,
    )


def rational_slope_consecutive_ray_certificate(
    ray: Point,
    multiplier: int,
    odd_leg: int,
) -> Certificate | None:
    """Certificate for targets n * ray from signed consecutive strips."""

    if odd_leg < 3 or odd_leg % 2 == 0:
        raise ValueError("odd_leg must be an odd integer at least 3")
    ray_x, ray_y = ray
    if multiplier == 0 or ray_y == 0:
        return None

    target = (ray_x * multiplier, ray_y * multiplier)
    even_leg = (odd_leg * odd_leg - 1) // 2
    modulus = odd_leg * odd_leg + 1
    for direction_sign in (1, -1):
        numerator = (
            even_leg * ray_x
            + direction_sign * odd_leg * ray_y * (ray_y * multiplier - 1)
        )
        denominator = ray_y * modulus
        if numerator % denominator != 0:
            continue

        certificate = euclid_strip_certificate(
            (direction_sign * odd_leg, even_leg),
            ray_y * multiplier,
            numerator // denominator,
        )
        if certificate is not None:
            if certificate.target != target:
                raise AssertionError("rational-slope ray formula produced the wrong target")
            return certificate

    return None


def two_one_ray_consecutive_certificate(
    multiplier: int,
    odd_leg: int,
) -> Certificate | None:
    """Certificate for (2n, n) from the solved consecutive strip.

    For odd u >= 3, this covers positive multipliers in either family

        n = t(u^2 + 1) - 2u + 1,  t >= 1,
        n = t(u^2 + 1) + 2u + 1,  t >= 0,

    except for any strip degeneracies handled by
    consecutive_direction_strip_certificate.
    """

    if odd_leg < 3 or odd_leg % 2 == 0:
        raise ValueError("odd_leg must be an odd integer at least 3")
    if multiplier <= 0:
        return None

    denominator = odd_leg * odd_leg + 1
    numerator = multiplier + 2 * odd_leg - 1
    if numerator % denominator != 0:
        numerator = multiplier - 2 * odd_leg - 1
        if numerator % denominator != 0:
            return None
        quotient = numerator // denominator
        if quotient < 0:
            return None
        return euclid_strip_certificate(
            (-odd_leg, (odd_leg * odd_leg - 1) // 2),
            multiplier,
            -odd_leg * quotient - 1,
        )

    quotient = numerator // denominator
    if quotient < 1:
        return None

    return consecutive_direction_strip_certificate((2 * multiplier, multiplier), odd_leg)


def two_one_ray_consecutive_orbit_certificate(
    target: Point,
    odd_leg: int,
) -> Certificate | None:
    """Symmetric certificate for sign/swap images of the (2n, n) ray family."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        multiplier = abs_h
        base = two_one_ray_consecutive_certificate(multiplier, odd_leg)
        if base is None:
            return None
        midpoint_x, midpoint_y = base.midpoint
        return Certificate(
            target=target,
            midpoint=(
                (1 if g > 0 else -1) * midpoint_x,
                (1 if h > 0 else -1) * midpoint_y,
            ),
        )

    if abs_h == 2 * abs_g:
        multiplier = abs_g
        base = two_one_ray_consecutive_certificate(multiplier, odd_leg)
        if base is None:
            return None
        midpoint_x, midpoint_y = base.midpoint
        return Certificate(
            target=target,
            midpoint=(
                (1 if g > 0 else -1) * midpoint_y,
                (1 if h > 0 else -1) * midpoint_x,
            ),
        )

    return None


def two_one_ray_even_certificate(multiplier: int) -> Certificate | None:
    """Certificate for even positive multipliers of the (2, 1) ray."""

    if multiplier <= 0 or multiplier % 2 != 0:
        return None

    base = Certificate(target=(4, 2), midpoint=(-36, 77))
    return scale_certificate(base, multiplier // 2)


def two_one_ray_even_orbit_certificate(target: Point) -> Certificate | None:
    """Symmetric certificate for even multiples of the (2, 1) ray."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        base = two_one_ray_even_certificate(abs_h)
        if base is None:
            return None
        midpoint_x, midpoint_y = base.midpoint
        return Certificate(
            target=target,
            midpoint=(
                (1 if g > 0 else -1) * midpoint_x,
                (1 if h > 0 else -1) * midpoint_y,
            ),
        )

    if abs_h == 2 * abs_g:
        base = two_one_ray_even_certificate(abs_g)
        if base is None:
            return None
        midpoint_x, midpoint_y = base.midpoint
        return Certificate(
            target=target,
            midpoint=(
                (1 if g > 0 else -1) * midpoint_y,
                (1 if h > 0 else -1) * midpoint_x,
            ),
        )

    return None


def two_one_ray_explicit_base_certificate(multiplier: int) -> Certificate | None:
    """Certificate from a finite table of exact base certificates on the (2, 1) ray."""

    if multiplier <= 0:
        return None

    for base_multiplier, midpoint in EXPLICIT_TWO_ONE_RAY_BASE_CERTIFICATES.items():
        if multiplier % base_multiplier != 0:
            continue

        base = Certificate(
            target=(2 * base_multiplier, base_multiplier),
            midpoint=midpoint,
        )
        certificate = scale_certificate(base, multiplier // base_multiplier)
        if not certificate.valid():
            raise AssertionError("explicit ray base certificate did not scale correctly")
        return certificate

    return None


def two_one_ray_explicit_base_orbit_certificate(target: Point) -> Certificate | None:
    """Symmetric certificate from the finite explicit base table."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        base = two_one_ray_explicit_base_certificate(abs_h)
        if base is None:
            return None
        midpoint_x, midpoint_y = base.midpoint
        return Certificate(
            target=target,
            midpoint=(
                (1 if g > 0 else -1) * midpoint_x,
                (1 if h > 0 else -1) * midpoint_y,
            ),
        )

    if abs_h == 2 * abs_g:
        base = two_one_ray_explicit_base_certificate(abs_g)
        if base is None:
            return None
        midpoint_x, midpoint_y = base.midpoint
        return Certificate(
            target=target,
            midpoint=(
                (1 if g > 0 else -1) * midpoint_y,
                (1 if h > 0 else -1) * midpoint_x,
            ),
        )

    return None


def two_one_ray_finite_audit_certificate(multiplier: int) -> Certificate | None:
    """Certificate from finite-audit base rows on the (2, 1) ray."""

    if multiplier <= 0:
        return None

    for base_multiplier, midpoint in EXPLICIT_TWO_ONE_RAY_FINITE_AUDIT_CERTIFICATES.items():
        if multiplier % base_multiplier != 0:
            continue

        base = Certificate(
            target=(2 * base_multiplier, base_multiplier),
            midpoint=midpoint,
        )
        certificate = scale_certificate(base, multiplier // base_multiplier)
        if not certificate.valid():
            raise AssertionError("finite-audit ray certificate did not scale correctly")
        return certificate

    return None


def two_one_ray_finite_audit_orbit_certificate(target: Point) -> Certificate | None:
    """Symmetric certificate from finite-audit base rows."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        base = two_one_ray_finite_audit_certificate(abs_h)
        if base is None:
            return None
        midpoint_x, midpoint_y = base.midpoint
        return Certificate(
            target=target,
            midpoint=(
                (1 if g > 0 else -1) * midpoint_x,
                (1 if h > 0 else -1) * midpoint_y,
            ),
        )

    if abs_h == 2 * abs_g:
        base = two_one_ray_finite_audit_certificate(abs_g)
        if base is None:
            return None
        midpoint_x, midpoint_y = base.midpoint
        return Certificate(
            target=target,
            midpoint=(
                (1 if g > 0 else -1) * midpoint_y,
                (1 if h > 0 else -1) * midpoint_x,
            ),
        )

    return None


def _strip_y_one_multiple_of_five_certificate(t: int) -> Certificate | None:
    """Certificate for the strip target (5t, 1), t nonzero."""

    return consecutive_hypotenuse_unit_coordinate_certificate(2, t)


def unit_coordinate_multiple_of_five_certificate(target: Point) -> Certificate | None:
    """Certificate when one coordinate is +/-1 and the other is a nonzero multiple of 5."""

    g, h = target
    if h in (-1, 1) and g != 0 and g % 5 == 0:
        base = _strip_y_one_multiple_of_five_certificate(g // 5)
        if base is None:
            return None
        midpoint_x, midpoint_y = base.midpoint
        return Certificate(target=target, midpoint=(midpoint_x, h * midpoint_y))

    if g in (-1, 1) and h != 0 and h % 5 == 0:
        base = _strip_y_one_multiple_of_five_certificate(h // 5)
        if base is None:
            return None
        midpoint_x, midpoint_y = base.midpoint
        return Certificate(target=target, midpoint=(g * midpoint_y, midpoint_x))

    return None


def consecutive_hypotenuse_unit_coordinate_certificate(m: int, t: int) -> Certificate | None:
    """Certificate for (ct, 1), where c = m^2 + (m - 1)^2 and t is nonzero."""

    if m < 2:
        raise ValueError("m must be at least 2")
    if t == 0:
        return None

    certificate = affine_consecutive_hypotenuse_certificate(m, q=1, t=t)
    if certificate is None:
        raise AssertionError("unit-coordinate specialization unexpectedly degenerated")
    return certificate


def affine_consecutive_hypotenuse_certificate(
    m: int,
    q: int,
    t: int,
) -> Certificate | None:
    """Affine strip certificate from consecutive Euclid parameters.

    For u = 2m - 1, v = 2m(m - 1), c = m^2 + (m - 1)^2, this certifies
    (cqt + u q(1-q)/v, q) whenever v divides q(1-q) and the displayed
    Euclid vectors are nondegenerate.
    """

    if m < 2:
        raise ValueError("m must be at least 2")
    if q == 0 or t == 0:
        return None

    odd_leg = 2 * m - 1
    even_leg = 2 * m * (m - 1)
    hypotenuse = m * m + (m - 1) * (m - 1)
    if (q * (1 - q)) % even_leg != 0:
        return None

    parameter_a = m * (m - 1) * t
    parameter_b = odd_leg * parameter_a - q
    coefficient = (
        q * (1 - q) // even_leg
        + odd_leg * q * t
        - 2 * parameter_a * parameter_a
    )

    if coefficient == 0 or parameter_b == 0 or abs(parameter_b) == abs(parameter_a):
        return None

    certificate = Certificate(
        target=(
            hypotenuse * q * t + odd_leg * q * (1 - q) // even_leg,
            q,
        ),
        midpoint=(odd_leg * coefficient, even_leg * coefficient),
    )
    if not certificate.valid():
        raise AssertionError("affine consecutive-hypotenuse formula produced an invalid certificate")
    return certificate


def unit_coordinate_consecutive_hypotenuse_certificate(
    target: Point,
    m: int,
) -> Certificate | None:
    """Symmetric unit-coordinate certificate for c = m^2 + (m - 1)^2."""

    if m < 2:
        raise ValueError("m must be at least 2")

    hypotenuse = m * m + (m - 1) * (m - 1)
    g, h = target
    if h in (-1, 1) and g != 0 and g % hypotenuse == 0:
        base = consecutive_hypotenuse_unit_coordinate_certificate(m, g // hypotenuse)
        if base is None:
            return None
        midpoint_x, midpoint_y = base.midpoint
        return Certificate(target=target, midpoint=(midpoint_x, h * midpoint_y))

    if g in (-1, 1) and h != 0 and h % hypotenuse == 0:
        base = consecutive_hypotenuse_unit_coordinate_certificate(m, h // hypotenuse)
        if base is None:
            return None
        midpoint_x, midpoint_y = base.midpoint
        return Certificate(target=target, midpoint=(g * midpoint_y, midpoint_x))

    return None


def pythagorean_leg_completion(leg: int) -> tuple[int, int]:
    """Return one positive partner leg and hypotenuse for any leg >= 3.

    Odd legs use (a, (a^2 - 1) / 2, (a^2 + 1) / 2).  Even legs a = 2k use
    (2k, k^2 - 1, k^2 + 1).  The excluded positive legs 1 and 2 are exactly
    the cases where these formulas would be degenerate or impossible.
    """

    if leg < 3:
        raise ValueError("positive Pythagorean leg completion requires leg >= 3")
    if leg % 2 == 1:
        return ((leg * leg - 1) // 2, (leg * leg + 1) // 2)

    half = leg // 2
    return (half * half - 1, half * half + 1)


def midpoint_axis_certificate(n: int) -> Certificate | None:
    """Certificate for even horizontal targets n >= 6.

    If n = 2a and a >= 3 is a Pythagorean leg, the midpoint (a, y) has equal
    integer distances to (0, 0) and (n, 0).
    """

    if n < 6 or n % 2 == 1:
        return None
    half = n // 2
    partner_leg, _hypotenuse = pythagorean_leg_completion(half)
    return Certificate(target=(n, 0), midpoint=(half, partner_leg))


def explicit_axis_certificate(n: int) -> Certificate | None:
    """Recorded exceptional certificates not covered by the even midpoint rule."""

    if n == 4:
        return Certificate(target=(4, 0), midpoint=(-5, 12))
    return None


@dataclass(frozen=True, order=True)
class PythagoreanTriple:
    leg_a: int
    leg_b: int
    hypotenuse: int

    @property
    def legs(self) -> tuple[int, int]:
        return (self.leg_a, self.leg_b)

    def valid(self) -> bool:
        legs_square_sum = self.leg_a * self.leg_a + self.leg_b * self.leg_b
        return (
            self.leg_a > 0
            and self.leg_b > 0
            and self.hypotenuse > 0
            and legs_square_sum == self.hypotenuse * self.hypotenuse
        )


def pythagorean_triple_orthogonal_lattice_certificate(
    target: Point,
    triple: PythagoreanTriple,
) -> Certificate | None:
    """Certificate from a triple direction and its quarter-turn rotation."""

    if not triple.valid():
        raise ValueError("triple must be a positive Pythagorean triple")

    leg_a, leg_b = triple.legs
    return lattice_two_step_certificate(
        target,
        (leg_a, leg_b),
        (-leg_b, leg_a),
    )


def consecutive_leg_pythagorean_triple(index: int) -> PythagoreanTriple:
    """Return the index-th positive triple with consecutive legs.

    The odd sum z = a + (a + 1) and hypotenuse c satisfy z^2 - 2c^2 = -1.
    Multiplication by 3 + 2 sqrt(2) gives the next positive solution.
    """

    if index < 0:
        raise ValueError("index must be nonnegative")

    odd_sum = 7
    hypotenuse = 5
    for _ in range(index):
        odd_sum, hypotenuse = (
            3 * odd_sum + 4 * hypotenuse,
            2 * odd_sum + 3 * hypotenuse,
        )

    first_leg = (odd_sum - 1) // 2
    return PythagoreanTriple(first_leg, first_leg + 1, hypotenuse)


def consecutive_leg_swap_lattice_certificate(
    target: Point,
    index: int,
) -> Certificate | None:
    """Certificate from the swap lattice of a consecutive-leg triple.

    For legs (a, a + 1), the pairs (a, a + 1),(a + 1, a) and
    (a, -a - 1),(a + 1, -a) cover the exact congruence lines
    g + h == 0 and g - h == 0 modulo 2a + 1, up to the usual one-step
    zero-coefficient cases.
    """

    triple = consecutive_leg_pythagorean_triple(index)
    first_leg, second_leg = triple.legs
    return first_lattice_certificate(
        target,
        (
            ((first_leg, second_leg), (second_leg, first_leg)),
            ((first_leg, -second_leg), (second_leg, -first_leg)),
        ),
    )


def generate_pythagorean_triples(m_limit: int, scale_limit: int) -> list[PythagoreanTriple]:
    """Generate triples d(m^2-k^2), 2dmk, d(m^2+k^2) within parameter limits."""

    triples: set[PythagoreanTriple] = set()
    for m in range(2, m_limit + 1):
        for k in range(1, m):
            leg_1 = m * m - k * k
            leg_2 = 2 * m * k
            hypotenuse = m * m + k * k
            for scale in range(1, scale_limit + 1):
                a, b = sorted((scale * leg_1, scale * leg_2))
                triples.add(PythagoreanTriple(a, b, scale * hypotenuse))
    return sorted(triples)


@dataclass(frozen=True)
class SharedLegAxisCertificate:
    target_n: int
    midpoint: Point
    shared_leg: int
    first_horizontal_leg: int
    second_horizontal_leg: int
    first_hypotenuse: int
    second_hypotenuse: int
    relation: str

    @property
    def target(self) -> Point:
        return (self.target_n, 0)

    @property
    def certificate(self) -> Certificate:
        return Certificate(target=self.target, midpoint=self.midpoint)

    def valid(self) -> bool:
        return (
            self.first_horizontal_leg > 0
            and self.second_horizontal_leg > 0
            and self.shared_leg > 0
            and self.first_horizontal_leg * self.first_horizontal_leg
            + self.shared_leg * self.shared_leg
            == self.first_hypotenuse * self.first_hypotenuse
            and self.second_horizontal_leg * self.second_horizontal_leg
            + self.shared_leg * self.shared_leg
            == self.second_hypotenuse * self.second_hypotenuse
            and self.certificate.valid()
        )


def shared_leg_axis_certificate_records(
    m_limit: int,
    scale_limit: int,
    n_min: int = 3,
    n_max: int | None = None,
) -> list[SharedLegAxisCertificate]:
    """Generate axis certificates from pairs of triples sharing a vertical leg.

    If two triples have the same leg y and horizontal legs a < b, then:
    - (a, y) certifies target a + b;
    - (-a, y) certifies target b - a.
    """

    by_shared_leg: dict[int, set[tuple[int, int]]] = {}
    for triple in generate_pythagorean_triples(m_limit, scale_limit):
        a, b = triple.legs
        by_shared_leg.setdefault(a, set()).add((b, triple.hypotenuse))
        by_shared_leg.setdefault(b, set()).add((a, triple.hypotenuse))

    records: list[SharedLegAxisCertificate] = []
    for shared_leg, options in by_shared_leg.items():
        for first, second in combinations(sorted(options), 2):
            small_leg, small_hypotenuse = first
            large_leg, large_hypotenuse = second
            if small_leg == large_leg:
                continue

            difference = large_leg - small_leg
            if difference >= n_min and (n_max is None or difference <= n_max):
                records.append(
                    SharedLegAxisCertificate(
                        target_n=difference,
                        midpoint=(-small_leg, shared_leg),
                        shared_leg=shared_leg,
                        first_horizontal_leg=small_leg,
                        second_horizontal_leg=large_leg,
                        first_hypotenuse=small_hypotenuse,
                        second_hypotenuse=large_hypotenuse,
                        relation="difference",
                    )
                )

            total = small_leg + large_leg
            if total >= n_min and (n_max is None or total <= n_max):
                records.append(
                    SharedLegAxisCertificate(
                        target_n=total,
                        midpoint=(small_leg, shared_leg),
                        shared_leg=shared_leg,
                        first_horizontal_leg=small_leg,
                        second_horizontal_leg=large_leg,
                        first_hypotenuse=small_hypotenuse,
                        second_hypotenuse=large_hypotenuse,
                        relation="sum",
                    )
                )

    return sorted(
        records,
        key=lambda record: (
            record.target_n,
            max(record.first_hypotenuse, record.second_hypotenuse),
            record.shared_leg,
            abs(record.midpoint[0]),
            record.relation,
        ),
    )


def shared_leg_axis_certificate_table(
    m_limit: int,
    scale_limit: int,
    n_min: int = 3,
    n_max: int | None = None,
) -> dict[int, SharedLegAxisCertificate]:
    """Return the shortest-hypotenuse generated certificate for each target n."""

    table: dict[int, SharedLegAxisCertificate] = {}
    for record in shared_leg_axis_certificate_records(m_limit, scale_limit, n_min, n_max):
        table.setdefault(record.target_n, record)
    return table


def odd_residues(modulus: int) -> tuple[int, ...]:
    return tuple(residue for residue in range(modulus) if residue % 2 == 1)


def residue_witnesses(
    records: Iterable[SharedLegAxisCertificate],
    modulus: int,
    residues: Iterable[int] | None = None,
) -> dict[int, SharedLegAxisCertificate]:
    """Return the smallest-hypotenuse witness found for each requested residue."""

    wanted = None if residues is None else {residue % modulus for residue in residues}
    witnesses: dict[int, SharedLegAxisCertificate] = {}
    ordered_records = sorted(
        records,
        key=lambda record: (
            max(record.first_hypotenuse, record.second_hypotenuse),
            record.target_n,
            record.shared_leg,
            abs(record.midpoint[0]),
        ),
    )
    for record in ordered_records:
        residue = record.target_n % modulus
        if wanted is not None and residue not in wanted:
            continue
        witnesses.setdefault(residue, record)
    return witnesses


def missing_residues(
    records: Iterable[SharedLegAxisCertificate],
    modulus: int,
    residues: Iterable[int] | None = None,
) -> tuple[int, ...]:
    if residues is None:
        requested = tuple(range(modulus))
    else:
        requested = tuple(residue % modulus for residue in residues)
    witnesses = residue_witnesses(records, modulus, requested)
    return tuple(residue for residue in requested if residue not in witnesses)


def euclid_parameter_difference_certificate(m: int, t: int) -> SharedLegAxisCertificate:
    """Certificate from the Euclid parameter pair (m, 1) and (m + t, 1).

    Scaling these two triples to the common vertical leg 2m(m+t) gives
    horizontal legs (m+t)(m^2-1) and m((m+t)^2-1). Their difference is
    t(m^2 + mt + 1).
    """

    if m < 2:
        raise ValueError("m must be at least 2 to avoid a degenerate first triple")
    if t < 1:
        raise ValueError("t must be positive")

    shared_leg = 2 * m * (m + t)
    first_horizontal_leg = (m + t) * (m * m - 1)
    second_horizontal_leg = m * ((m + t) * (m + t) - 1)
    first_hypotenuse = (m + t) * (m * m + 1)
    second_hypotenuse = m * ((m + t) * (m + t) + 1)

    return SharedLegAxisCertificate(
        target_n=second_horizontal_leg - first_horizontal_leg,
        midpoint=(-first_horizontal_leg, shared_leg),
        shared_leg=shared_leg,
        first_horizontal_leg=first_horizontal_leg,
        second_horizontal_leg=second_horizontal_leg,
        first_hypotenuse=first_hypotenuse,
        second_hypotenuse=second_hypotenuse,
        relation="difference",
    )


def theorem3_certificate(
    target: Point,
    triple: PythagoreanTriple,
    x_sign: int,
    y_sign: int,
) -> Certificate | None:
    """Certificate from the signed form of the paper's Theorem 3.

    For a Pythagorean triple (a, b, c), non-axis target (g, h), and signs
    sx, sy in {-1, 1}, the relation

        (c - sx*a) g = (c + sy*b) h - 1

    makes P = (sx*a*g*h, sy*b*g*h) a two-step midpoint for (g, h).
    The sign convention records the actual midpoint signs; it also covers the
    mixed-sign examples listed after Theorem 3 in the paper.
    """

    if x_sign not in (-1, 1) or y_sign not in (-1, 1):
        raise ValueError("x_sign and y_sign must be -1 or 1")
    if not triple.valid():
        raise ValueError("triple must be a positive Pythagorean triple")

    g, h = target
    if g == 0 or h == 0:
        return None

    a, b, c = triple.leg_a, triple.leg_b, triple.hypotenuse
    if (c - x_sign * a) * g != (c + y_sign * b) * h - 1:
        return None

    certificate = Certificate(
        target=target,
        midpoint=(x_sign * a * g * h, y_sign * b * g * h),
    )
    if not certificate.valid():
        raise AssertionError("theorem 3 relation did not produce a valid certificate")
    return certificate


def theorem3_line_certificate(
    triple: PythagoreanTriple,
    x_sign: int,
    y_sign: int,
    h: int,
) -> Certificate | None:
    """Generate a signed Theorem 3 certificate using h as the free parameter."""

    if x_sign not in (-1, 1) or y_sign not in (-1, 1):
        raise ValueError("x_sign and y_sign must be -1 or 1")
    if not triple.valid():
        raise ValueError("triple must be a positive Pythagorean triple")
    if h == 0:
        return None

    a, b, c = triple.leg_a, triple.leg_b, triple.hypotenuse
    denominator = c - x_sign * a
    numerator = (c + y_sign * b) * h - 1
    if numerator % denominator != 0:
        return None

    g = numerator // denominator
    if g == 0:
        return None

    return theorem3_certificate((g, h), triple, x_sign, y_sign)


def theorem3_quadratic_strip_certificate(target: Point, parameter_n: int) -> Certificate | None:
    """Recognize the first quadratic-strip corollaries of Theorem 3.

    For n >= 1, the consecutive Euclid triples with parameters (n + 1, n)
    produce certificates for

        (2 h n^2 - 1, h) and (g, 2 g n^2 + 1)

    whenever the fixed coordinate is nonzero.
    """

    if parameter_n < 1:
        raise ValueError("parameter_n must be positive")

    g, h = target
    if g == 0 or h == 0:
        return None

    n = parameter_n
    hypotenuse = 2 * n * n + 2 * n + 1

    if g == 2 * h * n * n - 1:
        return theorem3_certificate(
            target,
            PythagoreanTriple(2 * n * (n + 1), 2 * n + 1, hypotenuse),
            x_sign=1,
            y_sign=-1,
        )

    if h == 2 * g * n * n + 1:
        return theorem3_certificate(
            target,
            PythagoreanTriple(2 * n + 1, 2 * n * (n + 1), hypotenuse),
            x_sign=1,
            y_sign=-1,
        )

    return None


def theorem3_quadratic_strip_orbit_certificate(
    target: Point,
    parameter_n: int,
) -> Certificate | None:
    """Symmetric certificate for sign/swap images of the quadratic strips."""

    if parameter_n < 1:
        raise ValueError("parameter_n must be positive")

    for swap in (False, True):
        for x_sign in (-1, 1):
            for y_sign in (-1, 1):
                candidate_target = signed_swap_point(target, x_sign, y_sign, swap)
                base = theorem3_quadratic_strip_certificate(candidate_target, parameter_n)
                if base is None:
                    continue

                certificate = sign_swap_certificate(base, target)
                if certificate is not None:
                    return certificate

    return None


def theorem3_certificates(
    target: Point,
    triples: Iterable[PythagoreanTriple],
) -> tuple[Certificate, ...]:
    """Return all signed Theorem 3 certificates from a supplied triple list."""

    certificates: list[Certificate] = []
    for triple in triples:
        for x_sign in (-1, 1):
            for y_sign in (-1, 1):
                certificate = theorem3_certificate(target, triple, x_sign, y_sign)
                if certificate is not None:
                    certificates.append(certificate)
    return tuple(certificates)


def consecutive_parameter_odd_axis_certificate(n: int) -> SharedLegAxisCertificate | None:
    """Certificate for every odd horizontal target n >= 3.

    The construction scales the Euclid triples with parameter pairs (n + 1, n)
    and (n, n - 1).  The scale factors (n - 1) / 2 and (n + 1) / 2 make their
    even legs equal to n(n^2 - 1), while their odd legs differ by n.
    """

    if n < 3 or n % 2 == 0:
        return None

    first_scale = (n - 1) // 2
    second_scale = (n + 1) // 2

    shared_leg = n * (n * n - 1)
    first_horizontal_leg = first_scale * (2 * n + 1)
    second_horizontal_leg = second_scale * (2 * n - 1)
    first_hypotenuse = first_scale * (2 * n * n + 2 * n + 1)
    second_hypotenuse = second_scale * (2 * n * n - 2 * n + 1)

    return SharedLegAxisCertificate(
        target_n=second_horizontal_leg - first_horizontal_leg,
        midpoint=(-first_horizontal_leg, shared_leg),
        shared_leg=shared_leg,
        first_horizontal_leg=first_horizontal_leg,
        second_horizontal_leg=second_horizontal_leg,
        first_hypotenuse=first_hypotenuse,
        second_hypotenuse=second_hypotenuse,
        relation="difference",
    )


def horizontal_axis_proof_certificate(n: int) -> Certificate | None:
    """Certificate supplied by the written proof for every horizontal n >= 3."""

    if n < 3:
        return None

    explicit = explicit_axis_certificate(n)
    if explicit is not None:
        return explicit

    if n % 2 == 0:
        return midpoint_axis_certificate(n)

    odd_record = consecutive_parameter_odd_axis_certificate(n)
    if odd_record is None:
        return None
    return odd_record.certificate


def axis_orbit_proof_certificate(target: Point) -> Certificate | None:
    """Symmetric axis certificate for horizontal or vertical targets with |n| >= 3."""

    g, h = target
    if h == 0 and abs(g) >= 3:
        base = horizontal_axis_proof_certificate(abs(g))
        if base is None:
            return None
        midpoint_x, midpoint_y = base.midpoint
        return Certificate(
            target=target,
            midpoint=((1 if g > 0 else -1) * midpoint_x, midpoint_y),
        )

    if g == 0 and abs(h) >= 3:
        base = horizontal_axis_proof_certificate(abs(h))
        if base is None:
            return None
        midpoint_x, midpoint_y = base.midpoint
        return Certificate(
            target=target,
            midpoint=(midpoint_y, (1 if h > 0 else -1) * midpoint_x),
        )

    return None


def box_twenty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 20."""

    for base_target, midpoint in BOX_TWENTY_RESIDUAL_CERTIFICATES.items():
        certificate = sign_swap_certificate(Certificate(base_target, midpoint), target)
        if certificate is not None:
            return certificate
    return None


def box_twenty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 20.

    One-step targets and known distance-three exceptions intentionally return
    None; the finite audit handles those cases separately.
    """

    g, h = target
    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(g), abs(h)) > 20:
        return None

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        box_twenty_residual_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    return None


def box_thirty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 30."""

    for base_target, midpoint in BOX_THIRTY_RESIDUAL_CERTIFICATES.items():
        certificate = sign_swap_certificate(Certificate(base_target, midpoint), target)
        if certificate is not None:
            return certificate
    return None


def box_thirty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 30.

    One-step targets and known distance-three exceptions intentionally return
    None; the finite audit handles those cases separately.
    """

    g, h = target
    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(g), abs(h)) > 30:
        return None

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        box_thirty_residual_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    return None


def box_forty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 40."""

    for base_target, midpoint in BOX_FORTY_RESIDUAL_CERTIFICATES.items():
        certificate = sign_swap_certificate(Certificate(base_target, midpoint), target)
        if certificate is not None:
            return certificate
    return None


def box_forty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 40.

    One-step targets and known distance-three exceptions intentionally return
    None; the finite audit handles those cases separately.
    """

    g, h = target
    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(g), abs(h)) > 40:
        return None

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        box_forty_residual_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    return None


def box_fifty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 50."""

    for base_target, midpoint in BOX_FIFTY_RESIDUAL_CERTIFICATES.items():
        certificate = sign_swap_certificate(Certificate(base_target, midpoint), target)
        if certificate is not None:
            return certificate
    return None


def box_fifty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 50.

    One-step targets and known distance-three exceptions intentionally return
    None; the finite audit handles those cases separately.
    """

    g, h = target
    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(g), abs(h)) > 50:
        return None

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        box_fifty_residual_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    return None


def box_sixty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 60."""

    for base_target, midpoint in BOX_SIXTY_RESIDUAL_CERTIFICATES.items():
        certificate = sign_swap_certificate(Certificate(base_target, midpoint), target)
        if certificate is not None:
            return certificate
    return None


def box_sixty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 60.

    One-step targets and known distance-three exceptions intentionally return
    None; the finite audit handles those cases separately.
    """

    g, h = target
    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(g), abs(h)) > 60:
        return None

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        box_sixty_residual_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    return None

"""Verification helpers for Pythagorean walks on Z^2.

The graph has an edge for a displacement (dx, dy) exactly when dx and dy are
both nonzero and dx^2 + dy^2 is a square.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
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
    gx, gy = target
    x, y = midpoint
    return edge_delta(x, y) and edge_delta(gx - x, gy - y)


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


def _residual_certificate_lookup(records: dict[Point, Point]) -> dict[Point, Certificate]:
    """Precompute sign/swap images for static residual certificate tables."""

    lookup: dict[Point, Certificate] = {}
    for base_target, midpoint in records.items():
        base_certificate = Certificate(base_target, midpoint)
        for orbit_target in sign_swap_orbit(base_target):
            if orbit_target in lookup:
                continue
            certificate = sign_swap_certificate(base_certificate, orbit_target)
            if certificate is None:
                raise AssertionError("residual table orbit lookup missed a target")
            lookup[orbit_target] = certificate
    return lookup


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


LatticePairMetadata = tuple[Point, Point, int, bool]


@cache
def _lattice_pair_metadata(
    direction_pairs: tuple[tuple[Point, Point], ...],
) -> tuple[LatticePairMetadata, ...]:
    """Cache determinant and primality for static lattice direction tables."""

    metadata: list[LatticePairMetadata] = []
    for first_direction, second_direction in direction_pairs:
        pair_determinant = abs(determinant(first_direction, second_direction))
        metadata.append(
            (
                first_direction,
                second_direction,
                pair_determinant,
                is_prime(pair_determinant),
            )
        )
    return tuple(metadata)


def _prime_determinant_lattice_certificate_with_determinant(
    target: Point,
    first_direction: Point,
    second_direction: Point,
    lattice_determinant: int,
) -> Certificate | None:
    gx, gy = target
    ux, uy = first_direction
    if (
        (gx % lattice_determinant != 0 or gy % lattice_determinant != 0)
        and (gx * uy - gy * ux) % lattice_determinant != 0
    ):
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
    ((3, 4), (160, 231)),
    ((4, 3), (231, 160)),
    ((4, -3), (231, -160)),
    ((3, -4), (160, -231)),
    ((3, -4), (280, -351)),
    ((4, -3), (351, -280)),
    ((4, 3), (351, 280)),
    ((3, 4), (280, 351)),
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
    ((15, -8), (572, -315)),
    ((8, -15), (315, -572)),
    ((8, 15), (315, 572)),
    ((15, 8), (572, 315)),
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
    ((15, 112), (28, 195)),
    ((112, -15), (195, -28)),
    ((112, 15), (195, 28)),
    ((15, -112), (28, -195)),
    ((119, -120), (120, -119)),
    ((119, 120), (120, 119)),
    ((15, -112), (32, -255)),
    ((112, -15), (255, -32)),
    ((112, 15), (255, 32)),
    ((15, 112), (32, 255)),
    ((60, 91), (161, 240)),
    ((91, 60), (240, 161)),
    ((91, -60), (240, -161)),
    ((60, -91), (161, -240)),
    ((72, -65), (275, -252)),
    ((65, 72), (252, 275)),
    ((65, -72), (252, -275)),
    ((72, 65), (275, 252)),
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


BOX_SEVENTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    **BOX_SIXTY_RESIDUAL_CERTIFICATES,
    (61, 7): (861, -1148),
    (61, 11): (21, 20),
    (61, 22): (21, -20),
    (61, 39): (45, -24),
    (61, 46): (-56, 90),
    (61, 48): (-16, 12),
    (61, 57): (-308, -435),
    (62, 19): (20, -21),
    (62, 33): (-110, -96),
    (62, 37): (18, -80),
    (62, 45): (-10, 24),
    (62, 49): (-210, -176),
    (63, 11): (-105, -88),
    (63, 23): (-189, -252),
    (64, 12): (20, -21),
    (64, 19): (24, 10),
    (64, 39): (8, 6),
    (64, 60): (4, -3),
    (65, 8): (-75, -40),
    (65, 11): (-75, -40),
    (65, 27): (-12, -9),
    (65, 35): (-195, 104),
    (65, 46): (-40, -42),
    (65, 50): (9, -40),
    (66, 34): (-222, -296),
    (66, 47): (24, 7),
    (67, 9): (-5, -12),
    (67, 35): (7, 24),
    (67, 49): (7, 24),
    (67, 65): (-308, -435),
    (68, 7): (20, 21),
    (68, 11): (-52, -39),
    (68, 15): (20, -21),
    (68, 20): (-100, -75),
    (68, 21): (20, -15),
    (68, 39): (8, -6),
    (68, 52): (-51, -68),
    (69, 9): (-36, -27),
    (69, 11): (-48, 55),
    (69, 32): (-6, -8),
    (69, 33): (9, -12),
    (69, 35): (21, -20),
    (69, 59): (36, 15),
    (70, 1): (10, -24),
    (70, 4): (-35, -84),
    (70, 8): (7, 24),
    (70, 16): (-35, -84),
    (70, 23): (840, -1081),
    (70, 47): (-714, 152),
    (70, 52): (-5, 12),
    (70, 66): (-40, -30),
}


UNIT_COORDINATE_500_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (38, 1): (8, -15),
    (79, 1): (-5, -12),
    (89, 1): (5, -12),
    (93, 1): (9, -12),
    (128, 1): (-40, 96),
    (136, 1): (16, -63),
    (151, 1): (-16653, 12604),
    (203, 1): (60, 25),
    (259, 1): (-2345, 804),
    (261, 1): (9, 40),
    (266, 1): (90, -56),
    (326, 1): (-37830, -28616),
    (353, 1): (24153, -32204),
    (371, 1): (-85, -132),
    (376, 1): (-240, 364),
    (389, 1): (104, 153),
    (392, 1): (-160, 231),
    (422, 1): (-6888, -5375),
    (436, 1): (16, 30),
    (441, 1): (21, -28),
    (473, 1): (-1435, -4080),
    (476, 1): (140, -51),
}


BOX_EIGHTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (71, 14): (-49, -168),
    (71, 25): (15, -8),
    (71, 46): (39, -80),
    (71, 61): (9815, -10872),
    (72, 25): (24, 45),
    (72, 35): (-24, 7),
    (73, 5): (48, -55),
    (73, 12): (-32, -24),
    (73, 34): (-488, -366),
    (73, 55): (52, -165),
    (74, 6): (-30, -72),
    (74, 19): (-36, -77),
    (74, 20): (42, -40),
    (74, 41): (-70, 24),
    (74, 50): (24, -70),
    (74, 65): (-2368, 345),
    (74, 69): (-36, -27),
    (75, 3): (15, -8),
    (75, 28): (-15, -20),
    (75, 42): (35, 12),
    (75, 46): (-45, 24),
    (76, 2): (-8, 15),
    (76, 3): (36, -27),
    (76, 30): (-24, -45),
    (76, 53): (12, 5),
    (76, 61): (-12, -5),
    (77, 15): (-28, -21),
    (77, 19): (-595, 204),
    (77, 24): (35, -120),
    (77, 27): (-35, 12),
    (77, 53): (5, -12),
    (77, 59): (-7, 24),
    (77, 64): (-3, 4),
    (78, 46): (6, -8),
    (78, 60): (30, 40),
    (78, 63): (-42, -56),
    (78, 73): (6, 8),
    (79, 6): (7, -24),
    (79, 31): (-956, -717),
    (79, 45): (7, 24),
    (79, 52): (-50, -120),
    (79, 63): (275, -252),
    (80, 12): (32, -24),
    (80, 15): (8, -6),
    (80, 41): (-40, -9),
    (80, 63): (32, -126),
    (80, 75): (-32, 60),
    (80, 79): (32, 24),
}


BOX_NINETY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (81, 19): (9, 40),
    (81, 47): (60, -25),
    (82, 11): (12, 35),
    (82, 24): (5, -12),
    (82, 59): (12, 35),
    (83, 18): (-216, -162),
    (83, 51): (216, -405),
    (84, 9): (36, -27),
    (84, 25): (12, -5),
    (84, 51): (8, -6),
    (84, 55): (24, 10),
    (84, 79): (36, 15),
    (84, 81): (4, -3),
    (85, 9): (-175, -60),
    (85, 19): (40, -9),
    (85, 26): (-1595, -1092),
    (85, 32): (15, 8),
    (85, 46): (-155, -372),
    (85, 65): (-812, -3315),
    (85, 74): (-195, -28),
    (86, 13): (20, -99),
    (86, 14): (456, -1330),
    (86, 18): (14, 48),
    (86, 60): (119, -120),
    (86, 69): (14, 48),
    (86, 81): (10, 24),
    (87, 34): (15, -20),
    (87, 35): (12, -5),
    (87, 50): (15, 20),
    (87, 86): (63, 16),
    (88, 7): (120, -119),
    (88, 34): (-8, -6),
    (88, 54): (8, -6),
    (88, 58): (24, 10),
    (88, 62): (12, 5),
    (88, 65): (40, -75),
    (89, 24): (-16, -12),
    (89, 25): (5, 12),
    (89, 29): (-11692, 8769),
    (89, 49): (33, -56),
    (89, 64): (-7, 24),
    (89, 78): (-455, 528),
    (89, 87): (-76, -57),
    (90, 7): (-120, 119),
    (90, 47): (30, -16),
    (90, 58): (-54, -72),
}


BOX_ONE_HUNDRED_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (91, 10): (4371, 3220),
    (91, 16): (-455, -504),
    (91, 17): (-8789, -3948),
    (91, 24): (-3584, 2688),
    (91, 27): (575, -1260),
    (91, 48): (-259, 888),
    (91, 53): (735, 1088),
    (91, 71): (3003, 8096),
    (92, 12): (308, 75),
    (92, 44): (12, 5),
    (92, 58): (-1404, -2747),
    (92, 63): (56, 90),
    (92, 73): (-1060, 1113),
    (93, 92): (-1767, -900),
    (94, 7): (376, -2193),
    (94, 20): (-221, -60),
    (94, 26): (6256, -8190),
    (94, 42): (-144, 858),
    (94, 50): (1590, 2120),
    (94, 58): (366, -488),
    (94, 71): (2632, 1551),
    (94, 75): (3572, -765),
    (94, 85): (1576, -2955),
    (94, 86): (5590, 2376),
    (95, 26): (-2040, -1222),
    (95, 34): (-1105, 1224),
    (95, 44): (63, -16),
    (95, 63): (-180, -189),
    (95, 71): (-325, -780),
    (95, 72): (-5665, -3792),
    (95, 91): (35, -84),
    (95, 93): (-3820, 2865),
    (96, 18): (12, 5),
    (96, 74): (1284, -535),
    (96, 83): (240, 100),
    (96, 90): (-2280, -117),
    (97, 32): (5152, -2664),
    (97, 87): (7337, 1716),
    (97, 95): (949, 2580),
    (98, 4): (-133, -156),
    (98, 10): (-462, -1040),
    (98, 29): (230, 504),
    (98, 58): (5928, 5146),
    (98, 87): (-4214, 552),
    (98, 90): (-126, 120),
    (99, 5): (-189, 180),
    (99, 10): (-2565, 2100),
    (99, 25): (1659, -2900),
    (99, 31): (-4620, -5029),
    (99, 51): (-265, 636),
    (99, 68): (714, 2552),
    (99, 73): (-2484, -2387),
    (100, 4): (-4040, 7575),
    (100, 15): (2160, 4959),
    (100, 34): (960, -9191),
    (100, 56): (3235, -7764),
    (100, 57): (56, 90),
    (100, 67): (-140, -171),
}


BOX_ONE_TEN_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (101, 6): (296, 222),
    (101, 15): (156, -117),
    (101, 16): (2390, 5736),
    (101, 71): (22940, -30381),
    (101, 98): (-760, -522),
    (101, 99): (4313, -40860),
    (102, 13): (126, -32),
    (102, 22): (2016, 270),
    (102, 26): (-41706, 39720),
    (102, 37): (18, 24),
    (102, 40): (29205, -5900),
    (102, 77): (-654, -35640),
    (102, 78): (936, 1190),
    (103, 15): (-1517, -156),
    (103, 18): (40, -198),
    (103, 28): (13312, -2784),
    (103, 34): (8008, -10506),
    (103, 50): (2079, 2600),
    (103, 67): (-22448, 30135),
    (103, 71): (280, -165),
    (103, 91): (1720, -1449),
    (104, 42): (-5880, 7182),
    (104, 47): (440, 99),
    (104, 49): (224, 168),
    (104, 80): (159, 212),
    (104, 84): (56, -105),
    (104, 86): (17292, -12805),
    (104, 93): (4888, -495),
    (105, 12): (-19530, 15456),
    (105, 24): (-1200, -900),
    (105, 31): (11025, -2800),
    (105, 37): (22680, -43127),
    (105, 76): (-23625, 1820),
    (105, 78): (385, 180),
    (105, 99): (10480, -15561),
    (106, 4): (4528, -3396),
    (106, 51): (3060, 10179),
    (106, 66): (1602, 2136),
    (106, 67): (126, -32),
    (106, 75): (5452, 1155),
    (106, 77): (-1680, 1925),
    (106, 94): (-46854, -10472),
    (106, 100): (-3815, 5328),
    (107, 13): (10728, 9685),
    (107, 21): (-4465, -3408),
    (107, 24): (1440, -420),
    (107, 55): (72, -65),
    (107, 83): (-2725, 34008),
    (107, 88): (315, -572),
    (107, 102): (-7725, 14976),
    (107, 106): (8352, -986),
    (108, 19): (684, -1463),
    (108, 61): (-720, 1540),
    (108, 65): (38040, -8559),
    (108, 83): (-21120, -49022),
    (109, 12): (-35, 120),
    (109, 40): (-18915, 14308),
    (109, 47): (1305, -1900),
    (109, 51): (-8151, -1368),
    (109, 90): (-91, -60),
    (109, 92): (159, 212),
    (110, 52): (-17490, -28424),
    (110, 53): (-12084, -7987),
    (110, 81): (1978, -1320),
    (110, 92): (33005, -11316),
}


BOX_ONE_TWENTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (111, 9): (1420, 7029),
    (111, 30): (-8529, 11372),
    (111, 61): (-2520, 3569),
    (111, 65): (-2760, -4807),
    (111, 75): (9615, -5128),
    (111, 103): (240, 275),
    (112, 9): (1232, -399),
    (112, 12): (567, 540),
    (112, 34): (1168, -876),
    (112, 51): (140, 147),
    (112, 55): (21112, -13920),
    (112, 68): (-156, -133),
    (112, 81): (-248, -465),
    (112, 94): (-308, 435),
    (112, 95): (-47520, 24140),
    (112, 99): (672, 1260),
    (112, 108): (32, 24),
    (113, 35): (-9432, -15865),
    (113, 37): (-18915, 14308),
    (113, 46): (-7, 24),
    (113, 58): (-160, -78),
    (113, 63): (9653, 33096),
    (113, 70): (-559, 840),
    (113, 108): (2068, -4176),
    (114, 13): (1206, 1608),
    (114, 29): (-11940, 2189),
    (114, 34): (3138, -4184),
    (114, 45): (-1998, -2664),
    (114, 88): (189, 648),
    (114, 98): (24354, -42120),
    (115, 9): (-11820, -12411),
    (115, 15): (52, 675),
    (115, 26): (-13160, 16074),
    (115, 29): (12400, -3195),
    (115, 55): (-900, -1925),
    (115, 61): (-24704, 33153),
    (115, 63): (3395, 8148),
    (115, 68): (-50, 120),
    (115, 78): (-341, 420),
    (115, 93): (135, 72),
    (115, 106): (16395, -8744),
    (116, 26): (-4024, 3018),
    (116, 33): (-3420, 10560),
    (116, 71): (1476, -1357),
    (116, 79): (3096, -3050),
    (116, 99): (636, -477),
    (116, 105): (-304, -570),
    (117, 11): (6105, -2484),
    (117, 17): (-12276, 5957),
    (117, 38): (576, 350),
    (117, 43): (-1044, -517),
    (117, 46): (-12243, 13024),
    (117, 69): (-20475, 13500),
    (117, 73): (-3015, -1232),
    (117, 90): (1456, 5310),
    (118, 11): (-3710, -1584),
    (118, 25): (-50, 120),
    (118, 26): (2328, 18746),
    (118, 47): (-22448, 30135),
    (118, 51): (954, -1272),
    (118, 59): (-3422, 2640),
    (118, 86): (-46632, 19430),
    (118, 98): (17598, -23464),
    (118, 102): (-800, -1122),
    (118, 116): (-23325, 12440),
    (118, 117): (-4466, 8712),
    (119, 9): (135, 72),
    (119, 11): (-8169, -7780),
    (119, 25): (-21829, 31140),
    (119, 27): (308, 75),
    (119, 38): (-11305, -27132),
    (119, 48): (-5600, -17052),
    (119, 62): (39, 80),
    (119, 69): (17199, 46368),
    (119, 75): (4396, -7065),
    (119, 93): (483, 720),
    (119, 104): (273, -736),
    (119, 116): (159, 212),
    (120, 11): (12432, -23074),
    (120, 18): (-38640, -47196),
}


BOX_ONE_THIRTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (121, 4): (-3266, -4512),
    (121, 17): (3300, -1411),
    (121, 35): (4005, 2948),
    (121, 50): (576, 350),
    (121, 57): (396, 297),
    (121, 69): (7268, -24435),
    (121, 87): (1581, -1008),
    (121, 91): (9333, -6344),
    (121, 97): (3553, 396),
    (121, 119): (85, -204),
    (122, 22): (-294, -21608),
    (122, 23): (-18582, 24776),
    (122, 44): (369, 1640),
    (122, 78): (-6566, -2088),
    (122, 79): (-238, -240),
    (122, 96): (320, -240),
    (122, 114): (5850, -22440),
    (123, 36): (-4389, 26352),
    (123, 56): (-675, 816),
    (123, 68): (-11100, -8512),
    (123, 100): (-567, 1020),
    (123, 107): (159, 212),
    (124, 27): (-100, -105),
    (124, 38): (7600, 6195),
    (124, 39): (-4536, 11223),
    (124, 71): (684, -3040),
    (124, 74): (16872, -4921),
    (124, 85): (-104, -1350),
    (124, 90): (3204, 47472),
    (124, 98): (-336, -385),
    (124, 113): (-2976, -15232),
    (125, 5): (825, 260),
    (125, 14): (240, -238),
    (125, 16): (-495, -1472),
    (125, 53): (29645, -3432),
    (125, 61): (10653, 10396),
    (125, 70): (-3808, -3150),
    (125, 74): (2600, 4662),
    (125, 91): (1113, -1184),
    (125, 101): (309, -412),
    (125, 108): (-11484, 19488),
    (126, 22): (29526, -5368),
    (126, 31): (2076, -865),
    (126, 43): (3276, 33043),
    (126, 46): (-4098, 5464),
    (127, 10): (47271, -45020),
    (127, 18): (5447, 35196),
    (127, 33): (22204, -29403),
    (127, 70): (15631, -7308),
    (127, 72): (-21608, -15840),
    (127, 75): (-1160, 2175),
    (127, 88): (1026, -13832),
    (127, 93): (11160, 5049),
    (127, 117): (260, 273),
    (128, 24): (-14432, -9576),
    (128, 78): (4860, -8073),
    (128, 95): (-304, -570),
    (128, 120): (320, -240),
    (129, 7): (-6171, 10472),
    (129, 8): (-831, 1108),
    (129, 20): (309, -412),
    (129, 21): (-9387, 2384),
    (129, 26): (-3663, -7084),
    (129, 27): (-4536, 11223),
    (129, 90): (-46935, 16092),
    (129, 92): (-567, 1020),
    (129, 128): (39, 80),
    (130, 16): (-3266, -4512),
    (130, 22): (-6126, -8168),
    (130, 54): (-13200, -40194),
    (130, 57): (-5036, 3777),
    (130, 92): (15265, -7980),
    (130, 100): (690, 304),
    (130, 105): (6916, 2145),
    (130, 107): (-2460, -781),
    (130, 113): (44460, 7553),
}


BOX_ONE_FORTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (131, 14): (-133, -156),
    (131, 27): (-3213, -3240),
    (131, 28): (1001, -6468),
    (131, 38): (456, -190),
    (131, 53): (1671, 2228),
    (131, 92): (-43, 924),
    (131, 102): (-800, 1122),
    (131, 119): (-24805, 7392),
    (132, 51): (-308, 435),
    (132, 67): (-7920, 23552),
    (132, 68): (7188, -20965),
    (132, 81): (8832, 15776),
    (132, 87): (2860, -3168),
    (132, 93): (2860, -7161),
    (132, 94): (-1008, -3055),
    (132, 95): (1980, 400),
    (132, 115): (1632, 3060),
    (133, 8): (-441, -1960),
    (133, 11): (15753, -11704),
    (133, 18): (616, -1638),
    (133, 29): (43165, -3720),
    (133, 33): (23485, -13728),
    (133, 73): (-5180, -1887),
    (133, 78): (-2835, -5148),
    (133, 101): (4840, 21021),
    (133, 102): (1640, -8118),
    (133, 124): (1456, 960),
    (133, 125): (13, -84),
    (133, 130): (5005, -1716),
    (134, 9): (5402, 3960),
    (134, 18): (-34, 288),
    (134, 39): (-238, -240),
    (134, 47): (110, -96),
    (134, 70): (14, 48),
    (134, 73): (-1026, -368),
    (134, 91): (3686, -9048),
    (134, 98): (374, 168),
    (134, 121): (24, -143),
    (134, 130): (25944, 35530),
    (135, 13): (-4965, -6620),
    (135, 43): (4371, 3220),
    (135, 49): (-2736, -323),
    (135, 62): (-14040, -11970),
    (135, 87): (-4845, -1988),
    (135, 101): (-18180, 38885),
    (136, 7): (-26520, 24640),
    (136, 14): (-29120, -12936),
    (136, 22): (-260, -825),
    (136, 30): (80, -60),
    (136, 78): (-1736, 1023),
    (136, 104): (-1235, 1932),
    (136, 117): (9416, 11235),
    (136, 131): (-2424, 707),
    (137, 35): (-91, -60),
    (137, 42): (-2320, -882),
    (137, 65): (-1320, 689),
    (137, 72): (17633, -23256),
    (137, 82): (-424, -318),
    (137, 103): (15204, 33847),
    (138, 18): (1656, 1242),
    (138, 22): (864, 990),
    (138, 53): (1380, 253),
    (138, 66): (-3192, -2006),
    (138, 87): (-19992, -38369),
    (138, 118): (3960, -6578),
    (139, 31): (7, -24),
    (139, 35): (51, 140),
    (139, 52): (75, 100),
    (139, 59): (-4385, 10524),
    (139, 73): (-1316, 2013),
    (139, 84): (209, -1140),
    (139, 109): (-11088, 745),
    (139, 112): (22525, -11040),
    (140, 2): (-4060, -768),
    (140, 15): (108, -45),
    (140, 16): (308, -144),
    (140, 32): (159, 212),
    (140, 46): (-40660, 24651),
    (140, 47): (300, 125),
    (140, 85): (-924, 2080),
    (140, 94): (31388, 43680),
    (140, 104): (3234, 26312),
    (140, 109): (1848, -11786),
    (140, 123): (4560, -10944),
    (140, 127): (-10500, 8800),
    (140, 132): (-260, -288),
    (140, 135): (-280, 450),
}


BOX_ONE_FIFTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (141, 2): (261, -348),
    (141, 14): (-19008, 39294),
    (141, 30): (21, -20),
    (141, 37): (24, -7),
    (141, 39): (-1364, -477),
    (141, 56): (-31779, 38380),
    (141, 63): (21945, -12740),
    (141, 74): (-5355, 16104),
    (141, 75): (-1208, -2265),
    (141, 87): (889, -3048),
    (141, 91): (6045, -3224),
    (141, 129): (-17227, 25680),
    (141, 131): (-27, 36),
    (141, 133): (1680, -1127),
    (142, 15): (-33408, 29295),
    (142, 28): (-13685, -23436),
    (142, 31): (20892, -8705),
    (142, 50): (4158, -7480),
    (142, 71): (32470, 29256),
    (142, 91): (40194, -8120),
    (142, 92): (-1392, -3220),
    (142, 122): (-19488, 21866),
    (143, 6): (2400, -1170),
    (143, 28): (-91, -60),
    (143, 29): (-1677, 164),
    (143, 30): (4959, 2160),
    (143, 42): (23903, -41340),
    (143, 63): (8883, 11844),
    (143, 82): (-3360, -5822),
    (143, 106): (1007, -1224),
    (143, 110): (-1032, 14774),
    (143, 111): (-38940, 44955),
    (143, 126): (-1072, -8946),
    (143, 131): (-38857, -8580),
    (144, 19): (18744, 1370),
    (144, 27): (-3600, -2415),
    (144, 37): (-28284, 37712),
    (144, 50): (40800, -6660),
    (144, 70): (72, -65),
    (144, 89): (-4728, 6304),
    (144, 111): (-6600, -1856),
    (144, 135): (21840, -35100),
    (145, 49): (-12180, 1885),
    (145, 53): (4005, 2948),
    (145, 64): (-495, -1472),
    (145, 76): (75, 100),
    (145, 102): (19240, 31062),
    (145, 106): (-3855, 2056),
    (145, 119): (-41615, 408),
    (145, 134): (-25935, -12580),
    (145, 139): (-35, 120),
    (146, 5): (-11550, 9680),
    (146, 10): (90, 400),
    (146, 21): (4416, 1485),
    (146, 24): (8096, -6528),
    (146, 31): (-2190, 5104),
    (146, 68): (-12720, -44044),
    (146, 110): (-1150, 13200),
    (147, 2): (-9408, 8694),
    (147, 6): (-645, 812),
    (147, 15): (6615, 4180),
    (147, 20): (-40320, 45240),
    (147, 46): (75, 100),
    (147, 50): (1995, 2660),
    (147, 61): (-897, 496),
    (147, 87): (-10661, 36552),
    (147, 109): (10395, 6148),
    (147, 134): (-47040, -15106),
    (147, 135): (-189, 180),
    (148, 12): (8840, 3927),
    (148, 38): (7332, -28249),
    (148, 40): (-900, -1925),
    (148, 51): (108, -45),
    (148, 53): (17292, -12805),
    (148, 81): (-100, -105),
    (148, 82): (268, 201),
    (148, 100): (-7076, 5307),
    (148, 121): (-8880, 1876),
    (148, 130): (88, 105),
    (148, 138): (728, -1254),
    (149, 35): (-48151, 20160),
    (149, 36): (261, -348),
    (149, 43): (-17451, 4432),
    (149, 46): (3405, 1816),
    (149, 77): (1689, 2252),
    (149, 94): (221, -60),
    (149, 98): (3224, 7350),
    (149, 104): (10640, -35316),
    (149, 118): (429, 460),
    (149, 120): (1391, 5640),
    (149, 123): (-711, 9348),
    (150, 6): (3870, -5160),
    (150, 23): (-1560, -4081),
    (150, 51): (-550, 480),
    (150, 56): (-135, -324),
    (150, 84): (-19530, 15456),
    (150, 92): (-22881, 30800),
    (150, 103): (90, 400),
}


BOX_ONE_SIXTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (151, 34): (-5336, -2550),
    (151, 49): (63, 1984),
    (151, 64): (-4728, 6304),
    (151, 83): (3976, -4257),
    (151, 86): (-3776, -6450),
    (151, 103): (-260, 651),
    (151, 121): (180, -299),
    (151, 127): (-2948, -4005),
    (151, 131): (-10925, -912),
    (151, 147): (-14240, 20559),
    (152, 4): (14472, 15040),
    (152, 6): (-308, 435),
    (152, 21): (-260, -288),
    (152, 59): (-20680, 19899),
    (152, 60): (737, -2184),
    (152, 69): (7344, 6075),
    (152, 83): (-11440, 4578),
    (152, 106): (-5568, 1624),
    (152, 113): (-2208, 644),
    (152, 122): (708, -295),
    (153, 28): (5148, -8400),
    (153, 33): (7425, -2088),
    (153, 39): (932, 699),
    (153, 60): (-135, -324),
    (153, 65): (-4095, 3900),
    (153, 80): (16470, 14960),
    (153, 88): (-22881, 30800),
    (153, 115): (4320, 5671),
    (153, 117): (16065, -14248),
    (153, 143): (-9675, 5508),
    (154, 9): (-24704, 33153),
    (154, 30): (1666, 1680),
    (154, 37): (-2772, 5605),
    (154, 38): (-15006, 11408),
    (154, 48): (-3266, -4512),
    (154, 53): (-22092, 49181),
    (154, 54): (-630, 11016),
    (154, 87): (-2576, 3255),
    (154, 93): (6750, -8160),
    (154, 101): (22410, 11336),
    (154, 106): (29760, 4498),
    (154, 118): (-2142, -23360),
    (154, 128): (3234, -1312),
    (155, 11): (-1672, 1575),
    (155, 12): (12110, 28704),
    (155, 18): (-12248, -9186),
    (155, 21): (-18900, 45753),
    (155, 52): (189, 340),
    (155, 59): (11859, 15812),
    (155, 63): (56, -105),
    (155, 72): (26400, 5940),
    (155, 79): (3795, -1400),
    (155, 149): (-20680, 13113),
    (156, 35): (576, 350),
    (156, 63): (-1736, -1302),
    (156, 92): (-2169, 9640),
    (156, 109): (-1716, -16687),
    (156, 120): (8736, 1352),
    (156, 126): (4020, -26784),
    (156, 129): (22620, 48177),
    (156, 146): (1368, 651),
    (157, 2): (6240, 158),
    (157, 19): (184, -345),
    (157, 27): (-42291, 5712),
    (157, 47): (-299, 180),
    (157, 50): (33925, 36900),
    (157, 92): (4125, 7268),
    (157, 110): (-6968, 22110),
    (157, 117): (-4491, -5988),
    (157, 154): (-800, -1122),
    (158, 2): (198, -40),
    (158, 12): (-117, -240),
    (158, 13): (1106, -6192),
    (158, 23): (-1738, 6120),
    (158, 37): (33162, -44216),
    (158, 41): (-46740, -14839),
    (158, 51): (-6200, -2805),
    (158, 62): (6054, 8072),
    (158, 79): (-6162, 4720),
    (158, 90): (-1170, -2400),
    (158, 104): (-6532, 9024),
    (158, 113): (-34252, 25689),
    (158, 121): (-1482, -1160),
    (158, 126): (6840, -43050),
    (158, 155): (308, 75),
    (159, 6): (1071, 272),
    (159, 7): (6039, 10248),
    (159, 49): (483, -644),
    (159, 52): (-567, 1020),
    (159, 99): (324, 243),
    (159, 137): (375, 200),
    (159, 141): (236, 177),
    (159, 150): (18744, 1370),
    (159, 154): (7056, 4158),
    (160, 24): (-1404, 1197),
    (160, 30): (-288, -384),
    (160, 82): (-8060, -1425),
    (160, 89): (33480, -12361),
    (160, 93): (29920, 1038),
    (160, 126): (10800, -35190),
    (160, 150): (17920, -39000),
    (160, 158): (46360, -31842),
}


BOX_ONE_SEVENTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (161, 10): (105, 100),
    (161, 16): (43995, -36872),
    (161, 27): (13, -84),
    (161, 34): (105, -56),
    (161, 47): (-30156, 4667),
    (161, 53): (1421, 4872),
    (161, 65): (-22791, -16960),
    (161, 82): (560, -1518),
    (161, 86): (-672, -754),
    (161, 87): (11501, -24168),
    (161, 139): (3128, 4095),
    (161, 151): (1176, 343),
    (162, 35): (-2412, -4165),
    (162, 38): (42, -144),
    (162, 94): (5202, -6936),
    (163, 14): (-14397, 19196),
    (163, 25): (20068, 26565),
    (163, 27): (28, -45),
    (163, 46): (8008, 10506),
    (163, 48): (32558, 44400),
    (163, 95): (2295, 1100),
    (163, 126): (39347, 18396),
    (163, 130): (-10469, 4560),
    (163, 153): (15228, 2121),
    (163, 157): (2368, 345),
    (164, 5): (-32956, -46545),
    (164, 22): (6644, 4983),
    (164, 48): (308, -144),
    (164, 51): (-1552, -18786),
    (164, 69): (864, -360),
    (164, 91): (35588, -15141),
    (164, 103): (-7116, -9488),
    (164, 105): (-3276, -2793),
    (164, 113): (200, -210),
    (164, 118): (-760, -522),
    (164, 125): (-24168, 11501),
    (164, 155): (312, 266),
    (165, 47): (-1296, 1995),
    (165, 58): (-576, -1482),
    (165, 78): (-13475, -1560),
    (165, 85): (9405, -2244),
    (165, 106): (-6435, -12852),
    (165, 138): (7480, -10350),
    (166, 15): (-23754, 30240),
    (166, 36): (1995, 1296),
    (166, 55): (9780, -1793),
    (166, 59): (-4814, 6048),
    (166, 63): (374, 168),
    (166, 85): (1020, 3757),
    (166, 102): (432, -810),
    (166, 109): (156, 133),
    (166, 119): (-5538, -7384),
    (167, 9): (23172, -17379),
    (167, 12): (16836, 19152),
    (167, 25): (21171, 28228),
    (167, 40): (966, -920),
    (167, 56): (80, -60),
    (167, 63): (572, 315),
    (167, 74): (95, 228),
    (167, 82): (2415, 1768),
    (167, 105): (16147, 26796),
    (167, 133): (300, 589),
    (167, 156): (130, 840),
    (168, 18): (-1404, 1197),
    (168, 19): (432, 5824),
    (168, 50): (15960, 24206),
    (168, 51): (-4144, 4692),
    (168, 53): (11484, -12960),
    (168, 97): (-17472, 30096),
    (168, 102): (18816, -2912),
    (168, 110): (-840, 704),
    (168, 125): (-22632, 15785),
    (168, 141): (-3312, 3795),
    (168, 151): (17952, 37111),
    (168, 158): (6720, -328),
    (168, 162): (-960, 1008),
    (169, 14): (-143, 924),
    (169, 23): (-22035, -29380),
    (169, 38): (23104, 3990),
    (169, 67): (633, 844),
    (169, 79): (-260, 651),
    (169, 81): (-936, -24327),
    (169, 94): (5016, 7990),
    (169, 119): (7029, -2380),
    (169, 138): (1664, -1710),
    (169, 151): (3117, 4156),
    (169, 161): (-3212, -35259),
    (170, 8): (-4345, 3792),
    (170, 18): (35090, -6384),
    (170, 21): (-600, -1827),
    (170, 38): (90, 56),
    (170, 52): (20090, -3600),
    (170, 64): (-3510, 3496),
    (170, 77): (2850, 680),
    (170, 92): (40625, 28500),
    (170, 97): (1490, 3576),
    (170, 130): (7130, 2160),
    (170, 143): (5270, 12648),
    (170, 148): (-11235, 27520),
    (170, 167): (-14110, 336),
}


BOX_ONE_EIGHTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (171, 35): (-6321, -18900),
    (171, 49): (38316, -20295),
    (171, 51): (-9072, -3425),
    (171, 55): (351, -1560),
    (171, 64): (-22881, 30800),
    (171, 100): (-1920, 560),
    (171, 104): (12441, -6440),
    (171, 128): (-60, -32),
    (171, 132): (6750, -14896),
    (171, 147): (7315, -3420),
    (172, 13): (-29172, -27104),
    (172, 26): (40, -198),
    (172, 28): (7984, -5988),
    (172, 36): (-260, -288),
    (172, 89): (3840, -25456),
    (172, 91): (-40232, 5226),
    (172, 107): (5152, 1020),
    (172, 120): (-1428, -279),
    (172, 138): (-2688, 5850),
    (172, 149): (1920, 1904),
    (172, 161): (312, 266),
    (172, 162): (-8892, 6960),
    (173, 22): (29576, -22182),
    (173, 31): (6840, 4675),
    (173, 35): (19173, 43160),
    (173, 41): (-37228, 27921),
    (173, 48): (1581, -1008),
    (173, 84): (-11132, 8976),
    (173, 97): (5360, 2613),
    (173, 126): (-3675, -1260),
    (173, 136): (572, 96),
    (173, 137): (-532, -855),
    (173, 141): (-14740, 20025),
    (173, 150): (144, -270),
    (173, 171): (-135, -324),
    (174, 39): (-10980, 18239),
    (174, 53): (156, 133),
    (174, 61): (-5220, 6669),
    (174, 68): (261, -348),
    (174, 70): (864, 990),
    (174, 77): (-150, -616),
    (174, 95): (1974, 1880),
    (174, 100): (159, 212),
    (174, 172): (-2466, 3288),
    (175, 19): (1275, 160),
    (175, 20): (-260, -288),
    (175, 23): (-30381, 22940),
    (175, 40): (4305, 2296),
    (175, 46): (5215, 12516),
    (175, 51): (10115, 24276),
    (175, 74): (-22640, -5094),
    (175, 117): (-22540, 6237),
    (175, 121): (7923, -24464),
    (175, 130): (-600, -2210),
    (175, 165): (-24656, -31155),
    (176, 14): (56, -105),
    (176, 19): (-23140, -6141),
    (176, 23): (-26964, 6848),
    (176, 33): (-40, -30),
    (176, 39): (-260, -288),
    (176, 68): (159, 212),
    (176, 108): (8816, -2412),
    (176, 116): (80, 396),
    (176, 124): (-10432, 7824),
    (176, 130): (308, 75),
    (176, 137): (14916, -19888),
    (176, 165): (-1984, -63),
    (177, 10): (672, -90),
    (177, 39): (29925, 3000),
    (177, 55): (4389, -1340),
    (177, 73): (405, -252),
    (177, 94): (744, -1850),
    (177, 112): (4257, 860),
    (177, 129): (4437, 21216),
    (177, 139): (69, -92),
    (177, 147): (16225, -14868),
    (177, 153): (-600, -1827),
    (177, 160): (3927, -8840),
    (177, 164): (6240, 9180),
    (177, 174): (-175, -15312),
    (178, 2): (-702, 560),
    (178, 19): (19558, -9144),
    (178, 37): (6006, 4408),
    (178, 48): (-110, 264),
    (178, 50): (4600, 3450),
    (178, 58): (23586, -31448),
    (178, 98): (490, -168),
    (178, 119): (-20262, -34384),
    (178, 128): (-43712, 32784),
    (178, 139): (-12282, 3160),
    (178, 156): (4130, 1416),
    (178, 174): (330, 288),
    (179, 20): (18120, -24160),
    (179, 34): (11424, -12818),
    (179, 37): (7604, -5703),
    (179, 49): (43071, -32120),
    (179, 111): (25724, -19293),
    (179, 112): (-15405, 11800),
    (179, 135): (-13096, 24555),
    (179, 166): (42936, 17890),
    (180, 11): (2640, 1036),
    (180, 14): (-828, -896),
    (180, 27): (9900, 8640),
    (180, 94): (-2520, -1677),
    (180, 116): (-675, 816),
    (180, 119): (720, -448),
}


BOX_ONE_NINETY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (181, 5): (300, 125),
    (181, 32): (-399, -1600),
    (181, 138): (-2320, -882),
    (181, 154): (616, 462),
    (181, 156): (-43, 924),
    (181, 175): (-11204, 8403),
    (182, 17): (-15006, 11408),
    (182, 20): (-609, 6380),
    (182, 27): (-16968, 28251),
    (182, 32): (12180, 41168),
    (182, 34): (-4000, 5610),
    (182, 48): (-28288, 31584),
    (182, 54): (-968, 2574),
    (182, 61): (5642, -7320),
    (182, 83): (-36190, 5712),
    (182, 90): (-31080, -35190),
    (182, 92): (-2992, -4140),
    (182, 95): (22386, 45920),
    (182, 96): (45632, 13824),
    (182, 106): (6510, -10064),
    (182, 109): (-9828, 5365),
    (182, 123): (-390, -432),
    (182, 129): (-14740, 20025),
    (182, 139): (7280, 3675),
    (182, 142): (30030, 3256),
    (183, 2): (9735, -17908),
    (183, 26): (-19824, -7150),
    (183, 33): (-2261, 8700),
    (183, 46): (-897, 496),
    (183, 66): (-20880, 4550),
    (183, 70): (-6321, -18900),
    (183, 77): (23340, -35399),
    (183, 80): (-6336, 11880),
    (183, 98): (783, 11340),
    (183, 109): (-15405, 11800),
    (183, 117): (2211, 6552),
    (183, 144): (2583, 1144),
    (183, 171): (-8772, -21321),
    (184, 24): (6624, -2760),
    (184, 29): (7656, 5633),
    (184, 39): (46440, -46053),
    (184, 41): (20592, -15265),
    (184, 43): (-18260, 7728),
    (184, 67): (-1160, 2175),
    (184, 88): (-201, 268),
    (184, 116): (-260, -69),
    (184, 126): (-10640, 7308),
    (184, 133): (-44616, -3887),
    (184, 139): (26904, -21350),
    (184, 141): (-5336, -2550),
    (184, 146): (3360, -2236),
    (184, 153): (-1256, -2355),
    (184, 165): (1680, -225),
    (184, 171): (-2376, -3525),
    (185, 15): (-420, -513),
    (185, 16): (-205, -4200),
    (185, 19): (-3895, -9348),
    (185, 47): (3165, 22148),
    (185, 50): (4200, -21850),
    (185, 86): (600, -910),
    (185, 104): (18368, 2460),
    (185, 119): (33372, 15635),
    (185, 125): (-14740, 20025),
    (185, 138): (-135, -324),
    (185, 141): (35805, -37260),
    (185, 161): (23460, -6307),
    (185, 182): (-2415, -1768),
    (186, 2): (240, -70),
    (186, 37): (23664, -8323),
    (186, 43): (-10650, -24080),
    (186, 57): (130, 840),
    (186, 83): (-276, -4757),
    (186, 111): (54, -240),
    (186, 135): (-804, 335),
    (186, 147): (342, 280),
    (186, 184): (-6600, -1856),
    (187, 14): (-30381, 22940),
    (187, 25): (-14945, -3300),
    (187, 39): (-5525, 8580),
    (187, 49): (1755, -1400),
    (187, 56): (-1700, 672),
    (187, 69): (-13608, -17331),
    (187, 78): (-7821, -10428),
    (187, 112): (9372, -7904),
    (187, 116): (159, 212),
    (187, 122): (20955, -6604),
    (187, 125): (-4620, -3751),
    (187, 140): (-2816, 3360),
    (187, 143): (-7557, 10076),
    (187, 144): (24640, -26076),
    (187, 147): (-765, 32508),
    (187, 172): (-8840, -9792),
    (187, 174): (-16368, 5850),
    (187, 185): (-261, 1160),
    (188, 14): (-4300, -651),
    (188, 40): (308, 75),
    (188, 45): (-2664, 16320),
    (188, 52): (-1255, 3012),
    (188, 53): (308, 75),
    (188, 77): (308, -819),
    (188, 84): (-340, 255),
    (188, 91): (-2496, 3328),
    (188, 100): (-2992, -4140),
    (188, 103): (10296, -11753),
    (188, 116): (-456, -217),
    (188, 123): (4180, -2871),
    (188, 133): (7608, 10144),
    (188, 142): (-25576, 19182),
    (188, 150): (-15228, -8880),
    (188, 157): (236, 177),
    (188, 159): (20988, -30441),
    (188, 170): (-10452, 1595),
    (188, 172): (-39948, 16645),
    (188, 173): (312, 266),
    (188, 185): (-1300, -8400),
    (189, 19): (-156, -133),
    (189, 33): (10864, 6273),
    (189, 38): (-4032, 1110),
    (189, 52): (-1341, 1788),
    (189, 55): (-336, -385),
    (189, 62): (-504, -78),
    (189, 69): (-8791, -9360),
    (189, 79): (105, -56),
    (189, 85): (3360, 3105),
    (189, 100): (-1155, 6300),
    (189, 149): (-3627, -1364),
    (189, 157): (-21756, 24705),
    (189, 179): (-46704, 6255),
    (190, 17): (-16380, 39785),
    (190, 52): (3502, -29664),
    (190, 68): (-14690, -16272),
    (190, 75): (3600, -4125),
    (190, 88): (126, -32),
    (190, 103): (4690, 1608),
    (190, 126): (-440, 4830),
    (190, 142): (-25160, -3498),
    (190, 144): (-728, -480),
    (190, 173): (49374, -30832),
    (190, 182): (-20880, 4550),
    (190, 186): (2990, 3696),
    (190, 187): (-12350, -8664),
}


BOX_TWENTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(BOX_TWENTY_RESIDUAL_CERTIFICATES)
BOX_THIRTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(BOX_THIRTY_RESIDUAL_CERTIFICATES)
BOX_FORTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(BOX_FORTY_RESIDUAL_CERTIFICATES)
BOX_FIFTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(BOX_FIFTY_RESIDUAL_CERTIFICATES)
BOX_SIXTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(BOX_SIXTY_RESIDUAL_CERTIFICATES)
BOX_SEVENTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(BOX_SEVENTY_RESIDUAL_CERTIFICATES)
UNIT_COORDINATE_500_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    UNIT_COORDINATE_500_RESIDUAL_CERTIFICATES
)
BOX_EIGHTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(BOX_EIGHTY_RESIDUAL_CERTIFICATES)
BOX_NINETY_RESIDUAL_LOOKUP = _residual_certificate_lookup(BOX_NINETY_RESIDUAL_CERTIFICATES)
BOX_ONE_HUNDRED_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_ONE_HUNDRED_RESIDUAL_CERTIFICATES
)
BOX_ONE_TEN_RESIDUAL_LOOKUP = _residual_certificate_lookup(BOX_ONE_TEN_RESIDUAL_CERTIFICATES)
BOX_ONE_TWENTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_ONE_TWENTY_RESIDUAL_CERTIFICATES
)
BOX_ONE_THIRTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_ONE_THIRTY_RESIDUAL_CERTIFICATES
)
BOX_ONE_FORTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_ONE_FORTY_RESIDUAL_CERTIFICATES
)
BOX_ONE_FIFTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_ONE_FIFTY_RESIDUAL_CERTIFICATES
)
BOX_ONE_SIXTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_ONE_SIXTY_RESIDUAL_CERTIFICATES
)
BOX_ONE_SEVENTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_ONE_SEVENTY_RESIDUAL_CERTIFICATES
)
BOX_ONE_EIGHTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_ONE_EIGHTY_RESIDUAL_CERTIFICATES
)
BOX_ONE_NINETY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_ONE_NINETY_RESIDUAL_CERTIFICATES
)


def first_lattice_certificate(
    target: Point,
    direction_pairs: Iterable[tuple[Point, Point]],
) -> Certificate | None:
    """Return the first two-edge lattice certificate from a list of pairs."""

    for first_direction, second_direction, pair_determinant, determinant_is_prime in (
        _lattice_pair_metadata(tuple(direction_pairs))
    ):
        if determinant_is_prime:
            certificate = _prime_determinant_lattice_certificate_with_determinant(
                target,
                first_direction,
                second_direction,
                pair_determinant,
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


@cache
def determinant_seven_lattice_certificate(target: Point) -> Certificate | None:
    """Two-step certificate for the 3-4-5 determinant-seven congruence families.

    The first pair covers targets with g + h divisible by 7.  The second pair
    covers targets with g - h divisible by 7.  If the target is a scalar
    multiple of one of the basis directions, the target is already one step
    from the origin and this two-step certificate constructor returns None.
    """

    return first_lattice_certificate(target, DETERMINANT_SEVEN_DIRECTION_PAIRS)


@cache
def determinant_thirteen_lattice_certificate(target: Point) -> Certificate | None:
    """Two-step certificate for determinant-thirteen lattice families.

    These 3-4-5 and 8-15-17 direction pairs cover targets with
    g congruent to one of +/-3h or +/-4h modulo 13, except for scalar
    multiples of the basis directions, which are already one-step targets.
    """

    return first_lattice_certificate(target, DETERMINANT_THIRTEEN_DIRECTION_PAIRS)


@cache
def determinant_seventeen_lattice_certificate(target: Point) -> Certificate | None:
    """Two-step certificate for determinant-seventeen lattice families.

    These direction pairs cover targets with g congruent to one of
    +/-5h or +/-7h modulo 17, except for scalar multiples of the basis
    directions, which are already one-step targets.
    """

    return first_lattice_certificate(target, DETERMINANT_SEVENTEEN_DIRECTION_PAIRS)


@cache
def small_prime_lattice_certificate(target: Point) -> Certificate | None:
    """Two-step certificate for additional small prime-determinant families.

    The encoded table covers the residue lines g/h congruent to:
    - +/-5 and +/-9 modulo 23;
    - +/-3 and +/-10 modulo 31;
    - +/-10 and +/-11 modulo 37;
    - +/-1 modulo 41;
    - +/-10, +/-13, +/-15, and +/-20 modulo 43;
    - +/-4, +/-7, +/-11, +/-12, +/-17, and +/-20 modulo 47;
    - +/-14 and +/-19 modulo 53;
    - +/-16 and +/-21 modulo 67;
    - +/-13, +/-17, +/-28, and +/-30 modulo 73;
    - +/-8, +/-19, +/-31, and +/-35 modulo 83;
    - +/-13 and +/-41 modulo 89;
    - +/-22 and +/-34 modulo 107;
    - +/-45 and +/-46 modulo 109;
    - +/-54 and +/-69 modulo 149;
    - +/-14, +/-19, +/-33, +/-56, +/-66, and +/-69 modulo 157;
    - +/-18, +/-34, +/-48, and +/-56 modulo 173;
    - +/-12 and +/-15 modulo 179;
    - +/-13, +/-44, +/-87, and +/-90 modulo 191;
    - +/-86 and +/-92 modulo 193;
    - +/-51 and +/-91 modulo 211;
    - +/-1 modulo 239;
    - +/-101 and +/-105 modulo 241;
    - +/-31 and +/-81 modulo 251;
    - +/-32 and +/-42 modulo 269.
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


def half_leg_strip_target_certificate(
    target: Point,
    direction: Point,
) -> Certificate | None:
    """Recognize half-leg strip targets for one odd-even direction."""

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")

    u, v = direction
    if u % 2 == 0 or v % 2 != 0:
        raise ValueError("direction must have odd first coordinate and even second coordinate")

    g, q = target
    if q == 0 or (q * (1 - q)) % v != 0:
        return None

    constant = u * q * (1 - q) // v
    linear_coefficient = q * (u * u - v)
    quadratic_coefficient = u * v * (1 + 2 * v - u * u) // 4

    candidate_parameters: set[int] = set()
    target_offset = g - constant
    if quadratic_coefficient == 0:
        if linear_coefficient != 0 and target_offset % linear_coefficient == 0:
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
                for numerator in (-linear_coefficient + root, -linear_coefficient - root):
                    if numerator % denominator == 0:
                        candidate_parameters.add(numerator // denominator)

    for parameter_t in sorted(candidate_parameters):
        certificate = half_leg_strip_certificate(direction, q, parameter_t)
        if certificate is not None and certificate.target == target:
            return certificate

    return None


def half_leg_strip_orbit_certificate(
    target: Point,
    direction: Point,
) -> Certificate | None:
    """Symmetric target-facing certificate for half-leg strips."""

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")

    u, v = direction
    if u % 2 == 0 or v % 2 != 0:
        raise ValueError("direction must have odd first coordinate and even second coordinate")

    for swap in (False, True):
        for x_sign in (-1, 1):
            for y_sign in (-1, 1):
                candidate_target = signed_swap_point(target, x_sign, y_sign, swap)
                base = half_leg_strip_target_certificate(candidate_target, direction)
                if base is None:
                    continue

                certificate = sign_swap_certificate(base, target)
                if certificate is not None:
                    return certificate

    return None


def half_leg_unit_coordinate_certificate(direction: Point, t: int) -> Certificate | None:
    """Unit-coordinate specialization of the half-leg strip family."""

    return half_leg_strip_certificate(direction, q=1, t=t)


def half_leg_unit_coordinate_target_certificate(
    target: Point,
    direction: Point,
) -> Certificate | None:
    """Recognize unit-coordinate half-leg strip targets for one direction."""

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")

    u, v = direction
    if u % 2 == 0 or v % 2 != 0:
        raise ValueError("direction must have odd first coordinate and even second coordinate")

    g, h = target
    if h != 1:
        return None

    linear_coefficient = u * u - v
    quadratic_coefficient = u * v * (1 + 2 * v - u * u) // 4

    candidate_parameters: set[int] = set()
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
                for numerator in (-linear_coefficient + root, -linear_coefficient - root):
                    if numerator % denominator == 0:
                        candidate_parameters.add(numerator // denominator)

    for parameter_t in sorted(candidate_parameters):
        certificate = half_leg_unit_coordinate_certificate(direction, parameter_t)
        if certificate is not None and certificate.target == target:
            return certificate

    return None


def half_leg_unit_coordinate_orbit_certificate(
    target: Point,
    direction: Point,
) -> Certificate | None:
    """Symmetric target-facing certificate for unit-coordinate half-leg strips."""

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")

    u, v = direction
    if u % 2 == 0 or v % 2 != 0:
        raise ValueError("direction must have odd first coordinate and even second coordinate")

    for swap in (False, True):
        for x_sign in (-1, 1):
            for y_sign in (-1, 1):
                candidate_target = signed_swap_point(target, x_sign, y_sign, swap)
                base = half_leg_unit_coordinate_target_certificate(
                    candidate_target,
                    direction,
                )
                if base is None:
                    continue

                certificate = sign_swap_certificate(base, target)
                if certificate is not None:
                    return certificate

    return None


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


def affine_consecutive_hypotenuse_target_certificate(
    target: Point,
    m: int,
) -> Certificate | None:
    """Recognize affine consecutive-hypotenuse strip targets for a fixed m."""

    if m < 2:
        raise ValueError("m must be at least 2")

    g, q = target
    if q == 0:
        return None

    odd_leg = 2 * m - 1
    even_leg = 2 * m * (m - 1)
    hypotenuse = m * m + (m - 1) * (m - 1)
    if (q * (1 - q)) % even_leg != 0:
        return None

    offset = odd_leg * q * (1 - q) // even_leg
    denominator = hypotenuse * q
    if (g - offset) % denominator != 0:
        return None

    return affine_consecutive_hypotenuse_certificate(
        m,
        q,
        (g - offset) // denominator,
    )


def affine_consecutive_hypotenuse_orbit_certificate(
    target: Point,
    m: int,
) -> Certificate | None:
    """Symmetric target-facing affine consecutive-hypotenuse certificate."""

    if m < 2:
        raise ValueError("m must be at least 2")

    certificate = affine_consecutive_hypotenuse_target_certificate(target, m)
    if certificate is not None:
        return certificate

    swapped_target = (target[1], target[0])
    swapped_certificate = affine_consecutive_hypotenuse_target_certificate(
        swapped_target,
        m,
    )
    if swapped_certificate is None:
        return None

    midpoint_x, midpoint_y = swapped_certificate.midpoint
    return Certificate(target=target, midpoint=(midpoint_y, midpoint_x))


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


@cache
def box_twenty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 20."""

    return BOX_TWENTY_RESIDUAL_LOOKUP.get(target)


@cache
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


@cache
def box_thirty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 30."""

    return BOX_THIRTY_RESIDUAL_LOOKUP.get(target)


@cache
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


@cache
def box_forty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 40."""

    return BOX_FORTY_RESIDUAL_LOOKUP.get(target)


@cache
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


@cache
def box_fifty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 50."""

    return BOX_FIFTY_RESIDUAL_LOOKUP.get(target)


@cache
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


@cache
def box_sixty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 60."""

    return BOX_SIXTY_RESIDUAL_LOOKUP.get(target)


@cache
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


@cache
def box_seventy_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 70."""

    return BOX_SEVENTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_seventy_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 70.

    One-step targets and known distance-three exceptions intentionally return
    None; the finite audit handles those cases separately.
    """

    g, h = target
    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(g), abs(h)) > 70:
        return None

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        box_seventy_residual_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    return None


@cache
def unit_coordinate_500_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit of unit-coordinate targets."""

    return UNIT_COORDINATE_500_RESIDUAL_LOOKUP.get(target)


@cache
def unit_coordinate_500_audit_certificate(target: Point) -> Certificate | None:
    """Certificate for the finite audit of unit-coordinate targets up to 500."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 500:
        return None
    if abs(target[0]) != 1 and abs(target[1]) != 1:
        return None

    for constructor in (
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        unit_coordinate_multiple_of_five_certificate,
        diagonal_pythagorean_multiplier_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    for direction in (
        (3, 4),
        (5, 12),
        (7, 24),
        (9, 40),
        (11, 60),
        (13, 84),
        (15, 8),
        (15, 112),
        (17, 144),
        (21, 20),
        (-3, 4),
        (5, -12),
    ):
        certificate = half_leg_unit_coordinate_orbit_certificate(target, direction)
        if certificate is not None:
            return certificate

    for m in range(2, 18):
        certificate = affine_consecutive_hypotenuse_orbit_certificate(target, m)
        if certificate is not None:
            return certificate

    for parameter_n in range(1, 17):
        certificate = theorem3_quadratic_strip_orbit_certificate(target, parameter_n)
        if certificate is not None:
            return certificate

    return unit_coordinate_500_residual_certificate(target)


@cache
def box_eighty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 80."""

    return BOX_EIGHTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_eighty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 80."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 80:
        return None

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        unit_coordinate_500_audit_certificate,
        diagonal_pythagorean_multiplier_certificate,
        box_seventy_residual_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    for direction in (
        (3, 4),
        (5, 12),
        (7, 24),
        (9, 40),
        (11, 60),
        (13, 84),
        (15, 8),
        (15, 112),
        (17, 144),
        (21, 20),
        (-3, 4),
        (5, -12),
    ):
        certificate = half_leg_strip_orbit_certificate(target, direction)
        if certificate is not None:
            return certificate

    for m in range(2, 18):
        certificate = affine_consecutive_hypotenuse_orbit_certificate(target, m)
        if certificate is not None:
            return certificate

    for parameter_n in range(1, 17):
        certificate = theorem3_quadratic_strip_orbit_certificate(target, parameter_n)
        if certificate is not None:
            return certificate

    return box_eighty_residual_certificate(target)


@cache
def box_ninety_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 90."""

    return BOX_NINETY_RESIDUAL_LOOKUP.get(target)


@cache
def box_ninety_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 90."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 90:
        return None

    certificate = box_eighty_audit_certificate(target)
    if certificate is not None:
        return certificate

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        unit_coordinate_500_audit_certificate,
        diagonal_pythagorean_multiplier_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    for direction in (
        (3, 4),
        (5, 12),
        (7, 24),
        (9, 40),
        (11, 60),
        (13, 84),
        (15, 8),
        (15, 112),
        (17, 144),
        (21, 20),
        (-3, 4),
        (5, -12),
    ):
        certificate = half_leg_strip_orbit_certificate(target, direction)
        if certificate is not None:
            return certificate

    for m in range(2, 18):
        certificate = affine_consecutive_hypotenuse_orbit_certificate(target, m)
        if certificate is not None:
            return certificate

    for parameter_n in range(1, 17):
        certificate = theorem3_quadratic_strip_orbit_certificate(target, parameter_n)
        if certificate is not None:
            return certificate

    return box_ninety_residual_certificate(target)


@cache
def box_one_hundred_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 100."""

    return BOX_ONE_HUNDRED_RESIDUAL_LOOKUP.get(target)


@cache
def box_one_hundred_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 100."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 100:
        return None

    certificate = box_ninety_audit_certificate(target)
    if certificate is not None:
        return certificate

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        unit_coordinate_500_audit_certificate,
        diagonal_pythagorean_multiplier_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    for direction in (
        (3, 4),
        (5, 12),
        (7, 24),
        (9, 40),
        (11, 60),
        (13, 84),
        (15, 8),
        (15, 112),
        (17, 144),
        (21, 20),
        (-3, 4),
        (5, -12),
    ):
        certificate = half_leg_strip_orbit_certificate(target, direction)
        if certificate is not None:
            return certificate

    for m in range(2, 18):
        certificate = affine_consecutive_hypotenuse_orbit_certificate(target, m)
        if certificate is not None:
            return certificate

    for parameter_n in range(1, 17):
        certificate = theorem3_quadratic_strip_orbit_certificate(target, parameter_n)
        if certificate is not None:
            return certificate

    return box_one_hundred_residual_certificate(target)


@cache
def box_one_ten_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 110."""

    return BOX_ONE_TEN_RESIDUAL_LOOKUP.get(target)


@cache
def box_one_ten_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 110."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 110:
        return None

    certificate = box_one_hundred_audit_certificate(target)
    if certificate is not None:
        return certificate

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        unit_coordinate_500_audit_certificate,
        diagonal_pythagorean_multiplier_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    for direction in (
        (3, 4),
        (5, 12),
        (7, 24),
        (9, 40),
        (11, 60),
        (13, 84),
        (15, 8),
        (15, 112),
        (17, 144),
        (21, 20),
        (-3, 4),
        (5, -12),
    ):
        certificate = half_leg_strip_orbit_certificate(target, direction)
        if certificate is not None:
            return certificate

    for m in range(2, 18):
        certificate = affine_consecutive_hypotenuse_orbit_certificate(target, m)
        if certificate is not None:
            return certificate

    for parameter_n in range(1, 17):
        certificate = theorem3_quadratic_strip_orbit_certificate(target, parameter_n)
        if certificate is not None:
            return certificate

    return box_one_ten_residual_certificate(target)


@cache
def box_one_twenty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 120."""

    return BOX_ONE_TWENTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_one_twenty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 120."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 120:
        return None

    certificate = box_one_ten_audit_certificate(target)
    if certificate is not None:
        return certificate

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        unit_coordinate_500_audit_certificate,
        diagonal_pythagorean_multiplier_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    for direction in (
        (3, 4),
        (5, 12),
        (7, 24),
        (9, 40),
        (11, 60),
        (13, 84),
        (15, 8),
        (15, 112),
        (17, 144),
        (21, 20),
        (-3, 4),
        (5, -12),
    ):
        certificate = half_leg_strip_orbit_certificate(target, direction)
        if certificate is not None:
            return certificate

    for m in range(2, 18):
        certificate = affine_consecutive_hypotenuse_orbit_certificate(target, m)
        if certificate is not None:
            return certificate

    for parameter_n in range(1, 17):
        certificate = theorem3_quadratic_strip_orbit_certificate(target, parameter_n)
        if certificate is not None:
            return certificate

    return box_one_twenty_residual_certificate(target)


@cache
def box_one_thirty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 130."""

    return BOX_ONE_THIRTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_one_thirty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 130."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 130:
        return None

    certificate = box_one_twenty_audit_certificate(target)
    if certificate is not None:
        return certificate

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        unit_coordinate_500_audit_certificate,
        diagonal_pythagorean_multiplier_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    for direction in (
        (3, 4),
        (5, 12),
        (7, 24),
        (9, 40),
        (11, 60),
        (13, 84),
        (15, 8),
        (15, 112),
        (17, 144),
        (21, 20),
        (-3, 4),
        (5, -12),
    ):
        certificate = half_leg_strip_orbit_certificate(target, direction)
        if certificate is not None:
            return certificate

    for m in range(2, 18):
        certificate = affine_consecutive_hypotenuse_orbit_certificate(target, m)
        if certificate is not None:
            return certificate

    for parameter_n in range(1, 17):
        certificate = theorem3_quadratic_strip_orbit_certificate(target, parameter_n)
        if certificate is not None:
            return certificate

    return box_one_thirty_residual_certificate(target)


@cache
def box_one_forty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 140."""

    return BOX_ONE_FORTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_one_forty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 140."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 140:
        return None

    certificate = box_one_thirty_audit_certificate(target)
    if certificate is not None:
        return certificate

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        unit_coordinate_500_audit_certificate,
        diagonal_pythagorean_multiplier_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    for direction in (
        (3, 4),
        (5, 12),
        (7, 24),
        (9, 40),
        (11, 60),
        (13, 84),
        (15, 8),
        (15, 112),
        (17, 144),
        (21, 20),
        (-3, 4),
        (5, -12),
    ):
        certificate = half_leg_strip_orbit_certificate(target, direction)
        if certificate is not None:
            return certificate

    for m in range(2, 18):
        certificate = affine_consecutive_hypotenuse_orbit_certificate(target, m)
        if certificate is not None:
            return certificate

    for parameter_n in range(1, 17):
        certificate = theorem3_quadratic_strip_orbit_certificate(target, parameter_n)
        if certificate is not None:
            return certificate

    return box_one_forty_residual_certificate(target)


@cache
def box_one_fifty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 150."""

    return BOX_ONE_FIFTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_one_fifty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 150."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 150:
        return None

    certificate = box_one_forty_audit_certificate(target)
    if certificate is not None:
        return certificate

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        unit_coordinate_500_audit_certificate,
        diagonal_pythagorean_multiplier_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    for direction in (
        (3, 4),
        (5, 12),
        (7, 24),
        (9, 40),
        (11, 60),
        (13, 84),
        (15, 8),
        (15, 112),
        (17, 144),
        (21, 20),
        (-3, 4),
        (5, -12),
    ):
        certificate = half_leg_strip_orbit_certificate(target, direction)
        if certificate is not None:
            return certificate

    for m in range(2, 18):
        certificate = affine_consecutive_hypotenuse_orbit_certificate(target, m)
        if certificate is not None:
            return certificate

    for parameter_n in range(1, 17):
        certificate = theorem3_quadratic_strip_orbit_certificate(target, parameter_n)
        if certificate is not None:
            return certificate

    return box_one_fifty_residual_certificate(target)


@cache
def box_one_sixty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 160."""

    return BOX_ONE_SIXTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_one_sixty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 160."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 160:
        return None

    certificate = box_one_fifty_audit_certificate(target)
    if certificate is not None:
        return certificate

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        unit_coordinate_500_audit_certificate,
        diagonal_pythagorean_multiplier_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    for direction in (
        (3, 4),
        (5, 12),
        (7, 24),
        (9, 40),
        (11, 60),
        (13, 84),
        (15, 8),
        (15, 112),
        (17, 144),
        (21, 20),
        (-3, 4),
        (5, -12),
    ):
        certificate = half_leg_strip_orbit_certificate(target, direction)
        if certificate is not None:
            return certificate

    for m in range(2, 18):
        certificate = affine_consecutive_hypotenuse_orbit_certificate(target, m)
        if certificate is not None:
            return certificate

    for parameter_n in range(1, 17):
        certificate = theorem3_quadratic_strip_orbit_certificate(target, parameter_n)
        if certificate is not None:
            return certificate

    return box_one_sixty_residual_certificate(target)


@cache
def box_one_seventy_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 170."""

    return BOX_ONE_SEVENTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_one_seventy_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 170."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 170:
        return None

    certificate = box_one_sixty_audit_certificate(target)
    if certificate is not None:
        return certificate

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        unit_coordinate_500_audit_certificate,
        diagonal_pythagorean_multiplier_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    for direction in (
        (3, 4),
        (5, 12),
        (7, 24),
        (9, 40),
        (11, 60),
        (13, 84),
        (15, 8),
        (15, 112),
        (17, 144),
        (21, 20),
        (-3, 4),
        (5, -12),
    ):
        certificate = half_leg_strip_orbit_certificate(target, direction)
        if certificate is not None:
            return certificate

    for m in range(2, 18):
        certificate = affine_consecutive_hypotenuse_orbit_certificate(target, m)
        if certificate is not None:
            return certificate

    for parameter_n in range(1, 17):
        certificate = theorem3_quadratic_strip_orbit_certificate(target, parameter_n)
        if certificate is not None:
            return certificate

    return box_one_seventy_residual_certificate(target)


@cache
def box_one_eighty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 180."""

    return BOX_ONE_EIGHTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_one_eighty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 180."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 180:
        return None

    certificate = box_one_seventy_audit_certificate(target)
    if certificate is not None:
        return certificate

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        unit_coordinate_500_audit_certificate,
        diagonal_pythagorean_multiplier_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    for direction in (
        (3, 4),
        (5, 12),
        (7, 24),
        (9, 40),
        (11, 60),
        (13, 84),
        (15, 8),
        (15, 112),
        (17, 144),
        (21, 20),
        (-3, 4),
        (5, -12),
    ):
        certificate = half_leg_strip_orbit_certificate(target, direction)
        if certificate is not None:
            return certificate

    for m in range(2, 18):
        certificate = affine_consecutive_hypotenuse_orbit_certificate(target, m)
        if certificate is not None:
            return certificate

    for parameter_n in range(1, 17):
        certificate = theorem3_quadratic_strip_orbit_certificate(target, parameter_n)
        if certificate is not None:
            return certificate

    return box_one_eighty_residual_certificate(target)


@cache
def box_one_ninety_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 190."""

    return BOX_ONE_NINETY_RESIDUAL_LOOKUP.get(target)


@cache
def box_one_ninety_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 190."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 190:
        return None

    certificate = box_one_eighty_audit_certificate(target)
    if certificate is not None:
        return certificate

    for constructor in (
        axis_orbit_proof_certificate,
        determinant_seven_lattice_certificate,
        determinant_thirteen_lattice_certificate,
        determinant_seventeen_lattice_certificate,
        small_prime_lattice_certificate,
        two_one_ray_even_orbit_certificate,
        two_one_ray_explicit_base_orbit_certificate,
        unit_coordinate_500_audit_certificate,
        diagonal_pythagorean_multiplier_certificate,
    ):
        certificate = constructor(target)
        if certificate is not None:
            return certificate

    for direction in (
        (3, 4),
        (5, 12),
        (7, 24),
        (9, 40),
        (11, 60),
        (13, 84),
        (15, 8),
        (15, 112),
        (17, 144),
        (21, 20),
        (-3, 4),
        (5, -12),
    ):
        certificate = half_leg_strip_orbit_certificate(target, direction)
        if certificate is not None:
            return certificate

    for m in range(2, 18):
        certificate = affine_consecutive_hypotenuse_orbit_certificate(target, m)
        if certificate is not None:
            return certificate

    for parameter_n in range(1, 17):
        certificate = theorem3_quadratic_strip_orbit_certificate(target, parameter_n)
        if certificate is not None:
            return certificate

    return box_one_ninety_residual_certificate(target)

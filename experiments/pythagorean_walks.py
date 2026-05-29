"""Verification helpers for Pythagorean walks on Z^2.

The graph has an edge for a displacement (dx, dy) exactly when dx and dy are
both nonzero and dx^2 + dy^2 is a square.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from itertools import combinations
from math import gcd, isqrt, lcm
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


def positive_divisors(n: int) -> tuple[int, ...]:
    """Return all positive divisors of a positive integer."""

    if n <= 0:
        raise ValueError("n must be positive")

    remaining = n
    prime_powers: list[tuple[int, int]] = []
    exponent = 0
    while remaining % 2 == 0:
        remaining //= 2
        exponent += 1
    if exponent:
        prime_powers.append((2, exponent))

    candidate = 3
    while candidate * candidate <= remaining:
        exponent = 0
        while remaining % candidate == 0:
            remaining //= candidate
            exponent += 1
        if exponent:
            prime_powers.append((candidate, exponent))
        candidate += 2
    if remaining > 1:
        prime_powers.append((remaining, 1))

    divisors = [1]
    for prime, exponent in prime_powers:
        expanded: list[int] = []
        power = 1
        for _ in range(exponent + 1):
            expanded.extend(divisor * power for divisor in divisors)
            power *= prime
        divisors = expanded

    return tuple(sorted(divisors))


def prime_factors(n: int) -> tuple[int, ...]:
    """Return the distinct prime factors of a positive integer."""

    if n <= 0:
        raise ValueError("n must be positive")

    factors: list[int] = []
    remaining = n
    if remaining % 2 == 0:
        factors.append(2)
        while remaining % 2 == 0:
            remaining //= 2

    candidate = 3
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            factors.append(candidate)
            while remaining % candidate == 0:
                remaining //= candidate
        candidate += 2
    if remaining > 1:
        factors.append(remaining)

    return tuple(factors)


def squareclass_decomposition(n: int) -> tuple[int, int]:
    """Return ``(q, a)`` with ``n = q*a^2`` and q squarefree."""

    if n <= 0:
        raise ValueError("n must be positive")

    squareclass = 1
    square_part = 1
    remaining = n
    for prime in prime_factors(n):
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1
        if exponent % 2:
            squareclass *= prime
        square_part *= prime ** (exponent // 2)

    return (squareclass, square_part)


@cache
def squarefree_numbers(limit: int) -> tuple[int, ...]:
    """Positive squarefree integers up to a bound."""

    if limit < 1:
        raise ValueError("limit must be positive")

    return tuple(
        candidate
        for candidate in range(1, limit + 1)
        if squareclass_decomposition(candidate)[1] == 1
    )


def squarefree_divisors(n: int) -> tuple[int, ...]:
    """Positive squarefree divisors of a positive integer."""

    if n <= 0:
        raise ValueError("n must be positive")

    divisors = [1]
    for prime in prime_factors(n):
        divisors.extend(divisor * prime for divisor in tuple(divisors))
    return tuple(sorted(divisors))


def has_divisor_three_or_seven_mod_ten(n: int) -> bool:
    """Return whether a positive integer has a divisor 3 or 7 modulo 10."""

    return any(divisor % 10 in (3, 7) for divisor in positive_divisors(n))


def has_divisor_in_residue_classes(
    n: int,
    modulus: int,
    residues: Iterable[int],
) -> bool:
    """Return whether a positive integer has a divisor in given residue classes."""

    if modulus <= 0:
        raise ValueError("modulus must be positive")

    residue_set = {residue % modulus for residue in residues}
    return any(divisor % modulus in residue_set for divisor in positive_divisors(n))


def minimal_periodic_residue_classes(
    modulus: int,
    residues: Iterable[int],
) -> tuple[int, tuple[int, ...]]:
    """Compress residue classes modulo ``modulus`` to their smallest period."""

    if modulus <= 0:
        raise ValueError("modulus must be positive")

    normalized = tuple(sorted({residue % modulus for residue in residues}))
    for period in positive_divisors(modulus):
        folded = tuple(sorted({residue % period for residue in normalized}))
        lifted = tuple(
            residue
            for residue in range(modulus)
            if residue % period in folded
        )
        if lifted == normalized:
            return period, folded

    return modulus, normalized


def periodic_residue_union(
    period_residue_classes: Iterable[tuple[int, Iterable[int]]],
) -> tuple[int, tuple[int, ...]]:
    """Combine periodic residue-class criteria into one modulus."""

    modulus = 1
    normalized_classes: list[tuple[int, frozenset[int]]] = []
    for period, residues in period_residue_classes:
        if period <= 0:
            raise ValueError("period must be positive")

        residue_set = frozenset(residue % period for residue in residues)
        if not residue_set:
            continue

        normalized_classes.append((period, residue_set))
        modulus = lcm(modulus, period)

    return (
        modulus,
        tuple(
            residue
            for residue in range(modulus)
            if any(
                residue % period in residue_set
                for period, residue_set in normalized_classes
            )
        ),
    )


def all_prime_factors_one_or_nine_mod_ten(n: int) -> bool:
    """Return whether every prime factor is 1 or 9 modulo 10."""

    return all(prime % 10 in (1, 9) for prime in prime_factors(n))


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


DeltaSliceDirection = tuple[int, int, int, int, int]


@cache
def primitive_pythagorean_directions(
    max_parameter: int,
) -> tuple[DeltaSliceDirection, ...]:
    """Primitive signed Pythagorean directions up to a Euclid parameter bound.

    Each returned row is ``(u, v, c, a, b)``, where ``u^2 + v^2 = c^2`` and
    ``(u, v)`` is one signed/swapped orientation of the primitive direction
    generated by Euclid parameters ``a > b > 0``.
    """

    if max_parameter < 2:
        raise ValueError("max_parameter must be at least 2")

    directions: list[DeltaSliceDirection] = []
    seen: set[tuple[int, int, int]] = set()
    for a in range(2, max_parameter + 1):
        for b in range(1, a):
            if (a - b) % 2 == 0 or gcd(a, b) != 1:
                continue

            odd_leg = a * a - b * b
            even_leg = 2 * a * b
            hypotenuse = a * a + b * b
            for base_x, base_y in ((odd_leg, even_leg), (even_leg, odd_leg)):
                for x_sign in (-1, 1):
                    for y_sign in (-1, 1):
                        direction = (x_sign * base_x, y_sign * base_y, hypotenuse)
                        if direction in seen:
                            continue
                        seen.add(direction)
                        directions.append((*direction, a, b))

    directions.sort(key=lambda row: (row[2], abs(row[0]) + abs(row[1]), row[0], row[1]))
    return tuple(directions)


@cache
def signed_delta_values(limit: int) -> tuple[int, ...]:
    """Return signed length-difference candidates in increasing absolute size."""

    if limit < 0:
        raise ValueError("limit must be nonnegative")

    values = [0]
    for delta in range(1, limit + 1):
        values.extend((delta, -delta))
    return tuple(values)


@cache
def delta_slice_certificate(
    target: Point,
    max_parameter: int,
    max_abs_delta: int | None = None,
) -> Certificate | None:
    """Search the signed length-difference conic slice for a certificate.

    Let ``d = |OP| - |TP|`` be a signed integer.  If the first edge is
    ``P = K(u, v)`` with ``K > 0`` and ``u^2 + v^2 = c^2``, then a two-step
    certificate must satisfy

        2K(gu + hv - dc) = g^2 + h^2 - d^2.

    This bounded constructor tests that divisibility condition over primitive
    Pythagorean directions up to ``max_parameter`` and signed deltas up to
    ``max_abs_delta``.  It is a discovery/probing tool, not a theorem-level
    classification by itself.
    """

    target_norm_squared = target[0] * target[0] + target[1] * target[1]
    if target_norm_squared == 0:
        return None

    triangle_bound = isqrt(target_norm_squared)
    if max_abs_delta is None:
        delta_bound = triangle_bound
    else:
        if max_abs_delta < 0:
            raise ValueError("max_abs_delta must be nonnegative")
        delta_bound = min(max_abs_delta, triangle_bound)

    g, h = target
    for signed_delta in signed_delta_values(delta_bound):
        numerator = target_norm_squared - signed_delta * signed_delta
        if numerator <= 0 or numerator % 2 != 0:
            continue

        half_numerator = numerator // 2
        for u, v, hypotenuse, _parameter_a, _parameter_b in primitive_pythagorean_directions(
            max_parameter
        ):
            denominator = g * u + h * v - signed_delta * hypotenuse
            if denominator == 0 or half_numerator % denominator != 0:
                continue

            coefficient = half_numerator // denominator
            if coefficient <= 0:
                continue

            certificate = Certificate(
                target=target,
                midpoint=(coefficient * u, coefficient * v),
            )
            if certificate.valid():
                return certificate

    return None


def linear_delta_direction_certificate(
    target: Point,
    direction: Point,
    delta_coefficients: Point,
) -> Certificate | None:
    """Certificate from one direction and a linear signed-delta choice.

    Fix a legal Pythagorean direction ``(u, v)`` with hypotenuse ``c`` and set
    ``d = alpha*g + beta*h`` for target ``(g, h)``.  The signed-delta slice
    identity gives

        2K(gu + hv - dc) = g^2 + h^2 - d^2.

    Whenever this determines a positive integer ``K``, ``K(u, v)`` is tested as
    an exact two-step midpoint.  Fixed choices of ``direction`` and
    ``delta_coefficients`` define theorem-level infinite divisibility families.
    """

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")

    u, v = direction
    hypotenuse = isqrt(u * u + v * v)
    alpha, beta = delta_coefficients
    g, h = target
    signed_delta = alpha * g + beta * h
    numerator = g * g + h * h - signed_delta * signed_delta
    if numerator <= 0 or numerator % 2 != 0:
        return None

    denominator = g * u + h * v - signed_delta * hypotenuse
    if denominator == 0 or numerator % (2 * denominator) != 0:
        return None

    coefficient = numerator // (2 * denominator)
    if coefficient <= 0:
        return None

    certificate = Certificate(
        target=target,
        midpoint=(coefficient * u, coefficient * v),
    )
    if not certificate.valid():
        return None
    return certificate


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


def primitive_pythagorean_direction_gaussian_root(direction: Point) -> tuple[Point, Point]:
    """Return ``(root, unit)`` with ``direction = unit * root^2``.

    A primitive Pythagorean direction is a Gaussian square up to multiplication
    by one of the four units.  The root has norm equal to the direction length.
    """

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")
    if gcd(abs(direction[0]), abs(direction[1])) != 1:
        raise ValueError("direction must be primitive")

    hypotenuse = isqrt(direction[0] * direction[0] + direction[1] * direction[1])
    roots: list[Point] = []
    for real in range(1, isqrt(hypotenuse) + 1):
        imaginary_square = hypotenuse - real * real
        imaginary = isqrt(imaginary_square)
        if imaginary == 0 or imaginary * imaginary != imaginary_square:
            continue
        for base in ((real, imaginary), (imaginary, real)):
            for real_sign in (-1, 1):
                for imaginary_sign in (-1, 1):
                    candidate = (real_sign * base[0], imaginary_sign * base[1])
                    if candidate not in roots:
                        roots.append(candidate)

    units: tuple[Point, ...] = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for root in roots:
        root_square = gaussian_multiply(root, root)
        for unit in units:
            if gaussian_multiply(unit, root_square) == direction:
                return (root, unit)

    raise AssertionError("primitive Pythagorean direction had no Gaussian square root")


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


def ray_multiplier(target: Point, ray: Point) -> int | None:
    """Return the integer multiplier expressing ``target`` on ``ray``."""

    ray_x, ray_y = ray
    if ray_x == 0 and ray_y == 0:
        raise ValueError("ray must be nonzero")
    if determinant(ray, target) != 0:
        return None

    target_x, target_y = target
    if ray_x != 0:
        if target_x % ray_x != 0:
            return None
        multiplier = target_x // ray_x
    else:
        if target_y % ray_y != 0:
            return None
        multiplier = target_y // ray_y

    if (ray_x * multiplier, ray_y * multiplier) != target:
        return None
    return multiplier


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


@dataclass(frozen=True)
class ParallelDirectionFactorWitness:
    target: Point
    direction: Point
    factor: int
    determinant_leg: int
    other_leg: int
    scaled_hypotenuse: int
    second_length: int
    first_coefficient: int

    @property
    def midpoint(self) -> Point:
        u, v = self.direction
        return (self.first_coefficient * u, self.first_coefficient * v)

    @property
    def certificate(self) -> Certificate:
        return Certificate(target=self.target, midpoint=self.midpoint)


@dataclass(frozen=True)
class ParallelDirectionSquareclassSplitWitness:
    squareclass: int
    split_factor: int
    paired_split_factor: int
    factor_witness: ParallelDirectionFactorWitness

    @property
    def target(self) -> Point:
        return self.factor_witness.target

    @property
    def direction(self) -> Point:
        return self.factor_witness.direction

    @property
    def factor(self) -> int:
        return self.factor_witness.factor

    @property
    def midpoint(self) -> Point:
        return self.factor_witness.midpoint

    @property
    def signed_paired_split_factor(self) -> int:
        divisor = self.squareclass * self.split_factor
        determinant_leg = self.factor_witness.determinant_leg
        if determinant_leg % divisor != 0:
            raise AssertionError("determinant leg lost the requested split factor")
        return determinant_leg // divisor

    @property
    def certificate(self) -> Certificate:
        return self.factor_witness.certificate


@dataclass(frozen=True)
class PrimitiveRayParallelDirectionWitness:
    target: Point
    primitive: Point
    scale: int
    base_witness: ParallelDirectionFactorWitness

    @property
    def midpoint(self) -> Point:
        midpoint_x, midpoint_y = self.base_witness.midpoint
        return (self.scale * midpoint_x, self.scale * midpoint_y)

    @property
    def certificate(self) -> Certificate:
        return Certificate(target=self.target, midpoint=self.midpoint)


@dataclass(frozen=True)
class ParallelDirectionCoverWitnessCensus:
    max_coordinate: int
    max_parameter: int
    target_count: int
    uncovered_targets: tuple[Point, ...]
    direction_counts: tuple[tuple[Point, int], ...]
    factor_counts: tuple[tuple[int, int], ...]
    direction_factor_counts: tuple[tuple[Point, int, int], ...]


@dataclass(frozen=True)
class PythagoreanLatticePairWitness:
    target: Point
    first_direction: Point
    second_direction: Point
    determinant: int
    first_coefficient: int
    second_coefficient: int

    @property
    def midpoint(self) -> Point:
        ux, uy = self.first_direction
        return (self.first_coefficient * ux, self.first_coefficient * uy)

    @property
    def certificate(self) -> Certificate:
        return Certificate(target=self.target, midpoint=self.midpoint)


def standard_pythagorean_completion_factors(leg: int) -> tuple[int, ...]:
    """Factors of leg^2 giving the two signed standard completions of a leg."""

    absolute_leg = abs(leg)
    if absolute_leg == 0:
        return ()
    leg_square = absolute_leg * absolute_leg
    if absolute_leg % 2 == 1:
        factors = (1, leg_square)
    else:
        factors = (2, leg_square // 2)
    return tuple(dict.fromkeys(factors))


def parallel_direction_factor_witness(
    target: Point,
    direction: Point,
    factor: int,
) -> ParallelDirectionFactorWitness | None:
    """Return the Pythagorean-completion witness for one direction/factor."""

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")
    if factor <= 0:
        raise ValueError("factor must be positive")

    u, v = direction
    c = isqrt(u * u + v * v)
    target_x, target_y = target
    det_value = determinant(direction, target)
    if det_value == 0:
        return None

    determinant_square = det_value * det_value
    if determinant_square % factor != 0:
        return None

    paired_factor = determinant_square // factor
    factor_sum = factor + paired_factor
    factor_difference = paired_factor - factor
    if factor_sum % (2 * c) != 0 or factor_difference % 2 != 0:
        return None

    scaled_hypotenuse = factor_sum // 2
    other_leg = factor_difference // 2
    dot_product = target_x * u + target_y * v
    first_coefficient_numerator = other_leg + dot_product
    direction_norm = c * c
    if first_coefficient_numerator % direction_norm != 0:
        return None

    return ParallelDirectionFactorWitness(
        target=target,
        direction=direction,
        factor=factor,
        determinant_leg=det_value,
        other_leg=other_leg,
        scaled_hypotenuse=scaled_hypotenuse,
        second_length=scaled_hypotenuse // c,
        first_coefficient=first_coefficient_numerator // direction_norm,
    )


def parallel_direction_factor_certificate(
    target: Point,
    direction: Point,
    factor: int,
) -> Certificate | None:
    """Certificate with first step on a fixed Pythagorean direction.

    Let ``direction = U = (u, v)`` have length ``c`` and let the requested
    midpoint be ``rU``.  The second step is Pythagorean exactly when

        |target - rU|^2 = s^2.

    Writing ``A = target dot U`` and ``D = det(U, target)``, this is equivalent
    to

        (cs - (c^2 r - A))(cs + (c^2 r - A)) = D^2.

    A positive factor of ``D^2`` therefore determines a candidate ``r``.  This
    helper tests that exact candidate and returns the resulting certificate when
    both graph steps are nondegenerate.
    """

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")
    if factor <= 0:
        raise ValueError("factor must be positive")

    witness = parallel_direction_factor_witness(target, direction, factor)
    if witness is None:
        return None
    if witness.first_coefficient == 0:
        return None

    certificate = witness.certificate
    if not certificate.valid():
        return None
    return certificate


def parallel_direction_squareclass_split_witness(
    target: Point,
    direction: Point,
    squareclass: int,
    split_factor: int,
) -> ParallelDirectionSquareclassSplitWitness | None:
    """Fixed squareclass split of the determinant-leg completion factor.

    The factor tested is ``squareclass * split_factor^2``.  If it works, then
    the paired factor has the same squareclass, so the determinant leg has the
    form ``squareclass * split_factor * paired_split_factor``.
    """

    if squareclass <= 0:
        raise ValueError("squareclass must be positive")
    if squareclass_decomposition(squareclass) != (squareclass, 1):
        raise ValueError("squareclass must be squarefree")
    if split_factor <= 0:
        raise ValueError("split_factor must be positive")

    factor = squareclass * split_factor * split_factor
    factor_witness = parallel_direction_factor_witness(target, direction, factor)
    if factor_witness is None or factor_witness.first_coefficient == 0:
        return None
    if not factor_witness.certificate.valid():
        return None

    determinant_square = factor_witness.determinant_leg * factor_witness.determinant_leg
    paired_factor = determinant_square // factor
    if paired_factor % squareclass != 0:
        raise AssertionError("paired factor lost the requested squareclass")
    paired_split_factor = isqrt(paired_factor // squareclass)
    if squareclass * paired_split_factor * paired_split_factor != paired_factor:
        raise AssertionError("paired factor is not in the requested squareclass")

    return ParallelDirectionSquareclassSplitWitness(
        squareclass=squareclass,
        split_factor=split_factor,
        paired_split_factor=paired_split_factor,
        factor_witness=factor_witness,
    )


def parallel_direction_squareclass_split_certificate(
    target: Point,
    direction: Point,
    squareclass: int,
    split_factor: int,
) -> Certificate | None:
    """Certificate from one fixed determinant squareclass/split row."""

    witness = parallel_direction_squareclass_split_witness(
        target,
        direction,
        squareclass,
        split_factor,
    )
    if witness is None:
        return None
    return witness.certificate


def parallel_direction_squareclass_line_gaussian_numerator(
    direction: Point,
    squareclass: int,
    split_factor: int,
    signed_paired_split_factor: int,
) -> Point:
    """Return ``q * U * (a + ib)^2`` for a split-line row."""

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")
    if squareclass <= 0:
        raise ValueError("squareclass must be positive")
    if squareclass_decomposition(squareclass) != (squareclass, 1):
        raise ValueError("squareclass must be squarefree")
    if split_factor <= 0:
        raise ValueError("split_factor must be positive")
    if signed_paired_split_factor == 0:
        raise ValueError("signed_paired_split_factor must be nonzero")

    split_root = (split_factor, signed_paired_split_factor)
    split_square = gaussian_multiply(split_root, split_root)
    product = gaussian_multiply(direction, split_square)
    return (squareclass * product[0], squareclass * product[1])


def parallel_direction_squareclass_line_split_quotient(
    direction: Point,
    split_factor: int,
    signed_paired_split_factor: int,
) -> Point | None:
    """Return ``(a+ib)/conj(alpha)`` for ``direction = unit*alpha^2``."""

    if split_factor <= 0:
        raise ValueError("split_factor must be positive")
    if signed_paired_split_factor == 0:
        raise ValueError("signed_paired_split_factor must be nonzero")

    root, _unit = primitive_pythagorean_direction_gaussian_root(direction)
    conjugate_root = (root[0], -root[1])
    return gaussian_quotient_if_integer(
        (split_factor, signed_paired_split_factor),
        conjugate_root,
    )


def primitive_pythagorean_direction_conjugate_root_residue(
    direction: Point,
) -> tuple[int, int]:
    """Return ``(c, rho)`` for split roots divisible by ``conj(alpha)``.

    If ``direction = unit*alpha^2`` and ``c = norm(alpha)``, then
    ``a+i*b`` is divisible by ``conj(alpha)`` exactly when
    ``b == rho*a mod c``.
    """

    root, _unit = primitive_pythagorean_direction_gaussian_root(direction)
    root_real, root_imaginary = root
    hypotenuse = root_real * root_real + root_imaginary * root_imaginary
    residue = (-root_imaginary * pow(root_real % hypotenuse, -1, hypotenuse)) % (
        hypotenuse
    )
    if (residue * residue + 1) % hypotenuse != 0:
        raise AssertionError("conjugate-root residue is not a square root of -1")
    return (hypotenuse, residue)


def parallel_direction_squareclass_beta_split_root(
    direction: Point,
    beta: Point,
) -> Point:
    """Return ``conj(alpha) * beta`` for ``direction = unit*alpha^2``."""

    if beta == (0, 0):
        raise ValueError("beta must be nonzero")

    root, _unit = primitive_pythagorean_direction_gaussian_root(direction)
    conjugate_root = (root[0], -root[1])
    return gaussian_multiply(conjugate_root, beta)


def squareclass_beta_integral(squareclass: int, beta: Point) -> bool:
    """Return whether ``q*beta^2/2`` is a Gaussian integer."""

    if squareclass <= 0:
        raise ValueError("squareclass must be positive")
    if squareclass_decomposition(squareclass) != (squareclass, 1):
        raise ValueError("squareclass must be squarefree")
    if beta == (0, 0):
        raise ValueError("beta must be nonzero")

    beta_x, beta_y = beta
    if squareclass % 2 == 0:
        return True
    return (beta_x - beta_y) % 2 == 0


def beta_square_is_axis_degenerate(beta: Point) -> bool:
    """Return whether ``beta^2`` has a zero coordinate."""

    if beta == (0, 0):
        raise ValueError("beta must be nonzero")

    beta_x, beta_y = beta
    return beta_x == 0 or beta_y == 0 or abs(beta_x) == abs(beta_y)


def parallel_direction_squareclass_beta_quotient(
    direction: Point,
    squareclass: int,
    beta: Point,
) -> Point | None:
    """Unfiltered second-step quotient from the beta-parametrized family."""

    if squareclass <= 0:
        raise ValueError("squareclass must be positive")
    if squareclass_decomposition(squareclass) != (squareclass, 1):
        raise ValueError("squareclass must be squarefree")
    if beta == (0, 0):
        raise ValueError("beta must be nonzero")

    if not squareclass_beta_integral(squareclass, beta):
        return None

    _root, unit = primitive_pythagorean_direction_gaussian_root(direction)
    beta_square = gaussian_multiply(beta, beta)
    numerator = (squareclass * beta_square[0], squareclass * beta_square[1])

    return gaussian_multiply(unit, (numerator[0] // 2, numerator[1] // 2))


def parallel_direction_squareclass_beta_second_step(
    direction: Point,
    squareclass: int,
    beta: Point,
) -> Point | None:
    """Legal second edge from the beta-parametrized split-line family."""

    second_step = parallel_direction_squareclass_beta_quotient(
        direction,
        squareclass,
        beta,
    )
    if second_step is None:
        return None
    if beta_square_is_axis_degenerate(beta):
        return None
    if not edge_delta(*second_step):
        return None
    return second_step


def parallel_direction_squareclass_conjugate_ideal_split_roots(
    direction: Point,
    determinant_leg: int,
    squareclass: int,
) -> tuple[tuple[int, int, Point], ...]:
    """Legal split roots from the conjugate-root ideal and determinant level.

    Returned rows are ``(a, b, beta)`` with ``a > 0``, ``D = q*a*b``, and
    ``a+i*b = conj(alpha)*beta`` for ``direction = unit*alpha^2``.
    """

    if squareclass <= 0:
        raise ValueError("squareclass must be positive")
    if squareclass_decomposition(squareclass) != (squareclass, 1):
        raise ValueError("squareclass must be squarefree")
    if determinant_leg == 0 or determinant_leg % squareclass != 0:
        return ()

    hypotenuse, residue = primitive_pythagorean_direction_conjugate_root_residue(
        direction
    )
    split_product = determinant_leg // squareclass
    roots: list[tuple[int, int, Point]] = []
    for split_factor in positive_divisors(abs(split_product)):
        signed_paired_split_factor = split_product // split_factor
        if (signed_paired_split_factor - residue * split_factor) % hypotenuse != 0:
            continue
        beta = parallel_direction_squareclass_line_split_quotient(
            direction,
            split_factor,
            signed_paired_split_factor,
        )
        if beta is None:
            raise AssertionError("conjugate-root residue gave a nonintegral beta")
        if parallel_direction_squareclass_beta_second_step(
            direction,
            squareclass,
            beta,
        ) is None:
            continue
        roots.append((split_factor, signed_paired_split_factor, beta))
    return tuple(roots)


def parallel_direction_squareclass_beta_line_certificate(
    direction: Point,
    squareclass: int,
    beta: Point,
    first_coefficient: int,
) -> Certificate | None:
    """Certificate from the beta-parametrized split-line family."""

    second_step = parallel_direction_squareclass_beta_second_step(
        direction,
        squareclass,
        beta,
    )
    if second_step is None:
        return None

    u, v = direction
    midpoint = (first_coefficient * u, first_coefficient * v)
    target = (midpoint[0] + second_step[0], midpoint[1] + second_step[1])
    certificate = Certificate(target=target, midpoint=midpoint)
    if not certificate.valid():
        return None
    return certificate


def parallel_direction_squareclass_beta_target_coefficient(
    target: Point,
    direction: Point,
    squareclass: int,
    beta: Point,
) -> int | None:
    """First-step coefficient if a target lies on one beta split line."""

    second_step = parallel_direction_squareclass_beta_second_step(
        direction,
        squareclass,
        beta,
    )
    if second_step is None:
        return None

    quotient = gaussian_quotient_if_integer(
        (target[0] - second_step[0], target[1] - second_step[1]),
        direction,
    )
    if quotient is None or quotient[1] != 0:
        return None
    return quotient[0]


def parallel_direction_squareclass_beta_determinant_residue(
    direction: Point,
    squareclass: int,
    beta: Point,
) -> int | None:
    """Determinant level ``det(direction, W)`` of one legal beta split line."""

    second_step = parallel_direction_squareclass_beta_second_step(
        direction,
        squareclass,
        beta,
    )
    if second_step is None:
        return None
    return determinant(direction, second_step)


def parallel_direction_squareclass_beta_determinant_target_coefficient(
    target: Point,
    direction: Point,
    squareclass: int,
    beta: Point,
) -> int | None:
    """First-step coefficient from the determinant level of one beta split line."""

    second_step = parallel_direction_squareclass_beta_second_step(
        direction,
        squareclass,
        beta,
    )
    if second_step is None:
        return None
    if determinant(direction, target) != determinant(direction, second_step):
        return None

    return ray_multiplier(
        (target[0] - second_step[0], target[1] - second_step[1]),
        direction,
    )


def parallel_direction_squareclass_beta_determinant_target_certificate(
    target: Point,
    direction: Point,
    squareclass: int,
    beta: Point,
) -> Certificate | None:
    """Target-facing beta certificate using only the determinant line label."""

    first_coefficient = parallel_direction_squareclass_beta_determinant_target_coefficient(
        target,
        direction,
        squareclass,
        beta,
    )
    if first_coefficient is None:
        return None
    return parallel_direction_squareclass_beta_line_certificate(
        direction,
        squareclass,
        beta,
        first_coefficient,
    )


def parallel_direction_squareclass_conjugate_ideal_certificate(
    target: Point,
    direction: Point,
    squareclass: int,
) -> Certificate | None:
    """Target-facing certificate from conjugate-root ideal divisor roots."""

    determinant_leg = determinant(direction, target)
    for _split_factor, _signed_paired_split_factor, beta in (
        parallel_direction_squareclass_conjugate_ideal_split_roots(
            direction,
            determinant_leg,
            squareclass,
        )
    ):
        certificate = parallel_direction_squareclass_beta_determinant_target_certificate(
            target,
            direction,
            squareclass,
            beta,
        )
        if certificate is not None:
            return certificate
    return None


def parallel_direction_conjugate_ideal_split_roots(
    target: Point,
    direction: Point,
) -> tuple[tuple[int, int, int, Point], ...]:
    """All legal ``(q, a, b, beta)`` ideal rows for one target and direction."""

    determinant_leg = determinant(direction, target)
    if determinant_leg == 0:
        return ()

    roots: list[tuple[int, int, int, Point]] = []
    for squareclass in squarefree_divisors(abs(determinant_leg)):
        for split_factor, signed_paired_split_factor, beta in (
            parallel_direction_squareclass_conjugate_ideal_split_roots(
                direction,
                determinant_leg,
                squareclass,
            )
        ):
            roots.append(
                (
                    squareclass,
                    split_factor,
                    signed_paired_split_factor,
                    beta,
                )
            )
    return tuple(roots)


def parallel_direction_conjugate_ideal_certificate(
    target: Point,
    direction: Point,
) -> Certificate | None:
    """Exact fixed-direction split certificate over squarefree determinant divisors."""

    for squareclass, _split_factor, _signed_paired_split_factor, beta in (
        parallel_direction_conjugate_ideal_split_roots(target, direction)
    ):
        certificate = parallel_direction_squareclass_beta_determinant_target_certificate(
            target,
            direction,
            squareclass,
            beta,
        )
        if certificate is not None:
            return certificate
    return None


@cache
def parallel_direction_conjugate_ideal_cover_certificate(
    target: Point,
    max_parameter: int,
) -> Certificate | None:
    """Finite-direction exact split cover using conjugate-root divisor roots."""

    if max_parameter < 2:
        raise ValueError("max_parameter must be at least 2")

    for u, v, _hypotenuse, _parameter_a, _parameter_b in primitive_pythagorean_directions(
        max_parameter
    ):
        certificate = parallel_direction_conjugate_ideal_certificate(target, (u, v))
        if certificate is not None:
            return certificate
    return None


def parallel_direction_squareclass_beta_target_certificate(
    target: Point,
    direction: Point,
    squareclass: int,
    beta: Point,
) -> Certificate | None:
    """Target-facing certificate from one beta-parametrized split line."""

    first_coefficient = parallel_direction_squareclass_beta_target_coefficient(
        target,
        direction,
        squareclass,
        beta,
    )
    if first_coefficient is None:
        return None
    return parallel_direction_squareclass_beta_line_certificate(
        direction,
        squareclass,
        beta,
        first_coefficient,
    )


def parallel_direction_squareclass_line_root_quotient(
    direction: Point,
    squareclass: int,
    split_factor: int,
    signed_paired_split_factor: int,
) -> Point | None:
    """Second-step quotient after factoring a primitive direction as a square."""

    if squareclass <= 0:
        raise ValueError("squareclass must be positive")
    if squareclass_decomposition(squareclass) != (squareclass, 1):
        raise ValueError("squareclass must be squarefree")
    if split_factor <= 0:
        raise ValueError("split_factor must be positive")
    if signed_paired_split_factor == 0:
        raise ValueError("signed_paired_split_factor must be nonzero")

    split_quotient = parallel_direction_squareclass_line_split_quotient(
        direction,
        split_factor,
        signed_paired_split_factor,
    )
    if split_quotient is None:
        return None

    return parallel_direction_squareclass_beta_quotient(
        direction,
        squareclass,
        split_quotient,
    )


def parallel_direction_squareclass_line_congruence_holds(
    direction: Point,
    squareclass: int,
    split_factor: int,
    signed_paired_split_factor: int,
) -> bool:
    """Return whether one signed split satisfies the line congruences.

    Fix a legal direction ``U=(u,v)`` with length ``c`` and integers
    ``q,a,b`` with ``q`` squarefree.  The determinant split
    ``D=qab`` and the completion leg ``L=q(b^2-a^2)/2`` define a second edge

        W = (-L U + D U_perp) / c^2,  U_perp=(-v,u).

    This predicate checks the cleared congruence system that makes the length
    and both coordinates of ``W`` integral.  It does not exclude horizontal or
    vertical ``W``; `parallel_direction_squareclass_line_second_step` performs
    that final graph-edge check.
    """

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")
    if squareclass <= 0:
        raise ValueError("squareclass must be positive")
    if squareclass_decomposition(squareclass) != (squareclass, 1):
        raise ValueError("squareclass must be squarefree")
    if split_factor <= 0:
        raise ValueError("split_factor must be positive")
    if signed_paired_split_factor == 0:
        raise ValueError("signed_paired_split_factor must be nonzero")

    u, v = direction
    direction_norm = u * u + v * v
    hypotenuse = isqrt(direction_norm)
    paired = signed_paired_split_factor
    split_sum = paired * paired + split_factor * split_factor
    if squareclass * split_sum % (2 * hypotenuse) != 0:
        return False

    gaussian_numerator = parallel_direction_squareclass_line_gaussian_numerator(
        direction,
        squareclass,
        split_factor,
        signed_paired_split_factor,
    )
    gaussian_denominator = 2 * direction_norm
    return (
        gaussian_numerator[0] % gaussian_denominator == 0
        and gaussian_numerator[1] % gaussian_denominator == 0
    )


def parallel_direction_squareclass_line_second_step(
    direction: Point,
    squareclass: int,
    split_factor: int,
    signed_paired_split_factor: int,
) -> Point | None:
    """Second edge vector for one determinant-squareclass line family."""

    if not parallel_direction_squareclass_line_congruence_holds(
        direction,
        squareclass,
        split_factor,
        signed_paired_split_factor,
    ):
        return None

    u, v = direction
    direction_norm = u * u + v * v
    gaussian_numerator = parallel_direction_squareclass_line_gaussian_numerator(
        direction,
        squareclass,
        split_factor,
        signed_paired_split_factor,
    )
    gaussian_denominator = 2 * direction_norm
    second_step = (
        gaussian_numerator[0] // gaussian_denominator,
        gaussian_numerator[1] // gaussian_denominator,
    )
    if not edge_delta(*second_step):
        return None
    return second_step


def parallel_direction_squareclass_line_certificate(
    direction: Point,
    squareclass: int,
    split_factor: int,
    signed_paired_split_factor: int,
    first_coefficient: int,
) -> Certificate | None:
    """Certificate from one determinant-squareclass line family.

    When the split-line congruences define a legal second edge ``W``, every
    target ``rU + W`` has midpoint ``rU``.  This is the line-family normal form
    behind a squareclass split witness.
    """

    second_step = parallel_direction_squareclass_line_second_step(
        direction,
        squareclass,
        split_factor,
        signed_paired_split_factor,
    )
    if second_step is None:
        return None

    u, v = direction
    midpoint = (first_coefficient * u, first_coefficient * v)
    target = (midpoint[0] + second_step[0], midpoint[1] + second_step[1])
    certificate = Certificate(target=target, midpoint=midpoint)
    if not certificate.valid():
        return None
    return certificate


@cache
def parallel_direction_squareclass_line_residue_classes(
    direction: Point,
    squareclass: int,
    split_factor: int,
) -> tuple[int, tuple[int, ...]]:
    """Signed paired-factor residues giving a squareclass line family.

    For fixed ``U,q,a``, the line-family integrality conditions are periodic in
    the signed paired factor ``b`` modulo ``2*|U|^2``.  The returned pair is the
    minimal equivalent period and its accepted residue classes.
    """

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")
    if squareclass <= 0:
        raise ValueError("squareclass must be positive")
    if squareclass_decomposition(squareclass) != (squareclass, 1):
        raise ValueError("squareclass must be squarefree")
    if split_factor <= 0:
        raise ValueError("split_factor must be positive")

    direction_norm = direction[0] * direction[0] + direction[1] * direction[1]
    modulus = 2 * direction_norm
    residues = []
    for residue in range(modulus):
        paired = residue if residue != 0 else modulus
        second_step = parallel_direction_squareclass_line_second_step(
            direction,
            squareclass,
            split_factor,
            paired,
        )
        if second_step is not None:
            residues.append(residue)

    return minimal_periodic_residue_classes(modulus, residues)


def parallel_direction_squareclass_line_residue_certificate(
    target: Point,
    direction: Point,
    squareclass: int,
    split_factor: int,
) -> Certificate | None:
    """Target-facing certificate from one squareclass line-residue strip."""

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")
    if squareclass <= 0:
        raise ValueError("squareclass must be positive")
    if squareclass_decomposition(squareclass) != (squareclass, 1):
        raise ValueError("squareclass must be squarefree")
    if split_factor <= 0:
        raise ValueError("split_factor must be positive")

    det_value = determinant(direction, target)
    if det_value == 0:
        return None

    determinant_divisor = squareclass * split_factor
    if det_value % determinant_divisor != 0:
        return None

    paired = det_value // determinant_divisor
    period, residues = parallel_direction_squareclass_line_residue_classes(
        direction,
        squareclass,
        split_factor,
    )
    if paired % period not in residues:
        return None

    u, v = direction
    direction_norm = u * u + v * v
    factor_difference = squareclass * (paired * paired - split_factor * split_factor)
    if factor_difference % 2 != 0:
        return None

    other_leg = factor_difference // 2
    dot_product = target[0] * u + target[1] * v
    first_coefficient_numerator = dot_product + other_leg
    if first_coefficient_numerator % direction_norm != 0:
        return None

    certificate = parallel_direction_squareclass_line_certificate(
        direction,
        squareclass,
        split_factor,
        paired,
        first_coefficient_numerator // direction_norm,
    )
    if certificate is None or certificate.target != target:
        return None
    return certificate


def parallel_direction_witness(
    target: Point,
    direction: Point,
) -> ParallelDirectionFactorWitness | None:
    """First valid determinant-completion witness for one fixed direction."""

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")

    det_value = determinant(direction, target)
    if det_value == 0:
        return None

    for factor in positive_divisors(det_value * det_value):
        witness = parallel_direction_factor_witness(target, direction, factor)
        if witness is None or witness.first_coefficient == 0:
            continue
        if witness.certificate.valid():
            return witness

    return None


def parallel_direction_standard_completion_certificate(
    target: Point,
    direction: Point,
) -> Certificate | None:
    """Try the two signed standard Pythagorean completions of det(direction, target)."""

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")

    determinant_leg = determinant(direction, target)
    for factor in standard_pythagorean_completion_factors(determinant_leg):
        certificate = parallel_direction_factor_certificate(target, direction, factor)
        if certificate is not None:
            return certificate
    return None


def parallel_direction_factor_modulus(direction: Point, factor: int) -> int:
    """Return the natural modulus for a fixed direction/factor criterion."""

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")
    if factor <= 0:
        raise ValueError("factor must be positive")

    return 2 * (direction[0] * direction[0] + direction[1] * direction[1]) * factor


def parallel_direction_factor_coefficient(
    target: Point,
    direction: Point,
    factor: int,
) -> int | None:
    """Return the first-step coefficient forced by one factor, if integral.

    The arithmetic conditions depend only on ``target`` modulo
    ``2*|direction|^2*factor``.  A returned coefficient still needs the usual
    nonzero and nondegeneracy checks before it is promoted to a certificate.
    """

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")
    if factor <= 0:
        raise ValueError("factor must be positive")

    witness = parallel_direction_factor_witness(target, direction, factor)
    if witness is None:
        return None
    return witness.first_coefficient


@cache
def parallel_direction_factor_residue_classes(
    direction: Point,
    factor: int,
) -> frozenset[Point]:
    """Residue classes where one direction/factor has an integral coefficient."""

    modulus = parallel_direction_factor_modulus(direction, factor)
    residues: set[Point] = set()
    for g in range(modulus):
        for h in range(modulus):
            if parallel_direction_factor_coefficient((g, h), direction, factor) is not None:
                residues.add((g, h))
    return frozenset(residues)


@cache
def parallel_direction_factor_certificate_residue_classes(
    direction: Point,
    factor: int,
) -> frozenset[Point]:
    """Residue representatives where one direction/factor gives a certificate.

    This is a diagnostic for the fundamental residue box.  The arithmetic
    integrality condition is periodic modulo ``2*|direction|^2*factor``, but
    the nondegeneracy checks are pointwise: a degenerate representative can have
    valid translates in the same residue class.
    """

    modulus = parallel_direction_factor_modulus(direction, factor)
    residues: set[Point] = set()
    for g in range(modulus):
        for h in range(modulus):
            if parallel_direction_factor_certificate((g, h), direction, factor) is not None:
                residues.add((g, h))
    return frozenset(residues)


def parallel_direction_factor_residue_certificate(
    target: Point,
    direction: Point,
    factor: int,
) -> Certificate | None:
    """Certificate using the precomputed residue class for a direction/factor."""

    modulus = parallel_direction_factor_modulus(direction, factor)
    if (target[0] % modulus, target[1] % modulus) not in (
        parallel_direction_factor_residue_classes(direction, factor)
    ):
        return None
    return parallel_direction_factor_certificate(target, direction, factor)


def parallel_direction_certificate(
    target: Point,
    direction: Point,
) -> Certificate | None:
    """Search the exact divisor criterion for one fixed first-step direction."""

    witness = parallel_direction_witness(target, direction)
    if witness is None:
        return None
    return witness.certificate


@cache
def parallel_direction_standard_completion_cover_certificate(
    target: Point,
    max_parameter: int,
) -> Certificate | None:
    """Try the signed standard determinant-leg completions over finite directions."""

    if max_parameter < 2:
        raise ValueError("max_parameter must be at least 2")

    for u, v, _hypotenuse, _parameter_a, _parameter_b in primitive_pythagorean_directions(
        max_parameter
    ):
        certificate = parallel_direction_standard_completion_certificate(target, (u, v))
        if certificate is not None:
            return certificate

    return None


@cache
def parallel_direction_bounded_factor_cover_certificate(
    target: Point,
    max_parameter: int,
    max_factor: int,
) -> Certificate | None:
    """Try divisor-completion factors up to a fixed bound over finite directions."""

    if max_parameter < 2:
        raise ValueError("max_parameter must be at least 2")
    if max_factor <= 0:
        raise ValueError("max_factor must be positive")

    for u, v, _hypotenuse, _parameter_a, _parameter_b in primitive_pythagorean_directions(
        max_parameter
    ):
        direction = (u, v)
        determinant_leg = determinant(direction, target)
        if determinant_leg == 0:
            continue
        for factor in positive_divisors(determinant_leg * determinant_leg):
            if factor > max_factor:
                break
            certificate = parallel_direction_factor_certificate(target, direction, factor)
            if certificate is not None:
                return certificate

    return None


def unit_coordinate_factor_five_parallel_certificate(parameter_t: int) -> Certificate:
    """Certificate for the nonstandard factor-five family ``(1, 25t + 17)``."""

    fixed_coordinate = 25 * parameter_t + 17
    first_coefficient = 40 * parameter_t * parameter_t + 55 * parameter_t + 19
    certificate = Certificate(
        target=(1, fixed_coordinate),
        midpoint=(4 * first_coefficient, 3 * first_coefficient),
    )
    if not certificate.valid():
        raise AssertionError("factor-five parallel certificate formula is invalid")
    return certificate


def unit_coordinate_factor_five_parallel_orbit_certificate(
    target: Point,
) -> Certificate | None:
    """Symmetric certificate for the orbit of ``(1, 25t + 17)``."""

    for swap in (False, True):
        for x_sign in (-1, 1):
            for y_sign in (-1, 1):
                candidate_target = signed_swap_point(target, x_sign, y_sign, swap)
                if candidate_target[0] != 1:
                    continue
                if (candidate_target[1] - 17) % 25 != 0:
                    continue

                base = unit_coordinate_factor_five_parallel_certificate(
                    (candidate_target[1] - 17) // 25
                )
                certificate = sign_swap_certificate(base, target)
                if certificate is not None:
                    return certificate

    return None


@cache
def unit_coordinate_parallel_factor_residues(
    direction: Point,
    factor: int,
) -> tuple[int, ...]:
    """Residues h modulo the direction/factor modulus certifying ``(1, h)``."""

    modulus = parallel_direction_factor_modulus(direction, factor)
    return tuple(
        h
        for h in range(modulus)
        if parallel_direction_factor_certificate((1, h), direction, factor) is not None
    )


def unit_coordinate_parallel_factor_orbit_certificate(
    target: Point,
    direction: Point,
    factor: int,
) -> Certificate | None:
    """Symmetric unit-coordinate family from one direction/factor pair."""

    residues = set(unit_coordinate_parallel_factor_residues(direction, factor))
    modulus = parallel_direction_factor_modulus(direction, factor)
    for swap in (False, True):
        for x_sign in (-1, 1):
            for y_sign in (-1, 1):
                candidate_target = signed_swap_point(target, x_sign, y_sign, swap)
                if candidate_target[0] != 1:
                    continue
                if candidate_target[1] % modulus not in residues:
                    continue

                base = parallel_direction_factor_certificate(candidate_target, direction, factor)
                if base is None:
                    continue
                certificate = sign_swap_certificate(base, target)
                if certificate is not None:
                    return certificate

    return None


@cache
def ray_parallel_factor_residues(
    ray: Point,
    direction: Point,
    factor: int,
) -> tuple[int, ...]:
    """Multiplier residues where one ray/direction/factor has integral coefficient.

    For ``target = n*ray`` the fixed factor criterion depends only on ``n``
    modulo ``2*|direction|^2*factor``.  The returned residues are the arithmetic
    classes with integral first-step coefficient; callers still check the
    actual target to reject zero or horizontal/vertical graph steps.
    """

    if ray[0] == 0 and ray[1] == 0:
        raise ValueError("ray must be nonzero")

    modulus = parallel_direction_factor_modulus(direction, factor)
    residues: list[int] = []
    for residue in range(modulus):
        multiplier = residue if residue != 0 else modulus
        target = (ray[0] * multiplier, ray[1] * multiplier)
        if (
            parallel_direction_factor_coefficient(target, direction, factor)
            is not None
        ):
            residues.append(residue)
    return tuple(residues)


def ray_parallel_factor_certificate(
    target: Point,
    ray: Point,
    direction: Point,
    factor: int,
) -> Certificate | None:
    """Certificate for a target lying in a fixed ray multiplier residue class."""

    multiplier = ray_multiplier(target, ray)
    if multiplier is None or multiplier == 0:
        return None

    modulus = parallel_direction_factor_modulus(direction, factor)
    if multiplier % modulus not in ray_parallel_factor_residues(
        ray,
        direction,
        factor,
    ):
        return None
    return parallel_direction_factor_certificate(target, direction, factor)


def four_three_factor_five_parallel_certificate(target: Point) -> Certificate | None:
    """Fixed congruence family for direction ``(4, 3)`` and factor ``5``."""

    modulus = parallel_direction_factor_modulus((4, 3), 5)
    if (target[0] % modulus, target[1] % modulus) not in (
        parallel_direction_factor_residue_classes((4, 3), 5)
    ):
        return None
    return parallel_direction_factor_certificate(target, (4, 3), 5)


PARALLEL_DIRECTION_PROMOTED_345_DIRECTIONS: tuple[Point, ...] = (
    (-4, -3),
    (-4, 3),
    (-3, -4),
    (-3, 4),
    (3, -4),
    (3, 4),
    (4, -3),
    (4, 3),
)

PARALLEL_DIRECTION_PROMOTED_345_FACTORS: tuple[int, ...] = (
    1,
    2,
    3,
    4,
    5,
    6,
    8,
    9,
    25,
)

PARALLEL_DIRECTION_PROMOTED_345_FACTOR_ROWS: tuple[tuple[Point, int], ...] = tuple(
    (direction, factor)
    for direction in PARALLEL_DIRECTION_PROMOTED_345_DIRECTIONS
    for factor in PARALLEL_DIRECTION_PROMOTED_345_FACTORS
)

PYTHAGOREAN_LAYERED_ORTHOGONAL_MAX_PARAMETER = 4
PYTHAGOREAN_LAYERED_LATTICE_PAIR_MAX_PARAMETER = 25
PYTHAGOREAN_LAYERED_LATTICE_PAIR_MAX_DETERMINANT = 1435
PYTHAGOREAN_LAYERED_STANDARD_COMPLETION_MAX_PARAMETER = 8
PYTHAGOREAN_LAYERED_SPLIT_MAX_SQUARECLASS = 23
PYTHAGOREAN_LAYERED_SPLIT_MAX_FACTOR = 179
PYTHAGOREAN_LAYERED_PARALLEL_MAX_PARAMETER = 8


@cache
def parallel_direction_promoted_345_factor_witness(
    target: Point,
) -> ParallelDirectionFactorWitness | None:
    """First promoted signed ``3-4-5`` direction/factor witness for a target."""

    for direction, factor in PARALLEL_DIRECTION_PROMOTED_345_FACTOR_ROWS:
        witness = parallel_direction_factor_witness(target, direction, factor)
        if witness is None or witness.first_coefficient == 0:
            continue
        if witness.certificate.valid():
            return witness
    return None


def parallel_direction_promoted_345_factor_certificate(target: Point) -> Certificate | None:
    """Certificate from the promoted dominant signed ``3-4-5`` fixed rows."""

    witness = parallel_direction_promoted_345_factor_witness(target)
    if witness is None:
        return None
    return witness.certificate


@cache
def parallel_direction_cover_certificate(
    target: Point,
    max_parameter: int,
) -> Certificate | None:
    """Try a finite signed set of first-step directions in the divisor reduction.

    This is a theorem-candidate constructor: every returned certificate is an
    exact two-step certificate, but bounded success over a target box is not a
    proof that the fixed direction set covers all primitive rays.
    """

    if max_parameter < 2:
        raise ValueError("max_parameter must be at least 2")

    for u, v, _hypotenuse, _parameter_a, _parameter_b in primitive_pythagorean_directions(
        max_parameter
    ):
        certificate = parallel_direction_certificate(target, (u, v))
        if certificate is not None:
            return certificate

    return None


@cache
def parallel_direction_cover_witness(
    target: Point,
    max_parameter: int,
) -> ParallelDirectionFactorWitness | None:
    """First finite-direction determinant-completion witness for a target."""

    if max_parameter < 2:
        raise ValueError("max_parameter must be at least 2")

    for u, v, _hypotenuse, _parameter_a, _parameter_b in primitive_pythagorean_directions(
        max_parameter
    ):
        witness = parallel_direction_witness(target, (u, v))
        if witness is not None:
            return witness

    return None


def _sorted_count_items(counts):
    return tuple(
        sorted(
            counts.items(),
            key=lambda item: (-item[1], item[0]),
        )
    )


def parallel_direction_cover_witness_census(
    max_coordinate: int,
    max_parameter: int,
) -> ParallelDirectionCoverWitnessCensus:
    """Census of first finite-direction witnesses on primitive positive targets."""

    if max_coordinate < 1:
        raise ValueError("max_coordinate must be positive")
    if max_parameter < 2:
        raise ValueError("max_parameter must be at least 2")

    target_count = 0
    uncovered: list[Point] = []
    direction_counts: dict[Point, int] = {}
    factor_counts: dict[int, int] = {}
    direction_factor_counts: dict[tuple[Point, int], int] = {}

    for g in range(1, max_coordinate + 1):
        for h in range(1, max_coordinate + 1):
            target = (g, h)
            if target in KNOWN_DISTANCE_THREE_ORBIT or edge((0, 0), target):
                continue
            if gcd(g, h) != 1:
                continue

            target_count += 1
            witness = parallel_direction_cover_witness(target, max_parameter)
            if witness is None:
                uncovered.append(target)
                continue

            direction_counts[witness.direction] = direction_counts.get(witness.direction, 0) + 1
            factor_counts[witness.factor] = factor_counts.get(witness.factor, 0) + 1
            direction_factor = (witness.direction, witness.factor)
            direction_factor_counts[direction_factor] = (
                direction_factor_counts.get(direction_factor, 0) + 1
            )

    return ParallelDirectionCoverWitnessCensus(
        max_coordinate=max_coordinate,
        max_parameter=max_parameter,
        target_count=target_count,
        uncovered_targets=tuple(uncovered),
        direction_counts=_sorted_count_items(direction_counts),
        factor_counts=_sorted_count_items(factor_counts),
        direction_factor_counts=tuple(
            (direction, factor, count)
            for (direction, factor), count in sorted(
                direction_factor_counts.items(),
                key=lambda item: (-item[1], item[0][0], item[0][1]),
            )
        ),
    )


@cache
def pythagorean_orthogonal_lattice_cover_certificate(
    target: Point,
    max_parameter: int,
) -> Certificate | None:
    """Certificate from a Pythagorean direction and its quarter-turn rotation."""

    if max_parameter < 2:
        raise ValueError("max_parameter must be at least 2")

    for u, v, _hypotenuse, _parameter_a, _parameter_b in primitive_pythagorean_directions(
        max_parameter
    ):
        certificate = lattice_two_step_certificate(target, (u, v), (-v, u))
        if certificate is not None:
            return certificate
    return None


@cache
def pythagorean_lattice_direction_pairs(
    max_parameter: int,
    max_determinant: int | None = None,
) -> tuple[tuple[Point, Point], ...]:
    """Pairs of primitive Pythagorean directions with bounded parameters/index."""

    if max_parameter < 2:
        raise ValueError("max_parameter must be at least 2")
    if max_determinant is not None and max_determinant <= 0:
        raise ValueError("max_determinant must be positive")

    directions = tuple(
        (u, v)
        for u, v, _hypotenuse, _parameter_a, _parameter_b in primitive_pythagorean_directions(
            max_parameter
        )
    )
    pairs: list[tuple[Point, Point]] = []
    for first_direction in directions:
        for second_direction in directions:
            pair_determinant = abs(determinant(first_direction, second_direction))
            if pair_determinant == 0:
                continue
            if max_determinant is not None and pair_determinant > max_determinant:
                continue
            pairs.append((first_direction, second_direction))
    return tuple(pairs)


@cache
def pythagorean_lattice_pair_witness(
    target: Point,
    max_parameter: int,
    max_determinant: int | None = None,
) -> PythagoreanLatticePairWitness | None:
    """First bounded-index Pythagorean lattice-pair witness for a target."""

    for first_direction, second_direction in pythagorean_lattice_direction_pairs(
        max_parameter,
        max_determinant,
    ):
        coefficients = lattice_coefficients(target, first_direction, second_direction)
        if coefficients is None:
            continue

        first_coefficient, second_coefficient = coefficients
        if first_coefficient == 0 or second_coefficient == 0:
            continue

        witness = PythagoreanLatticePairWitness(
            target=target,
            first_direction=first_direction,
            second_direction=second_direction,
            determinant=abs(determinant(first_direction, second_direction)),
            first_coefficient=first_coefficient,
            second_coefficient=second_coefficient,
        )
        if not witness.certificate.valid():
            raise AssertionError("lattice-pair witness produced an invalid certificate")
        return witness

    return None


def pythagorean_lattice_pair_cover_certificate(
    target: Point,
    max_parameter: int,
    max_determinant: int | None = None,
) -> Certificate | None:
    """Certificate from a bounded-index pair of Pythagorean directions."""

    witness = pythagorean_lattice_pair_witness(
        target,
        max_parameter,
        max_determinant,
    )
    if witness is None:
        return None
    return witness.certificate


@cache
def parallel_direction_squareclass_split_cover_witness(
    target: Point,
    max_parameter: int,
    max_squareclass: int,
    max_split_factor: int,
) -> ParallelDirectionSquareclassSplitWitness | None:
    """First finite direction/squareclass/split witness for a target."""

    if max_parameter < 2:
        raise ValueError("max_parameter must be at least 2")
    if max_squareclass < 1:
        raise ValueError("max_squareclass must be positive")
    if max_split_factor < 1:
        raise ValueError("max_split_factor must be positive")

    for u, v, _hypotenuse, _parameter_a, _parameter_b in primitive_pythagorean_directions(
        max_parameter
    ):
        direction = (u, v)
        det_value = determinant(direction, target)
        if det_value == 0:
            continue
        for squareclass in squarefree_numbers(max_squareclass):
            for split_factor in range(1, max_split_factor + 1):
                if det_value % (squareclass * split_factor) != 0:
                    continue
                witness = parallel_direction_squareclass_split_witness(
                    target,
                    direction,
                    squareclass,
                    split_factor,
                )
                if witness is not None:
                    return witness

    return None


def parallel_direction_squareclass_split_cover_certificate(
    target: Point,
    max_parameter: int,
    max_squareclass: int,
    max_split_factor: int,
) -> Certificate | None:
    """Certificate from bounded determinant squareclass/split rows."""

    witness = parallel_direction_squareclass_split_cover_witness(
        target,
        max_parameter,
        max_squareclass,
        max_split_factor,
    )
    if witness is None:
        return None
    return witness.certificate


@cache
def pythagorean_layered_structural_certificate(target: Point) -> Certificate | None:
    """Fixed structural-layer certificate stack for primitive residual probes."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None

    constructors = (
        parallel_direction_promoted_345_factor_certificate,
        lambda point: pythagorean_orthogonal_lattice_cover_certificate(
            point,
            PYTHAGOREAN_LAYERED_ORTHOGONAL_MAX_PARAMETER,
        ),
        lambda point: pythagorean_lattice_pair_cover_certificate(
            point,
            PYTHAGOREAN_LAYERED_LATTICE_PAIR_MAX_PARAMETER,
            PYTHAGOREAN_LAYERED_LATTICE_PAIR_MAX_DETERMINANT,
        ),
        lambda point: parallel_direction_standard_completion_cover_certificate(
            point,
            PYTHAGOREAN_LAYERED_STANDARD_COMPLETION_MAX_PARAMETER,
        ),
    )
    for constructor in constructors:
        certificate = constructor(target)
        if certificate is None:
            continue
        if not certificate.valid():
            raise AssertionError("layered structural cover produced an invalid certificate")
        return certificate

    return None


@cache
def pythagorean_layered_split_certificate(target: Point) -> Certificate | None:
    """Layered structural stack plus bounded squareclass determinant splits."""

    certificate = pythagorean_layered_structural_certificate(target)
    if certificate is not None:
        return certificate

    certificate = parallel_direction_squareclass_split_cover_certificate(
        target,
        PYTHAGOREAN_LAYERED_PARALLEL_MAX_PARAMETER,
        PYTHAGOREAN_LAYERED_SPLIT_MAX_SQUARECLASS,
        PYTHAGOREAN_LAYERED_SPLIT_MAX_FACTOR,
    )
    if certificate is None:
        return None
    if not certificate.valid():
        raise AssertionError("layered split cover produced an invalid certificate")
    return certificate


@cache
def pythagorean_layered_conjugate_ideal_certificate(
    target: Point,
) -> Certificate | None:
    """Layered structural stack plus exact finite-direction split recognition."""

    certificate = pythagorean_layered_structural_certificate(target)
    if certificate is not None:
        return certificate

    certificate = parallel_direction_conjugate_ideal_cover_certificate(
        target,
        PYTHAGOREAN_LAYERED_PARALLEL_MAX_PARAMETER,
    )
    if certificate is None:
        return None
    if not certificate.valid():
        raise AssertionError("layered conjugate-ideal cover produced an invalid certificate")
    return certificate


@cache
def pythagorean_layered_parallel_certificate(target: Point) -> Certificate | None:
    """Layered structural stack with the finite-direction divisor cover as fallback."""

    certificate = pythagorean_layered_conjugate_ideal_certificate(target)
    if certificate is not None:
        return certificate

    certificate = parallel_direction_cover_certificate(
        target,
        PYTHAGOREAN_LAYERED_PARALLEL_MAX_PARAMETER,
    )
    if certificate is None:
        return None
    if not certificate.valid():
        raise AssertionError("layered parallel cover produced an invalid certificate")
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


BOX_TWO_HUNDRED_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (191, 39): (56, -33),
    (191, 56): (-364, -240),
    (191, 69): (-13, -84),
    (191, 84): (646, -72),
    (191, 85): (-9, 40),
    (191, 87): (4, 3),
    (191, 123): (-25, 60),
    (191, 141): (72, 21),
    (191, 158): (336, -190),
    (191, 186): (-105, -36),
    (192, 5): (72, -30),
    (192, 36): (24, 10),
    (192, 65): (312, -25),
    (192, 83): (-24, -7),
    (192, 117): (12, 5),
    (192, 119): (24, -7),
    (192, 133): (24, 7),
    (192, 148): (-12, -5),
    (192, 149): (-72, -21),
    (192, 166): (-48, -14),
    (192, 175): (-48, 14),
    (192, 180): (12, -9),
    (193, 16): (481, -600),
    (193, 37): (-14351, -1680),
    (193, 40): (385, -180),
    (193, 62): (40, -42),
    (193, 65): (180, -19),
    (193, 79): (57, -176),
    (193, 92): (6, 8),
    (193, 113): (-15, 8),
    (193, 118): (-80, -18),
    (193, 120): (-15, -36),
    (193, 131): (60, -25),
    (193, 146): (40, 42),
    (193, 155): (25, 60),
    (193, 156): (-27, -36),
    (193, 184): (165, 88),
    (194, 6): (-390, -432),
    (194, 63): (40, -9),
    (194, 64): (14, -48),
    (194, 85): (12, -35),
    (194, 98): (168, -70),
    (194, 105): (90, -48),
    (194, 109): (84, 13),
    (194, 129): (12, 9),
    (194, 161): (-66, -112),
    (194, 174): (-70, -24),
    (194, 181): (260, 69),
    (194, 190): (-984, -410),
    (195, 24): (35, -12),
    (195, 33): (-5, -12),
    (195, 68): (30, 16),
    (195, 81): (20, 21),
    (195, 82): (-45, 28),
    (195, 86): (-120, -22),
    (195, 109): (60, 25),
    (195, 115): (63, 16),
    (195, 138): (-5, -12),
    (195, 150): (24, 10),
    (195, 179): (-1092, -81),
    (196, 8): (70, -24),
    (196, 20): (112, -15),
    (196, 51): (36, 15),
    (196, 58): (40, -75),
    (196, 71): (84, -13),
    (196, 116): (28, 21),
    (196, 151): (-12, -5),
    (196, 167): (84, -13),
    (196, 174): (-24, -18),
    (196, 180): (-20, -15),
    (197, 10): (221, -60),
    (197, 23): (13221, -4972),
    (197, 26): (80, -18),
    (197, 30): (-240, -54),
    (197, 38): (165, -88),
    (197, 56): (245, -84),
    (197, 116): (-13, -84),
    (197, 147): (112, 15),
    (197, 166): (285, -68),
    (197, 170): (-280, -1950),
    (197, 173): (77, -36),
    (198, 10): (30, -16),
    (198, 20): (-27, -120),
    (198, 50): (-330, -104),
    (198, 62): (72, 30),
    (198, 85): (108, -315),
    (198, 102): (-130, -144),
    (198, 109): (-432, -51),
    (198, 136): (6, -8),
    (198, 141): (72, 21),
    (198, 146): (-360, -598),
    (199, 5): (399, -40),
    (199, 22): (1624, -1290),
    (199, 28): (24, -32),
    (199, 34): (-32, -126),
    (199, 65): (144, 17),
    (199, 78): (24, 18),
    (199, 113): (-12405, -16540),
    (199, 125): (99, 20),
    (199, 134): (975, -448),
    (199, 175): (-861, -620),
    (200, 8): (-220, -21),
    (200, 27): (40, -9),
    (200, 30): (-160, -36),
    (200, 49): (120, -35),
    (200, 68): (80, 18),
    (200, 112): (-45, 28),
    (200, 114): (-24, -18),
    (200, 134): (48, 20),
    (200, 161): (-24, -7),
}


BOX_TWO_TEN_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (201, 27): (-15, -36),
    (201, 43): (12, -5),
    (201, 71): (-15, 8),
    (201, 74): (105, -36),
    (201, 95): (21, 20),
    (201, 105): (-8, -15),
    (201, 113): (-24, -7),
    (201, 147): (-24, 7),
    (201, 178): (120, -182),
    (201, 195): (-72, -65),
    (202, 12): (247, -96),
    (202, 30): (312, -234),
    (202, 32): (10, -24),
    (202, 33): (112, -15),
    (202, 53): (-2292, -955),
    (202, 77): (748, -195),
    (202, 100): (576, -68),
    (202, 101): (180, -19),
    (202, 123): (72, -21),
    (202, 142): (37882, -37224),
    (202, 196): (10, -24),
    (202, 198): (440, -42),
    (202, 199): (240, -161),
    (203, 17): (-3741, -7900),
    (203, 30): (-72, -210),
    (203, 38): (35, 12),
    (203, 48): (-7, -24),
    (203, 57): (84, -63),
    (203, 96): (16, 12),
    (203, 100): (21, -20),
    (203, 103): (-3081, -2360),
    (203, 142): (968, -726),
    (203, 178): (-952, -186),
    (203, 183): (-112, 15),
    (203, 185): (-252, -115),
    (203, 195): (-105, -36),
    (204, 11): (36, -15),
    (204, 21): (-84, -13),
    (204, 26): (24, -7),
    (204, 33): (-16, 12),
    (204, 44): (-48, -20),
    (204, 45): (-20, 15),
    (204, 52): (-60, -25),
    (204, 74): (-12, -16),
    (204, 80): (-6, 8),
    (204, 89): (24, -7),
    (204, 95): (-12, 5),
    (204, 117): (-20, -15),
    (204, 154): (60, -11),
    (204, 156): (544, -33),
    (204, 173): (84, 13),
    (204, 175): (-48, -14),
    (204, 193): (-180, 33),
    (205, 49): (105, -56),
    (205, 60): (-5, -12),
    (205, 81): (-2360, -531),
    (205, 99): (-20, -21),
    (205, 106): (45, 28),
    (205, 136): (-42, 40),
    (205, 153): (40, 9),
    (205, 154): (120, 22),
    (205, 161): (-180, -19),
    (205, 169): (-143, 24),
    (205, 188): (-5, -12),
    (206, 26): (2736, -2470),
    (206, 30): (-80, -18),
    (206, 36): (143, -24),
    (206, 43): (-28, -45),
    (206, 56): (96, -40),
    (206, 68): (-15, 8),
    (206, 77): (-2310, -136),
    (206, 93): (154, -72),
    (206, 100): (-25, -60),
    (206, 127): (24, 7),
    (206, 134): (-81666, -30712),
    (206, 142): (6, -8),
    (206, 182): (126, 32),
    (206, 183): (-18, -24),
    (206, 191): (-234, -88),
    (206, 205): (308, -75),
    (207, 14): (-33, -56),
    (207, 27): (91, -60),
    (207, 28): (9, -12),
    (207, 33): (12, 5),
    (207, 71): (483, -44),
    (207, 97): (-4728, -1379),
    (207, 99): (12, -5),
    (207, 119): (-552, -161),
    (207, 124): (63, 16),
    (207, 169): (-1080, -315),
    (207, 177): (84, 13),
    (207, 188): (-99, -20),
    (208, 7): (40, -42),
    (208, 17): (40, -9),
    (208, 53): (312, -25),
    (208, 63): (180, -33),
    (208, 84): (-8, -6),
    (208, 94): (-32, 24),
    (208, 98): (48, 20),
    (208, 137): (144, 17),
    (208, 157): (-80, -18),
    (208, 160): (-12, -5),
    (208, 168): (-8, 6),
    (208, 171): (-112, 15),
    (208, 172): (-48, -20),
    (208, 185): (-32, 24),
    (208, 186): (-20, 15),
    (209, 21): (245, -84),
    (209, 40): (-22, -120),
    (209, 54): (1056, -342),
    (209, 58): (65, -72),
    (209, 115): (300, 55),
    (209, 123): (-176, -57),
    (209, 149): (2640, -511),
    (209, 150): (-16, 30),
    (209, 157): (-1540, -2175),
    (209, 200): (192, 56),
    (210, 3): (30, -16),
    (210, 48): (35, -12),
    (210, 62): (90, -120),
    (210, 67): (126, 32),
    (210, 69): (60, -11),
    (210, 74): (168, -70),
    (210, 104): (18, 24),
    (210, 141): (28, 21),
    (210, 152): (-63, 16),
    (210, 156): (63, 16),
    (210, 167): (126, 32),
    (210, 198): (-120, 22),
}


BOX_TWO_TWENTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (211, 7): (736, -273),
    (211, 11): (36796, -27597),
    (211, 24): (-180, -96),
    (211, 54): (224, -30),
    (211, 98): (40, -42),
    (211, 119): (-969, -1120),
    (211, 124): (198, 40),
    (211, 130): (120, -182),
    (211, 133): (-245, -84),
    (211, 179): (91, 60),
    (211, 180): (-9, -12),
    (211, 200): (99, 20),
    (211, 201): (-105, -36),
    (212, 8): (198, -40),
    (212, 35): (-12, 5),
    (212, 87): (-4, -3),
    (212, 95): (20, 15),
    (212, 102): (4, -3),
    (212, 111): (32, -24),
    (212, 132): (44, 33),
    (212, 134): (24, -7),
    (212, 150): (-8, -15),
    (212, 154): (1100, -105),
    (212, 188): (264, 23),
    (212, 195): (36, -15),
    (212, 197): (116, 87),
    (212, 200): (-60, -25),
    (213, 42): (45, -28),
    (213, 47): (-84, -13),
    (213, 55): (24, 7),
    (213, 75): (-8, 15),
    (213, 82): (168, -26),
    (213, 104): (-12, -16),
    (213, 138): (80, -18),
    (213, 166): (-3, 4),
    (213, 183): (65, 72),
    (213, 196): (3, -4),
    (214, 26): (22350, -16576),
    (214, 27): (-72, -21),
    (214, 42): (-840, -630),
    (214, 48): (27, -36),
    (214, 55): (5992, -10665),
    (214, 110): (144, -130),
    (214, 166): (20944, -10890),
    (214, 175): (280, 63),
    (214, 176): (192, 56),
    (214, 181): (1330, -456),
    (214, 204): (160, -36),
    (214, 212): (240, 44),
    (215, 35): (-589, -300),
    (215, 45): (35, 12),
    (215, 69): (40, 9),
    (215, 88): (75, 40),
    (215, 91): (75, 40),
    (215, 134): (72, -646),
    (215, 147): (35, 12),
    (215, 150): (455, -300),
    (215, 168): (160, 36),
    (215, 169): (920, -207),
    (215, 186): (143, -24),
    (215, 207): (-60, -45),
    (215, 209): (8, -15),
    (216, 5): (120, -35),
    (216, 38): (144, 17),
    (216, 61): (-24, 7),
    (216, 75): (48, -20),
    (216, 79): (-36, 15),
    (216, 105): (-72, 21),
    (216, 122): (60, -11),
    (216, 130): (-36, 15),
    (216, 131): (-264, 23),
    (216, 143): (-24, -18),
    (216, 166): (-12, -5),
    (217, 8): (168, -160),
    (217, 9): (-595, -600),
    (217, 43): (4585, -1572),
    (217, 52): (-35, -12),
    (217, 80): (-30, -16),
    (217, 97): (465, -368),
    (217, 115): (112, 15),
    (217, 121): (84, -35),
    (217, 128): (247, -96),
    (217, 138): (-15, -36),
    (217, 141): (77, 36),
    (217, 145): (9, 40),
    (217, 158): (-168, 26),
    (217, 171): (5, 12),
    (217, 174): (-143, 24),
    (217, 177): (-35, -12),
    (217, 187): (132, 55),
    (217, 191): (84, 35),
    (217, 197): (-1268, -951),
    (217, 199): (-35, 84),
    (217, 214): (-1551, -560),
    (218, 23): (456, -217),
    (218, 24): (64, -48),
    (218, 33): (-244, -183),
    (218, 80): (9, -40),
    (218, 94): (168, -26),
    (218, 102): (-238, -240),
    (218, 107): (966, -88),
    (218, 135): (36, 15),
    (218, 143): (-18850, -2808),
    (218, 161): (8, -15),
    (218, 171): (180, -189),
    (218, 180): (10, 24),
    (218, 184): (-55, 48),
    (218, 203): (182, -120),
    (219, 13): (120, -119),
    (219, 15): (99, -20),
    (219, 22): (3216, -938),
    (219, 28): (240, -44),
    (219, 36): (91, -60),
    (219, 50): (-21, -20),
    (219, 102): (440, 42),
    (219, 119): (72, -21),
    (219, 127): (39, 52),
    (219, 134): (-45, 24),
    (219, 140): (99, -20),
    (219, 165): (-12, 5),
    (219, 182): (120, 50),
    (219, 199): (3, 4),
    (220, 33): (-4, 3),
    (220, 51): (-60, -45),
    (220, 85): (-60, -11),
    (220, 104): (70, 24),
    (220, 106): (-300, -125),
    (220, 135): (-4, 3),
    (220, 145): (60, 25),
    (220, 155): (-224, -30),
    (220, 162): (-120, -27),
    (220, 169): (-12, -5),
    (220, 181): (-48, -20),
    (220, 184): (-165, 52),
}


BOX_TWO_THIRTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (221, 5): (296, -555),
    (221, 6): (77, -36),
    (221, 7): (156, -65),
    (221, 21): (-216, -63),
    (221, 23): (156, -133),
    (221, 28): (128, -96),
    (221, 30): (-504, -78),
    (221, 36): (572, -96),
    (221, 37): (-4084, -3063),
    (221, 42): (520, -138),
    (221, 54): (56, -90),
    (221, 61): (-255, -32),
    (221, 62): (336, -190),
    (221, 76): (-78, -104),
    (221, 79): (-87, -416),
    (221, 89): (-28084, -5487),
    (221, 113): (-8904, -5035),
    (221, 124): (51, -140),
    (221, 134): (144, -130),
    (221, 140): (195, -28),
    (221, 166): (77, 36),
    (221, 188): (285, 68),
    (221, 194): (-1035, -748),
    (221, 209): (-780, -451),
    (221, 210): (-899, 60),
    (222, 8): (195, -28),
    (222, 13): (-1020, -187),
    (222, 18): (-26, -168),
    (222, 57): (14, -48),
    (222, 60): (96, 28),
    (222, 83): (-12, -5),
    (222, 85): (198, 40),
    (222, 122): (288, 34),
    (222, 123): (-12, 35),
    (222, 130): (-48, -14),
    (222, 150): (-10, -24),
    (222, 169): (90, -216),
    (222, 195): (12, -5),
    (222, 206): (-378, 96),
    (222, 207): (2664, -73),
    (223, 53): (-16653, -12604),
    (223, 66): (7, -24),
    (223, 67): (-6840, -24149),
    (223, 108): (143, 24),
    (223, 114): (-8, 6),
    (223, 119): (255, -136),
    (223, 128): (70, 24),
    (223, 130): (-3177, -14120),
    (223, 145): (-8, -15),
    (223, 152): (63, -16),
    (223, 165): (520, -231),
    (223, 171): (7, -24),
    (223, 186): (-9, 12),
    (223, 192): (15, 36),
    (223, 210): (-105, -36),
    (223, 222): (-440, 42),
    (224, 5): (308, -75),
    (224, 11): (1040, -276),
    (224, 18): (4, -3),
    (224, 24): (4, 3),
    (224, 29): (140, -51),
    (224, 68): (-40, -9),
    (224, 71): (48, 14),
    (224, 73): (264, -23),
    (224, 75): (8, -15),
    (224, 102): (44, -33),
    (224, 110): (-84, 35),
    (224, 127): (56, -33),
    (224, 136): (180, 19),
    (224, 159): (-8, -15),
    (224, 162): (4, -3),
    (224, 188): (-60, -25),
    (224, 190): (-48, -14),
    (224, 193): (-24, 7),
    (224, 198): (-20, 15),
    (224, 201): (8, 6),
    (224, 216): (-32, 24),
    (225, 9): (5, -12),
    (225, 17): (105, -208),
    (225, 19): (57, -76),
    (225, 52): (-15, 8),
    (225, 56): (60, -32),
    (225, 84): (45, -28),
    (225, 89): (180, -19),
    (225, 119): (60, -25),
    (225, 126): (105, 36),
    (225, 138): (120, 50),
    (225, 145): (-315, -80),
    (225, 149): (-120, -35),
    (225, 154): (-360, -66),
    (225, 191): (-63, 16),
    (225, 221): (60, -175),
    (226, 53): (-924, -43),
    (226, 70): (-390, -800),
    (226, 74): (336, -190),
    (226, 92): (240, 44),
    (226, 109): (70, -24),
    (226, 113): (-14, -48),
    (226, 116): (-21, 20),
    (226, 126): (72, 54),
    (226, 139): (-924, 43),
    (226, 140): (-77, -264),
    (226, 147): (490, -168),
    (226, 207): (-18, 24),
    (226, 209): (-14, 48),
    (226, 216): (96, 72),
    (227, 36): (-70, -24),
    (227, 48): (-20, -48),
    (227, 58): (651, -260),
    (227, 71): (-333, -1480),
    (227, 82): (435, -308),
    (227, 91): (-28, -45),
    (227, 97): (612, -35),
    (227, 118): (360, -38),
    (227, 133): (12155, -6612),
    (227, 155): (12876, -5365),
    (227, 159): (-72, -21),
    (227, 168): (7, -24),
    (227, 201): (-72, 21),
    (227, 205): (-228, -95),
    (228, 6): (8, -15),
    (228, 9): (-60, -25),
    (228, 26): (-132, -55),
    (228, 43): (132, -85),
    (228, 58): (12, -5),
    (228, 68): (12, 5),
    (228, 90): (20, -15),
    (228, 159): (8, -6),
    (228, 176): (18, -24),
    (228, 183): (-8, 6),
    (228, 191): (-60, -25),
    (228, 196): (-24, 7),
    (229, 13): (988, -1275),
    (229, 43): (264, -77),
    (229, 92): (160, -168),
    (229, 94): (93, -476),
    (229, 95): (844, -633),
    (229, 104): (240, 44),
    (229, 105): (20, -15),
    (229, 109): (789, -1052),
    (229, 126): (-187, -84),
    (229, 153): (9, -12),
    (229, 157): (520, -231),
    (229, 200): (-96, -28),
    (230, 2): (-8970, -1288),
    (230, 17): (776, -1455),
    (230, 18): (280, -102),
    (230, 19): (2120, -477),
    (230, 30): (-10, -24),
    (230, 47): (9960, -3289),
    (230, 52): (315, -80),
    (230, 58): (-1200, -1190),
    (230, 110): (126, 32),
    (230, 122): (-3312, -1534),
    (230, 126): (-40, -42),
    (230, 136): (-70, -24),
    (230, 145): (120, -119),
    (230, 156): (-10, -24),
    (230, 177): (-40, 9),
    (230, 186): (-40, 42),
    (230, 212): (-45, -28),
    (230, 217): (380, -399),
    (230, 219): (-220, -21),
}


BOX_TWO_FORTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (231, 45): (-84, -35),
    (231, 57): (-325, -360),
    (231, 59): (-21, 20),
    (231, 65): (63, 16),
    (231, 71): (15, 8),
    (231, 72): (280, -96),
    (231, 76): (195, 28),
    (231, 81): (220, 21),
    (231, 85): (-21, -20),
    (231, 89): (36, -15),
    (231, 128): (6, 8),
    (231, 130): (63, 60),
    (231, 146): (-24, 10),
    (231, 159): (35, 12),
    (231, 163): (336, -45),
    (231, 177): (-364, -27),
    (231, 192): (-9, 12),
    (231, 218): (351, -132),
    (232, 52): (-80, -39),
    (232, 66): (72, 30),
    (232, 95): (24, -10),
    (232, 101): (-32, 24),
    (232, 117): (8, -15),
    (232, 142): (-56, -33),
    (232, 158): (48, 20),
    (232, 165): (-8, -15),
    (232, 173): (384, -112),
    (232, 185): (-24, -7),
    (232, 193): (760, 39),
    (232, 198): (-16, 12),
    (232, 205): (336, 52),
    (232, 207): (16, 12),
    (232, 210): (112, -15),
    (233, 11): (200, -45),
    (233, 20): (-7, -24),
    (233, 32): (143, -24),
    (233, 41): (-4515, -3520),
    (233, 53): (-39952, -12939),
    (233, 90): (3808, -510),
    (233, 99): (-779, -660),
    (233, 106): (-40, -30),
    (233, 115): (-75, 40),
    (233, 125): (8, -15),
    (233, 143): (80, 39),
    (233, 189): (-40, 9),
    (233, 190): (24, 70),
    (233, 214): (-7, -24),
    (234, 19): (594, -608),
    (234, 22): (2394, -608),
    (234, 34): (-126, -32),
    (234, 41): (252, -39),
    (234, 76): (-63, 16),
    (234, 86): (168, -26),
    (234, 92): (-6, -8),
    (234, 103): (6, 8),
    (234, 131): (612, 35),
    (234, 138): (18, -24),
    (234, 146): (1170, -1856),
    (234, 155): (-42, 40),
    (234, 163): (6, -8),
    (234, 180): (42, -40),
    (234, 189): (390, 56),
    (234, 211): (168, 99),
    (234, 219): (18, 24),
    (235, 14): (195, -28),
    (235, 27): (55, -48),
    (235, 50): (-416, -210),
    (235, 65): (-209, -120),
    (235, 76): (70, 24),
    (235, 77): (144, 17),
    (235, 86): (480, -1102),
    (235, 96): (10, -24),
    (235, 97): (-8025, -2912),
    (235, 103): (195, 28),
    (235, 105): (4, -3),
    (235, 125): (780, -1183),
    (235, 145): (63, 16),
    (235, 154): (312, -266),
    (235, 176): (-240, 44),
    (235, 181): (-465, -248),
    (235, 184): (15, -8),
    (235, 196): (70, -24),
    (235, 215): (8140, -777),
    (235, 222): (35, 12),
    (235, 233): (4740, -1975),
    (236, 13): (-600, -110),
    (236, 22): (264, -23),
    (236, 49): (-240, -44),
    (236, 50): (608, -105),
    (236, 52): (15, -8),
    (236, 55): (360, -38),
    (236, 63): (-44, -33),
    (236, 94): (-16, 30),
    (236, 102): (72, -21),
    (236, 155): (48, 14),
    (236, 172): (5, 12),
    (236, 183): (-4, 3),
    (236, 196): (-63, 16),
    (236, 204): (16, 12),
    (236, 232): (5, 12),
    (236, 234): (-140, -48),
    (237, 3): (-15, -36),
    (237, 18): (21, -72),
    (237, 26): (-120, -50),
    (237, 31): (-15, -8),
    (237, 47): (-15, 8),
    (237, 65): (-99, 20),
    (237, 67): (72, -21),
    (237, 89): (312, -91),
    (237, 93): (665, -228),
    (237, 135): (12, -5),
    (237, 137): (276, -115),
    (237, 156): (12, 16),
    (237, 189): (588, -91),
    (237, 193): (-123, -164),
    (237, 208): (30, -16),
    (238, 18): (224, -30),
    (238, 19): (210, -176),
    (238, 22): (10150, -1512),
    (238, 37): (84, -35),
    (238, 47): (112, 15),
    (238, 50): (70, 24),
    (238, 54): (-112, -66),
    (238, 76): (63, 16),
    (238, 93): (28, 21),
    (238, 96): (323, -36),
    (238, 97): (874, -168),
    (238, 124): (-35, -12),
    (238, 138): (286, 48),
    (238, 143): (-266, -312),
    (238, 150): (70, 24),
    (238, 151): (18, -80),
    (238, 186): (-224, -30),
    (238, 208): (-126, -32),
    (238, 215): (-90, -400),
    (238, 225): (108, 81),
    (238, 232): (-77, 36),
    (239, 38): (15, 8),
    (239, 40): (119, -120),
    (239, 42): (200, -210),
    (239, 53): (-21, -220),
    (239, 77): (116, -87),
    (239, 82): (224, -30),
    (239, 87): (-805, -348),
    (239, 88): (-2176, -132),
    (239, 100): (5, 12),
    (239, 117): (-112, -15),
    (239, 135): (-60, -45),
    (239, 164): (32, -60),
    (240, 22): (60, -11),
    (240, 36): (40, -9),
    (240, 43): (60, -32),
    (240, 91): (72, 21),
    (240, 97): (24, 7),
    (240, 123): (60, 11),
    (240, 169): (24, 7),
    (240, 181): (72, 21),
    (240, 185): (24, -10),
    (240, 189): (-48, 14),
    (240, 221): (84, 13),
    (240, 225): (112, -15),
    (240, 237): (-420, 29),
}


BOX_TWO_FIFTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (241, 12): (20, -48),
    (241, 20): (-45, -28),
    (241, 27): (-56, -33),
    (241, 29): (-29403, -22204),
    (241, 33): (385, -132),
    (241, 56): (-1859, -312),
    (241, 58): (2881, -1320),
    (241, 65): (105, -208),
    (241, 111): (108, -45),
    (241, 139): (156, -65),
    (241, 142): (1720, -3498),
    (241, 156): (-32, -24),
    (241, 173): (105, -100),
    (241, 181): (-423, -1064),
    (241, 182): (-39, 80),
    (241, 188): (-12, -16),
    (241, 195): (-12, -9),
    (241, 201): (80, -39),
    (241, 204): (70, -24),
    (241, 205): (-119, -120),
    (241, 215): (-84, -13),
    (242, 5): (42, -40),
    (242, 34): (-1870, -1632),
    (242, 70): (-2200, -210),
    (242, 100): (11, -60),
    (242, 103): (8, 15),
    (242, 114): (-550, -480),
    (242, 138): (88, 66),
    (242, 174): (792, -330),
    (242, 182): (-43648, -1386),
    (242, 194): (-6, 8),
    (242, 195): (-220, -21),
    (242, 238): (210, 112),
    (243, 7): (180, -273),
    (243, 13): (-156, -455),
    (243, 17): (63, -16),
    (243, 34): (-357, -76),
    (243, 57): (-21, -20),
    (243, 80): (63, -16),
    (243, 91): (63, 16),
    (243, 97): (-21, 20),
    (243, 98): (483, 44),
    (243, 104): (3, 4),
    (243, 115): (144, -17),
    (243, 141): (-12, 5),
    (243, 148): (-45, 28),
    (243, 164): (-30, -16),
    (243, 175): (-72, -21),
    (243, 200): (-9, -40),
    (243, 217): (-72, 21),
    (243, 227): (123, -164),
    (243, 242): (3, 4),
    (244, 23): (84, -13),
    (244, 44): (-20, 21),
    (244, 46): (-7056, -2783),
    (244, 73): (4, 3),
    (244, 88): (144, -17),
    (244, 101): (180, -19),
    (244, 117): (20, -15),
    (244, 156): (-24, -45),
    (244, 158): (4, -3),
    (244, 163): (60, 25),
    (244, 171): (8, -6),
    (244, 192): (-9, -12),
    (244, 201): (-12, 9),
    (244, 228): (20, 21),
    (245, 10): (21, -20),
    (245, 11): (-1680, -649),
    (245, 13): (77, -36),
    (245, 25): (525, -500),
    (245, 37): (140, -51),
    (245, 48): (210, -72),
    (245, 64): (-105, -56),
    (245, 74): (-840, -58),
    (245, 113): (1085, -132),
    (245, 116): (5, -12),
    (245, 139): (-7, 24),
    (245, 143): (-40, -9),
    (245, 145): (-391, -120),
    (245, 183): (105, 36),
    (245, 184): (65, 72),
    (245, 194): (-40, 42),
    (245, 225): (-28, 45),
    (245, 232): (-28, 96),
    (245, 243): (-280, 63),
    (245, 244): (165, 52),
    (246, 2): (360, -150),
    (246, 31): (-6, -8),
    (246, 33): (70, -24),
    (246, 53): (-18, -24),
    (246, 112): (21, -28),
    (246, 115): (300, -125),
    (246, 122): (126, 32),
    (246, 136): (6, 8),
    (246, 177): (126, -32),
    (246, 200): (15, -20),
    (246, 214): (126, 32),
    (246, 221): (390, 56),
    (246, 229): (84, 13),
    (246, 235): (30, 40),
    (247, 18): (112, -66),
    (247, 20): (7, -24),
    (247, 25): (39, -80),
    (247, 27): (-5, -12),
    (247, 32): (-143, -24),
    (247, 43): (651, -260),
    (247, 49): (15640, -20475),
    (247, 60): (-144, -60),
    (247, 64): (672, -104),
    (247, 69): (112, -15),
    (247, 71): (364, 27),
    (247, 88): (55, -132),
    (247, 98): (975, -448),
    (247, 101): (-2793, -424),
    (247, 116): (60, 32),
    (247, 118): (37240, -1158),
    (247, 126): (135, -84),
    (247, 129): (143, -24),
    (247, 137): (-144, 17),
    (247, 160): (798, -80),
    (247, 190): (16, -30),
    (247, 203): (-3905, -1008),
    (247, 217): (171, -140),
    (247, 224): (-2303, -96),
    (247, 235): (-105, 100),
    (247, 242): (-3848, -2886),
    (248, 13): (168, -26),
    (248, 41): (288, -34),
    (248, 51): (-112, -15),
    (248, 54): (-40, -30),
    (248, 63): (40, -42),
    (248, 76): (8, 6),
    (248, 77): (80, -18),
    (248, 78): (-12, 9),
    (248, 105): (-200, 45),
    (248, 141): (-32, -24),
    (248, 142): (24, 10),
    (248, 145): (312, 25),
    (248, 148): (528, 46),
    (248, 161): (24, -7),
    (248, 170): (144, 17),
    (248, 180): (4, -3),
    (248, 196): (48, -14),
    (248, 226): (-120, -50),
    (249, 23): (60, -25),
    (249, 40): (-6, 8),
    (249, 54): (969, -108),
    (249, 61): (45, -24),
    (249, 119): (-3, 4),
    (249, 142): (144, 42),
    (249, 146): (-24, 10),
    (249, 153): (104, -195),
    (249, 169): (60, -11),
    (249, 205): (60, 25),
    (250, 7): (-240, -161),
    (250, 10): (-150, -80),
    (250, 28): (195, -104),
    (250, 32): (96, -40),
    (250, 41): (-182, -624),
    (250, 85): (550, -504),
    (250, 97): (516, -215),
    (250, 106): (2850, -2624),
    (250, 109): (120, -35),
    (250, 122): (-80, 18),
    (250, 140): (-35, -12),
    (250, 143): (-80, 39),
    (250, 148): (-5, 12),
    (250, 151): (16, 63),
    (250, 182): (154, 72),
    (250, 189): (-20, 21),
    (250, 202): (618, -824),
    (250, 216): (-70, -24),
    (250, 231): (12, -9),
}


BOX_TWO_SIXTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (251, 2): (-15624, -250),
    (251, 7): (264, -77),
    (251, 39): (-429, -72),
    (251, 44): (30, -16),
    (251, 47): (476, -93),
    (251, 58): (-85, -132),
    (251, 72): (-140, -48),
    (251, 73): (1295, -444),
    (251, 100): (-99, -20),
    (251, 109): (-9, 40),
    (251, 136): (285, -152),
    (251, 152): (336, -52),
    (251, 165): (-65, -72),
    (251, 180): (-5, -12),
    (251, 203): (-13524, -24157),
    (251, 214): (-861, -620),
    (251, 219): (132, 99),
    (251, 221): (783, 56),
    (251, 229): (-2145, -1568),
    (252, 27): (540, -57),
    (252, 44): (525, -92),
    (252, 62): (84, 13),
    (252, 65): (12, -5),
    (252, 75): (12, 5),
    (252, 86): (-12, 9),
    (252, 92): (-63, -16),
    (252, 131): (420, -29),
    (252, 153): (-84, 13),
    (252, 165): (-12, -5),
    (252, 173): (84, 13),
    (252, 233): (12, -5),
    (252, 237): (84, 13),
    (252, 243): (12, 5),
    (253, 17): (-11, -60),
    (253, 33): (13, -84),
    (253, 35): (220, -21),
    (253, 52): (99, -20),
    (253, 53): (165, -52),
    (253, 59): (340, -357),
    (253, 68): (-77, -36),
    (253, 91): (-35, -84),
    (253, 94): (-99, -20),
    (253, 98): (-440, -42),
    (253, 121): (-20, -15),
    (253, 123): (-55, 48),
    (253, 147): (105, 36),
    (253, 238): (-2067, -644),
    (254, 20): (299, -180),
    (254, 25): (1956, -815),
    (254, 36): (144, -60),
    (254, 59): (44, -117),
    (254, 66): (72, -54),
    (254, 85): (-1102, -480),
    (254, 105): (44, 33),
    (254, 113): (144, 17),
    (254, 127): (350, -120),
    (254, 139): (-1468, -1101),
    (254, 140): (-418, -240),
    (254, 144): (45, 24),
    (254, 150): (72, 30),
    (254, 176): (14, 48),
    (254, 185): (72, 65),
    (254, 186): (912, -2070),
    (254, 234): (-154, -72),
    (255, 12): (45, -60),
    (255, 27): (-45, -28),
    (255, 55): (-60, -25),
    (255, 57): (-5, -12),
    (255, 65): (-9, -12),
    (255, 78): (15, 8),
    (255, 96): (63, 16),
    (255, 100): (45, 28),
    (255, 138): (360, 38),
    (255, 169): (15, 8),
    (255, 195): (60, 91),
    (255, 222): (-120, 22),
    (255, 226): (528, 46),
    (255, 239): (-60, -25),
    (255, 244): (3, 4),
    (256, 2): (112, -15),
    (256, 21): (40, -42),
    (256, 47): (280, -96),
    (256, 48): (35, -12),
    (256, 85): (48, -20),
    (256, 93): (112, -15),
    (256, 121): (96, -110),
    (256, 156): (24, -18),
    (256, 167): (24, -7),
    (256, 190): (96, -110),
    (256, 201): (8, 15),
    (256, 219): (36, 27),
    (256, 223): (120, -50),
    (256, 240): (16, -12),
    (257, 55): (180, 19),
    (257, 67): (-20044, -15033),
    (257, 70): (152, -714),
    (257, 80): (75, -40),
    (257, 132): (77, 36),
    (257, 136): (-4095, -128),
    (257, 161): (-4488, -391),
    (257, 169): (-4180, -11115),
    (257, 193): (-129096, -130247),
    (257, 223): (312, 91),
    (257, 249): (105, -36),
    (257, 255): (-100, -105),
    (258, 14): (90, -56),
    (258, 16): (105, -88),
    (258, 23): (126, -32),
    (258, 39): (90, -56),
    (258, 40): (198, -40),
    (258, 42): (-624, -182),
    (258, 52): (48, -20),
    (258, 54): (216, -90),
    (258, 95): (24, 7),
    (258, 103): (-252, 39),
    (258, 119): (42, 56),
    (258, 128): (-15, -8),
    (258, 130): (42, 40),
    (258, 145): (48, -55),
    (258, 180): (48, -20),
    (258, 184): (-12, 16),
    (258, 199): (300, 55),
    (258, 207): (216, 63),
    (258, 235): (42, 40),
    (258, 243): (286, 48),
    (258, 256): (45, -28),
    (259, 26): (715, -624),
    (259, 34): (168, -26),
    (259, 44): (-245, -84),
    (259, 46): (-693, -140),
    (259, 47): (84, -13),
    (259, 52): (175, -60),
    (259, 72): (70, 24),
    (259, 78): (-56, -90),
    (259, 83): (-21, 20),
    (259, 90): (224, -30),
    (259, 93): (-21, -72),
    (259, 102): (-200, -210),
    (259, 115): (364, 27),
    (259, 132): (160, -36),
    (259, 174): (-221, -60),
    (259, 180): (35, 12),
    (259, 209): (-140, -171),
    (259, 216): (7, -24),
    (259, 221): (-644, -483),
    (259, 236): (285, 68),
    (259, 240): (-16, -12),
    (259, 247): (175, 60),
    (260, 31): (-400, -90),
    (260, 32): (-55, -48),
    (260, 44): (5, 12),
    (260, 105): (-28, 21),
    (260, 108): (35, -12),
    (260, 114): (80, 18),
    (260, 131): (180, -19),
    (260, 163): (96, 40),
    (260, 177): (12, -9),
    (260, 184): (24, 7),
    (260, 187): (24, 10),
    (260, 193): (120, 22),
    (260, 200): (-70, 24),
    (260, 210): (-100, 105),
    (260, 214): (48, 55),
    (260, 215): (-60, -25),
    (260, 226): (-120, -35),
    (260, 231): (-24, 18),
    (260, 257): (440, -42),
}


BOX_TWO_SEVENTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (261, 14): (-432, -126),
    (261, 31): (-936, -273),
    (261, 32): (234, -88),
    (261, 34): (21, -20),
    (261, 102): (77, -36),
    (261, 105): (36, -15),
    (261, 148): (21, 20),
    (261, 150): (168, 26),
    (261, 175): (-12, -5),
    (261, 197): (-84, 13),
    (261, 248): (63, -16),
    (261, 253): (-60, -175),
    (261, 258): (21, 20),
    (262, 13): (-1040, -507),
    (262, 28): (-266, -312),
    (262, 54): (-88, -66),
    (262, 55): (-24, 7),
    (262, 56): (70, -24),
    (262, 63): (10, 24),
    (262, 76): (15, -20),
    (262, 106): (3312, -2990),
    (262, 119): (-3920, -801),
    (262, 131): (570, -304),
    (262, 133): (-612, -35),
    (262, 153): (-8, -15),
    (262, 167): (598, -360),
    (262, 184): (6, -8),
    (262, 191): (42, -40),
    (262, 204): (437, -84),
    (262, 217): (-816, -287),
    (262, 225): (-70, -24),
    (262, 238): (-1122, -800),
    (262, 245): (2812, -75),
    (263, 16): (87, -116),
    (263, 20): (42, -40),
    (263, 49): (15668, -11751),
    (263, 70): (200, -210),
    (263, 83): (35, -12),
    (263, 84): (16, -12),
    (263, 89): (-15105, -8056),
    (263, 146): (95, -228),
    (263, 154): (23, -264),
    (263, 166): (63, 16),
    (263, 189): (-5, -12),
    (263, 190): (399, -380),
    (263, 202): (168, -26),
    (263, 218): (575, -48),
    (263, 223): (-861, -620),
    (263, 224): (-12, -16),
    (263, 254): (168, 26),
    (263, 258): (55, -48),
    (264, 21): (40, -9),
    (264, 41): (-24, 7),
    (264, 102): (-144, -17),
    (264, 134): (-120, 22),
    (264, 136): (-6, -8),
    (264, 162): (-144, 17),
    (264, 174): (16, -12),
    (264, 186): (8, -6),
    (264, 188): (96, 28),
    (264, 190): (24, 10),
    (264, 195): (-16, 30),
    (264, 230): (-48, -36),
    (265, 3): (220, -21),
    (265, 10): (-575, -48),
    (265, 12): (90, -48),
    (265, 17): (165, -88),
    (265, 79): (-1160, -261),
    (265, 112): (10, -24),
    (265, 114): (105, 36),
    (265, 126): (-112, -210),
    (265, 165): (-8, -15),
    (265, 173): (-15, 8),
    (265, 178): (-575, 48),
    (265, 179): (220, -21),
    (265, 207): (5, 12),
    (265, 217): (-60, -11),
    (265, 229): (-75, 40),
    (265, 235): (-1407, -1340),
    (265, 238): (-1688, -1266),
    (265, 243): (236, -177),
    (265, 248): (55, 48),
    (265, 250): (7209, -680),
    (265, 252): (140, -48),
    (266, 16): (126, -32),
    (266, 22): (56, -90),
    (266, 36): (45, -24),
    (266, 45): (28, -195),
    (266, 58): (-1974, -1880),
    (266, 66): (168, -270),
    (266, 79): (56, -33),
    (266, 121): (-390, -1496),
    (266, 146): (456, -190),
    (266, 156): (-7, -24),
    (266, 199): (-40, -9),
    (266, 202): (56, 90),
    (266, 204): (-7, 24),
    (266, 237): (-18, 24),
    (266, 241): (168, -95),
    (266, 248): (285, 68),
    (266, 250): (-40, 42),
    (266, 260): (221, 60),
    (266, 261): (28, 21),
    (267, 3): (312, -25),
    (267, 7): (72, -21),
    (267, 56): (15, -8),
    (267, 72): (15, 8),
    (267, 75): (99, -20),
    (267, 87): (520, -117),
    (267, 95): (15, -20),
    (267, 100): (-21, -20),
    (267, 136): (27, 36),
    (267, 147): (144, -17),
    (267, 157): (135, 72),
    (267, 163): (195, 28),
    (267, 192): (-5, -12),
    (267, 214): (-165, 88),
    (267, 233): (420, 29),
    (267, 234): (-8, -6),
    (267, 235): (60, 11),
    (267, 238): (-45, -28),
    (267, 261): (-228, -171),
    (268, 18): (-1160, -261),
    (268, 35): (48, 14),
    (268, 36): (-20, -48),
    (268, 55): (-20, 21),
    (268, 73): (60, -32),
    (268, 77): (-104, -78),
    (268, 78): (-252, -39),
    (268, 94): (60, -11),
    (268, 140): (28, -21),
    (268, 146): (180, -19),
    (268, 182): (28, 21),
    (268, 196): (15, -8),
    (268, 211): (48, -20),
    (268, 217): (48, -14),
    (268, 242): (528, -46),
    (268, 251): (-84, -13),
    (268, 260): (-608, -105),
    (269, 9): (80, -39),
    (269, 20): (77, -36),
    (269, 28): (-105, -140),
    (269, 37): (-11020, -15015),
    (269, 41): (440, -99),
    (269, 43): (-1840, -897),
    (269, 54): (45, 24),
    (269, 65): (5, -12),
    (269, 71): (204, -85),
    (269, 78): (224, -30),
    (269, 84): (-270, -168),
    (269, 111): (-55, -132),
    (269, 128): (1209, -4240),
    (269, 145): (60, 25),
    (269, 169): (-3280, -1599),
    (269, 176): (170, -264),
    (269, 188): (-115, -252),
    (269, 254): (-4216, -390),
    (270, 19): (72, -21),
    (270, 21): (70, -24),
    (270, 23): (180, -33),
    (270, 26): (-120, -182),
    (270, 29): (180, -19),
    (270, 49): (144, 17),
    (270, 83): (60, 11),
    (270, 86): (30, 16),
    (270, 98): (126, -32),
    (270, 124): (-255, 32),
    (270, 141): (-30, 16),
    (270, 174): (70, 24),
    (270, 202): (-240, -70),
    (270, 203): (-390, -56),
    (270, 239): (132, 55),
    (270, 257): (-4284, -663),
}


BOX_TWO_EIGHTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (271, 11): (-132, -385),
    (271, 36): (91, -60),
    (271, 43): (76, -357),
    (271, 76): (-396, -80),
    (271, 108): (-9, 12),
    (271, 134): (7, 24),
    (271, 147): (27, -36),
    (271, 155): (-120, 35),
    (271, 172): (15, -20),
    (271, 196): (-35, -12),
    (271, 225): (-28, 45),
    (271, 263): (855, -832),
    (271, 269): (-5565, -4108),
    (271, 270): (-65, 72),
    (272, 14): (-400, -90),
    (272, 28): (80, 84),
    (272, 44): (48, 14),
    (272, 47): (-352, -135),
    (272, 60): (12, -9),
    (272, 109): (72, 154),
    (272, 156): (32, -24),
    (272, 175): (-112, 15),
    (272, 189): (72, -21),
    (272, 201): (240, -54),
    (272, 208): (-12, -5),
    (272, 213): (8, 15),
    (272, 234): (-20, 15),
    (272, 245): (-208, 105),
    (272, 249): (40, 75),
    (272, 262): (32, 24),
    (273, 17): (9, 40),
    (273, 30): (48, -90),
    (273, 40): (-42, -40),
    (273, 48): (-15, -36),
    (273, 51): (105, 100),
    (273, 62): (105, 36),
    (273, 72): (-7, -24),
    (273, 74): (105, 100),
    (273, 79): (-180, -525),
    (273, 81): (-75, -180),
    (273, 116): (63, -60),
    (273, 135): (21, 20),
    (273, 138): (-63, -60),
    (273, 144): (33, 44),
    (273, 145): (84, -35),
    (273, 159): (-35, 84),
    (273, 164): (3, -4),
    (273, 181): (21, 220),
    (273, 185): (-75, 40),
    (273, 190): (-216, -462),
    (273, 213): (5, 12),
    (273, 220): (21, -20),
    (273, 229): (-135, 84),
    (273, 242): (-135, 72),
    (273, 244): (-42, -56),
    (273, 263): (165, -52),
    (273, 269): (-60, -175),
    (274, 11): (-276, -493),
    (274, 63): (-76, -57),
    (274, 70): (-182, -120),
    (274, 84): (85, 132),
    (274, 119): (-608, -105),
    (274, 123): (-50, -120),
    (274, 130): (40, 42),
    (274, 144): (-34, 288),
    (274, 157): (-6, -8),
    (274, 164): (-117, 44),
    (274, 206): (-21590, -8904),
    (274, 213): (36, -27),
    (274, 219): (110, 96),
    (274, 249): (-104, 153),
    (274, 255): (36, 15),
    (275, 11): (20, -21),
    (275, 27): (55, 48),
    (275, 56): (35, 12),
    (275, 63): (135, -84),
    (275, 91): (-48, 55),
    (275, 118): (-13, 84),
    (275, 130): (-165, 88),
    (275, 153): (-5, -12),
    (275, 154): (-40, -42),
    (275, 182): (-165, -280),
    (275, 204): (-13, 84),
    (275, 230): (11, 60),
    (275, 238): (-40, 42),
    (275, 249): (-105, -36),
    (276, 29): (-12, -5),
    (276, 36): (88, -105),
    (276, 44): (-120, 209),
    (276, 85): (-12, -35),
    (276, 97): (24, -18),
    (276, 106): (-36, 15),
    (276, 107): (-24, -18),
    (276, 127): (36, 27),
    (276, 132): (3, -4),
    (276, 174): (-20, -48),
    (276, 189): (12, -9),
    (276, 197): (60, -91),
    (276, 205): (12, 35),
    (276, 219): (-8, 6),
    (276, 236): (39, -80),
    (276, 265): (-12, 5),
    (277, 15): (88, -165),
    (277, 19): (16377, -21836),
    (277, 22): (112, -66),
    (277, 30): (56, 90),
    (277, 63): (-360, -357),
    (277, 65): (-260, -651),
    (277, 71): (-308, 435),
    (277, 89): (57, -76),
    (277, 96): (144, -60),
    (277, 119): (1572, -4585),
    (277, 125): (-200, -1995),
    (277, 160): (39, -80),
    (277, 167): (-8, 15),
    (277, 173): (-48, -55),
    (277, 177): (4, -3),
    (277, 184): (132, -224),
    (277, 187): (117, -44),
    (277, 210): (112, 66),
    (277, 238): (-675, 52),
    (277, 245): (525, -700),
    (277, 252): (11, -60),
    (277, 253): (-668, 501),
    (277, 260): (192, 56),
    (277, 266): (240, -418),
    (277, 275): (117, 44),
    (278, 49): (98, -336),
    (278, 57): (-190, 456),
    (278, 62): (14, -48),
    (278, 70): (110, 96),
    (278, 104): (-30, -40),
    (278, 118): (-7248, -2114),
    (278, 139): (-190, -456),
    (278, 146): (30, -40),
    (278, 168): (5, -12),
    (278, 181): (-190, 336),
    (278, 203): (-702, 560),
    (278, 211): (-30, -224),
    (278, 218): (14, 48),
    (278, 224): (180, -112),
    (278, 239): (888, -1225),
    (279, 7): (84, 35),
    (279, 46): (-9, 12),
    (279, 79): (27, -36),
    (279, 95): (-36, 15),
    (279, 110): (-225, -120),
    (279, 116): (45, 28),
    (279, 173): (-2280, -3239),
    (279, 191): (-156, -117),
    (279, 208): (9, 40),
    (279, 212): (54, 72),
    (279, 235): (27, 120),
    (279, 241): (39, 80),
    (279, 250): (-72, -30),
    (279, 276): (27, 36),
    (280, 4): (60, 25),
    (280, 17): (112, 66),
    (280, 19): (-8, -15),
    (280, 27): (80, -18),
    (280, 30): (-40, -42),
    (280, 32): (60, 11),
    (280, 64): (112, 15),
    (280, 85): (28, 21),
    (280, 92): (-35, 12),
    (280, 94): (28, -21),
    (280, 129): (60, -63),
    (280, 170): (40, 9),
    (280, 188): (48, 14),
    (280, 191): (40, 30),
    (280, 208): (-35, 12),
    (280, 218): (-24, -10),
    (280, 235): (-12, 16),
    (280, 237): (24, 45),
    (280, 246): (-20, 21),
    (280, 254): (-8, -6),
    (280, 264): (5, 12),
    (280, 270): (-40, 30),
}


BOX_TWO_NINETY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (281, 18): (65, -72),
    (281, 26): (17, -144),
    (281, 52): (56, 192),
    (281, 53): (21, -220),
    (281, 61): (840, -3551),
    (281, 66): (72, -54),
    (281, 75): (-119, -120),
    (281, 86): (-9879, -2200),
    (281, 95): (-91, -60),
    (281, 100): (-55, 48),
    (281, 112): (-70, -168),
    (281, 122): (105, -88),
    (281, 126): (-135, -84),
    (281, 133): (-76, 57),
    (281, 151): (8, 15),
    (281, 172): (26, -168),
    (281, 191): (-206403, 155204),
    (281, 221): (17, 144),
    (281, 248): (6, 8),
    (281, 264): (-96, -72),
    (282, 4): (27, 36),
    (282, 13): (126, -120),
    (282, 21): (-180, -299),
    (282, 28): (105, -208),
    (282, 60): (42, -40),
    (282, 74): (48, -14),
    (282, 78): (370, -888),
    (282, 91): (72, -21),
    (282, 95): (-42, -40),
    (282, 112): (-6, -8),
    (282, 126): (42, 56),
    (282, 143): (48, 55),
    (282, 148): (-3, -4),
    (282, 150): (-238, -240),
    (282, 174): (18, -24),
    (282, 182): (42, -56),
    (282, 213): (-138, 184),
    (282, 221): (72, 21),
    (282, 225): (100, 105),
    (282, 255): (-60, -25),
    (282, 258): (130, 144),
    (282, 262): (-54, 72),
    (282, 266): (-48, 90),
    (283, 2): (-77, -36),
    (283, 15): (-25, -60),
    (283, 41): (-117, -520),
    (283, 49): (220, -231),
    (283, 97): (-7460, -36927),
    (283, 125): (112, -15),
    (283, 159): (-77, 264),
    (283, 163): (-5, -12),
    (283, 182): (168, -70),
    (283, 187): (-5, 12),
    (283, 202): (-312, -266),
    (283, 210): (-16, 30),
    (283, 232): (28, 96),
    (283, 244): (30, 40),
    (283, 245): (-5684, -4515),
    (283, 253): (-2145, -1568),
    (283, 273): (52, 165),
    (283, 279): (-45, -336),
    (284, 30): (-24, -45),
    (284, 56): (20, -21),
    (284, 62): (20, -15),
    (284, 91): (32, -24),
    (284, 100): (8, -15),
    (284, 113): (-16, -12),
    (284, 147): (44, -33),
    (284, 153): (40, -30),
    (284, 159): (36, -27),
    (284, 173): (120, 50),
    (284, 182): (60, -25),
    (284, 183): (20, -15),
    (284, 184): (-120, -119),
    (284, 223): (-16, 63),
    (284, 244): (-168, -95),
    (285, 8): (30, 40),
    (285, 32): (75, -40),
    (285, 52): (96, -128),
    (285, 53): (45, -108),
    (285, 78): (45, 24),
    (285, 85): (-63, -60),
    (285, 102): (120, 50),
    (285, 109): (60, -11),
    (285, 118): (117, -756),
    (285, 132): (15, -36),
    (285, 161): (-15, 36),
    (285, 182): (21, 72),
    (285, 189): (12, 9),
    (285, 213): (25, -60),
    (285, 216): (10, -24),
    (285, 220): (-3, 4),
    (285, 245): (-15, 20),
    (285, 253): (120, -27),
    (285, 259): (132, 55),
    (285, 262): (45, 24),
    (285, 273): (312, -91),
    (285, 279): (-15, -36),
    (286, 7): (-14, -48),
    (286, 9): (-110, 264),
    (286, 12): (65, 72),
    (286, 17): (132, -55),
    (286, 35): (-182, -120),
    (286, 37): (994, -3408),
    (286, 56): (96, -280),
    (286, 58): (-1794, -992),
    (286, 59): (-44, -117),
    (286, 60): (55, -48),
    (286, 84): (77, -36),
    (286, 105): (16, -63),
    (286, 126): (-312, -234),
    (286, 161): (-770, -672),
    (286, 164): (91, 60),
    (286, 179): (156, -133),
    (286, 212): (-2415, -1768),
    (286, 220): (48, -20),
    (286, 222): (70, -240),
    (286, 229): (-20, 21),
    (286, 231): (10, 24),
    (286, 250): (592, -1110),
    (286, 252): (-18, 24),
    (286, 262): (-114, 352),
    (286, 277): (-30, 40),
    (287, 15): (35, 120),
    (287, 26): (-112, 66),
    (287, 40): (119, -120),
    (287, 46): (63, 16),
    (287, 50): (119, 120),
    (287, 57): (-168, -99),
    (287, 66): (40, -30),
    (287, 72): (7, -24),
    (287, 73): (224, -207),
    (287, 104): (-63, -16),
    (287, 110): (-1209, -280),
    (287, 125): (-28, 45),
    (287, 130): (56, -90),
    (287, 157): (-4084, -3063),
    (287, 181): (-133, -456),
    (287, 187): (56, -33),
    (287, 195): (-105, -36),
    (287, 209): (3, -4),
    (287, 219): (-28, -45),
    (287, 240): (15, 36),
    (287, 242): (80, 18),
    (287, 249): (12, 9),
    (287, 254): (119, -120),
    (287, 278): (-2728, -954),
    (287, 281): (420, -175),
    (288, 17): (-72, -21),
    (288, 38): (-48, -14),
    (288, 54): (-20, -21),
    (288, 74): (48, 20),
    (288, 79): (36, 15),
    (288, 91): (36, 27),
    (288, 100): (24, -10),
    (288, 140): (-24, 10),
    (288, 178): (-48, -20),
    (288, 222): (-4, 3),
    (288, 249): (20, 48),
    (288, 270): (-36, 27),
    (289, 6): (-39, 252),
    (289, 15): (-35, -120),
    (289, 20): (91, 60),
    (289, 29): (220, -231),
    (289, 60): (65, -72),
    (289, 83): (25, 60),
    (289, 91): (156, -65),
    (289, 97): (-2795, -1188),
    (289, 98): (-63, -16),
    (289, 99): (36, -105),
    (289, 109): (-6456, -1883),
    (289, 130): (-63, 16),
    (289, 132): (-26, -168),
    (289, 146): (-272, 546),
    (289, 172): (51, -68),
    (289, 175): (-272, -225),
    (289, 176): (135, -352),
    (289, 192): (16, 12),
    (289, 195): (-63, 60),
    (289, 227): (76, -57),
    (289, 288): (14, 48),
    (290, 65): (522, -760),
    (290, 83): (-460, 483),
    (290, 98): (6026, -16632),
    (290, 106): (-2542, -720),
    (290, 111): (80, 39),
    (290, 128): (15, -112),
    (290, 152): (-60, 32),
    (290, 187): (-220, 459),
    (290, 189): (20, 21),
    (290, 204): (15, -36),
    (290, 212): (65, 72),
    (290, 238): (-16, 30),
    (290, 247): (-130, 312),
    (290, 268): (171, -140),
    (290, 271): (-16, 63),
    (290, 278): (26, 168),
}


BOX_THREE_HUNDRED_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (291, 9): (119, -120),
    (291, 47): (36, 15),
    (291, 62): (-24, -18),
    (291, 68): (-6, 8),
    (291, 77): (-105, -88),
    (291, 96): (-32, 60),
    (291, 104): (-108, 144),
    (291, 147): (-105, -56),
    (291, 169): (-129, -172),
    (291, 208): (-39, -80),
    (291, 226): (-45, 28),
    (291, 238): (-21, -28),
    (291, 260): (-45, -60),
    (291, 261): (-105, -36),
    (291, 285): (260, -195),
    (292, 10): (-20, -15),
    (292, 20): (88, 105),
    (292, 27): (-28, -45),
    (292, 42): (72, 21),
    (292, 45): (-16, -30),
    (292, 48): (-5, -12),
    (292, 62): (-456, -133),
    (292, 69): (40, 30),
    (292, 91): (12, -5),
    (292, 97): (12, -5),
    (292, 136): (-228, -95),
    (292, 139): (-20, 48),
    (292, 143): (64, 48),
    (292, 199): (52, -39),
    (292, 220): (-440, 525),
    (292, 231): (-8, 6),
    (292, 277): (52, 39),
    (292, 283): (-192, -80),
    (293, 10): (104, -330),
    (293, 19): (-52, -165),
    (293, 58): (-1120, -6222),
    (293, 59): (10616, -19905),
    (293, 66): (-200, -210),
    (293, 75): (72, 135),
    (293, 94): (72, 154),
    (293, 110): (429, -460),
    (293, 143): (-847, -396),
    (293, 149): (-7, 24),
    (293, 165): (20, -15),
    (293, 182): (-147, 140),
    (293, 194): (-568, -426),
    (293, 217): (33, -56),
    (293, 231): (77, 36),
    (293, 248): (5, -12),
    (293, 254): (117, 44),
    (293, 277): (-55, 132),
    (293, 280): (-48, -140),
    (293, 282): (189, -48),
    (294, 4): (-42, 56),
    (294, 12): (-42, -40),
    (294, 23): (84, 135),
    (294, 30): (-56, -90),
    (294, 40): (105, 88),
    (294, 61): (30, -16),
    (294, 73): (-54, -72),
    (294, 83): (-84, -13),
    (294, 87): (-56, -33),
    (294, 92): (6, 8),
    (294, 100): (-21, 20),
    (294, 109): (-84, 13),
    (294, 121): (114, -152),
    (294, 122): (144, 42),
    (294, 143): (-126, -32),
    (294, 174): (-130, -144),
    (294, 218): (-216, -462),
    (294, 235): (42, -40),
    (294, 257): (126, -168),
    (294, 260): (-48, -20),
    (294, 261): (-36, -27),
    (294, 268): (6, 8),
    (294, 270): (30, 72),
    (294, 289): (-420, 441),
    (295, 7): (-140, -225),
    (295, 18): (95, 168),
    (295, 19): (75, 40),
    (295, 24): (195, -216),
    (295, 46): (207, -920),
    (295, 65): (-20, -15),
    (295, 117): (180, -135),
    (295, 154): (175, -288),
    (295, 182): (-80, -18),
    (295, 184): (160, -168),
    (295, 214): (15, 112),
    (295, 228): (55, 48),
    (295, 245): (-765, -868),
    (295, 255): (20, 15),
    (295, 271): (75, 40),
    (295, 290): (-33, 44),
    (295, 291): (100, 75),
    (296, 24): (10, -24),
    (296, 55): (-16, 30),
    (296, 71): (56, -90),
    (296, 76): (-208, 306),
    (296, 80): (-12, 5),
    (296, 102): (-56, -33),
    (296, 106): (-52, -39),
    (296, 133): (56, 33),
    (296, 162): (40, -30),
    (296, 164): (-240, -238),
    (296, 200): (48, 14),
    (296, 221): (-120, -391),
    (296, 241): (48, 55),
    (296, 242): (44, -33),
    (296, 260): (21, 20),
    (296, 267): (40, 75),
    (296, 276): (-36, 27),
    (296, 281): (-40, -96),
    (297, 2): (-264, -950),
    (297, 14): (72, 154),
    (297, 15): (45, -24),
    (297, 30): (-648, 270),
    (297, 35): (-39, 80),
    (297, 43): (21, -72),
    (297, 50): (-63, -16),
    (297, 75): (72, -65),
    (297, 93): (108, 45),
    (297, 104): (-18, 24),
    (297, 106): (57, 176),
    (297, 119): (72, -21),
    (297, 153): (-75, 308),
    (297, 173): (24, -7),
    (297, 191): (-303, -404),
    (297, 204): (9, -12),
    (297, 205): (72, 65),
    (297, 219): (268, -201),
    (297, 257): (33, 180),
    (297, 272): (9, 12),
    (298, 7): (88, -105),
    (298, 8): (183, -244),
    (298, 19): (60, -221),
    (298, 21): (108, -315),
    (298, 70): (-3624, 1510),
    (298, 72): (18, -24),
    (298, 86): (66, -88),
    (298, 92): (33, -544),
    (298, 105): (108, -231),
    (298, 154): (-3080, -4350),
    (298, 169): (760, -5751),
    (298, 177): (60, -63),
    (298, 187): (-170, -408),
    (298, 188): (-105, -208),
    (298, 195): (60, -45),
    (298, 196): (25, 60),
    (298, 208): (60, -32),
    (298, 229): (-42, 40),
    (298, 236): (-6, 8),
    (298, 240): (10, 24),
    (298, 246): (-80, 150),
    (298, 259): (-152, -285),
    (299, 28): (-85, -132),
    (299, 34): (-24, 70),
    (299, 38): (-1581, -4180),
    (299, 42): (99, -168),
    (299, 59): (-13, 84),
    (299, 62): (-1221, 140),
    (299, 71): (-29836, -22377),
    (299, 77): (-520, -231),
    (299, 88): (-195, -104),
    (299, 97): (35, 120),
    (299, 113): (156, -667),
    (299, 127): (-345, 460),
    (299, 147): (364, -273),
    (299, 165): (91, 60),
    (299, 183): (-25, -60),
    (299, 190): (99, -20),
    (299, 197): (35, 120),
    (299, 216): (-5, -12),
    (299, 225): (-513, -420),
    (299, 227): (-481, -3108),
    (299, 248): (-391, -120),
    (299, 267): (-105, -36),
    (299, 272): (24, 32),
    (299, 280): (209, -120),
    (299, 294): (-16, 30),
    (299, 297): (24, 45),
    (300, 12): (60, -32),
    (300, 45): (60, -25),
    (300, 46): (120, 27),
    (300, 102): (60, 32),
    (300, 112): (45, -24),
    (300, 137): (36, 27),
    (300, 168): (-25, -60),
    (300, 171): (-20, 15),
    (300, 184): (12, 9),
    (300, 201): (16, -12),
    (300, 206): (-48, -55),
    (300, 227): (60, -11),
}


BOX_THREE_TEN_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (301, 2): (-483, -460),
    (301, 11): (-63, -16),
    (301, 15): (48, -189),
    (301, 17): (-7175, -1140),
    (301, 37): (-840, -3875),
    (301, 78): (80, 18),
    (301, 81): (-91, 312),
    (301, 104): (49, 168),
    (301, 107): (57, -76),
    (301, 108): (126, 168),
    (301, 114): (-35, -84),
    (301, 116): (21, 20),
    (301, 141): (85, 204),
    (301, 155): (-155, 372),
    (301, 173): (-5439, -7252),
    (301, 218): (-24, -10),
    (301, 233): (-224, -207),
    (301, 234): (5, 12),
    (301, 236): (-35, -84),
    (301, 249): (65, 72),
    (301, 296): (-98, 336),
    (302, 2): (-33306, 25208),
    (302, 21): (-150, 360),
    (302, 47): (78, -160),
    (302, 68): (-3999, -3400),
    (302, 98): (120, -22),
    (302, 128): (-805, -348),
    (302, 143): (-1666, -2112),
    (302, 151): (-1308, -545),
    (302, 161): (-88, 105),
    (302, 163): (530, -1272),
    (302, 166): (-48, 286),
    (302, 172): (1397, -8004),
    (302, 206): (822, -1096),
    (302, 213): (42, 144),
    (302, 219): (380, -285),
    (302, 229): (890, -2136),
    (302, 242): (-10, -24),
    (302, 247): (-9064, -8673),
    (302, 254): (-168, -874),
    (302, 262): (-154, 72),
    (302, 294): (32, 126),
    (302, 299): (-28, 195),
    (302, 301): (-220, -459),
    (303, 7): (147, 140),
    (303, 11): (-33, 56),
    (303, 18): (48, -14),
    (303, 22): (63, -216),
    (303, 31): (-105, -88),
    (303, 48): (15, -36),
    (303, 67): (-165, -88),
    (303, 74): (-57, -76),
    (303, 80): (-96, 40),
    (303, 150): (48, 14),
    (303, 167): (15, -8),
    (303, 193): (-516, -215),
    (303, 213): (35, 12),
    (303, 280): (-12, 16),
    (303, 294): (15, -36),
    (303, 297): (28, 45),
    (304, 8): (-32, 60),
    (304, 9): (-16, -63),
    (304, 12): (80, -18),
    (304, 35): (40, -42),
    (304, 42): (-16, -30),
    (304, 57): (24, -45),
    (304, 79): (-308, 495),
    (304, 118): (64, 48),
    (304, 120): (-20, -15),
    (304, 138): (-56, 33),
    (304, 166): (-32, -24),
    (304, 169): (-48, 55),
    (304, 187): (16, 12),
    (304, 203): (12, -16),
    (304, 212): (40, 42),
    (304, 226): (120, -119),
    (304, 239): (-24, -7),
    (304, 244): (-48, -20),
    (304, 259): (-32, -126),
    (304, 285): (40, -30),
    (305, 13): (-280, -351),
    (305, 42): (25, -60),
    (305, 55): (105, 100),
    (305, 82): (65, -156),
    (305, 91): (60, 175),
    (305, 110): (-40, -42),
    (305, 111): (85, 132),
    (305, 117): (160, -231),
    (305, 142): (-40, -42),
    (305, 149): (-355, -852),
    (305, 162): (25, 60),
    (305, 195): (-91, -60),
    (305, 204): (32, 24),
    (305, 240): (-10, -24),
    (305, 251): (20, 99),
    (305, 254): (80, -18),
    (305, 266): (105, 56),
    (305, 273): (-35, -84),
    (305, 274): (425, -168),
    (305, 285): (-27, 36),
    (305, 286): (-400, -90),
    (305, 287): (105, -88),
    (305, 289): (8, -15),
    (305, 303): (5, -12),
    (306, 13): (126, 32),
    (306, 39): (36, -105),
    (306, 56): (-78, -104),
    (306, 66): (-72, -30),
    (306, 78): (-54, -72),
    (306, 95): (18, -80),
    (306, 111): (-24, 7),
    (306, 113): (-264, -23),
    (306, 120): (-9, 12),
    (306, 130): (42, -40),
    (306, 157): (126, -32),
    (306, 160): (-45, 28),
    (306, 176): (87, -116),
    (306, 185): (-42, 40),
    (306, 230): (-30, 40),
    (306, 231): (-72, 135),
    (306, 234): (-390, -56),
    (306, 235): (396, -165),
    (306, 277): (414, -448),
    (306, 286): (96, 110),
    (307, 16): (55, -48),
    (307, 42): (120, 126),
    (307, 70): (280, -294),
    (307, 105): (35, -120),
    (307, 116): (175, -60),
    (307, 151): (124, -93),
    (307, 152): (112, 180),
    (307, 161): (27, -364),
    (307, 172): (192, -80),
    (307, 173): (-10068, -4195),
    (307, 179): (-11925, -14416),
    (307, 191): (-1953, -1504),
    (307, 196): (-77, 36),
    (307, 203): (120, 119),
    (307, 220): (-50, -120),
    (307, 234): (208, -306),
    (307, 261): (119, 120),
    (307, 263): (-35144, -28017),
    (307, 285): (-8, -15),
    (307, 291): (7, -24),
    (307, 303): (492, -369),
    (308, 13): (20, -21),
    (308, 15): (-56, 42),
    (308, 18): (28, -45),
    (308, 33): (48, -36),
    (308, 39): (128, -96),
    (308, 60): (-56, 33),
    (308, 74): (140, 48),
    (308, 76): (20, -99),
    (308, 85): (-88, 165),
    (308, 89): (48, 20),
    (308, 96): (-77, -36),
    (308, 106): (56, 42),
    (308, 108): (28, 45),
    (308, 123): (-16, -12),
    (308, 141): (20, 21),
    (308, 174): (140, 48),
    (308, 186): (28, 21),
    (308, 187): (12, -35),
    (308, 202): (-120, -119),
    (308, 212): (20, -48),
    (308, 215): (48, 20),
    (308, 221): (180, -19),
    (308, 227): (12, 5),
    (308, 236): (-28, 96),
    (308, 251): (-60, -25),
    (308, 255): (-16, 12),
    (308, 256): (-12, 16),
    (308, 297): (-44, 33),
    (309, 7): (-147, 140),
    (309, 39): (57, -76),
    (309, 45): (100, -75),
    (309, 54): (21, 20),
    (309, 84): (-21, -20),
    (309, 91): (-435, 308),
    (309, 102): (85, 132),
    (309, 107): (24, -45),
    (309, 110): (45, -60),
    (309, 112): (21, 28),
    (309, 122): (-120, 50),
    (309, 137): (9, 12),
    (309, 150): (-91, 60),
    (309, 161): (144, 17),
    (309, 175): (84, 35),
    (309, 201): (-119, -120),
    (309, 213): (9, -12),
    (309, 229): (-36, 77),
    (309, 247): (21, 72),
    (309, 263): (-15, 20),
    (309, 266): (144, -130),
    (309, 273): (25, 60),
    (309, 275): (36, 15),
    (310, 22): (24, 70),
    (310, 24): (30, -72),
    (310, 27): (90, 48),
    (310, 36): (63, -60),
    (310, 42): (-90, -48),
    (310, 63): (-230, -504),
    (310, 77): (90, 56),
    (310, 95): (-42, -40),
    (310, 104): (70, -24),
    (310, 118): (30, 16),
    (310, 126): (40, -42),
    (310, 127): (120, -209),
    (310, 144): (13, 84),
    (310, 157): (940, -987),
    (310, 158): (-50, 120),
    (310, 185): (70, 24),
    (310, 197): (-20, 21),
    (310, 225): (-50, 120),
    (310, 245): (-6, 8),
    (310, 273): (-20, -15),
    (310, 287): (90, 56),
    (310, 298): (1456, -1230),
    (310, 301): (120, -35),
}


BOX_THREE_TWENTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (311, 5): (11, 60),
    (311, 40): (-39, -80),
    (311, 47): (23240, -30525),
    (311, 89): (140, -51),
    (311, 92): (140, -48),
    (311, 97): (-340, 357),
    (311, 105): (-4, -3),
    (311, 138): (-25, -60),
    (311, 141): (-40, 9),
    (311, 142): (80, -18),
    (311, 149): (-217, -456),
    (311, 180): (-14, -48),
    (311, 197): (-25480, -34191),
    (311, 209): (51, 140),
    (311, 226): (56, 90),
    (311, 232): (1589, -5448),
    (311, 252): (-9, 12),
    (311, 253): (-2589, -3452),
    (311, 275): (-88, -105),
    (311, 293): (-424, -795),
    (311, 299): (-5565, -4108),
    (312, 23): (72, -21),
    (312, 70): (-24, 18),
    (312, 85): (-48, -20),
    (312, 103): (96, 40),
    (312, 126): (-12, -9),
    (312, 133): (-24, -7),
    (312, 141): (4, -3),
    (312, 147): (4, 3),
    (312, 155): (12, -5),
    (312, 184): (24, -32),
    (312, 218): (48, 20),
    (312, 233): (252, -64),
    (312, 240): (-4, 3),
    (312, 245): (-24, -7),
    (312, 252): (-12, 9),
    (312, 258): (-16, 12),
    (312, 279): (48, -36),
    (312, 292): (24, 32),
    (313, 6): (-119, -120),
    (313, 13): (24120, -27911),
    (313, 21): (133, 156),
    (313, 28): (28, 96),
    (313, 31): (-10412, -7809),
    (313, 105): (40, -75),
    (313, 122): (-1815, 968),
    (313, 130): (456, -650),
    (313, 136): (-1722, -1640),
    (313, 144): (25, 60),
    (313, 175): (133, 156),
    (313, 193): (-12, -35),
    (313, 210): (-15, -36),
    (313, 221): (33, 56),
    (313, 255): (40, 75),
    (313, 259): (76, -57),
    (313, 260): (-65, -420),
    (313, 279): (-299, -180),
    (313, 297): (-352, -135),
    (314, 4): (-9, 40),
    (314, 25): (-136, -255),
    (314, 35): (132, -85),
    (314, 37): (-540, -2891),
    (314, 38): (368, -690),
    (314, 51): (44, -117),
    (314, 54): (34, -288),
    (314, 94): (-190, -456),
    (314, 100): (144, -308),
    (314, 145): (-238, -240),
    (314, 184): (-70, 24),
    (314, 185): (42, -40),
    (314, 207): (70, 24),
    (314, 220): (105, 100),
    (314, 221): (104, -195),
    (314, 231): (-60, 63),
    (314, 234): (-310, -936),
    (314, 245): (276, -115),
    (314, 263): (90, 56),
    (314, 275): (-918, 440),
    (314, 285): (30, 72),
    (314, 308): (234, -88),
    (314, 313): (-5766, -7688),
    (315, 8): (-15, 112),
    (315, 37): (-1965, -1048),
    (315, 41): (147, 140),
    (315, 55): (63, 16),
    (315, 59): (60, 91),
    (315, 68): (-15, -36),
    (315, 72): (-21, 20),
    (315, 89): (15, -36),
    (315, 93): (135, -180),
    (315, 94): (-45, 28),
    (315, 111): (60, -25),
    (315, 115): (-189, -340),
    (315, 122): (-45, -28),
    (315, 146): (-45, 108),
    (315, 156): (-15, -20),
    (315, 166): (120, -50),
    (315, 169): (-105, 140),
    (315, 187): (-105, 252),
    (315, 214): (-525, -92),
    (315, 221): (60, -175),
    (315, 228): (-5, -12),
    (315, 234): (147, -140),
    (315, 271): (-273, 180),
    (315, 289): (-180, -19),
    (315, 292): (-21, -28),
    (315, 304): (-42, -56),
    (316, 4): (-20, -48),
    (316, 9): (-48, 36),
    (316, 11): (28, 45),
    (316, 24): (-20, -21),
    (316, 26): (136, -273),
    (316, 46): (-24, -143),
    (316, 47): (-48, 20),
    (316, 73): (-20, 21),
    (316, 74): (-476, 480),
    (316, 82): (-48, 55),
    (316, 102): (56, 33),
    (316, 115): (-84, -80),
    (316, 124): (40, 9),
    (316, 147): (60, -45),
    (316, 175): (-20, -15),
    (316, 180): (36, 15),
    (316, 201): (20, -21),
    (316, 208): (-84, 13),
    (316, 226): (24, 7),
    (316, 241): (-12, -5),
    (316, 242): (36, 77),
    (316, 243): (-4, 3),
    (316, 252): (16, -63),
    (316, 255): (-12, 9),
    (316, 301): (156, 133),
    (316, 310): (-152, -285),
    (317, 35): (9, -40),
    (317, 66): (-176, -210),
    (317, 69): (81, -108),
    (317, 73): (-844, 633),
    (317, 108): (20, 48),
    (317, 109): (-231, 520),
    (317, 118): (5, -12),
    (317, 143): (44, -117),
    (317, 155): (-184, -513),
    (317, 164): (-33, 44),
    (317, 169): (44, 33),
    (317, 192): (135, 72),
    (317, 211): (-903, -704),
    (317, 218): (-2680, 2814),
    (317, 220): (-25, -60),
    (317, 237): (-228, -1071),
    (317, 260): (18, 80),
    (317, 290): (56, -90),
    (317, 309): (-175, -60),
    (317, 316): (-100, -240),
    (318, 12): (33, -56),
    (318, 14): (198, -336),
    (318, 61): (-78, -104),
    (318, 98): (54, -72),
    (318, 104): (3, -4),
    (318, 139): (-12, 35),
    (318, 153): (108, 81),
    (318, 155): (42, 40),
    (318, 163): (66, -112),
    (318, 198): (-330, -288),
    (318, 201): (18, -24),
    (318, 225): (-42, 144),
    (318, 231): (-552, -385),
    (318, 253): (-12, -35),
    (318, 274): (6, 8),
    (318, 282): (-154, -72),
    (318, 287): (-24, 7),
    (318, 293): (-12, 5),
    (318, 300): (30, 40),
    (318, 308): (-39, -52),
    (319, 13): (91, -312),
    (319, 30): (119, -120),
    (319, 49): (7, 24),
    (319, 56): (-476, 480),
    (319, 64): (-384, -440),
    (319, 124): (13, -84),
    (319, 163): (-1605, 856),
    (319, 194): (-14241, -18988),
    (319, 208): (15, -20),
    (319, 225): (35, 12),
    (319, 243): (275, -240),
    (319, 254): (-1449, -1720),
    (319, 260): (132, 176),
    (319, 273): (44, 33),
    (319, 287): (88, -105),
    (319, 315): (-33, 180),
    (320, 3): (144, 60),
    (320, 17): (-520, 576),
    (320, 29): (-40, -9),
    (320, 48): (-30, -72),
    (320, 60): (32, -24),
    (320, 77): (20, -48),
    (320, 139): (12, -5),
    (320, 164): (35, 12),
    (320, 169): (56, 192),
    (320, 178): (-16, -12),
    (320, 186): (-16, -12),
    (320, 195): (40, 30),
    (320, 207): (40, 42),
    (320, 211): (48, -14),
    (320, 252): (-8, 6),
    (320, 300): (20, -15),
    (320, 316): (-40, -9),
}


BOX_THREE_THIRTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (321, 39): (-1128, -329),
    (321, 47): (36, -105),
    (321, 63): (-1260, -945),
    (321, 70): (24, 10),
    (321, 72): (6, -8),
    (321, 80): (96, -40),
    (321, 115): (-435, 232),
    (321, 119): (33, -56),
    (321, 121): (237, -316),
    (321, 149): (120, -119),
    (321, 151): (105, 88),
    (321, 154): (-15, -36),
    (321, 165): (100, 105),
    (321, 191): (-24, 7),
    (321, 247): (-3, 4),
    (321, 249): (5, 12),
    (321, 264): (-30, -16),
    (321, 266): (-543, -724),
    (321, 306): (9, 40),
    (321, 318): (120, 50),
    (322, 11): (-210, 176),
    (322, 20): (112, -180),
    (322, 31): (-3350, -3864),
    (322, 32): (49, 168),
    (322, 54): (-56, -42),
    (322, 55): (-378, -680),
    (322, 68): (112, 180),
    (322, 94): (-518, -1776),
    (322, 99): (-28, -21),
    (322, 106): (10, -24),
    (322, 123): (14, 48),
    (322, 125): (42, -40),
    (322, 130): (-30, 16),
    (322, 135): (70, 240),
    (322, 137): (-1008, -3055),
    (322, 153): (36, 105),
    (322, 164): (-63, -16),
    (322, 172): (7, -24),
    (322, 174): (-550, -480),
    (322, 179): (30, -40),
    (322, 185): (112, -15),
    (322, 219): (90, -216),
    (322, 239): (-120, 119),
    (322, 241): (210, -200),
    (322, 278): (-870, -616),
    (322, 289): (1498, -5136),
    (322, 302): (42, -40),
    (323, 4): (35, -612),
    (323, 40): (-247, -96),
    (323, 49): (-5605, -2772),
    (323, 61): (87, -116),
    (323, 67): (15, -8),
    (323, 79): (-1105, 300),
    (323, 80): (-7, -24),
    (323, 82): (-1645, -492),
    (323, 93): (8, -15),
    (323, 103): (-24753, -18704),
    (323, 121): (-3705, -2900),
    (323, 131): (888, -1225),
    (323, 145): (171, -140),
    (323, 168): (-13, -84),
    (323, 172): (-145, 348),
    (323, 173): (24, -7),
    (323, 206): (11, -60),
    (323, 208): (285, -152),
    (323, 222): (-165, -144),
    (323, 231): (-77, 36),
    (323, 234): (-5, -12),
    (323, 236): (3, -4),
    (323, 245): (-132, -55),
    (323, 247): (-112, 15),
    (323, 264): (-7, -24),
    (323, 298): (-112, 66),
    (323, 299): (276, -805),
    (323, 312): (-7, 24),
    (324, 57): (-12, 5),
    (324, 70): (36, -105),
    (324, 76): (36, 160),
    (324, 91): (-48, -64),
    (324, 115): (24, -10),
    (324, 183): (40, -30),
    (324, 188): (120, 35),
    (324, 193): (-12, -5),
    (324, 195): (-12, 5),
    (324, 203): (-12, 5),
    (324, 221): (48, 14),
    (324, 249): (-4, 3),
    (324, 253): (36, -77),
    (324, 307): (60, -45),
    (325, 34): (85, -204),
    (325, 40): (130, 144),
    (325, 55): (-375, -200),
    (325, 62): (85, 132),
    (325, 72): (45, -24),
    (325, 83): (-13740, -5725),
    (325, 89): (-60, -91),
    (325, 103): (-95, 168),
    (325, 106): (85, -132),
    (325, 124): (45, 28),
    (325, 135): (-60, -45),
    (325, 148): (-60, -32),
    (325, 149): (117, 44),
    (325, 152): (300, -160),
    (325, 159): (180, -189),
    (325, 229): (105, 208),
    (325, 230): (-200, -210),
    (325, 250): (-3, 4),
    (325, 264): (135, -72),
    (325, 271): (-60, 91),
    (325, 278): (-1160, -870),
    (325, 287): (105, 56),
    (325, 289): (-260, 69),
    (325, 306): (40, -198),
    (325, 321): (-15, -36),
    (325, 322): (45, 28),
    (325, 323): (45, -28),
    (326, 28): (-10, -24),
    (326, 37): (-70, 240),
    (326, 50): (-24, -70),
    (326, 54): (56, -90),
    (326, 65): (-136, -255),
    (326, 92): (-759, -280),
    (326, 93): (164, -123),
    (326, 96): (105, 36),
    (326, 111): (56, -33),
    (326, 190): (-24, 70),
    (326, 195): (-30, -72),
    (326, 245): (-852, -355),
    (326, 252): (-26, -168),
    (326, 260): (-325, -360),
    (326, 267): (60, -45),
    (326, 275): (156, -133),
    (326, 306): (88, 66),
    (326, 314): (14, 48),
    (327, 35): (63, -280),
    (327, 36): (-30, -40),
    (327, 38): (-105, -88),
    (327, 50): (63, -60),
    (327, 52): (168, -160),
    (327, 53): (72, 21),
    (327, 106): (-33, -44),
    (327, 120): (96, -40),
    (327, 141): (75, 180),
    (327, 143): (12, 35),
    (327, 153): (-93, 124),
    (327, 158): (-9, -40),
    (327, 172): (-3, -4),
    (327, 223): (-681, -908),
    (327, 270): (-24, -10),
    (327, 276): (60, -80),
    (327, 287): (-24, 7),
    (327, 308): (-9, -12),
    (327, 314): (-33, 44),
    (328, 3): (112, 66),
    (328, 10): (28, -45),
    (328, 21): (-36, 48),
    (328, 44): (-24, -70),
    (328, 49): (48, -14),
    (328, 65): (-24, -70),
    (328, 73): (88, -165),
    (328, 91): (132, -224),
    (328, 96): (20, 21),
    (328, 102): (80, -84),
    (328, 119): (168, -49),
    (328, 138): (4, 3),
    (328, 182): (136, 102),
    (328, 185): (48, 20),
    (328, 201): (48, 36),
    (328, 206): (120, 50),
    (328, 210): (20, -21),
    (328, 219): (-24, -45),
    (328, 221): (12, -16),
    (328, 226): (60, 25),
    (328, 236): (16, -30),
    (328, 250): (-12, -5),
    (328, 257): (-24, -7),
    (328, 301): (-32, -24),
    (328, 310): (48, -140),
    (328, 327): (72, 135),
    (329, 2): (-895, -2148),
    (329, 18): (-175, -60),
    (329, 31): (-28, -45),
    (329, 32): (9, -40),
    (329, 46): (56, -90),
    (329, 54): (385, -336),
    (329, 74): (-7, -24),
    (329, 78): (81, -108),
    (329, 95): (21, 20),
    (329, 100): (-21, -20),
    (329, 113): (-231, -160),
    (329, 117): (-1311, -252),
    (329, 125): (-91, 60),
    (329, 134): (161, -240),
    (329, 135): (-196, 315),
    (329, 136): (144, -308),
    (329, 137): (-91, 60),
    (329, 138): (-56, -42),
    (329, 143): (1445, -2244),
    (329, 148): (-21, 28),
    (329, 158): (1824, -6370),
    (329, 177): (189, -48),
    (329, 180): (54, -72),
    (329, 187): (945, -1700),
    (329, 197): (116, -87),
    (329, 240): (-55, -48),
    (329, 254): (273, -136),
    (329, 255): (5, 12),
    (329, 258): (385, -132),
    (329, 267): (164, 123),
    (329, 269): (44, 117),
    (329, 292): (35, 12),
    (329, 295): (-28, -45),
    (329, 304): (105, -56),
    (329, 318): (-175, -60),
    (329, 325): (-19, 180),
    (330, 23): (-510, 64),
    (330, 47): (120, 119),
    (330, 73): (150, -200),
    (330, 94): (120, 22),
    (330, 116): (15, 8),
    (330, 133): (60, -11),
    (330, 156): (90, 56),
    (330, 159): (234, -88),
    (330, 170): (-1110, -1480),
    (330, 173): (90, 56),
    (330, 212): (45, 60),
    (330, 217): (90, 56),
    (330, 235): (6, -8),
    (330, 243): (30, -72),
    (330, 276): (-70, -24),
    (330, 283): (240, -117),
}


BOX_THREE_FORTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (331, 27): (-264, 495),
    (331, 36): (110, 96),
    (331, 49): (-537, -716),
    (331, 53): (-2444, 1533),
    (331, 78): (16, -30),
    (331, 105): (16, -63),
    (331, 111): (-20, -21),
    (331, 146): (-333, 644),
    (331, 153): (-20, 21),
    (331, 157): (-1524, -635),
    (331, 178): (-5, -12),
    (331, 186): (-5, -12),
    (331, 188): (91, 60),
    (331, 234): (16, -30),
    (331, 246): (-448, -414),
    (331, 253): (1155, -1292),
    (331, 273): (15, 36),
    (331, 308): (-5, -12),
    (331, 319): (-93, -476),
    (331, 326): (-224, 30),
    (332, 30): (24, -45),
    (332, 49): (-4, -3),
    (332, 55): (-4, 3),
    (332, 72): (35, 12),
    (332, 75): (108, 45),
    (332, 103): (80, 39),
    (332, 110): (176, -210),
    (332, 118): (-88, -234),
    (332, 126): (24, -18),
    (332, 139): (20, 48),
    (332, 149): (32, 24),
    (332, 170): (-88, 105),
    (332, 204): (-8, 15),
    (332, 217): (96, 40),
    (332, 218): (20, -48),
    (332, 237): (8, -6),
    (332, 238): (24, 7),
    (332, 253): (-12, -5),
    (332, 259): (-48, -140),
    (332, 273): (-16, 12),
    (332, 279): (-20, 15),
    (332, 289): (-120, -50),
    (332, 299): (-24, 32),
    (332, 321): (-40, 42),
    (333, 12): (10, -24),
    (333, 23): (540, -897),
    (333, 27): (124, -93),
    (333, 34): (-987, 884),
    (333, 43): (165, -52),
    (333, 56): (-3, 4),
    (333, 65): (144, 17),
    (333, 82): (48, 14),
    (333, 90): (144, 42),
    (333, 133): (-5619, -7492),
    (333, 181): (-15, 36),
    (333, 182): (165, -88),
    (333, 183): (105, 88),
    (333, 190): (-315, -80),
    (333, 195): (-63, -60),
    (333, 211): (-612, 459),
    (333, 217): (-24, -143),
    (333, 225): (-15, -36),
    (333, 247): (-1452, 935),
    (333, 289): (36, -15),
    (333, 295): (-24, -45),
    (333, 302): (45, -28),
    (333, 309): (108, -231),
    (334, 17): (100, 105),
    (334, 18): (-26, 168),
    (334, 24): (14, -48),
    (334, 31): (54, -728),
    (334, 50): (8382, -15040),
    (334, 69): (-110, -264),
    (334, 80): (-128, -240),
    (334, 112): (48, 64),
    (334, 119): (294, -280),
    (334, 126): (-40, -42),
    (334, 139): (-966, 88),
    (334, 141): (164, -123),
    (334, 148): (144, -308),
    (334, 164): (-255, -136),
    (334, 167): (-210, 200),
    (334, 169): (-266, -312),
    (334, 210): (-40, 42),
    (334, 245): (70, 168),
    (334, 266): (-176, 330),
    (334, 301): (-156, 133),
    (334, 312): (64, -48),
    (334, 325): (1482, -1160),
    (335, 3): (-340, -357),
    (335, 32): (20, -48),
    (335, 45): (12, 9),
    (335, 46): (-105, 88),
    (335, 63): (-45, -336),
    (335, 81): (80, -315),
    (335, 112): (-15, -8),
    (335, 114): (95, 168),
    (335, 124): (95, 168),
    (335, 138): (135, -72),
    (335, 151): (1635, -2180),
    (335, 175): (20, -21),
    (335, 189): (20, 21),
    (335, 206): (-120, 50),
    (335, 208): (-10, 24),
    (335, 231): (35, -84),
    (335, 236): (110, 96),
    (335, 241): (60, -11),
    (335, 245): (3, -4),
    (335, 283): (255, -32),
    (335, 284): (60, 32),
    (335, 299): (-2532, 1055),
    (335, 319): (-120, -209),
    (335, 325): (104, -195),
    (336, 27): (56, 90),
    (336, 36): (-24, -45),
    (336, 38): (-24, 143),
    (336, 100): (21, 20),
    (336, 101): (24, 10),
    (336, 102): (-16, -12),
    (336, 106): (48, -14),
    (336, 121): (96, -40),
    (336, 153): (80, -39),
    (336, 157): (-24, 7),
    (336, 165): (28, 21),
    (336, 191): (72, 21),
    (336, 194): (168, 95),
    (336, 204): (32, -24),
    (336, 211): (48, 36),
    (336, 220): (51, 68),
    (336, 243): (-8, -15),
    (336, 250): (72, -65),
    (336, 251): (84, 187),
    (336, 271): (48, 55),
    (336, 282): (-20, 15),
    (336, 285): (-28, 45),
    (336, 297): (40, 75),
    (336, 302): (-24, 32),
    (336, 316): (-15, 36),
    (336, 324): (16, -12),
    (337, 18): (40, -42),
    (337, 33): (77, -36),
    (337, 46): (312, -266),
    (337, 51): (40, -9),
    (337, 58): (-824, 618),
    (337, 60): (64, -120),
    (337, 65): (117, 44),
    (337, 80): (7, -24),
    (337, 93): (-27, 120),
    (337, 119): (-363, -616),
    (337, 128): (7, 24),
    (337, 130): (-551, -240),
    (337, 137): (-8, -15),
    (337, 142): (-615, 328),
    (337, 163): (-1628, -885),
    (337, 170): (-2247, -2140),
    (337, 171): (-15, 36),
    (337, 180): (-14, 48),
    (337, 221): (312, -91),
    (337, 228): (-15, -36),
    (337, 235): (-48, 55),
    (337, 248): (-290, -816),
    (337, 249): (-235, 564),
    (337, 271): (-435, -308),
    (337, 294): (-40, -42),
    (338, 25): (-364, 585),
    (338, 28): (15, -8),
    (338, 45): (300, -315),
    (338, 46): (-5272, -3954),
    (338, 49): (-70, 168),
    (338, 67): (-364, 627),
    (338, 73): (-78, 160),
    (338, 76): (18, -80),
    (338, 85): (-12, -35),
    (338, 101): (-3732, -1555),
    (338, 111): (-12, -9),
    (338, 119): (8, 15),
    (338, 134): (152, -114),
    (338, 141): (-36, -27),
    (338, 151): (-1302, 520),
    (338, 158): (-22, 120),
    (338, 162): (-14, 48),
    (338, 175): (240, -161),
    (338, 188): (65, -72),
    (338, 225): (70, 24),
    (338, 238): (168, -26),
    (338, 253): (156, 133),
    (338, 255): (-42, -144),
    (338, 263): (-442, 120),
    (338, 276): (13, -84),
    (338, 281): (-40, -399),
    (338, 291): (-18, 24),
    (338, 295): (50, 120),
    (338, 302): (-190, 456),
    (338, 322): (224, -30),
    (339, 34): (51, 68),
    (339, 83): (120, -209),
    (339, 86): (-21, 20),
    (339, 89): (-57, -76),
    (339, 91): (168, -49),
    (339, 98): (24, -10),
    (339, 105): (-9, -40),
    (339, 111): (-33, -44),
    (339, 138): (40, -42),
    (339, 174): (51, 140),
    (339, 189): (24, -7),
    (339, 190): (51, -140),
    (339, 202): (3, 4),
    (339, 203): (24, 7),
    (339, 210): (40, 30),
    (339, 232): (24, -32),
    (339, 239): (168, 99),
    (339, 286): (-21, 220),
    (339, 324): (3, 4),
    (339, 331): (-57, 76),
    (340, 35): (100, 105),
    (340, 36): (-85, -132),
    (340, 42): (4, -3),
    (340, 55): (4, 3),
    (340, 61): (-20, 99),
    (340, 75): (-56, -90),
    (340, 76): (160, -36),
    (340, 104): (-45, -28),
    (340, 128): (10, 24),
    (340, 131): (-32, -24),
    (340, 141): (20, -15),
    (340, 154): (60, -11),
    (340, 184): (-60, -11),
    (340, 194): (-140, 225),
    (340, 195): (4, -3),
    (340, 223): (96, 40),
    (340, 233): (-24, -7),
    (340, 243): (8, -6),
    (340, 257): (-80, -84),
    (340, 260): (60, -91),
    (340, 286): (-60, 91),
    (340, 296): (172, -129),
    (340, 334): (-20, 15),
}


BOX_THREE_FIFTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {
    (341, 18): (736, -930),
    (341, 32): (-55, -48),
    (341, 34): (-123, -836),
    (341, 70): (-187, -84),
    (341, 71): (-55, -132),
    (341, 98): (-75, 308),
    (341, 101): (56, 33),
    (341, 111): (-91, 60),
    (341, 120): (-91, -60),
    (341, 123): (-55, -132),
    (341, 153): (2945, -4032),
    (341, 167): (180, -385),
    (341, 169): (-7, 24),
    (341, 188): (33, 44),
    (341, 190): (-1219, -1140),
    (341, 200): (33, 56),
    (341, 206): (77, 36),
    (341, 223): (176, -57),
    (341, 224): (-33, 56),
    (341, 237): (9, -12),
    (341, 258): (16, 30),
    (341, 270): (-35, -12),
    (341, 304): (-10, 24),
    (341, 323): (-18139, -8148),
    (341, 336): (-64, 120),
    (342, 9): (30, -16),
    (342, 11): (-378, 96),
    (342, 39): (-78, 104),
    (342, 67): (90, -48),
    (342, 70): (-48, 14),
    (342, 87): (90, 48),
    (342, 98): (216, -462),
    (342, 102): (102, -136),
    (342, 110): (-456, 190),
    (342, 115): (-30, -40),
    (342, 128): (123, -164),
    (342, 135): (-8, 15),
    (342, 151): (210, -200),
    (342, 161): (-18, 80),
    (342, 187): (-126, 32),
    (342, 200): (-18, -24),
    (342, 208): (93, -124),
    (342, 217): (-288, -175),
    (342, 229): (-108, -315),
    (342, 256): (36, 48),
    (342, 264): (27, -36),
    (342, 294): (-18, 24),
    (342, 319): (-30, 40),
    (343, 8): (-297, -304),
    (343, 12): (20, 48),
    (343, 16): (28, 96),
    (343, 17): (-6821, -64260),
    (343, 22): (-1457, 624),
    (343, 39): (-17, 144),
    (343, 52): (115, -252),
    (343, 57): (20, 21),
    (343, 62): (63, -280),
    (343, 69): (7, 24),
    (343, 86): (63, -16),
    (343, 94): (112, -66),
    (343, 95): (-9, -40),
    (343, 129): (28, 21),
    (343, 131): (-804, 335),
    (343, 153): (28, 45),
    (343, 164): (7, 24),
    (343, 165): (91, 60),
    (343, 170): (63, -280),
    (343, 181): (63, 16),
    (343, 198): (55, -132),
    (343, 199): (124, -93),
    (343, 204): (18, -24),
    (343, 218): (168, -70),
    (343, 229): (-692, -519),
    (343, 246): (312, -234),
    (343, 247): (208, -105),
    (343, 250): (408, -170),
    (343, 256): (210, -200),
    (343, 264): (55, 48),
    (343, 277): (-4284, -15587),
    (343, 282): (15, 36),
    (343, 296): (7, -24),
    (343, 303): (68, 51),
    (343, 328): (24, -32),
    (344, 26): (-16, -12),
    (344, 35): (32, 60),
    (344, 52): (120, 22),
    (344, 56): (21, 20),
    (344, 72): (-20, 99),
    (344, 95): (80, 18),
    (344, 103): (-40, -9),
    (344, 157): (120, -50),
    (344, 163): (24, 7),
    (344, 178): (104, 78),
    (344, 182): (84, -13),
    (344, 214): (12, -35),
    (344, 231): (-24, -45),
    (344, 233): (12, -16),
    (344, 240): (12, -9),
    (344, 276): (-12, 9),
    (344, 277): (48, 55),
    (344, 298): (-120, -50),
    (344, 299): (24, 143),
    (344, 315): (-16, -63),
    (344, 322): (-36, -77),
    (344, 324): (-44, 33),
    (344, 339): (40, 42),
    (344, 341): (192, 56),
    (345, 3): (133, -156),
    (345, 14): (105, -56),
    (345, 27): (45, -28),
    (345, 55): (165, 88),
    (345, 78): (-175, -60),
    (345, 87): (-915, -488),
    (345, 134): (-159, 212),
    (345, 165): (45, -60),
    (345, 183): (316, -237),
    (345, 189): (-40, 9),
    (345, 199): (132, -85),
    (345, 204): (-15, -20),
    (345, 211): (165, -88),
    (345, 214): (48, -90),
    (345, 224): (30, -40),
    (345, 234): (-15, -36),
    (345, 241): (-60, -11),
    (345, 266): (-15, -112),
    (345, 269): (-2580, -1075),
    (345, 279): (-60, 63),
    (345, 295): (180, 75),
    (345, 318): (48, 14),
    (345, 337): (-15, -20),
    (346, 27): (-28, 195),
    (346, 44): (-704, 228),
    (346, 49): (66, 112),
    (346, 57): (-14, -48),
    (346, 62): (-200, -210),
    (346, 70): (-9222, -4760),
    (346, 82): (16026, -21368),
    (346, 96): (-45, -24),
    (346, 117): (-4, -3),
    (346, 121): (-110, -96),
    (346, 131): (-110, 264),
    (346, 168): (26, -168),
    (346, 194): (-10374, -5032),
    (346, 211): (190, -456),
    (346, 237): (-130, 144),
    (346, 252): (80, -60),
    (346, 265): (-342, -1520),
    (346, 272): (-6, 8),
    (346, 273): (80, -39),
    (346, 274): (-182, 120),
    (346, 282): (-984, 738),
    (346, 287): (-528, 455),
    (346, 299): (138, -520),
    (346, 300): (16, 12),
    (346, 309): (-14, -48),
    (346, 335): (-182, -120),
    (346, 342): (50, 120),
    (346, 343): (-224, 207),
    (347, 54): (24, 18),
    (347, 65): (468, -595),
    (347, 89): (-1113, 1184),
    (347, 93): (-745, -1788),
    (347, 96): (-17, -144),
    (347, 98): (72, -154),
    (347, 149): (40700, -53655),
    (347, 162): (160, 78),
    (347, 182): (35, -84),
    (347, 187): (72, -65),
    (347, 201): (100, 105),
    (347, 208): (165, 88),
    (347, 316): (-10, -24),
    (347, 320): (-30, -16),
    (347, 329): (-33, 44),
    (347, 330): (152, 114),
    (348, 67): (96, 28),
    (348, 78): (-312, -130),
    (348, 99): (-72, -54),
    (348, 106): (36, 15),
    (348, 122): (120, 27),
    (348, 136): (-3, 4),
    (348, 140): (-12, 35),
    (348, 151): (-48, -14),
    (348, 154): (-72, -21),
    (348, 161): (48, 36),
    (348, 190): (-60, 45),
    (348, 197): (-12, 5),
    (348, 200): (18, 24),
    (348, 213): (32, -24),
    (348, 237): (16, -12),
    (348, 265): (-12, -5),
    (348, 281): (36, 15),
    (348, 297): (-20, 21),
    (348, 315): (12, -5),
    (348, 343): (-12, -35),
    (348, 344): (-30, -16),
    (349, 16): (-266, -312),
    (349, 17): (-95, -168),
    (349, 35): (-15, 8),
    (349, 51): (140, 171),
    (349, 67): (-24420, -15725),
    (349, 68): (93, -124),
    (349, 88): (-260, 288),
    (349, 121): (-10199, -22440),
    (349, 145): (-80, -315),
    (349, 154): (-435, -308),
    (349, 170): (-176, -330),
    (349, 172): (-35, 12),
    (349, 191): (-36, 323),
    (349, 205): (-4095, -3128),
    (349, 207): (-36, 27),
    (349, 248): (-15, 8),
    (349, 257): (-36, 77),
    (349, 262): (160, -78),
    (349, 264): (-42, 144),
    (349, 270): (5, 12),
    (349, 276): (-35, -12),
    (349, 285): (-56, 33),
    (349, 298): (24, 70),
    (349, 299): (496, -897),
    (349, 326): (-624, -3010),
    (349, 327): (144, -165),
    (349, 338): (429, -460),
    (349, 339): (-91, 60),
    (350, 5): (-70, -24),
    (350, 38): (-490, 168),
    (350, 40): (-40, 96),
    (350, 46): (-3864, 598),
    (350, 79): (86, -1848),
    (350, 80): (65, -72),
    (350, 92): (35, 12),
    (350, 99): (140, 171),
    (350, 102): (70, -240),
    (350, 115): (42, 40),
    (350, 148): (-315, -80),
    (350, 149): (140, -51),
    (350, 177): (-70, 24),
    (350, 193): (-1330, -456),
    (350, 197): (20, 21),
    (350, 233): (-70, 168),
    (350, 234): (70, 24),
    (350, 235): (-420, -29),
    (350, 242): (630, -1144),
    (350, 247): (56, -33),
    (350, 260): (-25, 60),
    (350, 330): (-200, -150),
    (350, 349): (-10, 24),
}


BOX_THREE_SIXTY_RESIDUAL_CERTIFICATES: dict[Point, Point] = {}


BOX_FIVE_HUNDRED_RESIDUAL_CERTIFICATES: dict[Point, Point] = {}


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
BOX_TWO_HUNDRED_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_TWO_HUNDRED_RESIDUAL_CERTIFICATES
)
BOX_TWO_TEN_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_TWO_TEN_RESIDUAL_CERTIFICATES
)
BOX_TWO_TWENTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_TWO_TWENTY_RESIDUAL_CERTIFICATES
)
BOX_TWO_THIRTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_TWO_THIRTY_RESIDUAL_CERTIFICATES
)
BOX_TWO_FORTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_TWO_FORTY_RESIDUAL_CERTIFICATES
)
BOX_TWO_FIFTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_TWO_FIFTY_RESIDUAL_CERTIFICATES
)
BOX_TWO_SIXTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_TWO_SIXTY_RESIDUAL_CERTIFICATES
)
BOX_TWO_SEVENTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_TWO_SEVENTY_RESIDUAL_CERTIFICATES
)
BOX_TWO_EIGHTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_TWO_EIGHTY_RESIDUAL_CERTIFICATES
)
BOX_TWO_NINETY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_TWO_NINETY_RESIDUAL_CERTIFICATES
)
BOX_THREE_HUNDRED_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_THREE_HUNDRED_RESIDUAL_CERTIFICATES
)
BOX_THREE_TEN_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_THREE_TEN_RESIDUAL_CERTIFICATES
)
BOX_THREE_TWENTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_THREE_TWENTY_RESIDUAL_CERTIFICATES
)
BOX_THREE_THIRTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_THREE_THIRTY_RESIDUAL_CERTIFICATES
)
BOX_THREE_FORTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_THREE_FORTY_RESIDUAL_CERTIFICATES
)
BOX_THREE_FIFTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_THREE_FIFTY_RESIDUAL_CERTIFICATES
)
BOX_THREE_SIXTY_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_THREE_SIXTY_RESIDUAL_CERTIFICATES
)
BOX_FIVE_HUNDRED_RESIDUAL_LOOKUP = _residual_certificate_lookup(
    BOX_FIVE_HUNDRED_RESIDUAL_CERTIFICATES
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


def two_one_ray_three_mod_four_certificate(multiplier: int) -> Certificate | None:
    """Certificate for positive multipliers ``n = 3 mod 4`` on the ``(2, 1)`` ray."""

    if multiplier <= 0 or multiplier % 4 != 3:
        return None

    if multiplier == 3:
        return two_one_ray_explicit_base_certificate(multiplier)

    odd_leg = (multiplier - 1) // 2
    if odd_leg < 3 or odd_leg % 2 == 0:
        return None

    certificate = Certificate(
        target=(2 * multiplier, multiplier),
        midpoint=(2 * odd_leg, 1 - odd_leg * odd_leg),
    )
    if not certificate.valid():
        raise AssertionError("three-mod-four ray certificate formula is invalid")
    return certificate


def two_one_ray_three_mod_four_orbit_certificate(target: Point) -> Certificate | None:
    """Symmetric certificate for ``3 mod 4`` multiples of the ``(2, 1)`` ray."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        base = two_one_ray_three_mod_four_certificate(abs_h)
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
        base = two_one_ray_three_mod_four_certificate(abs_g)
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


def two_one_ray_five_or_seventeen_mod_twenty_certificate(
    multiplier: int,
) -> Certificate | None:
    """Certificate for multipliers ``5`` or ``17`` modulo ``20`` on the ray."""

    if multiplier <= 0:
        return None

    if multiplier % 20 == 5:
        parameter_t = (multiplier + 5) // 10
        coefficient = 2 * (parameter_t * parameter_t + parameter_t - 1)
        certificate = Certificate(
            target=(2 * multiplier, multiplier),
            midpoint=(3 * coefficient, 4 * coefficient),
        )
    elif multiplier % 20 == 17:
        parameter_t = (multiplier - 7) // 10
        coefficient = 2 * (parameter_t * parameter_t + parameter_t - 1)
        certificate = Certificate(
            target=(2 * multiplier, multiplier),
            midpoint=(-3 * coefficient, 4 * coefficient),
        )
    else:
        return None

    if not certificate.valid():
        raise AssertionError("mod-twenty ray certificate formula is invalid")
    return certificate


def two_one_ray_five_or_seventeen_mod_twenty_orbit_certificate(
    target: Point,
) -> Certificate | None:
    """Symmetric certificate for the mod-twenty ``(2, 1)`` ray family."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        base = two_one_ray_five_or_seventeen_mod_twenty_certificate(abs_h)
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
        base = two_one_ray_five_or_seventeen_mod_twenty_certificate(abs_g)
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


def two_one_ray_mod20_skeleton_certificate(multiplier: int) -> Certificate | None:
    """Certificate for the main modular skeleton on the ``(2, 1)`` ray.

    The covered positive multipliers are every class except ``1`` and ``9``
    modulo ``20``.  The constructor combines the even scaling family, the
    ``3 mod 4`` formula, the ``5``/``17 mod 20`` strip corollary, and one fixed
    parallel-direction factor family.
    """

    if multiplier <= 0:
        return None

    for constructor in (
        two_one_ray_even_certificate,
        two_one_ray_three_mod_four_certificate,
        two_one_ray_five_or_seventeen_mod_twenty_certificate,
    ):
        certificate = constructor(multiplier)
        if certificate is not None:
            return certificate

    target = (2 * multiplier, multiplier)
    certificate = ray_parallel_factor_certificate(
        target,
        (2, 1),
        (-4, -3),
        2,
    )
    if certificate is not None:
        return certificate

    return None


def two_one_ray_mod20_skeleton_residues() -> tuple[int, ...]:
    """Multiplier residues modulo 20 covered by the modular skeleton."""

    residues: list[int] = []
    for residue in range(20):
        multiplier = residue if residue != 0 else 20
        if two_one_ray_mod20_skeleton_certificate(multiplier) is not None:
            residues.append(residue)
    return tuple(residues)


def two_one_ray_mod20_skeleton_orbit_certificate(target: Point) -> Certificate | None:
    """Symmetric certificate for the modular skeleton on the ``(2, 1)`` ray."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        base = two_one_ray_mod20_skeleton_certificate(abs_h)
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
        base = two_one_ray_mod20_skeleton_certificate(abs_g)
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


def two_one_ray_mod_ten_divisor_certificate(multiplier: int) -> Certificate | None:
    """Certificate from a divisor ``3`` or ``7`` modulo ``10``.

    If ``multiplier = d*q`` and ``q = 3 mod 10``, direction ``(3, -4)`` with
    factor ``d`` gives a parallel-direction certificate.  If ``q = 7 mod 10``,
    use direction ``(-3, 4)`` with the same factor.
    """

    if multiplier <= 0:
        return None

    target = (2 * multiplier, multiplier)
    for quotient in positive_divisors(multiplier):
        factor = multiplier // quotient
        if quotient % 10 == 3:
            certificate = ray_parallel_factor_certificate(
                target,
                (2, 1),
                (3, -4),
                factor,
            )
        elif quotient % 10 == 7:
            certificate = ray_parallel_factor_certificate(
                target,
                (2, 1),
                (-3, 4),
                factor,
            )
        else:
            continue

        if certificate is None:
            raise AssertionError("mod-ten divisor criterion failed")
        return certificate

    return None


def two_one_ray_mod_ten_divisor_orbit_certificate(target: Point) -> Certificate | None:
    """Symmetric certificate from a ``3``/``7 mod 10`` divisor."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        base = two_one_ray_mod_ten_divisor_certificate(abs_h)
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
        base = two_one_ray_mod_ten_divisor_certificate(abs_g)
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


@cache
def two_one_ray_complement_divisor_root(direction: Point) -> int | None:
    """Minimal quotient class for the complement-divisor construction.

    For ``T=q(2,1)`` and ``U=(u,v)``, the factor-one integrality condition is
    equivalent to

        ``(u - 2v)^2*q^2 + 2*(2u + v)*q - 1 == 0 mod 2*c^2``.

    Primitive Pythagorean directions with odd ``u`` and
    ``gcd(u - 2v, c) = 1`` have a single odd class modulo ``2c``.
    """

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")

    u, v = direction
    norm_squared = u * u + v * v
    c = isqrt(norm_squared)
    if u % 2 == 0:
        return None

    linear = 2 * u + v
    determinant_factor = u - 2 * v
    if gcd(determinant_factor, c) != 1:
        return None

    root = (
        -linear
        * pow((determinant_factor * determinant_factor) % c, -1, c)
    ) % c
    root = root if root % 2 == 1 else root + c
    if (
        determinant_factor * determinant_factor * root * root
        + 2 * linear * root
        - 1
    ) % (2 * c * c) != 0:
        return None
    return root


@cache
def two_one_ray_complement_divisor_residues(direction: Point) -> tuple[int, ...]:
    """Quotient residues for the complement-factor parallel construction.

    For a multiplier ``n = d*q``, this construction uses the fixed
    ``direction`` and the parallel-direction factor ``d``.  The returned
    residues modulo ``2*|direction|^2`` are exactly the quotient classes ``q``
    for which the base multiplier ``q`` has a valid factor-one certificate.
    Scaling then covers every positive complement ``d``.
    """

    root = two_one_ray_complement_divisor_root(direction)
    if root is None:
        return ()

    norm_squared = direction[0] * direction[0] + direction[1] * direction[1]
    c = isqrt(norm_squared)
    return tuple(range(root, 2 * c * c, 2 * c))


@cache
def two_one_ray_complement_divisor_period(
    direction: Point,
) -> tuple[int, tuple[int, ...]]:
    """Minimal quotient period for one complement-divisor direction."""

    root = two_one_ray_complement_divisor_root(direction)
    if root is None:
        return (1, ())

    c = isqrt(direction[0] * direction[0] + direction[1] * direction[1])
    return (2 * c, (root,))


def two_one_ray_complement_divisor_certificate(
    multiplier: int,
    direction: Point,
) -> Certificate | None:
    """Certificate using a divisor as quotient and its complement as factor."""

    if multiplier <= 0:
        return None

    modulus, residues = two_one_ray_complement_divisor_period(direction)
    residues = set(residues)
    target = (2 * multiplier, multiplier)
    for quotient in positive_divisors(multiplier):
        if quotient % modulus not in residues:
            continue

        certificate = parallel_direction_factor_certificate(
            target,
            direction,
            multiplier // quotient,
        )
        if certificate is None:
            raise AssertionError("complement divisor residue failed")
        return certificate

    return None


def two_one_ray_square_determinant_factor_certificate(
    multiplier: int,
    direction: Point,
) -> Certificate | None:
    """Certificate using factor ``(u - 2v)^2`` for a fixed direction."""

    if multiplier <= 0:
        return None
    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")

    modulus, residues = two_one_ray_square_determinant_factor_period(direction)
    if multiplier % modulus not in residues:
        return None

    determinant_factor = direction[0] - 2 * direction[1]
    return parallel_direction_factor_certificate(
        (2 * multiplier, multiplier),
        direction,
        determinant_factor * determinant_factor,
    )


def two_one_ray_square_determinant_divisor_certificate(
    multiplier: int,
    direction: Point,
) -> Certificate | None:
    """Certificate from a divisor in a square-determinant factor class."""

    if multiplier <= 0:
        return None
    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")

    modulus, residues = two_one_ray_square_determinant_factor_period(direction)
    residue_set = set(residues)
    if not residue_set:
        return None

    determinant_factor = direction[0] - 2 * direction[1]
    target = (2 * multiplier, multiplier)
    for quotient in positive_divisors(multiplier):
        if quotient % modulus not in residue_set:
            continue

        certificate = parallel_direction_factor_certificate(
            target,
            direction,
            (multiplier // quotient) * determinant_factor * determinant_factor,
        )
        if certificate is not None:
            return certificate

    return None


def two_one_ray_scaled_factor_divisor_certificate(
    multiplier: int,
    direction: Point,
    base_factor: int,
) -> Certificate | None:
    """Scale a fixed direction/factor residue class through divisors."""

    if multiplier <= 0:
        return None
    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")
    if base_factor <= 0:
        raise ValueError("base_factor must be positive")

    modulus = parallel_direction_factor_modulus(direction, base_factor)
    residues = set(ray_parallel_factor_residues((2, 1), direction, base_factor))
    target = (2 * multiplier, multiplier)
    for quotient in positive_divisors(multiplier):
        if quotient % modulus not in residues:
            continue

        certificate = parallel_direction_factor_certificate(
            target,
            direction,
            (multiplier // quotient) * base_factor,
        )
        if certificate is not None:
            return certificate

    return None


@cache
def two_one_ray_determinant_split_factor_period(
    direction: Point,
    base_factor: int,
) -> tuple[int, tuple[int, ...]]:
    """Minimal quotient period for a split factor of ``(u - 2v)^2``.

    For ``T=q(2,1)`` and ``U=(u,v)``, put
    ``A=2u+v``, ``B=u-2v``, and ``c=|U|``.  If
    ``base_factor * paired_factor = B^2`` and ``paired_factor`` is invertible
    modulo ``c``, the fixed-factor coefficient condition collapses to the
    double root

        ``q * paired_factor + A == 0 mod c``.

    The two parity lifts modulo ``2c`` are then checked against the exact
    factor and coefficient congruences.
    """

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")
    if base_factor <= 0:
        raise ValueError("base_factor must be positive")

    u, v = direction
    c = isqrt(u * u + v * v)
    linear_factor = 2 * u + v
    determinant_factor = u - 2 * v
    determinant_square = determinant_factor * determinant_factor
    if determinant_square == 0 or determinant_square % base_factor != 0:
        return (1, ())

    paired_factor = determinant_square // base_factor
    if gcd(paired_factor, c) != 1:
        return (1, ())

    root_mod_hypotenuse = (
        -linear_factor
        * pow(paired_factor % c, -1, c)
    ) % c
    roots: list[int] = []
    for root in (root_mod_hypotenuse, root_mod_hypotenuse + c):
        if (paired_factor * root * root - base_factor) % 2 != 0:
            continue
        if (
            paired_factor * root * root
            + 2 * linear_factor * root
            - base_factor
        ) % (2 * c * c) != 0:
            continue
        roots.append(root % (2 * c))

    return minimal_periodic_residue_classes(2 * c, roots)


def two_one_ray_determinant_split_factor_certificate(
    multiplier: int,
    direction: Point,
    base_factor: int,
) -> Certificate | None:
    """Certificate from a quotient in a split determinant-factor class."""

    if multiplier <= 0:
        return None

    modulus, residues = two_one_ray_determinant_split_factor_period(
        direction,
        base_factor,
    )
    residue_set = set(residues)
    if not residue_set:
        return None

    target = (2 * multiplier, multiplier)
    for quotient in positive_divisors(multiplier):
        if quotient % modulus not in residue_set:
            continue

        certificate = parallel_direction_factor_certificate(
            target,
            direction,
            (multiplier // quotient) * base_factor,
        )
        if certificate is not None:
            return certificate

    return None


@cache
def two_one_ray_hypotenuse_determinant_split_factor_layers(
    hypotenuse: int,
) -> tuple[tuple[Point, int], ...]:
    """All nonempty determinant split-factor layers for one hypotenuse."""

    layers: list[tuple[Point, int]] = []
    for direction in pythagorean_directions_for_hypotenuse(hypotenuse):
        determinant_factor = direction[0] - 2 * direction[1]
        determinant_square = determinant_factor * determinant_factor
        if determinant_square == 0:
            continue

        for base_factor in positive_divisors(determinant_square):
            if two_one_ray_determinant_split_factor_period(
                direction,
                base_factor,
            )[1]:
                layers.append((direction, base_factor))

    return tuple(layers)


def two_one_ray_hypotenuse_determinant_split_factor_certificate(
    multiplier: int,
    hypotenuse: int,
) -> Certificate | None:
    """Certificate from all determinant split factors with one hypotenuse."""

    if multiplier <= 0:
        return None

    for direction, base_factor in two_one_ray_hypotenuse_determinant_split_factor_layers(
        hypotenuse
    ):
        certificate = two_one_ray_determinant_split_factor_certificate(
            multiplier,
            direction,
            base_factor,
        )
        if certificate is not None:
            return certificate

    return None


@dataclass(frozen=True)
class TwoOneRayDeterminantSplitFactorWitness:
    """Witness data for a determinant split-factor certificate."""

    multiplier: int
    quotient: int
    direction: Point
    hypotenuse: int
    base_factor: int
    paired_factor: int
    period: int
    residue: int

    @property
    def linear_factor(self) -> int:
        return two_one_ray_determinant_coordinates(self.direction)[0]

    @property
    def determinant_factor(self) -> int:
        return two_one_ray_determinant_coordinates(self.direction)[1]

    @property
    def scaled_factor(self) -> int:
        return (self.multiplier // self.quotient) * self.base_factor

    @property
    def lift_parameter(self) -> int:
        numerator = self.linear_factor + self.quotient * self.paired_factor
        if numerator % self.hypotenuse != 0:
            raise AssertionError("determinant split witness has nonintegral lift")
        return numerator // self.hypotenuse

    @property
    def target(self) -> Point:
        return (2 * self.multiplier, self.multiplier)

    @property
    def certificate(self) -> Certificate:
        certificate = parallel_direction_factor_certificate(
            self.target,
            self.direction,
            self.scaled_factor,
        )
        if certificate is None:
            raise AssertionError("determinant split witness did not certify")
        return certificate

    def valid(self) -> bool:
        return self.certificate.valid()


def two_one_ray_determinant_paired_factor_root(
    quotient: int,
    paired_factor: int,
    hypotenuse: int,
) -> tuple[Point, int] | None:
    """Recover a split direction from a fixed quotient, paired factor, and hypotenuse.

    With ``F_0 H = B^2`` and ``H = paired_factor``, the split root condition is
    ``A == -quotient*H mod c``.  The determinant coordinates must also satisfy
    ``A^2 + B^2 = 5c^2``.  The finitely many lifts of ``A`` therefore recover
    possible determinant factors ``B`` directly.
    """

    if quotient <= 0:
        return None
    if paired_factor <= 0:
        raise ValueError("paired_factor must be positive")
    if hypotenuse <= 0:
        raise ValueError("hypotenuse must be positive")
    if gcd(paired_factor, hypotenuse) != 1:
        return None

    residue = (-quotient * paired_factor) % hypotenuse
    for lift in range(-3, 4):
        linear_factor = residue + lift * hypotenuse
        determinant_square = 5 * hypotenuse * hypotenuse - linear_factor * linear_factor
        if determinant_square <= 0 or determinant_square % paired_factor != 0:
            continue

        determinant_factor_abs = isqrt(determinant_square)
        if determinant_factor_abs * determinant_factor_abs != determinant_square:
            continue

        base_factor = determinant_square // paired_factor
        for determinant_factor in sorted(
            {-determinant_factor_abs, determinant_factor_abs}
        ):
            if (2 * linear_factor + determinant_factor) % 5 != 0:
                continue
            if (linear_factor - 2 * determinant_factor) % 5 != 0:
                continue

            direction = (
                (2 * linear_factor + determinant_factor) // 5,
                (linear_factor - 2 * determinant_factor) // 5,
            )
            if not edge_delta(*direction):
                continue

            period, residues = two_one_ray_determinant_split_factor_period(
                direction,
                base_factor,
            )
            if quotient % period in residues:
                return (direction, base_factor)

    return None


def two_one_ray_determinant_paired_factor_lift_root(
    quotient: int,
    paired_factor: int,
    lift_parameter: int,
) -> tuple[Point, int, int] | None:
    """Recover a split root from quotient, paired factor, and lift.

    If ``A + quotient*paired_factor = lift*c``, then with
    ``D = lift^2 - 5`` the determinant norm is equivalent to

        ``X^2 + D*B^2 = 5*quotient^2*paired_factor^2``,

    where ``X = D*c - lift*quotient*paired_factor``.  For ``D > 0`` this is a
    finite exact search in the determinant factor ``B``.
    """

    if quotient <= 0:
        return None
    if paired_factor <= 0:
        raise ValueError("paired_factor must be positive")

    discriminant_factor = lift_parameter * lift_parameter - 5
    if discriminant_factor <= 0:
        return None

    target_norm = 5 * quotient * quotient * paired_factor * paired_factor
    max_determinant_factor = isqrt(target_norm // discriminant_factor)
    for determinant_factor_abs in range(1, max_determinant_factor + 1):
        determinant_square = determinant_factor_abs * determinant_factor_abs
        if determinant_square % paired_factor != 0:
            continue

        x_square = target_norm - discriminant_factor * determinant_square
        if x_square < 0:
            continue

        x_abs = isqrt(x_square)
        if x_abs * x_abs != x_square:
            continue

        base_factor = determinant_square // paired_factor
        for x_value in sorted({-x_abs, x_abs}):
            numerator = x_value + lift_parameter * quotient * paired_factor
            if numerator % discriminant_factor != 0:
                continue

            hypotenuse = numerator // discriminant_factor
            if hypotenuse <= 0:
                continue

            linear_factor = (
                lift_parameter * hypotenuse
                - quotient * paired_factor
            )
            for determinant_factor in sorted(
                {-determinant_factor_abs, determinant_factor_abs}
            ):
                if (2 * linear_factor + determinant_factor) % 5 != 0:
                    continue
                if (linear_factor - 2 * determinant_factor) % 5 != 0:
                    continue

                direction = (
                    (2 * linear_factor + determinant_factor) // 5,
                    (linear_factor - 2 * determinant_factor) // 5,
                )
                if not edge_delta(*direction):
                    continue

                period, residues = two_one_ray_determinant_split_factor_period(
                    direction,
                    base_factor,
                )
                if quotient % period in residues:
                    return (direction, base_factor, hypotenuse)

    return None


def two_one_ray_determinant_split_factor_witness(
    multiplier: int,
    max_hypotenuse: int,
) -> TwoOneRayDeterminantSplitFactorWitness | None:
    """Find a determinant split-factor witness up to a hypotenuse bound.

    This is a target-facing diagnostic for the exact split-factor families: it
    searches quotient divisors and determinant split layers, not midpoint boxes.
    A returned row is already a directly valid two-step certificate.
    """

    if multiplier <= 0:
        return None
    if max_hypotenuse <= 0:
        raise ValueError("max_hypotenuse must be positive")

    target = (2 * multiplier, multiplier)
    for quotient in positive_divisors(multiplier):
        complement = multiplier // quotient
        for hypotenuse in range(1, max_hypotenuse + 1):
            for direction, base_factor in (
                two_one_ray_hypotenuse_determinant_split_factor_layers(
                    hypotenuse
                )
            ):
                period, residues = two_one_ray_determinant_split_factor_period(
                    direction,
                    base_factor,
                )
                residue = quotient % period
                if residue not in residues:
                    continue

                certificate = parallel_direction_factor_certificate(
                    target,
                    direction,
                    complement * base_factor,
                )
                if certificate is None:
                    continue

                determinant_factor = direction[0] - 2 * direction[1]
                return TwoOneRayDeterminantSplitFactorWitness(
                    multiplier=multiplier,
                    quotient=quotient,
                    direction=direction,
                    hypotenuse=hypotenuse,
                    base_factor=base_factor,
                    paired_factor=(
                        determinant_factor
                        * determinant_factor
                        // base_factor
                    ),
                    period=period,
                    residue=residue,
                )

    return None


def two_one_ray_paired_factor_split_factor_witness(
    multiplier: int,
    paired_factor: int,
    max_hypotenuse: int,
) -> TwoOneRayDeterminantSplitFactorWitness | None:
    """Find a determinant split witness by fixing the paired factor ``H``."""

    if multiplier <= 0:
        return None
    if paired_factor <= 0:
        raise ValueError("paired_factor must be positive")
    if max_hypotenuse <= 0:
        raise ValueError("max_hypotenuse must be positive")

    target = (2 * multiplier, multiplier)
    for quotient in positive_divisors(multiplier):
        complement = multiplier // quotient
        for hypotenuse in range(1, max_hypotenuse + 1):
            root = two_one_ray_determinant_paired_factor_root(
                quotient,
                paired_factor,
                hypotenuse,
            )
            if root is None:
                continue

            direction, base_factor = root
            certificate = parallel_direction_factor_certificate(
                target,
                direction,
                complement * base_factor,
            )
            if certificate is None:
                continue

            period, residues = two_one_ray_determinant_split_factor_period(
                direction,
                base_factor,
            )
            residue = quotient % period
            if residue not in residues:
                continue

            return TwoOneRayDeterminantSplitFactorWitness(
                multiplier=multiplier,
                quotient=quotient,
                direction=direction,
                hypotenuse=hypotenuse,
                base_factor=base_factor,
                paired_factor=paired_factor,
                period=period,
                residue=residue,
            )

    return None


def two_one_ray_paired_factor_lift_witness(
    multiplier: int,
    paired_factor: int,
    max_lift: int,
) -> TwoOneRayDeterminantSplitFactorWitness | None:
    """Find a determinant split witness by bounding the lift ``k``."""

    if multiplier <= 0:
        return None
    if paired_factor <= 0:
        raise ValueError("paired_factor must be positive")
    if max_lift < 3:
        raise ValueError("max_lift must be at least 3")

    target = (2 * multiplier, multiplier)
    for quotient in positive_divisors(multiplier):
        complement = multiplier // quotient
        for lift_parameter in range(3, max_lift + 1):
            root = two_one_ray_determinant_paired_factor_lift_root(
                quotient,
                paired_factor,
                lift_parameter,
            )
            if root is None:
                continue

            direction, base_factor, hypotenuse = root
            certificate = parallel_direction_factor_certificate(
                target,
                direction,
                complement * base_factor,
            )
            if certificate is None:
                continue

            period, residues = two_one_ray_determinant_split_factor_period(
                direction,
                base_factor,
            )
            residue = quotient % period
            if residue not in residues:
                continue

            return TwoOneRayDeterminantSplitFactorWitness(
                multiplier=multiplier,
                quotient=quotient,
                direction=direction,
                hypotenuse=hypotenuse,
                base_factor=base_factor,
                paired_factor=paired_factor,
                period=period,
                residue=residue,
            )

    return None


def two_one_ray_double_direction_certificate(direction: Point) -> Certificate | None:
    """Certificate with midpoint twice a Pythagorean direction.

    For ``U=(u,v)`` with hypotenuse ``c`` and ``A=2u+v``, the multiplier
    ``q=3c-A`` satisfies

        ``|q(2,1)-2U| = |3q-2c|``.

    Thus every nondegenerate positive row gives a two-step certificate.
    """

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")

    u, v = direction
    hypotenuse = isqrt(u * u + v * v)
    multiplier = 3 * hypotenuse - (2 * u + v)
    if multiplier <= 0:
        return None

    certificate = Certificate(
        target=(2 * multiplier, multiplier),
        midpoint=(2 * u, 2 * v),
    )
    if not certificate.valid():
        return None
    return certificate


def two_one_ray_lift_three_square_endpoint_certificate(
    multiplier: int,
) -> Certificate | None:
    """Prime-seed certificate from the ``k=3``, ``H=1`` split endpoint."""

    if multiplier <= 0:
        return None
    if not is_prime(multiplier):
        return None

    witness = two_one_ray_paired_factor_lift_witness(
        multiplier,
        paired_factor=1,
        max_lift=3,
    )
    if witness is None:
        return None

    certificate = two_one_ray_double_direction_certificate(witness.direction)
    if certificate is None:
        raise AssertionError("lift-three witness did not give double direction row")
    if certificate.target != witness.target:
        raise AssertionError("lift-three double direction target mismatch")
    return certificate


def two_one_ray_prime_one_mod_four_double_direction_certificate(
    multiplier: int,
) -> Certificate | None:
    """Certificate for primes ``1 mod 4`` via Fermat's two-square form.

    For an odd prime ``p = 1 mod 4``, write ``p = x^2 + 4y^2``.  Setting
    ``m=x+y`` and ``n=y`` gives the Pythagorean direction
    ``U=(m^2-n^2, 2mn)`` and

        ``p = 3|U| - (2u+v)``.

    Hence the double-direction midpoint ``2U`` certifies ``(2p,p)``.
    """

    if multiplier <= 0 or multiplier % 4 != 1 or not is_prime(multiplier):
        return None

    for y in range(1, isqrt(multiplier // 4) + 1):
        x_squared = multiplier - 4 * y * y
        x = isqrt(x_squared)
        if x <= 0 or x * x != x_squared:
            continue

        parameter_m = x + y
        parameter_n = y
        direction = (
            parameter_m * parameter_m - parameter_n * parameter_n,
            2 * parameter_m * parameter_n,
        )
        certificate = two_one_ray_double_direction_certificate(direction)
        if certificate is None:
            continue
        if certificate.target != (2 * multiplier, multiplier):
            raise AssertionError("one-mod-four double direction target mismatch")
        return certificate

    return None


def two_one_ray_square_determinant_factor_sieve_certificate(
    multiplier: int,
    directions: Iterable[Point],
) -> Certificate | None:
    """Certificate from the first applicable square-determinant factor direction."""

    if multiplier <= 0:
        return None

    for direction in directions:
        certificate = two_one_ray_square_determinant_divisor_certificate(
            multiplier,
            direction,
        )
        if certificate is not None:
            return certificate

    return None


@cache
def two_one_ray_square_determinant_factor_residues(
    direction: Point,
) -> tuple[int, ...]:
    """Natural-modulus residues for the factor ``(u - 2v)^2`` construction."""

    modulus, residues = two_one_ray_square_determinant_factor_period(direction)
    if not residues:
        return ()

    c = isqrt(direction[0] * direction[0] + direction[1] * direction[1])
    root = residues[0]
    return tuple(range(root, 2 * c * c, modulus))


@cache
def two_one_ray_square_determinant_factor_period(
    direction: Point,
) -> tuple[int, tuple[int, ...]]:
    """Minimal multiplier period for factor ``(u - 2v)^2`` on the ``(2,1)`` ray."""

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")

    u, v = direction
    c = isqrt(u * u + v * v)
    linear_factor = 2 * u + v
    determinant_factor = u - 2 * v
    if determinant_factor == 0:
        return (1, ())

    root = (-linear_factor) % c
    if root % 2 != determinant_factor % 2:
        root += c
    return (2 * c, (root,))


@cache
def two_one_ray_complement_divisor_sieve_residue_classes(
    directions: tuple[Point, ...],
) -> tuple[int, tuple[int, ...]]:
    """Combined quotient divisor classes proved by several directions."""

    return periodic_residue_union(
        two_one_ray_complement_divisor_period(direction)
        for direction in directions
    )


def two_one_ray_complement_divisor_sieve_certificate(
    multiplier: int,
    directions: Iterable[Point],
) -> Certificate | None:
    """Certificate from the first applicable complement-divisor direction."""

    if multiplier <= 0:
        return None

    direction_data: list[tuple[Point, int, frozenset[int]]] = []
    for direction in directions:
        modulus, residues = two_one_ray_complement_divisor_period(direction)
        residues = frozenset(residues)
        if residues:
            direction_data.append((direction, modulus, residues))

    target = (2 * multiplier, multiplier)
    for quotient in positive_divisors(multiplier):
        factor = multiplier // quotient
        for direction, modulus, residues in direction_data:
            if quotient % modulus not in residues:
                continue

            certificate = parallel_direction_factor_certificate(
                target,
                direction,
                factor,
            )
            if certificate is None:
                raise AssertionError("complement divisor sieve residue failed")
            return certificate

    return None


@cache
def pythagorean_directions_for_hypotenuse(hypotenuse: int) -> tuple[Point, ...]:
    """Primitive signed Pythagorean directions with a fixed hypotenuse."""

    if hypotenuse <= 0:
        raise ValueError("hypotenuse must be positive")

    directions: list[Point] = []
    for u in range(-hypotenuse + 1, hypotenuse):
        if u == 0:
            continue

        v_squared = hypotenuse * hypotenuse - u * u
        v_abs = isqrt(v_squared)
        if v_abs == 0 or v_abs * v_abs != v_squared:
            continue

        for v in (-v_abs, v_abs):
            if gcd(abs(u), abs(v)) == 1:
                directions.append((u, v))

    return tuple(sorted(set(directions)))


@cache
def two_one_ray_hypotenuse_divisor_directions(
    hypotenuse: int,
) -> tuple[Point, ...]:
    """Directions with this hypotenuse that produce complement-divisor roots."""

    return tuple(
        direction
        for direction in pythagorean_directions_for_hypotenuse(hypotenuse)
        if two_one_ray_complement_divisor_root(direction) is not None
    )


@cache
def two_one_ray_hypotenuse_divisor_residue_classes(
    hypotenuse: int,
) -> tuple[int, tuple[int, ...]]:
    """Combined quotient classes from all root directions with one hypotenuse."""

    return two_one_ray_complement_divisor_sieve_residue_classes(
        two_one_ray_hypotenuse_divisor_directions(hypotenuse)
    )


def two_one_ray_hypotenuse_divisor_certificate(
    multiplier: int,
    hypotenuse: int,
) -> Certificate | None:
    """Certificate from all complement-divisor directions with one hypotenuse."""

    return two_one_ray_complement_divisor_sieve_certificate(
        multiplier,
        two_one_ray_hypotenuse_divisor_directions(hypotenuse),
    )


@cache
def two_one_ray_hypotenuse_square_factor_directions(
    hypotenuse: int,
) -> tuple[Point, ...]:
    """Directions with this hypotenuse that produce square-factor classes."""

    return tuple(
        direction
        for direction in pythagorean_directions_for_hypotenuse(hypotenuse)
        if two_one_ray_square_determinant_factor_period(direction)[1]
    )


@cache
def two_one_ray_hypotenuse_square_factor_residue_classes(
    hypotenuse: int,
) -> tuple[int, tuple[int, ...]]:
    """Combined square-factor classes from all directions with one hypotenuse."""

    return periodic_residue_union(
        two_one_ray_square_determinant_factor_period(direction)
        for direction in two_one_ray_hypotenuse_square_factor_directions(hypotenuse)
    )


def two_one_ray_hypotenuse_square_factor_certificate(
    multiplier: int,
    hypotenuse: int,
) -> Certificate | None:
    """Certificate from square-factor directions with one hypotenuse."""

    return two_one_ray_square_determinant_factor_sieve_certificate(
        multiplier,
        two_one_ray_hypotenuse_square_factor_directions(hypotenuse),
    )


def two_one_ray_determinant_coordinates(direction: Point) -> tuple[int, int, int]:
    """Return ``(A, B, c)`` with ``A+iB = (2+i)(u-iv)`` for a direction."""

    if not edge_delta(*direction):
        raise ValueError("direction must be a legal Pythagorean edge vector")

    u, v = direction
    linear_factor, determinant_factor = gaussian_multiply((2, 1), (u, -v))
    hypotenuse = isqrt(u * u + v * v)
    return (linear_factor, determinant_factor, hypotenuse)


def euclid_sqrt_minus_one_residues(parameter_m: int, parameter_k: int) -> tuple[int, int]:
    """The two square roots of ``-1`` from Euclid parameters modulo ``m^2+k^2``."""

    if parameter_m <= parameter_k or parameter_k <= 0:
        raise ValueError("Euclid parameters must satisfy m > k > 0")
    if gcd(parameter_m, parameter_k) != 1:
        raise ValueError("Euclid parameters must be coprime")

    hypotenuse = parameter_m * parameter_m + parameter_k * parameter_k
    residue = (parameter_m * pow(parameter_k, -1, hypotenuse)) % hypotenuse
    return tuple(sorted({residue, (-residue) % hypotenuse}))


def two_one_ray_signed_euclid_root(
    parameter_m: int,
    parameter_k: int,
    odd_leg_sign: int,
    even_leg_sign: int,
) -> "TwoOneRayDeterminantSliceRoot | None":
    """Root for a signed odd-leg-first Euclid direction.

    For ``u = s_o*(m^2-k^2)`` and ``v = s_e*2mk``, the inverse-root condition
    is ``q*(u-2v) == +/- m/k mod c``.  The sign is positive exactly when
    ``s_o`` and ``s_e`` agree.
    """

    if odd_leg_sign not in (-1, 1) or even_leg_sign not in (-1, 1):
        raise ValueError("leg signs must be -1 or 1")
    if parameter_m <= parameter_k or parameter_k <= 0:
        raise ValueError("Euclid parameters must satisfy m > k > 0")
    if gcd(parameter_m, parameter_k) != 1:
        raise ValueError("Euclid parameters must be coprime")
    if (parameter_m - parameter_k) % 2 == 0:
        raise ValueError("Euclid parameters must have opposite parity")

    odd_leg = parameter_m * parameter_m - parameter_k * parameter_k
    even_leg = 2 * parameter_m * parameter_k
    hypotenuse = parameter_m * parameter_m + parameter_k * parameter_k
    direction = (odd_leg_sign * odd_leg, even_leg_sign * even_leg)
    linear_factor, determinant_factor, _ = two_one_ray_determinant_coordinates(
        direction
    )
    if gcd(determinant_factor, hypotenuse) != 1:
        return None

    sqrt_residue = (
        parameter_m
        * pow(parameter_k, -1, hypotenuse)
    ) % hypotenuse
    if odd_leg_sign != even_leg_sign:
        sqrt_residue = (-sqrt_residue) % hypotenuse

    root_mod_hypotenuse = (
        sqrt_residue
        * pow(determinant_factor % hypotenuse, -1, hypotenuse)
    ) % hypotenuse
    root = (
        root_mod_hypotenuse
        if root_mod_hypotenuse % 2 == 1
        else root_mod_hypotenuse + hypotenuse
    )

    determinant_root = two_one_ray_determinant_slice_root(
        linear_factor,
        determinant_factor,
        hypotenuse,
    )
    if determinant_root is None:
        return None
    if determinant_root.root != root:
        raise AssertionError("signed Euclid root disagrees with determinant root")
    return determinant_root


@cache
def two_one_ray_euclid_parameter_roots(
    parameter_m: int,
    parameter_k: int,
) -> tuple["TwoOneRayDeterminantSliceRoot", ...]:
    """All complement-divisor roots from one primitive Euclid parameter pair."""

    roots: list[TwoOneRayDeterminantSliceRoot] = []
    for odd_leg_sign in (-1, 1):
        for even_leg_sign in (-1, 1):
            root = two_one_ray_signed_euclid_root(
                parameter_m,
                parameter_k,
                odd_leg_sign,
                even_leg_sign,
            )
            if root is not None:
                roots.append(root)
    return tuple(sorted(roots, key=lambda root: (root.root, root.direction)))


@cache
def two_one_ray_euclid_parameter_residue_classes(
    parameter_m: int,
    parameter_k: int,
) -> tuple[int, tuple[int, ...]]:
    """Quotient classes modulo ``2*(m^2+k^2)`` from one Euclid pair."""

    roots = two_one_ray_euclid_parameter_roots(parameter_m, parameter_k)
    if not roots:
        return (1, ())

    modulus = roots[0].modulus
    return (modulus, tuple(root.root for root in roots))


def two_one_ray_euclid_parameter_certificate(
    multiplier: int,
    parameter_m: int,
    parameter_k: int,
) -> Certificate | None:
    """Complement-divisor certificate from one Euclid parameter pair."""

    if multiplier <= 0:
        return None

    roots = two_one_ray_euclid_parameter_roots(parameter_m, parameter_k)
    target = (2 * multiplier, multiplier)
    for quotient in positive_divisors(multiplier):
        for root in roots:
            if quotient % root.modulus != root.root:
                continue

            certificate = parallel_direction_factor_certificate(
                target,
                root.direction,
                multiplier // quotient,
            )
            if certificate is None:
                raise AssertionError("signed Euclid residue failed to certify")
            return certificate

    return None


TWO_ONE_RAY_PROMOTED_INVERSE_ROOT_PARAMETERS: tuple[tuple[int, int], ...] = (
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
)


@cache
def two_one_ray_promoted_inverse_root_certificate(
    multiplier: int,
) -> Certificate | None:
    """Certificate from inverse-root Euclid layers promoted to exact seeds."""

    if multiplier <= 0:
        return None

    for parameters in TWO_ONE_RAY_PROMOTED_INVERSE_ROOT_PARAMETERS:
        certificate = two_one_ray_euclid_parameter_certificate(
            multiplier,
            *parameters,
        )
        if certificate is not None:
            return certificate

    return None


@dataclass(frozen=True)
class TwoOneRayDeterminantSliceRoot:
    """Root data in coordinates adapted to the exceptional ray ``(2, 1)``."""

    linear_factor: int
    determinant_factor: int
    hypotenuse: int
    direction: Point
    root: int

    @property
    def modulus(self) -> int:
        return 2 * self.hypotenuse

    @property
    def sqrt_minus_one_residue(self) -> int:
        return (self.root * self.determinant_factor) % self.hypotenuse

    def certificate(self, multiplier: int) -> Certificate | None:
        if multiplier <= 0 or multiplier % self.modulus != self.root:
            return None
        certificate = parallel_direction_factor_certificate(
            (2 * multiplier, multiplier),
            self.direction,
            1,
        )
        if certificate is None:
            raise AssertionError("determinant-slice root did not certify its target")
        return certificate

    @property
    def square_endpoint_base_factor(self) -> int:
        return self.determinant_factor * self.determinant_factor

    @property
    def square_endpoint_period(self) -> tuple[int, tuple[int, ...]]:
        return two_one_ray_determinant_split_factor_period(
            self.direction,
            self.square_endpoint_base_factor,
        )

    def square_endpoint_certificate(self, multiplier: int) -> Certificate | None:
        """Certificate from the square-factor endpoint of this determinant slice."""

        if multiplier <= 0:
            return None

        period, residues = self.square_endpoint_period
        if multiplier % period not in residues:
            return None

        certificate = parallel_direction_factor_certificate(
            (2 * multiplier, multiplier),
            self.direction,
            self.square_endpoint_base_factor,
        )
        if certificate is None:
            raise AssertionError("determinant-slice square endpoint did not certify")
        return certificate


def two_one_ray_determinant_slice_root(
    linear_factor: int,
    determinant_factor: int,
    hypotenuse: int,
) -> TwoOneRayDeterminantSliceRoot | None:
    """Return a root from the ray-adapted determinant slice.

    With ``A = 2u + v`` and ``B = u - 2v``, every direction satisfies
    ``A^2 + B^2 = 5c^2``.  Conversely, such a triple reconstructs the
    direction by ``u=(2A+B)/5`` and ``v=(A-2B)/5`` when those are integral.
    The complement-divisor root condition is ``n*B^2 + A == 0 mod c``.
    """

    if hypotenuse <= 0:
        raise ValueError("hypotenuse must be positive")

    if (
        linear_factor * linear_factor
        + determinant_factor * determinant_factor
        != 5 * hypotenuse * hypotenuse
    ):
        return None
    if (2 * linear_factor + determinant_factor) % 5 != 0:
        return None
    if (linear_factor - 2 * determinant_factor) % 5 != 0:
        return None

    direction = (
        (2 * linear_factor + determinant_factor) // 5,
        (linear_factor - 2 * determinant_factor) // 5,
    )
    if not edge_delta(*direction):
        return None
    if direction[0] % 2 == 0 or gcd(determinant_factor, hypotenuse) != 1:
        return None

    root = (
        -linear_factor
        * pow((determinant_factor * determinant_factor) % hypotenuse, -1, hypotenuse)
    ) % hypotenuse
    root = root if root % 2 == 1 else root + hypotenuse

    if root != two_one_ray_complement_divisor_root(direction):
        raise AssertionError("determinant-slice root disagrees with direction root")

    return TwoOneRayDeterminantSliceRoot(
        linear_factor=linear_factor,
        determinant_factor=determinant_factor,
        hypotenuse=hypotenuse,
        direction=direction,
        root=root,
    )


@cache
def two_one_ray_determinant_factor_roots(
    determinant_factor: int,
    max_hypotenuse: int,
) -> tuple[TwoOneRayDeterminantSliceRoot, ...]:
    """One-dimensional negative-Pell slice for a fixed determinant factor."""

    if max_hypotenuse <= 0:
        raise ValueError("max_hypotenuse must be positive")
    if determinant_factor == 0:
        return ()

    roots: list[TwoOneRayDeterminantSliceRoot] = []
    for hypotenuse in range(1, max_hypotenuse + 1):
        linear_square = 5 * hypotenuse * hypotenuse - determinant_factor * determinant_factor
        if linear_square < 0:
            continue

        linear_abs = isqrt(linear_square)
        if linear_abs * linear_abs != linear_square:
            continue

        for linear_factor in sorted({-linear_abs, linear_abs}):
            root = two_one_ray_determinant_slice_root(
                linear_factor,
                determinant_factor,
                hypotenuse,
            )
            if root is not None:
                roots.append(root)

    return tuple(roots)


def two_one_ray_determinant_slice_successor(
    root: TwoOneRayDeterminantSliceRoot,
) -> TwoOneRayDeterminantSliceRoot:
    """Next valid root in the same determinant slice.

    Multiplication by ``161 + 72*sqrt(5)`` preserves
    ``A^2 - 5c^2 = -B^2`` and the congruence conditions that reconstruct
    ``(u, v)`` from ``A=2u+v`` and ``B=u-2v``.  A unit step can still produce
    a degenerate or non-coprime row, so this returns the next valid root after
    one or more unit steps.
    """

    linear_factor = root.linear_factor
    hypotenuse = root.hypotenuse
    for _ in range(16):
        linear_factor, hypotenuse = (
            161 * linear_factor + 360 * hypotenuse,
            72 * linear_factor + 161 * hypotenuse,
        )
        successor = two_one_ray_determinant_slice_root(
            linear_factor,
            root.determinant_factor,
            hypotenuse,
        )
        if successor is not None:
            return successor

    raise AssertionError("determinant-slice successor found no valid root")


def two_one_ray_determinant_slice_predecessor(
    root: TwoOneRayDeterminantSliceRoot,
) -> TwoOneRayDeterminantSliceRoot | None:
    """Previous valid root in the same square-unit Pell orbit, if smaller."""

    starting_hypotenuse = root.hypotenuse
    linear_factor = root.linear_factor
    hypotenuse = root.hypotenuse
    for _ in range(16):
        linear_factor, hypotenuse = (
            161 * linear_factor - 360 * hypotenuse,
            -72 * linear_factor + 161 * hypotenuse,
        )
        if hypotenuse <= 0 or hypotenuse >= starting_hypotenuse:
            return None

        predecessor = two_one_ray_determinant_slice_root(
            linear_factor,
            root.determinant_factor,
            hypotenuse,
        )
        if predecessor is not None:
            return predecessor

    return None


def two_one_ray_determinant_slice_reduced_root(
    root: TwoOneRayDeterminantSliceRoot,
) -> TwoOneRayDeterminantSliceRoot:
    """Lowest root reached by repeatedly taking valid square-unit predecessors."""

    current = root
    while True:
        predecessor = two_one_ray_determinant_slice_predecessor(current)
        if predecessor is None:
            return current
        current = predecessor


def two_one_ray_determinant_slice_orbit(
    seed: TwoOneRayDeterminantSliceRoot,
    count: int,
) -> tuple[TwoOneRayDeterminantSliceRoot, ...]:
    """First ``count`` roots in the Pell orbit generated by ``seed``."""

    if count < 0:
        raise ValueError("count must be nonnegative")

    roots: list[TwoOneRayDeterminantSliceRoot] = []
    current = seed
    for _ in range(count):
        roots.append(current)
        current = two_one_ray_determinant_slice_successor(current)
    return tuple(roots)


def two_one_ray_determinant_slice_orbit_certificate(
    multiplier: int,
    seed: TwoOneRayDeterminantSliceRoot,
    max_steps: int,
) -> Certificate | None:
    """Certificate from the first ``max_steps`` roots in one Pell orbit."""

    if multiplier <= 0:
        return None
    if max_steps < 0:
        raise ValueError("max_steps must be nonnegative")

    for root in two_one_ray_determinant_slice_orbit(seed, max_steps):
        certificate = root.certificate(multiplier)
        if certificate is not None:
            return certificate
    return None


def two_one_ray_determinant_square_endpoint_orbit_certificate(
    multiplier: int,
    seed: TwoOneRayDeterminantSliceRoot,
    max_steps: int,
) -> Certificate | None:
    """Certificate from square-factor endpoints along one determinant-slice orbit."""

    if multiplier <= 0:
        return None
    if max_steps < 0:
        raise ValueError("max_steps must be nonnegative")

    for root in two_one_ray_determinant_slice_orbit(seed, max_steps):
        certificate = root.square_endpoint_certificate(multiplier)
        if certificate is not None:
            return certificate
    return None


def two_one_ray_determinant_divisor_root(
    multiplier: int,
    determinant_factor: int,
    hypotenuse: int,
) -> TwoOneRayDeterminantSliceRoot | None:
    """Recover a determinant-slice root from the divisor condition.

    A valid inverse-root certificate for multiplier ``n`` and determinant
    factor ``B`` has ``c | n^2*B^2 + 1`` and
    ``A == -n*B^2 mod c``.  The possible integer values of ``A`` lie within a
    bounded set of lifts of that residue because ``A^2 + B^2 = 5c^2``.
    """

    if multiplier <= 0 or hypotenuse <= 0 or determinant_factor == 0:
        return None

    determinant_square = determinant_factor * determinant_factor
    if (multiplier * multiplier * determinant_square + 1) % hypotenuse != 0:
        return None

    residue = (-multiplier * determinant_square) % hypotenuse
    for lift in range(-3, 4):
        root = two_one_ray_determinant_slice_root(
            residue + lift * hypotenuse,
            determinant_factor,
            hypotenuse,
        )
        if root is not None and multiplier % root.modulus == root.root:
            return root

    return None


def two_one_ray_determinant_divisor_certificate(
    multiplier: int,
    determinant_factor: int,
    max_hypotenuse: int,
) -> Certificate | None:
    """Certificate by scanning hypotenuse divisors of ``n^2*B^2 + 1``."""

    if multiplier <= 0:
        return None
    if max_hypotenuse <= 0:
        raise ValueError("max_hypotenuse must be positive")

    for hypotenuse in range(1, max_hypotenuse + 1):
        root = two_one_ray_determinant_divisor_root(
            multiplier,
            determinant_factor,
            hypotenuse,
        )
        if root is None:
            continue

        certificate = root.certificate(multiplier)
        if certificate is not None:
            return certificate

    return None


def two_one_ray_determinant_factor_certificate(
    multiplier: int,
    determinant_factor: int,
    max_hypotenuse: int,
) -> Certificate | None:
    """Certificate from a bounded negative-Pell slice with fixed ``u - 2v``."""

    if multiplier <= 0:
        return None

    for root in two_one_ray_determinant_factor_roots(
        determinant_factor,
        max_hypotenuse,
    ):
        certificate = root.certificate(multiplier)
        if certificate is not None:
            return certificate

    return None


@dataclass(frozen=True)
class TwoOneRayInverseRootWitness:
    """A factor-one inverse-root certificate witness for ``(2n, n)``."""

    multiplier: int
    direction: Point
    hypotenuse: int
    euclid_parameters: tuple[int, int]
    root: int

    @property
    def linear_factor(self) -> int:
        return two_one_ray_determinant_coordinates(self.direction)[0]

    @property
    def determinant_factor(self) -> int:
        return two_one_ray_determinant_coordinates(self.direction)[1]

    @property
    def determinant_slice_root(self) -> TwoOneRayDeterminantSliceRoot:
        root = two_one_ray_determinant_slice_root(
            self.linear_factor,
            self.determinant_factor,
            self.hypotenuse,
        )
        if root is None:
            raise AssertionError("inverse-root witness has no determinant slice")
        return root

    @property
    def determinant_divisor_root(self) -> TwoOneRayDeterminantSliceRoot:
        root = two_one_ray_determinant_divisor_root(
            self.multiplier,
            self.determinant_factor,
            self.hypotenuse,
        )
        if root is None:
            raise AssertionError("inverse-root witness has no divisor root")
        return root

    @property
    def reduced_determinant_slice_root(self) -> TwoOneRayDeterminantSliceRoot:
        return two_one_ray_determinant_slice_reduced_root(
            self.determinant_slice_root
        )

    @property
    def target(self) -> Point:
        return (2 * self.multiplier, self.multiplier)

    @property
    def certificate(self) -> Certificate:
        certificate = self.determinant_slice_root.certificate(self.multiplier)
        if certificate is None:
            raise AssertionError("inverse-root witness did not certify its target")
        return certificate

    def valid(self) -> bool:
        return self.certificate.valid()


def two_one_ray_inverse_root_witness(
    multiplier: int,
    max_parameter: int,
) -> TwoOneRayInverseRootWitness | None:
    """Search Euclid parameters for a factor-one root of ``multiplier``.

    This is a bounded probe for the inverse problem: instead of enlarging a
    midpoint box, find a primitive Pythagorean direction whose complement-
    divisor root is congruent to the target multiplier modulo ``2c``.  A hit
    immediately gives a factor-one parallel-direction certificate.
    """

    if multiplier <= 0:
        return None

    target = (2 * multiplier, multiplier)
    for u, v, hypotenuse, m, k in primitive_pythagorean_directions(max_parameter):
        root = two_one_ray_complement_divisor_root((u, v))
        if root is None or multiplier % (2 * hypotenuse) != root:
            continue

        certificate = parallel_direction_factor_certificate(target, (u, v), 1)
        if certificate is None:
            raise AssertionError("inverse-root congruence failed to certify")
        return TwoOneRayInverseRootWitness(
            multiplier=multiplier,
            direction=(u, v),
            hypotenuse=hypotenuse,
            euclid_parameters=(m, k),
            root=root,
        )

    return None


TWO_ONE_RAY_MOD_THIRTY_FOUR_DIRECTIONS: tuple[Point, ...] = (
    (15, -8),
    (15, 8),
    (-15, -8),
    (-15, 8),
)

TWO_ONE_RAY_MOD_FIFTY_EIGHT_DIRECTIONS: tuple[Point, ...] = (
    (-21, -20),
    (-21, 20),
    (21, -20),
    (21, 20),
)

TWO_ONE_RAY_MOD_SEVENTY_FOUR_DIRECTIONS: tuple[Point, ...] = (
    (-35, 12),
    (-35, -12),
    (35, 12),
    (35, -12),
)

TWO_ONE_RAY_MOD_EIGHTY_TWO_DIRECTIONS: tuple[Point, ...] = (
    (9, -40),
    (9, 40),
    (-9, -40),
    (-9, 40),
)

TWO_ONE_RAY_PROMOTED_SQUARE_FACTOR_HYPOTENUSES: tuple[int, ...] = (
    13,
    17,
    37,
    41,
)

TWO_ONE_RAY_PROMOTED_SCALED_FACTOR_LAYERS: tuple[tuple[Point, int], ...] = (
    ((-12, 5), 22),
    ((-12, -5), 2),
    ((20, -21), 2),
)

TWO_ONE_RAY_PROMOTED_DETERMINANT_SPLIT_FACTOR_HYPOTENUSES: tuple[int, ...] = (
    17,
    29,
    37,
    41,
    53,
    61,
    73,
    89,
    97,
    197,
    401,
)


def two_one_ray_promoted_square_factor_certificate(
    multiplier: int,
) -> Certificate | None:
    """Certificate from promoted square-determinant hypotenuse layers."""

    if multiplier <= 0:
        return None

    for hypotenuse in TWO_ONE_RAY_PROMOTED_SQUARE_FACTOR_HYPOTENUSES:
        certificate = two_one_ray_hypotenuse_square_factor_certificate(
            multiplier,
            hypotenuse,
        )
        if certificate is not None:
            return certificate

    return None


def two_one_ray_promoted_scaled_factor_certificate(
    multiplier: int,
) -> Certificate | None:
    """Certificate from promoted scaled fixed-factor layers."""

    if multiplier <= 0:
        return None

    for direction, base_factor in TWO_ONE_RAY_PROMOTED_SCALED_FACTOR_LAYERS:
        certificate = two_one_ray_scaled_factor_divisor_certificate(
            multiplier,
            direction,
            base_factor,
        )
        if certificate is not None:
            return certificate

    return None


def two_one_ray_promoted_determinant_split_factor_certificate(
    multiplier: int,
) -> Certificate | None:
    """Certificate from promoted determinant split-factor hypotenuse layers."""

    if multiplier <= 0:
        return None

    for hypotenuse in TWO_ONE_RAY_PROMOTED_DETERMINANT_SPLIT_FACTOR_HYPOTENUSES:
        certificate = two_one_ray_hypotenuse_determinant_split_factor_certificate(
            multiplier,
            hypotenuse,
        )
        if certificate is not None:
            return certificate

    return None


def two_one_ray_mod_twenty_six_divisor_certificate(
    multiplier: int,
) -> Certificate | None:
    """Certificate from a divisor ``3``, ``7``, ``19``, or ``23`` modulo ``26``."""

    for direction in ((5, 12), (-5, 12), (5, -12), (-5, -12)):
        certificate = two_one_ray_complement_divisor_certificate(
            multiplier,
            direction,
        )
        if certificate is not None:
            return certificate
    return None


def two_one_ray_mod_twenty_six_square_factor_certificate(
    multiplier: int,
) -> Certificate | None:
    """Certificate from a divisor in the square-factor class ``15 mod 26``."""

    return two_one_ray_square_determinant_divisor_certificate(
        multiplier,
        (5, -12),
    )


def two_one_ray_mod_twenty_six_divisor_orbit_certificate(
    target: Point,
) -> Certificate | None:
    """Symmetric certificate from a ``3``/``7``/``19``/``23 mod 26`` divisor."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        base = two_one_ray_mod_twenty_six_divisor_certificate(abs_h)
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
        base = two_one_ray_mod_twenty_six_divisor_certificate(abs_g)
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


def two_one_ray_mod_thirty_four_divisor_certificate(
    multiplier: int,
) -> Certificate | None:
    """Certificate from a divisor ``7``, ``13``, ``21``, or ``27`` modulo ``34``."""

    return two_one_ray_complement_divisor_sieve_certificate(
        multiplier,
        TWO_ONE_RAY_MOD_THIRTY_FOUR_DIRECTIONS,
    )


def two_one_ray_mod_thirty_four_divisor_orbit_certificate(
    target: Point,
) -> Certificate | None:
    """Symmetric certificate from a ``7``/``13``/``21``/``27 mod 34`` divisor."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        base = two_one_ray_mod_thirty_four_divisor_certificate(abs_h)
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
        base = two_one_ray_mod_thirty_four_divisor_certificate(abs_g)
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


def two_one_ray_mod_fifty_eight_divisor_certificate(
    multiplier: int,
) -> Certificate | None:
    """Certificate from a divisor ``7``, ``25``, ``33``, or ``51`` modulo ``58``."""

    return two_one_ray_complement_divisor_sieve_certificate(
        multiplier,
        TWO_ONE_RAY_MOD_FIFTY_EIGHT_DIRECTIONS,
    )


def two_one_ray_mod_fifty_eight_divisor_orbit_certificate(
    target: Point,
) -> Certificate | None:
    """Symmetric certificate from a ``7``/``25``/``33``/``51 mod 58`` divisor."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        base = two_one_ray_mod_fifty_eight_divisor_certificate(abs_h)
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
        base = two_one_ray_mod_fifty_eight_divisor_certificate(abs_g)
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


def two_one_ray_mod_seventy_four_divisor_certificate(
    multiplier: int,
) -> Certificate | None:
    """Certificate from a divisor ``7``, ``23``, ``51``, or ``67`` modulo ``74``."""

    return two_one_ray_complement_divisor_sieve_certificate(
        multiplier,
        TWO_ONE_RAY_MOD_SEVENTY_FOUR_DIRECTIONS,
    )


def two_one_ray_mod_seventy_four_divisor_orbit_certificate(
    target: Point,
) -> Certificate | None:
    """Symmetric certificate from a ``7``/``23``/``51``/``67 mod 74`` divisor."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        base = two_one_ray_mod_seventy_four_divisor_certificate(abs_h)
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
        base = two_one_ray_mod_seventy_four_divisor_certificate(abs_g)
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


def two_one_ray_mod_eighty_two_divisor_certificate(
    multiplier: int,
) -> Certificate | None:
    """Certificate from a divisor ``13``, ``29``, ``53``, or ``69`` modulo ``82``."""

    return two_one_ray_complement_divisor_sieve_certificate(
        multiplier,
        TWO_ONE_RAY_MOD_EIGHTY_TWO_DIRECTIONS,
    )


def two_one_ray_mod_eighty_two_divisor_orbit_certificate(
    target: Point,
) -> Certificate | None:
    """Symmetric certificate from a ``13``/``29``/``53``/``69 mod 82`` divisor."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        base = two_one_ray_mod_eighty_two_divisor_certificate(abs_h)
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
        base = two_one_ray_mod_eighty_two_divisor_certificate(abs_g)
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


@cache
def two_one_ray_mod_130_divisor_residues() -> tuple[int, ...]:
    """Divisor residues modulo 130 covered by the mod-10 or mod-26 families."""

    return tuple(
        residue
        for residue in range(130)
        if residue % 10 in (3, 7) or residue % 26 in (3, 7, 19, 23)
    )


def has_two_one_ray_mod_130_divisor(multiplier: int) -> bool:
    """Return whether the combined mod-10/mod-26 divisor sieve applies."""

    return has_divisor_in_residue_classes(
        multiplier,
        130,
        two_one_ray_mod_130_divisor_residues(),
    )


@cache
def two_one_ray_mod_2210_divisor_residues() -> tuple[int, ...]:
    """Divisor residues modulo 2210 covered by the mod-10, mod-26, or mod-34 families."""

    return tuple(
        residue
        for residue in range(2210)
        if (
            residue % 10 in (3, 7)
            or residue % 26 in (3, 7, 19, 23)
            or residue % 34 in (7, 13, 21, 27)
        )
    )


def has_two_one_ray_mod_2210_divisor(multiplier: int) -> bool:
    """Return whether the combined mod-10/mod-26/mod-34 divisor sieve applies."""

    return has_divisor_in_residue_classes(
        multiplier,
        2210,
        two_one_ray_mod_2210_divisor_residues(),
    )


@cache
def two_one_ray_mod_64090_divisor_residues() -> tuple[int, ...]:
    """Divisor residues modulo 64090 covered through the mod-58 family."""

    return tuple(
        residue
        for residue in range(64090)
        if (
            residue % 10 in (3, 7)
            or residue % 26 in (3, 7, 19, 23)
            or residue % 34 in (7, 13, 21, 27)
            or residue % 58 in (7, 25, 33, 51)
        )
    )


def has_two_one_ray_mod_64090_divisor(multiplier: int) -> bool:
    """Return whether the combined mod-10/mod-26/mod-34/mod-58 sieve applies."""

    return has_divisor_in_residue_classes(
        multiplier,
        64090,
        two_one_ray_mod_64090_divisor_residues(),
    )


@cache
def two_one_ray_mod_2371330_divisor_residues() -> tuple[int, ...]:
    """Divisor residues modulo 2371330 covered through the mod-74 family."""

    return tuple(
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


def has_two_one_ray_mod_2371330_divisor(multiplier: int) -> bool:
    """Return whether the combined divisor sieve through the mod-74 layer applies."""

    return has_divisor_in_residue_classes(
        multiplier,
        2371330,
        two_one_ray_mod_2371330_divisor_residues(),
    )


def two_one_ray_seed_certificate(multiplier: int) -> Certificate | None:
    """Certificate from the current exact infinite families on the ``(2,1)`` ray."""

    for constructor in (
        two_one_ray_mod260_skeleton_certificate,
        two_one_ray_mod_ten_divisor_certificate,
        two_one_ray_mod_twenty_six_divisor_certificate,
        two_one_ray_mod_twenty_six_square_factor_certificate,
        two_one_ray_promoted_square_factor_certificate,
        two_one_ray_promoted_scaled_factor_certificate,
        two_one_ray_mod_thirty_four_divisor_certificate,
        two_one_ray_mod_fifty_eight_divisor_certificate,
        two_one_ray_mod_seventy_four_divisor_certificate,
        two_one_ray_mod_eighty_two_divisor_certificate,
        two_one_ray_promoted_inverse_root_certificate,
        two_one_ray_explicit_base_certificate,
        two_one_ray_promoted_determinant_split_factor_certificate,
        two_one_ray_prime_one_mod_four_double_direction_certificate,
        two_one_ray_lift_three_square_endpoint_certificate,
    ):
        certificate = constructor(multiplier)
        if certificate is not None:
            return certificate
    return None


@cache
def two_one_ray_divisor_lift_certificate(multiplier: int) -> Certificate | None:
    """Scale a certified proper divisor on the ``(2,1)`` ray.

    If a proper divisor ``q`` of ``n`` already has a two-step certificate for
    ``(2q,q)``, scaling that certificate by ``n/q`` certifies ``(2n,n)``.
    Thus once the prime multipliers are handled, every composite multiplier
    follows automatically.
    """

    if multiplier <= 0:
        return None

    certificate = two_one_ray_seed_certificate(multiplier)
    if certificate is not None:
        return certificate

    for divisor in positive_divisors(multiplier):
        if divisor == 1 or divisor == multiplier:
            continue

        base = two_one_ray_divisor_lift_certificate(divisor)
        if base is None:
            continue

        certificate = scale_certificate(base, multiplier // divisor)
        if not certificate.valid():
            raise AssertionError("divisor-lift ray certificate did not scale correctly")
        return certificate

    return None


def two_one_ray_divisor_lift_orbit_certificate(target: Point) -> Certificate | None:
    """Symmetric certificate from divisor-lift closure on the ``(2,1)`` ray."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        base = two_one_ray_divisor_lift_certificate(abs_h)
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
        base = two_one_ray_divisor_lift_certificate(abs_g)
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


@cache
def two_one_ray_prime_divisor_lift_certificate(multiplier: int) -> Certificate | None:
    """Direct exceptional-ray certificate from prime seeds plus divisor lift.

    Every multiplier ``n > 1`` has a prime divisor ``p``. Once every prime
    multiplier ``p`` on the ``(2,1)`` ray has a seed certificate, scaling that
    seed by ``n/p`` certifies ``(2n,n)`` without a recursive divisor search.
    """

    if multiplier <= 1:
        return None

    for prime in prime_factors(multiplier):
        base = two_one_ray_seed_certificate(prime)
        if base is None:
            raise AssertionError(f"missing exceptional-ray prime seed for {prime}")

        certificate = scale_certificate(base, multiplier // prime)
        if certificate.target != (2 * multiplier, multiplier):
            raise AssertionError("prime-divisor lift target mismatch")
        if not certificate.valid():
            raise AssertionError("prime-divisor lift produced an invalid certificate")
        return certificate

    return None


def two_one_ray_prime_divisor_lift_orbit_certificate(target: Point) -> Certificate | None:
    """Symmetric direct prime-divisor lift certificate on the exceptional ray."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        base = two_one_ray_prime_divisor_lift_certificate(abs_h)
    elif abs_h == 2 * abs_g:
        base = two_one_ray_prime_divisor_lift_certificate(abs_g)
    else:
        return None

    if base is None:
        return None

    certificate = sign_swap_certificate(base, target)
    if certificate is None:
        raise AssertionError("prime-divisor lift orbit transform missed target")
    return certificate


def two_one_ray_mod260_skeleton_certificate(multiplier: int) -> Certificate | None:
    """Certificate for the mod-260 refinement of the ``(2, 1)`` ray skeleton."""

    if multiplier <= 0:
        return None

    certificate = two_one_ray_mod20_skeleton_certificate(multiplier)
    if certificate is not None:
        return certificate

    return two_one_ray_consecutive_certificate(multiplier, 5)


def two_one_ray_mod260_skeleton_residues() -> tuple[int, ...]:
    """Multiplier residues modulo 260 covered by the refined skeleton."""

    residues: list[int] = []
    for residue in range(260):
        multiplier = residue if residue != 0 else 260
        if two_one_ray_mod260_skeleton_certificate(multiplier) is not None:
            residues.append(residue)
    return tuple(residues)


def two_one_ray_mod260_skeleton_orbit_certificate(target: Point) -> Certificate | None:
    """Symmetric certificate for the mod-260 skeleton on the ``(2, 1)`` ray."""

    g, h = target
    abs_g, abs_h = abs(g), abs(h)
    if abs_g == 0 or abs_h == 0:
        return None

    if abs_g == 2 * abs_h:
        base = two_one_ray_mod260_skeleton_certificate(abs_h)
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
        base = two_one_ray_mod260_skeleton_certificate(abs_g)
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


def theorem3_divisor_certificate(
    target: Point,
    triple: PythagoreanTriple,
    x_sign: int,
    y_sign: int,
    divisor: int,
) -> Certificate | None:
    """Divisor-strengthened signed Theorem 3 certificate.

    This is the d = g - h slice of the signed length-difference identity.
    Replacing the paper's constant 1 by a nonzero divisor q of gh gives

        (c - sx*a) g = (c + sy*b) h - q.

    If q divides gh and gh/q is positive, then
    P = (sx*a*gh/q, sy*b*gh/q) is a two-step midpoint for (g, h).
    The paper's Theorem 3 is the special case q = 1.
    """

    if x_sign not in (-1, 1) or y_sign not in (-1, 1):
        raise ValueError("x_sign and y_sign must be -1 or 1")
    if divisor == 0:
        raise ValueError("divisor must be nonzero")
    if not triple.valid():
        raise ValueError("triple must be a positive Pythagorean triple")

    g, h = target
    if g == 0 or h == 0 or (g * h) % divisor != 0:
        return None

    a, b, c = triple.leg_a, triple.leg_b, triple.hypotenuse
    if (c - x_sign * a) * g != (c + y_sign * b) * h - divisor:
        return None

    coefficient = (g * h) // divisor
    if coefficient <= 0:
        return None

    certificate = Certificate(
        target=target,
        midpoint=(x_sign * a * coefficient, y_sign * b * coefficient),
    )
    if not certificate.valid():
        return None
    return certificate


def theorem3_ray_divisor_certificate(
    ray: Point,
    multiplier: int,
    triple: PythagoreanTriple,
    x_sign: int,
    y_sign: int,
) -> Certificate | None:
    """Ray form of the divisor-strengthened signed Theorem 3.

    For a primitive ray direction ``(p, q)`` and target ``n(p, q)``, the
    divisor relation has

        divisor = n * ((c + sy*b)q - (c - sx*a)p).

    Thus the chosen triple and signs certify every multiplier ``n`` for which
    that divisor divides ``p*q*n^2`` and the graph steps are nondegenerate.
    """

    if multiplier == 0:
        return None
    ray_divisor = theorem3_ray_divisor(ray, triple, x_sign, y_sign)
    if ray_divisor is None:
        return None

    target = (ray[0] * multiplier, ray[1] * multiplier)
    return theorem3_divisor_certificate(
        target,
        triple,
        x_sign,
        y_sign,
        multiplier * ray_divisor,
    )


def theorem3_ray_divisor(
    ray: Point,
    triple: PythagoreanTriple,
    x_sign: int,
    y_sign: int,
) -> int | None:
    """Return the fixed ray divisor L from the strengthened Theorem 3 form."""

    p, q = ray
    if p == 0 or q == 0:
        return None
    if x_sign not in (-1, 1) or y_sign not in (-1, 1):
        raise ValueError("x_sign and y_sign must be -1 or 1")
    if not triple.valid():
        raise ValueError("triple must be a positive Pythagorean triple")

    a, b, c = triple.leg_a, triple.leg_b, triple.hypotenuse
    ray_divisor = (c + y_sign * b) * q - (c - x_sign * a) * p
    if ray_divisor == 0:
        return None
    return ray_divisor


def theorem3_ray_divisor_modulus(
    ray: Point,
    triple: PythagoreanTriple,
    x_sign: int,
    y_sign: int,
) -> int | None:
    """Return the multiplier modulus forced by a ray divisor certificate.

    For target n(p, q), the fixed triple/sign choice certifies exactly those
    multipliers for which L divides p*q*n.  Thus all multiples of
    |L|/gcd(|L|, |p*q|) pass the divisibility test; the certificate checker
    still enforces the required sign and nondegeneracy conditions.
    """

    ray_divisor = theorem3_ray_divisor(ray, triple, x_sign, y_sign)
    if ray_divisor is None:
        return None

    p, q = ray
    return abs(ray_divisor) // gcd(abs(ray_divisor), abs(p * q))


def theorem3_ray_pell_divisor_certificate(
    ray: Point,
    multiplier: int,
    x_parameter: int,
    y_parameter: int,
    swap_legs: bool = False,
) -> Certificate | None:
    """Pell-parametrized ray-divisor subfamily of signed Theorem 3.

    Put m = x + y and n = y.  With the unswapped Euclid triple

        (m^2 - n^2, 2mn, m^2 + n^2)

    and signs (1, -1), the ray divisor is q*x^2 - 2*p*y^2.  Swapping the two
    legs gives the companion divisor 2*q*y^2 - p*x^2.  When that divisor has
    the right multiplier divisibility and sign, the strengthened Theorem 3
    checker returns the resulting certificate.
    """

    if x_parameter <= 0 or y_parameter <= 0:
        raise ValueError("Pell parameters must be positive")

    m = x_parameter + y_parameter
    n = y_parameter
    difference_leg = m * m - n * n
    even_leg = 2 * m * n
    hypotenuse = m * m + n * n
    if swap_legs:
        triple = PythagoreanTriple(even_leg, difference_leg, hypotenuse)
    else:
        triple = PythagoreanTriple(difference_leg, even_leg, hypotenuse)

    return theorem3_ray_divisor_certificate(ray, multiplier, triple, 1, -1)


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


@cache
def box_two_hundred_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 200."""

    return BOX_TWO_HUNDRED_RESIDUAL_LOOKUP.get(target)


@cache
def box_two_hundred_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 200."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 200:
        return None

    certificate = box_one_ninety_audit_certificate(target)
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

    return box_two_hundred_residual_certificate(target)


@cache
def box_two_ten_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 210."""

    return BOX_TWO_TEN_RESIDUAL_LOOKUP.get(target)


@cache
def box_two_ten_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 210."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 210:
        return None

    certificate = box_two_hundred_audit_certificate(target)
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

    return box_two_ten_residual_certificate(target)


@cache
def box_two_twenty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 220."""

    return BOX_TWO_TWENTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_two_twenty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 220."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 220:
        return None

    certificate = box_two_ten_audit_certificate(target)
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

    return box_two_twenty_residual_certificate(target)


@cache
def box_two_thirty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 230."""

    return BOX_TWO_THIRTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_two_thirty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 230."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 230:
        return None

    certificate = box_two_twenty_audit_certificate(target)
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

    return box_two_thirty_residual_certificate(target)


@cache
def box_two_forty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 240."""

    return BOX_TWO_FORTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_two_forty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 240."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 240:
        return None

    certificate = box_two_thirty_audit_certificate(target)
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

    return box_two_forty_residual_certificate(target)


@cache
def box_two_fifty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 250."""

    return BOX_TWO_FIFTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_two_fifty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 250."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 250:
        return None

    certificate = box_two_forty_audit_certificate(target)
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

    return box_two_fifty_residual_certificate(target)


@cache
def box_two_sixty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 260."""

    return BOX_TWO_SIXTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_two_sixty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 260."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 260:
        return None

    certificate = box_two_fifty_audit_certificate(target)
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

    return box_two_sixty_residual_certificate(target)


@cache
def box_two_seventy_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 270."""

    return BOX_TWO_SEVENTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_two_seventy_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 270."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 270:
        return None

    certificate = box_two_sixty_audit_certificate(target)
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

    return box_two_seventy_residual_certificate(target)


@cache
def box_two_eighty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 280."""

    return BOX_TWO_EIGHTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_two_eighty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 280."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 280:
        return None

    certificate = box_two_seventy_audit_certificate(target)
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

    return box_two_eighty_residual_certificate(target)


@cache
def box_two_ninety_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 290."""

    return BOX_TWO_NINETY_RESIDUAL_LOOKUP.get(target)


@cache
def box_two_ninety_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 290."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 290:
        return None

    certificate = box_two_eighty_audit_certificate(target)
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

    return box_two_ninety_residual_certificate(target)


@cache
def box_three_hundred_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 300."""

    return BOX_THREE_HUNDRED_RESIDUAL_LOOKUP.get(target)


@cache
def box_three_hundred_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 300."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 300:
        return None

    certificate = box_two_ninety_audit_certificate(target)
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

    return box_three_hundred_residual_certificate(target)


@cache
def box_three_ten_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 310."""

    return BOX_THREE_TEN_RESIDUAL_LOOKUP.get(target)


@cache
def box_three_ten_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 310."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 310:
        return None

    certificate = box_three_hundred_audit_certificate(target)
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

    return box_three_ten_residual_certificate(target)


@cache
def box_three_twenty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 320."""

    return BOX_THREE_TWENTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_three_twenty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 320."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 320:
        return None

    certificate = box_three_ten_audit_certificate(target)
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

    return box_three_twenty_residual_certificate(target)


@cache
def box_three_thirty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 330."""

    return BOX_THREE_THIRTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_three_thirty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 330."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 330:
        return None

    certificate = box_three_twenty_audit_certificate(target)
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

    return box_three_thirty_residual_certificate(target)


@cache
def box_three_forty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 340."""

    return BOX_THREE_FORTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_three_forty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 340."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 340:
        return None

    certificate = box_three_thirty_audit_certificate(target)
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

    return box_three_forty_residual_certificate(target)


@cache
def box_three_fifty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 350."""

    return BOX_THREE_FIFTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_three_fifty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 350."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 350:
        return None

    certificate = box_three_forty_audit_certificate(target)
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

    return box_three_fifty_residual_certificate(target)


@cache
def box_three_sixty_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 360."""

    return BOX_THREE_SIXTY_RESIDUAL_LOOKUP.get(target)


@cache
def box_three_sixty_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 360."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 360:
        return None

    certificate = box_three_fifty_audit_certificate(target)
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

    certificate = parallel_direction_cover_certificate(target, 8)
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

    return box_three_sixty_residual_certificate(target)


@cache
def box_five_hundred_residual_certificate(target: Point) -> Certificate | None:
    """Explicit residual certificates for the finite audit box |g|, |h| <= 500."""

    return BOX_FIVE_HUNDRED_RESIDUAL_LOOKUP.get(target)


@cache
def box_five_hundred_audit_certificate(target: Point) -> Certificate | None:
    """Certificate used by the exact finite audit for |g|, |h| <= 500."""

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None
    if max(abs(target[0]), abs(target[1])) > 500:
        return None

    certificate = box_three_sixty_audit_certificate(target)
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

    certificate = parallel_direction_cover_certificate(target, 8)
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

    return box_five_hundred_residual_certificate(target)


@cache
def box_five_hundred_ray_lift_certificate(target: Point) -> Certificate | None:
    """Scale the audited primitive representative for a target ray.

    The finite box-500 audit certifies every non-exception target in that box.
    If the primitive representative of ``target`` lies in the audited box and
    has a two-step certificate there, scaling that certificate certifies the
    requested target. Axis targets and the exceptional ``(2,1)`` ray use their
    theorem-level helpers first.
    """

    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None

    certificate = axis_orbit_proof_certificate(target)
    if certificate is not None:
        return certificate

    certificate = two_one_ray_prime_divisor_lift_orbit_certificate(target)
    if certificate is not None:
        return certificate

    g, h = target
    common_factor = gcd(abs(g), abs(h))
    if common_factor == 0:
        return None

    primitive = (g // common_factor, h // common_factor)
    if max(abs(primitive[0]), abs(primitive[1])) > 500:
        return None

    base = box_five_hundred_audit_certificate(primitive)
    if base is None:
        return None

    certificate = scale_certificate(base, common_factor)
    if certificate.target != target:
        raise AssertionError("box-500 ray lift target mismatch")
    if not certificate.valid():
        raise AssertionError("box-500 ray lift produced an invalid certificate")
    return certificate


@cache
def parallel_direction_primitive_ray_certificate(
    target: Point,
    max_parameter: int,
) -> Certificate | None:
    """Scale a finite-direction certificate from the primitive ray representative.

    The finite-direction parallel cover is a primitive-ray candidate: if the
    primitive representative of ``target`` has a certificate from the fixed
    direction set, every nonzero multiple of that representative is certified by
    scaling. Axis targets and solved non-primitive exceptional-ray targets are
    handled by their theorem-level helpers first.
    """

    if max_parameter < 2:
        raise ValueError("max_parameter must be at least 2")
    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None

    certificate = axis_orbit_proof_certificate(target)
    if certificate is not None:
        return certificate

    certificate = two_one_ray_prime_divisor_lift_orbit_certificate(target)
    if certificate is not None:
        return certificate

    witness = parallel_direction_primitive_ray_witness(target, max_parameter)
    if witness is None:
        return None

    certificate = witness.certificate
    if certificate.target != target:
        raise AssertionError("primitive-ray parallel-direction lift target mismatch")
    if not certificate.valid():
        raise AssertionError(
            "primitive-ray parallel-direction lift produced an invalid certificate"
        )
    return certificate


@cache
def parallel_direction_primitive_ray_witness(
    target: Point,
    max_parameter: int,
) -> PrimitiveRayParallelDirectionWitness | None:
    """Finite-direction cover witness on the primitive representative of a ray."""

    if max_parameter < 2:
        raise ValueError("max_parameter must be at least 2")
    if target == (0, 0) or target in KNOWN_DISTANCE_THREE_ORBIT:
        return None

    g, h = target
    common_factor = gcd(abs(g), abs(h))
    if common_factor == 0:
        return None

    primitive = (g // common_factor, h // common_factor)
    if primitive in KNOWN_DISTANCE_THREE_ORBIT:
        return None

    base_witness = parallel_direction_cover_witness(primitive, max_parameter)
    if base_witness is None:
        return None

    witness = PrimitiveRayParallelDirectionWitness(
        target=target,
        primitive=primitive,
        scale=common_factor,
        base_witness=base_witness,
    )
    if not witness.certificate.valid():
        raise AssertionError("primitive-ray witness produced an invalid certificate")
    return witness

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


def is_square(n: int) -> bool:
    if n < 0:
        return False
    root = isqrt(n)
    return root * root == n


def edge_delta(dx: int, dy: int) -> bool:
    return dx != 0 and dy != 0 and is_square(dx * dx + dy * dy)


def edge(a: Point, b: Point) -> bool:
    return edge_delta(b[0] - a[0], b[1] - a[1])


def path_is_valid(path: Iterable[Point]) -> bool:
    pts = list(path)
    return all(edge(a, b) for a, b in zip(pts, pts[1:]))


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

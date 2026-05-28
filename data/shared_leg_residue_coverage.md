# Shared-Leg Residue Coverage Audit

Date: 2026-05-28

This artifact records bounded residue evidence for the horizontal-axis
subproblem. It is not a proof: covering every residue class modulo 24 does not
imply that every integer in those classes has a certificate. It is a guardrail
for proof search, because it shows that simple residue obstructions modulo 24
are not visible in the current shared-leg data.

The tables are backed by tests in `tests/test_pythagorean_walks.py`.

## Euclid Parameter Difference Family

Family:
$$
n=t(m^2+mt+1),\qquad m\ge2,\quad t\ge1.
$$

Audit bounds: `2 <= m <= 80`, `1 <= t <= 80`.

| residue mod 24 | witness $n$ | midpoint | parameters |
|---:|---:|---:|---|
| 1 | 217 | $(-80,60)$ | $m=3,\ t=7$ |
| 3 | 75 | $(-21,28)$ | $m=2,\ t=5$ |
| 5 | 125 | $(-64,48)$ | $m=3,\ t=5$ |
| 7 | 7 | $(-9,12)$ | $m=2,\ t=1$ |
| 9 | 33 | $(-15,20)$ | $m=2,\ t=3$ |
| 11 | 635 | $(-1120,252)$ | $m=9,\ t=5$ |
| 13 | 13 | $(-32,24)$ | $m=3,\ t=1$ |
| 15 | 87 | $(-105,56)$ | $m=4,\ t=3$ |
| 17 | 185 | $(-135,72)$ | $m=4,\ t=5$ |
| 19 | 43 | $(-245,84)$ | $m=6,\ t=1$ |
| 21 | 21 | $(-75,40)$ | $m=4,\ t=1$ |
| 23 | 335 | $(-385,132)$ | $m=6,\ t=5$ |

## Bounded Shared-Leg Generator

Generator bounds: Euclid triples with `2 <= m <= 30`, `1 <= k < m`,
`1 <= d <= 10`, restricted to targets `3 <= n <= 200`.

| residue mod 24 | witness $n$ | midpoint | shared-leg data |
|---:|---:|---:|---|
| 1 | 25 | $(9,12)$ | $y=12$, legs $(9,16)$, sum |
| 3 | 3 | $(-7,24)$ | $y=24$, legs $(7,10)$, difference |
| 5 | 77 | $(32,24)$ | $y=24$, legs $(32,45)$, sum |
| 7 | 7 | $(-9,12)$ | $y=12$, legs $(9,16)$, difference |
| 9 | 9 | $(-6,8)$ | $y=8$, legs $(6,15)$, difference |
| 11 | 11 | $(-5,12)$ | $y=12$, legs $(5,16)$, difference |
| 13 | 13 | $(-32,24)$ | $y=24$, legs $(32,45)$, difference |
| 15 | 39 | $(7,24)$ | $y=24$, legs $(7,32)$, sum |
| 17 | 17 | $(7,24)$ | $y=24$, legs $(7,10)$, sum |
| 19 | 19 | $(-16,12)$ | $y=12$, legs $(16,35)$, difference |
| 21 | 21 | $(6,8)$ | $y=8$, legs $(6,15)$, sum |
| 23 | 119 | $(55,48)$ | $y=48$, legs $(55,64)$, sum |

## Interpretation

- The even horizontal targets are already covered separately by the midpoint
  lemma, except for the explicit target $n=4$.
- Both the symbolic family and the bounded shared-leg search hit every odd
  residue modulo 24.
- The next proof task is not to find a missing residue class modulo 24, but to
  turn one of these residue witnesses into a construction that covers all
  integers in a family, such as a divisibility class or a parametrized sequence.

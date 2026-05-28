# Pythagorean Walks: Horizontal-Axis Subproblem

Date: 2026-05-28  
Paper: Jan Willemson, "Pythagorean walks on $\mathbb{Z}^2$", arXiv:2605.20831v1.

## Selected Open Aspect

The paper's central open conjecture says that the only vertices at graph distance $3$ from $O=(0,0)$ are $(1,0)$, $(2,0)$, $(2,1)$ and their symmetric counterparts.

I will focus first on the horizontal-axis slice:

**Target statement.** For every integer $n \ge 3$,
$$
d((0,0),(n,0)) \le 2.
$$

This is a strict subproblem of the conjecture. It is worth isolating because Theorem 3 in the paper assumes $g,h \ne 0$, so it does not directly cover targets with $h=0$. The paper proves that $(1,0)$ and $(2,0)$ have distance $3$; the conjecture predicts that every later axis point has distance $2$.

## Two-Step Certificate

A two-step path
$$
(0,0) \to (x,y) \to (n,0)
$$
exists exactly when there are integers $x,y,u,v$ such that
$$
u^2=x^2+y^2,\qquad v^2=(x-n)^2+y^2,
$$
with the graph edge restrictions
$$
x\ne0,\qquad x\ne n,\qquad y\ne0.
$$

Equivalently, we need two integer right triangles sharing the leg $|y|$, whose other horizontal legs differ by $n$.

Subtracting the two square equations gives
$$
u^2-v^2=2nx-n^2.
$$
With
$$
r=u-v,\qquad s=u+v,
$$
we get
$$
rs=2nx-n^2,\qquad x=\frac{rs+n^2}{2n},\qquad u=\frac{s+r}{2},\qquad v=\frac{s-r}{2}.
$$

This parameterization is useful only when:

- $r$ and $s$ have the same parity;
- $rs\equiv -n^2 \pmod {2n}$, so $x$ is integral;
- $y^2=u^2-x^2$ is a nonzero square;
- $x\notin\{0,n\}$.

## Initial Computational Notes

I ran a bounded direct search for $3\le n\le20$, looking for small certificates $(x,y)$ with both distances integral. The table records one certificate per $n$:

| $n$ | intermediate point $(x,y)$ | $|OP|$ | $|P(n,0)|$ |
|---:|---:|---:|---:|
| 3 | $(-7,24)$ | 25 | 26 |
| 4 | $(-5,12)$ | 13 | 15 |
| 5 | $(-22,120)$ | 122 | 123 |
| 6 | $(3,4)$ | 5 | 5 |
| 7 | $(-9,12)$ | 15 | 20 |
| 8 | $(4,3)$ | 5 | 5 |
| 9 | $(-6,8)$ | 10 | 17 |
| 10 | $(5,12)$ | 13 | 13 |
| 11 | $(-5,12)$ | 13 | 20 |
| 12 | $(6,8)$ | 10 | 10 |
| 13 | $(-32,24)$ | 40 | 51 |
| 14 | $(5,12)$ | 13 | 15 |
| 15 | $(-90,56)$ | 106 | 119 |
| 16 | $(8,6)$ | 10 | 10 |
| 17 | $(7,24)$ | 25 | 26 |
| 18 | $(9,12)$ | 15 | 15 |
| 19 | $(-16,12)$ | 20 | 37 |
| 20 | $(10,24)$ | 26 | 26 |

Observations:

- The midpoint construction works whenever $n/2$ is a leg of a Pythagorean triangle: choose $x=n/2$ and a nonzero $y$ with $(n/2)^2+y^2$ square.
- In fact this covers every even $n\ge 6$. The earlier note that it did not cover all even $n$ was false: the certificate found first by a bounded search need not be the midpoint certificate.
- Several odd $n$ have certificates with $x<0$, so allowing the intermediate point to lie outside the segment from $(0,0)$ to $(n,0)$ seems essential.

## Lemma: Even Horizontal Targets

For every even $n\ge 6$, there is a two-step path from $(0,0)$ to $(n,0)$.

Write $n=2a$, so $a\ge 3$. Every integer $a\ge 3$ is a leg of an integer right triangle:

- if $a$ is odd, use
  $$
  a^2+\left(\frac{a^2-1}{2}\right)^2=\left(\frac{a^2+1}{2}\right)^2;
  $$
- if $a=2k$ is even, use
  $$
  (2k)^2+(k^2-1)^2=(k^2+1)^2.
  $$

In either case choose a positive partner leg $y$ and set $P=(a,y)$. Then
$$
|OP|^2=a^2+y^2=|P(n,0)|^2,
$$
and both edges are legal because $a\ne0$, $a\ne n$, and $y\ne0$. Thus
$$
(0,0)\to(a,y)\to(2a,0)
$$
is a valid two-step certificate.

This leaves only $n=4$ among the even targets in the selected range $n\ge3$; the artifact and tests record the explicit certificate
$$
(0,0)\to(-5,12)\to(4,0).
$$
The paper proves $n=2$ is a genuine distance-$3$ exception.

## Shared-Leg Generator For Axis Certificates

A two-step certificate for $(n,0)$ is equivalent to two Pythagorean triples sharing the vertical leg $|y|$. If
$$
a^2+y^2=c_1^2,\qquad b^2+y^2=c_2^2,\qquad 0<a<b,
$$
then the pair gives two horizontal-axis targets:

- the difference target $n=b-a$, certified by $P=(-a,y)$;
- the sum target $n=a+b$, certified by $P=(a,y)$.

This is now implemented in `shared_leg_axis_certificate_records`, using Euclid triples
$$
d(m^2-k^2),\quad 2dmk,\quad d(m^2+k^2).
$$

Current bounded audit:

- parameters $2\le m\le30$, $1\le k<m$, $1\le d\le10$;
- targets $3\le n\le200$;
- every odd $n$ in that range has at least one generated shared-leg certificate.

This is not a proof of the odd case. It is useful evidence and, more importantly, a reproducible certificate source for testing proposed residue-class lemmas.

## Lemma: A Quadratic Shared-Leg Family

For integers $m\ge2$ and $t\ge1$, the horizontal target
$$
n=t(m^2+mt+1)
$$
has a two-step certificate.

Start from the Euclid triples with parameters $(m,1)$ and $(m+t,1)$, then scale them to the common vertical leg
$$
y=2m(m+t).
$$
This gives
$$
\begin{aligned}
a&=(m+t)(m^2-1),&
c_1&=(m+t)(m^2+1),\\
b&=m((m+t)^2-1),&
c_2&=m((m+t)^2+1).
\end{aligned}
$$
Direct expansion gives
$$
a^2+y^2=c_1^2,\qquad b^2+y^2=c_2^2,
$$
and
$$
b-a=m((m+t)^2-1)-(m+t)(m^2-1)=t(m^2+mt+1).
$$
Since $m\ge2$ and $t\ge1$, both horizontal legs and the shared vertical leg are nonzero. Therefore
$$
(0,0)\to(-a,y)\to(t(m^2+mt+1),0)
$$
is a valid two-step path.

The case $t=1$ gives the visible sequence
$$
n=m^2+m+1=7,13,21,31,43,57,\ldots.
$$

## Residue Coverage Audit

The file `data/shared_leg_residue_coverage.md` records a bounded residue audit
modulo $24$.

Two sources were checked:

- the symbolic family $n=t(m^2+mt+1)$ with $2\le m\le80$ and $1\le t\le80$;
- the bounded shared-leg generator with Euclid parameters $m\le30$ and
  scale $d\le10$, restricted to targets $3\le n\le200$.

Both sources contain witnesses for every odd residue class modulo $24$.

This does not prove the odd case. It is a useful negative result for proof
search: there is no simple obstruction among the odd residue classes modulo
$24$ in the current data. The next step should be stronger than residue
sampling, for example a construction that covers every odd multiple of a
specified base family, or a parametrized family whose image can be matched to
an infinite arithmetic or divisibility class.

## Possible Source Typo To Track

In the downloaded TeX, the first displayed equation in the proof of Theorem 3 appears as
$$
(agh\pm g)^2+(bgh\pm h)\stackrel{?}{=}(cgh+(h-g))^2,
$$
while the next line expands $(bgh\pm h)^2$. The intended first line is almost certainly
$$
(agh\pm g)^2+(bgh\pm h)^2\stackrel{?}{=}(cgh+(h-g))^2.
$$
I left the paper transcription faithful to the source and record the issue here.

## Attack Plan

1. Formalize the subproblem and keep it executable.

Prove the certificate criterion above as a lemma, including all non-horizontal and non-vertical edge restrictions. This becomes the target interface for every later construction.

At the same time, maintain a verification suite in `tests/` and reusable predicates in `experiments/`. The suite should be treated as part of the research log, not as an afterthought: every new lemma, conjectural family, and counterexample should get an executable check.

Current command:

```bash
python3 -m unittest discover -s tests -v
```

2. Build a certificate generator from paired Pythagorean triples.

Use Euclid's formula
$$
(A,B,C)=d(m^2-k^2,2mk,m^2+k^2)
$$
with scaling, and force two triples to share one leg:
$$
y=B_1=B_2,\qquad n=|A_1-A_2|.
$$
Track the alternative cases where the shared leg is the odd leg in one triple and the even leg in the other.

3. Split by easy infinite families.

Start with classes where an explicit formula is visible:

- $n=2a$ with $a\ge3$, via midpoint certificates. This proves all even $n\ge6$.
- $n$ equal to the difference of two legs in triples sharing a common leg.
- $n$ equal to the sum of two such legs, corresponding to certificates with $x<0$.

Each family should produce a lemma with a certificate formula and a checklist for excluded small cases.

4. Turn the remaining cases into modular coverage.

For a chosen family of shared-leg triples, compute the set of residues of $n$ covered modulo a natural modulus $M$. Increase the family until either all residues except $1,2$ are covered or the missing residues show a real obstruction.

5. If modular coverage stalls, switch to the factor equation.

Use
$$
x=\frac{rs+n^2}{2n},\qquad y^2=\left(\frac{s+r}{2}\right)^2-x^2
$$
and search for structured choices of $r,s$ as functions of $n$ that make $y^2$ square. This is likely to expose Pell-type or elliptic-curve structure.

6. Maintain proof and computation in lockstep.

For every proposed construction:

- record the formula for $(x,y,u,v)$;
- verify algebraically that $u^2=x^2+y^2$ and $v^2=(x-n)^2+y^2$;
- record edge exclusions;
- run a bounded search for counterexamples in the claimed residue class;
- only then promote the construction to a lemma.

7. Expand the verification suite whenever confusion appears.

The author reports that previous AI attempts got lost in unproductive lines of reasoning. The guardrail here is to make mistaken hypotheses cheap to falsify. When a new idea is proposed, add tests in one of these categories:

- **Predicate tests:** validate low-level graph definitions, especially the no-horizontal/no-vertical edge rule.
- **Certificate tests:** verify explicit paths from the paper and from our constructions.
- **Negative bounded searches:** for claimed obstructions, search a large box and fail if a certificate is found. These are not proofs, but they catch many unreasonable obstruction hypotheses early.
- **Formula tests:** for any parametrized family, test many parameter values and assert that every produced midpoint is a valid two-step certificate.
- **Regression tests:** when a hypothesis fails, keep the counterexample as a test so the same mistake is not reintroduced under a different name.
- **Coverage tests:** for a stated finite range or residue class, assert that the generator covers exactly what the note says it covers.

The suite should never be allowed to blur the line between a bounded search and a proof. Bounded tests can disprove universal claims and increase confidence in constructions; exact algebraic lemmas remain necessary for proof.

## Verification Suite Status

Initial files:

- `experiments/pythagorean_walks.py`: square tests, edge predicates, path validation, two-step certificate validation, and bounded certificate search.
- `tests/test_pythagorean_walks.py`: checks paper examples, graph edge restrictions, the known three-step path to $(1,0)$, the horizontal-axis certificates for $3\le n\le20$, and bounded negative checks for $(1,0),(2,0),(2,1)$.
- `data/horizontal_axis_certificates.json`: reusable recorded certificates and known horizontal-axis exceptions.
- `data/shared_leg_residue_coverage.md`: residue witness audit for the symbolic family and bounded shared-leg generator.
- `notes/verification-changelog.md`: audit trail for corrected hypotheses, new guardrails, and the tests that enforce them.

Current passing result:

```text
Ran 16 tests in 0.861s
OK
```

Current executable additions:

- Parametrized tests check the implemented midpoint formula for every even $n$ from $6$ through $400$.
- Shared-leg generator tests validate every produced certificate for a small parameter box.
- A bounded audit test records that the shared-leg generator covers every odd $n$ through $200$ with $m\le30$ and $d\le10$.
- The quadratic shared-leg family $n=t(m^2+mt+1)$ is tested for $2\le m<50$ and $1\le t<20$.
- Residue witness tests check that both the quadratic family and bounded shared-leg generator hit every odd class modulo $24$.
- Bounded search results now label missing certificates as `not_found_within_bound`, not as impossibility proofs.
- Certificate examples for $3\le n\le20$ are stored in JSON and validated by the test suite.

Immediate improvements needed:

- Convert the residue audit into stronger infinite-family coverage; residue witnesses alone do not prove any full congruence class.
- Keep extending `notes/verification-changelog.md` when a hypothesis fails or graduates into a tested lemma.

## Next Notes To Add

- A small script or table that groups certificates by shared-leg pattern.
- A divisibility or parametrized-family coverage table that goes beyond residues.
- A proof attempt for the midpoint family and for one non-midpoint family, likely covering $n\equiv 3,4,5 \pmod 8$ or a similar coarse split.
- Changelog entries for each failed idea or promoted lemma.

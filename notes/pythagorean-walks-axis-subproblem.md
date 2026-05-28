# Pythagorean Walks: Horizontal-Axis Subproblem

Date: 2026-05-28  
Paper: Jan Willemson, "Pythagorean walks on $\mathbb{Z}^2$", arXiv:2605.20831v1.

## Horizontal-Axis Target

The paper's central open conjecture says that the only vertices at graph distance $3$ from $O=(0,0)$ are $(1,0)$, $(2,0)$, $(2,1)$ and their symmetric counterparts.

This note proves the horizontal-axis slice:

**Target statement.** For every integer $n \ge 3$,
$$
d((0,0),(n,0)) \le 2.
$$

This is a strict subproblem of the conjecture. It is worth isolating because Theorem 3 in the paper assumes $g,h \ne 0$, so it does not directly cover targets with $h=0$. The paper proves that $(1,0)$ and $(2,0)$ have distance $3$; the result below proves that every later horizontal-axis point has a two-step path from the origin.

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
- The odd case is now resolved by the consecutive-parameter Euclid construction below. The small certificates in the table are retained as executable examples; they are not always the certificates produced by the final formula.

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

## Lemma: Odd Horizontal Targets

For every odd integer $n\ge3$, there is a two-step path from $(0,0)$ to $(n,0)$.

Let
$$
\alpha=\frac{n-1}{2},\qquad \beta=\frac{n+1}{2}.
$$
These are positive integers. Use Euclid's formula with consecutive parameter pairs $(n+1,n)$ and $(n,n-1)$:
$$
(2n+1)^2+\bigl(2n(n+1)\bigr)^2=(2n^2+2n+1)^2,
$$
and
$$
(2n-1)^2+\bigl(2n(n-1)\bigr)^2=(2n^2-2n+1)^2.
$$
Scale the first triple by $\alpha$ and the second by $\beta$. Their even legs become equal because
$$
\alpha\,2n(n+1)=\beta\,2n(n-1)=n(n^2-1).
$$
Set
$$
\begin{aligned}
a&=\alpha(2n+1),&
b&=\beta(2n-1),&
y&=n(n^2-1),\\
c&=\alpha(2n^2+2n+1),&
d&=\beta(2n^2-2n+1).
\end{aligned}
$$
Then the scaled triples give
$$
a^2+y^2=c^2,\qquad b^2+y^2=d^2.
$$
Their horizontal legs differ by exactly $n$:
$$
b-a
=\frac{(n+1)(2n-1)-(n-1)(2n+1)}{2}
=n.
$$
Therefore $P=(-a,y)$ certifies the target $(n,0)$, since the first horizontal displacement has length $a$ and the second has length $n+a=b$:
$$
(0,0)\to(-a,y)\to(n,0).
$$
The edge restrictions hold because $a>0$, $b>0$, and $y=n(n^2-1)>0$, so $x=-a$ is neither $0$ nor $n$ and the vertical displacement is nonzero.

For example, $n=3$ gives $a=7$, $b=10$, and $y=24$, hence the recorded certificate
$$
(0,0)\to(-7,24)\to(3,0).
$$

## Theorem: Horizontal-Axis Statement

For every integer $n\ge3$,
$$
d((0,0),(n,0))\le2.
$$

Proof. Split into the required cases.

- If $n=3$, the odd-target lemma gives the explicit certificate $(-7,24)$.
- If $n=4$, the explicit certificate $(-5,12)$ works because
  $$
  (-5)^2+12^2=13^2,\qquad (4-(-5))^2+12^2=15^2.
  $$
- If $n\ge6$ is even, the midpoint lemma applies.
- If $n\ge5$ is odd, the odd-target lemma applies.

In every case the displayed intermediate point has nonzero vertical displacement and both horizontal displacements are nonzero, so it is a legal two-step path in the Pythagorean-walk graph. This proves the target statement.

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

This bounded audit was not a proof of the odd case. It remains useful evidence and, more importantly, a reproducible certificate source for testing proposed residue-class lemmas.

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

This did not prove the odd case and is not used in the final theorem. It remains
as a proof-search artifact: there was no simple obstruction among the odd
residue classes modulo $24$ in the sampled data. The odd case is instead proved
by the consecutive-parameter Euclid construction above.

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

## Verification Suite Status

The executable workspace mirrors the final proof and the proof-search artifacts:

- `experiments/pythagorean_walks.py`: square tests, edge predicates, path validation, two-step certificate validation, bounded certificate search, formula constructors, and `horizontal_axis_proof_certificate`, which encodes the final case split.
- `tests/test_pythagorean_walks.py`: checks paper examples, graph edge restrictions, the known three-step path to $(1,0)$, the horizontal-axis certificates for $3\le n\le20$, formula families, the final theorem case split, and bounded negative checks for $(1,0),(2,0),(2,1)$.
- `data/horizontal_axis_certificates.json`: reusable recorded certificates and known horizontal-axis exceptions.
- `data/shared_leg_residue_coverage.md`: residue witness audit for the symbolic family and bounded shared-leg generator.
- `notes/verification-changelog.md`: audit trail for corrected hypotheses, new guardrails, and the tests that enforce them.

Current passing result:

```text
Ran 19 tests
OK
```

Current executable additions:

- Parametrized tests check the implemented midpoint formula for every even $n$ from $6$ through $400$.
- The explicit $n=4$ certificate is exposed as `explicit_axis_certificate` and tested directly.
- The consecutive-parameter odd formula is tested for every odd $n$ from $3$ through $401$.
- `horizontal_axis_proof_certificate` is tested for every integer $3\le n\le501$.
- Shared-leg generator tests validate every produced certificate for a small parameter box.
- A bounded audit test records that the shared-leg generator covers every odd $n$ through $200$ with $m\le30$ and $d\le10$.
- The quadratic shared-leg family $n=t(m^2+mt+1)$ is tested for $2\le m<50$ and $1\le t<20$.
- Residue witness tests check that both the quadratic family and bounded shared-leg generator hit every odd class modulo $24$.
- Bounded search results now label missing certificates as `not_found_within_bound`, not as impossibility proofs.
- Certificate examples for $3\le n\le20$ are stored in JSON and validated by the test suite.

The suite should never be read as a substitute for the algebraic proof above.
Its role is to verify the implemented formulas and prevent previous false
proof-search claims from being reintroduced.

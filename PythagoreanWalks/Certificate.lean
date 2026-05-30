import Mathlib

namespace PythagoreanWalks

structure Point where
  x : Int
  y : Int
deriving DecidableEq, Repr

namespace Point

@[ext]
theorem ext {p q : Point} (hx : p.x = q.x) (hy : p.y = q.y) : p = q := by
  cases p
  cases q
  simp_all

end Point

def sq (n : Int) : Int :=
  n * n

def add (p q : Point) : Point :=
  { x := p.x + q.x, y := p.y + q.y }

def sub (p q : Point) : Point :=
  { x := p.x - q.x, y := p.y - q.y }

def smul (k : Int) (p : Point) : Point :=
  { x := k * p.x, y := k * p.y }

def signPoint (sx sy : Int) (p : Point) : Point :=
  { x := sx * p.x, y := sy * p.y }

def swapPoint (p : Point) : Point :=
  { x := p.y, y := p.x }

def signedSwapPoint (sx sy : Int) (doSwap : Bool) (p : Point) : Point :=
  signPoint sx sy (if doSwap then swapPoint p else p)

def gaussianMul (p q : Point) : Point :=
  { x := p.x * q.x - p.y * q.y, y := p.x * q.y + p.y * q.x }

def dot (p q : Point) : Int :=
  p.x * q.x + p.y * q.y

def det (p q : Point) : Int :=
  p.x * q.y - p.y * q.x

def normSq (p : Point) : Int :=
  sq p.x + sq p.y

def nonAxis (p : Point) : Prop :=
  p.x ≠ 0 ∧ p.y ≠ 0

def isIntSquare (n : Int) : Prop :=
  ∃ z : Int, n = z * z

def legalStep (p : Point) : Prop :=
  nonAxis p ∧ isIntSquare (normSq p)

def certificateValid (target midpoint : Point) : Prop :=
  legalStep midpoint ∧ legalStep (sub target midpoint)

theorem sign_ne_zero_of_pm_one {s : Int} (hs : s = 1 ∨ s = -1) : s ≠ 0 := by
  rcases hs with rfl | rfl <;> norm_num

theorem sign_sq_of_pm_one {s : Int} (hs : s = 1 ∨ s = -1) : s * s = 1 := by
  rcases hs with rfl | rfl <;> norm_num

theorem normSq_smul (k : Int) (p : Point) :
    normSq (smul k p) = k * k * normSq p := by
  simp [normSq, smul, sq]
  ring

theorem legalStep_smul {k : Int} {p : Point} (hk : k ≠ 0) (hp : legalStep p) :
    legalStep (smul k p) := by
  rcases hp with ⟨⟨hx, hy⟩, ⟨z, hz⟩⟩
  constructor
  · constructor
    · intro h
      apply hx
      have hmul : k * p.x = 0 := by
        simpa [smul] using h
      rcases mul_eq_zero.mp hmul with hk0 | hp0
      · exact False.elim (hk hk0)
      · exact hp0
    · intro h
      apply hy
      have hmul : k * p.y = 0 := by
        simpa [smul] using h
      rcases mul_eq_zero.mp hmul with hk0 | hp0
      · exact False.elim (hk hk0)
      · exact hp0
  · refine ⟨k * z, ?_⟩
    calc
      normSq (smul k p) = k * k * normSq p := normSq_smul k p
      _ = k * k * (z * z) := by rw [hz]
      _ = (k * z) * (k * z) := by ring

theorem sub_smul (k : Int) (p q : Point) :
    sub (smul k p) (smul k q) = smul k (sub p q) := by
  ext <;> simp [sub, smul] <;> ring

theorem certificateValid_smul {k : Int} {target midpoint : Point}
    (hk : k ≠ 0) (hcert : certificateValid target midpoint) :
    certificateValid (smul k target) (smul k midpoint) := by
  rcases hcert with ⟨hmidpoint, hsecond⟩
  constructor
  · exact legalStep_smul hk hmidpoint
  · rw [sub_smul]
    exact legalStep_smul hk hsecond

theorem signedSwapPoint_smul (sx sy k : Int) (doSwap : Bool) (p : Point) :
    signedSwapPoint sx sy doSwap (smul k p) =
      smul k (signedSwapPoint sx sy doSwap p) := by
  cases doSwap <;>
    ext <;>
    simp [signedSwapPoint, signPoint, swapPoint, smul] <;>
    ring

theorem normSq_signedSwapPoint {sx sy : Int} {doSwap : Bool} (p : Point)
    (hsx : sx = 1 ∨ sx = -1) (hsy : sy = 1 ∨ sy = -1) :
    normSq (signedSwapPoint sx sy doSwap p) = normSq p := by
  rcases hsx with rfl | rfl <;>
    rcases hsy with rfl | rfl <;>
    cases doSwap <;>
    simp [signedSwapPoint, signPoint, swapPoint, normSq, sq] <;>
    ring

theorem nonAxis_signedSwapPoint {sx sy : Int} {doSwap : Bool} {p : Point}
    (hsx : sx = 1 ∨ sx = -1) (hsy : sy = 1 ∨ sy = -1) (hp : nonAxis p) :
    nonAxis (signedSwapPoint sx sy doSwap p) := by
  rcases hp with ⟨hx, hy⟩
  rcases hsx with rfl | rfl <;>
    rcases hsy with rfl | rfl <;>
    cases doSwap <;>
    simp [nonAxis, signedSwapPoint, signPoint, swapPoint, hx, hy]

theorem legalStep_signedSwapPoint {sx sy : Int} {doSwap : Bool} {p : Point}
    (hsx : sx = 1 ∨ sx = -1) (hsy : sy = 1 ∨ sy = -1) (hp : legalStep p) :
    legalStep (signedSwapPoint sx sy doSwap p) := by
  rcases hp with ⟨hp_nonAxis, z, hz⟩
  constructor
  · exact nonAxis_signedSwapPoint hsx hsy hp_nonAxis
  · refine ⟨z, ?_⟩
    calc
      normSq (signedSwapPoint sx sy doSwap p) = normSq p :=
        normSq_signedSwapPoint p hsx hsy
      _ = z * z := hz

theorem sub_signedSwapPoint (sx sy : Int) (doSwap : Bool) (p q : Point) :
    sub (signedSwapPoint sx sy doSwap p) (signedSwapPoint sx sy doSwap q) =
      signedSwapPoint sx sy doSwap (sub p q) := by
  cases doSwap <;>
    ext <;>
    simp [sub, signedSwapPoint, signPoint, swapPoint] <;>
    ring

theorem certificateValid_signedSwapPoint {sx sy : Int} {doSwap : Bool}
    {target midpoint : Point}
    (hsx : sx = 1 ∨ sx = -1) (hsy : sy = 1 ∨ sy = -1)
    (hcert : certificateValid target midpoint) :
    certificateValid
      (signedSwapPoint sx sy doSwap target)
      (signedSwapPoint sx sy doSwap midpoint) := by
  rcases hcert with ⟨hmidpoint, hsecond⟩
  constructor
  · exact legalStep_signedSwapPoint hsx hsy hmidpoint
  · rw [sub_signedSwapPoint]
    exact legalStep_signedSwapPoint hsx hsy hsecond

theorem certificateValid_signedSwapPoint_smul {sx sy k : Int} {doSwap : Bool}
    {target midpoint : Point}
    (hsx : sx = 1 ∨ sx = -1) (hsy : sy = 1 ∨ sy = -1)
    (hk : k ≠ 0) (hcert : certificateValid target midpoint) :
    certificateValid
      (signedSwapPoint sx sy doSwap (smul k target))
      (signedSwapPoint sx sy doSwap (smul k midpoint)) := by
  exact certificateValid_signedSwapPoint hsx hsy
    (certificateValid_smul hk hcert)

theorem certificateValid_evenAxisMidpoint {a b c : Int}
    (ha : a ≠ 0) (hb : b ≠ 0)
    (hleg : sq a + sq b = c * c) :
    certificateValid ({ x := 2 * a, y := 0 } : Point) ({ x := a, y := b } : Point) := by
  constructor
  · constructor
    · exact ⟨ha, hb⟩
    · exact ⟨c, by simpa [normSq] using hleg⟩
  · constructor
    · constructor
      · intro h
        apply ha
        have hcoord : 2 * a - a = 0 := by simpa [sub] using h
        linarith
      · intro h
        apply hb
        have hcoord : 0 - b = 0 := by simpa [sub] using h
        linarith
    · refine ⟨c, ?_⟩
      calc
        normSq (sub ({ x := 2 * a, y := 0 } : Point) ({ x := a, y := b } : Point))
            = sq a + sq b := by
              simp [normSq, sub, sq]
              ring
        _ = c * c := hleg

theorem certificateValid_axisDifferenceOfSharedLeg
    {small large shared cSmall cLarge : Int}
    (hsmall : small ≠ 0) (hlarge : large ≠ 0) (hshared : shared ≠ 0)
    (hfirst : sq small + sq shared = cSmall * cSmall)
    (hsecond : sq large + sq shared = cLarge * cLarge) :
    certificateValid
      ({ x := large - small, y := 0 } : Point)
      ({ x := -small, y := shared } : Point) := by
  constructor
  · constructor
    · constructor
      · intro h
        apply hsmall
        have hcoord : -small = 0 := by simpa using h
        linarith
      · exact hshared
    · refine ⟨cSmall, ?_⟩
      calc
        normSq ({ x := -small, y := shared } : Point)
            = sq small + sq shared := by
              simp [normSq, sq]
        _ = cSmall * cSmall := hfirst
  · constructor
    · constructor
      · intro h
        apply hlarge
        have hcoord : large - small - -small = 0 := by simpa [sub] using h
        linarith
      · intro h
        apply hshared
        have hcoord : 0 - shared = 0 := by simpa [sub] using h
        linarith
    · refine ⟨cLarge, ?_⟩
      calc
        normSq
            (sub ({ x := large - small, y := 0 } : Point)
              ({ x := -small, y := shared } : Point))
            = sq large + sq shared := by
              simp [normSq, sub, sq]
        _ = cLarge * cLarge := hsecond

theorem certificateValid_axisSumOfSharedLeg
    {small large shared cSmall cLarge : Int}
    (hsmall : small ≠ 0) (hlarge : large ≠ 0) (hshared : shared ≠ 0)
    (hfirst : sq small + sq shared = cSmall * cSmall)
    (hsecond : sq large + sq shared = cLarge * cLarge) :
    certificateValid
      ({ x := small + large, y := 0 } : Point)
      ({ x := small, y := shared } : Point) := by
  constructor
  · constructor
    · exact ⟨hsmall, hshared⟩
    · exact ⟨cSmall, by simpa [normSq] using hfirst⟩
  · constructor
    · constructor
      · intro h
        apply hlarge
        have hcoord : small + large - small = 0 := by simpa [sub] using h
        linarith
      · intro h
        apply hshared
        have hcoord : 0 - shared = 0 := by simpa [sub] using h
        linarith
    · refine ⟨cLarge, ?_⟩
      calc
        normSq
            (sub ({ x := small + large, y := 0 } : Point)
              ({ x := small, y := shared } : Point))
            = sq large + sq shared := by
              simp [normSq, sub, sq]
        _ = cLarge * cLarge := hsecond

theorem normSq_gaussianMul (p q : Point) :
    normSq (gaussianMul p q) = normSq p * normSq q := by
  simp [normSq, gaussianMul, sq]
  ring

theorem sub_gaussianMul_right (p q multiplier : Point) :
    sub (gaussianMul p multiplier) (gaussianMul q multiplier) =
      gaussianMul (sub p q) multiplier := by
  ext <;> simp [sub, gaussianMul] <;> ring

theorem legalStep_gaussianMul {p multiplier : Point}
    (hp : legalStep p)
    (hm_square : isIntSquare (normSq multiplier))
    (h_nonAxis : nonAxis (gaussianMul p multiplier)) :
    legalStep (gaussianMul p multiplier) := by
  rcases hp with ⟨_hp_nonAxis, z, hz⟩
  rcases hm_square with ⟨w, hw⟩
  constructor
  · exact h_nonAxis
  · refine ⟨z * w, ?_⟩
    calc
      normSq (gaussianMul p multiplier) = normSq p * normSq multiplier :=
        normSq_gaussianMul p multiplier
      _ = (z * z) * (w * w) := by rw [hz, hw]
      _ = (z * w) * (z * w) := by ring

theorem certificateValid_gaussianMul {target midpoint multiplier : Point}
    (hcert : certificateValid target midpoint)
    (hm_square : isIntSquare (normSq multiplier))
    (hmidpoint_nonAxis : nonAxis (gaussianMul midpoint multiplier))
    (hsecond_nonAxis : nonAxis (gaussianMul (sub target midpoint) multiplier)) :
    certificateValid
      (gaussianMul target multiplier)
      (gaussianMul midpoint multiplier) := by
  rcases hcert with ⟨hmidpoint, hsecond⟩
  constructor
  · exact legalStep_gaussianMul hmidpoint hm_square hmidpoint_nonAxis
  · rw [sub_gaussianMul_right]
    exact legalStep_gaussianMul hsecond hm_square hsecond_nonAxis

theorem certificateValid_gaussianTransformData
    {target midpoint multiplier transformedTarget transformedMidpoint : Point}
    (htransformedTarget : transformedTarget = gaussianMul target multiplier)
    (htransformedMidpoint : transformedMidpoint = gaussianMul midpoint multiplier)
    (hcert : certificateValid target midpoint)
    (hm_square : isIntSquare (normSq multiplier))
    (hmidpoint_nonAxis : nonAxis (gaussianMul midpoint multiplier))
    (hsecond_nonAxis : nonAxis (gaussianMul (sub target midpoint) multiplier)) :
    certificateValid transformedTarget transformedMidpoint := by
  subst transformedTarget
  subst transformedMidpoint
  exact certificateValid_gaussianMul hcert hm_square
    hmidpoint_nonAxis hsecond_nonAxis

theorem gaussianMul_eq_of_quotient_components {target divisor quotient : Point}
    (hnorm : normSq divisor ≠ 0)
    (hreal : dot target divisor = quotient.x * normSq divisor)
    (himag : det divisor target = quotient.y * normSq divisor) :
    gaussianMul divisor quotient = target := by
  ext
  · change divisor.x * quotient.x - divisor.y * quotient.y = target.x
    apply mul_right_cancel₀ hnorm
    calc
      (divisor.x * quotient.x - divisor.y * quotient.y) * normSq divisor
          = dot target divisor * divisor.x - det divisor target * divisor.y := by
            rw [hreal, himag]
            ring
      _ = target.x * normSq divisor := by
            simp [dot, det, normSq, sq]
            ring
  · change divisor.x * quotient.y + divisor.y * quotient.x = target.y
    apply mul_right_cancel₀ hnorm
    calc
      (divisor.x * quotient.y + divisor.y * quotient.x) * normSq divisor
          = det divisor target * divisor.x + dot target divisor * divisor.y := by
            rw [hreal, himag]
            ring
      _ = target.y * normSq divisor := by
            simp [dot, det, normSq, sq]
            ring

theorem quotient_components_of_gaussianMul_eq {target divisor quotient : Point}
    (h : gaussianMul divisor quotient = target) :
    dot target divisor = quotient.x * normSq divisor ∧
      det divisor target = quotient.y * normSq divisor := by
  constructor
  · rw [← h]
    simp [dot, gaussianMul, normSq, sq]
    ring
  · rw [← h]
    simp [det, gaussianMul, normSq, sq]
    ring

theorem gaussianMul_eq_iff_quotient_components {target divisor quotient : Point}
    (hnorm : normSq divisor ≠ 0) :
    gaussianMul divisor quotient = target ↔
      dot target divisor = quotient.x * normSq divisor ∧
        det divisor target = quotient.y * normSq divisor := by
  constructor
  · exact quotient_components_of_gaussianMul_eq
  · intro hcomponents
    exact gaussianMul_eq_of_quotient_components hnorm hcomponents.1 hcomponents.2

theorem certificateValid_gaussianDivisor_of_quotient_components
    {target baseTarget midpoint quotient : Point}
    (hnorm : normSq baseTarget ≠ 0)
    (hreal : dot target baseTarget = quotient.x * normSq baseTarget)
    (himag : det baseTarget target = quotient.y * normSq baseTarget)
    (hcert : certificateValid baseTarget midpoint)
    (hquotient_square : isIntSquare (normSq quotient))
    (hmidpoint_nonAxis : nonAxis (gaussianMul midpoint quotient))
    (hsecond_nonAxis : nonAxis (gaussianMul (sub baseTarget midpoint) quotient)) :
    certificateValid target (gaussianMul midpoint quotient) := by
  rw [← gaussianMul_eq_of_quotient_components hnorm hreal himag]
  exact certificateValid_gaussianMul hcert hquotient_square
    hmidpoint_nonAxis hsecond_nonAxis

theorem diagonalBaseCertificateValid :
    certificateValid ({ x := 1, y := 1 } : Point) ({ x := 4, y := -3 } : Point) := by
  constructor
  · constructor
    · norm_num [nonAxis]
    · exact ⟨5, by norm_num [normSq, sq]⟩
  · constructor
    · norm_num [nonAxis, sub]
    · exact ⟨5, by norm_num [normSq, sub, sq]⟩

theorem certificateValid_diagonalGaussianMultiplier {multiplier : Point}
    (hm_square : isIntSquare (normSq multiplier))
    (hmidpoint_nonAxis :
      nonAxis (gaussianMul ({ x := 4, y := -3 } : Point) multiplier))
    (hsecond_nonAxis :
      nonAxis
        (gaussianMul
          (sub ({ x := 1, y := 1 } : Point) ({ x := 4, y := -3 } : Point))
          multiplier)) :
    certificateValid
      (gaussianMul ({ x := 1, y := 1 } : Point) multiplier)
      (gaussianMul ({ x := 4, y := -3 } : Point) multiplier) := by
  exact certificateValid_gaussianMul diagonalBaseCertificateValid hm_square
    hmidpoint_nonAxis hsecond_nonAxis

theorem certificateValid_diagonalGaussianRow {a b : Int}
    (hm_square : isIntSquare (a * a + b * b))
    (hmid_x : 4 * a + 3 * b ≠ 0)
    (hmid_y : 4 * b - 3 * a ≠ 0)
    (hsecond_x : -3 * a - 4 * b ≠ 0)
    (hsecond_y : -3 * b + 4 * a ≠ 0) :
    certificateValid
      ({ x := a - b, y := a + b } : Point)
      ({ x := 4 * a + 3 * b, y := 4 * b - 3 * a } : Point) := by
  let multiplier : Point := { x := a, y := b }
  have hm_norm : isIntSquare (normSq multiplier) := by
    simpa [multiplier, normSq, sq] using hm_square
  have hmidpoint_nonAxis :
      nonAxis (gaussianMul ({ x := 4, y := -3 } : Point) multiplier) := by
    constructor
    · simpa [multiplier, gaussianMul] using hmid_x
    · simpa [multiplier, gaussianMul] using hmid_y
  have hsecond_nonAxis :
      nonAxis
        (gaussianMul
          (sub ({ x := 1, y := 1 } : Point) ({ x := 4, y := -3 } : Point))
          multiplier) := by
    constructor
    · simpa [multiplier, gaussianMul, sub] using hsecond_x
    · simpa [multiplier, gaussianMul, sub] using hsecond_y
  convert
    (certificateValid_diagonalGaussianMultiplier (multiplier := multiplier)
      hm_norm hmidpoint_nonAxis hsecond_nonAxis)
    using 1 <;>
    ext <;>
    simp [multiplier, gaussianMul] <;>
    ring

theorem certificateValid_linearDeltaDirection
    {g h u v c d k : Int}
    (hu : u ≠ 0) (hv : v ≠ 0) (hk : k ≠ 0)
    (hleg : sq u + sq v = c * c)
    (hslice : sq g + sq h - d * d = 2 * k * (g * u + h * v - d * c))
    (hsecond_x : g - k * u ≠ 0)
    (hsecond_y : h - k * v ≠ 0) :
    certificateValid
      ({ x := g, y := h } : Point)
      ({ x := k * u, y := k * v } : Point) := by
  constructor
  · constructor
    · exact ⟨mul_ne_zero hk hu, mul_ne_zero hk hv⟩
    · refine ⟨k * c, ?_⟩
      calc
        normSq ({ x := k * u, y := k * v } : Point)
            = k * k * (sq u + sq v) := by
              simp [normSq, sq]
              ring
        _ = k * k * (c * c) := by rw [hleg]
        _ = (k * c) * (k * c) := by ring
  · constructor
    · constructor
      · simpa [sub] using hsecond_x
      · simpa [sub] using hsecond_y
    · refine ⟨k * c - d, ?_⟩
      calc
        normSq
            (sub ({ x := g, y := h } : Point) ({ x := k * u, y := k * v } : Point))
            = g * g + h * h - 2 * k * (g * u + h * v) + k * k * (c * c) := by
              have hleg' : u ^ 2 + v ^ 2 = c ^ 2 := by
                simpa [sq, pow_two] using hleg
              simp [normSq, sub, sq]
              ring_nf
              rw [← hleg']
              ring
        _ = (k * c - d) * (k * c - d) := by
              have hslice' :
                  g * g + h * h - d * d =
                    2 * k * (g * u + h * v - d * c) := by
                simpa [sq] using hslice
              ring_nf at hslice' ⊢
              nlinarith [hslice']

theorem certificateValid_theorem3Divisor
    {g h a b c sx sy q k : Int}
    (hsx : sx = 1 ∨ sx = -1) (hsy : sy = 1 ∨ sy = -1)
    (ha : a ≠ 0) (hb : b ≠ 0) (hk : k ≠ 0)
    (hleg : sq a + sq b = c * c)
    (hdiv : q * k = g * h)
    (hrel : (c - sx * a) * g = (c + sy * b) * h - q)
    (hsecond_x : g - sx * a * k ≠ 0)
    (hsecond_y : h - sy * b * k ≠ 0) :
    certificateValid
      ({ x := g, y := h } : Point)
      ({ x := sx * a * k, y := sy * b * k } : Point) := by
  have hsx_nonzero : sx ≠ 0 := sign_ne_zero_of_pm_one hsx
  have hsy_nonzero : sy ≠ 0 := sign_ne_zero_of_pm_one hsy
  have hsx_sq : sx * sx = 1 := sign_sq_of_pm_one hsx
  have hsy_sq : sy * sy = 1 := sign_sq_of_pm_one hsy
  have hsx_pow : sx ^ 2 = 1 := by simpa [pow_two] using hsx_sq
  have hsy_pow : sy ^ 2 = 1 := by simpa [pow_two] using hsy_sq
  have hdot : sx * a * g + sy * b * h = c * (g - h) + q := by
    ring_nf at hrel ⊢
    linarith
  have hkq : k * q = g * h := by
    simpa [mul_comm] using hdiv
  constructor
  · constructor
    · exact
        ⟨mul_ne_zero (mul_ne_zero hsx_nonzero ha) hk,
          mul_ne_zero (mul_ne_zero hsy_nonzero hb) hk⟩
    · refine ⟨c * k, ?_⟩
      calc
        normSq ({ x := sx * a * k, y := sy * b * k } : Point)
            = k * k * (sq a + sq b) := by
              simp [normSq, sq]
              ring_nf
              rw [hsx_pow, hsy_pow]
              ring
        _ = k * k * (c * c) := by rw [hleg]
        _ = (c * k) * (c * k) := by ring
  · constructor
    · constructor
      · simpa [sub] using hsecond_x
      · simpa [sub] using hsecond_y
    · refine ⟨c * k - (g - h), ?_⟩
      calc
        normSq
            (sub ({ x := g, y := h } : Point)
              ({ x := sx * a * k, y := sy * b * k } : Point))
            =
              g * g + h * h -
                2 * k * (sx * a * g + sy * b * h) +
                k * k * (c * c) := by
              have hleg' : a ^ 2 + b ^ 2 = c ^ 2 := by
                simpa [sq, pow_two] using hleg
              simp [normSq, sub, sq]
              ring_nf
              rw [hsx_pow, hsy_pow]
              rw [← hleg']
              ring
        _ =
              g * g + h * h -
                2 * k * (c * (g - h) + q) +
                k * k * (c * c) := by rw [hdot]
        _ = (c * k - (g - h)) * (c * k - (g - h)) := by
              ring_nf
              nlinarith [hkq]

theorem certificateValid_theorem3UnitDivisorProgression
    {a b c sx sy p0 q0 t m pRay qRay : Int}
    (hsx : sx = 1 ∨ sx = -1) (hsy : sy = 1 ∨ sy = -1)
    (ha : a ≠ 0) (hb : b ≠ 0) (hm : m ≠ 0)
    (hpRay : pRay ≠ 0) (hqRay : qRay ≠ 0)
    (hleg : sq a + sq b = c * c)
    (hp : pRay = p0 + (c + sy * b) * t)
    (hq : qRay = q0 + (c - sx * a) * t)
    (hbase : (c + sy * b) * q0 - (c - sx * a) * p0 = 1)
    (hsecond_x : pRay * m - sx * a * (pRay * qRay * m) ≠ 0)
    (hsecond_y : qRay * m - sy * b * (pRay * qRay * m) ≠ 0) :
    certificateValid
      ({ x := pRay * m, y := qRay * m } : Point)
      ({ x := sx * a * (pRay * qRay * m),
          y := sy * b * (pRay * qRay * m) } : Point) := by
  have hk : pRay * qRay * m ≠ 0 :=
    mul_ne_zero (mul_ne_zero hpRay hqRay) hm
  have hunit : (c + sy * b) * qRay - (c - sx * a) * pRay = 1 := by
    rw [hp, hq]
    calc
      (c + sy * b) * (q0 + (c - sx * a) * t) -
          (c - sx * a) * (p0 + (c + sy * b) * t)
          = (c + sy * b) * q0 - (c - sx * a) * p0 := by ring
      _ = 1 := hbase
  have hdiv : m * (pRay * qRay * m) = (pRay * m) * (qRay * m) := by ring
  have hrel :
      (c - sx * a) * (pRay * m) =
        (c + sy * b) * (qRay * m) - m := by
    have hmul : ((c + sy * b) * qRay - (c - sx * a) * pRay) * m = 1 * m := by
      rw [hunit]
    ring_nf at hmul ⊢
    linarith
  exact certificateValid_theorem3Divisor hsx hsy ha hb hk hleg hdiv hrel
    hsecond_x hsecond_y

theorem certificateValid_theorem3Unit
    {g h a b c sx sy : Int}
    (hsx : sx = 1 ∨ sx = -1) (hsy : sy = 1 ∨ sy = -1)
    (ha : a ≠ 0) (hb : b ≠ 0) (hg : g ≠ 0) (hh : h ≠ 0)
    (hleg : sq a + sq b = c * c)
    (hrel : (c - sx * a) * g = (c + sy * b) * h - 1)
    (hsecond_x : g - sx * a * (g * h) ≠ 0)
    (hsecond_y : h - sy * b * (g * h) ≠ 0) :
    certificateValid
      ({ x := g, y := h } : Point)
      ({ x := sx * a * (g * h), y := sy * b * (g * h) } : Point) := by
  exact certificateValid_theorem3Divisor hsx hsy ha hb (mul_ne_zero hg hh)
    hleg (by ring) hrel hsecond_x hsecond_y

theorem certificateValid_twoOneRayMultipleOfThreeBase :
    certificateValid ({ x := 6, y := 3 } : Point) ({ x := 12, y := -5 } : Point) := by
  constructor
  · constructor
    · constructor <;> norm_num
    · exact ⟨13, by norm_num [normSq, sq]⟩
  · constructor
    · constructor <;> norm_num [sub]
    · exact ⟨10, by norm_num [normSq, sub, sq]⟩

theorem certificateValid_twoOneRayMultipleOfThree {m : Int} (hm : m ≠ 0) :
    certificateValid
      ({ x := 6 * m, y := 3 * m } : Point)
      ({ x := 12 * m, y := -5 * m } : Point) := by
  have hscaled := certificateValid_smul (target := ({ x := 6, y := 3 } : Point))
    (midpoint := ({ x := 12, y := -5 } : Point)) hm
    certificateValid_twoOneRayMultipleOfThreeBase
  simpa [smul, mul_comm, mul_left_comm, mul_assoc] using hscaled

theorem certificateValid_oneThreeRayTheorem3Base :
    certificateValid ({ x := 1, y := 3 } : Point) ({ x := 9, y := -12 } : Point) := by
  constructor
  · constructor
    · constructor <;> norm_num
    · exact ⟨15, by norm_num [normSq, sq]⟩
  · constructor
    · constructor <;> norm_num [sub]
    · exact ⟨17, by norm_num [normSq, sub, sq]⟩

theorem certificateValid_oneThreeRayTheorem3 {m : Int} (hm : m ≠ 0) :
    certificateValid
      ({ x := m, y := 3 * m } : Point)
      ({ x := 9 * m, y := -12 * m } : Point) := by
  have hscaled := certificateValid_smul (target := ({ x := 1, y := 3 } : Point))
    (midpoint := ({ x := 9, y := -12 } : Point)) hm
    certificateValid_oneThreeRayTheorem3Base
  simpa [smul, mul_comm, mul_left_comm, mul_assoc] using hscaled

theorem certificateValid_threeFourFiveOddSlopeRay {p m : Int}
    (hp : 0 < p) (hm : m ≠ 0) :
    certificateValid
      ({ x := p * m, y := (2 * p + 1) * m } : Point)
      ({ x := 3 * (p * (2 * p + 1) * m),
          y := -4 * (p * (2 * p + 1) * m) } : Point) := by
  let k : Int := p * (2 * p + 1) * m
  have hp_ne : p ≠ 0 := by omega
  have htwo_ne : 2 * p + 1 ≠ 0 := by omega
  have hthree_ne : 3 * p + 1 ≠ 0 := by omega
  have hfour_ne : 4 * p + 1 ≠ 0 := by omega
  have hk : k ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero hp_ne htwo_ne) hm
  have hsecond_x : p * m - 1 * 3 * k ≠ 0 := by
    have hfactor : -2 * p * (3 * p + 1) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hp_ne) hthree_ne) hm
    intro hx
    apply hfactor
    calc
      -2 * p * (3 * p + 1) * m = p * m - 1 * 3 * k := by
        simp [k]
        ring
      _ = 0 := hx
  have hsecond_y : (2 * p + 1) * m - (-1) * 4 * k ≠ 0 := by
    have hfactor : (2 * p + 1) * (4 * p + 1) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero htwo_ne hfour_ne) hm
    intro hy
    apply hfactor
    calc
      (2 * p + 1) * (4 * p + 1) * m =
          (2 * p + 1) * m - (-1) * 4 * k := by
        simp [k]
        ring
      _ = 0 := hy
  have hcert := certificateValid_theorem3Divisor
    (g := p * m) (h := (2 * p + 1) * m)
    (a := 3) (b := 4) (c := 5)
    (sx := 1) (sy := -1) (q := m) (k := k)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) hk
    (by norm_num [sq])
    (by
      simp [k]
      ring)
    (by ring)
    hsecond_x hsecond_y
  simpa [k, mul_comm, mul_left_comm, mul_assoc] using hcert

theorem certificateValid_threeFourFiveSteepOddSlopeRay {p m : Int}
    (hp : 0 < p) (hm : m ≠ 0) :
    certificateValid
      ({ x := p * m, y := (8 * p + 1) * m } : Point)
      ({ x := -3 * (p * (8 * p + 1) * m),
          y := -4 * (p * (8 * p + 1) * m) } : Point) := by
  let k : Int := p * (8 * p + 1) * m
  have hp_ne : p ≠ 0 := by omega
  have hq_ne : 8 * p + 1 ≠ 0 := by omega
  have hsix_ne : 6 * p + 1 ≠ 0 := by omega
  have hfour_ne : 4 * p + 1 ≠ 0 := by omega
  have hk : k ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero hp_ne hq_ne) hm
  have hsecond_x : p * m - (-1) * 3 * k ≠ 0 := by
    have hfactor : 4 * p * (6 * p + 1) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hp_ne) hsix_ne) hm
    intro hx
    apply hfactor
    calc
      4 * p * (6 * p + 1) * m = p * m - (-1) * 3 * k := by
        simp [k]
        ring
      _ = 0 := hx
  have hsecond_y : (8 * p + 1) * m - (-1) * 4 * k ≠ 0 := by
    have hfactor : (8 * p + 1) * (4 * p + 1) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero hq_ne hfour_ne) hm
    intro hy
    apply hfactor
    calc
      (8 * p + 1) * (4 * p + 1) * m =
          (8 * p + 1) * m - (-1) * 4 * k := by
        simp [k]
        ring
      _ = 0 := hy
  have hcert := certificateValid_theorem3Divisor
    (g := p * m) (h := (8 * p + 1) * m)
    (a := 3) (b := 4) (c := 5)
    (sx := -1) (sy := -1) (q := m) (k := k)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) hk
    (by norm_num [sq])
    (by
      simp [k]
      ring)
    (by ring)
    hsecond_x hsecond_y
  simpa [k, mul_comm, mul_left_comm, mul_assoc] using hcert

theorem certificateValid_threeFourFiveWideOddSlopeRay {t m : Int}
    (ht : 0 ≤ t) (hm : m ≠ 0) :
    certificateValid
      ({ x := (9 * t + 4) * m, y := (2 * t + 1) * m } : Point)
      ({ x := 3 * ((9 * t + 4) * (2 * t + 1) * m),
          y := 4 * ((9 * t + 4) * (2 * t + 1) * m) } : Point) := by
  let p : Int := 9 * t + 4
  let q : Int := 2 * t + 1
  let k : Int := p * q * m
  have hp_pos : 0 < p := by
    dsimp [p]
    omega
  have hq_pos : 0 < q := by
    dsimp [q]
    omega
  have hthree_pos : 0 < 3 * t + 1 := by omega
  have htwelve_pos : 0 < 12 * t + 5 := by omega
  have hp_ne : p ≠ 0 := ne_of_gt hp_pos
  have hq_ne : q ≠ 0 := ne_of_gt hq_pos
  have hthree_ne : 3 * t + 1 ≠ 0 := ne_of_gt hthree_pos
  have htwelve_ne : 12 * t + 5 ≠ 0 := ne_of_gt htwelve_pos
  have hk : k ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero hp_ne hq_ne) hm
  have hsecond_x : p * m - 1 * 3 * k ≠ 0 := by
    have hfactor : -2 * p * (3 * t + 1) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hp_ne) hthree_ne) hm
    intro hx
    apply hfactor
    calc
      -2 * p * (3 * t + 1) * m = p * m - 1 * 3 * k := by
        simp [p, q, k]
        ring
      _ = 0 := hx
  have hsecond_y : q * m - 1 * 4 * k ≠ 0 := by
    have hfactor : -3 * q * (12 * t + 5) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hq_ne) htwelve_ne) hm
    intro hy
    apply hfactor
    calc
      -3 * q * (12 * t + 5) * m = q * m - 1 * 4 * k := by
        simp [p, q, k]
        ring
      _ = 0 := hy
  have hcert := certificateValid_theorem3Divisor
    (g := p * m) (h := q * m)
    (a := 3) (b := 4) (c := 5)
    (sx := 1) (sy := 1) (q := m) (k := k)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) hk
    (by norm_num [sq])
    (by
      simp [p, q, k]
      ring)
    (by ring)
    hsecond_x hsecond_y
  simpa [p, q, k, mul_comm, mul_left_comm, mul_assoc] using hcert

theorem certificateValid_threeFourFiveNearDiagonalRay {t m : Int}
    (ht : 0 ≤ t) (hm : m ≠ 0) :
    certificateValid
      ({ x := (9 * t + 1) * m, y := (8 * t + 1) * m } : Point)
      ({ x := -3 * ((9 * t + 1) * (8 * t + 1) * m),
          y := 4 * ((9 * t + 1) * (8 * t + 1) * m) } : Point) := by
  let p : Int := 9 * t + 1
  let q : Int := 8 * t + 1
  let k : Int := p * q * m
  have hp_pos : 0 < p := by
    dsimp [p]
    omega
  have hq_pos : 0 < q := by
    dsimp [q]
    omega
  have hsix_pos : 0 < 6 * t + 1 := by omega
  have htwelve_pos : 0 < 12 * t + 1 := by omega
  have hp_ne : p ≠ 0 := ne_of_gt hp_pos
  have hq_ne : q ≠ 0 := ne_of_gt hq_pos
  have hsix_ne : 6 * t + 1 ≠ 0 := ne_of_gt hsix_pos
  have htwelve_ne : 12 * t + 1 ≠ 0 := ne_of_gt htwelve_pos
  have hk : k ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero hp_ne hq_ne) hm
  have hsecond_x : p * m - (-1) * 3 * k ≠ 0 := by
    have hfactor : 4 * p * (6 * t + 1) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hp_ne) hsix_ne) hm
    intro hx
    apply hfactor
    calc
      4 * p * (6 * t + 1) * m = p * m - (-1) * 3 * k := by
        simp [p, q, k]
        ring
      _ = 0 := hx
  have hsecond_y : q * m - 1 * 4 * k ≠ 0 := by
    have hfactor : -3 * q * (12 * t + 1) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hq_ne) htwelve_ne) hm
    intro hy
    apply hfactor
    calc
      -3 * q * (12 * t + 1) * m = q * m - 1 * 4 * k := by
        simp [p, q, k]
        ring
      _ = 0 := hy
  have hcert := certificateValid_theorem3Divisor
    (g := p * m) (h := q * m)
    (a := 3) (b := 4) (c := 5)
    (sx := -1) (sy := 1) (q := m) (k := k)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) hk
    (by norm_num [sq])
    (by
      simp [p, q, k]
      ring)
    (by ring)
    hsecond_x hsecond_y
  simpa [p, q, k, mul_comm, mul_left_comm, mul_assoc] using hcert

theorem certificateValid_fiveTwelveThirteenEightSlopeRay {p m : Int}
    (hp : 0 < p) (hm : m ≠ 0) :
    certificateValid
      ({ x := p * m, y := (8 * p + 1) * m } : Point)
      ({ x := 5 * (p * (8 * p + 1) * m),
          y := -12 * (p * (8 * p + 1) * m) } : Point) := by
  let k : Int := p * (8 * p + 1) * m
  have hp_ne : p ≠ 0 := by omega
  have hq_ne : 8 * p + 1 ≠ 0 := by omega
  have hten_ne : 10 * p + 1 ≠ 0 := by omega
  have htwelve_ne : 12 * p + 1 ≠ 0 := by omega
  have hk : k ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero hp_ne hq_ne) hm
  have hsecond_x : p * m - 1 * 5 * k ≠ 0 := by
    have hfactor : -4 * p * (10 * p + 1) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hp_ne) hten_ne) hm
    intro hx
    apply hfactor
    calc
      -4 * p * (10 * p + 1) * m = p * m - 1 * 5 * k := by
        simp [k]
        ring
      _ = 0 := hx
  have hsecond_y : (8 * p + 1) * m - (-1) * 12 * k ≠ 0 := by
    have hfactor : (8 * p + 1) * (12 * p + 1) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero hq_ne htwelve_ne) hm
    intro hy
    apply hfactor
    calc
      (8 * p + 1) * (12 * p + 1) * m =
          (8 * p + 1) * m - (-1) * 12 * k := by
        simp [k]
        ring
      _ = 0 := hy
  have hcert := certificateValid_theorem3Divisor
    (g := p * m) (h := (8 * p + 1) * m)
    (a := 5) (b := 12) (c := 13)
    (sx := 1) (sy := -1) (q := m) (k := k)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) hk
    (by norm_num [sq])
    (by
      simp [k]
      ring)
    (by ring)
    hsecond_x hsecond_y
  simpa [k, mul_comm, mul_left_comm, mul_assoc] using hcert

theorem certificateValid_fiveTwelveThirteenEighteenSlopeRay {p m : Int}
    (hp : 0 < p) (hm : m ≠ 0) :
    certificateValid
      ({ x := p * m, y := (18 * p + 1) * m } : Point)
      ({ x := -5 * (p * (18 * p + 1) * m),
          y := -12 * (p * (18 * p + 1) * m) } : Point) := by
  let k : Int := p * (18 * p + 1) * m
  have hp_ne : p ≠ 0 := by omega
  have hq_ne : 18 * p + 1 ≠ 0 := by omega
  have hfifteen_ne : 15 * p + 1 ≠ 0 := by omega
  have htwelve_ne : 12 * p + 1 ≠ 0 := by omega
  have hk : k ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero hp_ne hq_ne) hm
  have hsecond_x : p * m - (-1) * 5 * k ≠ 0 := by
    have hfactor : 6 * p * (15 * p + 1) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hp_ne) hfifteen_ne) hm
    intro hx
    apply hfactor
    calc
      6 * p * (15 * p + 1) * m = p * m - (-1) * 5 * k := by
        simp [k]
        ring
      _ = 0 := hx
  have hsecond_y : (18 * p + 1) * m - (-1) * 12 * k ≠ 0 := by
    have hfactor : (18 * p + 1) * (12 * p + 1) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero hq_ne htwelve_ne) hm
    intro hy
    apply hfactor
    calc
      (18 * p + 1) * (12 * p + 1) * m =
          (18 * p + 1) * m - (-1) * 12 * k := by
        simp [k]
        ring
      _ = 0 := hy
  have hcert := certificateValid_theorem3Divisor
    (g := p * m) (h := (18 * p + 1) * m)
    (a := 5) (b := 12) (c := 13)
    (sx := -1) (sy := -1) (q := m) (k := k)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) hk
    (by norm_num [sq])
    (by
      simp [k]
      ring)
    (by ring)
    hsecond_x hsecond_y
  simpa [k, mul_comm, mul_left_comm, mul_assoc] using hcert

theorem certificateValid_fiveTwelveThirteenTwentyFiveEightRay {t m : Int}
    (ht : 0 ≤ t) (hm : m ≠ 0) :
    certificateValid
      ({ x := (25 * t + 3) * m, y := (8 * t + 1) * m } : Point)
      ({ x := 5 * ((25 * t + 3) * (8 * t + 1) * m),
          y := 12 * ((25 * t + 3) * (8 * t + 1) * m) } : Point) := by
  let p : Int := 25 * t + 3
  let q : Int := 8 * t + 1
  let k : Int := p * q * m
  have hp_pos : 0 < p := by
    dsimp [p]
    omega
  have hq_pos : 0 < q := by
    dsimp [q]
    omega
  have hten_pos : 0 < 10 * t + 1 := by omega
  have hsixty_pos : 0 < 60 * t + 7 := by omega
  have hp_ne : p ≠ 0 := ne_of_gt hp_pos
  have hq_ne : q ≠ 0 := ne_of_gt hq_pos
  have hten_ne : 10 * t + 1 ≠ 0 := ne_of_gt hten_pos
  have hsixty_ne : 60 * t + 7 ≠ 0 := ne_of_gt hsixty_pos
  have hk : k ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero hp_ne hq_ne) hm
  have hsecond_x : p * m - 1 * 5 * k ≠ 0 := by
    have hfactor : -4 * p * (10 * t + 1) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hp_ne) hten_ne) hm
    intro hx
    apply hfactor
    calc
      -4 * p * (10 * t + 1) * m = p * m - 1 * 5 * k := by
        simp [p, q, k]
        ring
      _ = 0 := hx
  have hsecond_y : q * m - 1 * 12 * k ≠ 0 := by
    have hfactor : -5 * q * (60 * t + 7) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hq_ne) hsixty_ne) hm
    intro hy
    apply hfactor
    calc
      -5 * q * (60 * t + 7) * m = q * m - 1 * 12 * k := by
        simp [p, q, k]
        ring
      _ = 0 := hy
  have hcert := certificateValid_theorem3Divisor
    (g := p * m) (h := q * m)
    (a := 5) (b := 12) (c := 13)
    (sx := 1) (sy := 1) (q := m) (k := k)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) hk
    (by norm_num [sq])
    (by
      simp [p, q, k]
      ring)
    (by ring)
    hsecond_x hsecond_y
  simpa [p, q, k, mul_comm, mul_left_comm, mul_assoc] using hcert

theorem certificateValid_fiveTwelveThirteenTwentyFiveEighteenRay {t m : Int}
    (ht : 0 ≤ t) (hm : m ≠ 0) :
    certificateValid
      ({ x := (25 * t + 18) * m, y := (18 * t + 13) * m } : Point)
      ({ x := -5 * ((25 * t + 18) * (18 * t + 13) * m),
          y := 12 * ((25 * t + 18) * (18 * t + 13) * m) } : Point) := by
  let p : Int := 25 * t + 18
  let q : Int := 18 * t + 13
  let k : Int := p * q * m
  have hp_pos : 0 < p := by
    dsimp [p]
    omega
  have hq_pos : 0 < q := by
    dsimp [q]
    omega
  have hfifteen_pos : 0 < 15 * t + 11 := by omega
  have hsixty_pos : 0 < 60 * t + 43 := by omega
  have hp_ne : p ≠ 0 := ne_of_gt hp_pos
  have hq_ne : q ≠ 0 := ne_of_gt hq_pos
  have hfifteen_ne : 15 * t + 11 ≠ 0 := ne_of_gt hfifteen_pos
  have hsixty_ne : 60 * t + 43 ≠ 0 := ne_of_gt hsixty_pos
  have hk : k ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero hp_ne hq_ne) hm
  have hsecond_x : p * m - (-1) * 5 * k ≠ 0 := by
    have hfactor : 6 * p * (15 * t + 11) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hp_ne) hfifteen_ne) hm
    intro hx
    apply hfactor
    calc
      6 * p * (15 * t + 11) * m = p * m - (-1) * 5 * k := by
        simp [p, q, k]
        ring
      _ = 0 := hx
  have hsecond_y : q * m - 1 * 12 * k ≠ 0 := by
    have hfactor : -5 * q * (60 * t + 43) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hq_ne) hsixty_ne) hm
    intro hy
    apply hfactor
    calc
      -5 * q * (60 * t + 43) * m = q * m - 1 * 12 * k := by
        simp [p, q, k]
        ring
      _ = 0 := hy
  have hcert := certificateValid_theorem3Divisor
    (g := p * m) (h := q * m)
    (a := 5) (b := 12) (c := 13)
    (sx := -1) (sy := 1) (q := m) (k := k)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) hk
    (by norm_num [sq])
    (by
      simp [p, q, k]
      ring)
    (by ring)
    hsecond_x hsecond_y
  simpa [p, q, k, mul_comm, mul_left_comm, mul_assoc] using hcert

theorem certificateValid_consecutiveEuclidUnitDivisorRay {r p m : Int}
    (hr : 0 < r) (hp : 0 < p) (hm : m ≠ 0) :
    certificateValid
      ({ x := p * m, y := (2 * r * r * p + 1) * m } : Point)
      ({ x := (2 * r + 1) * (p * (2 * r * r * p + 1) * m),
          y := -(2 * r * (r + 1)) * (p * (2 * r * r * p + 1) * m) } :
        Point) := by
  let a : Int := 2 * r + 1
  let b : Int := 2 * r * (r + 1)
  let c : Int := 2 * r * r + 2 * r + 1
  let qRay : Int := 2 * r * r * p + 1
  let k : Int := p * qRay * m
  have ha_pos : 0 < a := by
    dsimp [a]
    omega
  have hb_pos : 0 < b := by
    dsimp [b]
    nlinarith [hr, sq_nonneg r]
  have hcoef_pos : 0 < 2 * r * r := by
    nlinarith [hr, sq_nonneg r]
  have hq_pos : 0 < qRay := by
    dsimp [qRay]
    have hprod_pos : 0 < (2 * r * r) * p := mul_pos hcoef_pos hp
    nlinarith
  have hten_pos : 0 < a * qRay - 1 := by
    have ha_ge : 1 ≤ a := by omega
    have hq_ge : 1 ≤ qRay := by omega
    nlinarith [mul_pos ha_pos hq_pos]
  have honebp_pos : 0 < 1 + b * p := by
    have hprod_pos : 0 < b * p := mul_pos hb_pos hp
    nlinarith
  have ha_ne : a ≠ 0 := ne_of_gt ha_pos
  have hb_ne : b ≠ 0 := ne_of_gt hb_pos
  have hp_ne : p ≠ 0 := ne_of_gt hp
  have hq_ne : qRay ≠ 0 := ne_of_gt hq_pos
  have hten_ne : a * qRay - 1 ≠ 0 := ne_of_gt hten_pos
  have honebp_ne : 1 + b * p ≠ 0 := ne_of_gt honebp_pos
  have hk : k ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero hp_ne hq_ne) hm
  have hsecond_x : p * m - 1 * a * k ≠ 0 := by
    have hfactor : -p * (a * qRay - 1) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (neg_ne_zero.mpr hp_ne) hten_ne) hm
    intro hx
    apply hfactor
    calc
      -p * (a * qRay - 1) * m = p * m - 1 * a * k := by
        simp [k]
        ring
      _ = 0 := hx
  have hsecond_y : qRay * m - (-1) * b * k ≠ 0 := by
    have hfactor : qRay * (1 + b * p) * m ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero hq_ne honebp_ne) hm
    intro hy
    apply hfactor
    calc
      qRay * (1 + b * p) * m = qRay * m - (-1) * b * k := by
        simp [k]
        ring
      _ = 0 := hy
  have hcert := certificateValid_theorem3Divisor
    (g := p * m) (h := qRay * m)
    (a := a) (b := b) (c := c)
    (sx := 1) (sy := -1) (q := m) (k := k)
    (by norm_num) (by norm_num) ha_ne hb_ne hk
    (by
      simp [a, b, c, sq]
      ring)
    (by
      simp [k, qRay]
      ring)
    (by
      simp [a, b, c, qRay]
      ring)
    hsecond_x hsecond_y
  simpa [a, b, c, qRay, k, mul_comm, mul_left_comm, mul_assoc] using hcert

theorem certificateValid_consecutiveEuclidAffineStrip {r h : Int}
    (hr : 0 < r) (hh : 0 < h) :
    certificateValid
      ({ x := 2 * r * r * h - 1, y := h } : Point)
      ({ x := (2 * r * (r + 1)) * ((2 * r * r * h - 1) * h),
          y := -(2 * r + 1) * ((2 * r * r * h - 1) * h) } : Point) := by
  let a : Int := 2 * r * (r + 1)
  let b : Int := 2 * r + 1
  let c : Int := 2 * r * r + 2 * r + 1
  let g : Int := 2 * r * r * h - 1
  have ha_pos : 0 < a := by
    dsimp [a]
    nlinarith [hr, sq_nonneg r]
  have hb_pos : 0 < b := by
    dsimp [b]
    omega
  have hg_pos : 0 < g := by
    dsimp [g]
    nlinarith [hr, hh, sq_nonneg r]
  have hah_gt_one : 1 < a * h := by
    have hprod_pos : 0 < a * h := mul_pos ha_pos hh
    have ha_even : 2 ≤ a := by
      dsimp [a]
      nlinarith [hr, sq_nonneg r]
    nlinarith
  have hbg_pos : 0 < b * g := mul_pos hb_pos hg_pos
  have ha_ne : a ≠ 0 := ne_of_gt ha_pos
  have hb_ne : b ≠ 0 := ne_of_gt hb_pos
  have hg_ne : g ≠ 0 := ne_of_gt hg_pos
  have hh_ne : h ≠ 0 := ne_of_gt hh
  have hone_minus_ne : 1 - a * h ≠ 0 := by omega
  have hone_plus_ne : 1 + b * g ≠ 0 := by
    have hpos : 0 < 1 + b * g := by nlinarith
    exact ne_of_gt hpos
  have hsecond_x : g - 1 * a * (g * h) ≠ 0 := by
    have hfactor : g * (1 - a * h) ≠ 0 :=
      mul_ne_zero hg_ne hone_minus_ne
    intro hx
    apply hfactor
    calc
      g * (1 - a * h) = g - 1 * a * (g * h) := by ring
      _ = 0 := hx
  have hsecond_y : h - (-1) * b * (g * h) ≠ 0 := by
    have hfactor : h * (1 + b * g) ≠ 0 :=
      mul_ne_zero hh_ne hone_plus_ne
    intro hy
    apply hfactor
    calc
      h * (1 + b * g) = h - (-1) * b * (g * h) := by ring
      _ = 0 := hy
  have hcert := certificateValid_theorem3Unit
    (g := g) (h := h)
    (a := a) (b := b) (c := c)
    (sx := 1) (sy := -1)
    (by norm_num) (by norm_num) ha_ne hb_ne hg_ne hh_ne
    (by
      simp [a, b, c, sq]
      ring)
    (by
      simp [a, b, c, g]
      ring)
    hsecond_x hsecond_y
  simpa [a, b, c, g, mul_comm, mul_left_comm, mul_assoc] using hcert

theorem certificateValid_affineConsecutiveHypotenuseStrip {m q t ell : Int}
    (hm : 2 ≤ m) (ht : t ≠ 0)
    (hdiv : q * (1 - q) = (2 * m * (m - 1)) * ell)
    (hrcoef : ell + (2 * m - 1) * q * t -
        2 * (m * (m - 1) * t) * (m * (m - 1) * t) ≠ 0)
    (hB : (2 * m - 1) * (m * (m - 1) * t) - q ≠ 0)
    (hdiff : ((2 * m - 1) * (m * (m - 1) * t) - q) *
          ((2 * m - 1) * (m * (m - 1) * t) - q) -
        (m * (m - 1) * t) * (m * (m - 1) * t) ≠ 0) :
    certificateValid
      ({ x := (m * m + (m - 1) * (m - 1)) * q * t + (2 * m - 1) * ell,
          y := q } : Point)
      ({ x := (2 * m - 1) *
            (ell + (2 * m - 1) * q * t -
              2 * (m * (m - 1) * t) * (m * (m - 1) * t)),
          y := (2 * m * (m - 1)) *
            (ell + (2 * m - 1) * q * t -
              2 * (m * (m - 1) * t) * (m * (m - 1) * t)) } : Point) := by
  let u : Int := 2 * m - 1
  let v : Int := 2 * m * (m - 1)
  let c : Int := m * m + (m - 1) * (m - 1)
  let A : Int := m * (m - 1) * t
  let B : Int := u * A - q
  let r : Int := ell + u * q * t - 2 * A * A
  have hm_pos : 0 < m := by omega
  have hm1_pos : 0 < m - 1 := by omega
  have hu_pos : 0 < u := by
    dsimp [u]
    omega
  have hv_pos : 0 < v := by
    dsimp [v]
    nlinarith [hm_pos, hm1_pos]
  have hm_ne : m ≠ 0 := ne_of_gt hm_pos
  have hm1_ne : m - 1 ≠ 0 := ne_of_gt hm1_pos
  have hA_ne : A ≠ 0 := by
    dsimp [A]
    exact mul_ne_zero (mul_ne_zero hm_ne hm1_ne) ht
  have hr_ne : r ≠ 0 := by
    simpa [u, A, r] using hrcoef
  have hB_ne : B ≠ 0 := by
    simpa [u, A, B] using hB
  have hdiff_ne : B * B - A * A ≠ 0 := by
    simpa [u, A, B] using hdiff
  have hU : legalStep ({ x := u, y := v } : Point) := by
    constructor
    · exact ⟨ne_of_gt hu_pos, ne_of_gt hv_pos⟩
    · refine ⟨c, ?_⟩
      simp [normSq, u, v, c, sq]
      ring
  have hV : legalStep ({ x := 2 * A * B, y := B * B - A * A } : Point) := by
    constructor
    · constructor
      · exact mul_ne_zero (mul_ne_zero (by norm_num) hA_ne) hB_ne
      · exact hdiff_ne
    · refine ⟨A * A + B * B, ?_⟩
      simp [normSq, sq]
      ring
  have hsecond :
      sub
        ({ x := c * q * t + u * ell, y := q } : Point)
        ({ x := u * r, y := v * r } : Point) =
      ({ x := 2 * A * B, y := B * B - A * A } : Point) := by
    ext
    · simp [sub, u, v, c, A, B, r]
      ring
    · simp [sub]
      dsimp [u, v, c, A, B, r]
      ring_nf at hdiv ⊢
      nlinarith [hdiv]
  have hmid : legalStep ({ x := u * r, y := v * r } : Point) := by
    simpa [smul, mul_comm] using legalStep_smul hr_ne hU
  constructor
  · simpa [u, v, A, r, mul_comm, mul_left_comm, mul_assoc] using hmid
  · rw [show sub
        ({ x := (m * m + (m - 1) * (m - 1)) * q * t + (2 * m - 1) * ell,
            y := q } : Point)
        ({ x := (2 * m - 1) *
              (ell + (2 * m - 1) * q * t -
                2 * (m * (m - 1) * t) * (m * (m - 1) * t)),
            y := (2 * m * (m - 1)) *
              (ell + (2 * m - 1) * q * t -
                2 * (m * (m - 1) * t) * (m * (m - 1) * t)) } : Point) =
        ({ x := 2 * A * B, y := B * B - A * A } : Point) by
          simpa [u, v, c, A, r, mul_comm, mul_left_comm, mul_assoc] using hsecond]
    exact hV

theorem certificateValid_consecutiveHypotenuseUnitCoordinate {m t : Int}
    (hm : 2 ≤ m) (ht : t ≠ 0) :
    certificateValid
      ({ x := (m * m + (m - 1) * (m - 1)) * t, y := 1 } : Point)
      ({ x := (2 * m - 1) *
            ((2 * m - 1) * t -
              2 * (m * (m - 1) * t) * (m * (m - 1) * t)),
          y := (2 * m * (m - 1)) *
            ((2 * m - 1) * t -
              2 * (m * (m - 1) * t) * (m * (m - 1) * t)) } : Point) := by
  let K : Int := m * (m - 1)
  have hK_ge : 2 ≤ K := by
    dsimp [K]
    nlinarith [sq_nonneg (m - 1)]
  have hcoeff_ne : ∀ C : Int, 2 ≤ C → C * t - 1 ≠ 0 := by
    intro C hC
    rcases lt_or_gt_of_ne ht with ht_neg | ht_pos
    · have hneg : C * t - 1 < 0 := by nlinarith [hC, ht_neg]
      exact ne_of_lt hneg
    · have hpos : 0 < C * t - 1 := by
        have ht_ge : 1 ≤ t := by omega
        nlinarith [hC, ht_ge]
      exact ne_of_gt hpos
  have hrcoef : (2 * m - 1) * 1 * t -
        2 * (m * (m - 1) * t) * (m * (m - 1) * t) ≠ 0 := by
    intro hzero
    have hmul : t * ((2 * m - 1) - 2 * K * K * t) = 0 := by
      calc
        t * ((2 * m - 1) - 2 * K * K * t)
            = (2 * m - 1) * 1 * t -
                2 * (m * (m - 1) * t) * (m * (m - 1) * t) := by
              simp [K]
              ring
        _ = 0 := hzero
    rcases mul_eq_zero.mp hmul with ht0 | hfactor
    · exact ht ht0
    · have heven : 2 * m - 1 = 2 * (K * K * t) := by nlinarith
      omega
  have hB : (2 * m - 1) * (m * (m - 1) * t) - 1 ≠ 0 := by
    have hu_ge : 3 ≤ 2 * m - 1 := by omega
    have hC : 2 ≤ (2 * m - 1) * K := by nlinarith [hu_ge, hK_ge]
    have hne := hcoeff_ne ((2 * m - 1) * K) hC
    simpa [K, mul_comm, mul_left_comm, mul_assoc] using hne
  have hdiff : ((2 * m - 1) * (m * (m - 1) * t) - 1) *
          ((2 * m - 1) * (m * (m - 1) * t) - 1) -
        (m * (m - 1) * t) * (m * (m - 1) * t) ≠ 0 := by
    let B : Int := (2 * m - 1) * (m * (m - 1) * t) - 1
    let A : Int := m * (m - 1) * t
    have hminus : B - A ≠ 0 := by
      have hcoef_ge : 2 ≤ (2 * m - 2) * K := by
        have htwo_ge : 2 ≤ 2 * m - 2 := by omega
        nlinarith [htwo_ge, hK_ge]
      have hne := hcoeff_ne ((2 * m - 2) * K) hcoef_ge
      have heq : B - A = ((2 * m - 2) * K) * t - 1 := by
        dsimp [B, A, K]
        ring
      rw [heq]
      exact hne
    have hplus : B + A ≠ 0 := by
      have hcoef_ge : 2 ≤ (2 * m) * K := by
        have htwo_ge : 4 ≤ 2 * m := by omega
        nlinarith [htwo_ge, hK_ge]
      have hne := hcoeff_ne ((2 * m) * K) hcoef_ge
      have heq : B + A = ((2 * m) * K) * t - 1 := by
        dsimp [B, A, K]
        ring
      rw [heq]
      exact hne
    have hprod : (B - A) * (B + A) ≠ 0 := mul_ne_zero hminus hplus
    intro hzero
    apply hprod
    calc
      (B - A) * (B + A) = B * B - A * A := by ring
      _ = 0 := by simpa [B, A] using hzero
  have hcert := certificateValid_affineConsecutiveHypotenuseStrip
    (m := m) (q := 1) (t := t) (ell := 0)
    hm ht
    (by ring)
    (by simpa using hrcoef)
    (by simpa using hB)
    (by simpa using hdiff)
  simpa [mul_comm, mul_left_comm, mul_assoc] using hcert

theorem certificateValid_halfLegUnitCoordinate {u z c t : Int}
    (hu : u ≠ 0) (hz : z ≠ 0) (ht : t ≠ 0)
    (hu_odd : ∃ k : Int, u = 2 * k + 1)
    (hleg : sq u + sq (4 * z) = c * c) :
    certificateValid
      ({ x := u * (u * t - z * (u * u - 1) * t * t) +
            2 * (2 * z * t) * (u * (2 * z * t) - 1),
          y := 1 } : Point)
      ({ x := u * (u * t - z * (u * u - 1) * t * t),
          y := (4 * z) * (u * t - z * (u * u - 1) * t * t) } : Point) := by
  let A : Int := 2 * z * t
  let B : Int := u * A - 1
  let R : Int := u * t - z * (u * u - 1) * t * t
  have hv_ne : 4 * z ≠ 0 := mul_ne_zero (by norm_num) hz
  have hA_ne : A ≠ 0 := by
    dsimp [A]
    exact mul_ne_zero (mul_ne_zero (by norm_num) hz) ht
  have hR_ne : R ≠ 0 := by
    rcases hu_odd with ⟨k, hk⟩
    subst u
    intro hzero
    have hmul : t * ((2 * k + 1) - z * (((2 * k + 1) * (2 * k + 1) - 1) * t)) = 0 := by
      dsimp [R] at hzero
      nlinarith
    rcases mul_eq_zero.mp hmul with ht0 | hfactor
    · exact ht ht0
    · have heq : 2 * k + 1 = 2 * (2 * k * (k + 1) * z * t) := by
        nlinarith
      omega
  have hB_ne : B ≠ 0 := by
    rcases hu_odd with ⟨k, hk⟩
    subst u
    intro hzero
    have heq : 1 = 2 * ((2 * k + 1) * z * t) := by
      dsimp [B, A] at hzero
      nlinarith
    omega
  have hminus : B - A ≠ 0 := by
    rcases hu_odd with ⟨k, hk⟩
    subst u
    intro hzero
    have heq : 1 = 2 * (2 * k * z * t) := by
      dsimp [B, A] at hzero
      nlinarith
    omega
  have hplus : B + A ≠ 0 := by
    rcases hu_odd with ⟨k, hk⟩
    subst u
    intro hzero
    have heq : 1 = 2 * (2 * (k + 1) * z * t) := by
      dsimp [B, A] at hzero
      nlinarith
    omega
  have hdiff_ne : B * B - A * A ≠ 0 := by
    have hprod : (B - A) * (B + A) ≠ 0 := mul_ne_zero hminus hplus
    intro hzero
    apply hprod
    calc
      (B - A) * (B + A) = B * B - A * A := by ring
      _ = 0 := hzero
  have hU : legalStep ({ x := u, y := 4 * z } : Point) := by
    constructor
    · exact ⟨hu, hv_ne⟩
    · exact ⟨c, by simpa [normSq] using hleg⟩
  have hV : legalStep ({ x := 2 * A * B, y := B * B - A * A } : Point) := by
    constructor
    · constructor
      · exact mul_ne_zero (mul_ne_zero (by norm_num) hA_ne) hB_ne
      · exact hdiff_ne
    · refine ⟨A * A + B * B, ?_⟩
      simp [normSq, sq]
      ring
  have hmid : legalStep ({ x := u * R, y := (4 * z) * R } : Point) := by
    simpa [smul, R, mul_comm, mul_left_comm, mul_assoc] using legalStep_smul hR_ne hU
  have hsecond :
      sub
        ({ x := u * R + 2 * A * B, y := 1 } : Point)
        ({ x := u * R, y := (4 * z) * R } : Point) =
      ({ x := 2 * A * B, y := B * B - A * A } : Point) := by
    ext
    · simp [sub]
    · simp [sub, A, B, R]
      ring
  constructor
  · simpa [A, B, R, mul_comm, mul_left_comm, mul_assoc] using hmid
  · rw [show sub
        ({ x := u * (u * t - z * (u * u - 1) * t * t) +
              2 * (2 * z * t) * (u * (2 * z * t) - 1),
            y := 1 } : Point)
        ({ x := u * (u * t - z * (u * u - 1) * t * t),
            y := (4 * z) * (u * t - z * (u * u - 1) * t * t) } : Point) =
        ({ x := 2 * A * B, y := B * B - A * A } : Point) by
          simpa [A, B, R, mul_comm, mul_left_comm, mul_assoc] using hsecond]
    exact hV

theorem certificateValid_unitCoordinateFactorFiveParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 25 * t + 17 } : Point)
      ({ x := 4 * (40 * t * t + 55 * t + 19),
          y := 3 * (40 * t * t + 55 * t + 19) } : Point) := by
  let R : Int := 40 * t * t + 55 * t + 19
  have hR_pos : 0 < R := by
    have hsquare : 0 ≤ (80 * t + 55) * (80 * t + 55) := by
      nlinarith [sq_nonneg (80 * t + 55)]
    have hidentity : 160 * R = (80 * t + 55) * (80 * t + 55) + 15 := by
      dsimp [R]
      ring
    nlinarith
  have hR_ne : R ≠ 0 := ne_of_gt hR_pos
  have hx_factor : 1 - 4 * R = -5 * (4 * t + 3) * (8 * t + 5) := by
    dsimp [R]
    ring
  have hy_factor : 25 * t + 17 - 3 * R = -20 * (2 * t + 1) * (3 * t + 2) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 4 * R ≠ 0 := by
    have hfirst : 4 * t + 3 ≠ 0 := by omega
    have hsecond : 8 * t + 5 ≠ 0 := by omega
    have hprod : -5 * (4 * t + 3) * (8 * t + 5) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 25 * t + 17 - 3 * R ≠ 0 := by
    have hfirst : 2 * t + 1 ≠ 0 := by omega
    have hsecond : 3 * t + 2 ≠ 0 := by omega
    have hprod : -20 * (2 * t + 1) * (3 * t + 2) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨5 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨5 * (40 * t * t + 52 * t + 17), ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateFactorFourParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 20 * t + 12 } : Point)
      ({ x := -3 * (18 * t * t + 16 * t + 3),
          y := -4 * (18 * t * t + 16 * t + 3) } : Point) := by
  let R : Int := 18 * t * t + 16 * t + 3
  have hR_pos : 0 < R := by
    dsimp [R]
    by_cases hnonneg : 0 ≤ t
    · nlinarith [sq_nonneg t]
    · have hle : t ≤ -1 := by omega
      have haux : 0 ≤ (t + 1) * (t + 1) := by
        nlinarith [sq_nonneg (t + 1)]
      nlinarith
  have hR_ne : R ≠ 0 := ne_of_gt hR_pos
  have hx_factor : 1 - (-3 * R) = 2 * (3 * t + 1) * (9 * t + 5) := by
    dsimp [R]
    ring
  have hy_factor : 20 * t + 12 - (-4 * R) = 12 * (2 * t + 1) * (3 * t + 2) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - (-3 * R) ≠ 0 := by
    have hfirst : 3 * t + 1 ≠ 0 := by omega
    have hsecond : 9 * t + 5 ≠ 0 := by omega
    have hprod : 2 * (3 * t + 1) * (9 * t + 5) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 20 * t + 12 - (-4 * R) ≠ 0 := by
    have hfirst : 2 * t + 1 ≠ 0 := by omega
    have hsecond : 3 * t + 2 ≠ 0 := by omega
    have hprod : 12 * (2 * t + 1) * (3 * t + 2) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨5 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨90 * t * t + 96 * t + 26, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateOneModFiveParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 5 * t + 1 } : Point)
      ({ x := 4 * (8 * t * t + 5 * t + 1),
          y := -3 * (8 * t * t + 5 * t + 1) } : Point) := by
  let R : Int := 8 * t * t + 5 * t + 1
  have hR_pos : 0 < R := by
    have hsquare : 0 ≤ (16 * t + 5) * (16 * t + 5) := by
      nlinarith [sq_nonneg (16 * t + 5)]
    have hidentity : 32 * R = (16 * t + 5) * (16 * t + 5) + 7 := by
      dsimp [R]
      ring
    nlinarith
  have hR_ne : R ≠ 0 := ne_of_gt hR_pos
  have hx_factor : 1 - 4 * R = -1 * (4 * t + 1) * (8 * t + 3) := by
    dsimp [R]
    ring
  have hy_factor : 5 * t + 1 - (-3 * R) = 4 * (2 * t + 1) * (3 * t + 1) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 4 * R ≠ 0 := by
    have hfirst : 4 * t + 1 ≠ 0 := by omega
    have hsecond : 8 * t + 3 ≠ 0 := by omega
    have hprod : -1 * (4 * t + 1) * (8 * t + 3) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 5 * t + 1 - (-3 * R) ≠ 0 := by
    have hfirst : 2 * t + 1 ≠ 0 := by omega
    have hsecond : 3 * t + 1 ≠ 0 := by omega
    have hprod : 4 * (2 * t + 1) * (3 * t + 1) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨5 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨40 * t * t + 28 * t + 5, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateSevenModTenParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 10 * t + 7 } : Point)
      ({ x := 3 * (18 * t * t + 22 * t + 7),
          y := 4 * (18 * t * t + 22 * t + 7) } : Point) := by
  let R : Int := 18 * t * t + 22 * t + 7
  have hR_pos : 0 < R := by
    have hsquare : 0 ≤ (36 * t + 22) * (36 * t + 22) := by
      nlinarith [sq_nonneg (36 * t + 22)]
    have hidentity : 72 * R = (36 * t + 22) * (36 * t + 22) + 20 := by
      dsimp [R]
      ring
    nlinarith
  have hR_ne : R ≠ 0 := ne_of_gt hR_pos
  have hx_factor : 1 - 3 * R = -2 * (3 * t + 2) * (9 * t + 5) := by
    dsimp [R]
    ring
  have hy_factor : 10 * t + 7 - 4 * R = -3 * (2 * t + 1) * (12 * t + 7) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 3 * R ≠ 0 := by
    have hfirst : 3 * t + 2 ≠ 0 := by omega
    have hsecond : 9 * t + 5 ≠ 0 := by omega
    have hprod : -2 * (3 * t + 2) * (9 * t + 5) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 10 * t + 7 - 4 * R ≠ 0 := by
    have hfirst : 2 * t + 1 ≠ 0 := by omega
    have hsecond : 12 * t + 7 ≠ 0 := by omega
    have hprod : -3 * (2 * t + 1) * (12 * t + 7) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨5 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨90 * t * t + 102 * t + 29, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateFactorTwentyFiveParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 25 * t + 18 } : Point)
      ({ x := 4 * (8 * t * t + 9 * t + 2),
          y := -3 * (8 * t * t + 9 * t + 2) } : Point) := by
  let R : Int := 8 * t * t + 9 * t + 2
  have hR_pos : 0 < R := by
    dsimp [R]
    by_cases hnonneg : 0 ≤ t
    · nlinarith [sq_nonneg t]
    · have hle : t ≤ -1 := by omega
      have haux : 0 ≤ (t + 1) * (t + 1) := by
        nlinarith [sq_nonneg (t + 1)]
      nlinarith
  have hR_ne : R ≠ 0 := ne_of_gt hR_pos
  have hx_factor : 1 - 4 * R = -1 * (4 * t + 1) * (8 * t + 7) := by
    dsimp [R]
    ring
  have hy_factor : 25 * t + 18 - (-3 * R) = 4 * (2 * t + 3) * (3 * t + 2) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 4 * R ≠ 0 := by
    have hfirst : 4 * t + 1 ≠ 0 := by omega
    have hsecond : 8 * t + 7 ≠ 0 := by omega
    have hprod : -1 * (4 * t + 1) * (8 * t + 7) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 25 * t + 18 - (-3 * R) ≠ 0 := by
    have hfirst : 2 * t + 3 ≠ 0 := by omega
    have hsecond : 3 * t + 2 ≠ 0 := by omega
    have hprod : 4 * (2 * t + 3) * (3 * t + 2) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨5 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨5 * (8 * t * t + 12 * t + 5), ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateTwentyTwoModTwentyFiveParallel {t : Int}
    (ht : t ≠ -1) :
    certificateValid
      ({ x := 1, y := 25 * t + 22 } : Point)
      ({ x := -4 * (40 * t * t + 65 * t + 26),
          y := -3 * (40 * t * t + 65 * t + 26) } : Point) := by
  let R : Int := 40 * t * t + 65 * t + 26
  have hR_pos : 0 < R := by
    dsimp [R]
    by_cases hnonneg : 0 ≤ t
    · nlinarith [sq_nonneg t]
    · have hle : t ≤ -1 := by omega
      by_cases hdeg : t = -1
      · omega
      · have hle_strict : t ≤ -2 := by omega
        nlinarith [sq_nonneg t]
  have hR_ne : R ≠ 0 := ne_of_gt hR_pos
  have hx_factor : 1 - (-4 * R) = 5 * (4 * t + 3) * (8 * t + 7) := by
    dsimp [R]
    ring
  have hy_factor : 25 * t + 22 - (-3 * R) = 20 * (t + 1) * (6 * t + 5) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - (-4 * R) ≠ 0 := by
    have hfirst : 4 * t + 3 ≠ 0 := by omega
    have hsecond : 8 * t + 7 ≠ 0 := by omega
    have hprod : 5 * (4 * t + 3) * (8 * t + 7) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 25 * t + 22 - (-3 * R) ≠ 0 := by
    have hfirst : t + 1 ≠ 0 := by omega
    have hsecond : 6 * t + 5 ≠ 0 := by omega
    have hprod : 20 * (t + 1) * (6 * t + 5) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨5 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨5 * (40 * t * t + 68 * t + 29), ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateTwelveThirtyFiveFactorOneParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 37 * t + 25 } : Point)
      ({ x := -12 * (72 * t * t + 85 * t + 25),
          y := -35 * (72 * t * t + 85 * t + 25) } : Point) := by
  let R : Int := 72 * t * t + 85 * t + 25
  have hR_ne : R ≠ 0 := by
    have hidentity : 288 * R = (144 * t + 80) * (144 * t + 90) := by
      dsimp [R]
      ring
    have hfirst : 144 * t + 80 ≠ 0 := by omega
    have hsecond : 144 * t + 90 ≠ 0 := by omega
    have hprod : (144 * t + 80) * (144 * t + 90) ≠ 0 :=
      mul_ne_zero hfirst hsecond
    intro hR
    apply hprod
    rw [← hidentity, hR]
    ring
  have hx_factor : 1 - (-12 * R) = (12 * t + 7) * (72 * t + 43) := by
    dsimp [R]
    ring
  have hy_factor : 37 * t + 25 - (-35 * R) = 12 * (5 * t + 3) * (42 * t + 25) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - (-12 * R) ≠ 0 := by
    have hfirst : 12 * t + 7 ≠ 0 := by omega
    have hsecond : 72 * t + 43 ≠ 0 := by omega
    have hprod : (12 * t + 7) * (72 * t + 43) ≠ 0 :=
      mul_ne_zero hfirst hsecond
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 37 * t + 25 - (-35 * R) ≠ 0 := by
    have hfirst : 5 * t + 3 ≠ 0 := by omega
    have hsecond : 42 * t + 25 ≠ 0 := by omega
    have hprod : 12 * (5 * t + 3) * (42 * t + 25) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨37 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨2664 * t * t + 3180 * t + 949, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateFortyNineFactorOneParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 41 * t + 23 } : Point)
      ({ x := 40 * (800 * t * t + 889 * t + 247),
          y := 9 * (800 * t * t + 889 * t + 247) } : Point) := by
  let R : Int := 800 * t * t + 889 * t + 247
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (1600 * t + 889) * (1600 * t + 889) := by
      nlinarith [sq_nonneg (1600 * t + 889)]
    have hidentity : 3200 * R = (1600 * t + 889) * (1600 * t + 889) + 79 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 3200 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 40 * R = -((160 * t + 89) * (200 * t + 111)) := by
    dsimp [R]
    ring
  have hy_factor : 41 * t + 23 - 9 * R = -40 * (9 * t + 5) * (20 * t + 11) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 40 * R ≠ 0 := by
    have hfirst : 160 * t + 89 ≠ 0 := by omega
    have hsecond : 200 * t + 111 ≠ 0 := by omega
    have hprod : -((160 * t + 89) * (200 * t + 111)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 41 * t + 23 - 9 * R ≠ 0 := by
    have hfirst : 9 * t + 5 ≠ 0 := by omega
    have hsecond : 20 * t + 11 ≠ 0 := by omega
    have hprod : -40 * (9 * t + 5) * (20 * t + 11) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨41 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨32800 * t * t + 36440 * t + 10121, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateTwentyEightFortyFiveFactorOneParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 53 * t + 10 } : Point)
      ({ x := 28 * (392 * t * t + 125 * t + 10),
          y := 45 * (392 * t * t + 125 * t + 10) } : Point) := by
  let R : Int := 392 * t * t + 125 * t + 10
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (784 * t + 125) * (784 * t + 125) := by
      nlinarith [sq_nonneg (784 * t + 125)]
    have hidentity : 1568 * R = (784 * t + 125) * (784 * t + 125) + 55 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 1568 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 28 * R = -((56 * t + 9) * (196 * t + 31)) := by
    dsimp [R]
    ring
  have hy_factor : 53 * t + 10 - 45 * R = -4 * (63 * t + 10) * (70 * t + 11) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 28 * R ≠ 0 := by
    have hfirst : 56 * t + 9 ≠ 0 := by omega
    have hsecond : 196 * t + 31 ≠ 0 := by omega
    have hprod : -((56 * t + 9) * (196 * t + 31)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 53 * t + 10 - 45 * R ≠ 0 := by
    have hfirst : 63 * t + 10 ≠ 0 := by omega
    have hsecond : 70 * t + 11 ≠ 0 := by omega
    have hprod : -4 * (63 * t + 10) * (70 * t + 11) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨53 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨20776 * t * t + 6580 * t + 521, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateSixtyElevenFactorOneParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 61 * t + 39 } : Point)
      ({ x := 60 * (1800 * t * t + 2291 * t + 729),
          y := 11 * (1800 * t * t + 2291 * t + 729) } : Point) := by
  let R : Int := 1800 * t * t + 2291 * t + 729
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (3600 * t + 2291) * (3600 * t + 2291) := by
      nlinarith [sq_nonneg (3600 * t + 2291)]
    have hidentity : 7200 * R = (3600 * t + 2291) * (3600 * t + 2291) + 119 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 7200 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 60 * R = -((300 * t + 191) * (360 * t + 229)) := by
    dsimp [R]
    ring
  have hy_factor : 61 * t + 39 - 11 * R = -60 * (11 * t + 7) * (30 * t + 19) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 60 * R ≠ 0 := by
    have hfirst : 300 * t + 191 ≠ 0 := by omega
    have hsecond : 360 * t + 229 ≠ 0 := by omega
    have hprod : -((300 * t + 191) * (360 * t + 229)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 61 * t + 39 - 11 * R ≠ 0 := by
    have hfirst : 11 * t + 7 ≠ 0 := by omega
    have hsecond : 30 * t + 19 ≠ 0 := by omega
    have hprod : -60 * (11 * t + 7) * (30 * t + 19) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨61 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨109800 * t * t + 139740 * t + 44461, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateFortyEightFiftyFiveFactorOneParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 73 * t + 31 } : Point)
      ({ x := 48 * (1152 * t * t + 943 * t + 193),
          y := 55 * (1152 * t * t + 943 * t + 193) } : Point) := by
  let R : Int := 1152 * t * t + 943 * t + 193
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (2304 * t + 943) * (2304 * t + 943) := by
      nlinarith [sq_nonneg (2304 * t + 943)]
    have hidentity : 4608 * R = (2304 * t + 943) * (2304 * t + 943) + 95 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 4608 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 48 * R = -((144 * t + 59) * (384 * t + 157)) := by
    dsimp [R]
    ring
  have hy_factor : 73 * t + 31 - 55 * R = -24 * (22 * t + 9) * (120 * t + 49) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 48 * R ≠ 0 := by
    have hfirst : 144 * t + 59 ≠ 0 := by omega
    have hsecond : 384 * t + 157 ≠ 0 := by omega
    have hprod : -((144 * t + 59) * (384 * t + 157)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 73 * t + 31 - 55 * R ≠ 0 := by
    have hfirst : 22 * t + 9 ≠ 0 := by omega
    have hsecond : 120 * t + 49 ≠ 0 := by omega
    have hprod : -24 * (22 * t + 9) * (120 * t + 49) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨73 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨84096 * t * t + 68784 * t + 14065, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateEightyThirtyNineFactorOneParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 89 * t + 71 } : Point)
      ({ x := 80 * (3200 * t * t + 5071 * t + 2009),
          y := 39 * (3200 * t * t + 5071 * t + 2009) } : Point) := by
  let R : Int := 3200 * t * t + 5071 * t + 2009
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (6400 * t + 5071) * (6400 * t + 5071) := by
      nlinarith [sq_nonneg (6400 * t + 5071)]
    have hidentity : 12800 * R = (6400 * t + 5071) * (6400 * t + 5071) + 159 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 12800 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 80 * R = -((400 * t + 317) * (640 * t + 507)) := by
    dsimp [R]
    ring
  have hy_factor : 89 * t + 71 - 39 * R = -40 * (24 * t + 19) * (130 * t + 103) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 80 * R ≠ 0 := by
    have hfirst : 400 * t + 317 ≠ 0 := by omega
    have hsecond : 640 * t + 507 ≠ 0 := by omega
    have hprod : -((400 * t + 317) * (640 * t + 507)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 89 * t + 71 - 39 * R ≠ 0 := by
    have hfirst : 24 * t + 19 ≠ 0 := by omega
    have hsecond : 130 * t + 103 ≠ 0 := by omega
    have hprod : -40 * (24 * t + 19) * (130 * t + 103) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨89 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨284800 * t * t + 451280 * t + 178769, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateSeventyTwoSixtyFiveFactorOneParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 97 * t + 78 } : Point)
      ({ x := 72 * (2592 * t * t + 4121 * t + 1638),
          y := 65 * (2592 * t * t + 4121 * t + 1638) } : Point) := by
  let R : Int := 2592 * t * t + 4121 * t + 1638
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (5184 * t + 4121) * (5184 * t + 4121) := by
      nlinarith [sq_nonneg (5184 * t + 4121)]
    have hidentity : 10368 * R = (5184 * t + 4121) * (5184 * t + 4121) + 143 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 10368 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 72 * R = -((288 * t + 229) * (648 * t + 515)) := by
    dsimp [R]
    ring
  have hy_factor : 97 * t + 78 - 65 * R = -24 * (39 * t + 31) * (180 * t + 143) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 72 * R ≠ 0 := by
    have hfirst : 288 * t + 229 ≠ 0 := by omega
    have hsecond : 648 * t + 515 ≠ 0 := by omega
    have hprod : -((288 * t + 229) * (648 * t + 515)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 97 * t + 78 - 65 * R ≠ 0 := by
    have hfirst : 39 * t + 31 ≠ 0 := by omega
    have hsecond : 180 * t + 143 ≠ 0 := by omega
    have hprod : -24 * (39 * t + 31) * (180 * t + 143) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨97 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨251424 * t * t + 399672 * t + 158833, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateTwentyNinetyNineFactorOneParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 101 * t + 60 } : Point)
      ({ x := 20 * (200 * t * t + 219 * t + 60),
          y := 99 * (200 * t * t + 219 * t + 60) } : Point) := by
  let R : Int := 200 * t * t + 219 * t + 60
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (400 * t + 219) * (400 * t + 219) := by
      nlinarith [sq_nonneg (400 * t + 219)]
    have hidentity : 800 * R = (400 * t + 219) * (400 * t + 219) + 39 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 800 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 20 * R = -((20 * t + 11) * (200 * t + 109)) := by
    dsimp [R]
    ring
  have hy_factor : 101 * t + 60 - 99 * R = -20 * (11 * t + 6) * (90 * t + 49) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 20 * R ≠ 0 := by
    have hfirst : 20 * t + 11 ≠ 0 := by omega
    have hsecond : 200 * t + 109 ≠ 0 := by omega
    have hprod : -((20 * t + 11) * (200 * t + 109)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 101 * t + 60 - 99 * R ≠ 0 := by
    have hfirst : 11 * t + 6 ≠ 0 := by omega
    have hsecond : 90 * t + 49 ≠ 0 := by omega
    have hprod : -20 * (11 * t + 6) * (90 * t + 49) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨101 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨20200 * t * t + 22020 * t + 6001, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateSixtyNinetyOneFactorOneParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 109 * t + 82 } : Point)
      ({ x := 60 * (1800 * t * t + 2659 * t + 982),
          y := 91 * (1800 * t * t + 2659 * t + 982) } : Point) := by
  let R : Int := 1800 * t * t + 2659 * t + 982
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (3600 * t + 2659) * (3600 * t + 2659) := by
      nlinarith [sq_nonneg (3600 * t + 2659)]
    have hidentity : 7200 * R = (3600 * t + 2659) * (3600 * t + 2659) + 119 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 7200 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 60 * R = -((180 * t + 133) * (600 * t + 443)) := by
    dsimp [R]
    ring
  have hy_factor : 109 * t + 82 - 91 * R = -60 * (42 * t + 31) * (65 * t + 48) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 60 * R ≠ 0 := by
    have hfirst : 180 * t + 133 ≠ 0 := by omega
    have hsecond : 600 * t + 443 ≠ 0 := by omega
    have hprod : -((180 * t + 133) * (600 * t + 443)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 109 * t + 82 - 91 * R ≠ 0 := by
    have hfirst : 42 * t + 31 ≠ 0 := by omega
    have hsecond : 65 * t + 48 ≠ 0 := by omega
    have hprod : -60 * (42 * t + 31) * (65 * t + 48) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨109 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨196200 * t * t + 289740 * t + 106969, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateOneHundredTwelveFifteenFactorOneParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 113 * t + 83 } : Point)
      ({ x := 112 * (6272 * t * t + 9199 * t + 3373),
          y := 15 * (6272 * t * t + 9199 * t + 3373) } : Point) := by
  let R : Int := 6272 * t * t + 9199 * t + 3373
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (12544 * t + 9199) * (12544 * t + 9199) := by
      nlinarith [sq_nonneg (12544 * t + 9199)]
    have hidentity :
        25088 * R = (12544 * t + 9199) * (12544 * t + 9199) + 223 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 25088 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 112 * R = -((784 * t + 575) * (896 * t + 657)) := by
    dsimp [R]
    ring
  have hy_factor : 113 * t + 83 - 15 * R = -112 * (15 * t + 11) * (56 * t + 41) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 112 * R ≠ 0 := by
    have hfirst : 784 * t + 575 ≠ 0 := by omega
    have hsecond : 896 * t + 657 ≠ 0 := by omega
    have hprod : -((784 * t + 575) * (896 * t + 657)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 113 * t + 83 - 15 * R ≠ 0 := by
    have hfirst : 15 * t + 11 ≠ 0 := by omega
    have hsecond : 56 * t + 41 ≠ 0 := by omega
    have hprod : -112 * (15 * t + 11) * (56 * t + 41) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨113 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨708736 * t * t + 1039472 * t + 381137, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateEightyEightOneHundredFiveFactorOneParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 137 * t + 7 } : Point)
      ({ x := 88 * (3872 * t * t + 329 * t + 7),
          y := 105 * (3872 * t * t + 329 * t + 7) } : Point) := by
  let R : Int := 3872 * t * t + 329 * t + 7
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (7744 * t + 329) * (7744 * t + 329) := by
      nlinarith [sq_nonneg (7744 * t + 329)]
    have hidentity : 15488 * R = (7744 * t + 329) * (7744 * t + 329) + 175 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 15488 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 88 * R = -((352 * t + 15) * (968 * t + 41)) := by
    dsimp [R]
    ring
  have hy_factor : 137 * t + 7 - 105 * R = -8 * (165 * t + 7) * (308 * t + 13) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 88 * R ≠ 0 := by
    have hfirst : 352 * t + 15 ≠ 0 := by omega
    have hsecond : 968 * t + 41 ≠ 0 := by omega
    have hprod : -((352 * t + 15) * (968 * t + 41)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 137 * t + 7 - 105 * R ≠ 0 := by
    have hfirst : 165 * t + 7 ≠ 0 := by omega
    have hsecond : 308 * t + 13 ≠ 0 := by omega
    have hprod : -8 * (165 * t + 7) * (308 * t + 13) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨137 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨530464 * t * t + 44968 * t + 953, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateOneHundredFortyFiftyOneFactorOneParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 149 * t + 82 } : Point)
      ({ x := 140 * (9800 * t * t + 10739 * t + 2942),
          y := 51 * (9800 * t * t + 10739 * t + 2942) } : Point) := by
  let R : Int := 9800 * t * t + 10739 * t + 2942
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (19600 * t + 10739) * (19600 * t + 10739) := by
      nlinarith [sq_nonneg (19600 * t + 10739)]
    have hidentity :
        39200 * R = (19600 * t + 10739) * (19600 * t + 10739) + 279 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 39200 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 140 * R = -((980 * t + 537) * (1400 * t + 767)) := by
    dsimp [R]
    ring
  have hy_factor : 149 * t + 82 - 51 * R = -20 * (42 * t + 23) * (595 * t + 326) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 140 * R ≠ 0 := by
    have hfirst : 980 * t + 537 ≠ 0 := by omega
    have hsecond : 1400 * t + 767 ≠ 0 := by omega
    have hprod : -((980 * t + 537) * (1400 * t + 767)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 149 * t + 82 - 51 * R ≠ 0 := by
    have hfirst : 42 * t + 23 ≠ 0 := by omega
    have hsecond : 595 * t + 326 ≠ 0 := by omega
    have hprod : -20 * (42 * t + 23) * (595 * t + 326) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨149 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨1460200 * t * t + 1600060 * t + 438329, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateOneHundredThirtyTwoEightyFiveFactorOneParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 157 * t + 4 } : Point)
      ({ x := 132 * (8712 * t * t + 373 * t + 4),
          y := 85 * (8712 * t * t + 373 * t + 4) } : Point) := by
  let R : Int := 8712 * t * t + 373 * t + 4
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (17424 * t + 373) * (17424 * t + 373) := by
      nlinarith [sq_nonneg (17424 * t + 373)]
    have hidentity :
        34848 * R = (17424 * t + 373) * (17424 * t + 373) + 263 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 34848 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 132 * R = -((792 * t + 17) * (1452 * t + 31)) := by
    dsimp [R]
    ring
  have hy_factor : 157 * t + 4 - 85 * R = -12 * (187 * t + 4) * (330 * t + 7) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 132 * R ≠ 0 := by
    have hfirst : 792 * t + 17 ≠ 0 := by omega
    have hsecond : 1452 * t + 31 ≠ 0 := by omega
    have hprod : -((792 * t + 17) * (1452 * t + 31)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 157 * t + 4 - 85 * R ≠ 0 := by
    have hfirst : 187 * t + 4 ≠ 0 := by omega
    have hsecond : 330 * t + 7 ≠ 0 := by omega
    have hprod : -12 * (187 * t + 4) * (330 * t + 7) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨157 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨1367784 * t * t + 58476 * t + 625, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateOneHundredTwentyOneHundredNineteenFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 169 * t + 168 } : Point)
      ({ x := 120 * (7200 * t * t + 14231 * t + 7032),
          y := 119 * (7200 * t * t + 14231 * t + 7032) } : Point) := by
  let R : Int := 7200 * t * t + 14231 * t + 7032
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (14400 * t + 14231) * (14400 * t + 14231) := by
      nlinarith [sq_nonneg (14400 * t + 14231)]
    have hidentity :
        28800 * R = (14400 * t + 14231) * (14400 * t + 14231) + 239 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 28800 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 120 * R = -((600 * t + 593) * (1440 * t + 1423)) := by
    dsimp [R]
    ring
  have hy_factor :
      169 * t + 168 - 119 * R = -120 * (84 * t + 83) * (85 * t + 84) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 120 * R ≠ 0 := by
    have hfirst : 600 * t + 593 ≠ 0 := by omega
    have hsecond : 1440 * t + 1423 ≠ 0 := by omega
    have hprod : -((600 * t + 593) * (1440 * t + 1423)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 169 * t + 168 - 119 * R ≠ 0 := by
    have hfirst : 84 * t + 83 ≠ 0 := by omega
    have hsecond : 85 * t + 84 ≠ 0 := by omega
    have hprod : -120 * (84 * t + 83) * (85 * t + 84) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨169 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨1216800 * t * t + 2404920 * t + 1188289, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateFiftyTwoOneHundredSixtyFiveFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 173 * t + 28 } : Point)
      ({ x := 52 * (1352 * t * t + 389 * t + 28),
          y := 165 * (1352 * t * t + 389 * t + 28) } : Point) := by
  let R : Int := 1352 * t * t + 389 * t + 28
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (2704 * t + 389) * (2704 * t + 389) := by
      nlinarith [sq_nonneg (2704 * t + 389)]
    have hidentity :
        5408 * R = (2704 * t + 389) * (2704 * t + 389) + 103 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 5408 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 52 * R = -((104 * t + 15) * (676 * t + 97)) := by
    dsimp [R]
    ring
  have hy_factor : 173 * t + 28 - 165 * R = -4 * (195 * t + 28) * (286 * t + 41) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 52 * R ≠ 0 := by
    have hfirst : 104 * t + 15 ≠ 0 := by omega
    have hsecond : 676 * t + 97 ≠ 0 := by omega
    have hprod : -((104 * t + 15) * (676 * t + 97)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 173 * t + 28 - 165 * R ≠ 0 := by
    have hfirst : 195 * t + 28 ≠ 0 := by omega
    have hsecond : 286 * t + 41 ≠ 0 := by omega
    have hprod : -4 * (195 * t + 28) * (286 * t + 41) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨173 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨233896 * t * t + 67132 * t + 4817, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateOneHundredEightyNineteenFactorOneParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 181 * t + 143 } : Point)
      ({ x := 180 * (16200 * t * t + 25579 * t + 10097),
          y := 19 * (16200 * t * t + 25579 * t + 10097) } : Point) := by
  let R : Int := 16200 * t * t + 25579 * t + 10097
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (32400 * t + 25579) * (32400 * t + 25579) := by
      nlinarith [sq_nonneg (32400 * t + 25579)]
    have hidentity :
        64800 * R = (32400 * t + 25579) * (32400 * t + 25579) + 359 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 64800 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 180 * R = -((1620 * t + 1279) * (1800 * t + 1421)) := by
    dsimp [R]
    ring
  have hy_factor :
      181 * t + 143 - 19 * R = -180 * (19 * t + 15) * (90 * t + 71) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 180 * R ≠ 0 := by
    have hfirst : 1620 * t + 1279 ≠ 0 := by omega
    have hsecond : 1800 * t + 1421 ≠ 0 := by omega
    have hprod : -((1620 * t + 1279) * (1800 * t + 1421)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 181 * t + 143 - 19 * R ≠ 0 := by
    have hfirst : 19 * t + 15 ≠ 0 := by omega
    have hsecond : 90 * t + 71 ≠ 0 := by omega
    have hprod : -180 * (19 * t + 15) * (90 * t + 71) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨181 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨2932200 * t * t + 4629780 * t + 1827541, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateOneHundredSixtyEightNinetyFiveFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 193 * t + 47 } : Point)
      ({ x := 168 * (14112 * t * t + 6791 * t + 817),
          y := 95 * (14112 * t * t + 6791 * t + 817) } : Point) := by
  let R : Int := 14112 * t * t + 6791 * t + 817
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (28224 * t + 6791) * (28224 * t + 6791) := by
      nlinarith [sq_nonneg (28224 * t + 6791)]
    have hidentity :
        56448 * R = (28224 * t + 6791) * (28224 * t + 6791) + 335 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 56448 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 168 * R = -((1176 * t + 283) * (2016 * t + 485)) := by
    dsimp [R]
    ring
  have hy_factor :
      193 * t + 47 - 95 * R = -24 * (133 * t + 32) * (420 * t + 101) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 168 * R ≠ 0 := by
    have hfirst : 1176 * t + 283 ≠ 0 := by omega
    have hsecond : 2016 * t + 485 ≠ 0 := by omega
    have hprod : -((1176 * t + 283) * (2016 * t + 485)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 193 * t + 47 - 95 * R ≠ 0 := by
    have hfirst : 133 * t + 32 ≠ 0 := by omega
    have hsecond : 420 * t + 101 ≠ 0 := by omega
    have hprod : -24 * (133 * t + 32) * (420 * t + 101) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨193 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨2723616 * t * t + 1310568 * t + 157657, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateTwentyEightOneHundredNinetyFiveFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 197 * t + 112 } : Point)
      ({ x := 28 * (392 * t * t + 419 * t + 112),
          y := 195 * (392 * t * t + 419 * t + 112) } : Point) := by
  let R : Int := 392 * t * t + 419 * t + 112
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (784 * t + 419) * (784 * t + 419) := by
      nlinarith [sq_nonneg (784 * t + 419)]
    have hidentity : 1568 * R = (784 * t + 419) * (784 * t + 419) + 55 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 1568 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 28 * R = -((28 * t + 15) * (392 * t + 209)) := by
    dsimp [R]
    ring
  have hy_factor : 197 * t + 112 - 195 * R = -28 * (15 * t + 8) * (182 * t + 97) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 28 * R ≠ 0 := by
    have hfirst : 28 * t + 15 ≠ 0 := by omega
    have hsecond : 392 * t + 209 ≠ 0 := by omega
    have hprod : -((28 * t + 15) * (392 * t + 209)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 197 * t + 112 - 195 * R ≠ 0 := by
    have hfirst : 15 * t + 8 ≠ 0 := by omega
    have hsecond : 182 * t + 97 ≠ 0 := by omega
    have hprod : -28 * (15 * t + 8) * (182 * t + 97) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨197 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨77224 * t * t + 82348 * t + 21953, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateSixtyTwoHundredTwentyOneFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 229 * t + 36 } : Point)
      ({ x := 60 * (1800 * t * t + 509 * t + 36),
          y := 221 * (1800 * t * t + 509 * t + 36) } : Point) := by
  let R : Int := 1800 * t * t + 509 * t + 36
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (3600 * t + 509) * (3600 * t + 509) := by
      nlinarith [sq_nonneg (3600 * t + 509)]
    have hidentity : 7200 * R = (3600 * t + 509) * (3600 * t + 509) + 119 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 7200 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 60 * R = -((120 * t + 17) * (900 * t + 127)) := by
    dsimp [R]
    ring
  have hy_factor : 229 * t + 36 - 221 * R = -60 * (78 * t + 11) * (85 * t + 12) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 60 * R ≠ 0 := by
    have hfirst : 120 * t + 17 ≠ 0 := by omega
    have hsecond : 900 * t + 127 ≠ 0 := by omega
    have hprod : -((120 * t + 17) * (900 * t + 127)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 229 * t + 36 - 221 * R ≠ 0 := by
    have hfirst : 78 * t + 11 ≠ 0 := by omega
    have hsecond : 85 * t + 12 ≠ 0 := by omega
    have hprod : -60 * (78 * t + 11) * (85 * t + 12) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨229 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨412200 * t * t + 116340 * t + 8209, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateThreeHundredTwelveTwentyFiveFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 313 * t + 263 } : Point)
      ({ x := 312 * (48672 * t * t + 81769 * t + 34343),
          y := 25 * (48672 * t * t + 81769 * t + 34343) } : Point) := by
  let R : Int := 48672 * t * t + 81769 * t + 34343
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (97344 * t + 81769) * (97344 * t + 81769) := by
      nlinarith [sq_nonneg (97344 * t + 81769)]
    have hidentity :
        194688 * R = (97344 * t + 81769) * (97344 * t + 81769) + 623 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 194688 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 312 * R = -((3744 * t + 3145) * (4056 * t + 3407)) := by
    dsimp [R]
    ring
  have hy_factor : 313 * t + 263 - 25 * R = -312 * (25 * t + 21) * (156 * t + 131) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 312 * R ≠ 0 := by
    have hfirst : 3744 * t + 3145 ≠ 0 := by omega
    have hsecond : 4056 * t + 3407 ≠ 0 := by omega
    have hprod : -((3744 * t + 3145) * (4056 * t + 3407)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 313 * t + 263 - 25 * R ≠ 0 := by
    have hfirst : 25 * t + 21 ≠ 0 := by omega
    have hsecond : 156 * t + 131 ≠ 0 := by omega
    have hprod : -312 * (25 * t + 21) * (156 * t + 131) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨313 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨15234336 * t * t + 25593672 * t + 10749337, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateThreeHundredEightSeventyFiveFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 317 * t + 296 } : Point)
      ({ x := 308 * (47432 * t * t + 88507 * t + 41288),
          y := 75 * (47432 * t * t + 88507 * t + 41288) } : Point) := by
  let R : Int := 47432 * t * t + 88507 * t + 41288
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (94864 * t + 88507) * (94864 * t + 88507) := by
      nlinarith [sq_nonneg (94864 * t + 88507)]
    have hidentity :
        189728 * R = (94864 * t + 88507) * (94864 * t + 88507) + 615 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 189728 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 308 * R = -((3388 * t + 3161) * (4312 * t + 4023)) := by
    dsimp [R]
    ring
  have hy_factor : 317 * t + 296 - 75 * R = -4 * (462 * t + 431) * (1925 * t + 1796) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 308 * R ≠ 0 := by
    have hfirst : 3388 * t + 3161 ≠ 0 := by omega
    have hsecond : 4312 * t + 4023 ≠ 0 := by omega
    have hprod : -((3388 * t + 3161) * (4312 * t + 4023)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 317 * t + 296 - 75 * R ≠ 0 := by
    have hfirst : 462 * t + 431 ≠ 0 := by omega
    have hsecond : 1925 * t + 1796 ≠ 0 := by omega
    have hprod : -4 * (462 * t + 431) * (1925 * t + 1796) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨317 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨15035944 * t * t + 28056644 * t + 13088225, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateTwoHundredEightyEightOneHundredSeventyFiveFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 337 * t + 241 } : Point)
      ({ x := 288 * (41472 * t * t + 59167 * t + 21103),
          y := 175 * (41472 * t * t + 59167 * t + 21103) } : Point) := by
  let R : Int := 41472 * t * t + 59167 * t + 21103
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (82944 * t + 59167) * (82944 * t + 59167) := by
      nlinarith [sq_nonneg (82944 * t + 59167)]
    have hidentity :
        165888 * R = (82944 * t + 59167) * (82944 * t + 59167) + 575 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 165888 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 288 * R = -((2592 * t + 1849) * (4608 * t + 3287)) := by
    dsimp [R]
    ring
  have hy_factor : 337 * t + 241 - 175 * R = -48 * (150 * t + 107) * (1008 * t + 719) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 288 * R ≠ 0 := by
    have hfirst : 2592 * t + 1849 ≠ 0 := by omega
    have hsecond : 4608 * t + 3287 ≠ 0 := by omega
    have hprod : -((2592 * t + 1849) * (4608 * t + 3287)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 337 * t + 241 - 175 * R ≠ 0 := by
    have hfirst : 150 * t + 107 ≠ 0 := by omega
    have hsecond : 1008 * t + 719 ≠ 0 := by omega
    have hprod : -48 * (150 * t + 107) * (1008 * t + 719) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨337 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨13976064 * t * t + 19939104 * t + 7111585, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateOneHundredEightyTwoHundredNinetyNineFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 349 * t + 206 } : Point)
      ({ x := 180 * (16200 * t * t + 18971 * t + 5554),
          y := 299 * (16200 * t * t + 18971 * t + 5554) } : Point) := by
  let R : Int := 16200 * t * t + 18971 * t + 5554
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (32400 * t + 18971) * (32400 * t + 18971) := by
      nlinarith [sq_nonneg (32400 * t + 18971)]
    have hidentity :
        64800 * R = (32400 * t + 18971) * (32400 * t + 18971) + 359 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 64800 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 180 * R = -((900 * t + 527) * (3240 * t + 1897)) := by
    dsimp [R]
    ring
  have hy_factor : 349 * t + 206 - 299 * R = -60 * (234 * t + 137) * (345 * t + 202) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 180 * R ≠ 0 := by
    have hfirst : 900 * t + 527 ≠ 0 := by omega
    have hsecond : 3240 * t + 1897 ≠ 0 := by omega
    have hprod : -((900 * t + 527) * (3240 * t + 1897)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 349 * t + 206 - 299 * R ≠ 0 := by
    have hfirst : 234 * t + 137 ≠ 0 := by omega
    have hsecond : 345 * t + 202 ≠ 0 := by omega
    have hprod : -60 * (234 * t + 137) * (345 * t + 202) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨349 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨5653800 * t * t + 6620580 * t + 1938169, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateTwoHundredSeventyTwoTwoHundredTwentyFiveFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 353 * t + 49 } : Point)
      ({ x := 272 * (36992 * t * t + 10097 * t + 689),
          y := 225 * (36992 * t * t + 10097 * t + 689) } : Point) := by
  let R : Int := 36992 * t * t + 10097 * t + 689
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (73984 * t + 10097) * (73984 * t + 10097) := by
      nlinarith [sq_nonneg (73984 * t + 10097)]
    have hidentity :
        147968 * R = (73984 * t + 10097) * (73984 * t + 10097) + 543 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 147968 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 272 * R = -((2176 * t + 297) * (4624 * t + 631)) := by
    dsimp [R]
    ring
  have hy_factor : 353 * t + 49 - 225 * R = -16 * (425 * t + 58) * (1224 * t + 167) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 272 * R ≠ 0 := by
    have hfirst : 2176 * t + 297 ≠ 0 := by omega
    have hsecond : 4624 * t + 631 ≠ 0 := by omega
    have hprod : -((2176 * t + 297) * (4624 * t + 631)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 353 * t + 49 - 225 * R ≠ 0 := by
    have hfirst : 425 * t + 58 ≠ 0 := by omega
    have hsecond : 1224 * t + 167 ≠ 0 := by omega
    have hprod : -16 * (425 * t + 58) * (1224 * t + 167) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨353 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨13058176 * t * t + 3564016 * t + 243185, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateTwoHundredFiftyTwoTwoHundredSeventyFiveFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 373 * t + 151 } : Point)
      ({ x := 252 * (31752 * t * t + 25523 * t + 5129),
          y := 275 * (31752 * t * t + 25523 * t + 5129) } : Point) := by
  let R : Int := 31752 * t * t + 25523 * t + 5129
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (63504 * t + 25523) * (63504 * t + 25523) := by
      nlinarith [sq_nonneg (63504 * t + 25523)]
    have hidentity :
        127008 * R = (63504 * t + 25523) * (63504 * t + 25523) + 503 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 127008 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 252 * R = -((1764 * t + 709) * (4536 * t + 1823)) := by
    dsimp [R]
    ring
  have hy_factor : 373 * t + 151 - 275 * R = -12 * (525 * t + 211) * (1386 * t + 557) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 252 * R ≠ 0 := by
    have hfirst : 1764 * t + 709 ≠ 0 := by omega
    have hsecond : 4536 * t + 1823 ≠ 0 := by omega
    have hprod : -((1764 * t + 709) * (4536 * t + 1823)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 373 * t + 151 - 275 * R ≠ 0 := by
    have hfirst : 525 * t + 211 ≠ 0 := by omega
    have hsecond : 1386 * t + 557 ≠ 0 := by omega
    have hprod : -12 * (525 * t + 211) * (1386 * t + 557) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨373 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨11843496 * t * t + 9519804 * t + 1913005, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateThreeHundredFiftyTwoOneHundredThirtyFiveFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 377 * t + 299 } : Point)
      ({ x := 352 * (61952 * t * t + 98143 * t + 38869),
          y := 135 * (61952 * t * t + 98143 * t + 38869) } : Point) := by
  let R : Int := 61952 * t * t + 98143 * t + 38869
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (123904 * t + 98143) * (123904 * t + 98143) := by
      nlinarith [sq_nonneg (123904 * t + 98143)]
    have hidentity :
        247808 * R = (123904 * t + 98143) * (123904 * t + 98143) + 703 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 247808 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 352 * R = -((3872 * t + 3067) * (5632 * t + 4461)) := by
    dsimp [R]
    ring
  have hy_factor : 377 * t + 299 - 135 * R = -8 * (880 * t + 697) * (1188 * t + 941) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 352 * R ≠ 0 := by
    have hfirst : 3872 * t + 3067 ≠ 0 := by omega
    have hsecond : 5632 * t + 4461 ≠ 0 := by omega
    have hprod : -((3872 * t + 3067) * (5632 * t + 4461)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 377 * t + 299 - 135 * R ≠ 0 := by
    have hfirst : 880 * t + 697 ≠ 0 := by omega
    have hsecond : 1188 * t + 941 ≠ 0 := by omega
    have hprod : -8 * (880 * t + 697) * (1188 * t + 941) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨377 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨23355904 * t * t + 36999776 * t + 14653505, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateThreeHundredFortyOneHundredEightyNineFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 389 * t + 97 } : Point)
      ({ x := 340 * (57800 * t * t + 28661 * t + 3553),
          y := 189 * (57800 * t * t + 28661 * t + 3553) } : Point) := by
  let R : Int := 57800 * t * t + 28661 * t + 3553
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (115600 * t + 28661) * (115600 * t + 28661) := by
      nlinarith [sq_nonneg (115600 * t + 28661)]
    have hidentity :
        231200 * R = (115600 * t + 28661) * (115600 * t + 28661) + 679 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 231200 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 340 * R = -((3400 * t + 843) * (5780 * t + 1433)) := by
    dsimp [R]
    ring
  have hy_factor : 389 * t + 97 - 189 * R = -20 * (238 * t + 59) * (2295 * t + 569) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 340 * R ≠ 0 := by
    have hfirst : 3400 * t + 843 ≠ 0 := by omega
    have hsecond : 5780 * t + 1433 ≠ 0 := by omega
    have hprod : -((3400 * t + 843) * (5780 * t + 1433)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 389 * t + 97 - 189 * R ≠ 0 := by
    have hfirst : 238 * t + 59 ≠ 0 := by omega
    have hsecond : 2295 * t + 569 ≠ 0 := by omega
    have hprod : -20 * (238 * t + 59) * (2295 * t + 569) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨389 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨22484200 * t * t + 11148940 * t + 1382069, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateTwoHundredTwentyEightThreeHundredTwentyFiveFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 397 * t + 141 } : Point)
      ({ x := 228 * (25992 * t * t + 18277 * t + 3213),
          y := 325 * (25992 * t * t + 18277 * t + 3213) } : Point) := by
  let R : Int := 25992 * t * t + 18277 * t + 3213
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (51984 * t + 18277) * (51984 * t + 18277) := by
      nlinarith [sq_nonneg (51984 * t + 18277)]
    have hidentity :
        103968 * R = (51984 * t + 18277) * (51984 * t + 18277) + 455 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 103968 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 228 * R = -((1368 * t + 481) * (4332 * t + 1523)) := by
    dsimp [R]
    ring
  have hy_factor : 397 * t + 141 - 325 * R = -12 * (475 * t + 167) * (1482 * t + 521) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 228 * R ≠ 0 := by
    have hfirst : 1368 * t + 481 ≠ 0 := by omega
    have hsecond : 4332 * t + 1523 ≠ 0 := by omega
    have hprod : -((1368 * t + 481) * (4332 * t + 1523)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 397 * t + 141 - 325 * R ≠ 0 := by
    have hfirst : 475 * t + 167 ≠ 0 := by omega
    have hsecond : 1482 * t + 521 ≠ 0 := by omega
    have hprod : -12 * (475 * t + 167) * (1482 * t + 521) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨397 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨10318824 * t * t + 7255644 * t + 1275445, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateFortyThreeHundredNinetyNineFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 401 * t + 220 } : Point)
      ({ x := 40 * (800 * t * t + 839 * t + 220),
          y := 399 * (800 * t * t + 839 * t + 220) } : Point) := by
  let R : Int := 800 * t * t + 839 * t + 220
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (1600 * t + 839) * (1600 * t + 839) := by
      nlinarith [sq_nonneg (1600 * t + 839)]
    have hidentity :
        3200 * R = (1600 * t + 839) * (1600 * t + 839) + 79 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 3200 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 40 * R = -((40 * t + 21) * (800 * t + 419)) := by
    dsimp [R]
    ring
  have hy_factor : 401 * t + 220 - 399 * R = -40 * (21 * t + 11) * (380 * t + 199) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 40 * R ≠ 0 := by
    have hfirst : 40 * t + 21 ≠ 0 := by omega
    have hsecond : 800 * t + 419 ≠ 0 := by omega
    have hprod : -((40 * t + 21) * (800 * t + 419)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 401 * t + 220 - 399 * R ≠ 0 := by
    have hfirst : 21 * t + 11 ≠ 0 := by omega
    have hsecond : 380 * t + 199 ≠ 0 := by omega
    have hprod : -40 * (21 * t + 11) * (380 * t + 199) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨401 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨320800 * t * t + 336040 * t + 88001, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateOneHundredTwentyThreeHundredNinetyOneFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 409 * t + 302 } : Point)
      ({ x := 120 * (7200 * t * t + 10519 * t + 3842),
          y := 391 * (7200 * t * t + 10519 * t + 3842) } : Point) := by
  let R : Int := 7200 * t * t + 10519 * t + 3842
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (14400 * t + 10519) * (14400 * t + 10519) := by
      nlinarith [sq_nonneg (14400 * t + 10519)]
    have hidentity :
        28800 * R = (14400 * t + 10519) * (14400 * t + 10519) + 239 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 28800 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 120 * R = -((360 * t + 263) * (2400 * t + 1753)) := by
    dsimp [R]
    ring
  have hy_factor : 409 * t + 302 - 391 * R = -120 * (115 * t + 84) * (204 * t + 149) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 120 * R ≠ 0 := by
    have hfirst : 360 * t + 263 ≠ 0 := by omega
    have hsecond : 2400 * t + 1753 ≠ 0 := by omega
    have hprod : -((360 * t + 263) * (2400 * t + 1753)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 409 * t + 302 - 391 * R ≠ 0 := by
    have hfirst : 115 * t + 84 ≠ 0 := by omega
    have hsecond : 204 * t + 149 ≠ 0 := by omega
    have hprod : -120 * (115 * t + 84) * (204 * t + 149) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨409 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨2944800 * t * t + 4301880 * t + 1571089, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateFourHundredTwentyTwentyNineFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 421 * t + 363 } : Point)
      ({ x := 420 * (88200 * t * t + 152069 * t + 65547),
          y := 29 * (88200 * t * t + 152069 * t + 65547) } : Point) := by
  let R : Int := 88200 * t * t + 152069 * t + 65547
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (176400 * t + 152069) * (176400 * t + 152069) := by
      nlinarith [sq_nonneg (176400 * t + 152069)]
    have hidentity :
        352800 * R = (176400 * t + 152069) * (176400 * t + 152069) + 839 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 352800 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 420 * R = -((5880 * t + 5069) * (6300 * t + 5431)) := by
    dsimp [R]
    ring
  have hy_factor : 421 * t + 363 - 29 * R = -420 * (29 * t + 25) * (210 * t + 181) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 420 * R ≠ 0 := by
    have hfirst : 5880 * t + 5069 ≠ 0 := by omega
    have hsecond : 6300 * t + 5431 ≠ 0 := by omega
    have hprod : -((5880 * t + 5069) * (6300 * t + 5431)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 421 * t + 363 - 29 * R ≠ 0 := by
    have hfirst : 29 * t + 25 ≠ 0 := by omega
    have hsecond : 210 * t + 181 ≠ 0 := by omega
    have hprod : -420 * (29 * t + 25) * (210 * t + 181) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨421 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨37132200 * t * t + 64021020 * t + 27595261, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateFourHundredEightOneHundredFortyFiveFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 433 * t + 39 } : Point)
      ({ x := 408 * (83232 * t * t + 14857 * t + 663),
          y := 145 * (83232 * t * t + 14857 * t + 663) } : Point) := by
  let R : Int := 83232 * t * t + 14857 * t + 663
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (166464 * t + 14857) * (166464 * t + 14857) := by
      nlinarith [sq_nonneg (166464 * t + 14857)]
    have hidentity :
        332928 * R = (166464 * t + 14857) * (166464 * t + 14857) + 815 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 332928 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 408 * R = -((4896 * t + 437) * (6936 * t + 619)) := by
    dsimp [R]
    ring
  have hy_factor : 433 * t + 39 - 145 * R = -24 * (493 * t + 44) * (1020 * t + 91) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 408 * R ≠ 0 := by
    have hfirst : 4896 * t + 437 ≠ 0 := by omega
    have hsecond : 6936 * t + 619 ≠ 0 := by omega
    have hprod : -((4896 * t + 437) * (6936 * t + 619)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 433 * t + 39 - 145 * R ≠ 0 := by
    have hfirst : 493 * t + 44 ≠ 0 := by omega
    have hsecond : 1020 * t + 91 ≠ 0 := by omega
    have hprod : -24 * (493 * t + 44) * (1020 * t + 91) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨433 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨36039456 * t * t + 6432936 * t + 287065, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateTwoHundredEightyThreeHundredFiftyOneFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 449 * t + 264 } : Point)
      ({ x := 280 * (39200 * t * t + 45879 * t + 13424),
          y := 351 * (39200 * t * t + 45879 * t + 13424) } : Point) := by
  let R : Int := 39200 * t * t + 45879 * t + 13424
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (78400 * t + 45879) * (78400 * t + 45879) := by
      nlinarith [sq_nonneg (78400 * t + 45879)]
    have hidentity :
        156800 * R = (78400 * t + 45879) * (78400 * t + 45879) + 559 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 156800 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 280 * R = -((1960 * t + 1147) * (5600 * t + 3277)) := by
    dsimp [R]
    ring
  have hy_factor : 449 * t + 264 - 351 * R = -280 * (135 * t + 79) * (364 * t + 213) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 280 * R ≠ 0 := by
    have hfirst : 1960 * t + 1147 ≠ 0 := by omega
    have hsecond : 5600 * t + 3277 ≠ 0 := by omega
    have hprod : -((1960 * t + 1147) * (5600 * t + 3277)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 449 * t + 264 - 351 * R ≠ 0 := by
    have hfirst : 135 * t + 79 ≠ 0 := by omega
    have hsecond : 364 * t + 213 ≠ 0 := by omega
    have hprod : -280 * (135 * t + 79) * (364 * t + 213) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨449 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨17600800 * t * t + 20599320 * t + 6027169, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateOneHundredSixtyEightFourHundredTwentyFiveFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 457 * t + 248 } : Point)
      ({ x := 168 * (14112 * t * t + 15161 * t + 4072),
          y := 425 * (14112 * t * t + 15161 * t + 4072) } : Point) := by
  let R : Int := 14112 * t * t + 15161 * t + 4072
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (28224 * t + 15161) * (28224 * t + 15161) := by
      nlinarith [sq_nonneg (28224 * t + 15161)]
    have hidentity :
        56448 * R = (28224 * t + 15161) * (28224 * t + 15161) + 335 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 56448 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 168 * R = -((672 * t + 361) * (3528 * t + 1895)) := by
    dsimp [R]
    ring
  have hy_factor : 457 * t + 248 - 425 * R = -24 * (175 * t + 94) * (1428 * t + 767) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 168 * R ≠ 0 := by
    have hfirst : 672 * t + 361 ≠ 0 := by omega
    have hsecond : 3528 * t + 1895 ≠ 0 := by omega
    have hprod : -((672 * t + 361) * (3528 * t + 1895)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 457 * t + 248 - 425 * R ≠ 0 := by
    have hfirst : 175 * t + 94 ≠ 0 := by omega
    have hsecond : 1428 * t + 767 ≠ 0 := by omega
    have hprod : -24 * (175 * t + 94) * (1428 * t + 767) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨457 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨6449184 * t * t + 6928152 * t + 1860673, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateThreeHundredEightyTwoHundredSixtyOneFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 461 * t + 373 } : Point)
      ({ x := 380 * (72200 * t * t + 116621 * t + 47093),
          y := 261 * (72200 * t * t + 116621 * t + 47093) } : Point) := by
  let R : Int := 72200 * t * t + 116621 * t + 47093
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (144400 * t + 116621) * (144400 * t + 116621) := by
      nlinarith [sq_nonneg (144400 * t + 116621)]
    have hidentity :
        288800 * R = (144400 * t + 116621) * (144400 * t + 116621) + 759 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 288800 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 380 * R = -((3800 * t + 3069) * (7220 * t + 5831)) := by
    dsimp [R]
    ring
  have hy_factor : 461 * t + 373 - 261 * R = -20 * (551 * t + 445) * (1710 * t + 1381) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 380 * R ≠ 0 := by
    have hfirst : 3800 * t + 3069 ≠ 0 := by omega
    have hsecond : 7220 * t + 5831 ≠ 0 := by omega
    have hprod : -((3800 * t + 3069) * (7220 * t + 5831)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 461 * t + 373 - 261 * R ≠ 0 := by
    have hfirst : 551 * t + 445 ≠ 0 := by omega
    have hsecond : 1710 * t + 1381 ≠ 0 := by omega
    have hprod : -20 * (551 * t + 445) * (1710 * t + 1381) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨461 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨33284200 * t * t + 53762020 * t + 21709661, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateThreeHundredSixtyThreeHundredNineteenFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 481 * t + 23 } : Point)
      ({ x := 360 * (64800 * t * t + 5959 * t + 137),
          y := 319 * (64800 * t * t + 5959 * t + 137) } : Point) := by
  let R : Int := 64800 * t * t + 5959 * t + 137
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (129600 * t + 5959) * (129600 * t + 5959) := by
      nlinarith [sq_nonneg (129600 * t + 5959)]
    have hidentity :
        259200 * R = (129600 * t + 5959) * (129600 * t + 5959) + 719 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 259200 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 360 * R = -((3240 * t + 149) * (7200 * t + 331)) := by
    dsimp [R]
    ring
  have hy_factor : 481 * t + 23 - 319 * R = -120 * (87 * t + 4) * (1980 * t + 91) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 360 * R ≠ 0 := by
    have hfirst : 3240 * t + 149 ≠ 0 := by omega
    have hsecond : 7200 * t + 331 ≠ 0 := by omega
    have hprod : -((3240 * t + 149) * (7200 * t + 331)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 481 * t + 23 - 319 * R ≠ 0 := by
    have hfirst : 87 * t + 4 ≠ 0 := by omega
    have hsecond : 1980 * t + 91 ≠ 0 := by omega
    have hprod : -120 * (87 * t + 4) * (1980 * t + 91) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨481 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨31168800 * t * t + 2865960 * t + 65881, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateOneHundredThirtyTwoFourHundredSeventyFiveFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 493 * t + 199 } : Point)
      ({ x := 132 * (8712 * t * t + 6907 * t + 1369),
          y := 475 * (8712 * t * t + 6907 * t + 1369) } : Point) := by
  let R : Int := 8712 * t * t + 6907 * t + 1369
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (17424 * t + 6907) * (17424 * t + 6907) := by
      nlinarith [sq_nonneg (17424 * t + 6907)]
    have hidentity :
        34848 * R = (17424 * t + 6907) * (17424 * t + 6907) + 263 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 34848 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 132 * R = -((396 * t + 157) * (2904 * t + 1151)) := by
    dsimp [R]
    ring
  have hy_factor : 493 * t + 199 - 475 * R = -12 * (275 * t + 109) * (1254 * t + 497) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 132 * R ≠ 0 := by
    have hfirst : 396 * t + 157 ≠ 0 := by omega
    have hsecond : 2904 * t + 1151 ≠ 0 := by omega
    have hprod : -((396 * t + 157) * (2904 * t + 1151)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 493 * t + 199 - 475 * R ≠ 0 := by
    have hfirst : 275 * t + 109 ≠ 0 := by omega
    have hsecond : 1254 * t + 497 ≠ 0 := by omega
    have hprod : -12 * (275 * t + 109) * (1254 * t + 497) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨493 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨4295016 * t * t + 3404676 * t + 674725, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateTwoHundredTwentyFourHundredFiftyNineFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 509 * t + 96 } : Point)
      ({ x := 220 * (24200 * t * t + 8931 * t + 824),
          y := 459 * (24200 * t * t + 8931 * t + 824) } : Point) := by
  let R : Int := 24200 * t * t + 8931 * t + 824
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (48400 * t + 8931) * (48400 * t + 8931) := by
      nlinarith [sq_nonneg (48400 * t + 8931)]
    have hidentity :
        96800 * R = (48400 * t + 8931) * (48400 * t + 8931) + 439 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 96800 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 220 * R = -((1100 * t + 203) * (4840 * t + 893)) := by
    dsimp [R]
    ring
  have hy_factor : 509 * t + 96 - 459 * R = -20 * (374 * t + 69) * (1485 * t + 274) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 220 * R ≠ 0 := by
    have hfirst : 1100 * t + 203 ≠ 0 := by omega
    have hsecond : 4840 * t + 893 ≠ 0 := by omega
    have hprod : -((1100 * t + 203) * (4840 * t + 893)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 509 * t + 96 - 459 * R ≠ 0 := by
    have hfirst : 374 * t + 69 ≠ 0 := by omega
    have hsecond : 1485 * t + 274 ≠ 0 := by omega
    have hprod : -20 * (374 * t + 69) * (1485 * t + 274) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨509 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨12317800 * t * t + 4545420 * t + 419329, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateFourHundredFortyTwoHundredSeventyNineFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 521 * t + 103 } : Point)
      ({ x := 440 * (96800 * t * t + 38039 * t + 3737),
          y := 279 * (96800 * t * t + 38039 * t + 3737) } : Point) := by
  let R : Int := 96800 * t * t + 38039 * t + 3737
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (193600 * t + 38039) * (193600 * t + 38039) := by
      nlinarith [sq_nonneg (193600 * t + 38039)]
    have hidentity :
        387200 * R = (193600 * t + 38039) * (193600 * t + 38039) + 879 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 387200 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 440 * R = -((4840 * t + 951) * (8800 * t + 1729)) := by
    dsimp [R]
    ring
  have hy_factor : 521 * t + 103 - 279 * R = -40 * (341 * t + 67) * (1980 * t + 389) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 440 * R ≠ 0 := by
    have hfirst : 4840 * t + 951 ≠ 0 := by omega
    have hsecond : 8800 * t + 1729 ≠ 0 := by omega
    have hprod : -((4840 * t + 951) * (8800 * t + 1729)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 521 * t + 103 - 279 * R ≠ 0 := by
    have hfirst : 341 * t + 67 ≠ 0 := by omega
    have hsecond : 1980 * t + 389 ≠ 0 := by omega
    have hprod : -40 * (341 * t + 67) * (1980 * t + 389) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨521 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨50432800 * t * t + 19818040 * t + 1946921, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateNinetyTwoFiveHundredTwentyFiveFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 533 * t + 78 } : Point)
      ({ x := 92 * (4232 * t * t + 1149 * t + 78),
          y := 525 * (4232 * t * t + 1149 * t + 78) } : Point) := by
  let R : Int := 4232 * t * t + 1149 * t + 78
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (8464 * t + 1149) * (8464 * t + 1149) := by
      nlinarith [sq_nonneg (8464 * t + 1149)]
    have hidentity :
        16928 * R = (8464 * t + 1149) * (8464 * t + 1149) + 183 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 16928 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 92 * R = -((184 * t + 25) * (2116 * t + 287)) := by
    dsimp [R]
    ring
  have hy_factor : 533 * t + 78 - 525 * R = -4 * (575 * t + 78) * (966 * t + 131) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 92 * R ≠ 0 := by
    have hfirst : 184 * t + 25 ≠ 0 := by omega
    have hsecond : 2116 * t + 287 ≠ 0 := by omega
    have hprod : -((184 * t + 25) * (2116 * t + 287)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 533 * t + 78 - 525 * R ≠ 0 := by
    have hfirst : 575 * t + 78 ≠ 0 := by omega
    have hsecond : 966 * t + 131 ≠ 0 := by omega
    have hprod : -4 * (575 * t + 78) * (966 * t + 131) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨533 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨2255656 * t * t + 611892 * t + 41497, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateFourHundredTwentyThreeHundredFortyOneFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 541 * t + 113 } : Point)
      ({ x := 420 * (88200 * t * t + 36581 * t + 3793),
          y := 341 * (88200 * t * t + 36581 * t + 3793) } : Point) := by
  let R : Int := 88200 * t * t + 36581 * t + 3793
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (176400 * t + 36581) * (176400 * t + 36581) := by
      nlinarith [sq_nonneg (176400 * t + 36581)]
    have hidentity :
        352800 * R = (176400 * t + 36581) * (176400 * t + 36581) + 839 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 352800 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 420 * R = -((4200 * t + 871) * (8820 * t + 1829)) := by
    dsimp [R]
    ring
  have hy_factor : 541 * t + 113 - 341 * R = -60 * (217 * t + 45) * (2310 * t + 479) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 420 * R ≠ 0 := by
    have hfirst : 4200 * t + 871 ≠ 0 := by omega
    have hsecond : 8820 * t + 1829 ≠ 0 := by omega
    have hprod : -((4200 * t + 871) * (8820 * t + 1829)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 541 * t + 113 - 341 * R ≠ 0 := by
    have hfirst : 217 * t + 45 ≠ 0 := by omega
    have hsecond : 2310 * t + 479 ≠ 0 := by omega
    have hprod : -60 * (217 * t + 45) * (2310 * t + 479) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨541 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨47716200 * t * t + 19789980 * t + 2051941, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateFiveHundredThirtyTwoOneHundredSixtyFiveFactorOneParallel
    {t : Int} :
    certificateValid
      ({ x := 1, y := 557 * t + 412 } : Point)
      ({ x := 532 * (141512 * t * t + 209189 * t + 77308),
          y := 165 * (141512 * t * t + 209189 * t + 77308) } : Point) := by
  let R : Int := 141512 * t * t + 209189 * t + 77308
  have hR_ne : R ≠ 0 := by
    have hsquare : 0 ≤ (283024 * t + 209189) * (283024 * t + 209189) := by
      nlinarith [sq_nonneg (283024 * t + 209189)]
    have hidentity :
        566048 * R = (283024 * t + 209189) * (283024 * t + 209189) + 1063 := by
      dsimp [R]
      ring
    intro hR
    have hpositive : 0 < 566048 * R := by nlinarith
    rw [hR] at hpositive
    norm_num at hpositive
  have hx_factor : 1 - 532 * R = -((7448 * t + 5505) * (10108 * t + 7471)) := by
    dsimp [R]
    ring
  have hy_factor : 557 * t + 412 - 165 * R = -4 * (1330 * t + 983) * (4389 * t + 3244) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 532 * R ≠ 0 := by
    have hfirst : 7448 * t + 5505 ≠ 0 := by omega
    have hsecond : 10108 * t + 7471 ≠ 0 := by omega
    have hprod : -((7448 * t + 5505) * (10108 * t + 7471)) ≠ 0 := by
      exact neg_ne_zero.mpr (mul_ne_zero hfirst hsecond)
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 557 * t + 412 - 165 * R ≠ 0 := by
    have hfirst : 1330 * t + 983 ≠ 0 := by omega
    have hsecond : 4389 * t + 3244 ≠ 0 := by omega
    have hprod : -4 * (1330 * t + 983) * (4389 * t + 3244) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨557 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨78822184 * t * t + 116518108 * t + 43060433, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem certificateValid_unitCoordinateFifteenEightFactorTwoParallel {t : Int} :
    certificateValid
      ({ x := 1, y := 34 * t + 26 } : Point)
      ({ x := 15 * (225 * t * t + 338 * t + 127),
          y := 8 * (225 * t * t + 338 * t + 127) } : Point) := by
  let R : Int := 225 * t * t + 338 * t + 127
  have hR_pos : 0 < R := by
    have hsquare : 0 ≤ (450 * t + 338) * (450 * t + 338) := by
      nlinarith [sq_nonneg (450 * t + 338)]
    have hidentity : 900 * R = (450 * t + 338) * (450 * t + 338) + 56 := by
      dsimp [R]
      ring
    nlinarith
  have hR_ne : R ≠ 0 := ne_of_gt hR_pos
  have hx_factor : 1 - 15 * R = -1 * (45 * t + 34) * (75 * t + 56) := by
    dsimp [R]
    ring
  have hy_factor : 34 * t + 26 - 8 * R = -30 * (4 * t + 3) * (15 * t + 11) := by
    dsimp [R]
    ring
  have hx_nonzero : 1 - 15 * R ≠ 0 := by
    have hfirst : 45 * t + 34 ≠ 0 := by omega
    have hsecond : 75 * t + 56 ≠ 0 := by omega
    have hprod : -1 * (45 * t + 34) * (75 * t + 56) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hx
    apply hprod
    exact hx_factor.symm.trans hx
  have hy_nonzero : 34 * t + 26 - 8 * R ≠ 0 := by
    have hfirst : 4 * t + 3 ≠ 0 := by omega
    have hsecond : 15 * t + 11 ≠ 0 := by omega
    have hprod : -30 * (4 * t + 3) * (15 * t + 11) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hy
    apply hprod
    exact hy_factor.symm.trans hy
  constructor
  · constructor
    · exact ⟨mul_ne_zero (by norm_num) hR_ne, mul_ne_zero (by norm_num) hR_ne⟩
    · refine ⟨17 * R, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hx_nonzero
      · simpa [sub, R, mul_comm, mul_left_comm, mul_assoc] using hy_nonzero
    · refine ⟨3825 * t * t + 5730 * t + 2146, ?_⟩
      simp [normSq, sub, sq]
      ring

theorem sub_add_smul_smul (r s : Int) (u v : Point) :
    sub (add (smul r u) (smul s v)) (smul r u) = smul s v := by
  ext <;> simp [sub, add, smul]

theorem det_add_smul_smul (strip u v : Point) (r s : Int) :
    det strip (add (smul r u) (smul s v)) =
      r * det strip u + s * det strip v := by
  simp [det, add, smul]
  ring

theorem det_add_smul_line (strip u w : Point) (r : Int) :
    det strip (add (smul r u) w) =
      r * det strip u + det strip w := by
  simp [det, add, smul]
  ring

theorem lineStripRowValid {strip direction secondStep : Point}
    {r paired pairedResidue pairedModulus stripResidue stripModulus : Int}
    (hline :
      certificateValid (add (smul r direction) secondStep) (smul r direction))
    (hpaired : paired ≡ pairedResidue [ZMOD pairedModulus])
    (hcoeff :
      det strip direction * r + det strip secondStep ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid (add (smul r direction) secondStep) (smul r direction) ∧
      det strip (add (smul r direction) secondStep) ≡
        stripResidue [ZMOD stripModulus] ∧
      paired ≡ pairedResidue [ZMOD pairedModulus] := by
  refine ⟨hline, ?_, hpaired⟩
  calc
    det strip (add (smul r direction) secondStep)
        = r * det strip direction + det strip secondStep :=
          det_add_smul_line strip direction secondStep r
    _ = det strip direction * r + det strip secondStep := by ring
    _ ≡ stripResidue [ZMOD stripModulus] := hcoeff

theorem lineStripCertificateValid {strip direction secondStep : Point}
    {r paired pairedResidue pairedModulus stripResidue stripModulus : Int}
    (hr : r ≠ 0)
    (hdirection : legalStep direction)
    (hsecondStep : legalStep secondStep)
    (hpaired : paired ≡ pairedResidue [ZMOD pairedModulus])
    (hcoeff :
      det strip direction * r + det strip secondStep ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid (add (smul r direction) secondStep) (smul r direction) ∧
      det strip (add (smul r direction) secondStep) ≡
        stripResidue [ZMOD stripModulus] ∧
      paired ≡ pairedResidue [ZMOD pairedModulus] := by
  have hsub :
      sub (add (smul r direction) secondStep) (smul r direction) =
        secondStep := by
    ext <;> simp [sub, add, smul]
  have hline :
      certificateValid (add (smul r direction) secondStep) (smul r direction) := by
    constructor
    · exact legalStep_smul hr hdirection
    · rw [hsub]
      exact hsecondStep
  exact lineStripRowValid hline hpaired hcoeff

theorem latticeStripLinearCongruence {target strip u v : Point}
    {r s residue modulus : Int}
    (htarget : target = add (smul r u) (smul s v)) :
    det strip target ≡ residue [ZMOD modulus] ↔
      det strip u * r + det strip v * s ≡ residue [ZMOD modulus] := by
  subst target
  rw [det_add_smul_smul]
  ring_nf

theorem latticePairSameStripLinearCongruence {target strip u v : Point}
    {r s residueM residueN m n : Int}
    (htarget : target = add (smul r u) (smul s v)) :
    (det strip target ≡ residueM [ZMOD m] ∧
      det strip target ≡ residueN [ZMOD n]) ↔
      (det strip u * r + det strip v * s ≡ residueM [ZMOD m] ∧
        det strip u * r + det strip v * s ≡ residueN [ZMOD n]) := by
  constructor
  · intro h
    exact
      ⟨(latticeStripLinearCongruence (target := target) (strip := strip)
          (u := u) (v := v) (r := r) (s := s) htarget).mp h.1,
        (latticeStripLinearCongruence (target := target) (strip := strip)
          (u := u) (v := v) (r := r) (s := s) htarget).mp h.2⟩
  · intro h
    exact
      ⟨(latticeStripLinearCongruence (target := target) (strip := strip)
          (u := u) (v := v) (r := r) (s := s) htarget).mpr h.1,
        (latticeStripLinearCongruence (target := target) (strip := strip)
          (u := u) (v := v) (r := r) (s := s) htarget).mpr h.2⟩

theorem modEq_lcm_of_modEq_pair {x y m n : Int}
    (hm : x ≡ y [ZMOD m]) (hn : x ≡ y [ZMOD n]) :
    x ≡ y [ZMOD (m.lcm n : Int)] := by
  rcases Int.modEq_iff_dvd.mp hm with ⟨km, hkm⟩
  rcases Int.modEq_iff_dvd.mp hn with ⟨kn, hkn⟩
  apply Int.modEq_iff_dvd.mpr
  have hm_abs : m ∣ ↑(y - x).natAbs := by
    rw [Int.dvd_natAbs]
    exact ⟨km, hkm⟩
  have hn_abs : n ∣ ↑(y - x).natAbs := by
    rw [Int.dvd_natAbs]
    exact ⟨kn, hkn⟩
  have hlcm_nat : m.lcm n ∣ (y - x).natAbs := Int.lcm_dvd hm_abs hn_abs
  have hlcm_int : (m.lcm n : Int) ∣ ↑(y - x).natAbs := by
    exact_mod_cast hlcm_nat
  exact Int.dvd_natAbs.mp hlcm_int

theorem latticePairSameStripCombinedLinearCongruence {target strip u v : Point}
    {r s residueM residueN m n x : Int}
    (htarget : target = add (smul r u) (smul s v))
    (hxm : x ≡ residueM [ZMOD m]) (hxn : x ≡ residueN [ZMOD n]) :
    (det strip target ≡ residueM [ZMOD m] ∧
      det strip target ≡ residueN [ZMOD n]) ↔
      det strip u * r + det strip v * s ≡ x [ZMOD (m.lcm n : Int)] := by
  let y := det strip u * r + det strip v * s
  constructor
  · intro h
    have hcoeff :
        y ≡ residueM [ZMOD m] ∧ y ≡ residueN [ZMOD n] := by
      simpa [y] using
        (latticePairSameStripLinearCongruence (target := target) (strip := strip)
          (u := u) (v := v) (r := r) (s := s)
          (residueM := residueM) (residueN := residueN)
          (m := m) (n := n) htarget).mp h
    exact modEq_lcm_of_modEq_pair (hcoeff.1.trans hxm.symm)
      (hcoeff.2.trans hxn.symm)
  · intro h
    have hcoeff :
        y ≡ residueM [ZMOD m] ∧ y ≡ residueN [ZMOD n] := by
      constructor
      · exact (Int.ModEq.of_dvd (Int.dvd_lcm_left m n) h).trans hxm
      · exact (Int.ModEq.of_dvd (Int.dvd_lcm_right m n) h).trans hxn
    exact
      (latticePairSameStripLinearCongruence (target := target) (strip := strip)
        (u := u) (v := v) (r := r) (s := s)
        (residueM := residueM) (residueN := residueN)
        (m := m) (n := n) htarget).mpr (by simpa [y] using hcoeff)

theorem exists_latticePairSameStripCombinedLinearCongruence
    {strip u v : Point} {residueM residueN m n x : Int}
    (hxm : x ≡ residueM [ZMOD m]) (hxn : x ≡ residueN [ZMOD n]) :
    (∃ r s : Int,
        det strip (add (smul r u) (smul s v)) ≡ residueM [ZMOD m] ∧
          det strip (add (smul r u) (smul s v)) ≡ residueN [ZMOD n]) ↔
      ∃ r s : Int,
        det strip u * r + det strip v * s ≡ x [ZMOD (m.lcm n : Int)] := by
  constructor
  · rintro ⟨r, s, h⟩
    refine ⟨r, s, ?_⟩
    exact (latticePairSameStripCombinedLinearCongruence
      (target := add (smul r u) (smul s v)) (strip := strip)
      (u := u) (v := v) (r := r) (s := s)
      (residueM := residueM) (residueN := residueN)
      (m := m) (n := n) (x := x) rfl hxm hxn).mp h
  · rintro ⟨r, s, h⟩
    refine ⟨r, s, ?_⟩
    exact (latticePairSameStripCombinedLinearCongruence
      (target := add (smul r u) (smul s v)) (strip := strip)
      (u := u) (v := v) (r := r) (s := s)
      (residueM := residueM) (residueN := residueN)
      (m := m) (n := n) (x := x) rfl hxm hxn).mpr h

theorem cramerTarget_eq_add_smul {target u v : Point} {r s : Int}
    (hdet : det u v ≠ 0)
    (hr : det target v = r * det u v)
    (hs : det u target = s * det u v) :
    target = add (smul r u) (smul s v) := by
  ext
  · change target.x = r * u.x + s * v.x
    apply mul_right_cancel₀ hdet
    calc
      target.x * det u v = det target v * u.x + det u target * v.x := by
        simp [det]
        ring
      _ = (r * det u v) * u.x + (s * det u v) * v.x := by rw [hr, hs]
      _ = (r * u.x + s * v.x) * det u v := by ring
  · change target.y = r * u.y + s * v.y
    apply mul_right_cancel₀ hdet
    calc
      target.y * det u v = det target v * u.y + det u target * v.y := by
        simp [det]
        ring
      _ = (r * det u v) * u.y + (s * det u v) * v.y := by rw [hr, hs]
      _ = (r * u.y + s * v.y) * det u v := by ring

theorem det_add_smul_smul_right (u v : Point) (r s : Int) :
    det (add (smul r u) (smul s v)) v = r * det u v := by
  simp [det, add, smul]
  ring

theorem det_left_add_smul_smul (u v : Point) (r s : Int) :
    det u (add (smul r u) (smul s v)) = s * det u v := by
  simp [det, add, smul]
  ring

theorem latticeCoefficients_cramer {target u v : Point} {r s : Int}
    (hdet : det u v ≠ 0) :
    target = add (smul r u) (smul s v) ↔
      det target v = r * det u v ∧ det u target = s * det u v := by
  constructor
  · intro htarget
    subst target
    exact ⟨det_add_smul_smul_right u v r s,
      det_left_add_smul_smul u v r s⟩
  · intro h
    exact cramerTarget_eq_add_smul hdet h.1 h.2

theorem exists_latticeCoefficients_iff_cramer_dvd {target u v : Point}
    (hdet : det u v ≠ 0) :
    (∃ r s : Int, target = add (smul r u) (smul s v)) ↔
      det u v ∣ det target v ∧ det u v ∣ det u target := by
  constructor
  · rintro ⟨r, s, htarget⟩
    have hcramer :
        det target v = r * det u v ∧ det u target = s * det u v :=
      (latticeCoefficients_cramer (target := target) (u := u) (v := v)
        (r := r) (s := s) hdet).mp htarget
    constructor
    · refine ⟨r, ?_⟩
      rw [hcramer.1]
      ring
    · refine ⟨s, ?_⟩
      rw [hcramer.2]
      ring
  · rintro ⟨hrdvd, hsdvd⟩
    rcases hrdvd with ⟨r, hr⟩
    rcases hsdvd with ⟨s, hs⟩
    refine ⟨r, s, cramerTarget_eq_add_smul hdet ?_ ?_⟩
    · rw [hr]
      ring
    · rw [hs]
      ring

theorem latticeCertificateValid {r s : Int} {u v : Point}
    (hr : r ≠ 0) (hs : s ≠ 0)
    (hu : legalStep u) (hv : legalStep v) :
    certificateValid (add (smul r u) (smul s v)) (smul r u) := by
  constructor
  · exact legalStep_smul hr hu
  · simpa [sub_add_smul_smul] using legalStep_smul hs hv

theorem latticeCertificateValid_of_cramer {target u v : Point} {r s : Int}
    (hdet : det u v ≠ 0)
    (hr : det target v = r * det u v)
    (hs : det u target = s * det u v)
    (hr_nonzero : r ≠ 0) (hs_nonzero : s ≠ 0)
    (hu : legalStep u) (hv : legalStep v) :
    certificateValid target (smul r u) := by
  rw [cramerTarget_eq_add_smul hdet hr hs]
  exact latticeCertificateValid hr_nonzero hs_nonzero hu hv

theorem certificateValid_latticeMidpointData {target midpoint u v : Point} {r s : Int}
    (hmidpoint : midpoint = smul r u)
    (hdet : det u v ≠ 0)
    (hr : det target v = r * det u v)
    (hs : det u target = s * det u v)
    (hr_nonzero : r ≠ 0) (hs_nonzero : s ≠ 0)
    (hu : legalStep u) (hv : legalStep v) :
    certificateValid target midpoint := by
  subst midpoint
  exact latticeCertificateValid_of_cramer hdet hr hs
    hr_nonzero hs_nonzero hu hv

theorem exists_latticeCertificateValid_of_cramer {target u v : Point}
    (hdet : det u v ≠ 0)
    (hr : ∃ r : Int, det target v = r * det u v ∧ r ≠ 0)
    (hs : ∃ s : Int, det u target = s * det u v ∧ s ≠ 0)
    (hu : legalStep u) (hv : legalStep v) :
    ∃ midpoint : Point, certificateValid target midpoint := by
  rcases hr with ⟨r, hr_eq, hr_nonzero⟩
  rcases hs with ⟨s, hs_eq, hs_nonzero⟩
  exact ⟨smul r u, latticeCertificateValid_of_cramer hdet hr_eq hs_eq
    hr_nonzero hs_nonzero hu hv⟩

theorem exists_latticeCertificateValid_of_cramer_dvd_nondegenerate
    {target u v : Point}
    (hdet : det u v ≠ 0)
    (hrdvd : det u v ∣ det target v)
    (hsdvd : det u v ∣ det u target)
    (hr_nonzero : det target v ≠ 0)
    (hs_nonzero : det u target ≠ 0)
    (hu : legalStep u) (hv : legalStep v) :
    ∃ midpoint : Point, certificateValid target midpoint := by
  rcases hrdvd with ⟨r, hr⟩
  rcases hsdvd with ⟨s, hs⟩
  have hr_eq : det target v = r * det u v := by
    rw [hr]
    ring
  have hs_eq : det u target = s * det u v := by
    rw [hs]
    ring
  have hr_coeff_nonzero : r ≠ 0 := by
    intro hzero
    apply hr_nonzero
    rw [hr_eq, hzero]
    ring
  have hs_coeff_nonzero : s ≠ 0 := by
    intro hzero
    apply hs_nonzero
    rw [hs_eq, hzero]
    ring
  exact exists_latticeCertificateValid_of_cramer hdet
    ⟨r, hr_eq, hr_coeff_nonzero⟩
    ⟨s, hs_eq, hs_coeff_nonzero⟩ hu hv

theorem normSq_mul_normSq_sub_smul (target u : Point) (r : Int) :
    normSq u * normSq (sub target (smul r u)) =
      sq (r * normSq u - dot target u) + sq (det u target) := by
  simp [normSq, sub, smul, dot, det, sq]
  ring

theorem normSq_sub_smul_of_parallelFactor {target u : Point}
    {c r otherLeg secondLength : Int}
    (hc : c ≠ 0)
    (hu_norm : normSq u = c * c)
    (hother : r * c * c - dot target u = otherLeg)
    (hcompletion :
      sq otherLeg + sq (det u target) = c * c * (secondLength * secondLength)) :
    normSq (sub target (smul r u)) = secondLength * secondLength := by
  have hc_sq : c * c ≠ 0 := mul_ne_zero hc hc
  have hother_assoc : r * (c * c) - dot target u = otherLeg := by
    rw [← hother]
    ring
  apply mul_left_cancel₀ hc_sq
  calc
    c * c * normSq (sub target (smul r u))
        = normSq u * normSq (sub target (smul r u)) := by rw [hu_norm]
    _ = sq (r * normSq u - dot target u) + sq (det u target) :=
        normSq_mul_normSq_sub_smul target u r
    _ = sq otherLeg + sq (det u target) := by rw [hu_norm, hother_assoc]
    _ = c * c * (secondLength * secondLength) := hcompletion

theorem isIntSquare_sub_smul_of_parallelFactor {target u : Point}
    {c r otherLeg secondLength : Int}
    (hc : c ≠ 0)
    (hu_norm : normSq u = c * c)
    (hother : r * c * c - dot target u = otherLeg)
    (hcompletion :
      sq otherLeg + sq (det u target) = c * c * (secondLength * secondLength)) :
    isIntSquare (normSq (sub target (smul r u))) := by
  exact ⟨secondLength, normSq_sub_smul_of_parallelFactor hc hu_norm hother hcompletion⟩

theorem sq_add_sq_of_factorPair {detValue factor paired otherLeg scaledHypotenuse : Int}
    (hprod : sq detValue = factor * paired)
    (hsum : factor + paired = 2 * scaledHypotenuse)
    (hdiff : paired - factor = 2 * otherLeg) :
    sq otherLeg + sq detValue = scaledHypotenuse * scaledHypotenuse := by
  have hfour : (4 : Int) ≠ 0 := by norm_num
  apply mul_left_cancel₀ hfour
  calc
    4 * (sq otherLeg + sq detValue)
        = (2 * otherLeg) * (2 * otherLeg) + 4 * sq detValue := by
          simp [sq]
          ring
    _ = (paired - factor) * (paired - factor) + 4 * (factor * paired) := by
      rw [← hdiff, hprod]
    _ = (factor + paired) * (factor + paired) := by ring
    _ = (2 * scaledHypotenuse) * (2 * scaledHypotenuse) := by rw [hsum]
    _ = 4 * (scaledHypotenuse * scaledHypotenuse) := by ring

theorem parallelFactorCompletion_of_factorPair {target u : Point}
    {c factor paired otherLeg scaledHypotenuse secondLength : Int}
    (hprod : sq (det u target) = factor * paired)
    (hsum : factor + paired = 2 * scaledHypotenuse)
    (hdiff : paired - factor = 2 * otherLeg)
    (hscaled : scaledHypotenuse = c * secondLength) :
    sq otherLeg + sq (det u target) = c * c * (secondLength * secondLength) := by
  calc
    sq otherLeg + sq (det u target)
        = scaledHypotenuse * scaledHypotenuse :=
            sq_add_sq_of_factorPair hprod hsum hdiff
    _ = c * c * (secondLength * secondLength) := by
      rw [hscaled]
      ring

theorem parallelFactorCertificateValid_of_nondegenerate {target u : Point}
    {c r otherLeg secondLength : Int}
    (hr : r ≠ 0)
    (hc : c ≠ 0)
    (hu : legalStep u)
    (hu_norm : normSq u = c * c)
    (hother : r * c * c - dot target u = otherLeg)
    (hcompletion :
      sq otherLeg + sq (det u target) = c * c * (secondLength * secondLength))
    (hsecond_nonAxis : nonAxis (sub target (smul r u))) :
    certificateValid target (smul r u) := by
  constructor
  · exact legalStep_smul hr hu
  · constructor
    · exact hsecond_nonAxis
    · exact isIntSquare_sub_smul_of_parallelFactor hc hu_norm hother hcompletion

theorem parallelFactorCertificateValid_of_factorPair {target u : Point}
    {c r factor paired otherLeg scaledHypotenuse secondLength : Int}
    (hr : r ≠ 0)
    (hc : c ≠ 0)
    (hu : legalStep u)
    (hu_norm : normSq u = c * c)
    (hprod : sq (det u target) = factor * paired)
    (hsum : factor + paired = 2 * scaledHypotenuse)
    (hdiff : paired - factor = 2 * otherLeg)
    (hscaled : scaledHypotenuse = c * secondLength)
    (hother : r * c * c - dot target u = otherLeg)
    (hsecond_nonAxis : nonAxis (sub target (smul r u))) :
    certificateValid target (smul r u) := by
  exact parallelFactorCertificateValid_of_nondegenerate hr hc hu hu_norm hother
    (parallelFactorCompletion_of_factorPair hprod hsum hdiff hscaled)
    hsecond_nonAxis

theorem parallelFactorCertificateValid_of_factorPairRow {target u : Point}
    {c r factor paired secondLength : Int}
    (hr : r ≠ 0)
    (hc : c ≠ 0)
    (hu : legalStep u)
    (hu_norm : normSq u = c * c)
    (hprod : sq (det u target) = factor * paired)
    (hsum : factor + paired = 2 * (c * secondLength))
    (hcoefficient :
      paired - factor + 2 * dot target u = 2 * (r * c * c))
    (hsecond_nonAxis : nonAxis (sub target (smul r u))) :
    certificateValid target (smul r u) := by
  let otherLeg : Int := r * c * c - dot target u
  have hdiff : paired - factor = 2 * otherLeg := by
    dsimp [otherLeg]
    calc
      paired - factor =
          (paired - factor + 2 * dot target u) - 2 * dot target u := by ring
      _ = 2 * (r * c * c) - 2 * dot target u := by rw [hcoefficient]
      _ = 2 * (r * c * c - dot target u) := by ring
  have hother : r * c * c - dot target u = otherLeg := rfl
  exact parallelFactorCertificateValid_of_factorPair
    (target := target) (u := u) (c := c) (r := r)
    (factor := factor) (paired := paired) (otherLeg := otherLeg)
    (scaledHypotenuse := c * secondLength) (secondLength := secondLength)
    hr hc hu hu_norm hprod (by simpa using hsum) hdiff rfl hother
    hsecond_nonAxis

def parallelFactorCongruenceData
    (target u : Point) (c factor secondLength r : Int) : Prop :=
  sq (det u target) + sq factor = 2 * c * factor * secondLength ∧
    sq (det u target) - sq factor + 2 * factor * dot target u =
      2 * factor * c * c * r

def parallelFactorCongruence (target u : Point) (c factor : Int) : Prop :=
  det u target ≠ 0 ∧
    ∃ secondLength r : Int,
      parallelFactorCongruenceData target u c factor secondLength r

theorem parallelFactorCongruenceData_of_factorPairRow {target u : Point}
    {c r factor paired secondLength : Int}
    (hprod : sq (det u target) = factor * paired)
    (hsum : factor + paired = 2 * (c * secondLength))
    (hcoefficient :
      paired - factor + 2 * dot target u = 2 * (r * c * c)) :
    parallelFactorCongruenceData target u c factor secondLength r := by
  constructor
  · calc
      sq (det u target) + sq factor = factor * paired + factor * factor := by
        rw [hprod]
        simp [sq]
      _ = factor * (factor + paired) := by ring
      _ = factor * (2 * (c * secondLength)) := by rw [hsum]
      _ = 2 * c * factor * secondLength := by ring
  · calc
      sq (det u target) - sq factor + 2 * factor * dot target u =
          factor * (paired - factor + 2 * dot target u) := by
        rw [hprod]
        simp [sq]
        ring
      _ = factor * (2 * (r * c * c)) := by rw [hcoefficient]
      _ = 2 * factor * c * c * r := by ring

theorem factorPairRow_of_parallelFactorCongruenceData {target u : Point}
    {c r factor paired secondLength : Int}
    (hfactor : factor ≠ 0)
    (hprod : sq (det u target) = factor * paired)
    (hdata : parallelFactorCongruenceData target u c factor secondLength r) :
    factor + paired = 2 * (c * secondLength) ∧
      paired - factor + 2 * dot target u = 2 * (r * c * c) := by
  rcases hdata with ⟨hsumData, hcoefficientData⟩
  constructor
  · apply mul_left_cancel₀ hfactor
    calc
      factor * (factor + paired) = factor * paired + factor * factor := by ring
      _ = sq (det u target) + sq factor := by
        rw [hprod]
        simp [sq]
      _ = 2 * c * factor * secondLength := hsumData
      _ = factor * (2 * (c * secondLength)) := by ring
  · apply mul_left_cancel₀ hfactor
    calc
      factor * (paired - factor + 2 * dot target u) =
          factor * paired - factor * factor + 2 * factor * dot target u := by ring
      _ = sq (det u target) - sq factor + 2 * factor * dot target u := by
        rw [hprod]
        simp [sq]
      _ = 2 * factor * c * c * r := hcoefficientData
      _ = factor * (2 * (r * c * c)) := by ring

theorem parallelFactorCongruence_of_factorPairRow {target u : Point}
    {c r factor paired secondLength : Int}
    (hdet : det u target ≠ 0)
    (hprod : sq (det u target) = factor * paired)
    (hsum : factor + paired = 2 * (c * secondLength))
    (hcoefficient :
      paired - factor + 2 * dot target u = 2 * (r * c * c)) :
    parallelFactorCongruence target u c factor := by
  exact ⟨hdet, secondLength, r,
    parallelFactorCongruenceData_of_factorPairRow hprod hsum hcoefficient⟩

theorem parallelFactorCertificateValid_of_congruenceData_factorPair
    {target u : Point}
    {c r factor paired secondLength : Int}
    (hr : r ≠ 0)
    (hc : c ≠ 0)
    (hfactor : factor ≠ 0)
    (hu : legalStep u)
    (hu_norm : normSq u = c * c)
    (hprod : sq (det u target) = factor * paired)
    (hdata : parallelFactorCongruenceData target u c factor secondLength r)
    (hsecond_nonAxis : nonAxis (sub target (smul r u))) :
    certificateValid target (smul r u) := by
  rcases factorPairRow_of_parallelFactorCongruenceData hfactor hprod hdata with
    ⟨hsum, hcoefficient⟩
  exact parallelFactorCertificateValid_of_factorPairRow
    (target := target) (u := u) (c := c) (r := r)
    (factor := factor) (paired := paired) (secondLength := secondLength)
    hr hc hu hu_norm hprod hsum hcoefficient hsecond_nonAxis

theorem dot_modEq_det_mul_left_inverse {target u : Point} {inv : Int}
    (hinv : u.x * inv ≡ 1 [ZMOD normSq u]) :
    dot target u ≡ u.y * inv * det u target [ZMOD normSq u] := by
  have hbasic :
      u.x * dot target u ≡ u.y * det u target [ZMOD normSq u] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-target.x, ?_⟩
    simp [dot, det, normSq, sq]
    ring
  have hleft :
      dot target u ≡ inv * (u.x * dot target u) [ZMOD normSq u] := by
    have h := Int.ModEq.mul hinv
      (Int.ModEq.refl (n := normSq u) (dot target u))
    simpa [mul_assoc, mul_comm, mul_left_comm] using h.symm
  have hright :
      inv * (u.x * dot target u) ≡
        u.y * inv * det u target [ZMOD normSq u] := by
    have h := Int.ModEq.mul (Int.ModEq.refl (n := normSq u) inv) hbasic
    simpa [mul_assoc, mul_comm, mul_left_comm] using h
  exact hleft.trans hright

theorem crtModEq_compat {x a b m n : Int}
    (hxm : x ≡ a [ZMOD m]) (hxn : x ≡ b [ZMOD n]) :
    a ≡ b [ZMOD (m.gcd n : Int)] := by
  have hgm : x ≡ a [ZMOD (m.gcd n : Int)] :=
    Int.ModEq.of_dvd (Int.gcd_dvd_left m n) hxm
  have hgn : x ≡ b [ZMOD (m.gcd n : Int)] :=
    Int.ModEq.of_dvd (Int.gcd_dvd_right m n) hxn
  exact hgm.symm.trans hgn

theorem exists_int_crt_of_gcd_modEq {a b m n : Int}
    (hcompat : a ≡ b [ZMOD (m.gcd n : Int)]) :
    ∃ x : Int, x ≡ a [ZMOD m] ∧ x ≡ b [ZMOD n] := by
  rcases Int.modEq_iff_dvd.mp hcompat with ⟨k, hk⟩
  let A := m.gcdA n
  let B := m.gcdB n
  let x := a + m * A * k
  refine ⟨x, ?_, ?_⟩
  · apply Int.modEq_iff_dvd.mpr
    refine ⟨-(A * k), ?_⟩
    simp [x]
    ring
  · apply Int.modEq_iff_dvd.mpr
    refine ⟨B * k, ?_⟩
    have hbez : (m.gcd n : Int) = m * A + n * B := by
      simpa [A, B] using Int.gcd_eq_gcd_ab m n
    calc
      b - x = (b - a) - m * A * k := by
        simp [x]
        ring
      _ = (m.gcd n : Int) * k - m * A * k := by rw [hk]
      _ = (m * A + n * B) * k - m * A * k := by rw [hbez]
      _ = n * (B * k) := by ring

theorem exists_twoVariableLinearCongruence_of_gcd_dvd
    {a b residue modulus : Int}
    (hdiv : (((a.gcd b : Int).gcd modulus : Int) ∣ residue)) :
    ∃ r s : Int, a * r + b * s ≡ residue [ZMOD modulus] := by
  rcases hdiv with ⟨k, hk⟩
  let gab : Int := (a.gcd b : Int)
  let A := a.gcdA b
  let B := a.gcdB b
  let C := gab.gcdA modulus
  let D := gab.gcdB modulus
  refine ⟨A * C * k, B * C * k, ?_⟩
  apply Int.modEq_iff_dvd.mpr
  refine ⟨D * k, ?_⟩
  have hab : gab = a * A + b * B := by
    simpa [gab, A, B] using Int.gcd_eq_gcd_ab a b
  have hg : ((gab.gcd modulus : Int)) = gab * C + modulus * D := by
    simpa [C, D] using Int.gcd_eq_gcd_ab gab modulus
  have hg_eq : (((a.gcd b : Int).gcd modulus : Int)) = gab * C + modulus * D := by
    simpa [gab] using hg
  calc
    residue - (a * (A * C * k) + b * (B * C * k))
        = ((a.gcd b : Int).gcd modulus : Int) * k -
            (a * (A * C * k) + b * (B * C * k)) := by rw [hk]
    _ = (gab * C + modulus * D) * k -
            (a * (A * C * k) + b * (B * C * k)) := by rw [hg_eq]
    _ = ((a * A + b * B) * C + modulus * D) * k -
            (a * (A * C * k) + b * (B * C * k)) := by rw [← hab]
    _ = modulus * (D * k) := by ring

theorem twoVariableLinearCongruence_gcd_dvd
    {a b residue modulus r s : Int}
    (hcong : a * r + b * s ≡ residue [ZMOD modulus]) :
    (((a.gcd b : Int).gcd modulus : Int) ∣ residue) := by
  let g : Int := ((a.gcd b : Int).gcd modulus : Int)
  rcases Int.modEq_iff_dvd.mp hcong with ⟨k, hk⟩
  have hg_gab : g ∣ (a.gcd b : Int) := by
    simpa [g] using Int.gcd_dvd_left (a.gcd b : Int) modulus
  have hg_a : g ∣ a :=
    dvd_trans hg_gab (Int.gcd_dvd_left a b)
  have hg_b : g ∣ b :=
    dvd_trans hg_gab (Int.gcd_dvd_right a b)
  have hg_modulus : g ∣ modulus := by
    simpa [g] using Int.gcd_dvd_right (a.gcd b : Int) modulus
  have hg_linear : g ∣ a * r + b * s :=
    dvd_add (dvd_mul_of_dvd_left hg_a r) (dvd_mul_of_dvd_left hg_b s)
  have hg_error : g ∣ residue - (a * r + b * s) := by
    rw [hk]
    exact dvd_mul_of_dvd_left hg_modulus k
  have hresidue : g ∣ (residue - (a * r + b * s)) + (a * r + b * s) :=
    dvd_add hg_error hg_linear
  simpa [g] using hresidue

theorem exists_twoVariableLinearCongruence_iff_gcd_dvd
    {a b residue modulus : Int} :
    (∃ r s : Int, a * r + b * s ≡ residue [ZMOD modulus]) ↔
      (((a.gcd b : Int).gcd modulus : Int) ∣ residue) := by
  constructor
  · rintro ⟨r, s, hcong⟩
    exact twoVariableLinearCongruence_gcd_dvd hcong
  · exact exists_twoVariableLinearCongruence_of_gcd_dvd

theorem linearCombination_gcd_dvd
    {a b modulus r s : Int} :
    (((a.gcd b : Int).gcd modulus : Int) ∣ a * r + b * s) := by
  let g : Int := ((a.gcd b : Int).gcd modulus : Int)
  have hg_gab : g ∣ (a.gcd b : Int) := by
    simpa [g] using Int.gcd_dvd_left (a.gcd b : Int) modulus
  have hg_a : g ∣ a :=
    dvd_trans hg_gab (Int.gcd_dvd_left a b)
  have hg_b : g ∣ b :=
    dvd_trans hg_gab (Int.gcd_dvd_right a b)
  simpa [g] using
    dvd_add (dvd_mul_of_dvd_left hg_a r) (dvd_mul_of_dvd_left hg_b s)

theorem twoVariableLinearCongruence_pair_crt_compat
    {a b residueM residueN m n r s : Int}
    (hm : a * r + b * s ≡ residueM [ZMOD m])
    (hn : a * r + b * s ≡ residueN [ZMOD n]) :
    residueM ≡ residueN [ZMOD (m.gcd n : Int)] :=
  crtModEq_compat hm hn

theorem exists_twoVariableLinearCongruence_pair_iff_exists_crt_gcd_dvd
    {a b residueM residueN m n : Int} :
    (∃ r s : Int,
        a * r + b * s ≡ residueM [ZMOD m] ∧
          a * r + b * s ≡ residueN [ZMOD n]) ↔
      ∃ x : Int,
        x ≡ residueM [ZMOD m] ∧
          x ≡ residueN [ZMOD n] ∧
            (((a.gcd b : Int).gcd (m * n) : Int) ∣ x) := by
  constructor
  · rintro ⟨r, s, hm, hn⟩
    refine ⟨a * r + b * s, hm, hn, ?_⟩
    exact linearCombination_gcd_dvd
  · rintro ⟨x, hxm, hxn, hdiv⟩
    rcases exists_twoVariableLinearCongruence_of_gcd_dvd hdiv with ⟨r, s, hprod⟩
    refine ⟨r, s, ?_, ?_⟩
    · have hm_prod : m ∣ m * n := by
        exact dvd_mul_right m n
      exact (Int.ModEq.of_dvd hm_prod hprod).trans hxm
    · have hn_prod : n ∣ m * n := by
        refine ⟨m, ?_⟩
        ring
      exact (Int.ModEq.of_dvd hn_prod hprod).trans hxn

theorem exists_twoVariableLinearCongruence_pair_iff_exists_lcm_crt_gcd_dvd
    {a b residueM residueN m n : Int} :
    (∃ r s : Int,
        a * r + b * s ≡ residueM [ZMOD m] ∧
          a * r + b * s ≡ residueN [ZMOD n]) ↔
      ∃ x : Int,
        x ≡ residueM [ZMOD m] ∧
          x ≡ residueN [ZMOD n] ∧
            (((a.gcd b : Int).gcd (m.lcm n : Int) : Int) ∣ x) := by
  constructor
  · rintro ⟨r, s, hm, hn⟩
    refine ⟨a * r + b * s, hm, hn, ?_⟩
    exact linearCombination_gcd_dvd
  · rintro ⟨x, hxm, hxn, hdiv⟩
    rcases exists_twoVariableLinearCongruence_of_gcd_dvd hdiv with ⟨r, s, hlcm⟩
    refine ⟨r, s, ?_, ?_⟩
    · exact (Int.ModEq.of_dvd (Int.dvd_lcm_left m n) hlcm).trans hxm
    · exact (Int.ModEq.of_dvd (Int.dvd_lcm_right m n) hlcm).trans hxn

theorem exists_twoVariableLinearCongruence_pair_iff_crtWitness_gcd_dvd
    {a b residueM residueN m n x : Int}
    (hxm : x ≡ residueM [ZMOD m]) (hxn : x ≡ residueN [ZMOD n]) :
    (∃ r s : Int,
        a * r + b * s ≡ residueM [ZMOD m] ∧
          a * r + b * s ≡ residueN [ZMOD n]) ↔
      (((a.gcd b : Int).gcd (m.lcm n : Int) : Int) ∣ x) := by
  constructor
  · rintro ⟨r, s, hm, hn⟩
    let y := a * r + b * s
    let g : Int := ((a.gcd b : Int).gcd (m.lcm n : Int) : Int)
    have hyx_m : y ≡ x [ZMOD m] := hm.trans hxm.symm
    have hyx_n : y ≡ x [ZMOD n] := hn.trans hxn.symm
    have hyx_lcm : y ≡ x [ZMOD (m.lcm n : Int)] :=
      modEq_lcm_of_modEq_pair hyx_m hyx_n
    have hg_linear : g ∣ y := by
      simpa [g, y] using (linearCombination_gcd_dvd (a := a) (b := b)
        (modulus := (m.lcm n : Int)) (r := r) (s := s))
    have hg_lcm : g ∣ (m.lcm n : Int) := by
      simpa [g] using Int.gcd_dvd_right (a.gcd b : Int) (m.lcm n : Int)
    have hg_error : g ∣ x - y := by
      rcases Int.modEq_iff_dvd.mp hyx_lcm with ⟨k, hk⟩
      rw [hk]
      exact dvd_mul_of_dvd_left hg_lcm k
    have hx : g ∣ (x - y) + y := dvd_add hg_error hg_linear
    simpa [g, y] using hx
  · intro hdiv
    rcases exists_twoVariableLinearCongruence_of_gcd_dvd hdiv with ⟨r, s, hlcm⟩
    refine ⟨r, s, ?_, ?_⟩
    · exact (Int.ModEq.of_dvd (Int.dvd_lcm_left m n) hlcm).trans hxm
    · exact (Int.ModEq.of_dvd (Int.dvd_lcm_right m n) hlcm).trans hxn

theorem exists_latticePairSameStrip_iff_crtWitness_gcd_dvd
    {strip u v : Point} {residueM residueN m n x : Int}
    (hxm : x ≡ residueM [ZMOD m]) (hxn : x ≡ residueN [ZMOD n]) :
    (∃ r s : Int,
        det strip (add (smul r u) (smul s v)) ≡ residueM [ZMOD m] ∧
          det strip (add (smul r u) (smul s v)) ≡ residueN [ZMOD n]) ↔
      ((((det strip u).gcd (det strip v) : Int).gcd (m.lcm n : Int) : Int) ∣ x) := by
  simpa [det_add_smul_smul, mul_comm, mul_left_comm, mul_assoc]
    using (exists_twoVariableLinearCongruence_pair_iff_crtWitness_gcd_dvd
      (a := det strip u) (b := det strip v)
      (residueM := residueM) (residueN := residueN)
      (m := m) (n := n) (x := x) hxm hxn)

theorem gaussianRootResidue_sq_neg_one {a b c rho inv : Int}
    (hc : c = a * a + b * b)
    (hinv : a * inv ≡ 1 [ZMOD c])
    (hres : a * rho + b ≡ 0 [ZMOD c]) :
    rho * rho + 1 ≡ 0 [ZMOD c] := by
  have h_arho : a * rho ≡ -b [ZMOD c] := by
    have hsub := Int.ModEq.sub hres (Int.ModEq.refl (n := c) b)
    simpa using hsub
  have h_square : (a * a) * (rho * rho + 1) ≡ 0 [ZMOD c] := by
    have hmul_raw := Int.ModEq.mul h_arho h_arho
    have hmul : a * a * (rho * rho) ≡ b * b [ZMOD c] := by
      calc
        a * a * (rho * rho) = (a * rho) * (a * rho) := by ring
        _ ≡ (-b) * (-b) [ZMOD c] := hmul_raw
        _ = b * b := by ring
    have hc0 : b * b + a * a ≡ 0 [ZMOD c] := by
      apply Int.modEq_iff_dvd.mpr
      refine ⟨-1, ?_⟩
      rw [hc]
      ring
    calc
      (a * a) * (rho * rho + 1) = a * a * (rho * rho) + a * a := by ring
      _ ≡ b * b + a * a [ZMOD c] :=
          Int.ModEq.add hmul (Int.ModEq.refl (n := c) (a * a))
      _ ≡ 0 [ZMOD c] := hc0
  have hinv_sq : (a * a) * (inv * inv) ≡ 1 [ZMOD c] := by
    have h := Int.ModEq.mul hinv hinv
    simpa [mul_assoc, mul_left_comm, mul_comm] using h
  have hzero_raw := Int.ModEq.mul h_square (Int.ModEq.refl (n := c) (inv * inv))
  have hzero : ((a * a) * (rho * rho + 1)) * (inv * inv) ≡ 0 [ZMOD c] := by
    calc
      ((a * a) * (rho * rho + 1)) * (inv * inv)
          ≡ 0 * (inv * inv) [ZMOD c] := hzero_raw
      _ = 0 := by ring
  have hleft :
      ((a * a) * (rho * rho + 1)) * (inv * inv) ≡
        (rho * rho + 1) [ZMOD c] := by
    calc
      ((a * a) * (rho * rho + 1)) * (inv * inv)
          = ((a * a) * (inv * inv)) * (rho * rho + 1) := by ring
      _ ≡ 1 * (rho * rho + 1) [ZMOD c] :=
          Int.ModEq.mul hinv_sq (Int.ModEq.refl (n := c) (rho * rho + 1))
      _ = rho * rho + 1 := by ring
  exact hleft.symm.trans hzero

theorem certificateValid_oneTwoRootSpineLine {q t r : Int}
    (hq : q ≠ 0) (ht : t ≠ 0) (hr : r ≠ 0) :
    certificateValid
      ({ x := -3 * r + 2 * q * t * (3 * t + 1),
          y := 4 * r - q * (4 * t + 1) * (2 * t + 1) } : Point)
      ({ x := -3 * r, y := 4 * r } : Point) := by
  let target : Point :=
    { x := -3 * r + 2 * q * t * (3 * t + 1),
      y := 4 * r - q * (4 * t + 1) * (2 * t + 1) }
  let midpoint : Point := { x := -3 * r, y := 4 * r }
  have hthree : 3 * t + 1 ≠ 0 := by omega
  have hfour : 4 * t + 1 ≠ 0 := by omega
  have htwo : 2 * t + 1 ≠ 0 := by omega
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num : (-3 : Int) ≠ 0) hr
      · exact mul_ne_zero (by norm_num) hr
    · refine ⟨5 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · have hx_factor : 2 * q * t * (3 * t + 1) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (mul_ne_zero (by norm_num) hq) ht) hthree
        intro hx
        apply hx_factor
        simpa [target, midpoint, sub] using hx
      · have hy_factor : -q * (4 * t + 1) * (2 * t + 1) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (neg_ne_zero.mpr hq) hfour) htwo
        intro hy
        apply hy_factor
        simpa [target, midpoint, sub] using hy
    · refine ⟨q * (10 * t * t + 6 * t + 1), ?_⟩
      calc
        normSq (sub target midpoint)
            =
                sq (2 * q * t * (3 * t + 1)) +
                sq (-q * (4 * t + 1) * (2 * t + 1)) := by
              simp [target, midpoint, normSq, sub, sq]
      _ = (q * (10 * t * t + 6 * t + 1)) *
          (q * (10 * t * t + 6 * t + 1)) := by
        simp [sq]
        ring_nf

theorem certificateValid_oneEvenRootSpineLine {k q t r : Int}
    (hk : 1 ≤ k) (hq : q ≠ 0) (ht : t ≠ 0) (hr : r ≠ 0) :
    certificateValid
      ({ x := (1 - 4 * k * k) * r +
            2 * q * ((2 * k + 1) * t + k) * ((2 * k - 1) * t + k - 1),
          y := (4 * k) * r - q * (4 * k * t + 2 * k - 1) * (2 * t + 1) } :
        Point)
      ({ x := (1 - 4 * k * k) * r, y := (4 * k) * r } : Point) := by
  let target : Point :=
    { x := (1 - 4 * k * k) * r +
          2 * q * ((2 * k + 1) * t + k) * ((2 * k - 1) * t + k - 1),
      y := (4 * k) * r - q * (4 * k * t + 2 * k - 1) * (2 * t + 1) }
  let midpoint : Point := { x := (1 - 4 * k * k) * r, y := (4 * k) * r }
  have hfirst_x : 1 - 4 * k * k ≠ 0 := by
    nlinarith [hk, sq_nonneg (2 * k)]
  have hfirst_y : 4 * k ≠ 0 := by
    exact mul_ne_zero (by norm_num) (ne_of_gt (lt_of_lt_of_le (by norm_num) hk))
  have hA : (2 * k + 1) * t + k ≠ 0 := by
    by_cases ht_nonneg : 0 ≤ t
    · have ht_pos : 1 ≤ t := by omega
      nlinarith [hk, ht_pos]
    · have ht_le : t ≤ -1 := by omega
      nlinarith [hk, ht_le]
  have hB : (2 * k - 1) * t + k - 1 ≠ 0 := by
    by_cases ht_nonneg : 0 ≤ t
    · have ht_pos : 1 ≤ t := by omega
      nlinarith [hk, ht_pos]
    · have ht_le : t ≤ -1 := by omega
      nlinarith [hk, ht_le]
  have hX : 4 * k * t + 2 * k - 1 ≠ 0 := by
    intro hzero
    have hone : 2 * (2 * k * t + k) = 1 := by nlinarith
    omega
  have hY : 2 * t + 1 ≠ 0 := by omega
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero hfirst_x hr
      · exact mul_ne_zero hfirst_y hr
    · refine ⟨(4 * k * k + 1) * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · have hx_factor :
            2 * q * ((2 * k + 1) * t + k) *
                ((2 * k - 1) * t + k - 1) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (mul_ne_zero (by norm_num) hq) hA) hB
        intro hx
        apply hx_factor
        simpa [target, midpoint, sub] using hx
      · have hy_factor :
            -q * (4 * k * t + 2 * k - 1) * (2 * t + 1) ≠ 0 := by
          exact mul_ne_zero (mul_ne_zero (neg_ne_zero.mpr hq) hX) hY
        intro hy
        apply hy_factor
        simpa [target, midpoint, sub] using hy
    · refine ⟨q * (8 * k * k * t * t + 8 * k * k * t + 2 * k * k -
          4 * k * t - 2 * k + 2 * t * t + 2 * t + 1), ?_⟩
      calc
        normSq (sub target midpoint)
            =
                sq (2 * q * ((2 * k + 1) * t + k) *
                    ((2 * k - 1) * t + k - 1)) +
                sq (-q * (4 * k * t + 2 * k - 1) * (2 * t + 1)) := by
              simp [target, midpoint, normSq, sub, sq]
        _ = (q * (8 * k * k * t * t + 8 * k * k * t + 2 * k * k -
              4 * k * t - 2 * k + 2 * t * t + 2 * t + 1)) *
            (q * (8 * k * k * t * t + 8 * k * k * t + 2 * k * k -
              4 * k * t - 2 * k + 2 * t * t + 2 * t + 1)) := by
          simp [sq]
          ring_nf

theorem certificateValid_oneSixSplitEightyNineThreeFortyNineResidueTwentyOneLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -35, y := 12 } : Point) * r +
          det strip
            ({ x := 70 * t * t - 18 * t - 112,
                y := -24 * t * t - 182 * t - 15 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -35, y := 12 } : Point))
          ({ x := 70 * t * t - 18 * t - 112,
              y := -24 * t * t - 182 * t - 15 } : Point))
        (smul r ({ x := -35, y := 12 } : Point)) ∧
      det strip
          (add (smul r ({ x := -35, y := 12 } : Point))
            ({ x := 70 * t * t - 18 * t - 112,
                y := -24 * t * t - 182 * t - 15 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      74 * t + 21 ≡ 21 [ZMOD 74] := by
  let direction : Point := { x := -35, y := 12 }
  let secondStep : Point :=
    { x := 70 * t * t - 18 * t - 112,
      y := -24 * t * t - 182 * t - 15 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨37, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 2 * (7 * t + 8) * (5 * t - 7) ≠ 0 := by
          exact mul_ne_zero (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          2 * (7 * t + 8) * (5 * t - 7)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : (12 * t + 1) * (-2 * t - 15) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          (12 * t + 1) * (-2 * t - 15)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨74 * t * t + 42 * t + 113, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 74 * t + 21 ≡ 21 [ZMOD 74] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 74 * t + 21)
    (pairedResidue := 21) (pairedModulus := 74)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_oneSixSplitEightyNineThreeFortyNineResidueFiftyNineLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -12, y := 35 } : Point) * r +
          det strip
            ({ x := 24 * t * t - 622 * t - 1045,
                y := -70 * t * t - 338 * t + 1332 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -12, y := 35 } : Point))
          ({ x := 24 * t * t - 622 * t - 1045,
              y := -70 * t * t - 338 * t + 1332 } : Point))
        (smul r ({ x := -12, y := 35 } : Point)) ∧
      det strip
          (add (smul r ({ x := -12, y := 35 } : Point))
            ({ x := 24 * t * t - 622 * t - 1045,
                y := -70 * t * t - 338 * t + 1332 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      74 * t + 59 ≡ 59 [ZMOD 74] := by
  let direction : Point := { x := -12, y := 35 }
  let secondStep : Point :=
    { x := 24 * t * t - 622 * t - 1045,
      y := -70 * t * t - 338 * t + 1332 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨37, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : (-12 * t - 19) * (-2 * t + 55) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          (-12 * t - 19) * (-2 * t + 55)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : 2 * (5 * t + 37) * (-7 * t + 18) ≠ 0 := by
          exact mul_ne_zero (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          2 * (5 * t + 37) * (-7 * t + 18)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨74 * t * t + 118 * t + 1693, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 74 * t + 59 ≡ 59 [ZMOD 74] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 74 * t + 59)
    (pairedResidue := 59) (pairedModulus := 74)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_oneSixSplitEightyNineThreeFortyNineLineStrip :
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -35, y := 12 } : Point) * r +
          det strip
            ({ x := 70 * t * t - 18 * t - 112,
                y := -24 * t * t - 182 * t - 15 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -35, y := 12 } : Point))
            ({ x := 70 * t * t - 18 * t - 112,
                y := -24 * t * t - 182 * t - 15 } : Point))
          (smul r ({ x := -35, y := 12 } : Point)) ∧
        det strip
            (add (smul r ({ x := -35, y := 12 } : Point))
              ({ x := 70 * t * t - 18 * t - 112,
                  y := -24 * t * t - 182 * t - 15 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        74 * t + 21 ≡ 21 [ZMOD 74]) ∧
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -12, y := 35 } : Point) * r +
          det strip
            ({ x := 24 * t * t - 622 * t - 1045,
                y := -70 * t * t - 338 * t + 1332 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -12, y := 35 } : Point))
            ({ x := 24 * t * t - 622 * t - 1045,
                y := -70 * t * t - 338 * t + 1332 } : Point))
          (smul r ({ x := -12, y := 35 } : Point)) ∧
        det strip
            (add (smul r ({ x := -12, y := 35 } : Point))
              ({ x := 24 * t * t - 622 * t - 1045,
                  y := -70 * t * t - 338 * t + 1332 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        74 * t + 59 ≡ 59 [ZMOD 74]) := by
  constructor
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_oneSixSplitEightyNineThreeFortyNineResidueTwentyOneLineStrip
      (strip := strip) hr hcoeff
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_oneSixSplitEightyNineThreeFortyNineResidueFiftyNineLineStrip
      (strip := strip) hr hcoeff

theorem certificateValid_oneSixSplitThirtyFiveEightyThreeResidueThirtySixLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ -582) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -35, y := 12 } : Point) * r +
          det strip
            ({ x := 5 * ((6 * t - 91) * (6 * t - 91) -
                  (-t - 582) * (-t - 582)),
                y := 10 * (6 * t - 91) * (-t - 582) } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -35, y := 12 } : Point))
          ({ x := 5 * ((6 * t - 91) * (6 * t - 91) -
                (-t - 582) * (-t - 582)),
              y := 10 * (6 * t - 91) * (-t - 582) } : Point))
        (smul r ({ x := -35, y := 12 } : Point)) ∧
      det strip
          (add (smul r ({ x := -35, y := 12 } : Point))
            ({ x := 5 * ((6 * t - 91) * (6 * t - 91) -
                  (-t - 582) * (-t - 582)),
                y := 10 * (6 * t - 91) * (-t - 582) } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      37 * t + 36 ≡ 36 [ZMOD 37] := by
  let direction : Point := { x := -35, y := 12 }
  let secondStep : Point :=
    { x := 5 * ((6 * t - 91) * (6 * t - 91) -
          (-t - 582) * (-t - 582)),
      y := 10 * (6 * t - 91) * (-t - 582) }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨37, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 5 * (7 * t + 491) * (5 * t - 673) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          5 * (7 * t + 491) * (5 * t - 673)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : 10 * (6 * t - 91) * (-t - 582) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          10 * (6 * t - 91) * (-t - 582)
              = secondStep.y := by simp [secondStep]
          _ = 0 := hy
    · refine ⟨5 * ((6 * t - 91) * (6 * t - 91) +
          (-t - 582) * (-t - 582)), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 37 * t + 36 ≡ 36 [ZMOD 37] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 37 * t + 36)
    (pairedResidue := 36) (pairedModulus := 37)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_oneSixSplitThirtyFiveEightyThreeResidueEighteenNinetyThreeLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -12, y := 35 } : Point) * r +
          det strip
            ({ x := 10 * (-444 * t - 307) * (-74 * t - 51),
                y := -5 * ((-444 * t - 307) * (-444 * t - 307) -
                  (-74 * t - 51) * (-74 * t - 51)) } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -12, y := 35 } : Point))
          ({ x := 10 * (-444 * t - 307) * (-74 * t - 51),
              y := -5 * ((-444 * t - 307) * (-444 * t - 307) -
                (-74 * t - 51) * (-74 * t - 51)) } : Point))
        (smul r ({ x := -12, y := 35 } : Point)) ∧
      det strip
          (add (smul r ({ x := -12, y := 35 } : Point))
            ({ x := 10 * (-444 * t - 307) * (-74 * t - 51),
                y := -5 * ((-444 * t - 307) * (-444 * t - 307) -
                  (-74 * t - 51) * (-74 * t - 51)) } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      2738 * t + 1893 ≡ 1893 [ZMOD 2738] := by
  let direction : Point := { x := -12, y := 35 }
  let secondStep : Point :=
    { x := 10 * (-444 * t - 307) * (-74 * t - 51),
      y := -5 * ((-444 * t - 307) * (-444 * t - 307) -
        (-74 * t - 51) * (-74 * t - 51)) }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨37, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 10 * (-444 * t - 307) * (-74 * t - 51) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          10 * (-444 * t - 307) * (-74 * t - 51)
              = secondStep.x := by simp [secondStep]
          _ = 0 := hx
      · intro hy
        have hfactor : -20 * (185 * t + 128) * (259 * t + 179) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -20 * (185 * t + 128) * (259 * t + 179)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨5 * ((-444 * t - 307) * (-444 * t - 307) +
          (-74 * t - 51) * (-74 * t - 51)), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 2738 * t + 1893 ≡ 1893 [ZMOD 2738] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 2738 * t + 1893)
    (pairedResidue := 1893) (pairedModulus := 2738)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_oneSixSplitTwentyNineSeventeenResidueFortyThreeLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -35, y := -12 } : Point) * r +
          det strip
            ({ x := 490 * t * t + 574 * t + 168,
                y := 168 * t * t + 182 * t + 49 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -35, y := -12 } : Point))
          ({ x := 490 * t * t + 574 * t + 168,
              y := 168 * t * t + 182 * t + 49 } : Point))
        (smul r ({ x := -35, y := -12 } : Point)) ∧
      det strip
          (add (smul r ({ x := -35, y := -12 } : Point))
            ({ x := 490 * t * t + 574 * t + 168,
                y := 168 * t * t + 182 * t + 49 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      74 * t + 43 ≡ 43 [ZMOD 74] := by
  let direction : Point := { x := -35, y := -12 }
  let secondStep : Point :=
    { x := 490 * t * t + 574 * t + 168,
      y := 168 * t * t + 182 * t + 49 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨37, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 14 * (5 * t + 3) * (7 * t + 4) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          14 * (5 * t + 3) * (7 * t + 4)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : 7 * (2 * t + 1) * (12 * t + 7) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          7 * (2 * t + 1) * (12 * t + 7)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨7 * (74 * t * t + 86 * t + 25), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 74 * t + 43 ≡ 43 [ZMOD 74] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 74 * t + 43)
    (pairedResidue := 43) (pairedModulus := 74)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_oneSixSplitTwentyNineSeventeenResidueThirtyOneLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -12, y := -35 } : Point) * r +
          det strip
            ({ x := 168 * t * t + 154 * t + 35,
                y := 490 * t * t + 406 * t + 84 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -12, y := -35 } : Point))
          ({ x := 168 * t * t + 154 * t + 35,
              y := 490 * t * t + 406 * t + 84 } : Point))
        (smul r ({ x := -12, y := -35 } : Point)) ∧
      det strip
          (add (smul r ({ x := -12, y := -35 } : Point))
            ({ x := 168 * t * t + 154 * t + 35,
                y := 490 * t * t + 406 * t + 84 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      74 * t + 31 ≡ 31 [ZMOD 74] := by
  let direction : Point := { x := -12, y := -35 }
  let secondStep : Point :=
    { x := 168 * t * t + 154 * t + 35,
      y := 490 * t * t + 406 * t + 84 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨37, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 7 * (2 * t + 1) * (12 * t + 5) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          7 * (2 * t + 1) * (12 * t + 5)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : 14 * (5 * t + 2) * (7 * t + 3) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          14 * (5 * t + 2) * (7 * t + 3)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨7 * (74 * t * t + 62 * t + 13), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 74 * t + 31 ≡ 31 [ZMOD 74] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 74 * t + 31)
    (pairedResidue := 31) (pairedModulus := 74)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_oneSixSplitTwentyNineSeventeenLineStrip :
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -35, y := -12 } : Point) * r +
          det strip
            ({ x := 490 * t * t + 574 * t + 168,
                y := 168 * t * t + 182 * t + 49 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -35, y := -12 } : Point))
            ({ x := 490 * t * t + 574 * t + 168,
                y := 168 * t * t + 182 * t + 49 } : Point))
          (smul r ({ x := -35, y := -12 } : Point)) ∧
        det strip
            (add (smul r ({ x := -35, y := -12 } : Point))
              ({ x := 490 * t * t + 574 * t + 168,
                  y := 168 * t * t + 182 * t + 49 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        74 * t + 43 ≡ 43 [ZMOD 74]) ∧
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -12, y := -35 } : Point) * r +
          det strip
            ({ x := 168 * t * t + 154 * t + 35,
                y := 490 * t * t + 406 * t + 84 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -12, y := -35 } : Point))
            ({ x := 168 * t * t + 154 * t + 35,
                y := 490 * t * t + 406 * t + 84 } : Point))
          (smul r ({ x := -12, y := -35 } : Point)) ∧
        det strip
            (add (smul r ({ x := -12, y := -35 } : Point))
              ({ x := 168 * t * t + 154 * t + 35,
                  y := 490 * t * t + 406 * t + 84 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        74 * t + 31 ≡ 31 [ZMOD 74]) := by
  constructor
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_oneSixSplitTwentyNineSeventeenResidueFortyThreeLineStrip
      (strip := strip) hr hcoeff
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_oneSixSplitTwentyNineSeventeenResidueThirtyOneLineStrip
      (strip := strip) hr hcoeff

theorem certificateValid_oneFourRootSpineLine {q t r : Int}
    (hq : q ≠ 0) (hr : r ≠ 0) :
    certificateValid
      ({ x := -8 * r + q * (2 * t + 1) * (8 * t + 3),
          y := -15 * r + 2 * q * (5 * t + 2) * (3 * t + 1) } : Point)
      ({ x := -8 * r, y := -15 * r } : Point) := by
  let target : Point :=
    { x := -8 * r + q * (2 * t + 1) * (8 * t + 3),
      y := -15 * r + 2 * q * (5 * t + 2) * (3 * t + 1) }
  let midpoint : Point := { x := -8 * r, y := -15 * r }
  have htwo : 2 * t + 1 ≠ 0 := by omega
  have height : 8 * t + 3 ≠ 0 := by omega
  have hfive : 5 * t + 2 ≠ 0 := by omega
  have hthree : 3 * t + 1 ≠ 0 := by omega
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num : (-8 : Int) ≠ 0) hr
      · exact mul_ne_zero (by norm_num : (-15 : Int) ≠ 0) hr
    · refine ⟨17 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · have hx_factor : q * (2 * t + 1) * (8 * t + 3) ≠ 0 := by
          exact mul_ne_zero (mul_ne_zero hq htwo) height
        intro hx
        apply hx_factor
        simpa [target, midpoint, sub] using hx
      · have hy_factor : 2 * q * (5 * t + 2) * (3 * t + 1) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (mul_ne_zero (by norm_num) hq) hfive) hthree
        intro hy
        apply hy_factor
        simpa [target, midpoint, sub] using hy
    · refine ⟨q * (34 * t * t + 26 * t + 5), ?_⟩
      calc
        normSq (sub target midpoint)
            =
                sq (q * (2 * t + 1) * (8 * t + 3)) +
                sq (2 * q * (5 * t + 2) * (3 * t + 1)) := by
              simp [target, midpoint, normSq, sub, sq]
        _ = (q * (34 * t * t + 26 * t + 5)) *
            (q * (34 * t * t + 26 * t + 5)) := by
          simp [sq]
          ring_nf

theorem certificateValid_oneFourRootSpineLineSwap {q t r : Int}
    (hq : q ≠ 0) (hr : r ≠ 0) :
    certificateValid
      ({ x := -15 * r + 2 * q * (5 * t + 2) * (3 * t + 1),
          y := -8 * r + q * (2 * t + 1) * (8 * t + 3) } : Point)
      ({ x := -15 * r, y := -8 * r } : Point) := by
  let target : Point :=
    { x := -15 * r + 2 * q * (5 * t + 2) * (3 * t + 1),
      y := -8 * r + q * (2 * t + 1) * (8 * t + 3) }
  let midpoint : Point := { x := -15 * r, y := -8 * r }
  have htwo : 2 * t + 1 ≠ 0 := by omega
  have height : 8 * t + 3 ≠ 0 := by omega
  have hfive : 5 * t + 2 ≠ 0 := by omega
  have hthree : 3 * t + 1 ≠ 0 := by omega
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num : (-15 : Int) ≠ 0) hr
      · exact mul_ne_zero (by norm_num : (-8 : Int) ≠ 0) hr
    · refine ⟨17 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · have hx_factor : 2 * q * (5 * t + 2) * (3 * t + 1) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (mul_ne_zero (by norm_num) hq) hfive) hthree
        intro hx
        apply hx_factor
        simpa [target, midpoint, sub] using hx
      · have hy_factor : q * (2 * t + 1) * (8 * t + 3) ≠ 0 := by
          exact mul_ne_zero (mul_ne_zero hq htwo) height
        intro hy
        apply hy_factor
        simpa [target, midpoint, sub] using hy
    · refine ⟨q * (34 * t * t + 26 * t + 5), ?_⟩
      calc
        normSq (sub target midpoint)
            =
                sq (2 * q * (5 * t + 2) * (3 * t + 1)) +
                sq (q * (2 * t + 1) * (8 * t + 3)) := by
              simp [target, midpoint, normSq, sub, sq]
        _ = (q * (34 * t * t + 26 * t + 5)) *
            (q * (34 * t * t + 26 * t + 5)) := by
          simp [sq]
          ring_nf

theorem certificateValid_oneFourEvenRootSpineLine {m a b r : Int}
    (hm : m ≠ 0) (ha : a ≠ 0) (hb : b ≠ 0)
    (hab : a * a ≠ b * b) (hr : r ≠ 0) :
    certificateValid
      ({ x := -8 * r - 2 * m * a * b,
          y := -15 * r + m * (a * a - b * b) } : Point)
      ({ x := -8 * r, y := -15 * r } : Point) := by
  let target : Point :=
    { x := -8 * r - 2 * m * a * b,
      y := -15 * r + m * (a * a - b * b) }
  let midpoint : Point := { x := -8 * r, y := -15 * r }
  have hdiff : a * a - b * b ≠ 0 := sub_ne_zero.mpr hab
  have hstep_x_factor : -2 * m * a * b ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hm) ha) hb
  have hstep_y_factor : m * (a * a - b * b) ≠ 0 := mul_ne_zero hm hdiff
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num) hr
      · exact mul_ne_zero (by norm_num) hr
    · refine ⟨17 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · intro hx
        apply hstep_x_factor
        calc
          -2 * m * a * b = (-8 * r - 2 * m * a * b) - (-8 * r) := by ring
          _ = (sub target midpoint).x := by simp [target, midpoint, sub]
          _ = 0 := hx
      · intro hy
        apply hstep_y_factor
        simpa [target, midpoint, sub] using hy
    · refine ⟨m * (a * a + b * b), ?_⟩
      calc
        normSq (sub target midpoint)
            = sq (-2 * m * a * b) + sq (m * (a * a - b * b)) := by
              simp [target, midpoint, normSq, sub, sq]
              ring
        _ = (m * (a * a + b * b)) * (m * (a * a + b * b)) := by
          simp [sq]
          ring_nf

theorem certificateValid_oneFourEvenRootSpineLineSwap {m a b r : Int}
    (hm : m ≠ 0) (ha : a ≠ 0) (hb : b ≠ 0)
    (hab : a * a ≠ b * b) (hr : r ≠ 0) :
    certificateValid
      ({ x := -15 * r + m * (a * a - b * b),
          y := -8 * r + 2 * m * a * b } : Point)
      ({ x := -15 * r, y := -8 * r } : Point) := by
  let target : Point :=
    { x := -15 * r + m * (a * a - b * b),
      y := -8 * r + 2 * m * a * b }
  let midpoint : Point := { x := -15 * r, y := -8 * r }
  have hdiff : a * a - b * b ≠ 0 := sub_ne_zero.mpr hab
  have hstep_x_factor : m * (a * a - b * b) ≠ 0 := mul_ne_zero hm hdiff
  have hstep_y_factor : 2 * m * a * b ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hm) ha) hb
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num) hr
      · exact mul_ne_zero (by norm_num) hr
    · refine ⟨17 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · intro hx
        apply hstep_x_factor
        simpa [target, midpoint, sub] using hx
      · intro hy
        apply hstep_y_factor
        simpa [target, midpoint, sub] using hy
    · refine ⟨m * (a * a + b * b), ?_⟩
      calc
        normSq (sub target midpoint)
            = sq (m * (a * a - b * b)) + sq (2 * m * a * b) := by
              simp [target, midpoint, normSq, sub, sq]
        _ = (m * (a * a + b * b)) * (m * (a * a + b * b)) := by
          simp [sq]
          ring_nf

theorem certificateValid_oneFourEvenSplitTwoFortyOneResidueTwelveLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ 56) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -15, y := -8 } : Point) * r +
          det strip
            ({ x := (-4 * t - 17) * (-4 * t - 17) -
                  (-t + 56) * (-t + 56),
                y := 2 * (-4 * t - 17) * (-t + 56) } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -15, y := -8 } : Point))
          ({ x := (-4 * t - 17) * (-4 * t - 17) -
                (-t + 56) * (-t + 56),
              y := 2 * (-4 * t - 17) * (-t + 56) } : Point))
        (smul r ({ x := -15, y := -8 } : Point)) ∧
      det strip
          (add (smul r ({ x := -15, y := -8 } : Point))
            ({ x := (-4 * t - 17) * (-4 * t - 17) -
                  (-t + 56) * (-t + 56),
                y := 2 * (-4 * t - 17) * (-t + 56) } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      17 * t + 12 ≡ 12 [ZMOD 17] := by
  let direction : Point := { x := -15, y := -8 }
  let secondStep : Point :=
    { x := (-4 * t - 17) * (-4 * t - 17) - (-t + 56) * (-t + 56),
      y := 2 * (-4 * t - 17) * (-t + 56) }
  have ha : -4 * t - 17 ≠ 0 := by omega
  have hb : -t + 56 ≠ 0 := by omega
  have hab :
      (-4 * t - 17) * (-4 * t - 17) ≠ (-t + 56) * (-t + 56) := by
    intro hsq
    have hprod : (-3 * t - 73) * (-5 * t + 39) = 0 := by
      calc
        (-3 * t - 73) * (-5 * t + 39)
            =
              (-4 * t - 17) * (-4 * t - 17) -
                (-t + 56) * (-t + 56) := by
              ring
        _ = 0 := by rw [hsq]; ring
    exact (mul_ne_zero (by omega) (by omega)) hprod
  have hline :
      certificateValid (add (smul r direction) secondStep) (smul r direction) := by
    have hraw :=
      certificateValid_oneFourEvenRootSpineLineSwap
        (m := 1) (a := -4 * t - 17) (b := -t + 56) (r := r)
        (by norm_num) ha hb hab hr
    convert hraw using 1
    · ext <;> simp [direction, secondStep, add, smul] <;> ring
    · ext <;> simp [direction, smul] <;> ring
  have hpaired : 17 * t + 12 ≡ 12 [ZMOD 17] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripRowValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 17 * t + 12)
    (pairedResidue := 12) (pairedModulus := 17)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hline hpaired hcoeff

theorem certificateValid_oneFourEvenSplitTwoFortyOneResidueFiveLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ -57) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -8, y := -15 } : Point) * r +
          det strip
            ({ x := -2 * (4 * t - 13) * (-t - 57),
                y := (4 * t - 13) * (4 * t - 13) -
                  (-t - 57) * (-t - 57) } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -8, y := -15 } : Point))
          ({ x := -2 * (4 * t - 13) * (-t - 57),
              y := (4 * t - 13) * (4 * t - 13) -
                (-t - 57) * (-t - 57) } : Point))
        (smul r ({ x := -8, y := -15 } : Point)) ∧
      det strip
          (add (smul r ({ x := -8, y := -15 } : Point))
            ({ x := -2 * (4 * t - 13) * (-t - 57),
                y := (4 * t - 13) * (4 * t - 13) -
                  (-t - 57) * (-t - 57) } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      17 * t + 5 ≡ 5 [ZMOD 17] := by
  let direction : Point := { x := -8, y := -15 }
  let secondStep : Point :=
    { x := -2 * (4 * t - 13) * (-t - 57),
      y := (4 * t - 13) * (4 * t - 13) - (-t - 57) * (-t - 57) }
  have ha : 4 * t - 13 ≠ 0 := by omega
  have hb : -t - 57 ≠ 0 := by omega
  have hab :
      (4 * t - 13) * (4 * t - 13) ≠ (-t - 57) * (-t - 57) := by
    intro hsq
    have hprod : (5 * t + 44) * (3 * t - 70) = 0 := by
      calc
        (5 * t + 44) * (3 * t - 70)
            =
              (4 * t - 13) * (4 * t - 13) -
                (-t - 57) * (-t - 57) := by
              ring
        _ = 0 := by rw [hsq]; ring
    exact (mul_ne_zero (by omega) (by omega)) hprod
  have hline :
      certificateValid (add (smul r direction) secondStep) (smul r direction) := by
    have hraw :=
      certificateValid_oneFourEvenRootSpineLine
        (m := 1) (a := 4 * t - 13) (b := -t - 57) (r := r)
        (by norm_num) ha hb hab hr
    convert hraw using 1
    · ext <;> simp [direction, secondStep, add, smul] <;> ring
    · ext <;> simp [direction, smul] <;> ring
  have hpaired : 17 * t + 5 ≡ 5 [ZMOD 17] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripRowValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 17 * t + 5)
    (pairedResidue := 5) (pairedModulus := 17)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hline hpaired hcoeff

theorem certificateValid_oneFourEvenSplitTwoFortyOneLineStrip :
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      t ≠ 56 → r ≠ 0 →
      det strip ({ x := -15, y := -8 } : Point) * r +
          det strip
            ({ x := (-4 * t - 17) * (-4 * t - 17) -
                  (-t + 56) * (-t + 56),
                y := 2 * (-4 * t - 17) * (-t + 56) } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -15, y := -8 } : Point))
            ({ x := (-4 * t - 17) * (-4 * t - 17) -
                  (-t + 56) * (-t + 56),
                y := 2 * (-4 * t - 17) * (-t + 56) } : Point))
          (smul r ({ x := -15, y := -8 } : Point)) ∧
        det strip
            (add (smul r ({ x := -15, y := -8 } : Point))
              ({ x := (-4 * t - 17) * (-4 * t - 17) -
                    (-t + 56) * (-t + 56),
                  y := 2 * (-4 * t - 17) * (-t + 56) } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        17 * t + 12 ≡ 12 [ZMOD 17]) ∧
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      t ≠ -57 → r ≠ 0 →
      det strip ({ x := -8, y := -15 } : Point) * r +
          det strip
            ({ x := -2 * (4 * t - 13) * (-t - 57),
                y := (4 * t - 13) * (4 * t - 13) -
                  (-t - 57) * (-t - 57) } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -8, y := -15 } : Point))
            ({ x := -2 * (4 * t - 13) * (-t - 57),
                y := (4 * t - 13) * (4 * t - 13) -
                  (-t - 57) * (-t - 57) } : Point))
          (smul r ({ x := -8, y := -15 } : Point)) ∧
        det strip
            (add (smul r ({ x := -8, y := -15 } : Point))
              ({ x := -2 * (4 * t - 13) * (-t - 57),
                  y := (4 * t - 13) * (4 * t - 13) -
                    (-t - 57) * (-t - 57) } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        17 * t + 5 ≡ 5 [ZMOD 17]) := by
  constructor
  · intro t r stripResidue stripModulus strip ht hr hcoeff
    exact certificateValid_oneFourEvenSplitTwoFortyOneResidueTwelveLineStrip
      (strip := strip) ht hr hcoeff
  · intro t r stripResidue stripModulus strip ht hr hcoeff
    exact certificateValid_oneFourEvenSplitTwoFortyOneResidueFiveLineStrip
      (strip := strip) ht hr hcoeff

theorem certificateValid_oneFourOddSquareclassSeventeenSplitTenThirtyThreeResidueThirtyThreeLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -15, y := 8 } : Point) * r +
          det strip
            ({ x := 510 * t * t - 15538 * t - 486336,
                y := -272 * t * t - 31518 * t + 220745 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -15, y := 8 } : Point))
          ({ x := 510 * t * t - 15538 * t - 486336,
              y := -272 * t * t - 31518 * t + 220745 } : Point))
        (smul r ({ x := -15, y := 8 } : Point)) ∧
      det strip
          (add (smul r ({ x := -15, y := 8 } : Point))
            ({ x := 510 * t * t - 15538 * t - 486336,
                y := -272 * t * t - 31518 * t + 220745 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      34 * t + 33 ≡ 33 [ZMOD 34] := by
  let direction : Point := { x := -15, y := 8 }
  let secondStep : Point :=
    { x := 510 * t * t - 15538 * t - 486336,
      y := -272 * t * t - 31518 * t + 220745 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨17, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 34 * (3 * t - 149) * (5 * t + 96) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          34 * (3 * t - 149) * (5 * t + 96)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -17 * (2 * t + 245) * (8 * t - 53) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -17 * (2 * t + 245) * (8 * t - 53)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨17 * (34 * t * t + 66 * t + 31417), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 34 * t + 33 ≡ 33 [ZMOD 34] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 34 * t + 33)
    (pairedResidue := 33) (pairedModulus := 34)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_oneFourOddSquareclassSeventeenSplitTenThirtyThreeResidueTwentyOneLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -8, y := 15 } : Point) * r +
          det strip
            ({ x := 272 * t * t + 306 * t + 85,
                y := -510 * t * t - 646 * t - 204 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -8, y := 15 } : Point))
          ({ x := 272 * t * t + 306 * t + 85,
              y := -510 * t * t - 646 * t - 204 } : Point))
        (smul r ({ x := -8, y := 15 } : Point)) ∧
      det strip
          (add (smul r ({ x := -8, y := 15 } : Point))
            ({ x := 272 * t * t + 306 * t + 85,
                y := -510 * t * t - 646 * t - 204 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      34 * t + 21 ≡ 21 [ZMOD 34] := by
  let direction : Point := { x := -8, y := 15 }
  let secondStep : Point :=
    { x := 272 * t * t + 306 * t + 85,
      y := -510 * t * t - 646 * t - 204 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨17, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 17 * (2 * t + 1) * (8 * t + 5) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          17 * (2 * t + 1) * (8 * t + 5)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -34 * (3 * t + 2) * (5 * t + 3) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -34 * (3 * t + 2) * (5 * t + 3)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨17 * (34 * t * t + 42 * t + 13), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 34 * t + 21 ≡ 21 [ZMOD 34] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 34 * t + 21)
    (pairedResidue := 21) (pairedModulus := 34)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_oneFourOddSquareclassSeventeenSplitTenThirtyThreeLineStrip :
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -15, y := 8 } : Point) * r +
          det strip
            ({ x := 510 * t * t - 15538 * t - 486336,
                y := -272 * t * t - 31518 * t + 220745 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -15, y := 8 } : Point))
            ({ x := 510 * t * t - 15538 * t - 486336,
                y := -272 * t * t - 31518 * t + 220745 } : Point))
          (smul r ({ x := -15, y := 8 } : Point)) ∧
        det strip
            (add (smul r ({ x := -15, y := 8 } : Point))
              ({ x := 510 * t * t - 15538 * t - 486336,
                  y := -272 * t * t - 31518 * t + 220745 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        34 * t + 33 ≡ 33 [ZMOD 34]) ∧
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -8, y := 15 } : Point) * r +
          det strip
            ({ x := 272 * t * t + 306 * t + 85,
                y := -510 * t * t - 646 * t - 204 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -8, y := 15 } : Point))
            ({ x := 272 * t * t + 306 * t + 85,
                y := -510 * t * t - 646 * t - 204 } : Point))
          (smul r ({ x := -8, y := 15 } : Point)) ∧
        det strip
            (add (smul r ({ x := -8, y := 15 } : Point))
              ({ x := 272 * t * t + 306 * t + 85,
                  y := -510 * t * t - 646 * t - 204 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        34 * t + 21 ≡ 21 [ZMOD 34]) := by
  constructor
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_oneFourOddSquareclassSeventeenSplitTenThirtyThreeResidueThirtyThreeLineStrip
      (strip := strip) hr hcoeff
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_oneFourOddSquareclassSeventeenSplitTenThirtyThreeResidueTwentyOneLineStrip
      (strip := strip) hr hcoeff

theorem certificateValid_twoThreeOddRootSpineLine {q t r : Int}
    (hq : q ≠ 0) (ht : t ≠ 0) (hr : r ≠ 0) :
    certificateValid
      ({ x := -12 * r + q * (4 * t - 1) * (6 * t - 1),
          y := -5 * r + 2 * q * t * (5 * t - 1) } : Point)
      ({ x := -12 * r, y := -5 * r } : Point) := by
  let target : Point :=
    { x := -12 * r + q * (4 * t - 1) * (6 * t - 1),
      y := -5 * r + 2 * q * t * (5 * t - 1) }
  let midpoint : Point := { x := -12 * r, y := -5 * r }
  have hfour : 4 * t - 1 ≠ 0 := by omega
  have hsix : 6 * t - 1 ≠ 0 := by omega
  have hfive : 5 * t - 1 ≠ 0 := by omega
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num : (-12 : Int) ≠ 0) hr
      · exact mul_ne_zero (by norm_num : (-5 : Int) ≠ 0) hr
    · refine ⟨13 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · have hx_factor : q * (4 * t - 1) * (6 * t - 1) ≠ 0 := by
          exact mul_ne_zero (mul_ne_zero hq hfour) hsix
        intro hx
        apply hx_factor
        simpa [target, midpoint, sub] using hx
      · have hy_factor : 2 * q * t * (5 * t - 1) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (mul_ne_zero (by norm_num) hq) ht) hfive
        intro hy
        apply hy_factor
        simpa [target, midpoint, sub] using hy
    · refine ⟨q * (26 * t * t - 10 * t + 1), ?_⟩
      calc
        normSq (sub target midpoint)
            =
                sq (q * (4 * t - 1) * (6 * t - 1)) +
                sq (2 * q * t * (5 * t - 1)) := by
              simp [target, midpoint, normSq, sub, sq]
        _ = (q * (26 * t * t - 10 * t + 1)) *
            (q * (26 * t * t - 10 * t + 1)) := by
          simp [sq]
          ring_nf

theorem certificateValid_twoThreeOddRootSpineLineSwap {q t r : Int}
    (hq : q ≠ 0) (ht : t ≠ 0) (hr : r ≠ 0) :
    certificateValid
      ({ x := -5 * r + 2 * q * t * (5 * t - 1),
          y := -12 * r + q * (4 * t - 1) * (6 * t - 1) } : Point)
      ({ x := -5 * r, y := -12 * r } : Point) := by
  let target : Point :=
    { x := -5 * r + 2 * q * t * (5 * t - 1),
      y := -12 * r + q * (4 * t - 1) * (6 * t - 1) }
  let midpoint : Point := { x := -5 * r, y := -12 * r }
  have hfour : 4 * t - 1 ≠ 0 := by omega
  have hsix : 6 * t - 1 ≠ 0 := by omega
  have hfive : 5 * t - 1 ≠ 0 := by omega
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num : (-5 : Int) ≠ 0) hr
      · exact mul_ne_zero (by norm_num : (-12 : Int) ≠ 0) hr
    · refine ⟨13 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · have hx_factor : 2 * q * t * (5 * t - 1) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (mul_ne_zero (by norm_num) hq) ht) hfive
        intro hx
        apply hx_factor
        simpa [target, midpoint, sub] using hx
      · have hy_factor : q * (4 * t - 1) * (6 * t - 1) ≠ 0 := by
          exact mul_ne_zero (mul_ne_zero hq hfour) hsix
        intro hy
        apply hy_factor
        simpa [target, midpoint, sub] using hy
    · refine ⟨q * (26 * t * t - 10 * t + 1), ?_⟩
      calc
        normSq (sub target midpoint)
            =
                sq (2 * q * t * (5 * t - 1)) +
                sq (q * (4 * t - 1) * (6 * t - 1)) := by
              simp [target, midpoint, normSq, sub, sq]
      _ = (q * (26 * t * t - 10 * t + 1)) *
          (q * (26 * t * t - 10 * t + 1)) := by
        simp [sq]
        ring_nf

theorem certificateValid_twoThreeOddSquareclassThirteenSplitFourSeventyThreeResidueTwentyOneLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ -1) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -12, y := 5 } : Point) * r +
          det strip
            ({ x := 312 * t * t + 494 * t + 195,
                y := -130 * t * t - 234 * t - 104 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -12, y := 5 } : Point))
          ({ x := 312 * t * t + 494 * t + 195,
              y := -130 * t * t - 234 * t - 104 } : Point))
        (smul r ({ x := -12, y := 5 } : Point)) ∧
      det strip
          (add (smul r ({ x := -12, y := 5 } : Point))
            ({ x := 312 * t * t + 494 * t + 195,
                y := -130 * t * t - 234 * t - 104 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      26 * t + 21 ≡ 21 [ZMOD 26] := by
  let direction : Point := { x := -12, y := 5 }
  let secondStep : Point :=
    { x := 312 * t * t + 494 * t + 195,
      y := -130 * t * t - 234 * t - 104 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 13 * (4 * t + 3) * (6 * t + 5) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          13 * (4 * t + 3) * (6 * t + 5)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -26 * (t + 1) * (5 * t + 4) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -26 * (t + 1) * (5 * t + 4)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨13 * (26 * t * t + 42 * t + 17), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 26 * t + 21 ≡ 21 [ZMOD 26] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 26 * t + 21)
    (pairedResidue := 21) (pairedModulus := 26)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeOddSquareclassThirteenSplitFourSeventyThreeResidueTwentyFiveLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ 90) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -5, y := 12 } : Point) * r +
          det strip
            ({ x := 130 * t * t - 11102 * t - 53820,
                y := -312 * t * t - 5330 * t + 98423 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -5, y := 12 } : Point))
          ({ x := 130 * t * t - 11102 * t - 53820,
              y := -312 * t * t - 5330 * t + 98423 } : Point))
        (smul r ({ x := -5, y := 12 } : Point)) ∧
      det strip
          (add (smul r ({ x := -5, y := 12 } : Point))
            ({ x := 130 * t * t - 11102 * t - 53820,
                y := -312 * t * t - 5330 * t + 98423 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      26 * t + 25 ≡ 25 [ZMOD 26] := by
  let direction : Point := { x := -5, y := 12 }
  let secondStep : Point :=
    { x := 130 * t * t - 11102 * t - 53820,
      y := -312 * t * t - 5330 * t + 98423 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 26 * (t - 90) * (5 * t + 23) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          26 * (t - 90) * (5 * t + 23)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -13 * (4 * t + 113) * (6 * t - 67) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -13 * (4 * t + 113) * (6 * t - 67)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨13 * (26 * t * t + 50 * t + 8629), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 26 * t + 25 ≡ 25 [ZMOD 26] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 26 * t + 25)
    (pairedResidue := 25) (pairedModulus := 26)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeOddSquareclassThirteenSplitFourSeventyThreeLineStrip :
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      t ≠ -1 → r ≠ 0 →
      det strip ({ x := -12, y := 5 } : Point) * r +
          det strip
            ({ x := 312 * t * t + 494 * t + 195,
                y := -130 * t * t - 234 * t - 104 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -12, y := 5 } : Point))
            ({ x := 312 * t * t + 494 * t + 195,
                y := -130 * t * t - 234 * t - 104 } : Point))
          (smul r ({ x := -12, y := 5 } : Point)) ∧
        det strip
            (add (smul r ({ x := -12, y := 5 } : Point))
              ({ x := 312 * t * t + 494 * t + 195,
                  y := -130 * t * t - 234 * t - 104 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        26 * t + 21 ≡ 21 [ZMOD 26]) ∧
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      t ≠ 90 → r ≠ 0 →
      det strip ({ x := -5, y := 12 } : Point) * r +
          det strip
            ({ x := 130 * t * t - 11102 * t - 53820,
                y := -312 * t * t - 5330 * t + 98423 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -5, y := 12 } : Point))
            ({ x := 130 * t * t - 11102 * t - 53820,
                y := -312 * t * t - 5330 * t + 98423 } : Point))
          (smul r ({ x := -5, y := 12 } : Point)) ∧
        det strip
            (add (smul r ({ x := -5, y := 12 } : Point))
              ({ x := 130 * t * t - 11102 * t - 53820,
                  y := -312 * t * t - 5330 * t + 98423 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        26 * t + 25 ≡ 25 [ZMOD 26]) := by
  constructor
  · intro t r stripResidue stripModulus strip ht hr hcoeff
    exact certificateValid_twoThreeOddSquareclassThirteenSplitFourSeventyThreeResidueTwentyOneLineStrip
      (strip := strip) ht hr hcoeff
  · intro t r stripResidue stripModulus strip ht hr hcoeff
    exact certificateValid_twoThreeOddSquareclassThirteenSplitFourSeventyThreeResidueTwentyFiveLineStrip
      (strip := strip) ht hr hcoeff

theorem certificateValid_twoThreeOddSquareclassThirteenSplitNineOhFiveResidueOneOhNineLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -12, y := -5 } : Point) * r +
          det strip
            ({ x := 52728 * t * t + 34138 * t + 5525,
                y := 21970 * t * t + 13858 * t + 2184 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -12, y := -5 } : Point))
          ({ x := 52728 * t * t + 34138 * t + 5525,
              y := 21970 * t * t + 13858 * t + 2184 } : Point))
        (smul r ({ x := -12, y := -5 } : Point)) ∧
      det strip
          (add (smul r ({ x := -12, y := -5 } : Point))
            ({ x := 52728 * t * t + 34138 * t + 5525,
                y := 21970 * t * t + 13858 * t + 2184 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      338 * t + 109 ≡ 109 [ZMOD 338] := by
  let direction : Point := { x := -12, y := -5 }
  let secondStep : Point :=
    { x := 52728 * t * t + 34138 * t + 5525,
      y := 21970 * t * t + 13858 * t + 2184 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 13 * (52 * t + 17) * (78 * t + 25) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          13 * (52 * t + 17) * (78 * t + 25)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : 26 * (13 * t + 4) * (65 * t + 21) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          26 * (13 * t + 4) * (65 * t + 21)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨13 * (4394 * t * t + 2834 * t + 457), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 338 * t + 109 ≡ 109 [ZMOD 338] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 338 * t + 109)
    (pairedResidue := 109) (pairedModulus := 338)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeOddSquareclassThirteenSplitNineOhFiveResidueTwentyOneLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ -1) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -5, y := -12 } : Point) * r +
          det strip
            ({ x := 130 * t * t + 234 * t + 104,
                y := 312 * t * t + 494 * t + 195 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -5, y := -12 } : Point))
          ({ x := 130 * t * t + 234 * t + 104,
              y := 312 * t * t + 494 * t + 195 } : Point))
        (smul r ({ x := -5, y := -12 } : Point)) ∧
      det strip
          (add (smul r ({ x := -5, y := -12 } : Point))
            ({ x := 130 * t * t + 234 * t + 104,
                y := 312 * t * t + 494 * t + 195 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      26 * t + 21 ≡ 21 [ZMOD 26] := by
  let direction : Point := { x := -5, y := -12 }
  let secondStep : Point :=
    { x := 130 * t * t + 234 * t + 104,
      y := 312 * t * t + 494 * t + 195 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 26 * (t + 1) * (5 * t + 4) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          26 * (t + 1) * (5 * t + 4)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : 13 * (4 * t + 3) * (6 * t + 5) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          13 * (4 * t + 3) * (6 * t + 5)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨13 * (26 * t * t + 42 * t + 17), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 26 * t + 21 ≡ 21 [ZMOD 26] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 26 * t + 21)
    (pairedResidue := 21) (pairedModulus := 26)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeEvenSplitSeventyOneOneTwentyOneResidueNineLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ -28) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -12, y := 5 } : Point) * r +
          det strip
            ({ x := 12 * t * t - 38 * t - 390,
                y := -5 * t * t - 138 * t + 56 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -12, y := 5 } : Point))
          ({ x := 12 * t * t - 38 * t - 390,
              y := -5 * t * t - 138 * t + 56 } : Point))
        (smul r ({ x := -12, y := 5 } : Point)) ∧
      det strip
          (add (smul r ({ x := -12, y := 5 } : Point))
            ({ x := 12 * t * t - 38 * t - 390,
                y := -5 * t * t - 138 * t + 56 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      13 * t + 9 ≡ 9 [ZMOD 13] := by
  let direction : Point := { x := -12, y := 5 }
  let secondStep : Point :=
    { x := 12 * t * t - 38 * t - 390,
      y := -5 * t * t - 138 * t + 56 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 2 * (2 * t - 15) * (3 * t + 13) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          2 * (2 * t - 15) * (3 * t + 13)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -(t + 28) * (5 * t - 2) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          -(t + 28) * (5 * t - 2)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨13 * t * t + 18 * t + 394, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 13 * t + 9 ≡ 9 [ZMOD 13] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 13 * t + 9)
    (pairedResidue := 9) (pairedModulus := 13)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeEvenSplitSeventyOneOneTwentyOneResidueSevenLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ 46) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -5, y := 12 } : Point) * r +
          det strip
            ({ x := 5 * t * t - 218 * t - 552,
                y := -12 * t * t - 106 * t + 986 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -5, y := 12 } : Point))
          ({ x := 5 * t * t - 218 * t - 552,
              y := -12 * t * t - 106 * t + 986 } : Point))
        (smul r ({ x := -5, y := 12 } : Point)) ∧
      det strip
          (add (smul r ({ x := -5, y := 12 } : Point))
            ({ x := 5 * t * t - 218 * t - 552,
                y := -12 * t * t - 106 * t + 986 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      13 * t + 7 ≡ 7 [ZMOD 13] := by
  let direction : Point := { x := -5, y := 12 }
  let secondStep : Point :=
    { x := 5 * t * t - 218 * t - 552,
      y := -12 * t * t - 106 * t + 986 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : (t - 46) * (5 * t + 12) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          (t - 46) * (5 * t + 12)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -2 * (2 * t + 29) * (3 * t - 17) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -2 * (2 * t + 29) * (3 * t - 17)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨13 * t * t + 14 * t + 1130, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 13 * t + 7 ≡ 7 [ZMOD 13] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 13 * t + 7)
    (pairedResidue := 7) (pairedModulus := 13)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeEvenSplitSeventyOneOneTwentyOneLineStrip :
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      t ≠ -28 → r ≠ 0 →
      det strip ({ x := -12, y := 5 } : Point) * r +
          det strip
            ({ x := 12 * t * t - 38 * t - 390,
                y := -5 * t * t - 138 * t + 56 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -12, y := 5 } : Point))
            ({ x := 12 * t * t - 38 * t - 390,
                y := -5 * t * t - 138 * t + 56 } : Point))
          (smul r ({ x := -12, y := 5 } : Point)) ∧
        det strip
            (add (smul r ({ x := -12, y := 5 } : Point))
              ({ x := 12 * t * t - 38 * t - 390,
                  y := -5 * t * t - 138 * t + 56 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        13 * t + 9 ≡ 9 [ZMOD 13]) ∧
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      t ≠ 46 → r ≠ 0 →
      det strip ({ x := -5, y := 12 } : Point) * r +
          det strip
            ({ x := 5 * t * t - 218 * t - 552,
                y := -12 * t * t - 106 * t + 986 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -5, y := 12 } : Point))
            ({ x := 5 * t * t - 218 * t - 552,
                y := -12 * t * t - 106 * t + 986 } : Point))
          (smul r ({ x := -5, y := 12 } : Point)) ∧
        det strip
            (add (smul r ({ x := -5, y := 12 } : Point))
              ({ x := 5 * t * t - 218 * t - 552,
                  y := -12 * t * t - 106 * t + 986 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        13 * t + 7 ≡ 7 [ZMOD 13]) := by
  constructor
  · intro t r stripResidue stripModulus strip ht hr hcoeff
    exact certificateValid_twoThreeEvenSplitSeventyOneOneTwentyOneResidueNineLineStrip
      (strip := strip) ht hr hcoeff
  · intro t r stripResidue stripModulus strip ht hr hcoeff
    exact certificateValid_twoThreeEvenSplitSeventyOneOneTwentyOneResidueSevenLineStrip
      (strip := strip) ht hr hcoeff

theorem certificateValid_twoThreeEvenSplitNineteenSixFortyOneResidueNineLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ -8) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -12, y := 5 } : Point) * r +
          det strip
            ({ x := 12 * t * t + 2 * t - 30,
                y := -5 * t * t - 42 * t - 16 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -12, y := 5 } : Point))
          ({ x := 12 * t * t + 2 * t - 30,
              y := -5 * t * t - 42 * t - 16 } : Point))
        (smul r ({ x := -12, y := 5 } : Point)) ∧
      det strip
          (add (smul r ({ x := -12, y := 5 } : Point))
            ({ x := 12 * t * t + 2 * t - 30,
                y := -5 * t * t - 42 * t - 16 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      13 * t + 9 ≡ 9 [ZMOD 13] := by
  let direction : Point := { x := -12, y := 5 }
  let secondStep : Point :=
    { x := 12 * t * t + 2 * t - 30,
      y := -5 * t * t - 42 * t - 16 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 2 * (2 * t - 3) * (3 * t + 5) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          2 * (2 * t - 3) * (3 * t + 5)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -(t + 8) * (5 * t + 2) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          -(t + 8) * (5 * t + 2)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨13 * t * t + 18 * t + 34, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 13 * t + 9 ≡ 9 [ZMOD 13] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 13 * t + 9)
    (pairedResidue := 9) (pairedModulus := 13)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeEvenSplitNineteenSixFortyOneResidueSevenLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ 246) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -5, y := 12 } : Point) * r +
          det strip
            ({ x := 5 * t * t - 1178 * t - 12792,
                y := -12 * t * t - 506 * t + 28906 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -5, y := 12 } : Point))
          ({ x := 5 * t * t - 1178 * t - 12792,
              y := -12 * t * t - 506 * t + 28906 } : Point))
        (smul r ({ x := -5, y := 12 } : Point)) ∧
      det strip
          (add (smul r ({ x := -5, y := 12 } : Point))
            ({ x := 5 * t * t - 1178 * t - 12792,
                y := -12 * t * t - 506 * t + 28906 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      13 * t + 7 ≡ 7 [ZMOD 13] := by
  let direction : Point := { x := -5, y := 12 }
  let secondStep : Point :=
    { x := 5 * t * t - 1178 * t - 12792,
      y := -12 * t * t - 506 * t + 28906 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : (t - 246) * (5 * t + 52) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          (t - 246) * (5 * t + 52)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -2 * (2 * t + 149) * (3 * t - 97) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -2 * (2 * t + 149) * (3 * t - 97)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨13 * t * t + 14 * t + 31610, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 13 * t + 7 ≡ 7 [ZMOD 13] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 13 * t + 7)
    (pairedResidue := 7) (pairedModulus := 13)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeEvenSplitNineteenSixFortyOneLineStrip :
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      t ≠ -8 → r ≠ 0 →
      det strip ({ x := -12, y := 5 } : Point) * r +
          det strip
            ({ x := 12 * t * t + 2 * t - 30,
                y := -5 * t * t - 42 * t - 16 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -12, y := 5 } : Point))
            ({ x := 12 * t * t + 2 * t - 30,
                y := -5 * t * t - 42 * t - 16 } : Point))
          (smul r ({ x := -12, y := 5 } : Point)) ∧
        det strip
            (add (smul r ({ x := -12, y := 5 } : Point))
              ({ x := 12 * t * t + 2 * t - 30,
                  y := -5 * t * t - 42 * t - 16 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        13 * t + 9 ≡ 9 [ZMOD 13]) ∧
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      t ≠ 246 → r ≠ 0 →
      det strip ({ x := -5, y := 12 } : Point) * r +
          det strip
            ({ x := 5 * t * t - 1178 * t - 12792,
                y := -12 * t * t - 506 * t + 28906 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -5, y := 12 } : Point))
            ({ x := 5 * t * t - 1178 * t - 12792,
                y := -12 * t * t - 506 * t + 28906 } : Point))
          (smul r ({ x := -5, y := 12 } : Point)) ∧
        det strip
            (add (smul r ({ x := -5, y := 12 } : Point))
              ({ x := 5 * t * t - 1178 * t - 12792,
                  y := -12 * t * t - 506 * t + 28906 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        13 * t + 7 ≡ 7 [ZMOD 13]) := by
  constructor
  · intro t r stripResidue stripModulus strip ht hr hcoeff
    exact certificateValid_twoThreeEvenSplitNineteenSixFortyOneResidueNineLineStrip
      (strip := strip) ht hr hcoeff
  · intro t r stripResidue stripModulus strip ht hr hcoeff
    exact certificateValid_twoThreeEvenSplitNineteenSixFortyOneResidueSevenLineStrip
      (strip := strip) ht hr hcoeff

theorem certificateValid_twoThreeSquareclassFiveSplitNineteenOneSeventyThreeResidueNineLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ -4) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -12, y := 5 } : Point) * r +
          det strip
            ({ x := 120 * t * t + 10 * t - 75,
                y := -50 * t * t - 210 * t - 40 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -12, y := 5 } : Point))
          ({ x := 120 * t * t + 10 * t - 75,
              y := -50 * t * t - 210 * t - 40 } : Point))
        (smul r ({ x := -12, y := 5 } : Point)) ∧
      det strip
          (add (smul r ({ x := -12, y := 5 } : Point))
            ({ x := 120 * t * t + 10 * t - 75,
                y := -50 * t * t - 210 * t - 40 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      26 * t + 9 ≡ 9 [ZMOD 26] := by
  let direction : Point := { x := -12, y := 5 }
  let secondStep : Point :=
    { x := 120 * t * t + 10 * t - 75,
      y := -50 * t * t - 210 * t - 40 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 5 * (4 * t - 3) * (6 * t + 5) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          5 * (4 * t - 3) * (6 * t + 5)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -10 * (t + 4) * (5 * t + 1) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -10 * (t + 4) * (5 * t + 1)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨5 * (26 * t * t + 18 * t + 17), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 26 * t + 9 ≡ 9 [ZMOD 26] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 26 * t + 9)
    (pairedResidue := 9) (pairedModulus := 26)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeSquareclassFiveSplitNineteenOneSeventyThreeResidueSevenLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ 33) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -5, y := 12 } : Point) * r +
          det strip
            ({ x := 50 * t * t - 1570 * t - 2640,
                y := -120 * t * t - 730 * t + 5125 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -5, y := 12 } : Point))
          ({ x := 50 * t * t - 1570 * t - 2640,
              y := -120 * t * t - 730 * t + 5125 } : Point))
        (smul r ({ x := -5, y := 12 } : Point)) ∧
      det strip
          (add (smul r ({ x := -5, y := 12 } : Point))
            ({ x := 50 * t * t - 1570 * t - 2640,
                y := -120 * t * t - 730 * t + 5125 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      26 * t + 7 ≡ 7 [ZMOD 26] := by
  let direction : Point := { x := -5, y := 12 }
  let secondStep : Point :=
    { x := 50 * t * t - 1570 * t - 2640,
      y := -120 * t * t - 730 * t + 5125 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 10 * (t - 33) * (5 * t + 8) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          10 * (t - 33) * (5 * t + 8)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -5 * (4 * t + 41) * (6 * t - 25) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -5 * (4 * t + 41) * (6 * t - 25)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨5 * (26 * t * t + 14 * t + 1153), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 26 * t + 7 ≡ 7 [ZMOD 26] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 26 * t + 7)
    (pairedResidue := 7) (pairedModulus := 26)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeSquareclassFiveSplitNineteenOneSeventyThreeLineStrip :
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      t ≠ -4 → r ≠ 0 →
      det strip ({ x := -12, y := 5 } : Point) * r +
          det strip
            ({ x := 120 * t * t + 10 * t - 75,
                y := -50 * t * t - 210 * t - 40 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -12, y := 5 } : Point))
            ({ x := 120 * t * t + 10 * t - 75,
                y := -50 * t * t - 210 * t - 40 } : Point))
          (smul r ({ x := -12, y := 5 } : Point)) ∧
        det strip
            (add (smul r ({ x := -12, y := 5 } : Point))
              ({ x := 120 * t * t + 10 * t - 75,
                  y := -50 * t * t - 210 * t - 40 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        26 * t + 9 ≡ 9 [ZMOD 26]) ∧
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      t ≠ 33 → r ≠ 0 →
      det strip ({ x := -5, y := 12 } : Point) * r +
          det strip
            ({ x := 50 * t * t - 1570 * t - 2640,
                y := -120 * t * t - 730 * t + 5125 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -5, y := 12 } : Point))
            ({ x := 50 * t * t - 1570 * t - 2640,
                y := -120 * t * t - 730 * t + 5125 } : Point))
          (smul r ({ x := -5, y := 12 } : Point)) ∧
        det strip
            (add (smul r ({ x := -5, y := 12 } : Point))
              ({ x := 50 * t * t - 1570 * t - 2640,
                  y := -120 * t * t - 730 * t + 5125 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        26 * t + 7 ≡ 7 [ZMOD 26]) := by
  constructor
  · intro t r stripResidue stripModulus strip ht hr hcoeff
    exact certificateValid_twoThreeSquareclassFiveSplitNineteenOneSeventyThreeResidueNineLineStrip
      (strip := strip) ht hr hcoeff
  · intro t r stripResidue stripModulus strip ht hr hcoeff
    exact certificateValid_twoThreeSquareclassFiveSplitNineteenOneSeventyThreeResidueSevenLineStrip
      (strip := strip) ht hr hcoeff

theorem certificateValid_twoThreeSquareclassFortySixSplitThreeSeventeenResidueEightLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ -1) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -12, y := 5 } : Point) * r +
          det strip
            ({ x := 276 * t * t + 322 * t + 92,
                y := -115 * t * t - 184 * t - 69 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -12, y := 5 } : Point))
          ({ x := 276 * t * t + 322 * t + 92,
              y := -115 * t * t - 184 * t - 69 } : Point))
        (smul r ({ x := -12, y := 5 } : Point)) ∧
      det strip
          (add (smul r ({ x := -12, y := 5 } : Point))
            ({ x := 276 * t * t + 322 * t + 92,
                y := -115 * t * t - 184 * t - 69 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      13 * t + 8 ≡ 8 [ZMOD 13] := by
  let direction : Point := { x := -12, y := 5 }
  let secondStep : Point :=
    { x := 276 * t * t + 322 * t + 92,
      y := -115 * t * t - 184 * t - 69 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 46 * (2 * t + 1) * (3 * t + 2) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          46 * (2 * t + 1) * (3 * t + 2)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -23 * (t + 1) * (5 * t + 3) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -23 * (t + 1) * (5 * t + 3)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨23 * (13 * t * t + 16 * t + 5), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 13 * t + 8 ≡ 8 [ZMOD 13] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 13 * t + 8)
    (pairedResidue := 8) (pairedModulus := 13)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeSquareclassFortySixSplitThreeSeventeenResidueTwelveLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ 121) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -5, y := 12 } : Point) * r +
          det strip
            ({ x := 115 * t * t - 13248 * t - 80707,
                y := -276 * t * t - 6118 * t + 158700 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -5, y := 12 } : Point))
          ({ x := 115 * t * t - 13248 * t - 80707,
              y := -276 * t * t - 6118 * t + 158700 } : Point))
        (smul r ({ x := -5, y := 12 } : Point)) ∧
      det strip
          (add (smul r ({ x := -5, y := 12 } : Point))
            ({ x := 115 * t * t - 13248 * t - 80707,
                y := -276 * t * t - 6118 * t + 158700 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      13 * t + 12 ≡ 12 [ZMOD 13] := by
  let direction : Point := { x := -5, y := 12 }
  let secondStep : Point :=
    { x := 115 * t * t - 13248 * t - 80707,
      y := -276 * t * t - 6118 * t + 158700 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 23 * (t - 121) * (5 * t + 29) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          23 * (t - 121) * (5 * t + 29)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -46 * (2 * t + 75) * (3 * t - 46) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -46 * (2 * t + 75) * (3 * t - 46)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨23 * (13 * t * t + 24 * t + 7741), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 13 * t + 12 ≡ 12 [ZMOD 13] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 13 * t + 12)
    (pairedResidue := 12) (pairedModulus := 13)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeSquareclassFortySixSplitThreeSeventeenLineStrip :
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      t ≠ -1 → r ≠ 0 →
      det strip ({ x := -12, y := 5 } : Point) * r +
          det strip
            ({ x := 276 * t * t + 322 * t + 92,
                y := -115 * t * t - 184 * t - 69 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -12, y := 5 } : Point))
            ({ x := 276 * t * t + 322 * t + 92,
                y := -115 * t * t - 184 * t - 69 } : Point))
          (smul r ({ x := -12, y := 5 } : Point)) ∧
        det strip
            (add (smul r ({ x := -12, y := 5 } : Point))
              ({ x := 276 * t * t + 322 * t + 92,
                  y := -115 * t * t - 184 * t - 69 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        13 * t + 8 ≡ 8 [ZMOD 13]) ∧
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      t ≠ 121 → r ≠ 0 →
      det strip ({ x := -5, y := 12 } : Point) * r +
          det strip
            ({ x := 115 * t * t - 13248 * t - 80707,
                y := -276 * t * t - 6118 * t + 158700 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -5, y := 12 } : Point))
            ({ x := 115 * t * t - 13248 * t - 80707,
                y := -276 * t * t - 6118 * t + 158700 } : Point))
          (smul r ({ x := -5, y := 12 } : Point)) ∧
        det strip
            (add (smul r ({ x := -5, y := 12 } : Point))
              ({ x := 115 * t * t - 13248 * t - 80707,
                  y := -276 * t * t - 6118 * t + 158700 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        13 * t + 12 ≡ 12 [ZMOD 13]) := by
  constructor
  · intro t r stripResidue stripModulus strip ht hr hcoeff
    exact certificateValid_twoThreeSquareclassFortySixSplitThreeSeventeenResidueEightLineStrip
      (strip := strip) ht hr hcoeff
  · intro t r stripResidue stripModulus strip ht hr hcoeff
    exact certificateValid_twoThreeSquareclassFortySixSplitThreeSeventeenResidueTwelveLineStrip
      (strip := strip) ht hr hcoeff

theorem certificateValid_oneSixSquareclassTenSplitFourSeventyFiveResidueOneLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (htx : t ≠ -18) (hty : t ≠ 77) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -35, y := -12 } : Point) * r +
          det strip
            ({ x := 175 * t * t + 1550 * t - 28800,
                y := 60 * t * t - 4490 * t - 10010 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -35, y := -12 } : Point))
          ({ x := 175 * t * t + 1550 * t - 28800,
              y := 60 * t * t - 4490 * t - 10010 } : Point))
        (smul r ({ x := -35, y := -12 } : Point)) ∧
      det strip
          (add (smul r ({ x := -35, y := -12 } : Point))
            ({ x := 175 * t * t + 1550 * t - 28800,
                y := 60 * t * t - 4490 * t - 10010 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      37 * t + 1 ≡ 1 [ZMOD 37] := by
  let direction : Point := { x := -35, y := -12 }
  let secondStep : Point :=
    { x := 175 * t * t + 1550 * t - 28800,
      y := 60 * t * t - 4490 * t - 10010 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨37, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 25 * (t + 18) * (7 * t - 64) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          25 * (t + 18) * (7 * t - 64)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : 10 * (t - 77) * (6 * t + 13) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          10 * (t - 77) * (6 * t + 13)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨5 * (37 * t * t + 2 * t + 6098), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 37 * t + 1 ≡ 1 [ZMOD 37] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 37 * t + 1)
    (pairedResidue := 1) (pairedModulus := 37)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_oneSixSquareclassTenSplitFourSeventyFiveResidueTwentySevenThirtySevenLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -12, y := -35 } : Point) * r +
          det strip
            ({ x := 328560 * t * t + 989380 * t + 650810,
                y := 958300 * t * t + 1801900 * t + 814800 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -12, y := -35 } : Point))
          ({ x := 328560 * t * t + 989380 * t + 650810,
              y := 958300 * t * t + 1801900 * t + 814800 } : Point))
        (smul r ({ x := -12, y := -35 } : Point)) ∧
      det strip
          (add (smul r ({ x := -12, y := -35 } : Point))
            ({ x := 328560 * t * t + 989380 * t + 650810,
                y := 958300 * t * t + 1801900 * t + 814800 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      2738 * t + 2737 ≡ 2737 [ZMOD 2738] := by
  let direction : Point := { x := -12, y := -35 }
  let secondStep : Point :=
    { x := 328560 * t * t + 989380 * t + 650810,
      y := 958300 * t * t + 1801900 * t + 814800 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨37, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 10 * (74 * t + 151) * (444 * t + 431) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          10 * (74 * t + 151) * (444 * t + 431)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : 100 * (37 * t + 28) * (259 * t + 291) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          100 * (37 * t + 28) * (259 * t + 291)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨10 * (101306 * t * t + 202538 * t + 104281), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 2738 * t + 2737 ≡ 2737 [ZMOD 2738] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 2738 * t + 2737)
    (pairedResidue := 2737) (pairedModulus := 2738)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoOddRootSpineLine {k q t r : Int}
    (hk : 1 ≤ k) (hq : q ≠ 0) (ht : t ≠ 0) (hr : r ≠ 0) :
    certificateValid
      ({ x := (-4 * (2 * k + 1)) * r +
            q * (4 * t - 1) * (2 * (2 * k + 1) * t - 1),
          y := (4 - (2 * k + 1) * (2 * k + 1)) * r +
            2 * q * t * (2 * k - 1) * ((2 * k + 1) * t + 2 * t - 1) } :
        Point)
      ({ x := (-4 * (2 * k + 1)) * r,
          y := (4 - (2 * k + 1) * (2 * k + 1)) * r } : Point) := by
  let target : Point :=
    { x := (-4 * (2 * k + 1)) * r +
          q * (4 * t - 1) * (2 * (2 * k + 1) * t - 1),
      y := (4 - (2 * k + 1) * (2 * k + 1)) * r +
          2 * q * t * (2 * k - 1) * ((2 * k + 1) * t + 2 * t - 1) }
  let midpoint : Point :=
    { x := (-4 * (2 * k + 1)) * r,
      y := (4 - (2 * k + 1) * (2 * k + 1)) * r }
  have hodd_pos : 0 < 2 * k + 1 := by omega
  have hfirst_x : -4 * (2 * k + 1) ≠ 0 := by
    exact mul_ne_zero (by norm_num) (ne_of_gt hodd_pos)
  have hfirst_y : 4 - (2 * k + 1) * (2 * k + 1) ≠ 0 := by
    nlinarith [hk, sq_nonneg (2 * k + 1)]
  have hfour : 4 * t - 1 ≠ 0 := by omega
  have hwide : 2 * (2 * k + 1) * t - 1 ≠ 0 := by
    intro hzero
    have hone : 2 * ((2 * k + 1) * t) = 1 := by nlinarith
    omega
  have hkfactor : 2 * k - 1 ≠ 0 := by omega
  have hnarrow : (2 * k + 1) * t + 2 * t - 1 ≠ 0 := by
    by_cases ht_nonneg : 0 ≤ t
    · have ht_pos : 1 ≤ t := by omega
      nlinarith [hk, ht_pos]
    · have ht_le : t ≤ -1 := by omega
      nlinarith [hk, ht_le]
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero hfirst_x hr
      · exact mul_ne_zero hfirst_y hr
    · refine ⟨((2 * k + 1) * (2 * k + 1) + 4) * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · have hx_factor : q * (4 * t - 1) *
            (2 * (2 * k + 1) * t - 1) ≠ 0 := by
          exact mul_ne_zero (mul_ne_zero hq hfour) hwide
        intro hx
        apply hx_factor
        simpa [target, midpoint, sub] using hx
      · have hy_factor :
            2 * q * t * (2 * k - 1) *
                ((2 * k + 1) * t + 2 * t - 1) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero
              (mul_ne_zero (mul_ne_zero (by norm_num) hq) ht)
              hkfactor)
            hnarrow
        intro hy
        apply hy_factor
        simpa [target, midpoint, sub] using hy
    · refine ⟨q * (8 * k * k * t * t + 8 * k * t * t -
          4 * k * t + 10 * t * t - 6 * t + 1), ?_⟩
      calc
        normSq (sub target midpoint)
            =
                sq (q * (4 * t - 1) * (2 * (2 * k + 1) * t - 1)) +
                sq (2 * q * t * (2 * k - 1) *
                    ((2 * k + 1) * t + 2 * t - 1)) := by
              simp [target, midpoint, normSq, sub, sq]
        _ = (q * (8 * k * k * t * t + 8 * k * t * t -
              4 * k * t + 10 * t * t - 6 * t + 1)) *
            (q * (8 * k * k * t * t + 8 * k * t * t -
              4 * k * t + 10 * t * t - 6 * t + 1)) := by
          simp [sq]
          ring_nf

theorem certificateValid_twoThreeOddGeneralRootSpineLine {m a b r : Int}
    (hm : m ≠ 0) (hdelta : 2 * a * a + 2 * a - 2 * b * b - 2 * b ≠ 0)
    (hr : r ≠ 0) :
    certificateValid
      ({ x := -12 * r - m * ((2 * a + 1) * (2 * b + 1)),
          y := -5 * r + m * (2 * a * a + 2 * a - 2 * b * b - 2 * b) } : Point)
      ({ x := -12 * r, y := -5 * r } : Point) := by
  let delta : Int := 2 * a * a + 2 * a - 2 * b * b - 2 * b
  let paired : Int := (2 * a + 1) * (2 * b + 1)
  let hyp : Int := 2 * a * a + 2 * a + 2 * b * b + 2 * b + 1
  let target : Point :=
    { x := -12 * r - m * paired,
      y := -5 * r + m * delta }
  let midpoint : Point := { x := -12 * r, y := -5 * r }
  have hodd_a : 2 * a + 1 ≠ 0 := by omega
  have hodd_b : 2 * b + 1 ≠ 0 := by omega
  have hpaired : paired ≠ 0 := mul_ne_zero hodd_a hodd_b
  have hstep_x_factor : m * paired ≠ 0 := mul_ne_zero hm hpaired
  have hstep_y_factor : m * delta ≠ 0 := by
    exact mul_ne_zero hm (by simpa [delta] using hdelta)
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num) hr
      · exact mul_ne_zero (by norm_num) hr
    · refine ⟨13 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · intro hx
        apply hstep_x_factor
        calc
          m * paired = -((-12 * r - m * paired) - (-12 * r)) := by ring
          _ = -((sub target midpoint).x) := by simp [target, midpoint, sub]
          _ = 0 := by rw [hx]; ring
      · intro hy
        apply hstep_y_factor
        simpa [target, midpoint, sub] using hy
    · refine ⟨m * hyp, ?_⟩
      calc
        normSq (sub target midpoint) = sq (m * paired) + sq (m * delta) := by
          simp [target, midpoint, normSq, sub, sq]
          ring
        _ = (m * hyp) * (m * hyp) := by
          simp [delta, paired, hyp, sq]
          ring_nf

theorem certificateValid_twoThreeOddSplitElevenResidueOneThirtyThreeLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -12, y := -5 } : Point) * r +
          det strip
            ({ x := -((78 * t + 29) * (-52 * t - 23)),
                y := 26 * (5 * t + 2) * (13 * t + 3) } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -12, y := -5 } : Point))
          ({ x := -((78 * t + 29) * (-52 * t - 23)),
              y := 26 * (5 * t + 2) * (13 * t + 3) } : Point))
        (smul r ({ x := -12, y := -5 } : Point)) ∧
      det strip
          (add (smul r ({ x := -12, y := -5 } : Point))
            ({ x := -((78 * t + 29) * (-52 * t - 23)),
                y := 26 * (5 * t + 2) * (13 * t + 3) } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      338 * t + 133 ≡ 133 [ZMOD 338] := by
  let direction : Point := { x := -12, y := -5 }
  let secondStep : Point :=
    { x := -((78 * t + 29) * (-52 * t - 23)),
      y := 26 * (5 * t + 2) * (13 * t + 3) }
  have hdelta :
      2 * (39 * t + 14) * (39 * t + 14) + 2 * (39 * t + 14) -
          2 * (-26 * t - 12) * (-26 * t - 12) - 2 * (-26 * t - 12) ≠ 0 := by
    have hfirst : 5 * t + 2 ≠ 0 := by omega
    have hsecond : 13 * t + 3 ≠ 0 := by omega
    have hprod : 26 * (5 * t + 2) * (13 * t + 3) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hzero
    apply hprod
    calc
      26 * (5 * t + 2) * (13 * t + 3)
          =
            2 * (39 * t + 14) * (39 * t + 14) + 2 * (39 * t + 14) -
              2 * (-26 * t - 12) * (-26 * t - 12) - 2 * (-26 * t - 12) := by
            ring
      _ = 0 := hzero
  have hline :
      certificateValid (add (smul r direction) secondStep) (smul r direction) := by
    have hraw :=
      certificateValid_twoThreeOddGeneralRootSpineLine
        (m := 1) (a := 39 * t + 14) (b := -26 * t - 12) (r := r)
        (by norm_num) hdelta hr
    convert hraw using 1
    · ext <;> simp [direction, secondStep, add, smul] <;> ring
    · ext <;> simp [direction, smul] <;> ring
  have hpaired : 338 * t + 133 ≡ 133 [ZMOD 338] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripRowValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 338 * t + 133)
    (pairedResidue := 133) (pairedModulus := 338)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hline hpaired hcoeff

theorem certificateValid_twoThreeOddGeneralRootSpineLineSwap {m a b r : Int}
    (hm : m ≠ 0) (hdelta : 2 * a * a + 2 * a - 2 * b * b - 2 * b ≠ 0)
    (hr : r ≠ 0) :
    certificateValid
      ({ x := -5 * r + m * (2 * a * a + 2 * a - 2 * b * b - 2 * b),
          y := -12 * r + m * ((2 * a + 1) * (2 * b + 1)) } : Point)
      ({ x := -5 * r, y := -12 * r } : Point) := by
  let delta : Int := 2 * a * a + 2 * a - 2 * b * b - 2 * b
  let paired : Int := (2 * a + 1) * (2 * b + 1)
  let hyp : Int := 2 * a * a + 2 * a + 2 * b * b + 2 * b + 1
  let target : Point :=
    { x := -5 * r + m * delta,
      y := -12 * r + m * paired }
  let midpoint : Point := { x := -5 * r, y := -12 * r }
  have hodd_a : 2 * a + 1 ≠ 0 := by omega
  have hodd_b : 2 * b + 1 ≠ 0 := by omega
  have hpaired : paired ≠ 0 := mul_ne_zero hodd_a hodd_b
  have hstep_x_factor : m * delta ≠ 0 := by
    exact mul_ne_zero hm (by simpa [delta] using hdelta)
  have hstep_y_factor : m * paired ≠ 0 := mul_ne_zero hm hpaired
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num) hr
      · exact mul_ne_zero (by norm_num) hr
    · refine ⟨13 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · intro hx
        apply hstep_x_factor
        calc
          m * delta = (-5 * r + m * delta) - (-5 * r) := by ring
          _ = (sub target midpoint).x := by simp [target, midpoint, sub]
          _ = 0 := hx
      · intro hy
        apply hstep_y_factor
        calc
          m * paired = (-12 * r + m * paired) - (-12 * r) := by ring
          _ = (sub target midpoint).y := by simp [target, midpoint, sub]
          _ = 0 := hy
    · refine ⟨m * hyp, ?_⟩
      calc
        normSq (sub target midpoint) = sq (m * delta) + sq (m * paired) := by
          simp [target, midpoint, normSq, sub, sq]
        _ = (m * hyp) * (m * hyp) := by
          simp [delta, paired, hyp, sq]
          ring_nf

theorem certificateValid_twoThreeOddSplitElevenResidueTwentyThreeLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ -3) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -5, y := -12 } : Point) * r +
          det strip
            ({ x := 2 * (t + 3) * (5 * t + 4),
                y := (-6 * t - 7) * (-4 * t - 1) } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -5, y := -12 } : Point))
          ({ x := 2 * (t + 3) * (5 * t + 4),
              y := (-6 * t - 7) * (-4 * t - 1) } : Point))
        (smul r ({ x := -5, y := -12 } : Point)) ∧
      det strip
          (add (smul r ({ x := -5, y := -12 } : Point))
            ({ x := 2 * (t + 3) * (5 * t + 4),
                y := (-6 * t - 7) * (-4 * t - 1) } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      26 * t + 23 ≡ 23 [ZMOD 26] := by
  let direction : Point := { x := -5, y := -12 }
  let secondStep : Point :=
    { x := 2 * (t + 3) * (5 * t + 4),
      y := (-6 * t - 7) * (-4 * t - 1) }
  have hdelta :
      2 * (-3 * t - 4) * (-3 * t - 4) + 2 * (-3 * t - 4) -
          2 * (-2 * t - 1) * (-2 * t - 1) - 2 * (-2 * t - 1) ≠ 0 := by
    have hfirst : t + 3 ≠ 0 := by omega
    have hsecond : 5 * t + 4 ≠ 0 := by omega
    have hprod : 2 * (t + 3) * (5 * t + 4) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) hfirst) hsecond
    intro hzero
    apply hprod
    calc
      2 * (t + 3) * (5 * t + 4)
          =
            2 * (-3 * t - 4) * (-3 * t - 4) + 2 * (-3 * t - 4) -
              2 * (-2 * t - 1) * (-2 * t - 1) - 2 * (-2 * t - 1) := by
            ring
      _ = 0 := hzero
  have hline :
      certificateValid (add (smul r direction) secondStep) (smul r direction) := by
    have hraw :=
      certificateValid_twoThreeOddGeneralRootSpineLineSwap
        (m := 1) (a := -3 * t - 4) (b := -2 * t - 1) (r := r)
        (by norm_num) hdelta hr
    convert hraw using 1
    · ext <;> simp [direction, secondStep, add, smul] <;> ring
    · ext <;> simp [direction, smul] <;> ring
  have hpaired : 26 * t + 23 ≡ 23 [ZMOD 26] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripRowValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 26 * t + 23)
    (pairedResidue := 23) (pairedModulus := 26)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hline hpaired hcoeff

theorem certificateValid_twoThreeEvenRootSpineLine {m a b r : Int}
    (hm : m ≠ 0) (ha : a ≠ 0) (hb : b ≠ 0)
    (hab : a * a ≠ b * b) (hr : r ≠ 0) :
    certificateValid
      ({ x := -12 * r - 2 * m * a * b,
          y := -5 * r + m * (a * a - b * b) } : Point)
      ({ x := -12 * r, y := -5 * r } : Point) := by
  let target : Point :=
    { x := -12 * r - 2 * m * a * b,
      y := -5 * r + m * (a * a - b * b) }
  let midpoint : Point := { x := -12 * r, y := -5 * r }
  have hdiff : a * a - b * b ≠ 0 := sub_ne_zero.mpr hab
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num : (-12 : Int) ≠ 0) hr
      · exact mul_ne_zero (by norm_num : (-5 : Int) ≠ 0) hr
    · refine ⟨13 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · intro hx
        have hx_factor : -2 * m * a * b ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (mul_ne_zero (by norm_num) hm) ha) hb
        apply hx_factor
        have hx' := hx
        simp [sub] at hx'
        nlinarith
      · intro hy
        have hy' := hy
        simp [sub] at hy'
        rcases hy' with hm0 | hdiff0
        · exact hm hm0
        · exact hdiff hdiff0
    · refine ⟨m * (a * a + b * b), ?_⟩
      calc
        normSq (sub target midpoint)
            =
                sq (-2 * m * a * b) +
                sq (m * (a * a - b * b)) := by
              simp [target, midpoint, normSq, sub, sq]
              ring
        _ = (m * (a * a + b * b)) * (m * (a * a + b * b)) := by
          simp [sq]
          ring_nf

theorem certificateValid_twoFiveRootSpineLine {m a b r : Int}
    (hm : m ≠ 0) (ha : a ≠ 0) (hb : b ≠ 0)
    (hab : a * a ≠ b * b) (hr : r ≠ 0) :
    certificateValid
      ({ x := -20 * r + 2 * m * a * b,
          y := 21 * r - m * (a * a - b * b) } : Point)
      ({ x := -20 * r, y := 21 * r } : Point) := by
  let target : Point :=
    { x := -20 * r + 2 * m * a * b,
      y := 21 * r - m * (a * a - b * b) }
  let midpoint : Point := { x := -20 * r, y := 21 * r }
  have habfactor : m * (a * a - b * b) ≠ 0 := by
    exact mul_ne_zero hm (sub_ne_zero.mpr hab)
  have hstep_x_factor : 2 * m * a * b ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hm) ha) hb
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num) hr
      · exact mul_ne_zero (by norm_num) hr
    · refine ⟨29 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · intro hx
        have hx_factor : 2 * m * a * b ≠ 0 := hstep_x_factor
        apply hx_factor
        simpa [target, midpoint, sub] using hx
      · intro hy
        apply habfactor
        simpa [target, midpoint, sub] using hy
    · refine ⟨m * (a * a + b * b), ?_⟩
      calc
        normSq (sub target midpoint)
            = sq (2 * m * a * b) + sq (m * (a * a - b * b)) := by
              simp [target, midpoint, normSq, sub, sq]
        _ = (m * (a * a + b * b)) * (m * (a * a + b * b)) := by
          simp [sq]
          ring_nf

theorem certificateValid_twoFiveRootSpineLineSwap {m a b r : Int}
    (hm : m ≠ 0) (ha : a ≠ 0) (hb : b ≠ 0)
    (hab : a * a ≠ b * b) (hr : r ≠ 0) :
    certificateValid
      ({ x := -21 * r + m * (a * a - b * b),
          y := 20 * r + 2 * m * a * b } : Point)
      ({ x := -21 * r, y := 20 * r } : Point) := by
  let target : Point :=
    { x := -21 * r + m * (a * a - b * b),
      y := 20 * r + 2 * m * a * b }
  let midpoint : Point := { x := -21 * r, y := 20 * r }
  have habfactor : m * (a * a - b * b) ≠ 0 := by
    exact mul_ne_zero hm (sub_ne_zero.mpr hab)
  have hstep_x_factor : 2 * m * a * b ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hm) ha) hb
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num) hr
      · exact mul_ne_zero (by norm_num) hr
    · refine ⟨29 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · intro hx
        have hx_factor : m * (a * a - b * b) ≠ 0 := habfactor
        apply hx_factor
        simpa [target, midpoint, sub] using hx
      · intro hy
        have hy_factor : 2 * m * a * b ≠ 0 := hstep_x_factor
        apply hy_factor
        simpa [target, midpoint, sub] using hy
    · refine ⟨m * (a * a + b * b), ?_⟩
      calc
        normSq (sub target midpoint)
            = sq (m * (a * a - b * b)) + sq (2 * m * a * b) := by
              simp [target, midpoint, normSq, sub, sq]
        _ = (m * (a * a + b * b)) * (m * (a * a + b * b)) := by
          simp [sq]
          ring_nf

theorem certificateValid_twoFiveSplitOneFifteenEightyThreeResidueTwelveLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -21, y := 20 } : Point) * r +
          det strip
            ({ x := 5 * ((5 * t + 2) * (5 * t + 2) -
                  (-2 * t - 1) * (-2 * t - 1)),
                y := 10 * (5 * t + 2) * (-2 * t - 1) } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -21, y := 20 } : Point))
          ({ x := 5 * ((5 * t + 2) * (5 * t + 2) -
                (-2 * t - 1) * (-2 * t - 1)),
              y := 10 * (5 * t + 2) * (-2 * t - 1) } : Point))
        (smul r ({ x := -21, y := 20 } : Point)) ∧
      det strip
          (add (smul r ({ x := -21, y := 20 } : Point))
            ({ x := 5 * ((5 * t + 2) * (5 * t + 2) -
                  (-2 * t - 1) * (-2 * t - 1)),
                y := 10 * (5 * t + 2) * (-2 * t - 1) } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      29 * t + 12 ≡ 12 [ZMOD 29] := by
  let direction : Point := { x := -21, y := 20 }
  let secondStep : Point :=
    { x := 5 * ((5 * t + 2) * (5 * t + 2) -
          (-2 * t - 1) * (-2 * t - 1)),
      y := 10 * (5 * t + 2) * (-2 * t - 1) }
  have ha : 5 * t + 2 ≠ 0 := by omega
  have hb : -2 * t - 1 ≠ 0 := by omega
  have hab : (5 * t + 2) * (5 * t + 2) ≠
      (-2 * t - 1) * (-2 * t - 1) := by
    intro hsq
    have hprod : (7 * t + 3) * (3 * t + 1) = 0 := by
      calc
        (7 * t + 3) * (3 * t + 1)
            =
              (5 * t + 2) * (5 * t + 2) -
                (-2 * t - 1) * (-2 * t - 1) := by
              ring
        _ = 0 := by rw [hsq]; ring
    exact (mul_ne_zero (by omega) (by omega)) hprod
  have hline :
      certificateValid (add (smul r direction) secondStep) (smul r direction) := by
    have hraw :=
      certificateValid_twoFiveRootSpineLineSwap
        (m := 5) (a := 5 * t + 2) (b := -2 * t - 1) (r := r)
        (by norm_num) ha hb hab hr
    convert hraw using 1
    · ext <;> simp [direction, secondStep, add, smul] <;> ring
    · ext <;> simp [direction, smul] <;> ring
  have hpaired : 29 * t + 12 ≡ 12 [ZMOD 29] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripRowValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 29 * t + 12)
    (pairedResidue := 12) (pairedModulus := 29)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hline hpaired hcoeff

theorem certificateValid_twoFiveSplitOneFifteenEightyThreeResidueTwentyEightLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -20, y := 21 } : Point) * r +
          det strip
            ({ x := 10 * (-5 * t - 114) * (-2 * t + 271),
                y := -5 * ((-5 * t - 114) * (-5 * t - 114) -
                  (-2 * t + 271) * (-2 * t + 271)) } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -20, y := 21 } : Point))
          ({ x := 10 * (-5 * t - 114) * (-2 * t + 271),
              y := -5 * ((-5 * t - 114) * (-5 * t - 114) -
                (-2 * t + 271) * (-2 * t + 271)) } : Point))
        (smul r ({ x := -20, y := 21 } : Point)) ∧
      det strip
          (add (smul r ({ x := -20, y := 21 } : Point))
            ({ x := 10 * (-5 * t - 114) * (-2 * t + 271),
                y := -5 * ((-5 * t - 114) * (-5 * t - 114) -
                  (-2 * t + 271) * (-2 * t + 271)) } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      29 * t + 28 ≡ 28 [ZMOD 29] := by
  let direction : Point := { x := -20, y := 21 }
  let secondStep : Point :=
    { x := 10 * (-5 * t - 114) * (-2 * t + 271),
      y := -5 * ((-5 * t - 114) * (-5 * t - 114) -
        (-2 * t + 271) * (-2 * t + 271)) }
  have ha : -5 * t - 114 ≠ 0 := by omega
  have hb : -2 * t + 271 ≠ 0 := by omega
  have hab : (-5 * t - 114) * (-5 * t - 114) ≠
      (-2 * t + 271) * (-2 * t + 271) := by
    intro hsq
    have hprod : (-3 * t - 385) * (-7 * t + 157) = 0 := by
      calc
        (-3 * t - 385) * (-7 * t + 157)
            =
              (-5 * t - 114) * (-5 * t - 114) -
                (-2 * t + 271) * (-2 * t + 271) := by
              ring
        _ = 0 := by rw [hsq]; ring
    exact (mul_ne_zero (by omega) (by omega)) hprod
  have hline :
      certificateValid (add (smul r direction) secondStep) (smul r direction) := by
    have hraw :=
      certificateValid_twoFiveRootSpineLine
        (m := 5) (a := -5 * t - 114) (b := -2 * t + 271) (r := r)
        (by norm_num) ha hb hab hr
    convert hraw using 1
    · ext <;> simp [direction, secondStep, add, smul] <;> ring
    · ext <;> simp [direction, smul] <;> ring
  have hpaired : 29 * t + 28 ≡ 28 [ZMOD 29] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripRowValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 29 * t + 28)
    (pairedResidue := 28) (pairedModulus := 29)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hline hpaired hcoeff

theorem certificateValid_twoFiveSplitOneFifteenEightyThreeLineStrip :
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -21, y := 20 } : Point) * r +
          det strip
            ({ x := 5 * ((5 * t + 2) * (5 * t + 2) -
                  (-2 * t - 1) * (-2 * t - 1)),
                y := 10 * (5 * t + 2) * (-2 * t - 1) } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -21, y := 20 } : Point))
            ({ x := 5 * ((5 * t + 2) * (5 * t + 2) -
                  (-2 * t - 1) * (-2 * t - 1)),
                y := 10 * (5 * t + 2) * (-2 * t - 1) } : Point))
          (smul r ({ x := -21, y := 20 } : Point)) ∧
        det strip
            (add (smul r ({ x := -21, y := 20 } : Point))
              ({ x := 5 * ((5 * t + 2) * (5 * t + 2) -
                    (-2 * t - 1) * (-2 * t - 1)),
                  y := 10 * (5 * t + 2) * (-2 * t - 1) } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        29 * t + 12 ≡ 12 [ZMOD 29]) ∧
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -20, y := 21 } : Point) * r +
          det strip
            ({ x := 10 * (-5 * t - 114) * (-2 * t + 271),
                y := -5 * ((-5 * t - 114) * (-5 * t - 114) -
                  (-2 * t + 271) * (-2 * t + 271)) } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -20, y := 21 } : Point))
            ({ x := 10 * (-5 * t - 114) * (-2 * t + 271),
                y := -5 * ((-5 * t - 114) * (-5 * t - 114) -
                  (-2 * t + 271) * (-2 * t + 271)) } : Point))
          (smul r ({ x := -20, y := 21 } : Point)) ∧
        det strip
            (add (smul r ({ x := -20, y := 21 } : Point))
              ({ x := 10 * (-5 * t - 114) * (-2 * t + 271),
                  y := -5 * ((-5 * t - 114) * (-5 * t - 114) -
                    (-2 * t + 271) * (-2 * t + 271)) } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        29 * t + 28 ≡ 28 [ZMOD 29]) := by
  constructor
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_twoFiveSplitOneFifteenEightyThreeResidueTwelveLineStrip
      (strip := strip) hr hcoeff
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_twoFiveSplitOneFifteenEightyThreeResidueTwentyEightLineStrip
      (strip := strip) hr hcoeff

theorem certificateValid_twoFiveOddSquareclassTwentyThreeSplitFifteenFortyNineResidueFiftySevenLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -21, y := 20 } : Point) * r +
          det strip
            ({ x := 966 * t * t - 47242 * t - 736368,
                y := -920 * t * t - 53406 * t + 604601 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -21, y := 20 } : Point))
          ({ x := 966 * t * t - 47242 * t - 736368,
              y := -920 * t * t - 53406 * t + 604601 } : Point))
        (smul r ({ x := -21, y := 20 } : Point)) ∧
      det strip
          (add (smul r ({ x := -21, y := 20 } : Point))
            ({ x := 966 * t * t - 47242 * t - 736368,
                y := -920 * t * t - 53406 * t + 604601 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      58 * t + 57 ≡ 57 [ZMOD 58] := by
  let direction : Point := { x := -21, y := 20 }
  let secondStep : Point :=
    { x := 966 * t * t - 47242 * t - 736368,
      y := -920 * t * t - 53406 * t + 604601 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨29, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 46 * (3 * t - 184) * (7 * t + 87) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          46 * (3 * t - 184) * (7 * t + 87)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -23 * (4 * t + 271) * (10 * t - 97) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -23 * (4 * t + 271) * (10 * t - 97)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨23 * (58 * t * t + 114 * t + 41425), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 58 * t + 57 ≡ 57 [ZMOD 58] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 58 * t + 57)
    (pairedResidue := 57) (pairedModulus := 58)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoFiveOddSquareclassTwentyThreeSplitFifteenFortyNineResidueSeventeenLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -20, y := 21 } : Point) * r +
          det strip
            ({ x := 920 * t * t + 506 * t + 69,
                y := -966 * t * t - 598 * t - 92 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -20, y := 21 } : Point))
          ({ x := 920 * t * t + 506 * t + 69,
              y := -966 * t * t - 598 * t - 92 } : Point))
        (smul r ({ x := -20, y := 21 } : Point)) ∧
      det strip
          (add (smul r ({ x := -20, y := 21 } : Point))
            ({ x := 920 * t * t + 506 * t + 69,
                y := -966 * t * t - 598 * t - 92 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      58 * t + 17 ≡ 17 [ZMOD 58] := by
  let direction : Point := { x := -20, y := 21 }
  let secondStep : Point :=
    { x := 920 * t * t + 506 * t + 69,
      y := -966 * t * t - 598 * t - 92 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨29, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 23 * (4 * t + 1) * (10 * t + 3) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          23 * (4 * t + 1) * (10 * t + 3)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -46 * (3 * t + 1) * (7 * t + 2) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -46 * (3 * t + 1) * (7 * t + 2)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨23 * (58 * t * t + 34 * t + 5), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 58 * t + 17 ≡ 17 [ZMOD 58] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 58 * t + 17)
    (pairedResidue := 17) (pairedModulus := 58)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoFiveOddSquareclassTwentyThreeSplitFifteenFortyNineLineStrip :
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -21, y := 20 } : Point) * r +
          det strip
            ({ x := 966 * t * t - 47242 * t - 736368,
                y := -920 * t * t - 53406 * t + 604601 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -21, y := 20 } : Point))
            ({ x := 966 * t * t - 47242 * t - 736368,
                y := -920 * t * t - 53406 * t + 604601 } : Point))
          (smul r ({ x := -21, y := 20 } : Point)) ∧
        det strip
            (add (smul r ({ x := -21, y := 20 } : Point))
              ({ x := 966 * t * t - 47242 * t - 736368,
                  y := -920 * t * t - 53406 * t + 604601 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        58 * t + 57 ≡ 57 [ZMOD 58]) ∧
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -20, y := 21 } : Point) * r +
          det strip
            ({ x := 920 * t * t + 506 * t + 69,
                y := -966 * t * t - 598 * t - 92 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -20, y := 21 } : Point))
            ({ x := 920 * t * t + 506 * t + 69,
                y := -966 * t * t - 598 * t - 92 } : Point))
          (smul r ({ x := -20, y := 21 } : Point)) ∧
        det strip
            (add (smul r ({ x := -20, y := 21 } : Point))
              ({ x := 920 * t * t + 506 * t + 69,
                  y := -966 * t * t - 598 * t - 92 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        58 * t + 17 ≡ 17 [ZMOD 58]) := by
  constructor
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_twoFiveOddSquareclassTwentyThreeSplitFifteenFortyNineResidueFiftySevenLineStrip
      (strip := strip) hr hcoeff
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_twoFiveOddSquareclassTwentyThreeSplitFifteenFortyNineResidueSeventeenLineStrip
      (strip := strip) hr hcoeff

theorem certificateValid_twoSevenOddSplitOneSeventyNineTwoTwentyNineResidueEightyNineLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -45, y := 28 } : Point) * r +
          det strip
            ({ x := 90 * t * t - 38 * t - 352,
                y := -56 * t * t - 398 * t - 135 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -45, y := 28 } : Point))
          ({ x := 90 * t * t - 38 * t - 352,
              y := -56 * t * t - 398 * t - 135 } : Point))
        (smul r ({ x := -45, y := 28 } : Point)) ∧
      det strip
          (add (smul r ({ x := -45, y := 28 } : Point))
            ({ x := 90 * t * t - 38 * t - 352,
                y := -56 * t * t - 398 * t - 135 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      106 * t + 89 ≡ 89 [ZMOD 106] := by
  let direction : Point := { x := -45, y := 28 }
  let secondStep : Point :=
    { x := 90 * t * t - 38 * t - 352,
      y := -56 * t * t - 398 * t - 135 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨53, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 2 * (5 * t - 11) * (9 * t + 16) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          2 * (5 * t - 11) * (9 * t + 16)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -(4 * t + 27) * (14 * t + 5) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          -(4 * t + 27) * (14 * t + 5)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨106 * t * t + 178 * t + 377, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 106 * t + 89 ≡ 89 [ZMOD 106] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 106 * t + 89)
    (pairedResidue := 89) (pairedModulus := 106)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoSevenOddSplitOneSeventyNineTwoTwentyNineResidueThirtyThreeLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -28, y := 45 } : Point) * r +
          det strip
            ({ x := 56 * t * t - 354 * t - 377,
                y := -90 * t * t - 298 * t + 336 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -28, y := 45 } : Point))
          ({ x := 56 * t * t - 354 * t - 377,
              y := -90 * t * t - 298 * t + 336 } : Point))
        (smul r ({ x := -28, y := 45 } : Point)) ∧
      det strip
          (add (smul r ({ x := -28, y := 45 } : Point))
            ({ x := 56 * t * t - 354 * t - 377,
                y := -90 * t * t - 298 * t + 336 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      106 * t + 33 ≡ 33 [ZMOD 106] := by
  let direction : Point := { x := -28, y := 45 }
  let secondStep : Point :=
    { x := 56 * t * t - 354 * t - 377,
      y := -90 * t * t - 298 * t + 336 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨53, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : (4 * t - 29) * (14 * t + 13) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          (4 * t - 29) * (14 * t + 13)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -2 * (5 * t + 21) * (9 * t - 8) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -2 * (5 * t + 21) * (9 * t - 8)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨106 * t * t + 66 * t + 505, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 106 * t + 33 ≡ 33 [ZMOD 106] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 106 * t + 33)
    (pairedResidue := 33) (pairedModulus := 106)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoSevenOddSplitOneSeventyNineTwoTwentyNineLineStrip :
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -45, y := 28 } : Point) * r +
          det strip
            ({ x := 90 * t * t - 38 * t - 352,
                y := -56 * t * t - 398 * t - 135 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -45, y := 28 } : Point))
            ({ x := 90 * t * t - 38 * t - 352,
                y := -56 * t * t - 398 * t - 135 } : Point))
          (smul r ({ x := -45, y := 28 } : Point)) ∧
        det strip
            (add (smul r ({ x := -45, y := 28 } : Point))
              ({ x := 90 * t * t - 38 * t - 352,
                  y := -56 * t * t - 398 * t - 135 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        106 * t + 89 ≡ 89 [ZMOD 106]) ∧
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -28, y := 45 } : Point) * r +
          det strip
            ({ x := 56 * t * t - 354 * t - 377,
                y := -90 * t * t - 298 * t + 336 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -28, y := 45 } : Point))
            ({ x := 56 * t * t - 354 * t - 377,
                y := -90 * t * t - 298 * t + 336 } : Point))
          (smul r ({ x := -28, y := 45 } : Point)) ∧
        det strip
            (add (smul r ({ x := -28, y := 45 } : Point))
              ({ x := 56 * t * t - 354 * t - 377,
                  y := -90 * t * t - 298 * t + 336 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        106 * t + 33 ≡ 33 [ZMOD 106]) := by
  constructor
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_twoSevenOddSplitOneSeventyNineTwoTwentyNineResidueEightyNineLineStrip
      (strip := strip) hr hcoeff
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_twoSevenOddSplitOneSeventyNineTwoTwentyNineResidueThirtyThreeLineStrip
      (strip := strip) hr hcoeff

theorem certificateValid_twoSevenEvenSplitNineteenElevenFiftyThreeResidueThirteenLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -45, y := 28 } : Point) * r +
          det strip
            ({ x := 45 * t * t + 2 * t - 8,
                y := -28 * t * t - 46 * t - 6 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -45, y := 28 } : Point))
          ({ x := 45 * t * t + 2 * t - 8,
              y := -28 * t * t - 46 * t - 6 } : Point))
        (smul r ({ x := -45, y := 28 } : Point)) ∧
      det strip
          (add (smul r ({ x := -45, y := 28 } : Point))
            ({ x := 45 * t * t + 2 * t - 8,
                y := -28 * t * t - 46 * t - 6 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      53 * t + 13 ≡ 13 [ZMOD 53] := by
  let direction : Point := { x := -45, y := 28 }
  let secondStep : Point :=
    { x := 45 * t * t + 2 * t - 8,
      y := -28 * t * t - 46 * t - 6 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨53, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : (5 * t - 2) * (9 * t + 4) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          (5 * t - 2) * (9 * t + 4)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -2 * (2 * t + 3) * (7 * t + 1) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -2 * (2 * t + 3) * (7 * t + 1)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨53 * t * t + 26 * t + 10, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 53 * t + 13 ≡ 13 [ZMOD 53] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 53 * t + 13)
    (pairedResidue := 13) (pairedModulus := 53)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoSevenEvenSplitNineteenElevenFiftyThreeResidueThirtyFourLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -28, y := 45 } : Point) * r +
          det strip
            ({ x := 28 * t * t - 1922 * t - 14496,
                y := -45 * t * t - 1276 * t + 20497 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -28, y := 45 } : Point))
          ({ x := 28 * t * t - 1922 * t - 14496,
              y := -45 * t * t - 1276 * t + 20497 } : Point))
        (smul r ({ x := -28, y := 45 } : Point)) ∧
      det strip
          (add (smul r ({ x := -28, y := 45 } : Point))
            ({ x := 28 * t * t - 1922 * t - 14496,
                y := -45 * t * t - 1276 * t + 20497 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      53 * t + 34 ≡ 34 [ZMOD 53] := by
  let direction : Point := { x := -28, y := 45 }
  let secondStep : Point :=
    { x := 28 * t * t - 1922 * t - 14496,
      y := -45 * t * t - 1276 * t + 20497 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨53, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 2 * (2 * t - 151) * (7 * t + 48) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          2 * (2 * t - 151) * (7 * t + 48)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -(5 * t + 199) * (9 * t - 103) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          -(5 * t + 199) * (9 * t - 103)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨53 * t * t + 68 * t + 25105, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 53 * t + 34 ≡ 34 [ZMOD 53] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 53 * t + 34)
    (pairedResidue := 34) (pairedModulus := 53)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoSevenEvenSplitNineteenElevenFiftyThreeLineStrip :
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -45, y := 28 } : Point) * r +
          det strip
            ({ x := 45 * t * t + 2 * t - 8,
                y := -28 * t * t - 46 * t - 6 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -45, y := 28 } : Point))
            ({ x := 45 * t * t + 2 * t - 8,
                y := -28 * t * t - 46 * t - 6 } : Point))
          (smul r ({ x := -45, y := 28 } : Point)) ∧
        det strip
            (add (smul r ({ x := -45, y := 28 } : Point))
              ({ x := 45 * t * t + 2 * t - 8,
                  y := -28 * t * t - 46 * t - 6 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        53 * t + 13 ≡ 13 [ZMOD 53]) ∧
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -28, y := 45 } : Point) * r +
          det strip
            ({ x := 28 * t * t - 1922 * t - 14496,
                y := -45 * t * t - 1276 * t + 20497 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -28, y := 45 } : Point))
            ({ x := 28 * t * t - 1922 * t - 14496,
                y := -45 * t * t - 1276 * t + 20497 } : Point))
          (smul r ({ x := -28, y := 45 } : Point)) ∧
        det strip
            (add (smul r ({ x := -28, y := 45 } : Point))
              ({ x := 28 * t * t - 1922 * t - 14496,
                  y := -45 * t * t - 1276 * t + 20497 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        53 * t + 34 ≡ 34 [ZMOD 53]) := by
  constructor
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_twoSevenEvenSplitNineteenElevenFiftyThreeResidueThirteenLineStrip
      (strip := strip) hr hcoeff
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_twoSevenEvenSplitNineteenElevenFiftyThreeResidueThirtyFourLineStrip
      (strip := strip) hr hcoeff

theorem certificateValid_twoThreeOddSplitOneHundredSevenOneFifteenResidueTwoThirtyOneLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -12, y := 5 } : Point) * r +
          det strip
            ({ x := 4056 * t * t + 4394 * t + 639,
                y := -1690 * t * t - 5070 * t - 2480 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -12, y := 5 } : Point))
          ({ x := 4056 * t * t + 4394 * t + 639,
              y := -1690 * t * t - 5070 * t - 2480 } : Point))
        (smul r ({ x := -12, y := 5 } : Point)) ∧
      det strip
          (add (smul r ({ x := -12, y := 5 } : Point))
            ({ x := 4056 * t * t + 4394 * t + 639,
                y := -1690 * t * t - 5070 * t - 2480 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      338 * t + 231 ≡ 231 [ZMOD 338] := by
  let direction : Point := { x := -12, y := 5 }
  let secondStep : Point :=
    { x := 4056 * t * t + 4394 * t + 639,
      y := -1690 * t * t - 5070 * t - 2480 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : (52 * t + 9) * (78 * t + 71) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          (52 * t + 9) * (78 * t + 71)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -10 * (13 * t + 8) * (13 * t + 31) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -10 * (13 * t + 8) * (13 * t + 31)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨13 * (338 * t * t + 462 * t + 197), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 338 * t + 231 ≡ 231 [ZMOD 338] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 338 * t + 231)
    (pairedResidue := 231) (pairedModulus := 338)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeOddSplitTwentyThreeFiveThirtyFiveResidueOneFortyOneLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -5, y := 12 } : Point) * r +
          det strip
            ({ x := 1690 * t * t + 858 * t + 56,
                y := -4056 * t * t - 3614 * t - 783 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -5, y := 12 } : Point))
          ({ x := 1690 * t * t + 858 * t + 56,
              y := -4056 * t * t - 3614 * t - 783 } : Point))
        (smul r ({ x := -5, y := 12 } : Point)) ∧
      det strip
          (add (smul r ({ x := -5, y := 12 } : Point))
            ({ x := 1690 * t * t + 858 * t + 56,
                y := -4056 * t * t - 3614 * t - 783 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      338 * t + 141 ≡ 141 [ZMOD 338] := by
  let direction : Point := { x := -5, y := 12 }
  let secondStep : Point :=
    { x := 1690 * t * t + 858 * t + 56,
      y := -4056 * t * t - 3614 * t - 783 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 2 * (13 * t + 1) * (65 * t + 28) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          2 * (13 * t + 1) * (65 * t + 28)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -(52 * t + 27) * (78 * t + 29) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          -(52 * t + 27) * (78 * t + 29)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨4394 * t * t + 3666 * t + 785, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 338 * t + 141 ≡ 141 [ZMOD 338] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 338 * t + 141)
    (pairedResidue := 141) (pairedModulus := 338)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeOddSplitElevenTwoFiftySevenResidueEightyOneLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -12, y := -5 } : Point) * r +
          det strip
            ({ x := 4056 * t * t + 2054 * t + 255,
                y := 1690 * t * t + 546 * t + 32 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -12, y := -5 } : Point))
          ({ x := 4056 * t * t + 2054 * t + 255,
              y := 1690 * t * t + 546 * t + 32 } : Point))
        (smul r ({ x := -12, y := -5 } : Point)) ∧
      det strip
          (add (smul r ({ x := -12, y := -5 } : Point))
            ({ x := 4056 * t * t + 2054 * t + 255,
                y := 1690 * t * t + 546 * t + 32 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      338 * t + 81 ≡ 81 [ZMOD 338] := by
  let direction : Point := { x := -12, y := -5 }
  let secondStep : Point :=
    { x := 4056 * t * t + 2054 * t + 255,
      y := 1690 * t * t + 546 * t + 32 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : (52 * t + 15) * (78 * t + 17) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          (52 * t + 15) * (78 * t + 17)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : 2 * (13 * t + 1) * (65 * t + 16) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          2 * (13 * t + 1) * (65 * t + 16)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨4394 * t * t + 2106 * t + 257, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 338 * t + 81 ≡ 81 [ZMOD 338] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 338 * t + 81)
    (pairedResidue := 81) (pairedModulus := 338)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeOddSplitElevenTwoFiftySevenResidueTwentyThreeLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ -3) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -5, y := -12 } : Point) * r +
          det strip
            ({ x := 10 * t * t + 38 * t + 24,
                y := 24 * t * t + 34 * t + 7 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -5, y := -12 } : Point))
          ({ x := 10 * t * t + 38 * t + 24,
              y := 24 * t * t + 34 * t + 7 } : Point))
        (smul r ({ x := -5, y := -12 } : Point)) ∧
      det strip
          (add (smul r ({ x := -5, y := -12 } : Point))
            ({ x := 10 * t * t + 38 * t + 24,
                y := 24 * t * t + 34 * t + 7 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      26 * t + 23 ≡ 23 [ZMOD 26] := by
  let direction : Point := { x := -5, y := -12 }
  let secondStep : Point :=
    { x := 10 * t * t + 38 * t + 24,
      y := 24 * t * t + 34 * t + 7 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 2 * (t + 3) * (5 * t + 4) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          2 * (t + 3) * (5 * t + 4)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : (4 * t + 1) * (6 * t + 7) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          (4 * t + 1) * (6 * t + 7)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨26 * t * t + 46 * t + 25, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 26 * t + 23 ≡ 23 [ZMOD 26] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 26 * t + 23)
    (pairedResidue := 23) (pairedModulus := 26)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeOddSplitSixtySevenTwoFiftySevenResidueThreeLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ -13) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -12, y := 5 } : Point) * r +
          det strip
            ({ x := 24 * t * t - 46 * t - 165,
                y := -10 * t * t - 126 * t + 52 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -12, y := 5 } : Point))
          ({ x := 24 * t * t - 46 * t - 165,
              y := -10 * t * t - 126 * t + 52 } : Point))
        (smul r ({ x := -12, y := 5 } : Point)) ∧
      det strip
          (add (smul r ({ x := -12, y := 5 } : Point))
            ({ x := 24 * t * t - 46 * t - 165,
                y := -10 * t * t - 126 * t + 52 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      26 * t + 3 ≡ 3 [ZMOD 26] := by
  let direction : Point := { x := -12, y := 5 }
  let secondStep : Point :=
    { x := 24 * t * t - 46 * t - 165,
      y := -10 * t * t - 126 * t + 52 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : (4 * t - 15) * (6 * t + 11) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          (4 * t - 15) * (6 * t + 11)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -2 * (t + 13) * (5 * t - 2) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -2 * (t + 13) * (5 * t - 2)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨26 * t * t + 6 * t + 173, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 26 * t + 3 ≡ 3 [ZMOD 26] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 26 * t + 3)
    (pairedResidue := 3) (pairedModulus := 26)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeOddSplitSixtySevenTwoFiftySevenResidueElevenLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ 49) (hr : r ≠ 0)
    (hcoeff :
          det strip ({ x := -5, y := 12 } : Point) * r +
          det strip
            ({ x := 10 * t * t - 466 * t - 1176,
                y := -24 * t * t - 218 * t + 2257 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -5, y := 12 } : Point))
          ({ x := 10 * t * t - 466 * t - 1176,
              y := -24 * t * t - 218 * t + 2257 } : Point))
        (smul r ({ x := -5, y := 12 } : Point)) ∧
      det strip
          (add (smul r ({ x := -5, y := 12 } : Point))
            ({ x := 10 * t * t - 466 * t - 1176,
                y := -24 * t * t - 218 * t + 2257 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      26 * t + 11 ≡ 11 [ZMOD 26] := by
  let direction : Point := { x := -5, y := 12 }
  let secondStep : Point :=
    { x := 10 * t * t - 466 * t - 1176,
      y := -24 * t * t - 218 * t + 2257 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨13, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 2 * (t - 49) * (5 * t + 12) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          2 * (t - 49) * (5 * t + 12)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -(4 * t + 61) * (6 * t - 37) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          -(4 * t + 61) * (6 * t - 37)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨26 * t * t + 22 * t + 2545, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 26 * t + 11 ≡ 11 [ZMOD 26] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 26 * t + 11)
    (pairedResidue := 11) (pairedModulus := 26)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_twoThreeOddSplitSixtySevenTwoFiftySevenLineStrip :
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      t ≠ -13 → r ≠ 0 →
      det strip ({ x := -12, y := 5 } : Point) * r +
          det strip
            ({ x := 24 * t * t - 46 * t - 165,
                y := -10 * t * t - 126 * t + 52 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -12, y := 5 } : Point))
            ({ x := 24 * t * t - 46 * t - 165,
                y := -10 * t * t - 126 * t + 52 } : Point))
          (smul r ({ x := -12, y := 5 } : Point)) ∧
        det strip
            (add (smul r ({ x := -12, y := 5 } : Point))
              ({ x := 24 * t * t - 46 * t - 165,
                  y := -10 * t * t - 126 * t + 52 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        26 * t + 3 ≡ 3 [ZMOD 26]) ∧
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      t ≠ 49 → r ≠ 0 →
          det strip ({ x := -5, y := 12 } : Point) * r +
          det strip
            ({ x := 10 * t * t - 466 * t - 1176,
                y := -24 * t * t - 218 * t + 2257 } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -5, y := 12 } : Point))
            ({ x := 10 * t * t - 466 * t - 1176,
                y := -24 * t * t - 218 * t + 2257 } : Point))
          (smul r ({ x := -5, y := 12 } : Point)) ∧
        det strip
            (add (smul r ({ x := -5, y := 12 } : Point))
              ({ x := 10 * t * t - 466 * t - 1176,
                  y := -24 * t * t - 218 * t + 2257 } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        26 * t + 11 ≡ 11 [ZMOD 26]) := by
  constructor
  · intro t r stripResidue stripModulus strip ht hr hcoeff
    exact certificateValid_twoThreeOddSplitSixtySevenTwoFiftySevenResidueThreeLineStrip
      (strip := strip) ht hr hcoeff
  · intro t r stripResidue stripModulus strip ht hr hcoeff
    exact certificateValid_twoThreeOddSplitSixtySevenTwoFiftySevenResidueElevenLineStrip
      (strip := strip) ht hr hcoeff

theorem certificateValid_fourFiveEvenSplitNineteenTwoThirtyNineResidueThirtyOneTwentyThreeLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -9, y := 40 } : Point) * r +
          det strip
            ({ x := 60516 * t * t + 109388 * t + 49392,
                y := -268960 * t * t - 500364 * t - 232706 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -9, y := 40 } : Point))
          ({ x := 60516 * t * t + 109388 * t + 49392,
              y := -268960 * t * t - 500364 * t - 232706 } : Point))
        (smul r ({ x := -9, y := 40 } : Point)) ∧
      det strip
          (add (smul r ({ x := -9, y := 40 } : Point))
            ({ x := 60516 * t * t + 109388 * t + 49392,
                y := -268960 * t * t - 500364 * t - 232706 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      3362 * t + 3123 ≡ 3123 [ZMOD 3362] := by
  let direction : Point := { x := -9, y := 40 }
  let secondStep : Point :=
    { x := 60516 * t * t + 109388 * t + 49392,
      y := -268960 * t * t - 500364 * t - 232706 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨41, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 4 * (41 * t + 36) * (369 * t + 343) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          4 * (41 * t + 36) * (369 * t + 343)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -2 * (328 * t + 307) * (410 * t + 379) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -2 * (328 * t + 307) * (410 * t + 379)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨2 * (137842 * t * t + 256086 * t + 118945), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 3362 * t + 3123 ≡ 3123 [ZMOD 3362] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 3362 * t + 3123)
    (pairedResidue := 3123) (pairedModulus := 3362)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_fourFiveEvenSplitNineteenTwoThirtyNineResidueTwentyTwoLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ -53) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -40, y := 9 } : Point) * r +
          det strip
            ({ x := 40 * t * t - 62 * t - 1404,
                y := -9 * t * t - 476 * t + 53 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -40, y := 9 } : Point))
          ({ x := 40 * t * t - 62 * t - 1404,
              y := -9 * t * t - 476 * t + 53 } : Point))
        (smul r ({ x := -40, y := 9 } : Point)) ∧
      det strip
          (add (smul r ({ x := -40, y := 9 } : Point))
            ({ x := 40 * t * t - 62 * t - 1404,
                y := -9 * t * t - 476 * t + 53 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      41 * t + 22 ≡ 22 [ZMOD 41] := by
  let direction : Point := { x := -40, y := 9 }
  let secondStep : Point :=
    { x := 40 * t * t - 62 * t - 1404,
      y := -9 * t * t - 476 * t + 53 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨41, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 2 * (4 * t - 27) * (5 * t + 26) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          2 * (4 * t - 27) * (5 * t + 26)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -(t + 53) * (9 * t - 1) ≠ 0 := by
          exact mul_ne_zero (by omega) (by omega)
        apply hfactor
        calc
          -(t + 53) * (9 * t - 1)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨41 * t * t + 44 * t + 1405, ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 41 * t + 22 ≡ 22 [ZMOD 41] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 41 * t + 22)
    (pairedResidue := 22) (pairedModulus := 41)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_oneTwoSquareclassFiveThirtyFiveSplitNineFortySevenResidueThreeLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (ht : t ≠ 0) (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -3, y := 4 } : Point) * r +
          det strip
            ({ x := 80250 * t * t + 5350 * t,
                y := -107000 * t * t - 16050 * t - 535 } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -3, y := 4 } : Point))
          ({ x := 80250 * t * t + 5350 * t,
              y := -107000 * t * t - 16050 * t - 535 } : Point))
        (smul r ({ x := -3, y := 4 } : Point)) ∧
      det strip
          (add (smul r ({ x := -3, y := 4 } : Point))
            ({ x := 80250 * t * t + 5350 * t,
                y := -107000 * t * t - 16050 * t - 535 } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      50 * t + 3 ≡ 3 [ZMOD 50] := by
  let direction : Point := { x := -3, y := 4 }
  let secondStep : Point :=
    { x := 80250 * t * t + 5350 * t,
      y := -107000 * t * t - 16050 * t - 535 }
  have hdirection : legalStep direction := by
    constructor
    · constructor <;> norm_num [direction]
    · refine ⟨5, ?_⟩
      norm_num [direction, normSq, sq]
  have hsecondStep : legalStep secondStep := by
    constructor
    · constructor
      · intro hx
        have hfactor : 5350 * t * (15 * t + 1) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) ht) (by omega)
        apply hfactor
        calc
          5350 * t * (15 * t + 1)
              = secondStep.x := by simp [secondStep]; ring
          _ = 0 := hx
      · intro hy
        have hfactor : -535 * (10 * t + 1) * (20 * t + 1) ≠ 0 := by
          exact mul_ne_zero
            (mul_ne_zero (by norm_num) (by omega)) (by omega)
        apply hfactor
        calc
          -535 * (10 * t + 1) * (20 * t + 1)
              = secondStep.y := by simp [secondStep]; ring
          _ = 0 := hy
    · refine ⟨535 * (250 * t * t + 30 * t + 1), ?_⟩
      simp [secondStep, normSq, sq]
      ring
  have hpaired : 50 * t + 3 ≡ 3 [ZMOD 50] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripCertificateValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 50 * t + 3)
    (pairedResidue := 3) (pairedModulus := 50)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hr hdirection hsecondStep hpaired hcoeff

theorem certificateValid_threeFourRootSpineLine {m a b r : Int}
    (hm : m ≠ 0) (ha : a ≠ 0) (hb : b ≠ 0)
    (hab : a * a ≠ b * b) (hr : r ≠ 0) :
    certificateValid
      ({ x := -7 * r + m * (a * a - b * b),
          y := 24 * r + 2 * m * a * b } : Point)
      ({ x := -7 * r, y := 24 * r } : Point) := by
  let target : Point :=
    { x := -7 * r + m * (a * a - b * b),
      y := 24 * r + 2 * m * a * b }
  let midpoint : Point := { x := -7 * r, y := 24 * r }
  have hdiff : a * a - b * b ≠ 0 := sub_ne_zero.mpr hab
  have hstep_x_factor : m * (a * a - b * b) ≠ 0 := mul_ne_zero hm hdiff
  have hstep_y_factor : 2 * m * a * b ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hm) ha) hb
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num) hr
      · exact mul_ne_zero (by norm_num) hr
    · refine ⟨25 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · intro hx
        apply hstep_x_factor
        simpa [target, midpoint, sub] using hx
      · intro hy
        apply hstep_y_factor
        simpa [target, midpoint, sub] using hy
    · refine ⟨m * (a * a + b * b), ?_⟩
      calc
        normSq (sub target midpoint)
            = sq (m * (a * a - b * b)) + sq (2 * m * a * b) := by
              simp [target, midpoint, normSq, sub, sq]
        _ = (m * (a * a + b * b)) * (m * (a * a + b * b)) := by
          simp [sq]
          ring_nf

theorem certificateValid_threeFourRootSpineLineSwap {m a b r : Int}
    (hm : m ≠ 0) (ha : a ≠ 0) (hb : b ≠ 0)
    (hab : a * a ≠ b * b) (hr : r ≠ 0) :
    certificateValid
      ({ x := 24 * r + 2 * m * a * b,
          y := 7 * r - m * (a * a - b * b) } : Point)
      ({ x := 24 * r, y := 7 * r } : Point) := by
  let target : Point :=
    { x := 24 * r + 2 * m * a * b,
      y := 7 * r - m * (a * a - b * b) }
  let midpoint : Point := { x := 24 * r, y := 7 * r }
  have hdiff : a * a - b * b ≠ 0 := sub_ne_zero.mpr hab
  have hstep_x_factor : 2 * m * a * b ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hm) ha) hb
  have hstep_y_factor : m * (a * a - b * b) ≠ 0 := mul_ne_zero hm hdiff
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num) hr
      · exact mul_ne_zero (by norm_num) hr
    · refine ⟨25 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · intro hx
        apply hstep_x_factor
        calc
          2 * m * a * b = (24 * r + 2 * m * a * b) - 24 * r := by ring
          _ = (sub target midpoint).x := by simp [target, midpoint, sub]
          _ = 0 := hx
      · intro hy
        apply hstep_y_factor
        calc
          m * (a * a - b * b) = -((7 * r - m * (a * a - b * b)) - 7 * r) := by ring
          _ = -((sub target midpoint).y) := by simp [target, midpoint, sub]
          _ = 0 := by rw [hy]; ring
    · refine ⟨m * (a * a + b * b), ?_⟩
      calc
        normSq (sub target midpoint)
            = sq (2 * m * a * b) + sq (m * (a * a - b * b)) := by
              simp [target, midpoint, normSq, sub, sq]
        _ = (m * (a * a + b * b)) * (m * (a * a + b * b)) := by
          simp [sq]
          ring_nf

theorem certificateValid_threeFourOddRootSpineLine {m a b r : Int}
    (hm : m ≠ 0) (hdiff : 2 * a * a + 2 * a - 2 * b * b - 2 * b ≠ 0)
    (hr : r ≠ 0) :
    certificateValid
      ({ x := -7 * r + m * (2 * a * a + 2 * a - 2 * b * b - 2 * b),
          y := 24 * r + m * ((2 * a + 1) * (2 * b + 1)) } : Point)
      ({ x := -7 * r, y := 24 * r } : Point) := by
  let delta : Int := 2 * a * a + 2 * a - 2 * b * b - 2 * b
  let paired : Int := (2 * a + 1) * (2 * b + 1)
  let hyp : Int := 2 * a * a + 2 * a + 2 * b * b + 2 * b + 1
  let target : Point :=
    { x := -7 * r + m * delta,
      y := 24 * r + m * paired }
  let midpoint : Point := { x := -7 * r, y := 24 * r }
  have hodd_a : 2 * a + 1 ≠ 0 := by omega
  have hodd_b : 2 * b + 1 ≠ 0 := by omega
  have hpaired : paired ≠ 0 := mul_ne_zero hodd_a hodd_b
  have hstep_x_factor : m * delta ≠ 0 := by
    exact mul_ne_zero hm (by simpa [delta] using hdiff)
  have hstep_y_factor : m * paired ≠ 0 := mul_ne_zero hm hpaired
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num) hr
      · exact mul_ne_zero (by norm_num) hr
    · refine ⟨25 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · intro hx
        apply hstep_x_factor
        calc
          m * delta = (-7 * r + m * delta) - (-7 * r) := by ring
          _ = (sub target midpoint).x := by simp [target, midpoint, sub]
          _ = 0 := hx
      · intro hy
        apply hstep_y_factor
        calc
          m * paired = (24 * r + m * paired) - 24 * r := by ring
          _ = (sub target midpoint).y := by simp [target, midpoint, sub]
          _ = 0 := hy
    · refine ⟨m * hyp, ?_⟩
      calc
        normSq (sub target midpoint) = sq (m * delta) + sq (m * paired) := by
          simp [target, midpoint, normSq, sub, sq]
        _ = (m * hyp) * (m * hyp) := by
          simp [delta, paired, hyp, sq]
          ring_nf

theorem certificateValid_threeFourOddRootSpineLineSwap {m a b r : Int}
    (hm : m ≠ 0) (hdiff : 2 * a * a + 2 * a - 2 * b * b - 2 * b ≠ 0)
    (hr : r ≠ 0) :
    certificateValid
      ({ x := 24 * r + m * ((2 * a + 1) * (2 * b + 1)),
          y := 7 * r - m * (2 * a * a + 2 * a - 2 * b * b - 2 * b) } : Point)
      ({ x := 24 * r, y := 7 * r } : Point) := by
  let delta : Int := 2 * a * a + 2 * a - 2 * b * b - 2 * b
  let paired : Int := (2 * a + 1) * (2 * b + 1)
  let hyp : Int := 2 * a * a + 2 * a + 2 * b * b + 2 * b + 1
  let target : Point :=
    { x := 24 * r + m * paired,
      y := 7 * r - m * delta }
  let midpoint : Point := { x := 24 * r, y := 7 * r }
  have hodd_a : 2 * a + 1 ≠ 0 := by omega
  have hodd_b : 2 * b + 1 ≠ 0 := by omega
  have hpaired : paired ≠ 0 := mul_ne_zero hodd_a hodd_b
  have hstep_x_factor : m * paired ≠ 0 := mul_ne_zero hm hpaired
  have hstep_y_factor : m * delta ≠ 0 := by
    exact mul_ne_zero hm (by simpa [delta] using hdiff)
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num) hr
      · exact mul_ne_zero (by norm_num) hr
    · refine ⟨25 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · intro hx
        apply hstep_x_factor
        calc
          m * paired = (24 * r + m * paired) - 24 * r := by ring
          _ = (sub target midpoint).x := by simp [target, midpoint, sub]
          _ = 0 := hx
      · intro hy
        apply hstep_y_factor
        calc
          m * delta = -((7 * r - m * delta) - 7 * r) := by ring
          _ = -((sub target midpoint).y) := by simp [target, midpoint, sub]
          _ = 0 := by rw [hy]; ring
    · refine ⟨m * hyp, ?_⟩
      calc
        normSq (sub target midpoint) = sq (m * paired) + sq (m * delta) := by
          simp [target, midpoint, normSq, sub, sq]
        _ = (m * hyp) * (m * hyp) := by
          simp [delta, paired, hyp, sq]
          ring_nf

theorem certificateValid_fourFiveRootSpineLine {m a b r : Int}
    (hm : m ≠ 0) (ha : a ≠ 0) (hb : b ≠ 0)
    (hab : a * a ≠ b * b) (hr : r ≠ 0) :
    certificateValid
      ({ x := -9 * r + m * (a * a - b * b),
          y := 40 * r + 2 * m * a * b } : Point)
      ({ x := -9 * r, y := 40 * r } : Point) := by
  let target : Point :=
    { x := -9 * r + m * (a * a - b * b),
      y := 40 * r + 2 * m * a * b }
  let midpoint : Point := { x := -9 * r, y := 40 * r }
  have hdiff : a * a - b * b ≠ 0 := sub_ne_zero.mpr hab
  have hstep_x_factor : m * (a * a - b * b) ≠ 0 := mul_ne_zero hm hdiff
  have hstep_y_factor : 2 * m * a * b ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hm) ha) hb
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num) hr
      · exact mul_ne_zero (by norm_num) hr
    · refine ⟨41 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · intro hx
        apply hstep_x_factor
        simpa [target, midpoint, sub] using hx
      · intro hy
        apply hstep_y_factor
        simpa [target, midpoint, sub] using hy
    · refine ⟨m * (a * a + b * b), ?_⟩
      calc
        normSq (sub target midpoint)
            = sq (m * (a * a - b * b)) + sq (2 * m * a * b) := by
              simp [target, midpoint, normSq, sub, sq]
        _ = (m * (a * a + b * b)) * (m * (a * a + b * b)) := by
          simp [sq]
          ring_nf

theorem certificateValid_fourFiveRootSpineLineSwap {m a b r : Int}
    (hm : m ≠ 0) (ha : a ≠ 0) (hb : b ≠ 0)
    (hab : a * a ≠ b * b) (hr : r ≠ 0) :
    certificateValid
      ({ x := -40 * r + 2 * m * a * b,
          y := 9 * r - m * (a * a - b * b) } : Point)
      ({ x := -40 * r, y := 9 * r } : Point) := by
  let target : Point :=
    { x := -40 * r + 2 * m * a * b,
      y := 9 * r - m * (a * a - b * b) }
  let midpoint : Point := { x := -40 * r, y := 9 * r }
  have hdiff : a * a - b * b ≠ 0 := sub_ne_zero.mpr hab
  have hstep_x_factor : 2 * m * a * b ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hm) ha) hb
  have hstep_y_factor : m * (a * a - b * b) ≠ 0 := mul_ne_zero hm hdiff
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num) hr
      · exact mul_ne_zero (by norm_num) hr
    · refine ⟨41 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · intro hx
        apply hstep_x_factor
        simpa [target, midpoint, sub] using hx
      · intro hy
        apply hstep_y_factor
        calc
          m * (a * a - b * b) = -((9 * r - m * (a * a - b * b)) - 9 * r) := by ring
          _ = -((sub target midpoint).y) := by simp [target, midpoint, sub]
          _ = 0 := by rw [hy]; ring
    · refine ⟨m * (a * a + b * b), ?_⟩
      calc
        normSq (sub target midpoint)
            = sq (2 * m * a * b) + sq (m * (a * a - b * b)) := by
              simp [target, midpoint, normSq, sub, sq]
        _ = (m * (a * a + b * b)) * (m * (a * a + b * b)) := by
          simp [sq]
          ring_nf

theorem certificateValid_threeEightOddRootSpineLine {m a b r : Int}
    (hm : m ≠ 0) (hdiff : 2 * a * a + 2 * a - 2 * b * b - 2 * b ≠ 0)
    (hr : r ≠ 0) :
    certificateValid
      ({ x := -55 * r + m * (2 * a * a + 2 * a - 2 * b * b - 2 * b),
          y := 48 * r + m * ((2 * a + 1) * (2 * b + 1)) } : Point)
      ({ x := -55 * r, y := 48 * r } : Point) := by
  let delta : Int := 2 * a * a + 2 * a - 2 * b * b - 2 * b
  let paired : Int := (2 * a + 1) * (2 * b + 1)
  let hyp : Int := 2 * a * a + 2 * a + 2 * b * b + 2 * b + 1
  let target : Point :=
    { x := -55 * r + m * delta,
      y := 48 * r + m * paired }
  let midpoint : Point := { x := -55 * r, y := 48 * r }
  have hodd_a : 2 * a + 1 ≠ 0 := by omega
  have hodd_b : 2 * b + 1 ≠ 0 := by omega
  have hpaired : paired ≠ 0 := mul_ne_zero hodd_a hodd_b
  have hstep_x_factor : m * delta ≠ 0 := by
    exact mul_ne_zero hm (by simpa [delta] using hdiff)
  have hstep_y_factor : m * paired ≠ 0 := mul_ne_zero hm hpaired
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num) hr
      · exact mul_ne_zero (by norm_num) hr
    · refine ⟨73 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · intro hx
        apply hstep_x_factor
        simpa [target, midpoint, sub] using hx
      · intro hy
        apply hstep_y_factor
        calc
          m * paired = (48 * r + m * paired) - 48 * r := by ring
          _ = (sub target midpoint).y := by simp [target, midpoint, sub]
          _ = 0 := hy
    · refine ⟨m * hyp, ?_⟩
      calc
        normSq (sub target midpoint) = sq (m * delta) + sq (m * paired) := by
          simp [target, midpoint, normSq, sub, sq]
        _ = (m * hyp) * (m * hyp) := by
          simp [delta, paired, hyp, sq]
          ring_nf

theorem certificateValid_threeEightOddRootSpineLineSwap {m a b r : Int}
    (hm : m ≠ 0) (hdiff : 2 * a * a + 2 * a - 2 * b * b - 2 * b ≠ 0)
    (hr : r ≠ 0) :
    certificateValid
      ({ x := -48 * r + m * ((2 * a + 1) * (2 * b + 1)),
          y := 55 * r - m * (2 * a * a + 2 * a - 2 * b * b - 2 * b) } : Point)
      ({ x := -48 * r, y := 55 * r } : Point) := by
  let delta : Int := 2 * a * a + 2 * a - 2 * b * b - 2 * b
  let paired : Int := (2 * a + 1) * (2 * b + 1)
  let hyp : Int := 2 * a * a + 2 * a + 2 * b * b + 2 * b + 1
  let target : Point :=
    { x := -48 * r + m * paired,
      y := 55 * r - m * delta }
  let midpoint : Point := { x := -48 * r, y := 55 * r }
  have hodd_a : 2 * a + 1 ≠ 0 := by omega
  have hodd_b : 2 * b + 1 ≠ 0 := by omega
  have hpaired : paired ≠ 0 := mul_ne_zero hodd_a hodd_b
  have hstep_x_factor : m * paired ≠ 0 := mul_ne_zero hm hpaired
  have hstep_y_factor : m * delta ≠ 0 := by
    exact mul_ne_zero hm (by simpa [delta] using hdiff)
  constructor
  · constructor
    · constructor
      · exact mul_ne_zero (by norm_num) hr
      · exact mul_ne_zero (by norm_num) hr
    · refine ⟨73 * r, ?_⟩
      simp [normSq, sq]
      ring
  · constructor
    · constructor
      · intro hx
        apply hstep_x_factor
        calc
          m * paired = (-48 * r + m * paired) - (-48 * r) := by ring
          _ = (sub target midpoint).x := by simp [target, midpoint, sub]
          _ = 0 := hx
      · intro hy
        apply hstep_y_factor
        calc
          m * delta = -((55 * r - m * delta) - 55 * r) := by ring
          _ = -((sub target midpoint).y) := by simp [target, midpoint, sub]
          _ = 0 := by rw [hy]; ring
    · refine ⟨m * hyp, ?_⟩
      calc
        normSq (sub target midpoint) = sq (m * paired) + sq (m * delta) := by
          simp [target, midpoint, normSq, sub, sq]
        _ = (m * hyp) * (m * hyp) := by
          simp [delta, paired, hyp, sq]
          ring_nf

theorem certificateValid_threeEightOddSplitNineteenFifteenThirtyOneResidueOneTwentySevenLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -55, y := 48 } : Point) * r +
          det strip
            ({ x := 2 * (8 * t - 25) * (8 * t - 25) + 2 * (8 * t - 25) -
                  2 * (-3 * t - 87) * (-3 * t - 87) - 2 * (-3 * t - 87),
                y := (16 * t - 49) * (-6 * t - 173) } : Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -55, y := 48 } : Point))
          ({ x := 2 * (8 * t - 25) * (8 * t - 25) + 2 * (8 * t - 25) -
                2 * (-3 * t - 87) * (-3 * t - 87) - 2 * (-3 * t - 87),
              y := (16 * t - 49) * (-6 * t - 173) } : Point))
        (smul r ({ x := -55, y := 48 } : Point)) ∧
      det strip
          (add (smul r ({ x := -55, y := 48 } : Point))
            ({ x := 2 * (8 * t - 25) * (8 * t - 25) + 2 * (8 * t - 25) -
                  2 * (-3 * t - 87) * (-3 * t - 87) - 2 * (-3 * t - 87),
                y := (16 * t - 49) * (-6 * t - 173) } : Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      146 * t + 127 ≡ 127 [ZMOD 146] := by
  let direction : Point := { x := -55, y := 48 }
  let secondStep : Point :=
    { x := 2 * (8 * t - 25) * (8 * t - 25) + 2 * (8 * t - 25) -
          2 * (-3 * t - 87) * (-3 * t - 87) - 2 * (-3 * t - 87),
      y := (16 * t - 49) * (-6 * t - 173) }
  have hdelta :
      2 * (8 * t - 25) * (8 * t - 25) + 2 * (8 * t - 25) -
          2 * (-3 * t - 87) * (-3 * t - 87) - 2 * (-3 * t - 87) ≠ 0 := by
    have hprod : 2 * (5 * t - 111) * (11 * t + 62) ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (by norm_num) (by omega)) (by omega)
    intro hzero
    apply hprod
    calc
      2 * (5 * t - 111) * (11 * t + 62)
          =
            2 * (8 * t - 25) * (8 * t - 25) + 2 * (8 * t - 25) -
              2 * (-3 * t - 87) * (-3 * t - 87) - 2 * (-3 * t - 87) := by
            ring
      _ = 0 := hzero
  have hline :
      certificateValid (add (smul r direction) secondStep) (smul r direction) := by
    have hraw :=
      certificateValid_threeEightOddRootSpineLine
        (m := 1) (a := 8 * t - 25) (b := -3 * t - 87) (r := r)
        (by norm_num) hdelta hr
    convert hraw using 1
    · ext <;> simp [direction, secondStep, add, smul] <;> ring
    · ext <;> simp [direction, smul] <;> ring
  have hpaired : 146 * t + 127 ≡ 127 [ZMOD 146] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripRowValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 146 * t + 127)
    (pairedResidue := 127) (pairedModulus := 146)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hline hpaired hcoeff

theorem certificateValid_threeEightOddSplitNineteenFifteenThirtyOneResidueSeventyFiveLineStrip
    {t r stripResidue stripModulus : Int} {strip : Point}
    (hr : r ≠ 0)
    (hcoeff :
      det strip ({ x := -48, y := 55 } : Point) * r +
          det strip
            ({ x := (-16 * t - 9) * (-6 * t - 1),
                y := -(2 * (-8 * t - 5) * (-8 * t - 5) + 2 * (-8 * t - 5) -
                  2 * (-3 * t - 1) * (-3 * t - 1) - 2 * (-3 * t - 1)) } :
              Point) ≡
        stripResidue [ZMOD stripModulus]) :
    certificateValid
        (add (smul r ({ x := -48, y := 55 } : Point))
          ({ x := (-16 * t - 9) * (-6 * t - 1),
              y := -(2 * (-8 * t - 5) * (-8 * t - 5) + 2 * (-8 * t - 5) -
                2 * (-3 * t - 1) * (-3 * t - 1) - 2 * (-3 * t - 1)) } :
            Point))
        (smul r ({ x := -48, y := 55 } : Point)) ∧
      det strip
          (add (smul r ({ x := -48, y := 55 } : Point))
            ({ x := (-16 * t - 9) * (-6 * t - 1),
                y := -(2 * (-8 * t - 5) * (-8 * t - 5) + 2 * (-8 * t - 5) -
                  2 * (-3 * t - 1) * (-3 * t - 1) - 2 * (-3 * t - 1)) } :
              Point)) ≡
        stripResidue [ZMOD stripModulus] ∧
      146 * t + 75 ≡ 75 [ZMOD 146] := by
  let direction : Point := { x := -48, y := 55 }
  let secondStep : Point :=
    { x := (-16 * t - 9) * (-6 * t - 1),
      y := -(2 * (-8 * t - 5) * (-8 * t - 5) + 2 * (-8 * t - 5) -
        2 * (-3 * t - 1) * (-3 * t - 1) - 2 * (-3 * t - 1)) }
  have hdelta :
      2 * (-8 * t - 5) * (-8 * t - 5) + 2 * (-8 * t - 5) -
          2 * (-3 * t - 1) * (-3 * t - 1) - 2 * (-3 * t - 1) ≠ 0 := by
    have hprod : 2 * (5 * t + 4) * (11 * t + 5) ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (by norm_num) (by omega)) (by omega)
    intro hzero
    apply hprod
    calc
      2 * (5 * t + 4) * (11 * t + 5)
          =
            2 * (-8 * t - 5) * (-8 * t - 5) + 2 * (-8 * t - 5) -
              2 * (-3 * t - 1) * (-3 * t - 1) - 2 * (-3 * t - 1) := by
            ring
      _ = 0 := hzero
  have hline :
      certificateValid (add (smul r direction) secondStep) (smul r direction) := by
    have hraw :=
      certificateValid_threeEightOddRootSpineLineSwap
        (m := 1) (a := -8 * t - 5) (b := -3 * t - 1) (r := r)
        (by norm_num) hdelta hr
    convert hraw using 1
    · ext <;> simp [direction, secondStep, add, smul] <;> ring
    · ext <;> simp [direction, smul] <;> ring
  have hpaired : 146 * t + 75 ≡ 75 [ZMOD 146] := by
    apply Int.modEq_iff_dvd.mpr
    refine ⟨-t, ?_⟩
    ring
  exact lineStripRowValid (strip := strip) (direction := direction)
    (secondStep := secondStep) (r := r) (paired := 146 * t + 75)
    (pairedResidue := 75) (pairedModulus := 146)
    (stripResidue := stripResidue) (stripModulus := stripModulus)
    hline hpaired hcoeff

theorem certificateValid_threeEightOddSplitNineteenFifteenThirtyOneLineStrip :
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -55, y := 48 } : Point) * r +
          det strip
            ({ x := 2 * (8 * t - 25) * (8 * t - 25) + 2 * (8 * t - 25) -
                  2 * (-3 * t - 87) * (-3 * t - 87) - 2 * (-3 * t - 87),
                y := (16 * t - 49) * (-6 * t - 173) } : Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -55, y := 48 } : Point))
            ({ x := 2 * (8 * t - 25) * (8 * t - 25) + 2 * (8 * t - 25) -
                  2 * (-3 * t - 87) * (-3 * t - 87) - 2 * (-3 * t - 87),
                y := (16 * t - 49) * (-6 * t - 173) } : Point))
          (smul r ({ x := -55, y := 48 } : Point)) ∧
        det strip
            (add (smul r ({ x := -55, y := 48 } : Point))
              ({ x := 2 * (8 * t - 25) * (8 * t - 25) + 2 * (8 * t - 25) -
                    2 * (-3 * t - 87) * (-3 * t - 87) - 2 * (-3 * t - 87),
                  y := (16 * t - 49) * (-6 * t - 173) } : Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        146 * t + 127 ≡ 127 [ZMOD 146]) ∧
    (∀ {t r stripResidue stripModulus : Int} {strip : Point},
      r ≠ 0 →
      det strip ({ x := -48, y := 55 } : Point) * r +
          det strip
            ({ x := (-16 * t - 9) * (-6 * t - 1),
                y := -(2 * (-8 * t - 5) * (-8 * t - 5) + 2 * (-8 * t - 5) -
                  2 * (-3 * t - 1) * (-3 * t - 1) - 2 * (-3 * t - 1)) } :
              Point) ≡
        stripResidue [ZMOD stripModulus] →
      certificateValid
          (add (smul r ({ x := -48, y := 55 } : Point))
            ({ x := (-16 * t - 9) * (-6 * t - 1),
                y := -(2 * (-8 * t - 5) * (-8 * t - 5) + 2 * (-8 * t - 5) -
                  2 * (-3 * t - 1) * (-3 * t - 1) - 2 * (-3 * t - 1)) } :
              Point))
          (smul r ({ x := -48, y := 55 } : Point)) ∧
        det strip
            (add (smul r ({ x := -48, y := 55 } : Point))
              ({ x := (-16 * t - 9) * (-6 * t - 1),
                  y := -(2 * (-8 * t - 5) * (-8 * t - 5) + 2 * (-8 * t - 5) -
                    2 * (-3 * t - 1) * (-3 * t - 1) - 2 * (-3 * t - 1)) } :
                Point)) ≡
          stripResidue [ZMOD stripModulus] ∧
        146 * t + 75 ≡ 75 [ZMOD 146]) := by
  constructor
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_threeEightOddSplitNineteenFifteenThirtyOneResidueOneTwentySevenLineStrip
      (strip := strip) hr hcoeff
  · intro t r stripResidue stripModulus strip hr hcoeff
    exact certificateValid_threeEightOddSplitNineteenFifteenThirtyOneResidueSeventyFiveLineStrip
      (strip := strip) hr hcoeff

theorem certificateValid_pinnedGlobalRootChoiceAlternateLineRow01 :
    certificateValid
      ({ x := 10375, y := -11282 } : Point)
      ({ x := -480, y := 550 } : Point) := by
  simpa using
    (certificateValid_threeEightOddRootSpineLineSwap
      (m := 1) (a := 83) (b := 32) (r := 10)
      (by norm_num) (by norm_num) (by norm_num))

theorem certificateValid_pinnedGlobalRootChoiceAlternateLineRow02 :
    certificateValid
      ({ x := -297590, y := 313261 } : Point)
      ({ x := -20, y := 21 } : Point) := by
  simpa using
    (certificateValid_twoFiveRootSpineLine
      (m := 5) (a := -109) (b := 273) (r := 1)
      (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num))

theorem certificateValid_pinnedGlobalRootChoiceAlternateLineRow03 :
    certificateValid
      ({ x := -1538, y := -3185 } : Point)
      ({ x := -56, y := -105 } : Point) := by
  simpa using
    (certificateValid_oneFourEvenRootSpineLine
      (m := 1) (a := -13) (b := -57) (r := 7)
      (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num))

theorem certificateValid_pinnedGlobalRootChoiceAlternateLineRow04 :
    certificateValid
      ({ x := 312988, y := -297330 } : Point)
      ({ x := -252, y := 240 } : Point) := by
  simpa using
    (certificateValid_twoFiveRootSpineLineSwap
      (m := 5) (a := -273) (b := 109) (r := 12)
      (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num))

theorem certificateValid_pinnedGlobalRootChoiceAlternateLineRow05 :
    certificateValid
      ({ x := -11997, y := 10999 } : Point)
      ({ x := -165, y := 144 } : Point) := by
  simpa using
    (certificateValid_threeEightOddRootSpineLine
      (m := 1) (a := -33) (b := -84) (r := 3)
      (by norm_num) (by norm_num) (by norm_num))

theorem certificateValid_pinnedGlobalRootChoiceAlternateLineRow06 :
    certificateValid
      ({ x := -3185, y := -1538 } : Point)
      ({ x := -105, y := -56 } : Point) := by
  simpa using
    (certificateValid_oneFourEvenRootSpineLineSwap
      (m := 1) (a := -13) (b := 57) (r := 7)
      (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num))

theorem certificateValid_pinnedGlobalRootChoiceAlternateLineRow07 :
    certificateValid
      ({ x := 2233, y := 1166 } : Point)
      ({ x := -24, y := -10 } : Point) := by
  simpa using
    (certificateValid_twoThreeOddGeneralRootSpineLine
      (m := 1) (a := -31) (b := 18) (r := 2)
      (by norm_num) (by norm_num) (by norm_num))

theorem certificateValid_pinnedGlobalRootChoiceAlternateLineRow08 :
    certificateValid
      ({ x := 1166, y := 2233 } : Point)
      ({ x := -10, y := -24 } : Point) := by
  simpa using
    (certificateValid_twoThreeOddGeneralRootSpineLineSwap
      (m := 1) (a := -31) (b := -19) (r := 2)
      (by norm_num) (by norm_num) (by norm_num))

theorem certificateValid_pinnedGlobalRootChoiceAlternateLineRow09 :
    certificateValid
      ({ x := -2582, y := 808 } : Point)
      ({ x := -1280, y := 288 } : Point) := by
  simpa using
    (certificateValid_fourFiveRootSpineLineSwap
      (m := 1) (a := -21) (b := 31) (r := 32)
      (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num))

theorem certificateValid_pinnedGlobalRootChoiceAlternateLineRow10 :
    certificateValid
      ({ x := 151, y := 338 } : Point)
      ({ x := -369, y := 1640 } : Point) := by
  simpa using
    (certificateValid_fourFiveRootSpineLine
      (m := 1) (a := -31) (b := 21) (r := 41)
      (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num))

theorem pinnedGlobalRootChoiceAlternateLineRow01_strip :
    det ({ x := -12, y := -5 } : Point) ({ x := 10375, y := -11282 } : Point) ≡
      7 [ZMOD 13] := by
  norm_num [det]

theorem pinnedGlobalRootChoiceAlternateLineRow02_strip :
    det ({ x := 5, y := -12 } : Point) ({ x := -297590, y := 313261 } : Point) ≡
      7 [ZMOD 13] := by
  norm_num [det]

theorem pinnedGlobalRootChoiceAlternateLineRow03_strip :
    det ({ x := 12, y := 5 } : Point) ({ x := -1538, y := -3185 } : Point) ≡
      7 [ZMOD 13] := by
  norm_num [det]

theorem pinnedGlobalRootChoiceAlternateLineRow04_strip :
    det ({ x := 12, y := 5 } : Point) ({ x := 312988, y := -297330 } : Point) ≡
      7 [ZMOD 13] := by
  norm_num [det]

theorem pinnedGlobalRootChoiceAlternateLineRow05_strip :
    det ({ x := -12, y := 5 } : Point) ({ x := 312988, y := -297330 } : Point) ≡
      6 [ZMOD 13] := by
  norm_num [det]

theorem pinnedGlobalRootChoiceAlternateLineRow06_strip :
    det ({ x := -5, y := -12 } : Point) ({ x := -11997, y := 10999 } : Point) ≡
      6 [ZMOD 13] := by
  norm_num [det]

theorem pinnedGlobalRootChoiceAlternateLineRow07_strip :
    det ({ x := 5, y := 12 } : Point) ({ x := -3185, y := -1538 } : Point) ≡
      6 [ZMOD 13] := by
  norm_num [det]

theorem pinnedGlobalRootChoiceAlternateLineRow08_strip :
    det ({ x := 5, y := 12 } : Point) ({ x := -297590, y := 313261 } : Point) ≡
      6 [ZMOD 13] := by
  norm_num [det]

theorem pinnedGlobalRootChoiceAlternateLineRow09_strip :
    det ({ x := 9, y := -40 } : Point) ({ x := 2233, y := 1166 } : Point) ≡
      20 [ZMOD 82] := by
  norm_num [det]

theorem pinnedGlobalRootChoiceAlternateLineRow10_strip :
    det ({ x := 40, y := -9 } : Point) ({ x := 1166, y := 2233 } : Point) ≡
      20 [ZMOD 82] := by
  norm_num [det]

theorem pinnedGlobalRootChoiceAlternateLineRow11_strip :
    det ({ x := -48, y := 55 } : Point) ({ x := -4055, y := -2002 } : Point) ≡
      38 [ZMOD 73] := by
  norm_num [det]

theorem pinnedGlobalRootChoiceAlternateLineRow12_strip :
    det ({ x := 55, y := 48 } : Point) ({ x := -2582, y := 808 } : Point) ≡
      38 [ZMOD 73] := by
  norm_num [det]

theorem pinnedGlobalRootChoiceAlternateLineRow13_strip :
    det ({ x := -55, y := 48 } : Point) ({ x := -2002, y := -4055 } : Point) ≡
      38 [ZMOD 73] := by
  norm_num [det]

theorem pinnedGlobalRootChoiceAlternateLineRow14_strip :
    det ({ x := -48, y := -55 } : Point) ({ x := 151, y := 338 } : Point) ≡
      38 [ZMOD 73] := by
  norm_num [det]

theorem pinnedGlobalRootChoiceAlternateLineRow01_valid :
    certificateValid ({ x := 10375, y := -11282 } : Point)
        ({ x := -480, y := 550 } : Point) ∧
      det ({ x := -12, y := -5 } : Point) ({ x := 10375, y := -11282 } : Point) ≡
        7 [ZMOD 13] := by
  exact ⟨certificateValid_pinnedGlobalRootChoiceAlternateLineRow01,
    pinnedGlobalRootChoiceAlternateLineRow01_strip⟩

theorem pinnedGlobalRootChoiceAlternateLineRow02_valid :
    certificateValid ({ x := -297590, y := 313261 } : Point)
        ({ x := -20, y := 21 } : Point) ∧
      det ({ x := 5, y := -12 } : Point) ({ x := -297590, y := 313261 } : Point) ≡
        7 [ZMOD 13] := by
  exact ⟨certificateValid_pinnedGlobalRootChoiceAlternateLineRow02,
    pinnedGlobalRootChoiceAlternateLineRow02_strip⟩

theorem pinnedGlobalRootChoiceAlternateLineRow03_valid :
    certificateValid ({ x := -1538, y := -3185 } : Point)
        ({ x := -56, y := -105 } : Point) ∧
      det ({ x := 12, y := 5 } : Point) ({ x := -1538, y := -3185 } : Point) ≡
        7 [ZMOD 13] := by
  exact ⟨certificateValid_pinnedGlobalRootChoiceAlternateLineRow03,
    pinnedGlobalRootChoiceAlternateLineRow03_strip⟩

theorem pinnedGlobalRootChoiceAlternateLineRow04_valid :
    certificateValid ({ x := 312988, y := -297330 } : Point)
        ({ x := -252, y := 240 } : Point) ∧
      det ({ x := 12, y := 5 } : Point) ({ x := 312988, y := -297330 } : Point) ≡
        7 [ZMOD 13] := by
  exact ⟨certificateValid_pinnedGlobalRootChoiceAlternateLineRow04,
    pinnedGlobalRootChoiceAlternateLineRow04_strip⟩

theorem pinnedGlobalRootChoiceAlternateLineRow05_valid :
    certificateValid ({ x := 312988, y := -297330 } : Point)
        ({ x := -252, y := 240 } : Point) ∧
      det ({ x := -12, y := 5 } : Point) ({ x := 312988, y := -297330 } : Point) ≡
        6 [ZMOD 13] := by
  exact ⟨certificateValid_pinnedGlobalRootChoiceAlternateLineRow04,
    pinnedGlobalRootChoiceAlternateLineRow05_strip⟩

theorem pinnedGlobalRootChoiceAlternateLineRow06_valid :
    certificateValid ({ x := -11997, y := 10999 } : Point)
        ({ x := -165, y := 144 } : Point) ∧
      det ({ x := -5, y := -12 } : Point) ({ x := -11997, y := 10999 } : Point) ≡
        6 [ZMOD 13] := by
  exact ⟨certificateValid_pinnedGlobalRootChoiceAlternateLineRow05,
    pinnedGlobalRootChoiceAlternateLineRow06_strip⟩

theorem pinnedGlobalRootChoiceAlternateLineRow07_valid :
    certificateValid ({ x := -3185, y := -1538 } : Point)
        ({ x := -105, y := -56 } : Point) ∧
      det ({ x := 5, y := 12 } : Point) ({ x := -3185, y := -1538 } : Point) ≡
        6 [ZMOD 13] := by
  exact ⟨certificateValid_pinnedGlobalRootChoiceAlternateLineRow06,
    pinnedGlobalRootChoiceAlternateLineRow07_strip⟩

theorem pinnedGlobalRootChoiceAlternateLineRow08_valid :
    certificateValid ({ x := -297590, y := 313261 } : Point)
        ({ x := -20, y := 21 } : Point) ∧
      det ({ x := 5, y := 12 } : Point) ({ x := -297590, y := 313261 } : Point) ≡
        6 [ZMOD 13] := by
  exact ⟨certificateValid_pinnedGlobalRootChoiceAlternateLineRow02,
    pinnedGlobalRootChoiceAlternateLineRow08_strip⟩

theorem pinnedGlobalRootChoiceAlternateLineRow09_valid :
    certificateValid ({ x := 2233, y := 1166 } : Point)
        ({ x := -24, y := -10 } : Point) ∧
      det ({ x := 9, y := -40 } : Point) ({ x := 2233, y := 1166 } : Point) ≡
        20 [ZMOD 82] := by
  exact ⟨certificateValid_pinnedGlobalRootChoiceAlternateLineRow07,
    pinnedGlobalRootChoiceAlternateLineRow09_strip⟩

theorem pinnedGlobalRootChoiceAlternateLineRow10_valid :
    certificateValid ({ x := 1166, y := 2233 } : Point)
        ({ x := -10, y := -24 } : Point) ∧
      det ({ x := 40, y := -9 } : Point) ({ x := 1166, y := 2233 } : Point) ≡
        20 [ZMOD 82] := by
  exact ⟨certificateValid_pinnedGlobalRootChoiceAlternateLineRow08,
    pinnedGlobalRootChoiceAlternateLineRow10_strip⟩

theorem pinnedGlobalRootChoiceAlternateLineRow11_valid :
    certificateValid ({ x := -4055, y := -2002 } : Point)
        ({ x := -975, y := -520 } : Point) ∧
      det ({ x := -48, y := 55 } : Point) ({ x := -4055, y := -2002 } : Point) ≡
        38 [ZMOD 73] := by
  constructor
  · simpa using
      (certificateValid_oneFourEvenRootSpineLineSwap
        (m := 1) (a := -13) (b := 57) (r := 65)
        (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num))
  · exact pinnedGlobalRootChoiceAlternateLineRow11_strip

theorem pinnedGlobalRootChoiceAlternateLineRow12_valid :
    certificateValid ({ x := -2582, y := 808 } : Point)
        ({ x := -1280, y := 288 } : Point) ∧
      det ({ x := 55, y := 48 } : Point) ({ x := -2582, y := 808 } : Point) ≡
        38 [ZMOD 73] := by
  exact ⟨certificateValid_pinnedGlobalRootChoiceAlternateLineRow09,
    pinnedGlobalRootChoiceAlternateLineRow12_strip⟩

theorem pinnedGlobalRootChoiceAlternateLineRow13_valid :
    certificateValid ({ x := -2002, y := -4055 } : Point)
        ({ x := -520, y := -975 } : Point) ∧
      det ({ x := -55, y := 48 } : Point) ({ x := -2002, y := -4055 } : Point) ≡
        38 [ZMOD 73] := by
  constructor
  · simpa using
      (certificateValid_oneFourEvenRootSpineLine
        (m := 1) (a := -13) (b := -57) (r := 65)
        (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num))
  · exact pinnedGlobalRootChoiceAlternateLineRow13_strip

theorem pinnedGlobalRootChoiceAlternateLineRow14_valid :
    certificateValid ({ x := 151, y := 338 } : Point)
        ({ x := -369, y := 1640 } : Point) ∧
      det ({ x := -48, y := -55 } : Point) ({ x := 151, y := 338 } : Point) ≡
        38 [ZMOD 73] := by
  exact ⟨certificateValid_pinnedGlobalRootChoiceAlternateLineRow10,
    pinnedGlobalRootChoiceAlternateLineRow14_strip⟩

theorem pinnedGlobalRootChoiceAlternateLineRows_valid :
    (certificateValid ({ x := 10375, y := -11282 } : Point)
        ({ x := -480, y := 550 } : Point) ∧
      det ({ x := -12, y := -5 } : Point) ({ x := 10375, y := -11282 } : Point) ≡
        7 [ZMOD 13]) ∧
      (certificateValid ({ x := -297590, y := 313261 } : Point)
          ({ x := -20, y := 21 } : Point) ∧
        det ({ x := 5, y := -12 } : Point) ({ x := -297590, y := 313261 } : Point) ≡
          7 [ZMOD 13]) ∧
      (certificateValid ({ x := -1538, y := -3185 } : Point)
          ({ x := -56, y := -105 } : Point) ∧
        det ({ x := 12, y := 5 } : Point) ({ x := -1538, y := -3185 } : Point) ≡
          7 [ZMOD 13]) ∧
      (certificateValid ({ x := 312988, y := -297330 } : Point)
          ({ x := -252, y := 240 } : Point) ∧
        det ({ x := 12, y := 5 } : Point) ({ x := 312988, y := -297330 } : Point) ≡
          7 [ZMOD 13]) ∧
      (certificateValid ({ x := 312988, y := -297330 } : Point)
          ({ x := -252, y := 240 } : Point) ∧
        det ({ x := -12, y := 5 } : Point) ({ x := 312988, y := -297330 } : Point) ≡
          6 [ZMOD 13]) ∧
      (certificateValid ({ x := -11997, y := 10999 } : Point)
          ({ x := -165, y := 144 } : Point) ∧
        det ({ x := -5, y := -12 } : Point) ({ x := -11997, y := 10999 } : Point) ≡
          6 [ZMOD 13]) ∧
      (certificateValid ({ x := -3185, y := -1538 } : Point)
          ({ x := -105, y := -56 } : Point) ∧
        det ({ x := 5, y := 12 } : Point) ({ x := -3185, y := -1538 } : Point) ≡
          6 [ZMOD 13]) ∧
      (certificateValid ({ x := -297590, y := 313261 } : Point)
          ({ x := -20, y := 21 } : Point) ∧
        det ({ x := 5, y := 12 } : Point) ({ x := -297590, y := 313261 } : Point) ≡
          6 [ZMOD 13]) ∧
      (certificateValid ({ x := 2233, y := 1166 } : Point)
          ({ x := -24, y := -10 } : Point) ∧
        det ({ x := 9, y := -40 } : Point) ({ x := 2233, y := 1166 } : Point) ≡
          20 [ZMOD 82]) ∧
      (certificateValid ({ x := 1166, y := 2233 } : Point)
          ({ x := -10, y := -24 } : Point) ∧
        det ({ x := 40, y := -9 } : Point) ({ x := 1166, y := 2233 } : Point) ≡
          20 [ZMOD 82]) ∧
      (certificateValid ({ x := -4055, y := -2002 } : Point)
          ({ x := -975, y := -520 } : Point) ∧
        det ({ x := -48, y := 55 } : Point) ({ x := -4055, y := -2002 } : Point) ≡
          38 [ZMOD 73]) ∧
      (certificateValid ({ x := -2582, y := 808 } : Point)
          ({ x := -1280, y := 288 } : Point) ∧
        det ({ x := 55, y := 48 } : Point) ({ x := -2582, y := 808 } : Point) ≡
          38 [ZMOD 73]) ∧
      (certificateValid ({ x := -2002, y := -4055 } : Point)
          ({ x := -520, y := -975 } : Point) ∧
        det ({ x := -55, y := 48 } : Point) ({ x := -2002, y := -4055 } : Point) ≡
          38 [ZMOD 73]) ∧
      (certificateValid ({ x := 151, y := 338 } : Point)
          ({ x := -369, y := 1640 } : Point) ∧
        det ({ x := -48, y := -55 } : Point) ({ x := 151, y := 338 } : Point) ≡
          38 [ZMOD 73]) := by
  exact ⟨pinnedGlobalRootChoiceAlternateLineRow01_valid,
    pinnedGlobalRootChoiceAlternateLineRow02_valid,
    pinnedGlobalRootChoiceAlternateLineRow03_valid,
    pinnedGlobalRootChoiceAlternateLineRow04_valid,
    pinnedGlobalRootChoiceAlternateLineRow05_valid,
    pinnedGlobalRootChoiceAlternateLineRow06_valid,
    pinnedGlobalRootChoiceAlternateLineRow07_valid,
    pinnedGlobalRootChoiceAlternateLineRow08_valid,
    pinnedGlobalRootChoiceAlternateLineRow09_valid,
    pinnedGlobalRootChoiceAlternateLineRow10_valid,
    pinnedGlobalRootChoiceAlternateLineRow11_valid,
    pinnedGlobalRootChoiceAlternateLineRow12_valid,
    pinnedGlobalRootChoiceAlternateLineRow13_valid,
    pinnedGlobalRootChoiceAlternateLineRow14_valid⟩

end PythagoreanWalks

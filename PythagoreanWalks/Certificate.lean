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

theorem sub_add_smul_smul (r s : Int) (u v : Point) :
    sub (add (smul r u) (smul s v)) (smul r u) = smul s v := by
  ext <;> simp [sub, add, smul]

theorem det_add_smul_smul (strip u v : Point) (r s : Int) :
    det strip (add (smul r u) (smul s v)) =
      r * det strip u + s * det strip v := by
  simp [det, add, smul]
  ring

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

end PythagoreanWalks

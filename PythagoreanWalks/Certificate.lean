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

theorem sub_add_smul_smul (r s : Int) (u v : Point) :
    sub (add (smul r u) (smul s v)) (smul r u) = smul s v := by
  ext <;> simp [sub, add, smul]

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

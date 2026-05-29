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

theorem sub_add_smul_smul (r s : Int) (u v : Point) :
    sub (add (smul r u) (smul s v)) (smul r u) = smul s v := by
  ext <;> simp [sub, add, smul]

theorem latticeCertificateValid {r s : Int} {u v : Point}
    (hr : r ≠ 0) (hs : s ≠ 0)
    (hu : legalStep u) (hv : legalStep v) :
    certificateValid (add (smul r u) (smul s v)) (smul r u) := by
  constructor
  · exact legalStep_smul hr hu
  · simpa [sub_add_smul_smul] using legalStep_smul hs hv

end PythagoreanWalks

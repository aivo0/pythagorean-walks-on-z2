import json
from pathlib import Path
import unittest

from experiments.pythagorean_walks import (
    Certificate,
    KNOWN_DISTANCE_THREE_REPRESENTATIVES,
    bounded_two_step_search,
    consecutive_parameter_odd_axis_certificate,
    edge,
    euclid_parameter_difference_certificate,
    explicit_axis_certificate,
    find_two_step_certificate,
    horizontal_axis_certificate_table,
    horizontal_axis_proof_certificate,
    is_square,
    is_two_step_certificate,
    missing_residues,
    midpoint_axis_certificate,
    odd_residues,
    path_is_valid,
    pythagorean_leg_completion,
    residue_witnesses,
    shared_leg_axis_certificate_records,
    shared_leg_axis_certificate_table,
)


ARTIFACT_DIR = Path(__file__).resolve().parents[1] / "data"


class BasicGraphPredicateTests(unittest.TestCase):
    def test_square_detection(self):
        self.assertTrue(is_square(0))
        self.assertTrue(is_square(25))
        self.assertFalse(is_square(26))
        self.assertFalse(is_square(-1))

    def test_edges_require_nonzero_coordinate_changes(self):
        self.assertTrue(edge((0, 0), (3, 4)))
        self.assertTrue(edge((0, 0), (4, -3)))
        self.assertFalse(edge((0, 0), (5, 0)))
        self.assertFalse(edge((0, 0), (0, 5)))
        self.assertFalse(edge((0, 0), (1, 1)))

    def test_known_three_step_path_to_1_0(self):
        self.assertTrue(path_is_valid([(0, 0), (9, 12), (-3, 3), (1, 0)]))


class CertificateTests(unittest.TestCase):
    def test_paper_two_step_examples(self):
        self.assertTrue(is_two_step_certificate((1, 1), (4, -3)))
        self.assertTrue(is_two_step_certificate((2, 4), (77, -36)))
        self.assertTrue(is_two_step_certificate((2111, 569), (-50643549, 196449668)))

    def test_certificate_lengths_are_squares(self):
        cert = Certificate(target=(2, 4), midpoint=(77, -36))
        self.assertTrue(cert.valid())
        self.assertEqual(cert.first_length_squared, 85 * 85)
        self.assertEqual(cert.second_length_squared, 85 * 85)

    def test_small_horizontal_axis_certificates(self):
        expected = {
            3: (-7, 24),
            4: (-5, 12),
            5: (-22, 120),
            6: (3, 4),
            7: (-9, 12),
            8: (4, 3),
            9: (-6, 8),
            10: (5, 12),
            11: (-5, 12),
            12: (6, 8),
            13: (-32, 24),
            14: (5, 12),
            15: (-90, 56),
            16: (8, 6),
            17: (7, 24),
            18: (9, 12),
            19: (-16, 12),
            20: (10, 24),
        }
        table = horizontal_axis_certificate_table(3, 20, bound=2000)
        self.assertEqual(table, expected)
        for n, midpoint in table.items():
            self.assertTrue(is_two_step_certificate((n, 0), midpoint))

    def test_axis_certificate_artifact_validates(self):
        artifact = ARTIFACT_DIR / "horizontal_axis_certificates.json"
        data = json.loads(artifact.read_text())
        certificates = {
            int(row["n"]): tuple(row["midpoint"])
            for row in data["certificates"]
        }

        self.assertEqual(set(certificates), set(range(3, 21)))
        for n, midpoint in certificates.items():
            self.assertTrue(is_two_step_certificate((n, 0), midpoint))


class AxisFamilyTests(unittest.TestCase):
    def test_every_integer_from_three_has_a_pythagorean_leg_completion(self):
        for leg in range(3, 201):
            partner_leg, hypotenuse = pythagorean_leg_completion(leg)
            self.assertGreater(partner_leg, 0)
            self.assertEqual(leg * leg + partner_leg * partner_leg, hypotenuse * hypotenuse)

    def test_midpoint_formula_covers_even_axis_points_from_six(self):
        for n in range(6, 402, 2):
            cert = midpoint_axis_certificate(n)
            self.assertIsNotNone(cert)
            self.assertEqual(cert.target, (n, 0))
            self.assertEqual(cert.midpoint[0], n // 2)
            self.assertTrue(cert.valid())

        for n in (3, 4, 5):
            self.assertIsNone(midpoint_axis_certificate(n))

    def test_explicit_axis_certificate_covers_four(self):
        cert = explicit_axis_certificate(4)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.target, (4, 0))
        self.assertEqual(cert.midpoint, (-5, 12))
        self.assertTrue(cert.valid())

        for n in (1, 2, 3, 5, 6):
            self.assertIsNone(explicit_axis_certificate(n))

    def test_consecutive_parameter_formula_covers_odd_axis_points(self):
        for n in range(3, 402, 2):
            record = consecutive_parameter_odd_axis_certificate(n)
            self.assertIsNotNone(record)

            first_horizontal = (n - 1) * (2 * n + 1) // 2
            second_horizontal = (n + 1) * (2 * n - 1) // 2
            shared_leg = n * (n * n - 1)

            self.assertEqual(record.target_n, n)
            self.assertEqual(record.midpoint, (-first_horizontal, shared_leg))
            self.assertEqual(record.first_horizontal_leg, first_horizontal)
            self.assertEqual(record.second_horizontal_leg, second_horizontal)
            self.assertEqual(
                record.first_hypotenuse,
                (n - 1) * (2 * n * n + 2 * n + 1) // 2,
            )
            self.assertEqual(
                record.second_hypotenuse,
                (n + 1) * (2 * n * n - 2 * n + 1) // 2,
            )
            self.assertEqual(second_horizontal - first_horizontal, n)
            self.assertTrue(record.valid())

        for n in (1, 2, 4, 6):
            self.assertIsNone(consecutive_parameter_odd_axis_certificate(n))

    def test_horizontal_axis_proof_certificate_case_split(self):
        for n in range(3, 502):
            cert = horizontal_axis_proof_certificate(n)
            self.assertIsNotNone(cert)
            self.assertEqual(cert.target, (n, 0))
            self.assertTrue(cert.valid())

        for n in (1, 2):
            self.assertIsNone(horizontal_axis_proof_certificate(n))

    def test_shared_leg_generator_records_are_valid(self):
        records = shared_leg_axis_certificate_records(m_limit=12, scale_limit=6, n_max=80)
        self.assertTrue(records)

        for record in records:
            self.assertIn(record.relation, {"difference", "sum"})
            self.assertTrue(record.valid())

        covered = {record.target_n for record in records}
        for n in (3, 4, 5, 7, 9, 11, 17, 25, 35):
            self.assertIn(n, covered)

    def test_shared_leg_generator_bounded_odd_axis_coverage(self):
        table = shared_leg_axis_certificate_table(m_limit=30, scale_limit=10, n_max=200)
        missing_odd = [n for n in range(3, 201, 2) if n not in table]

        self.assertEqual(missing_odd, [])
        for n in range(3, 201, 2):
            self.assertTrue(table[n].valid())

    def test_euclid_parameter_difference_family(self):
        for m in range(2, 50):
            for t in range(1, 20):
                record = euclid_parameter_difference_certificate(m, t)
                self.assertEqual(record.target_n, t * (m * m + m * t + 1))
                self.assertTrue(record.valid())

        first_targets = [
            euclid_parameter_difference_certificate(m, 1).target_n
            for m in range(2, 8)
        ]
        self.assertEqual(first_targets, [7, 13, 21, 31, 43, 57])

    def test_residue_witnesses_for_odd_classes_mod_24(self):
        residues = odd_residues(24)

        euclid_records = [
            euclid_parameter_difference_certificate(m, t)
            for m in range(2, 81)
            for t in range(1, 81)
        ]
        euclid_witnesses = residue_witnesses(euclid_records, 24, residues)
        self.assertEqual(set(euclid_witnesses), set(residues))

        shared_leg_records = shared_leg_axis_certificate_records(
            m_limit=30,
            scale_limit=10,
            n_max=200,
        )
        self.assertEqual(missing_residues(shared_leg_records, 24, residues), ())

        for residue, record in residue_witnesses(shared_leg_records, 24, residues).items():
            self.assertEqual(record.target_n % 24, residue)
            self.assertTrue(record.valid())


class FalsificationTests(unittest.TestCase):
    def test_known_distance_three_examples_have_no_small_two_step_certificate(self):
        # This is bounded falsification, not a proof. The paper gives exact
        # arguments for these three obstructions.
        for target in KNOWN_DISTANCE_THREE_REPRESENTATIVES:
            self.assertIsNone(find_two_step_certificate(target, bound=200))

    def test_bad_hypothesis_all_axis_points_need_three_steps_after_two_is_false(self):
        self.assertEqual(find_two_step_certificate((3, 0), bound=50), (-7, 24))

    def test_bounded_search_result_labels_are_not_proofs(self):
        found = bounded_two_step_search((3, 0), bound=50)
        self.assertEqual(found.status, "found")
        self.assertEqual(found.certificate, (-7, 24))

        not_found = bounded_two_step_search((1, 0), bound=50)
        self.assertEqual(not_found.status, "not_found_within_bound")
        self.assertFalse(not_found.found)


if __name__ == "__main__":
    unittest.main()

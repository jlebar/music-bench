import unittest

from music_bench.schema import DatasetExample, NormalizedAnswer
from music_bench.scoring import score_prediction, sequence_edit_distance


def make_example() -> DatasetExample:
    return DatasetExample(
        id="dev-0000",
        image_path="images/dev-0000.png",
        question="dummy",
        target_measure=2,
        answer_notes=["C4", "D4", "E4"],
        metadata={
            "measure_note_sequences": [["G3", "A3"], ["C4", "D4", "E4"], ["F4", "G4"]],
            "skill_tags": ["measure_localization"],
        },
        lilypond_path="sources/dev-0000.ly",
        split="dev",
    )


class ScoringTests(unittest.TestCase):
    def test_exact_match(self) -> None:
        result = score_prediction(make_example(), NormalizedAnswer(notes=["C4", "D4", "E4"], valid=True))
        self.assertEqual(result.exact_match, 1.0)
        self.assertEqual(result.error_type, "exact_match")

    def test_wrong_measure(self) -> None:
        result = score_prediction(make_example(), NormalizedAnswer(notes=["F4", "G4"], valid=True))
        self.assertEqual(result.error_type, "wrong_measure")

    def test_octave_mistake(self) -> None:
        result = score_prediction(make_example(), NormalizedAnswer(notes=["C5", "D5", "E5"], valid=True))
        self.assertEqual(result.error_type, "octave_mistake")

    def test_formatting_failure(self) -> None:
        result = score_prediction(make_example(), NormalizedAnswer(notes=[], valid=False, error="invalid_json"))
        self.assertEqual(result.error_type, "formatting_failure")
        self.assertEqual(result.edit_distance, 3)

    def test_truncated_before_final_answer(self) -> None:
        result = score_prediction(make_example(), NormalizedAnswer(notes=[], valid=False, error="truncated_before_final_answer"))
        self.assertEqual(result.error_type, "truncated_before_final_answer")
        self.assertEqual(result.edit_distance, 3)

    def test_edit_distance(self) -> None:
        self.assertEqual(sequence_edit_distance(["C4", "D4"], ["C4", "E4", "F4"]), 2)


if __name__ == "__main__":
    unittest.main()

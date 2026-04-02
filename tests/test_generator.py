import json
import tempfile
import unittest
from pathlib import Path

from music_bench.generator import generate_split
from music_bench.lilypond import load_manifest
from music_bench.music import expected_measure_units, duration_units


class GeneratorTests(unittest.TestCase):
    def test_generate_split_creates_manifest_and_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = generate_split(Path(tmpdir), "dev", example_count=4, seed=123)
            self.assertTrue(manifest_path.exists())
            examples = load_manifest(manifest_path)
            self.assertEqual(len(examples), 4)
            for example in examples:
                lilypond_path = example.resolved_lilypond_path(manifest_path)
                self.assertTrue(lilypond_path.exists())
                source = lilypond_path.read_text(encoding="utf-8")
                self.assertIn("\\set Score.barNumberVisibility = #all-bar-numbers-visible", source)
                self.assertIn(f"measure {example.target_measure}", example.question)
                self.assertIn("measure_localization", example.metadata["skill_tags"])

    def test_contrast_pair_changes_target_answer(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = generate_split(Path(tmpdir), "dev", example_count=2, seed=999)
            examples = load_manifest(manifest_path)
            self.assertEqual(examples[0].metadata["family_id"], examples[1].metadata["family_id"])
            self.assertNotEqual(examples[0].answer_notes, examples[1].answer_notes)

    def test_measure_lengths_are_not_constant(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = generate_split(Path(tmpdir), "dev", example_count=10, seed=456)
            examples = load_manifest(manifest_path)
            note_counts = {example.metadata["note_count"] for example in examples}
            self.assertGreater(len(note_counts), 1)

    def test_measures_match_time_signature(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = generate_split(Path(tmpdir), "dev", example_count=12, seed=321)
            examples = load_manifest(manifest_path)
            for example in examples:
                expected = expected_measure_units(example.metadata["time_signature"])
                lilypond_path = example.resolved_lilypond_path(manifest_path)
                source = lilypond_path.read_text(encoding="utf-8")
                body = source.split("\\absolute {", 1)[1].split("\\bar", 1)[0]
                measures = [measure.strip() for measure in body.split("|") if measure.strip()]
                for measure in measures:
                    total = 0
                    for token in measure.split():
                        digits = "".join(char for char in token if char.isdigit())
                        if digits:
                            total += duration_units(int(digits))
                    self.assertEqual(total, expected, msg=f"{example.id} has malformed measure: {measure}")


if __name__ == "__main__":
    unittest.main()

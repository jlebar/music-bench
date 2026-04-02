import json
import tempfile
import unittest
from pathlib import Path

from music_bench.generator import generate_split
from music_bench.lilypond import load_manifest


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


if __name__ == "__main__":
    unittest.main()


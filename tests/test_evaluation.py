import json
import tempfile
import unittest
from pathlib import Path

from music_bench.evaluation import evaluate_manifest
from music_bench.generator import generate_split
from music_bench.providers import ModelConfig
from music_bench.reporting import generate_report
from music_bench.util import load_jsonl


class EvaluationTests(unittest.TestCase):
    def test_replay_evaluation_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            manifest_path = generate_split(root, "dev", example_count=2, seed=42)
            examples = load_jsonl(manifest_path)
            replay_file = root / "replay.jsonl"
            with replay_file.open("w", encoding="utf-8") as handle:
                for item in examples:
                    handle.write(json.dumps({"id": item["id"], "response": json.dumps({"notes": item["answer_notes"]})}) + "\n")
            results_file = root / "results.jsonl"
            evaluate_manifest(
                manifest_path=manifest_path,
                provider_name="replay",
                model_config=ModelConfig(model="replay"),
                results_file=results_file,
                replay_file=replay_file,
            )
            results = load_jsonl(results_file)
            self.assertEqual(len(results), 2)
            self.assertTrue(all(result["metrics"]["exact_match"] == 1.0 for result in results))
            report_dir = root / "report"
            markdown_path, csv_path = generate_report(manifest_path, results_file, report_dir)
            self.assertTrue(markdown_path.exists())
            self.assertTrue(csv_path.exists())


if __name__ == "__main__":
    unittest.main()

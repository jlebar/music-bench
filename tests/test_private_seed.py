import tempfile
import unittest
from pathlib import Path

from music_bench.generator import load_private_seed_from_file


class PrivateSeedTests(unittest.TestCase):
    def test_missing_file_returns_none(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            self.assertIsNone(load_private_seed_from_file(Path(tmpdir) / "missing-seed"))

    def test_reads_integer_seed_from_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "seed"
            path.write_text("12345\n", encoding="utf-8")
            self.assertEqual(load_private_seed_from_file(path), 12345)


if __name__ == "__main__":
    unittest.main()

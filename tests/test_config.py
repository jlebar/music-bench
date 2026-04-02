import tempfile
import textwrap
import unittest
from pathlib import Path

from music_bench.config import load_benchmark_config
from music_bench.generator import load_private_seed_from_env


class ConfigTests(unittest.TestCase):
    def test_load_benchmark_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "benchmark_config.toml"
            path.write_text(
                textwrap.dedent(
                    """
                    [benchmark]
                    version = "v9"
                    private_seed_env = "MY_PRIVATE_SEED"
                    private_seed_file = ".my-private-seed"

                    [splits.dev]
                    seed = 11
                    default_count = 3
                    visibility = "public"

                    [splits.public_test]
                    seed = 22
                    default_count = 4
                    visibility = "public"

                    [splits.private_test]
                    default_count = 5
                    visibility = "private"
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )
            config = load_benchmark_config(path)
            self.assertEqual(config.version, "v9")
            self.assertEqual(config.private_seed_env, "MY_PRIVATE_SEED")
            self.assertEqual(config.private_seed_file, Path(".my-private-seed"))
            self.assertEqual(config.split("dev").seed, 11)
            self.assertEqual(config.split("private_test").seed, None)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import tomllib


DEFAULT_CONFIG_PATH = Path("benchmark_config.toml")


@dataclass(frozen=True)
class SplitConfig:
    name: str
    default_count: int
    visibility: str
    seed: int | None = None


@dataclass(frozen=True)
class BenchmarkConfig:
    version: str
    private_seed_env: str
    private_seed_file: Path
    splits: dict[str, SplitConfig]

    def split(self, name: str) -> SplitConfig:
        try:
            return self.splits[name]
        except KeyError as exc:
            raise ValueError(f"Unknown split in config: {name}") from exc


def load_benchmark_config(path: Path) -> BenchmarkConfig:
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    benchmark = data.get("benchmark", {})
    split_entries = data.get("splits", {})
    splits: dict[str, SplitConfig] = {}
    for name, split_data in split_entries.items():
        splits[name] = SplitConfig(
            name=name,
            default_count=int(split_data["default_count"]),
            visibility=str(split_data["visibility"]),
            seed=int(split_data["seed"]) if "seed" in split_data else None,
        )
    return BenchmarkConfig(
        version=str(benchmark["version"]),
        private_seed_env=str(benchmark["private_seed_env"]),
        private_seed_file=Path(str(benchmark["private_seed_file"])),
        splits=splits,
    )

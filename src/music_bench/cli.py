from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from music_bench.config import DEFAULT_CONFIG_PATH, load_benchmark_config
from music_bench.evaluation import evaluate_manifest
from music_bench.generator import generate_splits
from music_bench.lilypond import render_manifest
from music_bench.providers import ModelConfig
from music_bench.reporting import generate_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="music-bench")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="Generate manifests and LilyPond sources")
    generate_parser.add_argument("--output-dir", type=Path, required=True)
    generate_parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    generate_parser.add_argument("--dev-count", type=int)
    generate_parser.add_argument("--public-test-count", type=int)
    generate_parser.add_argument("--private-test-count", type=int)
    generate_parser.add_argument("--private-seed", type=int)

    render_parser = subparsers.add_parser("render", help="Render score images from a manifest")
    render_parser.add_argument("--manifest", type=Path, required=True)
    render_parser.add_argument("--overwrite", action="store_true")

    eval_parser = subparsers.add_parser("evaluate", help="Run a provider against a manifest")
    eval_parser.add_argument("--manifest", type=Path, required=True)
    eval_parser.add_argument("--provider", choices=["openai", "anthropic", "google", "replay"], required=True)
    eval_parser.add_argument("--model", required=True)
    eval_parser.add_argument("--temperature", type=float, default=0.0)
    eval_parser.add_argument("--max-tokens", type=int, default=256)
    eval_parser.add_argument("--reasoning-effort", choices=["none", "low", "medium", "high", "xhigh"])
    eval_parser.add_argument("--results-file", type=Path, required=True)
    eval_parser.add_argument("--replay-file", type=Path)

    report_parser = subparsers.add_parser("report", help="Generate markdown and CSV summaries")
    report_parser.add_argument("--manifest", type=Path, required=True)
    report_parser.add_argument("--results-file", type=Path, required=True)
    report_parser.add_argument("--output-dir", type=Path, required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "generate":
            config = load_benchmark_config(args.config)
            manifests = generate_splits(
                args.output_dir,
                config=config,
                dev_count=args.dev_count,
                public_test_count=args.public_test_count,
                private_seed=args.private_seed,
                private_test_count=args.private_test_count,
            )
            for manifest in manifests:
                print(manifest)
            private_env = config.private_seed_env
            private_file = config.private_seed_file
            if args.private_seed is None and not private_file.exists() and not os.environ.get(private_env):
                print(
                    f"note: private_test not generated; create {private_file}, set {private_env}, or pass --private-seed",
                    file=sys.stderr,
                )
            return 0
        if args.command == "render":
            rendered = render_manifest(args.manifest, overwrite=args.overwrite)
            for path in rendered:
                print(path)
            return 0
        if args.command == "evaluate":
            if args.provider == "replay" and args.replay_file is None:
                parser.error("--replay-file is required when --provider replay")
            output = evaluate_manifest(
                manifest_path=args.manifest,
                provider_name=args.provider,
                model_config=ModelConfig(
                    model=args.model,
                    temperature=args.temperature,
                    max_tokens=args.max_tokens,
                    reasoning_effort=args.reasoning_effort,
                ),
                results_file=args.results_file,
                replay_file=args.replay_file,
            )
            print(output)
            return 0
        if args.command == "report":
            markdown_path, csv_path = generate_report(args.manifest, args.results_file, args.output_dir)
            print(markdown_path)
            print(csv_path)
            return 0
        parser.error(f"Unknown command: {args.command}")
        return 2
    except (RuntimeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

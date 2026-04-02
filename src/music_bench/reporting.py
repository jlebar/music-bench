from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

from music_bench.lilypond import load_manifest
from music_bench.util import load_jsonl


def generate_report(manifest_path: Path, results_file: Path, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    examples = {example.id: example for example in load_manifest(manifest_path)}
    results = load_jsonl(results_file)
    if not results:
        raise ValueError("Results file is empty")

    overall = aggregate_metrics(results)
    by_tag = aggregate_by_tag(results, examples)
    error_counts = Counter(result["metrics"]["error_type"] for result in results)

    markdown_path = output_dir / "report.md"
    csv_path = output_dir / "summary.csv"
    write_markdown_report(markdown_path, results[0]["provider"], results[0]["model"], overall, by_tag, error_counts)
    write_csv_summary(csv_path, overall, by_tag)
    return markdown_path, csv_path


def aggregate_metrics(results: list[dict]) -> dict[str, float]:
    count = len(results)
    metric_names = ["exact_match", "note_precision", "note_recall", "note_f1", "edit_distance"]
    return {
        name: sum(float(result["metrics"][name]) for result in results) / count
        for name in metric_names
    }


def aggregate_by_tag(results: list[dict], examples: dict[str, object]) -> dict[str, dict[str, float]]:
    buckets: dict[str, list[dict]] = defaultdict(list)
    for result in results:
        example = examples[result["id"]]
        for tag in example.metadata["skill_tags"]:
            buckets[tag].append(result)
    return {tag: aggregate_metrics(items) for tag, items in sorted(buckets.items())}


def write_markdown_report(
    path: Path,
    provider: str,
    model: str,
    overall: dict[str, float],
    by_tag: dict[str, dict[str, float]],
    error_counts: Counter,
) -> None:
    lines = [
        "# Benchmark Report",
        "",
        f"- Provider: `{provider}`",
        f"- Model: `{model}`",
        "",
        "## Overall",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    for key, value in overall.items():
        lines.append(f"| {key} | {value:.4f} |")
    lines.extend(["", "## By Tag", "", "| Tag | Exact Match | Note F1 | Edit Distance |", "| --- | ---: | ---: | ---: |"])
    for tag, metrics in by_tag.items():
        lines.append(f"| {tag} | {metrics['exact_match']:.4f} | {metrics['note_f1']:.4f} | {metrics['edit_distance']:.4f} |")
    lines.extend(["", "## Error Types", "", "| Error Type | Count |", "| --- | ---: |"])
    for error_type, count in error_counts.most_common():
        lines.append(f"| {error_type} | {count} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_csv_summary(path: Path, overall: dict[str, float], by_tag: dict[str, dict[str, float]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["bucket", "exact_match", "note_precision", "note_recall", "note_f1", "edit_distance"])
        writer.writerow(["overall", overall["exact_match"], overall["note_precision"], overall["note_recall"], overall["note_f1"], overall["edit_distance"]])
        for tag, metrics in by_tag.items():
            writer.writerow([tag, metrics["exact_match"], metrics["note_precision"], metrics["note_recall"], metrics["note_f1"], metrics["edit_distance"]])


from __future__ import annotations

import json
from pathlib import Path

from music_bench.lilypond import load_manifest
from music_bench.normalization import normalize_response
from music_bench.providers import ModelConfig, create_provider
from music_bench.schema import EvaluationResult
from music_bench.scoring import score_prediction


DEFAULT_PROMPT_TEMPLATE = (
    "{question}\n"
    "Do not include any explanation, markdown, or extra keys."
)


def evaluate_manifest(
    manifest_path: Path,
    provider_name: str,
    model_config: ModelConfig,
    results_file: Path,
    replay_file: Path | None = None,
    prompt_template: str = DEFAULT_PROMPT_TEMPLATE,
) -> Path:
    examples = load_manifest(manifest_path)
    provider = create_provider(provider_name, replay_file=replay_file)
    results_file.parent.mkdir(parents=True, exist_ok=True)
    with results_file.open("w", encoding="utf-8") as handle:
        for example in examples:
            prompt = prompt_template.format(question=example.question, target_measure=example.target_measure)
            provider_response = provider.generate(example, prompt, model_config, manifest_path)
            normalized = normalize_response(provider_response)
            metrics = score_prediction(example, normalized)
            result = EvaluationResult(
                id=example.id,
                provider=provider_name,
                model=model_config.model,
                raw_response=provider_response.raw_text,
                normalized_notes=normalized.notes,
                valid_json=normalized.valid,
                error=normalized.error,
                response_status=normalized.response_status,
                incomplete_details=normalized.incomplete_details,
                usage=normalized.usage,
                metrics={
                    "exact_match": metrics.exact_match,
                    "note_precision": metrics.note_precision,
                    "note_recall": metrics.note_recall,
                    "note_f1": metrics.note_f1,
                    "edit_distance": metrics.edit_distance,
                    "error_type": metrics.error_type,
                },
            )
            handle.write(json.dumps(result.to_dict(), sort_keys=True) + "\n")
    return results_file

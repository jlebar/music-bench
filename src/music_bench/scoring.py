from __future__ import annotations

from music_bench.music import multiset_overlap
from music_bench.schema import DatasetExample, NormalizedAnswer, ScoreMetrics


def score_prediction(example: DatasetExample, normalized: NormalizedAnswer) -> ScoreMetrics:
    if not normalized.valid:
        error_type = "truncated_before_final_answer" if normalized.error == "truncated_before_final_answer" else "formatting_failure"
        return ScoreMetrics(
            exact_match=0.0,
            note_precision=0.0,
            note_recall=0.0,
            note_f1=0.0,
            edit_distance=len(example.answer_notes),
            error_type=error_type,
        )

    gold = example.answer_notes
    predicted = normalized.notes
    exact = float(predicted == gold)
    overlap = multiset_overlap(predicted, gold)
    precision = overlap / len(predicted) if predicted else 0.0
    recall = overlap / len(gold) if gold else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if precision and recall else 0.0
    error_type = classify_error(example, predicted, exact == 1.0)
    return ScoreMetrics(
        exact_match=exact,
        note_precision=precision,
        note_recall=recall,
        note_f1=f1,
        edit_distance=sequence_edit_distance(predicted, gold),
        error_type=error_type,
    )


def classify_error(example: DatasetExample, predicted: list[str], exact: bool) -> str:
    if exact:
        return "exact_match"
    measure_sequences = example.metadata.get("measure_note_sequences", [])
    for index, sequence in enumerate(measure_sequences, start=1):
        if index != example.target_measure and sequence == predicted:
            return "wrong_measure"
    if same_spelling_different_octave(predicted, example.answer_notes):
        return "octave_mistake"
    if same_letter_octave_different_accidental(predicted, example.answer_notes):
        return "accidental_mistake"
    return "other_mismatch"


def same_spelling_different_octave(predicted: list[str], gold: list[str]) -> bool:
    if len(predicted) != len(gold):
        return False
    for left, right in zip(predicted, gold):
        if left[:-1] != right[:-1]:
            return False
    return predicted != gold


def same_letter_octave_different_accidental(predicted: list[str], gold: list[str]) -> bool:
    if len(predicted) != len(gold):
        return False
    def normalize(token: str) -> tuple[str, str]:
        if len(token) >= 3 and token[1] in "#b":
            return token[0], token[2:]
        return token[0], token[1:]
    for left, right in zip(predicted, gold):
        if normalize(left) != normalize(right):
            return False
    return predicted != gold


def sequence_edit_distance(left: list[str], right: list[str]) -> int:
    rows = len(left) + 1
    cols = len(right) + 1
    dp = [[0] * cols for _ in range(rows)]
    for row in range(rows):
        dp[row][0] = row
    for col in range(cols):
        dp[0][col] = col
    for row in range(1, rows):
        for col in range(1, cols):
            cost = 0 if left[row - 1] == right[col - 1] else 1
            dp[row][col] = min(
                dp[row - 1][col] + 1,
                dp[row][col - 1] + 1,
                dp[row - 1][col - 1] + cost,
            )
    return dp[-1][-1]

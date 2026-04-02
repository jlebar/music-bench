from __future__ import annotations

import json
import os
import random
from pathlib import Path

from music_bench.config import BenchmarkConfig
from music_bench.music import (
    CLEF_RANGES,
    KEY_SIGNATURES,
    TIME_SIGNATURE_PATTERNS,
    accidental_count,
    classify_skill_tags,
    key_signature_accidentals,
    pitch_range,
)
from music_bench.schema import DatasetExample, Measure, NoteEvent, Pitch, ScoreExcerpt
from music_bench.lilypond import score_to_lilypond_source

QUESTION_TEMPLATE = (
    'Read the score image and identify the written pitches in measure {measure}. '
    'Reply with strict JSON only in the form {{"notes":["C4","D#4"]}}. '
    'Spell accidentals with ASCII "#" and "b", for example "F#4" and "Bb3".'
)


def generate_splits(
    output_dir: Path,
    config: BenchmarkConfig,
    dev_count: int | None = None,
    public_test_count: int | None = None,
    private_seed: int | None = None,
    private_test_count: int | None = None,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    dev_split = config.split("dev")
    public_split = config.split("public_test")
    private_split = config.split("private_test")
    resolved_private_seed = (
        private_seed
        if private_seed is not None
        else load_private_seed_from_file(config.private_seed_file) or load_private_seed_from_env(config.private_seed_env)
    )
    manifests = [
        generate_split(
            output_dir,
            "dev",
            dev_count if dev_count is not None else dev_split.default_count,
            seed=required_public_seed(dev_split),
            benchmark_version=config.version,
            visibility=dev_split.visibility,
        ),
        generate_split(
            output_dir,
            "public_test",
            public_test_count if public_test_count is not None else public_split.default_count,
            seed=required_public_seed(public_split),
            benchmark_version=config.version,
            visibility=public_split.visibility,
        ),
    ]
    if resolved_private_seed is not None:
        manifests.append(
            generate_split(
                output_dir,
                "private_test",
                private_test_count if private_test_count is not None else private_split.default_count,
                seed=resolved_private_seed,
                benchmark_version=config.version,
                visibility=private_split.visibility,
            )
        )
    return manifests


def generate_split(
    output_dir: Path,
    split: str,
    example_count: int,
    seed: int,
    benchmark_version: str = "v1",
    visibility: str = "public",
) -> Path:
    split_dir = output_dir / split
    sources_dir = split_dir / "sources"
    images_dir = split_dir / "images"
    sources_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = split_dir / "manifest.jsonl"
    write_split_info(split_dir, split=split, seed=seed, example_count=example_count, benchmark_version=benchmark_version, visibility=visibility)
    rng = random.Random(seed)
    examples: list[DatasetExample] = []
    family_index = 0
    while len(examples) < example_count:
        family_seed = rng.randint(0, 10**9)
        family_examples = generate_contrast_family(split, family_index, family_seed, split_dir)
        for example in family_examples:
            examples.append(example)
            if len(examples) >= example_count:
                break
        family_index += 1

    with manifest_path.open("w", encoding="utf-8") as handle:
        for example in examples:
            handle.write(json.dumps(example.to_dict(), sort_keys=True) + "\n")
    return manifest_path


def write_split_info(
    split_dir: Path,
    *,
    split: str,
    seed: int,
    example_count: int,
    benchmark_version: str,
    visibility: str,
) -> None:
    info = {
        "benchmark_version": benchmark_version,
        "split": split,
        "seed": seed,
        "example_count": example_count,
        "visibility": visibility,
    }
    (split_dir / "split_info.json").write_text(json.dumps(info, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def required_public_seed(split_config) -> int:
    if split_config.seed is None:
        raise ValueError(f"Public split {split_config.name} is missing a seed")
    return split_config.seed


def load_private_seed_from_env(env_var: str) -> int | None:
    value = os.environ.get(env_var)
    if value is None or value == "":
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{env_var} must be an integer seed") from exc


def load_private_seed_from_file(path: Path) -> int | None:
    if not path.exists():
        return None
    value = path.read_text(encoding="utf-8").strip()
    if value == "":
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{path} must contain a single integer seed") from exc


def generate_contrast_family(split: str, family_index: int, seed: int, split_dir: Path) -> list[DatasetExample]:
    base_excerpt = sample_excerpt(seed, family_id=f"{split}-family-{family_index}", family_role="base")
    contrast_excerpt = mutate_excerpt(base_excerpt, seed + 1, family_role="contrast")
    return [
        excerpt_to_example(base_excerpt, split=split, split_dir=split_dir, ordinal=family_index * 2),
        excerpt_to_example(contrast_excerpt, split=split, split_dir=split_dir, ordinal=family_index * 2 + 1),
    ]


def sample_excerpt(seed: int, family_id: str, family_role: str) -> ScoreExcerpt:
    rng = random.Random(seed)
    clef = rng.choice(["treble", "bass"])
    key_signature = rng.choice(sorted(KEY_SIGNATURES.keys()))
    time_signature = rng.choice(sorted(TIME_SIGNATURE_PATTERNS.keys()))
    measure_count = rng.randint(4, 8)
    target_measure = rng.randint(1, measure_count)
    measures: list[Measure] = []
    for index in range(measure_count):
        force_accidentals = index == target_measure - 1 and rng.random() < 0.45
        measure_seed = seed * 100 + index
        measures.append(sample_measure(measure_seed, clef, key_signature, time_signature, force_accidentals=force_accidentals))
    return ScoreExcerpt(
        clef=clef,
        key_signature=key_signature,
        time_signature=time_signature,
        measures=measures,
        target_measure=target_measure,
        generator_seed=seed,
        family_id=family_id,
        family_role=family_role,
    )


def sample_measure(seed: int, clef: str, key_signature: str, time_signature: str, force_accidentals: bool) -> Measure:
    rng = random.Random(seed)
    durations = list(rng.choice(TIME_SIGNATURE_PATTERNS[time_signature]))
    notes: list[NoteEvent] = []
    accidental_budget = 1 if force_accidentals else 0
    for duration in durations:
        pitch = sample_pitch(rng, clef, key_signature, must_show_accidental=accidental_budget > 0)
        if must_count_as_accidental(pitch, key_signature):
            accidental_budget = 0
        notes.append(NoteEvent(pitch=pitch, duration=duration))
    return Measure(notes)


def sample_pitch(rng: random.Random, clef: str, key_signature: str, must_show_accidental: bool) -> Pitch:
    letter, octave = rng.choice(CLEF_RANGES[clef])
    key_defaults = key_signature_accidentals(key_signature)
    if must_show_accidental:
        default = key_defaults.get(letter, 0)
        accidental = rng.choice([candidate for candidate in (-1, 0, 1) if candidate != default])
    else:
        if rng.random() < 0.22:
            accidental = rng.choice([-1, 1])
        else:
            accidental = key_defaults.get(letter, 0)
    return Pitch(letter=letter, accidental=accidental, octave=octave)


def must_count_as_accidental(pitch: Pitch, key_signature: str) -> bool:
    defaults = key_signature_accidentals(key_signature)
    return pitch.accidental != defaults.get(pitch.letter, 0)


def mutate_excerpt(excerpt: ScoreExcerpt, seed: int, family_role: str) -> ScoreExcerpt:
    rng = random.Random(seed)
    measures = [
        Measure([NoteEvent(Pitch(note.pitch.letter, note.pitch.accidental, note.pitch.octave), note.duration) for note in measure.notes])
        for measure in excerpt.measures
    ]
    target = measures[excerpt.target_measure - 1]
    note_index = rng.randrange(len(target.notes))
    original = target.notes[note_index]
    replacement = mutate_pitch(original.pitch, excerpt.clef, excerpt.key_signature, rng)
    target.notes[note_index] = NoteEvent(pitch=replacement, duration=original.duration)
    return ScoreExcerpt(
        clef=excerpt.clef,
        key_signature=excerpt.key_signature,
        time_signature=excerpt.time_signature,
        measures=measures,
        target_measure=excerpt.target_measure,
        generator_seed=seed,
        family_id=excerpt.family_id,
        family_role=family_role,
    )


def mutate_pitch(pitch: Pitch, clef: str, key_signature: str, rng: random.Random) -> Pitch:
    candidates = [candidate for candidate in pitch_candidates(clef, key_signature) if candidate.token() != pitch.token()]
    rng.shuffle(candidates)
    for candidate in candidates:
        if candidate.letter == pitch.letter and candidate.octave == pitch.octave and candidate.accidental != pitch.accidental:
            return candidate
    for candidate in candidates:
        if candidate.octave == pitch.octave:
            return candidate
    return candidates[0]


def pitch_candidates(clef: str, key_signature: str) -> list[Pitch]:
    defaults = key_signature_accidentals(key_signature)
    candidates = []
    for letter, octave in CLEF_RANGES[clef]:
        base = defaults.get(letter, 0)
        for accidental in sorted({base, -1, 0, 1}):
            candidates.append(Pitch(letter=letter, accidental=accidental, octave=octave))
    return candidates


def excerpt_to_example(excerpt: ScoreExcerpt, split: str, split_dir: Path, ordinal: int) -> DatasetExample:
    example_id = f"{split}-{ordinal:04d}"
    sources_dir = split_dir / "sources"
    images_dir = split_dir / "images"
    lilypond_path = sources_dir / f"{example_id}.ly"
    image_path = images_dir / f"{example_id}.png"
    lilypond_source = score_to_lilypond_source(excerpt)
    lilypond_path.write_text(lilypond_source, encoding="utf-8")

    target_notes = excerpt.target_notes()
    metadata = {
        "clef": excerpt.clef,
        "key_signature": excerpt.key_signature,
        "time_signature": excerpt.time_signature,
        "note_count": len(target_notes),
        "accidental_count": accidental_count(target_notes, excerpt.key_signature),
        "pitch_range": pitch_range(target_notes),
        "generator_seed": excerpt.generator_seed,
        "skill_tags": classify_skill_tags(
            target_notes,
            clef=excerpt.clef,
            target_measure=excerpt.target_measure,
            accidental_count=accidental_count(target_notes, excerpt.key_signature),
        ),
        "family_id": excerpt.family_id,
        "family_role": excerpt.family_role,
        "measure_note_sequences": excerpt.all_measure_tokens(),
    }
    return DatasetExample(
        id=example_id,
        image_path=str(image_path.relative_to(split_dir)),
        question=QUESTION_TEMPLATE.format(measure=excerpt.target_measure),
        target_measure=excerpt.target_measure,
        answer_notes=target_notes,
        metadata=metadata,
        lilypond_path=str(lilypond_path.relative_to(split_dir)),
        split=split,
    )

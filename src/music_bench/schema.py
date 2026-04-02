from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Pitch:
    letter: str
    accidental: int
    octave: int

    def token(self) -> str:
        accidental = {-1: "b", 0: "", 1: "#"}[self.accidental]
        return f"{self.letter.upper()}{accidental}{self.octave}"

    def pitch_class(self) -> str:
        accidental = {-1: "b", 0: "", 1: "#"}[self.accidental]
        return f"{self.letter.upper()}{accidental}"

    @classmethod
    def from_token(cls, token: str) -> "Pitch":
        token = token.strip()
        if len(token) < 2:
            raise ValueError(f"Invalid pitch token: {token!r}")
        letter = token[0].upper()
        tail = token[1:]
        accidental = 0
        if tail.startswith("#"):
            accidental = 1
            tail = tail[1:]
        elif tail.startswith("b"):
            accidental = -1
            tail = tail[1:]
        if not tail.isdigit():
            raise ValueError(f"Invalid pitch token: {token!r}")
        return cls(letter=letter, accidental=accidental, octave=int(tail))


@dataclass(frozen=True)
class NoteEvent:
    pitch: Pitch
    duration: int

    def token(self) -> str:
        return self.pitch.token()


@dataclass(frozen=True)
class Measure:
    notes: list[NoteEvent]

    def note_tokens(self) -> list[str]:
        return [note.token() for note in self.notes]


@dataclass(frozen=True)
class ScoreExcerpt:
    clef: str
    key_signature: str
    time_signature: str
    measures: list[Measure]
    target_measure: int
    generator_seed: int
    family_id: str | None = None
    family_role: str | None = None

    def target_notes(self) -> list[str]:
        return self.measures[self.target_measure - 1].note_tokens()

    def all_measure_tokens(self) -> list[list[str]]:
        return [measure.note_tokens() for measure in self.measures]


@dataclass
class DatasetExample:
    id: str
    image_path: str
    question: str
    target_measure: int
    answer_notes: list[str]
    metadata: dict[str, Any]
    lilypond_path: str
    split: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DatasetExample":
        return cls(**data)

    def resolved_image_path(self, manifest_path: Path | None = None) -> Path:
        path = Path(self.image_path)
        if path.is_absolute() or manifest_path is None:
            return path
        return (manifest_path.parent / path).resolve()

    def resolved_lilypond_path(self, manifest_path: Path | None = None) -> Path:
        path = Path(self.lilypond_path)
        if path.is_absolute() or manifest_path is None:
            return path
        return (manifest_path.parent / path).resolve()


@dataclass(frozen=True)
class NormalizedAnswer:
    notes: list[str]
    valid: bool
    error: str | None = None
    response_status: str | None = None
    incomplete_details: dict[str, Any] | None = None
    usage: dict[str, Any] | None = None


@dataclass(frozen=True)
class ScoreMetrics:
    exact_match: float
    note_precision: float
    note_recall: float
    note_f1: float
    edit_distance: int
    error_type: str


@dataclass
class EvaluationResult:
    id: str
    provider: str
    model: str
    raw_response: str
    normalized_notes: list[str]
    valid_json: bool
    error: str | None
    response_status: str | None
    incomplete_details: dict[str, Any] | None
    usage: dict[str, Any] | None
    metrics: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProviderResponse:
    raw_text: str
    status: str | None = None
    incomplete_details: dict[str, Any] | None = None
    usage: dict[str, Any] | None = None

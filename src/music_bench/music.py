from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from music_bench.schema import Pitch

LETTER_TO_SEMITONE = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,
}

KEY_SIGNATURES = {
    "c_major": {"tonic": "c", "mode": "major", "accidentals": {}},
    "g_major": {"tonic": "g", "mode": "major", "accidentals": {"F": 1}},
    "d_major": {"tonic": "d", "mode": "major", "accidentals": {"F": 1, "C": 1}},
    "f_major": {"tonic": "f", "mode": "major", "accidentals": {"B": -1}},
    "bb_major": {"tonic": "bes", "mode": "major", "accidentals": {"B": -1, "E": -1}},
}

CLEF_RANGES = {
    "treble": [("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("A", 4), ("B", 4), ("C", 5), ("D", 5), ("E", 5), ("F", 5), ("G", 5), ("A", 5)],
    "bass": [("E", 2), ("F", 2), ("G", 2), ("A", 2), ("B", 2), ("C", 3), ("D", 3), ("E", 3), ("F", 3), ("G", 3), ("A", 3), ("B", 3), ("C", 4)],
}

TIME_SIGNATURE_PATTERNS = {
    "4/4": [[4, 4, 4, 4], [2, 4, 4], [4, 2, 4], [4, 4, 2], [2, 2], [8, 8, 4, 4], [4, 8, 8, 4], [4, 4, 8, 8], [8, 8, 8, 8, 4], [4, 8, 8, 8, 8]],
    "3/4": [[4, 4, 4], [2, 4], [4, 2], [8, 8, 4], [4, 8, 8], [8, 8, 8, 8, 4]],
    "2/4": [[4, 4], [2], [8, 8, 4], [4, 8, 8]],
}


def pitch_to_midi(pitch: Pitch) -> int:
    semitone = LETTER_TO_SEMITONE[pitch.letter.upper()] + pitch.accidental
    return 12 * (pitch.octave + 1) + semitone


def token_to_midi(token: str) -> int:
    return pitch_to_midi(Pitch.from_token(token))


def key_signature_accidentals(name: str) -> dict[str, int]:
    return KEY_SIGNATURES[name]["accidentals"]


def lilypond_key_signature(name: str) -> tuple[str, str]:
    key = KEY_SIGNATURES[name]
    return key["tonic"], key["mode"]


def lilypond_pitch_name(pitch: Pitch) -> str:
    base = pitch.letter.lower()
    if pitch.accidental == 1:
        base = {
            "c": "cis",
            "d": "dis",
            "e": "eis",
            "f": "fis",
            "g": "gis",
            "a": "ais",
            "b": "bis",
        }[base]
    elif pitch.accidental == -1:
        base = {
            "c": "ces",
            "d": "des",
            "e": "ees",
            "f": "fes",
            "g": "ges",
            "a": "aes",
            "b": "bes",
        }[base]
    offset = pitch.octave - 3
    if offset > 0:
        base += "'" * offset
    elif offset < 0:
        base += "," * (-offset)
    return base


def classify_skill_tags(note_tokens: list[str], clef: str, target_measure: int, accidental_count: int) -> list[str]:
    tags = {"measure_localization", "clef_reading"}
    if accidental_count > 0:
        tags.add("accidental_reading")
    if any(has_ledger_lines(Pitch.from_token(token), clef) for token in note_tokens):
        tags.add("ledger_lines")
    if target_measure > 1:
        tags.add("mid_excerpt_measure")
    return sorted(tags)


def has_ledger_lines(pitch: Pitch, clef: str) -> bool:
    staff_span = {
        "treble": (Pitch("E", 0, 4), Pitch("F", 0, 5)),
        "bass": (Pitch("G", 0, 2), Pitch("A", 0, 3)),
    }[clef]
    low_midi = pitch_to_midi(staff_span[0])
    high_midi = pitch_to_midi(staff_span[1])
    midi = pitch_to_midi(pitch)
    return midi < low_midi or midi > high_midi


def accidental_count(tokens: list[str], key_signature: str) -> int:
    key_defaults = key_signature_accidentals(key_signature)
    count = 0
    for token in tokens:
        pitch = Pitch.from_token(token)
        if pitch.accidental != key_defaults.get(pitch.letter, 0):
            count += 1
    return count


def pitch_range(tokens: list[str]) -> dict[str, int | str]:
    midis = [token_to_midi(token) for token in tokens]
    low = Pitch.from_token(min(tokens, key=token_to_midi))
    high = Pitch.from_token(max(tokens, key=token_to_midi))
    return {
        "lowest": low.token(),
        "highest": high.token(),
        "span_semitones": max(midis) - min(midis),
    }


def multiset_overlap(left: list[str], right: list[str]) -> int:
    left_counter = Counter(left)
    right_counter = Counter(right)
    return sum((left_counter & right_counter).values())


@dataclass(frozen=True)
class PromptTemplate:
    text: str

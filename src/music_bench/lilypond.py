from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from music_bench.music import lilypond_key_signature, lilypond_pitch_name
from music_bench.schema import DatasetExample, ScoreExcerpt


def score_to_lilypond_source(excerpt: ScoreExcerpt) -> str:
    tonic, mode = lilypond_key_signature(excerpt.key_signature)
    measures = []
    for measure in excerpt.measures:
        body = " ".join(f"{lilypond_pitch_name(note.pitch)}{note.duration}" for note in measure.notes)
        measures.append(body)
    music = " |\n      ".join(measures)
    return f'''\\version "2.24.0"

\\paper {{
  indent = 0\\mm
  line-width = 180\\mm
  ragged-right = ##t
}}

\\layout {{
  \\context {{
    \\Score
    \\override BarNumber.break-visibility = ##(#t #t #t)
    \\override BarNumber.self-alignment-X = #CENTER
  }}
}}

\\score {{
  \\new Staff {{
    \\set Score.barNumberVisibility = #all-bar-numbers-visible
    \\set Score.currentBarNumber = #1
    \\clef {excerpt.clef}
    \\key {tonic} \\{mode}
    \\time {excerpt.time_signature}
    \\absolute {{
      {music}
      \\bar "|."
    }}
  }}
}}
'''


def render_manifest(manifest_path: Path, overwrite: bool = False) -> list[Path]:
    examples = load_manifest(manifest_path)
    rendered = []
    for example in examples:
        rendered.append(render_example(example, manifest_path=manifest_path, overwrite=overwrite))
    return rendered


def render_example(example: DatasetExample, manifest_path: Path, overwrite: bool = False) -> Path:
    lilypond_path = example.resolved_lilypond_path(manifest_path)
    image_path = example.resolved_image_path(manifest_path)
    if image_path.exists() and not overwrite:
        return image_path
    lilypond_executable = shutil.which("lilypond")
    if not lilypond_executable:
        raise RuntimeError("lilypond is not installed. Install LilyPond before running the render command.")
    image_path.parent.mkdir(parents=True, exist_ok=True)
    output_stem = image_path.with_suffix("")
    command = [
        lilypond_executable,
        "--png",
        "-dcrop",
        "-dresolution=220",
        "-o",
        str(output_stem),
        str(lilypond_path),
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)
    candidates = [
        output_stem.with_name(f"{output_stem.name}.cropped.png"),
        output_stem.with_suffix(".png"),
    ]
    expected = next((candidate for candidate in candidates if candidate.exists()), None)
    if expected is None:
        raise RuntimeError(f"LilyPond did not produce the expected image: {image_path}")
    if expected != image_path:
        expected.replace(image_path)
    if not image_path.exists():
        raise RuntimeError(f"LilyPond did not produce the expected image: {image_path}")
    return image_path


def load_manifest(manifest_path: Path) -> list[DatasetExample]:
    from music_bench.util import load_jsonl

    return [DatasetExample.from_dict(item) for item in load_jsonl(manifest_path)]

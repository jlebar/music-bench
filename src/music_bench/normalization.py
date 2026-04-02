from __future__ import annotations

import json
import re

from music_bench.schema import NormalizedAnswer, ProviderResponse

NOTE_TOKEN_RE = re.compile(r"^[A-G](?:#|b)?[0-8]$")


def normalize_response(response: str | ProviderResponse) -> NormalizedAnswer:
    if isinstance(response, ProviderResponse):
        raw_response = response.raw_text
        response_status = response.status
        incomplete_details = response.incomplete_details
        usage = response.usage
    else:
        raw_response = response
        response_status = None
        incomplete_details = None
        usage = None

    candidate = raw_response.strip()
    if not candidate and response_status == "incomplete":
        return NormalizedAnswer(
            notes=[],
            valid=False,
            error="truncated_before_final_answer",
            response_status=response_status,
            incomplete_details=incomplete_details,
            usage=usage,
        )
    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError:
        if response_status == "incomplete" and incomplete_details and incomplete_details.get("reason") == "max_output_tokens":
            return NormalizedAnswer(
                notes=[],
                valid=False,
                error="truncated_before_final_answer",
                response_status=response_status,
                incomplete_details=incomplete_details,
                usage=usage,
            )
        return NormalizedAnswer(
            notes=[],
            valid=False,
            error="invalid_json",
            response_status=response_status,
            incomplete_details=incomplete_details,
            usage=usage,
        )
    if not isinstance(payload, dict):
        return NormalizedAnswer(
            notes=[],
            valid=False,
            error="invalid_json",
            response_status=response_status,
            incomplete_details=incomplete_details,
            usage=usage,
        )
    notes = payload.get("notes")
    if not isinstance(notes, list):
        return NormalizedAnswer(
            notes=[],
            valid=False,
            error="missing_notes",
            response_status=response_status,
            incomplete_details=incomplete_details,
            usage=usage,
        )
    normalized: list[str] = []
    for note in notes:
        if not isinstance(note, str):
            return NormalizedAnswer(
                notes=[],
                valid=False,
                error="invalid_note_type",
                response_status=response_status,
                incomplete_details=incomplete_details,
                usage=usage,
            )
        token = canonicalize_note_token(note)
        if token is None:
            return NormalizedAnswer(
                notes=[],
                valid=False,
                error="invalid_note_token",
                response_status=response_status,
                incomplete_details=incomplete_details,
                usage=usage,
            )
        normalized.append(token)
    return NormalizedAnswer(
        notes=normalized,
        valid=True,
        error=None,
        response_status=response_status,
        incomplete_details=incomplete_details,
        usage=usage,
    )


def canonicalize_note_token(token: str) -> str | None:
    stripped = token.strip().replace("♯", "#").replace("♭", "b")
    if not stripped:
        return None
    letter = stripped[0].upper()
    remainder = stripped[1:]
    accidental = ""
    if remainder.startswith("#"):
        accidental = "#"
        remainder = remainder[1:]
    elif remainder.startswith(("b", "B")):
        accidental = "b"
        remainder = remainder[1:]
    canonical = f"{letter}{accidental}{remainder}"
    return canonical if NOTE_TOKEN_RE.match(canonical) else None

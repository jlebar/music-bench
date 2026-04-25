from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
from urllib import error, request

from music_bench.schema import DatasetExample, ProviderResponse

NOTE_TOKEN_ENUM = [
    f"{letter}{accidental}{octave}"
    for octave in range(9)
    for letter in "ABCDEFG"
    for accidental in ("", "#", "b")
]


def note_array_schema() -> dict:
    return {
        "type": "array",
        "items": {
            "type": "string",
            "enum": NOTE_TOKEN_ENUM,
        },
    }


class ProviderAdapter(Protocol):
    def generate(self, example: DatasetExample, prompt_template: str, model_config: "ModelConfig", manifest_path: Path) -> ProviderResponse:
        ...


@dataclass(frozen=True)
class ModelConfig:
    model: str
    temperature: float = 0.0
    max_tokens: int = 256
    reasoning_effort: str | None = None


def create_provider(name: str, replay_file: Path | None = None) -> ProviderAdapter:
    providers: dict[str, ProviderAdapter] = {
        "openai": OpenAIAdapter(),
        "anthropic": AnthropicAdapter(),
        "google": GoogleAdapter(),
    }
    if name == "replay":
        if replay_file is None:
            raise ValueError("Replay provider requires --replay-file")
        return ReplayAdapter(replay_file)
    try:
        return providers[name]
    except KeyError as exc:
        raise ValueError(f"Unsupported provider: {name}") from exc


class ReplayAdapter:
    def __init__(self, replay_file: Path) -> None:
        self.responses = {}
        with replay_file.open("r", encoding="utf-8") as handle:
            for line in handle:
                item = json.loads(line)
                self.responses[item["id"]] = item["response"]

    def generate(self, example: DatasetExample, prompt_template: str, model_config: ModelConfig, manifest_path: Path) -> ProviderResponse:
        try:
            return ProviderResponse(raw_text=self.responses[example.id], status="completed")
        except KeyError as exc:
            raise KeyError(f"Replay file is missing an entry for {example.id}") from exc


class OpenAIAdapter:
    endpoint = "https://api.openai.com/v1/responses"

    def generate(self, example: DatasetExample, prompt_template: str, model_config: ModelConfig, manifest_path: Path) -> ProviderResponse:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        data_url = image_to_data_url(example, manifest_path)
        payload = {
            "model": model_config.model,
            "max_output_tokens": model_config.max_tokens,
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt_template},
                        {"type": "input_image", "image_url": data_url},
                    ],
                }
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "measure_notes",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "notes": note_array_schema(),
                        },
                        "required": ["notes"],
                    },
                }
            },
        }
        if model_config.temperature not in (None, 0.0):
            payload["temperature"] = model_config.temperature
        reasoning_effort = openai_reasoning_effort(model_config.model, model_config.reasoning_effort)
        if reasoning_effort is not None:
            payload["reasoning"] = {"effort": reasoning_effort}
        response = http_post_json(self.endpoint, payload, headers={"Authorization": f"Bearer {api_key}"})
        raw_text = ""
        if "output_text" in response:
            raw_text = response["output_text"]
        else:
            texts: list[str] = []
            for item in response.get("output", []):
                for content in item.get("content", []):
                    if content.get("type") == "output_text":
                        texts.append(content.get("text", ""))
            raw_text = "\n".join(texts).strip()
        return ProviderResponse(
            raw_text=raw_text,
            status=response.get("status"),
            incomplete_details=response.get("incomplete_details"),
            usage=response.get("usage"),
        )


class AnthropicAdapter:
    endpoint = "https://api.anthropic.com/v1/messages"

    def generate(self, example: DatasetExample, prompt_template: str, model_config: ModelConfig, manifest_path: Path) -> ProviderResponse:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        media_type, b64 = image_to_base64(example, manifest_path)
        payload = {
            "model": model_config.model,
            "max_tokens": model_config.max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": b64,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt_template,
                        },
                    ],
                }
            ],
        }
        if model_config.temperature not in (None, 0.0):
            payload["temperature"] = model_config.temperature
        response = http_post_json(
            self.endpoint,
            payload,
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
        )
        parts = [part.get("text", "") for part in response.get("content", []) if part.get("type") == "text"]
        return ProviderResponse(raw_text="\n".join(parts).strip(), usage=response.get("usage"), status=response.get("stop_reason"))


def openai_reasoning_effort(model_name: str, reasoning_effort: str | None) -> str | None:
    if reasoning_effort is not None:
        return reasoning_effort
    if model_name.startswith("gpt-5.5"):
        return "none"
    return None


class GoogleAdapter:
    endpoint_template = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

    def generate(self, example: DatasetExample, prompt_template: str, model_config: ModelConfig, manifest_path: Path) -> ProviderResponse:
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY or GOOGLE_API_KEY is not set")
        media_type, b64 = image_to_base64(example, manifest_path)
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt_template},
                        {"inline_data": {"mime_type": media_type, "data": b64}},
                    ]
                }
            ],
            "generationConfig": {
                "temperature": model_config.temperature,
                "maxOutputTokens": model_config.max_tokens,
                "responseMimeType": "application/json",
                "responseJsonSchema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {"notes": note_array_schema()},
                    "required": ["notes"],
                },
            },
        }
        thinking_config = google_thinking_config(model_config.model, model_config.reasoning_effort)
        if thinking_config is not None:
            payload["generationConfig"]["thinkingConfig"] = thinking_config
        response = http_post_json(self.endpoint_template.format(model=model_config.model, key=api_key), payload, headers={})
        texts = []
        finish_reasons = []
        for candidate in response.get("candidates", []):
            finish_reasons.append(candidate.get("finishReason"))
            for part in candidate.get("content", {}).get("parts", []):
                if "text" in part:
                    texts.append(part["text"])
        raw_text = "\n".join(texts).strip()
        primary_reason = finish_reasons[0] if finish_reasons else None
        status = "completed"
        incomplete_details = None
        if primary_reason == "MAX_TOKENS":
            status = "incomplete"
            incomplete_details = {"reason": "max_output_tokens", "provider_finish_reason": primary_reason}
        elif not raw_text and primary_reason is not None:
            status = "incomplete"
            incomplete_details = {"reason": "no_text_output", "provider_finish_reason": primary_reason}
        return ProviderResponse(
            raw_text=raw_text,
            status=status,
            incomplete_details=incomplete_details,
            usage=response.get("usageMetadata"),
        )


def google_thinking_config(model_name: str, reasoning_effort: str | None) -> dict | None:
    if reasoning_effort is None:
        if model_name.startswith("gemini-2.5-flash"):
            return {"thinkingBudget": 0}
        if model_name.startswith("gemini-3.1-pro"):
            return {"thinkingLevel": "low"}
        if model_name.startswith("gemini-3"):
            return {"thinkingLevel": "minimal"}
        return None
    if model_name.startswith("gemini-2.5"):
        budget_map = {
            "none": 0,
            "low": 1024,
            "medium": 4096,
            "high": 8192,
            "xhigh": 16384,
        }
        return {"thinkingBudget": budget_map[reasoning_effort]}
    if model_name.startswith("gemini-3"):
        level_map = {
            "none": "minimal",
            "low": "low",
            "medium": "medium",
            "high": "high",
            "xhigh": "high",
        }
        return {"thinkingLevel": level_map[reasoning_effort]}
    return None


def image_to_base64(example: DatasetExample, manifest_path: Path) -> tuple[str, str]:
    image_path = example.resolved_image_path(manifest_path)
    data = image_path.read_bytes()
    media_type = "image/png" if image_path.suffix.lower() == ".png" else "image/jpeg"
    return media_type, base64.b64encode(data).decode("ascii")


def image_to_data_url(example: DatasetExample, manifest_path: Path) -> str:
    media_type, b64 = image_to_base64(example, manifest_path)
    return f"data:{media_type};base64,{b64}"


def http_post_json(url: str, payload: dict, headers: dict[str, str]) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    for key, value in headers.items():
        req.add_header(key, value)
    try:
        with request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from provider: {body}") from exc

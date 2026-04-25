import unittest
from pathlib import Path
from unittest import mock

from music_bench.providers import AnthropicAdapter, ModelConfig, google_thinking_config, note_array_schema, openai_reasoning_effort
from music_bench.schema import DatasetExample


class ProviderTests(unittest.TestCase):
    def test_google_default_thinking_for_gemini_25_flash(self) -> None:
        self.assertEqual(google_thinking_config("gemini-2.5-flash", None), {"thinkingBudget": 0})

    def test_google_default_thinking_for_gemini_3_flash(self) -> None:
        self.assertEqual(google_thinking_config("gemini-3-flash-preview", None), {"thinkingLevel": "minimal"})

    def test_google_default_thinking_for_gemini_3_pro(self) -> None:
        self.assertEqual(google_thinking_config("gemini-3.1-pro-preview", None), {"thinkingLevel": "low"})

    def test_google_latest_alias_has_no_implicit_default(self) -> None:
        self.assertIsNone(google_thinking_config("gemini-flash-latest", None))

    def test_google_schema_uses_enum_note_tokens(self) -> None:
        schema = note_array_schema()
        self.assertEqual(schema["type"], "array")
        self.assertEqual(schema["items"]["type"], "string")
        self.assertIn("C4", schema["items"]["enum"])
        self.assertIn("Bb3", schema["items"]["enum"])
        self.assertNotIn("H2", schema["items"]["enum"])

    def test_openai_default_reasoning_for_gpt_55(self) -> None:
        self.assertEqual(openai_reasoning_effort("gpt-5.5", None), "none")
        self.assertEqual(openai_reasoning_effort("gpt-5.5-2026-04-23", None), "none")
        self.assertIsNone(openai_reasoning_effort("gpt-5.4", None))
        self.assertEqual(openai_reasoning_effort("gpt-5.5", "low"), "low")

    def test_anthropic_omits_default_temperature(self) -> None:
        captured_payloads = []

        def fake_post(url: str, payload: dict, headers: dict) -> dict:
            captured_payloads.append(payload)
            return {"content": [{"type": "text", "text": '{"notes":["C4"]}'}], "stop_reason": "end_turn"}

        example = DatasetExample(
            id="example",
            image_path="example.png",
            question="Question?",
            target_measure=1,
            answer_notes=["C4"],
            metadata={},
            lilypond_path="example.ly",
            split="dev",
        )
        adapter = AnthropicAdapter()
        with (
            mock.patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}),
            mock.patch("music_bench.providers.image_to_base64", return_value=("image/png", "abc")),
            mock.patch("music_bench.providers.http_post_json", side_effect=fake_post),
        ):
            adapter.generate(example, "prompt", ModelConfig(model="claude-opus-4-7"), Path("manifest.jsonl"))

        self.assertNotIn("temperature", captured_payloads[0])


if __name__ == "__main__":
    unittest.main()

import unittest

from music_bench.providers import google_thinking_config, note_array_schema


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


if __name__ == "__main__":
    unittest.main()

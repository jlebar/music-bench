import unittest

from music_bench.normalization import canonicalize_note_token, normalize_response
from music_bench.schema import ProviderResponse


class NormalizationTests(unittest.TestCase):
    def test_normalizes_valid_json(self) -> None:
        normalized = normalize_response('{"notes":[" c4 ","f#5","Bb3"]}')
        self.assertTrue(normalized.valid)
        self.assertEqual(normalized.notes, ["C4", "F#5", "Bb3"])

    def test_rejects_non_json(self) -> None:
        normalized = normalize_response("C4 D4 E4")
        self.assertFalse(normalized.valid)
        self.assertEqual(normalized.error, "invalid_json")

    def test_rejects_invalid_note_token(self) -> None:
        normalized = normalize_response('{"notes":["H2"]}')
        self.assertFalse(normalized.valid)
        self.assertEqual(normalized.error, "invalid_note_token")

    def test_canonicalize_unicode_accidentals(self) -> None:
        self.assertEqual(canonicalize_note_token("g♯4"), "G#4")
        self.assertEqual(canonicalize_note_token("b♭3"), "Bb3")

    def test_incomplete_response_is_classified_as_truncated(self) -> None:
        normalized = normalize_response(
            ProviderResponse(
                raw_text="",
                status="incomplete",
                incomplete_details={"reason": "max_output_tokens"},
                usage={"output_tokens": 256, "output_tokens_details": {"reasoning_tokens": 256}},
            )
        )
        self.assertFalse(normalized.valid)
        self.assertEqual(normalized.error, "truncated_before_final_answer")
        self.assertEqual(normalized.response_status, "incomplete")
        self.assertEqual(normalized.incomplete_details, {"reason": "max_output_tokens"})

    def test_incomplete_invalid_json_is_classified_as_truncated(self) -> None:
        normalized = normalize_response(
            ProviderResponse(
                raw_text="Here is the JSON requested:",
                status="incomplete",
                incomplete_details={"reason": "max_output_tokens", "provider_finish_reason": "MAX_TOKENS"},
            )
        )
        self.assertFalse(normalized.valid)
        self.assertEqual(normalized.error, "truncated_before_final_answer")


if __name__ == "__main__":
    unittest.main()

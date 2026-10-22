"""Tests for application configuration."""

import os
import unittest
from unittest.mock import patch

from app.config.settings import Settings, SettingsError, get_settings


class SettingsTests(unittest.TestCase):
    @patch("app.config.settings.load_dotenv")
    @patch.dict(
        os.environ,
        {
            "OPENAI_API_KEY": "test-key",
            "OPENAI_MODEL": "test-model",
            "OPENAI_TEMPERATURE": "0.7",
            "OPENAI_MAX_OUTPUT_TOKENS": "256",
        },
        clear=True,
    )
    def test_loads_settings_from_environment(self, _load_dotenv: object) -> None:
        settings = get_settings()

        self.assertEqual(settings.api_key, "test-key")
        self.assertEqual(settings.model, "test-model")
        self.assertEqual(settings.temperature, 0.7)
        self.assertEqual(settings.max_output_tokens, 256)

    def test_defaults_generation_settings(self) -> None:
        settings = Settings()

        self.assertEqual(settings.model, "gpt-4.1-mini")
        self.assertEqual(settings.temperature, 0.2)
        self.assertEqual(settings.max_output_tokens, 512)

    def test_rejects_invalid_temperature(self) -> None:
        with self.assertRaises(SettingsError):
            Settings(temperature=2.1)

    def test_api_key_is_not_in_settings_repr(self) -> None:
        self.assertNotIn("secret", repr(Settings(api_key="secret")))


if __name__ == "__main__":
    unittest.main()

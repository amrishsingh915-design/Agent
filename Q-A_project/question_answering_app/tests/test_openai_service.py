"""Tests for the OpenAI service."""

import unittest
from unittest.mock import Mock, patch

from openai import APIError

from app.config.settings import Settings
from app.services.openai_service import (
    OpenAIConfigurationError,
    OpenAIRequestError,
    OpenAIService,
)


class OpenAIServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = Settings(api_key="test-key")
        self.client = Mock()
        self.service = OpenAIService(settings=self.settings, client=self.client)

    def test_generates_answer_using_model_parameters_and_history(self) -> None:
        messages = [
            {"role": "user", "content": "What is 2 + 2?"},
            {"role": "assistant", "content": "It is 4."},
            {"role": "user", "content": "Why?"},
        ]
        self.client.responses.create.return_value.output_text = "Because 2 + 2 = 4."

        answer = self.service.generate_answer(messages)

        self.assertEqual(answer, "Because 2 + 2 = 4.")
        self.client.responses.create.assert_called_once_with(
            model=self.settings.model,
            input=messages,
            temperature=self.settings.temperature,
            max_output_tokens=self.settings.max_output_tokens,
        )

    def test_missing_api_key_fails_with_safe_configuration_error(self) -> None:
        with self.assertRaisesRegex(
            OpenAIConfigurationError, "Set OPENAI_API_KEY"
        ):
            OpenAIService(settings=Settings())

    @patch("app.services.openai_service.OpenAI")
    def test_initializes_sdk_client_with_configured_api_key(
        self, openai_client: Mock
    ) -> None:
        OpenAIService(settings=self.settings)

        openai_client.assert_called_once_with(api_key="test-key")

    def test_empty_history_is_rejected_without_an_api_call(self) -> None:
        with self.assertRaises(ValueError):
            self.service.generate_answer([])

        self.client.responses.create.assert_not_called()

    def test_api_failure_is_wrapped_without_exposing_details(self) -> None:
        self.client.responses.create.side_effect = APIError(
            "sensitive internal detail", request=Mock(), body=None
        )

        with self.assertRaises(OpenAIRequestError) as error:
            self.service.generate_answer([{"role": "user", "content": "Hello"}])

        self.assertNotIn("sensitive internal detail", str(error.exception))
        self.assertEqual(
            str(error.exception),
            "Unable to generate an answer right now. Please try again.",
        )

    def test_empty_api_response_is_a_safe_error(self) -> None:
        self.client.responses.create.return_value.output_text = ""

        with self.assertRaisesRegex(OpenAIRequestError, "empty answer"):
            self.service.generate_answer([{"role": "user", "content": "Hello"}])


if __name__ == "__main__":
    unittest.main()

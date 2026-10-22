"""OpenAI Responses API integration."""

from typing import Literal, TypedDict

from openai import OpenAI, OpenAIError

from app.config.settings import Settings, SettingsError, get_settings


class ConversationMessage(TypedDict):
    role: Literal["system", "developer", "user", "assistant"]
    content: str


class OpenAIServiceError(Exception):
    """Base class for safe, user-facing OpenAI service errors."""


class OpenAIConfigurationError(OpenAIServiceError):
    """Raised when the OpenAI client cannot be configured."""


class OpenAIRequestError(OpenAIServiceError):
    """Raised when an OpenAI request fails or returns no answer."""


class OpenAIService:
    """Generate answers from conversation history using OpenAI."""

    def __init__(
        self,
        settings: Settings | None = None,
        client: OpenAI | None = None,
    ) -> None:
        try:
            self._settings = settings if settings is not None else get_settings()
        except SettingsError as exc:
            raise OpenAIConfigurationError(str(exc)) from None

        if not self._settings.api_key or not self._settings.api_key.strip():
            raise OpenAIConfigurationError(
                "OpenAI is not configured. Set OPENAI_API_KEY in the project .env file."
            )

        try:
            self._client = (
                client
                if client is not None
                else OpenAI(api_key=self._settings.api_key)
            )
        except OpenAIError:
            raise OpenAIConfigurationError(
                "The OpenAI client could not be initialized. Check your OpenAI settings."
            ) from None

    def generate_answer(self, messages: list[ConversationMessage]) -> str:
        """Return the assistant's text answer for the supplied conversation."""
        if not messages:
            raise ValueError("At least one conversation message is required.")

        try:
            response = self._client.responses.create(
                model=self._settings.model,
                input=messages,
                temperature=self._settings.temperature,
                max_output_tokens=self._settings.max_output_tokens,
            )
        except OpenAIError:
            raise OpenAIRequestError(
                "Unable to generate an answer right now. Please try again."
            ) from None

        if not response.output_text:
            raise OpenAIRequestError(
                "The AI returned an empty answer. Please try again."
            )
        return response.output_text

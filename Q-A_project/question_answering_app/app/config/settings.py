"""Application settings loaded from the project environment."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class SettingsError(ValueError):
    """Raised when an environment setting is invalid."""


@dataclass(frozen=True)
class Settings:
    api_key: str | None = field(default=None, repr=False)
    model: str = "gpt-4.1-mini"
    temperature: float = 0.2
    max_output_tokens: int = 512

    def __post_init__(self) -> None:
        if not self.model.strip():
            raise SettingsError("OPENAI_MODEL must not be empty.")
        if not 0 <= self.temperature <= 2:
            raise SettingsError("OPENAI_TEMPERATURE must be between 0 and 2.")
        if self.max_output_tokens <= 0:
            raise SettingsError("OPENAI_MAX_OUTPUT_TOKENS must be greater than 0.")


def get_settings() -> Settings:
    """Load settings from environment variables and the project .env file."""
    load_dotenv(PROJECT_ROOT / ".env")

    try:
        temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))
    except ValueError:
        raise SettingsError("OPENAI_TEMPERATURE must be a number.") from None

    try:
        max_output_tokens = int(os.getenv("OPENAI_MAX_OUTPUT_TOKENS", "512"))
    except ValueError:
        raise SettingsError("OPENAI_MAX_OUTPUT_TOKENS must be a whole number.") from None

    return Settings(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )

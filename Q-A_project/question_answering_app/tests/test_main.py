"""Tests for Streamlit conversation message preparation."""

import unittest

from app.main import build_request_messages
from app.prompts.qa_prompt import SYSTEM_PROMPT


class RequestMessagesTests(unittest.TestCase):
    def test_adds_system_prompt_and_new_question_after_history(self) -> None:
        history = [
            {"role": "user", "content": "What is a haiku?"},
            {"role": "assistant", "content": "A short poem."},
        ]

        messages = build_request_messages(history, "Give me an example.")

        self.assertEqual(
            messages,
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                *history,
                {"role": "user", "content": "Give me an example."},
            ],
        )
        self.assertEqual(history, messages[1:-1])


if __name__ == "__main__":
    unittest.main()

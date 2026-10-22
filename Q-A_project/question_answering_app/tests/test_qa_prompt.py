"""Tests for the question-answering system prompt."""

import unittest

from app.prompts.qa_prompt import SYSTEM_PROMPT


class SystemPromptTests(unittest.TestCase):
    def test_prompt_covers_answering_and_conversation_guidance(self) -> None:
        for instruction in (
            "Answer questions clearly",
            "concise",
            "If you do not know",
            "Do not fabricate facts",
            "conversation history",
            "Markdown",
        ):
            with self.subTest(instruction=instruction):
                self.assertIn(instruction, SYSTEM_PROMPT)


if __name__ == "__main__":
    unittest.main()

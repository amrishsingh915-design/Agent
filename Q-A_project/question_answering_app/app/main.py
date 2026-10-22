"""Streamlit application entry point."""

import streamlit as st

from app.prompts.qa_prompt import SYSTEM_PROMPT
from app.services.openai_service import (
    ConversationMessage,
    OpenAIService,
    OpenAIServiceError,
)


def build_request_messages(
    history: list[ConversationMessage], question: str
) -> list[ConversationMessage]:
    """Combine system instructions, prior turns, and the current question."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": question},
    ]


def main() -> None:
    st.set_page_config(page_title="Q&A")
    st.title("Question & Answer")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.sidebar.button("Reset conversation"):
        st.session_state.messages = []
        st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question")
    if not question:
        return

    try:
        answer = OpenAIService().generate_answer(
            build_request_messages(st.session_state.messages, question)
        )
    except OpenAIServiceError as exc:
        st.error(str(exc))
        return

    st.session_state.messages.extend(
        [
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ]
    )
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        st.markdown(answer)


if __name__ == "__main__":
    main()

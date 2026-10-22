# Question Answering App

## Setup

Activate the project's virtual environment and install dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set `OPENAI_API_KEY`. The model and response
generation settings can also be configured with `OPENAI_MODEL`,
`OPENAI_TEMPERATURE`, and `OPENAI_MAX_OUTPUT_TOKENS`.

The OpenAI Responses API is accessed through `app.services.openai_service`.
UI code should call this service rather than making OpenAI API requests directly.

Run the Streamlit app from this directory with:

```powershell
streamlit run app/main.py
```

Conversation history is kept in the Streamlit session and can be cleared with
the **Reset conversation** button.

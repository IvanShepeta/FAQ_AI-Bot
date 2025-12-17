# FAQ AI-Bot for Microsoft Azure

Simple FastAPI-based AI assistant that answers questions about Microsoft Azure using an LLM (Gemini), a local FAQ JSON knowledge base, and a list of official Azure links.

## 🚀 Architecture

- **Client Layer**  
  - HTTP API (`/agent/ask`) built with FastAPI.
- **Application Layer**  
  - `app/routers/agent.py` – API router that validates requests and returns answers from the AI service.
  - `app/gemini_client.py` – AI service that loads FAQ + links, builds the prompt and calls Gemini.
  - Logging middleware in `app/main.py` that logs all HTTP requests.
- **Data Layer**  
  - `data/faq_azure.json` – local FAQ knowledge base about Azure.
  - `data/links_azure.json` – list of useful Azure documentation links.
  - External AI API (Gemini model), configured via environment variables.

## ⚙️ Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

Install dependencies:
```shell
pip install -r requirements.txt
```

## Configuration

AI key and other settings are stored in environment variables (`.env`):
```shell
GEMINI_API_KEY=your_gemini_api_key_here
```
Google Gemini API Key ([Get one here](https://ai.google.dev/))

## 📡 Running the API

From the project root:
```shell
uvicorn app.main:app --reload
```

The API will be available at:

- Swagger UI: `http://localhost:8000/docs`
- Root health check: `GET /` → `{"Hello": "World"}`

## Asking a Question

Endpoint: `POST /agent/ask`

## 🤖 Agent

- If the question matches the FAQ, the model uses the FAQ content as the main source.
- Otherwise, the model uses general Azure knowledge and the provided links and may explicitly say that the question is not in the FAQ database.

## Error Handling & Security

- Empty questions return `400 Bad Request` with message `"Question is required"`.
- Failures in the AI service are returned as `502` with a generic `"AI agent error"` message.
- API keys are taken from environment settings, not hard-coded in the repository.



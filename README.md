# AI-First CRM: Log HCP Interaction

This is a small CRM screen where a sales rep logs a meeting with a healthcare professional (HCP), either with a form or by chatting. The backend can use an LLM to write a summary, sentiment and follow-up action for the notes.

## What it does

- Form to log an interaction (HCP name, specialty, type, channel, notes)
- Chat box that talks to a LangGraph agent with five tools: log interaction, edit interaction, suggest next action, draft a follow-up email, and a compliance check on the notes
- List and edit saved interactions
- If no Groq key is set, the app still runs and uses simple placeholder text instead of the LLM

## Tech used

Python, FastAPI, SQLAlchemy, SQLite by default (Postgres through `DATABASE_URL`), LangGraph, LangChain Groq, React, Redux, Vite

## How to run

Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Optional settings: `GROQ_API_KEY`, `GROQ_MODEL`, `DATABASE_URL`, `VITE_API_URL`.

Endpoints: `GET /api/health`, `POST` and `GET /api/interactions`, `GET` and `PUT /api/interactions/{id}`, `POST /api/agent/chat`.

## What I would improve

- Only one test exists (the health check)
- The LLM reply is not parsed as JSON, so the sentiment is a rough guess
- CORS allows every origin, which is fine for local use only

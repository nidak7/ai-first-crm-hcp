# AI-First CRM HCP Module – Log Interaction Screen

This repository contains a full-stack implementation for **Task 1** and support material for **Task 2**.

## What is built

- **Frontend:** React + Redux (Vite) with Google **Inter** font.
- **Backend:** FastAPI + SQLAlchemy.
- **AI Agent:** LangGraph + Groq model integration (`gemma2-9b-it`) with fallback mode when key is not configured.
- **Database:** SQL via SQLAlchemy (SQLite default for local run; can be switched to Postgres/MySQL).

---

## 1) Core Feature: Log Interaction Screen

The screen supports two modes:

1. **Structured Form**
   - Field rep enters HCP name, specialty, interaction type, channel, and notes.
   - Backend uses AI service to generate summary, sentiment, and follow-up action.

2. **Conversational Chat**
   - Rep logs or edits interactions using natural language.
   - LangGraph agent can call tools to perform CRM actions.

---

## 2) LangGraph Agent Role

The agent acts as an **HCP CRM copilot** that interprets user intent and executes operational tools. It reduces field rep admin effort and keeps records analysis-ready.

### Implemented Tools (5)

1. **Log Interaction Tool** ✅
   - Captures HCP name + free-text notes.
   - Uses LLM summarization helper and saves interaction to DB.

2. **Edit Interaction Tool** ✅
   - Updates an existing interaction by interaction ID.
   - Re-runs summary/sentiment/follow-up generation.

3. **Suggest Next Best Action Tool**
   - Reads recent HCP history.
   - Recommends next sales/medical engagement step.

4. **Generate Follow-up Email Tool**
   - Generates a compliant follow-up draft for HCP communication.

5. **Compliance Check Tool**
   - Flags risky terms (off-label, inducement style words, etc.) in notes.

---

## 3) Project Structure

```text
backend/
  app/
    api/routes.py
    core/config.py
    db/
    models/interaction.py
    schemas/interaction.py
    services/
  tests/
frontend/
  src/
    app/store.js
    components/
    features/
docs/
  qms-module-explainer.md
```

---

## 4) Local Setup

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Environment variables (optional):

```bash
export GROQ_API_KEY="your_groq_key"
export GROQ_MODEL="gemma2-9b-it"
export DATABASE_URL="postgresql+psycopg2://user:pass@localhost:5432/aifirstcrm"
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Set frontend API URL if needed:

```bash
export VITE_API_URL="http://localhost:8000/api"
```

---

## 5) API Endpoints

- `GET /api/health`
- `POST /api/interactions`
- `PUT /api/interactions/{id}`
- `GET /api/interactions`
- `GET /api/interactions/{id}`
- `POST /api/agent/chat`

---

## 6) Notes

- The app defaults to SQLite for quick run; switch to Postgres/MySQL by changing `DATABASE_URL`.
- If Groq key is missing, chat endpoint falls back with guidance text so app remains runnable.

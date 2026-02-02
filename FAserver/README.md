# FastAPI server
Service to create a tool for working in English to memorize words and phrases

## Launching the service
bush:

uvicorn app.main:app --reload 

Open:

http://127.0.0.1:8000/docs

## Tests

bash:

pytest -v

## Architecture

```mermaid
┌──────────────┐        HTTP / async
│   Frontend   │ ─────────────────────┐
└──────────────┘                      │
                                      ▼
┌──────────────────────────┐     ┌──────────────────────────┐
│  Core API (FastAPI)      │     │   ML Service (FastAPI)   │
│                          │     │                          │
│  Auth, Users             │     │  Text analysis           │
│  Words                   │     │  CEFR classification     │
│  Progress                │◄───►│  Spaced repetition       │
│  Exams                   │     │  Difficulty prediction   │
│                          │     │  Recommendation engine   │
└──────────────────────────┘     └──────────────────────────┘
        │                                   │
        ▼                                   ▼
┌──────────────┐                   ┌──────────────┐
│ PostgreSQL   │                   │  Model Store │
│ (Business)   │                   │  (joblib)    │
└──────────────┘                   └──────────────┘
```

# AI-Powered Digital Risk Protection Platform — Unified Backend

Single FastAPI process replacing the previous M1 + M2 + M3 multi-service architecture.

## Quick Start

```bash
python run.py
```

or

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Environment

Copy `.env.example` to `.env` and adjust values.

## What's Inside

- Brand Registry (M1) — `/api/brands`
- Social Monitoring (M2) — `/api/scan`, `/api/threats`, `/api/candidates`
- App Monitoring (M3) — `/api/app-monitoring/brands`, `/api/apps`, `/api/scans`, `/api/detection`

## Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

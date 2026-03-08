# Backend

LangGraph-based research and moderation service for the UV LED Knowledge Platform.

## Setup
1. Copy `.env.example` to `.env` and fill in values.
2. Apply Supabase schema from `backend/db/schema.sql`.
3. Install dependencies (using uv):
   - `uv sync`

## Run Once
```
python backend/scripts/run_once.py
```

## Run Scheduler
```
python backend/scripts/run_research_loop.py
```

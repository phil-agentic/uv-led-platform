# UV LED Knowledge Platform

Monorepo scaffold for an autonomous UV LED research platform.

## Structure
- `backend/` Python LangGraph service and research loop
- `frontend/` Next.js dashboard (App Router + TypeScript)

## Quick Start
1. Copy `.env.example` to `.env` and fill in values.
2. Apply Supabase schema in `backend/db/schema.sql`.
3. Backend:
   - Install deps with `uv sync`
   - Run once: `python backend/scripts/run_once.py`
   - Run loop: `python backend/scripts/run_research_loop.py`
4. Frontend:
   - Install deps with `npm install`
   - Run dev: `npm run dev`

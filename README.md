# Labor Platform Workspace

Labor learning platform with frontend-backend separation.

```text
labor-platform-main/
|-- frontend/   # Vue 3 + Vite
|-- backend/    # FastAPI + SQLAlchemy + Alembic + MySQL
`-- archive/    # historical code
```

## Quick Start

### 1) Start Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env
python -m alembic upgrade head
python -m app.db.seed
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend docs:
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### 2) Start Frontend

```powershell
cd frontend
npm install
npm run dev
```

Default frontend API base URL:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## Current Status

- Auth, basic lists, quiz submit, and growth display are working.
- MySQL migration and seed are working.
- Some routes still read from `backend/app/data/mock_db.py` and need ORM migration.

## Handoff

For unfinished items and task breakdown:
- `HANDOFF_UNFINISHED_WORK.md`

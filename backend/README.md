# FastAPI Backend

Tech stack: FastAPI + SQLAlchemy + Alembic + MySQL.

## Structure

```text
backend/
|-- app/
|   |-- api/routes/      # route layer
|   |-- core/            # config, auth, dependencies
|   |-- db/              # session, seed
|   |-- models/          # ORM models
|   |-- repositories/    # data access
|   `-- schemas/         # Pydantic schemas
|-- alembic/
|   `-- versions/
|-- alembic.ini
|-- requirements.txt
`-- README.md
```

## Local Run (Windows)

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

After startup:
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Minimal Env

```env
APP_NAME=Labor Platform FastAPI
APP_ENV=development
HOST=127.0.0.1
PORT=8000
JWT_SECRET=replace-with-a-long-secret
JWT_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:5173
DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/labor_platform?charset=utf8mb4
DB_ECHO=false
```

## DB Initialization

1) Create database:

```sql
CREATE DATABASE IF NOT EXISTS labor_platform
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

2) Run migration:

```powershell
python -m alembic upgrade head
```

3) Run seed:

```powershell
python -m app.db.seed
```

Default users:
- `student / 123456`
- `admin / 123456`

## Alembic Commands

Create migration:

```powershell
python -m alembic revision --autogenerate -m "message"
```

Upgrade:

```powershell
python -m alembic upgrade head
```

Downgrade one step:

```powershell
python -m alembic downgrade -1
```

## Notes

- Auth and basic user profile flow already use DB.
- Some business routes still use `app/data/mock_db.py`.
- Task attachments currently support metadata submit only; real file upload API is pending.

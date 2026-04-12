# FastAPI Backend

当前后端已经分成两层：

- 业务接口层：`app/api/routes/*`
- 数据层骨架：`app/db/*`、`app/models/*`、`alembic/*`

目前接口仍然默认读取 `app/data/mock_db.py`，这样前端可以继续联调；数据库骨架已经搭好，下一步可以逐个接口替换成真实查询。

## 1. 开发启动

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

文档地址：

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 2. 数据库配置

`.env` 里至少要有：

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5432/labor_platform
DB_ECHO=false
JWT_SECRET=replace-with-a-long-secret
CORS_ORIGINS=http://localhost:5173
```

推荐数据库：

- `PostgreSQL`

视频文件不要直接存数据库，数据库里只存元数据和 URL。

## 3. 现在已经有的数据库骨架

```text
backend/
├─ app/
│  ├─ api/
│  ├─ core/
│  ├─ data/
│  ├─ db/
│  │  ├─ base.py
│  │  ├─ session.py
│  │  └─ __init__.py
│  ├─ models/
│  │  ├─ user.py
│  │  ├─ tutorial.py
│  │  ├─ task.py
│  │  ├─ quiz.py
│  │  ├─ growth.py
│  │  └─ __init__.py
│  └─ schemas/
├─ alembic/
│  ├─ env.py
│  ├─ script.py.mako
│  └─ versions/
├─ alembic.ini
├─ requirements.txt
└─ README.md
```

## 4. 第一版模型范围

已经建好的核心模型：

- `User`
- `Tutorial`
- `TutorialChapter`
- `TutorialCollection`
- `TutorialChapterProgress`
- `Task`
- `TaskSubmission`
- `TaskSubmissionAttachment`
- `Quiz`
- `QuizQuestion`
- `QuizOption`
- `QuizRecord`
- `QuizAnswer`
- `PointRecord`
- `Badge`
- `UserBadge`

其中视频相关字段已经预留在 `TutorialChapter`：

- `video_url`
- `video_storage_key`
- `cover_image`
- `duration_seconds`

## 5. Alembic 使用方式

第一次生成迁移：

```bash
alembic revision --autogenerate -m "init tables"
```

执行迁移：

```bash
alembic upgrade head
```

执行种子数据：

```bash
python -m app.db.seed
```

默认会创建：

- `student / 123456`
- `admin / 123456`

回退一步：

```bash
alembic downgrade -1
```

## 6. 建议的迁移顺序

建议不要一口气把所有接口都从 mock 改掉，而是按这个顺序替换：

1. `auth` / `user profile`
2. `tutorials`
3. `tasks` / `task submissions`
4. `quizzes` / `quiz records`
5. `growth`
6. `admin`

## 7. 部署前还要补的东西

- Alembic 初始迁移文件
- 数据库种子数据
- 文件上传接口
- 对象存储或 MinIO
- 生产环境 Nginx / HTTPS
- 日志和备份

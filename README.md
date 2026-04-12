# Labor Platform Workspace

这个仓库已经整理为前后端分离结构：

```text
labor-platform-main/
├─ frontend/   # Vue 3 + Vite
├─ backend/    # FastAPI
└─ archive/    # 历史归档
```

## 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端默认读取：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## 后端启动

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 当前状态

- 前端核心页面已经接上 FastAPI
- 后端当前仍然保留 mock 数据，方便继续联调
- 数据库骨架、ORM 模型、Alembic 已经搭好

## 下一步推荐

1. 创建 PostgreSQL 数据库
2. 配置 `backend/.env`
3. 执行 Alembic 初始迁移
4. 把 `mock_db.py` 中的接口逐步替换成真实数据库查询

数据库初始化后建议再执行：

```bash
cd backend
python -m app.db.seed
```

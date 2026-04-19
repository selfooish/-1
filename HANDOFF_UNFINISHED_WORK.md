# Labor Platform 未完成事项交接文档

更新时间：2026-04-19  
适用分支：`feature/backend-fastapi-db`

## 1. 当前状态（已完成）

- 后端已切换到 **MySQL**，迁移与种子可执行。
- 本地推荐运行方式已切换到 **`backend/.venv` 虚拟环境**。
- `alembic` 初始化迁移已做 MySQL 兼容修复（移除 `TEXT` 默认值）。
- 任务提交 422（附件 `size` 字段）已修复：前后端都做了兼容处理。
- 登录、测验得分、成长积分展示已可用（目前部分仍基于 mock 数据）。

## 2. 关键结论（给接手同学）

项目目前是“**数据库底座可用，但业务 API 仍大量读取 `mock_db`**”的状态。  
上线前最核心工作是：把 API 从 `app/data/mock_db.py` 迁移到 ORM + MySQL。

---

## 3. 未完成工作总览（按优先级）

## P0（必须优先完成）

### 3.1 任务模块改为真实数据库读写

现状：`tasks` 路由使用内存 mock 列表，重启后提交记录会丢失。  
主要文件：
- `backend/app/api/routes/tasks.py`
- `backend/app/models/task.py`
- `backend/app/schemas/task.py`
- `backend/app/data/mock_db.py`（待淘汰依赖）

需要完成：
- `GET /tasks` 从 `Task` 表分页查询。
- `GET /tasks/my` 按当前用户联表查询提交状态、提交次数。
- `GET /tasks/{id}` 返回任务详情+当前用户状态。
- `POST /tasks/{id}/submit` 写入 `TaskSubmission` 和 `TaskSubmissionAttachment`。
- 校验 `max_submits`、任务存在性、用户权限。

验收标准：
- 提交任务后重启服务，数据仍存在。
- 管理员接口能看到待审核提交（不是 mock）。
- 前端“我的任务”状态与数据库一致。

### 3.2 管理后台任务审核改为真实数据库

现状：`admin` 路由仍使用 mock，审核结果只是内存修改。  
主要文件：
- `backend/app/api/routes/admin.py`
- `backend/app/models/task.py`
- `backend/app/models/growth.py`

需要完成：
- `/admin/stats` 改为数据库聚合。
- `/admin/tasks/submissions/pending` 查真实待审核提交。
- `/admin/tasks/submissions/{id}/approve` 更新提交状态、发放积分、写入积分记录（事务保证一致性）。

验收标准：
- 审核后用户积分变化持久化。
- 重启后审核结果不丢失。

### 3.3 教程模块改为真实数据库（含收藏/章节完成）

现状：教程列表、详情、收藏、章节完成都依赖 mock。  
主要文件：
- `backend/app/api/routes/tutorials.py`
- `backend/app/models/tutorial.py`

需要完成：
- 教程列表/详情从表查询。
- 收藏关系落库到 `tutorial_collections`。
- 章节完成落库到 `tutorial_chapter_progress`。

验收标准：
- 收藏和章节完成状态跨重启保持。
- 同一用户同一教程不重复收藏（唯一约束生效）。

### 3.4 测验模块改为真实数据库（题库、提交、记录）

现状：题目、提交、成绩均基于 mock。  
主要文件：
- `backend/app/api/routes/quizzes.py`
- `backend/app/models/quiz.py`

需要完成：
- 题库查询使用 `Quiz/QuizQuestion/QuizOption`。
- 提交后写 `QuizRecord/QuizAnswer`。
- `/quiz-records/my` 从表查询历史。

验收标准：
- 提交记录与分数持久化。
- 历史记录与题目明细可追溯。

### 3.5 成长模块改为真实数据库

现状：积分记录、徽章、成长曲线来自 mock。  
主要文件：
- `backend/app/api/routes/growth.py`
- `backend/app/models/growth.py`

需要完成：
- `points/records` 从 `PointRecord` 按用户查询。
- `badges/my` 使用 `UserBadge + Badge`。
- `growth` 由真实记录聚合最近 N 天数据。

验收标准：
- 用户做任务/测验后，成长页数据能反映真实变化。

---

## P1（重要但可并行）

### 3.6 真实附件上传（当前仅“元数据提交”）

现状：
- 前端提交的是 `local-upload://...` 占位 URL。
- 后端未提供真正文件上传接口。

建议实现：
- 新增上传 API（如 `POST /files/upload`）。
- 存储方案：本地磁盘（开发）+ MinIO/S3（生产）。
- 任务提交引用真实可访问 URL（或对象 key + CDN URL）。

主要文件：
- `frontend/src/views/task/TaskSubmitView.vue`
- `backend/app/api/routes`（新增文件路由）
- `backend/app/models/task.py`（字段已可承载 URL/key）

验收标准：
- 前端上传真实文件后可在任务详情打开附件。
- 文件可控（大小、类型白名单、鉴权策略）。

### 3.7 教程视频播放能力

现状：`videoUrl` 多为占位/空，页面可展示但不具备完整视频业务链路。  
需要完成：
- 管理端上传或配置视频 URL。
- 教程章节返回真实可播放地址。
- （可选）鉴权、防盗链、转码策略。

---

## P2（收尾质量）

### 3.8 错误处理与参数校验统一

问题：
- 多处 `next(...)` 直接取值，未找到会抛 500。
- 建议统一改为 404/400 的 `HTTPException`。

涉及文件：
- `backend/app/api/routes/*.py` 多处

### 3.9 自动化测试与回归清单

建议至少补：
- 认证流程（注册/登录/鉴权）。
- 任务提交与审核流程。
- 测验提交计分流程。
- 教程收藏/完成章节流程。

### 3.10 文档统一（MySQL + .venv）

需要同步检查：
- 根目录 `README.md`
- `backend/README.md`
- `.env.example`

目标：新同学按文档 10 分钟内可跑通。

---

## 4. 已知技术注意事项

- 当前已固定依赖：`bcrypt==4.0.1`（避免与 `passlib` 兼容问题）。
- MySQL 下不允许 `TEXT/JSON/BLOB` 默认值，新增迁移需避免类似写法。
- 当前数据库 URL 为 `mysql+pymysql://...`，不要再回退 `postgresql+psycopg`。
- 使用 `.venv` 运行，避免全局 Python 污染依赖。

---

## 5. 建议分工（3人并行）

1. A 同学：任务 + 管理审核全链路（3.1 + 3.2）  
2. B 同学：教程 + 视频（3.3 + 3.7）  
3. C 同学：测验 + 成长 + 测试（3.4 + 3.5 + 3.9）

---

## 6. 最小交付定义（DoD）

满足以下即认为“数据库改造一期完成”：

- `tutorials/tasks/quizzes/growth/admin` 路由不再依赖 `app/data/mock_db.py`。
- 前端主要页面刷新/重启后数据不丢失。
- 任务提交流程可上传真实附件或明确接入了稳定上传服务。
- 验收清单通过：登录、教程、任务提交、任务审核、测验、成长积分。


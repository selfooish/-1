# FastAPI Backend

褰撳墠鍚庣宸茬粡鍒嗘垚涓ゅ眰锛?
- 涓氬姟鎺ュ彛灞傦細`app/api/routes/*`
- 鏁版嵁灞傞鏋讹細`app/db/*`銆乣app/models/*`銆乣alembic/*`

鐩墠鎺ュ彛浠嶇劧榛樿璇诲彇 `app/data/mock_db.py`锛岃繖鏍峰墠绔彲浠ョ户缁仈璋冿紱鏁版嵁搴撻鏋跺凡缁忔惌濂斤紝涓嬩竴姝ュ彲浠ラ€愪釜鎺ュ彛鏇挎崲鎴愮湡瀹炴煡璇€?
## 1. 寮€鍙戝惎鍔?
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

鏂囨。鍦板潃锛?
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 2. 鏁版嵁搴撻厤缃?
`.env` 閲岃嚦灏戣鏈夛細

```env
DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/labor_platform?charset=utf8mb4
DB_ECHO=false
JWT_SECRET=replace-with-a-long-secret
CORS_ORIGINS=http://localhost:5173
```

鎺ㄨ崘鏁版嵁搴擄細

- `MySQL`

瑙嗛鏂囦欢涓嶈鐩存帴瀛樻暟鎹簱锛屾暟鎹簱閲屽彧瀛樺厓鏁版嵁鍜?URL銆?
## 3. 鐜板湪宸茬粡鏈夌殑鏁版嵁搴撻鏋?
```text
backend/
鈹溾攢 app/
鈹? 鈹溾攢 api/
鈹? 鈹溾攢 core/
鈹? 鈹溾攢 data/
鈹? 鈹溾攢 db/
鈹? 鈹? 鈹溾攢 base.py
鈹? 鈹? 鈹溾攢 session.py
鈹? 鈹? 鈹斺攢 __init__.py
鈹? 鈹溾攢 models/
鈹? 鈹? 鈹溾攢 user.py
鈹? 鈹? 鈹溾攢 tutorial.py
鈹? 鈹? 鈹溾攢 task.py
鈹? 鈹? 鈹溾攢 quiz.py
鈹? 鈹? 鈹溾攢 growth.py
鈹? 鈹? 鈹斺攢 __init__.py
鈹? 鈹斺攢 schemas/
鈹溾攢 alembic/
鈹? 鈹溾攢 env.py
鈹? 鈹溾攢 script.py.mako
鈹? 鈹斺攢 versions/
鈹溾攢 alembic.ini
鈹溾攢 requirements.txt
鈹斺攢 README.md
```

## 4. 绗竴鐗堟ā鍨嬭寖鍥?
宸茬粡寤哄ソ鐨勬牳蹇冩ā鍨嬶細

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

鍏朵腑瑙嗛鐩稿叧瀛楁宸茬粡棰勭暀鍦?`TutorialChapter`锛?
- `video_url`
- `video_storage_key`
- `cover_image`
- `duration_seconds`

## 5. Alembic 浣跨敤鏂瑰紡

绗竴娆＄敓鎴愯縼绉伙細

```bash
alembic revision --autogenerate -m "init tables"
```

鎵ц杩佺Щ锛?
```bash
alembic upgrade head
```

鎵ц绉嶅瓙鏁版嵁锛?
```bash
python -m app.db.seed
```

榛樿浼氬垱寤猴細

- `student / 123456`
- `admin / 123456`

鍥為€€涓€姝ワ細

```bash
alembic downgrade -1
```

## 6. 寤鸿鐨勮縼绉婚『搴?
寤鸿涓嶈涓€鍙ｆ皵鎶婃墍鏈夋帴鍙ｉ兘浠?mock 鏀规帀锛岃€屾槸鎸夎繖涓『搴忔浛鎹細

1. `auth` / `user profile`
2. `tutorials`
3. `tasks` / `task submissions`
4. `quizzes` / `quiz records`
5. `growth`
6. `admin`

## 7. 閮ㄧ讲鍓嶈繕瑕佽ˉ鐨勪笢瑗?
- Alembic 鍒濆杩佺Щ鏂囦欢
- 鏁版嵁搴撶瀛愭暟鎹?- 鏂囦欢涓婁紶鎺ュ彛
- 瀵硅薄瀛樺偍鎴?MinIO
- 鐢熶骇鐜 Nginx / HTTPS
- 鏃ュ織鍜屽浠?

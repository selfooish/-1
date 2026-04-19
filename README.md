# Labor Platform Workspace

杩欎釜浠撳簱宸茬粡鏁寸悊涓哄墠鍚庣鍒嗙缁撴瀯锛?
```text
labor-platform-main/
鈹溾攢 frontend/   # Vue 3 + Vite
鈹溾攢 backend/    # FastAPI
鈹斺攢 archive/    # 鍘嗗彶褰掓。
```

## 鍓嶇鍚姩

```bash
cd frontend
npm install
npm run dev
```

鍓嶇榛樿璇诲彇锛?
```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## 鍚庣鍚姩

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 褰撳墠鐘舵€?
- 鍓嶇鏍稿績椤甸潰宸茬粡鎺ヤ笂 FastAPI
- 鍚庣褰撳墠浠嶇劧淇濈暀 mock 鏁版嵁锛屾柟渚跨户缁仈璋?- 鏁版嵁搴撻鏋躲€丱RM 妯″瀷銆丄lembic 宸茬粡鎼ソ

## 涓嬩竴姝ユ帹鑽?
1. 鍒涘缓 MySQL 鏁版嵁搴?2. 閰嶇疆 `backend/.env`
3. 鎵ц Alembic 鍒濆杩佺Щ
4. 鎶?`mock_db.py` 涓殑鎺ュ彛閫愭鏇挎崲鎴愮湡瀹炴暟鎹簱鏌ヨ

鏁版嵁搴撳垵濮嬪寲鍚庡缓璁啀鎵ц锛?
```bash
cd backend
python -m app.db.seed
```


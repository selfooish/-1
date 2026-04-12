from __future__ import annotations

from datetime import datetime, timedelta

from app.core.security import hash_password


def to_iso(value: str | datetime) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    return datetime.fromisoformat(value).isoformat()


def calc_level(points: int) -> tuple[int, str]:
    levels = [
        (0, 1, "劳动新手"),
        (100, 2, "劳动学徒"),
        (300, 3, "劳动助手"),
        (600, 4, "劳动能手"),
        (1000, 5, "劳动标兵"),
        (1500, 6, "劳动达人"),
        (2100, 7, "劳动巧匠"),
        (2800, 8, "劳动高手"),
        (3600, 9, "劳动大师"),
        (5000, 10, "劳动传奇"),
    ]
    for min_points, level, title in reversed(levels):
        if points >= min_points:
            return level, title
    return 1, "劳动新手"


users = [
    {
        "id": 1,
        "username": "student",
        "nickname": "小明",
        "password_hash": hash_password("123456"),
        "avatar": "",
        "role": "student",
        "points": 850,
        "email": "xiaoming@example.com",
        "phone": "13800000000",
        "bio": "热爱劳动，喜欢动手实践。",
        "createdAt": to_iso("2025-01-01T08:00:00"),
    },
    {
        "id": 2,
        "username": "admin",
        "nickname": "管理员",
        "password_hash": hash_password("123456"),
        "avatar": "",
        "role": "admin",
        "points": 1800,
        "email": "",
        "phone": "",
        "bio": "",
        "createdAt": to_iso("2025-01-01T08:00:00"),
    },
]

tutorials = [
    {
        "id": 1,
        "title": "电饭煲常见故障与维修",
        "category": "家电维修",
        "coverImage": "https://picsum.photos/seed/tutorial-1/800/450",
        "description": "从拆解到排查，帮助学生理解常见家电维修的安全流程和基本方法。",
        "duration": "2h30m",
        "difficulty": "medium",
        "author": "王老师",
        "authorAvatar": "",
        "viewCount": 2341,
        "collectCount": 156,
        "tags": ["家电维修", "安全第一", "动手实践"],
        "rating": 4.8,
        "reviewCount": 156,
        "createdAt": to_iso("2025-01-10T08:00:00"),
        "updatedAt": to_iso("2025-02-10T08:00:00"),
        "chapters": [
            {"id": 1, "title": "基本结构", "duration": "15:00", "isFree": True, "videoUrl": ""},
            {"id": 2, "title": "常见故障", "duration": "20:00", "isFree": True, "videoUrl": ""},
            {"id": 3, "title": "不通电排查", "duration": "25:00", "isFree": False, "videoUrl": ""},
        ],
    },
    {
        "id": 2,
        "title": "衣柜收纳全攻略",
        "category": "收纳整理",
        "coverImage": "https://picsum.photos/seed/tutorial-2/800/450",
        "description": "理解分类、折叠、分层和长期维护的方法。",
        "duration": "1h15m",
        "difficulty": "easy",
        "author": "李老师",
        "authorAvatar": "",
        "viewCount": 4102,
        "collectCount": 289,
        "tags": ["收纳", "整理", "空间利用"],
        "rating": 4.9,
        "reviewCount": 289,
        "createdAt": to_iso("2025-01-12T08:00:00"),
        "updatedAt": to_iso("2025-02-12T08:00:00"),
        "chapters": [
            {"id": 4, "title": "衣物分类", "duration": "10:00", "isFree": True, "videoUrl": ""},
            {"id": 5, "title": "折叠方法", "duration": "18:00", "isFree": True, "videoUrl": ""},
            {"id": 6, "title": "长期维护", "duration": "12:00", "isFree": False, "videoUrl": ""},
        ],
    },
]

tasks = [
    {
        "id": 1,
        "title": "完成一次电饭煲清洁与维护",
        "description": "记录清洁前后对比和清洁心得。",
        "category": "家电维修",
        "coverImage": "https://picsum.photos/seed/task-1/800/450",
        "points": 50,
        "difficulty": "easy",
        "deadline": to_iso("2026-05-01T00:00:00"),
        "maxSubmits": 1,
        "createdAt": to_iso("2025-01-15T08:00:00"),
    },
    {
        "id": 2,
        "title": "整理衣柜并提交分类记录",
        "description": "按季节和使用频率进行分类整理。",
        "category": "收纳整理",
        "coverImage": "https://picsum.photos/seed/task-2/800/450",
        "points": 40,
        "difficulty": "easy",
        "deadline": to_iso("2026-05-10T00:00:00"),
        "maxSubmits": 1,
        "createdAt": to_iso("2025-01-18T08:00:00"),
    },
]

quizzes = [
    {
        "id": 1,
        "title": "家电维修基础知识测验",
        "description": "检验常见家电故障排查与安全操作知识。",
        "questionCount": 3,
        "timeLimit": 20,
        "passScore": 60,
        "totalScore": 100,
        "category": "家电维修",
        "difficulty": "easy",
        "tags": ["家电维修", "基础"],
        "createdAt": to_iso("2025-01-20T08:00:00"),
    }
]

questions = [
    {
        "id": 1,
        "quizId": 1,
        "type": "single",
        "stem": "电饭煲不通电时，优先检查哪一项？",
        "options": [
            {"label": "A", "text": "加热盘"},
            {"label": "B", "text": "电源线和插头"},
            {"label": "C", "text": "温度传感器"},
            {"label": "D", "text": "控制板"},
        ],
        "answer": "B",
        "explanation": "先检查电源线和插头是否正常，是最基础也最常见的排查步骤。",
        "difficulty": "easy",
        "category": "家电维修",
        "tags": ["基础"],
    },
    {
        "id": 2,
        "quizId": 1,
        "type": "multiple",
        "stem": "以下哪些做法有助于家电清洁安全？",
        "options": [
            {"label": "A", "text": "断电后再拆洗"},
            {"label": "B", "text": "手湿时操作插头"},
            {"label": "C", "text": "等待部件冷却"},
            {"label": "D", "text": "阅读说明书"},
        ],
        "answer": ["A", "C", "D"],
        "explanation": "安全前提包括断电、冷却和按说明操作。",
        "difficulty": "easy",
        "category": "家电维修",
        "tags": ["安全"],
    },
    {
        "id": 3,
        "quizId": 1,
        "type": "judge",
        "stem": "设备刚断电时可以立即清洗内部发热部件。",
        "options": [
            {"label": "T", "text": "正确"},
            {"label": "F", "text": "错误"},
        ],
        "answer": "F",
        "explanation": "需要等待冷却，避免烫伤和损坏设备。",
        "difficulty": "easy",
        "category": "家电维修",
        "tags": ["安全"],
    },
]

collections = {"1:1"}
completed_chapters = {"1:1"}

task_submissions = [
    {
        "id": 1,
        "taskId": 1,
        "userId": 1,
        "content": "我完成了电饭煲清洁，并记录了清洁前后的变化。",
        "attachments": [
            {
                "name": "before-after.jpg",
                "url": "https://picsum.photos/seed/submission-1/600/400",
                "type": "image",
                "size": 102400,
            }
        ],
        "submittedAt": to_iso("2025-02-01T08:00:00"),
        "status": "approved",
        "points": 50,
        "reviewerComment": "记录清晰，步骤完整。",
    }
]

quiz_records = [
    {
        "id": 1,
        "quizId": 1,
        "userId": 1,
        "score": 85,
        "totalScore": 100,
        "correctCount": 2,
        "totalQuestions": 3,
        "timeSpent": 420,
        "submittedAt": to_iso("2025-02-02T08:00:00"),
        "answers": [
            {"questionId": 1, "userAnswer": "B", "isCorrect": True, "score": 35},
            {"questionId": 2, "userAnswer": ["A", "C"], "isCorrect": False, "score": 0},
            {"questionId": 3, "userAnswer": "F", "isCorrect": True, "score": 50},
        ],
    }
]

point_records = [
    {"id": 1, "userId": 1, "type": "tutorial", "action": "完成教程《电饭煲常见故障与维修》", "points": 30, "createdAt": to_iso("2025-02-01T08:00:00")},
    {"id": 2, "userId": 1, "type": "quiz", "action": "完成测验《家电维修基础知识测验》", "points": 50, "createdAt": to_iso("2025-02-02T08:00:00")},
    {"id": 3, "userId": 1, "type": "task", "action": "任务《完成一次电饭煲清洁与维护》审核通过", "points": 80, "createdAt": to_iso("2025-02-03T08:00:00")},
]

badges = [
    {"id": 1, "name": "初学者", "description": "完成第一个教程", "icon": "🌱", "color": "#42b883", "type": "skill", "requirement": "完成1个教程", "unlockedAt": to_iso("2025-02-01T08:00:00"), "progress": 1, "total": 1},
    {"id": 2, "name": "答题达人", "description": "完成10次答题", "icon": "📝", "color": "#3498db", "type": "quiz", "requirement": "完成10次答题", "unlockedAt": None, "progress": 3, "total": 10},
]

growth_days = [
    {
        "date": (datetime.now() - timedelta(days=29 - index)).date().isoformat(),
        "points": (index % 5) * 20,
        "tasksCompleted": 1 if index % 3 == 0 else 0,
        "tutorialsCompleted": 1 if index % 4 == 0 else 0,
        "quizzesTaken": 1 if index % 2 == 0 else 0,
    }
    for index in range(30)
]


def get_user_by_id(user_id: int):
    return next((user for user in users if user["id"] == user_id), None)


def get_user_by_username(username: str):
    return next((user for user in users if user["username"] == username), None)


def public_user(user: dict) -> dict:
    level, title = calc_level(user["points"])
    return {
        "id": user["id"],
        "username": user["username"],
        "nickname": user["nickname"],
        "avatar": user["avatar"],
        "role": user["role"],
        "points": user["points"],
        "level": level,
        "title": title,
        "createdAt": user["createdAt"],
        "email": user.get("email", ""),
        "phone": user.get("phone", ""),
        "bio": user.get("bio", ""),
    }


def tutorial_detail_for_user(tutorial: dict, user_id: int | None = None) -> dict:
    return {
        **tutorial,
        "isCollected": bool(user_id and f"{user_id}:{tutorial['id']}" in collections),
        "isPurchased": True,
        "chapters": [
            {
                **chapter,
                "isCompleted": bool(user_id and f"{user_id}:{chapter['id']}" in completed_chapters),
            }
            for chapter in tutorial["chapters"]
        ],
    }


def tutorial_list_item_for_user(tutorial: dict, user_id: int | None = None) -> dict:
    detail = tutorial_detail_for_user(tutorial, user_id)
    return {
        "id": detail["id"],
        "title": detail["title"],
        "category": detail["category"],
        "coverImage": detail["coverImage"],
        "description": detail["description"],
        "duration": detail["duration"],
        "difficulty": detail["difficulty"],
        "author": detail["author"],
        "viewCount": detail["viewCount"],
        "collectCount": detail["collectCount"],
        "rating": detail["rating"],
        "reviewCount": detail["reviewCount"],
        "isCollected": detail["isCollected"],
    }


def task_detail_for_user(task: dict, user_id: int | None = None) -> dict:
    related = [item for item in task_submissions if item["taskId"] == task["id"] and item["userId"] == user_id]
    latest = related[0] if related else None
    status = "pending"
    review_status = None
    reviewer_comment = None
    attachments = []
    if latest:
        status = "submitted" if latest["status"] == "pending" else "reviewed"
        if latest["status"] == "approved":
            review_status = "excellent" if (latest.get("points") or 0) >= task["points"] else "pass"
        if latest["status"] == "rejected":
            review_status = "fail"
        reviewer_comment = latest.get("reviewerComment")
        attachments = latest.get("attachments", [])
    return {
        **task,
        "status": status,
        "submitCount": len(related),
        "maxSubmits": task["maxSubmits"],
        "attachments": attachments,
        "reviewStatus": review_status,
        "reviewerComment": reviewer_comment,
    }


def quiz_detail_for_user(quiz: dict, user_id: int | None = None) -> dict:
    related = [item for item in quiz_records if item["quizId"] == quiz["id"] and item["userId"] == user_id]
    best_score = max((item["score"] for item in related), default=None)
    return {
        **quiz,
        "attemptCount": len(related),
        "bestScore": best_score,
    }


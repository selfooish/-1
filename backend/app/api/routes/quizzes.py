from datetime import datetime

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user
from app.data.mock_db import questions, quiz_detail_for_user, quiz_records, quizzes
from app.schemas.common import success_response
from app.schemas.quiz import QuizSubmitRequest


router = APIRouter()
record_router = APIRouter()


@router.get("")
def list_quizzes(category: str | None = None, keyword: str = "", page: int = Query(default=1, ge=1)):
    page_size = 20
    filtered = [
        item for item in quizzes if (not category or item["category"] == category) and keyword in item["title"]
    ]
    sliced = filtered[(page - 1) * page_size : page * page_size]
    return success_response(
        {
            "list": [quiz_detail_for_user(item) for item in sliced],
            "total": len(filtered),
            "page": page,
            "pageSize": page_size,
        }
    )


@router.get("/{quiz_id}")
def get_quiz(quiz_id: int):
    quiz = next(item for item in quizzes if item["id"] == quiz_id)
    return success_response(quiz_detail_for_user(quiz))


@router.get("/{quiz_id}/questions")
def get_questions(quiz_id: int):
    return success_response([item for item in questions if item["quizId"] == quiz_id])


@router.post("/{quiz_id}/submit")
def submit_quiz(quiz_id: int, payload: QuizSubmitRequest, user=Depends(get_current_user)):
    quiz = next(item for item in quizzes if item["id"] == quiz_id)
    quiz_questions = [item for item in questions if item["quizId"] == quiz_id]
    score_per_question = max(1, round(quiz["totalScore"] / len(quiz_questions)))

    answers = []
    for question in quiz_questions:
        user_answer = payload.answers.get(str(question["id"]), "")
        is_correct = user_answer == question["answer"]
        answers.append(
            {
                "questionId": question["id"],
                "userAnswer": user_answer,
                "isCorrect": is_correct,
                "score": score_per_question if is_correct else 0,
            }
        )

    record = {
        "id": len(quiz_records) + 1,
        "quizId": quiz_id,
        "userId": user["id"],
        "score": sum(item["score"] for item in answers),
        "totalScore": quiz["totalScore"],
        "correctCount": sum(1 for item in answers if item["isCorrect"]),
        "totalQuestions": len(quiz_questions),
        "timeSpent": 0,
        "submittedAt": datetime.now().isoformat(),
        "answers": answers,
    }
    quiz_records.insert(0, record)

    return success_response(
        {
            **record,
            "quizTitle": quiz["title"],
        },
        "提交成功",
    )


@record_router.get("/my")
def my_quiz_records(user=Depends(get_current_user)):
    result = []
    for record in quiz_records:
        if record["userId"] != user["id"]:
            continue
        quiz = next(item for item in quizzes if item["id"] == record["quizId"])
        result.append({**record, "quizTitle": quiz["title"]})
    return success_response(result)


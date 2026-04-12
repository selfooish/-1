from fastapi import APIRouter, Depends

from app.core.deps import get_current_admin
from app.data.mock_db import point_records, public_user, quiz_records, quizzes, task_submissions, tasks, tutorials, users
from app.schemas.common import success_response


router = APIRouter()


@router.get("/stats")
def admin_stats(admin=Depends(get_current_admin)):
    _ = admin
    return success_response(
        {
            "userCount": len(users),
            "tutorialCount": len(tutorials),
            "quizCount": len(quizzes),
            "pendingTaskSubmissionCount": sum(1 for item in task_submissions if item["status"] == "pending"),
            "quizRecordCount": len(quiz_records),
            "taskCount": len(tasks),
        }
    )


@router.get("/users")
def admin_users(admin=Depends(get_current_admin)):
    _ = admin
    return success_response([public_user(user) for user in users])


@router.get("/tasks/submissions/pending")
def admin_pending_submissions(admin=Depends(get_current_admin)):
    _ = admin
    result = []
    for submission in task_submissions:
        if submission["status"] != "pending":
            continue
        user = next(item for item in users if item["id"] == submission["userId"])
        task = next(item for item in tasks if item["id"] == submission["taskId"])
        result.append({**submission, "user": public_user(user), "task": task})
    return success_response(result)


@router.post("/tasks/submissions/{submission_id}/approve")
def approve_submission(submission_id: int, admin=Depends(get_current_admin)):
    _ = admin
    submission = next(item for item in task_submissions if item["id"] == submission_id)
    if submission["status"] != "pending":
      return success_response(submission, "该提交已经处理过")

    task = next(item for item in tasks if item["id"] == submission["taskId"])
    user = next(item for item in users if item["id"] == submission["userId"])

    submission["status"] = "approved"
    submission["points"] = task["points"]
    submission["reviewerComment"] = "审核通过"

    user["points"] += task["points"]
    point_records.insert(
        0,
        {
            "id": len(point_records) + 1,
            "userId": user["id"],
            "type": "task",
            "action": f"任务《{task['title']}》审核通过",
            "points": task["points"],
            "createdAt": submission["submittedAt"],
        },
    )

    return success_response({**submission, "user": public_user(user), "task": task}, "审核通过")

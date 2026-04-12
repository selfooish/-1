from datetime import datetime

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user
from app.data.mock_db import task_detail_for_user, task_submissions, tasks
from app.schemas.common import success_response
from app.schemas.task import TaskSubmissionCreate


router = APIRouter()


@router.get("")
def list_tasks(category: str | None = None, status: str | None = None, page: int = Query(default=1, ge=1)):
    page_size = 20
    filtered = [item for item in tasks if not category or item["category"] == category]
    sliced = filtered[(page - 1) * page_size : page * page_size]
    result = [task_detail_for_user(item) for item in sliced]
    if status:
        result = [item for item in result if item["status"] == status]
    return success_response({"list": result, "total": len(filtered), "page": page, "pageSize": page_size})


@router.get("/my")
def my_tasks(user=Depends(get_current_user)):
    return success_response([task_detail_for_user(item, user["id"]) for item in tasks])


@router.get("/{task_id}")
def get_task(task_id: int):
    task = next(item for item in tasks if item["id"] == task_id)
    return success_response(task_detail_for_user(task))


@router.post("/{task_id}/submit")
def submit_task(task_id: int, payload: TaskSubmissionCreate, user=Depends(get_current_user)):
    record = {
        "id": len(task_submissions) + 1,
        "taskId": task_id,
        "userId": user["id"],
        "content": payload.content,
        "attachments": [item.model_dump() for item in payload.attachments],
        "submittedAt": datetime.now().isoformat(),
        "status": "pending",
        "points": None,
        "reviewerComment": "",
    }
    task_submissions.insert(0, record)
    return success_response(record, "提交成功")


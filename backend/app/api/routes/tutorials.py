from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user
from app.data.mock_db import collections, completed_chapters, tutorial_detail_for_user, tutorial_list_item_for_user, tutorials
from app.schemas.common import success_response


router = APIRouter()


@router.get("")
def list_tutorials(
    category: str | None = None,
    difficulty: str | None = None,
    keyword: str = "",
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=20, ge=1, le=100),
):
    filtered = [
        item
        for item in tutorials
        if (not category or item["category"] == category)
        and (not difficulty or item["difficulty"] == difficulty)
        and keyword in item["title"]
    ]
    sliced = filtered[(page - 1) * pageSize : page * pageSize]
    return success_response(
        {
            "list": [tutorial_list_item_for_user(item) for item in sliced],
            "total": len(filtered),
            "page": page,
            "pageSize": pageSize,
        }
    )


@router.get("/{tutorial_id}")
def get_tutorial_detail(tutorial_id: int):
    tutorial = next(item for item in tutorials if item["id"] == tutorial_id)
    return success_response(tutorial_detail_for_user(tutorial))


@router.post("/{tutorial_id}/collect")
def collect_tutorial(tutorial_id: int, user=Depends(get_current_user)):
    collections.add(f"{user['id']}:{tutorial_id}")
    return success_response(True, "收藏成功")


@router.delete("/{tutorial_id}/collect")
def uncollect_tutorial(tutorial_id: int, user=Depends(get_current_user)):
    collections.discard(f"{user['id']}:{tutorial_id}")
    return success_response(True, "取消收藏成功")


@router.post("/{tutorial_id}/chapters/{chapter_id}/complete")
def complete_chapter(tutorial_id: int, chapter_id: int, user=Depends(get_current_user)):
    completed_chapters.add(f"{user['id']}:{chapter_id}")
    return success_response({"tutorialId": tutorial_id, "chapterId": chapter_id}, "章节完成已记录")


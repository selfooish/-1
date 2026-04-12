from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_public_user, get_current_user, get_db
from app.repositories.user_repository import get_user_by_id, update_user_profile
from app.schemas.common import success_response
from app.schemas.user import UserProfileUpdate
from app.services.user_mapper import orm_user_to_public_dict


router = APIRouter()


@router.get("/profile")
def get_profile(user=Depends(get_current_public_user)):
    return success_response(user)


@router.put("/profile")
def update_profile(
    payload: UserProfileUpdate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_user = get_user_by_id(db, int(user["id"]))
    if db_user:
        updated_user = update_user_profile(db, db_user, **payload.model_dump(exclude_none=True))
        return success_response(orm_user_to_public_dict(updated_user), "更新成功")

    update_data = payload.model_dump(exclude_none=True)
    user.update(update_data)
    from app.data.mock_db import public_user

    return success_response(public_user(user), "更新成功")

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user
from app.data.mock_db import badges, growth_days, point_records
from app.schemas.common import success_response


router = APIRouter()


@router.get("/points/records")
def get_point_records(user=Depends(get_current_user)):
    return success_response([item for item in point_records if item["userId"] == user["id"]])


@router.get("/badges/my")
def get_my_badges(user=Depends(get_current_user)):
    _ = user
    return success_response(badges)


@router.get("/growth")
def get_growth(days: int = Query(default=30, ge=1, le=365), user=Depends(get_current_user)):
    _ = user
    return success_response(growth_days[-days:])


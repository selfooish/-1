from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import create_user, get_user_by_username
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.common import success_response
from app.services.user_mapper import orm_user_to_public_dict


router = APIRouter()


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_username(db, payload.username)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    token = create_access_token({"user_id": user.id, "role": user.role})
    return success_response({"token": token, "user": orm_user_to_public_dict(user)})


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if get_user_by_username(db, payload.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")

    user = create_user(
        db,
        username=payload.username,
        nickname=payload.nickname,
        password_hash=hash_password(payload.password),
    )
    token = create_access_token({"user_id": user.id, "role": user.role})
    return success_response({"token": token, "user": orm_user_to_public_dict(user)}, "注册成功")

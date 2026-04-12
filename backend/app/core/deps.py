from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.data.mock_db import get_user_by_id as get_mock_user_by_id
from app.data.mock_db import public_user as public_mock_user
from app.db.session import SessionLocal
from app.repositories.user_repository import get_user_by_id as get_db_user_by_id
from app.services.user_mapper import orm_user_to_internal_dict, orm_user_to_public_dict


bearer_scheme = HTTPBearer(auto_error=False)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="未登录")

    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登录状态失效") from exc

    user_id = int(payload["user_id"])

    db = SessionLocal()
    try:
        db_user = get_db_user_by_id(db, user_id)
        if db_user:
            return orm_user_to_internal_dict(db_user)
    finally:
        db.close()

    user = get_mock_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在")

    return user


def get_current_admin(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权限访问")
    return user


def get_current_public_user(user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        db_user = get_db_user_by_id(db, int(user["id"]))
        if db_user:
            return orm_user_to_public_dict(db_user)
    finally:
        db.close()

    return public_mock_user(user)

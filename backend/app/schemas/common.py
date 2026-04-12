from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "ok"
    data: T


def success_response(data, message: str = "ok") -> dict:
    return {"code": 0, "message": message, "data": data}


class PageResult(BaseModel):
    list: list
    total: int
    page: int
    pageSize: int


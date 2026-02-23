from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class Page[T](BaseModel):
    items: list[T]
    total: int
    limit: int
    offset: int
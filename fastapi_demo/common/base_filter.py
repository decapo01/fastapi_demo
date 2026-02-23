from enum import Enum
from typing import TypeVar

from pydantic import BaseModel


S = TypeVar('S', bound=Enum)


class BaseFilter[S](BaseModel):
    sort: S | None = None
    limit: int = 10
    offset: int = 0
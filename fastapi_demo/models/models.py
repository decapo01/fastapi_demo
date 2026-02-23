from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from fastapi_demo.common.base_filter import BaseFilter


class TodoModel(BaseModel):
    id: UUID
    title: str
    completed_date: datetime | None = None


class TodoSort(str, Enum):
    id_asc = "id_asc"
    id_desc = "id_desc"
    title_asc = "title_asc"
    title_desc = "title_desc"
    completed_date_asc = "completed_date_asc"
    completed_date_desc = "completed_date_desc"


class TodoFilter(BaseFilter[TodoSort]):
    id_eq: UUID | None = None
    id_neq: UUID | None = None
    id_in: list[UUID] | None = None
    id_nin: list[UUID] | None = None
    title_eq: str | None = None
    title_neq: str | None = None
    title_in: list[str] | None = None
    title_nin: list[str] | None = None
    title_ilike: str | None = None
    completed_date_eq: datetime | None = None
    completed_date_neq: datetime | None = None
    completed_date_gt: datetime | None = None
    completed_date_gte: datetime | None = None
    completed_date_lt: datetime | None = None
    completed_date_lte: datetime | None = None

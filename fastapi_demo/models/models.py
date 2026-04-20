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


class Author(BaseModel):
    id: UUID
    name: str

class Publisher(BaseModel):
    id: UUID
    name: str

class Book(BaseModel):
    id: UUID
    title: str
    author_id: UUID
    publisher_id: UUID
    published_date: datetime
    pages: int


class AuthorSort(str, Enum):
    id_asc = "id_asc"
    id_desc = "id_desc"
    name_asc = "name_asc"
    name_desc = "name_desc"

class AuthorFilter(BaseFilter[AuthorSort]):
    id_eq: UUID | None = None
    id_neq: UUID | None = None
    id_in: list[UUID] | None = None
    id_nin: list[UUID] | None = None
    name_eq: str | None = None
    name_neq: str | None = None
    name_in: list[str] | None = None
    name_nin: list[str] | None = None
    name_ilike: str | None = None


class PublisherSort(str, Enum):
    id_asc = "id_asc"
    id_desc = "id_desc"
    name_asc = "name_asc"
    name_desc = "name_desc"


class PublisherFilter(BaseFilter[PublisherSort]):
    id_eq: UUID | None = None
    id_neq: UUID | None = None
    id_in: list[UUID] | None = None
    id_nin: list[UUID] | None = None
    name_eq: str | None = None
    name_neq: str | None = None
    name_in: list[str] | None = None
    name_nin: list[str] | None = None
    name_ilike: str | None = None


class BookSort(str, Enum):
    id_asc = "id_asc"
    id_desc = "id_desc"
    title_asc = "title_asc"
    title_desc = "title_desc"
    published_date_asc = "published_date_asc"
    published_date_desc = "published_date_desc"
    pages_asc = "pages_asc"
    pages_desc = "pages_desc"


class BookFilter(BaseFilter[BookSort]):
    id_eq: UUID | None = None
    id_neq: UUID | None = None
    id_in: list[UUID] | None = None
    id_nin: list[UUID] | None = None
    title_eq: str | None = None
    title_neq: str | None = None
    title_in: list[str] | None = None
    title_nin: list[str] | None = None
    title_ilike: str | None = None
    published_date_eq: datetime | None = None
    published_date_gte: datetime | None = None
    published_date_lte: datetime | None = None
    pages_eq: int | None = None
    pages_gte: int | None = None
    pages_lte: int | None = None
    author_id_eq: UUID | None = None
    author_id_neq: UUID | None = None
    author_id_in: list[UUID] | None = None
    author_id_nin: list[UUID] | None = None
    publisher_id_eq: UUID | None = None
    publisher_id_neq: UUID | None = None
    publisher_id_in: list[UUID] | None = None
    publisher_id_nin: list[UUID] | None = None



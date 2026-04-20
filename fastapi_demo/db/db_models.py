from uuid import UUID
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.types import String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from fastapi_demo.common.datetime_utils import utc_now

Base = declarative_base()


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    completed_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    created_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    created_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)


class Publisher(Base):
    __tablename__ = "publishers"

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    created_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)


class Book(Base):
    __tablename__ = "books"

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    author_id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True))
    publisher_id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True))
    published_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    pages: Mapped[int] = mapped_column(Integer)
    created_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
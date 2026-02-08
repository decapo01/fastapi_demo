from uuid import UUID
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
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
    completed_date: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    created_on: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_on: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now)

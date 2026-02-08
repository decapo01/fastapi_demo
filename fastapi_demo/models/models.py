from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TodoModel(BaseModel):
    id: UUID
    title: str
    completed_date: datetime | None = None

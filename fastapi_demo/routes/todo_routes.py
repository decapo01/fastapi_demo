import logging
from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

from fastapi_demo.db.db_models import Todo
from fastapi_demo.db.get_db_session import get_db_session
from fastapi_demo.models.models import TodoModel

logger = logging.getLogger(__name__)

router = APIRouter()


# todo: move to package
def todo_model_from_todo(todo: Todo) -> TodoModel:
    return TodoModel(
        id=todo.id,
        title=todo.title,
        completed_date=todo.completed_date,
    )


@router.get("/{id}")
async def get_todo(id: UUID, db: AsyncSession = Depends(get_db_session)) -> Optional[TodoModel]:
    try:
        logger.info("Getting single todo with id: %s", id)
        query = select(Todo).where(Todo.id == id)
        result = await db.execute(query)
        todo: Optional[Todo] = result.scalar_one_or_none()
        return todo_model_from_todo(todo) if todo is not None else None
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("")
async def get_todos(db: AsyncSession = Depends(get_db_session)) -> list[TodoModel]:
    try:
        logger.info("Getting todos")
        query = select(Todo)
        result = await db.execute(query)
        todos: Sequence[Todo] = result.scalars().all()
        response = [todo_model_from_todo(t) for t in todos]
        return response
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

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

def todo_db_model_from_todo_model(todo_model: TodoModel) -> Todo:
    return Todo(
        id=todo_model.id,
        title=todo_model.title,
        completed_date=todo_model.completed_date,
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


@router.post("")
async def post_todos(todo_model: TodoModel, db: AsyncSession = Depends(get_db_session)) -> TodoModel:
    try:
        logger.info("Creating new todo")
        todo_db_model = todo_db_model_from_todo_model(todo_model)
        db.add(todo_db_model)
        await db.commit()
        await db.refresh(todo_db_model)
        return todo_model
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{id}")
async def post_update_todo(id: UUID, todo_model: TodoModel, db: AsyncSession = Depends(get_db_session)) -> TodoModel:
    try:
        logger.info(f"Updating todo with id: {id}")
        query = select(Todo).filter(Todo.id == id)
        result = await db.execute(query)
        response: Todo | None = result.scalar_one_or_none()
        if response is None:
            msg = f"todo with id: {id} not found"
            logger.error(msg)
            raise HTTPException(status_code=404, detail=msg)
        response.title = todo_model.title
        response.completed_date = todo_model.completed_date
        await db.commit()
        return todo_model
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

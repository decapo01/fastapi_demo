import logging
import re
from typing import Optional, AsyncGenerator
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

from fastapi_demo.common.pagination import Page
from fastapi_demo.db.db_models import Todo
from fastapi_demo.db.get_db_session import get_db_session
from fastapi_demo.models.models import TodoModel, TodoFilter
from fastapi_demo.query_transformers.todo_query_transformers import mk_count_query, mk_fetch_all_query

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


@router.get("/{todo_id}")
async def get_todo(todo_id: UUID, db: AsyncSession = Depends(get_db_session)) -> Optional[TodoModel]:
    try:
        logger.info("Getting single todo with id: %s", todo_id)
        query = select(Todo).where(Todo.id == todo_id)
        result = await db.execute(query)
        todo: Optional[Todo] = result.scalar_one_or_none()
        return todo_model_from_todo(todo) if todo is not None else None
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("")
async def get_todos(todo_filter: TodoFilter, db: AsyncSession = Depends(get_db_session)) -> list[TodoModel]:
    try:
        logger.info("Getting todos")
        todo_models = await fetch_all(db, todo_filter)
        return todo_models
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


@router.post("/page")
async def post_page_todos(todo_filter: TodoFilter, db: AsyncSession = Depends(get_db_session)) -> Page[TodoModel]:
    return await fetch_page(db, todo_filter)


@router.post("/stream")
async def post_stream_todos(todo_filter: TodoFilter, db: AsyncSession = Depends(get_db_session)) -> StreamingResponse:
    return StreamingResponse(stream_todos_json(db, todo_filter), media_type="application/json")


@router.post("/{todo_id}")
async def post_update_todo(todo_id: UUID, todo_model: TodoModel,
                           db: AsyncSession = Depends(get_db_session)) -> TodoModel:
    try:
        logger.info(f"Updating todo with id: {todo_id}")
        query = select(Todo).filter(Todo.id == todo_id)
        result = await db.execute(query)
        response: Todo | None = result.scalar_one_or_none()
        if response is None:
            msg = f"todo with id: {todo_id} not found"
            logger.error(msg)
            raise HTTPException(status_code=404, detail=msg)
        response.title = todo_model.title
        response.completed_date = todo_model.completed_date
        await db.commit()
        return todo_model
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")


async def fetch_all(db: AsyncSession, todo_filter: TodoFilter) -> list[TodoModel]:
    query = mk_fetch_all_query(todo_filter)
    query_result = await db.execute(query)
    items = query_result.scalars().all()
    return [todo_model_from_todo(t) for t in items]


async def fetch_page(db: AsyncSession, todo_filter: TodoFilter) -> Page[TodoModel]:
    query = mk_fetch_all_query(todo_filter)
    query = query.offset(todo_filter.offset).limit(todo_filter.limit)
    query_result = await db.execute(query)
    items = query_result.scalars().all()

    count_query = mk_count_query(todo_filter)
    total_count_result = await db.execute(count_query)
    total = total_count_result.scalar_one()

    todo_models = [todo_model_from_todo(t) for t in items]
    page = Page[TodoModel](items=todo_models, total=total, limit=todo_filter.limit, offset=todo_filter.offset)
    return page


async def stream_todos(db: AsyncSession, todo_filter: TodoFilter) -> AsyncGenerator[TodoModel]:
    query = mk_fetch_all_query(todo_filter)
    async for row in await db.stream(query):
        todo = row[0]
        yield todo_model_from_todo(todo)


async def stream_todos_json(db: AsyncSession, todo_filter: TodoFilter) -> AsyncGenerator[str]:
    yield "["

    first_item = True
    async for todo_model in stream_todos(db, todo_filter):
        if not first_item:
            yield ","
        else:
            first_item = False
        yield todo_model.model_dump_json()

    yield "]"

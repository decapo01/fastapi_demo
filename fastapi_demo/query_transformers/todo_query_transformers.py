from typing import TypeVar

from sqlalchemy.sql.functions import func
from sqlalchemy.sql.selectable import Select

from fastapi_demo.db.db_models import Todo
from fastapi_demo.models.models import TodoFilter, TodoSort

T = TypeVar('T', bound=Todo | int)

def query_from_filter[T](todo_filter: TodoFilter, query: Select[tuple[T]]) -> Select[tuple[T]]:

    if todo_filter.id_eq is not None:
        query = query.filter(Todo.id == todo_filter.id_eq)
    if todo_filter.id_neq is not None:
        query = query.filter(Todo.id != todo_filter.id_neq)
    if todo_filter.id_in is not None:
        query = query.filter(Todo.id.in_(todo_filter.id_in))
    if todo_filter.id_nin is not None:
        query = query.filter(Todo.id.notin_(todo_filter.id_nin))

    if todo_filter.title_eq is not None:
        query = query.filter(Todo.title == todo_filter.title_eq)
    if todo_filter.title_neq is not None:
        query = query.filter(Todo.title != todo_filter.title_neq)
    if todo_filter.title_in is not None:
        query = query.filter(Todo.title.in_(todo_filter.title_in))
    if todo_filter.title_nin is not None:
        query = query.filter(Todo.title.notin_(todo_filter.title_nin))
    if todo_filter.title_ilike is not None:
        query = query.filter(Todo.title.ilike(f"%{todo_filter.title_ilike}%"))

    if todo_filter.completed_date_eq is not None:
        query = query.filter(Todo.completed_date == todo_filter.completed_date_eq)
    if todo_filter.completed_date_neq is not None:
        query = query.filter(Todo.completed_date != todo_filter.completed_date_neq)
    if todo_filter.completed_date_gt is not None:
        query = query.filter(Todo.completed_date > todo_filter.completed_date_gt)
    if todo_filter.completed_date_gte is not None:
        query = query.filter(Todo.completed_date >= todo_filter.completed_date_gte)
    if todo_filter.completed_date_lt is not None:
        query = query.filter(Todo.completed_date < todo_filter.completed_date_lt)
    if todo_filter.completed_date_lte is not None:
        query = query.filter(Todo.completed_date <= todo_filter.completed_date_lte)

    return query


def select_from_filter[T](sort: TodoSort, query: Select[tuple[T]]) -> Select[tuple[T]]:
    match sort:
        case TodoSort.id_asc:
            return query.order_by(Todo.id.asc())
        case TodoSort.id_desc:
            return query.order_by(Todo.id.desc())
        case TodoSort.title_asc:
            return query.order_by(Todo.title.asc())
        case TodoSort.title_desc:
            return query.order_by(Todo.title.desc())
        case TodoSort.completed_date_asc:
            return query.order_by(Todo.completed_date.asc())
        case TodoSort.completed_date_desc:
            return query.order_by(Todo.completed_date.desc())
    return query


def mk_fetch_all_query(todo_filter: TodoFilter) -> Select[tuple[Todo]]:
    base_query: Select[tuple[Todo]] = Select(Todo)
    query = query_from_filter(todo_filter, base_query)
    if todo_filter.sort is not None:
        query = select_from_filter(todo_filter.sort, query)
    return query


def mk_count_query(todo_filter: TodoFilter) -> Select[tuple[int]]:
    count_query: Select[tuple[int]] = Select(func.count(Todo.id))
    count_query = query_from_filter(todo_filter, count_query)
    return count_query

from sqlalchemy import Select

from fastapi_demo.db.db_models import Author
from fastapi_demo.models.models import AuthorFilter, AuthorSort


def author_query_transformers():
    pass

def query_from_filter(filt: AuthorFilter, query: Select[tuple[Author]]) -> Select[tuple[Author]]:
    if filt.id_eq:
        query = query.filter(Author.id == filt.id_eq)
    if filt.id_neq:
        query = query.filter(Author.id != filt.id_neq)
    if filt.id_in:
        query = query.filter(Author.id.in_(filt.id_in))
    if filt.id_nin:
        query = query.filter(Author.id.notin_(filt.id_nin))
    if filt.name_eq:
        query = query.filter(Author.name == filt.name_eq)
    if filt.name_neq:
        query = query.filter(Author.name != filt.name_neq)
    if filt.name_in:
        query = query.filter(Author.name.in_(filt.name_in))
    if filt.name_nin:
        query = query.filter(Author.name.notin_(filt.name_nin))
    return query


def query_from_sort(sort: AuthorSort, query: Select[tuple[Author]]) -> Select[tuple[Author]]:
    match sort:
        case AuthorSort.id_asc:
            return query.order_by(Author.id.asc())
        case AuthorSort.id_desc:
            return query.order_by(Author.id.desc())
        case AuthorSort.name_asc:
            return query.order_by(Author.name.asc())
        case AuthorSort.name_desc:
            return query.order_by(Author.name.desc())
    return query
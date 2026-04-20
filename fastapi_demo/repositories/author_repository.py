from sqlalchemy import Select
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.functions import func

from fastapi_demo.db.db_models import Author
from fastapi_demo.models.models import AuthorFilter, AuthorSort
from fastapi_demo.query_transformers.author_query_transformers import query_from_filter, query_from_sort
from fastapi_demo.repositories.base_repository import BaseRepository


class AuthorRepository(BaseRepository[Author, AuthorFilter, AuthorSort]):

    def select_query(self) -> Select[tuple[Author]]:
        return select(Author)

    def count_query(self) -> Select[tuple[int]]:
        return select(func.count(Author.id))

    def apply_filter(self, query: Select[tuple[Author | int]], filter: AuthorFilter) -> Select[tuple[AuthorFilter | int]]:
        return query_from_filter(filter, query)

    def apply_sort(self, query: Select[tuple[Author]], sort: AuthorSort) -> Select[tuple[Author]]:
        return query_from_sort(sort, query)

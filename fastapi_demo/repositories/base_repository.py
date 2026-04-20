from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable, Optional, TypeVar, Any, cast, AsyncGenerator

from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')
S = TypeVar('S', bound=Enum)
F = TypeVar('F', bound=BaseModel)

class Page[T](BaseModel):
    items: list[T]
    total: int
    limit: int
    offset: int

class BaseReadRepository[T, F, S](ABC):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abstractmethod
    def select_query(self) -> Select[tuple[T]]:
        pass

    @abstractmethod
    def count_query(self) -> Select[tuple[int]]:
        pass

    @abstractmethod
    def apply_filter(self, query: Select[tuple[T | int]], filter: F) -> Select[tuple[T | int]]:
        pass

    @abstractmethod
    def apply_sort(self, query: Select[tuple[T]], sort: S) -> Select[tuple[T]]:
        pass

    async def find(self, fil: F) -> Optional[T]:
        query = self.select_query()
        query = self.apply_filter(query, fil)
        res = await self.session.execute(query)
        items = res.scalar_one_or_none()
        return items

    async def find_all(self, fil: F, sort: Optional[None] = None) -> list[T]:
        query = self.select_query()
        query = self.apply_filter(query, fil)
        if sort is not None:
            query = self.apply_sort(query, sort)
        res = await self.session.execute(query)
        items = res.scalars().all()
        return list(items)

    async def stream(self, fil: F, sort: Optional[None] = None) -> AsyncGenerator[T]:
        query = self.select_query()
        query = self.apply_filter(query, fil)
        if sort is not None:
            query = self.apply_sort(query, sort)
        async for row in await self.session.stream(query):
            yield row[0]

    async def find_page(self, fil: F, sort: Optional[None] = None, limit: int = 10, offset: int = 0) -> Page[T]:
        query = self.select_query()
        query = cast(Select[tuple[T]], self.apply_filter(query, fil))
        if sort is not None:
            query = self.apply_sort(query, sort)
        query = query.limit(limit).offset(offset)

        count_query = self.count_query()
        count_query = cast(Select[tuple[int]], self.apply_filter(count_query, fil))

        count_res = await self.session.execute(count_query)
        res = await self.session.execute(query)

        total = count_res.scalar_one()
        items = res.scalars().all()
        return Page(items=list(items), total=total, limit=limit, offset=offset)


class BaseRepository[T, F, S](BaseReadRepository[T, F, S], ABC):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(session)

    def insert(self, item: T) -> None:
        self.session.add(item)

    def insert_all(self, items: Iterable[T]) -> None:
        self.session.add_all(items)

    async def update(self, item: T) -> None:
        await self.session.merge(item)

    async def update_all(self, items: Iterable[T]) -> None:
        self.session.add_all(items)

    async def delete(self, item: T) -> None:
        await self.session.delete(item)



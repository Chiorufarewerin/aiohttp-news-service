import os
import aiofiles
import ujson
from abc import ABCMeta, abstractmethod

from settings import DATA_PATH


class Repository(metaclass=ABCMeta):
    @abstractmethod
    async def fetch_news(self) -> list[dict]:
        ...

    @abstractmethod
    async def fetch_comments(self) -> list[dict]:
        ...


class JSONRepository(Repository):
    async def _read_json(self, filename: str) -> dict:
        path = os.path.join(DATA_PATH, filename)

        async with aiofiles.open(path, mode='rb') as f:
            contents = await f.read()

        return ujson.loads(contents)

    async def fetch_news(self) -> list[dict]:
        data = await self._read_json('news.json')
        return data['news']

    async def fetch_comments(self) -> list[dict]:
        data = await self._read_json('comments.json')
        return data['comments']

from typing import Optional

from .utils import parse_datetime, current_datetime
from .repository import Repository, JSONRepository
from .models import News, Comment


class Controller:
    repository: Repository

    def __init__(self):
        self.repository = JSONRepository()

    async def _perform_news_with_comments(self) -> dict[int, News]:
        raw_news_list = await self.repository.fetch_news()
        raw_comments = await self.repository.fetch_comments()

        news_data = {}
        for raw_news in raw_news_list:
            news_data[raw_news['id']] = News(
                id=raw_news['id'],
                title=raw_news['title'],
                date=parse_datetime(raw_news['date']),
                body=raw_news['body'],
                deleted=raw_news['deleted'],
                comments=[],
            )

        for raw_comment in raw_comments:
            news_data[raw_comment['news_id']].comments.append(
                Comment(
                    id=raw_comment['id'],
                    news_id=raw_comment['news_id'],
                    title=raw_comment['title'],
                    date=parse_datetime(raw_comment['date']),
                    comment=raw_comment['comment'],
                ),
            )

        return news_data

    async def fetch_news_list(self) -> list[News]:
        news_data = await self._perform_news_with_comments()
        now = current_datetime()

        news_list = [
            news for news in news_data.values()
            if not news.deleted and news.date <= now
        ]

        return sorted(news_list, key=lambda x: x.date)

    async def get_news(self, news_id: int, /) -> Optional[News]:
        news_data = await self._perform_news_with_comments()
        now = current_datetime()

        news = news_data.get(news_id)
        if news and not news.deleted and news.date <= now:
            news.comments.sort(key=lambda x: x.date)
            return news
        return None

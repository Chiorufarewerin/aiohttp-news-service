import datetime
from dataclasses import dataclass


@dataclass(slots=True)
class Comment:
    id: int
    news_id: int
    title: str
    date: datetime.datetime
    comment: str


@dataclass(slots=True)
class News:
    id: int
    title: str
    date: datetime.datetime
    body: str
    deleted: bool
    comments: list[Comment]

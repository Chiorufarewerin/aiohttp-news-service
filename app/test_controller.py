import pytest
import datetime

from app.models import News, Comment
from app.repository import Repository
from app.utils import format_date
from app.controller import Controller


def make_news(*, id, date, deleted=False):
    return {
        'id': id,
        'title': f'title_{id}',
        'date': format_date(date),
        'body': f'body_{id}',
        'deleted': deleted,
    }


def make_comment(*, id, news_id, date):
    return {
        'id': id,
        'news_id': news_id,
        'title': f'title_{id}',
        'date': format_date(date),
        'comment': f'comment_{id}'
    }


class MockRepository(Repository):
    def __init__(self):
        self.news = [
            make_news(id=4, date=datetime.datetime(2021, 1, 1)),
            make_news(id=2, date=datetime.datetime(2021, 1, 2), deleted=True),
            make_news(id=1, date=datetime.datetime(2022, 1, 2)),
            make_news(id=3, date=datetime.datetime(2022, 1, 1)),
            make_news(id=5, date=datetime.datetime(2021, 5, 1)),
        ]
        self.comments = [
            make_comment(id=3, news_id=4, date=datetime.datetime(2022, 1, 2)),
            make_comment(id=2, news_id=2, date=datetime.datetime(2022, 1, 1)),
            make_comment(id=1, news_id=4, date=datetime.datetime(2022, 1, 1)),
        ]

    async def fetch_news(self):
        return self.news

    async def fetch_comments(self):
        return self.comments


@pytest.fixture(autouse=True)
def mock_now(mocker):
    mocker.patch('app.controller.current_datetime', return_value=datetime.datetime(2022, 1, 1))


@pytest.fixture(autouse=True)
def mock_repository(mocker):
    mocker.patch('app.controller.JSONRepository', return_value=MockRepository())


async def test_fetch_news_list():
    controller = Controller()
    assert await controller.fetch_news_list() == [
        News(
            id=4,
            title='title_4',
            date=datetime.datetime(2021, 1, 1, 0, 0),
            body='body_4',
            deleted=False,
            comments=[
                # Комментарии могут быть не отсортированы
                # Так как и не требуется при получении всех новостей
                Comment(
                    id=3,
                    news_id=4,
                    title='title_3',
                    date=datetime.datetime(2022, 1, 2, 0, 0),
                    comment='comment_3',
                ),
                Comment(
                    id=1,
                    news_id=4,
                    title='title_1',
                    date=datetime.datetime(2022, 1, 1, 0, 0),
                    comment='comment_1',
                ),
            ],
        ),
        News(
            id=5,
            title='title_5',
            date=datetime.datetime(2021, 5, 1, 0, 0),
            body='body_5',
            deleted=False,
            comments=[]
        ),
        News(
            id=3,
            title='title_3',
            date=datetime.datetime(2022, 1, 1, 0, 0),
            body='body_3',
            deleted=False,
            comments=[]
        ),
    ]


async def test_get_news_with_comments():
    controller = Controller()
    assert await controller.get_news(4) == News(
        id=4,
        title='title_4',
        date=datetime.datetime(2021, 1, 1, 0, 0),
        body='body_4',
        deleted=False,
        comments=[
            # А тут уже сортируются
            Comment(
                id=1,
                news_id=4,
                title='title_1',
                date=datetime.datetime(2022, 1, 1, 0, 0),
                comment='comment_1',
            ),
            Comment(
                id=3,
                news_id=4,
                title='title_3',
                date=datetime.datetime(2022, 1, 2, 0, 0),
                comment='comment_3',
            ),
        ],
    )


async def test_get_news_without_comments():
    controller = Controller()
    assert await controller.get_news(3) == News(
        id=3,
        title='title_3',
        date=datetime.datetime(2022, 1, 1, 0, 0),
        body='body_3',
        deleted=False,
        comments=[]
    )


async def test_get_news_deleted():
    controller = Controller()
    assert await controller.get_news(2) is None


async def test_get_news_future_date():
    controller = Controller()
    assert await controller.get_news(1) is None

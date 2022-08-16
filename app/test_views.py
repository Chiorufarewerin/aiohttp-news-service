import pytest
import datetime
from aiohttp import web

from app.models import News, Comment
from app.views import routes
from app.middlewares import error_middleware


class MockController:
    async def fetch_news_list(self):
        return [
            News(
                id=1,
                title='test_1',
                date=datetime.datetime.fromisoformat('2019-01-02T21:58:25'),
                body='test test 1',
                deleted=False,
                comments=[
                    Comment(
                        id=1,
                        news_id=1,
                        title='comment 1',
                        date=datetime.datetime.fromisoformat('2019-01-02T21:58:25'),
                        comment='hello',
                    ),
                ],
            ),
        ]

    async def get_news(self, news_id: int):
        if news_id == 1:
            return News(
                id=1,
                title='test_1',
                date=datetime.datetime.fromisoformat('2019-01-02T21:58:25'),
                body='test test 1',
                deleted=False,
                comments=[
                    Comment(
                        id=1,
                        news_id=1,
                        title='comment 1',
                        date=datetime.datetime.fromisoformat('2019-01-02T21:58:25'),
                        comment='hello',
                    ),
                ],
            )
        return None


@pytest.fixture(autouse=True)
def mock_controller(mocker):
    mocker.patch('app.views.Controller', return_value=MockController())


async def test_news_list(aiohttp_client):
    app = web.Application(middlewares=[error_middleware])
    app.router.add_routes(routes)
    client = await aiohttp_client(app)
    response = await client.get('/')
    assert response.status == 200
    assert await response.json() == {
        'news': [
            {
                'id': 1,
                'title': 'test_1',
                'date': '2019-01-02T21:58:25',
                'body': 'test test 1',
                'deleted': False,
                'comments_count': 1
            },
        ],
        'news_count': 1,
    }


async def test_news_detail(aiohttp_client):
    app = web.Application(middlewares=[error_middleware])
    app.router.add_routes(routes)
    client = await aiohttp_client(app)
    response = await client.get('/news/1')
    assert response.status == 200
    assert await response.json() == {
        'id': 1,
        'title': 'test_1',
        'date': '2019-01-02T21:58:25',
        'body': 'test test 1',
        'deleted': False,
        'comments': [
            {
                'id': 1,
                'news_id': 1,
                'title': 'comment 1',
                'date': '2019-01-02T21:58:25',
                'comment': 'hello',
            },
        ],
        'comments_count': 1,
    }


async def test_news_detail_not_found(aiohttp_client):
    app = web.Application(middlewares=[error_middleware])
    app.router.add_routes(routes)
    client = await aiohttp_client(app)
    response = await client.get('/news/2')
    assert response.status == 404
    assert await response.json() == {'error': 'Not found'}


async def test_news_detail_incorrect_id(aiohttp_client):
    app = web.Application(middlewares=[error_middleware])
    app.router.add_routes(routes)
    client = await aiohttp_client(app)
    response = await client.get('/news/test')
    assert response.status == 404
    assert await response.json() == {'error': 'Not found'}

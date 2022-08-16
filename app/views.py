import ujson
from aiohttp import web

from .controller import Controller
from .utils import format_date

routes = web.RouteTableDef()


@routes.get('/')
async def news_list(request: web.Request) -> web.Response:
    controller = Controller()
    news_list = await controller.fetch_news_list()

    data = {
        'news': [
            {
                'id': news.id,
                'title': news.title,
                'date': format_date(news.date),
                'body': news.body,
                'deleted': news.deleted,
                'comments_count': len(news.comments),
            }
            for news in news_list
        ],
        'news_count': len(news_list)
    }

    return web.json_response(data, dumps=ujson.dumps)


@routes.get('/news/{news_id:\\d+}')
async def news_detail(request: web.Request) -> web.Response:
    controller = Controller()
    news = await controller.get_news(int(request.match_info['news_id']))

    if news:
        data = {
            'id': news.id,
            'title': news.title,
            'date': format_date(news.date),
            'body': news.body,
            'deleted': news.deleted,
            'comments': [
                {
                    'id': comment.id,
                    'news_id': comment.news_id,
                    'title': comment.title,
                    'date': format_date(comment.date),
                    'comment': comment.comment,
                }
                for comment in news.comments
            ],
            'comments_count': len(news.comments),
        }
        return web.json_response(data, dumps=ujson.dumps)

    return web.json_response({'error': 'Not found'}, dumps=ujson.dumps, status=404)

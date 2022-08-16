import ujson
import logging
from typing import Awaitable, Callable
from aiohttp import web


logger = logging.getLogger(__name__)


@web.middleware
async def error_middleware(request: web.Request,
                           handler: Callable[[web.Request], Awaitable[web.Response]]) -> web.Response:
    try:
        return await handler(request)
    except web.HTTPNotFound:
        return web.json_response({'error': 'Not found'}, dumps=ujson.dumps, status=404)
    except Exception:
        logger.exception('Unexpected error')

    return web.json_response({'error': 'System error'}, dumps=ujson.dumps, status=500)

from aiohttp import web

from app.views import routes
from app.middlewares import error_middleware


def main():
    app = web.Application(middlewares=[error_middleware])
    app.add_routes(routes)
    web.run_app(app)


if __name__ == '__main__':
    main()

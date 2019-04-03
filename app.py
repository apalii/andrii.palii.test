import logging

from aiohttp import web
from aiohttp_cache import cache, setup_cache

from utils import WebClient, Parser

# Constants
DAY = 60 * 60 * 24

# Routes
routes = web.RouteTableDef()

# Logging
logging.basicConfig(level=logging.DEBUG)


async def init_web_client(app):
    """
    From the docs:
    Don’t create a session per request.
    Most likely you need a session per application which performs all requests altogether.
    """
    app['web_client'] = WebClient()
    yield
    await app['web_client'].close()


@cache(expires=DAY)
@routes.get('/games', name='games')
async def get_games(request):
    # Endpoint in functional style
    category = request.query.get('category', None)
    web_client = request.app['web_client']
    url = 'https://play.google.com/store/apps/category/GAME'
    raw_data = await web_client.get(url, data_type='text')
    parser = Parser(data=raw_data)
    data = parser.get_json()
    if category in data.keys():
        return web.json_response(data[category])
    return web.json_response(data)


@cache(expires=DAY)
@routes.view('/cbv_games')
class GamesView(web.View):
    """
    Endpoint in CBV style
    https://aiohttp.readthedocs.io/en/stable/web_quickstart.html#class-based-views
    """
    async def get(self):
        category = self.request.query.get('category', None)
        web_client = self.request.app['web_client']
        url = 'https://play.google.com/store/apps/category/GAME'
        raw_data = await web_client.get(url, data_type='text')
        parser = Parser(data=raw_data)
        data = parser.get_json()
        if category in data.keys():
            return web.json_response(data[category])
        return web.json_response(data)


# Creating the app
app = web.Application()
app.cleanup_ctx.append(init_web_client)
app.add_routes(routes)
setup_cache(app)
web.run_app(app, host='127.0.0.1', port=5000)

from sanic import Sanic
from .listeners import init_listeners
from .task import init_task
from .urls import init_routes
from .cache import init_cache

app = Sanic()


def init_app():
    init_cache(app)
    init_routes(app)
    init_listeners(app)
    init_task(app)
    return app

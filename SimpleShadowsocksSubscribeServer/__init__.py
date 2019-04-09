from sanic import Sanic
from .urls import init_routes
from .listeners import init_listeners

app = Sanic()


def init_app():
    init_routes(app)
    init_listeners(app)
    return app

from sanic import Sanic

from .listeners import init_listeners
from .task import init_task
from .urls import init_routes

app = Sanic()


def init_app():
    init_routes(app)
    init_listeners(app)
    init_task(app)
    return app

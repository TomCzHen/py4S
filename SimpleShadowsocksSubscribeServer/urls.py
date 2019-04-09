from sanic import Sanic
from .views import SubscribeView


def init_routes(app: Sanic):
    app.add_route(SubscribeView.as_view(), '/subscribe/<uid:uuid>', methods=['GET'])

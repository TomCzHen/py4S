import uuid

from sanic import response
from sanic.exceptions import abort
from sanic.request import Request
from sanic.views import HTTPMethodView as SanicHTTPView

from ..cache import cache


class SubscribeView(SanicHTTPView):

    async def get(self, request: Request, uid: uuid):
        token = request.args.get('token')
        num = request.args.get('max', '99')

        try:
            num = float(num)
        except ValueError:
            num = 0
        else:
            num = int(num)

        subscribe = await cache.get(key=str(uid)) or abort(404)

        accept_contents = request.headers.get('accept').split(',')

        if 'text/html' in accept_contents:
            abort(404)

        if subscribe.token == token:
            subscribe_file = await subscribe.output_file(num)
            return response.raw(
                subscribe_file,
                content_type='application/octet-stream; charset=utf-8',
                headers={"Content-Disposition": f"attachment; filename={uid}.txt"}
            )
        else:
            abort(404)

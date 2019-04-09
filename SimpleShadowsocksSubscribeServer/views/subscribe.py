import base64

from sanic import response
from sanic.exceptions import abort
from sanic.request import Request
from sanic.views import HTTPMethodView as SanicHTTPView

from ..exts import cache
from ..models import Shadowsocks


class SubscribeView(SanicHTTPView):

    async def get(self, request: Request, uid: str):
        token = request.args.get('token')
        sub = await cache.get(key=str(uid), default=dict())
        print(request.headers.get('accept'))
        accept_contents = request.headers.get('accept').split(',')
        if 'text/html' in accept_contents:
            abort(404)
        if sub.get('token', '') == token:
            encoded_uri_list = list()
            for _ in sub.get('shadowsocks'):
                encoded_uri_list.append(Shadowsocks(**_).encoded_uri)
            encoded_uri_text = "\n".join(encoded_uri_list)
            print(encoded_uri_text)
            subscribe_file = base64.urlsafe_b64encode(encoded_uri_text.encode('utf-8'))
            return response.raw(
                subscribe_file,
                content_type='application/octet-stream; charset=utf-8',
                headers={"Content-Disposition": f"attachment; filename={uid}.txt"}
            )
        else:
            abort(404)

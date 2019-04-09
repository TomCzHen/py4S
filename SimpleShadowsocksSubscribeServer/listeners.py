import toml
from aiofiles import open as aio_open
from sanic import Sanic

from .exts import cache
from .settings import SHADOWSOCKS_TOML_PATH


async def load_subscribe_data(app, loop):
    async with aio_open(SHADOWSOCKS_TOML_PATH) as f:
        toml_content = await f.read()
    data = toml.loads(toml_content)
    for _k, _v in data.items():
        await cache.set(key=_k, value=_v)


def init_listeners(app: Sanic):
    app.register_listener(load_subscribe_data, 'before_server_start')

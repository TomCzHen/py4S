import toml
from aiofiles import open as aio_open
from sanic import Sanic
from typing import NamedTuple, Tuple
from .exts import cache
from .models import SubscribeSchema
from .settings import CONFIG_PATH, SUBSCRIBE_PATH

Config = NamedTuple('Config', [('allowed_ua', Tuple[str])])


async def load_subscribe(app, loop):
    async with aio_open(SUBSCRIBE_PATH) as f:
        content = await f.read()

    toml_data = toml.loads(content)
    subscribes_data = toml_data['subscribe']

    for subscribe_data in subscribes_data:
        subscribe_schema = SubscribeSchema()
        subscribe = subscribe_schema.load(subscribe_data).data
        await cache.set(key=subscribe.uid, value=subscribe)


async def load_config(app, loop):
    async with aio_open(CONFIG_PATH) as f:
        content = await f.read()
    config_data = toml.loads(content)
    config = Config(config_data)
    await cache.set(key='config', value=config)


def init_listeners(app: Sanic):
    app.register_listener(load_config, 'before_server_start')
    app.register_listener(load_subscribe, 'before_server_start')

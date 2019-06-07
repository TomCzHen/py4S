import asyncio

from sanic import Sanic
from sanic.log import logger

from .cache import load_subscribe, load_config
from .settings import CONFIG_FILE, SUBSCRIBE_FILE
from .utils import config_watcher


async def watch_config_dir_filesystem_event(app: Sanic):
    event_funcs = {
        SUBSCRIBE_FILE.name: load_subscribe,
        CONFIG_FILE.name: load_config
    }

    await config_watcher.setup(app.loop)

    while True:
        event = await config_watcher.get_event()
        func = event_funcs.get(event.name)
        if func:
            try:
                logger.info(f"Get {event.name} changed event.")
                await func(app)
            except FileNotFoundError:
                logger.warn('File {event.name} not Found.')
                pass
        else:
            await asyncio.sleep(1)


def init_task(app: Sanic):
    app.add_task(watch_config_dir_filesystem_event)

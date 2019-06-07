from sanic import Sanic
from sanic.log import logger
from .cache import load_subscribe, load_config
from .utils import config_watcher
from .settings import CONFIG_FILE, SUBSCRIBE_FILE


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
            await func(app)


def init_task(app: Sanic):
    app.add_task(watch_config_dir_filesystem_event)

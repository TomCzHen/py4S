import asyncio
import hashlib
from typing import NamedTuple, Tuple

import toml
from aiocache import SimpleMemoryCache as Cache
from aiocache.lock import OptimisticLock, OptimisticLockError
from sanic import Sanic
from sanic.log import logger

from .models import SubscribeSchema, Subscribe
from .settings import CONFIG_FILE, SUBSCRIBE_FILE
from .utils import aio_open

cache = Cache()

Config = NamedTuple('Config', [('allowed_ua', Tuple[str])])


class InitCacheException(Exception):
    def __init__(self, **kwargs):
        pass


async def load_subscribe(app: Sanic):
    async with aio_open(SUBSCRIBE_FILE) as f:
        content = await f.read()

    toml_data = toml.loads(content)
    subscribes_data = toml_data['subscribe']
    for subscribe_data in subscribes_data:

        cache_digest = ''
        digest = await hash_content(str(subscribe_data))
        subscribe_data['digest'] = digest
        logger.debug(subscribe_data)

        cache_subscribe: Subscribe = await cache.get(subscribe_data.get('uid'))

        if cache_subscribe:
            cache_digest = cache_subscribe.digest
        async with OptimisticLock(cache, subscribe_data.get('uid')) as lock:
            if digest == cache_digest:
                pass
            else:
                subscribe_schema = SubscribeSchema()
                result = subscribe_schema.load(subscribe_data)

                if result.errors:
                    logger.warn(f"[Load Subscribes] {result.errors}")
                else:
                    subscribe = result.data
                    try:
                        await lock.cas(subscribe)
                    except OptimisticLockError:
                        pass


async def load_config(app: Sanic):
    async with aio_open(CONFIG_FILE) as f:
        content = await f.read()

    async with OptimisticLock(cache, 'config') as lock:
        config_data = toml.loads(content)

        digest = await hash_content(content)
        cache_digest = ""
        config_data['digest'] = digest

        logger.debug(config_data)

        cache_config: dict = await cache.get('config')
        if cache_config:
            cache_digest = cache_config.get('digest')
        try:
            if cache_digest == digest:
                pass
            else:
                await lock.cas(config_data)
        except OptimisticLockError:
            pass


async def hash_content(content: str):
    md5 = hashlib.md5()
    md5.update(content.encode('utf-8'))
    return str(md5.hexdigest())


def init_cache(app: Sanic):
    asyncio.run(load_subscribe(app))
    asyncio.run(load_config(app))

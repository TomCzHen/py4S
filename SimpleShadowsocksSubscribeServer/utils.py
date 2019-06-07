import asyncio
import base64
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import aionotify
import toml
from aiofiles import open as aio_open

from .settings import CONFIG_DIR

config_watcher = aionotify.Watcher()

watch_flags = aionotify.Flags.MODIFY | aionotify.Flags.CREATE | aionotify.Flags.DELETE | aionotify.Flags.MOVED_FROM | aionotify.Flags.MOVED_TO

config_watcher.watch(
    path=str(CONFIG_DIR),
    flags=watch_flags,
    alias='config_dir'
)


async def aio_toml_loads(file_path: Path, pool: ThreadPoolExecutor = None) -> dict:
    async with aio_open(file_path) as file:
        content = await file.read()
    loop = asyncio.get_running_loop()
    data = await loop.run_in_executor(
        pool,
        toml.loads,
        content
    )

    return data


async def aio_base64_urlsafe_encode(string: str, encoding='utf-8', pool: ThreadPoolExecutor = None) -> bytes:
    loop = asyncio.get_event_loop()
    string_bytes = string.encode(encoding=encoding)
    encode_bytes: bytes = await loop.run_in_executor(
        pool,
        base64.urlsafe_b64encode,
        string_bytes
    )

    return encode_bytes

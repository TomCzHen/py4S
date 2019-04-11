import asyncio
import base64
from unittest import TestCase

from SimpleShadowsocksSubscribeServer.models import SubscribeSchema, Subscribe
from SimpleShadowsocksSubscribeServer.utils import aio_toml_loads, aio_base64_urlsafe_encode
from test import SHADOWSOCKS_PATH


class TestSubscribe(TestCase):
    toml_content: dict = asyncio.run(aio_toml_loads(SHADOWSOCKS_PATH))
    subscribe_uid = '82bce78f-a084-48ac-9cbf-47693e0d0945'
    subscribe_content = toml_content.get(subscribe_uid)
    subscribe_schema = SubscribeSchema()
    subscribe: Subscribe = subscribe_schema.load(subscribe_content).data

    def test_subscribe_shadowsocks(self):
        shadowsocks_uri_list = [
            f"ss://{s['method']}:{s['password']}@{s['server']}:{s['server_port']}#{s['remark']}"
            for s in self.subscribe_content['shadowsocks']
        ]
        self.assertEqual(len(self.subscribe.shadowsocks), len(shadowsocks_uri_list))

        self.assertListEqual(
            [s.uri for s in self.subscribe.shadowsocks],
            shadowsocks_uri_list

        )

    def test_aio_base64_urlsafe_encode(self):
        plain_text = 'test_plain_text'
        self.assertEqual(
            base64.urlsafe_b64encode(plain_text.encode('utf-8')),
            asyncio.run(aio_base64_urlsafe_encode(plain_text))
        )

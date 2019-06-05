import asyncio
import base64
from unittest import TestCase
from typing import List
from SimpleShadowsocksSubscribeServer.models import SubscribeSchema, Subscribe
from SimpleShadowsocksSubscribeServer.utils import aio_toml_loads, aio_base64_urlsafe_encode
from test import SUBSCRIBE_PATH


class TestSubscribe(TestCase):
    toml_content: dict = asyncio.run(aio_toml_loads(SUBSCRIBE_PATH))
    subscribes_toml = toml_content.get('subscribe')

    def test_subscribe_shadowsocks(self):
        subscribes: List[Subscribe] = [SubscribeSchema().load(_).data for _ in self.subscribes_toml]
        subscribes_dict = {s['uid']: {'token': s['token'], 'shadowsocks': s['shadowsocks']} for s in
                           self.subscribes_toml}
        for subscribe in subscribes:
            subscribe_dict = subscribes_dict[subscribe.uid]

            shadowsocks_uri_list = [
                f"ss://{s['method']}:{s['password']}@{s['server']}:{s['server_port']}#{s['remark']}"
                for s in subscribe_dict['shadowsocks']
            ]
            self.assertEqual(len(subscribe.shadowsocks), len(shadowsocks_uri_list))

            self.assertListEqual(
                [s.uri for s in subscribe.shadowsocks],
                shadowsocks_uri_list
            )

    def test_aio_base64_urlsafe_encode(self):
        plain_text = 'test_plain_text'
        self.assertEqual(
            base64.urlsafe_b64encode(plain_text.encode('utf-8')),
            asyncio.run(aio_base64_urlsafe_encode(plain_text))
        )

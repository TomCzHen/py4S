from typing import List

from marshmallow import Schema, fields, post_load

from .shadowsocks import Shadowsocks, ShadowsocksSchema
from ..utils import aio_base64_urlsafe_encode
import random


class SubscribeSchema(Schema):
    uid = fields.UUID(required=True)
    token = fields.Str(required=True)
    shadowsocks = fields.List(fields.Nested(ShadowsocksSchema))
    digest = fields.Str(required=True)

    @post_load
    def make_subscribe(self, data):
        return Subscribe(**data)


class Subscribe:
    def __init__(self, uid, token, shadowsocks: List[Shadowsocks], digest):
        self.uid = uid
        self.token = token
        self.shadowsocks = shadowsocks
        self.digest = digest

    async def output_file(self, num: int):
        num = 99 if num == 0 else num
        if num < len(self.shadowsocks):
            random.shuffle(self.shadowsocks)

        subscribe_file = await aio_base64_urlsafe_encode(
            "\n".join([s.encoded_uri for s in self.shadowsocks[:num]]),
            'utf-8'
        )
        return subscribe_file

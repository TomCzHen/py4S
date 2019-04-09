from typing import List

from .shadowsocks import ShadowsocksServer, ShadowsocksServerSchema
from marshmallow import Schema, fields


class SubscribeSchema(Schema):
    uid = fields.Str()
    token = fields.Str()
    shadowsocks = fields.List(fields.Nested(ShadowsocksServerSchema))


class Subscribe:
    def __init__(self, uid, token, shadowsocks: List[Shadowsocks]):
        self.uid = uid
        self.token = token
        self.shadowsocks_server = shadowsocks

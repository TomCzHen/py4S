import asyncio
import base64

from marshmallow import Schema, fields, post_load

from ..utils import aio_base64_urlsafe_encode


class ShadowsocksSchema(Schema):
    host = fields.Str(load_from='server', attribute='server')
    port = fields.Int(load_from='server_port', attribute='server_port')
    method = fields.Str()
    password = fields.Str()
    remark = fields.Str()

    @post_load
    def make_shadowsocks(self, data):
        return Shadowsocks(**data)


class Shadowsocks:
    def __init__(self, server: str, server_port: int, method: str, password: str, remark: str):
        self._host = server
        self._port = server_port
        self._method = method
        self._password = password
        self._remark = remark

    def __str__(self):
        return self.uri

    @classmethod
    async def aio_create(cls, **kwargs):
        loop = asyncio.get_event_loop()

        obj: Shadowsocks = await loop.run_in_executor(
            None,
            cls,
            *kwargs
        )
        obj.encoded_hierarchical_part = await aio_base64_urlsafe_encode(obj.hierarchical_part, 'utf-8')
        return obj

    @property
    def scheme(self) -> str:
        return "ss"

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def method(self) -> str:
        return self._method

    @property
    def password(self) -> str:
        return self._password

    @property
    def remark(self) -> str:
        return self._remark

    @property
    def uri(self) -> str:
        return f'{self.scheme}://{self.hierarchical_part}#{self}'

    @property
    def hierarchical_part(self) -> str:
        return f'{self.method}:{self.password}@{self.host}:{self.port}'

    @property
    def encoded_uri(self) -> str:
        encoded_hierarchical_part = base64.urlsafe_b64encode(self.hierarchical_part.encode('utf-8')).decode('utf-8')
        return f'{self.scheme}://{encoded_hierarchical_part}#{self.remark}'

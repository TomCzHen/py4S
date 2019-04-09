import base64

from marshmallow import Schema, fields


class ShadowsocksSchema(Schema):
    host = fields.Str(attribute='server')
    port = fields.Int(attribute='server_port')
    method = fields.Str()
    password = fields.Str()
    remark = fields.Str()


class Shadowsocks:
    def __init__(self, server: str, server_port: int, method: str, password: str, remark: str):
        self.host = server
        self.port = server_port
        self.method = method
        self.password = password
        self._remark = remark

    def __str__(self):
        return self._remark

    @property
    def scheme(self):
        return "ss"

    @property
    def plain_uri(self):
        return f'{self.scheme}://{self.hierarchical_part}#{self}'

    @property
    def encoded_uri(self):
        return f'{self.scheme}://{self.encoded_hierarchical_part}#{self}'

    @property
    def hierarchical_part(self):
        return f'{self.method}:{self.password}@{self.host}:{self.port}'

    @property
    def encoded_hierarchical_part(self):
        return base64.urlsafe_b64encode(self.hierarchical_part.encode('utf-8')).decode('utf-8')

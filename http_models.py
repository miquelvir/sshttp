from dataclasses import dataclass
from typing import Dict
import json


class HttpMethod:
    OPTIONS = "OPTIONS"
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    TRACE = "TRACE"
    CONNECT = "CONNECT"
    PATCH = "PATCH"


@dataclass
class HttpRequest:
    method: str
    uri: str
    version: str
    headers: Dict[str, str]
    body: bytearray

    @property
    def json(self):
        return json.loads(self.body)


@dataclass
class HttpResponse:
    status_code: int
    reason_phrase: str
    version: str
    headers: Dict[str, str]
    body: bytearray

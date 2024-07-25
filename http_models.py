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
    body: str

    @property
    def json(self):
        return json.loads(self.body)

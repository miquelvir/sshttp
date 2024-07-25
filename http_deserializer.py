from http_models import HttpRequest
import logging
from typing import Dict


EOL = "\r\n"
EOL_BYTES = EOL.encode()
WS = " "

def deserialize_request(request: str) -> HttpRequest:
    lines = request.splitlines(keepends=True)
    request_line, *lines = lines

    # parse request line
    method, uri, version, *_ = request_line.strip(EOL).split(WS, 2)

    # parse message headers
    last_header_line = None
    headers: Dict[str, str] = {}
    for i, line in enumerate(lines):
        if line == "\r\n":
            last_header_line = i
            break
        key, value = line.strip(EOL).split(":", 1)
        stripped_value = value.lstrip(WS)
        if key not in headers:
            headers[key] = stripped_value
        else:
            headers[key] = f"{headers[key]},{stripped_value}"

    # parse message body
    body = ""
    if last_header_line is not None:
        for line in lines[last_header_line+1:]:
            body += line
    
    return HttpRequest(
        method=method,
        uri=uri,
        version=version,
        headers=headers,
        body=body
    )



class HttpRequestDeserializer:
    _READING_REQUEST_LINE_STATE = 0
    _READING_HEADERS_LINE_STATE = 1
    _READING_BODY_STATE = 2
    _DONE_STATE = 3
    
    def __init__(self) -> None:
        self.state = self._READING_REQUEST_LINE_STATE
        self.buffer = bytearray()
        self.method = None
        self.uri = None
        self.version = None
        self.headers = {}
        self.body = bytearray()
        self.body_bytes_to_read = 0
    
    def _parse_request_line(self, chunk: bytearray):
        request_line = chunk.decode()
        method, uri, version, *_ = request_line.strip(EOL).split(WS, 2)
        self.method = method
        self.uri = uri
        self.version = version
        self.state = self._READING_HEADERS_LINE_STATE
    
    def _parse_headers_line(self, chunk: bytearray):
        header_line = chunk.decode()
        if header_line == "\r\n":
            self.state = self._READING_BODY_STATE
            self.body_bytes_to_read = int(self.headers.get('Content-Length', 0))
            return
        
        key, value = header_line.strip(EOL).split(":", 1)
        stripped_value = value.lstrip(WS)
        if key not in self.headers:
            self.headers[key] = stripped_value
        else:
            self.headers[key] = f"{self.headers[key]},{stripped_value}"

    def _parse_body(self, chunk: bytearray):
        self.body.extend(chunk)
        self.body_bytes_to_read -= len(chunk)
        if self.body_bytes_to_read <= 0:
            self.state = self._DONE_STATE

    def _parse(self, chunk: bytearray):
        if self.state == self._READING_REQUEST_LINE_STATE:
            self._parse_request_line(chunk)
            
        elif self.state == self._READING_HEADERS_LINE_STATE:
            self._parse_headers_line(chunk)
            
        elif self.state == self._READING_BODY_STATE:
            self._parse_body(chunk)

    def next(self, chunk: bytearray):
        self.buffer.extend(chunk)

        if self.state != self._READING_BODY_STATE:
            last_parsed = 0
            last_read = 0
            while last_read < len(self.buffer) - 1:
                if self.buffer[last_read:last_read+2] == EOL_BYTES:
                    line = self.buffer[last_parsed:last_read+2]
                    last_parsed = last_read + 2
                    self._parse(line)
                    if self.state == self._READING_BODY_STATE:
                        break
                    last_read += 1
                last_read += 1
            self.buffer = self.buffer[last_parsed:]

        if self.state == self._READING_BODY_STATE:
            self._parse(self.buffer)
            self.buffer = bytearray()
        
        return not self.is_done()
    
    def is_done(self) -> bool:
        return self.state == self._DONE_STATE

    def to_request(self) -> HttpRequest:
        return HttpRequest(
            method=self.method,
            uri=self.uri,
            version=self.version,
            headers=self.headers,
            body=self.body
        )
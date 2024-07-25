from http_models import HttpRequest
import logging
from typing import Dict


EOL = "\r\n"
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

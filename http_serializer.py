from http_models import HttpResponse


ENCODING = "unicode_escape"


def serialize_response(response: HttpResponse) -> bytearray:
    buffer = bytearray()

    # status line
    status_line = f"{response.version} {response.status_code} {response.reason_phrase}\r\n"
    status_line_bytes = status_line.encode()
    buffer.extend(status_line_bytes)
    
    # headers
    for key, value in response.headers.items():
        buffer.extend(f"{key}: {value}\r\n".encode())
    if "Content-Length" not in response.headers:
        buffer.extend(f"Content-Length: {len(response.body)}\r\n".encode())
    buffer.extend("\r\n".encode())

    # body
    buffer.extend(response.body)

    return buffer

import socket
import logging
from http_deserializer import HttpRequestDeserializer
from http_models import HttpMethod, HttpRequest, HttpResponse
from http_serializer import serialize_response
from datetime import datetime
import json
from concurrent.futures import ThreadPoolExecutor
from threading import get_ident


HOST = "127.0.0.1"
PORT = 8080
THREAD_POOL_SIZE = 5

def handle_conn(conn):
    with conn:
        deserializer = HttpRequestDeserializer()
        print(f"Connected by {addr}")
        
        # read request
        keep_reading = True
        while keep_reading:
            bytes_data = conn.recv(5)
            if not bytes_data:
                break
            text_data = bytes_data.decode()
            keep_reading = deserializer.next(text_data)
        req: HttpRequest = deserializer.to_request()
        print(req)

        res_body = json.dumps({
            "status": "ok",
            "time": str(datetime.now().time()),
            "thread": get_ident()
        })
        res: HttpResponse = HttpResponse(
            200,
            "OK",
            "HTTP/1.0",
            {
                "Content-Type": "application/json",
                "Content-Length": len(res_body)
            },
            res_body
        )
        print(res)

        res_bytes = serialize_response(res)
        print(res_bytes)

        conn.sendall(res_bytes)
        conn.close()


with ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE) as exe:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        
        try:
            while True:
                conn, addr = s.accept()
                exe.submit(handle_conn, conn)

        finally:
            s.close()

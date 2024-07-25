from http_deserializer import deserialize_request
from http_models import HttpMethod
import logging


def get_test_file(name: str) -> str:
    with open(f"test_data/{name}", newline='') as f:
        return f.read()
    

def test_deserialize_get():
    raw_request = get_test_file("get1")
    request = deserialize_request(raw_request)
    assert request.method == HttpMethod.GET
    assert request.uri == "http://www.w3.org/pub/WWW/TheProject.html"
    assert request.version == "HTTP/1.1"
    assert request.headers == {
        "Host": "www.w3.org",
        "Accept": "application/json",
        "Authorization": "Bearer mytoken123"
    }
    assert request.body == ""


def test_deserialize_get_repeated_headers():
    raw_request = get_test_file("get2")
    request = deserialize_request(raw_request)
    assert request.method == HttpMethod.GET
    assert request.uri == "http://www.w3.org/pub/WWW/TheProject.html"
    assert request.version == "HTTP/1.1"
    assert request.headers == {
        "Host": "www.w3.org",
        "Accept": "application/json",
        "Authorization": "Bearer mytoken123",
        "X-Custom-List-Header": "a,b,c"
    }
    assert request.body == ""


def test_deserialize_post():
    raw_request = get_test_file("post1")
    request = deserialize_request(raw_request)
    assert request.method == HttpMethod.POST
    assert request.uri == "http://www.w3.org/pub/WWW/TheProject.html"
    assert request.version == "HTTP/1.1"
    assert request.headers == {
        "Host": "www.w3.org",
        "Accept": "application/json",
        "Authorization": "Bearer mytoken123",
        "Content-Type": "application/json"
    }
    assert request.body == """{"my":"new","posted":"data"}"""
    assert request.json == {"my":"new","posted":"data"}

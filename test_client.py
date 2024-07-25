import requests
import json
from concurrent.futures import ThreadPoolExecutor

def do_request():
    res = requests.post("http://127.0.0.1:8080/v1", data=json.dumps({}))
    print(res.json())

with ThreadPoolExecutor(max_workers=100) as exe:
    for _ in range(1000):
        exe.submit(do_request)

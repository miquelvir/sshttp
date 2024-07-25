# Setup

```zsh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Running

```zsh
python3 http_server.py
```

```zsh
curl 127.0.0.1:8080/v1 -X POST -d '{"a":"nice","evening":"with marta"}' -H 'Content-Type: application/json' | jq
```

# Test

```zsh
pytest --log-cli-level
```
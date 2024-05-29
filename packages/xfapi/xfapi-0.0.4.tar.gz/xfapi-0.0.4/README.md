配置文件示例

```yaml
apis:
- name: "token"
  path: "/token"
  method: "POST"
  handler: "apis.handler_token"

- name: "p"
  path: "/p"
  method: "GET"
  handler: "apis.p"

```

回调函数示例

```python

from fastapi import Request
def handler_token(data:dict):
    print(data)
    return {"token": "your_token_here"}

def p(request:Request):
    print(request._query_params._dict)
    return {"data": "your_token_here"}
```


调用示例

```python
from xapi.server import HTTPServer

server = HTTPServer()

server.start()

```

调用成功 日志

```log
INFO:xapi.server:注册路由: /token POST -> apis.handler_token
INFO:xapi.server:注册路由: /p GET -> apis.p
INFO:     Started server process [27480]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

配置文件示例

```yaml
apis:
- name: "index"
  path: "/index"
  method: "Get"
  handler: "apis.index"

- name: "save"
  path: "/save"
  method: "POST"
  handler: "apis.save"

```

回调函数示例

```python
from fastapi import Request


def index(request:Request):
    print(request._query_params._dict)
    return {"msg": "this is index msg"}

def save(data:dict):
    return {"msg": "this is save msg", "data":data}
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
